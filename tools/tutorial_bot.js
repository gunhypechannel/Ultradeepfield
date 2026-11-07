// Plays the Flight Academy from a fresh start by following the guide's hand, like a player would.
const { chromium, devices } = require('playwright');
const MAXIT = +process.env.MAXIT || 2600, DEV = process.env.DEV || 'iPhone 15 Pro Max', SHOTS = process.env.SHOTS || '';
(async () => { const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader', '--use-gl=angle', '--use-angle=swiftshader'] });
  const ctx = await b.newContext(DEV === 'land' ? { viewport: { width: 1180, height: 820 }, hasTouch: true, isMobile: true, deviceScaleFactor: 1 } : { ...devices[DEV] }); const pg = await ctx.newPage(); const errs = [];
  pg.on('pageerror', e => errs.push(e.message + ' @ ' + ((e.stack || '').split('\n')[1] || '').trim()));
  await pg.route('**/three.min.js', r => r.fulfill({ path: 'threelib/three.min.js', contentType: 'application/javascript' })); await pg.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
  pg.goto('file://' + process.cwd() + '/index.html', { waitUntil: 'commit' }).catch(() => {});
  await pg.waitForFunction(() => window.__dbg && window.__dbg.S && window.__dbg.G.list, null, { timeout: 180000, polling: 1000 }); await pg.waitForTimeout(3000);
  await pg.evaluate(() => { document.querySelectorAll('#authw').forEach(e => e.remove());
    window.__toasts = []; new MutationObserver(ms => { for (const m of ms) for (const n of m.addedNodes) if (n.nodeType === 1 && /toast/.test(n.className || '')) window.__toasts.push(n.textContent.trim().slice(0, 140)); }).observe(document.body, { childList: true, subtree: true }); });
  const E = c => pg.evaluate(c => window.__dbg.ev(c), c);
  let last = -1, stepIt = 0, labels = [], idle = 0, skipped = 0; const report = [], issues = [];
  const tag = s => s.replace(/\s+/g, ' ').slice(0, 110);
  for (let it = 0; it < MAXIT; it++) {
    const s = JSON.parse(await E(`JSON.stringify((() => { const st = TUT[S.tut.i]; const el = GD.el && GD.el.isConnected ? GD.el : null, r = el && el.getBoundingClientRect();
      return { i: S.tut.i, n: TUT.length, t: st ? st.t : null, ok: st ? !!st.ok(S) : 0, mode: G.ready ? advPick() : 'notready', adv: !!document.querySelector('#adv'), battle: !!battle, cine: !!(G3 && G3.cam && G3.cam.cine), sheet: sheet && sheet.type, view,
        lab: GD.label, el: el ? { tag: el.tagName, id: el.id, act: el.dataset.act || '', dis: !!el.disabled, x: r.left + r.width / 2, y: r.top + r.height / 2, w: r.width, h: r.height } : null,
        res: [S.res.m, S.res.c, S.res.g].map(Math.round), lv: cmdLevel(score()), bq: S.bq ? S.bq.k : '', rq: S.rq ? S.rq.k : '', sq: S.sq.length, fl: S.fleets.map(f => f.phase + (f.pid ? ':p' : f.xid ? ':x' : f.nid ? ':n' : f.yid ? ':y' : '')).join(','), ships: JSON.stringify(S.ships) }; })())`));
    if (s.i !== last) { if (last >= 0) console.log('STEP ' + (last + 1) + ' ok, ' + stepIt + ' taps'), report.push(`#${last + 1} done in ${stepIt} taps, ${Math.round(skipped / 60000)} min skipped | ${labels.join(' → ')}`); last = s.i; stepIt = 0; labels = []; skipped = 0;
      if (SHOTS && s.i < s.n) await pg.screenshot({ path: `${SHOTS}/s${String(s.i + 1).padStart(2, '0')}.png` }).catch(() => {}); }
    if (process.env.V) console.log(it, JSON.stringify({ i: s.i, sheet: s.sheet, mode: s.mode, adv: s.adv, lab: s.lab, el: s.el, view: s.view }));
    if (s.i >= s.n) { report.push('ACADEMY COMPLETE at iteration ' + it); break; }
    if (stepIt > 160 || idle > 300) { issues.push(`STUCK on #${s.i + 1} "${s.t}": ${JSON.stringify(s)} DIAG ` + await E(`JSON.stringify({ advLines, siege: !!(G3 && G3.cam.siege), cine: !!(G3 && G3.cam.cine), snz: tutSnoozed(), pathSnz: S.pathSnz > now(), ready: G.ready, demo: !!G.cubeDemo, pick: (() => { const p = guidePick(); return p ? [p.label, p.v] : null; })(), path: (() => { const st = TUT[S.tut.i]; return st.path ? st.path().map(q => q && [q[0], q[1], [...document.querySelectorAll(q[0])].map(e => guideVisible(e) + (e.disabled ? 'd' : '')).join('')]) : null; })(), mode: advPick(), stp: shipStep() && shipStep().t })`)); await pg.screenshot({ path: '../botstuck.png' }); break; }
    if (s.sheet === 'faction') { await pg.evaluate(() => { const b = document.querySelector('.sheet [data-act="facPick"]'); if (b) b.click(); }); labels.push('[faction]'); await pg.waitForTimeout(600); continue; }
    if (await pg.evaluate(() => !!document.querySelector('#celeb'))) { const bx = await pg.evaluate(() => { const r = document.querySelector('#celeb [data-act="celebX"]').getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }); labels.push('[celebration]'); await pg.waitForTimeout(600); await pg.touchscreen.tap(bx[0], bx[1]); await pg.waitForTimeout(400); continue; }
    if (s.adv) { const bx = await pg.evaluate(() => { const a = document.querySelector('#adv .box') || document.querySelector('#adv'); const r = a.getBoundingClientRect(); return [r.left + r.width * .7, r.top + r.height * .6]; }); await pg.touchscreen.tap(bx[0], bx[1]); await pg.waitForTimeout(350); continue; }
    if (s.battle) { await pg.waitForTimeout(1500); await pg.evaluate(() => window.__dbg.closeBattle()); labels.push('[battle]'); await pg.waitForTimeout(500); continue; }
    if (s.lab && labels[labels.length - 1] !== s.lab) labels.push(tag(s.lab));
    if (/^Close this/.test(s.lab || '') && !s.ok) { const d = await E(`(() => { const st = TUT[S.tut.i], p = st.path ? st.path() : []; return JSON.stringify({ sheet: sheet && sheet.type, k: sheet && sheet.k, id: sheet && sheet.id, path: p.map(q => q && [q[0], q[1], [...document.querySelectorAll(q[0])].map(e => guideVisible(e) + (e.disabled ? 'd' : '')).join('')]) }); })()`); issues.push(`#${s.i + 1} mid-step Close: ${d}`); await pg.screenshot({ path: `../bot/close_${s.i + 1}_${stepIt}.png` }).catch(() => {}); }
    if (/Not enough resources|Check the requirements|mines refill/.test(s.lab || "")) issues.push(`#${s.i + 1} "${s.t}": guide says "${s.lab}" res=${s.res} ` + await E(`JSON.stringify({ tutN: G.tutN, own: own("fighter"), armed: armedMax(), sq: S.sq.map(q => q.k + ":" + q.left), fund: TUT[S.tut.i].fund ? TUT[S.tut.i].fund() : null, sup: S.tutSup, qty: G.tutN ? tutQty(G.tutN[0], G.tutN[1]) : null, cost: SH.fighter.c, home: S.ships.fighter, hf: S.ships.heavyFighter, fl: S.fleets.map(f => f.phase + ':' + JSON.stringify(f.n)) })`));
    if (process.env.WANDER && it % 8 === 5 && !s.ok) { // a curious player: tap something else on screen
      const r = await pg.evaluate(() => { const bad = /tutSkip|tutMin|pathMin|signOut|logout|reset|wipe|restart|newGame|delete|leave|abandon|buy|iap|purchase|teleport|share|feedback|fbSend|close|nameSave|skinSave|facPick|vip|shop|prem|recall|dismiss|scrap|demolish|cancel|tutClaim|claim/i;
        const els = [...document.querySelectorAll('[data-act]')].filter(e => { const r = e.getBoundingClientRect(); if (r.width < 8 || r.height < 8 || r.top < 0 || r.bottom > innerHeight || e.disabled) return false; if (bad.test(e.dataset.act)) return false; const top = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); return top && (top === e || e.contains(top)); });
        if (!els.length) return null; const e = els[Math.floor(Math.random() * els.length)], r = e.getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2, e.dataset.act]; });
      if (r) { labels.push('[wander:' + r[2] + ']'); await pg.touchscreen.tap(r[0], r[1]); await pg.waitForTimeout(500); continue; } }
    const clickable = s.el && !s.el.dis && (s.el.tag === 'BUTTON' || s.el.act || s.el.id === 'tutfm' || s.el.tag === 'ARTICLE' || s.el.tag === 'INPUT');
    if (clickable) { idle = 0; stepIt++;
      if (s.el.tag === 'INPUT' || /^Type /.test(s.lab)) { const sel = (await E(`document.querySelector('.sheet #cnin') ? '#cnin' : document.querySelector('.sheet #pname') ? '#pname' : ''`));
        if (sel) { const v = await pg.$eval('.sheet ' + sel, e => e.value); if (!v) { await pg.fill('.sheet ' + sel, sel === '#cnin' ? 'Nova Tester' : 'Aurora Prime'); labels.push('[typed]'); await pg.waitForTimeout(300); if (s.el.tag === 'INPUT') continue; } } }
      if (s.el.id !== 'tutfm') { await pg.waitForTimeout(220); const r2 = JSON.parse(await E(`(() => { const e = GD.el && GD.el.isConnected ? GD.el : null; if (!e) return 'null'; const r = e.getBoundingClientRect(); return JSON.stringify([r.left + r.width / 2, r.top + r.height / 2]); })()`)); if (!r2 || Math.hypot(r2[0] - s.el.x, r2[1] - s.el.y) > 3) continue; } // a person waits for the screen to settle
      { const vy = Math.min(Math.max(s.el.y, 6), (await pg.evaluate(() => innerHeight)) - 6); s.el.y = vy; } // tap the part that is on screen, as a person would
      try { await pg.touchscreen.tap(s.el.x, s.el.y); } catch (e) { await pg.mouse.click(s.el.x, s.el.y); }
      await pg.waitForTimeout(s.el.id === 'tutfm' ? 900 : 450); continue; }
    // nothing to tap: waiting on a build, research, production or a fleet in flight
    idle++; const jump = s.cine || /on its way|flying home|Under construction|Researching|in production|Queued|finishes on its own|Wait/.test(s.lab || '') || !s.lab ? 60000 : 30000;
    await E(`TSKEW += ${jump}`); skipped += jump; if (idle % 20 === 19) stepIt++; await pg.waitForTimeout(350);
  }
  const toasts = await pg.evaluate(() => window.__toasts.filter((t, i, a) => a.indexOf(t) === i));
  console.log(report.join('\n')); console.log('\nISSUES:\n' + (issues.filter((x, i, a) => a.indexOf(x) === i).join('\n') || 'none'));
  console.log('\nTOASTS:\n' + toasts.join('\n')); console.log('\nERRORS:\n' + (errs.slice(0, 8).join('\n') || 'none'));
  console.log('\nFINAL ' + await E(`JSON.stringify({ i: S.tut.i, lv: cmdLevel(score()), res: S.res, planets: myPlanets().length, fs: !!(S.fs && S.fs.built), shipQ: S.shipQ, say: S.say && S.say.length })`));
  await pg.screenshot({ path: '../botend.png' }); await b.close(); })();
