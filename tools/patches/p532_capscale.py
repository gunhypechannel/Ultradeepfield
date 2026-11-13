# v532 the Reaper and the Discovery Class a little smaller in battle (owner: "Make discovery and reaper a tad smaller, they should
# [fit] well with the fleet's proportions and scale"). Battle lengths: Reaper 1.55 (was 1.72), Discovery Class 2.05 (was 2.6), so the
# ladder still reads Battleship .95 < Destroyer 1.16 < Citadel Supercarrier 1.5 < Reaper < Discovery Class < Cube Destroyer 4.3.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('k === "eclipse" ? 2.6 /* v531 the Discovery Class well above the Reaper (1.72) */ :', 'k === "eclipse" ? 2.05 /* v531; v532 a tad smaller: above the Reaper, in scale with the fleet */ : k === "dreadnought" ? 1.55 /* v532 the Reaper */ :')
s2 = re.sub(r"GAME_V = 531\b", "GAME_V = 532", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
