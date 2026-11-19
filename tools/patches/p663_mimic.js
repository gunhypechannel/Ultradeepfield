/* ---------- v663 the Mimic Protocol: the species ----------
   After the owner's paintings: bodies woven from segmented black cables, a monstrous fanged head, clawed limbs, and a cyan neural glow
   showing between the cables. Every class is built from the same parts so they read as one species. Models face +x, y up. */
const MIMM = {};
const MIM_D = { mstalk: { s: 1, legs: 4, mane: 26, hump: .5, len: 1, gape: .55, tail: 8 }, mhunt: { s: .95, legs: 2, mane: 18, hump: .15, len: 1.35, gape: .8, tail: 16 }, mharv: { s: 1, legs: 0, mane: 12, hump: 0, len: .8, gape: .35, tail: 4, sac: 1 },
    massim: { s: 1.05, legs: 4, mane: 20, hump: .45, len: 1.05, gape: .6, tail: 8, plates: 1 }, mguard: { s: 1.15, legs: 4, mane: 14, hump: .25, len: .9, gape: .4, tail: 6, armour: 1 }, mtitan: { s: 1.25, legs: 4, mane: 40, hump: .8, len: 1.1, gape: .7, tail: 12, brood: 1 } };
function mimMats() { const C = MIMM; if (C.cable) return C;
  const tex = (w, h, draw) => { const t = texCanvas(w, h, draw); t.wrapS = t.wrapT = TH.RepeatWrapping; return t; };
  /* a cable: u runs along it (one segment per unit), v round it. Each segment is a ribbed metal sleeve with a dark seam at both ends */
  const cC = tex(128, 64, (x, W, H) => { const g = x.createLinearGradient(0, 0, W, 0); g.addColorStop(0, "#07090d"); g.addColorStop(.1, "#1d2430"); g.addColorStop(.3, "#3c4757"); g.addColorStop(.5, "#283140"); g.addColorStop(.78, "#141922"); g.addColorStop(.92, "#0b0e14"); g.addColorStop(1, "#050608"); x.fillStyle = g; x.fillRect(0, 0, W, H);
    const r = rnd(6620); for (let i = 0; i < 260; i++) { x.fillStyle = `rgba(${r() < .5 ? "0,0,0" : "150,170,200"},${.04 + r() * .08})`; x.fillRect(r() * W, r() * H, 1 + r() * 6, 1); }
    x.fillStyle = "rgba(0,0,0,.55)"; x.fillRect(W * .62, 0, 2, H); });
  const cE = tex(128, 64, (x, W, H) => { x.fillStyle = "#000"; x.fillRect(0, 0, W, H); const g = x.createLinearGradient(0, 0, W, 0); g.addColorStop(0, "rgba(40,190,255,.9)"); g.addColorStop(.05, "rgba(40,190,255,.0)"); g.addColorStop(.94, "rgba(40,190,255,0)"); g.addColorStop(1, "rgba(80,220,255,.9)"); x.fillStyle = g; x.fillRect(0, 0, W, H); });
  cC.encoding = TH.sRGBEncoding;
  C.cable = new TH.MeshPhysicalMaterial({ map: cC, color: 0x55606e, emissiveMap: cE, emissive: 0x3fc8ff, emissiveIntensity: .18, metalness: .9, roughness: .34, clearcoat: 1, clearcoatRoughness: .2, envMapIntensity: 1.2 });
  C.cableL = C.cable.clone(); C.cableL.emissiveIntensity = 1.3; /* the lit cables nearest the neural cores */
  /* the skull and armour: black chitin-metal with fine cyan vein lines */
  const sC = tex(256, 128, (x, W, H) => { const n = fbm2(6621), img = x.createImageData(W, H), d = img.data; for (let py = 0; py < H; py++) for (let px = 0; px < W; px++) { const v = n(px / 26, py / 26, 10, 4), o = (py * W + px) * 4; d[o] = 18 + v * 34; d[o + 1] = 22 + v * 38; d[o + 2] = 30 + v * 46; d[o + 3] = 255; } x.putImageData(img, 0, 0); });
  const sE = tex(256, 128, (x, W, H) => { x.fillStyle = "#000"; x.fillRect(0, 0, W, H); const r = rnd(6622); x.lineCap = "round"; for (let i = 0; i < 22; i++) { let px = r() * W, py = r() * H; x.strokeStyle = `rgba(60,200,255,${.35 + r() * .5})`; x.lineWidth = .8 + r() * 1.3; x.beginPath(); x.moveTo(px, py); for (let j = 0; j < 7; j++) { px += (r() - .5) * 40; py += (r() - .5) * 26; x.lineTo(px, py); } x.stroke(); } });
  sC.encoding = TH.sRGBEncoding;
  C.shell = new TH.MeshPhysicalMaterial({ map: sC, emissiveMap: sE, emissive: 0xffffff, emissiveIntensity: 1.4, metalness: .6, roughness: .28, clearcoat: 1, clearcoatRoughness: .1, envMapIntensity: 1.1 });
  C.bone = new TH.MeshPhysicalMaterial({ color: 0xc9d2dc, metalness: .5, roughness: .25, clearcoat: 1, envMapIntensity: 1.2 });
  C.claw = new TH.MeshPhysicalMaterial({ color: 0x1a2230, metalness: .9, roughness: .18, clearcoat: 1, envMapIntensity: 1.5, emissive: 0x0a3a60, emissiveIntensity: .5 });
  C.glow = new TH.MeshBasicMaterial({ color: 0x8fe8ff, toneMapped: false });
  C.glowS = new TH.MeshBasicMaterial({ color: 0x1e90e0, transparent: true, opacity: .28, toneMapped: false, blending: TH.AdditiveBlending, depthWrite: false });
  C.core = new TH.MeshPhysicalMaterial({ color: 0x06203a, emissive: 0x22b4ff, emissiveIntensity: 1.15, roughness: .15, metalness: 0, clearcoat: 1, transparent: true, opacity: .92 });
  C.core.userData.pulse = "(.72 + .28 * sin(uMT * 2.1))";
  C.sac = new TH.MeshPhysicalMaterial({ color: 0x020a14, emissive: 0x1aa0f0, emissiveIntensity: .55, roughness: .3, metalness: 0, clearcoat: .6, clearcoatRoughness: .3, envMapIntensity: .3 }); C.sac.userData.pulse = "(.7 + .3 * sin(uMT * 1.4))";
  C.mouth = new TH.MeshBasicMaterial({ color: 0x46c8ff, toneMapped: false });
  C.egg = new TH.MeshPhysicalMaterial({ color: 0x050208, emissive: 0x5a1fd0, emissiveIntensity: .75, roughness: .35, clearcoat: .3, envMapIntensity: .2, transparent: true, opacity: .9 });
  C.egg.userData.pulse = "(.6 + .4 * sin(uMT * 1.3 + vViewPosition.x))";
  C.plate = new TH.MeshStandardMaterial({ color: 0x6f7c8c, metalness: .85, roughness: .4 });
  C.plateL = new TH.MeshBasicMaterial({ color: 0x9fe4ff, toneMapped: false });
  C.holo = new TH.MeshBasicMaterial({ color: 0x5ff0ff, transparent: true, opacity: .35, toneMapped: false, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide });
  return C; }
