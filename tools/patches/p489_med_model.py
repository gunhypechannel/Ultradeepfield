# v489 Medusara, the Stone Gaze: the 3D model (BOSS3D.medusara, source tools/patches/p489_medusara.js), from the owner's art
# (assets/bosses/medusa/ref). The hunt: p489_med_hunt.py.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep("  // merge each group's static leaf meshes that share a material", open('tools/patches/p489_medusara.js').read() + "  // merge each group's static leaf meshes that share a material")
rep("omega, khezaroth, EL, prep };", "omega, khezaroth, medusara, EL, prep };")
s = re.sub(r"GAME_V = 488\b", "GAME_V = 489", s)
open(P, 'w').write(s)
