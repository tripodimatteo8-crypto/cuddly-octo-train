import sys, os, re, urllib.parse, segno
S, T = sys.argv[1], sys.argv[2]
def logo(n): return re.sub(r'width="[^"]*" height="[^"]*"', '', open(os.path.join(T, 'logo', n)).read(), count=1).replace('<svg ', '<svg class="logo" ')
URL = 'https://wa.me/393471903026?text=' + urllib.parse.quote('Ciao 21Labs! (biglietto)')
def qr(dark): return segno.make(URL, error='m').svg_inline(dark=dark, light=None, border=0, scale=1, omitsize=True).replace('<svg ', '<svg class="qr-svg" ')
BASE = '''<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><style>
@font-face { font-family: A; src: url(Archivo-400.woff); font-weight: 400; }
@font-face { font-family: A; src: url(Archivo-500.woff); font-weight: 500; }
@font-face { font-family: AX; src: url(ArchivoExp-600.woff); font-weight: 600; }
@font-face { font-family: AX; src: url(ArchivoExp-800.woff); font-weight: 800; }
@page { size: 91mm 61mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { -webkit-print-color-adjust: exact; print-color-adjust: exact; background: #121114; }
body { font-family: A, sans-serif; color: #EDE8E3; }
.pagina { width: 91mm; height: 61mm; position: relative; overflow: hidden; background: #121114; page-break-after: always; }
.sf { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.logo { display: block; width: 100%; height: auto; }
.eti { font-family: AX; font-weight: 600; font-size: 4.6pt; letter-spacing: .14em; text-transform: uppercase; }
.dati { position: absolute; display: grid; gap: 1.3mm; font-size: 6.6pt; line-height: 1.2; }
.dati div { display: grid; grid-template-columns: 11mm auto; }
.dati b { font-family: AX; font-weight: 600; font-size: 4.4pt; letter-spacing: .14em; padding-top: .5mm; }
.qr-svg { display: block; width: 100%; height: 100%; }
@@CSS@@
</style></head><body>@@BODY@@</body></html>'''
DATI = lambda c: f'<div><b style="color:{c}">TEL</b><span>+39 347 190 3026</span></div><div><b style="color:{c}">EMAIL</b><span>21labsweb@gmail.com</span></div><div><b style="color:{c}">SITO</b><span>www.21labs.it</span></div>'
def retro_scuro():
    return f'''<div class="pagina">
  <div style="position:absolute;left:8mm;top:9mm;width:30mm">{logo('1-scritta-crema.svg')}</div>
  <p class="eti" style="position:absolute;left:8mm;top:15mm;color:#918C8F">Studio digitale · Napoli</p>
  <div class="dati" style="left:8mm;bottom:9mm">{DATI('#918C8F')}</div>
  <div style="position:absolute;right:8mm;top:9mm;width:23mm;height:23mm;background:#EDE8E3;padding:1.8mm;border-radius:1mm">{qr('#121114')}</div>
  <p class="eti" style="position:absolute;right:8mm;width:23mm;top:34.5mm;text-align:center;color:#EDE8E3">Scrivici su<br><span style="color:#EA6F41">WhatsApp</span></p>
  <span style="position:absolute;right:8mm;bottom:9.4mm;width:2.2mm;height:2.2mm;border-radius:50%;background:#EA6F41"></span></div>'''
def retro_crema():
    return f'''<div class="pagina" style="background:#EDE8E3;color:#121114">
  <div style="position:absolute;left:8mm;top:9mm;width:30mm">{logo('1-scritta-nero.svg')}</div>
  <p class="eti" style="position:absolute;left:8mm;top:15mm;color:#6E686B">Studio digitale · Napoli</p>
  <div class="dati" style="left:8mm;bottom:9mm">{DATI('#6E686B')}</div>
  <div style="position:absolute;right:8mm;top:9mm;width:22mm;height:22mm">{qr('#121114')}</div>
  <p class="eti" style="position:absolute;right:8mm;width:22mm;top:33.5mm;text-align:center">Scrivici su<br><span style="color:#C9502F">WhatsApp</span></p>
  <span style="position:absolute;right:8mm;bottom:9.4mm;width:2.2mm;height:2.2mm;border-radius:50%;background:#EA6F41"></span></div>'''
def scrivi(n, body): open(os.path.join(S, 'stampa-t', n + '.html'), 'w').write(BASE.replace('@@CSS@@', '').replace('@@BODY@@', body))
scrivi('termica-calore', f'''<div class="pagina"><img class="sf" src="biglietto-a.jpg">
  <div style="position:absolute;left:8mm;top:9mm;width:26mm">{logo('1-scritta-crema.svg')}</div>
  <p class="eti" style="position:absolute;left:8mm;top:14.6mm;color:#B9B2AE">Studio digitale · Napoli</p></div>''' + retro_scuro())
scrivi('termica-banda', f'''<div class="pagina"><img class="sf" src="biglietto-b.jpg">
  <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:36mm">{logo('2-blocco-crema.svg')}</div></div>''' + retro_crema())
scrivi('termica-figura', f'''<div class="pagina"><img class="sf" src="biglietto-c.jpg">
  <div style="position:absolute;left:8mm;top:9mm;width:28mm">{logo('3-punto-caldo-crema.svg')}</div>
  <p style="position:absolute;left:8mm;bottom:9mm;font-family:AX;font-weight:800;font-size:8.6pt;line-height:1.12;letter-spacing:-.01em">Il digitale<br>che lavora<br>per te.</p></div>''' + retro_scuro())
print('ok')
