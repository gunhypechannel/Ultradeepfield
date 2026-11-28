/* ---------- v849 the Mimics glow (owner: "give all mimics even more glow especially the neural node, nexus, and assimilation pod ...
   great elemental effects and glows for their attacks like charging up", then "build all the rest") ----------
   1 every Mimic's lights breathe slowly (6 s, in its sculpt's material, so on the map and in battle frames alike); the Node's brain
     ripples, the Pylon's lights climb its plates, the Nexus's eye swells and dims.
   2 every attack winds up: light gathers into the mouth or claws first; the Node's antennae and cage, the Nexus's dome and eye, the
     Pylon's plates and crystal each charge in their own way before they fire.
   3 each has an element: the Node electric, the Nexus psychic, the Pylon prismatic, each Mimic class acid green or bio-red.
   4 a hit leaves its element on the target for a few seconds (acid sizzle, scorch, static, psychic ripple, prismatic glints), its light
     spilling over the ships around it.
   5 a soft halo round every Mimic's lights so they read against space, even on a phone.
   6 when a Node or Pylon charges, a fast bright pulse races up its tether and Omega flares in answer. */
const MIM_EL = { mstalk: ["acid", "150,255,90"], mharv: ["acid", "150,255,90"], mguard: ["acid", "150,255,90"], mhunt: ["bio", "255,70,95"], mtitan: ["bio", "255,70,95"], massim: ["bio", "255,70,95"],
  mnode: ["volt", "175,230,255"], mnexus: ["psy", "190,120,255"], mpylon: ["prism", "127,240,255"] };
const mimEl = k => MIM_EL[k] || ["cyan", BOSS_GLOW[k] || "95,216,255"];
const MIM_PRISM = ["255,90,110", "255,200,90", "120,255,150", "110,190,255", "200,120,255"];
/* where the light gathers: the head, toward the prey (the structures and the hive gather at their centre) */
function mimChargePt(b, m, S0, E0, Lg) { const k = b.Q[m.s].k; if (/^(mnest|mnexus|mnode|mpylon|momega)/.test(k)) return { x: S0.x, y: S0.y - Lg * .15 }; const dx = E0.x - S0.x, dy = E0.y - S0.y, dl = Math.hypot(dx, dy) || 1; return { x: S0.x + dx / dl * Lg * .45, y: S0.y + dy / dl * Lg * .45 }; }
function mimCharge(ctx, b, m, u, S0, E0, Lg, d, T) { const k = u / .25, [el, col] = mimEl(b.Q[m.s].k), H = mimChargePt(b, m, S0, E0, Lg), gs = glowSprite(`rgba(${col},1)`); ctx.save(); ctx.globalCompositeOperation = "lighter";
  for (let j = 0; j < 9; j++) { const a = j * .698 + m.seed + k * 2.2, rr = Lg * .75 * (1 - k) * (.75 + .25 * Math.sin(j * 2.1)), x = H.x + Math.cos(a) * rr, y = H.y + Math.sin(a) * rr * .6, r = Math.max(2 * d, Lg * .03);
    ctx.globalAlpha = .85 * Math.min(1, k * 3); ctx.drawImage(gs, x - r * 2, y - r * 2, r * 4, r * 4); if (el === "volt" && j % 3 === 0 && (T * 20 | 0) % 2) mimBolt(ctx, x, y, H.x, H.y, 1.2 * d, `rgba(${col},1)`, m.seed + j + (T * 16 | 0)); } /* motes spiral in */
  const r = Lg * (.07 + .2 * k); ctx.globalAlpha = .55 + .45 * k; ctx.drawImage(gs, H.x - r, H.y - r, r * 2, r * 2); ctx.globalAlpha = .6 * k; ctx.drawImage(glowSprite("#ffffff"), H.x - r * .3, H.y - r * .3, r * .6, r * .6); ctx.restore(); }
/* the elements a hit leaves behind */
function mimMark(b, m, T) { const [el, col] = mimEl(b.Q[m.s].k), L = b.mMark || (b.mMark = []), ids = m.fo && m.fo.length ? m.fo : [m.e];
  for (const e of ids) { L.push({ e, t: T, el, col: m.a === "adapt" ? ((b.pylC || {})[m.s] || col) : col, seed: m.seed + e }); } if (L.length > 14) L.splice(0, L.length - 14); }
