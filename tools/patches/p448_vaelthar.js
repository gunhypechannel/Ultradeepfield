  /* ---------- Vaelthar, the Celestial Ruin (owner's art, assets/bosses/vaelthar/ref): a cosmic dragon deity in obsidian-violet scale
     with ornate gold plating and glowing violet sigils, great wings of luminous energy membrane, a radiant core in its chest, and behind
     its back an enormous celestial wheel: a gold outer ring with six stabilizer nodes, counter-rotating inner rings of engraved runes,
     spokes, floating glyph shards and a central focusing aperture, tied to the dragon by violet lightning.
     Moves: claw (Astral Claw), wing (Divine Wingstorm), judge (Celestial Judgment: rune circles fire bolts), seal (Golden Seal),
     rebirth (Celestial Rebirth), annihilate (Divine Annihilation, the full sequence: warning, rune ignition, accumulation, alignment,
     the beam, aftermath), hit. drive(name, f) pins a move to a progress (the galaxy map plays the event from the shared clock);
     stab[i] = 0 disables a stabilizer; crack (0..1) fractures the wheel (Final Eclipse). ---------- */
  function vaelthar() { const grp = new TH.Group(), shk = new TH.Group(), body = new TH.Group(); grp.add(shk); shk.add(body);
    const LO = LOD === 1, RC = [.75, .35, 1], GOLD = 0xffcf6a, VIOL = 0xa05cff;
    const MA = hullMat("vae", { rows: 7, pal: ["#140e1d", "#1b1326", "#100b17", "#22172e", "#181022"], slits: .18, sc: "#e8c8ff", sg: "#b45cff", veins: 10, vc: "#9a5cff", metal: .86, rough: .3, rc: RC, ei: 2.4, rep: [3, 1] });
    const MS = hullMat("vaes", { rows: 4, pal: ["#170f21", "#1f152b", "#120c1a"], slits: .1, sc: "#e8c8ff", sg: "#b45cff", veins: 6, vc: "#9a5cff", metal: .88, rough: .28, rc: RC, ei: 2.0, rep: [1, 1], side: 1 });
    const MG = hullMat("vaeg", { rows: 3, pal: ["#b88a2a", "#d6ad4c", "#a07a22", "#e2bd5c"], bronze: 0, slits: .22, sc: "#fff2c8", sg: "#ffc65a", metal: 1, rough: .2, rc: [1, .78, .4], ei: 1.6, rep: [2, 1] }); MG.envMapIntensity = 1.6;
    const MGd = hullMat("vaegd", { rows: 2, pal: ["#7a5a18", "#8f6c22", "#5f460f"], bronze: 0, slits: .3, sc: "#ffe0a0", sg: "#d070ff", metal: 1, rough: .26, rc: [1, .7, .4], ei: 2.2, rep: [4, 1], glyphs: 1 }); MGd.envMapIntensity = 1.3;
    const CORE = new TH.MeshBasicMaterial({ color: 0xf6e8ff, toneMapped: false });
    /* ---- the spine: torso, neck and tail are chains of armoured scale rings with gold collars, violet seams and gold dorsal blades ---- */
    const NT = 7, NN = LO ? 9 : 12, NL = LO ? 18 : 28, N = NT + NN + NL;
    const scG = new TH.LatheGeometry([[0, -.62], [.82, -.66], [1.04, -.28], [1.0, .3], [.76, .58], [0, .64]].map(([r, y]) => new TH.Vector2(r, y)), LO ? 10 : 14); scG.rotateX(Math.PI / 2);
    const segs = inst(scG, MA, N), colG = new TH.TorusGeometry(1.0, .055, 4, LO ? 18 : 28), cols = inst(colG, MG, N), seamM = new TH.MeshBasicMaterial({ color: 0xffffff, transparent: true, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false }), seams = inst(new TH.TorusGeometry(1.03, .045, 4, LO ? 18 : 30), seamM, N);
    const finG = new TH.ConeGeometry(.22, 1.5, 4); finG.translate(0, 1.5 / 2 + .8, 0); finG.scale(.6, 1, 1.6); const fins = inst(finG, MG, N);
    for (const m of [segs, cols, seams, fins]) body.add(m); for (let i = 0; i < N; i++) seams.setColorAt(i, new TH.Color(.6, .3, 1));
    const P = []; for (let i = 0; i <= N + 1; i++) P.push(V(0, 0, 0)); const SC = new Float32Array(N + 2);
    const st = { lift: 0, sway: 0, coil: 0, curl: 0, spread: 0, beat: 0, recoil: 0, claw: 0, clawS: 1, gape: 0, look: 0 };
    // the chain: neck tip (head) at i = 0, down the neck to the chest, the torso to the hips, then the tail; s = scale of each ring
    const spine = t => { const T = t * .001;
      for (let i = 0; i < NN; i++) { const u = i / (NN - 1), up = 1 - u; // 0 head end .. 1 chest
        const lx = Math.sin(T * .55 + u * 1.6) * .9 * up * (1 - st.lift * .6) + st.sway * up * 2.2, ly = 7.6 + up * (6.2 + st.lift * 2.4) - Math.pow(up, 2) * 1.4 * (1 - st.lift), lz = 2.1 + up * (4.6 - st.lift * 1.7) - st.recoil * up * up * 1.8 + st.look * up * 1.2;
        P[i].set(lx, ly, lz); SC[i] = 1.05 + u * .95; }
      for (let i = 0; i < NT; i++) { const u = i / (NT - 1), k = NN + i; P[k].set(Math.sin(T * .4) * .15 * (1 - u), 6.6 - u * 8.2 + Math.sin(T * .7) * .12, 1.7 - u * 2.9 + st.beat * .15); SC[k] = 2.4 + Math.sin(u * Math.PI) * 1.1 - u * .35; }
      for (let i = 0; i < NL; i++) { const u = (i + 1) / NL, k = NN + NT + i, a = u * (3.3 + st.curl * 1.4) + Math.sin(T * .6 + u * 4) * .35 * u + st.coil * u * 1.2, R = 3.4 + u * 6.5;
        P[k].set(Math.sin(T * .5 + u * 5) * u * 2.4 + Math.sin(a) * u * 4.5, -2.0 - Math.sin(a) * R * .55 - u * 2, -1.6 - (1 - Math.cos(a)) * R * .6 - u * 1.5); SC[k] = 2.0 * (1 - u * .86); }
      P[N].copy(P[N - 1]).multiplyScalar(2).sub(P[N - 2]); };
    /* ---- the head: a long armoured skull, gold crown of swept horns and a forehead blade, a hinged jaw full of teeth, violet-white eyes ---- */
    const head = new TH.Group(); body.add(head); const hd = new TH.Group(); head.add(hd); hd.scale.setScalar(1.25);
    { const sk = new TH.Mesh(new TH.LatheGeometry([[.15, -1.6], [1.15, -1.25], [1.45, -.1], [1.25, 1.3], [.92, 2.6], [.5, 3.6], [.12, 4.1]].map(([r, y]) => new TH.Vector2(r, y)), 14), MA); sk.rotation.x = Math.PI / 2; sk.scale.set(1, 1, .62); sk.position.set(0, .45, 0); hd.add(sk);
      const brow = new TH.Mesh(new TH.LatheGeometry([[.1, -1.0], [1.05, -.6], [1.15, .5], [.8, 1.6], [.2, 2.2]].map(([r, y]) => new TH.Vector2(r, y)), 10, 0, Math.PI), MG); brow.rotation.set(Math.PI / 2, 0, Math.PI / 2); brow.scale.set(1, 1, .5); brow.position.set(0, .95, -.2); hd.add(brow);
      const crest = new TH.Mesh(bladeGeo(5.2, 1.4, .18), MG); crest.rotation.set(0, Math.PI / 2, Math.PI - .35); crest.position.set(0, 1.35, 1.4); hd.add(crest);
      for (const sx of [-1, 1]) { for (let j = 0; j < 4; j++) { const h = new TH.Mesh(taper([V(sx * .7, .9, -.4 - j * .35), V(sx * (1.6 + j * .5), 1.7 + j * .25 - (j > 1 ? .8 : 0), -2.2 - j * .6), V(sx * (2.0 + j * .9), 2.6 + j * .1 - (j > 1 ? 1.9 : 0), -4.8 - j * .9 + (j > 2 ? 1.6 : 0))], .36 - j * .05, 16, 6), j ? MG : MGd); hd.add(h); }
        const ch = beam(V(sx * 1.05, .1, -.6), V(sx * .55, .05, 2.9), .55, .2, .22, MG); hd.add(ch); const ey = new TH.Mesh(new TH.SphereGeometry(.2, 10, 8), CORE); ey.position.set(sx * .78, .62, 1.05); hd.add(ey); } }
    const eyes = []; for (const sx of [-1, 1]) { const e = sprite(1.6, "rgba(225,190,255,1)", "vae_eye"); e.position.set(sx * .8, .64, 1.15); hd.add(e); eyes.push(e); }
    const jaw = new TH.Group(); jaw.position.set(0, -.15, -.9); hd.add(jaw);
    { const lj = new TH.Mesh(new TH.LatheGeometry([[1.05, 0], [.95, 1.5], [.62, 3.0], [.2, 3.9]].map(([r, y]) => new TH.Vector2(r, y)), 12, Math.PI / 2, Math.PI), MS); lj.rotation.x = Math.PI / 2; lj.scale.set(1, 1, .5); jaw.add(lj);
      for (let q = 0; q < 7; q++) for (const sx of [-1, 1]) { const f = shard(.11, .55 - q * .03, MG); f.position.set(sx * (.86 - q * .1), .02, .6 + q * .48); f.rotation.z = sx * .2; jaw.add(f); }
      for (const sx of [-1, 1]) { const g = beam(V(sx * .9, -.2, .2), V(sx * .3, -.25, 3.6), .4, .15, .18, MG); jaw.add(g); } }
    for (let q = 0; q < 7; q++) for (const sx of [-1, 1]) { const f = shard(.1, .5 - q * .03, MG); f.position.set(sx * (.86 - q * .1), -.05, .6 + q * .48); f.rotation.set(Math.PI, 0, -sx * .2); hd.add(f); }
    const mouth = new TH.Object3D(); mouth.position.set(0, .05, 3.3); hd.add(mouth);
    const orb = new TH.Mesh(new TH.SphereGeometry(1, 20, 14), glowMat(0xe6c8ff, .0)); orb.userData.dyn = 1; mouth.add(orb); const orbS = sprite(6, "rgba(235,215,255,1)", "vae_orb"); mouth.add(orbS); orbS.material.opacity = 0;
    // the beam (in the model's own frame, used by the close-up viewer; the galaxy map draws its own at world scale)
    const lens = new TH.Group(); mouth.add(lens); lens.visible = false; const bm = [];
    for (const [r, o, c] of [[2.4, .2, 0x8a40ff], [1.3, .42, 0xc890ff], [.5, .8, 0xf4e8ff]]) { const g = new TH.CylinderGeometry(r * .8, r, 80, 18, 1, true); g.translate(0, 40, 0); g.rotateX(Math.PI / 2); const m = new TH.Mesh(g, glowMat(c, o)); m.userData.dyn = 1; lens.add(m); bm.push([m, o]); }
    const halos = []; for (let k = 0; k < 5; k++) { const h = new TH.Mesh(new TH.TorusGeometry(3, .12, 6, 40), glowMat(0xe8d0ff, .8)); h.userData.dyn = 1; lens.add(h); halos.push(h); }
    /* ---- the chest core and the forelimbs: gold pauldrons, armoured arms, gold vambraces, four-taloned claws ---- */
    const core = new TH.Group(); core.position.set(0, 4.4, 3.45); body.add(core);
    { const c = new TH.Mesh(new TH.SphereGeometry(.85, 18, 12), CORE); core.add(c); const rr = runeRing(1.9, 0xd8a0ff, .85); core.add(rr); core.userData.rr = rr; const ring = new TH.Mesh(new TH.TorusGeometry(1.25, .16, 6, 32), MG); core.add(ring);
      for (let k = 0; k < 8; k++) { const s = shard(.18, .9, MG); const a = k / 8 * TAU; s.position.set(Math.cos(a) * 1.35, Math.sin(a) * 1.35, 0); s.rotation.z = a - Math.PI / 2; core.add(s); } }
    { const bp = new TH.Mesh(new TH.LatheGeometry([[.2, -2.6], [2.2, -2.2], [2.9, -.6], [2.8, 1.2], [2.2, 2.6], [.6, 3.2]].map(([r, y]) => new TH.Vector2(r, y)), 16, -Math.PI * .45, Math.PI * .9), MS); bp.position.set(0, 4.2, 1.0); bp.scale.set(1.05, 1, .82); body.add(bp);
      for (const sx of [-1, 1]) { body.add(beam(V(sx * 2.5, 6.6, 2.0), V(sx * .4, 1.6, 3.4), .5, .25, .3, MG)); body.add(beam(V(sx * 2.7, 6.8, 1.6), V(sx * 1.2, 7.6, 3.0), .5, .3, .3, MG)); }
      for (let k = 0; k < 7; k++) { const y = 1.4 - k * 1.25, w = 2.6 - k * .22, pl = box(w, .85, .5, k % 2 ? MS : MG); pl.position.set(0, y, 2.55 - k * .5); pl.rotation.x = .35 + k * .05; body.add(pl); } }
    const coreS = sprite(7, "rgba(230,200,255,1)", "vae_core"); core.add(coreS);
    const arms = []; for (const sx of [-1, 1]) { const sh = new TH.Group(); sh.position.set(sx * 2.3, 5.2, 2.0); body.add(sh); const up = new TH.Group(); sh.add(up);
      up.add(strut(V(0, 0, 0), V(sx * 1.4, -2.6, 1.6), 1.0, .75, MA, 7)); const pd = new TH.Mesh(crescentGeo(1.9, .7, 1.1, .5), MG); pd.position.set(sx * .3, .5, -.1); pd.rotation.set(-.4, sx * .5, sx * -.9); up.add(pd);
      for (let k = 0; k < 3; k++) { const s = shard(.2, 1.4 - k * .25, MG); s.position.set(sx * (.4 + k * .3), .9, -.3 - k * .3); s.rotation.set(-.6, 0, sx * -.5); up.add(s); }
      const el = new TH.Group(); el.position.set(sx * 1.4, -2.6, 1.6); up.add(el); el.add(strut(V(0, 0, 0), V(-sx * .4, -1.4, 3.0), .75, .55, MA, 7)); el.add(beam(V(-sx * .1, -.3, .5), V(-sx * .35, -1.2, 2.7), .9, .6, .55, MG));
      const hand = new TH.Group(); hand.position.set(-sx * .4, -1.4, 3.0); el.add(hand); hand.add(new TH.Mesh(new TH.SphereGeometry(.6, 10, 8), MA));
      for (let k = 0; k < 4; k++) { const tl = horn(1.9, .9, .2, k === 3 ? MGd : MG, 12); tl.rotation.set(0, -Math.PI / 2 + (k - 1.5) * .32 * sx, -.6 - (k === 3 ? .8 : 0)); if (k === 3) tl.rotation.y += sx * 1.2; hand.add(tl); }
      const trail = sprite(4, "rgba(200,150,255,1)", "vae_claw"); trail.material.opacity = 0; hand.add(trail); arms.push({ sx, sh, up, el, hand, trail }); }
    /* ---- the wings: gold bones and spars, dark spikes at the joints, membranes of luminous violet energy ---- */
    const memT = paint("vae_mem", 256, (x, N2) => { const g = x.createLinearGradient(0, 0, N2, N2); g.addColorStop(0, "#2a0b4a"); g.addColorStop(.6, "#4a1a86"); g.addColorStop(1, "#8e5cff"); x.fillStyle = g; x.fillRect(0, 0, N2, N2);
      x.strokeStyle = "#e0c0ff"; for (let i = 0; i < 70; i++) { let px = rnd() * N2, py = rnd() * N2, a = rnd() * TAU; x.globalAlpha = .25 + rnd() * .55; x.lineWidth = .6 + rnd() * 1.8; x.beginPath(); x.moveTo(px, py); for (let k = 0; k < 24; k++) { a += (rnd() - .5) * .7; px += Math.cos(a) * 7; py += Math.sin(a) * 7; x.lineTo(px, py); } x.stroke(); }
      x.globalAlpha = 1; for (let i = 0; i < 160; i++) { x.fillStyle = `rgba(255,${200 + rnd() * 55 | 0},255,${.3 + rnd() * .6})`; x.fillRect(rnd() * N2, rnd() * N2, 1.2, 1.2); } });
    const memM = new TH.MeshBasicMaterial({ map: memT, color: 0xffffff, transparent: true, opacity: .45, side: TH.DoubleSide, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false });
    const wings = []; for (const sx of [-1, 1]) { const root = new TH.Group(); root.position.set(sx * 1.8, 6.6, -.4); body.add(root); const w = new TH.Group(); root.add(w);
      const J = [V(0, 0, 0), V(sx * 6, 6.5, -2.4), V(sx * 11.5, 11.5, -4.4)], tips = [V(sx * 19, 20, -8), V(sx * 24, 13, -9), V(sx * 24, 5, -8.5), V(sx * 20, -1, -7), V(sx * 12, -4.5, -4.5)];
      w.add(strut(J[0], J[1], .55, .42, MG, 6)); w.add(strut(J[1], J[2], .42, .32, MG, 6)); for (const tp of tips) w.add(strut(J[2], tp, .26, .06, MG, 5));
      for (const j of [J[1], J[2]]) { const s = shard(.35, 2.2, MS); s.position.copy(j); s.rotation.set(-.5, 0, sx * -.6); w.add(s); const k = new TH.Mesh(new TH.SphereGeometry(.5, 8, 6), MG); k.position.copy(j); w.add(k); }
      for (let k = 0; k < 6; k++) { const f = k / 5, s = shard(.12, .9, MG); s.position.lerpVectors(J[0], J[1], f); s.position.y += .45; s.rotation.z = sx * -.3; w.add(s); }
      // membrane: a fan from the wrist between consecutive tips, and a panel from the root along the arm to the last tip and back to the flank
      const pts = [J[2], ...tips], pos = [], uv = [], uvOf = p => [.5 + p.x / 46 * sx, .5 + p.y / 30];
      for (let k = 0; k < tips.length - 1; k++) { const a = J[2], b = tips[k], c = tips[k + 1], m1 = b.clone().lerp(c, .5).lerp(a, .18); for (const tri of [[a, b, m1], [a, m1, c]]) for (const p of tri) { pos.push(p.x, p.y, p.z); uv.push(...uvOf(p)); } }
      { const fl = V(sx * .4, -5.5, .3); for (const tri of [[J[0], J[1], tips[4]], [J[1], J[2], tips[4]], [J[0], tips[4], fl]]) for (const p of tri) { pos.push(p.x, p.y, p.z); uv.push(...uvOf(p)); } }
      const mg = new TH.BufferGeometry(); mg.setAttribute("position", new TH.Float32BufferAttribute(pos, 3)); mg.setAttribute("uv", new TH.Float32BufferAttribute(uv, 2)); mg.computeVertexNormals(); const mem = new TH.Mesh(mg, memM); mem.userData.dyn = 1; w.add(mem);
      wings.push({ sx, root, w, tips: tips.map(p => p.clone()), J }); }
    /* ---- the celestial wheel ---- */
    const wheel = new TH.Group(); wheel.position.set(0, 10.5, -7.5); wheel.rotation.y = .18; body.add(wheel); const WR = 14.5;
    const runeShader = (R, col, op, w0 = .64) => { const m = new TH.ShaderMaterial({ uniforms: { map: { value: runeTex() }, uC: { value: new TH.Color(col) }, uO: { value: op }, uSw: { value: 0 }, uHot: { value: 0 } }, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, side: TH.DoubleSide,
        vertexShader: "varying vec2 vU; varying vec2 vP; void main() { vU = uv; vP = position.xy; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }",
        fragmentShader: "uniform sampler2D map; uniform vec3 uC; uniform float uO, uSw, uHot; varying vec2 vU; varying vec2 vP; void main() { float a = fract(atan(vP.x, vP.y) / 6.2831853 + 1.), lit = smoothstep(uSw, uSw - .04, a) * step(.001, uSw); vec4 t = texture2D(map, vU); float k = uO * (.35 + .65 * lit) * (1. + uHot * 1.6); gl_FragColor = vec4(mix(uC, vec3(1.), lit * .35 + uHot * .3) * t.a * k, t.a * k); }" });
      const g = new TH.RingGeometry(R * w0, R * 1.02, 128, 1); const me = new TH.Mesh(g, m); me.userData.dyn = 1; return me; };
    const ringsW = []; const mkRing = (R, wd, th, mat, rc, rop, segs) => { const r = new TH.Group(); wheel.add(r); const b = band(R, wd, th, mat, 0, TAU, LO ? 64 : 120, segs); b.rotation.x = Math.PI / 2; r.add(b);
      const rr = runeShader(R * 1.0, rc, rop); rr.position.z = th * .5 + .05; rr.scale.setScalar(1); r.add(rr); const rr2 = runeShader(R, rc, rop * .6); rr2.position.z = -th * .5 - .05; r.add(rr2);
      const ch = new TH.Mesh(new TH.TorusGeometry(R - wd * .55, .08, 4, LO ? 64 : 110), glowMat(0xb070ff, .85)); ch.userData.dyn = 1; r.add(ch); const o = { r, b, rr: [rr, rr2], ch, R, ang: 0 }; ringsW.push(o); return o; };
    const R0 = mkRing(WR, 1.6, 1.1, MG, GOLD, .75, 28), R1 = mkRing(WR * .76, 1.1, .8, MGd, 0xc890ff, .85, 22), R2 = mkRing(WR * .54, .9, .7, MG, GOLD, .8, 16), R3 = mkRing(WR * .3, .7, .9, MGd, 0xe0b0ff, .9, 10);
    R1.r.rotation.x = .0; R2.r.rotation.y = .0;
    // the outer ring carries a toothed gold crown and six stabilizer nodes (gold cages round violet cores)
    { const teeth = new TH.Group(); R0.r.add(teeth); for (let k = 0; k < 36; k++) { const a = k / 36 * TAU, s = shard(.32, k % 3 ? .9 : 1.7, MG); s.position.set(Math.sin(a) * (WR + .9), Math.cos(a) * (WR + .9), 0); s.rotation.z = -a; teeth.add(s); } teeth.userData.flat = 1; }
    const frags = []; for (let k = 0; k < 7; k++) { const a = k / 7 * TAU + .2, g = box(1.4, .9, 1.0, MG); g.position.set(Math.sin(a) * WR, Math.cos(a) * WR, 0); g.userData.o = g.position.clone(); g.userData.dyn = 1; g.visible = false; R0.r.add(g); frags.push(g); }
    const stabs = []; for (let k = 0; k < 6; k++) { const a = k / 6 * TAU + TAU / 12, n = new TH.Group(); n.position.set(Math.sin(a) * (WR + .3), Math.cos(a) * (WR + .3), 0); R0.r.add(n);
      const cg = new TH.Group(); n.add(cg); for (const [rx, ry] of [[0, 0], [Math.PI / 2, 0], [0, Math.PI / 2]]) { const t = new TH.Mesh(new TH.TorusGeometry(1.25, .11, 5, 26), MG); t.rotation.set(rx, ry, 0); cg.add(t); }
      const c = new TH.Mesh(new TH.SphereGeometry(.75, 16, 12), CORE); c.userData.dyn = 1; n.add(c); const s = sprite(4.2, "rgba(210,160,255,1)", "vae_stab"); n.add(s); stabs.push({ n, cg, c, s, a }); }
    // spokes between the inner and outer rings, on their own slow ring
    const spk = new TH.Group(); wheel.add(spk); for (let k = 0; k < 8; k++) { const a = k / 8 * TAU, b = beam(V(Math.sin(a) * WR * .33, Math.cos(a) * WR * .33, 0), V(Math.sin(a) * WR * .95, Math.cos(a) * WR * .95, 0), .5, .26, .3, MGd); spk.add(b); const gl = new TH.Mesh(new TH.CylinderGeometry(.06, .06, WR * .6, 4, 1, true), glowMat(0xc890ff, .7)); gl.position.set(Math.sin(a) * WR * .64, Math.cos(a) * WR * .64, .2); gl.rotation.z = -a; gl.userData.dyn = 1; spk.add(gl); }
    // the aperture: a swirling disc of light in the hub, its rim, and the focus point
    const ap = new TH.Mesh(new TH.CircleGeometry(WR * .26, 48), new TH.MeshBasicMaterial({ map: swirlTex(), transparent: true, opacity: .55, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false })); ap.userData.dyn = 1; wheel.add(ap);
    const apS = sprite(9, "rgba(240,220,255,1)", "vae_ap"); wheel.add(apS); const field = new TH.Mesh(new TH.CircleGeometry(WR * 1.25, 64), new TH.MeshBasicMaterial({ map: swirlTex(), transparent: true, opacity: 0, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false })); field.position.z = -1.2; field.userData.dyn = 1; wheel.add(field);
    // floating glyph shards orbiting the wheel, and the particles it drinks in while charging
    const NG = LO ? 24 : 40, glyphs = inst(new TH.PlaneGeometry(1.1, 1.1), new TH.MeshBasicMaterial({ map: runeTex(), color: 0xffd890, transparent: true, opacity: .8, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false }), NG); wheel.add(glyphs);
    const gD = []; for (let k = 0; k < NG; k++) gD.push({ a: rnd() * TAU, r: WR * (1.12 + rnd() * .35), z: (rnd() - .5) * 3, w: (rnd() < .5 ? -1 : 1) * (.0001 + rnd() * .0002), s: .5 + rnd() * .8 });
    const NP = LO ? 70 : 120, motes = puffs(NP, 0xd8b0ff); wheel.add(motes); const mD = []; for (let k = 0; k < NP; k++) mD.push({ a: rnd() * TAU, r0: WR * (1.4 + rnd() * 1.6), ph: rnd(), w: .00006 + rnd() * .00008 });
    const tetherA = stabs.map(s => s.n), backPts = [3, 5, 7].map(k => k); const tmpV = V(0, 0, 0), tmpV2 = V(0, 0, 0);
    const bt = bolts(body, 10, () => { const s = stabs[(rnd() * 6) | 0], a = s.n.getWorldPosition(tmpV).clone(), b = P[NN + backPts[(rnd() * 3) | 0]].clone().add(V(0, 1.6, -.4)); body.worldToLocal(a); return [a, b]; }, 0xc890ff);
    const btW = bolts(wheel, 8, () => { const a = (rnd() * 4) | 0, ra = ringsW[a].R, rb = ringsW[Math.min(3, a + 1)].R, an = rnd() * TAU; return [V(Math.sin(an) * ra, Math.cos(an) * ra, .4), V(Math.sin(an + .3) * rb, Math.cos(an + .3) * rb, .4)]; }, 0xe0c0ff);
    // waves: a wing shockwave, the seal circles, judgment circles, the beam's shockwave rings
    const wingWave = wave(body, 12, false, 0xc890ff), sealC = runeShader(9, GOLD, .9, .5); sealC.rotation.x = -Math.PI / 2; sealC.position.set(0, -7, 16); sealC.visible = false; body.add(sealC);
    const judges = []; for (let k = 0; k < 4; k++) { const j = runeShader(2.2, GOLD, .95, .45); j.visible = false; wheel.add(j); const p = sprite(2.4, "rgba(255,225,160,1)", "vae_jp"); p.visible = false; body.add(p); judges.push({ j, p }); }
    const shocks = []; for (let k = 0; k < 3; k++) { const m = new TH.Mesh(new TH.TorusGeometry(3, .25, 6, 48), glowMat(0xe8d0ff, 0)); m.userData.dyn = 1; m.visible = false; lens.add(m); shocks.push(m); }
    const mv = moves({ claw: 1500, wing: 2400, judge: 3200, seal: 3600, rebirth: 3400, annihilate: 18000, hit: 520 }), hit = hitKit(body, shk), drv = {};
    const S = scr(), c1 = new TH.Color(), Q = new TH.Quaternion(), tmpO = new TH.Object3D();
    const f = (n, t) => drv[n] != null ? drv[n] : mv.f(n, t);
    const out = { grp, r: 20, h: 16, mouth, lens, wheel, stab: [1, 1, 1, 1, 1, 1], crack: 0, ph: "idle", dark: 0, act: n => mv.play(n), drive: (n, v) => { if (v == null || v < 0) delete drv[n]; else drv[n] = v; }, moves: ["claw", "wing", "judge", "seal", "rebirth", "annihilate"] };
    const tick = t => { const fc = f("claw", t), fw = f("wing", t), fj = f("judge", t), fs = f("seal", t), fr = f("rebirth", t), fa = f("annihilate", t), fx = f("hit", t);
      /* Divine Annihilation, stage by stage: warning .00-.12, runes .12-.35, accumulation .35-.55, alignment .55-.66, beam .66-.86, aftermath .86-1 */
      const A = fa < 0 ? -1 : fa, warn = bell(A, 0, .06, .9, .97), runes = A < 0 ? 0 : ss(.12, .35, A), acc = bell(A, .35, .55, .7, .74), align = bell(A, .55, .64, .86, .92), fire = bell(A, .66, .685, .84, .88), after = bell(A, .86, .9, .97, 1);
      out.ph = A < 0 ? "idle" : A < .12 ? "warning" : A < .35 ? "runes" : A < .55 ? "accumulate" : A < .66 ? "align" : A < .86 ? "beam" : "aftermath"; out.dark = align * (1 - fire * .5) * .6;
      const spin = 1 + warn * 2 + runes * 3 + acc * 4 + align * 2 - after * 2.5, wob = out.stab.filter(x => !x).length;
      st.spread = Math.max(warn, bell(fw, 0, .2, .8, 1)); st.beat = fw < 0 ? 0 : Math.sin(fw * Math.PI * 3) * (1 - fw); st.lift = Math.max(acc, align) * .9 + fire * .4 - after * .2; st.recoil = fire * (.8 + Math.sin(t * .03) * .1); st.sway = fire * Math.sin((A - .66) / .2 * Math.PI * 1.2 - .6) * .35;
      st.coil = bell(fr, 0, .2, .8, 1) * .6 + warn * .2; st.curl = Math.sin(t * .0003) * .4; st.gape = Math.max(acc * .6, align * .85, fire, bell(fc, .2, .4, .7, .9) * .4, bell(fw, .3, .45, .6, .8) * .5);
      spine(t);
      for (let i = 0; i < N; i++) { const a = P[i], b = P[i + 1] || P[i]; S.v.subVectors(i < N ? P[i + 1] : P[i], i ? P[i - 1] : P[i]).normalize(); S.q.setFromUnitVectors(S.Z, S.v); const s = SC[i];
        S.s.set(s, s * .9, s * 1.45); S.m.compose(a, S.q, S.s); segs.setMatrixAt(i, S.m); S.p.copy(a).addScaledVector(S.v, s * .62); S.s.set(s * 1.01, s * .91, s).multiplyScalar(i % 2 ? .001 : 1); S.m.compose(S.p, S.q, S.s); cols.setMatrixAt(i, S.m); S.s.set(s * 1.0, s * .9, s);
        S.p.copy(a).addScaledVector(S.v, -s * .55); S.m.compose(S.p, S.q, S.s); seams.setMatrixAt(i, S.m);
        S.w.set(0, 1, 0).addScaledVector(S.v, -S.v.y).normalize(); Q.setFromUnitVectors(S.Y, S.w); if (i >= NN && i < NN + NT) Q.setFromUnitVectors(S.Y, tmpV.set(0, .2, -1).normalize()); S.s.setScalar(s * .75); S.p.copy(a).addScaledVector(S.w, s * .25); S.m.compose(S.p, Q, S.s); fins.setMatrixAt(i, S.m);
        let hot = 0; for (let k = 0; k < 2; k++) { const c = ((t * .00007 + k / 2) % 1) * N; hot = Math.max(hot, 1 - Math.min(1, Math.abs(i - c) / 2)); }
        const g = .55 + .2 * Math.sin(t * .003 - i * .45) + acc * .6 + fire * .8 + hot * .3 + bell(fr, 0, .3, .7, 1) * .6; c1.setRGB(g * .62, g * .32, g * 1.0); seams.setColorAt(i, c1); }
      for (const m of [segs, cols, seams, fins]) m.instanceMatrix.needsUpdate = true; seams.instanceColor.needsUpdate = true;
      head.position.copy(P[0]); S.v.subVectors(P[0], P[1]).normalize(); head.quaternion.setFromUnitVectors(S.Z, S.v); head.rotateX(-.5 - st.lift * .5 + st.recoil * .18); head.rotateY(st.sway * .5); head.rotateZ(Math.sin(t * .0007) * .06);
      jaw.rotation.x = .08 + st.gape * .62 + Math.sin(t * .002) * .02;
      const eyeK = .55 + warn * .5 + align * 1.2 + fire * .6 + .1 * Math.sin(t * .004); eyes.forEach(e => { e.material.opacity = Math.min(1, eyeK); e.scale.setScalar(1.6 * (1 + align * 1.2 + fire * .6)); });
      const og = Math.max(acc * .55, align, fire * .8, after * .3 * (1 - after)); orb.material.opacity = og * .9; orb.scale.setScalar(.2 + og * 1.4 + fire * Math.sin(t * .05) * .15); orbS.material.opacity = og; orbS.scale.setScalar(3 + og * 7 + fire * 3);
      lens.visible = fire > .01; if (lens.visible) { bm.forEach(([m, o], k) => { m.material.opacity = o * fire * (.85 + rnd() * .15); m.scale.set(1 + Math.sin(t * .04 + k) * .06, 1 + Math.sin(t * .05 + k) * .06, Math.min(1, (A - .66) / .02)); });
        halos.forEach((h, k) => { const z = ((t * .05 + k * 16) % 80); h.position.z = z; h.scale.setScalar(1 + z * .03); h.material.opacity = .8 * fire * (1 - z / 80); });
        shocks.forEach((m, k) => { const q = ((t * .0016 + k / 3) % 1); m.visible = true; m.position.z = 2 + q * 10; m.scale.setScalar(1 + q * 5); m.material.opacity = (1 - q) * fire * .7; }); }
      core.userData.rr.rotation.z = t * .0008; coreS.material.opacity = .55 + .25 * Math.sin(t * .003) + acc * .4 + bell(fr, 0, .3, .7, 1) * .5; coreS.scale.setScalar(7 * (1 + acc * .4 + fire * .3));
      // arms: idle breathing; the claw rakes forward and down, alternating
      const cl = fc < 0 ? 0 : fc; arms.forEach((a, k) => { const sw = k === (Math.floor(t / 4000) % 2) ? cl : 0, rake = Math.sin(ss(.15, .55, sw) * Math.PI) * 1.0 + bell(sw, .1, .3, .5, .8) * .4;
        a.up.rotation.set(-.15 + Math.sin(t * .0011 + k) * .06 - rake * 1.1 + align * .3, a.sx * (.1 - rake * .25), a.sx * (.15 + st.spread * .1)); a.el.rotation.set(.2 - rake * .6 + Math.sin(t * .0013 + k) * .05, 0, 0); a.hand.rotation.set(-.2 + rake * .9, 0, 0);
        a.trail.material.opacity = bell(sw, .2, .35, .55, .75); a.trail.scale.setScalar(4 + rake * 6); });
      // wings: folded half open at rest, flung wide for the warning and the wingstorm, beating in the storm
      wings.forEach(W => { const sp = .35 + st.spread * .65; W.root.rotation.set(-.2 + st.beat * .25 + Math.sin(t * .0009) * .04, W.sx * (.85 - sp * .75), W.sx * (-.15 + st.beat * .5 - sp * .1)); W.w.scale.set(.75 + sp * .25, .85 + sp * .15, 1); });
      memM.opacity = .36 + st.spread * .16 + acc * .12 + fire * .15; wingWave(fw < 0 ? -1 : ss(.35, 1, fw));
      // the wheel: majestic idle turn; it spins up through the charge, the rings counter-rotate, the runes ignite in sequence, then align
      const dt = Math.min(64, t - (out.lt || t)); out.lt = t; const crack = out.crack;
      ringsW.forEach((o, k) => { const dir = k % 2 ? -1 : 1, base = [.00009, .00014, .0002, .0003][k] * dir * (1 + wob * .15);
        o.ang += base * dt * spin; if (align > .01) { const snap = Math.round(o.ang / (TAU / 8)) * (TAU / 8); o.ang += (snap - o.ang) * Math.min(1, align * dt * .006); }
        o.r.rotation.z = o.ang + (crack > 0 && k === 0 ? Math.sin(t * .007) * crack * .05 : 0) + (wob ? Math.sin(t * .003 + k) * .01 * wob : 0);
        const sw = A < 0 ? (fj >= 0 ? bell(fj, 0, .2, .8, 1) : 0) : ss(.12 + k * .05, .3 + k * .05, A) * (1 - after); o.rr.forEach(r => { r.material.uniforms.uSw.value = sw > .001 ? Math.min(1.04, sw * 1.04) : 0; r.material.uniforms.uHot.value = (align + fire * .8) * .5; });
        o.ch.material.opacity = .45 + .2 * Math.sin(t * .003 + k) + acc * .4 + align * .5; });
      spk.rotation.z = -R0.ang * .5; ap.rotation.z = -t * (.0008 + acc * .006 + align * .01); ap.material.opacity = .45 + acc * .4 + align * .5; apS.material.opacity = .5 + acc * .5; apS.scale.setScalar(8 * (1 + acc * .5 + align * .8 + fire * .3));
      field.material.opacity = (acc * .25 + align * .45 + fire * .3) * (1 - after); field.rotation.z = t * .001; field.scale.setScalar(1 + align * .15);
      R0.r.scale.setScalar(1 + crack * .02 * Math.sin(t * .011)); R0.ch.material.opacity *= crack > 0 && rnd() < crack * .3 ? .2 : 1; frags.forEach((g, k) => { g.visible = crack > .05; if (g.visible) { const d = crack * (1.5 + k % 3) + Math.sin(t * .001 + k) * .3; g.position.copy(g.userData.o).multiplyScalar(1 + d * .06); g.rotation.set(t * .0004 * (k + 1), t * .0003, k); } });
      stabs.forEach((s, k) => { const on = out.stab[k]; s.cg.rotation.set(t * .0011 * (k % 2 ? -1 : 1), t * .0007, 0); s.c.material.color.setRGB(on ? 1 : .15, on ? .9 : .08, on ? 1 : .2); s.s.material.opacity = on ? .7 + acc * .3 + align * .4 + Math.sin(t * .004 + k) * .1 : (rnd() < .05 ? .6 : 0); s.s.scale.setScalar(4.2 * (1 + align * .6)); });
      for (let k = 0; k < NG; k++) { const g = gD[k]; g.a += g.w * dt * spin; const r = g.r * (1 - acc * .25 - align * .2); S.p.set(Math.sin(g.a) * r, Math.cos(g.a) * r, g.z + Math.sin(t * .001 + k) * .4); S.e.set(0, 0, -g.a + Math.sin(t * .002 + k)); S.q.setFromEuler(S.e); S.s.setScalar(g.s * (1 + runes * .3)); S.m.compose(S.p, S.q, S.s); glyphs.setMatrixAt(k, S.m); } glyphs.instanceMatrix.needsUpdate = true; glyphs.material.opacity = .45 + runes * .4 + align * .2;
      const draw = Math.max(warn * .4, acc, align * .6); for (let k = 0; k < NP; k++) { const m = mD[k], ph = (m.ph + t * m.w * (1 + draw * 6)) % 1, r = m.r0 * (1 - ph), a = m.a + ph * 4; motes.put(k, Math.sin(a) * r, Math.cos(a) * r, (1 - ph) * 3, .9 + (1 - ph) * .6, draw * (ph < .1 ? ph * 10 : 1) * (.5 + .5 * ph)); } motes.done();
      bt(t, .4 + acc * 4 + align * 6 + fire * 3 + bell(fr, 0, .2, .8, 1) * 3); btW(t, .3 + runes * 2 + align * 3 + crack * 3);
      // Celestial Judgment: rune circles bloom on the wheel and fire bolts forward; Golden Seal: a gold rune circle forms ahead
      judges.forEach((J, k) => { const on = fj >= 0, a = k / 4 * TAU + .4, open = bell(fj, k * .08, .2 + k * .08, .8, .95), shot = fj < 0 ? -1 : (fj - .35 - k * .1) / .3;
        J.j.visible = on && open > .01; if (J.j.visible) { J.j.position.set(Math.sin(a) * WR * .62, Math.cos(a) * WR * .62, 1.5); J.j.scale.setScalar(.2 + open); J.j.rotation.z = t * .004; J.j.material.uniforms.uSw.value = 1.04; J.j.material.uniforms.uO.value = .95 * open; }
        J.p.visible = shot > 0 && shot < 1; if (J.p.visible) { J.j.getWorldPosition(tmpV); body.worldToLocal(tmpV); J.p.position.copy(tmpV).lerp(tmpV2.set(tmpV.x * .2, -2, 40), shot); J.p.material.opacity = 1 - shot * .3; } });
      sealC.visible = fs >= 0; if (sealC.visible) { const k = bell(fs, 0, .25, .8, 1); sealC.material.uniforms.uSw.value = Math.min(1.04, ss(0, .45, fs) * 1.04); sealC.material.uniforms.uO.value = k; sealC.rotation.z = t * .0006; sealC.scale.setScalar(1 + ss(0, .3, fs) * .4); }
      hit(bell(fx, 0, .05, .4, 1), t); };
    out.tick = tick; tick(0); bake(body); return out; }
