# v531 the Cube Destroyer and the Discovery Class in the battle simulation (owner, later: "discovery class should be bigger than the reaper": its
# battle length 2.6, was 1.9 against the Reaper's 1.72).
# The Cube Destroyer (owner: "I want the cube destroyer to be our biggest ship in the battle field, make
# the best placement always near the rear"). Art only, the simulation is untouched:
#  - it is drawn longer than anything else on the field, the monsters included (bLen 4.3, was 3.46; the biggest monster is 4.09),
#    and always at the front depth (z .98), so it never shrinks into the background;
#  - it holds the rear of its own side: its formation sits near the screen edge behind its fleet (the side away from the enemy), and the
#    other ships make room around it instead of pushing it forward.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const bLen = k => k === "worldbreaker" ? 2 * (SIDE_LEN.dreadnought || 1.25) * 1.08 :', 'const bLen = k => k === "worldbreaker" ? 4.3 /* v531 the biggest thing on the field */ : k === "eclipse" ? 2.6 /* v531 the Discovery Class well above the Reaper (1.72) */ :')
rep('''  if (!b.z) b.z = Q.map((q, i) => q.role === "station" || q.role === "turret" ? .78 :''', '''  if (!b.z) b.z = Q.map((q, i) => q.k === "worldbreaker" ? .98 : q.role === "station" || q.role === "turret" ? .78 :''')
# hold the rear: aim each Cube Destroyer formation at its side's back edge, and let the others give way
rep('''    const lay = b.lay || (b.lay = Q.map(() => ({ x: 0, y: 0 }))), P = reps.map(i => { const [rx, ry, w] = fpOf(i); return { i, x: scr[i].x + lay[i].x, y: scr[i].y + lay[i].y, rx, ry, w }; }), x0 = W * .03, x1 = W * .97, y0 = top - (bot - top) * .02, y1 = bot + (bot - top) * .04;''',
    '''    const lay = b.lay || (b.lay = Q.map(() => ({ x: 0, y: 0 }))), P = reps.map(i => { const [rx, ry, w] = fpOf(i); return { i, x: scr[i].x + lay[i].x, y: scr[i].y + lay[i].y, rx, ry, w }; }), x0 = W * .03, x1 = W * .97, y0 = top - (bot - top) * .02, y1 = bot + (bot - top) * .04;
    if (!b.superSide) for (const p of P) { const q = Q[p.i]; if (q.k !== "worldbreaker") continue; /* v531 the Cube Destroyer holds the rear */
      let mo = 0, no = 0, me = 0, ne = 0; for (const o of P) { if (o.i === p.i) continue; if (Q[o.i].side === q.side) { mo += o.x; no++; } else { me += o.x; ne++; } }
      let my = 0, ey = 0; for (const o of P) { if (o.i === p.i) continue; if (Q[o.i].side === q.side) my += o.y; else ey += o.y; } my = no ? my / no : p.y; ey = ne ? ey / ne : p.y;
      const ox = no ? mo / no : p.x, ex = ne ? me / ne : p.x, vert = ne ? Math.abs(ey - my) > Math.abs(ex - ox) : W < H; /* portrait: the sides face each other top and bottom */
      if (vert) { const down = ne ? my >= ey : q.side === "a"; p.y = down ? y1 - p.ry * 1.05 : y0 + p.ry * .6; p.x = clamp(ox, x0 + p.rx * .8, x1 - p.rx * .8); }
      else { const left = ne ? ox <= ex : q.side === "a"; p.x = left ? x0 + p.rx * .8 : x1 - p.rx * .8; } p.w = .12; }''')
s2 = re.sub(r"GAME_V = 530\b", "GAME_V = 531", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
