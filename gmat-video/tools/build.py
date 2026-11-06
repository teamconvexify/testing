# -*- coding: utf-8 -*-
"""Genera index.html (composición HyperFrames) a partir de cues.py + timing.json.

python3 tools/build.py            -> usa timing.json (sale de align.py)
"""
import html
import json
import os
import re
import sys

from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cues import SONG  # noqa: E402

W, H, FPS = 1920, 1080, 30
DURATION = 212.04
AUDIO = "assets/cuadrado-cubo-raiz.mp3"

# Paleta de la hoja: rotulador rosa, boli verde azulado, boli granate, fluorescente amarillo
COLORS = {
    "pink": ("#E4479A", 0.20),
    "teal": ("#0E8A8C", 0.20),
    "wine": ("#A3164F", 0.2),
    "gold": ("#F0B000", 0.34),
}
INK = "#1A1918"
PAPER = "#FBF7EE"


# ── Métricas de fuente (para centrar y encajar sin medir en el navegador) ──
class Metrics:
    def __init__(self, path, wght):
        f = TTFont(path)
        if "fvar" in f:
            f = instancer.instantiateVariableFont(f, {"wght": wght})
        self.upm = f["head"].unitsPerEm
        self.cmap = f.getBestCmap()
        self.hmtx = f["hmtx"]
        os2 = f["OS/2"]
        if os2.fsSelection & (1 << 7):
            asc, desc = os2.sTypoAscender, -os2.sTypoDescender
        else:
            asc, desc = f["hhea"].ascent, -f["hhea"].descent
        self.asc, self.desc = asc / self.upm, desc / self.upm
        self.cap = os2.sCapHeight / self.upm
        self.xh = os2.sxHeight / self.upm

    def width(self, s):
        w = 0
        for ch in s:
            g = self.cmap.get(ord(ch)) or self.cmap.get(ord("0"))
            w += self.hmtx[g][0]
        return w / self.upm

    def center_shift(self):
        """em que hay que bajar la caja (line-height:1) para que las cifras queden centradas."""
        half_lead = (1 - (self.asc + self.desc)) / 2
        baseline = half_lead + self.asc
        digit_center = baseline - self.cap / 2
        return 0.5 - digit_center


FONTS = os.path.join(ROOT, "assets", "fonts")
M_BG = Metrics(os.path.join(FONTS, "fredoka.woff2"), 700)
M_FG = Metrics(os.path.join(FONTS, "rubik.woff2"), 600)
M_WORD = Metrics(os.path.join(FONTS, "rubik.woff2"), 700)
M_NOTE = Metrics(os.path.join(FONTS, "caveat.woff2"), 700)

SUP = 0.56     # tamaño del exponente
RAD_W = 0.56   # ancho del signo radical
ARROW_W = 0.95
HEART_W = 1.0


# ── Parser del marcado ─────────────────────────────────────────────────────
def parse(s):
    """Devuelve lista de tokens (kind, text, hl, ans)."""
    toks, i, hl, ans = [], 0, False, False
    while i < len(s):
        c = s[i]
        if c == "|":
            ans = True; i += 1; continue
        if c == "[":
            hl = True; i += 1; continue
        if c == "]":
            hl = False; i += 1; continue
        if s.startswith("->", i):
            toks.append(("arrow", "", hl, ans)); i += 2; continue
        if s.startswith("<3", i):
            toks.append(("heart", "", hl, ans)); i += 2; continue
        if c in "^√":
            kind = "sup" if c == "^" else "rad"
            i += 1
            if i < len(s) and s[i] == "{":
                j = s.index("}", i)
                arg = s[i + 1:j]; i = j + 1
            else:
                m = re.match(r"[0-9A-Za-zx]+", s[i:])
                arg = m.group(0); i += len(arg)
            sub_hl = hl
            if arg.startswith("[") and arg.endswith("]"):
                arg, sub_hl = arg[1:-1], True
            toks.append((kind, arg, sub_hl, ans)); continue
        toks.append(("txt", c, hl, ans)); i += 1
    return toks


