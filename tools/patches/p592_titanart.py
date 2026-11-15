# v592 the owner's new Titan paintings (Harbinger green, Sovereign gold and white, Armageddon orange) as their card art; docs/art/*.webp
# replaced in place (1100x785 crops), so the three card URLs get ?v=592 to skip the old cached pictures
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('''"radar robotics dome bigDome metalMine metalStore nanite interceptor ballistic flagDock").split(" ").map(k => [k, `art/${k}.webp`]));''',
    '''"radar robotics dome bigDome metalMine metalStore nanite interceptor ballistic flagDock").split(" ").map(k => [k, `art/${k}.webp`]));
for (const k of ["armageddon", "sovereign", "harbinger"]) ART[k] = `art/${k}.webp?v=592`; /* v592 the owner's new Titan paintings */''')
rep('"img": "art/armageddon.webp"', '"img": "art/armageddon.webp?v=592"')
s2 = re.sub(r"GAME_V = 591\b", "GAME_V = 592", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
