"""v850: the Battle for the Cube's siege fleet, its derelicts and its debris share one size, nearer the map's flagships (owner: "shrink
the super cube siege fleet a little and the debris to scale with the size of the new flagship scale on map ... find some size in the
middle that works best and set them all the same"). Before: squadrons x1.65-2.2, the three capital ships x3.45, derelicts x2-3.6 (a
battleship 9-18 world units long, planets 1.3 across, a map flagship about 1); fragments 1.3-5.7. Now every siege hull and derelict is
x1.2 (a battleship about 6.3, under five planets), and the fragments 1.1-3. (x0.8 was tried: the ships all but vanished.)"""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 849;", "const GAME_V = 850;")
rep("const CUBE_H = 2.5, CUBE_CORNER = 26,", "const CW_S = 1.2; /* v850 one size for every siege hull and derelict */\nconst CUBE_H = 2.5, CUBE_CORNER = 26,")
rep("sc = q.k * (q.cap ? 1 : 1.1) * SB;", "sc = CW_S;")
rep("k: 2 + r() * 1.6, f: sp(", "k: CW_S + r() * 0, f: sp(")
rep("k: .55 + r() * r() * 2.2, orb:", "k: .45 + r() * r() * .8, orb:")
open(p, "w", encoding="utf-8").write(s); print("ok")
