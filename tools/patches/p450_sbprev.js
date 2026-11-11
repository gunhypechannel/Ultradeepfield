/* v450 the Ultimate Super Bosses on the galaxy map: the owner's previews of Vaelthar and Aexion. Each tears in through a rift at its own
   place past the Rim, a fleet formation of our own ships takes station in front of it and opens fire, and the whole encounter plays on
   a script, with the camera directing: for Vaelthar its attacks, Divine Annihilation (the beam really cuts through the ships in its
   path), the stabilizers falling, Final Eclipse and its defeat, leaving a relic; for Aexion the Dreadnought Assault, the transformation,
   the Warform's blade, shield, missiles, rail and lance, Reactor Overdrive and its fall. On this device only. */
const SBX = {
  vae: { n: "Vaelthar", t: "The Celestial Ruin", m3: "vaelthar", p: [-340, 60, 250], sc: 4.4, dur: 100, col: "#c890ff", look: 11 },
  aex: { n: "Aexion", t: "The Warform Sovereign", m3: "aexion", p: [360, 40, -250], sc: 4.3, dur: 98, col: "#7ac8ff", look: 4 } };
const SBX_FT = [["battleship", 12], ["destroyer", 16], ["corvette", 26], ["dreadnought", 4], ["supercarrier", 2]];
function sbSimStart(key) { if (!duelOwner() || !SBX[key]) return; closeSheet(); if (view !== "galaxy") { view = "galaxy"; render(); } try { if (G.dvSim) dvSimStop(); } catch (e) {}
  G.sbSim = { key, t0: performance.now(), said: {} }; toast(`Owner preview: ${SBX[key].n}, ${SBX[key].t}. About a minute and a half; only you see this.`); }
function sbSimStop(done) { if (!G.sbSim) return; G.sbSim = null; try { if (G3) sbFree(G3); } catch (e) {} toast(done ? "Preview over." : "Preview stopped."); }
function sbFree(W) { const X = W.sb; if (!X) return; W.scene.remove(X.grp); X.grp.traverse(o => { if (o.userData && o.userData.keep) return; try { if (o.geometry) o.geometry.dispose(); if (o.material && o.material.dispose) o.material.dispose(); } catch (e) {} });
  if (X.exp != null) W.renderer.toneMappingExposure = X.exp; W.sb = null; if (W.cam) W.cam.goal = null; }
