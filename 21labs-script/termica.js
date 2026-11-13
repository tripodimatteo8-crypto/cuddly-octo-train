const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [dir, out, prev] = process.argv.slice(2);
  const b = await chromium.launch();
  const lavori = [['termica-calore', 91, 61], ['termica-banda', 91, 61], ['termica-figura', 91, 61]];
  for (const [n, w, h] of lavori) {
    const pg = await b.newPage({ viewport: { width: Math.round(w * 3.7795), height: Math.round(h * 3.7795) }, deviceScaleFactor: 300 / 96 });
    await pg.goto('file://' + path.join(dir, n + '.html')); await pg.evaluate(() => document.fonts.ready);
    await pg.pdf({ path: path.join(out, n + '.pdf'), preferCSSPageSize: true, printBackground: true });
    const pagine = await pg.locator('.pagina').count();
    for (let i = 0; i < pagine; i++) await pg.locator('.pagina').nth(i).screenshot({ path: path.join(prev, `${n}${pagine > 1 ? (i ? '-retro' : '-fronte') : ''}.png`) });
    console.log(n, 'pagine', pagine, 'font ok', await pg.evaluate(() => document.fonts.check('800 12px AX') && document.fonts.check('12px A')));
    await pg.close();
  }
  await b.close();
})();
