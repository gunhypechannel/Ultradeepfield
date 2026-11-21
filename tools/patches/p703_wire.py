# v703: Tide of the Carcinid, phase 1 (First Tides). See p703_crc.js (the event) and p703_crcm.js (battle profiles and 3D models).
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__)); R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)

# the event module, just before the galaxy's list of hideouts and monsters (which now carries the Breach Zones and patrols)
rep('const PIRATES = PIRATES_ALL.filter(x => !cubeGone(x) && !pirGone(x)).concat(MON_EXTRA, MON_NEW, MON_SP, MIM_HIVES, MIM_BOSSES, MIM_OM)',
    R('p703_crc.js').rstrip('\n') + '\nconst PIRATES = PIRATES_ALL.filter(x => !cubeGone(x) && !pirGone(x)).concat(MON_EXTRA, MON_NEW, MON_SP, MIM_HIVES, MIM_BOSSES, MIM_OM, CRC_NESTS, CRC_PATS)')
rep('x.mon === "mimic" ? mimForce(x) : x.mon ?', 'x.mon === "mimic" ? mimForce(x) : CRC_M[x.mon] ? crcForce(x) : x.mon ?')
rep('const xRegroup = x => x.mon === "mimic" ? MIM_REGROW :', 'const xRegroup = x => x.mon === "mimic" ? MIM_REGROW : x.mon === "carcinid" ? CRC_REGROW :')
# a Breach Zone or patrol that is not out yet (or any more) is hidden, like a Mimic hive
rep('if ((p.mon === "mimic" || MIM_BOSS[p.id]) && mimHid(p, T || now())) return true;', 'if ((p.mon === "mimic" || MIM_BOSS[p.id]) && mimHid(p, T || now())) return true; if (CRC_M[p.mon] && crcHid(p, T || now())) return true; /* v703 */')
rep('(it.mon === "mimic" || MIM_BOSS[it.id]) && mimHid(it, T)', '((it.mon === "mimic" || MIM_BOSS[it.id]) && mimHid(it, T) || CRC_M[it.mon] && crcHid(it, T))', 2)
rep('/* v663 a hive stays put and grows with its stage */', '/* v663 a hive stays put and grows with its stage */\n        if (it.mon === "carcinid") { o.body.position.set(0, Math.sin(t * .0004 + it.a0) * .15, 0); o.body.rotation.set(0, t * .00002 + it.a0, 0); o.body.scale.setScalar((.6 + it.lvl * .0082) * (.42 + .16 * crcStage(it, T))); } /* v703 a Breach Zone stays put and grows with its stage */')
rep('  if (k === "mimic") return buildMimic("mnest"); /* v663 */', '  if (k === "mimic") return buildMimic("mnest"); /* v663 */\n  if (CRC_M[k]) return buildCarc(CRC_M[k]); /* v703 */')
rep('  if (MIM_U[k] || /^e_/.test(k)) return buildMimic(k);', '  if (CRC_U[k]) return buildCarc(k); /* v703 */\n  if (MIM_U[k] || /^e_/.test(k)) return buildMimic(k);')
rep('if (MON[k] || k === "snest" || MIM_U[k]) { const s = .25', 'if (MON[k] || k === "snest" || MIM_U[k] || CRC_U[k]) { const s = .25')
# the hunt
rep('''  const mimSt = x.mon === "mimic" ? mimStage(x, f.arrive) : 0;''', '''  if (CRC_M[x.mon] && !crcLive(x, f.arrive)) { note(`${x.name} is gone. Fleet returning, nothing lost.`, "warn"); return; } /* v703 */
  const mimSt = x.mon === "mimic" ? mimStage(x, f.arrive) : 0, crcOn = !!CRC_M[x.mon];''')
