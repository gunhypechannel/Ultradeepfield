// Two (and three) real browsers in one shared galaxy (fakesrv.js): sign-up, joining, chat, DMs, alliances, espionage, PvP, report
// sharing, a second device on the same account, sign out / in. Prints PASS / FAIL per check.
const { chromium, devices } = require('playwright');
const URL = 'http://localhost:8123/index2.html', res = [], errs = [];
const ok = (name, cond, info) => { res.push((cond ? 'PASS ' : 'FAIL ') + name + (cond ? '' : '  ' + JSON.stringify(info).slice(0, 400))); console.log(res[res.length - 1]); };
(async () => {
  const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'] });
  async function player(tag) {
    const ctx = await b.newContext({ ...devices['Pixel 7'] }), pg = await ctx.newPage();
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
      const st = await pg.evaluate(() => ({ old: !!document.querySelector('#oldw'), fac: !!document.querySelector('.sheet [data-act="facPick"]'), adv: !!document.querySelector('#adv'), battle: !!window.__dbg.battle }));
      if (st.old) await pg.evaluate(() => document.querySelector('#oldw [data-act="oldNo"]').click());
      else if (st.fac) await pg.evaluate(() => document.querySelector('.sheet [data-act="facPick"]').click());
      else if (st.battle) await pg.evaluate(() => window.__dbg.closeBattle());
      else if (st.adv) await pg.evaluate(() => { const a = document.querySelector('#adv'); a.click(); });
      else if (k > 6) break; await pg.waitForTimeout(700); }
  }
  const wait = async (pg, code, ms = 20000) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { try { if (await pg.E(code)) return true; } catch (e) {} await pg.waitForTimeout(600); } return false; };
  const A = await player('A'), B = await player('B');
  await boot(A, 'up', 'Alpha One', 'alpha@test.io'); await boot(B, 'up', 'Bravo Two', 'bravo@test.io');
  const ua = await A.E('G.me'), ub = await B.E('G.me');
  // 1 joining
  for (const [pg, u] of [[A, ua], [B, ub]]) ok(pg.tag + ' joined the galaxy online with a homeworld', await pg.E(`G.mode === "online" && !!G.myHome && !!G.byId[G.myHome] && G.byId[G.myHome].owner === G.me`), await pg.E(`JSON.stringify({ mode: G.mode, home: G.myHome })`));
  ok('A and B have different homeworlds', (await A.E('G.myHome')) !== (await B.E('G.myHome')));
  ok('A sees B in the galaxy (players + homeworld)', await wait(A, `!!(G.players["${ub}"] && G.players["${ub}"].home && G.byId[G.players["${ub}"].home])`, 30000), await A.E(`JSON.stringify(G.players["${ub}"] || null)`));
  ok('B sees A', await wait(B, `!!(G.players["${ua}"] && G.byId[G.players["${ua}"].home])`, 30000));
  ok('Academy started for both', (await A.E('S.tut && S.tut.i === 0 && !!S.faction && S.intro')) && (await B.E('S.tut && S.tut.i === 0 && !!S.faction && S.intro')), [await A.E('JSON.stringify([S.tut, S.faction, S.intro])'), await B.E('JSON.stringify([S.tut, S.faction, S.intro])')]);
  // 2 global chat + reload keeps history
  await A.E(`chatPost("g", null, { u: G.me, x: "hello from alpha", t: now() })`);
  ok('global chat reaches B live', await wait(B, `(CHAT.g || []).some(m => m.x === "hello from alpha")`), await B.E('JSON.stringify((CHAT.g||[]).slice(-3))'));
  await B.E(`chatPost("g", null, { u: G.me, x: "bravo here", t: now() })`);
  ok('global chat reaches A live', await wait(A, `(CHAT.g || []).some(m => m.x === "bravo here")`));
  // 3 DMs
  await A.E(`chatPost("d", "${ub}", { u: G.me, x: "secret dm", t: now() })`);
  ok('DM reaches B', await wait(B, `JSON.stringify(CHAT.dms || {}).includes("secret dm")`, 25000), await B.E('JSON.stringify(CHAT.dms || null).slice(0, 300)'));
  // 4 alliance: A founds, B joins, chat both ways
  await A.E(`S.res.m = S.res.c = S.res.g = 9e6; for (const k in S.b) S.b[k] = Math.max(S.b[k] || 0, 12); for (const k in S.r) S.r[k] = Math.max(S.r[k] || 0, 6); dirty(); 1`);
  await A.E(`document.body.insertAdjacentHTML("beforeend", '<input id="alname" value="Test Legion"><input id="altag" value="TL">'); ACT.allyCreate(); 1`);
  ok('A founded an alliance', await wait(A, `!!S.ally && !!G.alliances[S.ally]`), await A.E('JSON.stringify({ ally: S.ally, lvl: cmdLevel(score()), toasts: [...document.querySelectorAll(".toast")].map(t => t.textContent).slice(-3) })'));
  const al = await A.E('S.ally');
  ok('B sees the alliance', await wait(B, `!!G.alliances["${al}"]`, 25000));
  await B.E(`ACT.allyJoin({ id: "${al}" }); 1`);
  ok('B joined the alliance', await wait(B, `S.ally === "${al}"`, 15000), await B.E(`JSON.stringify({ ally: S.ally, a: G.alliances["${al}"] })`));
  ok('A sees B as a member', await wait(A, `!!(G.alliances["${al}"].members || {})["${ub}"]`, 25000));
  await A.E(`chatInit && chatInit(); 1`); await B.E(`chatInit && chatInit(); 1`); await A.waitForTimeout(3000);
  await A.E(`chatPost("a", null, { u: G.me, x: "ally hello", t: now() })`);
  ok('alliance chat reaches B', await wait(B, `(CHAT.a || []).some(m => m.x === "ally hello")`, 25000), await B.E(`JSON.stringify({ aKey: CHAT.aKey, a: (CHAT.a||[]).slice(-3) })`));
  // 5 espionage of B's homeworld by A
  await B.E(`syncPlayer && (store.lastFast = 0, syncPlayer()); 1`); await B.waitForTimeout(2500);
  await A.E(`S.ships.spyProbe = 10; S.ships.fighter = (S.ships.fighter || 0) + 200; S.ships.cargo = (S.ships.cargo || 0) + 20; dirty(); 1`);
  const bh = await B.E('G.myHome');
  await A.E(`sendFleet(G.byId["${bh}"], { spyProbe: 2 }, "spy"); 1`);
  ok('B is warned of the incoming probe', await wait(B, `(G.spyIn || []).length > 0 || JSON.stringify(G.inbound || {}).includes("spy")`, 25000), await B.E(`JSON.stringify({ spyIn: G.spyIn || null })`).catch(() => ''));
  const fa = await A.E(`(() => { const f = S.fleets.find(f => f.mission === "spy" || f.n && f.n.spyProbe); return f ? Math.max(0, (f.arrive || f.at || now()) - now()) : -1; })()`);
  await A.E(`TSKEW += ${Math.max(0, fa) + 5000}; 1`);
  ok('A got a spy report on B', await wait(A, `(S.spyReps || []).length > 0`, 20000), await A.E(`JSON.stringify({ reps: (S.spyReps || []).slice(-1), fl: S.fleets.map(f => f.phase + ":" + f.mission) })`));
  ok('the spy report has B\'s data', await A.E(`(() => { const r = (S.spyReps || []).slice(-1)[0]; return !!r && !r.noData; })()`), await A.E(`JSON.stringify((S.spyReps || []).slice(-1)[0] || null).slice(0, 300)`));
  // 6 PvP: B gets an attackable colony, A attacks it
  await B.E(`G.joinedAt = now() - 5 * 864e5; S.res.m = S.res.c = S.res.g = 2e6; for (const k in S.b) S.b[k] = Math.max(S.b[k] || 0, 10); dirty(); store.lastPlayer = ""; store.lastFast = 0; syncPlayer(); 1`);
  const cid = await B.E(`(() => { const h = G.byId[G.myHome]; const c = G.list.filter(p => p.kind !== "home" && !p.owner && pStatus(p) === "hive").sort((a, b) => Math.hypot(a.x - h.x, a.y - h.y) - Math.hypot(b.x - h.x, b.y - h.y))[0]; settlePlanet(c, { m: 50000, c: 30000, g: 10000 }, now(), G.me, { fighter: 3 }); c.shieldUntil = 0; c.st = { m: 50000, c: 30000, g: 10000, t: now() }; putPlanet(c); return c.id; })()`);
  ok('A sees B\'s colony as attackable', await wait(A, `pStatus(G.byId["${cid}"]) === "player"`, 30000), await A.E(`JSON.stringify({ st: G.byId["${cid}"] && pStatus(G.byId["${cid}"]), owner: G.byId["${cid}"] && G.byId["${cid}"].owner, pl: G.players["${ub}"] })`));
  await A.E(`sendFleet(G.byId["${cid}"], { fighter: 150, cargo: 10 }, "attack"); 1`);
  ok('B gets the red alert (inbound attack)', await wait(B, `(G.inbound || []).length > 0 || !!document.querySelector(".redalert, #redalert")`, 20000), await B.E(`JSON.stringify(Object.keys(G).filter(k => /inb|alert/i.test(k)))`));
  const ta = await A.E(`(() => { const f = S.fleets.find(f => f.mission === "attack"); return f ? Math.max(0, (f.arrive || now()) - now()) : -1; })()`);
  await A.E(`TSKEW += ${Math.max(0, ta) + 5000}; 1`); await A.waitForTimeout(4000); await A.E('window.__dbg.battle && closeBattle(); 1');
  ok('A won and got a battle report', await wait(A, `S.reports && S.reports.some(r => r.pid === "${cid}" || r.p === "${cid}" || JSON.stringify(r).includes("${cid}"))`, 20000), await A.E(`JSON.stringify((S.reports || []).slice(0, 1)).slice(0, 300)`));
  ok('B\'s colony shows the loss (garrison gone)', await wait(B, `(() => { const p = G.byId["${cid}"]; return p && !Object.values(p.garrison || {}).some(v => v > 0); })()`, 30000), await B.E(`JSON.stringify(G.byId["${cid}"] && G.byId["${cid}"].garrison)`));
  ok('B got the defense report in Mail', await wait(B, `(S.reports || []).some(r => JSON.stringify(r).includes("${cid}"))`, 30000), await B.E(`JSON.stringify({ seen: S.inboxSeen && S.inboxSeen.length, reps: (S.reports || []).length })`));
  // 7 share the battle report into global chat
  await A.E(`(() => { const r = (S.reports || []).find(r => JSON.stringify(r).includes("${cid}")); repShare(r, "g"); })(); 1`);
  ok('shared battle report shows in B\'s chat', await wait(B, `(CHAT.g || []).some(m => m.r)`, 25000));
  // 8 a second device on A's account
  const A2 = await player('A2'); await boot(A2, 'in', '', 'alpha@test.io');
  ok('A\'s second device loads A\'s empire', await A2.E(`G.me === "${ua}" && S.ally === "${al}" && (S.ships.fighter || 0) > 0`), await A2.E('JSON.stringify({ me: G.me, ally: S.ally, f: S.ships.fighter, cname: S.cname })'));
  await A2.E(`S.res.m += 777777; dirty(); flush(); 1`); await A2.waitForTimeout(4000);
  await A.evaluate(() => document.dispatchEvent(new Event('visibilitychange')));
  ok('device 1 picks up device 2\'s progress', await wait(A, `S.res.m > 9e6 + 700000 || !!document.querySelector("#sessw")`, 45000), await A.E('JSON.stringify({ m: S.res.m, sess: !!document.querySelector("#sessw") })'));
  // 9 sign out and back in on B
  B.once('dialog', d => d.accept()); const bm = await B.E('S.res.m'); await B.evaluate(() => window.udfAccount.signOut()); await B.waitForTimeout(5000);
  await boot(B, 'in', '', 'bravo@test.io');
  ok('B signs back in to the same empire', await B.E(`G.me === "${ub}" && S.ally === "${al}" && Math.abs(S.res.m - ${bm}) < ${bm} * .2 + 1e5`), await B.E('JSON.stringify({ me: G.me, ally: S.ally, m: S.res.m })'));
  ok('B\'s alliance chat history survives the reload', await wait(B, `(CHAT.a || []).some(m => m.x === "ally hello")`, 25000));
  ok('no homeworld was overwritten', await B.E(`G.myHome === "${bh}" && G.byId["${bh}"].owner === G.me`));
  console.log('\n' + res.filter(r => r.startsWith('FAIL')).length + ' FAIL / ' + res.length); console.log('ERRORS:\n' + (errs.slice(0, 12).join('\n') || 'none'));
  await b.close(); })().catch(e => { console.log('CRASH', e.message); console.log(res.join('\n')); console.log(errs.slice(0, 8).join('\n')); process.exit(1); });
