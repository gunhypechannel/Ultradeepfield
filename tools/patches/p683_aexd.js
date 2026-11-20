/* v683 Aexion's dreadnought form: the ship turns slowly, and only to attack. Each attack is one choreographed beat in real time
   (turn toward the target, fire in step with the model's own animation, hold, turn back, rest), fired from the ship itself:
   missiles from the launch cells along its spine, a broadside rippling down the hull, the rail from the bow, and its own special,
   the Sovereign Rail (a charged spinal beam swept across the whole fleet, at most twice a fight, past 30% and 70%) */
const AEXD = { turn: 1500, hold: 500, rest: 2600 }, AEXD_MS = { missiles: 3000, broadside: 2200, lance: 2600, rail: 4600 }, AEXD_MV = { missiles: "missiles", broadside: "broadside", lance: "rail", rail: "rail" };
const aexdOn = b => !!(b && b.r && b.r.sbk === "aex" && !b.r.sbForm);
function aexdQueue(b, v) { const D = b.aexD || (b.aexD = { n: 0, rails: 0, c: null }); if (b.ending || (b.intro || 0) > 0) return; const t = D.now || performance.now(); if (D.c && t < D.c.end) return;
  const fr = v.t / (b.end || 40); let a; if ((D.rails === 0 && fr > .3) || (D.rails === 1 && fr > .7)) { a = "rail"; D.rails++; } else a = ["missiles", "lance", "broadside"][D.n++ % 3];
  const ms = AEXD_MS[a]; D.c = { a, e: v.e, t0: t, fireAt: t + 9e9, ms, end: t + 9e9, seed: (D.n * 7 + D.rails * 3) % 13, dir: null, hit: {} }; }
function aexdSfx(a, ms) { try { if (!SFX.ok()) return; const at = (f, fn) => setTimeout(() => { try { fn(); } catch (e) {} }, ms * f);
  if (a === "missiles") { for (let j = 0; j < 5; j++) at(.05 + j * .07, () => SFX.laser(false)); at(.5, () => SFX.blast(1.6, 0)); at(.62, () => SFX.blast(1.8, 0)); }
  else if (a === "broadside") { at(.1, () => SFX.blast(1.8, 0)); at(.14, () => SFX.laser(true)); at(.5, () => SFX.blast(2, 0)); at(.54, () => SFX.laser(true)); }
  else if (a === "lance") { mimSfx("hum", 0); at(.38, () => { SFX.laser(true); SFX.blast(2.2, 0); }); }
  else if (a === "rail") { if (SFX.charge) SFX.charge(0); else mimSfx("hum", 0); at(.42, () => { if (SFX.megaBeam) SFX.megaBeam(0); SFX.blast(3, 0); }); at(.6, () => SFX.blast(2.4, 0)); } } catch (e) {} }
