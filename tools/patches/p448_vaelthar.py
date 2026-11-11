# v448 Vaelthar, the Celestial Ruin: the 3D model, its wheel and its moves (p448_vaelthar.js), in the BOSS3D library
import re, os
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
js = open(os.path.join(os.path.dirname(__file__), 'p448_vaelthar.js')).read()
rep("  // merge each group's static leaf meshes that share a material (same look), so a boss costs tens of draw calls, not hundreds\n", js + "  // merge each group's static leaf meshes that share a material (same look), so a boss costs tens of draw calls, not hundreds\n")
rep("colossus, station, elemental, pentarch, EL, prep };", "colossus, station, elemental, pentarch, vaelthar, EL, prep };")
s, n = re.subn(r"GAME_V = 447\b", "GAME_V = 448", s); assert n == 1
open(P, 'w').write(s)
