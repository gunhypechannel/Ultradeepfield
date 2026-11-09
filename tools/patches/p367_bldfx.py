# v367: base buildings come alive. Building models get rows of lit windows on their walls (painted into the glow map from glbLights, on UV
# islands so nothing bleeds; each building has its own window tint), and each one gets a signature animation of its own (bldUniq):
# crystals orbiting the Crystal Mine, a rotating sweep over the Radar, a hologram atom over the Lab, a plasma core and ring on the Fusion
# Plant, a breathing shield dome on the Fortress, a sky beam on the Geo-Former, a small moon round the Lunar Outpost, drones circling Drone
# Works, a cargo lifter on the Metal Silo, pressure rings climbing the Gas Tank, a scanning fan on the Phalanx, and more. Slower Android
# phones (WEAK) keep the light hand-built buildings as before.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)

# 1) windows on building walls, painted into the glow map
rep("    x.putImageData(id, 0, 0);\n", r'''    try { glbWin(k, mesh, D, A); } catch (e) {} // v367 lit windows
    x.putImageData(id, 0, 0);
''')
rep("const BLD_FX = {", r'''/* v367 each building's window light (r,g,b) */
const BLD_WIN = { metalMine: "255,196,120", crystalMine: "150,220,255", gasSynth: "150,255,190", solar: "255,226,150", metalStore: "255,210,150", crystalStore: "150,215,255",
  gasTank: "160,255,200", robotics: "255,200,140", shipyard: "255,214,160", lab: "170,205,255", radar: "160,255,210", fusion: "255,170,110", repairYard: "255,200,130",
  nanite: "205,170,255", fortress: "150,200,255", terraformer: "170,255,170", allyDepot: "255,220,160", lunarBase: "220,230,255", phalanx: "255,140,120" };
/* v367 rows of lit windows on a building model's walls: horizontal runs on near-vertical faces, each kept on its own UV island */
function glbWin(k, mesh, D, A) {
  const g = mesh.geometry, P = g.attributes.position, U = g.attributes.uv, I = g.index; if (!P || !U) return;
  const WC = (BLD_WIN[k] || "255,210,150").split(",").map(v => +v / 255), core = WC.map(v => 255 * (.5 + .5 * v)), halo = WC.map(v => 255 * v);
  const nT = I ? I.count / 3 : P.count / 3, vi = j => I ? I.getX(j) : j, par = new Int32Array(P.count); for (let i = 0; i < P.count; i++) par[i] = i;
  const fd = a => { while (par[a] !== a) a = par[a] = par[par[a]]; return a; };
  for (let t = 0; t < nT; t++) { const a = fd(vi(t * 3)), b = fd(vi(t * 3 + 1)); par[b] = a; const c = fd(vi(t * 3 + 2)); par[c] = fd(a); }
  const isl = new Int32Array(A * A).fill(-1), bb = new TH.Box3().setFromBufferAttribute(P), size = Math.max(bb.max.x - bb.min.x, bb.max.z - bb.min.z, .001), hgt = bb.max.y - bb.min.y, tri = []; let tot = 0;
  for (let t = 0; t < nT; t++) { const ia = vi(t * 3), ib = vi(t * 3 + 1), ic = vi(t * 3 + 2), id = fd(ia);
    const u0 = U.getX(ia) * A, v0 = U.getY(ia) * A, u1 = U.getX(ib) * A, v1 = U.getY(ib) * A, u2 = U.getX(ic) * A, v2 = U.getY(ic) * A, den = (v1 - v2) * (u0 - u2) + (u2 - u1) * (v0 - v2); if (Math.abs(den) < 1e-9) continue;
    const x0 = Math.max(0, Math.floor(Math.min(u0, u1, u2))), x1 = Math.min(A - 1, Math.ceil(Math.max(u0, u1, u2))), y0 = Math.max(0, Math.floor(Math.min(v0, v1, v2))), y1 = Math.min(A - 1, Math.ceil(Math.max(v0, v1, v2)));
    for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) { const px = x + .5, py = y + .5, l0 = ((v1 - v2) * (px - u2) + (u2 - u1) * (py - v2)) / den, l1 = ((v2 - v0) * (px - u2) + (u0 - u2) * (py - v2)) / den; if (l0 >= -.02 && l1 >= -.02 && l0 + l1 <= 1.02) isl[y * A + x] = id; }
    const ax = P.getX(ia), ay = P.getY(ia), az = P.getZ(ia), e1 = [P.getX(ib) - ax, P.getY(ib) - ay, P.getZ(ib) - az], e2 = [P.getX(ic) - ax, P.getY(ic) - ay, P.getZ(ic) - az];
    const n = [e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0]], ar = Math.hypot(n[0], n[1], n[2]); if (ar < 1e-12) continue; n[0] /= ar; n[1] /= ar; n[2] /= ar;
    const cy = ay + (e1[1] + e2[1]) / 3; if (Math.abs(n[1]) > .45 || cy - bb.min.y < hgt * .1 || cy > bb.max.y - hgt * .05) continue;
    tri.push([ar / 2, id, e1, e2, n, u0, v0, u1 - u0, v1 - v0, u2 - u0, v2 - v0]); tot += ar / 2; }
  const rows = MOBILE ? 70 : 110, pitch = size * .032, rr = rnd(hash(k + "bwin"));
  for (let r0 = 0; r0 < rows && tot > 0; r0++) { let pick = rr() * tot, T = null; for (const q of tri) { pick -= q[0]; if (pick <= 0) { T = q; break; } } if (!T) T = tri[tri.length - 1];
    const [, id, e1, e2, n, u0, v0, du1, dv1, du2, dv2] = T;
    let d = [n[2], 0, -n[0]], dl = Math.hypot(d[0], d[2]); if (dl < .3) continue; d = [d[0] / dl, 0, d[2] / dl]; const hv = [n[1] * d[2] - n[2] * d[1], n[2] * d[0] - n[0] * d[2], n[0] * d[1] - n[1] * d[0]];
    const g11 = e1[0] * e1[0] + e1[1] * e1[1] + e1[2] * e1[2], g12 = e1[0] * e2[0] + e1[1] * e2[1] + e1[2] * e2[2], g22 = e2[0] * e2[0] + e2[1] * e2[1] + e2[2] * e2[2], gd = g11 * g22 - g12 * g12; if (Math.abs(gd) < 1e-18) continue;
    const uvOf = w => { const p1 = w[0] * e1[0] + w[1] * e1[1] + w[2] * e1[2], p2 = w[0] * e2[0] + w[1] * e2[1] + w[2] * e2[2], a = (g22 * p1 - g12 * p2) / gd, b = (g11 * p2 - g12 * p1) / gd; return [a * du1 + b * du2, a * dv1 + b * dv2]; };
    const Ju = uvOf(d), Jv = uvOf(hv), jd = Ju[0] * Jv[1] - Ju[1] * Jv[0]; if (Math.abs(jd) < 1e-9) continue; const ppu = Math.hypot(Ju[0], Ju[1]); if (ppu * pitch < 1.4 || ppu * pitch > A * .06) continue;
    let a0 = rr(), b0 = rr(); if (a0 + b0 > 1) { a0 = 1 - a0; b0 = 1 - b0; } const c0u = u0 + a0 * du1 + b0 * du2, c0v = v0 + a0 * dv1 + b0 * dv2;
    const ww = pitch * .55, wh = pitch * .75, hr = pitch * 1.2, nWin = 2 + Math.floor(rr() * 7), st = Math.floor(-nWin / 2), lit = .7 + rr() * .5;
    for (let wi = st; wi < st + nWin; wi++) { if (rr() < .15) continue; const cu = c0u + Ju[0] * pitch * wi, cv = c0v + Ju[1] * pitch * wi; if (cu < 0 || cv < 0 || cu >= A || cv >= A || isl[Math.floor(cv) * A + Math.floor(cu)] !== id) continue;
      const R2 = Math.ceil(hr * Math.max(ppu, Math.hypot(Jv[0], Jv[1]))) + 1;
      for (let y = Math.max(0, Math.floor(cv - R2)); y <= Math.min(A - 1, Math.ceil(cv + R2)); y++) for (let x = Math.max(0, Math.floor(cu - R2)); x <= Math.min(A - 1, Math.ceil(cu + R2)); x++) {
        const pi = y * A + x; if (isl[pi] !== id) continue; const ox = x + .5 - cu, oy = y + .5 - cv, wu = (ox * Jv[1] - oy * Jv[0]) / jd, wv = (Ju[0] * oy - Ju[1] * ox) / jd, o = pi * 4; let f = 0, hh = 0;
        if (Math.abs(wu) < ww / 2 && Math.abs(wv) < wh / 2) f = 1.1 * lit; const dd = Math.hypot(wu / hr, wv / (hr * .8)); if (dd < 1) hh = Math.pow(1 - dd, 2) * .45 * lit;
        if (f || hh) { D[o] = Math.min(255, D[o] + core[0] * f + halo[0] * hh); D[o + 1] = Math.min(255, D[o + 1] + core[1] * f + halo[1] * hh); D[o + 2] = Math.min(255, D[o + 2] + core[2] * f + halo[2] * hh); } } } }
}
/* v367 each building's signature animation, placed round the model: H its height, R its half width */
function bldUniq(k, b, anim, H, R) {
  const add = (o, kind, ph, u) => { if (u) Object.assign(o.userData, u); b.add(o); anim.push([o, kind, ph || 0]); return o; };
  const glow = (c, sc, op) => { const o = new TH.Sprite(new TH.SpriteMaterial({ map: glowTex(c, 1), transparent: true, opacity: op == null ? .9 : op, blending: TH.AdditiveBlending, depthWrite: false })); o.scale.setScalar(sc); o.userData.s0 = sc; o.userData.op = o.material.opacity; return o; };
  const neon = (c, op) => new TH.MeshBasicMaterial({ color: new TH.Color(`rgb(${c})`), transparent: true, opacity: op == null ? .8 : op, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false });
  const orbit = (o, r, y, w, ph, tilt) => add(o, "orbitF", ph, { r, y0: y, w, tilt: tilt || 0 });
  const rise = (c, n, r, y0, hh, sc) => { for (let i = 0; i < n; i++) { const o = glow(c, sc, .8); const a = i * 2.4; o.position.set(Math.cos(a) * r * (.4 + (i % 3) * .2), y0, Math.sin(a) * r * (.4 + (i % 3) * .2)); add(o, "riseL", i / n, { y0, h: hh }); } };
  switch (k) {
    case "metalMine": { const o = glow("255,150,60", R * .7, .85); o.position.set(R * .3, H * .35, R * .3); add(o, "pulseO", 0); rise("255,170,90", 6, R * .5, H * .4, H * .7, R * .09); break; } // molten ore and sparks
    case "crystalMine": for (let i = 0; i < 3; i++) { const c = new TH.Mesh(new TH.OctahedronGeometry(R * .12, 0), neon("140,220,255", .85)); c.scale.y = 1.8; orbit(c, R * .55, H + R * .25, .9, i * 2.09, R * .08); c.add(glow("140,220,255", R * .45, .5)); } break; // floating crystals
    case "gasSynth": { const o = glow("120,255,170", R * .8, .9); o.position.y = H + R * .1; add(o, "pulseO", 0); rise("140,255,180", 7, R * .45, H * .6, H * .9, R * .08); break; }
    case "solar": { const o = glow("255,236,170", R * .6, .9); orbit(o, R * .6, H * .8, .35, 0, R * .1); const h2 = glow("255,220,140", R * 1.6, .25); h2.position.y = H * .6; add(h2, "pulseO", 1.3); break; } // a sun-tracking glint
    case "metalStore": { const d = new TH.Group(); d.add(new TH.Mesh(new TH.BoxGeometry(R * .32, R * .18, R * .32), new TH.MeshStandardMaterial({ color: 0x9aa4ae, metalness: .9, roughness: .3 }))); const l = glow("255,80,60", R * .22, .95); l.position.y = R * .14; d.add(l); d.position.set(R * .95, 0, 0); add(d, "lift", 0, { y0: R * .2, h: H * .9 }); break; } // a cargo lifter
    case "crystalStore": { const t = new TH.Mesh(new TH.TorusGeometry(R * .55, R * .025, 6, 48), neon("80,170,255", .42)); t.rotation.x = Math.PI / 2; const g = new TH.Group(); g.add(t); g.position.y = H + R * .2; add(g, "spin", 1.4); const t2 = t.clone(); t2.scale.setScalar(.7); t2.rotation.x = Math.PI / 2 + .5; g.add(t2); break; } // hologram rings
    case "gasTank": for (let i = 0; i < 3; i++) { const t = new TH.Mesh(new TH.TorusGeometry(R * .78, R * .03, 6, 48), neon("70,255,150", .42)); t.rotation.x = Math.PI / 2; add(t, "ringRise", i / 3, { y0: H * .08, h: H * .85, op: .42 }); } break; // pressure rings
    case "robotics": for (let i = 0; i < 2; i++) { const d = new TH.Group(); d.add(new TH.Mesh(new TH.SphereGeometry(R * .08, 10, 8), new TH.MeshStandardMaterial({ color: 0xc8d0d8, metalness: .9, roughness: .25 }))); d.add(glow(i ? "255,190,90" : "120,220,255", R * .3, .9)); orbit(d, R * .95, H * .65 + i * R * .2, i ? -.8 : .6, i * 3.1, R * .12); } break; // drones circling
    case "shipyard": { const s = new TH.Mesh(new TH.PlaneGeometry(R * 1.6, H * .9), neon("120,220,255", .22)); s.rotation.y = Math.PI / 2; s.position.y = H * .45; add(s, "slideS", R * .7); break; } // a scan beam sweeping the hull
    case "lab": { const g = new TH.Group(); g.position.y = H + R * .35; for (let i = 0; i < 3; i++) { const t = new TH.Mesh(new TH.TorusGeometry(R * .32, R * .015, 6, 40), neon("110,160,255", .5)); t.rotation.set(Math.PI / 2 + i * 1.05, i * .7, 0); g.add(t); const e = glow("190,220,255", R * .16, 1); e.position.set(R * .32, 0, 0); t.add(e); } g.add(glow("200,225,255", R * .4, .9)); add(g, "atom", 0); break; } // a hologram atom
    case "radar": { const f = new TH.Mesh(new TH.CircleGeometry(R * 1.6, 24, 0, .5), neon("120,255,190", .22)); f.rotation.x = -Math.PI / 2; const g = new TH.Group(); g.add(f); g.position.y = H * .55; add(g, "spin", 2.2); break; } // a rotating sweep
    case "fusion": { const c = glow("255,200,120", R * .9, 1); c.position.y = H * .6; add(c, "pulseO", 0); const t = new TH.Mesh(new TH.TorusGeometry(R * .5, R * .035, 6, 48), neon("255,140,60", .55)); t.position.y = H * .6; t.rotation.x = 1.2; add(t, "spinX", 2.5); break; } // the plasma core
    case "repairYard": { const d = new TH.Group(); d.add(new TH.Mesh(new TH.BoxGeometry(R * .2, R * .08, R * .2), new TH.MeshStandardMaterial({ color: 0xb8c0c8, metalness: .9, roughness: .3 }))); const w = glow("200,230,255", R * .3, 1); w.position.y = -R * .1; w.userData.s0 = R * .3; d.add(w); orbit(d, R * .7, H * .75, .5, 0, R * .15); add(w, "flick", 1.7); break; } // a repair drone
    case "nanite": { const n = MOBILE ? 14 : 22; for (let i = 0; i < n; i++) { const o = glow(i % 2 ? "205,170,255" : "150,200,255", R * .12, .9); orbit(o, R * (.35 + (i % 5) * .12), H * (.4 + (i % 4) * .15), (i % 2 ? 1 : -1) * (.8 + (i % 3) * .3), i * .9, R * .2); } break; } // a swarm
    case "fortress": { const d = new TH.Mesh(new TH.SphereGeometry(R * 1.15, 32, 16, 0, TAU, 0, Math.PI / 2), neon("120,190,255", .12)); add(d, "shieldF", 0, { op: .12 }); break; } // a shield dome
    case "terraformer": { const bm = new TH.Mesh(new TH.CylinderGeometry(R * .06, R * .16, 26, 10, 1, true), neon("150,255,150", .35)); bm.position.y = H + 13; add(bm, "beamF", 0, { op: .35 }); rise("170,255,170", 6, R * .2, H, 6, R * .1); break; } // a beam into the sky
    case "allyDepot": for (let i = 0; i < 2; i++) { const o = glow("255,210,120", R * .5, .9); orbit(o, R * .25, H + R * .1, 2.4, i * Math.PI, 0); } break; // a lighthouse beacon
    case "lunarBase": { const mo = new TH.Mesh(new TH.SphereGeometry(R * .2, 20, 14), new TH.MeshStandardMaterial({ color: 0xc8ccd2, roughness: .9, emissive: 0x202630 })); mo.add(glow("210,225,255", R * .7, .35)); orbit(mo, R * 1.1, H + R * .4, .25, 0, R * .25); break; } // a little moon
    case "phalanx": { const f = new TH.Mesh(new TH.PlaneGeometry(R * 2.2, R * .02), neon("255,90,80", .9)); f.position.set(0, H * .9, 0); add(f, "scanF", 0, { y0: H * .9 }); break; } // a scanning laser fan
  }
}
const BLD_FX = {''')
# 2) call it from glbBld
rep("    if (F.beacon && fx.peaks[0]) {", "    try { bldUniq(k, b, anim, sz.y * s, span / 2); } catch (e) {} // v367 the building's own animation\n    if (F.beacon && fx.peaks[0]) {")
# 3) the new animation kinds
rep('''    else if (kind === "through") {''', '''    else if (kind === "orbitF") { const u = o.userData, a = T * .001 * u.w + p; o.position.set(Math.cos(a) * u.r, u.y0 + Math.sin(a * 1.7) * u.tilt, Math.sin(a) * u.r); o.rotation.y = -a; } // v367 orbiting
    else if (kind === "pulseO") { const u = o.userData, w = .5 + .5 * Math.sin(T * .003 + p); o.material.opacity = (u.op || .9) * (.55 + .45 * w); if (u.s0) o.scale.setScalar(u.s0 * (.9 + .2 * w)); }
    else if (kind === "riseL") { const u = o.userData, q = (T * .00035 + p) % 1; o.position.y = u.y0 + q * u.h; o.material.opacity = .8 * Math.sin(Math.PI * q); }
    else if (kind === "lift") { const u = o.userData; o.position.y = u.y0 + (.5 - .5 * Math.cos(T * .0011 + p)) * u.h; }
    else if (kind === "ringRise") { const u = o.userData, q = (T * .00022 + p) % 1; o.position.y = u.y0 + q * u.h; o.material.opacity = u.op * Math.sin(Math.PI * q); }
    else if (kind === "atom") { o.rotation.y = T * .0012; o.children.forEach((c, i) => { if (c.geometry && c.geometry.type === "TorusGeometry") c.rotation.z = T * .002 * (i + 1); }); }
    else if (kind === "spinX") o.rotation.z = T * .001 * p;
    else if (kind === "shieldF") { const u = o.userData; o.material.opacity = u.op * (.55 + .45 * Math.sin(T * .0018)); o.rotation.y = T * .0002; }
    else if (kind === "beamF") { const u = o.userData; o.material.opacity = u.op * (.7 + .3 * Math.sin(T * .006)) * (.9 + .1 * Math.random()); }
    else if (kind === "scanF") { const u = o.userData; o.rotation.y = Math.sin(T * .0011) * 1.2; o.position.y = u.y0 * (.55 + .45 * (.5 + .5 * Math.sin(T * .0007))); }
    else if (kind === "through") {''')
open(p, "w").write(h); print("ok")
