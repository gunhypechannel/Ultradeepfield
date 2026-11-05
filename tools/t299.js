const { chromium, devices } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--enable-unsafe-swiftshader','--use-gl=angle','--use-angle=swiftshader'] }); const pg = await (await b.newContext({ ...devices['iPhone 15 Pro Max'], deviceScaleFactor: 2 })).newPage(); const errs = []; pg.on('pageerror', e => errs.push(e.message + ' | ' + (e.stack || '').split('\n')[1]));
  await pg.route('**/three.min.js', r => r.fulfill({ path: 'threelib/three.min.js', contentType: 'application/javascript' })); await pg.route(/fonts\.(googleapis|gstatic)/, r => r.abort());
  pg.goto('file://' + process.cwd() + '/index.html', { waitUntil: 'commit' }).catch(() => {});
  await pg.waitForFunction(() => window.__dbg && window.__dbg.S && window.__dbg.G.list, null, { timeout: 180000, polling: 1000 }); await pg.waitForTimeout(2500);
  await pg.evaluate(() => { document.querySelectorAll('#authw,#adv').forEach(e => e.remove()); window.__dbg.closeAll(); });
  const E = c => pg.evaluate(c => window.__dbg.ev(c), c);
  const shot = async n => { await pg.evaluate(() => { try { advLines = []; } catch (e) {} document.querySelectorAll('#adv,#coach').forEach(e => e.remove()); }); await pg.screenshot({ path: '../' + n + '.png', timeout: 60000 }); };
  console.log('new:', await E(`(() => { S.fs = null; const L = cmdLevel(score()); return JSON.stringify({ L, ok: flagOK(G.me), on: fsOn(), built: S.fs.built, dockMiss: missing(B.flagDock.req).map(x => x.join(':')), lock: lockTxt(missing(B.flagDock.req)) }); })()`));
  console.log('drops pre-flagship:', await E(`(() => { const f = fsOf(); const x = Object.values(PB).find(q => !q.boss && !q.mon && q.lvl === 5); const xp0 = f.xp; fsLootPB(x); return JSON.stringify({ mats: f.mats, xpGain: f.xp - xp0 }); })()`));
  console.log('tut steps:', await E(`JSON.stringify({ len: TUT.length, V2: TUT_V2, last: TUT.slice(-4).map(s => s.t) })`));
  // walk the last three Academy steps
  console.log('academy:', await E(`(() => { const f = fsOf(); f.mats = {}; S.tut = { i: TUT_V2, open: 1 }; S.res.m = S.res.c = S.res.g = 0; S.spent = 2.5e6; const L = cmdLevel(score());
    tutClaim(); const a = TUT[S.tut.i].t; S.b.flagDock = 1; tutClaim(); const b = TUT[S.tut.i].t; const res0 = Object.assign({}, S.res), mats = Object.assign({}, f.mats);
    ACT.fsBuild(); const ok = flagOK(G.me); tutClaim(); return JSON.stringify({ L, a, b, res0, mats, built: f.built, ok, on: fsOn(), left: f.mats, tutI: S.tut.i, len: TUT.length, tutOn: tutOn() }); })()`));
  console.log('forge gate:', await E(`(() => { const f = fsOf(); for (const m of Object.keys(FS_MATS)) for (let t = 1; t <= 6; t++) f.mats[fsMatKey(m, t)] = 40; S.res.m = S.res.c = S.res.g = 1e9;
    openSheet({ type: 'flagship', tab: 'forge' }); sheet.fs = 'weapon'; sheet.ft = 3; ACT.fsCraft(); const n1 = f.q.length; sheet.ft = 1; ACT.fsCraft(); ACT.fsCraft(); const n2 = f.q.length; const ms1 = fsRecipe('weapon', 1).ms;
    S.b.flagDock = 9; const ms9 = fsRecipe('weapon', 1).ms; const r = { n1, n2, qmax1: fsQMax(1), qmax9: fsQMax(), tier1: fsDockTier(1), tier9: fsDockTier(9), ms1, ms9, eff: effect('flagDock', 9) }; S.b.flagDock = 1; return JSON.stringify(r); })()`));
  console.log('veteran:', await E(`(() => { const keep = S.fs; S.fs = null; S.spent = 2e7; const v = flagOK(G.me); const mid = (S.fs = null, S.spent = 4e6, flagOK(G.me)); S.fs = keep; return JSON.stringify({ lv15plus: v, lv11: mid }); })()`));
  console.log('others:', await E(`(() => { const id = 'tstP'; G.players[id] = G.players[id] || { score: 0, tech: {} }; const P = G.players[id], s0 = P.score, t0 = P.tech; P.score = 3000; P.tech = Object.assign({}, t0, { fl: null }); const a = flagOK(id); P.tech.fl = 1; const b2 = flagOK(id); P.tech.fl = 0; const c = flagOK(id); P.score = s0; P.tech = t0; return JSON.stringify({ oldClient: a, built: b2, notBuilt: c }); })()`));
  console.log('tut migrate:', await E(`(() => { S.tut = { i: TUT_V2, open: 0 }; S.tutFlag = 0; const keep = S.b.flagDock; S.b.flagDock = 0; coachRender(true); const r1 = [S.tut.i, S.tut.open]; S.tut = { i: TUT_V2 }; S.tutFlag = 0; S.b.flagDock = 1; coachRender(true); const r2 = S.tut.i; S.b.flagDock = keep; return JSON.stringify({ noDock: r1, done: r2, len: TUT.length }); })()`));
  // UI shots
  await E(`(() => { closeSheet(); const f = fsOf(); f.built = 0; openSheet({ type: 'flagship', tab: 'over' }); })()`); await pg.waitForTimeout(2500); await E('renderSheet()'); await pg.waitForTimeout(300); await shot('d_comm');
  await E(`(() => { fsOf().built = 1; closeSheet(); openSheet({ type: 'detail', kind: 'b', k: 'flagDock', qty: 1, tab: 1 }); })()`); await pg.waitForTimeout(800); await shot('d_dock');
  await E(`(() => { closeSheet(); openSheet({ type: 'flagship', tab: 'forge' }); })()`); await pg.waitForTimeout(600); await shot('d_forge');
  await E(`(() => { closeSheet(); sub.s = 'fac'; ACT.nav({ v: 'build', s: 'fac' }); })()`); await pg.waitForTimeout(1200); await pg.evaluate(() => { const e = document.querySelector('article.bn[data-k="flagDock"]'); if (e) e.scrollIntoView(); }); await pg.waitForTimeout(800); await shot('d_list');
  await E(`(() => { closeSheet(); ACT.nav({ v: 'base' }); })()`); await pg.waitForTimeout(4000); await E(`(() => { C3.v.tx = 2; C3.v.tz = -11; C3.v.zoom = 1.3; })()`); await pg.waitForTimeout(3000); try { await shot('d_base'); } catch (e) { console.log('base shot timeout'); }
  console.log(errs.slice(0, 6).join('\n') || 'no errors'); await b.close(); })();
