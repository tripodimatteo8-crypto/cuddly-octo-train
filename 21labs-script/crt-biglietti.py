import sys, os, urllib.parse, segno
S = sys.argv[1]
URL = 'https://wa.me/393471903026?text=' + urllib.parse.quote('Ciao 21Labs! (biglietto)')
QR = segno.make(URL, error='m').svg_inline(dark='#0B0E0E', light=None, border=0, scale=1, omitsize=True).replace('<svg ', '<svg style="display:block;width:100%;height:100%" ')
BASE = '''<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><style>
@font-face { font-family: Anton; src: url(Anton.woff); }
@font-face { font-family: A; src: url(Archivo-400.woff); font-weight: 400; }
@font-face { font-family: A; src: url(Archivo-500.woff); font-weight: 500; }
@page { size: 91mm 61mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { -webkit-print-color-adjust: exact; print-color-adjust: exact; background: #0B0E0E; }
body { font-family: A, sans-serif; color: #E4EFEA; }
.pagina { width: 91mm; height: 61mm; position: relative; overflow: hidden; background: #0B0E0E; page-break-after: always; }
.fosforo { font-family: Anton; text-transform: uppercase; line-height: 1; white-space: nowrap;
  background: linear-gradient(180deg, #B4E3CD 0%, #7FD0BF 35%, #5AB2A7 65%, #739CA9 100%); -webkit-background-clip: text; background-clip: text; color: transparent; }
.alone { position: absolute; filter: blur(2.2mm); opacity: .55; }
.righe { position: absolute; inset: 0; background: repeating-linear-gradient(90deg, rgba(11,14,14,.5) 0 .16mm, transparent .16mm .42mm); }
.vignetta { position: absolute; inset: 0; background: radial-gradient(115% 100% at 50% 50%, transparent 55%, rgba(0,0,0,.8) 100%); }
.eti { font-family: Anton; font-size: 5.6pt; letter-spacing: .14em; text-transform: uppercase; }
.dati { position: absolute; left: 8mm; bottom: 9mm; display: grid; gap: 1.3mm; font-size: 6.6pt; line-height: 1.2; }
.dati div { display: grid; grid-template-columns: 11mm auto; align-items: baseline; }
</style></head><body>@@BODY@@</body></html>'''
def doppio(stile, testo):  # testo con alone luminoso dietro
    return f'<p class="fosforo alone" style="{stile}">{testo}</p><p class="fosforo" style="position:absolute;{stile}">{testo}</p>'
def retro(scuro):
    bg, tx, gr, ac = ('#0B0E0E', '#E4EFEA', '#86999A', '#7FD0BF') if scuro else ('#E4EFEA', '#0B0E0E', '#5E6F70', '#2C8C86')
    qr = f'<div style="position:absolute;right:8mm;top:9mm;width:23mm;height:23mm;background:#E4EFEA;padding:1.8mm;border-radius:1mm">{QR}</div>' if scuro else f'<div style="position:absolute;right:8mm;top:9mm;width:22mm;height:22mm">{QR}</div>'
    return f'''<div class="pagina" style="background:{bg};color:{tx}">
  <p style="position:absolute;left:8mm;top:8.2mm;font-family:Anton;font-size:17pt;line-height:1.02;letter-spacing:.01em;text-transform:uppercase">Matteo<br>Tripodi</p>
  <div class="dati"><div><span class="eti" style="color:{gr}">Tel</span><span>+39 347 190 3026</span></div><div><span class="eti" style="color:{gr}">Email</span><span>21labsweb@gmail.com</span></div><div><span class="eti" style="color:{gr}">Sito</span><span>www.21labs.it</span></div></div>
  {qr}
  <p class="eti" style="position:absolute;right:8mm;width:23mm;top:34.6mm;text-align:center">Scrivimi su <span style="color:{ac}">WhatsApp</span></p>
  <p style="position:absolute;right:8mm;bottom:8.6mm;font-family:Anton;font-size:9pt;letter-spacing:.02em"><span style="color:{ac}">21</span>LABS</p></div>'''
def scrivi(n, body): open(os.path.join(S, 'stampa-c', n + '.html'), 'w').write(BASE.replace('@@BODY@@', body))
# 1. SCHERMO: 21LABS allungato a tutta pagina, come sul monitor
st = 'left:50%;top:50%;font-size:92pt;transform:translate(-50%,-50%) scale(.98,1.62)'
scrivi('crt-schermo', f'<div class="pagina">{doppio(st, "21LABS")}<div class="righe"></div><div class="vignetta"></div></div>' + retro(True))
# 2. VENTUNO: 21 gigante tagliato, scritta piccola
st = 'right:-3mm;top:50%;font-size:150pt;transform:translateY(-50%) scale(1,1.25)'
scrivi('crt-ventuno', f'''<div class="pagina">{doppio(st, "21")}<div class="righe"></div><div class="vignetta"></div>
  <p style="position:absolute;left:8mm;top:8.6mm;font-family:Anton;font-size:10pt;letter-spacing:.02em"><span style="color:#7FD0BF">21</span>LABS</p>
  <p class="eti" style="position:absolute;left:8mm;bottom:9mm;line-height:1.5;color:#B9CBC6">Digital studio<br>Napoli</p></div>''' + retro(False))
# 3. SEGNALE: scritta centrata piccola, banda di fosforo orizzontale
scrivi('crt-segnale', f'''<div class="pagina">
  <div style="position:absolute;left:-5mm;right:-5mm;top:21mm;height:19mm;background:linear-gradient(180deg,#B4E3CD,#5AB2A7 60%,#739CA9);filter:blur(3mm);opacity:.9"></div>
  <div class="righe"></div><div class="vignetta"></div>
  <p style="position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);text-align:center;font-family:Anton;font-size:26pt;letter-spacing:.04em;color:#0B0E0E">21LABS</p>
  <p class="eti" style="position:absolute;left:0;right:0;bottom:9mm;text-align:center;color:#B9CBC6">Digital studio · Napoli</p></div>''' + retro(True))
print('ok')
