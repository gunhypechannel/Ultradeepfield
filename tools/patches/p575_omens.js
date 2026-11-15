/* ---------- v575 The Omens: every server starts at Season 1, and the first two seasons are a prologue. No super bosses yet:
   each week one Warden's omen shows on the map (the same marks a cracked seal leaves), the Archives keep them, and the two
   prologue finales are short teasers (the Leviathan's shadow passing the wall; every omen at once, the Cube's count racing,
   then silence). Behind the galaxy, the Judge (the Architects' last Warden) opens one more eye with every omen, and once the
   Ten Seals begin his hands carry the Seal Ledger: gold for a seal held, red for a seal cracked. ---------- */
const OMEN_K = ["lev", "brd", "krk", "wym", "aex", "vae", "khz", "med"];
const omenWk = T => Math.floor((T - ROT_SEA0) / WEEK), omenKey = T => { const w = omenWk(T); return w >= 0 && w < 4 * PRO ? OMEN_K[w] : null; }, omenWk0 = T => ROT_SEA0 + omenWk(T) * WEEK;
/* the Archives: an omen's fragment the week it shows, its meaning when the week ends; the Judge's page after the count breaks */
function omArchTick(T) { const wi = omenWk(T); if (wi < 0 || !ARCH.o_1) return false; const n = Math.min(wi, 4 * PRO);
  for (let j = 0; j < OMEN_K.length; j++) { const k = "o_" + (j + 1), lv = archLv(k); if (j < n && lv < 2) { archUnlock(k, 2, j < n - 1); return true; } if (j === n && !lv) { archUnlock(k, 1); return true; } }
  const e2 = finWinOf("om2", 0)[2]; if (T >= e2 && archLv("l_judge") < 2) { archUnlock("l_judge", 2, T - e2 > 7 * 864e5); return true; } return false; }
/* ---------- the prologue's first finale: The Shadow at the Wall ---------- */
function om1Set(W, t, F) { const D = FIN_EV.om1, e = F.e, E = D.st.map(s => s[0]); let X = W.fin;
  if (!X || X.s0 !== F.s0 || X.k !== F.k) { X = finNew(W, F); X.R = LAYERS[0].r1 + 12; X.aB = Math.atan2(X.P1.z, X.P1.x);
    X.N = MOBILE ? 700 : 1300; X.ring = finPts(W, X, X.N, MOBILE ? 14 : 18, "255,130,50"); X.ang = new Float32Array(X.N); { const r = finR(31); for (let i = 0; i < X.N; i++) { const a = i / X.N * TAU + r() * .004, rr = X.R + (r() - .5) * 14; X.ang[i] = a; X.ring.P[i * 3] = Math.cos(a) * rr; X.ring.P[i * 3 + 1] = (r() - .5) * 8; X.ring.P[i * 3 + 2] = Math.sin(a) * rr; } }
    X.b = finModel(W, X, "lev"); if (X.b) X.b.grp.traverse(o => { if (!o.material) return; const one = m => { const c = m.clone(); if (c.color) c.color.multiplyScalar(.06); if (c.emissive) { c.emissive.setRGB(.5, .13, .02); c.emissiveIntensity = .7; } if (c.uniforms && c.uniforms.uOp) c.uniforms.uOp.value = 1; try { m.dispose(); } catch (er) {} return c; }; o.material = Array.isArray(o.material) ? o.material.map(one) : one(o.material); });
    X.back = finSpr(W, X, "255,110,30", 0xff6a2a); X.eye = finSpr(W, X, "255,200,120", 0xffc070); X.pos = new TH.Vector3(Math.cos(X.aB - 1.4) * (X.R + 240), 30, Math.sin(X.aB - 1.4) * (X.R + 240)); X.foc = X.pos; X.dist = 1150; X.cv = new TH.Vector3(); }
  const u = fseg(e, E[1], E[2]), pass = e >= E[1] && e < E[2], end = 1 - fsm((e - D.set) / 50e3), sink = fsm((u - .84) / .16);
  const a = X.aB - 1.4 + 2.8 * Math.max(0, Math.min(1, u)), r = X.R + 240 - 70 * Math.sin(Math.PI * Math.max(0, Math.min(1, u))); let y = 30 + 18 * Math.sin(u * TAU * 2) - 300 * sink, sc = pass ? 7 * fsm(u * 9) * (1 - sink) : 0;
  if (pass) X.pos.set(Math.cos(a) * r, y, Math.sin(a) * r);
  if (X.b) { X.b.grp.visible = sc > .03; X.b.grp.position.copy(X.pos); X.b.grp.scale.setScalar(Math.max(.01, sc)); X.b.grp.rotation.y = -a - Math.PI / 2; X.b.tick(t); if (t > X.nx) { X.b.act(Math.random() < .5 ? "coil" : "sweep"); X.nx = t + 7000 + Math.random() * 5000; } }
  { const k = sc / 7, cam = W.camera; if (cam) { X.cv.copy(X.pos).sub(cam.position).normalize(); X.back.position.copy(X.pos).addScaledVector(X.cv, 160); X.back.position.y -= 20; } X.back.scale.setScalar(620 * k); X.back.material.opacity = .42 * k * (.85 + .15 * Math.sin(t * .003));
    X.eye.position.copy(X.pos); X.eye.position.y += 14 * k; X.eye.scale.setScalar(70 * k); X.eye.material.opacity = .9 * k * (Math.sin(t * .0011) > .96 ? .15 : 1); }
  { const c = X.ring.C, base = (.22 + .5 * fsm(e / (5 * 60e3))) * end * (1 - .6 * fsm((e - E[2]) / (4 * 60e3))); for (let i = 0; i < X.N; i++) { const fl = .7 + .3 * Math.sin(t * .006 + i * 1.7), d = Math.abs(Math.atan2(Math.sin(X.ang[i] - a), Math.cos(X.ang[i] - a))); let b = base * fl; if (pass) b += 1.6 * Math.exp(-d * 9) * (1 - sink) * fl * fsm(u * 9); c[i * 3] = b; c[i * 3 + 1] = b * .45; c[i * 3 + 2] = b * .14; } X.ring.up(); } }
