import sys, os, re, urllib.parse, segno
S, O = sys.argv[1], sys.argv[2]
NUM = '393471903026'
def wa(testo): return 'https://wa.me/' + NUM + '?text=' + urllib.parse.quote(testo)
def qr(url):
    q = segno.make(url, error='m')
    svg = q.svg_inline(dark='#201D1C', light=None, border=0, scale=1, omitsize=True)
    return svg.replace('<svg ', '<svg class="qr-svg" '), q.version
def logo(nome):
    s = open(os.path.join(O, 'logo', nome)).read()
    return re.sub(r'width="[^"]*" height="[^"]*"', '', s, count=1).replace('<svg ', '<svg class="logo" ')
SIMB, ORIZ = logo('21labs-simbolo.svg'), logo('21labs-orizzontale-per-fondo-scuro.svg')
BASE = '''<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><style>
@font-face { font-family: Anton; src: url(Anton.woff); }
@font-face { font-family: Poppins; src: url(Poppins-400.woff); font-weight: 400; }
@font-face { font-family: Poppins; src: url(Poppins-500.woff); font-weight: 500; }
@page { size: %(w)smm %(h)smm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { -webkit-print-color-adjust: exact; print-color-adjust: exact; background: #201D1C; }
body { font-family: Poppins, sans-serif; color: #F2EDE9; }
.pagina { width: %(w)smm; height: %(h)smm; position: relative; overflow: hidden; background: #201D1C; page-break-after: always; }
.puntini { position: absolute; inset: 0; background-image: radial-gradient(rgba(242,237,233,0.08) 0.25mm, transparent 0.3mm); background-size: 2.6mm 2.6mm; }
.alone { position: absolute; inset: 0; background: radial-gradient(70%% 60%% at 50%% 115%%, rgba(62,135,150,0.45), transparent 70%%); }
.qr { background: #F2EDE9; border-radius: 1.6mm; display: grid; place-items: center; }
.qr-svg { display: block; width: 100%%; height: 100%%; }
.titolo { font-family: Anton; text-transform: uppercase; letter-spacing: 0.02em; line-height: 1; }
.petrolio { color: #6FB3C2; } .grigio { color: #A9A09A; }
%(css)s
</style></head><body>%(body)s</body></html>'''
def pagina(nome, w, h, css, body):
    open(os.path.join(S, 'stampa', nome + '.html'), 'w').write(BASE % {'w': w, 'h': h, 'css': css, 'body': body})
