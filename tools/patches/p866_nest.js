/* v866 the Abyssal Breach Nest remastered (owner: "can we remaster and revise the abyssal nests, it has no glow like the rest of the crabs
   and no special effects, we cant leave any of these ... without their own unique attacks and animations"). Its new sculpt (tools/sculpt/
   crc_nest.py) has a glow layer; here its life in battle, drawn in the battlefield's own frame round its squad:
   - the rift: a whirlpool of teal light turning in it round a burning eye, bubbles rising off its egg clutches, the eggs breathing, a few
     hatchlings scuttling round its foot, a haze of sea-light over it;
   - its own three attacks, in turn, each with a wind-up (the rift flares): Hatchling Swarm (a brood of glowing hatchlings leaps in arcs
     onto a ship and bursts on it), Abyssal Geyser (a column of abyssal water erupts under a ship), Riptide (a stream of dark water from
     the eye to a ship, a whirlpool forming round it, tightening, then bursting);
   - when it falls: the rift collapses in a ring of water and its light goes out. */
const NEST_C = "70,235,230", NEST_D = { nHatch: 1.5, nGeyser: 1.5, nRip: 1.7 }, NEST_A = ["nHatch", "nGeyser", "nRip"];
const nestRift = (P, Lg) => ({ x: P.x, y: P.y - Lg * .13, rx: Lg * .17, ry: Lg * .22 }); // where its rift sits on the sprite
function nestAtkAdd(b, v) { const q = b.Q[v.s]; if (!q || q.k !== "cnest" || v.e == null || v.e < 0) return; const L = b.nsA || (b.nsA = []), last = b.nsT || (b.nsT = {});
  if (last[v.s] != null && v.t - last[v.s] < 2.2) return; last[v.s] = v.t; const n = (b.nsN = (b.nsN || 0) + 1); L.push({ s: v.s, e: v.e, t0: v.t, a: NEST_A[(n - 1) % 3], seed: (v.s * 11 + n) % 13 }); if (L.length > 12) L.shift(); }
