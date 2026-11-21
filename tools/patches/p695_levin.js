/* ---------- v695 the Leviathan's arrival (owner: "what can we do to make his intro more visually impressive?" ... "Please build it all") ----------
   A 15-second directed entrance, played once per Leviathan event the first time you open the map while it is live (and from the Boss Lab):
   1. a fiery rift tears open at the edge of the galaxy (wide shot, a low rumble);
   2. he surges out head first and his body unspools ring by ring behind him, each ring leaving the rift with a flash, a small
      shockwave and a thump, while a chase camera runs along his flank;
   3. a three-quarter head-on shot: the jaws open with a roar and a river of fire;
   4. the camera pulls back as he settles into place with a shockwave, and the title card names him;
   5. then the Advisor's line, and the usual scan view (from the Boss Lab) or the map.
   Throughout: embers stream off his body, worlds he passes glow orange, and the camera keeps clear of stars and planets (every
   cinematic camera does now: it used to fly straight through the binary suns at the galaxy's edge). Skip with the button. */
const LEVIN = { len: 15000, a: 2600, c: 8200, d: 11600 };
function levRoar() { try { if (!SFX.ok()) return; const c = AU.ctx, t = c.currentTime;
  for (const [f0, ty, a] of [[66, "sawtooth", .3], [99, "sawtooth", .18], [48, "square", .14]]) { const o = c.createOscillator(), fl = c.createBiquadFilter(), lfo = c.createOscillator(), lg = c.createGain();
    o.type = ty; o.frequency.setValueAtTime(f0 * 1.3, t); o.frequency.exponentialRampToValueAtTime(f0, t + .45); o.frequency.exponentialRampToValueAtTime(f0 * .55, t + 2.5);
    lfo.frequency.value = 21 + f0 % 7; lg.gain.value = f0 * .09; lfo.connect(lg); lg.connect(o.frequency); fl.type = "lowpass"; fl.frequency.setValueAtTime(260, t); fl.frequency.linearRampToValueAtTime(1500, t + .35); fl.frequency.exponentialRampToValueAtTime(220, t + 2.5);
    o.connect(fl); SFX.bv(fl, t, a, 2.7, 0, .6, .22); o.start(t); lfo.start(t); o.stop(t + 2.8); lfo.stop(t + 2.8); }
  SFX.blast(2.6, 0); } catch (e) {} }
function levRumble(dur) { try { if (!SFX.ok()) return; const c = AU.ctx, t = c.currentTime; for (const f of [37, 40.5, 55]) { const o = c.createOscillator(); o.type = f > 50 ? "triangle" : "sine"; o.frequency.setValueAtTime(f, t); o.frequency.linearRampToValueAtTime(f * 1.12, t + dur / 1000); SFX.bv(o, t, f > 50 ? .08 : .22, dur / 1000, 0, .5, 1.1); o.start(t); o.stop(t + dur / 1000 + .1); } } catch (e) {} }
function levInDom() { let el = document.getElementById("levin"); if (el) return el;
  if (!document.getElementById("levinCss")) { const st = document.createElement("style"); st.id = "levinCss"; st.textContent = `#levin{position:fixed;inset:0;z-index:240;pointer-events:none}
#levin .lb{position:absolute;left:0;right:0;height:0;background:#000;transition:height .7s ease}#levin .lb.t{top:0}#levin .lb.b{bottom:0}#levin.on .lb{height:9vh}
#levin .fl{position:absolute;inset:0;background:#fff4e0;opacity:0}#levin .tt{position:absolute;left:0;right:0;top:58%;text-align:center;opacity:0;transform:scale(1.1);transition:opacity .9s ease,transform 3.2s ease-out;color:#ffe2c0;font-family:var(--f-display),sans-serif;font-weight:800;font-size:clamp(22px,7.2vw,58px);letter-spacing:.22em;padding-left:.22em;white-space:nowrap;text-shadow:0 0 16px #ff6a20,0 0 44px rgba(255,90,20,.65)}
#levin .tt small{display:block;font-family:var(--f-ui),sans-serif;font-weight:700;font-size:clamp(9px,2.6vw,13px);letter-spacing:.3em;color:#ffa060;margin-top:12px;text-shadow:0 0 10px rgba(255,90,20,.6)}#levin.tton .tt{opacity:1;transform:scale(1)}
#levin .sk{position:absolute;right:max(14px,env(safe-area-inset-right,0px));top:calc(9vh + 12px);pointer-events:auto;background:rgba(0,0,0,.55);border:1px solid rgba(255,160,90,.5);color:#ffd8b0;border-radius:999px;padding:7px 15px;font-family:var(--f-ui),sans-serif;font-weight:600;font-size:13px;opacity:0;transition:opacity .6s}#levin.on .sk{opacity:1}`; document.head.appendChild(st); }
  el = document.createElement("div"); el.id = "levin"; el.innerHTML = `<div class="lb t"></div><div class="lb b"></div><div class="fl"></div><div class="tt">THE LEVIATHAN<small>WORLD BOSS · THREAT CATASTROPHIC</small></div><button class="sk" type="button">Skip ›</button>`;
  document.body.appendChild(el); el.querySelector(".sk").onclick = () => levInEnd(1); return el; }
