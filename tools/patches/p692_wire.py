# v692: the Omega Cube turns slower and less often in the battle replay (owner: "slow the omega cube down while it turns and also
# make it turn less frequently"). It used the shared boss fencing cycle: a 0.65 s turn to a side and a 0.65 s turn back to the front
# every ~6 s (a turn every ~3 s). Now a turn takes 2.6 s (smootherstep: a heavy start, a soft stop), it keeps the new facing instead
# of swinging back, and it holds longer between turns (one turn every ~13-16 s). Its attacks are unchanged.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const WBF = { turn: 650, hold: 900, atk: 2600, rest: 1000 };', 'const WBF = { turn: 650, hold: 900, atk: 2600, rest: 1000 }, WBF_OMG = { turn: 2600, hold: 1400, atk: 2600, rest: 6000 }; /* v692 the Omega Cube: slow, heavy turns, and it keeps its facing */')
rep('/* v683 the dreadnought turns only to attack (aexdDraw) */ const F = WBF, C = WBR.cy,', '/* v683 the dreadnought turns only to attack (aexdDraw) */ const OM = key === "omg", F = OM ? WBF_OMG : WBF, C = WBR.cy,')
rep('WBR.cy = { t0: t, dir, fired: 0, end: t + T5 + F.rest * (.8 + Math.random() * .5) }; }', 'WBR.cy = { t0: t, dir, from: OM && C ? C.dir : 0, tn: OM && C && Math.abs(dir - C.dir) > 1 ? F.turn * 1.4 : F.turn, fired: 0, end: t + (OM ? T4 : T5) + F.rest * (.8 + Math.random() * .5) }; }')
rep('const c = WBR.cy, e = t - c.t0, sm = u => u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u);', 'const c = WBR.cy, e = t - c.t0, sm = u => u <= 0 ? 0 : u >= 1 ? 1 : OM ? u * u * u * (u * (u * 6 - 15) + 10) : u * u * (3 - 2 * u);')
rep('WBR.face = c.dir * (e < F.turn ? sm(e / F.turn) : e < T4 ? 1 : 1 - sm((e - T4) / F.turn)); }', 'WBR.face = OM ? c.from + (c.dir - c.from) * sm(e / c.tn) : c.dir * (e < F.turn ? sm(e / F.turn) : e < T4 ? 1 : 1 - sm((e - T4) / F.turn)); }')
rep('const GAME_V = 691;', 'const GAME_V = 692;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
