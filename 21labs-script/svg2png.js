const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [src, out, w, h, bg] = process.argv.slice(2);
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: +w, height: +h } });
  const svg = fs.readFileSync(src, 'utf8').replace(/width="[^"]*" height="[^"]*"/, `width="100%" height="100%"`);
  await pg.setContent(`<body style="margin:0;background:${bg || 'transparent'};width:${w}px;height:${h}px">${svg}</body>`);
  await pg.screenshot({ path: out, omitBackground: !bg, clip: { x: 0, y: 0, width: +w, height: +h } }); await b.close(); })();