function mimMarks(ctx, b, scr, T, d) { const L = b.mMark; if (!L || !L.length) return; ctx.save(); ctx.globalCompositeOperation = "lighter";
  for (const M of L) { const k = (T - M.t) / 3, P = scr[M.e]; if (k < 0 || k > 1 || !P) continue; const g = b.geo && b.geo[M.e], Lg = g ? g.L : 30, f = 1 - k, gs = glowSprite(`rgba(${M.col},1)`);
    ctx.globalAlpha = .26 * f; ctx.drawImage(gs, P.x - Lg, P.y - Lg * .7, Lg * 2, Lg * 1.4); /* its light spills over the ships around it */
    for (let j = 0; j < 6; j++) { const ph = T * .9 + j / 6 + M.seed * .13, q = ph % 1, a = j * 1.05 + M.seed, rx = Math.cos(a) * Lg * .35, ry = Math.sin(a * 1.3) * Lg * .18, r = Math.max(1.4 * d, Lg * .035);
      if (M.el === "acid") { ctx.globalAlpha = f * (1 - q) * .9; ctx.fillStyle = `rgba(${M.col},1)`; ctx.beginPath(); ctx.arc(P.x + rx, P.y + ry + q * Lg * .3, r * (1 - q * .5), 0, TAU); ctx.fill(); } /* acid drips and sizzles */
      else if (M.el === "bio") { ctx.globalAlpha = f * (1 - q) * .8; ctx.drawImage(gs, P.x + rx - r * 2, P.y + ry - q * Lg * .3 - r * 2, r * 4, r * 4); } /* embers rise off the scorch */
      else if (M.el === "volt") { if (((T * 14 | 0) + j) % 3 === 0) { ctx.globalAlpha = f * .9; mimBolt(ctx, P.x + rx, P.y + ry, P.x - rx * .6, P.y + ry * -.8, 1.2 * d, `rgba(${M.col},1)`, M.seed + j + (T * 14 | 0)); } } /* static crawls over it */
      else if (M.el === "psy") { if (j < 2) { const R = Lg * (.2 + q * .7); ctx.globalAlpha = f * (1 - q) * .7; ctx.strokeStyle = `rgba(${M.col},1)`; ctx.lineWidth = 1.5 * d; ctx.beginPath(); ctx.ellipse(P.x, P.y, R, R * .5, 0, 0, TAU); ctx.stroke(); } } /* its mind rings */
      else if (M.el === "prism") { ctx.globalAlpha = f * Math.sin(Math.PI * q); ctx.fillStyle = `rgba(${MIM_PRISM[j % 5]},1)`; ctx.fillRect(P.x + rx, P.y + ry, 2.4 * d, 2.4 * d); } /* rainbow glints */
      else { ctx.globalAlpha = f * (1 - q) * .7; ctx.drawImage(gs, P.x + rx - r * 2, P.y + ry - r * 2, r * 4, r * 4); } } }
  ctx.restore(); }
