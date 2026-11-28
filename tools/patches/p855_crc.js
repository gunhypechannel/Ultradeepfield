/* ---------- v855 the Carcinid bosses remastered (owner: "remaster the crab bosses in battle simulation they look very smooth and soft and
   unrealistic ... more visually entertaining and colorful ... slow the crab walking animation to a slow menacing walk ... can be an advisor
   line ... awesome and spectacular ... more glows and elemental water effects", then "build it all") ----------
   Models: tools/sculpt/crc_boss.py, hard-edged after each painting, with a glow layer (art/carcinid/m/<k>_g.bin).
   Material: wet and glossy, lit seams brighter, a rim light in the boss's colour, its lights breathing slowly, sea-light rippling over the shell.
   In battle: a haze of water round each boss, bubbles rising off its joints, water dripping from its claws; water swirls into its claws as it
   winds up; a pressure blast of spray where its blows land, a tidal ring from its crush, the Oracle's beam of glowing water; a hit leaves the
   target shimmering, bubbling and crusted with salt; an entrance (rings of water, its eyes lighting first, then its seams) and a death (its
   shell splits and pours out light and water). The crabs walk slowly: a heavy stride, about three seconds a step. */
const CRC_BK = new Set(["cmar", "cmat", "ctyr", "cora", "ckor", "cbeh", "ckbr", "cpal", "ccrown", "ccrownm"]);
for (const k of CRC_BK) if (CRC_SC[k]) CRC_SC[k].g = 1;
const CRC_WATER = "120,220,255";
function crcBossMat(k) { const C = crcBossMat.C || (crcBossMat.C = {}); if (C[k]) return C[k]; const b = cntMeshMat(), m = b.clone(), rgb = (BOSS_GLOW[k] || "120,220,255").split(",").map(v => (+v / 255).toFixed(3)).join(", ");
  const obc = sh => { b.userData.obc(sh); sh.vertexShader = sh.vertexShader.replace("#include <common>", "#include <common>\nvarying vec3 vMP;").replace("#include <begin_vertex>", "#include <begin_vertex>\nvMP = position;");
    sh.fragmentShader = sh.fragmentShader.replace("#include <common>", "#include <common>\nvarying vec3 vMP;").replace("roughnessFactor = max(.05, vRM.x);", "roughnessFactor = max(.06, vRM.x * .55);")
      .replace("totalEmissiveRadiance += vEm;", `totalEmissiveRadiance += vEm * 1.35; { float fr = pow(1. - saturate(abs(dot(normal, normalize(vViewPosition)))), 2.6); totalEmissiveRadiance += vec3(${rgb}) * fr * .3; }`); };
  m.onBeforeCompile = obc; m.userData.obc = obc; m.envMapIntensity = .5;
  /* the lights breathe (6 s), and bands of sea-light drift slowly over the shell */
  m.userData.pulse = "(.85 + .35 * (.5 + .5 * sin(uMT * 1.0472)) + .55 * pow(.5 + .5 * sin(vMP.x * 3.1 + vMP.z * 1.7 - uMT * 1.0472), 6.) * pow(.5 + .5 * sin(vMP.z * 2.6 - vMP.x * 1.3 + uMT * 1.0472), 6.))";
  m.customProgramCacheKey = () => "crcboss1" + k; return C[k] = m; }
