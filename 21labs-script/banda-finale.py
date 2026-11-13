import sys, os, re, urllib.parse, segno
BG = os.environ.get('BG', 'biglietto-b.jpg'); PUNTO = os.environ.get('PUNTO', '#EA6F41'); WA = os.environ.get('WA', 'eti-whatsapp-nero.svg'); NOME = os.environ.get('NOME', 'banda-finale')
S, T = sys.argv[1], sys.argv[2]
B = os.path.join(T, 'logo', 'banda')
def svg(n, stile=''): return re.sub(r'width="[^"]*" height="[^"]*"', '', open(os.path.join(B, n)).read(), count=1).replace('<svg ', f'<svg style="display:block;{stile}" ')
URL = 'https://wa.me/393471903026?text=' + urllib.parse.quote('Ciao 21Labs! (biglietto)')
QR = segno.make(URL, error='m').svg_inline(dark='#121114', light=None, border=0, scale=1, omitsize=True).replace('<svg ', '<svg class="qr-svg" ')
BASE = open(os.path.join(S, 'stampa-t', 'termica-banda.html')).read(); testa = BASE[:BASE.index('<body>') + 6]
riga = lambda e, v: f'<div style="display:grid;grid-template-columns:11mm auto;align-items:center"><span>{svg("eti-" + e + "-nero.svg", "height:1.45mm;width:auto")}</span><span>{v}</span></div>'
corpo = f'''<div class="pagina"><img class="sf" src="{BG}">
  <div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:40mm">{svg('6-michroma-bold-crema.svg', 'width:100%;height:auto')}</div></div>
<div class="pagina" style="background:#EDE8E3;color:#121114">
  <div style="position:absolute;left:8mm;top:9mm">{svg('nome-nero.svg', 'height:8.6mm;width:auto')}</div>
  <div style="position:absolute;left:8mm;bottom:9mm;display:grid;gap:1.5mm;font-size:6.6pt;line-height:1.2">
    {riga('tel', '+39 347 190 3026')}{riga('email', '21labsweb@gmail.com')}{riga('sito', 'www.21labs.it')}</div>
  <div style="position:absolute;right:8mm;top:9mm;width:22mm;height:22mm">{QR}</div>
  <div style="position:absolute;right:8mm;width:22mm;top:33.6mm;display:grid;justify-items:center;gap:1mm">{svg('eti-scrivimi-su-nero.svg', 'height:1.45mm;width:auto')}{svg(WA, 'height:1.45mm;width:auto')}</div>
  <div style="position:absolute;right:8mm;bottom:9.1mm;display:flex;align-items:center;gap:1.5mm"><span style="width:1.9mm;height:1.9mm;border-radius:50%;background:{PUNTO}"></span>{svg('21labs-michroma-nero.svg', 'height:2.3mm;width:auto')}</div>
</div>'''
open(os.path.join(S, 'stampa-t', NOME + '.html'), 'w').write(testa + corpo + '</body></html>')
print('ok')
