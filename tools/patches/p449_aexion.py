# v449 Aexion, the Warform Sovereign: one rigged model with a ship pose and a mech pose, the staged transformation and its weapons (p449_aexion.js)
import re, os
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
js = open(os.path.join(os.path.dirname(__file__), 'p449_aexion.js')).read()
rep("  // merge each group's static leaf meshes that share a material (same look), so a boss costs tens of draw calls, not hundreds\n", js + "  // merge each group's static leaf meshes that share a material (same look), so a boss costs tens of draw calls, not hundreds\n")
rep("pentarch, vaelthar, EL, prep };", "pentarch, vaelthar, aexion, EL, prep };")
s = re.sub(r"GAME_V = 44[89]\b", "GAME_V = 449", s)
open(P, 'w').write(s)
