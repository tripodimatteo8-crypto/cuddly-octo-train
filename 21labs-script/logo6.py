import sys, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
S, O = sys.argv[1], sys.argv[2]
ANTON = TTFont(S + '/font/Anton.woff'); POP6 = TTFont(S + '/font/Poppins-600.woff')
TC, TS, CR, NE = '#6FB3C2', '#275B66', '#F2EDE9', '#201D1C'
def larg(t, f, size, tr=0.0):
    hm, cm, u = f['hmtx'], f.getBestCmap(), f['head'].unitsPerEm
    return sum(hm[cm[ord(c)]][0] for c in t) * size / u + tr * size * (len(t) - 1)
def path(t, f, size, x, base, tr=0.0):
    gs, cm, hm, u = f.getGlyphSet(), f.getBestCmap(), f['hmtx'], f['head'].unitsPerEm
    k = size / u; pen = SVGPathPen(gs)
    for ch in t:
        g = cm[ord(ch)]; gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x, base))); x += hm[g][0] * k + tr * size
    return pen.getCommands()
def svg(nome, w, h, corpo, defs=''):
    open(os.path.join(O, nome), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}"><defs>{defs}</defs>{corpo}</svg>')
GRAD = f'<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8CC6D0"/><stop offset=".55" stop-color="{TC}"/><stop offset="1" stop-color="{TS}"/></linearGradient>'
ALTEZZA_ANTON = 0.865  # altezza reale di maiuscole e cifre di Anton (misurata dal font)
M = 6  # margine

for tema, testo_c, acc in [('scuro', CR, TC), ('chiaro', NE, TS)]:
    # 1. BLOCCO: 21 sopra, LABS sotto, stessa larghezza
    s21 = 200; w = larg('21', ANTON, s21); sL = s21 * w / larg('LABS', ANTON, s21, 0.06) * 1.0
    trL = 0.06; sL = w / (larg('LABS', ANTON, 1, trL))
    b21 = s21 * ALTEZZA_ANTON + M
    corpo = (f'<path d="{path("21", ANTON, s21, 0, b21)}" fill="{acc}"/>'
             f'<rect x="0" y="{b21+10:.1f}" width="{w:.1f}" height="9" fill="{acc}"/>'
             f'<path d="{path("LABS", ANTON, sL, 0, b21 + 29 + sL * ALTEZZA_ANTON, trL)}" fill="{testo_c}"/>')
    svg(f'1-blocco-{tema}.svg', w, b21 + 29 + sL * ALTEZZA_ANTON + M, corpo)

    # 2. TAGLIO: scritta tagliata in due, metà inferiore spostata, linea petrolio nello spacco
    size = 140; base = size * ALTEZZA_ANTON + M; W = larg('21LABS', ANTON, size, 0.01) + 30; meta = base - size * ALTEZZA_ANTON * 0.48
    d21 = path('21', ANTON, size, 0, base, 0.01); x2 = larg('21', ANTON, size, 0.01) + size * 0.01
    dL = path('LABS', ANTON, size, x2, base, 0.01)
    defs = (f'<clipPath id="sopra-{tema}"><rect x="-5" y="-5" width="{W+10}" height="{meta-3:.1f}"/></clipPath>'
            f'<clipPath id="sotto-{tema}"><rect x="-5" y="{meta+3:.1f}" width="{W+10}" height="{size*1.3:.0f}"/></clipPath>')
    lettere = f'<path d="{d21}" fill="{acc}"/><path d="{dL}" fill="{testo_c}"/>'
    corpo = (f'<g clip-path="url(#sopra-{tema})">{lettere}</g>'
             f'<g clip-path="url(#sotto-{tema})" transform="translate(16 0)">{lettere}</g>'
             f'<rect x="0" y="{meta-1.2:.1f}" width="{W:.1f}" height="2.4" fill="{acc}"/>')
    svg(f'2-taglio-{tema}.svg', W, base + M, corpo, defs)

    # 3. PIXEL: 21 fatto di quadratini, LABS accanto
    DUE = ['01110', '10001', '00001', '00010', '00100', '01000', '11111']
    UNO = ['00100', '01100', '00100', '00100', '00100', '00100', '01110']
    p, gap = 20, 4; pix = ''
    for ox, mat in [(0, DUE), (6 * (p + gap), UNO)]:
        for r, riga in enumerate(mat):
            for c, v in enumerate(riga):
                if v == '1':
                    op = 0.55 + 0.45 * (1 - r / 6)
                    pix += f'<rect x="{ox + c*(p+gap)}" y="{r*(p+gap)}" width="{p}" height="{p}" rx="3" fill="{acc}" opacity="{op:.2f}"/>'
    hP = 7 * (p + gap) - gap; xL = 11 * (p + gap) + 16; sL = hP / ALTEZZA_ANTON
    corpo = pix + f'<path d="{path("LABS", ANTON, sL, xL, hP, 0.02)}" fill="{testo_c}"/>'
    svg(f'3-pixel-{tema}.svg', xL + larg('LABS', ANTON, sL, 0.02) + 4, hP + 2, corpo)

    # 4. PUNTO: 21labs. minuscolo, pulitissimo
    size = 150; base = 120
    x21 = larg('21', POP6, size, -0.02)
    corpo = (f'<path d="{path("21", POP6, size, 0, base, -0.02)}" fill="{acc}"/>'
             f'<path d="{path("labs", POP6, size, x21 + 2, base, -0.02)}" fill="{testo_c}"/>')
    xf = x21 + 2 + larg('labs', POP6, size, -0.02)
    corpo += f'<rect x="{xf + 8:.1f}" y="{base - 24}" width="24" height="24" rx="3" fill="{acc}"/>'
    svg(f'4-punto-{tema}.svg', xf + 36, base + 8, corpo)

    # 5. BADGE: quadrato petrolio con 21 bianco, LABS accanto
    lato = 150; s21 = 112; b21 = lato / 2 + s21 * ALTEZZA_ANTON / 2
    x21 = (lato - larg('21', ANTON, s21)) / 2
    sL = lato * 0.62 / ALTEZZA_ANTON; bL = lato / 2 + sL * ALTEZZA_ANTON / 2
    corpo = (f'<rect width="{lato}" height="{lato}" rx="34" fill="url(#g)"/>'
             f'<path d="{path("21", ANTON, s21, x21, b21)}" fill="{CR}"/>'
             f'<path d="{path("LABS", ANTON, sL, lato + 26, bL, 0.03)}" fill="{testo_c}"/>')
    svg(f'5-badge-{tema}.svg', lato + 26 + larg('LABS', ANTON, sL, 0.03) + 4, lato, corpo, GRAD.replace('id="g"', 'id="g"'))
print('ok')
