const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'] });
  const ctx = await b.newContext({ viewport: { width: 430, height: 932 }, hasTouch: true, isMobile: true });
  const route = async pg => { await pg.route('**/three.min.js', r => r.fulfill({ path: '../gt/threelib/three.min.js', contentType: 'application/javascript' })); await pg.route(/fonts\.(googleapis|gstatic)/, r => r.abort()); };
  const ready = pg => pg.waitForFunction(() => window.__dbg && window.__dbg.G && window.__dbg.G.ready && window.__dbg.ev('store.ready'), null, { timeout: 300000, polling: 1000 });
  let pg = await ctx.newPage(); await route(pg); const E = (pg, c) => pg.evaluate(c => window.__dbg.ev(c), c);
  await pg.goto('http://localhost:8123/index.html', { waitUntil: 'commit' }).catch(() => {});
  await pg.waitForSelector('#udfAuth form', { timeout: 300000 }); await pg.evaluate(() => document.querySelector('#udfAuth [data-a=up]').click()); await pg.waitForTimeout(300);
  await pg.fill('#udfAuth input[name=n]', 'Back ' + Math.floor(Math.random() * 1e4)); await pg.fill('#udfAuth input[name=e]', 'b' + Date.now() + '@t.io'); await pg.fill('#udfAuth input[name=p]', 'secret123'); await pg.evaluate(() => document.querySelector('#udfAuth form').requestSubmit());
  await ready(pg); await pg.waitForTimeout(3000);
  await E(pg, `(() => { const o = document.querySelector('#oldw [data-act="oldNo"]'); if (o) o.click(); })()`); await pg.waitForTimeout(1500);
  await E(pg, `(() => { const b = document.querySelector('.sheet [data-act="facPick"]'); if (b) b.click(); })()`); await pg.waitForTimeout(2000);
  await E(pg, `S.tut.i = 10; S.say.length = 0; dirty(); flush()`); await pg.waitForTimeout(5000);
  console.log('before', await E(pg, `JSON.stringify({ i: S.tut.i, m: Math.round(S.res.m), cb: S.comeback || 0, uid: S.uid })`));
  await pg.close();
  for (const [k, shift] of [[1, 0], [2, 2 * 864e5], [3, 2 * 864e5]]) { // 1: same day (no gift), 2: two days later (gift), 3: again (no second gift)
    pg = await ctx.newPage(); await route(pg);
    await pg.addInitScript(s => { const D = Date, off = s; Date = class extends D { constructor(...a) { if (!a.length) super(D.now() + off); else super(...a); } static now() { return D.now() + off; } }; }, shift);
    await pg.goto('http://localhost:8123/index.html', { waitUntil: 'commit' }).catch(() => {}); await ready(pg); await pg.waitForTimeout(6000);
    console.log('open', k, await E(pg, `JSON.stringify({ i: S.tut.i, m: Math.round(S.res.m), cb: S.comeback || 0, away: Math.round((G.awayMs || 0) / 36e5) + 'h', celeb: (S.celeb || []).map(c => c.k).concat(document.querySelector('#celeb') ? ['SHOWN:' + document.querySelector('#celeb').textContent.slice(0, 80)] : []) })`));
    await E(pg, 'dirty(); flush()'); await pg.waitForTimeout(4000); await pg.close(); }
  await b.close(); })();
