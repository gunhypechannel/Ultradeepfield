"""v759: the Shard Colossus sculpted (tools/sculpt/wb_col_sculpt.py <part> <outdir>, packed to docs/art/boss/m/col_<part>.bin).
Owner: "Build all of them!" (the World Bosses, one at a time). Every rock of BOSS3D.colossus's rig (the floating mine chunk, chest,
pelvis, head, shoulders, upper arms, forearms, hands, thighs, shins, feet) is replaced by its sculpt in the same pivot frame, so the
rig, its moves and its effects are unchanged; the left side mirrors the right. The parts load the first time the boss is drawn; until
then the old rocks stand in, and when they arrive the map's model and the card art are rebuilt. Applies on top of v758."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 758;", "const GAME_V = 759;")
# the loader, beside the other sculpt loaders
rep("""function sculptGhost(g, geo, sc) {""", """/* v759 World Boss sculpts: each boss's rig parts in art/boss/m/<file prefix>_<part>.bin, loaded together the first time it is built */
const WB_SC = { colossus: ["col", ["chest", "pelvis", "head", "shoulder", "uarm", "farm", "hand", "thigh", "shin", "foot", "plat"]] }, WB_GEO = {};
function wbSculpt(b) { const D = WB_SC[b]; if (!D || !TH || typeof fetch !== "function") return null; if (WB_GEO[b]) return WB_GEO[b]; const L = wbSculpt.L || (wbSculpt.L = {}); if (L[b]) return null; L[b] = 1;
  const out = {}; Promise.all(D[1].map(k => fetch("art/boss/m/" + D[0] + "_" + k + ".bin").then(r => r.ok ? r.arrayBuffer() : Promise.reject(Error("HTTP " + r.status))).then(buf => { out[k] = cntMeshGeo(buf); })))
    .then(() => { WB_GEO[b] = out; wbSculptSwap(b); }).catch(e => console.warn("boss sculpt " + b, e && e.message)); return null; }
function wbScMat() { const b = cntMeshMat(), m = b.clone(); m.onBeforeCompile = b.userData.obc; m.userData.obc = b.userData.obc; m.customProgramCacheKey = () => "cntsculpt2"; m.envMapIntensity = .45; return m; } /* its own copy: the boss's renderer sets its envMap */
function wbSculptSwap(b) { try { const ks = Object.keys(WB).filter(k => WB[k].m3 === b); if (G3 && G3.wbM) for (const k of ks) { const M = G3.wbM[k]; if (M && M.b && !M.pd) { try { G3.scene.remove(M.b.grp); } catch (e) {} delete G3.wbM[k]; } }
  if (typeof WBR !== "undefined" && WBR.key && ks.includes(WBR.key)) WBR.key = null; /* the battle and card view rebuilds it */ } catch (e) { console.warn("boss sculpt swap", e); } }
window.wbSculpt = wbSculpt; window.wbScMat = wbScMat; /* BOSS3D lives in its own script */
function sculptGhost(g, geo, sc) {""")
# the rig takes the sculpts
rep("""    const rock = (r, det, sx, sy, sz) => { const g = new TH.IcosahedronGeometry(r, det),""",
    """    const SG = root.wbSculpt ? root.wbSculpt("colossus") : null, SM = SG ? root.wbScMat() : null; /* v759 the sculpted rig parts, when they have arrived */
    const rk = (nm, mir, ...a) => { if (SG && SG[nm]) { const m = new TH.Mesh(SG[nm], SM); m.userData.sculpt = 1; if (mir < 0) m.scale.x = -1; return m; } return rock(...a); };
    const rock = (r, det, sx, sy, sz) => { const g = new TH.IcosahedronGeometry(r, det),""")
rep("{ const pl = rock(8.5, 2, 1, .3, 1); pl.position.y = -1.5;", "{ const pl = rk(\"plat\", 1, 8.5, 2, 1, .3, 1); pl.position.y = -1.5;")
rep("const th = rock(1.3, 1, .95, 2.2, .95); th.position.set(sx * .3, -1.6, 0);", "const th = rk(\"thigh\", sx, 1.3, 1, .95, 2.2, .95); th.position.set(sx * .3, -1.6, 0);")
rep("hip.add(kn); const sh = rock(1.25, 1, 1, 2.1, 1);", "hip.add(kn); const sh = rk(\"shin\", sx, 1.25, 1, 1, 2.1, 1);")
rep("const ft = rock(1.4, 1, 1.25, .6, 1.6); ft.position.set(0, -3.25, .5);", "const ft = rk(\"foot\", sx, 1.4, 1, 1.25, .6, 1.6); ft.position.set(0, -3.25, .5);")
rep("{ const c = rock(3.2, 1, 1.15, 1.05, .85); T.add(c); const pv = rock(1.9, 1, 1.3, .8, 1);", "{ const c = rk(\"chest\", 1, 3.2, 1, 1.15, 1.05, .85); T.add(c); const pv = rk(\"pelvis\", 1, 1.9, 1, 1.3, .8, 1);")
rep("{ const h = rock(1.15, 1, 1, 1.1, 1); head.add(h);", "{ const h = rk(\"head\", 1, 1.15, 1, 1, 1.1, 1); head.add(h);")
rep("      sh.add(rock(1.5, 1, 1, 1, 1));", "      sh.add(rk(\"shoulder\", sx, 1.5, 1, 1, 1, 1));")
rep("const up = rock(1, 1, .85, 2.2, .85); up.position.set(sx * .8, -2, 0);", "const up = rk(\"uarm\", sx, 1, 1, .85, 2.2, .85); up.position.set(sx * .8, -2, 0);")
rep("const fa = rock(1.05, 1, .95, 2.1, .95); fa.position.set(0, -1.9, .4);", "const fa = rk(\"farm\", sx, 1.05, 1, .95, 2.1, .95); fa.position.set(0, -1.9, .4);")
rep("hand.add(rock(.95, 1, 1, .9, 1));", "hand.add(rk(\"hand\", sx, .95, 1, 1, .9, 1));")
open(p, "w", encoding="utf-8").write(s)
print("ok")
s = open(p, encoding="utf-8").read()
rep("for (const c of o.children) { if (!c.isMesh || c.userData.dyn || c.children.length", "for (const c of o.children) { if (!c.isMesh || c.userData.dyn || c.userData.sculpt || c.children.length") # a sculpt keeps its own colours (bake merges by material)
open(p, "w", encoding="utf-8").write(s)
print("ok2")
