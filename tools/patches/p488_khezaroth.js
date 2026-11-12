  /* ---------- Khezaroth, the Dark Matter Sphinx (owner's art and brief, assets/bosses/khezaroth/ref, 2026-11-12): a colossal lion body
     of living dark matter (black, veined with flowing violet light) lying in the sphinx pose, armoured in black obsidian plate with gold
     Egyptian trim; an alien-pharaoh face under a striped nemes and a tall crown with a cobra and a violet gem, a gold halo behind it;
     brilliant violet eyes; a gold collar and a winged scarab on the chest; gigantic armoured forepaws with gold claws, and between them a
     miniature black hole; floating pyramids round its head; two great broken rune rings turning round it; three rune anchors (gravity,
     runes, void) that shield it once the seals wake.
     Moves: claw (Abyssal Claw: a forepaw rises and sweeps a dark arc), crush (Gravity Crush: the singularity swells and drags),
     barrage (Rune Barrage: the rings and pyramids fire rune bolts), pulse (a gravitational shockwave), ag / ar / av (each anchor's own
     attack, with its warning flare), hit. Drives (0..1, from the shared clock on the map): awake (the awakening: dark, runes ignite,
     eyes open, paws extend, the black hole forms, the pulse), judge (Judgment of the Abyss: the head lifts, the paws rise, the black
     hole swells, starlight bends into it, then the shockwave), heart (the chest armour parts and the dark-matter heart shows), die (the
     rings fracture, the black hole destabilizes, the light fades, the body breaks into fragments that implode). anchOn shows the
     anchors, anch[i] = 0 breaks one; relic = 1 leaves only its broken head and a ring shard. ---------- */
  function khezaroth() { const grp = new TH.Group(), shk = new TH.Group(), body = new TH.Group(), hull = new TH.Group(); grp.add(shk); shk.add(body); body.add(hull);
    const LO = LOD === 1, RC = [.72, .36, 1], VIOL = 0xa860ff, GOLD = 0xffc85a, S = scr();
    const MO = hullMat("khz", { rows: 6, pal: ["#17121f", "#1d1628", "#120d19", "#221a30", "#19131f"], slits: .16, sc: "#ecd4ff", sg: "#b066ff", veins: 12, vc: "#a868ff", metal: .92, rough: .2, rc: RC, ei: 3.2, rep: [2, 1] }); MO.envMapIntensity = 1.7; MO.normalScale.set(2.2, 2.2);
    const MB = hullMat("khzb", { rows: 1, cols: 1, pal: ["#130a20"], slits: 0, sg: "#a64cff", veins: 46, vc: "#c48cff", metal: .4, rough: .52, rc: RC, ei: 4.0, rep: [3, 2], relief: 1.4 }); MB.envMapIntensity = 1.2;
    const MG = hullMat("khzg", { rows: 3, pal: ["#c8901e", "#e6b23c", "#a87418", "#f5c84a"], bronze: 0, slits: .2, sc: "#fff4d0", sg: "#c070ff", metal: 1, rough: .12, rc: [1, .8, .45], ei: 2.0, rep: [2, 1] }); MG.envMapIntensity = 2.3; MG.normalScale.set(2, 2);
    const strT = paint("khz_str", 256, (x, N) => { for (let i = 0; i < 16; i++) { x.fillStyle = i % 2 ? "#1a1326" : "#d4b062"; x.fillRect(0, i * N / 16, N, N / 16); } x.fillStyle = "rgba(255,255,255,.14)"; for (let i = 0; i < 16; i++) x.fillRect(0, i * N / 16, N, 1.5); });
    const strE = paint("khz_stre", 256, (x, N) => { x.fillStyle = "#000"; x.fillRect(0, 0, N, N); for (let i = 1; i < 16; i += 2) { x.fillStyle = "#8a3cff"; for (let k = 0; k < 6; k++) x.fillRect(k * N / 6 + 8, i * N / 16 + N / 48, N / 11, N / 70); } });
    const MS = new TH.MeshStandardMaterial({ map: strT, emissive: 0xffffff, emissiveMap: strE, emissiveIntensity: 2.4, metalness: .9, roughness: .24, side: TH.DoubleSide, envMapIntensity: 1.9 }); MS.userData.P = {}; rimOn(MS, 1, RC);
    const CORE = new TH.MeshBasicMaterial({ color: 0xf4e6ff, toneMapped: false }), GL = glowMat(VIOL, .85), BLK = new TH.MeshBasicMaterial({ color: 0x000000 });
    const put = (par, m, p, r, s) => { m.position.set(...p); if (r) m.rotation.set(...r); if (s != null) { if (typeof s === "number") m.scale.setScalar(s); else m.scale.set(...s); } par.add(m); return m; };
    const lathe = (pr, seg, mat, a0 = 0, aL = TAU) => new TH.Mesh(new TH.LatheGeometry(pr.map(([r, y]) => new TH.Vector2(r, y)), LO ? Math.max(8, seg * .6 | 0) : seg, a0, aL), mat);
    const shell = (r, len, a0, aL, mat) => { const g = new TH.CylinderGeometry(r, r, len, LO ? 10 : 18, 1, true, a0, aL); g.rotateX(Math.PI / 2); return new TH.Mesh(g, mat); };
    /* ---- the body: a lion's torso of dark matter, haunches folded, lying along z (the face looks down +z) ---- */
    const TP = [[0, -13.5], [3.2, -12.6], [5.0, -10.5], [5.6, -7.5], [5.0, -4], [4.8, -1], [5.6, 2.5], [6.3, 5.0], [5.6, 7.2], [3.4, 8.6], [0, 9.0]];
    const rAt = z => { for (let i = 1; i < TP.length; i++) if (z <= TP[i][1]) { const [r0, z0] = TP[i - 1], [r1, z1] = TP[i]; return r0 + (r1 - r0) * (z - z0) / (z1 - z0); } return 0; };
    const torso = put(hull, lathe(TP, 24, MB), [0, 6.5, 0], [Math.PI / 2, 0, 0], [1, 1, .82]);
    const aura = put(hull, new TH.Mesh(torso.geometry, auraMat(VIOL, .7)), [0, 6.5, 0], [Math.PI / 2, 0, 0], [1.05, 1.03, .87]); aura.userData.dyn = 1;
    // segmented obsidian back plates with gold edges, and a gold dorsal ridge
    for (let z = -11; z <= 6; z += 2.4) { const r = rAt(z) * 1.04 + .15, p = put(hull, shell(r, 2.3, Math.PI * .58, Math.PI * .84, MO), [0, 6.5, z], null, [1, .86, 1]); p.material = MO;
      put(hull, new TH.Mesh(new TH.TorusGeometry(r + .06, .13, 4, LO ? 14 : 22, Math.PI * .84), MG), [0, 6.5, z + 1.15], [0, 0, Math.PI * .08], [1, .86, 1]); }
    hull.add(beam(V(0, 11.4, -11), V(0, 12.2, 6), .55, .4, .5, MG));
    // haunches and hind paws, a tail curled along the right flank
    for (const sx of [-1, 1]) { put(hull, new TH.Mesh(new TH.SphereGeometry(1, LO ? 12 : 20, LO ? 8 : 14), MB), [sx * 3.9, 5.6, -8.6], null, [3.4, 4.4, 6.0]);
      put(hull, new TH.Mesh(new TH.SphereGeometry(1, LO ? 10 : 16, 8, 0, TAU, 0, Math.PI * .45), MO), [sx * 4.6, 6.0, -8.6], [0, 0, sx * -.35], [4.2, 4.6, 6.1]);
      put(hull, new TH.Mesh(new TH.TorusGeometry(4.3, .12, 4, 24), MG), [sx * 6.2, 5.4, -8.6], [0, Math.PI / 2, 0], [1.15, 1, 1.38]);
      const hp = put(hull, lathe([[0, -2.4], [1.5, -2], [1.9, 0], [1.6, 2], [0, 2.6]], 14, MB), [sx * 5.6, 1.5, -3.2], [Math.PI / 2, 0, 0], [1, 1, .6]);
      for (let c = 0; c < 3; c++) { const cl = put(hull, horn(1.6, .8, .32, MG), [sx * 5.6 + (c - 1) * .9, 1.0, -.7], [0, -Math.PI / 2, 0]); cl.scale.set(1, 1, 1); } }
    { const pts = []; for (let i = 0; i <= 10; i++) { const u = i / 10, a = u * 2.4; pts.push(V(4.2 + Math.sin(a) * 3.2 * u, 2.2 + Math.sin(u * 3) * .8, -12.5 + u * 11 + Math.cos(a) * -2)); } put(hull, new TH.Mesh(taper(pts, .75, LO ? 14 : 22, 7, .25), MB), [0, 0, 0]);
      put(hull, new TH.Mesh(new TH.ConeGeometry(.6, 2.2, 5), MG), [pts[10].x, pts[10].y, pts[10].z + 1], [Math.PI / 2, 0, 0]); }
    /* ---- the forelegs: shoulder, a forearm reaching forward with gold bracers, a great paw with four gold claws ---- */
    const legs = [-1, 1].map(sx => { const sh = put(hull, new TH.Group(), [sx * 4.7, 7.6, 4.4]);
      put(sh, new TH.Mesh(new TH.SphereGeometry(3.1, LO ? 12 : 18, 12), MB), [0, 0, 0], null, [1, 1.15, 1.2]); put(sh, new TH.Mesh(new TH.SphereGeometry(3.3, LO ? 10 : 16, 8, 0, TAU, 0, Math.PI * .5), MO), [sx * .2, .5, 0], [0, 0, sx * -.5], [1, 1, 1.15]); put(sh, new TH.Mesh(new TH.TorusGeometry(3.0, .13, 4, 26), MG), [sx * 1.0, .2, 0], [0, Math.PI / 2, sx * -.5], [1.15, 1, 1]);
      put(sh, new TH.Mesh(taper([V(0, 0, 0), V(0, -2.4, 1.2), V(0, -4.6, 2.3)], 2.2, 10, 9, .8), MB), [0, 0, 0]);
      const fa = put(sh, new TH.Group(), [0, -4.9, 2.4]); put(fa, new TH.Mesh(new TH.SphereGeometry(1.85, 12, 10), MB), [0, 0, 0]);
      put(fa, new TH.Mesh(taper([V(0, 0, 0), V(0, -.3, 4.5), V(0, -.6, 8.8)], 1.85, 12, 9, .78), MB), [0, 0, 0]);
      for (const z of [2.2, 5.0, 7.4]) { put(fa, new TH.Mesh(new TH.CylinderGeometry(1.95 - z * .03, 2.0 - z * .03, 1.5, LO ? 10 : 16, 1, true), MO), [0, -z * .07, z], [Math.PI / 2, 0, 0]); put(fa, new TH.Mesh(new TH.TorusGeometry(2.02 - z * .03, .12, 4, LO ? 14 : 22), MG), [0, -z * .07, z + .75]); put(fa, new TH.Mesh(new TH.TorusGeometry(2.02 - z * .03, .12, 4, LO ? 14 : 22), MG), [0, -z * .07, z - .75]); }
      put(fa, new TH.Mesh(new TH.BoxGeometry(.18, .18, 5.6), GL), [sx * 1.9, .2, 4.8]);
      const pw = put(fa, new TH.Group(), [0, -.9, 9.6]); put(pw, lathe([[0, -1.6], [2.2, -1.3], [2.6, .2], [2.2, 1.8], [0, 2.4]], 16, MB), [0, 0, 0], [Math.PI / 2, 0, 0], [1.05, 1, .62]);
      put(pw, new TH.Mesh(new TH.SphereGeometry(2.55, LO ? 10 : 16, 8, 0, TAU, 0, Math.PI * .42), MO), [0, .2, .2], null, [1.02, .62, 1.05]); put(pw, new TH.Mesh(new TH.TorusGeometry(2.45, .1, 4, 22), MG), [0, .55, .2], [Math.PI / 2, 0, 0], [1, 1.05, 1]);
      const claws = []; for (let c = 0; c < 4; c++) { const x = (c - 1.5) * 1.15, cl = put(pw, horn(2.6, 1.5, .42, MG), [x, -.2, 1.6], [0, -Math.PI / 2, 0]); const cg = put(pw, horn(2.6, 1.5, .5, GL), [x, -.2, 1.6], [0, -Math.PI / 2, 0]); cg.userData.dyn = 1; cg.material = glowMat(VIOL, .0); claws.push(cg); }
      return { sh, fa, pw, sx, claws }; });
    /* ---- the chest: the dark-matter heart behind two armour plates, a gold collar, a winged scarab ---- */
    const heartG = put(hull, new TH.Group(), [0, 7.0, 10.2]); put(heartG, new TH.Mesh(new TH.SphereGeometry(1.25, 18, 12), CORE), [0, 0, 0]);
    const heartS = sprite(9, "rgba(206,150,255,1)", "khz_heart"); heartG.add(heartS); const heartR = put(heartG, runeRing(2.6, VIOL, .9), [0, 0, .2]);
    const plates = [-1, 1].map(sx => { const p = put(hull, new TH.Group(), [0, 7.0, 8.3]); put(p, new TH.Mesh(new TH.SphereGeometry(2.9, LO ? 10 : 16, 10, sx > 0 ? Math.PI / 2 : 0, Math.PI / 2 - .04, Math.PI * .22, Math.PI * .56), MO), [0, 0, 0], null, [1, 1.25, .85]);
      put(p, new TH.Mesh(new TH.BoxGeometry(.24, 4.6, .24), MG), [sx * .12, 0, 2.45]); put(p, new TH.Mesh(new TH.BoxGeometry(.12, 3.4, .12), GL), [sx * 1.5, 0, 2.15], [0, sx * .55, 0]); return p; });
    const collar = put(hull, lathe([[3.0, .4], [3.6, 0], [5.6, -1.9], [5.9, -2.3], [5.5, -2.4], [3.2, -.2]], 30, MS), [0, 12.4, 6.9], [.5, 0, 0]);
    { const sc = put(hull, new TH.Group(), [0, 11.0, 9.3], [.35, 0, 0]); put(sc, new TH.Mesh(new TH.SphereGeometry(.85, 14, 10), new TH.MeshBasicMaterial({ color: 0xb46cff, toneMapped: false })), [0, 0, .25]);
      for (const sx of [-1, 1]) { const w = put(sc, new TH.Mesh(bladeGeo(4.4, 1.1, .16), MG), [sx * .4, 0, 0], [0, 0, sx > 0 ? .12 : Math.PI - .12]); w.scale.y = sx; } const sp = sprite(4, "rgba(190,120,255,1)", "khz_gem"); sp.position.set(0, 0, .9); sc.add(sp); }
    put(hull, lathe([[3.6, 0], [3.3, 3.5], [2.9, 6.4]], 18, MB), [0, 9.0, 6.4], [.42, 0, 0]); put(hull, new TH.Mesh(new TH.SphereGeometry(1, LO ? 14 : 22, 14), MB), [0, 7.4, 6.4], null, [5.8, 5.2, 4.2]);
    /* ---- the head: lion-pharaoh face, striped nemes, tall crown with cobra and gem, false beard, gold halo ---- */
    const head = put(hull, new TH.Group(), [0, 14.6, 8.2], null, 1.4); const MF = hullMat("khzf", { rows: 1, cols: 1, pal: ["#1c1626"], slits: 0, sg: "#9a50ff", veins: 8, vc: "#8a58d8", metal: .7, rough: .48, rc: RC, ei: 2.6, rep: [1, 1], relief: .8 }); MF.envMapIntensity = 1.1;
    // the face: a lion's (the owner's art): a broad skull, a heavy furrowed brow, slanted almond eyes with slit pupils, a wide flat
    // nose bridge running down to a dark nose pad, two full whisker pads with glowing whisker lines, a split upper lip, a small chin,
    // and a ruff of mane tufts framing the face under the nemes
    put(head, new TH.Mesh(new TH.SphereGeometry(2.7, LO ? 14 : 24, LO ? 10 : 18), MF), [0, 2.0, 0], null, [1.08, 1.0, 1.0]);
    put(head, new TH.Mesh(new TH.SphereGeometry(1, LO ? 12 : 20, 14), MF), [0, 1.65, 1.35], null, [2.35, 1.75, 1.7]);
    for (const sx of [-1, 1]) { put(head, new TH.Mesh(new TH.SphereGeometry(1, 14, 10), MF), [sx * .9, 3.0, 2.55], [.25, 0, sx * -.32], [1.25, .38, .75]); /* brow ridge */
      put(head, new TH.Mesh(new TH.SphereGeometry(1, 14, 10), MF), [sx * 1.6, 1.45, 1.95], [0, sx * .5, 0], [.8, 1.0, .6]); /* cheek */
      put(head, new TH.Mesh(new TH.SphereGeometry(1, 16, 12), MF), [sx * .58, .66, 3.0], null, [.7, .5, .55]); /* whisker pad */
      for (let k = 0; k < 3; k++) { const w = put(head, new TH.Mesh(new TH.BoxGeometry(2.2, .04, .04), glowMat(VIOL, .7)), [sx * 1.75, .82 - k * .2, 3.15 - k * .05], [0, sx * .3, sx * (.12 - k * .12)]); w.userData.dyn = 1; }
      for (let k = 0; k < 4; k++) put(head, new TH.Mesh(new TH.SphereGeometry(.06, 4, 3), glowMat(VIOL, .9)), [sx * (.4 + (k % 2) * .3), .78 - (k >> 1) * .2, 3.72 - (k % 2) * .1]);
      for (let k = 0; k < 7; k++) { const a = -1.2 + k * .36; put(head, new TH.Mesh(new TH.ConeGeometry(.6, 3.0, 5), k % 3 ? MF : MO), [sx * (2.35 + Math.cos(a) * .55), 1.3 + Math.sin(a) * 2.0, 1.55 - Math.abs(a) * .3], [.2, 0, sx * (-Math.PI / 2 - a * .8)]); } /* mane ruff */ }
    { const nb = new TH.CylinderGeometry(.42, .78, 2.1, 4); put(head, new TH.Mesh(nb, MF), [0, 2.05, 3.0], [-.38, Math.PI / 4, 0], [1, 1, .62]); } /* nose bridge */
    { const np = new TH.CylinderGeometry(.72, .12, .62, 3); np.rotateZ(Math.PI); const n = put(head, new TH.Mesh(np, new TH.MeshStandardMaterial({ color: 0x0a0610, metalness: .6, roughness: .25 })), [0, 1.18, 3.55], [-.35, 0, 0], [1, 1, .55]); n.material.envMap = null; } /* nose pad */
    put(head, new TH.Mesh(new TH.BoxGeometry(.06, .55, .1), MF), [0, .62, 3.62]); put(head, new TH.Mesh(new TH.SphereGeometry(1, 12, 8), MF), [0, -.05, 2.75], null, [.55, .42, .5]); /* lip cleft, chin */
    const mouth = put(head, new TH.Mesh(new TH.TorusGeometry(.9, .05, 4, 16, Math.PI * .5), glowMat(VIOL, .9)), [0, -.25, 3.1], [0, 0, Math.PI * .25]); mouth.userData.dyn = 1;
    const eyeM = new TH.MeshBasicMaterial({ color: 0xb470ff, transparent: true, toneMapped: false }), pupM = new TH.MeshBasicMaterial({ color: 0x14041f });
    const eyes = [-1, 1].map(sx => { const e = put(head, new TH.Mesh(new TH.SphereGeometry(.5, 14, 10), eyeM), [sx * .95, 2.5, 2.95], [0, sx * -.4, sx * .36], [1.15, .36, .3]); e.userData.dyn = 1;
      put(head, new TH.Mesh(new TH.BoxGeometry(.09, .34, .06), pupM), [sx * .95, 2.5, 3.1], [0, sx * -.4, sx * .1]);
      const s = sprite(3.0, "rgba(196,120,255,1)", "khz_eye"); s.position.set(sx * .98, 2.55, 3.35); head.add(s); return s; });
    // the nemes: a striped hood over the crown of the head, flaring to the shoulders, open at the face; two lappets down the chest
    const nemes = put(head, lathe([[.1, 5.25], [1.9, 5.05], [2.85, 4.3], [3.15, 3.0], [3.3, 1.6], [3.45, .3], [3.9, -1.1], [4.7, -2.5], [5.0, -3.0]], 34, MS, .78, TAU - 1.56), [0, 0, -.25]);
    put(head, new TH.Mesh(new TH.TorusGeometry(3.12, .14, 5, 40, TAU - 1.6), MG), [0, 3.0, -.25], [Math.PI / 2, 0, -Math.PI / 2 + .8]);
    for (const sx of [-1, 1]) { put(head, new TH.Mesh(new TH.BoxGeometry(1.6, 5.4, .4), MS), [sx * 3.1, -2.4, 1.9], [.16, 0, sx * -.08]); put(head, new TH.Mesh(new TH.BoxGeometry(1.75, .28, .5), MG), [sx * 3.12, -5.15, 1.45], [.16, 0, sx * -.08]); put(head, new TH.Mesh(new TH.BoxGeometry(.16, 5.4, .5), MG), [sx * 3.95, -2.4, 1.85], [.16, 0, sx * -.08]); }
    const crown = put(head, new TH.Group(), [0, 4.9, -.1], null, .62); put(crown, lathe([[0, 0], [2.1, 0], [2.4, 1.2], [2.05, 3.0], [1.45, 5.0], [.95, 6.6], [1.25, 7.2], [0, 7.7]], 22, MO), [0, 0, 0]);
    for (const [y, r] of [[1.2, 2.42], [3.0, 2.08], [6.75, 1.12]]) put(crown, new TH.Mesh(new TH.TorusGeometry(r, .15, 5, 28), MG), [0, y, 0], [Math.PI / 2, 0, 0]);
    for (let i = 0; i < 7; i++) { const a = Math.PI + (i - 3) * .42; put(crown, new TH.Mesh(new TH.ConeGeometry(.32, 2.2, 4), MG), [Math.sin(a) * 2.3, 1.9, Math.cos(a) * 2.3], [Math.cos(a) * -.35, 0, Math.sin(a) * .35]); }
    { const gem = put(crown, new TH.Mesh(new TH.OctahedronGeometry(.6, 0), new TH.MeshBasicMaterial({ color: 0xc890ff, toneMapped: false })), [0, 2.1, 2.35]); gem.scale.set(1, 1.4, .6); const gs = sprite(3.6, "rgba(200,140,255,1)", "khz_gem"); gs.position.set(0, 2.1, 2.7); crown.add(gs);
      put(crown, new TH.Mesh(taper([V(0, -.2, 2.2), V(0, .9, 2.8), V(0, 2.6, 2.6), V(0, 3.4, 2.9)], .3, 10, 7, .5), MG), [0, 0, 0]); put(crown, new TH.Mesh(new TH.SphereGeometry(.6, 10, 8), MG), [0, 3.4, 2.75], null, [1.3, 1, .45]); }
    const halo = put(head, new TH.Group(), [0, 4.4, -3.4]); put(halo, new TH.Mesh(new TH.TorusGeometry(7.2, .22, 6, LO ? 40 : 72), MG), [0, 0, 0]); const haloR = put(halo, runeRing(6.9, VIOL, .8), [0, 0, -.1]); put(halo, new TH.Mesh(new TH.TorusGeometry(5.0, .1, 4, LO ? 30 : 56), MG), [0, 0, 0]);
    /* ---- floating pyramids round the head ---- */
    const pyrG = new TH.ConeGeometry(1.1, 1.9, 4), pyrE = new TH.EdgesGeometry(pyrG), pyrL = new TH.LineBasicMaterial({ color: GOLD, transparent: true, toneMapped: false });
    const pyrs = []; for (let i = 0; i < (LO ? 6 : 8); i++) { const g = put(body, new TH.Group(), [0, 0, 0]); put(g, new TH.Mesh(pyrG, MO), [0, 0, 0]); const e = new TH.LineSegments(pyrE, pyrL); g.add(e); const tp = sprite(2.2, "rgba(200,140,255,1)", "khz_pyr"); tp.position.y = 1.1; g.add(tp); g.userData.dyn = 1; pyrs.push({ g, tp, a: i / (LO ? 6 : 8) * TAU, h: (i % 3) * 1.6, s: .8 + (i % 2) * .5 }); }
    /* ---- the rune rings: a great broken ring standing behind it, a tilted ring round its body ---- */
    const RA = put(body, new TH.Group(), [0, 16, -9]); const RB = put(body, new TH.Group(), [0, 13, -5], [.1, .95, .18]);
    const arcs = []; const ringOf = (par, R, n, col) => { for (let i = 0; i < n; i++) { const a0 = i / n * TAU + .08, L = TAU / n - .3, g = new TH.Group(); par.add(g); g.userData.dyn = 1;
        const b = band(R, 1.3, .9, MO, a0, L, LO ? 40 : 64, Math.max(4, Math.round(L * R / 4))); b.rotation.x = Math.PI / 2; g.add(b); const t = new TH.Mesh(new TH.TorusGeometry(R + .72, .14, 4, LO ? 30 : 48, L), MG); t.rotation.z = a0 - Math.PI / 2; g.add(t);
        arcs.push({ g, a: a0 + L / 2 - Math.PI / 2 }); }
      const rr = runeRing(R - .2, col, .75); par.add(rr); return rr; };
    const runeA = ringOf(RA, 21, 5, VIOL), runeB = ringOf(RB, 23, 6, 0xc49aff);
    const nodes = []; for (let i = 0; i < 10; i++) { const a = i / 10 * TAU, s = sprite(2.6, "rgba(210,160,255,1)", "khz_node"); s.position.set(Math.cos(a) * 21, Math.sin(a) * 21, .6); RA.add(s); nodes.push(s); }
    /* ---- the singularity between the paws ---- */
    const BH = put(body, new TH.Group(), [0, 3.6, 15.8]); const bhHz = put(BH, new TH.Mesh(new TH.SphereGeometry(1.5, 24, 16), BLK), [0, 0, 0]); bhHz.renderOrder = 2;
    const bhRing = ringSprite(7.5, "khz_bhr", [[0, "rgba(0,0,0,0)"], [.28, "rgba(0,0,0,0)"], [.34, "rgba(255,230,255,1)"], [.46, "rgba(180,100,255,.55)"], [1, "rgba(60,10,160,0)"]]); BH.add(bhRing);
    const accM = new TH.MeshBasicMaterial({ map: accTex(), color: 0xd0a0ff, transparent: true, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false });
    const disc = put(BH, new TH.Mesh(new TH.RingGeometry(1.9, 5.4, LO ? 40 : 72, 1), accM), [0, 0, 0], [-Math.PI / 2 + .38, 0, 0]); disc.userData.dyn = 1;
    const bhGlow = sprite(16, "rgba(150,70,255,1)", "khz_bhg"); bhGlow.material.opacity = .4; BH.add(bhGlow);
    const NP = LO ? 40 : 70, fall = puffs(NP, 0xc890ff); BH.add(fall); const fP = []; for (let i = 0; i < NP; i++) fP.push({ a: rnd() * TAU, r: 2 + rnd() * 9, y: (rnd() - .5) * 3, s: .3 + rnd() * .7 });
    // starlight bending into it (Judgment): streaks that run inward from all round
    const NL = LO ? 36 : 64, lg = new TH.BufferGeometry(); lg.setAttribute("position", new TH.BufferAttribute(new Float32Array(NL * 6), 3)); lg.setAttribute("color", new TH.BufferAttribute(new Float32Array(NL * 6), 3));
    const light = new TH.LineSegments(lg, new TH.LineBasicMaterial({ vertexColors: true, transparent: true, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); light.frustumCulled = false; BH.add(light); const lD = []; for (let i = 0; i < NL; i++) lD.push({ d: V(rnd() - .5, (rnd() - .5) * .8, rnd() - .5).normalize(), o: rnd() });
    // asteroid debris drawn toward it while it wakes, crushes and judges (none at rest)
    const ND = LO ? 20 : 34, deb = inst(new TH.DodecahedronGeometry(1, 0), MO, ND); body.add(deb); const dD = []; for (let i = 0; i < ND; i++) dD.push({ a: rnd() * TAU, r: 14 + rnd() * 26, y: (rnd() - .5) * 18, s: .4 + rnd() * 1.4, sp: rnd() * 6 });
    /* ---- waves, flashes, the claw's dark arc, rune bolts ---- */
    const BW = put(body, new TH.Group(), [0, 3.6, 15.8]); const wR = wave(BW, 6, false, 0xd8b0ff), wS = wave(BW, 7, true, 0xb070ff), wBig = wave(BW, 22, false, 0xe0c0ff), wBigS = wave(BW, 16, true, 0xa060ff);
    const flash = sprite(30, "rgba(235,210,255,1)", "khz_fl"); flash.material.opacity = 0; BW.add(flash);
    const arcM = new TH.Mesh(new TH.RingGeometry(12, 16, 48, 1, 0, Math.PI * .85), glowMat(0x8a40ff, 0)); arcM.userData.dyn = 1; arcM.visible = false; body.add(arcM);
    const RBn = 24, rb = []; for (let i = 0; i < RBn; i++) { const s = sprite(4.2, "rgba(230,190,255,1)", "khz_rb"); s.material.opacity = 0; body.add(s); rb.push({ s, d: i * .035, src: i % 2 ? "n" : "p", k: i }); }
    /* ---- the three anchors: Gravity (violet), Runes (gold), Void (indigo); a barrier shell while they stand ---- */
    const AC = [0xb070ff, 0xffc850, 0x6a6cff], ARGB = ["176,112,255", "255,200,80", "106,108,255"], AP = [V(-26, 10, 10), V(26, 10, 10), V(0, 31, -8)];
    const anchors = AC.map((c, i) => { const g = put(body, new TH.Group(), AP[i].toArray()); g.userData.dyn = 1; const ob = put(g, new TH.Group(), [0, 0, 0], null, 1.6);
      put(ob, new TH.Mesh(new TH.CylinderGeometry(.9, 1.7, 9, 4), MO), [0, 0, 0], [0, Math.PI / 4, 0]); put(ob, new TH.Mesh(new TH.ConeGeometry(1.25, 2.0, 4), MG), [0, 5.5, 0], [0, Math.PI / 4, 0]); put(ob, new TH.Mesh(new TH.ConeGeometry(1.7, 2.2, 4), MG), [0, -5.6, 0], [Math.PI, Math.PI / 4, 0]);
      put(ob, new TH.Mesh(new TH.BoxGeometry(.16, 6.5, .16), glowMat(c, .9)), [0, 0, 1.2]); const ring = put(g, runeRing(5.8, c, .85), [0, 0, 0], [Math.PI / 2, 0, 0]); const ring2 = put(g, runeRing(4.0, c, .7), [0, 2.4, 0], [0, 0, 0]);
      const core = sprite(8, `rgba(${ARGB[i]},1)`, "khz_an" + i); g.add(core); const tg = new TH.CylinderGeometry(.12, .12, 1, 6, 1, true); tg.translate(0, .5, 0); const teth = new TH.Mesh(tg, glowMat(c, .7)); teth.userData.dyn = 1; body.add(teth);
      const fx = new TH.Mesh(new TH.RingGeometry(4.4, 5.4, 48), glowMat(c, 0)); fx.userData.dyn = 1; g.add(fx);
      return { g, ob, ring, ring2, core, teth, fx, c, alive: 1, br: 0 }; });
    const barrier = put(body, new TH.Mesh(new TH.SphereGeometry(19, LO ? 24 : 40, LO ? 16 : 26), auraMat(0x9a60ff, .0)), [0, 9, 2]); barrier.userData.dyn = 1;
    /* ---- death: dark-matter fragments; the relic it leaves ---- */
    const NF = LO ? 40 : 80, frag = inst(new TH.TetrahedronGeometry(1, 0), MO, NF); body.add(frag); frag.visible = false; const fD = []; for (let i = 0; i < NF; i++) fD.push({ p: V((rnd() - .5) * 12, 1 + rnd() * 16, -12 + rnd() * 26), v: V(rnd() - .5, rnd() * .6, rnd() - .5).normalize(), s: .4 + rnd() * 1.3, r: rnd() * 6 });
    const relic = new TH.Group(); body.add(relic); relic.visible = false; { const h2 = head.clone(true); h2.traverse(o => { if (o.isSprite || (o.material && o.material.blending === TH.AdditiveBlending)) o.visible = false; }); h2.position.set(0, 2.2, 2); h2.rotation.set(.35, .5, -.95); relic.add(h2);
      const sh2 = band(10, 1.2, .8, MO, .3, 1.6, 32, 5); sh2.position.set(2, 1, -4); sh2.rotation.set(.9, .4, .2); relic.add(sh2); const rs = sprite(10, "rgba(150,80,255,1)", "khz_rel"); rs.material.opacity = .35; rs.position.set(0, 4, 2); relic.add(rs); }
    /* ---- the moves ---- */
    const mv = moves({ judge: 9000, claw: 2600, crush: 3200, barrage: 2800, pulse: 2200, ag: 2600, ar: 2600, av: 2600, hit: 520 }), hit = hitKit(body, shk), drv = {};
    const f = (n, t) => drv[n] != null ? drv[n] : mv.f(n, t);
    const out = { grp, r: 30, h: 34, anchOn: 0, anch: [1, 1, 1], relic: 0, act: n => mv.play(n), drive: (n, v) => { if (v == null || v < 0) delete drv[n]; else drv[n] = v; }, debris: deb,
      get moves() { return ["claw", "crush", "barrage", "pulse"].concat(out.anchOn ? ["ag", "ar", "av"].filter((n, i) => out.anch[i]) : []); }, mouth: BH, reactor: heartG };
    const MBe = MB.emissiveIntensity, MOe = MO.emissiveIntensity, MSe = MS.emissiveIntensity, MGe = MG.emissiveIntensity, emi = MB.userData.P.emi, q0 = new TH.Quaternion();
    const tick = t => { const T = t * .001;
      const aw = drv.awake != null ? drv.awake : 1, fj = f("judge", t), ht = drv.heart != null ? drv.heart : 0, fd = f("die", t), fc = f("claw", t), fcr = f("crush", t), fba = f("barrage", t), fp = f("pulse", t), fh = f("hit", t);
      const die = fd < 0 ? 0 : fd, live = 1 - ss(.3, .7, die), gone = ss(.86, .93, die);
      // the awakening
      const runeOn = ss(.22, .42, aw), dark = ss(.32, .6, aw), eyeO = ss(.55, .6, aw), paw = ss(.6, .78, aw), bhOn = ss(.74, .86, aw), awP = aw < 1 ? (aw - .88) / .1 : -1;
      // Judgment of the Abyss
      const jw = bell(fj, 0, .06, .8, .86), lift = bell(fj, .08, .3, .8, .9), grow = fj < 0 ? 0 : ss(.18, .74, fj) * (1 - ss(.76, .8, fj)), rel = fj < 0 ? -1 : (fj - .76) / .24, jF = bell(fj, .74, .77, .79, .86);
      const crush = bell(fcr, 0, .2, .75, 1), en = (.35 + dark * .65) * live * (1 + jw * .8 + crush * .4 + ht * .3);
      MB.emissiveIntensity = MBe * en; MO.emissiveIntensity = MOe * (.25 + dark * .75) * live * (1 + jw * .5); MS.emissiveIntensity = MSe * (.3 + dark * .7) * live; MG.emissiveIntensity = MGe * (.5 + dark * .5) * live;
      if (emi) emi.offset.set(T * .006, -T * .018); aura.material.uniforms.uK.value = .55 * en * (1 + Math.sin(T * 1.7) * .15); aura.visible = en > .02;
      // body breathing; the head lifts in Judgment
      body.position.y = Math.sin(T * .7) * .25 - ss(.45, .85, die) * 3; torso.scale.set(1 + Math.sin(T * .7) * .008, 1, .82 + Math.sin(T * .7) * .01);
      head.rotation.set(-lift * .42 + Math.sin(T * .35) * .03 + ss(.5, .85, die) * .3, Math.sin(T * .23) * .06, 0);
      eyeM.opacity = eyeO * live * (.85 + jw * .15); eyes.forEach(e => { e.material.opacity = eyeO * live * (.7 + .3 * Math.sin(T * 3)) ; e.scale.setScalar(3.2 * (1 + bell(aw, .55, .58, .62, .7) * 2.5 + jw * .8)); });
      mouth.material.opacity = .6 * live * (1 + jw);
      // the forelegs: tucked before the awakening, raised in Judgment; the claw sweep
      legs.forEach((L, i) => { L.sh.rotation.set(-(1 - paw) * .5 - lift * .55, 0, 0); L.fa.rotation.set((1 - paw) * .9 - lift * .35, 0, 0); L.pw.rotation.set(lift * .35, 0, 0);
        const cG = jw * .9 + crush * .4 + (fc >= 0 && i === 1 ? .8 : 0); L.claws.forEach(c => { c.material.opacity = cG * live; }); });
      arcM.visible = false; if (fc >= 0) { const R = legs[1], up = bell(fc, 0, .22, .7, .92), sw = ss(.3, .55, fc) * (1 - ss(.75, 1, fc));
        R.sh.rotation.x -= up * .9; R.sh.rotation.y = (ss(.3, .55, fc) - .5) * 1.0 * (1 - ss(.75, 1, fc)) * R.sx * -1; R.sh.rotation.z = up * .25 * R.sx; R.fa.rotation.x -= up * .4; R.pw.rotation.x += up * .5;
        const ak = bell(fc, .3, .38, .55, .72); if (ak > 0) { arcM.visible = true; arcM.material.opacity = ak * .8; arcM.position.set(0, 7, 12); arcM.rotation.set(-Math.PI / 2 + .25, 0, -.4 + ss(.3, .55, fc) * .5); arcM.scale.setScalar(1 + sw * .3); } }
      // the singularity
      const bhS = bhOn * (1 + crush * .7 + grow * 2.4) * (1 - ss(.82, .9, die)) * (die > .1 && die < .82 ? 1 + Math.sin(t * .05) * .12 * ss(.1, .3, die) : 1);
      BH.visible = bhS > .01; BH.scale.setScalar(Math.max(.001, bhS)); disc.rotation.z = -t * .0012 * (1 + crush * 2 + grow * 2); bhGlow.material.opacity = (.35 + grow * .4 + crush * .3) * bhOn; bhRing.material.opacity = bhOn;
      { const pull = 1 + crush * 3 + grow * 3 + jw; fP.forEach((p, i) => { p.a += .012 * pull * (8 / p.r); p.r -= .025 * pull; if (p.r < 1.8) { p.r = 6 + rnd() * 6; p.a = rnd() * TAU; } fall.put(i, Math.cos(p.a) * p.r, p.y * (p.r / 9), Math.sin(p.a) * p.r, p.s * 1.6, bhOn * Math.min(1, (p.r - 1.8) * .5) * .8); }); fall.done(); }
      { const P = lg.attributes.position.array, C = lg.attributes.color.array, k = jw * (1 - ss(.74, .78, fj < 0 ? 0 : fj)); light.visible = k > .01; if (light.visible) lD.forEach((L, i) => { const u = (L.o + t * .0006) % 1, r0 = 60 * (1 - u) + 4, r1 = r0 - 9 - u * 6, j = i * 6, b = Math.sin(u * Math.PI) * k;
          P[j] = L.d.x * r0; P[j + 1] = L.d.y * r0; P[j + 2] = L.d.z * r0; P[j + 3] = L.d.x * r1 + L.d.z * u * 2; P[j + 4] = L.d.y * r1; P[j + 5] = L.d.z * r1 - L.d.x * u * 2; C[j] = .6 * b; C[j + 1] = .45 * b; C[j + 2] = b; C[j + 3] = .95 * b; C[j + 4] = .85 * b; C[j + 5] = b; });
        lg.attributes.position.needsUpdate = true; lg.attributes.color.needsUpdate = true; }
      { const show = aw < .95 || crush > 0 || jw > 0; deb.visible = show && live > .1 && !out.noDeb; if (deb.visible) { const k = Math.max(aw < .95 ? ss(.05, .3, aw) * (1 - ss(.86, .95, aw)) : 0, crush, jw); dD.forEach((d, i) => { const a = d.a + T * (.15 + k * .3), r = d.r * (1 - k * .35 * ((T * .3 + d.sp) % 1)); S.p.set(Math.cos(a) * r, 3.6 + d.y * (1 - k * .3), 15.8 + Math.sin(a) * r * .6); S.q.setFromEuler(S.e.set(T + d.sp, T * .7, 0)); S.s.setScalar(d.s * Math.min(1, k * 3)); S.m.compose(S.p, S.q, S.s); deb.setMatrixAt(i, S.m); }); deb.instanceMatrix.needsUpdate = true; } }
      wR(fp < 0 ? (awP > 0 ? awP : -1) : (fp - .1) / .7); wS(fp < 0 ? (awP > 0 ? awP * .9 : -1) : (fp - .15) / .8); wBig(rel > 0 ? rel * 1.2 : (fcr >= 0 ? 1 - crush : -1)); wBigS(rel > 0 ? rel : -1);
      flash.material.opacity = Math.max(jF * .75, bell(fp, .08, .12, .2, .4) * .5, bell(aw, .88, .9, .92, .98) * .7, bell(die, .84, .86, .88, .94) * .85); flash.scale.setScalar(30 + jF * 30 + bell(die, .84, .86, .88, .94) * 50);
      // the pyramids and rings; the rune barrage
      const spin = 1 + jw * 2 + bell(fba, 0, .1, .8, 1) * 1.5; pyrs.forEach((p, i) => { const a = p.a + T * .25 * spin, r = 9.5 + Math.sin(T + i) * .6; p.g.position.set(Math.cos(a) * r, 22.5 + p.h + Math.sin(T * 1.3 + i) * .7, 8 + Math.sin(a) * r * .7); p.g.rotation.y = T * p.s; p.g.scale.setScalar(p.s * (.3 + .7 * runeOn) * live); p.tp.material.opacity = (.5 + .5 * Math.sin(T * 2 + i)) * runeOn * live * (1 + jw); });
      pyrL.opacity = runeOn * live; RA.rotation.z = T * .05 * spin; RB.rotation.z = -T * .04 * spin; halo.rotation.z = T * .1; haloR.material.opacity = .8 * runeOn * live * (1 + jw * .4);
      runeA.material.opacity = .75 * runeOn * live * (1 + jw * .5 + bell(fba, 0, .1, .8, 1) * .5); runeB.material.opacity = .6 * runeOn * live * (1 + jw * .5); nodes.forEach((n, i) => { n.material.opacity = runeOn * live * (.4 + .6 * Math.max(bell(fba, 0, .1, .7, .9), jw, .4 + .4 * Math.sin(T * 2 + i))); });
      const frac = ss(0, .3, die); arcs.forEach((A, i) => { if (frac > 0) { A.g.position.set(Math.cos(A.a) * frac * 6, Math.sin(A.a) * frac * 6, (i % 2 - .5) * frac * 4); A.g.rotation.z = (i % 2 ? 1 : -1) * frac * .3; A.g.scale.setScalar(Math.max(.001, 1 - ss(.75, .9, die))); } else { A.g.position.set(0, 0, 0); A.g.rotation.z = 0; A.g.scale.setScalar(1); } });
      body.updateMatrixWorld(); rb.forEach((B, i) => { const k = fba < 0 ? -1 : (fba - .15 - B.d) / .4, on = k > 0 && k < 1; B.s.material.opacity = on ? (1 - k * .6) : 0; if (on) { if (B.src === "p") { const p = pyrs[i % pyrs.length].g.position; S.v.copy(p); } else { nodes[i % nodes.length].getWorldPosition(S.v); body.worldToLocal(S.v); } B.s.position.set(S.v.x * (1 - k * .4), S.v.y * (1 - k * .55), S.v.z + k * 70); B.s.scale.setScalar(4.2 + k * 3); } });
      // the anchors: tethered to its shield, each flaring before its own attack; broken ones topple and go dark
      const aOn = out.anchOn && live > .05; let alive = 0;
      anchors.forEach((A, i) => { A.g.visible = !!aOn; A.teth.visible = false; if (!aOn) return; const al = out.anch[i] ? 1 : 0; alive += al; A.br += ((1 - al) - A.br) * .05;
        const fa = f(["ag", "ar", "av"][i], t), warn = bell(fa, 0, .08, .35, .42), fire = bell(fa, .4, .45, .8, .95);
        A.ob.rotation.set(A.br * .9, T * .2 * (1 - A.br), A.br * .5); A.g.position.copy(AP[i]).add(S.v.set(0, Math.sin(T * .8 + i * 2) * .8 - A.br * 6, 0)); A.ring.rotation.z = T * (.4 + warn * 3) * (1 - A.br); A.ring2.rotation.z = -T * .6;
        A.ring.material.opacity = .85 * (1 - A.br) * (1 + warn); A.ring2.material.opacity = .7 * (1 - A.br); A.core.material.opacity = (1 - A.br) * (.7 + .3 * Math.sin(T * 3 + i)) + warn; A.core.scale.setScalar(8 + warn * 14 + fire * 8);
        A.fx.visible = fa >= 0; if (A.fx.visible) { const k = fire; A.fx.material.opacity = Math.max(warn * .9, k * (1 - fa)); A.fx.scale.setScalar(i === 2 ? 1 + k * 8 : 1 + warn * .8); A.fx.rotation.set(i === 2 ? Math.PI / 2 : 0, 0, 0); }
        if (al) { A.teth.visible = true; const to = i === 2 ? S.w.set(0, 16, 0) : S.w.set(AP[i].x * .25, 9, 6); aimAt(A.teth, A.g.position, to); A.teth.scale.set(1 + fire * 3, A.g.position.distanceTo(to), 1 + fire * 3); A.teth.material.opacity = (.35 + .25 * Math.sin(T * 6 + i)) + fire * .6; } });
      barrier.material.uniforms.uK.value = aOn ? (.18 + .1 * Math.sin(T * 1.2)) * alive / 3 + (fh >= 0 ? bell(fh, 0, .05, .4, 1) * .25 * alive / 3 : 0) : 0; barrier.visible = aOn && alive > 0;
      // the unsealed heart
      plates.forEach((p, i) => { const sx = i ? 1 : -1; p.rotation.y = sx * ht * 1.1; p.position.x = sx * (.1 + ht * 1.6); p.position.z = 8.3 + ht * .8; });
      heartS.material.opacity = (.25 + ht * .75) * live * (.85 + .15 * Math.sin(T * 4)); heartS.scale.setScalar(9 * (1 + ht * .6 + Math.sin(T * 4) * .06 * ht)); heartR.material.opacity = ht * live; heartR.rotation.z = T * .8; heartR.scale.setScalar(1 + (ht > .5 ? Math.sin(T * 9) * .04 : 0));
      // death: the body breaks into fragments, they fly, then the implosion pulls them into the singularity
      { const br = ss(.42, .66, die), imp = ss(.72, .86, die); hull.scale.setScalar(1 - br * .25); hull.visible = br < .8; hull.position.y = -br * 2; frag.visible = br > 0 && imp < 1; grp.visible = gone < 1 || !!out.relic;
        if (frag.visible) { fD.forEach((d, i) => { const fl = br * (1 - imp); S.p.copy(d.p).addScaledVector(d.v, fl * 10).lerp(S.w.set(0, 3.6, 15.8), imp); S.q.setFromEuler(S.e.set(T * d.r, T * d.r * .7, 0)); S.s.setScalar(d.s * (1 - imp * .8) * Math.min(1, br * 4)); S.m.compose(S.p, S.q, S.s); frag.setMatrixAt(i, S.m); }); frag.instanceMatrix.needsUpdate = true; } }
      relic.visible = !!out.relic; if (out.relic) { [hull, RA, RB, BH, barrier, deb, frag, arcM, ...pyrs.map(p => p.g), ...anchors.map(A => A.g), ...anchors.map(A => A.teth)].forEach(o => { o.visible = false; }); grp.visible = true; }
      hit(bell(fh, 0, .05, .4, 1), t); };
    out.tick = tick; tick(0); bake(body); return out; }
