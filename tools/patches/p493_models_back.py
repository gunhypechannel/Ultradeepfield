# v493: owner: "No bosses get painted models". Every boss is its code-built 3D model again, in battle reports too (Khezaroth and
# Medusara included); the painting code stays dormant (BOSS3D.paint is never set, no skins are preloaded). Kept from v492: the
# head-on battle cameras and the strikes that cross the whole screen, now for every world boss's own model: each beam rakes
# across the fleet and runs to the screen edge, burning every ship it crosses, timed by each model's own move (WB_STRIKE).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('BOSS3D.paint = 1; const m3', 'BOSS3D.paint = 0; const m3')
rep('init(T) { TH = T; if (!ARL.medusara) setTimeout(() => { try { artLoad("khezaroth", () => {}); artLoad("medusara", () => {}); } catch (e) {} }, 0); }', 'init(T) { TH = T; }')
rep('PB = !!(WBR.b && WBR.b.art && WBR.b.art.ok)', 'PB = !!WB[k] /* v493 every world boss\'s strikes cross the screen */')
s = re.sub(r"GAME_V = 492\b", "GAME_V = 493", s)
open(P, 'w', encoding='utf-8').write(s); print('ok')
