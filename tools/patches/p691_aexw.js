/* v691 Aexion's Warform remastered (owner: "slow aexions war form turning speed and frequency in battle simulator, also his attacks
   need to be timed better with his animation"). The Warform used the generic boss fencing cycle (a 0.65 s snap to a random side
   every ~6 s, whatever he was doing), and his lance, sweep and time fracture were drawn on the fight's clock while the model played
   its move on the real one, so the beam left before the arm came up. Now each attack is one beat in real time, like the dreadnought:
   - he turns only when his target is on another side, and slowly (2.6 s a side, eased in and out), then holds that facing;
   - a short warning glow where the attack comes from;
   - the model's move starts, and the strike on the field lands on the model's own key frame (the lance on its release, the sweep as
     the blade crosses, the fracture's snap as the overdrive ends; missiles and broadside follow the model's cells and cannons);
   - a hold, then about 3 s of rest before the next attack. Damage is unchanged: this is the picture only. */
const AEXW = { turn: 2600, warn: 450, hold: 600, rest: 3000 }, AEXW_MS = { lance: 3200, sweep: 2600, missiles: 3000, broadside: 2200, frac: 4200 };
const AEXW_MAP = { lance: [[0, 0], [.3, .32], [.85, 1]], sweep: [[0, 0], [.3, .25], [.52, .7], [1, 1]], frac: [[0, 0], [.15, .2], [.85, .78], [1, 1]] }; /* model time -> the drawn effect's own time, so its strike sits on the model's key frame */
const aexwOn = b => !!(b && b.r && b.r.sbk === "aex" && b.r.sbForm);
function aexwQueue(b, v) { const D = b.aexW || (b.aexW = { n: 0, fr: 0, c: null, face: 0 }); if (b.ending || (b.intro || 0) > 0) return; const t = D.now || performance.now(); if (D.c && t < D.c.end) return;
  const fr = v.t / (b.end || 40); let a; if ((D.fr === 0 && fr > .3) || (D.fr === 1 && fr > .7)) { a = "frac"; D.fr++; } else a = ["lance", "missiles", "sweep", "broadside"][D.n++ % 4];
  D.c = { a, e: v.e, t0: t, seed: (D.n * 7 + D.fr * 3) % 13, dir: null, end: t + 9e9 }; }
function aexwU(m, t) { const P = AEXW_MAP[m.a], e = (t - m.rt) / m.Dr; if (!P) return e; if (e <= 0) return e * P[1][1] / P[1][0];
  for (let i = 1; i < P.length; i++) if (e <= P[i][0]) { const [a0, b0] = P[i - 1], [a1, b1] = P[i]; return b0 + (e - a0) / (a1 - a0) * (b1 - b0); }
  const [a0, b0] = P[P.length - 2], [a1, b1] = P[P.length - 1]; return b1 + (e - a1) / Math.max(.05, a1 - a0) * (b1 - b0) * .5; }
function aexwSfx(a, ms) { try { if (!SFX.ok()) return; const at = (f, fn) => setTimeout(() => { try { fn(); } catch (e) {} }, ms * f);
  if (a === "lance") { mimSfx("hum", 0); at(.3, () => { SFX.laser(true); SFX.blast(2, 0); }); }
  else if (a === "sweep") { mimSfx("hum", 0); at(.36, () => { mimSfx("whip", 0); SFX.blast(2.4, 0); }); }
  else if (a === "frac") { aexSfx("frac"); at(.85, () => SFX.blast(3, 0)); } } catch (e) {} }
function aexwDraw(ctx, b, scr, T, W, H, d, lo, t) { if (!aexwOn(b) || !b.scC) return; const D = b.aexW || (b.aexW = { n: 0, fr: 0, c: null, face: 0 }), dt = D.lt ? t - D.lt : 0; D.lt = t; D.now = t;
  const c = D.c, own = WBR.key === "aex", sm = u => u <= 0 ? 0 : u >= 1 ? 1 : u * u * u * (u * (u * 6 - 15) + 10); /* smootherstep: a heavy start and a soft stop */
  if (c && (b.paused || !b.speed) && dt > 0) { c.t0 += dt; if (c.fireAt) c.fireAt += dt; c.end += dt; const m = c.m; if (m) m.rt += dt; } /* a paused replay holds the beat */
  if (!c) { if (own) WBR.face = D.face; return; }
  const B = b.wbBox || { cx: b.scC.x, cy: b.scC.y, aw: W * .6, ah: W * .3 }, cx = B.cx, cy = B.cy;
  if (c.dir == null) { const foes = []; b.Q.forEach((q, i) => { if (q.side !== b.superSide && b.n[i] > 0 && scr[i]) foes.push(i); }); let mx = 0; for (const i of foes) mx += scr[i].x; mx = foes.length ? mx / foes.length : cx;
    const ex = c.a !== "frac" && c.a !== "sweep" && scr[c.e] && b.n[c.e] > 0 ? scr[c.e].x : mx, dx = ex - cx; c.dir = Math.abs(dx) < W * .1 ? 0 : Math.sign(dx); c.from = D.face;
    c.tn = c.dir === c.from ? 300 : AEXW.turn * (Math.abs(c.dir - c.from) > 1 ? 1.4 : 1); c.fireAt = c.t0 + c.tn + AEXW.warn; c.ms = AEXW_MS[c.a]; c.end = c.fireAt + c.ms + AEXW.hold + AEXW.rest + (c.a === "frac" ? 1500 : 0); }
  const e = t - c.t0, f = c.tn > 300 ? sm(e / c.tn) : 1, face = c.from + (c.dir - c.from) * f; if (f >= 1) D.face = c.dir; if (own) WBR.face = face; /* turns only toward a target on another side, then keeps that facing */
  if (t < c.fireAt && t > c.fireAt - AEXW.warn - 150) { /* the warning: the weapon lights before it fires */ const k = clamp(1 - (c.fireAt - t) / (AEXW.warn + 150), 0, 1), col = (SBW.aex && SBW.aex.col) || "#7ac8ff", g = glowSprite(col), w = glowSprite("#ffffff");
    const sx = c.dir || 0, P = c.a === "sweep" ? [{ x: cx + (sx || 1) * B.aw * .22, y: cy + B.ah * .05 }] : c.a === "missiles" ? [-.18, -.06, .06, .18].map(o => ({ x: cx + o * B.aw, y: cy - B.ah * .12 })) : c.a === "broadside" ? [-.2, .2].map(o => ({ x: cx + o * B.aw, y: cy + B.ah * .02 })) : [{ x: cx + sx * B.aw * .06, y: cy + B.ah * .02 }];
    ctx.save(); ctx.globalCompositeOperation = "lighter"; for (const p of P) { const r = B.aw * (c.a === "frac" ? .16 : .07) * (.6 + .4 * k) * (1 + .12 * Math.sin(t * .03)); ctx.globalAlpha = .75 * k; ctx.drawImage(g, p.x - r, p.y - r, r * 2, r * 2); ctx.globalAlpha = k; ctx.drawImage(w, p.x - r * .3, p.y - r * .3, r * .6, r * .6); } ctx.restore(); }
  if (!c.fired && t >= c.fireAt) { c.fired = 1; bossAct(b, c.a, t); aexwSfx(c.a, c.ms); if (c.a === "frac") try { bVoice(b, "sig"); } catch (e2) {}
    if (AEXW_MAP[c.a]) { const A = b.aexA || (b.aexA = []); c.m = { a: c.a, t0: -1e9, e: c.e, seed: c.seed, rt: t, Dr: c.ms, snd: 1 }; A.push(c.m); if (A.length > 8) A.shift(); } } }
