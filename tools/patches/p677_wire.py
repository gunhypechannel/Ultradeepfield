# v677 Mimics: no legs (tentacles hang where the legs were), and cinematic attacks (see p677_mimfx.js)
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
R = lambda f: open('tools/patches/' + f, encoding='utf-8').read()
OLD = lambda f: open('tools/patches/' + f, encoding='utf-8').read()
old676 = OLD('p676_mimatk.js')
def cut(src, start, end_marker):
    a = src.find(start); b = src.find(end_marker, a) + len(end_marker); return src[a:b]
# the v676 attack code is replaced whole by the v677 set
for st, en in [('const MIM_ATK = {', '\n'), ('const MIM_DUR = {', '\n'), ('function mimAtkAdd(b, v) {', 'if (L.length > 24) L.shift(); }'), ('function mimLunge(b, scr, T) {', 'done.add(S0); } }')]:
    rep(cut(old676, st, en), '')
rep(cut(old676, 'function mimAtkDraw(ctx, b, scr, T, W, d, lo) {', 'ctx.restore(); ctx.globalAlpha = 1; }'), R('p677_mimfx.js'))
rep('try { mimAtkDraw(ctx, b, scr, T, W, d, lo); } catch (e) {} /* v676 */', 'try { mimAtkDraw(ctx, b, scr, T, W, d, lo, t, H); } catch (e) {} /* v676, v677 */')
# no legs: tentacles hang where the legs were, and they sway instead of walking
rep(open('tools/patches/p677_oldlegs.txt', encoding='utf-8').read(), 'if (D.legs) { const nT = 8 + D.legs * 2; for (let i = 0; i < nT; i++) { const x = (1.3 - (i / (nT - 1)) * 2.9) * L, z = (i % 2 ? 1 : -1) * (.25 + r() * .55), Lt = (1.7 + r() * 1.1) * (D.alpha ? 1.25 : 1); tube([V(x, -.15, z * .6), V(x - .1, -.15 - Lt * .35, z), V(x - .35 - r() * .3, -.15 - Lt * .7, z * 1.3 + (r() - .5) * .3), V(x - .8 - r() * .4, -.15 - Lt * .95, z * 1.5 + (r() - .5) * .5)], .13 * (D.armour ? 1.3 : 1), .02, i % 4 === 1 ? C.cableL : C.cable, 0, 1.3); } } /* v677 owner: no legs, tentacles hang where they were */')
rep(open('tools/patches/p677_oldwave.txt', encoding='utf-8').read(), 'else w += ` float lw = clamp((-.1 - p.y) / 1.35, 0., 1.), d2 = clamp((-.1 - p.y) / 2.4, 0., 1.);\n    transformed.x += d2 * d2 * .55 * sin(mt * ${W1} + p.z * 2.3 + p.x * 1.1); transformed.z += d2 * d2 * .4 * cos(mt * ${W1} + p.x * 1.7 + p.z); transformed.y += d2 * .12 * sin(mt * ${W2} + p.x * 2.);\n    float bw = 1. - lw; transformed.y += .1 * sin(mt * ${W1}); transformed.z += bw * .04 * sin(mt * ${W1} + p.x * .7);`; /* v677 a float, the tentacles swaying (was a trot) */')
rep('const GAME_V = 676;', 'const GAME_V = 677;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
