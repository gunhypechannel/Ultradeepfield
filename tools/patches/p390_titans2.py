# v390 (owner feedback on the titans): the Shard Colossus loses the mining gantries; the Event Horizon Wyrm orbits opposite the
# Super Cube (same orbit, half a turn away) so it never crowds the Cube; the Iron Tyrant cruises high above the worlds with its
# claw hanging down at them; worlds near the Brood Matriarch's nest turn infected green.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep('if (key === "wym") { const r = LAYERS[5].r1 * .86, a = (hash("wym" + c2) % 6283) / 1000 + TAU * (T - WB2_BASE) / (9 * 3600e3); o.x = Math.cos(a) * r; o.z = Math.sin(a) * r; o.y = 14 + 6 * Math.sin(a * 3); return o; }',
    'if (key === "wym") { const q = P3(WB_WYM, T, WBS); o.x = q.x; o.z = q.z; o.y = q.y + 10 + 3 * Math.sin(T / 9e5); return o; } // on the Cube\'s orbit, half a turn away from it')
rep("let WB_LANE = null, WB_MINE = null;", "let WB_LANE = null, WB_MINE = null; const WB_WYM = { r: 26 * SC, a0: 1.2 + Math.PI };")
rep("o.y = A.y + (B.y - A.y) * k + 4 + Math.sin(f * Math.PI) * 10; return o; }", "o.y = A.y + (B.y - A.y) * k + 30 + Math.sin(f * Math.PI) * 6; return o; } // high above the worlds, claw hanging down")
# the Matriarch's infection: worlds near her nest are tinted green
rep("  for (const id of near) {\n    const p = G.byId[id]; if (!p) continue; seen.add(id); let o = W.planets.get(id);",
    "  const INF = wbInfect(T);\n  for (const id of near) {\n    const p = G.byId[id]; if (!p) continue; seen.add(id); let o = W.planets.get(id);")
rep("e.mesh.setColorAt(i, fg ? FOGC : p.tn && !pxOf(p) ? tintC(p.tn) : WHITEC);", "e.mesh.setColorAt(i, fg ? FOGC : INF && !pxOf(p) && (q.x - INF.x) ** 2 + (q.z - INF.z) ** 2 < INF.r2 ? INFC : p.tn && !pxOf(p) ? tintC(p.tn) : WHITEC);")
rep("const wbHp = (k, T) =>", """const INFC = new TH.Color(.42, 1, .22); let WB_INF = null; // v390: the worlds round the Brood Matriarch's nest, infected green while she lives
function wbInfect(T) { if (WB_INF && Math.abs(T - WB_INF.T) < 2000) return WB_INF.v; let v = null; try { if (wbAlive("brd", T)) { const q = wbPos("brd", T, {}); v = { x: q.x, z: q.z, r2: 85 * 85 }; } } catch (e) {} WB_INF = { T, v }; return v; }
const wbHp = (k, T) =>""")
rep('d: "The Hive\'s queen, nesting in the Far Reach.', 'd: "The Hive\'s queen, nesting in the Far Reach; the worlds round her nest turn infected green.')
open(p, "w").write(t); print("ok")