function levFlash(a, ms) { const f = document.querySelector("#levin .fl"); if (!f) return; f.style.transition = "none"; f.style.opacity = a; void f.offsetWidth; f.style.transition = `opacity ${ms}ms ease-out`; f.style.opacity = 0; }
function levIntroStart(lab) { if (G.levIn || !G3) return false; const W = G3; closeSheet(); if (view !== "galaxy") { view = "galaxy"; render(); }
  const c = W.cam; try { if (c.followMv) followMvEnd(W, 1); } catch (e) {} try { wbScanOff(); } catch (e) {} c.follow = null; c.followFleet = null; c.vel = null; c.cineObj = null; c.cine = { m: "levin" }; c.goal = null;
  try { const q = P3(WBO.lev, now()); c.tx = q.x; c.ty = q.y; c.tz = q.z; c.dist = Math.min(c.dist, 260); } catch (e) {} /* near enough for the model to be built */
  $("#app").classList.add("cine"); const bar = $("#cinebar"); if (bar) bar.remove(); G.levIn = { t0: performance.now(), lab: !!lab, ring: -1, beats: {} }; G.cineOn = 1;
  const el = levInDom(); requestAnimationFrame(() => el.classList.add("on")); levRumble(3200); return true; }
function levInEnd(skip) { const L = G.levIn; if (!L) return; G.levIn = null; G.cineOn = 0; const W = G3, M = W && W.wbM && W.wbM.lev;
  if (M && M.b) { M.b.noTw = 0; if (M.b.ring) M.b.ring.k = 1; M.next = performance.now() + 6000; } if (W && W.levFx) W.levFx.g.visible = false;
  const el = document.getElementById("levin"); if (el) { el.classList.remove("on", "tton"); setTimeout(() => { try { el.remove(); } catch (e) {} }, 800); }
  if (W) { const c = W.cam, P = W.camera.position, Lk = L.look || { x: 0, y: 0, z: 0 }, dx = P.x - Lk.x, dy = P.y - Lk.y, dz = P.z - Lk.z, dist = Math.hypot(dx, dy, dz) || 1;
    c.tx = Lk.x; c.ty = Lk.y; c.tz = Lk.z; c.dist = dist; c.ph = Math.acos(clamp(dy / dist, -1, 1)); c.th = Math.atan2(dz, dx); c.cine = null; c.goal = null; $("#app").classList.remove("cine"); } /* the map camera picks up exactly where the shot ended */
  if (L.lab) setTimeout(() => { try { cineObjStart("wb_lev"); } catch (e) {} }, 200);
  setTimeout(() => { try { if (ADV_NEWS.wb_new_lev) advHolo(ADV_NEWS.wb_new_lev); } catch (e) {} }, skip ? 400 : 900); }