function buildMimic(cls) {
  const C = mimMats(), g = new TH.Group(), r = rnd(hash("mim" + cls)); g.userData.eng = [];
  const V = (x, y, z) => new TH.Vector3(x, y, z), add = (m, x, y, z) => { if (x != null) m.position.set(x, y || 0, z || 0); g.add(m); return m; };
  /* a tapering cable along a curve, its rings swelling once per segment (the sleeves in the paintings); uv.x counts segments */
  const tube = (pts, r0, r1, mat, seg, curl) => { const cv = new TH.CatmullRomCurve3(pts), L = cv.getLength(), n = Math.max(8, Math.round(L * (seg || 9))), rad = 7, fr = cv.computeFrenetFrames(n, false), P = [], U = [], I = [], p = new TH.Vector3(), segL = .34;
    for (let i = 0; i <= n; i++) { const t = i / n; cv.getPointAt(t, p); const s = t * L / segL, rib = 1 + .16 * Math.pow(Math.abs(Math.sin(Math.PI * s)), 6) - .1 * Math.pow(Math.abs(Math.cos(Math.PI * s)), 18), R = (r0 + (r1 - r0) * Math.pow(t, curl || 1)) * rib;
      for (let j = 0; j <= rad; j++) { const a = j / rad * TAU, N = fr.normals[i], B = fr.binormals[i], cx = Math.cos(a), sx = Math.sin(a); P.push(p.x + R * (cx * N.x + sx * B.x), p.y + R * (cx * N.y + sx * B.y), p.z + R * (cx * N.z + sx * B.z)); U.push(s, j / rad); } }
    for (let i = 0; i < n; i++) for (let j = 0; j < rad; j++) { const a = i * (rad + 1) + j, b = a + rad + 1; I.push(a, b, a + 1, a + 1, b, b + 1); }
    const geo = new TH.BufferGeometry(); geo.setAttribute("position", new TH.Float32BufferAttribute(P, 3)); geo.setAttribute("uv", new TH.Float32BufferAttribute(U, 2)); geo.setIndex(I); geo.computeVertexNormals(); return add(new TH.Mesh(geo, mat || C.cable)); };
  const lerp3 = (a, b, t) => a.clone().lerp(b, t);
  /* a bundle: many cables braided round one path, some peeling off into loose tendrils that curl at the tip */
  const bundle = (path, n, rad, opt) => { opt = opt || {}; const cv = new TH.CatmullRomCurve3(path), fr = cv.computeFrenetFrames(24, false);
    for (let c = 0; c < n; c++) { const a0 = r() * TAU, tw = (r() - .5) * 5, rr = rad * (.35 + r() * .65), t0 = (opt.t0 || 0) + r() * .08, t1 = (opt.t1 || 1) - r() * .12, pts = [];
      for (let i = 0; i <= 10; i++) { const t = t0 + (t1 - t0) * i / 10, k = Math.round(t * 24), a = a0 + tw * t, R = rr * (opt.taper ? 1 - t * opt.taper : 1); pts.push(cv.getPointAt(Math.min(1, t)).addScaledVector(fr.normals[k], Math.cos(a) * R).addScaledVector(fr.binormals[k], Math.sin(a) * R)); }
      if (opt.loose && r() < opt.loose) { const e = pts[pts.length - 1], d = cv.getTangentAt(Math.min(1, t1)).clone().add(V((r() - .5) * 1.2, r() * 1.1 + (opt.up || 0), (r() - .5) * 1.4)).normalize(), L = (opt.len || 1.6) * (.6 + r() * .8), side = V(r() - .5, r() - .5, r() - .5).normalize();
        for (let i = 1; i <= 4; i++) pts.push(e.clone().addScaledVector(d, L * i / 4).addScaledVector(side, L * .28 * Math.pow(i / 4, 2.2) * (i === 4 ? 2 : 1))); }
      tube(pts, opt.r0 || .12, opt.r1 || .05, c % 7 === 3 ? C.cableL : C.cable, 0, 1.6); } };
  const cone = (len, rad, mat, from, dir, bend) => { const geo = new TH.ConeGeometry(rad, len, 8, 4); geo.translate(0, len / 2, 0); if (bend) { const P = geo.attributes.position; for (let i = 0; i < P.count; i++) { const y = P.getY(i) / len; P.setZ(i, P.getZ(i) + bend * y * y * len); } geo.computeVertexNormals(); }
    const m = add(new TH.Mesh(geo, mat)); m.position.copy(from); m.quaternion.setFromUnitVectors(V(0, 1, 0), dir.clone().normalize()); return m; };
  const orb = (rad, mat, p, seg) => add(new TH.Mesh(new TH.SphereGeometry(rad, seg || 20, Math.round((seg || 20) * .7)), mat), p.x, p.y, p.z);
  /* the head: a long fanged skull, its jaw dropped open on a glowing throat, eyes burning cyan, cables over the crown */
  const head = (at, s, gape) => { const H = new TH.Group(); g.add(H); H.position.copy(at); H.scale.setScalar(s); const hadd = m => { g.remove(m); H.add(m); return m; };
    const skull = new TH.LatheGeometry([[-.3, .02], [-.22, .42], [.05, .56], [.4, .5], [.75, .38], [1.1, .26], [1.38, .15], [1.5, .03]].map(([x, rr]) => new TH.Vector2(rr, x)), 22); skull.rotateZ(-Math.PI / 2); const sk = hadd(add(new TH.Mesh(skull, C.shell))); sk.scale.set(1, .74, 1.1); sk.position.y = .12;
    for (const sd of [1, -1]) { const br = hadd(cone(.75, .12, C.shell, V(.75, .4, sd * .22), V(-1, .55, sd * .35), .25)); const ch = hadd(cone(.55, .1, C.shell, V(.55, -.02, sd * .36), V(-1, -.1, sd * .6), .15)); }
    for (let i = 0; i < 5; i++) hadd(cone(.5 + i * .08, .07, C.claw, V(.1 - i * .12, .48 - i * .04, (i - 2) * .1), V(-1, .7, (i - 2) * .25), .3)); /* a crest of hooked spines */
    const jawG = new TH.LatheGeometry([[-.05, .02], [.15, .3], [.6, .3], [1.05, .16], [1.3, .03]].map(([x, rr]) => new TH.Vector2(rr, x)), 14); jawG.rotateZ(-Math.PI / 2); const jaw = hadd(add(new TH.Mesh(jawG, C.shell))); jaw.scale.set(1, .5, 1.05); jaw.position.set(-.05, -.16, 0); jaw.rotation.z = -(gape || .55);
    const throat = hadd(add(new TH.Mesh(new TH.SphereGeometry(.34, 16, 12), C.mouth))); throat.position.set(.55, -.12, 0); throat.scale.set(1.7, .75, .85);
    for (const sd of [1, -1]) { for (let i = 0; i < 6; i++) { const x = .35 + i * .17, t = hadd(cone(.16 + (i === 4 ? .14 : 0) + r() * .05, .035, C.bone, V(x, -.06, sd * (.32 - i * .045)), V(0, -1, 0), .2)); }
      for (let i = 0; i < 5; i++) { const a = -(gape || .55), x = .3 + i * .18, px = x * Math.cos(a), py = -.18 + x * Math.sin(a), t = hadd(cone(.18 + (i === 0 ? .16 : 0) + r() * .06, .04, C.bone, V(px, py, sd * (.26 - i * .04)), V(Math.sin(-a) * .3, 1, 0), -.15)); }
      const eye = hadd(orb(.075, C.glow, V(.82, .3, sd * .26), 10)); eye.scale.set(1.5, .7, .8); const eg = hadd(orb(.17, C.glowS, V(.84, .3, sd * .27), 10)); eg.scale.set(1.6, .8, .8);
      for (let i = 0; i < 3; i++) hadd(tube([V(1.1, .2, sd * .1 * i), V(.6, .44, sd * (.1 + .08 * i)), V(0, .5, sd * (.12 + .06 * i)), V(-.6, .42 + r() * .3, sd * (.1 + .1 * i)), V(-1.2, .6 + r() * .6, sd * (.2 + .2 * i))], .09, .035, C.cable)); }
    return H; };
  /* a limb: a cable bundle from the shoulder to the ground, splaying into hooked claws */
  const limb = (sh, foot, n, rad, clawL) => { const knee = lerp3(sh, foot, .45).add(V(.35, .25, 0)); tube([sh, knee, foot], rad * .7, rad * .4, C.shell, 3); bundle([sh, knee, foot], n, rad, { r0: .15, r1: .1 });
    for (let i = 0; i < 4; i++) { const a = (i - 1.5) * .42, d = V(Math.cos(a), -.15, Math.sin(a) * (foot.z > 0 ? 1 : 1)); cone(clawL * (.8 + r() * .4), .05 * clawL / .5, C.claw, foot.clone().add(V(0, -.05, 0)), d, -.25); } };
  /* the neural glow inside the body, seen between the cables */
  const cores = (pts, s) => { for (const p of pts) { orb(.22 * s, C.core, p, 16); orb(.5 * s, C.glowS, p, 12); } };
  if (cls === "mnest") { /* the hive (the third painting): a root mat of cables, curved black spires closing round a floating neural
       orb in thin holo rings, and a clutch of violet-lit eggs at its foot */
    for (let i = 0; i < 14; i++) { const a = i / 14 * TAU + r() * .3, R = 2.6 + r() * 1.3; tube([V(Math.cos(a) * .4, -1.2, Math.sin(a) * .4), V(Math.cos(a) * 1.4, -1.45, Math.sin(a) * 1.4), V(Math.cos(a + .2) * R, -1.6 + r() * .2, Math.sin(a + .2) * R), V(Math.cos(a + .35) * (R + 1), -1.4, Math.sin(a + .35) * (R + 1))], .24, .07); }
    for (let i = 0; i < 7; i++) { const a = i / 7 * TAU + .2, R = 1.5 + (i % 2) * .4, H = 3.1 + (i % 3) * .7, b = V(Math.cos(a) * R, -1.3, Math.sin(a) * R), tip = V(Math.cos(a) * .55, -1.3 + H, Math.sin(a) * .55), mid = lerp3(b, tip, .5).add(V(Math.cos(a) * .7, 0, Math.sin(a) * .7));
      tube([b, lerp3(b, mid, .5).add(V(Math.cos(a) * .2, 0, Math.sin(a) * .2)), mid, tip], .36, .02, C.shell, 6, .8); bundle([b, mid, tip], 3, .32, { t1: .7, r0: .06, r1: .03 }); }
    const cp = V(0, 1.15, 0); orb(.72, C.sac, cp, 28); orb(1.25, C.glowS, cp, 16);
    for (const [rr, tx, tz] of [[1.25, 1.35, .2], [1.55, 1.45, -.3], [1.0, .4, 1.2]]) { const t = add(new TH.Mesh(new TH.TorusGeometry(rr, .018, 6, 64), C.holo), 0, 1.15, 0); t.rotation.set(tx, 0, tz); }
    const pl = add(new TH.Mesh(new TH.CylinderGeometry(1.4, .9, .9, 6, 1, true), C.holo), 0, -.55, 0); pl.material = C.holo;
    for (let i = 0; i < 9; i++) { const a = 2.1 + i * .5 + r() * .3, R = 1.9 + r() * .7; const e = orb(.3 + r() * .14, C.egg, V(Math.cos(a) * R, -1.15 + r() * .15, Math.sin(a) * R), 14); e.scale.y = 1.25; }
    bundle([V(0, -1.4, 0), V(0, -.6, 0), V(0, .2, 0)], 10, .35, { r0: .07, r1: .04 });
    g.userData.mimR = 3.6; return g; }
  /* the creatures: one recipe, sized and shaped by class */
  const D = MIM_D[cls] || {};
  const L = D.len, spine = [V(-2.6 * L, .35, 0), V(-1.6 * L, .55 + D.hump * .5, 0), V(-.4 * L, .72 + D.hump, 0), V(.8 * L, .9 + D.hump * .8, 0), V(1.75 * L, .8, 0)];
  if (D.sac) { /* the Harvester: a great glowing biomass sac slung in a cradle of cables, grasping tendrils hanging under it */
    const sp = V(-.4, .45, 0), sac = orb(1.25, C.sac, sp, 32); sac.scale.set(1.25, 1, 1); orb(1.8, C.glowS, sp, 16);
    for (let i = 0; i < 16; i++) { const a = i / 16 * TAU, w = (r() - .5) * .5; tube([V(1.4, .7, 0), V(.7, .5 + Math.sin(a) * 1.25, Math.cos(a) * 1.25), V(-.4 + w, .45 + Math.sin(a) * 1.3, Math.cos(a) * 1.35), V(-1.5, .45 + Math.sin(a) * 1.15, Math.cos(a) * 1.1), V(-2.3, .6 + Math.sin(a) * .3, Math.cos(a) * .3)], .13, .09); }
    for (let i = 0; i < 12; i++) { const x = -1.6 + r() * 2.6, z = (r() - .5) * 1.6, L2 = 1.6 + r() * 1.4; tube([V(x, -.4, z), V(x + .1, -.4 - L2 * .4, z * 1.1), V(x + .35, -.4 - L2 * .8, z * 1.2 + (r() - .5) * .4), V(x + .7, -.4 - L2 * .9, z * 1.25)], .07, .02, C.cable, 0, 1.4); cone(.3, .05, C.claw, V(x + .7, -.4 - L2 * .9, z * 1.25), V(1, -.4, 0), -.2); }
    bundle([V(.9, .65, 0), V(1.5, .7, 0), V(2, .62, 0)], 8, .2, { r0: .07, r1: .05 }); head(V(2.0, .55, 0), .75, D.gape); }
  else {
    tube(spine, .7, .55, C.shell, 3); /* the dark mass under the cables, so the gaps show shadow and glow, not space */
    bundle(spine, 38 + (D.mane >> 1), .72 * D.s, { loose: .4, len: 1.6 * D.s, up: .6, r0: .2, r1: .11 });
    bundle(spine.slice(1).reverse().concat([V(2.2 * L, .6, 0)]), 8, .3, { t1: .9, r0: .07, r1: .05 });
    for (let i = 0; i < D.mane; i++) { const t = .15 + r() * .75, base = new TH.CatmullRomCurve3(spine).getPointAt(t).add(V(0, .35 + r() * .2, (r() - .5) * .7)), d = V(-.6 - r() * .6, .6 + r() * .9, (r() - .5) * 1.6).normalize(), Ln = (1.4 + r() * 1.8) * D.s, side = V(r() - .5, 0, r() - .5).normalize();
      tube([base, base.clone().addScaledVector(d, Ln * .35), base.clone().addScaledVector(d, Ln * .7).addScaledVector(side, Ln * .15), base.clone().addScaledVector(d, Ln * .9).addScaledVector(side, Ln * .4).add(V(0, -Ln * .05, 0)), base.clone().addScaledVector(d, Ln * .8).addScaledVector(side, Ln * .55).add(V(0, -Ln * .25, 0))], .16, .03, i % 6 === 2 ? C.cableL : C.cable, 0, 1.3); }
    for (let i = 0; i < D.tail; i++) { const z = (r() - .5) * .6, y = (r() - .5) * .5, Lt = 1.6 + r() * 2.2 * (D.tail > 10 ? 1.4 : 1); tube([V(-2.4 * L, .45 + y, z), V(-2.4 * L - Lt * .4, .4 + y * 2, z * 2), V(-2.4 * L - Lt * .75, .55 + y * 3 + (r() - .5) * .6, z * 3.2), V(-2.4 * L - Lt, .9 + y * 3 + r() * .5, z * 3.6 + (r() - .5))], .15, .02, C.cable, 0, 1.2); }
    cores([V(-.9 * L, .65 + D.hump * .7, .12), V(.3 * L, .72 + D.hump * .8, -.1), V(1.1 * L, .72, .1)], D.s);
    if (D.legs) { const sh = [V(1.1 * L, .45, .35), V(1.1 * L, .45, -.35), V(-1.6 * L, .45, .35), V(-1.6 * L, .45, -.35)].slice(0, D.legs), ft = [V(1.9 * L, -1.45, 1.0), V(1.9 * L, -1.45, -1.0), V(-1.3 * L, -1.45, 1.05), V(-1.3 * L, -1.45, -1.05)];
      sh.forEach((p, i) => limb(p, ft[i], i < 2 ? 10 : 8, i < 2 ? .36 : .28, i < 2 ? (D.armour ? 1.1 : .8) : .55)); }
    if (D.legs === 2) for (let i = 0; i < 10; i++) { const z = (r() - .5) * .8; tube([V(-1.2 * L, .3, z), V(-1.4 * L, -.4, z * 1.4), V(-1.9 * L, -.9 - r() * .3, z * 2), V(-2.4 * L, -1 - r() * .4, z * 2.4)], .06, .015, C.cable, 0, 1.3); }
    head(V(1.85 * L, .78, 0), 1.9, D.gape);
    if (D.armour) /* the Guardian: overlapping dark carapace plates down its back, and a pair of great crushing claws */
      for (let i = 0; i < 6; i++) { const x = 1.3 - i * .7, p = add(new TH.Mesh(new TH.SphereGeometry(.85, 18, 10, 0, TAU, 0, Math.PI * .42), C.shell), x * L, .95 + D.hump * (1 - Math.abs(x) * .3), 0); p.scale.set(.8, .55, 1.05); p.rotation.z = .2; }
    if (D.plates) /* the Assimilator: torn starship plating fused into its body, running lights still lit, and a wrecked hull in its tendrils */
      for (let i = 0; i < 7; i++) { const b = add(new TH.Mesh(new TH.BoxGeometry(.5 + r() * .5, .08, .3 + r() * .3), C.plate), (-1.8 + i * .55) * L, .9 + r() * .4, (r() - .5) * .8); b.rotation.set((r() - .5) * 1.2, r() * 3, (r() - .5) * .8);
        const l = add(new TH.Mesh(new TH.BoxGeometry(.08, .03, .08), C.plateL)); l.position.copy(b.position).add(V(0, .06, 0)); }
    if (D.brood) /* the Brood Titan: violet brood sacs swelling along its flanks */
      for (let i = 0; i < 8; i++) { const sd = i % 2 ? 1 : -1, e = orb(.26 + r() * .12, C.egg, V((-1.8 + (i >> 1) * .8) * L, .35 + r() * .3, sd * (.55 + r() * .15)), 14); e.scale.y = 1.2; }
  }
  g.scale.setScalar(D.s || 1); return g; }
