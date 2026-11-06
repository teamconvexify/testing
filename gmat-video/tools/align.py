# -*- coding: utf-8 -*-
"""Sincroniza la letra (cues.py) con el audio usando faster-whisper por bloques.

1. Transcribe cada bloque de la canción con su letra como pista (initial_prompt) -> whisper_windows.json
2. Alinea palabra a palabra la letra con lo transcrito (difflib) e interpola lo que falte
3. Ajusta cada rótulo a la semicorchea más cercana (rejilla de beats de librosa) -> timing.json

uso: python tools/align.py <ruta_modelo_whisper> <audio_16k.wav> [--retranscribe]
"""
import difflib
import json
import os
import re
import sys
import unicodedata

from num2words import num2words

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cues import SONG  # noqa: E402

# (inicio, fin, primera línea, última línea) — bloques sacados de una primera pasada completa
WINDOWS = [
    (0.0, 16.6, 0, 6),
    (16.5, 47.5, 7, 25),
    (47.0, 56.0, 26, 29),
    (55.4, 79.0, 30, 37),
    (77.8, 105.2, 38, 48),
    (104.6, 131.3, 49, 60),
    (128.8, 155.0, 61, 71),
    (155.3, 164.6, 72, 75),
    (164.0, 177.6, 76, 80),
    (177.0, 196.0, 81, 87),
    (195.4, 212.0, 88, 92),
]
LEAD = 0.033      # el rótulo entra un fotograma antes de la sílaba
SNAP = 0.09       # distancia máxima para pegar a la semicorchea


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", w)


def expand(word):
    """palabra de whisper -> lista de tokens normalizados (las cifras se pasan a letra)."""
    n = norm(word)
    if not n:
        return []
    if n.isdigit():
        return [norm(t) for t in num2words(int(n), lang="es").split()]
    return [n]


def lyric_tokens(text):
    return [norm(w) for w in text.split() if norm(w)]


def transcribe(model_path, wav):
    import soundfile as sf
    from faster_whisper import WhisperModel
    a, sr = sf.read(wav, dtype="float32")
    m = WhisperModel(model_path, device="cpu", compute_type="int8", cpu_threads=4)
    out = []
    for s0, s1, l0, l1 in WINDOWS:
        prompt = " ".join(SONG[i]["text"] for i in range(l0, l1 + 1))
        prompt = re.sub(r"[()¡!¿?]", "", prompt)
        segs, _ = m.transcribe(a[int(s0 * sr):int(s1 * sr)], language="es", word_timestamps=True, beam_size=5,
                               vad_filter=False, condition_on_previous_text=False, initial_prompt=prompt,
                               no_speech_threshold=0.95)
        ws = [dict(w=w.word, s=round(w.start + s0, 3), e=round(w.end + s0, 3), p=round(w.probability, 3))
              for s in segs for w in (s.words or [])]
        out.append(dict(s0=s0, s1=s1, l0=l0, l1=l1, words=ws))
        print(f"{s0:6.1f}-{s1:6.1f}: " + " ".join(w["w"].strip() for w in ws), flush=True)
    return out


def beat_grid(wav):
    import librosa
    import numpy as np
    y, sr = librosa.load(wav, sr=22050, mono=True)
    _, beats = librosa.beat.beat_track(y=y, sr=sr, start_bpm=99, tightness=400, units="time")
    grid = []
    for a, b in zip(beats, beats[1:]):
        grid += [a + (b - a) * k / 4 for k in range(4)]
    grid.append(beats[-1])
    return np.array(grid)


def syllables(word):
    w = word.lower().replace("í", "-i-").replace("ú", "-u-")
    return max(1, len(re.findall(r"[aeiouáéóü]+", w)))


def fix_glued(words, s0):
    """Whisper estira hacia atrás la primera palabra tras una pausa: si una palabra empieza
    pegada a la anterior y dura más de lo que permiten sus sílabas, se recorta el inicio."""
    prev_end = s0
    for w in words:
        maxdur = 0.12 + 0.17 * syllables(w["w"])
        if w["s"] - prev_end <= 0.03 and w["e"] - w["s"] > maxdur:
            w["s"] = round(w["e"] - maxdur, 3)
        prev_end = w["e"]
    return words


