"""v756: the last aliens and event units sculpted (tools/sculpt/mon4_sculpt.py): the Hive (drone, spitter, brute, lord, leviathan),
the Collective (cdrone, cube, sphere), Omega's Neural Node and Assimilation Pylon, the Carcinid Breach nest and the fallen Leviathan.
Owner: "Build all of them!" Applies on top of v755."""
import sys, re, json
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 755;", "const GAME_V = 756;")
# the alien sculpts ride on the monster loader (art/mon/m/), with an optional turn
def addsc(name, extra):
    global s
    m = re.search(r"const " + name + r" = (\{.*?\}), ", s); assert m, name
    d = json.loads(m.group(1)); d.update(extra); s = s.replace(m.group(0), "const " + name + " = " + json.dumps(d, separators=(",", ":")) + ", ", 1)
addsc("MON_SC", {"drone": {"s": 1}, "spitter": {"s": 1}, "brute": {"s": 1}, "lord": {"s": 1}, "leviathan": {"s": 1}, "cdrone": {"s": 1, "r": [.2, .5, 0]}, "cube": {"s": 1, "r": [.4, .6, 0]}, "sphere": {"s": 1}, "drone_": {}})
s = s.replace(',"drone_":{}', "")
addsc("MIM_SC", {"mnode": {"g": 1}, "mpylon": {"g": 1}})
addsc("CRC_SC", {"cnest": {"s": 1, "g": 1}, "clevd": {"s": 1}})
rep("""m.userData.sculpt = 1; m.scale.setScalar(D.s || 1); g.add(m); sculptGhost(g, MON_GEO[k + "_g"], D.s); g.userData.eng = [];""",
    """m.userData.sculpt = 1; m.scale.setScalar(D.s || 1); if (D.r) m.rotation.set(D.r[0], D.r[1], D.r[2]); g.add(m); sculptGhost(g, MON_GEO[k + "_g"], D.s); if (D.r && g.children[1]) g.children[1].rotation.copy(m.rotation); g.userData.eng = [];""")
rep("""  if (k === "cube" || k === "sphere" || k === "cdrone") return buildCollective(k);
  const A = alienMats(),""", """  if (MON_SC[k]) { monSculptLoad(k); if (MON_GEO[k]) return monSculpted(k); } /* v756 the Hive and the Collective, sculpted */
  if (k === "cube" || k === "sphere" || k === "cdrone") return buildCollective(k);
  const A = alienMats(),""")
# the Carcinid loader learns the see-through second mesh too
rep("""  fetch("art/carcinid/m/" + k + ".bin").then(r => r.ok ? r.arrayBuffer() : Promise.reject(Error("HTTP " + r.status))).then(b => { CRC_GEO[k] = cntMeshGeo(b); crcSculptSwap(k); }).catch(e => console.warn("sculpt " + k, e && e.message)); }""",
    """  sculptFetch("art/carcinid/m/", k, CRC_SC[k].g, (a, b) => { CRC_GEO[k + "_g"] = b; CRC_GEO[k] = a; crcSculptSwap(k); }); }""")
rep("""function crcSculpted(k) { const D = CRC_SC[k], g = new TH.Group(), m = new TH.Mesh(CRC_GEO[k], cntMeshMat()); m.userData.sculpt = 1; m.scale.setScalar(D.s || 1); g.add(m);""",
    """function crcSculpted(k) { const D = CRC_SC[k], g = new TH.Group(), m = new TH.Mesh(CRC_GEO[k], cntMeshMat()); m.userData.sculpt = 1; m.scale.setScalar(D.s || 1); g.add(m); sculptGhost(g, CRC_GEO[k + "_g"], D.s);""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