/* ---- in battle ---- */
const crcBoss = q => q && CRC_BK.has(q.k);
const crcFace = (b, i, P) => { let sx = 0, n = 0; const sd = b.Q[i].side; for (let j = 0; j < b.Q.length; j++) { const q = b.Q[j]; if (q && q.side !== sd && b.n[j] > 0 && b.scr && b.scr[j]) { sx += b.scr[j].x; n++; } } return n ? Math.sign(sx / n - P.x) || 1 : (sd === "d" ? -1 : 1); };
function crcBossFx(ctx, b, scr, T, d) { if (!b || !b.Q) return; b.scr = scr; ctx.save(); ctx.globalCompositeOperation = "lighter"; const seen = b.cbSeen || (b.cbSeen = {}), was = b.cbAlive || (b.cbAlive = {}), ws = glowSprite(`rgba(${CRC_WATER},1)`);
  for (let i = 0; i < b.Q.length; i++) { const q = b.Q[i], P = scr[i]; if (!crcBoss(q)) continue; const g = b.geo && b.geo[i], Lg = g ? g.L : 60, col = BOSS_GLOW[q.k] || CRC_WATER, gs = glowSprite(`rgba(${col},1)`);
    if (!(b.n[i] > 0)) { if (was[i] && P) (b.cbDie || (b.cbDie = [])).push({ x: P.x, y: P.y, t: T, col, Lg }); was[i] = 0; continue; } was[i] = 1; if (!P) continue; if (seen[i] == null) seen[i] = T;
    const br = .5 + .5 * Math.sin(T * 1.0472 + i), fc = crcFace(b, i, P);
    ctx.globalAlpha = .04 + .035 * br; ctx.drawImage(gs, P.x - Lg * .85, P.y - Lg * .55, Lg * 1.7, Lg * 1.1); /* its light, breathing */
    ctx.globalAlpha = .06; ctx.drawImage(ws, P.x - Lg * 1.1, P.y - Lg * .2, Lg * 2.2, Lg * .8); /* the haze of water round it */
    for (let j = 0; j < 7; j++) { const ph = T * .28 + j / 7 + i * .31, k = ph % 1, c = Math.floor(ph), x = P.x + Math.sin(i * 5.3 + j * 2.9 + c * 9.7) * Lg * .5, y = P.y + Lg * .1 - k * Lg * .75, r = Math.max(1.4 * d, Lg * .022) * (.6 + .6 * k);
      ctx.globalAlpha = Math.sin(Math.PI * k) * .7; ctx.strokeStyle = `rgba(${CRC_WATER},1)`; ctx.lineWidth = Math.max(1, .9 * d); ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.stroke(); } /* bubbles rise off its joints */
    for (let j = 0; j < 4; j++) { const ph = T * .45 + j / 4 + i * .17, k = ph % 1, s = j % 2 ? 1 : -1, x = P.x + fc * Lg * (.5 + .08 * j), y = P.y + s * Lg * .12 + k * k * Lg * .45, r = Math.max(1.2 * d, Lg * .018) * (1 - k * .4);
      ctx.globalAlpha = (1 - k) * .8; ctx.fillStyle = `rgba(${CRC_WATER},1)`; ctx.beginPath(); ctx.ellipse(x, y, r * .7, r * 1.5, 0, 0, TAU); ctx.fill(); } /* water drips from its claws */
    for (let j = 0; j < 2; j++) { const k = (T / 5 + j * .5 + i * .23) % 1, x = P.x - Lg * .5 + k * Lg; ctx.globalAlpha = .22 * Math.sin(Math.PI * k); ctx.strokeStyle = "rgba(200,245,255,1)"; ctx.lineWidth = 1.2 * d; ctx.beginPath(); ctx.ellipse(x, P.y - Lg * .12, Lg * .16, Lg * .05, .3, 0, Math.PI); ctx.stroke(); } /* sea-light rippling across its shell */
    const e = T - seen[i]; if (e < 3) { /* the entrance: rings of water, its eyes first, then its seams */
      for (let j = 0; j < 3; j++) { const k = (e - j * .35) / 1.6; if (k < 0 || k > 1) continue; const R = Lg * (.4 + .9 * k); ctx.globalAlpha = (1 - k) * .45; ctx.strokeStyle = `rgba(${CRC_WATER},1)`; ctx.lineWidth = (3 - 2 * k) * d; ctx.beginPath(); ctx.ellipse(P.x, P.y + Lg * .2, R, R * .32, 0, 0, TAU); ctx.stroke(); }
      if (e < 1.4) { const k = e / 1.4; for (const s of [-1, 1]) { ctx.globalAlpha = Math.sin(Math.PI * k); ctx.drawImage(gs, P.x + fc * Lg * .38 - Lg * .1, P.y - Lg * .05 + s * Lg * .06 - Lg * .1, Lg * .2, Lg * .2); } }
      if (e > .9 && e < 2.6) { const k = (e - .9) / 1.7; ctx.globalAlpha = Math.sin(Math.PI * k) * .35; ctx.drawImage(gs, P.x - Lg * .7 * k, P.y - Lg * .4 * k, Lg * 1.4 * k, Lg * .8 * k); } } }
  for (const D of b.cbDie || []) { const k = (T - D.t) / 2.2; if (k < 0 || k > 1) continue; const gs = glowSprite(`rgba(${D.col},1)`);
    ctx.globalAlpha = (1 - k) * .95; ctx.strokeStyle = `rgba(${D.col},1)`; ctx.lineWidth = 2 * d; ctx.beginPath(); for (let j = 0; j < 6; j++) { const a = j * 1.05 + .4; ctx.moveTo(D.x, D.y); ctx.lineTo(D.x + Math.cos(a) * D.Lg * (.3 + .5 * Math.min(1, k * 3)), D.y + Math.sin(a) * D.Lg * .3 * (.3 + .5 * Math.min(1, k * 3))); } ctx.stroke(); /* the shell splits */
    const r = D.Lg * (.3 + k * 1.2); ctx.globalAlpha = (1 - k) * .8; ctx.drawImage(gs, D.x - r, D.y - r * .7, r * 2, r * 1.4);
    for (let j = 0; j < 14; j++) { const a = j * .449 + D.t, dd = D.Lg * (.2 + 1.3 * k), x = D.x + Math.cos(a) * dd, y = D.y + Math.sin(a) * dd * .5 + k * k * D.Lg * .4; ctx.globalAlpha = (1 - k) * .85; ctx.fillStyle = `rgba(${CRC_WATER},1)`; ctx.beginPath(); ctx.arc(x, y, Math.max(1.5 * d, D.Lg * .025) * (1 - k * .5), 0, TAU); ctx.fill(); } } /* light and water pour out */
  crcMarks(ctx, b, scr, T, d); ctx.restore(); }
