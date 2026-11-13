import sys, os, math
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
S, O = sys.argv[1], sys.argv[2]
ANTON = TTFont(S + '/font/Anton.woff'); POP6 = TTFont(S + '/font/Poppins-600.woff'); POP5 = TTFont(S + '/font/Poppins-500.woff')
TC, TS, CR, NE, GR = '#6FB3C2', '#275B66', '#F2EDE9', '#201D1C', '#A9A09A'

def larghezza(txt, font, size, track=0.0):
    hm, cm, upm = font['hmtx'], font.getBestCmap(), font['head'].unitsPerEm
    return sum(hm[cm[ord(c)]][0] for c in txt) * size / upm + track * size * (len(txt) - 1)
def testo(txt, font, size, x, base, fill, track=0.0, centro=False):
    gs, cm, hm, upm = font.getGlyphSet(), font.getBestCmap(), font['hmtx'], font['head'].unitsPerEm
    k = size / upm
    if centro: x -= larghezza(txt, font, size, track) / 2
    pen = SVGPathPen(gs)
    for ch in txt:
        g = cm[ord(ch)]; gs[g].draw(TransformPen(pen, (k, 0, 0, -k, x, base))); x += hm[g][0] * k + track * size
    return f'<path d="{pen.getCommands()}" fill="{fill}"/>'
def testo_cerchio(txt, font, size, cx, cy, r, fill, track=0.0, inizio=None):
    """Testo lungo un cerchio, letto in senso orario, centrato in alto."""
    gs, cm, hm, upm = font.getGlyphSet(), font.getBestCmap(), font['hmtx'], font['head'].unitsPerEm
    k = size / upm; tot = larghezza(txt, font, size, track)
    ang = -tot / (2 * r) if inizio is None else inizio
    pen = SVGPathPen(gs)
    for ch in txt:
        g = cm[ord(ch)]; adv = hm[g][0] * k
        phi = ang + adv / (2 * r); c, s = math.cos(phi), math.sin(phi)
        tx, ty = cx + r * s, cy - r * c
        ox = -hm[g][0] / 2  # centra il glifo sul punto
        gs[g].draw(TransformPen(pen, (c * k, s * k, s * k, -c * k, tx + c * k * ox, ty + s * k * ox)))
        ang += (adv + track * size) / r
    return f'<path d="{pen.getCommands()}" fill="{fill}"/>'
def grad(id_, a=TC, b=TS, verticale=True):
    x2, y2 = ('0', '1') if verticale else ('1', '0')
    return f'<linearGradient id="{id_}" x1="0" y1="0" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
def svg(nome, w, h, corpo, defs=''):
    open(os.path.join(O, nome), 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}"><defs>{defs}</defs>{corpo}</svg>')

# 1. ELEMENTO — tessera da tavola periodica: 21 / LABS / NA (Napoli)
def elemento(c_testo=CR, c_acc=TC, fondo=NE, bordo=TS):
    return (f'<rect x="4" y="4" width="232" height="232" rx="22" fill="{fondo}" stroke="{bordo}" stroke-width="4"/>'
            + testo('NA', ANTON, 30, 210, 50, c_acc) .replace('M', 'M', 1)
            + testo('21', ANTON, 128, 120, 170, c_acc, centro=True)
            + testo('LABS', ANTON, 40, 120, 212, c_testo, track=0.12, centro=True)
            + testo('agenzia web', POP5, 13, 28, 46, GR))
# "NA" allineato a destra
def elemento_svg(nome, c_testo, fondo):
    w = larghezza('NA', ANTON, 30)
    corpo = (f'<rect x="4" y="4" width="232" height="232" rx="22" fill="{fondo}" stroke="{TS}" stroke-width="4"/>'
             + testo('NA', ANTON, 30, 212 - w, 50, TC if fondo == NE else TS)
             + testo('agenzia web', POP5, 13, 28, 46, GR)
             + testo('21', ANTON, 128, 120, 168, TC if fondo == NE else TS, centro=True)
             + testo('LABS', ANTON, 40, 120, 212, c_testo, track=0.12, centro=True))
    svg(nome, 240, 240, corpo)
elemento_svg('1-elemento-scuro.svg', CR, NE); elemento_svg('1-elemento-chiaro.svg', NE, CR)

# 2. SOLE 21 — il 21 è il sole che sorge sull'orizzonte, con riflessi
def sole_svg(nome, c_scritta, fondo):
    W = 520; cx, oriz = 110, 128
    corpo = (f'<clipPath id="sopra"><rect x="0" y="0" width="{W}" height="{oriz}"/></clipPath>'
             f'<g clip-path="url(#sopra)"><circle cx="{cx}" cy="{oriz}" r="92" fill="url(#gs)"/>'
             + testo('21', ANTON, 78, cx, oriz - 8, fondo, centro=True) + '</g>'
             f'<rect x="10" y="{oriz}" width="200" height="3" fill="{TC}"/>'
             f'<rect x="60" y="{oriz+14}" width="100" height="3" rx="1.5" fill="{TC}" opacity=".45"/>'
             f'<rect x="80" y="{oriz+26}" width="60" height="3" rx="1.5" fill="{TC}" opacity=".28"/>'
             f'<rect x="98" y="{oriz+38}" width="24" height="3" rx="1.5" fill="{TC}" opacity=".16"/>'
             + testo('21LABS', ANTON, 96, 240, 124, c_scritta, track=0.02)
             + testo('AGENZIA WEB · NAPOLI', POP5, 15, 243, 156, GR, track=0.18))
    svg(nome, W, 180, corpo, grad('gs'))
