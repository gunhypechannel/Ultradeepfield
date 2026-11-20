# v679 the v678 letterbox bars were drawn at the edges of the ships' field (mg.top/mg.bot), not the edges of what is seen: on a Fold
# the picture runs far past the field behind the panels, so the bars cut across the middle of the battle (owner's screenshot). The HUD
# panels already frame the view, so the bars go; the grain stays.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
rep('ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = "#000"; ctx.globalAlpha = .9; ctx.fillRect(0, top - 2, W, h + 2); ctx.fillRect(0, bot - h, W, h + 2);', 'ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); /* v679 no letterbox bars */')
rep('const GAME_V = 678;', 'const GAME_V = 679;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