function aexdDraw(ctx, b, scr, T, W, H, d, lo, t) { if (!aexdOn(b) || !b.scC) return; const D = b.aexD || (b.aexD = { n: 0, rails: 0, c: null }), dt = D.lt ? t - D.lt : 0; D.lt = t; D.now = t;
  const c = D.c, sm = u => u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u), own = WBR.key === "aex";
  if (c && (b.paused || !b.speed) && dt > 0) { c.t0 += dt; c.fireAt += dt; c.end += dt; } /* a paused replay holds the beat */
  if (!c || t >= c.end) { if (own) WBR.face = 0; return; }
  const B = b.wbBox || { cx: b.scC.x, cy: b.scC.y, aw: W * .6, ah: W * .3 }, cx = B.cx, cy = B.cy, col = (SBW.aex && SBW.aex.col) || "#7ac8ff", gl = glowSprite(col), wh = glowSprite("#ffffff");
  const foes = []; b.Q.forEach((q, i) => { if (q.side !== b.superSide && b.n[i] > 0 && scr[i]) foes.push(i); });
  let mx = 0, my = 0; for (const i of foes) { mx += scr[i].x; my += scr[i].y; } if (foes.length) { mx /= foes.length; my /= foes.length; } else { mx = W / 2; my = H * .75; }
  const spine = cy + B.ah * .06, deck = cy + B.ah * .18, out = p => p.y > deck + B.ah * .1 || Math.abs(p.x - cx) > B.aw * .4, far = foes.filter(i => out(scr[i])); /* squadrons tangling with the hull are not targets for the big guns */
  let fx = 0, fy = 0; for (const i of far) { fx += scr[i].x; fy += scr[i].y; } if (far.length) { fx /= far.length; fy /= far.length; } else { fx = mx; fy = Math.max(my, deck + B.ah * .3); }
  const E = c.a !== "rail" && scr[c.e] && b.n[c.e] > 0 && out(scr[c.e]) ? scr[c.e] : c.a !== "rail" && far.length ? scr[far[c.seed % far.length]] : { x: fx, y: fy };
  if (c.dir == null) { const dx = E.x - cx; c.dir = Math.abs(dx) < W * .06 ? 0 : Math.sign(dx); c.tn = c.dir ? AEXD.turn : 500; c.fireAt = c.t0 + c.tn; c.end = c.fireAt + c.ms + AEXD.hold + c.tn + AEXD.rest + (c.a === "rail" ? 1500 : 0); } /* no side to turn to: a short settle, not a turn */
  const e = t - c.t0, tOut = c.tn + c.ms + AEXD.hold, f = e < c.tn ? sm(e / c.tn) : e < tOut ? 1 : 1 - sm((e - tOut) / c.tn);
  if (own) WBR.face = -c.dir * f; /* the model's bow points the other way to the face sign */ /* the turn is slow and only comes with an attack */
  if (!c.fired && t >= c.fireAt) { c.fired = 1; try { if (own && WBR.b && WBR.b.act) { WBR.b.act(AEXD_MV[c.a]); WBR.mv = { m: AEXD_MV[c.a], t0: t }; } } catch (e2) {} aexdSfx(c.a, c.ms); if (c.a === "rail") try { bVoice(b, "sig"); } catch (e2) {} }
  const u = (t - c.fireAt) / c.ms; if (u < -.25 || u > 1.05) return; const n = foes.length, tgt = j => n ? scr[foes[(j * 5 + c.seed) % n]] : { x: mx, y: my };
  const mo = WBR.mouth && own ? { x: cx + (WBR.mouth.u - .5) * B.aw, y: cy + (WBR.mouth.v - .5) * B.ah } : { x: cx, y: cy + B.ah * .22 }, bow = c.dir ? { x: cx + c.dir * B.aw * .3, y: deck } : mo, glow = (x, y, r, g, a) => { ctx.globalAlpha = a; ctx.drawImage(g, x - r, y - r, r * 2, r * 2); };
  const boom = (k, x, y, s, snd) => { if (c.hit[k]) return; c.hit[k] = 1; aexBoom(b, x, y, t, s, snd); };
  ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.lineCap = "round";
  if (c.a === "missiles") { const N = lo ? 6 : 10;
    if (u < .08) for (let j = 0; j < N; j++) glow(cx + (j / (N - 1) - .5) * B.aw * .34, spine, 7 * d, gl, .4 + .6 * Math.max(0, u + .25) / .33); /* the launch cells open */
    for (let j = 0; j < N; j++) { const lj = .04 + j * .035, v = (u - lj) / .42; if (v < 0) continue; const P0 = { x: cx + (j / (N - 1) - .5) * B.aw * .34, y: spine }, P2 = tgt(j), C1 = { x: P0.x + (P2.x - P0.x) * .15 + (j % 2 ? 1 : -1) * W * .05, y: Math.min(P0.y, P2.y) - H * .14 };
      const at = q => ({ x: (1 - q) * (1 - q) * P0.x + 2 * (1 - q) * q * C1.x + q * q * P2.x, y: (1 - q) * (1 - q) * P0.y + 2 * (1 - q) * q * C1.y + q * q * P2.y });
      if (v < .1) glow(P0.x, P0.y, 16 * d * (1 - v * 8), wh, .9);
      if (v < 1) { const p = at(v); ctx.strokeStyle = col; for (let s2 = 0; s2 < 6; s2++) { const qa = Math.max(0, v - (s2 + 1) * .035), qb = Math.max(0, v - s2 * .035), A1 = at(qa), A2 = at(qb); ctx.globalAlpha = .55 * (1 - s2 / 6); ctx.lineWidth = (4 - s2 * .5) * d; ctx.beginPath(); ctx.moveTo(A1.x, A1.y); ctx.lineTo(A2.x, A2.y); ctx.stroke(); }
        glow(p.x, p.y, 10 * d, gl, .9); glow(p.x, p.y, 4 * d, wh, 1); }
      else boom("m" + j, P2.x, P2.y, 1.1, j % 3 === 0); } }
  else if (c.a === "broadside") { const N = lo ? 5 : 8;
    if (u > 0 && u < .85) { ctx.globalAlpha = .35 * Math.sin(Math.PI * u / .85); ctx.strokeStyle = col; ctx.lineWidth = 3 * d; ctx.beginPath(); ctx.moveTo(cx - B.aw * .3, deck); ctx.lineTo(cx + B.aw * .3, deck); ctx.stroke(); } /* the gun deck lights */
    for (const [si, s0] of [[0, .1], [1, .5]]) for (let j = 0; j < N; j++) { const g = c.dir < 0 ? N - 1 - j : j, gx = cx + (g / (N - 1) - .5) * B.aw * .58, gy = deck, f0 = s0 + j * .025, v = (u - f0) / .16; if (v < 0) continue;
      if (v < .35) { glow(gx, gy, 20 * d * (1 - v), gl, .9); glow(gx, gy, 8 * d, wh, 1 - v * 2); }
      const P = tgt(j * 3 + si * 5); if (v < 1) { const x = gx + (P.x - gx) * v, y = gy + (P.y - gy) * v, bx = gx + (P.x - gx) * Math.max(0, v - .16), by = gy + (P.y - gy) * Math.max(0, v - .16);
        for (const [lw, a2, cc] of [[12, .3, col], [4, .9, "#ffffff"]]) { ctx.globalAlpha = a2; ctx.strokeStyle = cc; ctx.lineWidth = lw * d; ctx.beginPath(); ctx.moveTo(bx, by); ctx.lineTo(x, y); ctx.stroke(); } }
      else boom("b" + si + "_" + j, P.x, P.y, .9, j % 4 === 0); } }
  else if (c.a === "lance") { const dx = E.x - bow.x, dy = E.y - bow.y, dl = Math.hypot(dx, dy) || 1, ux = dx / dl, uy = dy / dl, far = Math.hypot(W, H) * 1.3;
    if (u < .38) { const k = Math.max(0, (u + .25) / .63), r = B.aw * (.02 + .06 * k); glow(bow.x, bow.y, r * 2, gl, .5 + .5 * k); glow(bow.x, bow.y, r * .5, wh, k); ctx.strokeStyle = col; ctx.lineWidth = 2 * d;
      for (let j = 0; j < 7; j++) { const a = j * .9 + t * .005, R = r * (3.4 - k * 2.4); ctx.globalAlpha = .8 * k; ctx.beginPath(); ctx.moveTo(bow.x + Math.cos(a) * R, bow.y + Math.sin(a) * R); ctx.lineTo(bow.x + Math.cos(a) * R * .55, bow.y + Math.sin(a) * R * .55); ctx.stroke(); } }
    else { const k = (u - .38) / .62, ex = bow.x + ux * far, ey = bow.y + uy * far, wd = (k < .38 ? 18 : 18 * (1 - (k - .38) / .62)) * d;
      if (!c.fired2) { c.fired2 = 1; b.shake = Math.max(b.shake || 0, 10 * d); b.flash = Math.max(b.flash || 0, .22); b.slowUntil = Math.max(b.slowUntil || 0, t + 220); for (const i of foes) { const p = scr[i], q2 = (p.x - bow.x) * ux + (p.y - bow.y) * uy, off = Math.abs((p.x - bow.x) * uy - (p.y - bow.y) * ux); if (q2 > 0 && off < W * .06) aexBoom(b, p.x, p.y, t + 80 + q2 * .2, 1.5, off < W * .025); } }
      if (k < .12) glow(bow.x, bow.y, B.aw * .1 * (1 - k / .12), wh, 1);
      for (const [lw, a2, cc] of [[2.4, .3, col], [1, .7, col], [.35, 1, "#ffffff"]]) { ctx.globalAlpha = a2 * (k < .38 ? 1 : 1 - (k - .38) / .62); ctx.strokeStyle = cc; ctx.lineWidth = Math.max(.5, wd * lw); ctx.beginPath(); ctx.moveTo(bow.x, bow.y); ctx.lineTo(ex, ey); ctx.stroke(); } } }
  else if (c.a === "rail") { /* the Sovereign Rail */ const ch = .42, dim = u < 0 ? 0 : u < ch ? u / ch : u < .8 ? 1 : 1 - (u - .8) / .2;
    ctx.save(); ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = .4 * dim; ctx.fillStyle = "rgb(10,16,26)"; ctx.fillRect(-W, -H, W * 3, H * 3); ctx.restore();
    let a0 = Infinity, a1 = -Infinity, R = 0; for (const i of (far.length ? far : foes)) { const p = scr[i], a = Math.atan2(p.y - bow.y, p.x - bow.x); a0 = Math.min(a0, a); a1 = Math.max(a1, a); R = Math.max(R, Math.hypot(p.x - bow.x, p.y - bow.y)); } if (!foes.length) { a0 = 1.2; a1 = 1.9; R = H * .6; }
    const mid = (a0 + a1) / 2, spr = Math.min(.9, Math.max(.25, a1 - a0 + .2)), s0 = mid - spr / 2 * (c.seed % 2 ? 1 : -1), s1 = mid + spr / 2 * (c.seed % 2 ? 1 : -1); R = Math.max(R * 1.3, Math.hypot(W, H));
    if (u < ch) { const k = Math.max(0, (u + .25) / (ch + .25)); /* the hull drains into the bow */
      for (let j = 0; j < 6; j++) { const hx = cx + (j / 5 - .5) * B.aw * .6, hy = (j % 2 ? spine : deck), q = ((t * .0016 + j / 6) % 1); ctx.globalAlpha = .7 * k; ctx.strokeStyle = col; ctx.lineWidth = 2 * d; ctx.beginPath(); ctx.moveTo(hx, hy); ctx.lineTo(bow.x, bow.y); ctx.stroke(); glow(hx + (bow.x - hx) * q, hy + (bow.y - hy) * q, 6 * d, wh, k); }
      const r = B.aw * (.03 + .09 * k); glow(bow.x, bow.y, r * 2, gl, .6 + .4 * k); glow(bow.x, bow.y, r * .55, wh, .4 + .6 * k);
      ctx.strokeStyle = col; ctx.lineWidth = 2.5 * d; for (let j = 0; j < 3; j++) { const q = (k * 2.2 + j / 3) % 1, rr = r * (3.4 - q * 2.8); ctx.globalAlpha = .7 * q; ctx.beginPath(); ctx.ellipse(bow.x, bow.y, rr, rr * .75, 0, 0, TAU); ctx.stroke(); }
      ctx.globalAlpha = .45 * k; ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 1.5 * d; ctx.setLineDash([6 * d, 10 * d]); ctx.beginPath(); ctx.moveTo(bow.x, bow.y); ctx.lineTo(bow.x + Math.cos(s0) * R, bow.y + Math.sin(s0) * R); ctx.stroke(); ctx.setLineDash([]); /* the aim line */ }
    else if (u <= 1) { const k = clamp((u - ch) / (.8 - ch), 0, 1), ease = 1 - Math.pow(1 - k, 2), a = s0 + (s1 - s0) * ease, fade = u < .8 ? 1 : 1 - (u - .8) / .2, wd = 64 * d * (1 - k * .45) * fade;
      if (!c.fired2) { c.fired2 = 1; b.flash = Math.max(b.flash || 0, .7); b.shake = Math.max(b.shake || 0, 24 * d); b.slowUntil = Math.max(b.slowUntil || 0, t + 700); }
      const ex = bow.x + Math.cos(a) * R, ey = bow.y + Math.sin(a) * R;
      for (const [lw, a2, cc] of [[1.8, .25, col], [1, .55, col], [.42, .9, "#eaf8ff"], [.16, 1, "#ffffff"]]) { ctx.globalAlpha = a2 * fade; ctx.strokeStyle = cc; ctx.lineWidth = Math.max(1, wd * lw); ctx.beginPath(); ctx.moveTo(bow.x, bow.y); ctx.lineTo(ex, ey); ctx.stroke(); }
      glow(bow.x, bow.y, B.aw * .14 * fade, gl, .8); glow(bow.x, bow.y, B.aw * .045 * fade, wh, 1);
      for (const i of foes) { const p = scr[i], ap = Math.atan2(p.y - bow.y, p.x - bow.x), past = s1 > s0 ? ap <= a + .04 : ap >= a - .04; if (past && Math.abs(ap - mid) < spr) boom("r" + i, p.x, p.y, 2.2, Object.keys(c.hit).length % 3 === 0); }
      if (u > .8) { const q = (u - .8) / .2, rr = Math.hypot(W, H) * q; ctx.globalAlpha = (1 - q) * .6; ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 6 * d * (1 - q); ctx.beginPath(); ctx.arc(bow.x, bow.y, rr, 0, TAU); ctx.stroke(); } }
    const ta = u < -.1 ? 0 : u < .05 ? (u + .1) / .15 : u < .7 ? 1 : Math.max(0, 1 - (u - .7) / .2); /* the callout */
    if (ta > 0) { ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = ta; ctx.textAlign = "center"; ctx.font = `italic 800 ${20 * d}px Oxanium, sans-serif`; ctx.fillStyle = "#e8f8ff"; ctx.shadowColor = col; ctx.shadowBlur = 18 * d; ctx.fillText("SOVEREIGN RAIL", W / 2, H * .17); ctx.font = `600 ${10 * d}px Oxanium, sans-serif`; ctx.shadowBlur = 0; ctx.fillStyle = "#9fd8ff"; ctx.fillText("AEXION'S SPINAL CANNON", W / 2, H * .17 + 18 * d); ctx.textAlign = "left"; } }
  ctx.restore(); ctx.globalAlpha = 1; ctx.globalCompositeOperation = "source-over"; }
