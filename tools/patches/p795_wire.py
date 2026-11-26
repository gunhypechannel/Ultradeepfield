"""v795: the Leviathan whale refined after its painting (owner: "go back and refine the whale"). A longer armoured head with a
snout, brow plates over the eyes, a glowing mouth line and throat pleats, a pale belly, armour plates over the back only, a spiked
crest from the brow down the back, glowing veins in the front fins, and long veins of light along the flanks instead of spots.
Sculpt only (tools/sculpt/mon2_sculpt.py, art/mon/m/slevi.bin). Applies on top of v794."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 794;", "const GAME_V = 795;")
open(p, "w", encoding="utf-8").write(s)
print("ok")
