import sys, os, re, segno
S, T = sys.argv[1], sys.argv[2]
def qr(url): return segno.make(url, error='m').svg_inline(dark='#121114', light=None, border=0, scale=1, omitsize=True).replace('<svg ', '<svg style="display:block;width:100%;height:100%" ')
def svg(n, stile): return re.sub(r'width="[^"]*" height="[^"]*"', '', open(os.path.join(T, 'logo', 'banda', n)).read(), count=1).replace('<svg ', f'<svg style="display:block;{stile}" ')
Q = lambda fonte: qr('https://www.21labs.it/?utm_source=' + fonte)
def pagina(n, w, h, body):
    open(os.path.join(S, 'stampa-t', n + '.html'), 'w').write(f'''<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><style>
@font-face {{ font-family: MI; src: url(Michroma-400.woff); }}
@font-face {{ font-family: A; src: url(Archivo-500.woff); }}
@page {{ size: {w}mm {h}mm; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; background: #121114; }}
.pagina {{ width: {w}mm; height: {h}mm; position: relative; overflow: hidden; background: #121114; color: #EDE8E3; }}
.sf {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.mi {{ font-family: MI; text-transform: uppercase; -webkit-text-stroke: .035em currentColor; letter-spacing: .08em; }}
.qr {{ position: absolute; background: #EDE8E3; border-radius: 1.2mm; }}
</style></head><body><div class="pagina">{body}</div></body></html>''')
pagina('adesivo-tondo-60mm', 64, 64, f'''<img class="sf" src="adesivo-tondo.jpg">
  <div style="position:absolute;left:50%;top:9.5mm;transform:translateX(-50%)">{svg('21labs-michroma-crema.svg', 'height:3mm;width:auto')}</div>
  <div class="qr" style="left:50%;top:17.5mm;transform:translateX(-50%);width:27mm;height:27mm;padding:2.1mm">{Q('adesivo-tondo')}</div>
  <p class="mi" style="position:absolute;left:0;right:0;top:47.4mm;text-align:center;font-size:5pt">Inquadra · www.21labs.it</p>
  <p class="mi" style="position:absolute;left:0;right:0;top:51.6mm;text-align:center;font-size:3.8pt;color:#C9C2BD">Digital studio · Napoli</p>''')
pagina('adesivo-quadrato-50mm', 54, 54, f'''<img class="sf" src="adesivo-quadrato.jpg">
  <div style="position:absolute;left:6mm;top:13.2mm;width:30mm">{svg('6-michroma-bold-crema.svg', 'width:100%;height:auto')}</div>
  <div class="qr" style="right:6mm;bottom:6mm;width:20mm;height:20mm;padding:1.6mm">{Q('adesivo-quadrato')}</div>
  <p class="mi" style="position:absolute;left:6mm;bottom:6.4mm;width:20mm;font-size:4.4pt;line-height:1.5">Il tuo sito<br>da 499 euro<br><span style="color:#C9C2BD">21labs.it</span></p>''')
pagina('adesivo-vetrina-80x30mm', 84, 34, f'''<img class="sf" src="adesivo-vetrina.jpg">
  <p class="mi" style="position:absolute;left:6mm;top:7.4mm;font-size:3.9pt;color:#EDE8E3">Sito web realizzato da</p>
  <div style="position:absolute;left:6mm;top:12.6mm;width:34mm">{svg('6-michroma-bold-crema.svg', 'width:100%;height:auto')}</div>
  <p class="mi" style="position:absolute;left:6mm;bottom:6.6mm;font-size:3.9pt;color:#C9C2BD">www.21labs.it</p>
  <div class="qr" style="right:6mm;top:7mm;width:20mm;height:20mm;padding:1.6mm">{Q('adesivo-vetrina')}</div>''')
print('ok')
