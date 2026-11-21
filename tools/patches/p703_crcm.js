/* ---------- v703 the Carcinid on the battle screen and the map: profiles, sizes, weapons, and their 3D models (built in code) ----------
   Styled on the owner's paintings: near-black chitin with a violet sheen, gilded seams, gold claw tips and spines, cyan light in the joints and eyes, violet and red coral. The crabs walk (each leg steps in turn,
   the claws lift and the body rides on them), the coral on a Spitter sways, and a Breach nest's coral breathes round its rift. */
Object.assign(CPROF, { cscut: ["fighter", "acid", .12, .24, 7, 0], cspit: ["frigate", "plasma", .08, .12, 5, 0], charv: ["support", "acid", .14, .08, 3, 0], cguard: ["cruiser", "laser", .36, .03, 3, 2], cfrig: ["frigate", "ion", .16, .14, 5.5, 1], cint: ["interceptor", "laser", .06, .3, 9, 0], cnest: ["station", "acid", .3, 0, 0, 2] });
Object.assign(BOSSK, { cscut: 1.55, cspit: 1.6, charv: 1.6, cguard: 1.85, cfrig: 1.7, cint: 1.55, cnest: 2.1 });
Object.assign(MIM_HULL, { cscut: .8, cspit: .9, charv: .95, cguard: 1.4, cfrig: 1.15, cint: .9, cnest: 1.7 });
Object.assign(MIM_PACK, { cscut: 1, cspit: 1, charv: 1, cint: 1 }); MIM_STA.cnest = .44;
Object.assign(MON_ATK, { cscut: [["acid", 3, "#3fe0c8", .14, {}], ["flak", 4, "#ffc870", .12, {}]], cspit: [["plasma", 2, "#b48cff", .24, { hv: 1 }], ["acid", 3, "#ffc870", .2, {}]], charv: [["acid", 3, "#3fe0c8", .2, {}], ["flak", 3, "#7ff8e4", .14, {}]],
  cguard: [["flak", 6, "#e8b45a", .12, {}], ["ion", 2, "#7ff8e4", .22, {}]], cfrig: [["ion", 3, "#7ff8e4", .18, {}], ["missile", 3, "#e8b45a", .2, {}]], cint: [["laser", 3, "#9ff8ec", .1, {}], ["flak", 5, "#ffc870", .1, {}]],
  cnest: [["missile", 4, "#3fe0c8", .2, { flank: 1 }], ["plasma", 2, "#e8b45a", .26, { hv: 1 }]] });
Object.assign(MIM_ATK, { cscut: "slam", cguard: "slam", cspit: "spit", cint: "spit" });
Object.assign(MON_EL, { carcinid: "water", crcpat: "water" });
{ const crab = `vec3 p = position; float ph = mt * 6.28318 + p.x * 2.6 + (p.z > 0. ? 0. : 3.14159), lz = clamp((abs(p.z) - .95) / 1.5, 0., 1.) * (1. - smoothstep(1.15, 1.35, p.x));
    transformed.y += lz * .16 * max(0., sin(ph)); transformed.x += lz * .12 * cos(ph);
    float cl = smoothstep(1.3, 1.9, p.x); transformed.y += cl * (.09 * sin(mt * 2.0944 + (p.z > 0. ? 0. : 1.6)) + .05 * (p.x - 1.3) * sin(mt * 4.18879));
    float tu = smoothstep(.55, 1.6, p.y) * step(abs(p.z), .9) * (1. - cl); transformed.x += tu * .07 * sin(mt * 2.0944 + p.y * 1.4); transformed.z += tu * .05 * cos(mt * 2.0944 + p.y);
    transformed.y += (1. - lz) * .045 * sin(mt * 4.18879);`;
  for (const k of ["cscut", "cspit", "charv", "cguard"]) MON_WAVE[k] = crab;
  MON_WAVE.cnest = MON_WAVE.carcinid = `vec3 p = position; float an = atan(p.z, p.x), rr = length(p.xz), sp = smoothstep(-.6, 3.6, p.y) * step(.6, rr) * (1. - step(2.35, rr) * step(1.6, p.y) * .7);
    transformed.x += sp * .09 * sin(mt * 2.0944 + an * 3. + p.y); transformed.z += sp * .09 * cos(mt * 2.0944 + an * 3. + p.y);
    float rf = 1. - smoothstep(1.2, 1.7, length(p.xy - vec2(0., 1.1))) * step(abs(p.z), .5); transformed.xy += (p.xy - vec2(0., 1.1)) * (1. - rf) * .03 * sin(mt * 4.18879);`;
  MON_WAVE.crcpat = `transformed.y += .08 * sin(mt * 2.0944 + position.x * .25 + position.z * .3);`; }
