# v658 (owner: "When premium hull attacks cubes it should change the color of the ships battle animation, they still show standard").
# The map battle (clashes: Cubes, bosses, monsters, planets) built its ship models without the hull finish: FLEET_FIN is set only for
# fleets in flight. Now your side of a clash wears your finish (the finish of the ship type you sent most of), and other sides are
# left standard; FLEET_FIN is restored afterwards so it can't leak into other models.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
rep('''      const mk = (n, col, hostile, fg) => { const g = fleet3D(W, clashShips(n) || genComp(clashCnt(n)), col, hostile, false, false, fg);''',
    '''      const mk = (n, col, hostile, fg, sd) => { const ff0 = FLEET_FIN, sn = clashShips(n); FLEET_FIN = sd === c.you && !c.demo ? (() => { try { return hullFleet(G.me, sn || n); } catch (e) { return null; } })() : null; /* v658 your side wears your finish */
        let g; try { g = fleet3D(W, sn || genComp(clashCnt(n)), col, hostile, false, false, fg); } finally { FLEET_FIN = ff0; }''')
rep('''c.o = { ga: mk(c.a, c.aCol, c.you !== "a", c.aF || (c.aCmd === false ? null : DEMO_FAC[hash(String(c.key) + "a") % 4])), gd: mk(c.d, c.dCol, c.you === "a", c.dF || (c.dCmd === false ? null : DEMO_FAC[hash(String(c.key) + "d") % 4])),''',
    '''c.o = { ga: mk(c.a, c.aCol, c.you !== "a", c.aF || (c.aCmd === false ? null : DEMO_FAC[hash(String(c.key) + "a") % 4]), "a"), gd: mk(c.d, c.dCol, c.you === "a", c.dF || (c.dCmd === false ? null : DEMO_FAC[hash(String(c.key) + "d") % 4]), "d"),''')
rep('const GAME_V = 657', 'const GAME_V = 658')
open(p, 'w', encoding='utf-8').write(s)
