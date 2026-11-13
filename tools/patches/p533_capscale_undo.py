# v533 the Reaper and Discovery Class sizes back to v531 (owner, right after v532: "Never mind keep the ships sizes the same").
# Battle lengths: Reaper back to its ladder value 1.72, Discovery Class 2.6.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('k === "eclipse" ? 2.05 /* v531; v532 a tad smaller: above the Reaper, in scale with the fleet */ : k === "dreadnought" ? 1.55 /* v532 the Reaper */ :', 'k === "eclipse" ? 2.6 /* v531 the Discovery Class well above the Reaper (1.72); v533 kept */ :')
s2 = re.sub(r"GAME_V = 532\b", "GAME_V = 533", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