/* the attacks: water gathers in the claws, a pressure blast of spray where the blow lands, a tidal ring from the crush, the Oracle's beam */
function crcBossAtk(ctx, b, scr, T, d) { const L = []; for (const m of b.cAtk || []) L.push([m, CRC_ADUR[m.a] || 1, 0]); for (const m of b.mAtk || []) if (crcBoss(b.Q[m.s])) L.push([m, MIM_DUR[m.a] || 1, 1]); if (!L.length) return;
  ctx.save(); ctx.globalCompositeOperation = "lighter"; const ws = glowSprite(`rgba(${CRC_WATER},1)`);
  for (const [m, D, mi] of L) { const q = b.Q[m.s]; if (!crcBoss(q) || !(b.n[m.s] > 0)) continue; const u = (T - m.t0) / D; if (u < 0 || u > 1.2) continue; const S0 = scr[m.s], E0 = scr[m.e]; if (!S0 || !E0) continue;
    const g = b.geo && b.geo[m.s], Lg = g ? g.L : 60, col = BOSS_GLOW[q.k] || CRC_WATER, fc = Math.sign(E0.x - S0.x) || 1, H = { x: S0.x + fc * Lg * .55, y: S0.y };
    if (u < .3) { const k = u / .3; for (let j = 0; j < 10; j++) { const a = j * .628 + k * 5 + m.seed, rr = Lg * .6 * (1 - k), x = H.x + Math.cos(a) * rr, y = H.y + Math.sin(a) * rr * .55; ctx.globalAlpha = .8 * Math.min(1, k * 3); ctx.fillStyle = `rgba(${CRC_WATER},1)`; ctx.beginPath(); ctx.arc(x, y, Math.max(1.4 * d, Lg * .02), 0, TAU); ctx.fill(); }
      const r = Lg * (.08 + .18 * k); ctx.globalAlpha = .35 + .4 * k; ctx.drawImage(glowSprite(`rgba(${col},1)`), H.x - r, H.y - r, r * 2, r * 2); ctx.drawImage(ws, H.x - r * .6, H.y - r * .6, r * 1.2, r * 1.2); } /* water swirls into its claws */
    if (q.k === "cora" && u >= .3 && u < .75) { const k = (u - .3) / .45, wd = 10 * d * (1 - k * .6); ctx.globalAlpha = 1 - k; ctx.strokeStyle = `rgba(${CRC_WATER},1)`; ctx.lineWidth = wd; ctx.beginPath(); ctx.moveTo(S0.x, S0.y - Lg * .3);
      for (let j = 1; j <= 12; j++) { const t2 = j / 12; ctx.lineTo(S0.x + (E0.x - S0.x) * t2, S0.y - Lg * .3 + (E0.y - S0.y + Lg * .3) * t2 + Math.sin(t2 * 18 - T * 14) * 4 * d * (1 - t2 * .5)); } ctx.stroke(); ctx.strokeStyle = "rgba(220,200,255,1)"; ctx.lineWidth = wd * .3; ctx.stroke(); } /* the Oracle's beam of glowing water */
    if (u >= .35 && !m.cw) { m.cw = 1; m.cwT = T; crcMark(b, m.e, T, col); }
    if (m.cwT != null) { const k = (T - m.cwT) / .9; if (k >= 0 && k < 1) { for (let j = 0; j < 12; j++) { const a = j * .524 + m.seed, dd = Lg * (.15 + .75 * k), x = E0.x + Math.cos(a) * dd, y = E0.y + Math.sin(a) * dd * .55 + k * k * Lg * .25; ctx.globalAlpha = (1 - k) * .9; ctx.fillStyle = `rgba(${CRC_WATER},1)`; ctx.beginPath(); ctx.arc(x, y, Math.max(1.3 * d, Lg * .02) * (1 - k * .5), 0, TAU); ctx.fill(); } /* the pressure blast of spray */
        const R = Lg * (.25 + (mi ? 1.2 : .55) * k); ctx.globalAlpha = (1 - k) * .5; ctx.strokeStyle = `rgba(${CRC_WATER},1)`; ctx.lineWidth = (mi ? 4 : 2.4) * d * (1 - k * .6); ctx.beginPath(); ctx.ellipse(E0.x, E0.y + Lg * .05, R, R * .35, 0, 0, TAU); ctx.stroke();
        if (mi) { ctx.globalAlpha = (1 - k) * .45; ctx.beginPath(); ctx.ellipse(E0.x, E0.y + Lg * .05, R * .7, R * .25, 0, 0, TAU); ctx.stroke(); ctx.globalAlpha = (1 - k) * .5; ctx.drawImage(glowSprite("rgba(235,245,255,1)"), E0.x - R * .5, E0.y - R * .5, R, R * .7); } } } } /* a tidal ring from its crush, and steam */
  ctx.restore(); }
