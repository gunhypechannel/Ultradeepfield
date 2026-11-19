  if (cls === "mnexus") { /* the Neural Nexus (the fourth painting) */
    const beam = (a, b, rad, mat) => { const d = b.clone().sub(a), m = add(new TH.Mesh(new TH.CylinderGeometry(rad, rad, d.length(), 6, 1, true), mat)); m.position.copy(a).addScaledVector(d, .5); m.quaternion.setFromUnitVectors(V(0, 1, 0), d.normalize()); return m; };
    add(new TH.Mesh(new TH.CylinderGeometry(3.2, 3.6, .5, 32), C.shell), 0, -1.6, 0);
    for (let i = 0; i < 18; i++) { const a = i / 18 * TAU + r() * .2, R = 3.4 + r() * 1.4; tube([V(Math.cos(a) * 1.5, -1.42, Math.sin(a) * 1.5), V(Math.cos(a) * 3.2, -1.5, Math.sin(a) * 3.2), V(Math.cos(a + .25) * R, -1.75, Math.sin(a + .25) * R), V(Math.cos(a + .4) * (R + .9), -1.6, Math.sin(a + .4) * (R + .9))], .2, .06); }
    for (let i = 0; i < 6; i++) { const a = i / 6 * TAU + .5, b = V(Math.cos(a) * 3.15, -1.4, Math.sin(a) * 3.15), tip = V(Math.cos(a) * 1.9, 3.7 + (i % 2) * .9, Math.sin(a) * 1.9), mid = lerp3(b, tip, .45).add(V(Math.cos(a) * 1.0, 0, Math.sin(a) * 1.0));
      tube([b, lerp3(b, mid, .5).add(V(Math.cos(a) * .3, 0, Math.sin(a) * .3)), mid, tip], .42, .03, C.shell, 6, .8); bundle([b, mid, tip], 3, .38, { t1: .75, r0: .07, r1: .04 }); }
    const top = 2.6, bot = 1.05; add(new TH.Mesh(new TH.CylinderGeometry(top, bot, 2.4, 6, 1, true), C.holo), 0, 1.2, 0);
    for (let i = 0; i < 6; i++) { const a = i / 6 * TAU, a2 = a + TAU / 6; beam(V(Math.cos(a) * bot, 0, Math.sin(a) * bot), V(Math.cos(a) * top, 2.4, Math.sin(a) * top), .028, C.glow); beam(V(Math.cos(a) * top, 2.4, Math.sin(a) * top), V(Math.cos(a2) * top, 2.4, Math.sin(a2) * top), .028, C.glow); beam(V(Math.cos(a) * bot, 0, Math.sin(a) * bot), V(Math.cos(a2) * bot, 0, Math.sin(a2) * bot), .022, C.glow); }
    for (const [rr, y, tx] of [[2.9, 2.45, 0], [1.75, 1.0, .25], [3.3, 2.1, -.12], [2.2, 3.9, .4]]) { const t = add(new TH.Mesh(new TH.TorusGeometry(rr, .02, 6, 72), C.holo), 0, y, 0); t.rotation.set(Math.PI / 2 + tx, 0, 0); }
    const op = V(0, 3.95, 0); orb(.95, C.sac, op, 30); orb(1.55, C.glowS, op, 16);
    beam(V(0, -1.3, 0), V(0, 3.2, 0), .1, C.glowS); beam(V(0, -1.3, 0), V(0, 3.2, 0), .035, C.glow);
    const sc = V(0, 1.35, 0); orb(.22, C.glow, sc, 12); orb(.6, C.glowS, sc, 12);
    for (let i = 0; i < 10; i++) { const a = i / 10 * TAU, d = V(Math.cos(a), (i % 2 ? .25 : -.2), Math.sin(a)); cone(1.15 + (i % 2) * .35, .07, C.claw, sc.clone().addScaledVector(d, .12), d, 0); }
    for (let i = 0; i < 4; i++) { const a = i / 4 * TAU + Math.PI / 4, p = V(Math.cos(a) * 3.05, -.75, Math.sin(a) * 3.05), cr = orb(.42, C.core, p, 8); cr.scale.set(.8, 2.5, .8); orb(.85, C.glowS, p, 10);
      bundle([p.clone().add(V(0, -.8, 0)), p.clone().add(V(Math.cos(a) * .4, -.6, Math.sin(a) * .4)), p.clone().add(V(Math.cos(a) * .9, -.85, Math.sin(a) * .9))], 4, .3, { r0: .09, r1: .05 }); }
    g.userData.mimR = 4.4; return g; }
