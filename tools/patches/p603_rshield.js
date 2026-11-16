/* ---------- v603 reactive shields (owner: "remove the numbers and the critical hits and replace them with reactive shielding effects;
   all ships should have a reactive shield animation and a shield break animation, especially for boss fights"). The floating
   numbers, CRITICAL, kill counts and SHIELDS DOWN are gone. Every hit on a formation's shield lights its barrier: a rim-lit bubble,
   a honeycomb of hex cells that flares from the point of impact outward, ripples crossing the bubble and a flash where the shot
   struck (a critical hit strikes white-gold with a lens flare). The barrier's colour follows its real strength: blue when strong,
   violet when strained, red as it fails. When it fails it shatters: a flash, crackling arcs, shards of barrier flying outward and a
   shock ring. A boss's barrier is the whole hull's: it ripples across the colossus and its break is a cataclysm, with slow motion. */
function rs603Hit(b, i, x, y, sx, sy, crit, big, t) { try { if (b.lowFx) return; const L = b.rs603 || (b.rs603 = []); L.push({ i, t, a: Math.atan2(sy - y, sx - x), x, y, crit: !!crit, big: !!big }); const cap = b.Q.length > 60 ? 10 : 36; if (L.length > cap) L.splice(0, L.length - cap); } catch (e) {} }
function rs603Col(sv) { return sv > .5 ? "110,210,255" : sv > .2 ? "175,140,255" : "255,105,140"; }
/* where a formation's barrier is: a normal squadron's ellipse is recorded as it is drawn; the boss side shares one great barrier */
function rs603Geo(b, i, pos, W, H) { const q = b.Q[i]; if (!q) return null;
  if (b.superSide && q.side === b.superSide && b.scC) { const bx = b.wbBox, R = bx ? Math.min(bx.aw, bx.ah) * .42 : Math.min(W, H) * .5; let s = 0, n = 0; b.Q.forEach((q2, k) => { if (q2.side === b.superSide && b.n[k] > 0 && pos[k]) { s += clamp(pos[k].sh, 0, 1); n++; } }); return [bx ? bx.cx : b.scC.x, bx ? bx.cy : b.scC.y, R, R * .92, n ? s / n : 0, 1]; }
  const g = (b.shG || [])[i]; return g ? [g[0], g[1], g[2], g[3], g[4], 0] : null; }
