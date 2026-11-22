# v721 (owner: "Can we give all monsters more unique attack animations"): every space monster gets its own signature attack on the
# battle screen (p721_beast.js), drawn over the existing shots, with its body moving and the hit landing.
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__))
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
rep("function spawnVolley(b, v) { fx589Spawn(b, v); /* v589 */", R('p721_beast.js') + "\nfunction spawnVolley(b, v) { fx589Spawn(b, v); /* v589 */ try { if (BEAST_ATK[(b.Q[v.s] || {}).k]) beastAtkAdd(b, v); } catch (e) {} /* v721 */")
rep("try { mimLunge(b, scr, T); } catch (e) {} /* v676 */", "try { mimLunge(b, scr, T); } catch (e) {} /* v676 */ try { beastLunge(b, scr, T); } catch (e) {} /* v721 */")
rep("try { mimAtkDraw(ctx, b, scr, T, W, d, lo, t, H); } catch (e) {} /* v676, v677 */", "try { mimAtkDraw(ctx, b, scr, T, W, d, lo, t, H); } catch (e) {} /* v676, v677 */ try { beastAtkDraw(ctx, b, scr, T, W, d, lo, t); } catch (e) {} /* v721 */")
rep('const GAME_V = 720;', 'const GAME_V = 721;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
