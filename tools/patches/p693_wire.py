# v693 (owner screenshot of an Omega fight): the Omega Cube's tractor beams are solid again (v681 drew them as dashes), every ship
# group can be caught, the Cube Destroyer and the Titans first (it took the first 8 groups in fleet order, so the Cube Destroyer near
# the end of the list never got one), and the Cube turns slower and less often still.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('''else if (m.a === "tractor") { const tg = fx.slice(0, 8); tg.forEach((p, j) => { const k2 = clamp((u - .1 - j * .03) / .2, 0, 1); if (!k2) return; ctx.globalAlpha = .75 * (u > .85 ? (1.1 - u) / .25 : 1); ctx.strokeStyle = C(1); ctx.lineWidth = 6 * d; ctx.setLineDash([10 * d, 6 * d]); ctx.lineDashOffset = T * 160 * d; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx + (p.x - cx) * k2, cy + (p.y - cy) * k2); ctx.stroke(); ctx.setLineDash([]); if (k2 >= 1) ctx.drawImage(gl, p.x - 18 * d, p.y - 18 * d, 36 * d, 36 * d); });''',
    '''else if (m.a === "tractor") { /* v693 solid beams (a soft outer glow, the beam, a white core, rings drawn back along it toward the Cube), the Cube Destroyer and the Titans caught first */
      const rk = i => { const q = b.Q[i] || {}; return q.k === "worldbreaker" ? 0 : q.role === "titan" || q.k === "eclipse" ? 1 : BIG_R.has(q.role) ? 2 : 3; }, tg = foes.map((i, j) => [i, j]).sort((x, y) => rk(x[0]) - rk(y[0]) || x[1] - y[1]).slice(0, lo ? 7 : 12).map(x => scr[x[0]]), fa = u > .85 ? (1.1 - u) / .25 : 1;
      tg.forEach((p, j) => { const k2 = clamp((u - .1 - j * .025) / .2, 0, 1); if (!k2) return; const ex = cx + (p.x - cx) * k2, ey = cy + (p.y - cy) * k2, pul = 1 + .12 * Math.sin(t * .02 + j);
        for (const [lw, al, c2] of [[20, .16, C(1)], [8, .5, C(1)], [2.4, .95, "#ffffff"]]) { ctx.globalAlpha = al * fa; ctx.strokeStyle = c2; ctx.lineWidth = lw * d * pul; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(ex, ey); ctx.stroke(); }
        if (k2 >= 1) { ctx.globalAlpha = .9 * fa; ctx.drawImage(gl, p.x - 22 * d, p.y - 22 * d, 44 * d, 44 * d); const an = Math.atan2(p.y - cy, p.x - cx); ctx.strokeStyle = C(1); ctx.lineWidth = 2 * d;
          for (let r = 0; r < 3; r++) { const q = 1 - ((t * .0009 + r / 3 + j * .13) % 1), rx = cx + (p.x - cx) * q, ry = cy + (p.y - cy) * q, rr = (5 + 9 * q) * d; ctx.globalAlpha = .7 * fa * Math.sin(Math.PI * q); ctx.beginPath(); ctx.ellipse(rx, ry, rr * .35, rr, an, 0, TAU); ctx.stroke(); } } });''')
rep('WBF_OMG = { turn: 2600, hold: 1400, atk: 2600, rest: 6000 };', 'WBF_OMG = { turn: 4000, hold: 2000, atk: 2600, rest: 11000 }; /* v693 slower and rarer still */')
rep('const GAME_V = 692;', 'const GAME_V = 693;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
