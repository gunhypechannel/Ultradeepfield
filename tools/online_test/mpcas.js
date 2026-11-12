// v483 phase 1 check: two players hit the same world boss at the same moment (lease off, slowed reads) and both hits must land.
// Also runs the old path (no compare-and-set) as a control, which loses one. Same setup as mp.js (fakesrv.js + index2.html).
// Two (and three) real browsers in one shared galaxy (fakesrv.js): sign-up, joining, chat, DMs, alliances, espionage, PvP, report
// sharing, a second device on the same account, sign out / in. Prints PASS / FAIL per check.
const { chromium, devices } = require('playwright');
const URL = 'http://localhost:8123/index2.html', res = [], errs = [];
const ok = (name, cond, info) => { res.push((cond ? 'PASS ' : 'FAIL ') + name + (cond ? '' : '  ' + JSON.stringify(info).slice(0, 400))); console.log(res[res.length - 1]); };
(async () => {
  const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'] });
  async function player(tag) {
    const ctx = await b.newContext({ viewport: { width: 412, height: 900 }, hasTouch: true, isMobile: true, deviceScaleFactor: 1, userAgent: devices['Pixel 7'].userAgent }), pg = await ctx.newPage();
    pg.on('pageerror', e => errs.push(tag + ': ' + e.message + ' @ ' + ((e.stack || '').split('\n')[1] || '').trim()));
    await pg.route('**/three.min.js', r => r.fulfill({ path: '../gt/threelib/three.min.js', contentType: 'application/javascript' })); await pg.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
    pg.E = c => pg.evaluate(c => window.__dbg.ev(c), c); pg.tag = tag; pg.ctx = ctx; return pg; }
  async function boot(pg, mode, name, email) {
    await pg.goto(URL, { waitUntil: 'commit' }).catch(() => {});
    await pg.waitForSelector('#udfAuth form', { timeout: 180000 });
    if (mode === 'up') { await pg.evaluate(() => document.querySelector('#udfAuth [data-a=up]').click()); await pg.waitForTimeout(300); await pg.fill('#udfAuth input[name=n]', name); }
    await pg.fill('#udfAuth input[name=e]', email); await pg.fill('#udfAuth input[name=p]', 'secret123'); await pg.evaluate(() => document.querySelector('#udfAuth form').requestSubmit());
    await pg.waitForFunction(() => window.__dbg && window.__dbg.G && window.__dbg.G.ready, null, { timeout: 240000, polling: 1000 });
    for (let k = 0; k < 40; k++) { // a new player: the old-server card, the faction, the opening briefing and battle
      const st = await pg.evaluate(() => ({ celeb: !!document.querySelector('#celeb'), old: !!document.querySelector('#oldw'), fac: !!document.querySelector('.sheet [data-act="facPick"]'), adv: !!document.querySelector('#adv'), battle: !!window.__dbg.battle }));
      if (st.celeb) await pg.evaluate(() => document.querySelector('#celeb [data-act="celebX"]')?.click());
      else if (st.old) await pg.evaluate(() => document.querySelector('#oldw [data-act="oldNo"]')?.click());
      else if (st.fac) await pg.evaluate(() => document.querySelector('.sheet [data-act="facPick"]')?.click());
      else if (st.battle) await pg.evaluate(() => { try { window.__dbg.closeBattle(); } catch (e) {} });
      else if (st.adv) await pg.evaluate(() => { const a = document.querySelector('#adv .adv') || document.querySelector('#adv'); a?.click(); });
      else if (k > 6) break; await pg.waitForTimeout(700); }
  }
  const wait = async (pg, code, ms = 20000) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { try { if (await pg.E(code)) return true; } catch (e) {} await pg.waitForTimeout(600); } return false; };
  const A = await player('A'), B = await player('B');
  await boot(A, 'up', 'Alpha One', 'alpha@test.io'); await boot(B, 'up', 'Bravo Two', 'bravo@test.io');
  const ua = await A.E('G.me'), ub = await B.E('G.me');
  ok('both online', (await A.E('G.mode')) === 'online' && (await B.E('G.mode')) === 'online');
  const key = await A.E(`["brd","tyr","wym","col","ovl","dev","war"].find(k => wbOn(k, now())) || ""`); ok('a world boss is live: ' + key, !!key);
  const fleet = tag => `({ id: "tf${tag}" + Date.now(), wb: "${key}", arrive: now(), tt: 60000, phase: "out", n: { battleship: 3000, destroyer: 4000, bomber: 3000 } })`;
  const srv = async () => (await (await fetch('http://localhost:8124/dump')).json());
  const run = async (label, noLease, noCas) => {
    for (const pg of [A, B]) await pg.E(`(() => { const P = Object.getPrototypeOf(adb().doc("event/wboss")); if (!P.__acq) { P.__acq = P.acquire; P.__cas = P.cas; P.__getV = P.getV; P.__get = P.get; }
      const slow = f => function () { return f.call(this).then(s => new Promise(r => setTimeout(() => r(s), 1500))); };
      P.acquire = ${noLease ? 'async () => ({ acquired: true })' : 'P.__acq'}; P.cas = ${noCas ? 'undefined' : 'P.__cas'}; P.getV = ${noCas ? 'undefined' : 'slow(P.__getV)'}; P.get = slow(P.__get); return 1; })()`);
    await A.E(`(async () => { const P = Object.getPrototypeOf(adb().doc("event/wboss")), r = adb().doc("event/wboss"), s = await P.__get.call(r), d = s.exists ? s.data() : null; if (!d) return 0; d.hp["${key}"] = WB_SEG; if (d.dmg) d.dmg["${key}"] = {}; if (d.dead) delete d.dead["${key}"]; if (d.last) delete d.last["${key}"]; await r.set(d); return 1; })()`);
    await A.waitForTimeout(800);
    const d0 = (await srv()).T['event/wboss']; const hp0 = d0 ? d0.data.hp[key] : null, dm0 = d0 && d0.data.dmg[key] ? d0.data.dmg[key] : {};
    await Promise.all([A.E(`(window.__f = ${fleet('A')}, wbResolve(window.__f).then(() => 1))`), B.E(`(window.__f = ${fleet('B')}, wbResolve(window.__f).then(() => 1))`)]);
    await A.waitForTimeout(1500); const d1 = (await srv()).T['event/wboss'].data, sA = await A.E(`(S.reports.find(r => r.wb) || {}).wbSeg`), sB = await B.E(`(S.reports.find(r => r.wb) || {}).wbSeg`);
    const repA = await A.E(`JSON.stringify(S.reports.filter(r => r.wb).slice(0, 1).map(r => r.wbSeg))`), repB = await B.E(`JSON.stringify(S.reports.filter(r => r.wb).slice(0, 1).map(r => r.wbSeg))`);
    const segA = JSON.parse(repA)[0], segB = JSON.parse(repB)[0], dA = (d1.dmg[key][ua] || 0) - (dm0[ua] || 0), dB = (d1.dmg[key][ub] || 0) - (dm0[ub] || 0), conf = (await srv()).LOG.filter(l => l[1] === 'cas').length;
    const tot = (segA[0] - segA[1]) + (segB[0] - segB[1]);
    console.log(label, JSON.stringify({ hp0, hp1: d1.hp[key], segA, segB, dA, dB, casWrites: conf, conflictsA: await A.E('CRUMBS.ev.filter(e => /cas conflict/.test(e[1])).length'), conflictsB: await B.E('CRUMBS.ev.filter(e => /cas conflict/.test(e[1])).length') }));
    return { both: dA > 0 && dB > 0, hpOk: hp0 == null || d1.hp[key] === hp0 - dA - dB };
  };
  await run('warm-up', true, false); const r1 = await run('with CAS, no lease', true, false); ok('with compare-and-set, both hits land on the record', r1.both && r1.hpOk, r1);
  const r2 = await run('no CAS, no lease (the old risk)', true, true); console.log('control (expected to lose a hit sometimes):', JSON.stringify(r2));
  const r3 = await run('with CAS and the lease (normal)', false, false); ok('normal path: both land', r3.both && r3.hpOk, r3);
  console.log('errs', JSON.stringify(errs.slice(0, 6))); await b.close(); process.exit(0); })();
