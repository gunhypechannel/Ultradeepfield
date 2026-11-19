# v659 battle scale (owner: "Why are the cubes so small? Why are the ships so small? Every battle simulation should try to use up
# empty space and still fit all ships on screen and should only be scaled against enemy ... the cube destroyer moves back and forth
# unnaturally"). The fit scale was one number for the whole field and ignored the v645 x0.55 shrink against Cubes and world bosses, so
# it planned for bigger ships than it drew and a big fight sat at its 0.4 floor with half the screen empty. Now each side is fitted to
# its own half; both sides share the smaller fit, so sizes stay true against each other, and a boss side (Cubes, Spheres, world and
# super bosses, monsters) may be drawn up to 2.2x larger than that, so the boss is big against the fleet instead of the fleet shrunk.
# The fit aims at half the field (was 42%) and can zoom to 2.4x for a small fight. The Cube Destroyer holds a steady post at the rear:
# it eased toward its side's average position every frame, which slid it back and forth as the fleet moved; now it drifts slowly.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
# the boss side is sized by the fit now, not by shrinking the fleet
rep('return (C[q.side] = foes.some(x => bBig(x.k)) ? .55 : foes.some(', 'return (C[q.side] = foes.some(x => bBig(x.k)) ? 1 /* v659: the boss side is drawn bigger instead */ : foes.some(')
rep('  const crowd = b.fit || clamp(Math.sqrt(22 / Math.max(22, alive)), .46, .92),', '  const crowd = clamp(Math.sqrt(22 / Math.max(22, alive)), .46, .92), fitOf = sd => (b.fitS && b.fitS[sd]) || b.fit || crowd,')
rep(', s: crowd * (.66 + .54 * b.z[i]) }));', ', s: fitOf(Q[i].side) * (.66 + .54 * b.z[i]) }));')
rep('L = Math.max(8 * d, clamp(W * .1 * bLen(q.k), 11 * d, W * (BOSSK[q.k] || q.k === "worldbreaker" ? .55 : .3)) * zs);\n    const fk = FOOTK(q.k);',
    'L = Math.max(8 * d, clamp(W * .1 * bLen(q.k), 11 * d, W * (BOSSK[q.k] || q.k === "worldbreaker" ? .55 : .3)) * zs * bVsK(b, q));\n    const fk = FOOTK(q.k);')
rep('''    const fitT = A0 ? clamp(crowd * Math.sqrt((W * .88 * (bot - top)) * (busy ? .44 : .42) / A0), .4, 1.85) : crowd;
    b.fit = b.fit ? b.fit + (fitT - b.fit) * Math.min(1, real / 700) : fitT;''',
    '''    const fitT = A0 ? clamp(crowd * Math.sqrt((W * .88 * (bot - top)) * (busy ? .44 : .42) / A0), .4, 1.85) : crowd;
    b.fit = b.fit ? b.fit + (fitT - b.fit) * Math.min(1, real / 700) : fitT;
    { /* v659 each side fitted to its own half; both share the smaller, a boss side may be up to 2.2x bigger */ const Ar = { a: 0, d: 0 }; for (const i of reps) { const [rx, ry] = fpOf(i); Ar[Q[i].side] += rx * ry * 4; }
      const half = W * .88 * (bot - top) * .5 * (busy ? .52 : .5), fs = sd => Ar[sd] ? clamp(fitOf(sd) * Math.sqrt(half / Ar[sd]), .35, 2.4) : null, ta = fs("a"), td = fs("d"), com = Math.min(ta || td || crowd, td || ta || crowd);
      const boss = sd => reps.some(i => Q[i].side === sd && (BOSSK[Q[i].k] || bBig(Q[i].k) || Q[i].k === "sphere" || Q[i].k === "cdrone")), tgt = { a: boss("a") ? Math.min(ta || com, com * 2.2) : com, d: boss("d") ? Math.min(td || com, com * 2.2) : com };
      const F0 = b.fitS || (b.fitS = { a: tgt.a, d: tgt.d }), ek = Math.min(1, real / 700); F0.a += (tgt.a - F0.a) * ek; F0.d += (tgt.d - F0.d) * ek; }''')
# the drawn size matches: the per-side fit already carries the boss boost
rep('''      if (vert) { const down = ne ? my >= ey : q.side === "a"; p.y = down ? y1 - p.ry * 1.05 : y0 + p.ry * .6; p.x = clamp(ox, x0 + p.rx * .8, x1 - p.rx * .8); }
      else { const left = ne ? ox <= ex : q.side === "a"; p.x = left ? x0 + p.rx * .8 : x1 - p.rx * .8; } p.w = .12; }''',
    '''      const cd = b.cdA || (b.cdA = {}), ca = cd[p.i] || (cd[p.i] = { x: ox, y: my }), ck = Math.min(1, real / 9000); ca.x += (ox - ca.x) * ck; ca.y += (my - ca.y) * ck; /* v659 a steady post: drifts, never slides */
      if (vert) { const down = ne ? my >= ey : q.side === "a"; p.y = down ? y1 - p.ry * 1.05 : y0 + p.ry * .6; p.x = clamp(ca.x, x0 + p.rx * .8, x1 - p.rx * .8); }
      else { const left = ne ? ox <= ex : q.side === "a"; p.x = left ? x0 + p.rx * .8 : x1 - p.rx * .8; p.y = clamp(ca.y, y0 + p.ry * .6, y1 - p.ry * 1.05); } p.w = .03; }''')
rep('const GAME_V = 658', 'const GAME_V = 659')
open(p, 'w', encoding='utf-8').write(s)