/* ---------- the prologue's second finale: The Count Breaks ---------- */
function om2Set(W, t, F) { const D = FIN_EV.om2, e = F.e, E = D.st.map(s => s[0]); let X = W.fin;
  if (!X || X.s0 !== F.s0 || X.k !== F.k) { X = finNew(W, F); X.cp = new TH.Vector3(); X.fv = new TH.Vector3(); X.hd = new TH.Vector3(); X.foc = X.fv; X.dist = 1650; X.sc = [];
    OMEN_K.forEach((k, i) => { const Z = { grp: new TH.Group(), M: new TH.Matrix4(), Q: new TH.Quaternion(), V: new TH.Vector3(), Sc: new TH.Vector3(), at: (i + .5) * 75e3 }; Z.grp.visible = false; X.grp.add(Z.grp); try { Z.tick = FIN_SCAR[k](W, Z, F.s0); } catch (er) { Z.tick = null; } X.sc.push(Z); });
    X.Rk = LAYERS[4].r1 * 1.15; X.NT = 60; X.ticks = new TH.InstancedMesh(new TH.BoxGeometry(1, 1, 1), new TH.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: .95, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false }), X.NT); X.ticks.frustumCulled = false; X.grp.add(X.ticks);
    X.tc = new TH.Color(); X.ring = finRing(X, 0x5dff6a, 192); X.ring2 = finRing(X, 0xb8ffcf, 192); X.beam = finSpr(W, X, "120,255,150", 0x6aff8a); X.flash = finSpr(W, X, "220,255,230", 0xeaffef); X.pop = finSpr(W, X, "200,255,210", 0xc8ffd8); X.lp = -1; }
  try { if (W.nexus) W.nexus.getWorldPosition(X.cp); } catch (er) {}
  const cp = X.cp, u = fseg(e, E[1], E[2]), stir = e < E[2], count = e >= E[1] && e < E[2], quiet = e >= E[2], end = 1 - fsm((e - D.set) / 50e3);
  /* every omen lights up again, one after another */
  let popA = 0; for (const Z of X.sc) { const on = stir && e >= Z.at; Z.grp.visible = on; if (on && Z.tick && (Z.nt || 0) <= t) { Z.tick(t); Z.nt = t + 33; } popA = Math.max(popA, stir ? Math.max(0, 1 - Math.abs(e - Z.at) / 5e3) : 0); }
  X.pop.position.copy(cp); X.pop.position.y += 30; X.pop.scale.setScalar(160 + 340 * popA); X.pop.material.opacity = .5 * popA;
  /* the count: sixty marks round the Cube, the light running faster and faster */
  const p = count ? 60 * (u * 3 + u * u * u * 26) : 0, head = Math.floor(p), lit = fsm(e / (4 * 60e3)) * (quiet ? 0 : 1);
  for (let i = 0; i < X.NT; i++) { const a = i / X.NT * TAU - Math.PI / 2, big = i % 5 === 0, back = ((head - i) % X.NT + X.NT) % X.NT, tr = count ? Math.exp(-back / (4 + 10 * u)) : 0, b = lit * (.14 + (big ? .1 : 0) + 1.3 * tr);
    X.V.set(cp.x + Math.cos(a) * X.Rk, cp.y + 2, cp.z + Math.sin(a) * X.Rk); X.Q.setFromAxisAngle(X.A.set(0, 1, 0), -a); X.Sc.set(big ? 26 : 15, 3, big ? 5 : 3); X.M.compose(X.V, X.Q, X.Sc); X.ticks.setMatrixAt(i, X.M);
    X.tc.setRGB(b * .45, b, b * .55); X.ticks.setColorAt(i, X.tc); } X.ticks.instanceMatrix.needsUpdate = true; if (X.ticks.instanceColor) X.ticks.instanceColor.needsUpdate = true;
  if (head !== X.lp && head % 5 === 0) X.beat = t; X.lp = head; const beat = count ? Math.max(0, 1 - (t - (X.beat || 0)) / 260) : 0;
  X.ring.position.set(cp.x, cp.y + 1, cp.z); X.ring.scale.setScalar(X.Rk * (1.06 + .02 * beat)); X.ring.material.opacity = lit * (.25 + .6 * beat) * (count ? 1 : .5);
  X.ring2.position.set(cp.x, cp.y + 1, cp.z); X.ring2.scale.setScalar(X.Rk * (.9 - .06 * fsm(u))); X.ring2.material.opacity = count ? .35 * fsm(u * 3) * (.6 + .4 * Math.sin(t * .02 * (1 + u * 4))) : 0;
  X.beam.position.set(cp.x, cp.y + 260, cp.z); X.beam.scale.set(70 + 40 * beat, 520 + 200 * fsm(u), 1); X.beam.material.opacity = count ? (.25 + .5 * fsm(u)) * (.7 + .3 * beat) : 0;
  /* then everything stops at once */
  const fl = Math.max(0, 1 - Math.abs(e - E[2]) / 5e3); X.flash.position.set(cp.x, cp.y + 30, cp.z); X.flash.scale.setScalar(300 + 1600 * fl); X.flash.material.opacity = fl;
  /* at the end the camera lifts toward the Judge's face, his eyes blazing */
  { const A = W.celArt, cam = W.camera, k = fsm((e - E[3]) / 25e3) * .75; X.fv.copy(cp); if (A && cam && k > 0) { X.R = X.R || new TH.Vector3(); X.U = X.U || new TH.Vector3(); X.R.setFromMatrixColumn(cam.matrixWorld, 0); X.U.setFromMatrixColumn(cam.matrixWorld, 1); X.hd.copy(A.grp.position).addScaledVector(X.R, (395 / 1100 - .5) * CEL_ART_W).addScaledVector(X.U, (.5 - 160 / 619) * CEL_ART_W * CEL_ART_AR); X.fv.lerp(X.hd, k); } }
  W.renderer.toneMappingExposure = X.exp0 * (1 - .4 * fsm((e - E[2]) / 4e3) * (1 - fsm((e - E[3]) / 90e3)) * end); }
