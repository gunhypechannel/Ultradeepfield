"""v790: the Comet Ram blue and icy (owner: "comet rams could look more blue and icy like its reference art"). Its lore is a horned beast
of ice riding its own comet: blue-grey stone, cracks glowing ice-blue, frosted silver-blue horns, and a comet tail of glowing ice
shards (v787 had made it bronze and fire). Sculpt only (tools/sculpt/mon_sculpt.py, art/mon/m/cram.bin). Applies on top of v789."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 789;", "const GAME_V = 790;")
open(p, "w", encoding="utf-8").write(s)
print("ok")