def measure(toks, m):
    w = 0
    for kind, t, _, _ in toks:
        if kind == "txt":
            w += m.width(t)
        elif kind == "sup":
            w += m.width(t) * SUP + 0.05
        elif kind == "rad":
            w += RAD_W + m.width(t) + 0.08
        elif kind == "arrow":
            w += ARROW_W
        elif kind == "heart":
            w += HEART_W
    return w


def rad_svg(m, th=0.075):
    # coordenadas en centésimas de em; y=0 arriba del vinculum, abajo 0.10em bajo la línea base
    top = m.cap + 0.13 + th
    hgt = top + 0.10
    Hh = hgt * 100
    path = f"M{th*50:.1f} {Hh*0.60:.1f} L15 {Hh*0.52:.1f} L29 {Hh-th*50:.1f} L{RAD_W*100:.1f} {th*50:.2f}"
    return (f'<svg class="radsign" viewBox="0 0 {RAD_W*100:.0f} {Hh:.1f}" '
            f'style="width:{RAD_W}em;height:{hgt:.3f}em;vertical-align:-0.10em">'
            f'<path d="{path}" fill="none" stroke="currentColor" stroke-width="{th*100:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')


ARROW_SVG = ('<svg class="arrow" viewBox="0 0 95 50" style="width:{w}em;height:.5em;vertical-align:{v:.3f}em">'
             '<path d="M8 25 H82 M62 7 L84 25 L62 43" fill="none" stroke="currentColor" stroke-width="7" '
             'stroke-linecap="round" stroke-linejoin="round"/></svg>')
HEART_SVG = ('<svg class="heart" viewBox="0 0 100 92" style="width:{w}em;height:{h:.3f}em;vertical-align:{v:.3f}em">'
             '<path d="M50 88 C20 66 4 50 4 30 C4 15 16 4 30 4 C40 4 46 9 50 17 C54 9 60 4 70 4 C84 4 96 15 96 30 '
             'C96 50 80 66 50 88 Z" fill="currentColor"/></svg>')


def render(toks, m, th=0.075):
    out, cur_ans, cur_hl = [], False, False

    def esc(t):
        return html.escape(t)

    groups = []  # agrupar por (ans, hl)
    for tk in toks:
        key = (tk[3], tk[2] if tk[0] in ("txt", "arrow", "heart") else False)
        if groups and groups[-1][0] == key:
            groups[-1][1].append(tk)
        else:
            groups.append((key, [tk]))

    ans_open = False
    for (ans, hl), tks in groups:
        if ans and not ans_open:
            out.append('<span class="ans">'); ans_open = True
        inner = []
        for kind, t, thl, _ in tks:
            if kind == "txt":
                inner.append(esc(t))
            elif kind == "sup":
                body = esc(t)
                if thl:
                    body = f'<span class="mk"><i></i>{body}</span>'
                inner.append(f'<span class="sup">{body}</span>')
            elif kind == "rad":
                inner.append(f'<span class="rad">{rad_svg(m, th)}<span class="radicand">{esc(t)}</span></span>')
            elif kind == "arrow":
                inner.append(ARROW_SVG.format(w=ARROW_W, v=m.cap / 2 - 0.25))
            elif kind == "heart":
                inner.append(HEART_SVG.format(w=HEART_W, h=0.92, v=-0.04))
        s = "".join(inner)
        if hl:
            s = f'<span class="mk"><i></i>{s}</span>'
        out.append(s)
    if ans_open:
        out.append("</span>")
    return "".join(out)


# ── Tiempos ────────────────────────────────────────────────────────────────
def load_timing():
    p = os.path.join(ROOT, "tools", "timing.json")
    return json.load(open(p))


