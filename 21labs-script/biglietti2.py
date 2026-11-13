import sys, os, re, urllib.parse, segno
S, O = sys.argv[1], sys.argv[2]
def qr(url, dark='#201D1C'):
    return segno.make(url, error='m').svg_inline(dark=dark, light=None, border=0, scale=1, omitsize=True).replace('<svg ', '<svg class="qr-svg" ')
def logo(nome): return re.sub(r'width="[^"]*" height="[^"]*"', '', open(os.path.join(O, 'logo', nome)).read(), count=1).replace('<svg ', '<svg class="logo" ')
SCURO, CHIARO = logo('21labs-orizzontale-per-fondo-scuro.svg'), logo('21labs-orizzontale-per-fondo-chiaro.svg')
URL = 'https://wa.me/393471903026?text=' + urllib.parse.quote('Ciao 21Labs! (biglietto)')
Q_CREMA_BOX, Q_DIRETTO = qr(URL), qr(URL)
BASE = '''<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><style>
@font-face { font-family: Anton; src: url(Anton.woff); }
@font-face { font-family: Poppins; src: url(Poppins-400.woff); font-weight: 400; }
@font-face { font-family: Poppins; src: url(Poppins-500.woff); font-weight: 500; }
@page { size: 91mm 61mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { -webkit-print-color-adjust: exact; print-color-adjust: exact; background: #201D1C; }
body { font-family: Poppins, sans-serif; color: #F2EDE9; }
.pagina { width: 91mm; height: 61mm; position: relative; overflow: hidden; background: #201D1C; page-break-after: always; }
.titolo { font-family: Anton; text-transform: uppercase; letter-spacing: 0.02em; line-height: 1; }
.petrolio { color: #6FB3C2; } .grigio { color: #A9A09A; }
.logo { display: block; width: 100%; height: auto; }
.qr { background: #F2EDE9; border-radius: 1.6mm; padding: 2mm; } .qr-svg { display: block; width: 100%; height: 100%; }
.dati { position: absolute; display: grid; gap: 1.25mm; font-size: 6.6pt; line-height: 1.2; }
.dati div { display: grid; grid-template-columns: 11mm auto; }
.dati b { font-weight: 500; font-size: 5.2pt; letter-spacing: 0.08em; text-transform: uppercase; padding-top: 0.35mm; }
@@CSS@@
</style></head><body>@@BODY@@</body></html>'''
DATI = lambda colore_b: f'''<div><b style="color:{colore_b}">Tel</b><span>+39 347 190 3026</span></div>
<div><b style="color:{colore_b}">Email</b><span>21labsweb@gmail.com</span></div>
<div><b style="color:{colore_b}">Sito</b><span>www.21labs.it</span></div>'''
RETRO_SCURO = f'''<div class="pagina"><div style="position:absolute;inset:0;background-image:radial-gradient(rgba(242,237,233,.06) .25mm,transparent .3mm);background-size:2.6mm 2.6mm"></div>
  <div style="position:absolute;left:8mm;top:9mm;width:30mm">{SCURO}<p class="grigio" style="margin-top:1.6mm;font-size:5.6pt;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap">Agenzia web a Napoli</p></div>
  <div class="dati" style="left:8mm;bottom:9mm">{DATI('#A9A09A')}</div>
  <div class="qr" style="position:absolute;right:8mm;top:9.5mm;width:25mm;height:25mm">{Q_CREMA_BOX}</div>
  <p style="position:absolute;right:8mm;width:25mm;top:36mm;text-align:center;font-size:5.6pt;line-height:1.25">Inquadra e scrivici<br><span class="petrolio">su WhatsApp</span></p></div>'''
RETRO_CREMA = f'''<div class="pagina" style="background:#F2EDE9;color:#201D1C">
  <div style="position:absolute;left:8mm;top:9mm;width:30mm">{CHIARO}<p style="margin-top:1.6mm;font-size:5.6pt;letter-spacing:.08em;text-transform:uppercase;color:#6B635E;white-space:nowrap">Agenzia web a Napoli</p></div>
  <div class="dati" style="left:8mm;bottom:9mm;color:#201D1C">{DATI('#6B635E')}</div>
  <div style="position:absolute;right:8mm;top:9mm;width:23mm;height:23mm">{Q_DIRETTO}</div>
  <p style="position:absolute;right:8mm;width:23mm;top:34.5mm;text-align:center;font-size:5.6pt;line-height:1.25">Inquadra e scrivici<br><span style="color:#275B66;font-weight:500">su WhatsApp</span></p>
  <div style="position:absolute;left:0;right:0;bottom:0;height:3mm;background:linear-gradient(90deg,#275B66,#6FB3C2)"></div></div>'''
