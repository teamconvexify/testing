# -*- coding: utf-8 -*-
"""Guion del vídeo: cada verso de la letra y las ecuaciones que dispara.

Marcado de ecuaciones (fg = delante, en negro; bg = resultado gigante de fondo):
  ^2 ^n ^{par}   exponente
  √2  √{10}      raíz con vinculum
  [..]           subrayador amarillo (como el rotulador de la hoja)
  |              separa pregunta y respuesta: lo de la derecha aparece en `reveal`
  ->             flecha
  <3             corazón

Cada item: at = palabra de la letra que lo dispara, reveal = palabra que destapa el resultado.
"""

INTRO, CHORUS, POST = "intro", "chorus", "post"


def chorus():
    return [
        dict(text="Cuadrado, cubo y raíz", label="Estribillo", items=[
            dict(at="Cuadrado", fg="cuadrado", bg="x^2", color="pink", word=True),
            dict(at="cubo", fg="cubo", bg="x^3", color="teal", word=True),
            dict(at="raíz", fg="raíz", bg="√x", color="wine", word=True),
        ]),
        dict(text="el GMAT me hace feliz (¡feliz!)", label="Estribillo", items=[
            dict(at="GMAT", fg="el GMAT me hace feliz", bg="GMAT", color="pink", word=True),
            dict(at="¡feliz!", fg="¡feliz!", bg="<3", color="pink", word=True),
        ]),
        dict(text="Cuadrado, cubo y raíz", label="Estribillo", items=[
            dict(at="Cuadrado", fg="x^2 · x^3 · √x", bg="x^2", color="pink"),
            dict(at="cubo", fg="x^2 · x^3 · √x", bg="x^3", color="teal"),
            dict(at="raíz", fg="x^2 · x^3 · √x", bg="√x", color="wine"),
        ]),
        dict(text="me lo sé, me lo sé… ¡así!", label="Estribillo", items=[
            dict(at="me", fg="me lo sé, me lo sé", bg="<3", color="pink", word=True),
            dict(at="¡así!", fg="¡así!", bg="<3", color="pink", word=True),
        ]),
    ]


def roots(with_tail):
    L = "Raíces"
    lines = [
        dict(text="Raíz de dos, uno cuarenta y uno (¡uno!)", label=L, items=[
            dict(at="Raíz", fg="√2 = |1,41", bg="1,41", reveal="uno")]),
        dict(text="Raíz de tres, uno setenta y tres (¡tres!)", label=L, items=[
            dict(at="Raíz", fg="√3 = |1,73", bg="1,73", reveal="uno")]),
        dict(text="Raíz de cinco, dos veinticuatro", label=L, items=[
            dict(at="Raíz", fg="√5 = |2,24", bg="2,24", reveal="dos")]),
        dict(text="Raíz de seis, dos cuarenta y cinco", label=L, items=[
            dict(at="Raíz", fg="√6 = |2,45", bg="2,45", reveal="dos")]),
        dict(text="Raíz de siete, dos sesenta y cinco", label=L, items=[
            dict(at="Raíz", fg="√7 = |2,65", bg="2,65", reveal="dos")]),
        dict(text="Raíz de ocho, dos ochenta y tres", label=L, items=[
            dict(at="Raíz", fg="√8 = |2,83", bg="2,83", reveal="dos")]),
        dict(text="Raíz de diez… ¡tres dieciséis!", label=L, items=[
            dict(at="Raíz", fg="√{10} = |3,16", bg="3,16", reveal="¡tres")]),
    ]
    if with_tail:
        lines.append(dict(text="(Raíz de cuatro, dos. ¡Raíz de uno, uno!)", label=L, items=[
            dict(at="(Raíz", fg="√4 = |2", bg="2", reveal="dos."),
            dict(at="¡Raíz", fg="√1 = |1", bg="1", reveal="uno!)"),
        ]))
    return lines


def sq(n, word, res_word, note=None, label=None):
    return dict(at=word, fg=f"{n}^2 = |{n*n}", bg=str(n * n), reveal=res_word, note=note)


SONG = []

