/* v860 the Swarm comes first and fights like turrets (owner: "it should have the drone swarm first, the swarm should attack ships like
   turrets first and then fly into them and explode red sparkle and then the other firing animations as long as its drones are out first").
   0-.2 sixteen drones pour from its hub and fan out; .2-.62 each pair holds station off its target (up to eight) and fires red bolts into
   it like a turret; .62-.8 they dive in; then each bursts in a shower of red sparks. It opens every cycle of the Commander's attacks. */
function cntEterSwarm(ctx, b, m, u, S0, E0, Lg, d, T, scr, hit, rs) { const tg = m.fo || (m.fo = [m.e].concat(kFoes(b, m.s).filter(j => j !== m.e && scr[j]).sort((x, y) => (bLen(b.Q[y].k) || 1) - (bLen(b.Q[x].k) || 1))).slice(0, 8));
  if (u < .2) { const r = Lg * (.1 + .4 * u / .2); ctx.globalAlpha = .7; ctx.drawImage(rs, S0.x - r, S0.y - r, r * 2, r * 2); }
  for (let j = 0; j < tg.length * 2; j++) { const P = scr[tg[j >> 1]]; if (!P) continue; const sd = j % 2 ? 1 : -1, gE = b.geo && b.geo[tg[j >> 1]], LE = gE ? gE.L : 30;
    const away = P.x < S0.x ? 1 : -1, st = { x: P.x + away * LE * (1.1 + .25 * (j % 3)), y: P.y + sd * LE * (.55 + .2 * ((j >> 1) % 2)) }; /* its station off the target */
    const a0 = (j / (tg.length * 2) - .5) * 2.6 + (P.x < S0.x ? Math.PI : 0), c0 = { x: S0.x + Math.cos(a0) * Lg * .9, y: S0.y + Math.sin(a0) * Lg * .6 };
    let h, tl;
    const bz = (A, C, B, q) => ({ x: (1 - q) * (1 - q) * A.x + 2 * (1 - q) * q * C.x + q * q * B.x, y: (1 - q) * (1 - q) * A.y + 2 * (1 - q) * q * C.y + q * q * B.y });
    if (u < .2) { const k = clamp(u / .2 - j * .02, 0, 1); h = bz(S0, c0, st, k); tl = bz(S0, c0, st, Math.max(0, k - .1)); }
    else if (u < .62) { const w = Math.sin(T * 3 + j) * 4 * d; h = { x: st.x, y: st.y + w }; tl = { x: st.x + away * 6 * d, y: h.y };
      const f = ((u - .2) * 40 + j * .37) % 1; if (f < .45) { const k = f / .45, x = h.x + (P.x - h.x) * k, y = h.y + (P.y - h.y) * k; ctx.globalAlpha = 1; ctx.strokeStyle = `rgba(${CNT_RED},1)`; ctx.lineWidth = 2 * d; ctx.beginPath(); ctx.moveTo(x - (P.x - h.x) * .12, y - (P.y - h.y) * .12); ctx.lineTo(x, y); ctx.stroke(); } /* firing like a turret */
      if (u > .26) hit(m, E0.x, E0.y, false); }
    else if (u < .8) { const k = (u - .62) / .18; h = { x: st.x + (P.x - st.x) * k * k, y: st.y + (P.y - st.y) * k * k }; tl = { x: st.x + (P.x - st.x) * Math.max(0, k - .2) ** 2, y: st.y + (P.y - st.y) * Math.max(0, k - .2) ** 2 }; } /* the dive */
    if (h) { ctx.globalAlpha = .75; ctx.strokeStyle = `rgba(${CNT_RED},1)`; ctx.lineWidth = 2.2 * d; ctx.beginPath(); ctx.moveTo(tl.x, tl.y); ctx.lineTo(h.x, h.y); ctx.stroke();
      const an = u >= .2 && u < .62 ? Math.atan2(P.y - h.y, P.x - h.x) : Math.atan2(h.y - tl.y, h.x - tl.x); ctx.save(); ctx.translate(h.x, h.y); ctx.rotate(an); ctx.globalAlpha = 1; ctx.fillStyle = "rgba(255,210,210,1)"; ctx.beginPath(); ctx.moveTo(6 * d, 0); ctx.lineTo(-4 * d, 3.2 * d); ctx.lineTo(-4 * d, -3.2 * d); ctx.closePath(); ctx.fill(); ctx.restore(); ctx.drawImage(rs, h.x - 9 * d, h.y - 9 * d, 18 * d, 18 * d); }
    else if (u >= .8) { const kk = (u - .8) / .2; hit(m, E0.x, E0.y, true); const R = (8 + 26 * kk) * d; ctx.globalAlpha = (1 - kk) * .9; ctx.drawImage(rs, P.x - R, P.y - R, R * 2, R * 2);
      for (let s2 = 0; s2 < 10; s2++) { const a = s2 * .628 + j, dd = (6 + 40 * kk) * d * (.6 + .4 * Math.sin(s2 * 3.1 + j)), x = P.x + Math.cos(a) * dd, y = P.y + Math.sin(a) * dd * .7 + kk * kk * 10 * d; ctx.globalAlpha = (1 - kk) * ((T * 20 + s2) % 2 < 1 ? 1 : .4); ctx.fillStyle = s2 % 3 ? `rgba(${CNT_RED},1)` : "rgba(255,230,230,1)"; ctx.fillRect(x - d, y - d, 2.4 * d, 2.4 * d); } } } } /* a burst of red sparks */
