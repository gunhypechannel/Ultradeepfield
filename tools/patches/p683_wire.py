# v683 bosses raise their shields again in a fight (sim v8 shield pulse + hex bubble); Aexion's dreadnought form: slow turns only to
# attack, attacks fired from the ship in step with its model, and its own special, the Sovereign Rail (see p683_aexd.js)
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__)); R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# the simulator, v8: a boss's shield comes back every 12 s, under fire too (before, it went in the first seconds and never returned)
rep('const CB_V = 7, CB_OK = v => v === 3 || v === 4 || v === 5 || v === 6 || v === 7,', 'const CB_V = 8, CB_OK = v => v === 3 || v === 4 || v === 5 || v === 6 || v === 7 || v === 8, /* v683 v8: bosses raise their shields again every 12 s */')
rep('V7 = (o.v || CB_V) >= 7,', 'V7 = (o.v || CB_V) >= 7, V8 = (o.v || CB_V) >= 8,')
rep('const sim = { v: V7 ? 7 :', 'const sim = { v: V8 ? 8 : V7 ? 7 :')
rep('for (const s of sq) if (s.n > 0 && t - s.lastHit > 2) s.shp = Math.min(s.n * s.shPer, s.shp + s.n * s.shPer * .06 * dt);',
    'for (const s of sq) if (s.n > 0 && t - s.lastHit > 2) s.shp = Math.min(s.n * s.shPer, s.shp + s.n * s.shPer * .06 * dt);\n    if (V8) for (const s of sq) { if (s.bsp == null) s.bsp = typeof s.k === "string" && /^wb[A-Z]/.test(s.k) && AL[s.k] ? 10 : 0; if (s.bsp && s.n > 0 && t >= s.bsp) { s.shp = Math.max(s.shp, s.n * s.shPer * .6); s.bsp += 12; } } /* v683 a boss raises its shield again every 12 s, under fire too */')
# Aexion's dreadnought form
rep('const A = b.aexA || (b.aexA = []), last = A[A.length - 1]; if (last && v.t - last.t0 < AEX_DUR[last.a] + .7) return;', 'if (aexdOn(b)) return aexdQueue(b, v); /* v683 */ const A = b.aexA || (b.aexA = []), last = A[A.length - 1]; if (last && v.t - last.t0 < AEX_DUR[last.a] + .7) return;')
rep('try { aexDraw(ctx, b, scr, T, W, H, d, lo, t); } catch (e) {} /* v680 */', 'try { aexDraw(ctx, b, scr, T, W, H, d, lo, t); } catch (e) {} /* v680 */ try { aexdDraw(ctx, b, scr, T, W, H, d, lo, t); } catch (e) {} try { bShDraw(ctx, b, W, H, d, T, t); } catch (e) {} /* v683 */')
rep('function wbFend(key, b, t) { const F = WBF,', 'function wbFend(key, b, t) { if (key === "aex" && aexdOn(battle)) { if (!b.live) WBR.face = 0; WBR.cy = null; return; } /* v683 the dreadnought turns only to attack (aexdDraw) */ const F = WBF,')
rep('(b.r.sbk && WB_STRIKE[b.r.sbk] ? b.r.sbk : null)', '(b.r.sbk && WB_STRIKE[b.r.sbk] && !aexdOn(b) ? b.r.sbk : null)')
rep('  for (const m of b.aexA || []) { const u = (T - m.t0) / AEX_DUR[m.a]; if (u > -.4 && u < .4) {', '  { const c = b.aexD && b.aexD.c; if (c && t > c.fireAt - 900 && t < c.fireAt + 600) { b.focus = { s: 1, x: .5, y: .5, until: c.fireAt + c.ms + 300, cine: "boss" }; C.n++; return; } } /* v683 */\n  for (const m of b.aexA || []) { const u = (T - m.t0) / AEX_DUR[m.a]; if (u > -.4 && u < .4) {')
rep('function spawnVolley(b, v) { fx589Spawn(b, v);', R('p683_aexd.js') + 'function spawnVolley(b, v) { fx589Spawn(b, v);')
rep('const GAME_V = 682;', 'const GAME_V = 683;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