# ── Intro ───────────────────────────────────────────────────────────────
SONG += [
    dict(text="(¡Eh! ¡Eh!)", label="Common squares, cubes and square roots", items=[
        dict(at="(¡Eh!", fg="cuadrado, cubo y raíz", bg="GMAT", color="pink", word=True),
    ]),
    dict(text="Uno a la que quieras… (¡uno!)", label="Uno a la que quieras", items=[
        dict(at="Uno", fg="1^n = 1", bg="1", color="gold"),
        dict(at="quieras…", fg="1^2 = 1", bg="1", color="pink"),
        dict(at="(¡uno!)", fg="1^3 = 1", bg="1", color="teal"),
    ]),
    dict(text="Uno a la que quieras… (¡uno!)", label="Uno a la que quieras", items=[
        dict(at="Uno", fg="1^4 = 1", bg="1", color="gold"),
        dict(at="quieras…", fg="1^5 = 1", bg="1", color="gold"),
        dict(at="(¡uno!)", fg="1^6 = 1", bg="1", color="gold"),
    ]),
]

SONG += chorus()

# ── Verso 1 · potencias de 2 ────────────────────────────────────────────
L2 = "Potencias de 2"
SONG += [
    dict(text="Dobla, dobla, dobla, ¡dale!", label=L2, items=[
        dict(at="Dobla,", fg="2 × 2 × 2 × 2 …", bg="×2", color="gold"),
    ]),
    dict(text="Dos, cuatro, ocho, dieciséis", label=L2, items=[
        dict(at="Dos,", fg="2^1 = 2", bg="2"),
        dict(at="cuatro,", fg="2^2 = 4", bg="4"),
        dict(at="ocho,", fg="2^3 = 8", bg="8"),
        dict(at="dieciséis", fg="2^4 = 16", bg="16"),
    ]),
    dict(text="Treinta y dos, sesenta y cuatro", label=L2, items=[
        dict(at="Treinta", fg="2^5 = 32", bg="32"),
        dict(at="sesenta", fg="2^6 = 64", bg="64"),
    ]),
    dict(text="Ciento veintiocho…", label=L2, items=[
        dict(at="Ciento", fg="2^7 = 128", bg="128"),
    ]),
    dict(text="¡Doscientos cincuenta y seis!", label=L2, items=[
        dict(at="¡Doscientos", fg="2^8 = 256", bg="256"),
    ]),
    dict(text="(Dos a la ocho, ¡ya lo ves!)", label=L2, items=[
        dict(at="(Dos", fg="[2^8] = 256", bg="256", color="gold"),
    ]),
    dict(text="Y el final da vueltas: dos, cuatro, ocho, seis", label="La última cifra de 2^n", items=[
        dict(at="Y", fg="2 · 4 · 8 · 6", bg="2486", color="gold", note="el final da vueltas"),
        dict(at="dos,", fg="[2] · 4 · 8 · 6", bg="2", color="gold"),
        dict(at="cuatro,", fg="2 · [4] · 8 · 6", bg="4", color="gold"),
        dict(at="ocho,", fg="2 · 4 · [8] · 6", bg="8", color="gold"),
        dict(at="seis", fg="2 · 4 · 8 · [6]", bg="6", color="gold"),
    ]),
    dict(text="Dos, cuatro, ocho, seis (¡otra vez!)", label="La última cifra de 2^n", items=[
        dict(at="Dos,", fg="2^5 = 3[2]", bg="2", color="gold"),
        dict(at="cuatro,", fg="2^6 = 6[4]", bg="4", color="gold"),
        dict(at="ocho,", fg="2^7 = 12[8]", bg="8", color="gold"),
        dict(at="seis", fg="2^8 = 25[6]", bg="6", color="gold"),
        dict(at="(¡otra", fg="2 · 4 · 8 · 6 …", bg="2486", color="gold", note="¡otra vez!"),
    ]),
]

