"""v753: the Mimic sculpted as legless cable ships (loader p753_mim.js, meshes docs/art/mimic/m/<cls>.bin listed in
tools/sculpt/mim_sc.json); mimWave drops the legs for a sculpted class."""
import sys, os, json
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(D, "..", "..")
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 752;", "const GAME_V = 753;")
js = open(os.path.join(D, "p753_mim.js"), encoding="utf-8").read().strip()
sc = json.load(open(os.path.join(R, "tools", "sculpt", "mim_sc.json")))
have = {k: v for k, v in sc.items() if os.path.exists(os.path.join(R, "docs", "art", "mimic", "m", k + ".bin"))}
js = js.replace("const MIM_SC = {}, MIM_GEO = {},", "const MIM_SC = " + json.dumps(have, separators=(",", ":")) + ", MIM_GEO = {},")
rep("\nfunction mimWave(k) {", "\n" + js + "\nfunction mimWave(k) {")
rep("""function buildMimic(cls) {
""", """function buildMimic(cls) { mimSculptLoad(cls); if (MIM_GEO[cls]) return mimSculpted(cls); /* v753 */
""")
rep("""  let w = `vec3 p = position; float ph = mt * ${W2};`;
  if (D.sac) w +=""", """  let w = `vec3 p = position; float ph = mt * ${W2};`;
  if (MIM_SC[k]) w += ` float lw = 0.; transformed.y += .1 * sin(mt * ${W1}); transformed.z += .04 * sin(mt * ${W1} + p.x * .7);`; /* v753 a sculpted Mimic has no legs: it floats like a ship */
  else if (D.sac) w +=""")
rep("""const m = buildMonster("slevi"); m.traverse(o => { if (!o.isMesh || !o.material || Array.isArray(o.material)) return; const mt = o.material.clone();""",
    """const m = buildMonster("slevi"); m.traverse(o => { if (!o.isMesh || !o.material || Array.isArray(o.material)) return; const mt = o.material.clone();
      if (o.userData.sculpt) { mt.onBeforeCompile = o.material.userData.obc; mt.userData.obc = mt.onBeforeCompile; mt.customProgramCacheKey = () => "cntsculpt2"; mt.color.setRGB(.55, .5, .68); o.material = mt; return; } /* v753 the sculpted Leviathan, its body gone dark */""")
# when the Leviathan's sculpt arrives, the fallen one (clevd) is rebuilt from it too
rep("""function monSculptSwap(k) { try {""", """function monSculptSwap(k) { try { if (k === "slevi" && typeof crcSculptSwap === "function") crcSculptSwap("clevd");""")
open(p, "w", encoding="utf-8").write(s)
print("ok", len(have), "sculpted:", " ".join(sorted(have)))
