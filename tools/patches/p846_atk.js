/* ---------- v846 Omega's structures remastered (owner: "upgrade and remaster the mimic neural node, neural nexus and the assimilation
   pylon ... what kind of unique attacks can we give them", then "build it all") ----------
   Neural Node  synapse : its brain flares, then branching nerve lightning leaps from ship to ship, static crawling over each one it hits.
   Neural Nexus command : it marks a ship with a turning hex sigil, lines of command run to it from every Mimic near it, then its halo
                          rings align and fire the Overmind Lance.
   Assimilation Pylon adapt : its crystal flickers through colours, settles on the colour of its target's own weapon, and fires that back.
   In a battle with Omega, every Node and Pylon is tethered to it: pulses run up a Node's line (the regeneration it feeds) and a Pylon's
   line carries its crystal's colour (the damage it soaks); when a Pylon dies its line snaps and a crack flashes across Omega's shield. */
Object.assign(MIM_DUR, { synapse: 1.25, command: 1.7, adapt: 1.35 }); Object.assign(MIMX_DUR, { synapse: 1.25, command: 1.7, adapt: 1.35 });
Object.assign(MIMX_SND, { synapse: "hum", command: "hum", adapt: "hum" }); Object.assign(MIM_ATK, { mnode: "synapse", mnexus: "command", mpylon: "adapt" });
const MIM_WCOL = { laser: "255,90,100", beam: "255,205,90", plasma: "120,255,150", ion: "140,170,255", missile: "255,150,70", torpedo: "255,120,50", mass: "235,235,245", flak: "255,220,130", acid: "160,255,90" };
const mimWcol = k => MIM_WCOL[(CPROF[k] || [])[1]] || "127,240,255";
function mimStructX(ctx, b, m, u, S0, E0, Lg, C, gl, d, T, t, scr, hit, pan) {
  const side = b.Q[m.s].side; ctx.save(); ctx.globalCompositeOperation = "lighter";
  if (m.a === "synapse") { const top = { x: S0.x, y: S0.y - Lg * .1 };
    if (!m.fo) { m.fo = [m.e]; for (let j = 0; j < b.Q.length && m.fo.length < 4; j++) if (j !== m.e && b.Q[j] && b.Q[j].side !== side && b.n[j] > 0) m.fo.push(j); }
    const ch = Math.min(1, u / .32), r = Lg * (.15 + .3 * ch); ctx.globalAlpha = u < .32 ? .5 + .5 * ch : Math.max(0, 1 - (u - .32) * 1.6); ctx.drawImage(gl, top.x - r, top.y - r, r * 2, r * 2); ctx.drawImage(glowSprite("#ffffff"), top.x - r * .3, top.y - r * .3, r * .6, r * .6);
    if (u >= .32 && u < .95) { hit(m, E0.x, E0.y, false); let px = top.x, py = top.y; const n = Math.min(m.fo.length, 1 + Math.floor((u - .32) / .1));
      for (let j = 0; j < n; j++) { const F = scr[m.fo[j]]; if (!F) continue; ctx.globalAlpha = .95 * (1 - Math.max(0, u - .8) * 5); if ((T * 24 | 0) % 4) mimBolt(ctx, px, py, F.x, F.y, 2.6 * d, C(1), m.seed + j * 5 + (T * 18 | 0)); /* the leap */
        for (let s2 = 0; s2 < 5; s2++) { const a = s2 * 1.3 + T * 9 + j, rr = Lg * .25; ctx.fillStyle = "rgba(220,250,255,1)"; ctx.globalAlpha = .7; ctx.fillRect(F.x + Math.cos(a) * rr, F.y + Math.sin(a * 1.3) * rr * .5, 2 * d, 2 * d); } /* static crawling over it */
        px = F.x; py = F.y; } } }
  else if (m.a === "command") { const al = []; for (let j = 0; j < b.Q.length && al.length < 6; j++) if (j !== m.s && b.Q[j] && b.Q[j].side === side && b.n[j] > 0 && scr[j] && MIM_D[b.Q[j].k]) al.push(scr[j]);
    if (u > .08 && u < .98) { const k = Math.min(1, (u - .08) / .15), f = u < .85 ? 1 : (.98 - u) / .13, rr = Lg * (.55 - .15 * k); ctx.globalAlpha = f; ctx.strokeStyle = C(1); ctx.lineWidth = 2.2 * d; ctx.save(); ctx.translate(E0.x, E0.y); ctx.rotate(T * .8); ctx.beginPath(); mimHex(ctx, 0, 0, rr); ctx.stroke(); ctx.rotate(-T * 1.6); ctx.globalAlpha = f * .6; ctx.beginPath(); mimHex(ctx, 0, 0, rr * .62); ctx.stroke(); ctx.restore(); } /* the sigil */
    if (u > .22 && u < .85) { const f = Math.min(1, (u - .22) / .1) * Math.min(1, (.85 - u) / .1); ctx.setLineDash([5 * d, 6 * d]); ctx.lineDashOffset = -T * 60 * d; ctx.lineWidth = 1.4 * d; ctx.strokeStyle = C(1); for (const A of al) { ctx.globalAlpha = .7 * f; ctx.beginPath(); ctx.moveTo(A.x, A.y); ctx.lineTo(E0.x, E0.y); ctx.stroke(); } ctx.setLineDash([]); } /* every Mimic near it turns to the mark */
    for (let j = 0; j < 3; j++) { const k = Math.min(1, Math.max(0, (u - .3) / .3)), R = Lg * (.45 + j * .14), tilt = (1 - k) * (j - 1) * .9; ctx.globalAlpha = .55 * (u < .9 ? 1 : (1 - u) * 10); ctx.strokeStyle = C(1); ctx.lineWidth = 2 * d; ctx.beginPath(); ctx.ellipse(S0.x, S0.y - Lg * .25, R, R * (.25 + .2 * Math.abs(Math.sin(tilt + j))), tilt, 0, TAU); ctx.stroke(); } /* the rings come into line */
    if (u >= .6 && u < .95) { hit(m, E0.x, E0.y, true); const k = (u - .6) / .35, wd = 14 * d * (1 - k * .6); ctx.globalAlpha = 1 - k; ctx.strokeStyle = C(1); ctx.lineWidth = wd; ctx.beginPath(); ctx.moveTo(S0.x, S0.y - Lg * .25); ctx.lineTo(E0.x, E0.y); ctx.stroke(); ctx.strokeStyle = "rgba(255,255,255,1)"; ctx.lineWidth = wd * .35; ctx.stroke(); const r = Lg * (.4 + k * .6); ctx.drawImage(gl, E0.x - r, E0.y - r, r * 2, r * 2); } }
  else if (m.a === "adapt") { const cy = { x: S0.x, y: S0.y - Lg * .38 }, wc = mimWcol((b.Q[m.e] || {}).k), CY = ["127,240,255", "255,150,70", "190,120,255", "120,255,150"];
    (b.pylC || (b.pylC = {}))[m.s] = wc;
    const col = u < .38 ? CY[Math.floor(u * 22) % 4] : wc, gs = glowSprite(`rgba(${col},1)`), r = Lg * (u < .38 ? .2 + .25 * (u / .38) : .4); ctx.globalAlpha = u < .38 ? .9 : Math.max(0, 1 - (u - .38) * 1.4); ctx.drawImage(gs, cy.x - r, cy.y - r, r * 2, r * 2); /* the crystal flickers, then settles */
    if (u >= .42 && u < .9) { hit(m, E0.x, E0.y, false); const k = (u - .42) / .48, wd = 8 * d * (1 - k * .5); ctx.globalAlpha = 1 - k; ctx.strokeStyle = `rgba(${col},1)`; ctx.lineWidth = wd; ctx.beginPath(); ctx.moveTo(cy.x, cy.y); ctx.lineTo(E0.x, E0.y); ctx.stroke(); ctx.strokeStyle = "rgba(255,255,255,1)"; ctx.lineWidth = wd * .3; ctx.stroke();
      for (let j = 0; j < 6; j++) { const a = j * 1.05 + m.seed, rr = Lg * .5 * k; ctx.fillStyle = `rgba(${CY[j % 4]},1)`; ctx.fillRect(E0.x + Math.cos(a) * rr, E0.y + Math.sin(a) * rr * .6, 3 * d, 3 * d); } } } /* its own fire, returned, scattering prismatic shards */
  ctx.restore(); }
