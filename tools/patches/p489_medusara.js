  /* ---------- Medusara, the Stone Gaze (owner's art, assets/bosses/medusa/ref, 2026-11-12): a moon-sized face of cracked grey-violet
     stone veined with molten gold, a gold diadem with a red gem, eyes burning red; a crown of gold-armoured serpents with red eyes and
     open fangs writhing round her head; below the chin the stone dissolves into a violet storm of lightning; a gold ring rail with
     gothic ruin towers orbits her. Moves: gaze (Petrifying Gaze: the eyes flare and two red beams sweep the field), lunge (the serpents
     strike forward), storm (lightning bursts from the storm beneath her), ring (the ruin towers fire), hit. Drives (0..1): awake (her
     eyes open, the serpents uncoil), charge (the gaze charging on the shared clock: eyes and gem brighten, serpents rear, then the
     beams), shatter (Shattered Visage: the face cracks wide, gold light pours out, the third eye opens), die (she turns to grey stone
     and crumbles away). snk[i] = 0 severs a serpent. ---------- */
  function medusara() { const grp = new TH.Group(), shk = new TH.Group(), body = new TH.Group(), hull = new TH.Group(); grp.add(shk); shk.add(body); body.add(hull);
    const LO = LOD === 1, RC = [1, .45, .35], S = scr(), RED = 0xff3a2a, GOLD = 0xffc85a;
    const MS = hullMat("med", { rows: 1, cols: 1, pal: ["#3a3542"], slits: 0, sg: "#ff9a20", veins: 70, vc: "#d8a040", metal: .15, rough: .88, rc: [.75, .45, 1], ei: 2.4, rep: [3, 2], relief: 3.6, rust: 0 }); MS.envMapIntensity = .45; MS.normalScale.set(2.6, 2.6);
    const MSd = hullMat("medd", { rows: 1, cols: 1, pal: ["#2a2632"], slits: 0, sg: "#ffa030", veins: 30, vc: "#d89a40", metal: .2, rough: .85, rc: [.75, .45, 1], ei: 2.6, rep: [2, 2], relief: 3 });
    const MG = hullMat("medg", { rows: 3, pal: ["#c8901e", "#e6b23c", "#a87418", "#f5c84a"], bronze: 0, slits: .2, sc: "#fff4d0", sg: "#ff6a3a", metal: 1, rough: .14, rc: [1, .7, .4], ei: 1.8, rep: [3, 1] }); MG.envMapIntensity = 2.2;
    const scT = paint("med_scale", 256, (x, N) => { x.fillStyle = "#3a2c1c"; x.fillRect(0, 0, N, N); for (let r = 0; r < 12; r++) for (let c = 0; c < 8; c++) { const cx = c * N / 8 + (r % 2) * N / 16, cy = r * N / 12; const g = x.createRadialGradient(cx, cy - 4, 1, cx, cy, N / 12); g.addColorStop(0, "#f4cf72"); g.addColorStop(.6, "#b07a26"); g.addColorStop(1, "#2a1c0e"); x.fillStyle = g; x.beginPath(); x.ellipse(cx, cy, N / 15, N / 20, 0, 0, Math.PI); x.fill(); } });
    const MSn = new TH.MeshStandardMaterial({ map: scT, metalness: .95, roughness: .25, envMapIntensity: 2.0, emissive: 0x331006, emissiveIntensity: .4 }); MSn.userData.P = {}; rimOn(MSn, 1, [1, .6, .3]);
    const MSb = new TH.MeshStandardMaterial({ color: 0x2a1c30, metalness: .7, roughness: .35, envMapIntensity: 1.4 }); MSb.userData.P = {}; rimOn(MSb, .8, [.7, .3, 1]);
    const REDM = new TH.MeshBasicMaterial({ color: 0xff6040, toneMapped: false, transparent: true }), WHT = new TH.MeshBasicMaterial({ color: 0xfff0e0, toneMapped: false });
    const put = (par, m, p, r, s) => { m.position.set(...p); if (r) m.rotation.set(...r); if (s != null) { if (typeof s === "number") m.scale.setScalar(s); else m.scale.set(...s); } par.add(m); return m; };
    const sph = (mat, seg = 24) => new TH.Mesh(new TH.SphereGeometry(1, LO ? Math.max(10, seg / 2) : seg, LO ? 8 : Math.round(seg * .7)), mat);
    /* ---- the face: a great stone head looking down +z; forehead, heavy lids, a straight nose, full lips, high cheeks, a strong chin ---- */
    const head = put(hull, new TH.Group(), [0, 14, 0]);
    put(head, sph(MS, 40), [0, 0, 0], null, [11.5, 12.5, 11]);
    put(head, sph(MS, 30), [0, 1.2, 4.2], null, [9.6, 9.8, 7.6]); /* the face plane */
    for (const sx of [-1, 1]) { put(head, sph(MS), [sx * 4.4, -1.4, 8.4], null, [3.0, 2.6, 2.2]); /* cheek */
      put(head, sph(MS), [sx * 3.4, 3.3, 10.6], [0, 0, sx * -.15], [3.0, .9, 1.2]); /* brow */
      put(head, sph(MSd), [sx * 3.3, 1.7, 10.85], [0, 0, sx * .06], [2.4, 1.0, .6]); /* the eye socket */
      put(head, sph(MS), [sx * 3.3, 2.3, 11.15], [.3, 0, sx * .06], [2.5, .55, .7]); /* heavy upper lid */ }
    { const ng = new TH.CylinderGeometry(.7, 1.7, 5.4, 4); put(head, new TH.Mesh(ng, MS), [0, -.6, 11.5], [-.28, Math.PI / 4, 0], [1, 1, .75]); put(head, sph(MS), [0, -3.0, 11.6], null, [1.6, .9, 1.0]); }
    put(head, sph(MS), [0, -5.3, 10.6], null, [2.7, .75, 1.1]); put(head, sph(MS), [0, -6.5, 10.4], null, [2.3, .85, 1.1]); /* lips */
    put(head, sph(MS), [0, -1.2, 10.2], null, [7.2, 5.2, 1.6]); /* the mid-face, smoothing cheeks into the nose */
    const lipL = put(head, new TH.Mesh(new TH.BoxGeometry(4.6, .14, .3), new TH.MeshBasicMaterial({ color: 0x2a0a10 })), [0, -5.85, 11.55]);
    put(head, sph(MS), [0, -9.0, 8.6], null, [3.4, 2.4, 2.8]); /* chin */
    // the eyes: red-hot irises in dark sockets
    const eyes = [-1, 1].map(sx => { const g = put(head, new TH.Group(), [sx * 3.3, 1.65, 11.25]); put(g, sph(REDM, 16), [0, 0, 0], null, [1.5, .55, .4]); const c = put(g, sph(WHT, 12), [0, 0, .25], null, [.45, .3, .2]);
      const s = sprite(9, "rgba(255,80,50,1)", "med_eye"); s.position.z = .8; g.add(s); return { g, s, c }; });
    // the diadem: a gold band over the brow, a spiked crest, a red gem (the third eye, which opens in the Shattered Visage)
    put(head, new TH.Mesh(new TH.TorusGeometry(10.6, .55, 6, LO ? 40 : 64, Math.PI * 1.1), MG), [0, 5.6, -.6], [Math.PI / 2 - .32, 0, Math.PI * -.05 - Math.PI * .5]);
    for (let i = 0; i < 9; i++) { const a = (i - 4) * .2; put(head, new TH.Mesh(new TH.ConeGeometry(.55, 3.4 - Math.abs(i - 4) * .45, 4), MG), [Math.sin(a) * 10.4, 7.6 + Math.cos(a) * .4 - Math.abs(i - 4) * .3, Math.cos(a) * 9.3 - 1.4], [-.35, 0, -a * .9]); }
    const gemG = put(head, new TH.Group(), [0, 6.4, 11.0]); put(gemG, new TH.Mesh(new TH.OctahedronGeometry(1.1, 0), new TH.MeshBasicMaterial({ color: 0xff3a50, toneMapped: false })), [0, 0, 0], null, [1, 1.35, .5]); put(gemG, new TH.Mesh(new TH.TorusGeometry(1.5, .25, 5, 18), MG), [0, 0, -.1]);
    const gemS = sprite(7, "rgba(255,70,90,1)", "med_gem"); gemS.position.z = .8; gemG.add(gemS);
    // the cracks of the Shattered Visage: glowing gold seams that widen
    const crG = new TH.BufferGeometry(), crP = []; { for (let k = 0; k < 9; k++) { let a = rnd() * TAU, b = (rnd() - .3) * 1.4, p = [Math.cos(a) * Math.cos(b), Math.sin(b), Math.sin(a) * Math.cos(b)]; for (let j = 0; j < 7; j++) { const q = [p[0] + (rnd() - .5) * .25, p[1] + (rnd() - .5) * .25, p[2] + (rnd() - .5) * .25], l = Math.hypot(...q); crP.push(p[0] * 11.7, p[1] * 12.7, p[2] * 11.2 + (p[2] > 0 ? 1.2 : 0), q[0] / l * 11.7, q[1] / l * 12.7, q[2] / l * 11.2 + (q[2] / l > 0 ? 1.2 : 0)); p = q.map(v => v / l); } } }
    crG.setAttribute("position", new TH.BufferAttribute(new Float32Array(crP), 3)); const cracks = new TH.LineSegments(crG, new TH.LineBasicMaterial({ color: 0xffd070, transparent: true, opacity: 0, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); cracks.userData.dyn = 1; head.add(cracks);
    const shine = sprite(40, "rgba(255,190,90,1)", "med_shine"); shine.material.opacity = 0; shine.position.set(0, 0, 6); head.add(shine);
    /* ---- the storm beneath her: violet energy where the stone ends, and lightning ---- */
    const storm = put(body, new TH.Mesh(new TH.SphereGeometry(13, LO ? 20 : 32, LO ? 14 : 22, 0, TAU, Math.PI * .55, Math.PI * .45), auraMat(0xa050ff, 1)), [0, 13, 0]); storm.userData.dyn = 1;
    const stormS = sprite(64, "rgba(170,80,255,1)", "med_storm"); stormS.position.set(0, 0, 4); stormS.material.opacity = .5; body.add(stormS);
    const bt = bolts(body, LO ? 8 : 14, () => { const a = rnd() * TAU, b = rnd() * TAU; return [V(Math.cos(a) * 9, 4 + rnd() * 4, Math.sin(a) * 9), V(Math.cos(b) * 20, -6 - rnd() * 10, Math.sin(b) * 20)]; }, 0xd8a0ff);
    /* ---- the serpent crown: gold-scaled snakes rising from her head, red-eyed, fangs bared ---- */
    const NSN = 8, snakes = []; for (let i = 0; i < NSN; i++) { const a = -2.5 + i / (NSN - 1) * 5.0, root = V(Math.sin(a) * 10.5, 14 + Math.cos(a) * 10.5, -3.5), out = V(Math.sin(a), Math.cos(a) + .25, .15).normalize();
      const g = put(body, new TH.Group(), root.toArray()); g.userData.dyn = 1; const L = 15 + (i % 3) * 3, pts = [], up = V(0, 1, 0), fw = V(0, 0, 1);
      for (let k = 0; k <= 10; k++) { const u = k / 10, w = Math.sin(u * Math.PI * 1.6 + i) * 1.4 * (1 - u * .5); pts.push(out.clone().multiplyScalar(L * .7 * u).addScaledVector(up, L * .3 * Math.sin(u * Math.PI * .85) + w).addScaledVector(fw, L * .55 * u * u)); }
      const tube = put(g, new TH.Mesh(taper(pts, 2.1, LO ? 18 : 30, 9, .45), MSn), [0, 0, 0]);
      const tip = pts[10], hd = put(g, new TH.Group(), tip.toArray(), null, 1.9); const dir = pts[10].clone().sub(pts[9]).normalize().lerp(fw, .5).normalize(); hd.quaternion.setFromUnitVectors(V(0, 0, 1), dir);
      { const sk = new TH.ConeGeometry(1, 2.8, 6); sk.rotateX(Math.PI / 2); sk.translate(0, 0, 1.2); put(hd, new TH.Mesh(sk, MSn), [0, .15, 0], null, [1.15, .55, 1]); put(hd, sph(MSn, 12), [0, .1, -.2], null, [1.15, .7, 1.1]); }
      const jaw = put(hd, new TH.Group(), [0, -.25, -.3]); { const jg = new TH.ConeGeometry(.85, 2.5, 6); jg.rotateX(Math.PI / 2); jg.translate(0, 0, 1.3); put(jaw, new TH.Mesh(jg, MSn), [0, 0, 0], null, [1, .4, 1]); put(jaw, sph(new TH.MeshBasicMaterial({ color: 0xc01828, toneMapped: false }), 8), [0, .12, 1.0], null, [.6, .12, 1.0]); }
      for (const sx of [-1, 1]) { put(hd, new TH.Mesh(new TH.ConeGeometry(.1, .8, 5), WHT), [sx * .4, -.15, 2.0], [Math.PI, 0, 0]); const e = sprite(2.0, "rgba(255,50,30,1)", "med_se"); e.position.set(sx * .62, .5, .6); hd.add(e); put(hd, sph(REDM, 8), [sx * .58, .42, .55], null, [.22, .14, .2]); }
      snakes.push({ g, hd, jaw, pts, a, i, cut: 0, base: g.quaternion.clone() }); }
    /* ---- the gold ring rail with gothic ruin towers, orbiting at a tilt ---- */
    const RR = put(body, new TH.Group(), [0, 10, 0], [.3, 0, .2]); const ringR = 27;
    RR.add(band(ringR, 1.4, 1.0, MG, 0, TAU, LO ? 60 : 110, 26)); put(RR, new TH.Mesh(new TH.TorusGeometry(ringR + .9, .16, 4, LO ? 60 : 110), new TH.MeshBasicMaterial({ color: 0xffd070, toneMapped: false })), [0, 0, 0], [Math.PI / 2, 0, 0]);
    const towers = []; for (let i = 0; i < 6; i++) { const a = i / 6 * TAU + .3, t = put(RR, new TH.Group(), [Math.sin(a) * ringR, 0, Math.cos(a) * ringR], [0, a, 0]);
      put(t, new TH.Mesh(new TH.BoxGeometry(2.2, 6, 2.2), MSd), [0, 3.2, 0]); for (const sx of [-1, 1]) put(t, new TH.Mesh(new TH.BoxGeometry(.7, 4.6, .7), MSd), [sx * 1.6, 7.4, 0]); put(t, new TH.Mesh(new TH.TorusGeometry(1.6, .35, 4, 10, Math.PI), MSd), [0, 9.6, 0]);
      put(t, new TH.Mesh(new TH.ConeGeometry(.6, 2.2, 4), MSd), [0, 11.6, 0]); const w = sprite(2.4, "rgba(255,170,80,1)", "med_tw"); w.position.set(0, 4, 1.2); t.add(w); put(t, new TH.Mesh(new TH.BoxGeometry(3, 2.2, 3), MSd), [0, -1.4, 0]); towers.push({ t, w }); }
    /* ---- the gaze: two red beams from her eyes, sweeping; their flare; ring bolts; waves ---- */
    const beams = [-1, 1].map(sx => { const g = new TH.Group(); body.add(g); g.userData.dyn = 1; for (const [r, o, c] of [[1.4, .5, RED], [.45, 1, 0xffe0d0]]) { const geo = new TH.CylinderGeometry(r, r * .7, 1, 12, 1, true); geo.translate(0, .5, 0); geo.rotateX(Math.PI / 2); g.add(new TH.Mesh(geo, glowMat(c, o))); } g.visible = false; return g; });
    const flare = sprite(24, "rgba(255,90,60,1)", "med_fl"); flare.material.opacity = 0; flare.position.set(0, 15.6, 13); body.add(flare);
    const rbs = []; for (let i = 0; i < 12; i++) { const s = sprite(3.2, "rgba(255,190,110,1)", "med_rb"); s.material.opacity = 0; body.add(s); rbs.push(s); }
    const wv = wave(body, 18, false, 0xd090ff), wvS = wave(body, 16, true, 0xff7050);
    /* ---- the moves ---- */
    const mv = moves({ gaze: 3600, lunge: 2400, storm: 2600, ring: 2800, hit: 520 }), hit = hitKit(body, shk), drv = {}, f = (n, t) => drv[n] != null ? drv[n] : mv.f(n, t);
    const out = { grp, r: 30, h: 36, snk: Array(NSN).fill(1), act: n => mv.play(n), drive: (n, v) => { if (v == null || v < 0) delete drv[n]; else drv[n] = v; }, moves: ["gaze", "lunge", "storm", "ring"], mouth: head, reactor: gemG };
    const MSe = MS.emissiveIntensity, MGe = MG.emissiveIntensity, gray = new TH.Color(.55, .55, .58), white = new TH.Color(1, 1, 1);
    const tick = t => { const T = t * .001, aw = drv.awake != null ? drv.awake : 1, ch = f("charge", t), sh = drv.shatter != null ? drv.shatter : 0, fd = f("die", t), die = fd < 0 ? 0 : fd;
      const fg = f("gaze", t), fl = f("lunge", t), fs = f("storm", t), fr = f("ring", t), fh = f("hit", t), live = 1 - ss(.15, .5, die);
      const eyeO = ss(.35, .55, aw) * live, coil = ss(.4, .9, aw), chg = ch < 0 ? 0 : ss(0, .7, ch) * (1 - ss(.94, 1, ch)), fire = Math.max(bell(fg, .3, .38, .78, .92), ch < 0 ? 0 : bell(ch, .72, .76, .92, .98));
      // she breathes; the face tilts to her prey
      head.rotation.set(Math.sin(T * .3) * .03 - chg * .08, Math.sin(T * .21) * .07, Math.sin(T * .17) * .02); body.position.y = Math.sin(T * .5) * .5 - ss(.5, 1, die) * 4;
      MS.emissiveIntensity = MSe * (.35 + .65 * aw) * live * (1 + sh * 1.2 + chg * .5); MG.emissiveIntensity = MGe * (.6 + .4 * aw) * live; MS.color.copy(white).lerp(gray, ss(.1, .4, die));
      eyes.forEach(E => { E.g.children[0].material.opacity = eyeO; E.c.visible = eyeO > .05; E.s.material.opacity = Math.min(1, eyeO * (.6 + .2 * Math.sin(T * 3) + chg * .3 + fire * .3)); E.s.scale.setScalar(9 * (1 + chg * .6 + fire * .5) * (eyeO > 0 ? 1 : 0)); });
      gemS.material.opacity = (.5 + chg * .5 + sh * .6) * live * aw; gemS.scale.setScalar(7 * (1 + sh * 1.6 + chg * .6)); gemG.scale.setScalar(1 + sh * .5);
      cracks.material.opacity = Math.max(sh * (.7 + .3 * Math.sin(T * 5)), bell(die, .05, .2, .5, .7)); shine.material.opacity = sh * .55 * live; lipL.scale.y = 1 + chg * 6 + fire * 8;
      storm.material.uniforms.uK.value = (.5 + .5 * aw) * live * (1 + bell(fs, 0, .2, .7, 1) * 1.5 + chg * .4); stormS.material.opacity = (.3 + .2 * Math.sin(T)) * aw * live * (1 + bell(fs, 0, .2, .7, 1)); bt(t, (1 + bell(fs, .1, .2, .8, .95) * 6 + chg * 3) * live * aw);
      // the serpents: sway, rear while she charges, strike in the lunge; severed ones are gone
      snakes.forEach((Sn, i) => { const cut = out.snk[i] ? 0 : 1; Sn.cut += (cut - Sn.cut) * .08; Sn.g.visible = Sn.cut < .98 && live > .02;
        const ln = fl < 0 ? 0 : bell(fl, .1 + (i % 4) * .05, .3 + (i % 4) * .05, .55, .85), sw = Math.sin(T * 1.3 + i * 1.7) * .12 * coil;
        Sn.g.rotation.set(-ln * .9 + chg * -.25 + (1 - coil) * .8, sw + Math.sin(Sn.a) * ln * .2, Math.sin(T * .9 + i) * .08 + (1 - coil) * Math.sign(Sn.a) * .6); Sn.g.scale.setScalar((1 - Sn.cut) * (.45 + .55 * coil) * (1 - ss(.2, .55, die)) + .001);
        Sn.jaw.rotation.x = .3 + ln * .5 + chg * .35 + Math.max(0, Math.sin(T * 2 + i)) * .12; });
      // the ring and its towers
      RR.rotation.y = T * .05; towers.forEach((w, i) => { w.w.material.opacity = (.5 + .5 * Math.sin(T * 2 + i)) * aw * live + bell(fr, .1, .25, .7, .9); }); RR.scale.setScalar(1 - ss(.3, .8, die) * .4); RR.visible = die < .95;
      body.updateMatrixWorld(); rbs.forEach((B, i) => { const k = fr < 0 ? -1 : (fr - .2 - (i % 6) * .05) / .45, on = k > 0 && k < 1; B.material.opacity = on ? 1 - k * .5 : 0; if (on) { towers[i % 6].t.getWorldPosition(S.v); body.worldToLocal(S.v); B.position.set(S.v.x * (1 - k * .6), S.v.y + 8 - k * 4, S.v.z + k * 70); B.scale.setScalar(3.2 + k * 3); } });
      // the gaze: two beams from the eyes, sweeping across the field
      beams.forEach((g, j) => { g.visible = fire > .02 && live > .2; if (!g.visible) return; const E = eyes[j]; E.g.getWorldPosition(S.v); body.worldToLocal(S.v); g.position.copy(S.v); const sweep = (fg >= 0 ? (fg - .55) : (ch - .85)) * 2.2;
        g.rotation.set(.18 + Math.sin(T * 2) * .03, sweep * (j ? 1 : 1) + (j ? -.06 : .06), 0); g.scale.set(1 + chg, 1 + chg, 140); g.children[0].material.opacity = .5 * fire * (.85 + Math.random() * .15); g.children[1].material.opacity = fire; });
      flare.material.opacity = Math.max(chg * .3, fire * .5) * live; flare.scale.setScalar(20 + chg * 14 + fire * 10);
      wv(fs < 0 ? (ch >= 0 && ch > .74 ? (ch - .74) / .26 : -1) : (fs - .3) / .7); wvS(fg >= 0 ? (fg - .35) / .65 : -1);
      // death: grey stone, the light gone, crumbling down and fading
      hull.scale.setScalar(1 - ss(.55, 1, die) * .15); hull.position.y = -ss(.5, 1, die) * 6; storm.visible = die < .5; stormS.visible = die < .5; grp.visible = die < .99;
      hit(bell(fh, 0, .05, .4, 1), t); };
    out.tick = tick; tick(0); bake(body); return out; }
