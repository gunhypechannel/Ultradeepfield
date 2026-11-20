/* ---------- v678 cinematic replays (owner: "slow the battle down in a cinematic style but keep the same damage; movie finish") ----------
   The replay is a playback of a battle already settled, so nothing here touches damage, losses or the result. Cinematic mode (the
   default; 🎞 in the replay bar, ⚡ for quick):
   - the clock runs at CINE_PACE (62%) of normal, and slow motion still deepens on big kills and Mimic hits;
   - volleys land on a beat (cineDue): one side on the beat, the other on the off-beat, so fire comes in answering waves;
   - a director (cineDirect) frames each moment: opening shots of each fleet, then the biggest thing about to happen (a Cube
     Destroyer beam, a Titan's shot, a Mimic's tentacles or Omega's beam, the heaviest salvo), a wide shot every third cut, and the
     winner at the end; shots hold about two seconds and the camera eases slowly between them; tap 🎬 for the free camera;
   - a film look: letterbox bars that close in for the opening and the finish, and a light grain (not on low effects). */
const CINE_PACE = .62, CINE_BEAT = .2;
const cineOn = () => { try { return localStorage.getItem("udf.cineRep") !== "0"; } catch (e) { return true; } };
const cineIntro = ms => cineOn() ? Math.max(ms, 3000) : ms;
function cineDue(b, v, T) { if (!b.cine) return v.t <= T; const off = (b.Q[v.s] && b.Q[v.s].side === "d") ? CINE_BEAT / 2 : 0; return Math.ceil((v.t - off) / CINE_BEAT - 1e-6) * CINE_BEAT + off <= T; }
function cineDirect(b, t, T, W, H) { const P = b.lastP; if (!P || !P.length || !W) return; const C = b.cdir || (b.cdir = { n: 0 });
  const at = i => { const j = b.repOf && b.repOf[i] != null ? b.repOf[i] : i, p = P.find(q => q.i === j); return p ? [p.x, p.y] : null; };
  const mid = (i, j) => { const a = at(i), c = at(j); return a && c ? [(a[0] + c[0]) / 2, (a[1] + c[1]) / 2] : a || c; };
  const ctr = sd => { let x = 0, y = 0, w = 0; for (const p of P) { const q = b.Q[p.i]; if (!q || q.side !== sd) continue; const k = (p.rx || 1) * (p.ry || 1); x += p.x * k; y += p.y * k; w += k; } return w ? [x / w, y / w] : null; };
  const shot = (p, s, hold, tag) => { if (!p) return false; b.focus = { s, x: clamp(p[0] / W, .18, .82), y: clamp(p[1] / H, .18, .82), until: t + hold, cine: tag || 1 }; C.n++; return true; };
  if (b.done) return;
  if (b.ending || T >= b.end - .05) { if (C.fin) return; C.fin = 1; shot(ctr((b.res && b.res.winner) || "a") || [W / 2, H / 2], 1.3, 6000, "fin"); return; } /* act three: the winner */
  if (b.focus && t < b.focus.until) return;
  if (b.intro > 0) { if (!C.o1) { C.o1 = 1; shot(ctr("a"), 1.35, 1400, "open"); } else if (!C.o2) { C.o2 = 1; shot(ctr("d"), 1.35, 1400, "open"); } return; } /* act one: each fleet */
  if (C.n % 3 === 2) { b.focus = { s: 1, x: .5, y: .5, until: t + 2000, cine: "wide" }; C.n++; return; }
  for (const m of b.mAtk || []) { const u = (T - m.t0) / MIM_DUR[m.a]; if (u > -.4 && u < .5 && /storm|omega|grab|slam|claw|lance/.test(m.a)) { if (shot(mid(m.s, m.e), m.a === "omegaX" ? 1.12 : 1.55, m.a === "omegaX" ? 3400 : 2300, "mim")) return; } }
  for (const m of (b.beams || []).concat(b.cdQ || [])) { if ((m.wb || m.ti) && m.t0 > T - .3 && m.t0 < T + 1.4) { if (shot(mid(m.s, m.e), 1.5, 2400, "beam")) return; } }
  let best = null, bd = 0; for (let k = b.vi; k < b.R.vols.length; k++) { const v = b.R.vols[k]; if (v.t > T + 1.1) break; const w = (v.dead || 0) * (unitCost((b.Q[v.e] || {}).k) || 1); if (w > bd) { bd = w; best = v; } }
  if (best && shot(mid(best.s, best.e), 1.45, 2000, "salvo")) return;
  b.focus = { s: 1, x: .5, y: .5, until: t + 1800, cine: "wide" }; C.n++; }
let CINE_GR = null;
function cineLook(ctx, b, W, H, top, bot, t, lo) { if (lo) return; const T = b.simT, fh = bot - top, opening = b.intro > 0 ? 1 : 0, closing = b.ending || T >= b.end - .05 ? 1 : 0, k = b.lbK = (b.lbK == null ? 1 : b.lbK) + (((opening || closing) ? 1 : .55) - (b.lbK == null ? 1 : b.lbK)) * .04, h = fh * .075 * k;
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = "#000"; ctx.globalAlpha = .9; ctx.fillRect(0, top - 2, W, h + 2); ctx.fillRect(0, bot - h, W, h + 2);
  if (!CINE_GR) { CINE_GR = document.createElement("canvas"); CINE_GR.width = CINE_GR.height = 128; const x = CINE_GR.getContext("2d"), D = x.createImageData(128, 128); for (let i = 0; i < D.data.length; i += 4) { const v = Math.random() * 255 | 0; D.data[i] = D.data[i + 1] = D.data[i + 2] = v; D.data[i + 3] = 255; } x.putImageData(D, 0, 0); }
  ctx.globalAlpha = .045; ctx.globalCompositeOperation = "overlay"; const ox = (t * 7.3) % 128 | 0, oy = (t * 3.1) % 128 | 0; const pat = ctx.createPattern(CINE_GR, "repeat"); ctx.translate(-ox, -oy); ctx.fillStyle = pat; ctx.fillRect(0, 0, W + 128, H + 128); ctx.restore(); }
