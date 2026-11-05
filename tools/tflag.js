const { chromium, devices } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader','--use-gl=angle','--use-angle=swiftshader'] }); const pg = await (await b.newContext({ ...devices['iPhone 15 Pro Max'] })).newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message + ' ' + (e.stack||'').split('\n')[1]));
  await pg.route('**/three.min.js', r => r.fulfill({ path: 'threelib/three.min.js', contentType: 'application/javascript' })); await pg.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
  pg.goto('file://' + process.cwd() + '/index.html', { waitUntil: 'commit' }).catch(() => {});
  await pg.waitForFunction(() => window.__dbg && window.__dbg.S && window.__dbg.G.list, null, { timeout: 180000, polling: 1000 }); await pg.waitForTimeout(2500);
  const E = c => pg.evaluate(c => window.__dbg.ev(c), c);
  for (const fac of ['terran', 'solar', 'nyx', 'verdant']) { const u = await E(`(() => { const c = shipArt('flagship', '#55d6e8@${fac}', 'side'); return c && c.toDataURL ? c.toDataURL('image/png') : null; })()`);
    if (u) fs.writeFileSync('../ui300/side_' + fac + '.png', Buffer.from(u.split(',')[1], 'base64')); else console.log(fac, 'null'); }
  console.log(errs.slice(0, 3).join('\n') || 'no errors'); await b.close(); })();
