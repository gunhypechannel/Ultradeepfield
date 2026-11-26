"""v794: the Leviathan reshaped as a whale (owner: "build it all"). Its sculpt was an eel; it is now a broad, tapering whale body
with the armoured head and jaw kept, a spiked ridge, and horizontal tail flukes (tools/sculpt/mon2_sculpt.py, art/mon/m/slevi.bin).
It swims like a whale now: an up-and-down fluke stroke instead of a side-to-side S wave, with the jaw opening as before.
Applies on top of v793."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 793;", "const GAME_V = 794;")
rep('slevi: "float tl = clamp((3.2 - position.x) / 11.8, 0., 1.); transformed.z += (.12 + .85 * tl) * sin(position.x * .62 + mt * 2.4); transformed.y += .2 * tl * sin(position.x * .4 + mt * 1.6);',
    'slevi: "float tl = clamp((2.4 - position.x) / 10.5, 0., 1.); transformed.y += (.04 + .95 * tl * tl) * sin(position.x * .42 + mt * 1.5); transformed.z += .08 * tl * sin(position.x * .3 + mt * .9);')
open(p, "w", encoding="utf-8").write(s)
print("ok")
