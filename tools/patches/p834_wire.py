"""v834: painted cards for the Continuum Neural Corvette and Fabrication Carrier (owner-supplied art, art/rwar/c_corvette.webp and c_fabcarrier.webp)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 833;", "const GAME_V = 834;")
rep('const CNT_ART = { cnint: "interceptor",', 'const CNT_ART = { cncor: "c_corvette", cnfab: "c_fabcarrier", cnint: "interceptor",')
open(p, "w", encoding="utf-8").write(s); print("ok")
