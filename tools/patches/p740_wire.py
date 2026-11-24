"""v740: the Resurrection War, phases 1-3 (behind the owner flag): the clock, the Continuum fleet, patrols and platforms,
the resurrection network (relays, Arks, commanders, the Eternal Commander), War Command, the map layer, the Battle Lab."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:120]); s = s.replace(a, b)
A = open(os.path.join(D, "p740_cnt_a.js"), encoding="utf-8").read()
B = open(os.path.join(D, "p740_cnt_b.js"), encoding="utf-8").read()
CSS = open(os.path.join(D, "p740_cnt.css"), encoding="utf-8").read()
rep("const GAME_V = 739;", "const GAME_V = 740;")
rep("const PIRATES = PIRATES_ALL.filter(", A + "\nconst PIRATES = PIRATES_ALL.filter(")
rep("CRC_NESTS, CRC_PATS, CRC_KRAK,", "CRC_NESTS, CRC_PATS, CRC_KRAK, CNT_NET, CNT_PATS, CNT_PLATS,")
tables = '''
Object.assign(CPROF, { cnint: ["interceptor", "laser", .07, .3, 9, 0], cncor: ["frigate", "ion", .16, .14, 5.5, 1], cnexe: ["frigate", "beam", .16, .12, 6, 1], cnfab: ["carrier", "laser", .2, .04, 3, 3], cnasm: ["cruiser", "ion", .22, .08, 4.2, 2],
  cndre: ["battleship", "beam", .3, .04, 3, 3], cnrel: ["station", "ion", .32, 0, 0, 2], cnark: ["titan", "beam", .38, 0, 1.2, 6], cnprime: ["titan", "beam", .42, 0, 1, 8], cneter: ["titan", "plasma", .38, .02, 1.8, 6], cncom: ["titan", "laser", .34, .02, 1.8, 4] });
Object.assign(MIM_HULL, { cnint: .85, cncor: 1, cnexe: 1.35, cnfab: 2, cnasm: 1.6, cndre: 2.6, cnrel: 2.2, cnark: 4, cnprime: 5.4, cneter: 3.6, cncom: 3.2 });
Object.assign(MIM_PACK, { cnint: 1 }); MIM_STA.cnrel = .5;
Object.assign(BOSS_GLOW, { cnark: "255,40,60", cnprime: "255,30,50", cneter: "255,24,48", cncom: "255,90,110", cnrel: "255,42,64" });
'''
rep('Object.assign(MON_EL, { carcinid: "water", crcpat: "water", wkraken: "water" });', B + tables + 'Object.assign(MON_EL, { carcinid: "water", crcpat: "water", wkraken: "water" });')
# routing through the boss hooks (the network targets live in MIM_BOSS with cnt set)
rep("if (B.crc) return crcHid(x, T); /* v704 */", "if (B.crc) return crcHid(x, T); /* v704 */ if (B.cnt) return cntHid(x, T); /* v740 */")
rep("function alphaForce(x, T) { if (MIM_BOSS[x.id].crc) return crcBossForce(x, T);", "function alphaForce(x, T) { if (MIM_BOSS[x.id].cnt) return cntBossForce(x, T); /* v740 */ if (MIM_BOSS[x.id].crc) return crcBossForce(x, T);")
rep("function mimBossInfo(x, T) { if (MIM_BOSS[x.id].crc) return crcBossInfo(x, T);", "function mimBossInfo(x, T) { if (MIM_BOSS[x.id].cnt) return cntBossInfo(x, T); /* v740 */ if (MIM_BOSS[x.id].crc) return crcBossInfo(x, T);")
rep("(MIM_BOSS[f.xid].crc ? crcBossResolve(f) :", "(MIM_BOSS[f.xid].cnt ? cntBossResolve(f) : MIM_BOSS[f.xid].crc ? crcBossResolve(f) :")
rep("CRC_M[x.mon] ? crcForce(x) : x.mon ? monForce(x.mon, x.lvl)", "CNT_M[x.mon] ? cntForce(x) : CRC_M[x.mon] ? crcForce(x) : x.mon ? monForce(x.mon, x.lvl)")
rep("const xRegroup = x => x.mon === \"mimic\" ? MIM_REGROW :", "const xRegroup = x => CNT_M[x.mon] ? CNT_REGROW : x.mon === \"mimic\" ? MIM_REGROW :")
# patrols and platforms: gone check, the machine tactics, the war's salvage
rep('if (CRC_M[x.mon] && !crcLive(x, f.arrive)) { note(`${x.name} is gone. Fleet returning, nothing lost.`, "warn"); return; } /* v703 */',
    'if (CRC_M[x.mon] && !crcLive(x, f.arrive)) { note(`${x.name} is gone. Fleet returning, nothing lost.`, "warn"); return; } /* v703 */\n  if (CNT_M[x.mon] && !cntLive(x, f.arrive)) { note(`${x.name} is gone. Fleet returning, nothing lost.`, "warn"); return; } /* v740 */')
rep("const mine0 = Object.assign({}, f.n), res = simulate(stacksOf(f.n, techElVs(x), G.me).concat(allyStacks(f.allies, x.lvl)), xStacks(x));",
    "const mine0 = Object.assign({}, f.n), res = cntFight(x, f) || simulate(stacksOf(f.n, techElVs(x), G.me).concat(allyStacks(f.allies, x.lvl)), xStacks(x)); /* v740 the machine tactics */ if (res.cntTac) for (const t of res.cntTac) note(`${CNT_TAC[t][0]}: ${CNT_TAC[t][1]}`, \"info\");")
rep("if (crcOn) try { crcWin(x, rep, f.arrive); } catch (e) {} /* v703 */", "if (crcOn) try { crcWin(x, rep, f.arrive); } catch (e) {} /* v703 */\n    if (CNT_M[x.mon]) try { cntWin(x, rep, f.arrive); } catch (e) {} /* v740 */")
# hidden while not in play
rep("if (CRC_M[p.mon] && crcH", "if (CNT_M[p.mon] && cntHid(p, T || now())) return true; /* v740 */ if (CRC_M[p.mon] && crcH")
rep("|| CRC_M[it.mon] && crcHid(it, T)));", "|| CRC_M[it.mon] && crcHid(it, T) || CNT_M[it.mon] && cntHid(it, T)));", 2)
# the target's page
rep("CRC_M[x.mon] ? crcInfo(x, T) :", "CNT_M[x.mon] ? cntInfo(x, T) : CRC_M[x.mon] ? crcInfo(x, T) :")
rep("if (CRC_M[x.mon]) try { crcSurvey(x); } catch (e) {} /* v703 */", "if (CRC_M[x.mon]) try { crcSurvey(x); } catch (e) {} /* v703 */ if (CNT_M[x.mon]) try { cntSurvey(x); } catch (e) {} /* v740 */")
# models, stats
rep("  if (CRC_M[k]) return buildCarc(CRC_M[k]); /* v703 */", "  if (CRC_M[k]) return buildCarc(CRC_M[k]); /* v703 */\n  if (CNT_M[k]) return buildCnt(CNT_M[k]); /* v740 */")
rep("  if (CRC_U[k]) return buildCarc(k); /* v703 */", "  if (CNT_U[k]) return buildCnt(k); /* v740 */\n  if (CRC_U[k]) return buildCarc(k); /* v703 */")
rep('if (MON[k] || k === "snest" || MIM_U[k] || CRC_U[k]) {', 'if (MON[k] || k === "snest" || MIM_U[k] || CRC_U[k] || CNT_U[k]) {')
# the band, the sheet, the actions, the lab, the server record, the map layer, the switch
rep("html = crcBand(T); /* v703 */", "html = crcBand(T) || cntBand(T); /* v703 */ /* v740 */")
rep("+ mimBand(T) + crcBand(T) +", "+ mimBand(T) + crcBand(T) + cntBand(T) +")
rep("carcinid: shCarcinid,", "carcinid: shCarcinid, cnt: shCnt,")
rep("  crcGoB: d => { const x = PB[d.id]; if (x) mimGo(x); },", '''  crcGoB: d => { const x = PB[d.id]; if (x) mimGo(x); },
  cntOpen: () => { openSheet({ type: "cnt" }); setTimeout(() => { try { const M = cntS(); if (cntOn(now()) && !M.loreSeen) { M.loreSeen = 1; dirty(); } } catch (e) {} }, 3000); }, /* v740 */
  cntGo: d => { const x = PB[d.id]; if (x) mimGo(x); },
  cntFind: d => { const x = cntNearest(now(), d.m); if (x) mimGo(x); else toast("Nothing of theirs within reach right now."); },
  cntPrev: d => { if (!ownerFree()) return; const s = +d.s; S.cntPrev = s ? { s, at: now() } : null; CNTC = {}; dirty(); toast(s ? `Previewing stage ${s}, ${CNT_STN[s]} (this device only).` : "Preview off."); renderSheet(); },
  cntLabStage: d => { if (!duelOwner()) return; const s = +d.k; S.cntPrev = s ? { s, at: now() } : null; CNTC = {}; dirty(); toast(s ? `Previewing stage ${s} of the Resurrection War (this device only).` : "Resurrection War preview off."); renderSheet(); },
  cntLabFight: d => { if (!duelOwner()) return; labReset(); cntLabFight(d.k); },
  cntClaimO: d => { const s = +d.s, o = (CNT_OBJ[s] || []).find(x => x[0] === d.id), M = cntS(), id = `s${s}${d.id}`; if (!o || M.got[id] || cntObjN(s, o[0]) < o[2]) return; M.got[id] = 1; cntGrant(Object.assign({ sh: o[3] }, o[4]), `War order: ${o[1]}`); toast(`Order complete: ◆${o[3]} and ${cntMatTxt(o[4])}.`, "win"); renderSheet(); },
  cntMile: d => { const p = +d.p, m = CNT_MILE.find(x => x[0] === p), M = cntS(), st = cntStC(now()), id = "m" + p; if (!m || M.got[id] || cntWar(st) < p || !((st.con[G.me] || 0) + (M.pend || 0))) return; M.got[id] = 1; cntGrant(Object.assign({ sh: m[1] }, m[2]), `War progress ${p}%`); toast(`War progress ${p}%: ◆${m[1]} and ${cntMatTxt(m[2])}.`, "win"); renderSheet(); },''')
rep('return sec("Tide of the Carcinid", crcLabHTML(row, b)) +', 'return sec("The Resurrection War", cntLabHTML(row, b)) + sec("Tide of the Carcinid", crcLabHTML(row, b)) +')
rep('    for (const d of ["event/carcinid", "event/carcinid_prev"]) db.doc(d).onSnapshot(', '    for (const d of ["event/cnt", "event/cnt_prev"]) db.doc(d).onSnapshot(s => { (G.cntDoc = G.cntDoc || {})[d] = s.exists ? s.data() : null; CNTC = {}; try { cntClaim(); } catch (e) {} softRender(); }, () => {}); /* v740 */\n    for (const d of ["event/carcinid", "event/carcinid_prev"]) db.doc(d).onSnapshot(')
rep("  try { finTick(W, t, T); } catch (e) { mapErr(e); } // v571 The Ten Seals", "  try { finTick(W, t, T); } catch (e) { mapErr(e); } // v571 The Ten Seals\n  try { cntMapTick(W, t, T); } catch (e) { mapErr(e); } /* v740 */")
rep('.then(r => r.ok ? r.json() : null).then(j => { const v = j && +j.v;', '.then(r => r.ok ? r.json() : null).then(j => { if (j && j.f) G.flags = j.f; /* v740 server switches */ const v = j && +j.v;')
rep("</style>", CSS + "</style>", 1) if s.count("</style>") == 1 else None
if "v740 the Resurrection War: black chrome" not in s:
    i = s.index("</style>"); s = s[:i] + CSS + s[i:]
# the network's giant structures broadcast across the galaxy: never hidden by fog
rep("a = it.a0 + T * TAU / period(it.r), x = Math.cos(a) * it.r, z = Math.sin(a) * it.r, nf = fogSeen(x, z);", "a = it.a0 + T * TAU / period(it.r), x = Math.cos(a) * it.r, z = Math.sin(a) * it.r, nf = fogSeen(x, z) || !!CNT_BOSS[it.id];")
rep("const q = P3(it, T, PQ), dc = Math.hypot(q.x - cp.x, q.y - cp.y, q.z - cp.z), nf = fogSeen(q.x, q.z);", "const q = P3(it, T, PQ), dc = Math.hypot(q.x - cp.x, q.y - cp.y, q.z - cp.z), nf = fogSeen(q.x, q.z) || !!CNT_BOSS[it.id];")
rep('if (!fogSeen(q.x, q.y)) return shUnexplored(x); }', 'if (!fogSeen(q.x, q.y) && !CNT_BOSS[x.id]) return shUnexplored(x); }')
rep("function isFogged(p, T) { if (!p || p.owner === G.me) return false;", "function isFogged(p, T) { if (!p || p.owner === G.me || CNT_BOSS[p.id]) return false;")
open(p, "w", encoding="utf-8").write(s)
print("ok")
