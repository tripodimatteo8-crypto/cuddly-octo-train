import sys, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
S, O = sys.argv[1], sys.argv[2]
MI = TTFont(f'{S}/font/Michroma-400.woff')
ING = 0.042   # ingrassatura: spessore del contorno rispetto alla grandezza del testo
def larg(t, size, tr=0.0):
    hm, cm, u = MI['hmtx'], MI.getBestCmap(), MI['head'].unitsPerEm
    return sum(hm[cm[ord(c)]][0] for c in t) * size / u + tr * size * (len(t) - 1)
def alt(ch):
    gs, cm, u = MI.getGlyphSet(), MI.getBestCmap(), MI['head'].unitsPerEm
    p = BoundsPen(gs); gs[cm[ord(ch)]].draw(p); return p.bounds[3] / u
def testo(t, size, x, base, col, tr=0.0):
    gs, cm, hm, u = MI.getGlyphSet(), MI.getBestCmap(), MI['hmtx'], MI['head'].unitsPerEm
    k = size / u; pen = SVGPathPen(gs)
    for ch in t:
        g = cm[ord(ch)]; gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x, base))); x += hm[g][0] * k + tr * size
    return f'<path d="{pen.getCommands()}" fill="{col}" stroke="{col}" stroke-width="{size*ING:.2f}" stroke-linejoin="round"/>'
def scrivi(nome, w, h, corpo, pad):
    open(os.path.join(O, nome), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad:.1f} {-pad:.1f} {w+2*pad:.1f} {h+2*pad:.1f}" width="{w+2*pad:.0f}" height="{h+2*pad:.0f}">{corpo}</svg>')
CAP = alt('L')
for tema, col in [('crema', '#EDE8E3'), ('nero', '#121114')]:
    # blocco del fronte: 21 + LABS / DIGITAL STUDIO / NAPOLI
    s21 = 120; h21 = s21 * alt('2'); w21 = larg('21', s21, -0.02); sp = 7; sr = (h21 - 2 * sp) / 3 / CAP; tr = 0.06
    righe = ['LABS', 'DIGITAL STUDIO', 'NAPOLI']; x0 = w21 + 20
    corpo = testo('21', s21, 0, h21, col, -0.02) + ''.join(testo(r, sr, x0, (i + 1) * sr * CAP + i * sp, col, tr) for i, r in enumerate(righe))
    scrivi(f'6-michroma-bold-{tema}.svg', x0 + max(larg(r, sr, tr) for r in righe), h21, corpo, s21 * ING)
    # nome su due righe
    sn = 40; righe = ['MATTEO', 'TRIPODI']; il = sn * CAP * 0.42
    corpo = ''.join(testo(r, sn, 0, (i + 1) * sn * CAP + i * il, col, 0.02) for i, r in enumerate(righe))
    scrivi(f'nome-{tema}.svg', max(larg(r, sn, 0.02) for r in righe), 2 * sn * CAP + il, corpo, sn * ING)
    # piccolo 21LABS
    sw = 40; scrivi(f'21labs-michroma-{tema}.svg', larg('21LABS', sw, 0.02), sw * CAP, testo('21LABS', sw, 0, sw * CAP, col, 0.02), sw * ING)
    # etichette TEL / EMAIL / SITO / SCRIVIMI SU / WHATSAPP
    for e in ['TEL', 'EMAIL', 'SITO', 'SCRIVIMI SU', 'WHATSAPP']:
        se = 40; c = '#C9502F' if e == 'WHATSAPP' else ('#6E686B' if e in ('TEL', 'EMAIL', 'SITO') else col)
        scrivi(f'eti-{e.replace(" ", "-").lower()}-{tema}.svg', larg(e, se, 0.12), se * CAP, testo(e, se, 0, se * CAP, c, 0.12), se * ING)
print('ok')
