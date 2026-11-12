# v488 Khezaroth, the Dark Matter Sphinx: the 3D model (BOSS3D.khezaroth, source tools/patches/p488_khezaroth.js), built from the owner's
# art and brief (assets/bosses/khezaroth/ref). The hunt itself comes in v489.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
src = open('tools/patches/p488_khezaroth.js').read()
rep("  // merge each group's static leaf meshes that share a material", src + "  // merge each group's static leaf meshes that share a material")
rep("station, elemental, pentarch, vaelthar, aexion, omega, EL, prep };", "station, elemental, pentarch, vaelthar, aexion, omega, khezaroth, EL, prep };")
rep("if (WBR.b.debris) WBR.b.debris.visible = false; /* v486 */", "if (WBR.b.debris) { WBR.b.debris.visible = false; WBR.b.noDeb = 1; } /* v486, v488 */")
s = re.sub(r"GAME_V = 487\b", "GAME_V = 488", s)
open(P, 'w').write(s)
