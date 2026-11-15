/* ---------- v595 the Sovereign Ark and the Eclipse Harbinger, remastered (owner: "the last ships, they need to be unique and
   breathtaking with popping details and HDR"). Each attack is its own staged shot in the battle's beam pipeline (b.beams, ti = two
   letters), timed in battle time so slow motion and pause apply; a hidden volley still lands the damage at the right moment.
   Sovereign Ark  SL  Imperial Lance: gold sparks gather at the prow while running lights race along the hull, then twin white-hot
                      beams wrapped in a gold helix with pulses running down them; the target's shield breaks into gold hex shards
                  SW  Fleet Command: a gold command wave and uplink lines to every friendly squadron, then a strike wing of gold-
                      trimmed fighters launches from both hangars, strafes the enemy and peels away
   Eclipse Harbinger HP Eclipse Pulse: six arms focus violet and emerald beams into one point where a black eclipse with an emerald
                      corona forms, flies to the target and implodes into an emerald blast with violet lightning
                  HS  Neural Swarm: drones pour out of the reactor, linked by a neural web, weave out to up to six formations and burst
                  HT  arm-tip lasers converging from all six arms ---------- */
function tx595Draw(ctx, b, m, age, scr, W, d, lo, T) { const S0 = scr[m.s]; if (!S0) return; const q = b.Q[m.s]; if (!q) return;
  const fc = b.face[m.s] || 1, Lg = Math.max(30 * d, W * .1 * bLen(q.k) * S0.s), E0 = scr[m.e] || null, f = TX595[m.ti]; if (!f) return;
  ctx.save(); ctx.globalCompositeOperation = "lighter"; try { f(ctx, b, m, age, S0, E0, fc, Lg, d, lo, T, scr); } catch (e) {} ctx.restore(); }
const tx5 = {
  glow(ctx, x, y, r, col, a) { if (a <= 0 || r <= 0) return; ctx.globalAlpha = Math.min(1, a); ctx.drawImage(glowSprite(col), x - r, y - r, r * 2, r * 2); },
  star(ctx, x, y, r, col, a) { if (a <= 0 || r <= 0) return; ctx.globalAlpha = Math.min(1, a); ctx.drawImage(starSprite(col), x - r, y - r, r * 2, r * 2); },
  /* an anamorphic lens flare: a long thin horizontal streak through a bright core */
  flare(ctx, x, y, L, col, a) { if (a <= 0) return; ctx.globalAlpha = Math.min(1, a); const g = glowSprite(col); ctx.drawImage(g, x - L, y - L * .045, L * 2, L * .09); ctx.drawImage(g, x - L * .35, y - L * .02, L * .7, L * .04); ctx.drawImage(glowSprite("#ffffff"), x - L * .12, y - L * .12, L * .24, L * .24); },
  /* a beam with a soft sheath and a white-hot core: layers = [[width, "r,g,b", alpha], ...] */
  beam(ctx, x1, y1, x2, y2, layers, a) { const L = Math.hypot(x2 - x1, y2 - y1); if (L < 1 || a <= 0) return; ctx.save(); ctx.translate(x1, y1); ctx.rotate(Math.atan2(y2 - y1, x2 - x1));
    for (const [w, c, al] of layers) { const g = ctx.createLinearGradient(0, -w, 0, w); g.addColorStop(0, `rgba(${c},0)`); g.addColorStop(.5, `rgba(${c},${Math.min(1, al * a)})`); g.addColorStop(1, `rgba(${c},0)`); ctx.globalAlpha = 1; ctx.fillStyle = g; ctx.fillRect(0, -w, L, w * 2); }
    ctx.restore(); },
  bolt(ctx, x1, y1, x2, y2, seg, amp, seed, col, w, a) { ctx.globalAlpha = Math.min(1, a); ctx.strokeStyle = col; ctx.lineWidth = w; ctx.beginPath(); ctx.moveTo(x1, y1); const nx = -(y2 - y1), ny = x2 - x1, nl = Math.hypot(nx, ny) || 1;
    for (let i = 1; i < seg; i++) { const u = i / seg, o = (((Math.sin(seed + i * 12.9898) * 43758.5453) % 1) - .25) * amp * 2; ctx.lineTo(x1 + (x2 - x1) * u + nx / nl * o, y1 + (y2 - y1) * u + ny / nl * o); } ctx.lineTo(x2, y2); ctx.stroke(); },
  rnd: (s, i) => { const x = Math.sin(s * 9.13 + i * 78.233) * 43758.5453; return x - Math.floor(x); },
  ease: x => 1 - Math.pow(1 - x, 3),
  bez(p0, p1, p2, p3, u) { const v = 1 - u; return [v * v * v * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u * u * u * p3[0], v * v * v * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u * u * u * p3[1]]; },
  foes(b, m, scr, from, n) { const sd = b.Q[m.s].side, L = []; b.Q.forEach((q2, j) => { if (q2.side !== sd && b.n[j] > 0 && scr[j]) L.push([Math.hypot(scr[j].x - from.x, scr[j].y - from.y), j]); }); L.sort((a, c) => a[0] - c[0]); return L.slice(0, n).map(x => x[1]); },
  friends(b, m, scr, n) { const sd = b.Q[m.s].side, L = []; b.Q.forEach((q2, j) => { if (j !== m.s && q2.side === sd && b.n[j] > 0 && scr[j]) L.push(j); }); return L.slice(0, n); } };