/* the effects: a pool of sprites and two ring meshes, made once */
function levFxKit(W) { if (W.levFx) return W.levFx; const g = new TH.Group(); g.visible = false; W.scene.add(g); const tx = glowTex("255,255,255", 1), sp = (col, ro) => { const s = new TH.Sprite(W.additive(tx, col, 0)); s.renderOrder = ro || 14; s.visible = false; g.add(s); return s; };
  const rgeo = new TH.RingGeometry(.86, 1, 72), ring = col => { const m = new TH.Mesh(rgeo, new TH.MeshBasicMaterial({ color: col, transparent: true, opacity: 0, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false })); m.visible = false; m.frustumCulled = false; g.add(m); return m; };
  W.levFx = { g, rift: [sp(0xff5a14, 15), sp(0xffb060, 16), sp(0xfff0d8, 17), sp(0xff3a0a, 15)], emb: Array.from({ length: MOBILE ? 36 : 64 }, () => ({ s: sp(0xff8a30, 16), t0: -1e9, p: new TH.Vector3(), v: new TH.Vector3() })), pl: Array.from({ length: 8 }, () => sp(0xff7a30, 13)),
    flash: [sp(0xffe0b0, 17), sp(0xffe0b0, 17), sp(0xffe0b0, 17)], fi: 0, waves: [ring(0xff8a40), ring(0xff8a40), ring(0xffc080)], wi: 0, last: 0 };
  return W.levFx; }
