"""v743: seven more Continuum classes sculpted after their paintings; the sculpted meshes now face outward (v742's were inside out)."""
import sys, os, re
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:120]); s = s.replace(a, b)
rep("const GAME_V = 742;", "const GAME_V = 743;")
i = s.index("const CNT_SC = {"); j = s.index("\n", s.index("function cntSculptLoad()")); j = s.index("\n", j + 1)
s = s[:i] + """/* each sculpted class: its scale into the procedural hull's frame and its engine mouths [x, y, z, radius]; a class loads its own file
   the first time it is built (v743: all eleven; the Corvette, Fabrication Carrier and Command Frame have no painting yet and follow the family's style) */
const CNT_SC = { cnark: { s: .8, eng: [[-4.92, .04, .44, .34], [-4.92, .04, -.44, .34], [-4.92, .5, .44, .24], [-4.92, .5, -.44, .24], [-4.92, -.44, .44, .24], [-4.92, -.44, -.44, .24]] },
  cnint: { s: 1, eng: [[-2.35, .05, .28, .2], [-2.35, .05, -.28, .2]] }, cnexe: { s: 1, eng: [[-2.7, .05, .35, .27], [-2.7, .05, -.35, .27]] },
  cnasm: { s: 1, eng: [[-2.2, .05, .16, .14], [-2.2, .05, -.16, .14]] }, cndre: { s: 1, eng: [[-3.75, .1, .5, .34], [-3.75, .1, -.5, .34], [-3.75, .55, .25, .26], [-3.75, .55, -.25, .26], [-3.75, -.35, .25, .26], [-3.75, -.35, -.25, .26]] },
  cnrel: { s: 1, eng: [] }, cnprime: { s: 1, eng: [] }, cneter: { s: 1, eng: [[-1.7, 0, .38, .28], [-1.7, 0, -.38, .28]] },
  cncor: { s: 1, eng: [[-2.3, 0, .2, .2], [-2.3, 0, -.2, .2]] }, cnfab: { s: 1, eng: [[-3.85, 0, .55, .32], [-3.85, 0, -.55, .32], [-3.85, .3, 0, .26]] },
  cncom: { s: 1, eng: [[-3.75, .1, .5, .34], [-3.75, .1, -.5, .34], [-3.75, .55, .22, .24], [-3.75, .55, -.22, .24], [-3.75, -.35, .22, .24], [-3.75, -.35, -.22, .24]] } }, CNT_GEO = {};
function cntSculptLoad(k) { if (!CNT_SC[k] || !TH || typeof fetch !== "function") return; const L = cntSculptLoad.L || (cntSculptLoad.L = {}); if (L[k]) return; L[k] = 1;
  fetch("art/rwar/m/" + k + ".bin").then(r => r.ok ? r.arrayBuffer() : Promise.reject(Error("HTTP " + r.status))).then(b => { CNT_GEO[k] = cntMeshGeo(b); cntSculptSwap(k); }).catch(e => console.warn("sculpt " + k, e && e.message)); }""" + s[j:]
rep("function buildCnt(k) { cntSculptLoad(); if (CNT_GEO[k])", "function buildCnt(k) { cntSculptLoad(k); if (CNT_GEO[k])")
rep('"reflectedLight.directSpecular *= mix(.16, 1., smoothstep(.03, .3, max(diffuseColor.r, max(diffuseColor.g, diffuseColor.b))));\\n#include <aomap_fragment>"',
    '"reflectedLight.directSpecular *= mix(.14, 1., smoothstep(.04, .3, max(diffuseColor.r, max(diffuseColor.g, diffuseColor.b)))) * mix(.3, 1., smoothstep(.12, .55, saturate(dot(geometry.normal, geometry.viewDir))));\\n#include <aomap_fragment>"')
rep('m.customProgramCacheKey = () => "cntsculpt1";', 'm.customProgramCacheKey = () => "cntsculpt2";')
open(p, "w", encoding="utf-8").write(s)
print("ok")
