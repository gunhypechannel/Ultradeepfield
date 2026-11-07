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
  const A = await player('A'), B = await player('B'), C = await player('C');
  await boot(A, 'up', 'Alpha Mail', 'alpha@test.io'); await boot(B, 'up', 'Bravo Mail', 'bravo@test.io'); await boot(C, 'up', 'Charlie Mail', 'charlie@test.io');
  const ua = await A.E('G.me'), ub = await B.E('G.me'), uc = await C.E('G.me');
  ok('all three online', await A.E('G.mode === "online"') && await B.E('G.mode === "online"') && await C.E('G.mode === "online"'));
  await wait(A, `!!G.players["${ub}"] && !!G.players["${uc}"]`, 40000);
  await A.E(`ACT.befriend({ u: "${ub}" }); ACT.befriend({ u: "${uc}" }); 1`); await A.waitForTimeout(800);
  ok('A has 2 friends', await A.E(`(S.friends || []).length === 2`), await A.E('JSON.stringify(S.friends)'));
  // alliance: A founds, B joins (C stays out)
  await A.E(`for (const k in B) S.b[k] = Math.max(S.b[k] || 0, 12); for (const k in S.r) S.r[k] = Math.max(S.r[k] || 0, 6); advance(now()); S.res.m = S.res.c = S.res.g = 9e5; dirty(); 1`);
  await A.E(`document.body.insertAdjacentHTML("beforeend", '<input id="alname" value="Mail Legion"><input id="altag" value="ML">'); S.spent = Math.max(S.spent || 0, 3e6); ACT.allyCreate(); 1`); // a commander past level 3
  ok('A founded an alliance', await wait(A, `!!S.ally && !!G.alliances[S.ally]`), await A.E('JSON.stringify({ ally: S.ally, lvl: cmdLevel(score()), res: S.res, toasts: [...document.querySelectorAll(".toast")].map(t => t.textContent).slice(-3) })'));
  const al = await A.E('S.ally'); await wait(B, `!!G.alliances["${al}"]`, 30000); await B.E(`ACT.allyJoin({ id: "${al}" }); 1`);
  ok('B joined', await wait(A, `!!(G.alliances["${al}"].members || {})["${ub}"]`, 30000));
  // the UI: Mail tab → 📣 Mail all → Mail all friends → type → Send
  await A.E(`ACT.nav({ v: "mail" }); 1`); await A.waitForTimeout(800);
  ok('Mail screen shows a Mail all button', await A.evaluate(() => [...document.querySelectorAll('[data-act="mailNew"]')].some(b => /Mail all/.test(b.textContent))));
  await A.evaluate(() => [...document.querySelectorAll('[data-act="mailNew"]')].find(b => /Mail all/.test(b.textContent)).click()); await A.waitForTimeout(800);
  const btns = await A.evaluate(() => [...document.querySelectorAll('.sheet [data-act="mailAllOpen"]')].map(b => b.textContent.trim() + (b.disabled ? ' (off)' : '')));
  ok('chat shows Mail all friends · 2 and Mail all alliance · 1', btns.some(x => /friends · 2/.test(x)) && btns.some(x => /alliance · 1/.test(x)), btns);
  await A.evaluate(() => document.querySelector('.sheet [data-act="mailAllOpen"][data-g="f"]').click()); await A.waitForTimeout(600);
  ok('compose lists the friends', await A.evaluate(() => /Bravo Mail/.test(document.querySelector('.sheet').textContent) && /Charlie Mail/.test(document.querySelector('.sheet').textContent)), await A.evaluate(() => document.querySelector('.sheet').textContent.slice(0, 300)));
  await A.fill('.sheet #chatin', 'Fleet meeting at 8!'); await A.evaluate(() => document.querySelector('.sheet [data-act="chatSend"]').click());
  for (const [pg, n] of [[B, 'B'], [C, 'C']]) ok(n + ' got the friends mail', await wait(pg, `JSON.stringify(CHAT.dms || {}).includes("Fleet meeting at 8!")`, 30000), await pg.E('JSON.stringify(CHAT.dms || {}).slice(0, 200)'));
  ok('the mail is marked "to all friends"', await B.E(`Object.values(CHAT.dms).some(c => c.m.some(m => m.x === "Fleet meeting at 8!" && m.bc === "f"))`));
  await B.E(`ACT.dmOpen({ u: "${ua}" }); 1`); await B.waitForTimeout(800);
  ok('B sees the 📣 label in the conversation', await B.evaluate(() => /Sent to all friends/.test((document.querySelector('.sheet') || {}).textContent || '')));
  // too soon again: blocked with a clear message
  await A.E(`ACT.mailAllOpen({ g: "a" }); 1`); await A.waitForTimeout(500); await A.fill('.sheet #chatin', 'Alliance rally'); await A.evaluate(() => document.querySelector('.sheet [data-act="chatSend"]').click()); await A.waitForTimeout(2500);
  ok('second mail-all within 2 minutes is held back', !(await B.E(`JSON.stringify(CHAT.dms || {}).includes("Alliance rally")`)) && await A.evaluate(() => [...document.querySelectorAll('.toast')].some(t => /mail everyone again/.test(t.textContent))));
  await A.E(`S.mailAllAt = 0; 1`); await A.evaluate(() => document.querySelector('.sheet [data-act="chatSend"]').click());
  ok('B got the alliance mail', await wait(B, `Object.values(CHAT.dms).some(c => c.m.some(m => m.x === "Alliance rally" && m.bc === "a"))`, 30000));
  ok('C (not in the alliance) did not', !(await C.E(`JSON.stringify(CHAT.dms || {}).includes("Alliance rally")`)));
  console.log('\n' + res.filter(r => r.startsWith('FAIL')).length + ' FAIL / ' + res.length); console.log('ERRORS:\n' + (errs.slice(0, 12).join('\n') || 'none'));
  await b.close(); })().catch(e => { console.log('CRASH', e.message); console.log(res.join('\n')); console.log(errs.slice(0, 8).join('\n')); process.exit(1); });
