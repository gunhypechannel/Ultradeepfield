const { chromium, devices } = require('playwright');
(async () => { const cfg = JSON.parse(process.env.CFG); const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader','--use-gl=angle','--use-angle=swiftshader'] }); const pg = await (await b.newContext({ ...devices['iPhone 15 Pro Max'], deviceScaleFactor: 2 })).newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message + ' | ' + (e.stack || '').split('\n')[1]));
  await pg.route('**/three.min.js', r => r.fulfill({ path: 'threelib/three.min.js', contentType: 'application/javascript' })); await pg.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
  pg.goto('file://' + process.cwd() + '/index.html', { waitUntil: 'commit' }).catch(() => {});
  await pg.waitForFunction(() => window.__dbg && window.__dbg.S && window.__dbg.G.list, null, { timeout: 180000, polling: 1000 }); await pg.waitForTimeout(2500);
  await pg.evaluate(() => { document.querySelectorAll('#authw,#adv').forEach(e => e.remove()); window.__dbg.closeAll(); });
  const E = c => pg.evaluate(c => window.__dbg.ev(c), c);
  for (const [fac, L, built, nm] of [cfg]) {
    await E(`(() => { closeSheet(); S.faction = '${fac}'; S.spent = 3e6; const f = fsOf(); f.built = ${built}; S.b.flagDock = ${L}; fsBump(); ACT.nav({ v: 'base' }); })()`);
    await pg.waitForTimeout(14000); await E(`(() => { C3.v.tx = -0.4; C3.v.tz = -13; C3.v.zoom = 1.6; })()`); await pg.waitForTimeout(3500); await E('closeSheet()'); await pg.waitForTimeout(800);
    await pg.evaluate(() => { try { advLines = []; } catch (e) {} document.querySelectorAll('#adv,#coach,.toast').forEach(e => e.remove()); }); await pg.screenshot({ path: '../d303_' + nm + '.png', timeout: 60000 }); }
  console.log(errs.slice(0, 6).join('\n') || 'no errors'); await b.close(); })();
