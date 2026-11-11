# v422 (2): the Cube Destroyer holds its lock and cycles three attacks. Once it has turned onto a target it no longer swings back to its
# rest pose between shots: it holds its aim and turns the short way to the next target. Its staged shots (cdPlan) cycle per formation:
#   1 "beam"  the superlaser: 1.2 s charge, a 1.6 s beam, the shock-ring splash (as v418);
#   2 "sweep" a raking beam: it lands on its target, then sweeps across to the nearest other enemy group, explosions along its path and
#             the station tracking the sweep, a smaller splash where it ends (charge 1 s, beam 2.2 s);
#   3 "nova"  a 1.6 s charge in a dish half again as large, then a plasma orb hurled from the dish (trail, crackling arcs, launch flash)
#             that detonates in the biggest splash (34% of the screen, 1.7 s) with a white-out flash.
# Each is timed so its hit lands with the replay's volley. If the target dies first, the shot finishes where it last was.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("let want = CD_PHI0; if (m) { const E = scr[m.e] || (m.ix != null ? { x: m.ix, y: m.iy } : null);",
    "let want = A[i] == null ? CD_PHI0 : A[i]; /* v422 it holds its lock between shots */ if (m) { const E = (m.mode === \"sweep\" && m.cxy) || scr[m.e] || (m.ix != null ? { x: m.ix, y: m.iy } : m.lx != null ? { x: m.lx, y: m.ly } : null);")
rep("out.push({ t0: Math.max(.3, v.t - 1.4), s: v.s, e: v.e, side: q.side, w: 12, charge: 1.2, life: 1.6, wb: 1 }); }",
    "const md = CD_MODES[(cnt[v.s] = (cnt[v.s] || 0) + 1) % 3 === 1 ? 0 : cnt[v.s] % 3 === 2 ? 1 : 2]; out.push({ t0: Math.max(.3, v.t - md.lead), s: v.s, e: v.e, side: q.side, w: 12, charge: md.charge, life: md.life, wb: 1, mode: md.m }); }")
rep("function cdPlan(b) { const out = [], last = {}, ord = {};", "const CD_MODES = [{ m: \"beam\", charge: 1.2, life: 1.6, lead: 1.4 }, { m: \"sweep\", charge: 1, life: 2.2, lead: 1.2 }, { m: \"nova\", charge: 1.6, life: 1, lead: 2.55 }]; // v422 its three attacks, in turn\nfunction cdPlan(b) { const out = [], last = {}, ord = {}, cnt = {};")
rep('if (m.ox == null || (!E0 && m.ix == null)) continue;', 'if (E0) { m.lx = E0.x; m.ly = E0.y; } if (m.ox == null || (!E0 && m.ix == null && m.lx == null)) continue;')
rep('const ox = m.ox, oy = m.oy, Lg = m.L, ex = E0 ? E0.x : m.ix, ey = E0 ? E0.y : m.iy, R0 = Lg * .16, red = "#ff2a1a";',
    'const ox = m.ox, oy = m.oy, Lg = m.L, R0 = Lg * .16 * (m.mode === "nova" ? 1.5 : 1), red = "#ff2a1a"; let ex = E0 ? E0.x : m.ix != null ? m.ix : m.lx, ey = E0 ? E0.y : m.iy != null ? m.iy : m.ly;')
