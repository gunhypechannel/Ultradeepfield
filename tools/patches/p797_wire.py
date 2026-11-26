"""v797: the three Mimic units that still looked alike get parts of their own (owner: "continue", finishing up). The Stalker, after
its painting, gets a writhing mass of cables arching high over its back and hooked grapple tendrils reaching forward under its
jaws; the Hunter twin long blades swept back from its flanks and a lance under its prow; the Assimilator bigger, plainly visible
slabs of stolen starship plating. Sculpt only (tools/sculpt/mim_sculpt.py, art/mimic/m/{mstalk,mhunt,massim}.bin). Applies on top of v796."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 796;", "const GAME_V = 797;")
open(p, "w", encoding="utf-8").write(s)
print("ok")