let CRC_MC = null;
function crcMats() { if (CRC_MC) return CRC_MC; const C = CRC_MC = {}, tex = (w, h, draw) => { const t = texCanvas(w, h, draw); t.wrapS = t.wrapT = TH.RepeatWrapping; return t; };
  /* the paintings' chitin: near-black plates with a violet and blue sheen, gilded seams between the segments, pitted */
  const sC = tex(256, 128, (x, W, H) => { const n = fbm2(7031), img = x.createImageData(W, H), d = img.data;
    for (let py = 0; py < H; py++) for (let px = 0; px < W; px++) { const v = n(px / 22, py / 22, 10, 4), band = Math.abs(Math.sin(py / H * Math.PI * 7)), seam = band < .12 ? .35 : 1, sp = n(px / 6, py / 6, 10, 2) > .72 ? .55 : 1, o = (py * W + px) * 4;
      const ir = n(px / 40 + 7, py / 30, 10, 3); if (band < .1) { d[o] = 214; d[o + 1] = 160; d[o + 2] = 78; } else { d[o] = (16 + v * 26 + ir * 30) * sp; d[o + 1] = (12 + v * 14 + (1 - ir) * 18) * sp; d[o + 2] = (26 + v * 40 + ir * 36) * sp; } d[o + 3] = 255; } x.putImageData(img, 0, 0); });
  const sE = tex(256, 128, (x, W, H) => { x.fillStyle = "#000"; x.fillRect(0, 0, W, H); for (let i = 1; i < 7; i++) { const y = i / 7 * H; x.strokeStyle = "rgba(255,255,255,.55)"; x.lineWidth = 1.2; x.beginPath(); x.moveTo(0, y); for (let px = 0; px <= W; px += 16) x.lineTo(px, y + Math.sin(px * .09 + i) * 2); x.stroke(); }
    const r = rnd(7032); for (let i = 0; i < 40; i++) { x.fillStyle = `rgba(255,255,255,${.3 + r() * .5})`; x.beginPath(); x.arc(r() * W, r() * H, .8 + r() * 1.6, 0, TAU); x.fill(); } });
  sC.encoding = TH.sRGBEncoding;
  C.shell = new TH.MeshPhysicalMaterial({ map: sC, emissiveMap: sE, emissive: 0x3fe8f0, emissiveIntensity: .7, metalness: .55, roughness: .3, clearcoat: 1, clearcoatRoughness: .12, envMapIntensity: 1.1 });
  C.shellD = C.shell.clone(); C.shellD.color = new TH.Color(0x8a80a0); C.shellD.emissiveIntensity = .5;
  C.under = new TH.MeshPhysicalMaterial({ color: 0x1c1430, roughness: .45, metalness: .1, clearcoat: .6, envMapIntensity: .7 });
  C.joint = new TH.MeshStandardMaterial({ color: 0x0e0a16, roughness: .55, metalness: .2 });
  C.claw = new TH.MeshPhysicalMaterial({ map: sC, color: 0xb8a8e0, metalness: .5, roughness: .24, clearcoat: 1, clearcoatRoughness: .1, envMapIntensity: 1.2 });
  C.tip = new TH.MeshPhysicalMaterial({ color: 0xd2a45c, metalness: .85, roughness: .26, clearcoat: 1, envMapIntensity: 1.4 });
  const cC = tex(128, 128, (x, W, H) => { const n = fbm2(7033), img = x.createImageData(W, H), d = img.data; for (let py = 0; py < H; py++) for (let px = 0; px < W; px++) { const v = n(px / 9, py / 9, 10, 3), pore = n(px / 3, py / 3, 10, 2) > .66 ? .45 : 1, o = (py * W + px) * 4;
    d[o] = (190 + v * 60) * pore; d[o + 1] = (50 + v * 50) * pore; d[o + 2] = (180 + v * 70) * pore; d[o + 3] = 255; } x.putImageData(img, 0, 0); });
  cC.encoding = TH.sRGBEncoding;
  C.coral = new TH.MeshPhysicalMaterial({ map: cC, roughness: .75, metalness: 0, clearcoat: .3, emissive: 0x3a0a40, emissiveIntensity: .4, envMapIntensity: .6 });
  C.coralB = C.coral.clone(); C.coralB.color = new TH.Color(0xffb070); /* red-orange coral among the violet, as in the paintings */
  C.glow = new TH.MeshBasicMaterial({ color: 0x8ffbe8, toneMapped: false });
  C.glowS = new TH.MeshBasicMaterial({ color: 0x2fd0b8, transparent: true, opacity: .3, toneMapped: false, blending: TH.AdditiveBlending, depthWrite: false });
  C.eye = new TH.MeshBasicMaterial({ color: 0x9ffcff, toneMapped: false });
  C.pearl = new TH.MeshPhysicalMaterial({ color: 0x1a5a64, roughness: .08, metalness: 0, clearcoat: 1, emissive: 0x2fe0d0, emissiveIntensity: .8, envMapIntensity: 1.5 }); C.pearl.userData.pulse = "(.6 + .4 * sin(uMT * 1.5 + vViewPosition.x))";
  C.sac = new TH.MeshPhysicalMaterial({ color: 0x03322c, emissive: 0x2fe0c0, emissiveIntensity: .85, roughness: .2, clearcoat: .8, transparent: true, opacity: .88, envMapIntensity: .4 }); C.sac.userData.pulse = "(.7 + .3 * sin(uMT * 1.3))";
  C.metal = new TH.MeshPhysicalMaterial({ color: 0x2c2438, metalness: .85, roughness: .32, clearcoat: 1, envMapIntensity: 1.2 });
  C.rock = new TH.MeshStandardMaterial({ color: 0x0c0a10, roughness: .92, metalness: .05, flatShading: true });
  C.void = new TH.MeshBasicMaterial({ color: 0x010a0c, side: TH.DoubleSide });
  C.core = new TH.MeshPhysicalMaterial({ color: 0x021a18, emissive: 0x2fe8cc, emissiveIntensity: 1.2, roughness: .15, clearcoat: 1, transparent: true, opacity: .9 }); C.core.userData.pulse = "(.65 + .35 * sin(uMT * 2.1))";
  return C; }