/* the lights at rest: a soft halo that breathes, and each structure's own life */
function mimGlow(ctx, b, scr, T, d) { if (!b || !b.Q) return; let n = 0; ctx.save(); ctx.globalCompositeOperation = "lighter";
  for (let i = 0; i < b.Q.length && n < 16; i++) { const q = b.Q[i], P = scr[i]; if (!q || !P || !MIM_D[q.k] || !(b.n[i] > 0)) continue; n++;
    const g = b.geo && b.geo[i], Lg = g ? g.L : 40, col = BOSS_GLOW[q.k] || "95,216,255", br = .5 + .5 * Math.sin(T * 1.0472 + i * 1.7), gs = glowSprite(`rgba(${col},1)`);
    ctx.globalAlpha = .07 + .07 * br; ctx.drawImage(gs, P.x - Lg * .75, P.y - Lg * .5, Lg * 1.5, Lg); /* the halo */
    if (q.k === "mnode") { const c = { x: P.x, y: P.y - Lg * .1 }, vs = glowSprite("rgba(175,230,255,1)");
      ctx.globalAlpha = .3 + .25 * br; ctx.drawImage(vs, c.x - Lg * .3, c.y - Lg * .3, Lg * .6, Lg * .6);
      for (let j = 0; j < 2; j++) { const k = (T / 3 + j * .5 + i * .2) % 1, R = Lg * (.12 + .4 * k); ctx.globalAlpha = .45 * (1 - k); ctx.strokeStyle = "rgba(175,230,255,1)"; ctx.lineWidth = 1.4 * d; ctx.beginPath(); ctx.ellipse(c.x, c.y, R, R * .75, 0, 0, TAU); ctx.stroke(); } /* the brain ripples */
      const ph = (T / 2.6 + i * .37) % 1; if (ph < .07) { const s = Math.floor(T / 2.6 + i * .37), a1 = s * 2.3, a2 = a1 + 1.4 + (s % 3) * .5, R = Lg * .35; ctx.globalAlpha = .9 * (1 - ph / .07); mimBolt(ctx, c.x + Math.cos(a1) * R, c.y + Math.sin(a1) * R * .8, c.x + Math.cos(a2) * R, c.y + Math.sin(a2) * R * .8, 1.4 * d, "rgba(200,240,255,1)", s * 7 + i); } } /* a crackle across the cage */
    else if (q.k === "mnexus") { const e = { x: P.x, y: P.y - Lg * .25 }, ps = glowSprite("rgba(190,120,255,1)"); ctx.globalAlpha = .3 + .3 * br; ctx.drawImage(ps, e.x - Lg * .28, e.y - Lg * .28, Lg * .56, Lg * .56); ctx.globalAlpha = .5 + .3 * br; ctx.drawImage(gs, e.x - Lg * .1, e.y - Lg * .1, Lg * .2, Lg * .2); /* the eye swells and dims */
      const k = (T / 4 + i * .3) % 1, R = Lg * (.3 + .9 * k); ctx.globalAlpha = .35 * (1 - k); ctx.strokeStyle = "rgba(190,120,255,1)"; ctx.lineWidth = 2 * d * (1 - k * .6); ctx.beginPath(); ctx.ellipse(e.x, e.y, R, R * .55, 0, 0, TAU); ctx.stroke(); } /* a psychic ripple rolls out */
    else if (q.k === "mpylon") { const c = { x: P.x, y: P.y - Lg * .38 }, pc = (b.pylC || {})[i] || "127,240,255", cs = glowSprite(`rgba(${pc},1)`); ctx.globalAlpha = .35 + .3 * br; ctx.drawImage(cs, c.x - Lg * .25, c.y - Lg * .25, Lg * .5, Lg * .5);
      for (let j = 0; j < 3; j++) { const a = T * .6 + j * 2.094 + i, x = c.x + Math.cos(a) * Lg * .22, y = c.y + Math.sin(a) * Lg * .08; ctx.globalAlpha = .8; ctx.drawImage(glowSprite(`rgba(${MIM_PRISM[(j + i) % 5]},1)`), x - 3 * d, y - 3 * d, 6 * d, 6 * d); } /* prismatic motes circle the crystal */
      const k = (T / 6 + i * .2) % 1, y = P.y + Lg * .3 - k * Lg * .62; ctx.globalAlpha = .5 * Math.sin(Math.PI * k); ctx.fillStyle = `rgba(${pc},1)`; ctx.fillRect(P.x - Lg * .12, y, Lg * .24, 1.6 * d); } /* a band of light climbs its plates */ }
  ctx.restore(); mimMarks(ctx, b, scr, T, d); }
