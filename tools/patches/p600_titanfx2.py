# v600 the Titans' arsenal, second pass (see p600_titanfx2.js): the Neural Swarm v2 and the Sovereign Ark's three rotating main guns
# (Imperial Lance, Solar Broadside, Halo of Judgment) plus Gilded Flak
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('if (q.k === "sovereign" && main) { b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: "SL", charge: 0, life: .9, seed: hash(v.t + "|" + v.s) % 997 }); b.fx.push(Object.assign({}, hid, { t0: v.t, t1: v.t + .32 })); return true; } /* v595 */',
    'if (q.k === "sovereign" && main) { const sv = b.sv600 || (b.sv600 = {}), nS = sv[v.s] = (sv[v.s] || 0) + 1, W = [["SL", .9, .32], ["SB", 1.15, .7], ["SH", 1.5, 1.0]][(nS - 1) % 3]; /* v600 the Ark turns through its three main guns */\n    b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: W[0], charge: 0, life: W[1], seed: hash(v.t + "|" + v.s) % 997 }); b.fx.push(Object.assign({}, hid, { t0: v.t, t1: v.t + W[2] })); return true; }')
rep('if (q.k === "sovereign" && pd) { const n = lo ? 3 : 6; for (let j = 0; j < n; j++) { const t0 = v.t + j * .05; b.fx.push({ t0, t1: t0 + .28, v, last: j === n - 1, first: j === 0, n, mis: false, ic: false, side, off: (j / (n - 1) - .5) * 1.2, hv: 0, sz: 0, j: 500 + j, col: j % 2 ? "#7af4ff" : "#ffffff" }); } return true; }',
    'if (q.k === "sovereign" && pd) { b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: "SP", charge: 0, life: .55, seed: hash(v.t + "|" + v.s) % 997 }); b.fx.push(Object.assign({}, hid, { t0: v.t, t1: v.t + .2 })); return true; } /* v600 Gilded Flak */')
rep('ti: sw ? "HS" : "SW", charge: 0, life: sw ? 1.9 : 2.2,', 'ti: sw ? "HS" : "SW", charge: 0, life: sw ? 2.6 : 2.2,')
rep('b.fx.push({ t0: v.t, t1: v.t + (sw ? 1.05 : 1.1), v, last: true,', 'b.fx.push({ t0: v.t, t1: v.t + (sw ? 1.85 : 1.1), v, last: true,')
i = s.index('function titanBeamDraw('); s = s[:i] + open('tools/patches/p600_titanfx2.js', encoding='utf-8').read() + s[i:]
s2 = re.sub(r"GAME_V = 599\b", "GAME_V = 600", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
