# v514 a space monster fights as one creature (owner: the battle replay showed several of them). The simulator used to split every
# stack into a few squadrons (a pack of 6 Space Squids became two squads of 3, drawn as two monsters); from battle rules v6 a
# space monster's pack stays one squadron, drawn as one creature. Older reports (v3-v5) still replay exactly as they were fought.
# The server's fight check accepts v6 (settle_fight redeployed with the new sim.js).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const CB_V = 5, CB_OK = v => v === 3 || v === 4 || v === 5,', 'const CB_V = 6, CB_OK = v => v === 3 || v === 4 || v === 5 || v === 6, /* v6: a space monster\'s pack is one squadron */')
rep('V4 = (o.v || CB_V) >= 4, V5 = (o.v || CB_V) >= 5;', 'V4 = (o.v || CB_V) >= 4, V5 = (o.v || CB_V) >= 5, V6 = (o.v || CB_V) >= 6;')
rep('const cap = quick || role === "turret" ? 1 :', 'const cap = quick || role === "turret" || (V6 && (s.k === "swhale" || s.k === "slevi" || s.k === "ssquid")) ? 1 :')
rep('const sim = { v: V5 ? 5 : V4 ? 4 : 3,', 'const sim = { v: V6 ? 6 : V5 ? 5 : V4 ? 4 : 3,')
s2 = re.sub(r"GAME_V = 513\b", "GAME_V = 514", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
