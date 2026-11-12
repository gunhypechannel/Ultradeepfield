# v498 (owner): "All 5 elementals should be smaller than the Pentarch" (they looked the same size or bigger). The Pentarch grows and the
# Elementals shrink a little: on the galaxy map the Pentarch is .72 -> 1.2 and each Elemental 1.3 -> 1.0
# (about 48 tall), so the Pentarch is clearly the largest; in battle reports the Pentarch already fills the view; the
# camera stands further from each Elemental (62 -> 86) so they read smaller.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('m3: "elemental", sc: 1.3', 'm3: "elemental", sc: 1.0', 5)
rep('m3: "pentarch", sc: .72', 'm3: "pentarch", sc: 1.2')
rep('elemental: [-.2, [-8, 4, 62], [0, 0, 0]]', 'elemental: [-.2, [-8, 4, 86], [0, 0, 0]]')
s = re.sub(r"GAME_V = 497\b", "GAME_V = 498", s)
open(P, 'w', encoding='utf-8').write(s); print('ok')
