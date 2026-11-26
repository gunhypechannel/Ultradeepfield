"""v785: the hunt monsters sharper and closer to their paintings (owner: "the shark armament looks dull and unrealistic, I want them
to feel like their art"; then "build it all").
- Every sculpted hunt monster gets its own material (it shared the plain matte sculpt material): glossier, wetter surfaces with
  sharper highlights, brighter glowing parts, a rim light in the species' own colour round its silhouette, and a slow pulse of its
  glow while it swims.
- The Void Shark re-sculpted from its painting (tools/sculpt/mon_sculpt.py, art/mon/m/swhale.bin): dark steel back and pale belly
  with a mottled hide and armour seams, eight branching scars of blue light a side, glowing eyes, a wider gape with bigger, denser
  rows of teeth, and four armoured twin laser turrets (two on the back, one on each flank) with sights, muzzle bands and cyan-lit
  barrels, at higher detail (40,000 triangles, was 24,000).
Applies on top of v784."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 784;", "const GAME_V = 785;")
rep("function monSculpted(k) { const D = MON_SC[k], g = new TH.Group(), m = new TH.Mesh(MON_GEO[k], cntMeshMat());",
r'''/* v785 each hunt monster's own sculpt material: wetter and sharper, brighter glow, a rim light in its colour, its glow pulsing as it swims */
function monSculptMat(k) { const C = monSculptMat.C || (monSculptMat.C = {}); if (C[k]) return C[k]; const b = cntMeshMat(), m = b.clone(), D = typeof MON !== "undefined" && MON[k], rgb = (D && D.rgb ? D.rgb : "140,200,255").split(",").map(v => (+v / 255).toFixed(3)).join(", ");
  const obc = sh => { b.userData.obc(sh); sh.vertexShader = sh.vertexShader.replace("#include <common>", "#include <common>\nvarying vec3 vMP;").replace("#include <begin_vertex>", "#include <begin_vertex>\nvMP = position;");
    sh.fragmentShader = sh.fragmentShader.replace("#include <common>", "#include <common>\nvarying vec3 vMP;").replace("roughnessFactor = max(.05, vRM.x);", "roughnessFactor = max(.04, vRM.x * .55);")
      .replace("totalEmissiveRadiance += vEm;", "totalEmissiveRadiance += vEm * 1.7; { float fr = pow(1. - saturate(abs(dot(normal, normalize(vViewPosition)))), 3.); totalEmissiveRadiance += vec3(" + rgb + ") * fr * .26; }"); };
  m.envMapIntensity = .75; m.onBeforeCompile = obc; m.userData.obc = obc; m.userData.pulse = "(1. + .55 * pow(.5 + .5 * sin(uMT * 2. - vMP.x * 1.4), 6.))"; m.customProgramCacheKey = () => "monsculpt-" + k; return C[k] = m; }
function monSculpted(k) { const D = MON_SC[k], g = new TH.Group(), m = new TH.Mesh(MON_GEO[k], monSculptMat(k));''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
