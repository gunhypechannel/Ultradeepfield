"""v742: the sculpting pipeline: the Resurrection Ark is a sculpted, baked mesh after the owner's painting (tools/sculpt)."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:120]); s = s.replace(a, b)
rep("const GAME_V = 741;", "const GAME_V = 742;")
rep("function buildCnt(k) { const C = cntMats(),", open(os.path.join(D, "p742_sculpt.js"), encoding="utf-8").read().strip() + "\nfunction buildCnt(k) { cntSculptLoad(); if (CNT_GEO[k]) return cntSculpted(k); const C = cntMats(),")
# a sculpted mesh carries its own attributes: the merge keeps it whole rather than flattening it to position/normal/uv
rep("src.traverse(o => { if (!o.isMesh || o.isInstancedMesh) { if (o.isPoints || o.isSprite || o.isInstancedMesh) keep.push(o); return; }",
    "src.traverse(o => { if (!o.isMesh || o.isInstancedMesh || o.userData.sculpt) { if (o.isPoints || o.isSprite || o.isInstancedMesh || o.userData.sculpt) keep.push(o); return; }")
# a species with no swim motion keeps its materials (the Continuum's map models used to get a shader with "undefined" in it)
rep("function monAnimate(master, kind, U) { const done = new Map();", "function monAnimate(master, kind, U) { if (!MON_WAVE[kind] && CNT_M[kind]) return; /* v742 */ const done = new Map();")
open(p, "w", encoding="utf-8").write(s)
print("ok")
