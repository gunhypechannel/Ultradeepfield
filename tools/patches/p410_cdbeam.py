# v410: the Cube Destroyer fires from the red dish on its hull (the owner's card art: concentric red rings, a white-hot core, a thick red
# beam). The charge pulls three red rings and sparks into the dish while its core heats white; the beam leaves the core (measured on the
# side sprite: 0.47 L forward, 0.15 L down), stops on its target instead of running off the screen, with a red double helix wound round
# it; the hit is a wide splash: a fireball, three shock rings (red, orange, white) out to 20% of the screen, 40 sparks, a hard shake,
# and every enemy formation inside the ring flashes. Visual only: damage is still the simulation's.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("""if (q.k === "worldbreaker") { b.beams = b.beams.filter(m => m.s !== v.s); b.beams.push({ t0: v.t, s: v.s, e: v.e, side, w: 12, charge: .32, life: .55, wb: 1 }); return; }""",
    """if (q.k === "worldbreaker") { b.beams = b.beams.filter(m => m.s !== v.s || m.ht); b.beams.push({ t0: v.t, s: v.s, e: v.e, side, w: 12, charge: .5, life: .7, wb: 1 }); return; }""")
rep("""  b.beams = b.beams.filter(m => T - m.t0 <= m.charge + m.life);""", """  b.beams = b.beams.filter(m => T - m.t0 <= m.charge + m.life + (m.wb ? 1 : 0)); // v410: the Cube Destroyer's splash outlives its beam""")
rep("""  for (const m of b.beams) { const age = T - m.t0; if (age < 0) continue; const A = scr[m.s], E = scr[m.e]; if (!A || !E) continue;""",
    """  for (const m of b.beams) { const age = T - m.t0; if (age < 0) continue;
    if (m.wb) { /* v410 the Cube Destroyer: charge in the dish, beam from its core, a wide splash */ const S0 = scr[m.s], E0 = scr[m.e], g = b.geo && b.geo[m.s], ok = g && g.f === b.gf;
      if (S0 && b.n[m.s] > 0 && !m.ht) { const Lg = ok ? g.L : Math.min(W * .1 * bLen("worldbreaker") * S0.s, W * .55 * S0.s), fc = ok ? g.face : (b.face[m.s] || 1); m.ox = S0.x + fc * Lg * .47; m.oy = S0.y + Lg * .152; m.L = Lg; }
      if (m.ox == null || (!E0 && m.ix == null)) continue;
      const ox = m.ox, oy = m.oy, Lg = m.L, ex = E0 ? E0.x : m.ix, ey = E0 ? E0.y : m.iy, R0 = Lg * .16, red = "#ff2a1a";
      ctx.save(); ctx.globalCompositeOperation = "lighter";
      if (age < m.charge) { const k = age / m.charge; if (!m.cs) { m.cs = 1; try { SFX.charge(sp(ox, oy)); } catch (e) {} }
        ctx.strokeStyle = red; for (let r = 0; r < 3; r++) { const u = (k * 1.6 + r / 3) % 1, rr = R0 * (2.4 - 1.9 * u); ctx.globalAlpha = .3 + .6 * u; ctx.lineWidth = (1.5 + 2.5 * u) * d; ctx.beginPath(); ctx.ellipse(ox, oy, rr * .62, rr, 0, 0, TAU); ctx.stroke(); }
        for (let j = 0; j < (lo ? 3 : 9); j++) { const a = j * 2.4 + m.s * 1.3, u = (k * 2 + j * .137) % 1, rr = R0 * (3.2 - 2.9 * u), px = ox + Math.cos(a) * rr * .7, py = oy + Math.sin(a) * rr; ctx.globalAlpha = u * .9; ctx.drawImage(glowSprite(red), px - 3 * d, py - 3 * d, 6 * d, 6 * d); }
        const cr = R0 * (.4 + 1.1 * k); ctx.globalAlpha = .6 + .4 * k; ctx.drawImage(glowSprite(red), ox - cr * 2, oy - cr * 2, cr * 4, cr * 4); ctx.drawImage(glowSprite("#ffffff"), ox - cr * .5, oy - cr * .5, cr, cr);
        ctx.restore(); continue; }
      const k = (age - m.charge) / m.life;
      if (k < 1) { const al = k < .06 ? k / .06 : Math.pow(Math.max(0, 1 - (k - .06) / .94), 1.4), reach = Math.min(1, k * 7), x1 = ox + (ex - ox) * reach, y1 = oy + (ey - oy) * reach, w = Math.max(5 * d, Lg * .09) * (.85 + .15 * Math.sin(t * .08));
        if (!m.fs) { m.fs = 1; try { SFX.megaBeam(sp(ox, oy)); } catch (e) {} b.shake = Math.max(b.shake, 12 * d); b.flash = Math.max(b.flash, .3); }
        for (const [lw, a, c2] of [[6, .12, red], [3, .35, red], [1.5, .85, "#ff8a6a"], [.6, 1, "#ffffff"]]) { ctx.beginPath(); ctx.moveTo(ox, oy); ctx.lineTo(x1, y1); ctx.strokeStyle = c2; ctx.globalAlpha = al * a * (.5 + .5 * dim); ctx.lineWidth = w * lw; ctx.stroke(); }
        if (!lo) { const dx = x1 - ox, dy = y1 - oy, Ln = Math.hypot(dx, dy) || 1, nx = -dy / Ln, ny = dx / Ln, n = Math.max(8, Ln / (6 * d) | 0);
          for (const ph of [0, Math.PI]) { ctx.beginPath(); for (let s = 0; s <= n; s++) { const f = s / n, a2 = f * Ln / (14 * d) - t * .03 + ph, amp = w * 1.3 * Math.min(1, f * 4), px = ox + dx * f + nx * Math.sin(a2) * amp, py = oy + dy * f + ny * Math.sin(a2) * amp; if (s) ctx.lineTo(px, py); else ctx.moveTo(px, py); } ctx.strokeStyle = red; ctx.globalAlpha = al * .6; ctx.lineWidth = 1.6 * d; ctx.stroke(); } }
        const mr = R0 * (1.3 + .25 * Math.sin(t * .05)); ctx.globalAlpha = al; ctx.drawImage(glowSprite(red), ox - mr * 2, oy - mr * 2, mr * 4, mr * 4); ctx.drawImage(starSprite(red), ox - mr * 1.6, oy - mr * 1.6, mr * 3.2, mr * 3.2); ctx.drawImage(glowSprite("#ffffff"), ox - mr * .5, oy - mr * .5, mr, mr);
        ctx.strokeStyle = red; ctx.lineWidth = 2.5 * d; ctx.globalAlpha = al * .8; ctx.beginPath(); ctx.ellipse(ox, oy, R0 * .62, R0, 0, 0, TAU); ctx.stroke();
        if (reach >= 1 && !m.ht) { m.ht = T || 1e-6; m.ix = ex; m.iy = ey; } }
      if (m.ht) { const u = (T - m.ht) / .9; if (u < 1) { const Rs = Math.max(W, H) * .2, e1 = 1 - Math.pow(1 - u, 3), ix = m.ix, iy = m.iy;
        if (!m.hs) { m.hs = 1; try { SFX.blast(2.4, 0); } catch (e) {} b.shake = Math.max(b.shake, 16 * d); b.flash = Math.max(b.flash, .35); b.flashes.push({ x: ix, y: iy, t, r: Rs * .5, life: 420, rot: Math.random() * .8 });
          if (!lo) for (let j = 0; j < 40 && b.sparks.length < 420; j++) { const a = Math.random() * TAU, v = (.2 + Math.random() * .6) * d; b.sparks.push({ x: ix, y: iy, vx: Math.cos(a) * v, vy: Math.sin(a) * v * .7, t, life: 400 + Math.random() * 500 }); }
          const sd = (Q[m.s] || {}).side; Q.forEach((q, i) => { const p = scr[i]; if (q.side !== sd && b.n[i] > 0 && p && Math.hypot(p.x - ix, (p.y - iy) / .6) < Rs) b.flashes.push({ x: p.x, y: p.y, t: t + 60 + Math.random() * 160, r: (30 + Math.random() * 20) * d, life: 320, rot: Math.random() * .8 }); }); }
        const fr = Rs * (.25 + .45 * e1); ctx.globalAlpha = (1 - u) * .9; ctx.drawImage(glowSprite("fire"), ix - fr, iy - fr * .7, fr * 2, fr * 1.4); ctx.globalAlpha = (1 - u) * .7; ctx.drawImage(glowSprite(red), ix - fr * 1.3, iy - fr * .9, fr * 2.6, fr * 1.8);
        if (u < .25) { const wr = Rs * .25 * (1 - u / .25); ctx.globalAlpha = 1 - u / .25; ctx.drawImage(glowSprite("#ffffff"), ix - wr, iy - wr, wr * 2, wr * 2); }
        for (const [dl, c2, lw] of [[0, red, 9], [.12, "#ff9a5a", 5], [.24, "#ffffff", 2.5]]) { const v = (u - dl) / (1 - dl); if (v <= 0) continue; const R = Rs * (1 - Math.pow(1 - v, 2.4)); ctx.globalAlpha = (1 - v) * .9; ctx.strokeStyle = c2; ctx.lineWidth = lw * d * (1 - v * .6); ctx.beginPath(); ctx.ellipse(ix, iy, R, R * .6, 0, 0, TAU); ctx.stroke(); } } }
      ctx.restore(); ctx.globalAlpha = 1; continue; }
    const A = scr[m.s], E = scr[m.e]; if (!A || !E) continue;""")
t = t.replace("const GAME_V = 409;", "const GAME_V = 410;")
open(p, "w").write(t); print("ok")