/* the tethers to Omega, and a Pylon's dying snap */
function mimTethers(ctx, b, scr, T, d) { if (!b || !b.Q) return; let om = -1; for (let i = 0; i < b.Q.length; i++) if (b.Q[i] && /^momega/.test(b.Q[i].k) && b.n[i] > 0 && scr[i]) { om = i; break; } if (om < 0) return; const O = scr[om], gO = b.geo && b.geo[om], LO = gO ? gO.L : 80;
  const was = b.tAlive || (b.tAlive = {}); ctx.save(); ctx.globalCompositeOperation = "lighter";
  for (let i = 0; i < b.Q.length; i++) { const q = b.Q[i]; if (!q || (q.k !== "mnode" && q.k !== "mpylon")) continue; const P = scr[i], alive = b.n[i] > 0;
    if (!alive) { if (was[i] && q.k === "mpylon") (b.snaps || (b.snaps = [])).push({ x: P ? P.x : O.x, y: P ? P.y : O.y, t: T }); was[i] = 0; continue; } was[i] = 1; if (!P) continue;
    const g = b.geo && b.geo[i], Lg = g ? g.L : 40, sx = P.x, sy = P.y - Lg * (q.k === "mpylon" ? .38 : .1), col = q.k === "mpylon" ? ((b.pylC || {})[i] || "127,240,255") : "127,240,255";
    ctx.globalAlpha = .28; ctx.strokeStyle = `rgba(${col},1)`; ctx.lineWidth = 1.6 * d; ctx.beginPath(); ctx.moveTo(sx, sy); ctx.quadraticCurveTo((sx + O.x) / 2, Math.min(sy, O.y) - LO * .3, O.x, O.y); ctx.stroke();
    for (let j = 0; j < 2; j++) { const k = ((T * .35 + j * .5 + i * .13) % 1), x = (1 - k) * (1 - k) * sx + 2 * (1 - k) * k * ((sx + O.x) / 2) + k * k * O.x, y = (1 - k) * (1 - k) * sy + 2 * (1 - k) * k * (Math.min(sy, O.y) - LO * .3) + k * k * O.y, r = Math.max(3 * d, Lg * .08);
      ctx.globalAlpha = .8 * Math.sin(Math.PI * k); ctx.drawImage(glowSprite(`rgba(${col},1)`), x - r, y - r, r * 2, r * 2); } } /* the pulses run toward Omega, slowly */
  for (const s of b.snaps || []) { const k = (T - s.t) / 1.5; if (k < 0 || k > 1) continue; ctx.globalAlpha = 1 - k; ctx.strokeStyle = "rgba(200,245,255,1)"; ctx.lineWidth = 2 * d; ctx.beginPath(); let x = O.x - LO * .4, y = O.y - LO * .1; ctx.moveTo(x, y); for (let j = 1; j <= 7; j++) { x = O.x - LO * .4 + j * LO * .12; y = O.y - LO * .1 + Math.sin(j * 2.7 + s.t) * LO * .12; ctx.lineTo(x, y); } ctx.stroke(); /* the crack across its shield */
    ctx.globalAlpha = (1 - k) * .6; ctx.beginPath(); ctx.ellipse(O.x, O.y, LO * .7 * (1 + k * .3), LO * .4 * (1 + k * .3), 0, 0, TAU); ctx.stroke(); }
  ctx.restore(); }