# ── Verso 2 · potencias de 3, 4 y 5 ─────────────────────────────────────
SONG += [
    dict(text="Tres, nueve, veintisiete", label="Potencias de 3", items=[
        dict(at="Tres,", fg="3^1 = 3", bg="3"),
        dict(at="nueve,", fg="3^2 = 9", bg="9"),
        dict(at="veintisiete", fg="3^3 = 27", bg="27"),
    ]),
    dict(text="Ochenta y uno… (¡y qué!)", label="Potencias de 3", items=[
        dict(at="Ochenta", fg="3^4 = 81", bg="81"),
    ]),
    dict(text="Doscientos cuarenta y tres", label="Potencias de 3", items=[
        dict(at="Doscientos", fg="3^5 = 243", bg="243"),
    ]),
    dict(text="(Empieza en tres y acaba en tres)", label="Potencias de 3", items=[
        dict(at="(Empieza", fg="[3]^5 = 24[3]", bg="3", color="gold", note="empieza en 3 y acaba en 3"),
    ]),
    dict(text="Cuatro, dieciséis", label="Potencias de 4", items=[
        dict(at="Cuatro,", fg="4^1 = 4", bg="4"),
        dict(at="dieciséis", fg="4^2 = 16", bg="16"),
    ]),
    dict(text="Sesenta y cuatro (¡eso es!)", label="Potencias de 4", items=[
        dict(at="Sesenta", fg="4^3 = 64", bg="64"),
    ]),
    dict(text="Doscientos cincuenta y seis", label="Potencias de 4", items=[
        dict(at="Doscientos", fg="4^4 = 256", bg="256"),
    ]),
    dict(text="Cinco, veinticinco", label="Potencias de 5", items=[
        dict(at="Cinco,", fg="5^1 = 5", bg="5"),
        dict(at="veinticinco", fg="5^2 = 25", bg="25"),
    ]),
    dict(text="Ciento veinticinco", label="Potencias de 5", items=[
        dict(at="Ciento", fg="5^3 = 125", bg="125"),
    ]),
    dict(text="Seiscientos veinticinco", label="Potencias de 5", items=[
        dict(at="Seiscientos", fg="5^4 = 625", bg="625"),
    ]),
    dict(text="(¡Todos acaban en cinco!)", label="Potencias de 5", items=[
        dict(at="(¡Todos", fg="2[5] · 12[5] · 62[5]", bg="5", color="gold", note="todos acaban en 5"),
    ]),
]

SONG += chorus()
SONG += roots(with_tail=True)

# ── Verso 3 · 6, 7, 8 y 9 ───────────────────────────────────────────────
SONG += [
    dict(text="Seis por seis, treinta y seis", label="El 6", items=[
        dict(at="Seis", fg="6^2 = |36", bg="36", reveal="treinta")]),
    dict(text="Seis al cubo, doscientos dieciséis", label="El 6", items=[
        dict(at="Seis", fg="6^3 = |216", bg="216", reveal="doscientos")]),
    dict(text="(El seis, el seis… ¡siempre acaba en seis!)", label="El 6", items=[
        dict(at="(El", fg="6^x -> …[6]", bg="6", color="gold", note="unidad siempre 6")]),
    dict(text="Siete por siete, cuarenta y nueve", label="El 7", items=[
        dict(at="Siete", fg="7^2 = |49", bg="49", reveal="cuarenta")]),
    dict(text="Al cubo, trescientos cuarenta y tres", label="El 7", items=[
        dict(at="Al", fg="7^3 = |343", bg="343", reveal="trescientos")]),
    dict(text="(Siete, nueve, tres, uno… ¡y vuelta otra vez!)", label="La última cifra de 7^n", items=[
        dict(at="(Siete,", fg="7^1 = [7]", bg="7", color="gold"),
        dict(at="nueve,", fg="7^2 = 4[9]", bg="9", color="gold"),
        dict(at="tres,", fg="7^3 = 34[3]", bg="3", color="gold"),
        dict(at="uno…", fg="7^4 = 240[1]", bg="1", color="gold"),
        dict(at="¡y", fg="7 · 9 · 3 · 1 …", bg="7931", color="gold", note="¡y vuelta otra vez!"),
    ]),
    dict(text="Ocho por ocho, sesenta y cuatro", label="El 8", items=[
        dict(at="Ocho", fg="8^2 = |64", bg="64", reveal="sesenta")]),
    dict(text="Al cubo, quinientos doce (¡doce!)", label="El 8", items=[
        dict(at="Al", fg="8^3 = |512", bg="512", reveal="quinientos")]),
    dict(text="Nueve por nueve, ochenta y uno", label="El 9", items=[
        dict(at="Nueve", fg="9^2 = |81", bg="81", reveal="ochenta")]),
    dict(text="Al cubo, setecientos veintinueve", label="El 9", items=[
        dict(at="Al", fg="9^3 = |729", bg="729", reveal="setecientos")]),
    dict(text="(Par acaba en uno, impar acaba en nueve)", label="La última cifra de 9^n", items=[
        dict(at="(Par", fg="9^{par} -> …[1]", bg="1", color="gold", note="par acaba en 1"),
        dict(at="impar", fg="9^{impar} -> …[9]", bg="9", color="gold", note="impar acaba en 9"),
    ]),
]

