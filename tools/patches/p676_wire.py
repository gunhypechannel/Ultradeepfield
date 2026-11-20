# v676 the Mimics animate in battle (their baked motion frames) and each kind has its own attack (see p676_mimatk.js)
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
R = lambda f: open('tools/patches/' + f, encoding='utf-8').read()
rep('function spawnVolley(b, v) { fx589Spawn(b, v); /* v589 */', R('p676_mimatk.js') + 'function spawnVolley(b, v) { fx589Spawn(b, v); /* v589 */ try { if (MIM_ATK[(b.Q[v.s] || {}).k]) mimAtkAdd(b, v); } catch (e) {} /* v676 */')
rep('const mf = MON[q.k] && !dying ? monBatFrame(b, i, q.k, real, moving) : null;', 'const mf = (MON[q.k] || (MIM_D[q.k] && MON_WAVE[q.k] && mimAnimOK(b, q.k))) && !dying ? monBatFrame(b, i, q.k, real, moving) : null; /* v676 the Mimics move too */')
rep('Q.forEach((q, i) => { if (tot[i] === -1 && rep[i] != null) scr[i] = scr[rep[i]]; }); b.repOf = rep; /* v673 */ }', 'Q.forEach((q, i) => { if (tot[i] === -1 && rep[i] != null) scr[i] = scr[rep[i]]; }); b.repOf = rep; /* v673 */ } try { mimLunge(b, scr, T); } catch (e) {} /* v676 */')
rep('try { wbStrike(ctx, b, scr, Q, W, H, t, d, lo); } catch (e) {}', 'try { wbStrike(ctx, b, scr, Q, W, H, t, d, lo); } catch (e) {} try { mimAtkDraw(ctx, b, scr, T, W, d, lo); } catch (e) {} /* v676 */')
rep('const GAME_V = 675;', 'const GAME_V = 676;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