def build():
    timing = load_timing()
    lines = timing["lines"]
    assert len(lines) == len(SONG), (len(lines), len(SONG))

    items = []
    for li, (line, tl) in enumerate(zip(SONG, lines)):
        for k, it in enumerate(line["items"]):
            t = tl["items"][k]
            items.append(dict(it, line=li, label=line["label"], t=t["at"], r=t.get("reveal") or t["at"]))

    # Cabecera y cierre
    last_line_end = lines[-1]["end"]
    outro_t = max(items[-1]["t"] + 0.8, min(last_line_end + 0.4, DURATION - 1.5))
    outro = dict(fg="cuadrado, cubo y raíz", bg="<3", color="pink", word=True, t=outro_t, r=outro_t,
                 label="", note="me lo sé, me lo sé", line=-1)
    items = items + [outro]
    for a, b in zip(items, items[1:]):
        a["end"] = b["t"]
    items[-1]["end"] = DURATION

    for a, b in zip(items, items[1:]):
        if b["t"] - a["t"] < 0.12:
            raise SystemExit(f"items demasiado juntos: {a['fg']} {a['t']} / {b['fg']} {b['t']}")

    sections, tweens = [], []
    X = "expo.out"
    prev = None
    for n, it in enumerate(items):
        sid = f"it{n}"
        t0, tr, t1 = it["t"], max(it["r"], it["t"]), it["end"]
        color = it.get("color")
        if not color:
            fg = it["fg"]
            color = "wine" if "√" in fg else ("pink" if "^2" in fg else ("teal" if "^3" in fg else "gold"))
        hexc, alpha = COLORS[color]

        # Fondo: el resultado enorme
        btoks = parse(it["bg"])
        bw = measure(btoks, M_BG)
        bsize = min(1000, 1640 / max(bw, 0.01), 750 / M_BG.cap)
        if "^" in it["bg"] or "," in it["bg"]:
            bsize *= 0.8
        if "√" in it["bg"]:
            bsize *= 0.72
        bshift = M_BG.center_shift()
        bg_html = render(btoks, M_BG, th=0.13)

        # Delante: la ecuación en negro
        word = it.get("word")
        fm = M_WORD if word else M_FG
        ftxt = it["fg"].upper() if word else it["fg"]
        ftoks = parse(ftxt)
        fw = measure(ftoks, fm)
        fsize = min(190 if word else 168, 1500 / max(fw, 0.01))
        fshift = fm.center_shift()
        fg_html = render(ftoks, fm)

        note_html = ""
        if it.get("note"):
            ntoks = parse(it["note"])
            nw = measure(ntoks, M_NOTE)
            nsize = min(84, 1300 / max(nw, 0.01))
            ntop = H / 2 + fsize * 0.62 + 18
            ncol = "#8E1A47" if color == "teal" else "#14787E"
            note_html = (f'<div class="notew" style="top:{ntop:.0f}px"><div class="note" style="font-size:{nsize:.0f}px;color:{ncol}">'
                         f'{render(ntoks, M_NOTE)}</div></div>')

        same_bg = prev is not None and prev["bg"] == it["bg"] and prev["_color"] == color
        same_fg = prev is not None and prev["fg"] == it["fg"]
        it["_color"] = color

        sections.append(
            f'<section class="clip it" id="{sid}" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" data-track-index="2">'
            f'<div class="bgw"><div class="bg" style="font-size:{bsize:.0f}px;margin-top:{bshift*bsize*2:.0f}px;'
            f'color:{hexc};opacity:{alpha}">{bg_html}</div></div>'
            f'<div class="fgw"><div class="fg{" word" if word else ""}" style="font-size:{fsize:.0f}px;'
            f'margin-top:{fshift*fsize*2:.0f}px">{fg_html}</div></div>'
            f'{note_html}</section>')

        S = f"#{sid}"
        hold = t1 - t0
        # Delante
        if same_fg:
            tweens.append(f"tl.set('{S} .fgw',{{opacity:1}},{t0:.3f});")
        else:
            d = min(0.4, hold * 0.6)
            tweens.append(f"tl.fromTo('{S} .fgw',{{opacity:0,y:24,scale:0.97}},{{opacity:1,y:0,scale:1,duration:{d:.3f},ease:'{X}'}},{t0:.3f});")
        if "|" in it["fg"]:
            if tr > t0 + 0.05:
                tweens.append(f"tl.set('{S} .ans',{{opacity:0}},{t0:.3f});")
            tweens.append(f"tl.fromTo('{S} .ans',{{opacity:0,scale:1.45}},{{opacity:1,scale:1,duration:{min(0.42, t1 - tr):.3f},ease:'back.out(2)'}},{tr:.3f});")
        # Fondo
        # (el resultado de fondo está siempre: entra con el rótulo y late cuando se canta la respuesta)
        has_reveal = tr > t0 + 0.25
        if same_bg:
            tweens.append(f"tl.set('{S} .bgw',{{opacity:1,scale:1}},{t0:.3f});")
            slam_end = t0
        else:
            d = min(0.6, max(0.15, (tr if has_reveal else t1) - t0 - 0.05))
            tweens.append(f"tl.fromTo('{S} .bgw',{{opacity:0,scale:1.25}},{{opacity:1,scale:1,duration:{d:.3f},ease:'{X}'}},{t0:.3f});")
            slam_end = t0 + d
        if has_reveal:
            pre = tr - slam_end - 0.03
            if pre > 0.3:
                tweens.append(f"tl.to('{S} .bgw',{{scale:1.03,duration:{pre:.3f},ease:'none'}},{slam_end + 0.01:.3f});")
            d = min(0.45, max(0.12, t1 - tr - 0.05))
            tweens.append(f"tl.fromTo('{S} .bgw',{{scale:1.14}},{{scale:1,duration:{d:.3f},ease:'back.out(2)'}},{tr:.3f});")
            slam_end = tr + d
        slam_end += 0.01
        drift = t1 - slam_end - 0.02
        if drift > 0.4:
            tweens.append(f"tl.to('{S} .bgw',{{scale:1+{min(0.06, drift*0.012):.4f},duration:{drift:.3f},ease:'none'}},{slam_end:.3f});")
        # Subrayador
        if "[" in it["fg"]:
            at = tr + 0.08
            tweens.append(f"tl.fromTo('{S} .fg .mk i',{{scaleX:0}},{{scaleX:1,duration:{min(0.35, max(0.1, t1-at-0.02)):.3f},ease:'power2.out',stagger:0.06}},{at:.3f});")
        if it.get("note"):
            at = min(tr + 0.15, t1 - 0.2)
            tweens.append(f"tl.fromTo('{S} .notew',{{opacity:0,y:16}},{{opacity:1,y:0,duration:{min(0.45, t1-at):.3f},ease:'{X}'}},{at:.3f});")
        prev = it

    # Letra (abajo) y etiqueta de sección (arriba)
    lyr = []
    for li, (line, tl) in enumerate(zip(SONG, lines)):
        s = tl["start"]
        nxt = lines[li + 1]["start"] if li + 1 < len(lines) else outro_t
        e = min(nxt, tl["end"] + 1.2) if nxt - tl["end"] > 3 else nxt
        lyr.append((s, e, line["text"]))
    lyric_secs = []
    for n, (s, e, txt) in enumerate(lyr):
        lyric_secs.append(f'<section class="clip lyr" id="ly{n}" data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="3">'
                          f'<div class="lyrw"><div class="lyric">{html.escape(txt)}</div></div></section>')
        tweens.append(f"tl.fromTo('#ly{n} .lyrw',{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3,ease:'{X}'}},{s:.3f});")

    labels = []
    for li, (line, tl) in enumerate(zip(SONG, lines)):
        if labels and labels[-1][2] == line["label"]:
            continue
        labels.append([tl["start"] if li else 0.0, None, line["label"]])
    for a, b in zip(labels, labels[1:]):
        a[1] = b[0]
    labels[-1][1] = outro_t
    label_secs = []
    for n, (s, e, lab) in enumerate(labels):
        label_secs.append(f'<section class="clip lab" id="lb{n}" data-start="{s:.3f}" data-duration="{e - s:.3f}" data-track-index="4">'
                          f'<div class="labw"><div class="label">{render(parse(lab.upper().replace("^N", "^n")), M_FG)}</div></div></section>')
        tweens.append(f"tl.fromTo('#lb{n} .labw',{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.35,ease:'{X}'}},{s:.3f});")

    css = CSS.replace("%PAPER%", PAPER).replace("%INK%", INK)
    css += f".fg .radicand::before{{top:{M_FG.asc - M_FG.cap - 0.13:.3f}em}}\n"
    css += f".fg.word .radicand::before{{top:{M_WORD.asc - M_WORD.cap - 0.13:.3f}em}}\n"
    css += f".bg .radicand::before{{top:{M_BG.asc - M_BG.cap - 0.13:.3f}em;height:.13em}}\n"
    css += f".note .radicand::before{{top:{M_NOTE.asc - M_NOTE.cap - 0.13:.3f}em}}\n"

    doc = TEMPLATE.format(
        css=css, W=W, H=H, FPS=FPS, DUR=f"{DURATION:.2f}", AUDIO=AUDIO,
        sections="\n".join(sections), lyrics="\n".join(lyric_secs), labels="\n".join(label_secs),
        tweens="\n".join(tweens), heart=HEART_SVG.format(w=1, h=0.92, v=-0.1),
    )
    open(os.path.join(ROOT, "index.html"), "w").write(doc)
    print(f"index.html: {len(items)} rótulos, {len(lyr)} versos, {len(labels)} etiquetas")