function crcMark(b, e, T, col) { const L = b.cMark || (b.cMark = []); L.push({ e, t: T, col, seed: (e * 13 + L.length) % 17 }); if (L.length > 12) L.splice(0, L.length - 12); }
function crcMarks(ctx, b, scr, T, d) { for (const M of b.cMark || []) { const k = (T - M.t) / 3, P = scr[M.e]; if (k < 0 || k > 1 || !P) continue; const g = b.geo && b.geo[M.e], Lg = g ? g.L : 30, f = 1 - k;
    ctx.globalAlpha = .14 * f; ctx.drawImage(glowSprite(`rgba(${CRC_WATER},1)`), P.x - Lg * .8, P.y - Lg * .5, Lg * 1.6, Lg); /* a watery shimmer */
    for (let j = 0; j < 5; j++) { const q = (T * .7 + j / 5 + M.seed * .1) % 1, x = P.x + Math.sin(j * 2.1 + M.seed) * Lg * .3, y = P.y - q * Lg * .4; ctx.globalAlpha = f * Math.sin(Math.PI * q) * .8; ctx.strokeStyle = `rgba(${CRC_WATER},1)`; ctx.lineWidth = Math.max(1, .8 * d); ctx.beginPath(); ctx.arc(x, y, Math.max(1.2 * d, Lg * .03), 0, TAU); ctx.stroke(); } /* bubbling */
    for (let j = 0; j < 6; j++) { const a = j * 1.05 + M.seed; ctx.globalAlpha = f * .7; ctx.fillStyle = "rgba(235,245,250,1)"; ctx.fillRect(P.x + Math.cos(a) * Lg * .28, P.y + Math.sin(a * 1.3) * Lg * .14, 1.8 * d, 1.8 * d); } } } /* crusted with salt */
/* the Advisor, the first time she sees one walk (owner-approved line) */
const CRC_WALK_LINE = "They don't need legs out here, Commander. They walk anyway. Every step is a memory of the oceans they crawled out of… and a promise about the ones they mean to drown next.";
function crcWalkSay(b) { try { if (b.cbSaid || !b.Q.some(q => crcBoss(q)) || !(b.simT > 4)) return; b.cbSaid = 1; if (advOnce("crcWalk")) sbSay(CRC_WALK_LINE); } catch (e) {} }