# ── Verso 4 · rap, cuadrados del 11 al 20 ───────────────────────────────
LQ = "Al cuadrado"
SONG += [
    dict(text="(¡Al cuadrado!)", label=LQ, items=[
        dict(at="(¡Al", fg="al cuadrado", bg="x^2", color="pink", word=True)]),
    dict(text="Once, ciento veintiuno", label=LQ, items=[sq(11, "Once,", "ciento")]),
    dict(text="Doce, ciento cuarenta y cuatro", label=LQ, items=[sq(12, "Doce,", "ciento")]),
    dict(text="Y al revés, veintiuno, cuatrocientos cuarenta y uno (¡espejo!)", label=LQ, items=[
        dict(at="Y", fg="12^2 = 144", bg="144", color="pink", note="y al revés…"),
        sq(21, "veintiuno,", "cuatrocientos"),
        dict(at="(¡espejo!)", fg="12^2 = [144]   21^2 = [441]", bg="441", color="pink", note="¡espejo!"),
    ]),
    dict(text="Trece, ciento sesenta y nueve", label=LQ, items=[sq(13, "Trece,", "ciento")]),
    dict(text="Catorce, ciento noventa y seis", label=LQ, items=[sq(14, "Catorce,", "ciento")]),
    dict(text="Quince, doscientos veinticinco", label=LQ, items=[sq(15, "Quince,", "doscientos")]),
    dict(text="Dieciséis, doscientos cincuenta y seis", label=LQ, items=[
        sq(16, "Dieciséis,", "doscientos", note="= 4^4 = 2^8")]),
    dict(text="Diecisiete, doscientos ochenta y nueve", label=LQ, items=[sq(17, "Diecisiete,", "doscientos")]),
    dict(text="Dieciocho, trescientos veinticuatro", label=LQ, items=[sq(18, "Dieciocho,", "trescientos")]),
    dict(text="Diecinueve, trescientos sesenta y uno", label=LQ, items=[sq(19, "Diecinueve,", "trescientos")]),
    dict(text="Veinte, ¡cuatrocientos!", label=LQ, items=[sq(20, "Veinte,", "¡cuatrocientos!")]),
]

# ── Verso 5 · rap, cuadrados del 22 al 30 ───────────────────────────────
SONG += [
    dict(text="(¡Al cuadrado!)", label=LQ, items=[
        dict(at="(¡Al", fg="al cuadrado", bg="x^2", color="pink", word=True)]),
    dict(text="Veintidós, cuatrocientos ochenta y cuatro", label=LQ, items=[sq(22, "Veintidós,", "cuatrocientos")]),
    dict(text="Veintitrés, quinientos veintinueve", label=LQ, items=[sq(23, "Veintitrés,", "quinientos")]),
    dict(text="Veinticuatro, quinientos setenta y seis", label=LQ, items=[sq(24, "Veinticuatro,", "quinientos")]),
    dict(text="Veintiséis, seiscientos setenta y seis", label=LQ, items=[sq(26, "Veintiséis,", "seiscientos")]),
    dict(text="(¡Setenta y seis, setenta y seis!)", label=LQ, items=[
        dict(at="(¡Setenta", fg="26^2 = 6[76]", bg="76", color="pink", note="…76, …76")]),
    dict(text="Veinticinco, seiscientos veinticinco (¡cinco, cinco!)", label=LQ, items=[
        sq(25, "Veinticinco,", "seiscientos"),
        dict(at="(¡cinco,", fg="25^2 = 6[25]", bg="625", color="pink", note="¡cinco, cinco!"),
    ]),
    dict(text="Veintisiete, setecientos veintinueve (¡como nueve al cubo!)", label=LQ, items=[
        sq(27, "Veintisiete,", "setecientos"),
        dict(at="(¡como", fg="27^2 = 729 = [9^3]", bg="729", color="teal", note="¡como nueve al cubo!"),
    ]),
    dict(text="Veintiocho, setecientos ochenta y cuatro", label=LQ, items=[sq(28, "Veintiocho,", "setecientos")]),
    dict(text="Veintinueve, ochocientos cuarenta y uno", label=LQ, items=[sq(29, "Veintinueve,", "ochocientos")]),
    dict(text="Treinta… ¡novecientos!", label=LQ, items=[sq(30, "Treinta…", "¡novecientos!")]),
]