B = 3  # abbondanza biglietto (mm)
q_big, v1 = qr(wa('Ciao 21Labs! (biglietto)'))
pagina('biglietto', 85 + 2 * B, 55 + 2 * B, '''
.f-logo { position: absolute; left: 50%; top: 22.5mm; transform: translateX(-50%); width: 46mm; }
.f-logo .logo { width: 100%; height: auto; display: block; }
.f-motto { position: absolute; left: 0; right: 0; top: 37.5mm; text-align: center; font-size: 8.4pt; }
.f-servizi { position: absolute; left: 0; right: 0; bottom: 8mm; text-align: center; font-size: 5.6pt; letter-spacing: 0.06em; text-transform: uppercase; }
.r-sx { position: absolute; left: 8mm; top: 9mm; width: 46mm; }
.r-sx .logo { width: 30mm; height: auto; display: block; }
.r-sx .eti { margin-top: 1.6mm; font-size: 5.6pt; letter-spacing: 0.08em; text-transform: uppercase; }
.r-dati { position: absolute; left: 8mm; bottom: 8.5mm; display: grid; gap: 1.25mm; font-size: 6.6pt; line-height: 1.2; }
.r-dati div { display: grid; grid-template-columns: 11mm auto; }
.r-dati b { font-weight: 500; color: #A9A09A; font-size: 5.2pt; letter-spacing: 0.08em; text-transform: uppercase; padding-top: 0.35mm; }
.r-qr { position: absolute; right: 8mm; top: 9.5mm; width: 25mm; height: 25mm; padding: 2mm; }
.r-qr-testo { position: absolute; right: 8mm; width: 25mm; top: 36mm; text-align: center; font-size: 5.6pt; line-height: 1.25; }
.r-linea { position: absolute; left: 8mm; right: 8mm; top: 48.6mm; height: 0.25mm; background: linear-gradient(90deg, #3E8796, rgba(62,135,150,0)); opacity: 0; }
''', f'''
<div class="pagina"><div class="puntini"></div><div class="alone"></div>
  <div class="f-logo">{ORIZ}</div>
  <p class="f-motto titolo petrolio">Lavora anche quando sei chiuso.</p>
  <p class="f-servizi grigio">Siti · E-commerce · Gestionali · Automazioni · Centralino IA</p>
</div>
<div class="pagina"><div class="puntini" style="opacity:.6"></div>
  <div class="r-sx">{ORIZ}<p class="eti grigio">Agenzia web a Napoli</p></div>
  <div class="r-dati">
    <div><b>Tel</b><span>+39 347 190 3026</span></div>
    <div><b>Email</b><span>21labsweb@gmail.com</span></div>
    <div><b>Sito</b><span>www.21labs.it</span></div>
    <div><b>Studio</b><span>Viale Raffaello 15, 80129 Napoli</span></div>
  </div>
  <div class="r-qr qr">{q_big}</div>
  <p class="r-qr-testo">Inquadra e scrivici<br><span class="petrolio">su WhatsApp</span></p>
</div>''')
A = 2  # abbondanza adesivi (mm)
q_tondo, v2 = qr(wa('Ciao 21Labs! (adesivo)'))
pagina('adesivo-tondo-60mm', 60 + 2 * A, 60 + 2 * A, '''
.cerchio { position: absolute; left: 2mm; top: 2mm; width: 60mm; height: 60mm; border-radius: 50%; }
.t-alto { position: absolute; left: 0; right: 0; top: 8mm; text-align: center; font-size: 15pt; }
.t-qr { position: absolute; left: 50%; top: 16.6mm; transform: translateX(-50%); width: 27mm; height: 27mm; padding: 2.2mm; }
.t-basso { position: absolute; left: 0; right: 0; top: 45.4mm; text-align: center; font-size: 6.4pt; letter-spacing: 0.06em; text-transform: uppercase; }
.t-logo { position: absolute; left: 50%; top: 49.8mm; transform: translateX(-50%); width: 16mm; }
.t-logo .logo { width: 100%; height: auto; display: block; }
''', f'''<div class="pagina"><div class="puntini"></div><div class="alone"></div>
  <p class="t-alto titolo petrolio">Scansiona</p>
  <div class="t-qr qr">{q_tondo}</div>
  <p class="t-basso">e scrivici su WhatsApp</p>
  <div class="t-logo">{ORIZ}</div>
</div>''')
q_quad, v3 = qr(wa('Ciao 21Labs! (bozza 499)'))
pagina('adesivo-quadrato-50mm', 50 + 2 * A, 50 + 2 * A, '''
.q-titolo { position: absolute; left: 6mm; top: 6.5mm; font-size: 17pt; line-height: 0.98; }
.q-sotto { position: absolute; left: 6mm; top: 25.5mm; width: 21mm; font-size: 6pt; line-height: 1.3; }
.q-qr { position: absolute; right: 6mm; bottom: 6mm; width: 19mm; height: 19mm; padding: 1.6mm; }
.q-logo { position: absolute; left: 6mm; bottom: 7mm; width: 20mm; }
.q-logo .logo { width: 100%; height: auto; display: block; }
''', f'''<div class="pagina"><div class="puntini"></div><div class="alone"></div>
  <p class="q-titolo titolo">Il tuo sito<br><span class="petrolio">da 499 €</span></p>
  <p class="q-sotto grigio">Prima vedi la bozza, gratis. Poi decidi.</p>
  <div class="q-qr qr">{q_quad}</div>
  <div class="q-logo">{ORIZ}</div>
</div>''')
q_vet, v4 = qr(wa('Ciao 21Labs! (vetrina)'))
pagina('adesivo-vetrina-80x30mm', 80 + 2 * A, 30 + 2 * A, '''
.v-simb { position: absolute; left: 6mm; top: 7mm; width: 20mm; }
.v-simb .logo { width: 100%; height: auto; display: block; }
.v-testo { position: absolute; left: 30mm; top: 8.3mm; }
.v-testo .eti { font-size: 5.6pt; letter-spacing: 0.08em; text-transform: uppercase; }
.v-testo .titolo { font-size: 15pt; margin-top: 1mm; }
.v-testo .sito { font-size: 6pt; margin-top: 1.2mm; }
.v-qr { position: absolute; right: 6mm; top: 7mm; width: 20mm; height: 20mm; padding: 1.6mm; }
''', f'''<div class="pagina"><div class="puntini"></div><div class="alone" style="background:radial-gradient(60% 90% at 0% 100%, rgba(62,135,150,.4), transparent 70%)"></div>
  <div class="v-simb">{SIMB}</div>
  <div class="v-testo"><p class="eti grigio">Sito web realizzato da</p><p class="titolo"><span class="petrolio">21</span>Labs</p><p class="sito grigio">www.21labs.it</p></div>
  <div class="v-qr qr">{q_vet}</div>
</div>''')
print('versioni QR', v1, v2, v3, v4)
