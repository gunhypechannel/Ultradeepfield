"""v826: the Celestial Serpent's face (owner: "celestial serpant model still broken, whats going on with its face"). Since v819 the sculpt's
skull and jaw (tools/sculpt/mon3_sculpt.py serpent) were empty: lathe_x wants its profile snout first and they were listed back to front,
so the horns, frill, eyes, teeth and mouth glow floated with no head under them. Fixed there and rebuilt art/mon/m/cserp.bin; this only
bumps the version."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 825;", "const GAME_V = 826;")
open(p, "w", encoding="utf-8").write(s); print("ok")
