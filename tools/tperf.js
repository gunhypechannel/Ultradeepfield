const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader','--use-gl=angle','--use-angle=swiftshader'] }); const pg = await (await b.newContext({ ...devices['iPhone 15 Pro Max'] })).newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.route('**/three.min.js', r => r.fulfill({ path: 'threelib/three.min.js', contentType: 'application/javascript' })); await pg.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
  pg.goto('file://' + process.cwd() + '/index.html', { waitUntil: 'commit' }).catch(() => {});
  await pg.waitForFunction(() => window.__dbg && window.__dbg.S && window.__dbg.G.list, null, { timeout: 180000, polling: 1000 }); await pg.waitForTimeout(2500);
  const E = c => pg.evaluate(c => window.__dbg.ev(c), c);
  await E(`(() => { ACT.nav({ v: 'galaxy' }); })()`); await pg.waitForTimeout(6000);
  console.log(await E(require('fs').readFileSync('c304.txt', 'utf8')));
  console.log(errs.slice(0, 3).join('\n') || 'no errors'); await b.close(); })();
