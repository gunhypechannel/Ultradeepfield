# v672 the stress-test list drew each row's name from WB[key]; the 8 Mimic cases (v671) are not world bosses, so their rows threw.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
rep('const rows = out.map((r, i) => { const D = r.c.t === "sb" ?', 'const rows = out.map((r, i) => { const D = r.c.t === "mim" ? { ic: "⬢", n: (AL[r.c.key] || {}).n || r.c.key } : r.c.t === "sb" ?')
rep('One fleet of ${fmt(tot)} ships (${fmt(STRESS_FLEET.worldbreaker)} Cube Destroyers among them) against every super boss in every form.', 'One fleet of ${fmt(tot)} ships (${fmt(STRESS_FLEET.worldbreaker)} Cube Destroyers among them) against every super boss in every form, and the Mimic Alphas, Nexus and Omega.')
rep('const GAME_V = 671;', 'const GAME_V = 672;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
