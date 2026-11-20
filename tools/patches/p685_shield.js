/* v685 reactive boss shields: every shot a boss's shield absorbs ripples where it lands (a cluster of hexes) and lights the stretch of the
   bubble's rim facing the shot; the whole bubble shimmers while the hits keep coming. The shield is real in the simulator (it comes back
   every 12 s, v683), so the ripples come in bursts after each pulse and stop when the shield is drained and the hull takes the fire. */
function bShHit(b, x, y, t, sh) { const H = b.bShH || (b.bShH = []); if (H.length && t - H[H.length - 1].t < 45) return; H.push({ x, y, t, s: sh > 0 ? 1 : .6 }); if (H.length > 28) H.shift(); }
function bShHits(ctx, b, W, H, d, t) { const L = b.bShH; if (!L || !L.length || !b.scC) return; const B = b.wbBox || { cx: b.scC.x, cy: b.scC.y, aw: W * .6, ah: W * .3 }, rx = B.aw * .5, ry = Math.max(B.ah * .55, rx * .45);
  const col = b.r.sbk && SBW[b.r.sbk] ? SBW[b.r.sbk].col : b.r.wb && WB[b.r.wb] ? WB[b.r.wb].col : b.r.mon || b.r.mim ? "#b0ff7a" : "#7ad8ff", LIFE = 560; let heat = 0;
  ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.lineCap = "round";
  for (const h of L) { const u = (t - h.t) / LIFE; if (u < 0 || u > 1) continue; heat += (1 - u) * h.s; const a = Math.atan2((h.y - B.cy) / ry, (h.x - B.cx) / rx), px = B.cx + Math.cos(a) * rx, py = B.cy + Math.sin(a) * ry, f = 1 - u;
    ctx.globalAlpha = .85 * f * h.s; ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2.2 * d; ctx.beginPath(); ctx.ellipse(B.cx, B.cy, rx, ry, 0, a - .32 * (.5 + u), a + .32 * (.5 + u)); ctx.stroke(); /* the rim facing the shot */
    ctx.globalAlpha = .5 * f * h.s; ctx.strokeStyle = col; ctx.lineWidth = 7 * d; ctx.stroke();
    const hs = (7 + 10 * u) * d; ctx.lineWidth = 1.4 * d; ctx.strokeStyle = col; for (let j = 0; j < 7; j++) { const aa = j * Math.PI / 3, cx = px + (j ? Math.cos(aa) * hs * 1.5 : 0), cy = py + (j ? Math.sin(aa) * hs * 1.5 : 0); ctx.globalAlpha = (j ? .45 : .9) * f * h.s; ctx.beginPath(); for (let k = 0; k <= 6; k++) { const q = k * Math.PI / 3 + Math.PI / 6; ctx[k ? "lineTo" : "moveTo"](cx + Math.cos(q) * hs * .8, cy + Math.sin(q) * hs * .8); } ctx.stroke(); } /* the hex ripple */
    ctx.globalAlpha = .7 * f * f * h.s; ctx.drawImage(glowSprite(col), px - 18 * d, py - 18 * d, 36 * d, 36 * d); }
  if (heat > .05) { ctx.globalAlpha = Math.min(.35, heat * .08); ctx.strokeStyle = col; ctx.lineWidth = 3 * d; ctx.beginPath(); ctx.ellipse(B.cx, B.cy, rx, ry, 0, 0, TAU); ctx.stroke(); } /* the bubble shimmers under sustained fire */
  ctx.restore(); ctx.globalAlpha = 1; }