/* each structure's wind-up, drawn under its attack */
function mimStructCharge(ctx, b, m, u, S0, E0, Lg, d, T) { ctx.save(); ctx.globalCompositeOperation = "lighter";
  if (m.a === "synapse" && u < .34) { const k = u / .32, top = { x: S0.x, y: S0.y - Lg * .1 }; ctx.strokeStyle = "rgba(200,240,255,1)";
    for (let j = -1; j <= 1; j++) { const bx = top.x + j * Lg * .16, tx = top.x + j * Lg * .26, ty = top.y - Lg * .5, y = top.y + (ty - top.y) * ((k * 1.6 + j * .17 + 1) % 1), x = bx + (tx - bx) * ((y - top.y) / (ty - top.y)); ctx.globalAlpha = .9; ctx.drawImage(glowSprite("rgba(175,230,255,1)"), x - 4 * d, y - 4 * d, 8 * d, 8 * d);
      if (k > .7) { ctx.globalAlpha = (k - .7) / .3; ctx.drawImage(glowSprite("#ffffff"), tx - 5 * d, ty - 5 * d, 10 * d, 10 * d); } } /* sparks climb the antenna spines */
    if ((T * 22 | 0) % 2) for (let j = 0; j < 2; j++) { const a = T * 7 + j * 3, R = Lg * .34; ctx.globalAlpha = .7 * k; mimBolt(ctx, top.x + Math.cos(a) * R, top.y + Math.sin(a) * R * .8, top.x + Math.cos(a + 1.9) * R, top.y + Math.sin(a + 1.9) * R * .8, 1.3 * d, "rgba(200,240,255,1)", m.seed + j + (T * 22 | 0)); } } /* arcs leap between the ribs */
  else if (m.a === "command" && u < .62) { const k = u / .6, e = { x: S0.x, y: S0.y - Lg * .25 };
    for (let j = 0; j < 7; j++) { const lit = k * 8 - j; if (lit <= 0) continue; const a = j * .9 - 2.7, x = e.x + Math.cos(a) * Lg * .42, y = e.y - Lg * .12 + Math.sin(a) * Lg * .22; ctx.globalAlpha = Math.min(1, lit) * .75; ctx.strokeStyle = "rgba(200,150,255,1)"; ctx.lineWidth = 1.4 * d; ctx.beginPath(); mimHex(ctx, x, y, Lg * .07); ctx.stroke(); } /* the dome lights panel by panel */
    const rx = Lg * .14, ry = Math.max(1.5 * d, Lg * .12 * (1 - k * .85)); ctx.globalAlpha = .9; ctx.fillStyle = "rgba(235,215,255,1)"; ctx.beginPath(); ctx.ellipse(e.x, e.y, rx, ry, 0, 0, TAU); ctx.fill(); ctx.globalAlpha = .6 + .4 * k; ctx.drawImage(glowSprite("rgba(190,120,255,1)"), e.x - Lg * .35, e.y - Lg * .35, Lg * .7, Lg * .7); /* the eye narrows to a white slit */
    if (k > .8) { const R = Lg * (.3 + (k - .8) * 4); ctx.globalAlpha = (1 - (k - .8) / .2) * .8; ctx.strokeStyle = "rgba(190,120,255,1)"; ctx.lineWidth = 2.4 * d; ctx.beginPath(); ctx.ellipse(e.x, e.y, R, R * .55, 0, 0, TAU); ctx.stroke(); } } /* a psychic shock as it fires */
  else if (m.a === "adapt" && u < .44) { const k = u / .42, cy = { x: S0.x, y: S0.y - Lg * .38 };
    for (let j = 0; j < 10; j++) { const a = j * .628 + m.seed, rr = Lg * .95 * (1 - ((k + j * .1) % 1)), x = cy.x + Math.cos(a) * rr, y = cy.y + Math.sin(a) * rr * .6; ctx.globalAlpha = .8; ctx.fillStyle = `rgba(${MIM_PRISM[j % 5]},1)`; ctx.fillRect(x, y, 2.4 * d, 2.4 * d); } /* light is drawn in from all round */
    for (let j = 0; j < 6; j++) { const lit = k * 7 - j; if (lit <= 0) continue; const y = S0.y + Lg * .28 - j * Lg * .1; ctx.globalAlpha = Math.min(1, lit) * .7; ctx.fillStyle = "rgba(127,240,255,1)"; ctx.fillRect(S0.x - Lg * .1, y, Lg * .2, 1.8 * d); } } /* its plates light from the base up */
  ctx.restore(); }
/* the Pylon's returned fire splits into a rainbow */
function mimPrismBeam(ctx, x0, y0, x1, y1, k, d) { const dx = x1 - x0, dy = y1 - y0, dl = Math.hypot(dx, dy) || 1, nx = -dy / dl, ny = dx / dl; ctx.save(); ctx.globalCompositeOperation = "lighter";
  for (let j = 0; j < 3; j++) { const o = (j - 1) * 7 * d * (1 - k * .5); ctx.globalAlpha = (1 - k) * .75; ctx.strokeStyle = `rgba(${MIM_PRISM[j * 2 % 5]},1)`; ctx.lineWidth = 2 * d; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.quadraticCurveTo((x0 + x1) / 2 + nx * o * 3, (y0 + y1) / 2 + ny * o * 3, x1, y1); ctx.stroke(); } ctx.restore(); }
