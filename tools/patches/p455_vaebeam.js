/* v455 Divine Annihilation at the scale of the galaxy (owner: "its attack should nearly blanket the whole map"): the beam the map draws
   from Vaelthar's jaws is 1700 units long and widens to 300: a white-hot core in layers of violet plasma, four spiralling streams,
   shockwave rings racing along it, explosions erupting the length of its path and a violet glow flooding the map beneath, sweeping
   about 70 degrees across the galaxy as his head turns. It follows his real head, so it is the same for everyone. */
function sbVaeBeam(W, X, b, t, kill) { const on = b.ph === "beam" && b.fireK > .01;
  if (!X.vb) { const g = new TH.Group(), mats = []; const add = (geo, col, op) => { const m = new TH.Mesh(geo, new TH.MeshBasicMaterial({ color: col, transparent: true, opacity: op, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false })); m.frustumCulled = false; m.userData.o = op; g.add(m); mats.push(m); return m; };
    const L = 1700, cyl = (r0, r1) => { const c = new TH.CylinderGeometry(r1, r0, L, 28, 1, true); c.translate(0, L / 2, 0); c.rotateX(Math.PI / 2); return c; };
    const layers = [[160, 210, 0x5a1aa8, .05], [90, 125, 0x8a40ff, .1], [48, 70, 0xb070ff, .26], [22, 34, 0xe0c0ff, .6], [9, 14, 0xffffff, .95]].map(([a, c, col, op]) => add(cyl(a, c), col, op));
    const streams = []; for (let k = 0; k < 4; k++) { const m = add(cyl(6, 9), 0xd8b0ff, .55); streams.push(m); }
    const rings = []; for (let k = 0; k < 9; k++) { const m = add(new TH.TorusGeometry(70, 5, 6, 48), 0xf0e0ff, .7); rings.push(m); }
    const glow = []; for (let k = 0; k < 4; k++) { const s = new TH.Sprite(W.additive(W.glow.wh || (W.glow.wh = glowTex("255,255,255", .85)), new TH.Color("#b070ff"), 0)); s.renderOrder = 2; X.grp.add(s); glow.push(s); }
    const muz = new TH.Sprite(W.additive(W.glow.wh, new TH.Color("#f0e0ff"), 0)); X.grp.add(muz); const hit = new TH.Sprite(W.additive(W.glow.wh, new TH.Color("#d8b0ff"), 0)); X.grp.add(hit);
    X.grp.add(g); X.vb = { g, layers, streams, rings, glow, muz, hit, L, d: new TH.Vector3(), o: new TH.Vector3(), q: new TH.Quaternion(), on0: 0 }; }
  const V0 = X.vb; V0.g.visible = on; V0.glow.forEach(s => s.visible = on); V0.muz.visible = V0.hit.visible = on; if (!on) { V0.on0 = 0; return 0; }
  if (!V0.on0) V0.on0 = t; const age = (t - V0.on0) / 1000, k = b.fireK, grow = Math.min(1, age / 1.2);
  b.mouth.getWorldPosition(V0.o); V0.d.set(-V0.o.x, -V0.o.y * .92, -V0.o.z).normalize(); { const sw = (b.sway || 0) * .8, c = Math.cos(sw), sn = Math.sin(sw), x = V0.d.x * c - V0.d.z * sn, z = V0.d.x * sn + V0.d.z * c; V0.d.x = x; V0.d.z = z; V0.d.normalize(); } /* down through the heart of the galaxy, swept by his head */ V0.g.position.copy(V0.o); V0.g.lookAt(V0.o.clone().add(V0.d));
  const wob = 1 + Math.sin(t * .05) * .06 + Math.sin(t * .13) * .04; V0.layers.forEach((m, i) => { m.material.opacity = m.userData.o * k * (.85 + Math.random() * .15); m.scale.set((.35 + grow * .65) * wob * (1 + i * .02 * Math.sin(t * .02 + i)), (.35 + grow * .65) * wob, Math.min(1, age / .35)); });
  V0.streams.forEach((m, i) => { const a = t * .006 + i * Math.PI / 2, r = 55 + Math.sin(t * .004 + i) * 12; m.position.set(Math.cos(a) * r, Math.sin(a) * r, 0); m.material.opacity = .55 * k; m.scale.set(1, 1, Math.min(1, age / .45)); });
  V0.rings.forEach((m, i) => { const z = ((t * .9 + i * V0.L / 9) % V0.L); m.position.set(0, 0, z); m.scale.setScalar(.6 + z / V0.L * 2.2); m.material.opacity = .7 * k * (1 - z / V0.L); });
  V0.glow.forEach((s, i) => { s.position.copy(V0.o).addScaledVector(V0.d, (i + .6) * V0.L / 4.4); s.position.y -= 30; s.scale.setScalar(900 * (.6 + grow * .4)); s.material.opacity = .22 * k; });
  V0.muz.position.copy(V0.o); V0.muz.scale.setScalar(380 + Math.sin(t * .04) * 40); V0.muz.material.opacity = .9 * k; V0.hit.position.copy(V0.o).addScaledVector(V0.d, V0.L * Math.min(1, age / .35)); V0.hit.scale.setScalar(700 + Math.sin(t * .03) * 80); V0.hit.material.opacity = .7 * k;
  if (Math.random() < .55) sbBoom(X, V0.o.clone().addScaledVector(V0.d, 120 + Math.random() * (V0.L - 120)).add(new TH.Vector3((Math.random() - .5) * 200, (Math.random() - .5) * 60, (Math.random() - .5) * 200)), t, 60 + Math.random() * 130);
  const cam = W.camera; if (cam) { const amp = (age < 1.2 ? (1.2 - age) * 9 : 0) + 1.5 * k; cam.position.x += (Math.random() - .5) * amp; cam.position.y += (Math.random() - .5) * amp; cam.position.z += (Math.random() - .5) * amp; }
  if (kill) sbBeamKill(X, V0.o, V0.d, 70 * (.35 + grow * .65), V0.L, t); return k; }
function sbBoomTick(X, t) { for (const Bm of X.booms) { const a = (t - Bm.t) / 900; Bm.s.visible = a >= 0 && a < 1; if (Bm.s.visible) { Bm.s.material.opacity = (1 - a) * .95; Bm.s.scale.setScalar(Bm.sz * (.4 + a * 1.4)); } } }
