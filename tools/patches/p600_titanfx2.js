/* ---------- v600 the Titans' arsenal, second pass (owner: "the drones need a brighter green glow, a cooler swarm animation and a
   drone detonation animation; Sovereign Ark's weapons should be more varied, more unique, worth the wait and the grind").
   Eclipse Harbinger  HS  Neural Swarm v2: drones spiral out of the reactor in a vortex, lock into a turning halo round the hull,
                          pour out in sinuous ribbons with light running along the neural web, circle each target in a tightening
                          spiral and detonate: white flash, emerald shockwave, spark shards, violet crackle, chained to the last blast
   Sovereign Ark      it turns through three main guns, one per salvo:
                      SL  Imperial Lance (v595)
                      SB  Solar Broadside: gun ports ripple down the hull, gold plasma comets, a gold sunburst on every hit
                      SH  Halo of Judgment: twelve motes gather into a turning golden halo, then launch as seeker lances that
                          curve onto the enemy and strike with cross-shaped star flares
                      SP  Gilded Flak (point defence): gold tracer streams and flak bursts ---------- */
const tx6 = {
  /* a cross-shaped star flare: a long horizontal and a shorter vertical streak through a white core */
  cross(ctx, x, y, L, col, a) { if (a <= 0) return; ctx.globalAlpha = Math.min(1, a); const g = glowSprite(col); ctx.drawImage(g, x - L, y - L * .04, L * 2, L * .08); ctx.drawImage(g, x - L * .04, y - L * .6, L * .08, L * 1.2); ctx.drawImage(glowSprite("#ffffff"), x - L * .14, y - L * .14, L * .28, L * .28); },
  /* thin light rays fanning out of a point */
  rays(ctx, x, y, R, n, col, a, rot) { if (a <= 0) return; ctx.save(); ctx.translate(x, y); ctx.rotate(rot || 0); for (let i = 0; i < n; i++) { ctx.rotate(TAU / n); const L = R * (.6 + ((i * 37) % 10) / 22), w = R * .035; const g = ctx.createLinearGradient(0, 0, L, 0); g.addColorStop(0, `rgba(255,255,255,${.9 * a})`); g.addColorStop(.3, `rgba(${col},${.6 * a})`); g.addColorStop(1, `rgba(${col},0)`); ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(0, -w); ctx.lineTo(L, 0); ctx.lineTo(0, w); ctx.fill(); } ctx.restore(); },
  ring(ctx, x, y, r, w, col, a, sq) { if (a <= 0 || r <= 0) return; ctx.globalAlpha = Math.min(1, a); ctx.strokeStyle = col; ctx.lineWidth = Math.max(.5, w); ctx.beginPath(); ctx.ellipse(x, y, r, r * (sq || .7), 0, 0, TAU); ctx.stroke(); } };
