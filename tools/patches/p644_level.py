# v644: commander level counts buildings and research only (owner: "I level up super fast and don't even really build",
# "Even if players drop that's fine I just need this scaled and balanced"). Ranking score is unchanged (everything spent counts,
# OGame-style). Level points = resources that went into every building level (home and colonies) and research level, / 1000,
# on a curve about 2.6x steeper (26·(L-1)^2.5 instead of 10·(L-1)^2.5). Calibrated on the live players: the top commander
# goes from Lv.91 to about Lv.50, a mid player from 23 to about 15, new players start at Lv.1.
import sys, re
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)

rep('const myCmdLv = () => { try { return cmdLevel(score()); } catch (e) { return 1; } };',
    '''/* v644 level points: what your buildings (every world) and research are worth, in thousands of resources */
const LVP = { t: -1e9, v: 0 };
function lvPts() { const T = performance.now(); if (T - LVP.t < 1000) return LVP.v; let t = 0;
  try { const sb = b => { for (const k in b || {}) { if (!B[k]) continue; const n = Math.min(+b[k] || 0, 200); for (let l = 1; l <= n; l++) t += total(cost(B[k], l)); } };
    sb(S.b); for (const k in S.r || {}) { if (!R[k]) continue; const n = Math.min(+S.r[k] || 0, 200); for (let l = 1; l <= n; l++) t += total(cost(R[k], l)); }
    for (const p of myPlanets()) if (p.kind !== "home") sb(p.b); } catch (e) {}
  LVP.t = T; LVP.v = Math.floor(t / 1000); return LVP.v; }
const myCmdLv = () => { try { return cmdLevel(lvPts()); } catch (e) { return 1; } };''')
n0 = s.count('cmdLevel(score())')
s = s.replace('cmdLevel(score())', 'myCmdLv()')
print('replaced own-level calls:', n0)
rep('const sc = score(), L = cmdLevel(sc), mx = L >= CMD_MAX, a = lvlXP(L)', 'const sc = lvPts(), L = cmdLevel(sc), mx = L >= CMD_MAX, a = lvlXP(L)')
rep('const lvlXP = L => Math.round(10 * Math.pow(Math.max(0, L - 1), 2.5));', 'const lvlXP = L => Math.round(26 * Math.pow(Math.max(0, L - 1), 2.5)); /* v644 was 10·(L-1)^2.5 on total score */')
rep('const cmdLevel = s => { let L = Math.min(CMD_MAX, Math.floor(Math.pow(Math.max(0, s) / 10, .4)) + 1);', 'const cmdLevel = s => { let L = Math.min(CMD_MAX, Math.floor(Math.pow(Math.max(0, s) / 26, .4)) + 1);')
# other commanders: the level they publish (their own client works it out the same way); score only as a fallback
rep('return fl == null ? cmdLevel(P.score) >= FLAG_OLD : fl > 0 && (fl > 1 || cmdLevel(P.score) >= FLAG_LV);', 'return fl == null ? (P.lvl || cmdLevel(P.score)) >= FLAG_OLD : fl > 0 && (fl > 1 || (P.lvl || cmdLevel(P.score)) >= FLAG_LV);')
rep('w = (p.kind === "home" ? 3 : 1) + Math.floor(cmdLevel(pl.score || 0) / 10);', 'w = (p.kind === "home" ? 3 : 1) + Math.floor((pl.lvl || cmdLevel(pl.score || 0)) / 10);')
rep('lv = m.u === G.me ? myCmdLv() : pl && pl.score != null ? cmdLevel(pl.score) : 0;', 'lv = m.u === G.me ? myCmdLv() : pl && pl.score != null ? (pl.lvl || cmdLevel(pl.score)) : 0;')
# buddy picks compare levels too
s2 = re.sub(r'(function buddyPicks\(n = 3\) \{[^\n]*?)cmdLevel\(p\.score \|\| 0\)', lambda m: m.group(1) + '(p.lvl || cmdLevel(p.score || 0))', s, count=1)
if s2 == s: raise SystemExit('buddyPicks not patched')
s = s2
rep('Raise your Commander level by growing your score: buildings, research, fleets and victories all count.', 'Raise your Commander level by building and researching: every building level, on every world, and every research level counts. Fleets and battles raise your ranking score instead.')
# rewards that grew with total score (a crate was ~31M metal and a daily task ~20M for the top player: each one filled storage,
# fed the fleet, raised the score, and made the next reward bigger) now scale with production, like the shop's Pods
rep('const crateAmt = () => Math.round(15000 + score() * 40);', 'const crateAmt = () => { try { return Math.max(15000, Math.round(rates().m * 60 * 4)); } catch (e) { return 15000; } }; /* v644: 4 hours of metal production (was 15k + 40 per score point) */')
rep('const amt = Math.round((2500 + score() * 12) * (c.kind === "g" ? .5 : c.kind === "c" ? .75 : 1));', 'let amt = Math.round(2500 * (c.kind === "g" ? .5 : c.kind === "c" ? .75 : 1)); try { amt = Math.max(amt, Math.round(rates()[c.kind] * 60)); } catch (e) {} /* v644: an hour of that resource (was 2,500 + 12 per score point) */')
rep('const dailyReward = () => { const s = Math.max(1, score()); return { m: Math.round(600 + s * 25), c: Math.round(400 + s * 15), g: Math.round(150 + s * 6) ', 'const dailyReward = () => { let R = { m: 0, c: 0, g: 0 }; try { R = rates(); } catch (e) {} return { m: Math.max(600, Math.round(R.m * 90)), c: Math.max(400, Math.round(R.c * 90)), g: Math.max(150, Math.round(R.g * 90)) /* v644: 1.5 hours of production (was 600 + 25 per score point) */ ')
rep('const GAME_V = 642', 'const GAME_V = 644')
open(p, 'w', encoding='utf-8').write(s)