sole_svg('2-sole-scuro.svg', CR, NE); sole_svg('2-sole-chiaro.svg', NE, CR)

# 3. CODICE — </21> + LABS
def codice_svg(nome, c_scritta, fondo):
    a = testo('<', ANTON, 110, 6, 120, TS if fondo == NE else TS)
    x = 6 + larghezza('<', ANTON, 110) + 4
    b = testo('21', ANTON, 110, x, 120, TC if fondo == NE else TS); x += larghezza('21', ANTON, 110) + 4
    c = testo('/>', ANTON, 110, x, 120, TS if fondo == NE else TS); x += larghezza('/>', ANTON, 110) + 14
    d = testo('LABS', ANTON, 110, x, 120, c_scritta); x += larghezza('LABS', ANTON, 110)
    cur = f'<rect x="{x+10:.1f}" y="40" width="10" height="80" fill="{TC}"/>'
    svg(nome, x + 30, 140, a + b + c + d + cur)
codice_svg('3-codice-scuro.svg', CR, NE); codice_svg('3-codice-chiaro.svg', NE, CR)

# 4. LINEA — Vesuvio e sole in un tratto, wordmark minuscolo Poppins
def linea_svg(nome, c_scritta, fondo):
    icona = (f'<circle cx="70" cy="74" r="22" fill="none" stroke="{TC}" stroke-width="7"/>'
             f'<path d="M8 120 C30 118 42 100 52 84 C56 78 61 77 64 81 L68 86 Q70 88 72 86 L76 81 C79 77 84 78 88 84 C98 100 110 118 132 120" '
             f'fill="{fondo}" stroke="{CR if fondo == NE else NE}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>'
             f'<path d="M8 134 H132" stroke="{TC}" stroke-width="7" stroke-linecap="round"/>')
    scritta = testo('21', POP6, 92, 160, 118, TC if fondo == NE else TS) + testo('labs', POP6, 92, 160 + larghezza('21', POP6, 92) + 2, 118, c_scritta)
    w = 160 + larghezza('21labs', POP6, 92) + 12
    svg(nome, w, 150, icona + scritta)
linea_svg('4-linea-scuro.svg', CR, NE); linea_svg('4-linea-chiaro.svg', NE, CR)

# 5. TIMBRO — sigillo rotondo con testo sul cerchio e alba al centro
def timbro_svg(nome, c_testo, fondo):
    cx = cy = 150
    frase = '21LABS · AGENZIA WEB · NAPOLI · '
    nat = larghezza(frase, ANTON, 26)
    tr = (2 * math.pi * 112 - nat) / (26 * len(frase))
    t = testo_cerchio(frase, ANTON, 26, cx, cy, 112, c_testo, track=tr, inizio=-larghezza('21LABS', ANTON, 26, tr) / (2 * 112))
    centro = (f'<clipPath id="tc"><rect x="0" y="0" width="300" height="{cy+14}"/></clipPath>'
              f'<circle cx="{cx}" cy="{cy+14}" r="54" fill="url(#gt)" clip-path="url(#tc)"/>'
              f'<path d="M86 {cy+14} C100 {cy+13} 110 {cy-2} 118 {cy-14} C121 {cy-19} 125 {cy-20} 128 {cy-16} L132 {cy-12} Q134 {cy-10.5} 136 {cy-12} L140 {cy-16} C143 {cy-20} 147 {cy-19} 150 {cy-14} C158 {cy-2} 168 {cy+13} 182 {cy+14} Z" fill="{fondo}" transform="translate({cx-134} 0)"/>'
              f'<rect x="{cx-62}" y="{cy+13}" width="124" height="3" fill="{TC}"/>'
              f'<rect x="{cx-34}" y="{cy+26}" width="68" height="3" rx="1.5" fill="{TC}" opacity=".45"/>'
              f'<rect x="{cx-18}" y="{cy+38}" width="36" height="3" rx="1.5" fill="{TC}" opacity=".25"/>')
    anelli = (f'<circle cx="{cx}" cy="{cy}" r="146" fill="{fondo}"/>'
              f'<circle cx="{cx}" cy="{cy}" r="140" fill="none" stroke="{TS}" stroke-width="3"/>'
              f'<circle cx="{cx}" cy="{cy}" r="96" fill="none" stroke="{TS}" stroke-width="2" opacity=".7"/>')
    svg(nome, 300, 300, anelli + t + centro, grad('gt'))
timbro_svg('5-timbro-scuro.svg', CR, NE); timbro_svg('5-timbro-chiaro.svg', NE, CR)
print('ok')
