# v407: a super boss's attacks reach across the battle report. The boss is a 3D picture drawn in a box round itself, so its own beams were
# clipped halfway down the screen (and in portrait it faces the camera). Each attack now also plays on the full field, timed to the
# model's move and in the boss's colour: a beam to the fleet (sweeping for the Wyrm), a volley of bolts each striking a ship (jagged
# lightning for the storm), or a shockwave rolling over the whole field, with impact flashes, light and shake on the ships it hits.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
# [type, window start, window end (fractions of the move), bolts, move length ms]
rep("""const wbMoves = key => WB_ATK[key] || WB_ATK.c0;""", """const wbMoves = key => WB_ATK[key] || WB_ATK.c0;
const WB_STRIKE = {
  ovl: { beam: ["beam", .35, .82, 0, 3200], stomp: ["wave", .42, .9, 0, 1700] },
  dev: { lash: ["bolts", .3, .65, 4, 1600], beam: ["beam", .35, .85, 0, 3000], roar: ["wave", .3, .85, 0, 2400] },
  war: { pulse: ["wave", .2, .75, 0, 1800], beam: ["beam", .35, .82, 0, 3200] },
  c0: { discharge: ["bolts", .2, .7, 5, 1800] },
  brd: { hatch: ["bolts", .4, .92, 7, 3000], acid: ["bolts", .3, .8, 5, 2800], slam: ["wave", .4, .88, 0, 1900] },
  tyr: { broadside: ["bolts", .25, .82, 10, 2800], claw: ["beam", .42, .72, 0, 2600], mines: ["bolts", .4, .92, 6, 3800] },
  wym: { lens: ["beam", .35, .85, 0, 3000], sweep: ["sweep", .2, .82, 0, 2200] },
  col: { prism: ["beam", .35, .85, 0, 3000], rain: ["bolts", .3, .88, 9, 2800], shatter: ["wave", .4, .9, 0, 2800] },
  eic: { nova: ["wave", .35, .85, 0, 2800], lance: ["bolts", .35, .8, 5, 2800], zero: ["wave", .4, .92, 0, 2800] },
  efi: { flare: ["wave", .3, .8, 0, 2800], rain: ["bolts", .3, .9, 9, 2800], inferno: ["wave", .4, .92, 0, 2800] },
  eli: { lance: ["beam", .35, .78, 0, 2800], halo: ["wave", .35, .85, 0, 2800], judgement: ["beam", .4, .9, 0, 2800] },
  est: { chain: ["chain", .3, .8, 6, 2800], ion: ["bolts", .3, .85, 7, 2800], clap: ["wave", .4, .88, 0, 2800] },
  ena: { thorn: ["bolts", .3, .8, 8, 2800], spore: ["wave", .3, .9, 0, 2800], growth: ["beam", .4, .88, 0, 2800] },
  epx: { converge: ["beam", .5, .95, 0, 3400], storm: ["bolts", .2, .9, 12, 3000], cataclysm: ["wave", .45, .95, 0, 3200] } };
/* v407 a boss's attack on the whole battle field (its 3D picture is drawn in a box round the boss, which clipped its beams halfway) */
function wbStrike(ctx, b, scr, Q, W, H, t, d, lo) { const k = b.r && b.r.wb, M = WBR.mv; if (!k || !M || WBR.key !== k || !b.scC) return;
  const S = (WB_STRIKE[k] || {})[M.m]; if (!S) return; const f = (t - M.t0) / S[4]; if (f < S[1] || f > S[2]) return; const u = (f - S[1]) / (S[2] - S[1]), env = Math.sin(Math.min(1, u) * Math.PI);
  const tg = []; Q.forEach((q, i) => { if (q.side !== b.superSide && b.n[i] > 0 && scr[i]) tg.push(i); }); if (!tg.length) return;
  const els = k === "epx" ? ((b.r.pent && b.r.pent.length ? b.r.pent : ["ice", "fire", "light", "storm", "nature"]).map(e => WB[WB_EL.find(x => WB[x].el === e)].col)) : [WB[k].col], col = j => els[j % els.length];
  const cx = b.scC.x, cy = b.scC.y, F = M.fx || (M.fx = { hit: {}, snd: 0 }), hit = (x, y, s, key) => { if (F.hit[key]) return; F.hit[key] = 1; b.flashes.push({ x, y, t, r: (26 + s * 30) * d, life: 260 + s * 160, rot: Math.random() * .8 }); b.shake = Math.max(b.shake || 0, (2 + s * 3) * d); };
  if (!F.snd) { F.snd = 1; try { if (S[0] === "wave") SFX.blast(2.4, 0); else SFX.laser(true); } catch (e) {} }
  ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.lineCap = "round";
  const glow = (x, y, r, c, a) => { ctx.globalAlpha = a; ctx.drawImage(glowSprite(c), x - r, y - r, r * 2, r * 2); };
  if (S[0] === "beam" || S[0] === "sweep") { let ex = 0, ey = 0; for (const i of tg) { ex += scr[i].x; ey += scr[i].y; } ex /= tg.length; ey /= tg.length;
    if (S[0] === "sweep") ex += Math.sin((u - .5) * Math.PI) * W * .38; // the Wyrm's sweep: across the whole fleet
    const wide = k === "epx" || M.m === "judgement" ? 1.6 : 1, grow = Math.min(1, u * 5), x1 = cx + (ex - cx) * grow, y1 = cy + (ey - cy) * grow;
    for (const [lw, a, c] of [[46 * wide, .22, col(0)], [20 * wide, .55, col(0)], [7 * wide, .95, "#ffffff"]]) { ctx.globalAlpha = a * env; ctx.strokeStyle = c; ctx.lineWidth = lw * d * (.7 + .3 * Math.sin(t * .05)); ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(x1, y1); ctx.stroke(); }
    if (k === "epx") els.forEach((c, j) => { const a = t * .004 + j * TAU / els.length, o = 14 * d; ctx.globalAlpha = .7 * env; ctx.strokeStyle = c; ctx.lineWidth = 5 * d; ctx.beginPath(); ctx.moveTo(cx + Math.cos(a) * o * 3, cy + Math.sin(a) * o * 3); ctx.lineTo(x1 + Math.cos(a) * o, y1 + Math.sin(a) * o); ctx.stroke(); });
    glow(cx, cy, W * .14 * wide, col(0), .8 * env); if (grow >= 1) { glow(x1, y1, W * .2 * wide, col(0), .9 * env); glow(x1, y1, W * .07 * wide, "#ffffff", env);
      for (const i of tg) if (Math.hypot(scr[i].x - x1, scr[i].y - y1) < W * .22 * wide) hit(scr[i].x, scr[i].y, 1, "b" + i + (S[0] === "sweep" ? Math.round(u * 6) : "")); } }
  else if (S[0] === "wave") { const R = u * Math.hypot(W, H) * 1.05, w0 = (30 - 22 * u) * d;
    for (const [lw, a, c] of [[w0 * 3, .25, col(0)], [w0, .7, col(0)], [w0 * .3, .9, "#ffffff"]]) { ctx.globalAlpha = a * (1 - u * .8); ctx.strokeStyle = c; ctx.lineWidth = lw; ctx.beginPath(); ctx.ellipse(cx, cy, R, R * .82, 0, 0, TAU); ctx.stroke(); }
    if (u < .3) glow(cx, cy, W * (.25 + u), col(0), (1 - u / .3) * .9);
    for (const i of tg) { const p = scr[i], r = Math.hypot(p.x - cx, (p.y - cy) / .82); if (r < R) hit(p.x, p.y, .7, "w" + i); } }
  else { const n = S[3] || 5; for (let j = 0; j < n; j++) { const i = tg[(j * 7 + ((M.t0 / 97) | 0)) % tg.length], p = scr[i], a = (j / n) * .55, v = clamp((u - a) / .35, 0, 1); if (u < a) continue; const c = col(j), sx = cx + Math.cos(j * 2.4) * W * .06, sy = cy + Math.sin(j * 2.4) * W * .04;
    if (v < 1) { const x = sx + (p.x - sx) * v, y = sy + (p.y - sy) * v + (S[0] === "bolts" && (M.m === "rain" || M.m === "mines" || M.m === "hatch") ? -Math.sin(v * Math.PI) * H * .12 : 0), bx = sx + (p.x - sx) * Math.max(0, v - .14), by = sy + (p.y - sy) * Math.max(0, v - .14);
      if (S[0] === "chain") { ctx.globalAlpha = .9; ctx.strokeStyle = c; ctx.lineWidth = 3 * d; ctx.beginPath(); ctx.moveTo(sx, sy); for (let s = 1; s <= 8; s++) { const q = s / 8 * v; ctx.lineTo(sx + (p.x - sx) * q + (Math.random() - .5) * 26 * d, sy + (p.y - sy) * q + (Math.random() - .5) * 26 * d); } ctx.stroke(); ctx.globalAlpha = .3; ctx.lineWidth = 12 * d; ctx.stroke(); }
      else { ctx.globalAlpha = .9; ctx.strokeStyle = c; ctx.lineWidth = 6 * d; ctx.beginPath(); ctx.moveTo(bx, by); ctx.lineTo(x, y); ctx.stroke(); ctx.globalAlpha = .3; ctx.lineWidth = 18 * d; ctx.stroke(); glow(x, y, 16 * d, "#ffffff", .9); } }
    else { hit(p.x, p.y, .6, "j" + j); const age = (u - a - .35) / .2; if (age < 1) { glow(p.x, p.y, W * .07 * (1 + age), c, .9 * (1 - age)); } } } }
  ctx.restore(); ctx.globalAlpha = 1; ctx.globalCompositeOperation = "source-over"; }""")