def scrivi(nome, css, body): open(os.path.join(S, 'stampa', nome + '.html'), 'w').write(BASE.replace('@@CSS@@', css).replace('@@BODY@@', body))

# 1. ALBA — foto a tutta pagina
scrivi('biglietto-alba', '', f'''<div class="pagina">
  <img src="sfondo-alba.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(32,29,28,.75) 0%,rgba(32,29,28,0) 45%,rgba(32,29,28,0) 70%,rgba(32,29,28,.6) 100%)"></div>
  <div style="position:absolute;left:8mm;top:8mm;width:34mm">{SCURO}</div>
  <p class="titolo" style="position:absolute;left:8mm;bottom:8mm;font-size:10pt;line-height:1.05">Lavora anche<br><span class="petrolio">quando sei chiuso.</span></p>
</div>''' + RETRO_SCURO)

# 2. 21 IN VETRO — render 3D a tutta pagina
scrivi('biglietto-21-vetro', '', f'''<div class="pagina">
  <img src="sfondo-21.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
  <div style="position:absolute;left:8mm;top:9mm;width:30mm">{SCURO}</div>
  <p class="grigio" style="position:absolute;left:8mm;top:20.5mm;font-size:5.6pt;letter-spacing:.08em;text-transform:uppercase">Agenzia web a Napoli</p>
  <p class="titolo" style="position:absolute;left:8mm;bottom:8.5mm;font-size:10pt;line-height:1.05">Siti, gestionali<br>e automazioni.<br><span class="petrolio">Prezzo fisso.</span></p>
</div>''' + RETRO_SCURO)

# 3. TIPOGRAFICA — 21 gigante tagliato dai bordi, retro crema
scrivi('biglietto-tipografico', '', f'''<div class="pagina">
  <p class="titolo" style="position:absolute;right:-6mm;top:-14.5mm;font-size:236pt;line-height:1;letter-spacing:-0.01em;background:linear-gradient(160deg,#8CC6D0 0%,#3E8796 45%,#1A3238 100%);-webkit-background-clip:text;background-clip:text;color:transparent">21</p>
  <p class="titolo" style="position:absolute;left:8mm;bottom:8mm;font-size:30pt;letter-spacing:.04em">LABS</p>
  <p class="grigio" style="position:absolute;left:8.4mm;bottom:20.5mm;font-size:5.6pt;letter-spacing:.1em;text-transform:uppercase">Agenzia web · Napoli</p>
</div>''' + RETRO_CREMA)
print('ok')

# ===== Seconda serie: linee =====
# 4. MAPPA del Vesuvio a curve di livello
scrivi('biglietto-mappa', '', f'''<div class="pagina">
  <img src="sfondo-mappa.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
  <div style="position:absolute;left:8mm;top:9mm;width:30mm">{SCURO}</div>
  <p class="titolo" style="position:absolute;left:8mm;bottom:13mm;font-size:10pt;line-height:1.05">Lavora anche<br><span class="petrolio">quando sei chiuso.</span></p>
  <p class="grigio" style="position:absolute;left:8mm;bottom:8mm;font-size:5.4pt;letter-spacing:.1em">40,82° N · 14,43° E · NAPOLI</p>
</div>''' + RETRO_SCURO)

# 5. SCIE di luce sul vulcano
scrivi('biglietto-scie', '', f'''<div class="pagina">
  <img src="sfondo-scie.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover">
  <div style="position:absolute;left:8mm;top:8.5mm;width:30mm">{SCURO}</div>
  <p class="titolo" style="position:absolute;right:8mm;bottom:8mm;font-size:10pt;line-height:1.05;text-align:right">Il digitale<br><span class="petrolio">che lavora per te.</span></p>
</div>''' + RETRO_CREMA)