SONG += chorus()

# ── Puente ──────────────────────────────────────────────────────────────
LB = "Cuadrados perfectos"
SONG += [
    dict(text="Cuadrado perfecto, rómpelo en primos", label=LB, items=[
        dict(at="Cuadrado", fg="36 = 6^2", bg="36", color="pink", note="cuadrado perfecto"),
        dict(at="rómpelo", fg="36 = 2^2 · 3^2", bg="36", color="pink", note="rómpelo en primos"),
    ]),
    dict(text="¿Y los exponentes? (¡Pares, pares!)", label=LB, items=[
        dict(at="¿Y", fg="36 = 2^{[2]} · 3^{[2]}", bg="2 2", color="pink", note="¿y los exponentes?"),
        dict(at="(¡Pares,", fg="36 = 2^{[2]} · 3^{[2]}", bg="PAR", color="pink", note="¡pares, pares!"),
    ]),
    dict(text="¿Y los divisores? (¡Impares, impares!)", label=LB, items=[
        dict(at="¿Y", fg="1 · 2 · 3 · 4 · 6 · 9 · 12 · 18 · 36", bg="9", color="pink", note="¿y los divisores?"),
        dict(at="(¡Impares,", fg="36 tiene [9] divisores", bg="9", color="pink", note="¡impares, impares!"),
    ]),
    dict(text="Nueve enteros seguidos, multiplicados", label="9 enteros seguidos", items=[
        dict(at="Nueve", fg="n · (n+1) · (n+2) · … · (n+8)", bg="×9", color="gold", note="nueve enteros seguidos"),
    ]),
    dict(text="¿Entre nueve? (¡Siempre, siempre!)", label="9 enteros seguidos", items=[
        dict(at="¿Entre", fg="÷ 9", bg="9", color="gold", note="¿entre nueve?"),
        dict(at="(¡Siempre,", fg="siempre divisible entre [9]", bg="9", color="gold", word=True),
    ]),
]

SONG += roots(with_tail=False)

SONG += chorus()

SONG += [
    dict(text="(¡Dos, cuatro, ocho, seis! ¡Siete, nueve, tres, uno!)", label="Las últimas cifras", items=[
        dict(at="(¡Dos,", fg="2^n -> [2] · 4 · 8 · 6", bg="2", color="gold"),
        dict(at="cuatro,", fg="2^n -> 2 · [4] · 8 · 6", bg="4", color="gold"),
        dict(at="ocho,", fg="2^n -> 2 · 4 · [8] · 6", bg="8", color="gold"),
        dict(at="seis!", fg="2^n -> 2 · 4 · 8 · [6]", bg="6", color="gold"),
        dict(at="¡Siete,", fg="7^n -> [7] · 9 · 3 · 1", bg="7", color="gold"),
        dict(at="nueve,", fg="7^n -> 7 · [9] · 3 · 1", bg="9", color="gold"),
        dict(at="tres,", fg="7^n -> 7 · 9 · [3] · 1", bg="3", color="gold"),
        dict(at="uno!)", fg="7^n -> 7 · 9 · 3 · [1]", bg="1", color="gold"),
    ]),
]