rep("if (k < 1) { const al = k < .06 ? k / .06", """if (k < 1 && m.mode === "sweep") { /* v422 the raking beam: from its target across to the nearest other enemy group */
        if (m.e2 == null) { const sd = (Q[m.s] || {}).side; let best = -1, bd = 1e9; Q.forEach((q, i) => { const p = scr[i]; if (i !== m.e && q.side !== sd && b.n[i] > 0 && p) { const dd = Math.hypot(p.x - ex, p.y - ey); if (dd < bd && dd > 30 * d) { bd = dd; best = i; } } }); m.e2 = best; }
        const P2 = m.e2 >= 0 ? scr[m.e2] : null, tx2 = P2 ? P2.x : ex + 140 * d, ty2 = P2 ? P2.y : ey - 30 * d, u2 = clamp((k - .18) / .7, 0, 1), es = u2 * u2 * (3 - 2 * u2); ex += (tx2 - ex) * es; ey += (ty2 - ey) * es; m.cxy = { x: ex, y: ey };
        if (k > .15 && (!m.lf || T - m.lf > .12)) { m.lf = T; b.flashes.push({ x: ex + (Math.random() - .5) * 24 * d, y: ey + (Math.random() - .5) * 16 * d, t, r: (34 + Math.random() * 26) * d, life: 300, rot: Math.random() * .8 }); b.shake = Math.max(b.shake, 6 * d); } }
      if (k < 1 && m.mode === "nova") { /* v422 the nova: a plasma orb hurled from the dish */ const al = Math.min(1, k * 8), e3 = k * k * (1.6 - .6 * k), px = ox + (ex - ox) * e3, py = oy + (ey - oy) * e3, rr = R0 * (1.1 + .15 * Math.sin(t * .04));
        if (!m.fs) { m.fs = 1; try { SFX.megaBeam(sp(ox, oy)); } catch (e) {} b.shake = Math.max(b.shake, 14 * d); b.flash = Math.max(b.flash, .35); }
        for (let j = 1; j <= 6; j++) { const f = Math.max(0, e3 - j * .035), qx = ox + (ex - ox) * f, qy = oy + (ey - oy) * f; ctx.globalAlpha = al * (.5 - j * .07); ctx.drawImage(glowSprite(red), qx - rr * 1.6, qy - rr * 1.6, rr * 3.2, rr * 3.2); }
        ctx.globalAlpha = al; ctx.drawImage(glowSprite(red), px - rr * 3, py - rr * 3, rr * 6, rr * 6); ctx.drawImage(starSprite(red), px - rr * 2.2, py - rr * 2.2, rr * 4.4, rr * 4.4); ctx.drawImage(glowSprite("#ffffff"), px - rr * .8, py - rr * .8, rr * 1.6, rr * 1.6);
        if (!lo) { ctx.strokeStyle = "#ffd0c0"; ctx.lineWidth = 1.6 * d; for (let j = 0; j < 5; j++) { let a = Math.random() * TAU, x = px, y = py; ctx.globalAlpha = al * .8; ctx.beginPath(); ctx.moveTo(x, y); for (let s = 0; s < 4; s++) { a += (Math.random() - .5) * 1.4; x += Math.cos(a) * rr * .6; y += Math.sin(a) * rr * .6; ctx.lineTo(x, y); } ctx.stroke(); } }
        if (k < .15) { const mr = R0 * 1.6 * (1 - k / .15); ctx.globalAlpha = 1; ctx.drawImage(glowSprite("#ffffff"), ox - mr, oy - mr, mr * 2, mr * 2); }
        if (k >= .97 && !m.ht) { m.ht = T || 1e-6; m.ix = ex; m.iy = ey; } }
      else if (k < 1) { const al = k < .06 ? k / .06""")
rep("if (reach >= 1 && !m.ht) { m.ht = T || 1e-6; m.ix = ex; m.iy = ey; } }", "if (reach >= 1 && !m.ht && (m.mode !== \"sweep\" || k > .9)) { m.ht = T || 1e-6; m.ix = ex; m.iy = ey; } }")
rep("const u = (T - m.ht) / 1.3;", "const u = (T - m.ht) / (m.mode === \"nova\" ? 1.7 : 1.3);")
rep("const Rs = Math.max(W, H) * .26,", "const Rs = Math.max(W, H) * (m.mode === \"nova\" ? .34 : m.mode === \"sweep\" ? .2 : .26),")
rep("b.shake = Math.max(b.shake, 16 * d); b.flash = Math.max(b.flash, .35);", "b.shake = Math.max(b.shake, (m.mode === \"nova\" ? 22 : 16) * d); b.flash = Math.max(b.flash, m.mode === \"nova\" ? .65 : .35);")
open(p, "w").write(t); print("ok")
