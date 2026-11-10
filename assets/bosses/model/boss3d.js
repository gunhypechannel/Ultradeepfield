/* UDF bosses in 3D, built from the owner's reference art (assets/bosses/<boss>/reference/ref-2026-11-09.png):
   Energy Conduit, Void Warden, Pyramid Overlord, Orbital Devourer. Plated gunmetal with bronze trim and violet light slits,
   faceted violet crystal, living lightning, moving parts. Each build returns { grp, tick(t), r } with r = bounding radius. */
(function (root) {
  const TAU = Math.PI * 2;
  let TH = null; const cache = {};
  const rnd = (s => () => (s = (s * 16807) % 2147483647) / 2147483647)(9137);
  const VIO = 0xb45cff, VIO2 = 0xd9a0ff, CORE = 0xf3dcff;

  /* ---------- shared textures ---------- */
  function cv(w, h) { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; }
  function plateTex(key, opt = {}) { // panel plating: colour map + emissive map (violet slits) + roughness
    if (cache[key]) return cache[key]; const N = opt.n || 512, c = cv(N, N), e = cv(N, N), r = cv(N, N), x = c.getContext("2d"), y = e.getContext("2d"), z = r.getContext("2d");
    x.fillStyle = opt.base || "#44424b"; x.fillRect(0, 0, N, N); y.fillStyle = "#000"; y.fillRect(0, 0, N, N); z.fillStyle = "#6a6a6a"; z.fillRect(0, 0, N, N);
    const rows = opt.rows || 6; let yy = 0;
    for (let i = 0; i < rows; i++) { const hh = N / rows; let xx = 0;
      while (xx < N) { const ww = (opt.cols ? N / opt.cols : 28 + rnd() * 70); const sh = 56 + rnd() * 34 | 0, bz = rnd() < (opt.bronze ?? .14) * .6;
        x.fillStyle = bz ? `rgb(${118 + rnd() * 22 | 0},${96 + rnd() * 16 | 0},${70 + rnd() * 12 | 0})` : `rgb(${sh},${sh},${sh + 5})`; x.fillRect(xx + 1, yy + 1, ww - 2, hh - 2);
        z.fillStyle = bz ? "#4a4a4a" : `rgb(${90 + rnd() * 60 | 0},0,0)`.replace(/rgb\((\d+),0,0\)/, (m, v) => `rgb(${v},${v},${v})`); z.fillRect(xx + 1, yy + 1, ww - 2, hh - 2);
        x.fillStyle = "rgba(255,255,255,.08)"; x.fillRect(xx + 1, yy + 1, ww - 2, 2); x.fillStyle = "rgba(0,0,0,.35)"; x.fillRect(xx + 1, yy + hh - 3, ww - 2, 2);
        if (rnd() < (opt.slits ?? .3)) { const sw = ww * (.25 + rnd() * .45), sx = xx + (ww - sw) / 2, sy = yy + hh * (.35 + rnd() * .3), sl = Math.max(2, hh * .07);
          x.fillStyle = "#d8b8ff"; x.fillRect(sx, sy, sw, sl); y.fillStyle = "#c066ff"; y.fillRect(sx, sy, sw, sl); y.fillStyle = "rgba(170,70,255,.35)"; y.fillRect(sx - 3, sy - 3, sw + 6, sl + 6); }
        if (rnd() < .25) { x.fillStyle = "rgba(20,16,30,.6)"; for (let k = 0; k < 3; k++) x.fillRect(xx + 6 + k * 9, yy + 6, 5, 5); }
        xx += ww; }
      x.fillStyle = "rgba(10,8,18,.9)"; x.fillRect(0, yy, N, 2); yy += N / rows; }
    // relief: panels raised, seams and light slits sunk; a Sobel pass turns it into a normal map
    { const hc = cv(N, N), hx = hc.getContext("2d"); hx.drawImage(c, 0, 0); const d = hx.getImageData(0, 0, N, N).data, H = new Float32Array(N * N);
      for (let i = 0; i < N * N; i++) H[i] = (d[i * 4] + d[i * 4 + 1] + d[i * 4 + 2]) / 765;
      const nc = cv(N, N), nx = nc.getContext("2d"), nd = nx.createImageData(N, N), s = opt.relief ?? 3.2;
      for (let yy2 = 0; yy2 < N; yy2++) for (let xx2 = 0; xx2 < N; xx2++) { const at = (a, b) => H[((b + N) % N) * N + ((a + N) % N)];
        const dx = (at(xx2 + 1, yy2) - at(xx2 - 1, yy2)) * s, dy = (at(xx2, yy2 + 1) - at(xx2, yy2 - 1)) * s, l = Math.hypot(dx, dy, 1), o = (yy2 * N + xx2) * 4;
        nd.data[o] = (-dx / l * .5 + .5) * 255; nd.data[o + 1] = (dy / l * .5 + .5) * 255; nd.data[o + 2] = (1 / l * .5 + .5) * 255; nd.data[o + 3] = 255; }
      nx.putImageData(nd, 0, 0); cache[key + "_n"] = nc; }
    if (opt.glyphs) { y.font = `bold ${N / rows * .55 | 0}px monospace`; x.font = y.font; const gl = "◇◈⌬⏃⏚⍜⎔⟁⊕⊗⋔⍟";
      for (let i = 0; i < 16; i++) { const g = gl[i % gl.length], gx = i * N / 16 + 6, gy = N / 2 + 6; y.fillStyle = "#e0a8ff"; y.fillText(g, gx, gy); x.fillStyle = "#e6ccff"; x.fillText(g, gx, gy); } }
    const T = [c, e, r, cache[key + "_n"]].map(k => { const t = new TH.CanvasTexture(k); t.wrapS = t.wrapT = TH.RepeatWrapping; t.anisotropy = 4; return t; }); T[0].encoding = TH.sRGBEncoding; T[1].encoding = TH.sRGBEncoding;
    return cache[key] = { map: T[0], emi: T[1], rough: T[2], nrm: T[3] }; }
  function radial(key, stops) { if (cache[key]) return cache[key]; const c = cv(128, 128), x = c.getContext("2d"), g = x.createRadialGradient(64, 64, 0, 64, 64, 64); stops.forEach(([o, col]) => g.addColorStop(o, col)); x.fillStyle = g; x.fillRect(0, 0, 128, 128); const t = new TH.CanvasTexture(c); return cache[key] = t; }
  function swirlTex() { if (cache.swirl) return cache.swirl; const N = 256, c = cv(N, N), x = c.getContext("2d"); x.fillStyle = "#000"; x.fillRect(0, 0, N, N); x.translate(N / 2, N / 2);
    for (let i = 0; i < 900; i++) { const a = rnd() * TAU, r0 = rnd() * N * .48, sp = .9 + rnd() * 1.4; x.strokeStyle = `rgba(${170 + rnd() * 80 | 0},${70 + rnd() * 90 | 0},255,${.05 + rnd() * .12})`; x.lineWidth = 1 + rnd() * 2.5; x.beginPath();
      for (let k = 0; k < 14; k++) { const rr = r0 * (1 - k * .045), aa = a + k * .09 * sp; const px = Math.cos(aa) * rr, py = Math.sin(aa) * rr; k ? x.lineTo(px, py) : x.moveTo(px, py); } x.stroke(); }
    const t = new TH.CanvasTexture(c); t.encoding = TH.sRGBEncoding; return cache.swirl = t; }

  /* ---------- shared materials and parts ---------- */
  function hullMat(key, opt = {}) { const P = plateTex(key, opt), m = new TH.MeshStandardMaterial({ map: P.map, roughnessMap: P.rough, normalMap: P.nrm, normalScale: new TH.Vector2(1.4, 1.4), metalness: opt.metal ?? .9, roughness: opt.rough ?? .32, emissive: 0xffffff, emissiveMap: P.emi, emissiveIntensity: opt.ei ?? 2.8, envMapIntensity: .9 });
    if (opt.rep) for (const t of [P.map, P.rough, P.emi, P.nrm]) { t.repeat.set(opt.rep[0], opt.rep[1]); } m.userData.P = P; rimOn(m, opt.rim ?? 1); return m; }
  // violet rim light baked into the shader: edges facing away from the camera glow, so the bosses read in any scene
  function rimOn(m, k) { m.customProgramCacheKey = () => "bossrim"; const prev = m.onBeforeCompile; m.onBeforeCompile = sh => { if (prev) prev(sh); sh.uniforms.uRim = { value: k }; m.userData.rim = sh.uniforms.uRim;
      sh.fragmentShader = "uniform float uRim;\n" + sh.fragmentShader.replace("#include <emissivemap_fragment>", "#include <emissivemap_fragment>\n float fr = pow(1. - clamp(abs(dot(normalize(vViewPosition), normal)), 0., 1.), 4.5);\n totalEmissiveRadiance += vec3(.62, .26, 1.) * fr * .45 * uRim;"); }; }
  const glowMat = (c = VIO, o = .9) => new TH.MeshBasicMaterial({ color: c, transparent: true, opacity: o, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false, side: TH.DoubleSide });
  function crystalMat() { const m = new TH.MeshStandardMaterial({ color: 0x4a10b0, emissive: 0x7020ff, emissiveIntensity: .55, metalness: .5, roughness: .18, flatShading: true, transparent: true, opacity: .96, envMapIntensity: .7 }); rimOn(m, .5); return m; }
  function sprite(sz, col = "rgba(200,120,255,1)", key = "g" + col) { const s = new TH.Sprite(new TH.SpriteMaterial({ map: radial(key, [[0, col], [.25, col.replace(/[\d.]+\)$/, ".45)")], [1, "rgba(120,40,255,0)"]]), blending: TH.AdditiveBlending, depthWrite: false, transparent: true, toneMapped: false })); s.scale.set(sz, sz, 1); return s; }
  // a thick plated band: a ring (or an arc) with a rectangular cross-section
  function band(R, w, h, mat, phi0 = 0, phiL = TAU, seg = 96, segs = 0) { const p = [new TH.Vector2(R - w / 2, -h / 2), new TH.Vector2(R + w / 2, -h / 2), new TH.Vector2(R + w / 2 + w * .12, -h * .2), new TH.Vector2(R + w / 2 + w * .12, h * .2), new TH.Vector2(R + w / 2, h / 2), new TH.Vector2(R - w / 2, h / 2), new TH.Vector2(R - w / 2, -h / 2)];
    const n = segs || Math.max(6, Math.round(phiL * R * 1.1)); if (n < 3) return new TH.Mesh(new TH.LatheGeometry(p, seg, phi0, phiL), mat);
    const g = new TH.Group(), gap = Math.min(.035, .3 / R), each = phiL / n, sub = Math.max(2, Math.round(seg / n));
    const geo = new TH.LatheGeometry(p, sub, 0, each - gap); for (let i = 0; i < n; i++) { const m = new TH.Mesh(geo, mat); m.rotation.y = phi0 + i * each; g.add(m); }
    // a raised armour cap on every second segment
    const cap = new TH.BoxGeometry(w * .55, h * .25, Math.min(1.2, each * R * .55)); for (let i = 0; i < n; i += 2) { const a = phi0 + (i + .5) * each, m = new TH.Mesh(cap, mat); m.position.set(Math.sin(a) * R, h * .55, Math.cos(a) * R); m.rotation.y = a; g.add(m); }
    return g; }
  function bandGlow(R, h, phi0 = 0, phiL = TAU, c = VIO2) { const g = new TH.Group(); g.add(new TH.Mesh(new TH.CylinderGeometry(R, R, h, 96, 1, true, phi0, phiL), glowMat(c, .95)));
    g.add(new TH.Mesh(new TH.CylinderGeometry(R, R, h * 2.0, 96, 1, true, phi0, phiL), glowMat(VIO, .1))); return g; }
  function crystal(prof, sides = 6) { return new TH.Mesh(new TH.LatheGeometry(prof.map(([r, y]) => new TH.Vector2(r, y)), sides), crystalMat()); }
  function shard(r, h, mat) { const g = new TH.ConeGeometry(r, h, 4); g.translate(0, h / 2, 0); return new TH.Mesh(g, mat); }
  // lightning: jagged lines between point pairs, re-struck several times a second
  function bolts(grp, n, pick, col = VIO2) { const L = []; for (let i = 0; i < n; i++) { const g = new TH.BufferGeometry(); g.setAttribute("position", new TH.Float32BufferAttribute(new Float32Array(14 * 3), 3));
      const m = new TH.LineBasicMaterial({ color: col, transparent: true, opacity: .9, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false }), l = new TH.Line(g, m); l.frustumCulled = false; l.userData.next = 0; grp.add(l); L.push(l); }
    return (t, rate = 1) => { for (const l of L) { if (t < l.userData.next) continue; l.userData.next = t + (60 + rnd() * 220) / rate; const [a, b] = pick(), p = l.geometry.attributes.position, d = a.distanceTo(b);
        for (let k = 0; k < 14; k++) { const f = k / 13, j = (k === 0 || k === 13) ? 0 : d * .09; p.setXYZ(k, a.x + (b.x - a.x) * f + (rnd() - .5) * j, a.y + (b.y - a.y) * f + (rnd() - .5) * j, a.z + (b.z - a.z) * f + (rnd() - .5) * j); }
        p.needsUpdate = true; l.material.opacity = rnd() < .25 ? 0 : .55 + rnd() * .45; } }; }
  const V = (x, y, z) => new TH.Vector3(x, y, z);
  function box(w, h, d, mat) { return new TH.Mesh(new TH.BoxGeometry(w, h, d), mat); }
  // a strut from a to b, with a square (4-sided) tapering section
  function strut(a, b, r0, r1, mat, sides = 4) { const d = b.clone().sub(a), L = d.length(), g = new TH.CylinderGeometry(r1, r0, L, sides); g.translate(0, L / 2, 0); g.rotateY(Math.PI / 4);
    const m = new TH.Mesh(g, mat); m.position.copy(a); m.quaternion.setFromUnitVectors(V(0, 1, 0), d.normalize()); return m; }
  // a tapered armour beam with a flattened (w x t) section
  function beam(a, b, w0, w1, th, mat) { const d = b.clone().sub(a), L = d.length(), g = new TH.CylinderGeometry(w1 * Math.SQRT1_2, w0 * Math.SQRT1_2, L, 4); g.rotateY(Math.PI / 4); g.scale(1, 1, th / w0); g.translate(0, L / 2, 0);
    const m = new TH.Mesh(g, mat); m.position.copy(a); m.quaternion.setFromUnitVectors(V(0, 1, 0), d.normalize()); return m; }
  // a curved horn / claw: a tapering tube along a bent path
  function horn(len, bend, r0, mat, seg = 18) { const pts = []; for (let i = 0; i <= 6; i++) { const f = i / 6; pts.push(V(f * len, -Math.pow(f, 2) * bend, 0)); }
    const g = new TH.TubeGeometry(new TH.CatmullRomCurve3(pts), seg, r0, 7, false), P = g.attributes.position;
    for (let i = 0; i <= seg; i++) { let cx = 0, cy = 0, cz = 0; for (let j = 0; j < 8; j++) { const q = i * 8 + j; cx += P.getX(q); cy += P.getY(q); cz += P.getZ(q); } cx /= 8; cy /= 8; cz /= 8;
      const s = Math.max(.04, 1 - i / seg); for (let j = 0; j < 8; j++) { const q = i * 8 + j; P.setXYZ(q, cx + (P.getX(q) - cx) * s, cy + (P.getY(q) - cy) * s, cz + (P.getZ(q) - cz) * s); } }
    g.computeVertexNormals(); return new TH.Mesh(g, mat); }
  // move set: act(name) starts a timed move; f(name, t) gives its 0..1 progress (or -1 when idle)
  const ss = (a, b, x) => { x = Math.min(1, Math.max(0, (x - a) / (b - a))); return x * x * (3 - 2 * x); };
  const bell = (f, a, b, c, d) => f < 0 ? 0 : ss(a, b, f) * (1 - ss(c, d, f));
  function moves(dur) { const S = {}; return { dur, play(n) { if (dur[n]) S[n] = { t0: -1, d: dur[n] }; }, f(n, t) { const s = S[n]; if (!s) return -1; if (s.t0 < 0) s.t0 = t; const f = (t - s.t0) / s.d; if (f >= 1) { delete S[n]; return -1; } return f; }, busy() { return Object.keys(S).length > 0; } }; }
  // an expanding shockwave ring (flat) or shell (sphere)
  function wave(par, R, sphere, col = VIO2) { const m = new TH.Mesh(sphere ? new TH.SphereGeometry(R, 32, 16) : new TH.RingGeometry(R * .9, R, 96), glowMat(col, 0)); if (!sphere) m.rotation.x = -Math.PI / 2; m.visible = false; par.add(m);
    return f => { m.visible = f > 0 && f < 1; if (!m.visible) return; m.scale.setScalar(.2 + f * 2.6); m.material.opacity = (1 - f) * (sphere ? .16 : .9); }; }
  // hit reaction: every hull material flares its rim and the model shudders
  function hitKit(grp, mover = grp) { const mats = new Set(); grp.traverse(o => { if (o.material && o.material.userData && o.material.userData.P) mats.add(o.material); });
    return (k, t) => { for (const m of mats) if (m.userData.rim) m.userData.rim.value = 1 + k * 6; mover.position.set(Math.sin(t * .09) * k * .25, Math.sin(t * .11 + 1) * k * .18, Math.sin(t * .13 + 2) * k * .2); }; }

  /* ---------- Energy Conduit: a stepped plinth with four buttress legs, a towering violet crystal threaded through three
     plated rings (the top one split into two horned arcs), dark shard collars, and lightning everywhere ---------- */
  function conduit() { const grp = new TH.Group(), M = hullMat("cond", { rows: 6, bronze: .2, rep: [14, 1] }), M2 = hullMat("cond2", { rows: 6, slits: .5, rep: [4, 1] });
    // stepped plinth: three square tiers with glowing risers
    [[3.3, 3.6, .55, .28], [2.6, 3.0, .55, .83], [1.9, 2.35, .55, 1.38], [1.25, 1.6, .5, 1.9]].forEach(([a, b, h, y]) => { const m = new TH.Mesh(new TH.CylinderGeometry(a, b, h, 4), M2); m.rotation.y = Math.PI / 4; m.position.y = y; grp.add(m);
      const gl = new TH.Mesh(new TH.CylinderGeometry(a * 1.004, a * 1.004, .07, 4, 1, true), glowMat(VIO, .8)); gl.rotation.y = Math.PI / 4; gl.position.y = y + h / 2 - .05; grp.add(gl); });
    // four buttress legs leaning in to the crystal's base, each with a spike cap
    for (let k = 0; k < 4; k++) { const a = k * TAU / 4 + TAU / 8, c = Math.cos(a), s = Math.sin(a), foot = V(c * 4.6, 0, s * 4.6), top = V(c * 1.9, 3.3, s * 1.9);
      grp.add(strut(foot, top, .38, .26, M)); const cap = shard(.32, 1.1, M); cap.position.copy(top).add(V(c * .35, -.2, s * .35)); grp.add(cap);
      const st = strut(foot.clone().add(V(0, .02, 0)), top.clone().add(V(0, -.05, 0)), .09, .07, glowMat(VIO2, .85)); st.position.add(V(-s * .28, .05, c * .28)); grp.add(st); }
    // front spine: a tall plated blade down the middle of the plinth
    { const sp = box(.55, 2.6, .35, M); sp.position.set(0, 1.4, 2.0); grp.add(sp); const sg = box(.12, 2.2, .05, glowMat(VIO2)); sg.position.set(0, 1.45, 2.19); grp.add(sg); }
    // the crystal: one long faceted shard from the plinth to the crown
    const cr = crystal([[0, 0], [.75, .5], [1.25, 2.6], [1.5, 4.7], [1.3, 6.4], [.75, 7.9], [0, 10.2]], 6); cr.position.y = 1.9; grp.add(cr);
    const inner = crystal([[0, 0], [.4, .6], [.7, 4.4], [.35, 7.6], [0, 9.2]], 6); inner.material = glowMat(0x9a40ff, .22); inner.position.y = 2.0; grp.add(inner);
    // shard collars: low (round the crystal's foot), mid (an emblem), crown
    const collar = (y, n, R, h, lean) => { for (let k = 0; k < n; k++) { const a = k * TAU / n, s = shard(.22, h, M); s.position.set(Math.cos(a) * R, y, Math.sin(a) * R); s.rotation.set(Math.sin(a) * lean, 0, -Math.cos(a) * lean); grp.add(s); } };
    collar(2.0, 8, 1.3, 1.9, .18); collar(5.0, 6, 1.15, 1.5, .1); collar(7.1, 6, 1.0, 1.6, .14);
    const emb = box(.7, 1.3, .3, M); emb.position.set(0, 5.6, 1.12); emb.rotation.z = Math.PI / 4; grp.add(emb); const eg = box(.18, .9, .06, glowMat(VIO2)); eg.position.set(0, 5.6, 1.29); grp.add(eg);
    // three rings: wide middle, low, and the split horned crown
    const rings = [];
    const mk = (R, y, w, h, tilt, arcs) => { const g = new TH.Group(); g.position.y = y; g.rotation.x = tilt;
      g.userData.arcs = []; for (const [p0, pl] of arcs) { const ag = new TH.Group(); ag.userData.c = p0 + pl / 2; ag.add(band(R, w, h, M, p0, pl)); ag.add(bandGlow(R - w / 2 - .012, h * .28, p0, pl)); ag.add(bandGlow(R + w / 2 + .012, h * .14, p0, pl, VIO)); g.add(ag); g.userData.arcs.push(ag); }
      grp.add(g); rings.push(g); return g; };
    mk(3.5, 3.3, .55, .6, .05, [[0, TAU]]); mk(4.7, 4.95, .62, .66, -.04, [[0, TAU]]);
    const top = mk(4.1, 6.9, .55, .6, .06, [[.25, Math.PI - .5], [Math.PI + .25, Math.PI - .5]]);
    for (const a of [.25, Math.PI - .25, Math.PI + .25, TAU - .25]) { const h = shard(.32, 1.4, M); h.position.set(Math.sin(a) * 4.1, .1, Math.cos(a) * 4.1); h.rotation.set(0, a, (a % Math.PI < 1 ? -1 : 1) * .9); top.userData.arcs[a < Math.PI ? 0 : 1].add(h); }
    // detail: conduit cables from each leg foot into the plinth, and vent greebles on every tier
    for (let k = 0; k < 4; k++) { const a = k * TAU / 4 + TAU / 8 + .32, c = Math.cos(a), s = Math.sin(a), pts = [V(c * 4.4, .1, s * 4.4), V(c * 3.9, .6, s * 3.9), V(c * 3.2, .5, s * 3.2), V(c * 2.6, 1.2, s * 2.6)];
      grp.add(new TH.Mesh(new TH.TubeGeometry(new TH.CatmullRomCurve3(pts), 16, .12, 6), M2)); const gl = new TH.Mesh(new TH.TubeGeometry(new TH.CatmullRomCurve3(pts.map(p => p.clone().add(V(0, .13, 0)))), 16, .03, 4), glowMat(VIO2, .8)); grp.add(gl); }
    [[3.45, .28], [2.8, .83], [2.12, 1.38]].forEach(([r, y]) => { for (let k = 0; k < 4; k++) for (let j = -1; j <= 1; j++) { const F = new TH.Group(); F.rotation.y = k * Math.PI / 2; const v = box(.45, .22, .16, M); v.position.set(j * r * .5, y, r * Math.SQRT1_2 + .04); F.add(v); const vg = box(.3, .05, .04, glowMat(VIO2, .9)); vg.position.set(j * r * .5, y, r * Math.SQRT1_2 + .13); F.add(vg); grp.add(F); } });
    // light
    const core = sprite(7, "rgba(190,110,255,1)"); core.position.y = 5; grp.add(core); const base = sprite(6, "rgba(190,100,255,1)"); base.position.y = 1.2; grp.add(base);
    const crPts = () => { const y = 2.5 + rnd() * 6.5, a = rnd() * TAU; return V(Math.cos(a) * .9, y, Math.sin(a) * .9); };
    const ringPt = () => { const g = rings[rnd() * 3 | 0], a = rnd() * TAU, R = g === rings[1] ? 4.4 : g === rings[0] ? 3.2 : 3.8; return V(Math.cos(a) * R, g.position.y, Math.sin(a) * R); };
    const bt = bolts(grp, 22, () => rnd() < .75 ? [crPts(), ringPt()] : [ringPt(), V((rnd() - .5) * 5, .4, (rnd() - .5) * 5)]);
    // moves: charge (rings spin up and spread, the crown opens), discharge (a bolt up from the tip, a ring shockwave),
    // link (a feed beam out along +x: the Overlord's shield), hit
    const shk = new TH.Group(), body = new TH.Group(); body.add(...grp.children); shk.add(body); grp.add(shk);
    const up1 = new TH.Mesh(new TH.CylinderGeometry(.25, .7, 40, 16, 1, true), glowMat(0xd090ff, .6)), up2 = new TH.Mesh(new TH.CylinderGeometry(.1, .25, 40, 12, 1, true), glowMat(0xf6e6ff, .95)); for (const b of [up1, up2]) { b.position.y = 12.1 + 20; b.visible = false; body.add(b); }
    const tipS = sprite(5, "rgba(240,210,255,1)", "hot2"); tipS.position.y = 12; body.add(tipS);
    const lnk = new TH.Group(); lnk.position.y = 9; body.add(lnk); const lb = new TH.Mesh(new TH.CylinderGeometry(.18, .18, 1, 10, 1, true), glowMat(0xd090ff, .7)); lb.rotation.z = -Math.PI / 2; lb.geometry.translate(0, .5, 0); lnk.add(lb); lnk.visible = false; lnk.userData.len = 30;
    const sw = wave(body, 5, false); body.children[body.children.length - 1].position.y = 5;
    const mv = moves({ charge: 2600, discharge: 1800, link: 4000, hit: 520 }), hit = hitKit(body, shk);
    const tick = t => { const fc = mv.f("charge", t), fd = mv.f("discharge", t), fl = mv.f("link", t), fh = mv.f("hit", t), ch = Math.max(bell(fc, 0, .7, .9, 1), bell(fd, 0, .01, .2, .5));
      const spin = 1 + ch * 9; rings[0].userData.a = (rings[0].userData.a || 0) + .00022 * 16 * spin; rings[1].userData.a = (rings[1].userData.a || 0) - .00015 * 16 * spin; rings[2].userData.a = (rings[2].userData.a || 0) + .0001 * 16 * spin;
      rings.forEach((r, i) => { r.rotation.y = r.userData.a; r.userData.y0 ??= r.position.y; r.position.y = r.userData.y0 + Math.sin(t * .0011 + i * 2) * .12 + (i - 1) * ch * .8 + (i === 2 ? ch * .9 : 0); });
      for (const ag of rings[2].userData.arcs) { const c = ag.userData.c, o = ch * .9 + Math.sin(t * .0013) * .05; ag.position.set(Math.sin(c) * o * 1.3, o * .4, Math.cos(c) * o * 1.3); ag.rotation.set(Math.cos(c) * o * .35, 0, -Math.sin(c) * o * .35); }
      const hov = Math.sin(t * .0012) * .15 + ch * .5; cr.position.y = 1.9 + hov; inner.position.y = 2.0 + hov; cr.rotation.y = t * .0002 + ch * t * .002;
      const p = .85 + Math.sin(t * .004) * .15 + ch * .9; cr.material.emissiveIntensity = .8 * p + .15; inner.material.opacity = Math.min(.9, .2 * p); core.material.opacity = Math.min(1, .35 * p); core.scale.setScalar(7 * (1 + ch * .5));
      const fire = bell(fd, .15, .2, .55, .9); for (const b of [up1, up2]) b.visible = fire > .01; up1.material.opacity = .6 * fire * (.8 + rnd() * .2); up2.material.opacity = fire; tipS.material.opacity = .3 + ch * .7; tipS.scale.setScalar(5 * (1 + fire * 1.5)); sw(fd < 0 ? -1 : (fd - .18) / .6);
      const lk = bell(fl, 0, .1, .9, 1); lnk.visible = lk > .01; if (lnk.visible) { lb.scale.set(1 + Math.sin(t * .03) * .25, lnk.userData.len * ss(0, .15, fl), 1 + Math.sin(t * .03) * .25); lb.material.opacity = .75 * lk; }
      bt(t, 1 + ch * 5 + lk * 2); hit(bell(fh, 0, .05, .4, 1), t); };
    return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), link: lnk, r: 6.5, h: 11.5 }; }

  /* ---------- Void Warden: a black, crackling void sphere inside a gyroscope of plated rings (one carved with glyphs),
     two great horned crescents left and right, crystal pylons above and below, and small ring-satellites ---------- */
  function warden() { const grp = new TH.Group(), M = hullMat("ward", { rows: 5, bronze: .22, rep: [18, 1] }), MG = hullMat("wardg", { rows: 1, cols: 16, slits: 0, glyphs: 1, bronze: .3, rep: [3, 1] });
    const core = new TH.Mesh(new TH.SphereGeometry(2.0, 48, 32), new TH.MeshBasicMaterial({ color: 0x07000f })); grp.add(core); const cor = new TH.Mesh(new TH.RingGeometry(2.0, 3.1, 64), new TH.MeshBasicMaterial({ map: radial("corona", [[0, "rgba(255,255,255,0)"], [.62, "rgba(255,255,255,0)"], [.66, "rgba(230,170,255,1)"], [.75, "rgba(170,70,255,.7)"], [1, "rgba(90,20,200,0)"]]), transparent: true, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); grp.add(cor);
    const shell = new TH.Mesh(new TH.SphereGeometry(2.15, 48, 32), new TH.MeshBasicMaterial({ map: swirlTex(), transparent: true, opacity: .95, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); grp.add(shell);
    const shell2 = shell.clone(); shell2.material = shell.material.clone(); shell2.scale.setScalar(1.12); shell2.material.opacity = .5; grp.add(shell2);
    const halo = sprite(10, "rgba(200,110,255,1)"); grp.add(halo);
    const gyro = [];
    const ring = (R, w, h, rot, mat = M) => { const g = new TH.Group(); g.add(band(R, w, h, mat)); g.add(bandGlow(R - w / 2 - .015, h * .3)); g.add(bandGlow(R + w / 2 + .015, h * .12, 0, TAU, VIO)); g.rotation.set(rot[0], rot[1], rot[2]); grp.add(g); gyro.push(g); return g; };
    const glyph = ring(4.1, 1.0, .8, [.1, 0, 0], MG); ring(2.9, .34, .4, [Math.PI / 2 - .2, 0, .3]); ring(5.0, .36, .45, [.32, 0, -.22]); ring(5.8, .26, .32, [-.22, 0, .45]);
    // two horned crescents, standing upright to the left and right, opening toward the core
    const crs = []; for (const side of [-1, 1]) { const g = new TH.Group(); const arc = band(6.6, .9, .85, M, -1.15, 2.3, 48); arc.rotation.z = Math.PI / 2; g.add(arc);
      const gl = new TH.Mesh(new TH.CylinderGeometry(6.6 - .47, 6.6 - .47, .24, 48, 1, true, -1.15, 2.3), glowMat(VIO2)); gl.rotation.z = Math.PI / 2; g.add(gl); const gh = new TH.Mesh(new TH.CylinderGeometry(6.6 - .47, 6.6 - .47, .7, 48, 1, true, -1.15, 2.3), glowMat(VIO, .2)); gh.rotation.z = Math.PI / 2; g.add(gh);
      for (const s of [-1, 1]) { const tip = shard(.52, 2.2, M), a = 1.15 * s; tip.position.set(0, Math.sin(a) * 6.6, Math.cos(a) * 6.6); tip.rotation.x = s > 0 ? -.4 : Math.PI + .4; g.add(tip); }
      for (let k = 0; k < 5; k++) { const a = -1 + k * .5, sp = shard(.24, 1.1, M); sp.position.set(0, Math.sin(a) * 7.1, Math.cos(a) * 7.1); sp.rotation.x = a - Math.PI / 2 + Math.PI; g.add(sp); }
      // detail: inner rib plates and outer armour knuckles along the crescent, and a glowing eye at its middle
      for (let k = 0; k < 9; k++) { const a = -1.0 + k * .25, rb = box(.5, .22, .5, M); rb.position.set(0, Math.sin(a) * 5.95, Math.cos(a) * 5.95); rb.rotation.x = -a; g.add(rb); const kn = box(.7, .3, .42, M); kn.position.set(0, Math.sin(a + .12) * 7.15, Math.cos(a + .12) * 7.15); kn.rotation.x = -a; g.add(kn); }
      { const e = new TH.Group(); e.position.set(0, 0, 7.3); e.add(new TH.Mesh(new TH.TorusGeometry(.55, .13, 8, 28), M)); e.add(new TH.Mesh(new TH.CircleGeometry(.42, 24), glowMat(CORE))); const es = sprite(2.2); e.add(es); g.add(e); }
      g.rotation.y = side > 0 ? Math.PI / 2 : -Math.PI / 2; grp.add(g); crs.push({ g, side }); }
    // crystal pylons, top and bottom
    const pyl = []; for (const s of [1, -1]) { const g = new TH.Group(); const c = crystal([[0, 0], [.45, .6], [.7, 2.0], [.4, 3.6], [0, 4.6]], 6); g.add(c); const col = new TH.Mesh(new TH.CylinderGeometry(.55, .75, .5, 6), M); col.position.y = .2; g.add(col);
      const r = band(.9, .16, .2, M); r.position.y = 1.1; g.add(r); { const sp = sprite(2.2); sp.position.set(0, 1.4, 0); g.add(sp); } g.position.y = s * 4.4; if (s < 0) g.rotation.x = Math.PI; grp.add(g); pyl.push({ g, s }); }
    // ring-satellites
    const sats = []; for (let k = 0; k < 3; k++) { const g = new TH.Group(); g.add(band(.75, .12, .14, M)); const r2 = band(.6, .1, .12, M); r2.rotation.x = Math.PI / 2; g.add(r2);
      const c = crystal([[0, 0], [.18, .3], [.12, .8], [0, 1.1]], 5); c.position.y = -.55; g.add(c); g.add(sprite(1.4)); grp.add(g); sats.push(g); }
    const bt = bolts(grp, 16, () => { const a = rnd() * TAU, b = rnd() * TAU, R = rnd() < .5 ? 3 : 4.4; return [V(Math.cos(a) * 1.8, (rnd() - .5) * 2, Math.sin(a) * 1.8), V(Math.cos(b) * R, (rnd() - .5) * 1.6, Math.sin(b) * R)]; });
    // moves: pulse (the crescents clench in and burst out with a void shockwave), beam (the gyroscope locks, the core fires
    // forward along +z), summon (the satellites fly wide and rain lightning), hit
    const shk = new TH.Group(), body = new TH.Group(); body.add(...grp.children); shk.add(body); grp.add(shk);
    const vw = wave(body, 4, true, 0x9a40ff), vw2 = wave(body, 6, false);
    const b1 = new TH.Mesh(new TH.CylinderGeometry(1.2, 1.6, 44, 24, 1, true), glowMat(0xb060ff, .5)), b2 = new TH.Mesh(new TH.CylinderGeometry(.35, .5, 44, 16, 1, true), glowMat(0xf6e6ff, .9)); for (const b of [b1, b2]) { b.rotation.x = Math.PI / 2; b.position.z = 22; b.visible = false; body.add(b); }
    const gy0 = gyro.map(g => g.rotation.clone()), ga = gyro.map(() => 0);
    const mv = moves({ pulse: 1800, beam: 3200, summon: 3000, hit: 520 }), hit = hitKit(body, shk);
    const tick = t => { const fp = mv.f("pulse", t), fb = mv.f("beam", t), fs = mv.f("summon", t), fh = mv.f("hit", t);
      const clench = bell(fp, 0, .4, .45, .55), burst = bell(fp, .45, .55, .7, 1), lock = bell(fb, 0, .25, .85, 1), fire = bell(fb, .28, .34, .8, .95), wide = bell(fs, 0, .3, .7, 1);
      const spd = [.00016, -.0004, .00025, -.0002]; gyro.forEach((g, i) => { ga[i] += spd[i] * 16 * (1 + clench * 4 + lock * 2); g.rotation.set(gy0[i].x * (1 - lock), ga[i] * (1 - lock) + (i % 2 ? Math.PI / 2 : 0) * lock, gy0[i].z * (1 - lock)); });
      for (const c of crs) { const br = Math.sin(t * .0009) * .25; c.g.position.x = c.side * (-clench * 2.4 + burst * 1.2 + br); c.g.rotation.z = c.side * (Math.sin(t * .0007) * .05 - clench * .25); c.g.scale.setScalar(1 + burst * .08); }
      for (const p of pyl) { p.g.position.y = p.s * (4.4 + Math.sin(t * .0013) * .25 + lock * 1.2 + wide * .8); p.g.rotation.y = t * .0006 * p.s; }
      const pul = 1 + Math.sin(t * .0025) * .03 - clench * .18 + burst * .25 + fire * .1; core.scale.setScalar(pul); shell.scale.setScalar(pul); shell2.scale.setScalar(pul * 1.12); cor.scale.setScalar(pul * (1 + fire * .25));
      shell.rotation.y = -t * (.0007 + fire * .006); shell.rotation.z = t * .0002; shell2.rotation.y = t * .0004; halo.material.opacity = Math.min(1, .7 + Math.sin(t * .003) * .2 + fire * .3 + clench * .3); halo.scale.setScalar(10 * (1 + fire * .6 + burst * .4));
      vw(fp < 0 ? -1 : (fp - .45) / .55); vw2(fp < 0 ? -1 : (fp - .47) / .5);
      for (const b of [b1, b2]) b.visible = fire > .01; b1.material.opacity = .5 * fire * (.85 + rnd() * .15); b2.material.opacity = .9 * fire; b1.scale.set(1 + fire * .25, 1, 1 + fire * .25);
      sats.forEach((g, k) => { const a = t * (.00018 + wide * .0006) + k * TAU / 3, R = 9.2 + wide * 5; g.position.set(Math.cos(a) * R, Math.sin(a * 1.7 + k) * 1.5 + wide * Math.sin(k * 2) * 3, Math.sin(a) * R); g.rotation.y = t * .001; g.scale.setScalar(1 + wide * .4); });
      bt(t, 1 + clench * 4 + fire * 3 + wide * 3); hit(bell(fh, 0, .05, .4, 1), t); };
    return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 10, h: 15 }; }

  /* ---------- Pyramid Overlord: a monumental pyramid of layered armour plates on six walking legs. Each face carries the
     ring-and-diamond sigil with a light channel down to the apex; the stepped underbelly pours a violet beam.
     Moves: walk (tripod gait), beam (rears back, the front sigil fires), stomp (front legs rise and slam, ground shockwave),
     summon (belly claws open, the down-beam surges), hit. ---------- */
  function overlord() { const grp = new TH.Group(), shk = new TH.Group(), body = new TH.Group(); grp.add(shk); shk.add(body);
    const M = hullMat("ovl", { rows: 6, bronze: .16, slits: .35, rep: [1, 1] }), MP = hullMat("ovlp", { rows: 3, slits: .55, bronze: .3, rep: [1, 1] }), ML = hullMat("ovl2", { rows: 5, slits: .4, rep: [2, 3] }), MD = hullMat("ovld", { rows: 8, base: "#26242c", slits: .2, rep: [3, 2] });
    const B = 4.3, H = 5.8, y0 = .45, Ls = Math.hypot(B, H), phi = Math.atan2(B, H);
    const core = new TH.Mesh(new TH.ConeGeometry(B * Math.SQRT2, H, 4, 1), MD); core.rotation.y = Math.PI / 4; core.position.y = y0 + H / 2; body.add(core);
    const sigils = [];
    for (let k = 0; k < 4; k++) { const F = new TH.Group(); F.rotation.y = k * Math.PI / 2; body.add(F); const S = new TH.Group(); S.position.set(0, y0, B); S.rotation.x = -phi; F.add(S);
      // nine rows of armour plates, thicker every other row, clipped to the face's taper
      const nR = 9; for (let i = 0; i < nR; i++) { const s0 = Ls * i / nR, s1 = Ls * (i + 1) / nR, hwT = B * (1 - s1 / Ls) - .1, hwB = B * (1 - s0 / Ls) - .1; if (hwT < .2) break;
        const np = Math.max(1, Math.round(hwB * 2 / 1.25)), pw = hwB * 2 / np;
        for (let j = 0; j < np; j++) { let x0 = -hwB + pw * j + .05, x1 = x0 + pw - .1; x0 = Math.max(x0, -hwT); x1 = Math.min(x1, hwT); if (x1 - x0 < .25) continue;
          if (Math.abs((x0 + x1) / 2) < .35 && i < 7) { const w = x1 - x0; if (w < 1.1) continue; } // keep the centre channel clear
          const d = .14 + rnd() * .12 + (i % 2) * .08, h = (s1 - s0) * .9, P = box(x1 - x0, h, d, rnd() < .3 ? MP : M); P.position.set((x0 + x1) / 2, (s0 + s1) / 2, d / 2); S.add(P);
          if (rnd() < .45) { const gw = .3 + rnd() * .7, G = box(gw, .12 + rnd() * .2, .12, M); G.position.set((x0 + x1) / 2 + (rnd() - .5) * (x1 - x0 - gw) * .8, (s0 + s1) / 2 + (rnd() - .5) * h * .5, d + .06); S.add(G); }
          if (rnd() < .25) { const sl = box((x1 - x0) * .5, .05, .04, glowMat(VIO2, .9)); sl.position.set((x0 + x1) / 2, s0 + h * .2, d + .02); S.add(sl); } }
        if (i % 3 === 2) { const gl = box(hwB * 2, .07, .05, glowMat(VIO, .8)); gl.position.set(0, s1 - .02, .05); S.add(gl); } }
      // the centre light channel from the sigil up to the apex, framed by two rails
      { const ch = box(.14, Ls * .62, .06, glowMat(VIO2)); ch.position.set(0, Ls * .58, .42); S.add(ch); for (const sx of [-1, 1]) { const r = box(.16, Ls * .6, .32, M); r.position.set(sx * .2, Ls * .58, .2); S.add(r); }
        const ch2 = box(.1, Ls * .2, .05, glowMat(VIO2)); ch2.position.set(0, Ls * .1, .32); S.add(ch2); }
      // the sigil: armoured ring, glowing inner ring, a diamond eye and four arms
      const sg = new TH.Group(); sg.position.set(0, Ls * .3, .55); S.add(sg); const sgs = new TH.Group(); sg.add(sgs);
      sg.add(new TH.Mesh(new TH.TorusGeometry(1.05, .2, 8, 40), M)); sgs.add(new TH.Mesh(new TH.TorusGeometry(.78, .07, 8, 40), glowMat(VIO2))); sg.add(new TH.Mesh(new TH.TorusGeometry(1.35, .04, 6, 48), glowMat(VIO, .6)));
      for (let q = 0; q < 8; q++) { const n = box(.12, .3, .12, M), a = q * TAU / 8; n.position.set(Math.cos(a) * .92, Math.sin(a) * .92, .16); n.rotation.z = a; sgs.add(n); }
      const eye = box(.55, .55, .3, M); eye.rotation.z = Math.PI / 4; sg.add(eye); const eg = box(.32, .32, .1, glowMat(CORE)); eg.rotation.z = Math.PI / 4; eg.position.z = .17; sg.add(eg);
      for (let q = 0; q < 4; q++) { const a = q * Math.PI / 2, arm = shard(.22, q === 1 ? 1.0 : .7, M); arm.position.set(Math.cos(a) * 1.25, Math.sin(a) * 1.25, 0); arm.rotation.z = a - Math.PI / 2; sg.add(arm); }
      const sp = sprite(3.4); sp.position.z = .3; sg.add(sp); sigils.push({ sg, sgs, sp, eg, front: k === 0 }); }
    // corner ribs: armour along each edge with a light line, and the apex crown
    for (let k = 0; k < 4; k++) { const a = k * Math.PI / 2 + Math.PI / 4, cor = V(Math.cos(a) * B * Math.SQRT2, y0, Math.sin(a) * B * Math.SQRT2), apex = V(0, y0 + H, 0);
      body.add(strut(cor, apex, .34, .12, M)); const gl = strut(cor.clone().multiplyScalar(1.02).setY(y0 + .1), apex.clone().setY(y0 + H - .15), .07, .03, glowMat(VIO2, .9)); body.add(gl);
      for (let i = 1; i < 6; i++) { const p = cor.clone().lerp(apex, i / 6.5), n = shard(.16, .55, M); n.position.copy(p); n.lookAt(p.clone().multiplyScalar(2).setY(p.y + 1)); n.rotateX(Math.PI / 2); body.add(n); } }
    { const cap = new TH.Mesh(new TH.ConeGeometry(.75, 1.3, 4), M); cap.rotation.y = Math.PI / 4; cap.position.y = y0 + H + .05; body.add(cap); const as = sprite(2.6); as.position.y = y0 + H + .5; body.add(as); }
    // armoured skirt round the base with vents and a light band
    { const sk = new TH.Mesh(new TH.CylinderGeometry(B * Math.SQRT2 * 1.03, B * Math.SQRT2 * .93, 1.0, 4, 1), ML); sk.rotation.y = Math.PI / 4; sk.position.y = y0 - .5; body.add(sk);
      const sg = new TH.Mesh(new TH.CylinderGeometry(B * Math.SQRT2 * 1.0, B * Math.SQRT2 * .98, .1, 4, 1, true), glowMat(VIO2)); sg.rotation.y = Math.PI / 4; sg.position.y = y0 - .55; body.add(sg);
      for (let k = 0; k < 4; k++) for (let j = -3; j <= 3; j++) { const F = new TH.Group(); F.rotation.y = k * Math.PI / 2; const v = box(.7, .35, .25, M); v.position.set(j * 1.15, y0 - .25, B * 1.0 + .08); F.add(v); body.add(F); } }
    // stepped underbelly, emitter rings, eight hanging claws, and the beam
    const belly = new TH.Group(); body.add(belly);
    [[3.9, 3.3, .6, -.45], [3.1, 2.4, .6, -1.05], [2.3, 1.6, .5, -1.6]].forEach(([a, b, h, y]) => { const m = new TH.Mesh(new TH.CylinderGeometry(a, b, h, 8), ML); m.position.y = y; belly.add(m); const g = new TH.Mesh(new TH.CylinderGeometry(b * 1.01, b * 1.01, .06, 8, 1, true), glowMat(VIO2)); g.position.y = y - h / 2 + .04; belly.add(g); });
    const emit = new TH.Group(); emit.position.y = -1.9; belly.add(emit); for (const [R, w] of [[1.5, .09], [1.05, .07], [.6, .06]]) { const r = new TH.Mesh(new TH.TorusGeometry(R, w, 8, 48), glowMat(VIO2)); r.rotation.x = Math.PI / 2; emit.add(r); }
    const claws = []; for (let k = 0; k < 8; k++) { const a = k * TAU / 8 + TAU / 16, h = new TH.Group(); h.position.set(Math.cos(a) * 2.6, -1.4, Math.sin(a) * 2.6); h.rotation.y = -a; const c = horn(1.6, .5, .16, M); c.rotation.z = -Math.PI / 2 - .25; h.add(c); belly.add(h); claws.push(h); }
    const bm = new TH.Mesh(new TH.CylinderGeometry(.35, 1.1, 9, 24, 1, true), glowMat(0xc070ff, .45)); bm.position.y = -6.4; belly.add(bm);
    const bm2 = new TH.Mesh(new TH.CylinderGeometry(.12, .32, 9, 16, 1, true), glowMat(0xf0d8ff, .8)); bm2.position.y = -6.4; belly.add(bm2); const em = sprite(4.5); em.position.y = -2.0; belly.add(em);
    // six legs: hip drum, armoured femur rising to a peaked knee, a long blade-shin plunging to a three-claw foot
    const legs = [];
    for (let k = 0; k < 6; k++) { const a = k * TAU / 6, L = new TH.Group(); L.position.set(Math.cos(a) * 3.9, -.55, Math.sin(a) * 3.9); L.rotation.y = -a; body.add(L);
      const hip = new TH.Mesh(new TH.CylinderGeometry(.95, .95, 1.6, 14), ML); hip.rotation.x = Math.PI / 2; L.add(hip); for (const z of [-.83, .83]) { const r = new TH.Mesh(new TH.TorusGeometry(.6, .06, 6, 24), glowMat(VIO2)); r.position.z = z; L.add(r); }
      const cx = new TH.Group(); L.add(cx);
      const kp = V(3.4, 2.8, 0); cx.add(beam(V(0, 0, 0), kp, 1.5, 1.1, 1.0, M));
      { const fin = beam(V(.3, .75, 0), V(3.2, 3.6, 0), .6, .3, .8, ML); cx.add(fin); for (const z of [-.53, .53]) { const s = strut(V(.5, .2, z), V(3.1, 2.55, z), .05, .04, glowMat(VIO2)); cx.add(s); } }
      { const cyl = strut(V(.3, -.55, 0), V(2.0, 1.1, 0), .16, .16, MD, 8); cx.add(cyl); const rod = strut(V(2.0, 1.1, 0), V(2.9, 2.0, 0), .08, .08, M, 8); cx.add(rod); }
      const kn = new TH.Group(); kn.position.copy(kp); cx.add(kn);
      { const d = new TH.Mesh(new TH.CylinderGeometry(1.0, 1.0, 1.5, 14), ML); d.rotation.x = Math.PI / 2; kn.add(d); const r = new TH.Mesh(new TH.TorusGeometry(.5, .07, 6, 24), glowMat(VIO2)); r.position.z = .78; kn.add(r); const r2 = r.clone(); r2.position.z = -.78; kn.add(r2);
        const pk = shard(.6, 2.0, M); pk.position.set(.2, .5, 0); pk.rotation.z = -.35; kn.add(pk); const ks = sprite(1.6); ks.position.z = .65; kn.add(ks); }
      const fp = V(1.7, -8.4, 0); kn.add(beam(V(0, 0, 0), fp, 1.55, .4, .85, M));
      { const blade = beam(V(.65, -.6, 0), V(1.75, -7.2, 0), .8, .14, .3, ML); kn.add(blade); kn.add(strut(V(.62, -.8, 0), V(1.72, -7.4, 0), .06, .03, glowMat(VIO2)));
        for (let q = 1; q < 4; q++) { const p = V(0, 0, 0).lerp(fp, q / 5), ar = box(1.3, .6, 1.05, ML); ar.position.copy(p); ar.rotation.z = -.2; kn.add(ar); const gl = box(.06, .3, 1.08, glowMat(VIO, .6)); gl.position.copy(p).add(V(.66, 0, 0)); gl.rotation.z = -.2; kn.add(gl); } }
      const foot = new TH.Group(); foot.position.copy(fp); kn.add(foot); for (const za of [-.6, 0, .6]) { const c = horn(1.5, .45, .2, M); c.rotation.set(za, 0, -Math.PI / 2 + .35); foot.add(c); }
      legs.push({ L, cx, kn, a, front: Math.sin(a) > .2, ph: (k % 2) * Math.PI }); }
    const bt = bolts(body, 8, () => [V((rnd() - .5) * 1.6, -2, (rnd() - .5) * 1.6), V((rnd() - .5) * 3.4, -6 - rnd() * 5, (rnd() - .5) * 3.4)]);
    // attack fx: the forward sigil beam and the ground shockwave
    const fBeam = new TH.Group(); fBeam.visible = false; body.add(fBeam); { const sg = sigils[0].sg; sg.updateWorldMatrix(true, false); }
    const fb1 = new TH.Mesh(new TH.CylinderGeometry(.9, .55, 40, 24, 1, true), glowMat(0xc070ff, .5)), fb2 = new TH.Mesh(new TH.CylinderGeometry(.3, .2, 40, 16, 1, true), glowMat(0xf6e6ff, .9)); for (const b of [fb1, fb2]) { b.rotation.x = Math.PI / 2; b.position.z = 20; fBeam.add(b); }
    const fbS = sprite(7, "rgba(240,210,255,1)", "hot2"); fBeam.add(fbS);
    const groundY = -.55 + 2.8 - 8.4 - .4, quake = wave(grp, 9, false); grp.children[grp.children.length - 1].position.y = groundY;
    const mv = moves({ walk: 6000, beam: 3200, stomp: 1700, summon: 2600, hit: 520 }), hit = hitKit(body, shk);
    const tick = t => { const fw = mv.f("walk", t), fbm = mv.f("beam", t), fst = mv.f("stomp", t), fsu = mv.f("summon", t), fh = mv.f("hit", t);
      const W = .12 + .88 * bell(fw, 0, .08, .92, 1), sp = .0014 + .0021 * bell(fw, 0, .08, .92, 1);
      const rear = bell(fbm, 0, .25, .8, 1) , lift = bell(fst, 0, .35, .42, .5), slam = bell(fst, .42, .5, .6, .95);
      for (const g of legs) { const p = t * sp + g.ph, sw = Math.sin(p), up = Math.max(0, Math.cos(p)); let lz = up * .38 * W, ly = sw * .3 * W, kz = -up * .3 * W;
        if (g.front) { lz += rear * .6 + lift * 1.1 - slam * .15; kz += -rear * .35 - lift * .8 + slam * .2; } else { lz -= rear * .12; }
        g.cx.rotation.set(0, ly, lz); g.kn.rotation.z = kz; }
      body.position.y = Math.sin(t * sp * 2) * .12 * W + Math.sin(t * .0011) * .1 - slam * .35; body.rotation.x = -rear * .2 + slam * .04; body.rotation.z = Math.sin(t * sp) * .02 * W;
      const charge = ss(0, .3, fbm < 0 ? 0 : fbm) * (fbm < 0 ? 0 : 1), fire = bell(fbm, .3, .36, .82, .95);
      for (const s of sigils) { s.sgs.rotation.z = t * .0006 + (s.front ? charge * t * .008 : 0); s.sp.material.opacity = .75 + Math.sin(t * .003) * .2 + (s.front ? charge * .8 : 0); s.sp.scale.setScalar(3.4 * (1 + (s.front ? fire * 1.2 : 0))); }
      fBeam.visible = fire > .01; if (fBeam.visible) { const sg = sigils[0].sg; fBeam.position.set(0, y0 + Math.cos(phi) * Ls * .3 + .1, B - Math.sin(phi) * Ls * .3 + .7); fBeam.rotation.x = -rear * .05; fb1.material.opacity = .5 * fire * (.85 + rnd() * .15); fb2.material.opacity = .9 * fire; fb1.scale.set(1 + fire * .2, 1, 1 + fire * .2); fbS.material.opacity = fire; }
      quake(fst < 0 ? -1 : (fst - .5) / .5);
      const surge = bell(fsu, 0, .2, .75, 1); for (const c of claws) c.rotation.z = -surge * .7 + Math.sin(t * .002) * .04;
      const f = (.8 + Math.sin(t * .006) * .12 + (rnd() < .05 ? .15 : 0)) * (1 + surge * .8); bm.material.opacity = .4 * f; bm2.material.opacity = .75 * Math.min(1.3, f); bm.scale.set(1 + surge * .6, 1, 1 + surge * .6); em.material.opacity = Math.min(1, f);
      bt(t, 1 + surge * 4 + fire * 2); hit(bell(fh, 0, .05, .4, 1), t); };
    return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 12, h: 16 }; }

  /* ---------- Orbital Devourer: a long hull of overlapping chitin scales tapering to a lance tail, scythe blades sweeping
     back, a maw of eight hinged claws round a crackling vortex, and many jointed tentacles that never stop moving.
     Moves: bite (claws gape and snap, lunge), lash (tentacles whip forward in a travelling wave), beam (maw gapes, the
     vortex fires), roar (claws flare, tentacles splay, lightning), hit. ---------- */
  function devourer() { const grp = new TH.Group(), shk = new TH.Group(), body = new TH.Group(); grp.add(shk); shk.add(body);
    const M = hullMat("dev", { rows: 12, bronze: .12, slits: .55, rep: [12, 3] }), MS = hullMat("devs", { rows: 2, cols: 2, bronze: .15, slits: .45, rep: [1, 1] }), MB = hullMat("devb", { rows: 4, bronze: .35, slits: .15, rep: [1, 1] });
    MS.side = TH.DoubleSide; MB.side = TH.DoubleSide;
    const rad = x => x > 2.6 ? 2.6 + (x - 2.6) * .45 : Math.max(.22, 2.6 * Math.pow(Math.max(0, (x + 11.5) / 14.1), .85));
    { const pr = []; for (let x = -11.5; x <= 3.5; x += .25) pr.push(new TH.Vector2(rad(x) * .92, x)); pr.unshift(new TH.Vector2(0, -11.6)); pr.push(new TH.Vector2(1.8, 3.55));
      const hull = new TH.Mesh(new TH.LatheGeometry(pr, 32), M); hull.rotation.z = -Math.PI / 2; body.add(hull); }
    // overlapping scale rows, back edges lifted, light glowing through the seams
    const scales = new TH.Group(); body.add(scales);
    for (let x = 2.5, row = 0; x > -10.5; x -= .62, row++) { const R = rad(x), n = Math.max(4, Math.round(R * 3.2)), sl = TAU / n;
      for (let j = 0; j < n; j++) { const th0 = j * sl + (row % 2) * sl / 2, g = new TH.CylinderGeometry(R * 1.0 + .03, R * 1.1 + .22, .95, 4, 1, true, th0, sl * .94), m = new TH.Mesh(g, MS); m.rotation.z = -Math.PI / 2; m.position.x = x - .4; scales.add(m); }
      if (row % 2 === 0) { const g = new TH.Mesh(new TH.TorusGeometry(R * .99, .05, 6, 32), glowMat(VIO2, .8)); g.rotation.y = Math.PI / 2; g.position.x = x - .85; body.add(g); } }
    // scythe blades and dorsal spines
    const scy = (len, wid) => { const s = new TH.Shape(); s.moveTo(0, 0); s.quadraticCurveTo(len * .45, wid * 1.2, len, wid * .15); s.quadraticCurveTo(len * .5, wid * .45, 0, 0);
      const g = new TH.ExtrudeGeometry(s, { depth: .14, bevelEnabled: true, bevelThickness: .05, bevelSize: .05, bevelSegments: 1, curveSegments: 12 }); g.translate(0, 0, -.07); return g; };
    const blades = [];
    for (let i = 0; i < 34; i++) { const x = 2.4 - i * .34, R = rad(x) + .1, a = [0, .7, -.7, 1.5, -1.5, 2.3, -2.3][i % 7] + (rnd() - .5) * .3, len = (3.0 + rnd() * 3.2) * (x > -2 ? 1.5 : 1.1);
      const h = new TH.Group(); h.rotation.x = a; h.position.x = x; const m = new TH.Mesh(scy(len, 1.0 + rnd() * .8), MB); m.position.y = R - .2; m.rotation.z = Math.PI - (.35 + rnd() * .35); m.scale.y = -1; h.add(m); body.add(h); blades.push({ h, m, ph: rnd() * TAU, z0: m.rotation.z }); }
    for (let i = 0; i < 14; i++) { const x = 2.0 - i * .72, sp = shard(.24, 1.3 + rnd() * 1.1, MB); sp.position.set(x, rad(x) + .1, 0); sp.rotation.z = .7; body.add(sp); }
    // the lance tail
    { const t1 = horn(3.4, .3, .32, MB); t1.rotation.z = Math.PI; t1.position.x = -11.0; body.add(t1); const tg = sprite(1.6); tg.position.x = -11; body.add(tg); }
    // the maw: armoured collar, eight hinged claws, a ring of teeth, two counter-turning vortex discs and a white-hot heart
    const maw = new TH.Group(); maw.position.x = 3.5; body.add(maw);
    { const col = band(2.85, .5, .7, M, 0, TAU, 96, 18); col.rotation.z = Math.PI / 2; maw.add(col); for (const [R, x] of [[2.55, .05], [2.0, -.1], [3.15, -.2]]) { const r = new TH.Mesh(new TH.TorusGeometry(R, .08, 8, 64), glowMat(VIO2)); r.rotation.y = Math.PI / 2; r.position.x = x; maw.add(r); } }
    const claws = []; for (let k = 0; k < 8; k++) { const a = k * TAU / 8 + .2, h = new TH.Group(); h.rotation.x = a; maw.add(h); const hg = new TH.Group(); hg.position.y = 2.75; h.add(hg);
      const c = horn(4.6 + (k % 2) * .9, 1.9, .5, MB); hg.add(c); for (let q = 1; q < 4; q++) { const s = shard(.13, .5, MB); s.position.set(q * 1.0, -Math.pow(q / 4.6, 2) * 1.9 + .32, 0); s.rotation.z = -.4; hg.add(s); }
      const gl = strut(V(.2, -.25, 0), V(3.6, -1.4, 0), .05, .02, glowMat(VIO2, .8)); hg.add(gl); claws.push({ hg, ph: k * .7 }); }
    for (let k = 0; k < 18; k++) { const a = k * TAU / 18, s = shard(.14, .7, MB); s.position.set(.05, Math.cos(a) * 2.25, Math.sin(a) * 2.25); s.lookAt(s.position.clone().add(V(.6, -Math.cos(a), -Math.sin(a)))); s.rotateX(Math.PI / 2); maw.add(s); }
    const vmat = new TH.MeshBasicMaterial({ map: swirlTex(), transparent: true, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false, side: TH.DoubleSide });
    const vort = new TH.Mesh(new TH.CircleGeometry(2.4, 48), vmat); vort.rotation.y = Math.PI / 2; maw.add(vort); const vort2 = new TH.Mesh(vort.geometry, vmat.clone()); vort2.material.opacity = .6; vort2.rotation.y = Math.PI / 2; vort2.scale.setScalar(.72); vort2.position.x = .15; maw.add(vort2);
    const hot = sprite(4.2, "rgba(250,225,255,1)", "hot"); hot.position.x = .4; maw.add(hot); const glow = sprite(9); glow.position.x = .2; maw.add(glow);
    const mb1 = new TH.Mesh(new TH.CylinderGeometry(1.4, 1.9, 44, 24, 1, true), glowMat(0xc070ff, .5)), mb2 = new TH.Mesh(new TH.CylinderGeometry(.45, .6, 44, 16, 1, true), glowMat(0xf6e6ff, .9)); for (const b of [mb1, mb2]) { b.rotation.z = -Math.PI / 2; b.position.x = 22; b.visible = false; maw.add(b); }
    // jointed tentacles: chains of plated segments with light rings at every joint and spurs along the length
    const TM = hullMat("tent", { rows: 3, cols: 4, bronze: .1, slits: .22, rep: [1, 1], ei: 2.4, base: "#34323c", rim: .6 });
    const tents = [];
    const tent = (len, n, r0, x0, dir, curl, front) => { const root = new TH.Group(), base = new TH.Group(); root.add(base); let par = base, prevL = 0; const J = [];
      for (let i = 0; i < n; i++) { const f = i / n, L = len / n * (1.3 - .6 * f), r = r0 * (1 - .82 * f) + .04, j = new TH.Group(); j.position.y = prevL; par.add(j);
        const g = new TH.CylinderGeometry(r * .8, r, L * 1.04, 9); g.translate(0, L / 2, 0); j.add(new TH.Mesh(g, TM));
        const rg = new TH.Mesh(new TH.TorusGeometry(r * .86, Math.max(.02, r * .06), 6, 18), glowMat(VIO, .55)); rg.rotation.x = Math.PI / 2; rg.position.y = L * .97; j.add(rg);
        if (i % 2 === 1 && i < n - 2) { const s = shard(r * .35, r * 1.6, MB); s.position.set(r * .85, L * .5, 0); s.rotation.z = -1.0; j.add(s); }
        J.push(j); par = j; prevL = L; }
      const tip = horn(len / n * 1.6, .4, Math.max(.06, r0 * .2), MB); tip.rotation.z = Math.PI / 2; tip.position.y = prevL; par.add(tip);
      const R = rad(x0) * .88; root.position.set(x0, dir.y * R, dir.z * R); const d = V(dir.x, dir.y, dir.z).normalize(); root.quaternion.setFromUnitVectors(V(0, 1, 0), d); root.rotateY(rnd() * TAU);
      body.add(root); tents.push({ root, base, J, curl, ph: rnd() * TAU, w: .0009 + rnd() * .0006, front }); };
    for (let k = 0; k < 8; k++) { const a = k * TAU / 8 + .3, x0 = 1.6 - (k % 4) * 1.9; tent(12 + rnd() * 6, 15, .85 + rnd() * .2, x0, V(-1.1, Math.cos(a) - .35, Math.sin(a)), (rnd() < .5 ? 1 : -1) * (.1 + rnd() * .09), false); }
    for (let k = 0; k < 6; k++) { const a = k * TAU / 6, x0 = 2.9; tent(4.5 + rnd() * 2, 9, .42, x0, V(.55, Math.cos(a), Math.sin(a)), (rnd() < .5 ? 1 : -1) * (.12 + rnd() * .08), true); }
    const bt = bolts(maw, 10, () => { const a = rnd() * TAU, b = a + (rnd() - .5) * 2; return [V(.3, 0, 0), V(.1, Math.cos(b) * 1.9, Math.sin(b) * 1.9)]; }, 0xf0d0ff);
    const roarW = wave(maw, 3.5, true);
    const mv = moves({ bite: 1100, lash: 1600, beam: 3000, roar: 2400, hit: 520 }), hit = hitKit(body, shk);
    const tick = t => { const fb = mv.f("bite", t), fl = mv.f("lash", t), fm = mv.f("beam", t), fr = mv.f("roar", t), fh = mv.f("hit", t);
      const gapeB = bell(fb, 0, .4, .45, .55), snap = bell(fb, .45, .55, .7, 1), gapeM = bell(fm, 0, .2, .85, 1), fire = bell(fm, .25, .3, .82, .95), flare = bell(fr, 0, .15, .7, 1);
      const open = .12 + Math.sin(t * .0015) * .06 + gapeB * .85 + gapeM * .7 + flare * .5 - snap * .25;
      for (const c of claws) c.hg.rotation.z = open + Math.sin(t * .004 + c.ph) * .03;
      body.position.x = snap * 1.4 - gapeB * .3 - fire * .4 * (.6 + rnd() * .4); body.rotation.x = Math.sin(t * .00035) * .12; body.rotation.z = Math.sin(t * .0006) * .04 + Math.sin(t * .00023) * .03;
      for (const b of blades) b.m.rotation.z = b.z0 + Math.sin(t * .0012 + b.ph) * .05 + flare * .25;
      const splay = Math.max(gapeM, flare);
      for (const T of tents) { const n = T.J.length; let whip = 0;
        if (fl >= 0 && !T.front) whip = 1; const cf = T.curl * (.75 + .25 * Math.sin(t * .0007 + T.ph)) * (1 - splay * .8);
        T.J.forEach((j, i) => { const u = i / n, w = T.w * 1000;
          let z = cf + Math.sin(t * T.w * 2.4 + i * .55 + T.ph) * .14 * (.35 + u), x = Math.cos(t * T.w * 2 + i * .5 + T.ph * 1.3) * .1 * (.35 + u);
          if (whip) { const ff = fl - u * .25; z += -bell(ff, 0, .15, .2, .35) * .35 + bell(ff, .2, .35, .45, .75) * .28 * (i ? 1 : 2.5); }
          if (T.front) z += Math.sin(t * .006 + i + T.ph) * .08 * (gapeB + flare);
          j.rotation.set(x, 0, z); });
        T.base.rotation.z = -splay * .45 * Math.sign(T.curl) + (whip ? -bell(fl, 0, .2, .3, .6) * .4 + bell(fl, .3, .45, .6, 1) * .9 : 0); }
      vort.rotation.x = -t * (.0012 + fire * .01); vort2.rotation.x = t * (.002 + fire * .012); hot.material.opacity = .8 + Math.sin(t * .007) * .2; hot.scale.setScalar(4.2 * (1 + fire * 1.4 + gapeM * .3)); glow.material.opacity = .7 + fire * .3;
      for (const b of [mb1, mb2]) b.visible = fire > .01; mb1.material.opacity = .5 * fire * (.85 + rnd() * .15); mb2.material.opacity = .9 * fire; mb1.scale.set(1 + fire * .25, 1, 1 + fire * .25);
      roarW(fr < 0 ? -1 : fr * 1.3); bt(t, 1 + flare * 5 + fire * 3); hit(bell(fh, 0, .05, .4, 1), t); };
    return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 15, h: 18 }; }

  root.BOSS3D = { init(T) { TH = T; }, conduit, warden, overlord, devourer };
})(typeof window !== "undefined" ? window : globalThis);
