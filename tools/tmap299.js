const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader','--use-gl=angle','--use-angle=swiftshader'] }); const pg = await (await b.newContext({ ...devices['iPhone 15 Pro Max'] })).newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message + ' | ' + (e.stack || '').split('\n')[1]));
  await pg.route('**/three.min.js', r => r.fulfill({ path: 'threelib/three.min.js', contentType: 'application/javascript' })); await pg.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
  pg.goto('file://' + process.cwd() + '/index.html', { waitUntil: 'commit' }).catch(() => {});
  await pg.waitForFunction(() => window.__dbg && window.__dbg.S && window.__dbg.G.list, null, { timeout: 180000, polling: 1000 }); await pg.waitForTimeout(2500);
  await pg.evaluate(() => { document.querySelectorAll('#authw,#adv').forEach(e => e.remove()); window.__dbg.closeAll(); });
  const E = c => pg.evaluate(c => window.__dbg.ev(c), c);
  await E(`(() => { ACT.nav({ v: 'galaxy' }); })()`); await pg.waitForTimeout(6000);
  for (const dist of [260, 120, 60, 420]) {
    await E(`(() => { const h = homePlanet(), q = P3(h, now()); S.caches = [{ id: 'kT', x: +(q.x + 14).toFixed(1), y: +(q.z + 6).toFixed(1), kind: 'm', at: now(), until: now() + 9e6 }]; G3.cam.follow = null; G3.cam.goal = null; G3.cam.tx = q.x; G3.cam.tz = q.z; G3.cam.dist = ${dist}; })()`);
    await pg.waitForTimeout(2500);
    const r = await E(`(() => { const h = G3.hits.find(x => x.cache), el = G3.renderer.domElement, R = el.getBoundingClientRect(); if (!h) return 'no cache hit'; const out = {};
      for (const [dx, dy] of [[0, 0], [14, 8], [22, 12], [30, 0]]) { const p = pick3(el, { clientX: R.left + h.x + dx, clientY: R.top + h.y + dy }); const bb = p.best; out[dx + ',' + dy] = bb ? (bb.cache ? 'cache' : bb.pl ? 'planet' : bb.nid ? 'field' : bb.xid ? 'pirate' : bb.fleet ? 'fleet' : bb.tid ? 'orbit' : 'other:' + (bb.id || '')) : 'none'; }
      const hp = homePlanet(); return JSON.stringify({ sr: h.sr, at: [Math.round(h.x), Math.round(h.y)], out }); })()`);
    console.log('dist', dist, r);
  }
  await E(`(() => { S.caches = []; })()`); await pg.waitForTimeout(800);
  console.log('planet still tappable:', await E(`(() => { const el = G3.renderer.domElement, R = el.getBoundingClientRect(), h = homePlanet(), q = P3(h, now()); V3.set(q.x, q.y, q.z).project(G3.camera); const sx = (V3.x * .5 + .5) * R.width, sy = (-V3.y * .5 + .5) * R.height; const p = pick3(el, { clientX: R.left + sx + 6, clientY: R.top + sy + 4 }); return p.best ? (p.best.pl ? 'planet ' + p.best.id : JSON.stringify(Object.keys(p.best))) : 'none'; })()`));
  await pg.screenshot({ path: '../d_map.png', timeout: 60000 });
  console.log(errs.slice(0, 6).join('\n') || 'no errors'); await b.close(); })();
