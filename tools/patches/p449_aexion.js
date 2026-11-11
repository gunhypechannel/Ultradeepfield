  /* ---------- Aexion, the Warform Sovereign (owner's art, assets/bosses/aexion/ref): one rigged machine with two poses. As a ship it is a
     long silver-and-gunmetal dreadnought: a split prow, flank cannons, deck turrets, a rune halo standing on its deck, swept rear wings and
     great engines at its stern. Every part of it is a part of the mech: the stern is its legs (the engines are in its heels, firing down
     once it stands), the flank cannons its forearms, the prow its shoulder armour, the deck turrets its shoulder cannons, the halo rises
     behind its head, the wings become the V behind its shoulders, and the hull plates close round the reactor in its chest.
     transform (0..1) moves every joint from the ship pose to the mech pose in stages (activation, hull separation, limb deployment, core
     alignment, weapons, reveal): nothing is swapped or hidden. Moves: broadside, missiles, rail, aegis, blade, lance, overdrive, hit.
     form is 0 (ship) .. 1 (Warform); drive(name, f) pins a move to a progress, as on Vaelthar. ---------- */
  function aexion() { const grp = new TH.Group(), shk = new TH.Group(), body = new TH.Group(); grp.add(shk); shk.add(body);
    const LO = LOD === 1, RC = [.3, .62, 1], BLUE = 0x58b8ff;
    const MA = hullMat("aex", { rows: 3, pal: ["#7c8592", "#6c7482", "#8e97a4", "#5e6672", "#868e9a"], bronze: 0, slits: .42, sc: "#d8f4ff", sg: "#3aa8ff", metal: .92, rough: .3, rc: RC, ei: 3.4, rep: [.14, .14], relief: 2.2 }); MA.envMapIntensity = .85;
    const MD = hullMat("aexd", { rows: 4, pal: ["#141a25", "#1a2130", "#10151e", "#222a38"], bronze: 0, slits: .55, sc: "#cfefff", sg: "#2a90ff", metal: .9, rough: .34, rc: RC, ei: 3.6, rep: [.16, .16] });
    const MR = hullMat("aexr", { rows: 4, cols: 6, pal: ["#20242c"], bronze: 0, slits: 1, sc: "#ffd0c0", sg: "#ff4a3a", metal: .9, rough: .3, rc: [1, .4, .3], ei: 3.2, rep: [.4, .4] });
    const CORE = new TH.MeshBasicMaterial({ color: 0xe8f6ff, toneMapped: false }), GL = glowMat(BLUE, .85), GW = glowMat(0xcfeeff, .95);
    // angular armour: a chamfered slab, and a pointed blade
    const slab = (w, h, d, mat, ch = .35, tp = 1) => { const s = new TH.Shape(), x = w / 2, y = h / 2, c = Math.min(ch, x * .45, y * .45), xb = x * tp; s.moveTo(-xb + c, -y); s.lineTo(xb - c, -y); s.lineTo(xb, -y + c); s.lineTo(x, y - c); s.lineTo(x - c, y); s.lineTo(-x + c, y); s.lineTo(-x, y - c); s.lineTo(-xb, -y + c); s.closePath();
      const g = new TH.ExtrudeGeometry(s, { depth: d, bevelEnabled: true, bevelThickness: Math.min(.14, d * .2), bevelSize: Math.min(.14, c * .5), bevelSegments: 1 }); g.translate(0, 0, -d / 2); return new TH.Mesh(g, mat); };
    const spike = (w, h, d, mat) => { const s = new TH.Shape(); s.moveTo(-w / 2, 0); s.lineTo(w / 2, 0); s.lineTo(w * .22, h * .72); s.lineTo(0, h); s.lineTo(-w * .22, h * .72); s.closePath(); const g = new TH.ExtrudeGeometry(s, { depth: d, bevelEnabled: true, bevelThickness: Math.min(.12, d * .25), bevelSize: Math.min(.12, w * .08), bevelSegments: 1 }); g.translate(0, 0, -d / 2); return new TH.Mesh(g, mat); };
    const glowBar = (w, h, d, mat = GL) => { const m = new TH.Mesh(new TH.BoxGeometry(w, h, d), mat); return m; };
    const put = (par, m, p, r) => { m.position.set(...p); if (r) m.rotation.set(...r); par.add(m); return m; };
    // the rig: each joint has a pivot, a ship pose, a mech pose and the stage window in which it moves
    const joints = [], E = (x, y, z) => new TH.Quaternion().setFromEuler(new TH.Euler(x, y, z));
    const J = (par, mechP, shipP, mechR, shipR, a, b, ease = 1) => { const g = new TH.Group(); par.add(g); const j = { g, mp: V(...mechP), sp: V(...(shipP || mechP)), mq: E(...(mechR || [0, 0, 0])), sq: E(...(shipR || mechR || [0, 0, 0])), a, b, ease }; joints.push(j); return g; };
    /* the pelvis is the root: lying along the keel as a ship (torso forward, back up), upright as the mech */
    const root = J(body, [0, 0, 0], [0, 1.5, 6], [0, 0, 0], [Math.PI / 2, 0, 0], .16, .5);
    put(root, slab(5.2, 2.6, 3.4, MD), [0, 0, 0]); put(root, slab(3.4, 1.4, 3.8, MA), [0, -1.1, .2]); for (const sx of [-1, 1]) { put(root, slab(2.3, 3.6, .55, MA), [sx * 2.5, -1.8, 1.4], [.22, 0, sx * .12]); put(root, glowBar(.12, 2.6, .1), [sx * 2.5, -1.8, 1.75], [.22, 0, sx * .12]); }
    const chest = J(root, [0, 1.6, 0], [0, 1.6, 0], [-.04, 0, 0], [0, 0, 0], .3, .6);
    put(chest, slab(8.0, 6.4, 4.4, MD, .6, .62), [0, 3.5, 0]); put(chest, slab(4.0, 2.6, 3.2, MD, .35, .8), [0, .5, 0]); put(chest, slab(6.4, 1.3, 3.2, MA), [0, 6.7, -.2]); put(chest, slab(6.8, 5.2, 1.2, MA), [0, 4.0, -2.4]);
    for (const sx of [-1, 1]) { put(chest, slab(3.8, 5.4, 1.1, MA, .5, .55), [sx * 2.3, 4.0, 2.05], [0, sx * -.28, 0]); put(chest, glowBar(.14, 4.4, .12), [sx * 1.15, 3.9, 2.45]); put(chest, slab(2.0, 1.8, 1.0, MA), [sx * 1.2, 1.2, 1.8], [.2, 0, 0]); put(chest, spike(1.2, 2.4, .5, MA), [sx * 3.4, 6.9, .4], [0, 0, sx * -.5]); }
    put(chest, spike(1.6, 2.2, .6, MA), [0, 6.2, 2.1], [Math.PI, 0, 0]);
    // the reactor, and the two hull plates that slide over it as the mech forms (open on the ship's belly)
    const core = put(chest, new TH.Group(), [0, 4.3, 2.25]); { core.add(new TH.Mesh(new TH.SphereGeometry(.9, 18, 12), CORE)); const r = new TH.Mesh(new TH.TorusGeometry(1.25, .14, 6, 32), MA); core.add(r); const g = new TH.Mesh(new TH.TorusGeometry(1.55, .06, 4, 40), GL); g.userData.dyn = 1; core.add(g); core.userData.g = g; }
    const coreS = sprite(6, "rgba(190,230,255,1)", "aex_core"); coreS.position.copy(core.position).add(V(0, 0, .6)); chest.add(coreS);
    const plates = [-1, 1].map(sx => { const p = J(chest, [sx * 1.15, 4.3, 2.35], [sx * 2.9, 4.3, 2.0], [0, 0, 0], [0, sx * .55, 0], .58, .7); put(p, slab(2.1, 3.2, .55, MA), [0, 0, 0]); put(p, glowBar(.1, 2.6, .1), [-sx * .95, 0, .3]); return p; });
    /* the head rises out of the chest; the prow halves cover it as a ship and swing out over the shoulders */
    const head = J(chest, [0, 7.2, .2], [0, 4.7, -.4], [0, 0, 0], [0, 0, 0], .5, .66);
    put(head, slab(2.0, 2.3, 2.3, MA), [0, 1.1, 0]); put(head, slab(1.4, .5, .5, GW), [0, 1.25, 1.2]); put(head, spike(.9, 3.4, .45, MA), [0, 2.0, -.2]);
    for (const sx of [-1, 1]) { const h = put(head, spike(.8, 2.8, .4, MA), [sx * .9, 1.8, -.3], [0, 0, sx * -.7]); const c = put(head, new TH.Mesh(crescentGeo(1.6, .35, 1.0, .3), MA), [sx * .2, 2.6, -.4], [0, 0, 0]); c.scale.setScalar(.8); }
    const eyes = [-1, 1].map(sx => { const e = sprite(1.4, "rgba(200,235,255,1)", "aex_eye"); e.position.set(sx * .42, 1.3, 1.25); head.add(e); return e; });
    const prow = [-1, 1].map(sx => { const p = J(chest, [sx * 2.4, 6.8, .8], [sx * 1.0, 6.9, .9], [-.35, 0, sx * -2.25], [0, 0, sx * .1], .12, .32);
      put(p, spike(3.2, 11, 1.3, MA), [-sx * .35, 0, 0], [0, 0, 0]); put(p, glowBar(.12, 7, .1), [-sx * .35, 3.4, .72]); put(p, slab(2.6, 2, 1.0, MD), [0, .6, -.2]); return p; });
    /* arms: raised along the hull as the ship's flank cannons, lowered to the mech's sides */
    const arms = [-1, 1].map(sx => { const sh = J(chest, [sx * 5.3, 5.6, 0], [sx * 4.2, 5.6, .2], [0, 0, sx * .2], [0, 0, sx * (Math.PI - .08)], .3, .56);
      put(sh, slab(4.2, 3.0, 4.4, MA), [sx * 1.0, .7, 0]); put(sh, spike(1.4, 3.2, .6, MA), [sx * 1.9, 1.8, 0], [0, 0, sx * -.9]); put(sh, slab(2.2, 5.4, 2.4, MD, .35, .8), [0, -3.0, 0]); put(sh, slab(2.8, 3.0, 2.9, MA, .5, .8), [0, -2.0, .1]);
      const el = J(sh, [0, -6, 0], [0, -6, 0], [-.4, 0, 0], [0, 0, 0], .45, .6);
      put(el, slab(3.3, 6.2, 3.2, MA, .6, .72), [0, -3.0, .2]); put(el, slab(2.0, 4.2, 2.2, MD), [0, -3.2, -.5]); put(el, glowBar(.12, 4.4, .12), [sx * 1.5, -3.0, .4]); put(el, glowBar(.1, 3.6, .1), [-sx * 1.2, -3.2, 1.75]); put(el, glowBar(1.4, .1, .1), [0, -1.4, 1.85]);
      const bar = []; for (const dx of [-.55, .55]) { const b = new TH.Mesh(new TH.CylinderGeometry(.3, .38, 5.4, 10), MD); b.position.set(sx * 1.55 + dx * .5, -3.8, 1.5 + (dx > 0 ? 0 : .02)); el.add(b); const m = new TH.Mesh(new TH.TorusGeometry(.34, .07, 5, 14), GL); m.rotation.x = Math.PI / 2; m.position.set(b.position.x, -6.5, b.position.z); m.userData.dyn = 1; el.add(m); const f = sprite(2.4, "rgba(170,220,255,1)", "aex_mz"); f.position.set(b.position.x, -7.0, b.position.z); f.material.opacity = 0; el.add(f); bar.push(f); }
      const hand = J(el, [0, -6.3, .2], [0, -6.3, .2], [0, 0, 0], [0, 0, 0], .55, .62); put(hand, slab(1.9, 1.9, 1.9, MD), [0, -.9, 0]); for (let k = 0; k < 4; k++) put(hand, slab(.38, 1.3, .5, MA), [(k - 1.5) * .45, -2.0, .4], [.5, 0, 0]);
      return { sx, sh, el, hand, bar }; });
    // the Judgment Blade (right hand) and the Holographic Aegis (left forearm)
    const RH = arms[1].hand, LF = arms[0].el; const sword = new TH.Group(); sword.position.set(0, -1.6, .2); sword.rotation.x = Math.PI / 2 + .25; RH.add(sword);
    put(sword, new TH.Mesh(new TH.CylinderGeometry(.24, .24, 2.6, 8), MD), [0, 0, 0]); put(sword, slab(2.6, .4, .6, MA), [0, 1.3, 0]);
    const blade = new TH.Group(); blade.position.y = 1.5; sword.add(blade); { const g1 = new TH.Mesh(new TH.BoxGeometry(.28, 1, 1.0), GW), g2 = new TH.Mesh(new TH.BoxGeometry(.9, 1.05, 2.0), glowMat(0x58b8ff, .45)), g3 = new TH.Mesh(new TH.BoxGeometry(1.8, 1.1, 3.4), glowMat(0x3a7aff, .16)); for (const g of [g1, g2, g3]) { g.geometry.translate(0, .5, 0); g.userData.dyn = 1; blade.add(g); } const tip = spike(1.0, 1.6, .3, GW); tip.position.y = 1; blade.add(tip); }
    blade.scale.set(1, .001, 1); const bladeS = sprite(4, "rgba(190,230,255,1)", "aex_bl"); sword.add(bladeS); bladeS.position.y = 1.5;
    const hexM = new TH.ShaderMaterial({ uniforms: { uC: { value: new TH.Color(0x6ac8ff) }, uO: { value: .0 }, uT: { value: 0 }, uHit: { value: new TH.Vector3(0, 0, -9) } }, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, side: TH.DoubleSide,
      vertexShader: "varying vec2 vP; void main() { vP = position.xy; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }",
      fragmentShader: "uniform vec3 uC; uniform float uO, uT; uniform vec3 uHit; varying vec2 vP; float hx(vec2 p) { p /= .9; vec2 q = vec2(p.x * 1.1547, p.y + p.x * .57735); vec2 i = floor(q), f = fract(q); float a = mod(i.x + i.y, 3.); vec2 c = a < 1. ? vec2(0.) : a < 2. ? vec2(1.) : vec2(step(f.y, f.x), step(f.x, f.y)); vec2 d = f - c; return length(vec2(d.x - d.y * .5, d.y * .866)); }\n void main() { float r = length(vP), e = smoothstep(6., 5.6, r), h = smoothstep(.36, .5, hx(vP)), d = length(vP - uHit.xy), w = uHit.z > 0. ? exp(-pow((d - uHit.z * 6.) / .8, 2.)) * (1. - uHit.z) : 0.; float rim = smoothstep(5.2, 5.9, r) * e;\n float k = uO * e * (.08 + h * .5 + rim * .9 + w * 1.6 + .06 * sin(uT * .004 + r * 2.)); gl_FragColor = vec4(uC * k + vec3(w * .6), k); }" });
    const shield = new TH.Mesh(new TH.CircleGeometry(6, 48), hexM); shield.userData.dyn = 1; shield.position.set(-2.4, -3.2, .3); shield.rotation.y = -Math.PI / 2 + .2; LF.add(shield);
    /* legs: the stern of the ship; the engines are in the heels */
    const legs = [-1, 1].map(sx => { const hip = J(root, [sx * 2.3, -1.3, 0], [sx * 2.0, -1.3, 0], [-.12, 0, sx * .07], [0, 0, sx * .02], .22, .5);
      put(hip, slab(3.3, 7.0, 3.2, MA, .6, .74), [0, -3.4, 0]); put(hip, slab(2.0, 5.4, 2.2, MD), [0, -3.5, -.6]); put(hip, glowBar(.12, 5, .12), [sx * 1.5, -3.4, .5]); put(hip, glowBar(.1, 4.4, .1), [0, -3.6, 1.68]);
      const kn = J(hip, [0, -7, 0], [0, -7, 0], [.3, 0, 0], [0, 0, 0], .35, .55); put(kn, spike(2.0, 3.0, 1.0, MA), [0, -.2, 1.6], [-.15, 0, 0]); put(kn, slab(3.5, 7.8, 3.6, MA, .7, .66), [0, -3.9, 0]); put(kn, slab(2.2, 5.6, 1.4, MD), [0, -4.2, -1.6]); for (const dy of [-2.4, -4.4]) put(kn, glowBar(1.6, .12, .12), [0, dy, -2.35]);
      const an = J(kn, [0, -7.9, 0], [0, -7.9, 0], [-.18, 0, 0], [-Math.PI / 2, 0, 0], .45, .62); put(an, slab(3.1, 1.4, 5.2, MD), [0, -.8, 1.3]); put(an, spike(2.6, 2.4, .9, MA), [0, -.9, 3.4], [Math.PI / 2, 0, 0]);
      const eng = put(an, new TH.Group(), [0, -1.2, -1.5]); put(eng, slab(2.8, 2.4, 2.8, MD), [0, .5, 0]); const fl = []; for (const dx of [-.7, .7]) { const n = new TH.Mesh(new TH.CylinderGeometry(.55, .8, 1.0, 12, 1, true), MA); n.position.set(dx, -.9, 0); eng.add(n); const g = new TH.Mesh(new TH.CircleGeometry(.5, 16), GW); g.rotation.x = Math.PI / 2; g.position.set(dx, -1.35, 0); g.userData.dyn = 1; eng.add(g); const f = sprite(3, "rgba(150,210,255,1)", "aex_fl"); f.position.set(dx, -2.4, 0); eng.add(f); fl.push(f); }
      return { sx, hip, kn, an, fl }; });
    /* the wings, the halo and the deck turrets, all on the back */
    const wings = [-1, 1].map(sx => { const w = J(chest, [sx * 2.6, 5.6, -2.6], [sx * 2.4, 5.0, -2.5], [.35, 0, sx * (Math.PI - .75)], [-.05, 0, sx * .22], .35, .6);
      [[0, 12, 1.4], [.32, 10, 1.1], [.62, 7.5, .9]].forEach(([a, L, wd], k) => { put(w, spike(wd, L, .45, MA), [sx * k * .5, 0, -k * .25], [0, 0, Math.PI + sx * a]); put(w, glowBar(.1, L * .6, .1), [sx * (k * .5 + Math.sin(a) * L * .3), -Math.cos(a) * L * .3, -k * .25 + .3], [0, 0, sx * a]); }); return w; });
    const halo = J(chest, [0, 7.4, -3.4], [0, 5.6, -3.2], [0, 0, 0], [-Math.PI / 2, 0, 0], .6, .76); { const b = band(5.2, .55, .5, MA, 0, TAU, 72, 24); b.rotation.x = Math.PI / 2; halo.add(b); const rr = runeRing(5.0, 0x7ac8ff, .9); halo.add(rr); halo.userData.rr = rr; for (let k = 0; k < 4; k++) { const a = k / 4 * TAU; const o = new TH.Mesh(new TH.SphereGeometry(.45, 10, 8), CORE); o.position.set(Math.sin(a) * 5.4, Math.cos(a) * 5.4, 0); halo.add(o); } const top = spike(1.2, 3, .5, MA); top.position.y = 5.2; halo.add(top); }
    const cannons = [-1, 1].map(sx => { const c = J(chest, [sx * 2.4, 7.0, -2.8], [sx * 2.0, 6.0, -2.9], [Math.PI / 2 - .1, 0, 0], [0, 0, 0], .7, .82); put(c, slab(2.2, 2.0, 2.2, MD), [0, .4, 0]); const mz = []; for (const dx of [-.45, .45]) { const b = new TH.Mesh(new TH.CylinderGeometry(.22, .26, 4.4, 8), MA); b.position.set(dx, 3.0, 0); c.add(b); const f = sprite(2.2, "rgba(170,220,255,1)", "aex_mz"); f.position.set(dx, 5.5, 0); f.material.opacity = 0; c.add(f); mz.push(f); } return { c, mz }; });
    const pods = [-1, 1].map(sx => { const p = put(chest, new TH.Group(), [sx * 3.9, 7.2, .5]); put(p, slab(2.4, 1.4, 2.8, MR), [0, 0, 0]); const lid = J(p, [0, .75, -1.4], [0, .75, -1.4], [-1.25, 0, 0], [0, 0, 0], .72, .84); put(lid, slab(2.5, .3, 2.9, MA), [0, 0, 1.45]); return { p, lid }; });
    // effects: missiles, the rail slug, the lance, the blade's arc, the reveal shockwave, the unlock flashes
    const NM = LO ? 16 : 28, mis = puffs(NM, 0xbfe4ff); body.add(mis); const mD = []; for (let k = 0; k < NM; k++) mD.push({ s: k % 2, a: rnd() * TAU, d: .3 + rnd() * .5, h: rnd() });
    const rail = new TH.Mesh(new TH.CylinderGeometry(.25, .25, 1, 8, 1, true), GW); rail.geometry.translate(0, .5, 0); rail.userData.dyn = 1; rail.visible = false; arms[1].el.add(rail); rail.position.set(1.55, -6.5, 1.5); rail.rotation.x = Math.PI;
    const lance = new TH.Group(); core.add(lance); lance.visible = false; for (const [r, o, c] of [[1.2, .3, 0x3a7aff], [.5, .9, 0xe8f6ff]]) { const g = new TH.CylinderGeometry(r * .8, r, 60, 14, 1, true); g.translate(0, 30, 0); g.rotateX(Math.PI / 2); const m = new TH.Mesh(g, glowMat(c, o)); m.userData.dyn = 1; lance.add(m); }
    const arcM = new TH.Mesh(new TH.RingGeometry(14, 17, 48, 1, 0, Math.PI * .9), glowMat(0x9ad8ff, 0)); arcM.userData.dyn = 1; arcM.visible = false; body.add(arcM);
    const reveal = wave(body, 18, false, 0x9ad8ff), seams = []; body.traverse(o => { if (o.isMesh && o.material === GL) seams.push(o); });
    const bt = bolts(body, 8, () => { const a = joints[(rnd() * joints.length) | 0].g.getWorldPosition(V(0, 0, 0)), b = joints[(rnd() * joints.length) | 0].g.getWorldPosition(V(0, 0, 0)); body.worldToLocal(a); body.worldToLocal(b); return [a, b]; }, 0x9ad8ff);
    const mv = moves({ transform: 20000, broadside: 2200, missiles: 3000, rail: 2600, aegis: 2400, blade: 2600, lance: 2800, overdrive: 4200, hit: 520 }), hit = hitKit(body, shk), drv = {};
    const f = (n, t) => drv[n] != null ? drv[n] : mv.f(n, t), q0 = new TH.Quaternion(), S = scr();
    const out = { grp, r: 22, h: 30, form: 0, ph: "ship", act: n => { if (n === "transform" && out.form > .99) return; mv.play(n); }, drive: (n, v) => { if (v == null || v < 0) delete drv[n]; else drv[n] = v; },
      moves: ["broadside", "missiles", "rail", "aegis", "blade", "lance", "overdrive"], mouth: core, lens: null, reactor: core };
    const tick = t => { const ft = f("transform", t); if (ft >= 0) out.form = ft; else if (out.ftL > .9) out.form = 1; out.ftL = ft; const u = out.form;
      out.ph = u <= 0 ? "ship" : u < .12 ? "activation" : u < .32 ? "separation" : u < .5 ? "limbs" : u < .7 ? "core" : u < .88 ? "weapons" : u < 1 ? "reveal" : "warform";
      const wake = u > 0 && u < 1 ? bell(u, 0, .05, .9, 1) : 0, unlock = bell(u, .02, .06, .1, .14);
      for (const j of joints) { const k = j.ease ? ss(j.a, j.b, u) : Math.min(1, Math.max(0, (u - j.a) / (j.b - j.a))); j.g.position.lerpVectors(j.sp, j.mp, k); j.g.quaternion.slerpQuaternions(j.sq, j.mq, k);
        if (unlock > 0) j.g.position.y += Math.sin(t * .05 + j.a * 40) * .05 * unlock; }
      // the ship drifts nose-on; the mech breathes in its stance
      const mech = ss(.88, 1, u); body.position.y = Math.sin(t * .0008) * (.4 + mech * .2); body.rotation.z = Math.sin(t * .0005) * .02 * (1 - mech);
      const fo = f("overdrive", t), od = bell(fo, 0, .15, .85, 1), fb = f("blade", t), fa = f("aegis", t), fl = f("lance", t), fr = f("rail", t), fm = f("missiles", t), fbs = f("broadside", t), fx = f("hit", t);
      // the blade swing: the right arm sweeps across, the arc trails it
      if (fb >= 0 && u > .99) { const sw = ss(.25, .6, fb), back = bell(fb, 0, .2, .3, .45); arms[1].sh.rotation.x += -back * 1.6 + sw * 1.2; arms[1].sh.rotation.z += back * .5 - sw * 1.1; arms[1].el.rotation.x -= back * .4; }
      arcM.visible = fb >= 0 && u > .99; if (arcM.visible) { const k = bell(fb, .3, .4, .6, .85); arcM.material.opacity = k * .8; arcM.position.set(0, 4, 6); arcM.rotation.set(-Math.PI / 2 + .3, 0, -.6 + ss(.3, .6, fb) * 1.4); arcM.scale.setScalar(.6 + ss(.3, .9, fb) * .7); }
      const bl = u > .99 ? 1 : ss(.74, .88, u); blade.scale.set(1, .001 + bl * 17 * (1 + od * .15), 1); blade.visible = bl > .01; bladeS.material.opacity = bl * (.5 + .3 * Math.sin(t * .02)); bladeS.scale.setScalar(3 + bl * 3 + bell(fb, .3, .4, .6, .8) * 6);
      const sh = Math.max(ss(.7, .85, u) * .5, bell(fa, 0, .15, .8, 1), od * .6); hexM.uniforms.uO.value = u < .99 ? sh : .5 + bell(fa, 0, .15, .8, 1) * .7 + od * .4; hexM.uniforms.uT.value = t; shield.scale.setScalar(u < .7 ? .55 : .55 + ss(.7, .85, u) * .45);
      const hq = fa >= 0 ? (fa * 3) % 1 : -1; hexM.uniforms.uHit.value.set(Math.sin(t * .001) * 2.5, Math.cos(t * .0013) * 2, hq);
      // reactor, eyes, seams: the awakening lights the hull; the reveal and overdrive flare them
      const glow = .45 + wake * .6 + bell(u, .58, .66, .9, 1) * .8 + od * 1.2 + bell(fl, 0, .2, .8, 1) * .6; coreS.material.opacity = Math.min(1, glow * .7); coreS.scale.setScalar(5 + glow * 3 + od * Math.sin(t * .04) * 1.5); core.userData.g.rotation.z = t * .002;
      eyes.forEach(e => { const k = u < .6 ? 0 : ss(.6, .66, u) * (.7 + bell(u, .88, .92, .96, 1) * .8) + od * .4; e.material.opacity = Math.min(1, k); e.scale.setScalar(1.4 * (1 + bell(u, .88, .92, .96, 1) * 1.5)); });
      seams.forEach((m, k) => { m.material.opacity = Math.min(1, .55 + wake * .3 + od * (.4 + .3 * Math.sin(t * .03 + k)) + unlock * .4 * Math.sin(t * .06 + k)); }); halo.userData.rr.rotation.z = t * (.0005 + wake * .002 + od * .004);
      // engines: the ship's stern thrust; they flare through the awakening and fire beneath the mech at the reveal
      legs.forEach(L => L.fl.forEach((s, k) => { const th = (u <= 0 ? .75 : 0) + wake * .9 + bell(u, .86, .9, .97, 1) * 1.2 + .35 * mech + od * .5; s.material.opacity = Math.min(1, th * (.8 + .2 * Math.sin(t * .05 + k))); s.scale.setScalar(2.4 + th * 3.2); }));
      // weapons: broadside flashes from the flank/forearm cannons and the deck turrets, missiles from the pods, the rail slug, the lance
      const fire = (fbs >= 0 ? Math.max(0, Math.sin(fbs * Math.PI * 7)) * (1 - fbs) : 0) + od * (rnd() < .3 ? 1 : 0); arms.forEach((A, k) => A.bar.forEach((s, i) => { s.material.opacity = fire * (((i + k) % 2) ? 1 : .7); s.scale.setScalar(2 + fire * 3); })); cannons.forEach(C => C.mz.forEach(s => { s.material.opacity = fire * .9; s.scale.setScalar(2 + fire * 2.5); }));
      const open = Math.max(fm >= 0 ? bell(fm, 0, .1, .85, 1) : 0, od); if (u > .99) pods.forEach(P => P.lid.rotation.set(-1.25 - open * .5, 0, 0));
      for (let k = 0; k < NM; k++) { const m = mD[k], q = fm < 0 ? -1 : (fm - m.h * .4) / .5; if (q > 0 && q < 1) { const P = pods[m.s].p.getWorldPosition(S.p); body.worldToLocal(P); mis.put(k, P.x + Math.sin(m.a) * q * 6, P.y + q * 6 - q * q * 4 + Math.cos(m.a) * q * 2, P.z + q * 34 * m.d + q * 8, 1.6, 1 - q * .3); } else mis.put(k, 0, 0, 0, 0, 0); } mis.done();
      rail.visible = fr >= 0 && fr > .55 && fr < .75; if (rail.visible) { rail.scale.set(1 + (1 - (fr - .55) / .2), 70 * ss(.55, .6, fr), 1); rail.material.opacity = 1 - (fr - .55) / .2; } if (fr >= 0) arms[1].bar.forEach(s => { s.material.opacity = Math.max(s.material.opacity, bell(fr, 0, .5, .55, .6)); s.scale.setScalar(2 + bell(fr, 0, .5, .55, .6) * 3); });
      lance.visible = fl >= 0 && fl > .3 && fl < .85; if (lance.visible) { const k = bell(fl, .3, .36, .75, .85); lance.children.forEach((m, i) => { m.material.opacity = (i ? .9 : .3) * k; m.scale.set(1 + Math.sin(t * .05) * .05, 1 + Math.sin(t * .06) * .05, ss(.3, .4, fl)); }); }
      reveal(u > .88 && u < 1 ? ss(.9, 1, u) : -1); bt(t, wake * 3 + od * 5 + unlock * 6);
      hit(bell(fx, 0, .05, .4, 1) + od * .15, t); };
    out.tick = tick; tick(0); bake(body); return out; }