function sbBuild(W, key) { const D = SBX[key], X = { key, grp: new TH.Group(), V: new TH.Vector3(), V2: new TH.Vector3(), D3: new TH.Object3D(), exp: W.renderer.toneMappingExposure }; W.scene.add(X.grp);
  BOSS3D.init(TH); BOSS3D.lod = MOBILE ? 1 : 0; X.b = BOSS3D.prep(BOSS3D[D.m3](), wbEnv(W.renderer)); X.B = new TH.Vector3(...D.p); X.F = new TH.Vector3(-D.p[0], 0, -D.p[2]).normalize(); X.R = new TH.Vector3(X.F.z, 0, -X.F.x);
  X.b.grp.position.copy(X.B); X.b.grp.rotation.y = Math.atan2(X.F.x, X.F.z); X.b.grp.scale.setScalar(.001); X.grp.add(X.b.grp);
  // the rift it comes through, and the flash of its arrival and its fall
  X.rift = new TH.Mesh(new TH.RingGeometry(.6, 1, 96), new TH.MeshBasicMaterial({ color: new TH.Color(D.col), transparent: true, opacity: 0, side: TH.DoubleSide, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); X.rift.position.copy(X.B); X.rift.lookAt(X.B.clone().add(X.F)); X.grp.add(X.rift);
  X.flash = new TH.Sprite(W.additive(W.glow.wh || (W.glow.wh = glowTex("255,255,255", .85)), new TH.Color(D.col), 0)); X.flash.position.copy(X.B); X.grp.add(X.flash);
  // the fleet: our own ship models, instanced, in an arc in front of it, every hull facing it
  const K = fleetKit(W, "terran"); X.ships = []; X.types = [];
  if (K) SBX_FT.forEach(([k, n], ti) => { const G0 = shipGeo(K, k), cap = MOBILE ? Math.ceil(n * .6) : n, T = { body: null, glow: null, n: 0 };
    if (G0.midB) { T.body = new TH.InstancedMesh(G0.midB, midMat(K, 0), cap); T.body.setColorAt(0, new TH.Color(1, 1, 1)); } if (G0.midG) T.glow = new TH.InstancedMesh(G0.midG, midMat(K, 1), cap);
    for (const m of [T.body, T.glow]) if (m) { m.frustumCulled = false; m.count = 0; m.userData.keep = 1; X.grp.add(m); } X.types.push(T);
    const r = cwRnd(hash(key + k)); for (let i = 0; i < cap; i++) { const a = (r() - .5) * 1.25, d = 190 + r() * 150 + (ti === 3 || ti === 4 ? 70 : 0), p = X.B.clone().addScaledVector(X.F, Math.cos(a) * d).addScaledVector(X.R, Math.sin(a) * d); p.y += (r() - .5) * 90 + 10;
      X.ships.push({ ti, p, dead: -1, dr: new TH.Vector3(r() - .5, r() - .5, r() - .5).normalize(), rs: [r() - .5, r() - .5, r() - .5], arr: r() * 4 }); } });
  const NS = 120, lg = new TH.BufferGeometry(); lg.setAttribute("position", new TH.BufferAttribute(new Float32Array(NS * 6), 3)); lg.setAttribute("color", new TH.BufferAttribute(new Float32Array(NS * 6), 3));
  X.bolts = new TH.LineSegments(lg, new TH.LineBasicMaterial({ vertexColors: true, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false })); X.bolts.frustumCulled = false; X.grp.add(X.bolts); X.NS = NS;
  X.booms = []; for (let i = 0; i < (MOBILE ? 16 : 30); i++) { const s = new TH.Sprite(W.additive(W.glow.fire || (W.glow.fire = glowTex("255,190,120", .8)), 0xffd0a0, 0)); s.visible = false; X.grp.add(s); X.booms.push({ s, t: -1e9, sz: 30 }); } X.bi = 0;
  X.dark = new TH.Color(.14, .1, .1); X.white = new TH.Color(1, 1, 1); return (W.sb = X); }
function sbBoom(X, p, t, sz) { const B = X.booms[X.bi++ % X.booms.length]; B.t = t; B.sz = sz || 30; B.s.position.copy(p); }
function sbKill(X, s, t, sz) { if (s.dead >= 0) return; s.dead = t; sbBoom(X, s.p, t, sz || 34); }
function sbKillN(X, n, t, near) { const L = X.ships.filter(s => s.dead < 0); if (near) L.sort((a, b) => a.p.distanceTo(X.B) - b.p.distanceTo(X.B)); else L.sort(() => Math.random() - .5); for (const s of L.slice(0, n)) sbKill(X, s, t + Math.random() * 600); }
/* kill every ship within a beam: from point o along unit dir d, radius w, length L */
function sbBeamKill(X, o, d, w, L, t) { for (const s of X.ships) { if (s.dead >= 0) continue; X.V.subVectors(s.p, o); const al = X.V.dot(d); if (al < 0 || al > L) continue; X.V.addScaledVector(d, -al); if (X.V.length() < w) sbKill(X, s, t + al * 2, 40); } }
const SBX_CAM = (X, W, s, dt, K) => { const c = W.cam; if (!c) return; c.goal = null; c.follow = null; c.followFleet = null; const e = 1 - Math.pow(.96, (dt || 16) / 16.7);
  const tx = K.tx != null ? K.tx : X.B.x, ty = K.ty != null ? K.ty : X.B.y + K.y, tz = K.tz != null ? K.tz : X.B.z; c.tx += (tx - c.tx) * e; c.ty += (ty - c.ty) * e; c.tz += (tz - c.tz) * e; c.dist += (K.d - c.dist) * e; c.ph += (Math.PI / 2 - K.th - c.ph) * e; /* K.th: height above the horizon; K.ph: angle round from straight in front of the boss */
  let dp = Math.atan2(X.F.z, X.F.x) + K.ph - c.th; while (dp > Math.PI) dp -= TAU; while (dp < -Math.PI) dp += TAU; c.th += dp * e; };
function sbTick(W, t) { const P = G.sbSim; if (!P) { if (W.sb) sbFree(W); return; } const D = SBX[P.key]; if (W.sb && W.sb.key !== P.key) sbFree(W); const X = W.sb || sbBuild(W, P.key), b = X.b, s = (performance.now() - P.t0) / 1000;
  if (s > D.dur) { sbSimStop(true); return; } const dt = Math.min(64, t - (X.lt || t)); X.lt = t; const say = (k, line) => { if (P.said[k]) return; P.said[k] = 1; try { advHolo(line, 1); } catch (e) { toast(line); } };
  const yaw = Math.atan2(X.F.x, X.F.z), side = yaw + Math.PI / 2; // the camera's azimuth is measured round the target; ph = yaw puts it in front of the boss
  /* arrival: the rift opens, it pushes through and grows to full size */
  const arr = clamp((s - 1.5) / 4, 0, 1), k = 1 - Math.pow(1 - arr, 3); X.rift.material.opacity = bell01(s, .2, 1.5, 5, 8) * .9; X.rift.scale.setScalar(4 + D.sc * 22 * clamp(s / 3, 0, 1) * (1 - clamp((s - 6) / 3, 0, 1) * .4)); X.rift.rotation.z += dt * .0006;
  X.flash.material.opacity = Math.max(bell01(s, 1.2, 1.8, 2.4, 4.5), X.fall ? bell01(s, X.fall, X.fall + .4, X.fall + 1.2, X.fall + 4) : 0); X.flash.scale.setScalar(D.sc * 60 * (1 + (X.fall ? clamp(s - X.fall, 0, 3) : 0)));
  let scl = D.sc * Math.max(.001, k); if (X.fall && s > X.fall) scl *= P.key === "vae" ? Math.max(.001, 1 - clamp((s - X.fall - .6) / 2.5, 0, 1)) : 1; b.grp.scale.setScalar(scl);
  if (P.key === "vae") sbVae(X, W, b, s, t, dt, say, yaw, side); else sbAex(X, W, b, s, t, dt, say, yaw, side);
  b.tick(t);
  /* the fleet: warps in, fires on the boss, and dies where the attacks really reach it */
  const n = X.types.map(() => 0), D3 = X.D3, look = X.V2.copy(X.B).add(new TH.Vector3(0, D.look * D.sc, 0)), bp = X.bolts.geometry.attributes.position.array, bc = X.bolts.geometry.attributes.color.array; let nb = 0;
  for (const sh of X.ships) { const T = X.types[sh.ti], i = n[sh.ti]++, u = clamp((s - 3 - sh.arr) / 2.5, 0, 1), w = 1 - Math.pow(1 - u, 3), dead = sh.dead >= 0 && t >= sh.dead;
    D3.position.copy(sh.p).addScaledVector(X.F, (1 - w) * 260); if (dead) { const a = (t - sh.dead) / 1000; D3.position.addScaledVector(sh.dr, a * 9); } D3.lookAt(look); if (dead) { const a = (t - sh.dead) / 1000; D3.rotateX(sh.rs[0] * a); D3.rotateY(sh.rs[1] * a); D3.rotateZ(sh.rs[2] * a); }
    D3.scale.setScalar(DV_SHIPK * (u > 0 ? 1 : 0)); D3.updateMatrix(); if (T.body) { T.body.setMatrixAt(i, D3.matrix); T.body.setColorAt(i, dead ? X.dark : X.white); } if (T.glow) { if (dead) D3.scale.setScalar(0), D3.updateMatrix(); T.glow.setMatrixAt(i, D3.matrix); }
    if (!dead && u >= 1 && !X.quiet && nb < X.NS && Math.random() < .035) { const o = nb * 6, tg = X.V.copy(look).add(new TH.Vector3((Math.random() - .5) * 14 * D.sc, (Math.random() - .5) * 10 * D.sc, (Math.random() - .5) * 8 * D.sc)); bp.set([sh.p.x, sh.p.y, sh.p.z, tg.x, tg.y, tg.z], o); bc.set([.5, .8, 1, 1, .7, .4], o); nb++; } }
  for (const T of X.types) for (const m of [T.body, T.glow]) if (m) { m.count = T === X.types[0] ? n[0] : n[X.types.indexOf(T)]; m.instanceMatrix.needsUpdate = true; if (m.instanceColor) m.instanceColor.needsUpdate = true; }
  X.bolts.geometry.setDrawRange(0, nb * 2); X.bolts.geometry.attributes.position.needsUpdate = true; X.bolts.geometry.attributes.color.needsUpdate = true; X.bolts.material.opacity = .6 + Math.random() * .4;
  for (const B of X.booms) { const a = (t - B.t) / 900; B.s.visible = a >= 0 && a < 1; if (B.s.visible) { B.s.material.opacity = (1 - a) * .95; B.s.scale.setScalar(B.sz * (.4 + a * 1.4)); } }
  W.renderer.toneMappingExposure = X.exp * (1 - (b.dark || 0) * .55); }
const bell01 = (x, a, b, c, d) => x <= a || x >= d ? 0 : x < b ? (x - a) / (b - a) : x <= c ? 1 : 1 - (x - c) / (d - c);
/* Vaelthar's encounter, 100 s */
function sbVae(X, W, b, s, t, dt, say, yaw, side) { const sc = SBX.vae.sc;
  if (s < 1) say("v0", "WARNING: a celestial anomaly is tearing open beyond the Rim.");
  if (s > 6) say("v1", "Vaelthar, the Celestial Ruin. Its wheel turns the light of dying stars. All fleets, engage!");
  // phase 1, Celestial Guardian: claw, wingstorm, judgment and the seal, each felt by the fleet
  for (const [at, mv, kn] of [[9, "claw", 2], [13, "wing", 4], [18, "judge", 3], [24, "seal", 0], [28, "claw", 2]]) if (s > at && !X["m" + at]) { X["m" + at] = 1; b.act(mv); if (kn) setTimeout(() => { try { sbKillN(X, kn, performance.now(), mv !== "judge"); } catch (e) {} }, mv === "judge" ? 1600 : 900); }
  if (s > 24) say("v2", "A golden seal is forming. Our fleets are slowed inside the circle.");
  // phase 3, Divine Judgment: the full sequence, 22 s, the beam cutting the formation
  const A0 = 33, AL = 22, fa = (s - A0) / AL; b.drive("annihilate", fa >= 0 && fa < 1 ? fa : -1);
  if (fa >= 0 && fa < 1) { X.quiet = fa > .55 && fa < .9; if (fa > .0) say("v3", "WARNING: CATASTROPHIC CELESTIAL ENERGY SIGNATURE DETECTED."); if (fa > .4) say("v4", "The wheel is aligning. Brace for impact!");
    if (b.lens && b.lens.visible) { b.mouth.getWorldPosition(X.V); const o = X.V.clone(), d = new TH.Vector3(0, 0, 1).applyQuaternion(b.lens.getWorldQuaternion(new TH.Quaternion())); sbBeamKill(X, o, d, 4.2 * sc, 80 * sc, t); } }
  else X.quiet = false;
  if (s > A0 + AL) say("v5", "We survived the blast. Now hit the wheel's stabilizers before it charges again!");
  // phase 4: the stabilizers fall one by one, the wheel fractures: Final Eclipse
  for (let k = 0; k < 6; k++) { const at = 58 + k * 2.6; if (s > at && b.stab[k]) { b.stab[k] = 0; b.wheel.updateMatrixWorld(); const p = X.V.copy(b.wheel.position); b.grp.localToWorld(p); sbBoom(X, p.clone().add(new TH.Vector3((Math.random() - .5) * 40 * sc / 4, (Math.random() - .5) * 40 * sc / 4, 0)), t, 60); b.act("hit"); } }
  if (s > 58) say("v6", "Stabilizer down! The wheel is losing its balance!"); b.crack = clamp((s - 66) / 14, 0, 1); if (s > 72) say("v7", "Final Eclipse! The wheel is fracturing. Its core is exposed!");
  if (s > 74 && !X.mw) { X.mw = 1; b.act("wing"); } if (s > 78 && !X.mr) { X.mr = 1; b.act("rebirth"); }
  // its fall: a last roar, the wheel collapses inward, a great shockwave; a relic of the wheel stays
  if (s > 84 && !X.fall) { X.fall = s; say("v8", "Vaelthar has fallen! The wheel collapses. A celestial relic drifts where it died."); }
  if (X.fall && !X.relic && s > X.fall + 2) { X.relic = new TH.Group(); const r = new TH.Mesh(new TH.TorusGeometry(18, 2.2, 8, 40, Math.PI * 1.3), new TH.MeshStandardMaterial({ color: 0xc9a24a, metalness: 1, roughness: .25, emissive: 0x6a3aa0, emissiveIntensity: .6 })); X.relic.add(r); const g = new TH.Sprite(W.additive(W.glow.wh, new TH.Color("#c890ff"), .6)); g.scale.setScalar(70); X.relic.add(g); X.relic.position.copy(X.B).add(new TH.Vector3(0, 40, 0)); X.grp.add(X.relic); }
  if (X.relic) { X.relic.rotation.set(t * .0002, t * .0003, t * .0001); }
  // the camera: wide arrival, around the fight, slowly round the dragon as it charges, beside the beam, on the wheel, wide for the fall
  const K = s < 8 ? { y: 40, d: 900, th: .5, ph: .25 } : s < 33 ? { y: 50, d: 620 + Math.sin(s * .2) * 60, th: .55, ph: .35 + Math.sin((s - 8) * .08) * .25 } : s < A0 + AL * .35 ? { y: 60, d: 430, th: .35, ph: .5 + (s - A0) * .03 }
    : s < A0 + AL * .66 ? { y: 55, d: 360, th: .28, ph: .8 + (s - A0 - AL * .35) * .04 } : s < A0 + AL * .9 ? { y: 30, d: 760, th: .42, ph: Math.PI / 2 + .55, tx: X.B.x + X.F.x * 160, tz: X.B.z + X.F.z * 160 } : s < 58 ? { y: 40, d: 700, th: .5, ph: .3 }
    : s < 84 ? { y: 70, d: 460, th: .3, ph: -.45 + (s - 58) * .02 } : { y: 40, d: 1000, th: .55, ph: .3 };
  SBX_CAM(X, W, s, dt, K); }
/* Aexion's encounter, 98 s */
function sbAex(X, W, b, s, t, dt, say, yaw, side) { const sc = SBX.aex.sc;
  if (s < 1) say("a0", "WARNING: a dreadnought-class signature is dropping out of warp.");
  if (s > 6) say("a1", "Aexion, the Warform Sovereign. Target its stern engines and shield emitters. Open fire!");
  // phase 1, Dreadnought Assault: it creeps forward broadside on, guns, missiles, the Railbreaker
  const creep = clamp(s / 22, 0, 1); b.grp.position.copy(X.B).addScaledVector(X.F, creep * 40);
  for (const [at, mv, kn] of [[8, "broadside", 3], [12.5, "missiles", 5], [17, "rail", 1], [20, "broadside", 2]]) if (s > at && !X["m" + at]) { X["m" + at] = 1; b.act(mv); setTimeout(() => { try { sbKillN(X, kn, performance.now(), mv === "rail"); } catch (e) {} }, mv === "missiles" ? 1400 : mv === "rail" ? 1500 : 500); }
  // phase 2, Warform Awakening: the transformation, 24 s, the fleet holding fire to watch
  const T0 = 24, TL = 24, ft = (s - T0) / TL; if (ft >= 0) b.drive("transform", Math.min(1, ft)); X.quiet = ft > .05 && ft < .95;
  if (ft > 0) say("a2", "WARNING: Aexion is transforming! Its hull is splitting apart!"); if (ft > .5) say("a3", "It's standing up. That thing is a Warform!");
  // phase 3, Sovereign Warform: shield, blade (a travelling shockwave through the line), missiles, lance
  for (const [at, mv, kn, near] of [[50, "aegis", 0], [54, "blade", 7, 1], [59, "missiles", 6], [63.5, "lance", 0], [68, "blade", 6, 1]]) if (s > at && !X["w" + at]) { X["w" + at] = 1; b.act(mv); if (kn) setTimeout(() => { try { sbKillN(X, kn, performance.now(), near); } catch (e) {} }, 1200); }
  if (s > 50) say("a4", "Its holographic shield is soaking our fire. Wait for the blade, then strike!");
  if (s > 63.5 && s < 66.5 && b.reactor) { const o = b.reactor.getWorldPosition(X.V).clone(), d = X.F.clone(); sbBeamKill(X, o, d, 3.5 * sc, 70 * sc, t); }
  // phase 4, Reactor Overdrive: everything at once; its reactor is exposed
  const od = (s - 72) / 10; if (od >= 0 && od < 1) { b.drive("overdrive", (od * 2.4) % 1); if (Math.random() < .03) sbKillN(X, 1, t); } else b.drive("overdrive", -1);
  if (s > 72) say("a5", "Reactor Overdrive! Its core is exposed. Everything we have, now!");
  // its fall: the weapons fail, the shield collapses, it topples back in a last discharge; the wreck stays
  if (s > 84 && !X.fall) { X.fall = s; say("a6", "Aexion is down! Its reactor has burned out. The Warform is a wreck."); }
  if (X.fall) { const f = clamp((s - X.fall) / 5, 0, 1); b.grp.rotation.x = -f * .9; b.grp.position.y = X.B.y - f * 40; b.drive("overdrive", f < .4 ? (f * 6) % 1 : -1); }
  const K = s < 8 ? { y: 30, d: 620, th: .45, ph: .6 } : s < T0 ? { y: 20, d: 380, th: .4, ph: Math.PI / 2 + .3 + (s - 8) * .02, tx: b.grp.position.x, tz: b.grp.position.z } : s < T0 + TL * .5 ? { y: 15 + ft * 60, d: 260, th: .25, ph: 1.1 + (s - T0) * .05, tx: b.grp.position.x, tz: b.grp.position.z }
    : s < T0 + TL ? { y: 40, d: 330 + ft * 90, th: .18, ph: .35, tx: b.grp.position.x, tz: b.grp.position.z } : s < 84 ? { y: 50, d: 420, th: .32, ph: .6 + Math.sin(s * .08) * .5, tx: b.grp.position.x, tz: b.grp.position.z } : { y: 20, d: 640, th: .45, ph: .8 };
  SBX_CAM(X, W, s, dt, K); }
