import sys, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
S, O = sys.argv[1], sys.argv[2]
ANTON = TTFont(S + '/font/Anton.woff')

def testo_path(txt, font, size, x0=0, base=0, track=0.0):
    """Percorso SVG del testo, con la linea di base a 'base' e grandezza 'size' (px)."""
    gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font['hmtx']
    upm = font['head'].unitsPerEm; k = size / upm
    pen = SVGPathPen(gs); x = x0
    for ch in txt:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x, base)))
        x += hmtx[g][0] * k + track * size
    return pen.getCommands(), x - track * size

PETROLIO_CHIARO, PETROLIO, CREMA, NERO = '#6FB3C2', '#275B66', '#F2EDE9', '#201D1C'

def simbolo(x, y, s, fondo=NERO, bordo=True, id_='g'):
    """Tessera: alba petrolio dietro un vulcano a due cime, su linea d'orizzonte. s = lato."""
    k = s / 120
    def P(px, py): return f'{x + px * k:.2f},{y + py * k:.2f}'
    vulcano = (f'M{P(8,80)} C{P(26,79.5)} {P(38,71)} {P(46,63)} C{P(49,60)} {P(52,59)} {P(54.5,61)} '
               f'L{P(57,63.5)} C{P(59,64.6)} {P(61,64.6)} {P(63,63.5)} L{P(65.5,61)} C{P(68,59)} {P(71,60)} {P(74,63)} '
               f'C{P(82,71)} {P(94,79.5)} {P(112,80)} Z')
    return f'''<defs><linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{PETROLIO_CHIARO}"/><stop offset="1" stop-color="{PETROLIO}"/></linearGradient>
<clipPath id="{id_}c"><rect x="{x:.2f}" y="{y:.2f}" width="{s:.2f}" height="{s:.2f}" rx="{28*k:.2f}"/></clipPath>
<clipPath id="{id_}h"><rect x="{x:.2f}" y="{y:.2f}" width="{s:.2f}" height="{80*k:.2f}"/></clipPath></defs>
<rect x="{x:.2f}" y="{y:.2f}" width="{s:.2f}" height="{s:.2f}" rx="{28*k:.2f}" fill="{fondo}"/>
<g clip-path="url(#{id_}c)"><circle cx="{x+60*k:.2f}" cy="{y+80*k:.2f}" r="{40*k:.2f}" fill="url(#{id_})" clip-path="url(#{id_}h)"/>
<path d="{vulcano}" fill="{fondo}"/>
<rect x="{x:.2f}" y="{y+79.4*k:.2f}" width="{s:.2f}" height="{1.4*k:.2f}" fill="{PETROLIO_CHIARO}" opacity="0.6"/>
<rect x="{x+40*k:.2f}" y="{y+87*k:.2f}" width="{40*k:.2f}" height="{1.6*k:.2f}" rx="{0.8*k:.2f}" fill="{PETROLIO_CHIARO}" opacity="0.35"/>
<rect x="{x+48*k:.2f}" y="{y+93*k:.2f}" width="{24*k:.2f}" height="{1.6*k:.2f}" rx="{0.8*k:.2f}" fill="{PETROLIO_CHIARO}" opacity="0.22"/>
<rect x="{x+55*k:.2f}" y="{y+99*k:.2f}" width="{10*k:.2f}" height="{1.6*k:.2f}" rx="{0.8*k:.2f}" fill="{PETROLIO_CHIARO}" opacity="0.14"/></g>''' +       (f'<rect x="{x+0.5:.2f}" y="{y+0.5:.2f}" width="{s-1:.2f}" height="{s-1:.2f}" rx="{28*k-0.5:.2f}" fill="none" stroke="{CREMA}" stroke-opacity="0.12"/>' if bordo else '')

def wordmark(x, base, size, c21, clabs):
    p21, x1 = testo_path('21', ANTON, size, x, base)
    pl, x2 = testo_path('LABS', ANTON, size, x1 + size * 0.02, base)
    return f'<path d="{p21}" fill="{c21}"/><path d="{pl}" fill="{clabs}"/>', x2

def scrivi(nome, w, h, corpo):
    with open(os.path.join(O, 'logo', nome), 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}">{corpo}</svg>')

# simbolo da solo (icona profilo, favicon)
scrivi('21labs-simbolo.svg', 120, 120, simbolo(0, 0, 120, id_='s'))
# orizzontale: misura il wordmark per fissare la larghezza
for nome, c21, clabs, fondo in [('21labs-orizzontale-per-fondo-scuro.svg', PETROLIO_CHIARO, CREMA, NERO), ('21labs-orizzontale-per-fondo-chiaro.svg', PETROLIO, NERO, NERO)]:
    wm, xfine = wordmark(150, 100, 112, c21, clabs)
    scrivi(nome, xfine + 10, 130, simbolo(5, 5, 120, fondo=fondo, id_='o') + wm)
# verticale
wm, xf = wordmark(0, 0, 90, PETROLIO_CHIARO, CREMA)
larg = xf
wm, xf = wordmark((max(larg, 120) - larg) / 2, 250, 90, PETROLIO_CHIARO, CREMA)
scrivi('21labs-verticale-per-fondo-scuro.svg', max(larg, 120), 262, simbolo((max(larg, 120) - 120) / 2, 0, 120, id_='v') + wm)
print('ok', round(xfine))