rep("""      if (b.live && t > WBR.next) { WBR.next = t + 2400 + Math.random() * 1400; const m = wbMoves(key); WBR.b.act(m[(Math.random() * m.length) | 0]); } }""",
    """      if (b.live && t > WBR.next) { WBR.next = t + 2400 + Math.random() * 1400; const m = wbMoves(key), mv = m[(Math.random() * m.length) | 0]; WBR.b.act(mv); WBR.mv = { m: mv, t0: t }; } } /* v407: the move, so its strike plays on the whole field */""")
rep("""  // mega beams from stations, titans and beam batteries: a charge-up glow, then a roaring column with a blinding impact
  b.beams = b.beams.filter(""", """  try { wbStrike(ctx, b, scr, Q, W, H, t, d, lo); } catch (e) {} // v407 the boss's attack across the whole field
  // mega beams from stations, titans and beam batteries: a charge-up glow, then a roaring column with a blinding impact
  b.beams = b.beams.filter(""")
rep("""const A = wbArt(wbk, aw, ah, t, { hp, live: alive.length > 0 }); if (A) ctx.drawImage(A, -aw / 2, -ah / 2, aw, ah); }""", """const A = wbArt(wbk, aw, ah, t, { hp, live: alive.length > 0 }); if (A) ctx.drawImage(wbSoft(A), -aw / 2, -ah / 2, aw, ah); }""")
rep("""function wbStrike(ctx,""", """/* the boss picture with its edges faded, so a beam or wave that runs past its box fades out instead of stopping on a hard straight edge */
function wbSoft(A) { const w = A.width, h = A.height; let c = WBR.soft; if (!c || c.width !== w || c.height !== h) { c = WBR.soft = document.createElement("canvas"); c.width = w; c.height = h; c.m = null; }
  const x = c.getContext("2d"); x.globalCompositeOperation = "copy"; x.drawImage(A, 0, 0); x.globalCompositeOperation = "destination-in";
  if (!c.m) { const m = document.createElement("canvas"); m.width = w; m.height = h; const y = m.getContext("2d"), g = y.createRadialGradient(0, 0, 0, 0, 0, 1); for (const [o, v] of [[0, 1], [.62, 1], [.82, .55], [1, 0]]) g.addColorStop(o, `rgba(0,0,0,${v})`); y.setTransform(w / 2, 0, 0, h / 2, w / 2, h / 2); y.fillStyle = g; y.fillRect(-1, -1, 2, 2); c.m = m; }
  x.drawImage(c.m, 0, 0); x.globalCompositeOperation = "source-over"; return c; }
function wbStrike(ctx,""")
t = t.replace("const GAME_V = 406;", "const GAME_V = 407;")
open(p, "w").write(t); print("ok")