rep('    if (mimSt) try { mimWin(x, rep, f.arrive); } catch (e) {} /* v663 */', '    if (mimSt) try { mimWin(x, rep, f.arrive); } catch (e) {} /* v663 */\n    if (crcOn) try { crcWin(x, rep, f.arrive); } catch (e) {} /* v703 */')
# its sheet: the model instead of a painting, the stage and garrison, and charting it counts toward the week's orders
rep('{ const q = pos(x, now()); if (!fogSeen(q.x, q.y)) return shUnexplored(x); }', '{ const q = pos(x, now()); if (!fogSeen(q.x, q.y)) return shUnexplored(x); } if (CRC_M[x.mon]) try { crcSurvey(x); } catch (e) {} /* v703 */')
rep('${monArt(MON_ARTF[x.mon] || x.mon)}', '${CRC_M[x.mon] ? `<div class="monart crcart"><img src="art/carcinid/${CRC_ART[x.mon]}.webp?v=1" alt="" loading="lazy"></div>` : monArt(MON_ARTF[x.mon] || x.mon)}')
rep('x.mon === "mimic" ? `Stage ${mimStage(x, T)} · ${MIM_STAGE[mimStage(x, T)]}</dd><dt>The brood</dt><dd>${mimForceTxt(x)}` : ', 'x.mon === "mimic" ? `Stage ${mimStage(x, T)} · ${MIM_STAGE[mimStage(x, T)]}</dd><dt>The brood</dt><dd>${mimForceTxt(x)}` : CRC_M[x.mon] ? crcInfo(x, T) : ')
rep('let html = ({ mimic: shMimic,', 'let html = ({ mimic: shMimic, carcinid: shCarcinid,')
# the band and the server record
rep('html = mimBand(T); /* v663 */', 'html = mimBand(T); /* v663 */\n  if (!html && view === "galaxy" && !sheet && !battle && !G.sbSim && !cineOn) html = crcBand(T); /* v703 */')
rep('+ mimBand(T) +', '+ mimBand(T) + crcBand(T) +')
rep('''    for (const d of ["event/mimic", "event/mimic_prev"]) db.doc(d)''', '''    for (const d of ["event/carcinid", "event/carcinid_prev"]) db.doc(d).onSnapshot(s => { (G.crcDoc = G.crcDoc || {})[d] = s.exists ? s.data() : null; CSC = {}; softRender(); }, () => {}); /* v703 */
    for (const d of ["event/mimic", "event/mimic_prev"]) db.doc(d)''')
# the Battle Lab
rep('return sec("The Mimic Protocol", mimLabHTML(row, b)) +', 'return sec("Tide of the Carcinid", crcLabHTML(row, b)) + sec("The Mimic Protocol", mimLabHTML(row, b)) +')
rep('  mimOpen: () => openSheet({ type: "mimic" }), /* v663 */', '''  mimOpen: () => openSheet({ type: "mimic" }), /* v663 */
  crcOpen: () => { openSheet({ type: "carcinid" }); setTimeout(() => { try { const M = crcS(); if (crcWeek(now()) >= 1 && !M.loreSeen) { M.loreSeen = 1; dirty(); } } catch (e) {} }, 3000); /* the lore opens the first time */ }, /* v703 */
  crcFind: () => { const x = crcNearest(now(), "carcinid"); if (x) mimGo(x); else toast("No Breach Zone within reach right now."); },
  crcFindP: () => { const x = crcNearest(now(), "crcpat"); if (x) mimGo(x); else toast("No scout patrol within reach right now."); },
  crcPrev: d => { if (!ownerFree()) return; const w = +d.w; S.crcPrev = w ? { w, at: now() } : null; CSC = {}; dirty(); toast(w ? `Previewing week ${w} of the Tide of the Carcinid (this device only).` : "Preview off."); renderSheet(); },
  crcClaim: d => { const w = +d.w, o = CRC_OBJ.find(x => x[0] === d.id), M = crcS(), id = `w${w}${d.id}`; if (!o || M.got[id] || crcObjN(w, o[0]) < o[2]) return; M.got[id] = 1; S.shards = (S.shards || 0) + o[3];
    for (const [m, v] of Object.entries(o[4])) M.m[m] = (M.m[m] || 0) + v; M.pend = (M.pend || 0) + 10; setTimeout(() => crcFlush(1), 50); dirty();
    toast(`+◆${o[3]} and ${Object.entries(o[4]).map(([m, v]) => `${v} ${CRC_MAT[m][0]}`).join(", ")}`, "win"); try { logReward(`Tide of the Carcinid · week ${w} order`, null, { shards: o[3], kind: "event" }); } catch (e) {} renderSheet(); },
  crcSup: d => { const p = +d.p, Rw = CRC_SUPM.find(x => x[0] === p), M = crcS(), st = crcStC(now()); if (!Rw || M.got["s" + p] || crcSupPct(st) * 100 < p || !((st.con[G.me] || 0) + (M.pend || 0) > 0)) return;
    M.got["s" + p] = 1; S.shards = (S.shards || 0) + Rw[1]; M.m.resin = (M.m.resin || 0) + Rw[2]; dirty(); toast(`Abyssal Suppression ${p}%: +◆${Rw[1]} and ${Rw[2]} Tidal Resin`, "win"); try { logReward(`Abyssal Suppression ${p}%`, null, { shards: Rw[1], kind: "event" }); } catch (e) {} renderSheet(); },
  crcLabWeek: d => { if (!duelOwner()) return; const w = +d.k; S.crcPrev = w ? { w, at: now() } : null; CSC = {}; dirty(); toast(w ? `Previewing week ${w} of the Tide of the Carcinid (this device only).` : "Carcinid preview off."); renderSheet(); },
  crcLabFight: d => { if (!duelOwner()) return; labReset(); crcLabFight(d.k); },''')
