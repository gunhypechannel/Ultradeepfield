const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader', '--autoplay-policy=no-user-gesture-required'] });
  const ctx = await b.newContext({ viewport: { width: 430, height: 932 }, hasTouch: true, isMobile: true }); const pg = await ctx.newPage(); const errs = [];
  pg.on('pageerror', e => errs.push(e.message)); pg.on('requestfailed', r => { if (/voice\//.test(r.url())) errs.push('voice req failed ' + r.url()); });
  await pg.addInitScript(() => { const A = window.Audio; window.__played = []; window.Audio = function (src) { const a = new A(src); window.__played.push(String(src).replace(/^.*voice\//, '')); return a; }; });
  await pg.route('**/three.min.js', r => r.fulfill({ path: '../gt/threelib/three.min.js', contentType: 'application/javascript' })); await pg.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
  await pg.goto('http://localhost:8123/index.html', { waitUntil: 'commit' }).catch(() => {});
  await pg.waitForSelector('#udfAuth form', { timeout: 300000 }); await pg.evaluate(() => document.querySelector('#udfAuth [data-a=up]').click()); await pg.waitForTimeout(300);
  await pg.fill('#udfAuth input[name=n]', 'Voice ' + Math.floor(Math.random() * 1e4)); await pg.fill('#udfAuth input[name=e]', 'v' + Date.now() + '@t.io'); await pg.fill('#udfAuth input[name=p]', 'secret123'); await pg.evaluate(() => document.querySelector('#udfAuth form').requestSubmit());
  await pg.waitForFunction(() => window.__dbg && window.__dbg.G && window.__dbg.G.ready, null, { timeout: 300000, polling: 1000 });
  const E = c => pg.evaluate(c => window.__dbg.ev(c), c); const log = [];
  for (let k = 0; k < 60; k++) { const st = await pg.evaluate(() => ({ old: !!document.querySelector('#oldw'), fac: !!document.querySelector('.sheet [data-act="facPick"]'), adv: !!document.querySelector('#adv'), battle: !!window.__dbg.battle, txt: (document.querySelector('#advt') || {}).textContent || '' }));
    if (st.old) await pg.evaluate(() => document.querySelector('#oldw [data-act="oldNo"]')?.click());
    else if (st.fac) await pg.evaluate(() => document.querySelector('.sheet [data-act="facPick"]')?.click());
    else if (st.battle) await pg.evaluate(() => { try { window.__dbg.closeBattle(); } catch (e) {} });
    else if (st.adv) { log.push(st.txt.slice(0, 50)); await pg.waitForTimeout(1500); await pg.evaluate(() => document.querySelector('#adv .adv')?.click()); }
    else if (k > 12) break; await pg.waitForTimeout(800); }
  await pg.waitForTimeout(3000);
  const r = await E(`JSON.stringify({ clips: VOICE.clips ? Object.keys(VOICE.clips).length : 0, on: VOICE.on, step: S.tut.i, btn: !!document.querySelector('[data-act="voiceToggle"]') || 'n/a' })`);
  console.log('STATE', r); console.log('ADVISOR LINES SHOWN', log.length); console.log('CLIPS PLAYED', JSON.stringify(await pg.evaluate(() => window.__played)));
  const keys = await E(`JSON.stringify([...INTRO_PRE, ...INTRO_POST, ...INTRO, TUT[0].say].map(s => voiceKey(s)))`); console.log('EXPECTED', keys);
  console.log('ERRORS', JSON.stringify(errs.slice(0, 5))); await b.close(); })();