/* v663 how they move (vertex motion in model units, baked into battle frames and run live on the map). A trot: the diagonal legs step
   together, each foot swinging forward lifted and planting back on the ground, the claws riding with it; the body bobs twice a stride and
   snakes a little; the head nods and the jaw works; tendrils, mane and tail ripple outward from the body, later the further out they reach */
function mimWave(k) { const D = MIM_D[k], f = v => (+v).toFixed(4), W1 = "2.0944", W2 = "4.18879";
  if (k === "mnest") return `vec3 p = position; float an = atan(p.z, p.x), sp = smoothstep(-1.1, 2.6, p.y) * step(.35, length(p.xz));
    transformed.x += sp * .1 * sin(mt * ${W1} + an * 2.); transformed.z += sp * .1 * cos(mt * ${W1} + an * 2.);
    float rt = smoothstep(1.3, 2.4, length(p.xz)) * step(p.y, -1.05); transformed.y += rt * .14 * sin(mt * ${W2} - length(p.xz) * 2.2 + an);
    float ob = 1. - smoothstep(1.3, 1.8, length(p - vec3(0., 1.15, 0.))); transformed.y += ob * .14 * sin(mt * ${W1}); transformed.xz *= 1. + ob * .03 * sin(mt * ${W2});`;
  const L = D.len, mid = f(-.25 * L), hx = f(1.85 * L), cy = f(.82 + D.hump * .6), tl = f(-2.35 * L), te = f(-4.3 * L);
  let w = `vec3 p = position; float ph = mt * ${W2};`;
  if (D.sac) w += ` float lw = smoothstep(-.35, -2.4, p.y); transformed.x += lw * .32 * sin(ph + p.z * 2.1 + p.x); transformed.z += lw * .2 * sin(mt * ${W1} + p.x * 1.7);
    vec3 sc = p - vec3(-.4, .45, 0.); float sw = 1. - smoothstep(1.3, 1.6, length(sc)); transformed += sc * sw * .05 * sin(mt * ${W1}); transformed.y += (1. - lw) * .1 * sin(mt * ${W1});`;
  else w += ` float lw = clamp((-.1 - p.y) / 1.35, 0., 1.)${D.legs === 2 ? ` * step(${mid}, p.x)` : ""}, lp = ph + (p.x > ${mid} ? 0. : 3.14159) + (p.z > 0. ? 0. : 3.14159);
    transformed.x += lw * .48 * sin(lp); transformed.y += lw * lw * .34 * max(0., cos(lp)); transformed.z += lw * .05 * sin(lp) * sign(p.z);
    float bw = 1. - lw; transformed.y += bw * .06 * sin(ph * 2. + .6); transformed.z += bw * .06 * sin(ph + p.x * .7);`;
  w += ` float hw = smoothstep(${f(1.25 * L)}, ${f(1.95 * L)}, p.x) * (1. - lw); transformed.y += hw * .09 * sin(ph + 1.2); transformed.z += hw * .06 * sin(mt * ${W1});
    float jw = smoothstep(${hx}, ${f(1.85 * L + .5)}, p.x) * step(p.y, ${f(.6 + (D.sac ? -.1 : 0))}) * (1. - lw); transformed.y -= jw * (p.x - ${hx}) * (.1 + .12 * sin(mt * ${W1} * 2.));
    float dd = length(vec2(p.y - ${cy}, p.z)), tw = max(smoothstep(1.0, 2.5, dd) * step(-.05, p.y), smoothstep(${tl}, ${te}, p.x)) * (1. - lw) * (1. - hw);
    transformed.z += tw * .3 * sin(mt * ${W1} - dd * 1.6 + p.x * .6); transformed.y += tw * .2 * sin(mt * ${W2} - dd * 1.3 + p.z * 1.2); transformed.x += tw * .12 * sin(mt * ${W1} - dd);`;
  return w; }
for (const k in MIM_U) MON_WAVE[k] = mimWave(k);
MON_WAVE.mimic = mimWave("mnest");
