// v537 iPhone memory check. Serve a harness build (the one-file game with three.js routed locally) on http://localhost:8124/ and run:
//   node tools/ios_memcheck.js [threejs-path]
// It loads the game with an iPhone user agent and screen, switches base -> galaxy -> base -> mail, and fails unless: the map is never
// built in the background, only one 3D world is alive 10 s after each switch, the studio renderer is released when idle, and the
// drawing buffers stay inside the iPhone pixel budget.
const { chromium, devices } = require('playwright');
const THREE = process.argv[2] || 'threelib/three.min.js';
(async () => { const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'] });
  const c = await b.newContext({ ...devices['iPhone 13'] }); const pg = await c.newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.route('**/three.min.js', r => r.fulfill({ path: THREE, contentType: 'application/javascript' })); await pg.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
  pg.goto('http://localhost:8124/', { waitUntil: 'commit' }).catch(() => {}); await pg.waitForFunction(() => window.__dbg && window.__dbg.G.ready, null, { timeout: 240000, polling: 1000 });
  const E = q => pg.evaluate(q => window.__dbg.ev(q), q), fails = [];
  await E(`(() => { document.querySelectorAll('#authw,#adv,#advh,#celeb').forEach(e => e.remove()); advLines = null; S.tut.i = TUT.length; S.tut.k = "done"; S.fTour = 2; VOICE.on = false; return 1; })()`);
  const st = () => E(`JSON.stringify({ view, ios: IOS, mt: MEMT, gal: !!G3, col: !!C3, stu: !!STU, park: !!document.getElementById("mappark"), pr: [G3 && G3.renderer.getPixelRatio(), C3 && C3.renderer.getPixelRatio()], px: [G3, C3].filter(Boolean).map(W => { const gl = W.renderer.getContext(); return gl.drawingBufferWidth * gl.drawingBufferHeight; }) })`).then(JSON.parse);
  const step = async (v, wait) => { await E(`(ACT.nav({ v: "${v}" }), 1)`); await pg.waitForTimeout(wait); const s = await st(); console.log(v, JSON.stringify(s)); return s; };
  let s = await step('base', 20000); if (!s.ios) fails.push('not detected as iOS'); if (s.park || s.gal) fails.push('map built in the background on iOS');
  s = await step('galaxy', 14000); if (s.col) fails.push('base still alive 10 s after opening the galaxy');
  s = await step('base', 14000); if (s.gal) fails.push('galaxy still alive 10 s after going home');
  s = await step('mail', 14000); if (s.gal) fails.push('galaxy alive on mail after the base was used last');
  await E(`(studio(), G.stuT = Date.now() - 20000, 1)`); await pg.waitForTimeout(4500); s = await st(); if (s.stu) fails.push('studio not released when idle');
  await step('base', 8000); s = await st(); const budget = [1e6, .75e6, .55e6, .4e6][s.mt] * 1.05; if (s.px.some(p => p > budget)) fails.push(`drawing buffer over the budget: ${s.px} > ${budget}`);
  const beat = await E(`(crumbBeat(), JSON.stringify({ ctx: CRUMBS.beat.ctx, fbMB: CRUMBS.beat.fbMB, mt: CRUMBS.beat.mt }))`); console.log('beat', beat);
  if (errs.length) fails.push('page errors: ' + errs.slice(0, 3).join(' | '));
  console.log(fails.length ? 'FAIL\n- ' + fails.join('\n- ') : 'PASS'); await b.close(); process.exit(fails.length ? 1 : 0); })();