def align_window(win):
    fix_glued(win["words"], win["s0"])
    toks, owner = [], []  # tokens de la letra y (línea, índice en línea)
    for li in range(win["l0"], win["l1"] + 1):
        for k, t in enumerate(lyric_tokens(SONG[li]["text"])):
            toks.append(t); owner.append((li, k))
    hyp, ht = [], []
    for w in win["words"]:
        ex = expand(w["w"])
        dur = max(w["e"] - w["s"], 0.01)
        for j, t in enumerate(ex):
            hyp.append(t); ht.append(w["s"] + dur * j / len(ex))
    times = [None] * len(toks)
    sm = difflib.SequenceMatcher(None, toks, hyp, autojunk=False)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            times[a + k] = ht[b + k]
    matched = sum(t is not None for t in times)
    # interpolar huecos
    idx = [i for i, t in enumerate(times) if t is not None]
    if not idx:
        raise SystemExit(f"sin coincidencias en bloque {win['s0']}")
    for i in range(len(times)):
        if times[i] is not None:
            continue
        prev = max([j for j in idx if j < i], default=None)
        nxt = min([j for j in idx if j > i], default=None)
        if prev is None:
            times[i] = max(win["s0"], times[nxt] - 0.25 * (nxt - i))
        elif nxt is None:
            times[i] = min(win["s1"], times[prev] + 0.25 * (i - prev))
        else:
            times[i] = times[prev] + (times[nxt] - times[prev]) * (i - prev) / (nxt - prev)
    # no permitir retrocesos
    for i in range(1, len(times)):
        times[i] = max(times[i], times[i - 1])
    per_line = {}
    for (li, k), t, ok in zip(owner, times, [x in idx for x in range(len(toks))]):
        per_line.setdefault(li, []).append((t, ok))
    return per_line, matched, len(toks)


def find(tokens, word, start):
    target = norm(word)
    for i in range(start, len(tokens)):
        if tokens[i] == target:
            return i
    raise SystemExit(f"no encuentro '{word}' en {tokens}")


def main():
    model, wav = sys.argv[1], sys.argv[2]
    cache = os.path.join(HERE, "whisper_windows.json")
    if "--retranscribe" in sys.argv or not os.path.exists(cache):
        json.dump(transcribe(model, wav), open(cache, "w"), ensure_ascii=False, indent=1)
    wins = json.load(open(cache))
    grid = beat_grid(wav)

    def snap(t):
        j = abs(grid - t).argmin()
        g = float(grid[j])
        return (g if abs(g - t) <= SNAP else t) - LEAD

    lines_t = {}
    for w in wins:
        per_line, matched, total = align_window(w)
        print(f"bloque {w['s0']:6.1f}-{w['s1']:6.1f}: {matched}/{total} palabras reconocidas")
        lines_t.update(per_line)

    out = []
    for li, line in enumerate(SONG):
        toks = lyric_tokens(line["text"])
        tt = lines_t[li]
        assert len(tt) == len(toks)
        pos, items = 0, []
        for it in line["items"]:
            i = find(toks, it["at"], pos)
            rec = {"at": round(max(0.0, snap(tt[i][0])), 3)}
            pos = i
            if it.get("reveal"):
                r = find(toks, it["reveal"], i + 1)
                rec["reveal"] = round(snap(tt[r][0]), 3)
                pos = r
            items.append(rec)
        if li == 0:
            items[0]["at"] = 0.0
        start = items[0]["at"] if li else 0.0
        end = tt[-1][0] + 0.45
        out.append(dict(start=round(min(start, tt[0][0]), 3), end=round(end, 3), items=items,
                        unmatched=[toks[k] for k, (t, ok) in enumerate(tt) if not ok]))
    json.dump(dict(lines=out), open(os.path.join(HERE, "timing.json"), "w"), ensure_ascii=False, indent=1)
    for li, (line, o) in enumerate(zip(SONG, out)):
        its = " ".join(f"{x['at']:.2f}" + (f"/{x['reveal']:.2f}" if 'reveal' in x else "") for x in o["items"])
        miss = f"   (sin oír: {' '.join(o['unmatched'])})" if o["unmatched"] else ""
        print(f"{li:3d} {o['start']:7.2f} {line['text'][:46]:46s} {its}{miss}")


if __name__ == "__main__":
    main()
