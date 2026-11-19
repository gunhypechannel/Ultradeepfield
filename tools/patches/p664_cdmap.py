# v664 a fleet carrying a Cube Destroyer is drawn on the map as the Cube Destroyer and its flagship escort (the faction flagship and any
# titans), not the whole formation. Owner: "when a player sends a cube destroyer on an attack instead of the fleet sailing it just shows
# the flag ships and the cube destroyer". A picture only: the fleet's ships and numbers are untouched.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
rep('grp = fleet3D(W, hostile && !f.n ? null : f.n, col', 'grp = fleet3D(W, hostile && !f.n ? null : cdEscort(f.n), col')
rep('const fleetFlagU = (f, hostile) =>', '''const cdEscort = n => { if (!n || !(n.worldbreaker > 0)) return n; const o = { worldbreaker: n.worldbreaker }; for (const k in n) if (n[k] > 0 && MINI_CLS[k] === "x") o[k] = n[k]; return o; }; /* v664 */
const fleetFlagU = (f, hostile) =>''')
rep('const cap = { s: 4, m: 3, l: 2, x: 1 }[MINI_CLS[k]]', 'const cap = { s: 4, m: 3, l: 2, x: 1, q: 1 }[MINI_CLS[k]]') # the Cube Destroyer (class q) had no slot cap, so it was never drawn in a formation
rep('const GAME_V = 663;', 'const GAME_V = 664;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
