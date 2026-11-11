# v447 the Cube Devastation countdown becomes a screen of living code (see p447_cdmatrix.js)
import re, os
P = 'docs/index.html'; s = open(P).read()
i = s.index("function dvCdBuild(W) {"); k = "C.arcs.material.opacity = .7 + .3 * Math.random(); }"; j = s.index(k, i) + len(k)
old = s[i:j]; a = old.index("  { const cp = W.camera.position"); b = old.index("  C.grp.quaternion.copy(W.camera.quaternion);")
new = open(os.path.join(os.path.dirname(__file__), 'p447_cdmatrix.js')).read().rstrip("\n").replace("  /*POS*/\n", old[a:b])
s = s[:i] + new + s[j:]
s, n = re.subn(r"GAME_V = 446\b", "GAME_V = 447", s); assert n == 1
open(P, 'w').write(s)
