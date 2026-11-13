import sys, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
S, O = sys.argv[1], sys.argv[2]
EXB = TTFont(S + '/font/ArchivoExp-800.woff'); EXS = TTFont(S + '/font/ArchivoExp-600.woff')
CR, NE, AR = '#EDE8E3', '#121114', '#EA6F41'
def larg(t, f, size, tr=0.0):
    hm, cm, u = f['hmtx'], f.getBestCmap(), f['head'].unitsPerEm
    return sum(hm[cm[ord(c)]][0] for c in t) * size / u + tr * size * (len(t) - 1)
def cap(f):
    gs, cm, u = f.getGlyphSet(), f.getBestCmap(), f['head'].unitsPerEm
    p = BoundsPen(gs); gs[cm[ord('L')]].draw(p); return p.bounds[3] / u
def path(t, f, size, x, base, tr=0.0):
    gs, cm, hm, u = f.getGlyphSet(), f.getBestCmap(), f['hmtx'], f['head'].unitsPerEm
    k = size / u; pen = SVGPathPen(gs)
    for ch in t:
        g = cm[ord(ch)]; gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x, base))); x += hm[g][0] * k + tr * size
    return pen.getCommands()
def svg(nome, w, h, corpo):
    open(os.path.join(O, nome), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}">{corpo}</svg>')
CAPB, CAPS = cap(EXB), cap(EXS)
for tema, col in [('crema', CR), ('nero', NE)]:
    # 1. SCRITTA
    size, tr = 100, -0.01; h = size * CAPB
    svg(f'1-scritta-{tema}.svg', larg('21LABS', EXB, size, tr), h, f'<path d="{path("21LABS", EXB, size, 0, h, tr)}" fill="{col}"/>')
    # 2. BLOCCO: 21 pesante + tre righe piccole
    s21 = 120; h21 = s21 * CAPB; w21 = larg('21', EXB, s21, -0.02)
    righe = ['LABS', 'STUDIO DIGITALE', 'NAPOLI']; sp = 7; sr = (h21 - 2 * sp) / 3 / CAPS
    x0 = w21 + 18; corpo = f'<path d="{path("21", EXB, s21, 0, h21, -0.02)}" fill="{col}"/>'
    for i, r in enumerate(righe):
        base = (i + 1) * sr * CAPS + i * sp
        corpo += f'<path d="{path(r, EXS, sr, x0, base, 0.04)}" fill="{col}"/>'
    wr = max(larg(r, EXS, sr, 0.04) for r in righe)
    svg(f'2-blocco-{tema}.svg', x0 + wr, h21, corpo)
    # 3. PUNTO CALDO: pallino arancio + scritta
    size = 100; h = size * CAPB; r = h * 0.36
    corpo = f'<circle cx="{r}" cy="{h/2}" r="{r}" fill="{AR}"/><path d="{path("21LABS", EXB, size, 2 * r + 16, h, -0.01)}" fill="{col}"/>'
    svg(f'3-punto-caldo-{tema}.svg', 2 * r + 16 + larg('21LABS', EXB, size, -0.01), h, corpo)
    # simbolo solo (per icona): 21 in un quadrato
    lato = 120; s = 74; hh = s * CAPB; w = larg('21', EXB, s, -0.02)
    fondo, scr = (NE, CR) if tema == 'crema' else (CR, NE)
    svg(f'icona-21-{tema}.svg', lato, lato, f'<rect width="{lato}" height="{lato}" fill="{fondo}"/><path d="{path("21", EXB, s, (lato - w) / 2, (lato + hh) / 2, -0.02)}" fill="{scr}"/>')
print('ok', round(CAPB, 3), round(CAPS, 3))
