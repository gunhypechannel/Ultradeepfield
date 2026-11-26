"""v799: the Mimics' faces wrapped in cables, as in the paintings (owner: "continue", after the v798 mouths). Seven cables a side
hug each skull from behind the head toward the snout, over the brow and down the cheek, leaving the eyes and the snarl clear.
All 12 classes re-sculpted (tools/sculpt/mim_sculpt.py, art/mimic/m/*.bin). Applies on top of v798."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 798;", "const GAME_V = 799;")
open(p, "w", encoding="utf-8").write(s)
print("ok")