const levEase = u => u <= 0 ? 0 : u >= 1 ? 1 : u * u * u * (u * (u * 6 - 15) + 10);
/* called from wbMapFx each frame for the Leviathan (ring mode): unspools the body out of the rift and runs the effects */
function levInFx(W, M, t, T) { const L = G.levIn; if (!L || !M || !M.b || !M.b.ring) return; const RG = M.b.ring, e = L.fz != null ? L.fz : t - L.t0, s = RG.s, Lf = TAU * .465, aF = RG.a, aR = aF - Lf, F = levFxKit(W); F.g.visible = true; M.next = t + 20000;
  if (e > LEVIN.len) return levInEnd(0);
  const p = levEase(clamp((e - LEVIN.a) / 5600, 0, 1)); RG.k = 1; RG.a = aR + Lf * Math.max(.003, p); RG.cut = aR; M.b.noTw = 1; M.b.grp.visible = e > LEVIN.a - 150; L.p = p; /* head first out of the rift: the body behind it is still on the other side (hidden past the cut) */
  const R0 = RG.R0, y0 = RG.y, P = a => ({ x: Math.cos(a) * R0, y: y0, z: Math.sin(a) * R0 }), rp = P(aR), hp = P(RG.a); L.aR = aR; L.aF = aF; L.hA = RG.a; L.s = s; L.R0 = R0; L.y0 = y0; L.hp = hp; L.rp = rp;
  /* the rift: a vertical tear of fire, flickering; it closes once the tail is through */
  const open = clamp(e / 900, 0, 1) * (1 - clamp((e - 9000) / 1500, 0, 1)), fl = .85 + .15 * Math.sin(t * .031) * Math.sin(t * .017);
  F.rift.forEach((sp, i) => { sp.visible = open > .01; if (!sp.visible) return; sp.position.set(rp.x, rp.y + s * .3, rp.z); const w = [s * 7, s * 3, s * 1, s * 18][i] * (.6 + .4 * open), h = [s * 22, s * 17, s * 13, s * 10][i] * open; sp.scale.set(w * fl, h * (.95 + .05 * fl), 1); sp.material.opacity = [.75, .85, 1, .35][i] * open * fl; });
  /* each ring leaving the rift: a flash, a small shockwave, a thump */
  const N = M.b.N || 24, out = e < LEVIN.a ? -1 : Math.floor(p * N); if (out > L.ring && out < N) { for (let r = L.ring + 1; r <= out; r++) { if (r % 2) continue; const fs = F.flash[F.fi++ % F.flash.length]; fs.userData.t0 = t; fs.userData.big = 0; const wv = F.waves[F.wi++ % 2]; wv.userData = { t0: t, s: s * 3, life: 700, p: rp }; } L.ring = out; try { if (SFX.ok() && t - (L.thump || 0) > 260) { L.thump = t; SFX.blast(1.2, 0); } } catch (e2) {} }
  for (const fs of F.flash) { const a = fs.userData.t0 ? (t - fs.userData.t0) / 380 : 2; fs.visible = a < 1; if (fs.visible) { fs.position.set(rp.x, rp.y + s * .3, rp.z); fs.scale.setScalar(s * (fs.userData.big ? 30 : 9) * (.5 + a)); fs.material.opacity = (1 - a) * .95; } }
  for (const wv of F.waves) { const u = wv.userData && wv.userData.t0 ? (t - wv.userData.t0) / wv.userData.life : 2; wv.visible = u < 1; if (!wv.visible) continue; const q = wv.userData.p; wv.position.set(q.x, q.y, q.z); wv.rotation.set(-Math.PI / 2, 0, 0); wv.scale.setScalar(wv.userData.s * (.2 + u * 1.6)); wv.material.opacity = (1 - u) * .85; }
  /* settling: one big shockwave round him, and the jaws: a roar and fire, in the head-on shot */
  if (e > LEVIN.c + 500 && !L.beats.roar) { L.beats.roar = 1; try { M.b.act("lens"); } catch (e2) {} levRoar(); levFlash(.35, 500); }
  if (e > LEVIN.d + 200 && !L.beats.settle) { L.beats.settle = 1; const wv = F.waves[2]; wv.userData = { t0: t, s: s * 60, life: 2200, p: hp }; const fs = F.flash[0]; fs.userData.t0 = t; fs.userData.big = 1; try { SFX.blast(3, 0); } catch (e2) {} }
  if (e > LEVIN.d + 400 && !L.beats.title) { L.beats.title = 1; const el = document.getElementById("levin"); if (el) el.classList.add("tton"); }
  if (e > LEVIN.len - 1300 && !L.beats.ttoff) { L.beats.ttoff = 1; const el = document.getElementById("levin"); if (el) el.classList.remove("tton"); }
  /* embers streaming off the emerged body */
  const dt = Math.min(60, t - (F.last || t)); F.last = t; let spawn = e > LEVIN.a - 400 ? Math.ceil(dt / 16 * (MOBILE ? 1 : 2)) : 0;
  for (const m of F.emb) { const age = (t - m.t0) / 1700; if (age >= 1 && spawn > 0) { spawn--; const u = Math.random() * (e < LEVIN.a ? .02 : p), a = RG.a - u * Lf; m.p.set(Math.cos(a) * R0, y0 + (Math.random() - .3) * s * 1.2, Math.sin(a) * R0); if (e < LEVIN.a + 600) m.p.set(rp.x + (Math.random() - .5) * s * 2, rp.y + (Math.random() - .5) * s * 8, rp.z + (Math.random() - .5) * s * 2);
      m.v.set(Math.cos(a) * (.4 + Math.random()), .6 + Math.random() * 1.2, Math.sin(a) * (.4 + Math.random())).multiplyScalar(s * .0016); m.t0 = t; continue; }
    m.s.visible = age < 1; if (!m.s.visible) continue; m.p.addScaledVector(m.v, dt); m.s.position.copy(m.p); m.s.scale.setScalar(s * (.55 + .5 * Math.sin(age * 9 + m.t0)) * (1 - age * .6)); m.s.material.opacity = (age < .1 ? age / .1 : 1 - age) * .9; }
  /* worlds he passes glow orange */
  const near = []; if (W.planets) for (const [, o] of W.planets) { if (!o.grp || !o.grp.visible) continue; const q = o.grp.position; let best = 1e9; for (let j = 0; j <= 6; j++) { const a = RG.a - j / 6 * Lf * p; best = Math.min(best, Math.hypot(q.x - Math.cos(a) * R0, q.z - Math.sin(a) * R0)); } if (best < s * 26) near.push([best, o]); }
  near.sort((x, y) => x[0] - y[0]); F.pl.forEach((sp, i) => { const n = near[i]; sp.visible = !!n && e > LEVIN.a; if (!sp.visible) return; const o = n[1], q = o.grp.position, kk = 1 - n[0] / (s * 26); sp.position.copy(q); sp.scale.setScalar((o.rad || 2) * 7 * (o.grp.scale.x || 1)); sp.material.opacity = .55 * kk * (.85 + .15 * Math.sin(t * .02 + i)); }); }
