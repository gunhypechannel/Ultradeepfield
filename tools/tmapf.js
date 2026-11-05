const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader','--use-gl=angle','--use-angle=swiftshader'] }); const pg = await (await b.newContext({ ...devices['iPhone 15 Pro Max'], deviceScaleFactor: 2 })).newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message + ' ' + (e.stack||'').split('\n')[1]));
  await pg.route('**/three.min.js', r => r.fulfill({ path: 'threelib/three.min.js', contentType: 'application/javascript' })); await pg.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
  pg.goto('file://' + process.cwd() + '/index.html', { waitUntil: 'commit' }).catch(() => {});
  await pg.waitForFunction(() => window.__dbg && window.__dbg.S && window.__dbg.G.list, null, { timeout: 180000, polling: 1000 }); await pg.waitForTimeout(3000);
  await pg.evaluate(() => { document.querySelectorAll('#authw,#adv').forEach(e => e.remove()); window.__dbg.closeAll(); window.__dbg.G.owner = true; });
  const E = c => pg.evaluate(c => window.__dbg.ev(c), c);
  let n = 0; for (const fac of ['terran', 'solar', 'nyx', 'verdant']) {
    await E(`(() => { closeSheet(); S.fleets = S.fleets.filter(f => f.id !== 'fT'); S.faction = '${fac}'; S.spent = 3e6; fsOf().built = 1; fsBump(); const h = homePlanet(), p = G.list.find(q => q.id !== h.id && Math.hypot(q.x - h.x, q.y - h.y) > 40) || G.list[1]; const T = now(), tt = 3600e3;
      S.fleets.push({ id: 'fT', pid: p.id, mission: 'station', n: { cruiser: 6, fighter: 12 }, out: T - tt * .4, arrive: T + tt * .6, tt, back: T + tt * 1.6, loot: null, phase: 'out' }); try { if (G3) G3.fleetsSig = null; } catch (e) {} ACT.nav({ v: 'galaxy' }); })()`);
    await pg.waitForTimeout(4000); await E(`(() => { ACT.fleetFocus({ id: 'fT' }); G3.cam.goal = { dist: 9 }; })()`); await pg.waitForTimeout(6000);
    await pg.evaluate(() => { try { advLines = []; } catch (e) {} document.querySelectorAll('#adv,#coach,.sheet').forEach(e => e.remove()); }); await pg.screenshot({ path: '../m304_' + fac + '.png', timeout: 60000 }); }
  console.log(errs.slice(0, 4).join('\n') || 'no errors'); await b.close(); })();