CSS = r"""
@font-face{font-family:'Fredoka';src:url('assets/fonts/fredoka.woff2') format('woff2');font-weight:300 700;font-display:block}
@font-face{font-family:'Rubik';src:url('assets/fonts/rubik.woff2') format('woff2');font-weight:300 900;font-display:block}
@font-face{font-family:'Montserrat';src:url('assets/fonts/montserrat.woff2') format('woff2');font-weight:100 900;font-display:block}
@font-face{font-family:'Caveat';src:url('assets/fonts/caveat.woff2') format('woff2');font-weight:700;font-display:block}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:%PAPER%}
#root{position:relative;width:1920px;height:1080px;overflow:hidden;background:%PAPER%}
.paper{position:absolute;inset:0;background:
  radial-gradient(ellipse at 50% 45%,rgba(255,255,255,.75),rgba(255,255,255,0) 62%),
  repeating-linear-gradient(0deg,rgba(26,25,24,.035) 0 1px,transparent 1px 54px);}
.frame{position:absolute;inset:44px;border:3px solid #F08CC0;border-radius:34px}
.byheart{position:absolute;top:66px;right:96px;font-family:'Caveat';font-weight:700;font-size:46px;color:#E4479A;display:flex;gap:10px;align-items:center}
.clip{position:absolute;inset:0}
.it{z-index:2}
.bgw,.fgw{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.bg{font-family:'Fredoka';font-weight:700;line-height:1;white-space:pre;letter-spacing:-0.01em}
.fg{font-family:'Rubik';font-weight:600;line-height:1;white-space:pre;color:%INK%;letter-spacing:-0.005em}
.fg.word{font-weight:700;letter-spacing:0.02em}
.sup{font-size:.56em;position:relative;top:-0.78em;margin-left:.05em}
.rad{white-space:pre}
.radsign{overflow:visible;margin-right:-0.02em}
.radicand{position:relative;padding:0 .04em 0 .06em}
.radicand::before{content:'';position:absolute;left:-0.02em;right:0;height:.075em;background:currentColor;border-radius:.04em}
.ans{display:inline-block}
.mk{position:relative;display:inline-block;z-index:0}
.mk i{position:absolute;left:-.07em;right:-.07em;bottom:.02em;height:.5em;background:#F6DE3B;z-index:-1;border-radius:.06em;transform-origin:left center;opacity:.9}
.bg .mk i{display:none}
.notew{position:absolute;left:0;right:0;display:flex;justify-content:center}
.note{font-family:'Caveat';font-weight:700;color:#14787E;line-height:1;white-space:pre;rotate:-3deg}
.note .sup{top:-0.6em}
.lyr{z-index:3}
.lyrw{position:absolute;left:0;right:0;bottom:104px;display:flex;justify-content:center}
.lyric{font-family:'Montserrat';font-weight:500;font-size:32px;color:#5E564C;letter-spacing:.02em}
.lab{z-index:3}
.labw{position:absolute;left:0;right:0;top:96px;display:flex;justify-content:center}
.label{font-family:'Montserrat';font-weight:600;font-size:24px;letter-spacing:.32em;color:#A39686}
.label .sup{top:-0.6em}
"""

TEMPLATE = """<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<title>Cuadrado, Cubo y Raíz</title>
<script src="assets/gsap.min.js"></script>
<style>{css}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}" data-fps="{FPS}">
<audio id="song" src="{AUDIO}" data-start="0" data-duration="{DUR}" data-track-index="0" data-volume="1"></audio>
<div class="paper"></div>
<div class="frame"></div>
<div class="byheart">BY {heart}</div>
{sections}
{lyrics}
{labels}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{tweens}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
