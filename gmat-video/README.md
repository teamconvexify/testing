# Cuadrado, Cubo y Raíz · vídeo HyperFrames

Vídeo musical (1920×1080, 30 fps, 3:32) con todas las ecuaciones de la hoja "Common Squares, Cubes and Square Roots", sincronizado con la canción de Suno.

Cada pantalla tiene el **resultado de fondo**, enorme, redondito y translúcido, y **la ecuación delante**, más pequeña, en negro y centrada. Arriba va la sección y abajo el verso que suena.

Colores de la hoja: rosa para los cuadrados, verde azulado para los cubos, granate para las raíces y amarillo fluorescente para las potencias y las últimas cifras.

## Archivos

| Ruta | Qué es |
| --- | --- |
| `index.html` | Composición HyperFrames, generada por `tools/build.py` (no editar a mano) |
| `tools/cues.py` | Guion: cada verso de la letra y las ecuaciones que dispara |
| `tools/align.py` | Sincroniza la letra con el audio (faster-whisper por bloques + rejilla de beats) |
| `tools/timing.json` | Tiempos resultantes de cada rótulo |
| `tools/build.py` | Genera `index.html` desde `cues.py` + `timing.json` |
| `assets/` | Canción, fuentes locales (Fredoka, Rubik, Montserrat, Caveat) y GSAP |
| `renders/` | Vídeos renderizados |
| `video-backups/` | Copia del HTML de cada versión |

## Cambiar algo

1. Edita `tools/cues.py` (textos, ecuaciones, notas) o `tools/build.py` (diseño).
2. `python3 tools/build.py`
3. `npx hyperframes@0.8.27 lint .` y `npx hyperframes@0.8.27 snapshot . --at 10,60,120`
4. `npx hyperframes@0.8.27 render . -o renders/cuadrado-cubo-raiz-vN.mp4 --quality high`

Si cambia la canción, vuelve a sincronizar con `python3 tools/align.py <modelo_whisper> <audio_16k.wav> --retranscribe`. Necesita `faster-whisper`, `librosa` y `num2words`.

Marcado de ecuaciones en `cues.py`:
- `^2` exponente
- `√{10}` raíz
- `[..]` subrayador
- `|` separa la pregunta de la respuesta, que aparece cuando se canta
- `->` flecha
- `<3` corazón
