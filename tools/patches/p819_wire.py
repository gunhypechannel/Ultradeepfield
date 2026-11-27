"""v819: seven more monsters rebuilt after their card art (owner: "work on rock eaters, petrified sentinels and beehives, also we need to fix
celestial serpent and I don't like the new small cubes I want them to look a lot better and closer to the reference", then "Build all").
The sculpts are in tools/sculpt/mon3_sculpt.py (Rock Eaters, Petrified Sentinel, Starhive, Celestial Serpent) and mon4_sculpt.py (the
Collective Drone, Assimilation Cube, Tactical Sphere); here only the Drone's scale changes, so its wider claw-spread keeps about its old
footprint in battle."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 818;", "const GAME_V = 819;")
rep('"cdrone":{"s":1,"r":[0.2,0.5,0]}', '"cdrone":{"s":0.7,"r":[0.2,0.5,0]}')
open(p, "w", encoding="utf-8").write(s); print("ok")
