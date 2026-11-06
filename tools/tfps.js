const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader','--use-gl=angle','--use-angle=swiftshader'] }); const pg = await (await b.newContext({ ...devices['iPhone 15 Pro Max'] })).newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.route('**/three.min.js', r => r.fulfill({ path: 'threelib/three.min.js', contentType: 'application/javascript' })); await pg.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
  pg.goto('file://' + process.cwd() + '/index.html', { waitUntil: 'commit' }).catch(() => {});
  await pg.waitForFunction(() => window.__dbg && window.__dbg.S && window.__dbg.G.list, null, { timeout: 180000, polling: 1000 }); await pg.waitForTimeout(2500);
  await pg.evaluate(() => { document.querySelectorAll('#authw,#adv').forEach(e => e.remove()); window.__dbg.closeAll(); window.__dbg.G.owner = true; });
  const E = c => pg.evaluate(c => window.__dbg.ev(c), c);
  await E(`(() => { closeSheet(); ACT.nav({ v: 'galaxy' }); })()`); await pg.waitForTimeout(5000);
  if (process.env.DEMO) { await E('cubeDemoStart(20)'); await pg.waitForTimeout(8000); }
  const res = [];
  for (const dist of [60, 250]) { await E(`(() => { closeSheet(); G3.cam.dist = ${dist}; })()`); await pg.waitForTimeout(3000);
    const r = await pg.evaluate(() => new Promise(res => { const t0 = performance.now(); let n = 0, long = 0, last = t0; const f = () => { const t = performance.now(); if (t - last > 100) long++; last = t; n++; if (t - t0 < 8000) requestAnimationFrame(f); else res([n, long]); }; requestAnimationFrame(f); }));
    const cpu = await E(`(() => { const a = performance.now(); for (let i = 0; i < 20; i++) { try { G3.renderer.info.reset && 0; } catch (e) {} } return G3.renderer.info.render.calls + ' calls ' + G3.renderer.info.render.triangles + ' tris'; })()`);
    res.push('dist ' + dist + ': ' + (r[0] / 8).toFixed(1) + ' fps, long frames ' + r[1] + ', ' + cpu); }
  console.log(res.join(' | ')); console.log(errs.slice(0, 3).join('\n') || 'no errors'); await b.close(); })();