function buildCarc(k) { const C = crcMats(), g = new TH.Group(), r = rnd(hash("crc" + k)); g.userData.eng = [];
  const V = (x, y, z) => new TH.Vector3(x, y, z), add = (m, x, y, z) => { if (x != null) m.position.set(x, y || 0, z || 0); g.add(m); return m; };
  const ell = (sx, sy, sz, mat, x, y, z, seg) => { const m = add(new TH.Mesh(new TH.SphereGeometry(1, seg || 18, Math.round((seg || 18) * .7)), mat), x, y, z); m.scale.set(sx, sy, sz); return m; };
  const seg = (a, b, r0, r1, mat) => { const d = b.clone().sub(a), L = d.length(), m = new TH.Mesh(new TH.CylinderGeometry(r1, r0, L, 8, 1), mat); m.position.copy(a).addScaledVector(d, .5); m.quaternion.setFromUnitVectors(V(0, 1, 0), d.normalize()); g.add(m); return m; };
  const cone = (len, rad, mat, from, dir, bend) => { const geo = new TH.ConeGeometry(rad, len, 8, 4); geo.translate(0, len / 2, 0); if (bend) { const P = geo.attributes.position; for (let i = 0; i < P.count; i++) { const y = P.getY(i) / len; P.setZ(i, P.getZ(i) + bend * y * y * len); } geo.computeVertexNormals(); }
    const m = add(new TH.Mesh(geo, mat)); m.position.copy(from); m.quaternion.setFromUnitVectors(V(0, 1, 0), dir.clone().normalize()); return m; };
  /* a carapace: a flattened, front-pointed dome with segment ridges across it and a slight lip at the rim */
  const shell = (rx, ry, rz, o, x, y, z, mat) => { o = o || {}; const geo = new TH.SphereGeometry(1, 40, 24), P = geo.attributes.position;
    for (let i = 0; i < P.count; i++) { let px = P.getX(i), py = P.getY(i), pz = P.getZ(i); if (py < 0) py *= o.belly == null ? .35 : o.belly; const f = Math.max(0, px); px *= 1 + (o.point == null ? .14 : o.point) * f * f;
      py += (o.ridge == null ? .05 : o.ridge) * Math.cos(px * Math.PI * 3.2) * Math.max(0, py); pz *= 1 + .07 * Math.max(0, 1 - Math.abs(py) * 6); P.setXYZ(i, px * rx, py * ry, pz * rz); }
    geo.computeVertexNormals(); const m = add(new TH.Mesh(geo, mat || C.shell), x || 0, y || 0, z || 0);
    if (!mat || mat === C.shell) { const rim = add(new TH.Mesh(new TH.TorusGeometry(1, .035, 6, 48), C.tip), x || 0, (y || 0) + .01, z || 0); rim.rotation.x = Math.PI / 2; rim.scale.set(rx * 1.01, rz * 1.06, ry * 1.4); } /* the gilded rim */
    return m; };
  const legs = (n, th, reach, x0, dx) => { for (const s of [1, -1]) for (let i = 0; i < n; i++) { const xi = x0 - i * dx, lean = (n / 2 - .5 - i) * .22;
    const hip = V(xi, -.05, s * .8), knee = V(xi + lean * .5, .5, s * (1.45 * reach)), ank = V(xi + lean, -.25, s * (2.1 * reach)), foot = V(xi + lean * 1.3, -.95, s * (2.35 * reach));
    seg(hip, knee, .17 * th, .14 * th, C.shell); seg(knee, ank, .14 * th, .1 * th, C.shell); seg(ank, foot, .095 * th, .025 * th, C.tip);
    for (const [a, b2] of [[hip, knee], [knee, ank]]) { const mpt = a.clone().lerp(b2, .55); cone(.16 * th, .04 * th, C.tip, mpt, V(.2, 1, s * .6), .05); }
    for (const j of [knee, ank]) { ell(.15 * th, .15 * th, .15 * th, C.joint, j.x, j.y, j.z, 8); ell(.06 * th, .06 * th, .06 * th, C.glow, j.x, j.y - .08 * th, j.z, 6); } } };
  const claw = (s, kk, x0) => { x0 = x0 || 0; kk *= 1.3; const sh = V(.95 + x0, 0, s * .62), el = V(1.4 + x0, .3, s * 1.22), wr = V(1.9 + x0, .15, s * 1.02), pm = V(2.2 + x0 * 1.1 + .1 * (kk - 1), .12, s * .95);
    seg(sh, el, .13 * kk, .12 * kk, C.shellD); seg(el, wr, .12 * kk, .14 * kk, C.claw); ell(.13 * kk, .13 * kk, .13 * kk, C.joint, el.x, el.y, el.z, 8);
    const palm = ell(.42 * kk, .27 * kk, .24 * kk, C.claw, pm.x, pm.y, pm.z, 18); palm.rotation.y = s * .15;
    cone(.62 * kk, .11 * kk, C.claw, V(pm.x + .3 * kk, pm.y - .06 * kk, pm.z), V(1, -.12, -s * .12), .08); /* the fixed finger */
    cone(.56 * kk, .1 * kk, C.tip, V(pm.x + .26 * kk, pm.y + .14 * kk, pm.z), V(1, .2, -s * .1), -.1); /* the moving finger */
    for (let i = 0; i < 4; i++) cone(.12 * kk, .035 * kk, C.tip, V(pm.x + (-.1 + i * .12) * kk, pm.y + .22 * kk, pm.z), V(.2, 1, s * .2)); ell(.08 * kk, .05 * kk, .05 * kk, C.glow, pm.x - .1 * kk, pm.y - .05 * kk, pm.z + s * .2 * kk, 8); };
  const eyes = (rx, ry, sp) => { for (const s of [1, -1]) { const a = V(rx * .82, ry * .25, s * (sp || .26)), b = V(rx * .98 + .14, ry * .35 + .34, s * ((sp || .26) + .06)); seg(a, b, .045, .035, C.shellD); ell(.085, .07, .07, C.eye, b.x, b.y, b.z, 10); ell(.16, .13, .13, C.glowS, b.x, b.y, b.z, 8); } };
  const rimSpikes = (rx, rz, n, len, mat) => { for (let i = 0; i < n; i++) { const a = -Math.PI * .82 + i / (n - 1) * Math.PI * 1.64, rim = V(Math.cos(a) * rx, -.02, Math.sin(a) * rz);
    for (const s of [1, -1]) { const p = V(rim.x, rim.y, rim.z * s); cone(len * (.8 + r() * .4), .05 + len * .12, mat || C.tip, p, V(Math.cos(a) * .6, .45, Math.sin(a) * s), .05); } } };
  const vents = (pts) => { for (const p of pts) { ell(.07, .03, .07, C.glow, p.x, p.y, p.z, 8); ell(.18, .08, .18, C.glowS, p.x, p.y, p.z, 8); } };
  const coralTree = (base, h, spread, depth, mat, glowTip) => { const grow = (a, dir, len, d, rad) => { const b = a.clone().addScaledVector(dir.clone().normalize(), len); seg(a, b, rad, rad * .72, mat); ell(rad * .74, rad * .74, rad * .74, mat, b.x, b.y, b.z, 8);
      if (d <= 0) { if (glowTip) { ell(rad * .9, rad * .9, rad * .9, C.glow, b.x, b.y, b.z, 8); ell(rad * 2.4, rad * 2.4, rad * 2.4, C.glowS, b.x, b.y, b.z, 8); } return; }
      const nb = 2 + (r() < .35 ? 1 : 0); for (let i = 0; i < nb; i++) grow(b, dir.clone().normalize().add(V((r() - .5) * spread, .25 + r() * .3, (r() - .5) * spread)), len * (.62 + r() * .2), d - 1, rad * .72); };
    grow(base, V((r() - .5) * .3, 1, (r() - .5) * .3), h, depth, h * .12); };
  if (k === "cscut") { /* the Scuttle Drone: small, sleek, all points */
    shell(1.25, .52, .95, { point: .3, ridge: .06 }); shell(1.0, .25, .8, { belly: 1, ridge: 0 }, 0, -.12, 0, C.under);
    cone(.55, .08, C.tip, V(1.45, .05, 0), V(1, .15, 0), 0); rimSpikes(1.2, .92, 6, .26); legs(4, .85, .95, .55, .42); claw(1, .72); claw(-1, .72); eyes(1.25, .52, .22);
    vents([V(-.2, .5, .25), V(-.2, .5, -.25), V(-.6, .42, 0)]); }
  else if (k === "cspit") { /* the Coral Spitter: a living battery of coral on its back */
    shell(1.2, .5, 1.0, { point: .12, ridge: .05 }); shell(1.0, .25, .85, { belly: 1, ridge: 0 }, 0, -.12, 0, C.under); legs(4, .95, 1, .5, .42); claw(1, .62); claw(-1, .62); eyes(1.2, .5, .24);
    for (let i = 0; i < 5; i++) { const a = i / 5 * TAU; coralTree(V(-.15 + Math.cos(a) * .35, .35, Math.sin(a) * .35), .35 + r() * .15, .9, 2, i % 3 ? C.coral : C.coralB, true); }
    const bA = V(.1, .45, 0), bB = V(.95, 1.25, 0); seg(bA, bB, .2, .15, C.coral); for (let i = 0; i < 4; i++) { const t = .2 + i * .22, p = bA.clone().lerp(bB, t); ell(.2, .07, .2, C.shellD, p.x, p.y, p.z, 12).quaternion.setFromUnitVectors(V(0, 1, 0), bB.clone().sub(bA).normalize()); }
    ell(.13, .13, .13, C.glow, bB.x, bB.y, bB.z, 10); ell(.34, .34, .34, C.glowS, bB.x, bB.y, bB.z, 10); }
  else if (k === "charv") { /* the Tide Harvester: wide and low, resin sacs on its back, long feelers */
    shell(1.15, .42, 1.25, { point: .05, ridge: .04 }); shell(1.0, .22, 1.1, { belly: 1, ridge: 0 }, 0, -.1, 0, C.under); legs(4, .9, 1.08, .5, .4); eyes(1.15, .42, .3);
    for (const s of [1, -1]) { ell(.55, .4, .42, C.sac, -.25, .45, s * .45, 20); for (let i = 0; i < 3; i++) { const b = ell(.57, .06, .44, C.shellD, -.25 + (i - 1) * .3, .45, s * .45, 14); b.scale.set(.1, .43, .45); } }
    for (const s of [1, -1]) { const a = V(1.05, .05, s * .3), b = V(1.9, .35, s * .55), c = V(2.6, .15, s * .4); seg(a, b, .06, .045, C.shellD); seg(b, c, .045, .03, C.claw); cone(.22, .04, C.tip, c, V(1, -.3, -s * .3)); cone(.2, .035, C.tip, c, V(1, .2, -s * .2)); }
    for (const s of [1, -1]) cone(.3, .06, C.tip, V(1.15, -.12, s * .14), V(1, -.4, -s * .2), .1); vents([V(.35, .38, 0)]); }
  else if (k === "cguard") { /* the Shell Guardian: a domed fortress of a shell, crusted with coral, one great claw */
    shell(1.3, .95, 1.1, { point: .06, ridge: .08, belly: .3 }); shell(1.1, .28, .95, { belly: 1, ridge: 0 }, 0, -.14, 0, C.under); legs(4, 1.25, 1.0, .5, .42); claw(1, 1.05, .05); claw(-1, .78); eyes(1.3, .7, .3);
    for (let i = 0; i < 14; i++) { const a = r() * TAU, el = .25 + r() * .9, p = V(Math.cos(a) * Math.cos(el) * 1.25, Math.sin(el) * .9, Math.sin(a) * Math.cos(el) * 1.05); cone(.22 + r() * .2, .07, C.tip, p, p.clone().normalize().add(V(0, .4, 0)), .04); }
    for (let i = 0; i < 4; i++) { const a = r() * TAU, p = V(Math.cos(a) * .6 - .2, .72, Math.sin(a) * .5); coralTree(p, .22, .8, 1, i % 2 ? C.coral : C.coralB, i === 0); }
    vents([V(-.5, .75, .3), V(-.5, .75, -.3)]); }
  else if (k === "cfrig") { /* the Scuttle Frigate: a carapace hull, dorsal plates, mandible prows, folded legs and teal drives */
    shell(2.2, .55, .95, { point: .25, ridge: .03, belly: .55 }, 0, 0, 0, C.shell); shell(2.0, .25, .8, { belly: 1, ridge: 0 }, -.05, -.2, 0, C.metal);
    for (let i = 0; i < 5; i++) { const p = ell(.5, .14, .62 - i * .04, C.shellD, .9 - i * .48, .5 - Math.abs(i - 1.5) * .04, 0, 18); p.rotation.z = -.15; }
    for (const s of [1, -1]) { cone(.9, .12, C.tip, V(2.0, -.02, s * .32), V(1, -.05, -s * .25), .12); cone(.5, .07, C.claw, V(1.6, .1, s * .55), V(1, .05, 0)); }
    for (const s of [1, -1]) for (let i = 0; i < 3; i++) { const x = .7 - i * .75, a = V(x, -.25, s * .8), b = V(x - .3, -.6, s * 1.2), c = V(x - .8, -.5, s * .95); seg(a, b, .08, .07, C.shellD); seg(b, c, .07, .04, C.tip); ell(.08, .08, .08, C.joint, b.x, b.y, b.z, 8); }
    for (let i = 0; i < 7; i++) for (const s of [1, -1]) cone(.35 + (i % 2) * .15, .07, C.tip, V(1.3 - i * .5, .4, s * (.55 + Math.sin(i) * .05)), V(-.6, .8, s * .5), -.1);
    ell(.35, .16, .3, C.metal, 1.15, .42, 0, 14); for (const s of [1, -1]) ell(.14, .04, .05, C.glow, 1.35, .45, s * .17, 8);
    for (const z of [-.42, 0, .42]) { ell(.12, .18, .18, C.glow, -2.25, .02, z, 10); ell(.4, .32, .32, C.glowS, -2.4, .02, z, 10); }
    vents([V(-.3, .45, .45), V(-.3, .45, -.45)]); }
  else if (k === "cint") { /* the Tidal Interceptor: a slim body behind a split claw of a prow, swept fins, hot drives */
    shell(1.55, .34, .45, { point: .2, ridge: .03, belly: .6 }, 0, 0, 0, C.shell);
    for (const s of [1, -1]) { cone(1.6, .13, C.claw, V(.9, 0, s * .32), V(1, 0, s * .12), -s * .35); cone(.5, .05, C.tip, V(2.1, 0, s * .26), V(1, 0, -s * .5), -s * .1); }
    for (const s of [1, -1]) { const f = ell(.75, .05, .45, C.shellD, -.7, -.02, s * .65, 16); f.rotation.y = s * .5; f.rotation.x = s * .25; }
    cone(.6, .1, C.shellD, V(-.4, .25, 0), V(-.4, 1, 0), -.2); for (let i = 0; i < 4; i++) cone(.25, .05, C.tip, V(.6 - i * .4, .22, 0), V(-.5, 1, 0), -.05); ell(.25, .1, .14, C.glow, .55, .25, 0, 10);
    for (const s of [1, -1]) { ell(.1, .12, .12, C.glow, -1.6, 0, s * .18, 10); ell(.34, .26, .26, C.glowS, -1.75, 0, s * .18, 10); } }
  else if (k === "cnest") { /* the Breach nest: a rift into the Abyss in a mound of rock, ringed by chitin spires, choked with coral and eggs */
    const base = add(new TH.Mesh(new TH.DodecahedronGeometry(3, 1), C.rock), 0, -1.55, 0); base.scale.set(1, .32, .85);
    for (let i = 0; i < 9; i++) { const a = r() * TAU, d = 1.6 + r() * 1.3, b = add(new TH.Mesh(new TH.DodecahedronGeometry(.35 + r() * .35, 0), C.rock), Math.cos(a) * d, -1.05, Math.sin(a) * d * .85); b.rotation.set(r() * 3, r() * 3, r() * 3); }
    for (let i = 0; i < 9; i++) { const a = i / 9 * TAU + .2, p = V(Math.cos(a) * 2.35, -1.1, Math.sin(a) * 2.0), in2 = V(-Math.cos(a), 0, -Math.sin(a)); cone(3.6 + r() * 1.4, .28, C.shell, p, V(0, 1, 0).addScaledVector(in2, .18), .32).rotation.y += 0; }
    const ring = add(new TH.Mesh(new TH.TorusGeometry(1.15, .2, 10, 36), C.shell), 0, 1.1, 0); ring.scale.set(1, 1.35, 1);
    for (let i = 0; i < 12; i++) { const a = i / 12 * TAU; cone(.42, .08, C.tip, V(Math.cos(a) * 1.25, 1.1 + Math.sin(a) * 1.6, 0), V(Math.cos(a), Math.sin(a) * 1.3, 0)); }
    const hole = add(new TH.Mesh(new TH.CircleGeometry(1.02, 36), C.void), 0, 1.1, 0); hole.scale.set(1, 1.35, 1);
    const core = ell(.55, .75, .2, C.core, 0, 1.1, 0, 20); ell(1.0, 1.35, .5, C.glowS, 0, 1.1, 0, 18); ell(1.5, 1.9, .9, C.glowS, 0, 1.1, 0, 14); core.renderOrder = 2;
    for (let i = 0; i < 14; i++) { const a = r() * TAU, d = .9 + r() * 1.7; coralTree(V(Math.cos(a) * d, -1.0, Math.sin(a) * d * .85), .45 + r() * .45, 1, 2, i % 3 ? C.coral : C.coralB, i % 2 === 0); }
    for (let i = 0; i < 26; i++) { const a = r() * TAU, d = .6 + r() * 1.8, s = .14 + r() * .16; ell(s, s * 1.15, s, C.pearl, Math.cos(a) * d, -.95 + s * .6, Math.sin(a) * d * .85, 12); } }
  else if (k === "cpat") { /* a scout patrol on the map: a frigate with two interceptors on its wings */
    const f = buildCarc("cfrig"); g.add(f); for (const s of [1, -1]) { const c = buildCarc("cint"); c.scale.setScalar(.72); c.position.set(-1.4, .35, s * 2.3); g.add(c); } }
  return g; }
