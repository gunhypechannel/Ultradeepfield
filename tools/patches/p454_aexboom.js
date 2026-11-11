/* v454 Aexion's death (owner: "a super massive explosion that sends shockwaves through the map and scatters his pieces everywhere"):
   two seconds of reactor overload, then the detonation: a blinding flash that lights the whole map, a burst shell of energy, shockwave
   rings racing across the galaxy (the camera shakes as each passes, surviving ships are thrown outward), and every real part of the
   machine (head, chest, arms, legs, wings, halo, cannons, prow) tumbling away across the map with secondary explosions in its wake.
   The pieces drift there as a wreck field until the hunt ends. Timed from the record's moment of death, so everyone sees the same
   blast, and a commander arriving later finds the pieces where they came to rest. e = seconds since the detonation. */
function sbBlast(W, X, e, t) { if (e < -.2 || e > 14) { if (X.bl) for (const m of X.bl.all) m.visible = false; X.expK = 1; X.bR = 0; return; }
  if (!X.bl) { const mk = (w, c) => { const m = new TH.Mesh(new TH.RingGeometry(1 - w, 1, 160), new TH.MeshBasicMaterial({ color: c, transparent: true, opacity: 0, side: TH.DoubleSide, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); m.position.copy(X.B); m.frustumCulled = false; X.grp.add(m); return m; };
    const r1 = mk(.03, 0xcfeeff), r2 = mk(.09, 0x58b8ff), r3 = mk(.025, 0xffffff), sh = new TH.Mesh(new TH.SphereGeometry(1, 40, 24), dvRim(0x7ac8ff)); r1.rotation.x = r2.rotation.x = -Math.PI / 2; r3.lookAt(X.B.clone().add(X.F)); sh.position.copy(X.B); sh.frustumCulled = false; X.grp.add(sh); X.bl = { r1, r2, r3, sh, all: [r1, r2, r3, sh], nb: 0 }; }
  const B = X.bl, R1 = 30 + Math.max(0, e) * 430, R2 = 20 + Math.max(0, e - .35) * 330, R3 = 10 + Math.max(0, e) * 260, Rs = 20 + Math.max(0, e) * 220;
  B.r1.visible = e >= 0 && e < 4; B.r1.scale.setScalar(R1); B.r1.material.opacity = .9 * (1 - e / 4); B.r2.visible = e >= .35 && e < 5; B.r2.scale.setScalar(R2); B.r2.material.opacity = .55 * (1 - (e - .35) / 4.65);
  B.r3.visible = e >= 0 && e < 3; B.r3.scale.setScalar(R3); B.r3.material.opacity = .8 * (1 - e / 3); B.sh.visible = e >= 0 && e < 2.6; B.sh.scale.setScalar(Rs); B.sh.material.uniforms.uA.value = .9 * (1 - e / 2.6);
  X.flash.material.opacity = bell01(e, -.15, .05, .35, 2.2); X.flash.scale.setScalar(1700 * (1 + Math.max(0, e) * .15)); X.expK = 1 + 1.4 * bell01(e, -.1, .05, .3, 1.8); X.bR = e >= 0 && e < 4 ? R1 : 0;
  // secondary explosions along the flying wreckage, then fading out
  const b = X.b; if (e > 0 && e < 4.5 && b.pieces && Math.random() < (e < 1.5 ? .7 : .25)) { const P = b.pieces[(Math.random() * b.pieces.length) | 0]; if (P) { P.getWorldPosition(X.V); sbBoom(X, X.V.clone(), t, 50 + Math.random() * 110); } }
  if (!X.fleetBooms) for (const Bm of X.booms) { const a = (t - Bm.t) / 900; Bm.s.visible = a >= 0 && a < 1; if (Bm.s.visible) { Bm.s.material.opacity = (1 - a) * .95; Bm.s.scale.setScalar(Bm.sz * (.4 + a * 1.4)); } }
  // the camera shakes when a wave passes it, hardest at the moment of the blast
  const cam = W.camera; if (cam && e > -2 && e < 4.5) { const d = cam.position.distanceTo(X.B), front = Math.abs(d - R1), amp = (e < 0 ? .6 : 0) + bell01(e, 0, .05, .5, 1.6) * 7 + (front < 140 ? (1 - front / 140) * 9 : 0); cam.position.x += (Math.random() - .5) * amp; cam.position.y += (Math.random() - .5) * amp; cam.position.z += (Math.random() - .5) * amp; } }
