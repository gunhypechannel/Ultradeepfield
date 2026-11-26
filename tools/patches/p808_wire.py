"""v808: the First Aperture hangs above Nhalis (height 20) instead of beside it, so no neighbouring world sits inside its ring."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 807;", "const GAME_V = 808;")
rep("function aetGatePos(T, out) { const q = aetNhalis(T, out), L = Math.hypot(q.x, q.z) || 1; q.x += q.x / L * 9; q.z += q.z / L * 9; q.y = 5; return q; }",
    "function aetGatePos(T, out) { const q = aetNhalis(T, out); q.y = 20; return q; } /* v808 above Nhalis: beside it, 17-19 worlds sat inside the ring */")
open(p, "w", encoding="utf-8").write(s)
print("ok")
