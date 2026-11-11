# v442: Cube Devastation moves to every 15th (first: Sun 15 Nov 2026, 18:00 UTC = 11am Phoenix) (owner), and the Omega Cube becomes a
#  fight (owner: "let's do it, put it with the rest of the previews"): after the Last Stand it stays over the Void for 36 hours as a
#  shared boss of 100 sections (p442_fight.js); every section destroyed breaks a cube off it, it shatters when it falls or disperses
#  when time runs out. Fleets sent at an Assimilation Cube that has left for the Omega turn back with nothing lost. The owner preview
#  now plays the fight too (the hull falls section by section, then it shatters and the cubes disperse).
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
FIGHT = open("tools/patches/p442_fight.js").read()
# the schedule: the 15th
rep("DV_FIRST = Date.UTC(2026, 11, 11, 18)", "DV_FIRST = Date.UTC(2026, 10, 15, 18) /* v442 every 15th */")
rep("function dvStartOf(T) { const d = new Date(T); let s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), 11, 18); if (T < s) s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth() - 1, 11, 18); return s; }",
    "function dvStartOf(T) { const d = new Date(T); let s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), 15, 18); if (T < s) s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth() - 1, 15, 18); return s; }")
rep("s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, 11, 18); } return s; }", "s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, 15, 18); } return s; }")
# the timeline: the fight, and a break-up that waits for it
rep("war1: 200 * DV_M, ret: 205 * DV_M, end: 250 * DV_M };", "war1: 200 * DV_M, fight0: 205 * DV_M, get ret() { return G.dvRBv || 205 * DV_M; }, get end() { return this.ret + 45 * DV_M; } }; /* v442 it comes apart when it falls, or after its 36 hours */")
rep('e < DV.war1 ? "war" : e < DV.ret ? "after" : "ret";', 'e < DV.war1 ? "war" : e < DV.fight0 ? "after" : e < DV.ret ? "fight" : "ret";')
rep("const DV_SIM = [[0, 0], [15, DV.mig], [140, DV.act], [160, DV.combat], [176, DV.war0], [230, DV.war1], [238, DV.ret], [270, DV.end]];",
    "const DV_SIM = [[0, 0], [15, DV.mig], [140, DV.act], [160, DV.combat], [176, DV.war0], [230, DV.war1], [236, DV.fight0], [272, DV.fight0 + 39 * DV_M], [304, DV.fight0 + 84 * DV_M]];")
rep("function dvSimNow() { const C = G.dvSim,", "function dvSimNow() { G.dvRBv = DV.fight0 + 39 * DV_M; const C = G.dvSim,")
rep("const s0 = dvStartOf(T), e = T - s0; return e >= 0 && e < DV.end ?", "const s0 = dvStartOf(T), e = T - s0; G.dvRBv = omRB(s0); return e >= 0 && e < DV.end ?")
rep("best.ret = DV.ret + (N - 1 - i2) * 12 * DV_M / N; });", "best.retOff = (N - 1 - i2) * 12 * DV_M / N; });")
rep("function dvCube(c, e, D, o) { const s0 = D.s0,", "function dvCube(c, e, D, o) { c.ret = DV.ret + (c.retOff || 0); const s0 = D.s0,")
rep('if (e < c.ret) { o.x = S2.x; o.y = S2.y; o.z = S2.z; o.k = f2; o.al = 1; o.st = "locked"; o.lkT = c.lk2; return o; }',
    'if (e < c.ret) { const b = e >= DV.fight0 ? dvBrk(c, D, (G.dvP && G.dvP.N) || OM_SEG) : Infinity; /* v442 a section the fleets destroyed breaks off, dark, and drifts */\n    if (e >= b) { const a = dvEase(Math.min(1, (e - b) / 20e3)), d = 4 + 34 * a + (e - b) / 60e3 * 2, q = slotW([c.s2.p[0] + c.s2.n[0] * d, c.s2.p[1] + c.s2.n[1] * d - 6 * a, c.s2.p[2] + c.s2.n[2] * d], P[2]); o.x = q.x; o.y = q.y; o.z = q.z; o.k = f2 * .96; o.al = 1 - .45 * a; o.st = "broken"; o.brk = b; return o; }\n    o.x = S2.x; o.y = S2.y; o.z = S2.z; o.k = f2; o.al = 1; o.st = "locked"; o.lkT = c.lk2; return o; }')
