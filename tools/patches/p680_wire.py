# v680 Aexion's move set in battle replays (see p680_aex.js)
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
R = lambda f: open('tools/patches/' + f, encoding='utf-8').read()
rep('function spawnVolley(b, v) { fx589Spawn(b, v); /* v589 */ try { if (MIM_ATK[(b.Q[v.s] || {}).k]) mimAtkAdd(b, v); } catch (e) {} /* v676 */',
    R('p680_aex.js') + 'function spawnVolley(b, v) { fx589Spawn(b, v); /* v589 */ try { if (MIM_ATK[(b.Q[v.s] || {}).k]) mimAtkAdd(b, v); } catch (e) {} /* v676 */ try { if (b.r && b.r.sbk === "aex") aexAtkAdd(b, v); } catch (e) {} /* v680 */')
rep('try { mimAtkDraw(ctx, b, scr, T, W, d, lo, t, H); } catch (e) {} /* v676, v677 */', 'try { mimAtkDraw(ctx, b, scr, T, W, d, lo, t, H); } catch (e) {} /* v676, v677 */ try { aexDraw(ctx, b, scr, T, W, H, d, lo, t); } catch (e) {} /* v680 */')
# the director frames his moves: wide for the sweep and the fracture, between him and his target for the lance
rep('  for (const m of b.mAtk || []) { const u = (T - m.t0) / MIM_DUR[m.a]; if (u > -.4', '''  for (const m of b.aexA || []) { const u = (T - m.t0) / AEX_DUR[m.a]; if (u > -.4 && u < .4) { if (m.a === "lance") { if (shot(mid(m.e, m.e) && b.scC ? [(b.scC.x + at(m.e)[0]) / 2, (b.scC.y + at(m.e)[1]) / 2] : null, 1.3, 2600, "aex")) return; } else { b.focus = { s: 1, x: .5, y: .5, until: t + (m.a === "frac" ? 4200 : 2800), cine: "aex" }; C.n++; return; } } } /* v680 */
  for (const m of b.mAtk || []) { const u = (T - m.t0) / MIM_DUR[m.a]; if (u > -.4''')
rep('const GAME_V = 679;', 'const GAME_V = 680;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
