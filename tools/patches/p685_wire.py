# v685 part 1: the memory leak behind the iPhone crashes (see p685_mem.js)
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__)); R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('let G3 = null, G3fail = !TH;', R('p685_mem.js') + 'let G3 = null, G3fail = !TH;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
# v685 part 2: every boss move crosses the screen: the Super Cube's tractor beam, burst and wave, and the world bosses' bite, coil, charge
# and summon, which still played only inside the boss's picture box
s = open(p, encoding='utf-8').read()
rep('function wbStrike(ctx, b, scr, Q, W, H, t, d, lo) { const k = b.r && (b.r.wb || (b.r.sbk && WB_STRIKE[b.r.sbk] && !aexdOn(b) ? b.r.sbk : null)) /* v681 super bosses too */, M = WBR.mv;',
    'const wbCol = k => (WB[k] || (typeof SBW !== "undefined" && SBW[k]) || { col: "#5dff7a" }).col; /* v685 */\nfunction wbStrike(ctx, b, scr, Q, W, H, t, d, lo) { const k = b.r && (b.r.wb || (b.r.sbk && WB_STRIKE[b.r.sbk] && !aexdOn(b) ? b.r.sbk : null) || (!b.r.omega && b.superSide != null && !b.r.sbk ? "scb" : null)) /* v681 super bosses, v685 the Super Cube */, M = WBR.mv;')
rep('PB = !!WB[k] /* v493', 'PB = !!(WB[k] || k === "scb") /* v685 the Super Cube too; v493')
rep('glowSprite(PB && k !== "wym" ? WB[k].col : "rgba(255,170,60,1)")', 'glowSprite(PB && k !== "wym" ? wbCol(k) : "rgba(255,170,60,1)")')
rep(': [(WB[k] || SBW[k]).col], col = j => els[j % els.length];', ': [wbCol(k)], col = j => els[j % els.length];')
rep('  epx: { converge: ["beam", .5, .95, 0, 3400], storm: ["bolts", .2, .9, 12, 3000], cataclysm: ["wave", .45, .95, 0, 3200] } };',
    '''  epx: { converge: ["beam", .5, .95, 0, 3400], storm: ["bolts", .2, .9, 12, 3000], cataclysm: ["wave", .45, .95, 0, 3200] },
  scb: { tractor: ["beam", .3, .85, 0, 3000], burst: ["bolts", .3, .85, 8, 2600], wave: ["wave", .35, .9, 0, 2600] } }; /* v685 the Super Cube */
Object.assign(WB_STRIKE.ovl, { summon: ["bolts", .4, .9, 6, 3000] }); Object.assign(WB_STRIKE.war, { summon: ["bolts", .4, .9, 6, 3000] }); Object.assign(WB_STRIKE.c0, { charge: ["beam", .3, .85, 0, 2600] });
Object.assign(WB_STRIKE.dev, { bite: ["bolts", .35, .7, 3, 2000] }); Object.assign(WB_STRIKE.krk, { bite: ["bolts", .35, .7, 3, 2000] }); Object.assign(WB_STRIKE.wym, { coil: ["wave", .35, .85, 0, 2600] }); Object.assign(WB_STRIKE.lev, { coil: ["wave", .35, .85, 0, 2600] }); /* v685 the moves that stayed in the box */''')
open(p, 'w', encoding='utf-8').write(s); print('ok2')
# v685 part 3: the Super Cube rose out of reach. It rises to meet each fleet so one attack takes a set share of it, but that share was
# counted in units, and its units are mostly cheap drones: it grew until only drones died (owner's alliance assault 2026-11-20: Cube
# attack 19.4M and hull 259M, 540x the 2026-11-08 Cube they beat; 41 of 68 units lost, every one a drone). Now the share is counted
# in hull, so the Cube itself and its spheres take the hits, and the week's wear on the Warden is counted the same way.
s = open(p, encoding='utf-8').read()
rep('const cubeKilled = res => { const s0 = Object.values(res.start.d || {}).reduce((a, v) => a + v, 0), s1 = Object.values(res.dLeft || {}).reduce((a, v) => a + Math.max(0, v), 0); return s0 ? 1 - s1 / s0 : 1; };',
    'const cubeHW = o => Object.entries(o || {}).reduce((a, [k, n]) => a + Math.max(0, +n || 0) * ((AL[k] && AL[k].hull) || (SH[k] && SH[k].hull) || 1), 0); /* v685 hull, not head count */\nconst cubeKilled = res => { const s0 = cubeHW(res.start.d), s1 = cubeHW(res.dLeft); return s0 ? 1 - s1 / s0 : 1; };')
rep('function wardenWear(cur, res) { const s0 = sumN(res.start.d || {}), s1 = sumN(cleanShips(res.dLeft || {})) + sumN(Object.fromEntries(Object.entries(res.dLeft || {}).filter(([k]) => !SH[k]))); if (!s0) return;',
    'function wardenWear(cur, res) { const s0 = cubeHW(res.start.d), s1 = cubeHW(res.dLeft); if (!s0) return; /* v685 by hull */')
open(p, 'w', encoding='utf-8').write(s); print('ok3')
# v685 part 4: reactive boss shields (see p685_shield.js), and the Mimic bosses raise their shields too (simulator v9)
s = open(p, encoding='utf-8').read()
rep('if (v.bounce || v.sh > 0) { b.shHit[v.e] = T;', 'if (v.bounce || v.sh > 0) { b.shHit[v.e] = T; if (b.superSide != null && b.Q[v.e] && b.Q[v.e].side === b.superSide) try { bShHit(b, ex, ey, t, v.sh); } catch (er) {} /* v685 */')
rep('try { bShDraw(ctx, b, W, H, d, T, t); } catch (e) {} /* v683 */', 'try { bShDraw(ctx, b, W, H, d, T, t); } catch (e) {} /* v683 */ try { bShHits(ctx, b, W, H, d, t); } catch (e) {} /* v685 */')
rep('function spawnVolley(b, v) { fx589Spawn(b, v);', R('p685_shield.js') + 'function spawnVolley(b, v) { fx589Spawn(b, v);')
rep('const CB_V = 8, CB_OK = v => v === 3 || v === 4 || v === 5 || v === 6 || v === 7 || v === 8,', 'const CB_V = 9, CB_OK = v => v === 3 || v === 4 || v === 5 || v === 6 || v === 7 || v === 8 || v === 9, /* v685 v9: the Mimic bosses raise their shields too */')
rep('V8 = (o.v || CB_V) >= 8,', 'V8 = (o.v || CB_V) >= 8, V9 = (o.v || CB_V) >= 9,')
rep('const sim = { v: V8 ? 8 :', 'const sim = { v: V9 ? 9 : V8 ? 8 :')
rep('s.bsp = typeof s.k === "string" && /^wb[A-Z]/.test(s.k) && AL[s.k] ? 10 : 0;', 's.bsp = typeof s.k === "string" && (/^wb[A-Z]/.test(s.k) || (V9 && /^(malpha\\d*|momega\\w*|mnexus|mimic)$/.test(s.k))) && AL[s.k] ? 10 : 0;')
rep('const GAME_V = 684;', 'const GAME_V = 685;')
open(p, 'w', encoding='utf-8').write(s); print('ok4')