rep('const lv = o.st === "locked" ?', 'const lv = o.st === "broken" ? 0 : o.st === "locked" ?')
rep("    if (o.st !== \"locked\") X.locked.delete(c.i); }", "    if (o.st !== \"locked\") X.locked.delete(c.i);\n    if (o.st === \"broken\" && !(X.brk || (X.brk = new Set())).has(c.i)) { X.brk.add(c.i); if (e - o.brk < 8000 * (D.rate || 1) * 3) dvFx(X, o, c.s2.n, 2.2, t); } }")
rep("/* the owner's preview: the whole event", FIGHT + "/* the owner's preview: the whole event")
rep("Cube Devastation in four and a half minutes.", "Cube Devastation in five minutes, the fight included.")
# fleets: the Omega Cube as a target
rep("f.wb ? WBO[f.wb] : f.pid === \"nexus\" ? NEXUS : G.byId[f.pid];", "f.wb ? WBO[f.wb] : f.om ? OMO : f.pid === \"nexus\" ? NEXUS : G.byId[f.pid];")
rep("wbById(id) || (id === \"nexus\" ? NEXUS : null);", "wbById(id) || (id === \"nexus\" ? NEXUS : id === \"omega\" ? OMO : null);")
rep("f.wb ? (f.phase = \"resolving\") : f.nid ?", "f.wb || f.om ? (f.phase = \"resolving\") : f.nid ?")
rep("{ if (f.wb) wbResolve(f); else if", "{ if (f.wb) wbResolve(f); else if (f.om) omResolve(f); else if")
# the cubes are away: no fight at a Cube that has left for the Omega
rep("  if (!x) return;\n  if (pirDown(x) > f.arrive)", "  if (!x) return;\n  if (x.boss && dvNow(f.arrive) && !G.dvSim) { note(`${x.name} had left to join the Omega Cube. Fleet returning, nothing lost.`, \"warn\"); return; } /* v442 */\n  if (pirDown(x) > f.arrive)")
rep("    const x = PB[d.id]; if (!x || !canPlay()) return; if (pirDown(x) > now()) return toast(`${x.name} is still regrouping.`, \"warn\");",
    "    const x = PB[d.id]; if (!x || !canPlay()) return; if (x.boss && dvLive(now()) && !G.dvSim) return toast(`${x.name} has left to join the Omega Cube. Attack the Omega Cube instead.`, \"warn\"); if (pirDown(x) > now()) return toast(`${x.name} is still regrouping.`, \"warn\");")
# battle reports: the Omega Cube is one colossal cube
rep("battle.superSide = r.wb ? \"d\" :", "battle.superSide = r.omega ? \"d\" : r.wb ? \"d\" :")
rep("const superSideOf = r => r ? (r.wb ? \"d\" :", "const superSideOf = r => r ? (r.omega ? \"d\" : r.wb ? \"d\" :")
rep("const scName = r => r && r.wb && WB[r.wb] ? WB[r.wb].n : \"Super Cube\";", "const scName = r => r && r.omega ? \"Omega Cube\" : r && r.wb && WB[r.wb] ? WB[r.wb].n : \"Super Cube\";")
# the panel, the band, the actions, the live record
rep("wboss: shWboss,", "wboss: shWboss, omega: shOmega,")
rep("  wboss: d => { const key = d.id, O = WBO[key];", """  omOpen: () => { pick = {}; for (const k in S.ships) if (S.ships[k] && SH[k]) pick[k] = S.ships[k]; if (view !== "galaxy") { view = "galaxy"; render(); } if (G3) { G3.cam.followFleet = null; G3.cam.follow = null; G3.cam.goal = { tx: 0, ty: DV_Y, tz: 0, dist: 520 }; } openSheet({ type: "omega" }); }, /* v442 */
  omGo: () => act(() => { if (!canPlay()) return; if (!omOn()) return toast("The Omega Cube can't be attacked right now.", "warn"); if (S.fleets.some(f => f.om && f.phase === "out")) return toast("A fleet is already on its way there.", "warn"); if (slotsFull()) return;
    const n = takeShips(pick); if (!Object.keys(n).length) return; const f = sendFleet(OMO, n, "attack", { om: 1 }); if (!f) return; closeSheet(); toast(`Fleet launched at the Omega Cube. Arrival in ${ftime(f.tt)}.`); }),
  wboss: d => { const key = d.id, O = WBO[key];""")
rep('db.doc("event/wboss").onSnapshot(s => { G.wb = s.exists ? s.data() : null; wbSeen(G.wb); wbClaim(); softRender(); }, () => {});',
    'db.doc("event/wboss").onSnapshot(s => { G.wb = s.exists ? s.data() : null; wbSeen(G.wb); wbClaim(); softRender(); }, () => {});\n    db.doc("event/omega").onSnapshot(s => { G.om = s.exists ? s.data() : null; OMN = null; omClaim(); softRender(); }, () => {}); /* v442 the Omega Cube */')
rep(".kv{display:grid;", "#omband{position:absolute;left:50%;transform:translateX(-50%);top:calc(var(--hudH,150px) + 8px);z-index:24}.omb{display:flex;align-items:center;gap:10px;padding:8px 14px;border-radius:14px;border:1px solid #5dff6a;background:rgba(4,22,10,.9);color:#d9ffe0;font-family:var(--f-display);font-size:13px;cursor:pointer;box-shadow:0 0 18px rgba(93,255,106,.35)}.omb b{color:#7dff90;letter-spacing:.06em}.omb i{font-style:normal;color:#ffd66a}\n.kv{display:grid;")
t = t.replace("const GAME_V = 441;", "const GAME_V = 442;")
open(p, "w").write(t); print("ok")