# the battle screen: profiles, sizes, weapons and models, registered once the tables exist; the crabs walk like the Mimics move
rep('function mimAtkAdd(b, v) {', R('p703_crcm.js').rstrip('\n') + '\nfunction mimAtkAdd(b, v) {')
rep('filter(x => MIM_D[x] && MON_WAVE[x])', 'filter(x => (MIM_D[x] || CRC_U[x]) && MON_WAVE[x])')
rep('(MIM_D[q.k] && MON_WAVE[q.k] && mimAnimOK(b, q.k))', '((MIM_D[q.k] || CRC_U[q.k]) && MON_WAVE[q.k] && mimAnimOK(b, q.k))')
rep('.mimb{--fc:#5fd8ff}', '''.mimb{--fc:#5fd8ff}
.crcb{--fc:#e8b45a}.crcban{border-color:rgba(232,180,90,.4);box-shadow:0 0 24px rgba(63,224,200,.18);background:radial-gradient(ellipse at 50% 60%,rgba(63,224,200,.22),rgba(16,8,30,.9) 70%)}.crcban img{object-position:50% 40%}
.crcban div{background:linear-gradient(transparent,rgba(10,6,20,.92))}.crcban b{color:#fff2d8;text-shadow:0 0 12px rgba(232,180,90,.6)}.crcban span{color:#7fe8d8}
.crclore{flex:none;margin:2px 0 8px;padding:8px 10px;border-radius:10px;border:1px solid rgba(232,180,90,.25);background:rgba(18,10,30,.5)}.crclore summary{cursor:pointer;font-weight:700;color:#f0c878}.crclore p{margin:6px 0 0;font-size:13px;line-height:1.45;color:#e2dcf0}
.crcwk{border-color:rgba(232,180,90,.2)}.crcwk.on{border-color:#e8b45a;background:rgba(232,180,90,.1);box-shadow:inset 0 0 12px rgba(232,180,90,.15)}.crcwk b{color:#f0c878}
.crcst div{background:rgba(24,14,40,.5);border-color:rgba(232,180,90,.18)}.crcst b{color:#ffe8b8}.crcst .off{opacity:.4}
.crcfind{display:flex;flex-wrap:wrap;gap:6px;flex:none;margin-bottom:6px}.crcfind .btn{flex:1 1 140px}
.crcobj{border-color:rgba(232,180,90,.25);background:rgba(18,10,30,.55)}.crcobj .bar i{background:linear-gradient(90deg,#e8b45a,#3fe0c8)}
.crcbar i{background:linear-gradient(90deg,#e8b45a,#3fe0c8)}
.crcms{display:grid;grid-template-columns:repeat(4,1fr);gap:5px;flex:none;margin:6px 0 4px}.crcm{display:flex;flex-direction:column;align-items:center;gap:3px;padding:6px 4px;border-radius:9px;border:1px solid rgba(63,224,200,.15);background:rgba(6,24,22,.45);text-align:center}
.crcm b{font:700 15px/1 var(--f-display);color:#bff6ec}.crcm small{font-size:10px;color:#9ab}.crcm .btn{padding:3px 8px;font-size:11px}.crcm.ok{border-color:#3fe0c8}.crcm.got{opacity:.6}
.crccl{border-color:rgba(232,180,90,.14);background:rgba(18,10,30,.5)}.crccl img{width:112px;height:72px;flex:none;border-radius:7px;object-fit:cover;object-position:50% 35%}.crccl em{color:#e8b45a}
.crcmi{width:40px;height:40px;border-radius:8px;object-fit:cover;margin-bottom:2px}
.crcart{background:radial-gradient(ellipse at 50% 60%,rgba(63,224,200,.2),rgba(16,8,30,.6) 70%)}''')
rep('const GAME_V = 702;', 'const GAME_V = 703;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
