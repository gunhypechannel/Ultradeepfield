"""v798: every Mimic's mouth remade after the paintings (owner: "Fix all the mimics mouths they look nothing like the reference art").
The blunt capsule skull with a jaw hanging wide and a few thick cone teeth is now a long low wedge of a skull with a pointed snout,
brows over the eyes, jaws open at a snarl, packed with long curved needle fangs (two great fangs at the front of each jaw), cables
ribbing the snout and jaw, and the open mouth lined with glow in each unit's own colour. All 12 classes re-sculpted
(tools/sculpt/mim_sculpt.py, art/mimic/m/*.bin); mimWave's jaw snap still fits. Applies on top of v797."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 797;", "const GAME_V = 798;")
open(p, "w", encoding="utf-8").write(s)
print("ok")