FIN_SET.om1 = om1Set; FIN_SET.om2 = om2Set;
/* ---------- the Judge: one eye opens with every omen, and the Seal Ledger shows on his hands ---------- */
const JUDGE_EYE = [[361, 126], [409, 141], [357, 151], [405, 166], [352, 176], [399, 190]];
const JUDGE_MARK = (() => { const seg = (a, b, f) => f.map(u => [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u]); return seg([470, 590], [635, 290], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map(i => .04 + i * .1)); })(); /* along the near finger of his open hand, base to tip */
function judgeLit(T) { const wi = omenWk(T); return wi < 0 ? 0 : wi >= 4 * PRO ? 6 : Math.ceil((wi + 1) * 6 / (4 * PRO)); }
function judgeBlaze(T, t) { if (G.jbT && t < G.jbT && t > G.jbT - 1000) return G.jb; G.jbT = t + 400; let b = 0; try { const F = finNow(T); if (F && F.k === "om2") { const E = FIN_EV.om2.st; b = F.e < E[1][0] ? 0 : F.e < E[2][0] ? .35 : 1; } } catch (e) {} return (G.jb = b); }
function judgeArt(W, A, e, t) { const T = now(); let J = A.jx;
  /* overlays the same size and place as the painting, so every mark sits exactly on it: dark lids over the closed eyes, the eyes' glow,
     and the Seal Ledger on his near finger (gold steady for a seal held, red flickering for a seal cracked, white pulsing for one live) */
  if (!J) { J = A.jx = { key: "" }; const lay = (normal, ro) => { const c = document.createElement("canvas"); c.width = 550; c.height = 310; const tx = new TH.CanvasTexture(c); tx.encoding = TH.sRGBEncoding; const m = new TH.SpriteMaterial({ map: tx, transparent: true, opacity: 0, depthWrite: false }); if (!normal) m.blending = TH.AdditiveBlending; m.toneMapped = false; const s = new TH.Sprite(m); s.scale.copy(A.base.scale); s.renderOrder = ro; A.grp.add(s); return { c, x: c.getContext("2d"), tx, s }; };
    J.lid = lay(1, 1); J.glow = lay(0, 2); J.held = lay(0, 3); J.crk = lay(0, 3); J.live = lay(0, 3); }
  if (!J.t || t > J.t) { J.t = t + 2000; const L = judgeLit(T); let led = []; try { led = T >= ROT_SEA0 + 4 * PRO * WEEK ? finLedger(T) : []; } catch (er) {} const st = i => { const x = led.find(q => q.ch === i + 1); return x ? x.st : "soon"; };
    const key = L + "|" + JUDGE_MARK.map((m, i) => st(i)).join(","); if (key !== J.key) { J.key = key; const dot = (o, px, py, r, a, b) => { const x = o.x, g = x.createRadialGradient(px / 2, py / 2, 0, px / 2, py / 2, r); g.addColorStop(0, a); g.addColorStop(.5, b); g.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = g; x.beginPath(); x.arc(px / 2, py / 2, r, 0, TAU); x.fill(); };
      for (const o of [J.lid, J.glow, J.held, J.crk, J.live]) o.x.clearRect(0, 0, 550, 310);
      JUDGE_EYE.forEach(([px, py], i) => { if (i < L) dot(J.glow, px, py, 10, "rgba(235,255,240,1)", "rgba(80,255,130,.55)"); else { dot(J.lid, px, py, 9, "rgba(2,6,4,1)", "rgba(2,6,4,.97)"); dot(J.lid, px, py, 9, "rgba(2,6,4,1)", "rgba(2,6,4,.9)"); } });
      JUDGE_MARK.forEach(([px, py], i) => { const s2 = st(i); if (s2 === "held") dot(J.held, px, py, 11, "rgba(255,250,220,1)", "rgba(255,200,90,.6)"); else if (s2 === "cracked") dot(J.crk, px, py, 11, "rgba(255,200,180,1)", "rgba(255,50,30,.65)"); else if (s2 === "live") dot(J.live, px, py, 13, "rgba(255,255,255,1)", "rgba(200,230,255,.6)"); });
      for (const o of [J.lid, J.glow, J.held, J.crk, J.live]) o.tx.needsUpdate = true; } }
  const bz = judgeBlaze(T, t), tt = reduced ? 0 : t * .001; J.lid.s.material.opacity = e; J.glow.s.material.opacity = e * Math.min(1, .25 + .15 * Math.sin(tt * 2.2) + .75 * bz * (.85 + .15 * Math.sin(tt * 9)));
  J.held.s.material.opacity = e * (.85 + .1 * Math.sin(tt)); J.crk.s.material.opacity = e * (.6 + .4 * Math.max(0, Math.sin(tt * 5))) * (Math.sin(tt * 13) > -.7 ? 1 : .3); J.live.s.material.opacity = e * (.5 + .5 * Math.sin(tt * 4)); }
