# v527 the battle replay back to its earlier style (owner: "restore the battle simulation to the previous style"): undoes v523's battle
# changes and v524's defence rank. Hull sizes back to length^1.15 with the Cube Destroyer at its old size, monsters at their old
# battle size, no rank formation and no reserved flagship room (the squadrons are placed by the battle again), and the Solar Moth's
# battle picture back to its v522 tilt. The Star Leviathan's look (v522, v524), the shop, the Bestiary and everything else stay.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const bLen = k => k === "worldbreaker" ? 2 * (SIDE_LEN.dreadnought || 1.25) * 1.08 * 1.5 : Math.pow(SIDE_LEN[k] || .5, 1.3) * (BOSSK[k] || 1); /* v523 a steeper class ladder; the Cube Destroyer x1.5 */\n',
    'const bLen = k => k === "worldbreaker" ? 2 * (SIDE_LEN.dreadnought || 1.25) * 1.08 : Math.pow(SIDE_LEN[k] || .5, 1.15) * (BOSSK[k] || 1);\n')
i = s.index('for (const k in MON) BOSSK[k] = (BOSSK[k] || 1) * 1.35;'); j = s.index('\n', i) + 1; s = s[:i] + s[j:]
i = s.index('    if (!b.superSide && b.fdir !== "x") { const fm'); j = s.index('/* v523 */', i) + len('/* v523 */'); j = s.index('\n', j) + 1; s = s[:i] + s[j:]
i = s.index('    if (b.flags && !b.superSide) { const Lf'); j = s.index('\n', i) + 1; s = s[:i] + s[j:]
s = s.replace('for (const p of P) { if (p.fixed) continue; ', 'for (const p of P) { ')
rep('if (k === "smoth" && view === "side") { ship.rotation.order = "ZYX"; ship.rotation.set(Math.PI / 2, 0, Math.PI / 2); } /* v523 its back: head up, wings spread */', 'if (k === "smoth" && view === "side") ship.rotation.x = 1.15; /* v522 the Solar Moth shows its wings in battle, not their edge */')
rep('smoth: 2.4, cram: 1.8 },', 'smoth: 1.6, cram: 1.8 },')
assert 'p.fixed' not in s and 'v523 the lineup' not in s
s2 = re.sub(r"GAME_V = 526\b", "GAME_V = 527", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