function nestFx(ctx, b, scr, T, d, lo) { if (!b || !b.Q) return; ctx.save(); ctx.globalCompositeOperation = "lighter"; const ws = glowSprite(`rgba(${NEST_C},1)`), wh = glowSprite("#ffffff");
  for (let i = 0; i < b.Q.length; i++) { const q = b.Q[i]; if (!q || q.k !== "cnest") continue; const P = scr[i], g = b.geo && b.geo[i], Lg = g ? g.L : 90; if (!P) continue;
    const alive = b.n[i] > 0, D = b.nsDie || (b.nsDie = {});
    if (!alive) { if (D[i] == null) D[i] = T; const k = (T - D[i]) / 1.6; if (k < 1) { const R = nestRift(P, Lg); ctx.globalAlpha = (1 - k) * .8; ctx.strokeStyle = `rgba(${NEST_C},1)`; ctx.lineWidth = 3 * d * (1 - k); ctx.beginPath(); ctx.ellipse(R.x, R.y + Lg * .3, Lg * (.3 + k), Lg * (.1 + k * .3), 0, 0, TAU); ctx.stroke(); ctx.globalAlpha = (1 - k) * .9; const s = R.rx * 2.5 * (1 - k); ctx.drawImage(ws, R.x - s, R.y - s, s * 2, s * 2); } continue; }
    const R = nestRift(P, Lg), A = (b.nsA || []).find(m => m.s === i && T - m.t0 < NEST_D[m.a] && T >= m.t0), wind = A ? (T - A.t0 < .45 ? (T - A.t0) / .45 : Math.max(0, 1 - (T - A.t0 - .45) / .6)) : 0, br = .75 + .25 * Math.sin(T * 2.2 + i);
    // the haze over it, and the rift's light
    ctx.globalAlpha = .05 + .03 * br; ctx.drawImage(ws, P.x - Lg * .7, P.y - Lg * .55, Lg * 1.4, Lg * 1.1);
    ctx.globalAlpha = (.2 + .14 * br + wind * .45); ctx.drawImage(ws, R.x - R.rx * 1.7, R.y - R.ry * 1.6, R.rx * 3.4, R.ry * 3.2);
    // the whirlpool: spiral arms turning in the rift
    if (!lo) { ctx.lineCap = "round"; for (let j = 0; j < 4; j++) { const a0 = T * (1.6 + wind * 3) + j * TAU / 4; ctx.strokeStyle = `rgba(${j % 2 ? "160,255,250" : NEST_C},1)`; ctx.globalAlpha = .55 + wind * .3; ctx.lineWidth = Math.max(1, 1.6 * d);
        ctx.beginPath(); for (let s = 0; s <= 14; s++) { const u = s / 14, rr = 1 - u * .85, a = a0 + u * 3.4, x = R.x + Math.cos(a) * R.rx * rr, y = R.y + Math.sin(a) * R.ry * rr; s ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke(); } }
    const es = R.rx * (.45 + .12 * Math.sin(T * 3.1) + wind * .5); ctx.globalAlpha = .75; ctx.drawImage(wh, R.x - es * .5, R.y - es * .6, es, es * 1.2); ctx.drawImage(ws, R.x - es, R.y - es, es * 2, es * 2); // the eye
    // the eggs breathing at its foot, bubbles rising off them
    for (let j = 0; j < 7; j++) { const a = j / 7 * TAU + .5, ex = P.x + Math.cos(a) * Lg * .26, ey = P.y + Lg * .3 + Math.sin(a) * Lg * .05, p2 = .5 + .5 * Math.sin(T * 2.6 + j * 1.7), s = Lg * (.035 + .02 * p2);
      ctx.globalAlpha = .35 + .4 * p2; ctx.drawImage(ws, ex - s * 2, ey - s * 2, s * 4, s * 4);
      if (!lo) { const k = (T * .5 + j * .37) % 1, bx = ex + Math.sin(k * 9 + j) * Lg * .02, by = ey - k * Lg * .55, r = Math.max(1.2 * d, Lg * .012) * (.6 + k); ctx.globalAlpha = Math.sin(Math.PI * k) * .6; ctx.strokeStyle = `rgba(${NEST_C},1)`; ctx.lineWidth = Math.max(1, .8 * d); ctx.beginPath(); ctx.arc(bx, by, r, 0, TAU); ctx.stroke(); } }
    // hatchlings scuttling round its foot
    if (!lo) for (let j = 0; j < 4; j++) { const a = T * (.35 + j * .07) * (j % 2 ? 1 : -1) + j * 1.6, hx = P.x + Math.cos(a) * Lg * .36, hy = P.y + Lg * .34 + Math.sin(a) * Lg * .07, s = Lg * .022;
      ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = .9; ctx.fillStyle = "#130a18"; ctx.beginPath(); ctx.ellipse(hx, hy, s * 1.3, s * .8, 0, 0, TAU); ctx.fill();
      ctx.strokeStyle = "#2a1630"; ctx.lineWidth = Math.max(1, d * .8); for (const sd of [-1, 1]) for (let l = 0; l < 2; l++) { const ph = Math.sin(T * 14 + j + l * 2) * s * .4; ctx.beginPath(); ctx.moveTo(hx + sd * s * .6, hy); ctx.lineTo(hx + sd * s * 1.7, hy + s * .5 + ph); ctx.stroke(); }
      ctx.globalCompositeOperation = "lighter"; ctx.globalAlpha = .9; ctx.drawImage(ws, hx - s * .8, hy - s * .9, s * 1.6, s * 1.6); } }
  ctx.restore(); }
function nestAtkDraw(ctx, b, scr, T, W, H, d, t) { const A = b.nsA; if (!A || !A.length) return; ctx.save(); ctx.globalCompositeOperation = "lighter"; const ws = glowSprite(`rgba(${NEST_C},1)`), wh = glowSprite("#ffffff");
  for (const m of A) { const dur = NEST_D[m.a], u = (T - m.t0) / dur; if (u < 0 || u > 1) continue; const S0 = scr[m.s], E0 = scr[m.e]; if (!S0 || !E0 || !(b.n[m.s] > 0)) continue;
    const g = b.geo && b.geo[m.s], Lg = g ? g.L : 90, gE = b.geo && b.geo[m.e], LE = gE ? gE.L : 30, R = nestRift(S0, Lg), w = .3; // the first 0.3 of each is its wind-up (the rift flaring)
    if (!m.snd && u > w) { m.snd = 1; try { mimSfx(m.a === "nGeyser" ? "omega" : m.a === "nRip" ? "hum" : "whip", clamp(S0.x / W * 2 - 1, -1, 1)); } catch (e) {} }
    if (u < w) { const k = u / w; ctx.globalAlpha = .6 * k; const s = R.rx * (1.5 + k); ctx.drawImage(ws, R.x - s, R.y - s, s * 2, s * 2); continue; }
    const v = (u - w) / (1 - w);
    if (m.a === "nHatch") { // a brood leaps in arcs from its foot onto the ship and bursts on it
      for (let j = 0; j < 7; j++) { const st = j * .06, k = clamp((v - st) / .55, 0, 1); if (k <= 0) continue; const x0 = S0.x + (j - 3) * Lg * .06, y0 = S0.y + Lg * .3, tx = E0.x + Math.sin(j * 2.1 + m.seed) * LE * .3, ty = E0.y + Math.cos(j * 1.7) * LE * .15;
        if (k < 1) { const x = x0 + (tx - x0) * k, y = y0 + (ty - y0) * k - Math.sin(Math.PI * k) * (Lg * .35 + Math.abs(tx - x0) * .2), s = Lg * .03; ctx.globalAlpha = .95; ctx.drawImage(ws, x - s * 2, y - s * 2, s * 4, s * 4); ctx.drawImage(wh, x - s * .6, y - s * .6, s * 1.2, s * 1.2); }
        else { const k2 = clamp((v - st - .55) / .3, 0, 1); if (k2 < 1) { const r = LE * (.12 + .35 * k2); ctx.globalAlpha = (1 - k2) * .9; ctx.drawImage(ws, tx - r, ty - r, r * 2, r * 2); ctx.strokeStyle = `rgba(${NEST_C},1)`; ctx.lineWidth = 2 * d * (1 - k2); ctx.beginPath(); ctx.arc(tx, ty, r * .8, 0, TAU); ctx.stroke(); } } }
      if (v > .55 && !m.hit) { m.hit = 1; b.shake = Math.max(b.shake || 0, 5 * d); } }
    else if (m.a === "nGeyser") { // a column of abyssal water erupts under the ship
      const rise = Math.min(1, v / .35), fall = v > .7 ? 1 - (v - .7) / .3 : 1, top = E0.y - LE * 2.4 * rise, x = E0.x, wd = LE * .45;
      ctx.globalAlpha = .5 * fall; ctx.strokeStyle = `rgba(${NEST_C},1)`; ctx.lineWidth = 2 * d; ctx.beginPath(); ctx.ellipse(x, E0.y + LE * .35, LE * (.6 + rise * .5), LE * (.18 + rise * .1), 0, 0, TAU); ctx.stroke(); // the swell under it
      const gr = ctx.createLinearGradient(0, E0.y + LE * .4, 0, top); gr.addColorStop(0, `rgba(${NEST_C},${.8 * fall})`); gr.addColorStop(.7, `rgba(170,255,250,${.55 * fall})`); gr.addColorStop(1, "rgba(170,255,250,0)"); ctx.globalAlpha = 1; ctx.fillStyle = gr;
      ctx.beginPath(); ctx.moveTo(x - wd, E0.y + LE * .4); for (let s = 0; s <= 8; s++) { const yy = E0.y + LE * .4 - (E0.y + LE * .4 - top) * s / 8; ctx.lineTo(x - wd * (1 - s / 12) + Math.sin(T * 20 + s) * 2 * d, yy); } for (let s = 8; s >= 0; s--) { const yy = E0.y + LE * .4 - (E0.y + LE * .4 - top) * s / 8; ctx.lineTo(x + wd * (1 - s / 12) + Math.cos(T * 18 + s) * 2 * d, yy); } ctx.closePath(); ctx.fill();
      for (let s = 0; s < 10; s++) { const k = (v * 1.6 + s * .1) % 1, ang = -Math.PI / 2 + (s - 4.5) * .22, rr = LE * (.4 + k * 1.6), px = x + Math.cos(ang) * rr, py = top + LE * .3 + Math.sin(ang) * rr * -.2 + k * k * LE * 1.2, z = Math.max(1.4 * d, LE * .05); ctx.globalAlpha = (1 - k) * fall; ctx.drawImage(ws, px - z * 2, py - z * 2, z * 4, z * 4); } // spray
      if (v > .3 && !m.hit) { m.hit = 1; b.shake = Math.max(b.shake || 0, 9 * d); b.flash = Math.max(b.flash || 0, .05); } }
    else { // Riptide: a stream of dark water from the eye, a whirlpool round the ship tightening, then bursting
      const k = Math.min(1, v / .3), x1 = R.x + (E0.x - R.x) * k, y1 = R.y + (E0.y - R.y) * k, fade = v > .8 ? 1 - (v - .8) / .2 : 1;
      for (const [lw, a, col] of [[9, .18, NEST_C], [4, .45, NEST_C], [1.5, .9, "220,255,255"]]) { ctx.globalAlpha = a * fade; ctx.strokeStyle = `rgba(${col},1)`; ctx.lineWidth = lw * d; ctx.beginPath(); for (let s = 0; s <= 16; s++) { const u2 = s / 16, x = R.x + (x1 - R.x) * u2, y = R.y + (y1 - R.y) * u2 + Math.sin(u2 * 12 - T * 14) * 4 * d * Math.sin(Math.PI * u2); s ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.stroke(); }
      if (v > .3) { const k2 = (v - .3) / .7, Rr = LE * (1.3 - .8 * Math.min(1, k2 * 1.3)); ctx.strokeStyle = `rgba(${NEST_C},1)`; for (let j = 0; j < 3; j++) { ctx.globalAlpha = (.75 - j * .2) * fade; ctx.lineWidth = (2.5 - j * .6) * d; ctx.beginPath(); ctx.ellipse(E0.x, E0.y, Rr * (1 - j * .2), Rr * .45 * (1 - j * .2), 0, T * (6 + j * 2) + j, T * (6 + j * 2) + j + 4.4); ctx.stroke(); }
        if (k2 > .8) { const k3 = (k2 - .8) / .2, r = LE * (.3 + 1.2 * k3); ctx.globalAlpha = (1 - k3) * .9; ctx.drawImage(ws, E0.x - r, E0.y - r, r * 2, r * 2); if (!m.hit) { m.hit = 1; b.shake = Math.max(b.shake || 0, 7 * d); } } } } }
  ctx.restore(); }