# 6. NOTIFICHE delle 07:30
ICONE = {
 'borsa': '<svg viewBox="0 0 18 18" fill="none" stroke="#0F1535" stroke-width="1.8" stroke-linejoin="round"><path d="M3.5 6.5h11l-1 8.5h-9z"/><path d="M6.5 6.5V5a2.5 2.5 0 0 1 5 0v1.5" stroke-linecap="round"/></svg>',
 'agenda': '<svg viewBox="0 0 18 18" fill="none" stroke="#0F1535" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"><rect x="3" y="4.5" width="12" height="10.5" rx="2"/><path d="M3 8h12M6.5 3v3M11.5 3v3"/></svg>',
 'fulmine': '<svg viewBox="0 0 18 18" fill="#0F1535"><path d="M10.2 2 4 10h4l-.6 6L14 8h-4z"/></svg>'}
def notifica(icona, colore, titolo, testo_, ora):
    return f'''<div style="display:grid;grid-template-columns:5mm 1fr auto;gap:2mm;align-items:center;background:rgba(242,237,233,.1);border:0.2mm solid rgba(242,237,233,.12);border-radius:2.4mm;padding:1.7mm 2.2mm">
      <span style="width:5mm;height:5mm;border-radius:1.3mm;background:{colore};display:grid;place-items:center"><span style="width:3.2mm;height:3.2mm;display:block">{ICONE[icona].replace('<svg ', '<svg style="display:block;width:100%;height:100%" ')}</span></span>
      <span style="font-size:5.4pt;line-height:1.25"><b style="font-weight:500">{titolo}</b><br><span style="color:#D9D2CC">{testo_}</span></span>
      <span style="font-size:4.6pt;color:#A9A09A;align-self:start">{ora}</span></div>'''
scrivi('biglietto-notifiche', '', f'''<div class="pagina">
  <div style="position:absolute;inset:0;background:radial-gradient(80% 90% at 85% 50%, rgba(62,135,150,.35), transparent 70%)"></div>
  <p class="titolo" style="position:absolute;left:8mm;top:9mm;font-size:34pt;letter-spacing:.01em">07:30</p>
  <p class="petrolio" style="position:absolute;left:8.3mm;top:23mm;font-size:6.4pt">Mentre eri chiuso…</p>
  <div style="position:absolute;left:8mm;bottom:8.5mm;width:24mm">{SCURO}</div>
  <div style="position:absolute;right:7mm;top:9mm;width:41mm;display:grid;gap:1.6mm">
    {notifica('borsa','#FF9A62','Negozio online','Nuovo ordine da 64 €','23:47')}
    {notifica('agenda','#FFD08A','Prenotazioni','Sabato alle 10:30, confermata','01:12')}
    {notifica('fulmine','#8CC6D0','Automazione','Preventivo inviato a un cliente','06:58')}
  </div>
</div>''' + RETRO_CREMA)

# 7. ORIZZONTE a righe: sole fatto di archi, orizzonte e riflessi
archi = ''.join(f'<path d="M{45.5-r:.2f} 37 A{r:.2f} {r:.2f} 0 0 1 {45.5+r:.2f} 37" fill="none" stroke="#6FB3C2" stroke-width="0.45" opacity="{0.25+0.75*(1-i/7):.2f}"/>' for i, r in enumerate([3.5 + 2.35 * k for k in range(8)]))
riflessi = ''.join(f'<rect x="{45.5-w/2:.2f}" y="{39.5+i*2.4:.2f}" width="{w:.2f}" height="0.45" rx="0.22" fill="#6FB3C2" opacity="{0.6-i*0.09:.2f}"/>' for i, w in enumerate([44, 34, 25, 17, 10, 5]))
scrivi('biglietto-orizzonte', '', f'''<div class="pagina">
  <svg viewBox="0 0 91 61" style="position:absolute;inset:0;width:100%;height:100%">{archi}
    <rect x="0" y="36.8" width="91" height="0.5" fill="#6FB3C2"/>{riflessi}</svg>
  <div style="position:absolute;left:8mm;top:8.5mm;width:24mm">{SCURO}</div>
  <p class="grigio" style="position:absolute;right:8mm;top:9.6mm;font-size:5.4pt;letter-spacing:.1em;text-transform:uppercase">Agenzia web · Napoli</p>
  <p class="titolo" style="position:absolute;left:0;right:0;bottom:7.5mm;text-align:center;font-size:8pt;letter-spacing:.08em">Lavora anche <span class="petrolio">quando sei chiuso.</span></p>
</div>''' + RETRO_SCURO)
print('ok serie 2')
