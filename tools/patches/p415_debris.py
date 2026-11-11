# v415: the wreckage the super bosses leave is remastered from the game's own models. Each fight site (wbScars, not the path marks) near
# the camera gets a wreck set: charred derelicts of real fleet hulls (battleships, dreadnoughts, carriers...) with burning holes and fires,
# tumbling slowly, torn hull plates round them; a kill site also gets a destroyed Cube Destroyer (charred, a slab of its shell blown off and
# drifting, its core glowing through) and a shattered planetoid (a world with a huge bite carved out of it, magma glowing in the wound,
# rubble orbiting). Pooled: at most 3 sets shown (1 on phones, within 450 units; 2 with Lite effects), built once and moved to the nearest sites within 700 units;
# fires burn hotter on fresh sites and die down over the 48 h a site lasts. The scattered scar plates are now torn extruded plates.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("""function wbScarFx(W, t, T) {
  let X = W.wbScar; if (!X) { const N = 1400, P = 4200;
    const mesh = new TH.InstancedMesh(new TH.IcosahedronGeometry(1, 0), """, """/* v415 boss wreck sites: real hulls, a destroyed Cube Destroyer and a shattered planetoid */
function wbWreckSet(W, kill, seed) { const LITE = MOBILE || FX_LITE(), DK = debrisKit(W), r = cwRnd(seed), grp = new TH.Group(); grp.visible = false; W.add(grp);
  const S = { grp, kill, ders: [], fires: [], spin: [], V: new TH.Vector3(), site: null };
  const char = g => { g.userData.noBatch = 1; const done = new Map(); g.traverse(o => { if (!o.isMesh || !o.material || Array.isArray(o.material) || o.material.emissive === undefined) return;
    let m = done.get(o.material); if (!m) { m = o.material.clone(); m.color.multiplyScalar(.4); m.roughness = Math.min(1, (m.roughness || .5) + .25); m.emissive.set(0xffffff); m.emissiveMap = DK.emi; m.emissiveIntensity = 1.4; done.set(o.material, m); } o.material = m; }); };
  const kinds = ["battleship", "dreadnought", "supercarrier", "destroyer", "bastion", "escortCarrier", "lancer", "corvette"], nd = kill ? (LITE ? 2 : 3) : (LITE ? 1 : 2);
  const hull = (k, p, sc, nf) => { let g; if (k === "worldbreaker") { const sh = buildShip(k, shipMats("#ff3b30")); sh.traverse(c => { if (c.userData && c.userData.fx) c.visible = false; }); const b0 = new TH.Box3().setFromObject(sh), s0 = b0.getSize(new TH.Vector3()); g = new TH.Group(); sh.scale.setScalar(2 / Math.max(s0.x, s0.y, s0.z)); sh.position.copy(b0.getCenter(new TH.Vector3())).multiplyScalar(-sh.scale.x); g.add(sh); }
    else { g = fleet3D(W, { [k]: 1 }, 0x3a2a20, false); if (g.userData.eng) g.userData.eng.visible = false; } char(g); grp.add(g); g.updateMatrixWorld(true);
    const bb = new TH.Box3().setFromObject(g), sz = bb.getSize(new TH.Vector3()), d = { g, p, e: [r() * TAU, r() * TAU, r() * TAU], s: [(r() - .5) * 4e-5, (r() - .5) * 3e-5, (r() - .5) * 2e-5], k: sc, fl: [], fires: [], fs: Math.max(sz.x, sz.y, sz.z) * .22 };
    for (let i = 0; i < nf; i++) { const q = new TH.Vector3(bb.min.x + r() * sz.x, bb.min.y + r() * sz.y, bb.min.z + r() * sz.z), ax = (r() * 3) | 0; q.setComponent(ax, r() < .5 ? bb.min.getComponent(ax) : bb.max.getComponent(ax)); d.fl.push(q); d.fires.push(fireSprite(W, grp, DK)); }
    S.ders.push(d); return d; };
  for (let i = 0; i < nd; i++) { const a = r() * TAU, rr = 10 + r() * 16; hull(kinds[(seed + i * 3) % kinds.length], new TH.Vector3(Math.cos(a) * rr, -3 + r() * 8, Math.sin(a) * rr), 3.4 + r() * 1.4, LITE ? 2 : 4); }
  if (kill) { // a destroyed Cube Destroyer: charred, a slab of its shell blown off, its core glowing through the wound
    const a = r() * TAU, d = hull("worldbreaker", new TH.Vector3(Math.cos(a) * 16, 3, Math.sin(a) * 16), 5.5, LITE ? 3 : 6); d.g.updateMatrixWorld(true); const bb = new TH.Box3().setFromObject(d.g), R = Math.max(bb.max.x - bb.min.x, bb.max.y - bb.min.y) * .5;
    const slab = new TH.Mesh(new TH.SphereGeometry(R * 1.01, 16, 10, 0, 1.3, .9, 1.1), DK.mat); slab.userData.off = new TH.Vector3(R * .9, R * .4, R * .5); d.g.add(slab); slab.position.copy(slab.userData.off); slab.rotation.set(.3, -.4, .2); d.slab = slab;
    const core = new TH.Sprite(W.additive(glowTex("255,110,40", 1), 0xff7a30, .95)); core.scale.setScalar(R * 1.6); core.position.set(R * .35, R * .15, R * .2); d.g.add(core); d.core = core; d.R = R;
    // a shattered planetoid: a world with a bite carved out of it, magma glowing in the wound, rubble round it
    const pg = new TH.IcosahedronGeometry(1, LITE ? 3 : 4), pa = pg.attributes.position, v = new TH.Vector3(), cut = new TH.Vector3(.55, .35, .76).normalize(), cols = new Float32Array(pa.count * 3);
    for (let i = 0; i < pa.count; i++) { v.fromBufferAttribute(pa, i); const n = 1 + .05 * (Math.sin(7 * v.x) + Math.sin(9 * v.y + 1) + Math.sin(8 * v.z + 2)) / 3 + .025 * Math.sin(23 * v.x + 17 * v.y), c = v.dot(cut);
      if (c > .28) v.addScaledVector(cut, -(c - .28) * (1 + .12 * Math.sin(31 * v.x + 13 * v.z))); v.multiplyScalar(n); pa.setXYZ(i, v.x, v.y, v.z);
      const hot = clamp((c - .18) / .12, 0, 1), k = .2 + .08 * Math.sin(11 * v.x + 5 * v.z); cols[i * 3] = k + hot * .5; cols[i * 3 + 1] = k * .9 + hot * .12; cols[i * 3 + 2] = k * .85; }
    pg.setAttribute("color", new TH.BufferAttribute(cols, 3)); pg.computeVertexNormals();
    const planet = new TH.Mesh(pg, new TH.MeshStandardMaterial({ vertexColors: true, roughness: .95, metalness: .05, flatShading: true }));
    const lava = texCanvas(256, 256, x => { const g = x.createRadialGradient(128, 128, 6, 128, 128, 128); g.addColorStop(0, "rgba(255,240,190,1)"); g.addColorStop(.3, "rgba(255,150,40,1)"); g.addColorStop(.7, "rgba(200,40,10,.95)"); g.addColorStop(1, "rgba(60,8,4,0)"); x.fillStyle = g; x.fillRect(0, 0, 256, 256);
      x.strokeStyle = "rgba(30,6,4,.85)"; x.lineWidth = 3; const rr = cwRnd(77); for (let i = 0; i < 26; i++) { x.beginPath(); let px = 128, py = 128; x.moveTo(px, py); const a0 = rr() * TAU; for (let k = 0; k < 6; k++) { px += Math.cos(a0 + (rr() - .5) * 1.2) * 20; py += Math.sin(a0 + (rr() - .5) * 1.2) * 20; x.lineTo(px, py); } x.stroke(); } });
    const disc = new TH.Mesh(new TH.CircleGeometry(.93, 40), new TH.MeshBasicMaterial({ map: lava, transparent: true, toneMapped: false, depthWrite: false })); disc.position.copy(cut).multiplyScalar(.285); disc.lookAt(cut.clone().multiplyScalar(2)); planet.add(disc);
    const halo = new TH.Sprite(W.additive(glowTex("255,120,50", 1), 0xff7a30, .55)); halo.position.copy(cut).multiplyScalar(.6); halo.scale.setScalar(1.9); planet.add(halo);
    const pr = 7 + r() * 2, b2 = a + Math.PI * (.7 + r() * .6); planet.scale.setScalar(pr); planet.position.set(Math.cos(b2) * 22, -6 + r() * 4, Math.sin(b2) * 22); planet.rotation.set(r(), r() * TAU, r()); grp.add(planet); S.planet = planet; S.pspin = (r() < .5 ? -1 : 1) * 2e-5;
    const rocks = new TH.InstancedMesh(new TH.IcosahedronGeometry(1, 0), new TH.MeshStandardMaterial({ color: 0x5a4a44, roughness: 1, flatShading: true }), LITE ? 16 : 36); rocks.frustumCulled = false; grp.add(rocks); S.rocks = rocks; S.rk = [];
    for (let i = 0; i < rocks.count; i++) S.rk.push({ a: r() * TAU, d: pr * (1.15 + r() * .9), y: (r() - .5) * pr * .5, k: .25 + r() * r() * 1.3, w: (r() < .5 ? -1 : 1) * TAU / (200000 + r() * 300000), e: r() * TAU }); }
  // torn hull plates and girders drifting through the site
  const nP = LITE ? 18 : 40; S.plates = DK.geos.slice(0, 3).map(geo => { const im = new TH.InstancedMesh(geo, DK.mat, Math.ceil(nP / 3)); im.frustumCulled = false; grp.add(im); return im; }); S.pl = [];
  S.plates.forEach(im => { for (let j = 0; j < im.count; j++) { const a = r() * TAU, rr = 6 + Math.sqrt(r()) * 30; S.pl.push({ im, j, p: new TH.Vector3(Math.cos(a) * rr, -6 + r() * 12, Math.sin(a) * rr), e: [r() * TAU, r() * TAU, r() * TAU], s: [(r() - .5) * 3e-4, (r() - .5) * 3e-4, (r() - .5) * 2e-4], k: .35 + r() * r() * 1.3 }); } });
  return S; }
function wbWrecks(W, t, T) { const X = W.wbWk || (W.wbWk = { sets: [], at: 0, pick: [] }), cam = W.camera.position;
  if (t - X.at > 1000) { X.at = t; const L = wbScars(T).filter(s => !s.a && Math.hypot(s.x - cam.x, s.y - cam.y, s.z - cam.z) < (MOBILE ? 450 : 700)); L.sort((a, b) => (b.b || 0) - (a.b || 0) || Math.hypot(a.x - cam.x, a.z - cam.z) - Math.hypot(b.x - cam.x, b.z - cam.z));
    const NS = MOBILE ? 1 : FX_LITE() ? 2 : 3; X.pick = L.slice(0, NS); }
  if (reduced || !X.pick.length) { for (const S of X.sets) S.grp.visible = false; return; }
  const used = new Set();
  for (const s of X.pick) { let S = X.sets.find(S => !used.has(S) && S.site === s.k + s.at) || X.sets.find(S => !used.has(S) && S.kill === !!s.b && !X.pick.some(q => q.k + q.at === S.site));
    if (!S && X.sets.length < (MOBILE ? 2 : FX_LITE() ? 2 : 3)) { S = wbWreckSet(W, !!s.b, 1 + hash(s.k + ":" + s.at) % 99991); X.sets.push(S); }
    if (!S) continue; used.add(S); S.site = s.k + s.at;
    const age = clamp((T - s.at) / WB_SCAR_MS, 0, 1), heat = clamp(1 - (T - s.at) / (12 * 3600e3), .15, 1), V = S.V; S.grp.visible = true; S.grp.position.set(s.x, s.y, s.z);
    for (const d of S.ders) { d.g.position.copy(d.p); d.g.rotation.set(d.e[0] + T * d.s[0], d.e[1] + T * d.s[1], d.e[2] + T * d.s[2]); d.g.scale.setScalar(d.k);
      d.g.updateMatrix(); d.fl.forEach((lp, k) => { if (k / d.fl.length > heat + .2) { d.fires[k].visible = false; return; } fireTick(d.fires[k], t, V.copy(lp).applyMatrix4(d.g.matrix), d.fs * d.k * (.35 + .3 * heat)); });
      if (d.slab) { const u = ((T - s.at) / 3600e3) % 1e3; d.slab.position.copy(d.slab.userData.off).multiplyScalar(1 + Math.min(.6, u * .02)); d.core.material.opacity = (.5 + .45 * heat) * (.85 + .15 * Math.sin(t * .005)); } }
    if (S.planet) { S.planet.rotation.y += S.pspin * 16; const P = S.planet.position, m4 = S.m4 || (S.m4 = new TH.Matrix4()), q = S.q || (S.q = new TH.Quaternion()), e = S.e || (S.e = new TH.Euler()), sc = S.sc || (S.sc = new TH.Vector3());
      S.rk.forEach((o, i) => { const a = o.a + T * o.w; V.set(P.x + Math.cos(a) * o.d, P.y + o.y, P.z + Math.sin(a) * o.d); q.setFromEuler(e.set(o.e + T * 1e-4, o.e * 2, a)); sc.setScalar(o.k); m4.compose(V, q, sc); S.rocks.setMatrixAt(i, m4); }); S.rocks.instanceMatrix.needsUpdate = true; }
    if (!S.plT || t - S.plT > 80) { S.plT = t; const m4 = S.m4 || (S.m4 = new TH.Matrix4()), q = S.q || (S.q = new TH.Quaternion()), e = S.e || (S.e = new TH.Euler()), sc = S.sc || (S.sc = new TH.Vector3());
      for (const o of S.pl) { q.setFromEuler(e.set(o.e[0] + T * o.s[0], o.e[1] + T * o.s[1], o.e[2] + T * o.s[2])); sc.setScalar(o.k); m4.compose(o.p, q, sc); o.im.setMatrixAt(o.j, m4); } S.plates.forEach(im => im.instanceMatrix.needsUpdate = true); } }
  for (const S of X.sets) if (!used.has(S)) { S.grp.visible = false; S.site = null; } }
function wbScarFx(W, t, T) {
  try { wbWrecks(W, t, T); } catch (e) { mapErr(e); } // v415
  let X = W.wbScar; if (!X) { const N = 1400, P = 4200;
    const mesh = new TH.InstancedMesh(debrisKit(W).geos[0], """)
t = t.replace("const GAME_V = 414;", "const GAME_V = 415;")
open(p, "w").write(t); print("ok")