function rs603Draw(ctx, b, t, d, W, H, pos) { if (b.lowFx) { b.rs603 = []; return; }
  const L = (b.rs603 || []).filter(h => t - h.t < (h.crit ? 850 : 620)); b.rs603 = L; const busy = b.Q.length > 60;
  ctx.save(); ctx.globalCompositeOperation = "lighter";
  /* the boss's barrier breaking: when the whole side's shields fall */
  if (b.superSide && b.scC) { const g = rs603Geo(b, b.Q.findIndex(q => q.side === b.superSide), pos, W, H); if (g) { if (b.bsPv != null && b.bsPv > .1 && g[4] <= .02) { (b.brk603 = b.brk603 || []).push({ boss: 1, t, x: g[0], y: g[1], rx: g[2], ry: g[3], col: "120,255,170" }); b.slowUntil = Math.max(b.slowUntil || 0, t + 1500); b.shake = Math.max(b.shake || 0, 22 * d); b.flash = Math.max(b.flash || 0, .45); try { SFX.shield && SFX.shield(0); } catch (e) {} } b.bsPv = g[4]; } }
  const seen = {}; for (let n = L.length - 1; n >= 0; n--) { const h = L[n], g = rs603Geo(b, h.i, pos, W, H); if (!g) continue; const key = h.i + (g[5] ? "B" : ""); seen[key] = (seen[key] || 0) + 1; if (seen[key] > (g[5] ? 6 : busy ? 1 : 3)) continue;
    const [cx, cy, rx, ry, sv, boss] = g, life = h.crit ? 850 : 620, k = (t - h.t) / life, a = 1 - k, col = boss ? (sv > .5 ? "120,255,170" : sv > .2 ? "175,255,140" : "255,170,110") : rs603Col(sv);
    const th = Math.atan2(Math.sin(h.a) / ry, Math.cos(h.a) / rx), px = cx + Math.cos(th) * rx * .96, py = cy + Math.sin(th) * ry * .96;
    /* the rim-lit bubble */
    ctx.save(); ctx.translate(cx, cy); ctx.scale(1, ry / rx); const rg = ctx.createRadialGradient(0, 0, rx * .2, 0, 0, rx); rg.addColorStop(0, `rgba(${col},0)`); rg.addColorStop(.72, `rgba(${col},${(boss ? .05 : .06) * a})`); rg.addColorStop(.94, `rgba(${col},${(h.crit ? .45 : .3) * a})`); rg.addColorStop(1, `rgba(${col},0)`); ctx.fillStyle = rg; ctx.globalAlpha = 1; ctx.beginPath(); ctx.arc(0, 0, rx, 0, TAU); ctx.fill(); ctx.restore();
    /* inside the bubble: the hex cells flaring outward from the impact, and the ripples */
    ctx.save(); ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, 0, 0, TAU); ctx.clip();
    const hs = Math.max(4 * d, rx * (boss ? .055 : .12)), R = rx * (boss ? .7 : 1.1) * (.25 + .75 * Math.min(1, k * 1.6)), wave = R; ctx.lineWidth = Math.max(.6, (boss ? 1.3 : 1) * d);
    const cols = Math.ceil(R / (hs * 1.5)) + 1, rows = Math.ceil(R / (hs * 1.732)) + 1, gx0 = Math.round(px / (hs * 1.5)), gy0 = Math.round(py / (hs * 1.732)); let cnt = 0;
    for (let gx = gx0 - cols; gx <= gx0 + cols && cnt < (boss ? 70 : 34); gx++) for (let gy = gy0 - rows; gy <= gy0 + rows; gy++) { const hx = gx * hs * 1.5, hy = gy * hs * 1.732 + (gx & 1 ? hs * .866 : 0), dd = Math.hypot(hx - px, hy - py); if (dd > R) continue; const e = Math.pow((hx - cx) / rx, 2) + Math.pow((hy - cy) / ry, 2); if (e > 1) continue;
      const band = Math.max(0, 1 - Math.abs(dd - wave * .85) / (hs * 2.2)), I = (band * .9 + (1 - dd / R) * .35) * a * (.6 + .4 * Math.sqrt(e)); if (I < .05) continue; cnt++;
      ctx.globalAlpha = Math.min(1, I); ctx.strokeStyle = band > .8 ? "#e8fff6" : `rgb(${col})`; ctx.beginPath(); for (let v = 0; v < 6; v++) { const an = v / 6 * TAU, x = hx + Math.cos(an) * hs * .9, y = hy + Math.sin(an) * hs * .9; v ? ctx.lineTo(x, y) : ctx.moveTo(x, y); } ctx.closePath(); ctx.stroke(); if (band > .7) { ctx.globalAlpha = Math.min(.12, I * .12); ctx.fillStyle = `rgb(${col})`; ctx.fill(); } }
    for (const [f, w] of [[1, 2.2], [.55, 1.2]]) { const rr = rx * (boss ? .9 : 1.4) * k * f; ctx.globalAlpha = a * .7; ctx.strokeStyle = `rgba(${col},1)`; ctx.lineWidth = w * d; ctx.beginPath(); ctx.ellipse(px, py, rr, rr * .8, 0, 0, TAU); ctx.stroke(); }
    ctx.restore();
    /* the strike */
    const fr = (boss ? rx * .14 : rx * .32) * (h.crit ? 1.5 : 1) * (1 - k * .5); ctx.globalAlpha = a; ctx.drawImage(glowSprite(`rgba(${col},1)`), px - fr, py - fr, fr * 2, fr * 2); ctx.globalAlpha = a * (k < .3 ? 1 : 0); ctx.drawImage(glowSprite("#ffffff"), px - fr * .4, py - fr * .4, fr * .8, fr * .8);
    if (h.crit) { tx5.flare(ctx, px, py, rx * (boss ? .5 : 1.1) * a, "#ffe6a0", a); tx5.glow(ctx, px, py, fr * 1.4, "#ffd36b", a * .8); } }
  /* a barrier shattering */
  const B = (b.brk603 || []).filter(o => t - o.t < (o.boss ? 1600 : 900)); b.brk603 = B;
  for (const o of B) { const life = o.boss ? 1600 : 900, k = (t - o.t) / life, a = 1 - k, ek = 1 - Math.pow(1 - k, 3), N = o.boss ? (busy ? 26 : 48) : busy ? 8 : 18;
    if (k < .18) { ctx.save(); ctx.translate(o.x, o.y); ctx.scale(1, o.ry / o.rx); ctx.globalAlpha = 1 - k / .18; ctx.fillStyle = `rgba(${o.col},.35)`; ctx.beginPath(); ctx.arc(0, 0, o.rx, 0, TAU); ctx.fill(); ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3 * d; ctx.stroke(); ctx.restore(); } // the flash of the whole barrier
    if (k < .45) for (let j = 0; j < (o.boss ? 8 : 4); j++) { const a1 = tx5.rnd(o.t % 997, j) * TAU, a2 = a1 + 1 + tx5.rnd(o.t % 991, j + 5) * 2; tx5.bolt(ctx, o.x + Math.cos(a1) * o.rx, o.y + Math.sin(a1) * o.ry, o.x + Math.cos(a2) * o.rx * .6, o.y + Math.sin(a2) * o.ry * .6, 7, o.rx * .1, j * 3 + Math.floor(t / 40), "#ffffff", 1.4 * d, (1 - k / .45)); } // crackling arcs
    for (let j = 0; j < N; j++) { const an = tx5.rnd(o.t % 983, j) * TAU, sp = .9 + tx5.rnd(o.t % 977, j) * .9, r = (1 + ek * (o.boss ? .9 : 1.3) * sp), x = o.x + Math.cos(an) * o.rx * r, y = o.y + Math.sin(an) * o.ry * r + ek * ek * o.ry * .25, s = (o.boss ? o.rx * .07 : Math.max(4 * d, o.rx * .12)) * (1 - k * .4), rot = an + k * (3 + j % 4);
      ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.globalAlpha = a; ctx.fillStyle = `rgba(${o.col},.28)`; ctx.strokeStyle = j % 3 ? `rgb(${o.col})` : "#ffffff"; ctx.lineWidth = Math.max(.6, d); ctx.beginPath(); ctx.moveTo(s, 0); ctx.lineTo(-s * .6, -s * .55); ctx.lineTo(-s * .4, s * .7); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore(); } // shards of barrier
    ctx.globalAlpha = a; ctx.strokeStyle = `rgba(${o.col},1)`; ctx.lineWidth = (o.boss ? 5 : 2.5) * d * a; ctx.beginPath(); ctx.ellipse(o.x, o.y, o.rx * (1 + ek * (o.boss ? .8 : 1.2)), o.ry * (1 + ek * (o.boss ? .8 : 1.2)), 0, 0, TAU); ctx.stroke(); // the shock ring
    if (o.boss && k < .5) tx5.flare(ctx, o.x, o.y, o.rx * 2 * (1 - k * 2), "#c8ffe0", 1 - k * 2); }
  ctx.restore(); ctx.globalAlpha = 1; }