/* v683 a boss raises its shield again (the sim's v8 shield pulse): a hex bubble flashes round it */
function bShDraw(ctx, b, W, H, d, T, t) { if (b.superSide == null || !b.scC || !b.R || !b.R.frames) return; let sh = 0, n = 0; b.Q.forEach((q, i) => { if (q.side === b.superSide && q.shPer > 0 && b.n[i] > 0) { sh += bPos(b, i, T).sh || 0; n++; } }); if (!n) return; sh /= n;
  if (b.bShL != null && sh - b.bShL > .2 && T > .5) { b.bSh = { t0: t }; try { mimSfx("hum", 0); } catch (e) {} } b.bShL = sh; const S = b.bSh; if (!S) return; const u = (t - S.t0) / 1700; if (u < 0 || u > 1) return;
  const B = b.wbBox || { cx: b.scC.x, cy: b.scC.y, aw: W * .6, ah: W * .3 }, rx = B.aw * .5, ry = Math.max(B.ah * .55, rx * .45), col = b.r.sbk && SBW[b.r.sbk] ? SBW[b.r.sbk].col : b.r.wb && WB[b.r.wb] ? WB[b.r.wb].col : "#5dff7a", env = u < .15 ? u / .15 : 1 - (u - .15) / .85;
  ctx.save(); ctx.globalCompositeOperation = "lighter"; const s = u < .3 ? .7 + .3 * (u / .3) : 1;
  ctx.beginPath(); ctx.ellipse(B.cx, B.cy, rx * s, ry * s, 0, 0, TAU); ctx.save(); ctx.clip(); const g = ctx.createRadialGradient(B.cx, B.cy, 0, B.cx, B.cy, rx * s); g.addColorStop(0, "rgba(0,0,0,0)"); g.addColorStop(.75, col); g.addColorStop(1, "#ffffff"); ctx.globalAlpha = .22 * env; ctx.fillStyle = g; ctx.fillRect(B.cx - rx, B.cy - ry, rx * 2, ry * 2);
  const hs = 15 * d, sw = u * rx * 2.4; ctx.strokeStyle = col; ctx.lineWidth = 1.4 * d; for (let y = B.cy - ry, r = 0; y < B.cy + ry + hs; y += hs * .87, r++) for (let x = B.cx - rx + (r % 2) * hs * .75; x < B.cx + rx + hs; x += hs * 1.5) { const dd = Math.hypot((x - B.cx) / rx, (y - B.cy) / ry), on = Math.abs(dd * rx - sw * .5) < rx * .35 ? 1 : .25; ctx.globalAlpha = env * .55 * on * dd; ctx.beginPath(); for (let k = 0; k <= 6; k++) { const a = k * Math.PI / 3; ctx[k ? "lineTo" : "moveTo"](x + Math.cos(a) * hs * .48, y + Math.sin(a) * hs * .48); } ctx.stroke(); }
  ctx.restore(); ctx.globalAlpha = .85 * env; ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2.5 * d; ctx.beginPath(); ctx.ellipse(B.cx, B.cy, rx * s, ry * s, 0, 0, TAU); ctx.stroke(); ctx.globalAlpha = .5 * env; ctx.strokeStyle = col; ctx.lineWidth = 8 * d; ctx.stroke();
  ctx.restore(); ctx.globalAlpha = 1; }
