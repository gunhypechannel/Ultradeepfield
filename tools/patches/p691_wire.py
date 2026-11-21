# v691: Aexion's Warform remastered in the battle replay: slower, rarer turns and attacks timed to the model (see p691_aexw.js)
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__)); R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('function wbFend(key, b, t) { if (key === "aex" && aexdOn(battle)) {', 'function wbFend(key, b, t) { if (key === "aex" && (aexdOn(battle) || aexwOn(battle))) { /* v691 the Warform turns with its attacks too (aexwDraw) */')
rep('if (aexdOn(b)) return aexdQueue(b, v); /* v683 */', 'if (aexdOn(b)) return aexdQueue(b, v); /* v683 */ if (aexwOn(b)) return aexwQueue(b, v); /* v691 */')
rep('for (const m of b.aexA || []) { const D = AEX_DUR[m.a], u = (T - m.t0) / D;', 'for (const m of b.aexA || []) { const D = AEX_DUR[m.a], u = m.rt != null ? aexwU(m, t) : (T - m.t0) / D; /* v691 Warform beats run on the model\'s clock */')
rep('try { aexDraw(ctx, b, scr, T, W, H, d, lo, t); } catch (e) {}', 'try { aexwDraw(ctx, b, scr, T, W, H, d, lo, t); } catch (e) {} try { aexDraw(ctx, b, scr, T, W, H, d, lo, t); } catch (e) {}')
rep('const aexdOn = b => !!(b && b.r && b.r.sbk === "aex" && !b.r.sbForm);', 'const aexdOn = b => !!(b && b.r && b.r.sbk === "aex" && !b.r.sbForm);\n' + R('p691_aexw.js').rstrip('\n'))
rep('const GAME_V = 690;', 'const GAME_V = 691;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