/* the shots */
function levInCam(W, t) { const L = G.levIn; if (!L || L.hp == null) return; const e = L.fz != null ? L.fz : t - L.t0, s = L.s, ah = L.hA, fw = { x: -Math.sin(ah), z: Math.cos(ah) }, ou = { x: Math.cos(ah), z: Math.sin(ah) }, H = L.hp;
  const at = (B, f, o, u) => ({ x: B.x + fw.x * f + ou.x * o, y: B.y + u, z: B.z + fw.z * f + ou.z * o }); let pos, look;
  if (e < LEVIN.a) { const k = e / LEVIN.a, R = L.rp, rf = { x: -Math.sin(L.aR), z: Math.cos(L.aR) }, ro = { x: Math.cos(L.aR), z: Math.sin(L.aR) }, d = 1 - .18 * levEase(k);
    pos = { x: R.x + (-ro.x * 24 + rf.x * 18) * s * d, y: R.y + s * 7 * d, z: R.z + (-ro.z * 24 + rf.z * 18) * s * d }; look = { x: R.x, y: R.y + s * 1.5, z: R.z }; } /* wide on the rift */
  else if (e < LEVIN.c) { if (!L.cutB) { L.cutB = 1; levFlash(.7, 260); } const k = (e - LEVIN.a) / (LEVIN.c - LEVIN.a); pos = at(H, -s * (15 - 4 * k), -s * (8 + 2 * Math.sin(k * 3)), s * (4.5 - 1.5 * k)); look = at(H, s * 6, 0, s * .5); } /* the chase along his flank */
  else if (e < LEVIN.d) { if (!L.cutC) L.cutC = 1; const k = (e - LEVIN.c) / (LEVIN.d - LEVIN.c); pos = at(H, s * (17 - 3 * levEase(k)), -s * 7, s * 2.6); look = at(H, 0, 0, s * .4); } /* three-quarter head-on: the roar */
  else { const k = levEase(clamp((e - LEVIN.d) / 3000, 0, 1)), A = at(H, s * 14, -s * 7, s * 2.6), B = at(H, -s * 12, -s * 46, s * 28); pos = { x: A.x + (B.x - A.x) * k, y: A.y + (B.y - A.y) * k, z: A.z + (B.z - A.z) * k }; const LA = at(H, 0, 0, s * .4), LB = at(H, -s * 26, 0, 0); look = { x: LA.x + (LB.x - LA.x) * k, y: LA.y + (LB.y - LA.y) * k, z: LA.z + (LB.z - LA.z) * k }; } /* the pull-back */
  camClear(W, pos); W.camera.position.set(pos.x, pos.y, pos.z); W.camera.lookAt(look.x, look.y, look.z); L.look = look; }
/* every cinematic camera keeps clear of stars and planets (it used to fly straight through the binary suns at the galaxy's edge) */
function camClear(W, P) { const V = W._ccV || (W._ccV = new TH.Vector3()), push = (cx, cy, cz, r) => { const dx = P.x - cx, dy = P.y - cy, dz = P.z - cz, d = Math.hypot(dx, dy, dz); if (d >= r) return; const k = d > 1e-3 ? r / d : 1; P.x = cx + (d > 1e-3 ? dx * k : r); P.y = cy + (d > 1e-3 ? dy * k : 0); P.z = cz + (d > 1e-3 ? dz * k : 0); };
  for (const b of W.binaries || []) for (const st of [b.big, b.small]) { if (!st || !st.userData) continue; st.getWorldPosition(V); push(V.x, V.y, V.z, (st.userData.rad || 4) * 6); }
  if (W.planets) for (const [, o] of W.planets) { if (!o.grp || !o.grp.visible) continue; const q = o.grp.position, r = (o.rad || 2) * (o.grp.scale.x || 1) * 2.6; if (Math.abs(P.x - q.x) < r && Math.abs(P.z - q.z) < r) push(q.x, q.y, q.z, r); } }