const TX595 = {
  /* ---- Sovereign Ark: the Imperial Lance ---- */
  SL(ctx, b, m, age, S0, E0, fc, Lg, d, lo) { const CH = .26, mx = S0.x + fc * Lg * .47, my = S0.y;
    if (age < CH) { const k = age / CH;
      for (let i = 0; i < 6; i++) { const u = (k * 1.6 - i / 6); if (u < 0 || u > 1) continue; tx5.glow(ctx, S0.x + fc * Lg * (-.42 + i * .16), S0.y + Lg * .05, 3.2 * d, "#ffd36b", (1 - Math.abs(u - .5) * 2) * .9); } // running lights race to the prow
      if (!lo) for (let i = 0; i < 12; i++) { const a = tx5.rnd(m.seed || 3, i) * TAU, r = Lg * .45 * (1 - k) * (.5 + tx5.rnd(5, i) * .5); tx5.star(ctx, mx + Math.cos(a) * r, my + Math.sin(a) * r * .6, (2.5 + 3 * k) * d, "#ffd36b", .4 + .6 * k); }
      tx5.glow(ctx, mx, my, Lg * (.05 + .1 * k), "#ffd36b", .6 + .4 * k); tx5.glow(ctx, mx, my, Lg * .04 * k, "#ffffff", k); return; }
    if (!E0) return; const u = (age - CH) / .6, env = u < .1 ? u / .1 : 1 - Math.max(0, (u - .55) / .45), wv = Lg * .026 * env, ang = Math.atan2(E0.y - my, E0.x - mx), px = -Math.sin(ang), py = Math.cos(ang), L = Math.hypot(E0.x - mx, E0.y - my);
    if (!m.fired) { m.fired = 1; b.shake = Math.max(b.shake || 0, 6 * d); b.flash = Math.max(b.flash || 0, .3); }
    for (const sd of [-1, 1]) { const ox = px * sd * Lg * .03, oy = py * sd * Lg * .03; tx5.beam(ctx, mx + ox, my + oy, E0.x + ox * .25, E0.y + oy * .25, [[wv * 2.8, "60,150,255", .28], [wv * 1.3, "140,215,255", .7], [wv * .42, "255,255,255", 1]], env); }
    if (!lo) { ctx.globalAlpha = .85 * env; ctx.strokeStyle = "rgba(255,214,120,1)"; ctx.lineWidth = 1.6 * d; for (const ph of [0, Math.PI]) { ctx.beginPath(); for (let i = 0; i <= 40; i++) { const s = i / 40, o = Math.sin(s * L / (Lg * .09) - age * 38 + ph) * wv * 1.9 * (1 - s * .5); const x = mx + (E0.x - mx) * s + px * o, y = my + (E0.y - my) * s + py * o; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke(); } } // the gold helix
    for (let j = 0; j < 3; j++) { const s = (age * 2.4 + j / 3) % 1; tx5.glow(ctx, mx + (E0.x - mx) * s, my + (E0.y - my) * s, wv * 2.2, "#bfe8ff", env * .9); } // pulses running down the beams
    tx5.flare(ctx, mx, my, Lg * .55 * env, "#ffd36b", env * .9); tx5.glow(ctx, mx, my, Lg * .12 * env, "#ffffff", env);
    tx5.glow(ctx, E0.x, E0.y, Lg * (.16 + .05 * Math.sin(age * 60)), "#7fd0ff", env); tx5.flare(ctx, E0.x, E0.y, Lg * .35 * env, "#bfe8ff", env * .8);
    const hk = clamp((u - .05) / .9, 0, 1); if (hk > 0) { ctx.globalAlpha = (1 - hk) * .95; ctx.strokeStyle = "#ffd36b"; ctx.lineWidth = 1.5 * d; for (let i = 0; i < (lo ? 6 : 14); i++) { const a = tx5.rnd(m.seed || 7, i) * TAU, r = Lg * (.05 + .45 * tx5.ease(hk) * (.5 + tx5.rnd(11, i) * .6)), hx = E0.x + Math.cos(a) * r, hy = E0.y + Math.sin(a) * r * .7, hs = (3 + tx5.rnd(13, i) * 5) * d * (1 - hk * .5);
        ctx.beginPath(); for (let v2 = 0; v2 < 6; v2++) { const aa = v2 / 6 * TAU + hk * 4 + i; v2 ? ctx.lineTo(hx + Math.cos(aa) * hs, hy + Math.sin(aa) * hs) : ctx.moveTo(hx + Math.cos(aa) * hs, hy + Math.sin(aa) * hs); } ctx.closePath(); ctx.stroke(); } // the shield breaks into gold hex shards
      ctx.globalAlpha = (1 - hk) * .7; ctx.strokeStyle = "#bfe8ff"; ctx.lineWidth = 2 * d * (1 - hk); ctx.beginPath(); ctx.ellipse(E0.x, E0.y, Lg * .7 * hk, Lg * .42 * hk, 0, 0, TAU); ctx.stroke(); } },
  /* ---- Sovereign Ark: Fleet Command and the strike wing ---- */
  SW(ctx, b, m, age, S0, E0, fc, Lg, d, lo, T, scr) {
    const ck = age / .9; if (ck < 1) { const r = Lg * (.3 + 2.2 * tx5.ease(ck)); ctx.globalAlpha = (1 - ck) * .8; ctx.strokeStyle = "#ffd36b"; ctx.lineWidth = 2.4 * d * (1 - ck) + .6 * d; ctx.beginPath(); for (let i = 0; i <= 6; i++) { const a = i / 6 * TAU + .52; i ? ctx.lineTo(S0.x + Math.cos(a) * r, S0.y + Math.sin(a) * r * .55) : ctx.moveTo(S0.x + Math.cos(a) * r, S0.y + Math.sin(a) * r * .55); } ctx.stroke();
      tx5.glow(ctx, S0.x, S0.y, Lg * .5 * (1 - ck), "#ffd36b", (1 - ck) * .8);
      const fr = m.fr || (m.fr = tx5.friends(b, m, scr, 6)); for (const j of fr) { const P = scr[j]; if (!P) continue; ctx.globalAlpha = (1 - ck) * .6; ctx.strokeStyle = "rgba(255,214,120,1)"; ctx.lineWidth = 1.2 * d; ctx.setLineDash([4 * d, 5 * d]); ctx.lineDashOffset = -age * 60 * d; ctx.beginPath(); ctx.moveTo(S0.x, S0.y); ctx.lineTo(P.x, P.y); ctx.stroke(); ctx.setLineDash([]); tx5.glow(ctx, P.x, P.y, 14 * d * S0.s + 8 * d, "#ffd36b", (1 - ck) * .7); } }
    const tg = m.tg || (m.tg = tx5.foes(b, m, scr, E0 || S0, 3)); if (!tg.length && E0) tg.push(m.e); const n = lo ? 4 : 10, fs = Math.max(8 * d, Lg * .075);
    for (let i = 0; i < n; i++) { const t0 = .25 + i * .07, u = (age - t0) / 1.55; if (u < 0 || u > 1) continue; const T0 = scr[tg[i % tg.length]] || E0; if (!T0) continue;
      const up = i % 2 ? 1 : -1, bay = [S0.x - fc * Lg * .12, S0.y + up * Lg * .14], out = [S0.x + fc * Lg * .25, S0.y + up * Lg * (.55 + tx5.rnd(2, i) * .3)], tgt = [T0.x - fc * Lg * .1, T0.y + (tx5.rnd(4, i) - .5) * Lg * .35], away = [T0.x + fc * Lg * (.9 + tx5.rnd(6, i)), T0.y - up * Lg * (.5 + tx5.rnd(8, i) * .4)];
      const pt = s => s < .62 ? tx5.bez(bay, out, [tgt[0] - fc * Lg * .6, tgt[1]], tgt, s / .62) : tx5.bez(tgt, [tgt[0] + fc * Lg * .4, tgt[1]], away, away, (s - .62) / .38);
      const [x, y] = pt(u), [x0, y0] = pt(Math.max(0, u - .01)), an = Math.atan2(y - y0, x - x0), fade = u > .85 ? (1 - u) / .15 : u < .05 ? u / .05 : 1;
      if (!lo) { ctx.globalAlpha = .55 * fade; ctx.strokeStyle = "rgba(110,190,255,1)"; ctx.lineWidth = 1.4 * d; ctx.beginPath(); for (let k = 0; k <= 8; k++) { const [tx, ty] = pt(Math.max(0, u - k * .012)); k ? ctx.lineTo(tx, ty) : ctx.moveTo(tx, ty); } ctx.stroke(); } // engine trail
      tx5.glow(ctx, x - Math.cos(an) * fs * .8, y - Math.sin(an) * fs * .8, fs * 1.3, "#5fc8ff", fade);
      ctx.save(); ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = fade; ctx.translate(x, y); ctx.rotate(an); const g = ctx.createLinearGradient(-fs, -fs, fs, fs); g.addColorStop(0, "#c9ced8"); g.addColorStop(.5, "#ffffff"); g.addColorStop(1, "#9aa2b0");
      ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(fs * 1.1, 0); ctx.lineTo(-fs * .7, -fs * .62); ctx.lineTo(-fs * .35, 0); ctx.lineTo(-fs * .7, fs * .62); ctx.closePath(); ctx.fill(); ctx.strokeStyle = "#ffcf5a"; ctx.lineWidth = Math.max(.8, .9 * d); ctx.stroke(); ctx.restore(); // a gold-trimmed strike fighter
      if (u > .45 && u < .66) { const k2 = ((u - .45) * 40 + i) % 1; tx5.beam(ctx, x, y, x + Math.cos(an) * Lg * .5 * k2 + Math.cos(an) * fs, y + Math.sin(an) * Lg * .5 * k2 + Math.sin(an) * fs, [[2.6 * d, "90,180,255", .6], [1 * d, "255,255,255", 1]], 1);
        tx5.star(ctx, T0.x + (tx5.rnd(i, Math.floor(u * 50)) - .5) * Lg * .3, T0.y + (tx5.rnd(i + 3, Math.floor(u * 50)) - .5) * Lg * .2, 7 * d, "#9fdcff", .8); } } }, // strafing run
  /* ---- Eclipse Harbinger: the Eclipse Pulse ---- */
  HP(ctx, b, m, age, S0, E0, fc, Lg, d, lo, T) { const CH = .42, TR = .5, F = [S0.x + fc * Lg * .58, S0.y], arms = [];
    for (let i = 0; i < 6; i++) { const a = i / 6 * TAU + T * .9; arms.push([S0.x + Math.cos(a) * Lg * .36, S0.y + Math.sin(a) * Lg * .22]); }
    const reac = .6 + .4 * Math.sin(age * 30); tx5.glow(ctx, S0.x, S0.y, Lg * .28 * reac, "#3dff9a", age < CH + .1 ? .8 : .4);
    if (age < CH + .08) { const k = Math.min(1, age / CH);
      arms.forEach(([x, y], i) => { const col = i % 2 ? "176,107,255" : "61,255,154"; tx5.beam(ctx, x, y, F[0], F[1], [[Lg * .02 * k + d, col, .5], [Lg * .006 * k + .6 * d, "255,255,255", .9]], k); tx5.glow(ctx, x, y, Lg * .05, i % 2 ? "#b06bff" : "#3dff9a", k); });
      const r = Lg * .09 * k; tx5.glow(ctx, F[0], F[1], r * 3.2, "#3dff9a", k); ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = .96; ctx.fillStyle = "#000"; ctx.beginPath(); ctx.arc(F[0], F[1], r, 0, TAU); ctx.fill(); ctx.globalCompositeOperation = "lighter";
      ctx.globalAlpha = k; ctx.strokeStyle = "#c8ffe0"; ctx.lineWidth = 1.3 * d; ctx.beginPath(); ctx.arc(F[0], F[1], r, 0, TAU); ctx.stroke(); return; }
    if (!E0) return; const u = (age - CH) / TR;
    if (u < 1) { const e = tx5.ease(u), x = F[0] + (E0.x - F[0]) * e, y = F[1] + (E0.y - F[1]) * e - Math.sin(e * Math.PI) * Lg * .25, r = Lg * .1;
      for (let j = 1; j <= (lo ? 2 : 5); j++) { const e2 = Math.max(0, e - j * .06), x2 = F[0] + (E0.x - F[0]) * e2, y2 = F[1] + (E0.y - F[1]) * e2 - Math.sin(e2 * Math.PI) * Lg * .25; tx5.glow(ctx, x2, y2, r * (1.6 - j * .15), "#b06bff", .45 - j * .07); ctx.globalAlpha = .4 - j * .06; ctx.strokeStyle = "#3dff9a"; ctx.lineWidth = d; ctx.beginPath(); ctx.ellipse(x2, y2, r * (1 + j * .35), r * (1 + j * .35) * .7, 0, 0, TAU); ctx.stroke(); }
      tx5.glow(ctx, x, y, r * 3.4, "#3dff9a", .95); ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = .97; ctx.fillStyle = "#000"; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.fill(); ctx.globalCompositeOperation = "lighter";
      ctx.globalAlpha = 1; ctx.strokeStyle = "#e6fff0"; ctx.lineWidth = 1.6 * d; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.stroke(); const da = age * 9; tx5.star(ctx, x + Math.cos(da) * r, y + Math.sin(da) * r, r * 1.3, "#d8ffe8", 1); return; } // the diamond-ring glint on the eclipse's rim
    const k = (u - 1) * TR / .5; if (k > 1) return; if (!m.hit) { m.hit = 1; b.shake = Math.max(b.shake || 0, 9 * d); b.flash = Math.max(b.flash || 0, .25); }
    if (k < .18) { const c = k / .18; ctx.globalAlpha = 1 - c; ctx.strokeStyle = "#3dff9a"; ctx.lineWidth = 3 * d; ctx.beginPath(); ctx.ellipse(E0.x, E0.y, Lg * .6 * (1 - c), Lg * .4 * (1 - c), 0, 0, TAU); ctx.stroke(); tx5.glow(ctx, E0.x, E0.y, Lg * .2, "#3dff9a", c); return; } // the implosion
    const c = (k - .18) / .82, a = 1 - c; tx5.glow(ctx, E0.x, E0.y, Lg * (.3 + .5 * c), "#3dff9a", a); tx5.glow(ctx, E0.x, E0.y, Lg * .18 * (1 - c * .5), "#ffffff", a); tx5.flare(ctx, E0.x, E0.y, Lg * .9 * a + Lg * .2, "#9affc8", a * .8);
    if (!lo) for (let i = 0; i < 7; i++) { const an = tx5.rnd(m.seed || 9, i) * TAU, R = Lg * (.4 + .5 * c) * (.6 + tx5.rnd(4, i) * .5); tx5.bolt(ctx, E0.x, E0.y, E0.x + Math.cos(an) * R, E0.y + Math.sin(an) * R * .7, 7, R * .12, i * 3.1 + Math.floor(age * 30), "#c890ff", 1.6 * d, a); }
    ctx.globalAlpha = a; ctx.strokeStyle = "#b06bff"; ctx.lineWidth = 2.4 * d * a; ctx.beginPath(); ctx.ellipse(E0.x, E0.y, Lg * 1.1 * c, Lg * .7 * c, 0, 0, TAU); ctx.stroke(); },
  /* ---- Eclipse Harbinger: the Neural Swarm ---- */
  HS(ctx, b, m, age, S0, E0, fc, Lg, d, lo, T, scr) { const tg = m.tg || (m.tg = tx5.foes(b, m, scr, E0 || S0, 6)); if (!tg.length) { if (!E0) return; tg.push(m.e); } const n = lo ? 6 : 16, ds = Math.max(6.5 * d, Lg * .05), P = [];
    tx5.glow(ctx, S0.x, S0.y, Lg * .3 * (age < .5 ? 1 : Math.max(0, 1.5 - age)), "#3dff9a", .7);
    for (let i = 0; i < n; i++) { const t0 = i * .045, u = (age - t0) / 1.25; if (u < 0 || u > 1.25) { P.push(null); continue; } const T0 = scr[tg[i % tg.length]]; if (!T0) { P.push(null); continue; }
      if (u > 1) { const c = (u - 1) / .25; tx5.glow(ctx, T0.x + (tx5.rnd(i, 2) - .5) * Lg * .2, T0.y + (tx5.rnd(i, 3) - .5) * Lg * .14, Lg * .12 * (.5 + c), "#3dff9a", 1 - c); tx5.glow(ctx, T0.x + (tx5.rnd(i, 2) - .5) * Lg * .2, T0.y + (tx5.rnd(i, 3) - .5) * Lg * .14, Lg * .05, "#ffffff", 1 - c); P.push(null); continue; } // each drone bursts on its target
      const a0 = tx5.rnd(m.seed || 5, i) * TAU, p0 = [S0.x, S0.y], p1 = [S0.x + Math.cos(a0) * Lg * .9, S0.y + Math.sin(a0) * Lg * .6], tp = [T0.x + (tx5.rnd(i, 2) - .5) * Lg * .2, T0.y + (tx5.rnd(i, 3) - .5) * Lg * .14], p2 = [tp[0] - fc * Lg * .5, tp[1] + (tx5.rnd(i, 7) - .5) * Lg * .8];
      const e = u * u * (3 - 2 * u), [bx0, by0] = tx5.bez(p0, p1, p2, tp, e), wob = Math.sin(u * 22 + i) * Lg * .04 * (1 - u), x = bx0 + wob, y = by0 + Math.cos(u * 17 + i * 2) * Lg * .03 * (1 - u), [xa, ya] = tx5.bez(p0, p1, p2, tp, Math.max(0, e - .02)), an = Math.atan2(y - ya, x - xa);
      P.push([x, y]); if (!lo) { ctx.globalAlpha = .5; ctx.strokeStyle = "rgba(176,107,255,1)"; ctx.lineWidth = 1.2 * d; ctx.beginPath(); for (let k = 0; k <= 6; k++) { const [tx, ty] = tx5.bez(p0, p1, p2, tp, Math.max(0, e - k * .018)); k ? ctx.lineTo(tx, ty) : ctx.moveTo(tx, ty); } ctx.stroke(); }
      ctx.save(); ctx.globalCompositeOperation = "source-over"; ctx.translate(x, y); ctx.rotate(an); ctx.fillStyle = "#0b0f0d"; ctx.strokeStyle = "#3dff9a"; ctx.lineWidth = Math.max(.7, .8 * d); ctx.beginPath(); ctx.moveTo(ds * 1.2, 0); ctx.lineTo(-ds * .6, -ds * .8); ctx.lineTo(-ds * .2, 0); ctx.lineTo(-ds * .6, ds * .8); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore();
      const fl = .5 + .5 * Math.sin(age * 70 + i * 2); tx5.glow(ctx, x + Math.cos(an) * ds * .35, y + Math.sin(an) * ds * .35, ds * 1.2, "#3dff9a", .9); tx5.glow(ctx, x - Math.cos(an) * ds * .5, y - Math.sin(an) * ds * .5, ds * 1.4 * fl, "#b06bff", .6); } // the green eye, the violet wing flicker
    if (!lo) { ctx.strokeStyle = "rgba(61,255,154,1)"; ctx.lineWidth = .8 * d; for (let i = 0; i + 1 < P.length; i++) { const A = P[i], B = P[i + 1]; if (!A || !B) continue; const L = Math.hypot(B[0] - A[0], B[1] - A[1]); if (L > Lg * 1.2) continue; ctx.globalAlpha = .35 * (1 - L / (Lg * 1.2)); ctx.beginPath(); ctx.moveTo(A[0], A[1]); ctx.lineTo(B[0], B[1]); ctx.stroke(); } } }, // the neural web
  /* ---- Eclipse Harbinger: arm-tip lasers converging from all six arms ---- */
  HT(ctx, b, m, age, S0, E0, fc, Lg, d, lo, T) { if (!E0) return; const k = age / .42, a = k < .15 ? k / .15 : 1 - Math.max(0, (k - .5) / .5);
    for (let i = 0; i < 6; i++) { const an = i / 6 * TAU + T * .9, x = S0.x + Math.cos(an) * Lg * .36, y = S0.y + Math.sin(an) * Lg * .22, col = i % 2 ? "176,107,255" : "61,255,154";
      tx5.beam(ctx, x, y, E0.x, E0.y, [[Lg * .018 + d, col, .55], [Lg * .005 + .5 * d, "255,255,255", 1]], a); tx5.glow(ctx, x, y, Lg * .05, i % 2 ? "#b06bff" : "#3dff9a", a); }
    tx5.glow(ctx, E0.x, E0.y, Lg * .2, "#9affc8", a); tx5.flare(ctx, E0.x, E0.y, Lg * .4 * a, "#d0a0ff", a * .8); } };
