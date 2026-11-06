const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader','--use-gl=angle','--use-angle=swiftshader'] }); const pg = await (await b.newContext({ ...devices['iPhone 15 Pro Max'] })).newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.route('**/three.min.js', r => r.fulfill({ path: 'threelib/three.min.js', contentType: 'application/javascript' })); await pg.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
  pg.goto('file://' + process.cwd() + '/index.html', { waitUntil: 'commit' }).catch(() => {});
  await pg.waitForFunction(() => window.__dbg && window.__dbg.S && window.__dbg.G.list, null, { timeout: 180000, polling: 1000 }); await pg.waitForTimeout(2500);
  const E = c => pg.evaluate(c => window.__dbg.ev(c), c);
  await pg.evaluate(() => { document.querySelectorAll('#authw,#adv').forEach(e => e.remove()); window.__dbg.closeAll(); });
  console.log(await E(require('fs').readFileSync('c307.txt', 'utf8'))); await E("(() => { const y = Object.values(YB).filter(y => y.lvl >= 5).pop(); S.pyr = {}; openSheet({ type: 'pyramid', id: y.id }); })()"); await pg.waitForTimeout(1500); await pg.evaluate(() => { const b = document.querySelector('.sheet [data-act=pkeff]'); if (b) b.scrollIntoView(); document.querySelectorAll('#adv,#coach,.toast').forEach(e => e.remove()); }); await pg.screenshot({ path: '../pyr307.png' });
  console.log(errs.slice(0, 3).join('\n') || 'no errors'); await b.close(); })();