Object.assign(TX595, {
  /* ---- Eclipse Harbinger: the Neural Swarm, v2 ---- */
  HS(ctx, b, m, age, S0, E0, fc, Lg, d, lo, T, scr) { const tg = m.tg || (m.tg = tx5.foes(b, m, scr, E0 || S0, 6)); if (!tg.length) { if (!E0) return; tg.push(m.e); }
    const n = lo ? 8 : 18, ds = Math.max(6.5 * d, Lg * .05), RR = Lg * .55, e3 = tx5.ease;
    const D = m.dr || (m.dr = Array.from({ length: n }, (_, i) => { const tS = .75 + (i % 6) * .035 + Math.floor(i / 6) * .02, tA = tS + .72 + tx5.rnd(m.seed || 5, i) * .12, tD = tA + .3; return { a: i / n * TAU, tS, tA, tD, j: tg[i % tg.length] }; }));
    const ring = (q, t) => { const a = q.a + 3 + (t - .45) * 5; return [S0.x + Math.cos(a) * RR, S0.y + Math.sin(a) * RR * .6]; };
    const pos = (i, t) => { const q = D[i], T0 = scr[q.j] || E0; if (t < .45) { const k = clamp((t - i * .015) / (.45 - i * .015), 0, 1), a = q.a + k * 3, r = Lg * (.08 + .47 * e3(k)); return [S0.x + Math.cos(a) * r, S0.y + Math.sin(a) * r * .6]; }
      if (t < q.tS || !T0) return ring(q, t); const p0 = ring(q, q.tS), ent = [T0.x + Math.cos(q.a) * Lg * .3, T0.y + Math.sin(q.a) * Lg * .18];
      if (t < q.tA) { const u = (t - q.tS) / (q.tA - q.tS), dx = p0[0] - S0.x, dy = p0[1] - S0.y, dl = Math.hypot(dx, dy) || 1, p1 = [p0[0] + dx / dl * Lg * .7, p0[1] + dy / dl * Lg * .7], p2 = [ent[0] - fc * Lg * .5, ent[1] + (tx5.rnd(i, 7) - .5) * Lg * .7];
        const [x, y] = tx5.bez(p0, p1, p2, ent, u * u * (3 - 2 * u)), w = Math.sin(u * Math.PI) * Math.sin(u * 11 + i) * Lg * .07; return [x - dy / dl * w, y + dx / dl * w]; }
      const v = clamp((t - q.tA) / (q.tD - q.tA), 0, 1), a = q.a + v * TAU * 1.2, r = Lg * (.3 - .22 * v); return [T0.x + Math.cos(a) * r, T0.y + Math.sin(a) * r * .6]; };
    /* the reactor flares as the swarm pours out, and a vortex ring turns round the hull while the halo holds */
    const rg = age < .9 ? (age < .2 ? age / .2 : 1 - Math.max(0, (age - .6) / .3)) : 0; tx5.glow(ctx, S0.x, S0.y, Lg * .38, "#3dff9a", .8 * rg); tx5.glow(ctx, S0.x, S0.y, Lg * .12, "#ffffff", .7 * rg);
    if (!lo && rg > 0) { ctx.save(); ctx.translate(S0.x, S0.y); ctx.scale(1, .6); ctx.rotate(age * 4); ctx.globalAlpha = .55 * rg; ctx.strokeStyle = "#7dffb8"; ctx.lineWidth = 1.6 * d; ctx.setLineDash([Lg * .09, Lg * .05]); ctx.beginPath(); ctx.arc(0, 0, RR, 0, TAU); ctx.stroke(); ctx.setLineDash([]); ctx.restore(); }
    const P = [], booms = [];
    for (let i = 0; i < n; i++) { const q = D[i]; if (age < i * .015) { P.push(null); continue; }
      if (age >= q.tD) { const c = (age - q.tD) / .45; P.push(null); if (c < 1) booms.push([i, c, pos(i, q.tD)]); continue; }
      const [x, y] = pos(i, age), [xa, ya] = pos(i, Math.max(0, age - .012)), an = Math.atan2(y - ya, x - xa); P.push([x, y]);
      if (!lo) { ctx.lineCap = "round"; for (let k = 0; k < 7; k++) { const [x1, y1] = pos(i, Math.max(0, age - k * .02)), [x2, y2] = pos(i, Math.max(0, age - (k + 1) * .02)); ctx.globalAlpha = .6 * (1 - k / 7); ctx.strokeStyle = k < 3 ? "#7dffb8" : "#b06bff"; ctx.lineWidth = (2.4 - k * .25) * d; ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke(); } } // a green-to-violet ribbon
      tx5.glow(ctx, x, y, ds * 2.6, "#3dff9a", .55); // the bright emerald halo
      ctx.globalAlpha = 1; if (!tx5.craft(ctx, "drone", "#3dff9a", "rgba(20,70,44,.34)", x, y, an, ds * 2)) { ctx.save(); ctx.globalCompositeOperation = "source-over"; ctx.translate(x, y); ctx.rotate(an); ctx.fillStyle = "#0b1a12"; ctx.strokeStyle = "#5dffa8"; ctx.lineWidth = Math.max(.7, .9 * d); ctx.beginPath(); ctx.moveTo(ds * 1.2, 0); ctx.lineTo(-ds * .6, -ds * .8); ctx.lineTo(-ds * .2, 0); ctx.lineTo(-ds * .6, ds * .8); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore(); }
      ctx.globalCompositeOperation = "lighter"; const fl = .6 + .4 * Math.sin(age * 60 + i * 2);
      tx5.glow(ctx, x + Math.cos(an) * ds * .9, y + Math.sin(an) * ds * .9, ds * .9 * fl, "#5dffa8", 1); tx5.glow(ctx, x + Math.cos(an) * ds * .9, y + Math.sin(an) * ds * .9, ds * .35, "#ffffff", 1); tx5.glow(ctx, x - Math.cos(an) * ds * 1.1, y - Math.sin(an) * ds * 1.1, ds * .9 * fl, "#b06bff", .7); }
    /* the neural web, with light running along each link */
    if (!lo) for (let i = 0; i < P.length; i++) for (const jj of [i + 1, i + 3]) { const A = P[i], B = P[jj]; if (!A || !B) continue; const L = Math.hypot(B[0] - A[0], B[1] - A[1]); if (L > Lg * 1.3) continue; const a = 1 - L / (Lg * 1.3);
      ctx.globalAlpha = .45 * a; ctx.strokeStyle = "#5dffa8"; ctx.lineWidth = .9 * d; ctx.beginPath(); ctx.moveTo(A[0], A[1]); ctx.lineTo(B[0], B[1]); ctx.stroke(); const s = (age * 2.6 + i * .37) % 1; tx5.glow(ctx, A[0] + (B[0] - A[0]) * s, A[1] + (B[1] - A[1]) * s, 4 * d, "#d8ffe8", .9 * a); }
    /* the detonations: a white flash, an emerald shockwave, spark shards and violet crackle, chained to the drone before */
    for (const [i, c, [x, y]] of booms) { const a = 1 - c, ec = e3(c);
      if (!m["h" + i]) { m["h" + i] = 1; if (!m.hit) { m.hit = 1; b.shake = Math.max(b.shake || 0, 7 * d); } }
      tx5.glow(ctx, x, y, Lg * (.1 + .25 * ec), "#3dff9a", a); if (c < .25) tx5.glow(ctx, x, y, Lg * .16 * (1 - c * 3), "#ffffff", 1 - c * 4);
      tx6.ring(ctx, x, y, Lg * .38 * ec, 3 * d * a, "#7dffb8", a * .9, .62); if (!lo) tx6.ring(ctx, x, y, Lg * .22 * ec, 1.5 * d * a, "#ffffff", a * .6, .62);
      if (!lo) { ctx.strokeStyle = "#c8ffe0"; ctx.lineWidth = 1.4 * d; ctx.lineCap = "round"; for (let k = 0; k < 6; k++) { const an = tx5.rnd(i, k + 20) * TAU, r0 = Lg * .06 * ec, r1 = Lg * (.1 + .3 * ec) * (.6 + tx5.rnd(i, k + 40) * .6); ctx.globalAlpha = a; ctx.beginPath(); ctx.moveTo(x + Math.cos(an) * r0, y + Math.sin(an) * r0 * .7); ctx.lineTo(x + Math.cos(an) * r1, y + Math.sin(an) * r1 * .7); ctx.stroke(); } }
      if (!lo && c < .45) for (let k = 0; k < 2; k++) { const an = tx5.rnd(i, k + 60) * TAU, R = Lg * .3; tx5.bolt(ctx, x, y, x + Math.cos(an) * R, y + Math.sin(an) * R * .7, 5, R * .2, i * 5 + k + Math.floor(age * 30), "#c890ff", 1.2 * d, (1 - c / .45) * .9); }
      const pv = booms.find(o => o[0] === i - 1); if (pv && c < .3 && pv[1] < .5) tx5.bolt(ctx, pv[2][0], pv[2][1], x, y, 6, Lg * .05, i * 3.3 + Math.floor(age * 25), "#7dffb8", 1.3 * d, (1 - c / .3) * .8); } },
  /* ---- Sovereign Ark: the Solar Broadside ---- */
  SB(ctx, b, m, age, S0, E0, fc, Lg, d, lo) { if (!E0) return; const N = lo ? 4 : 8, TR = .38;
    for (let j = 0; j < N; j++) { const tj = j * .07, px = S0.x + fc * Lg * (-.36 + j * (.72 / (N - 1))), py = S0.y + (j % 2 ? -1 : 1) * Lg * .07, tx = E0.x + (tx5.rnd(m.seed || 3, j) - .5) * Lg * .35, ty = E0.y + (tx5.rnd(m.seed || 3, j + 9) - .5) * Lg * .22, k = age - tj; if (k < 0) continue;
      if (k < .14) { const f = 1 - k / .14; tx5.glow(ctx, px, py, Lg * .09 * f + 2 * d, "#ffd36b", f); tx5.flare(ctx, px, py, Lg * .22 * f, "#ffd36b", f * .8); } // the gun port flashes
      const pt = u => { const e = u; return [px + (tx - px) * e, py + (ty - py) * e - Math.sin(e * Math.PI) * Lg * .12 * (j % 2 ? 1 : -1)]; };
      if (k < TR) { const u = k / TR, [x, y] = pt(u); ctx.lineCap = "round"; for (let s = 0; s < 6; s++) { const [x1, y1] = pt(Math.max(0, u - s * .025)), [x2, y2] = pt(Math.max(0, u - (s + 1) * .025)); ctx.globalAlpha = .85 * (1 - s / 6); ctx.strokeStyle = s < 2 ? "#fff3c8" : "#ffb02e"; ctx.lineWidth = (Lg * .028 - s * Lg * .003) + d; ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke(); }
        tx5.glow(ctx, x, y, Lg * .1, "#ffd36b", 1); tx5.glow(ctx, x, y, Lg * .035, "#ffffff", 1); continue; } // a gold plasma comet
      const c = (k - TR) / .4; if (c > 1) continue; const a = 1 - c; if (!m["b" + j]) { m["b" + j] = 1; if (j === 0) b.shake = Math.max(b.shake || 0, 4 * d); }
      tx5.glow(ctx, tx, ty, Lg * (.12 + .14 * c), "#ffb02e", a); if (c < .3) tx5.glow(ctx, tx, ty, Lg * .07, "#ffffff", 1 - c / .3); tx6.rays(ctx, tx, ty, Lg * (.15 + .25 * tx5.ease(c)), lo ? 6 : 10, "255,200,90", a, j); tx6.ring(ctx, tx, ty, Lg * .3 * tx5.ease(c), 2 * d * a, "#ffd36b", a * .8); } }, // a gold sunburst
  /* ---- Sovereign Ark: the Halo of Judgment ---- */
  SH(ctx, b, m, age, S0, E0, fc, Lg, d, lo, T, scr) { if (!E0) return; const N = lo ? 6 : 12, RR = Lg * .45, G0 = .45, tg = m.tg || (m.tg = tx5.foes(b, m, scr, E0, 3));
    const ringA = j => j / N * TAU + age * 1.6, rp = j => [S0.x + Math.cos(ringA(j)) * RR, S0.y + Math.sin(ringA(j)) * RR * .55];
    const hk = age < G0 ? age / G0 : 1, hf = age > G0 + N * .035 ? Math.max(0, 1 - (age - G0 - N * .035) / .3) : 1; // the halo gathers, holds while it launches, fades
    if (hf > 0) { ctx.save(); ctx.translate(S0.x, S0.y); ctx.scale(1, .55); ctx.globalAlpha = .75 * hk * hf; ctx.strokeStyle = "#ffd36b"; ctx.lineWidth = 2 * d; ctx.beginPath(); ctx.arc(0, 0, RR, 0, TAU); ctx.stroke(); ctx.globalAlpha = .45 * hk * hf; ctx.lineWidth = 1 * d; ctx.beginPath(); ctx.arc(0, 0, RR * 1.12, 0, TAU); ctx.stroke();
      ctx.rotate(-age * 1.2); for (let i = 0; i < 24; i++) { ctx.rotate(TAU / 24); ctx.globalAlpha = .6 * hk * hf; ctx.fillStyle = "#ffe6a0"; ctx.fillRect(RR * 1.04, -.8 * d, RR * .06, 1.6 * d); } ctx.restore(); tx5.glow(ctx, S0.x, S0.y, Lg * .6 * hk, "#ffd36b", .35 * hf); } // twin rings and turning ticks
    for (let j = 0; j < N; j++) { const tL = G0 + j * .035, T0 = scr[tg[j % tg.length]] || E0, tx = T0.x + (tx5.rnd(m.seed || 7, j) - .5) * Lg * .3, ty = T0.y + (tx5.rnd(m.seed || 7, j + 5) - .5) * Lg * .2;
      if (age < tL) { const k = clamp(age / G0, 0, 1), a = ringA(j) - (1 - k) * 2, r = RR * (2.2 - 1.2 * tx5.ease(k)); const x = S0.x + Math.cos(a) * r, y = S0.y + Math.sin(a) * r * .55; tx5.star(ctx, x, y, (4 + 4 * k) * d, "#ffe6a0", .5 + .5 * k); tx5.glow(ctx, x, y, 6 * d, "#ffd36b", .8); continue; } // the motes gather into the halo
      const p0 = rp(j), dx = p0[0] - S0.x, dy = p0[1] - S0.y, dl = Math.hypot(dx, dy) || 1, p1 = [p0[0] + dx / dl * Lg * .6, p0[1] + dy / dl * Lg * .6], p2 = [tx - fc * Lg * .4, ty - Lg * .3], u = (age - tL) / .5;
      if (u < 1) { const pt = s => tx5.bez(p0, p1, p2, [tx, ty], s), [x, y] = pt(u), [x0, y0] = pt(Math.max(0, u - .14)); tx5.beam(ctx, x0, y0, x, y, [[Lg * .03 + 2 * d, "255,200,90", .5], [Lg * .008 + .8 * d, "255,255,255", 1]], 1); tx5.star(ctx, x, y, 9 * d, "#fff3c8", 1); continue; } // a seeker lance
      const c = (u - 1) * .5 / .35; if (c > 1) continue; if (!m["s" + j]) { m["s" + j] = 1; if (j === 0) b.shake = Math.max(b.shake || 0, 5 * d); }
      tx6.cross(ctx, tx, ty, Lg * .35 * (1 - c * .5), "#ffd36b", 1 - c); tx5.glow(ctx, tx, ty, Lg * .14 * (1 - c), "#ffe6a0", 1 - c); } }, // a cross-shaped star flare
  /* ---- Sovereign Ark: Gilded Flak ---- */
  SP(ctx, b, m, age, S0, E0, fc, Lg, d, lo) { if (!E0) return; const N = lo ? 3 : 5, L = .5, a = age < .06 ? age / .06 : 1 - Math.max(0, (age - .3) / .2);
    for (let j = 0; j < N; j++) { const px = S0.x + fc * Lg * (-.25 + j * .14), py = S0.y + (j % 2 ? -1 : 1) * Lg * .1, tx = E0.x + (tx5.rnd(m.seed || 4, j) - .5) * Lg * .5, ty = E0.y + (tx5.rnd(m.seed || 4, j + 3) - .5) * Lg * .3;
      ctx.globalAlpha = .85 * a; ctx.strokeStyle = "#ffd36b"; ctx.lineWidth = 1.6 * d; ctx.setLineDash([5 * d, 9 * d]); ctx.lineDashOffset = -age * 900 * d; ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(tx, ty); ctx.stroke(); ctx.setLineDash([]); tx5.glow(ctx, px, py, 5 * d, "#ffe6a0", a); // tracer stream
      for (let k = 0; k < (lo ? 2 : 3); k++) { const tb = .12 + k * .1 + j * .02, c = (age - tb) / .28; if (c < 0 || c > 1) continue; const bx = tx + (tx5.rnd(j, k + 11) - .5) * Lg * .2, by = ty + (tx5.rnd(j, k + 13) - .5) * Lg * .14;
        tx5.glow(ctx, bx, by, Lg * .07 * (.5 + c), "#ffb02e", 1 - c); tx5.star(ctx, bx, by, Lg * .05 * (1 - c * .5), "#fff3c8", 1 - c); tx6.ring(ctx, bx, by, Lg * .09 * c, 1.2 * d, "#ffd36b", (1 - c) * .8); } } } }); // flak bursts
