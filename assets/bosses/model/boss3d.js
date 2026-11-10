/* UDF bosses in 3D, built from the owner's reference art (assets/bosses/<boss>/reference/ref-2026-11-09.png):
   Energy Conduit, Void Warden, Pyramid Overlord, Orbital Devourer, and the Wednesday four (same folders, ref-2026-11-10.png):
   Brood Matriarch, Iron Tyrant, Event Horizon Wyrm, Shard Colossus. Plated gunmetal with bronze trim and violet light slits,
   faceted violet crystal, living lightning, moving parts. Each build returns { grp, tick(t), r } with r = bounding radius. */
(function (root) {
  const TAU = Math.PI * 2;
  let TH = null; const cache = {}; let LOD = 0; // 0 = close-up (viewer, desktop report), 1 = galaxy map (smaller textures, simpler tentacles), 2 = phone report (full textures, simpler tentacles)
  const rnd = (s => () => (s = (s * 16807) % 2147483647) / 2147483647)(9137);
  const VIO = 0xb45cff, VIO2 = 0xd9a0ff, CORE = 0xf3dcff;

  /* ---------- shared textures ---------- */
  function cv(w, h) { const c = document.createElement("canvas"); c.width = w; c.height = h; return c; }
  function plateTex(key, opt = {}) { // panel plating: colour map + emissive map (violet slits) + roughness
    key += "@" + LOD; if (cache[key]) return cache[key]; const N = opt.n || (LOD === 1 ? 256 : 512), c = cv(N, N), e = cv(N, N), r = cv(N, N), x = c.getContext("2d", { willReadFrequently: true }), y = e.getContext("2d"), z = r.getContext("2d");
    x.fillStyle = opt.base || "#44424b"; x.fillRect(0, 0, N, N); y.fillStyle = "#000"; y.fillRect(0, 0, N, N); z.fillStyle = "#6a6a6a"; z.fillRect(0, 0, N, N);
    const rows = opt.rows || 6; let yy = 0;
    for (let i = 0; i < rows; i++) { const hh = N / rows; let xx = 0;
      while (xx < N) { const ww = (opt.cols ? N / opt.cols : 28 + rnd() * 70); const sh = 56 + rnd() * 34 | 0, bz = !opt.pal && rnd() < (opt.bronze ?? .14) * .6;
        x.fillStyle = opt.pal ? shade(opt.pal[rnd() * opt.pal.length | 0], .78 + rnd() * .4) : bz ? `rgb(${118 + rnd() * 22 | 0},${96 + rnd() * 16 | 0},${70 + rnd() * 12 | 0})` : `rgb(${sh},${sh},${sh + 5})`; x.fillRect(xx + 1, yy + 1, ww - 2, hh - 2);
        z.fillStyle = bz ? "#4a4a4a" : `rgb(${90 + rnd() * 60 | 0},0,0)`.replace(/rgb\((\d+),0,0\)/, (m, v) => `rgb(${v},${v},${v})`); z.fillRect(xx + 1, yy + 1, ww - 2, hh - 2);
        x.fillStyle = "rgba(255,255,255,.08)"; x.fillRect(xx + 1, yy + 1, ww - 2, 2); x.fillStyle = "rgba(0,0,0,.35)"; x.fillRect(xx + 1, yy + hh - 3, ww - 2, 2);
        if (rnd() < (opt.slits ?? .3)) { const sw = ww * (.25 + rnd() * .45), sx = xx + (ww - sw) / 2, sy = yy + hh * (.35 + rnd() * .3), sl = Math.max(2, hh * .07);
          x.fillStyle = opt.sc || "#d8b8ff"; x.fillRect(sx, sy, sw, sl); y.fillStyle = opt.sg || "#c066ff"; y.fillRect(sx, sy, sw, sl); y.globalAlpha = .35; y.fillStyle = opt.sg || "#aa46ff"; y.fillRect(sx - 3, sy - 3, sw + 6, sl + 6); y.globalAlpha = 1; }
        if (rnd() < .25) { x.fillStyle = "rgba(20,16,30,.6)"; for (let k = 0; k < 3; k++) x.fillRect(xx + 6 + k * 9, yy + 6, 5, 5); }
        xx += ww; }
      x.fillStyle = "rgba(10,8,18,.9)"; x.fillRect(0, yy, N, 2); yy += N / rows; }
    if (opt.rust) for (let i = 0; i < N / 5; i++) { const px = rnd() * N, py = rnd() * N; x.fillStyle = `rgba(${80 + rnd() * 60 | 0},${34 + rnd() * 26 | 0},${12 + rnd() * 10 | 0},${.12 + rnd() * .3})`; x.beginPath(); x.ellipse(px, py, 3 + rnd() * 14, 2 + rnd() * 8, rnd() * 3, 0, TAU); x.fill();
      if (rnd() < .5) { x.fillRect(px, py, 1 + rnd() * 2, 8 + rnd() * 40); } z.fillStyle = "rgba(230,230,230,.5)"; z.fillRect(px - 4, py - 3, 8, 6); }
    if (opt.veins) for (let i = 0; i < opt.veins; i++) { let px = rnd() * N, py = rnd() * N, a = rnd() * TAU; const w = .8 + rnd() * 2.4, P = [[px, py]];
      for (let k = 0; k < 26; k++) { a += (rnd() - .5) * 1.1; px += Math.cos(a) * N / 70; py += Math.sin(a) * N / 70; P.push([px, py]); }
      const ln = (c, lw, al) => { c.globalAlpha = al; c.lineWidth = lw; c.beginPath(); P.forEach(([u, v], k) => k ? c.lineTo(u, v) : c.moveTo(u, v)); c.stroke(); c.globalAlpha = 1; };
      x.strokeStyle = opt.vc || "#b080ff"; ln(x, w, .9); y.strokeStyle = opt.sg || "#c066ff"; ln(y, w * 3.2, .25); ln(y, w, 1); }
    // relief: panels raised, seams and light slits sunk; a Sobel pass turns it into a normal map
    { const d = x.getImageData(0, 0, N, N).data, H = new Float32Array(N * N);
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
  function shade(hex, k) { const n = parseInt(hex.slice(1), 16); return `rgb(${Math.min(255, (n >> 16 & 255) * k) | 0},${Math.min(255, (n >> 8 & 255) * k) | 0},${Math.min(255, (n & 255) * k) | 0})`; }
  function radial(key, stops) { if (cache[key]) return cache[key]; const c = cv(128, 128), x = c.getContext("2d"), g = x.createRadialGradient(64, 64, 0, 64, 64, 64); stops.forEach(([o, col]) => g.addColorStop(o, col)); x.fillStyle = g; x.fillRect(0, 0, 128, 128); const t = new TH.CanvasTexture(c); return cache[key] = t; }
  function swirlTex() { if (cache.swirl) return cache.swirl; const N = 256, c = cv(N, N), x = c.getContext("2d"); x.fillStyle = "#000"; x.fillRect(0, 0, N, N); x.translate(N / 2, N / 2);
    for (let i = 0; i < 900; i++) { const a = rnd() * TAU, r0 = rnd() * N * .48, sp = .9 + rnd() * 1.4; x.strokeStyle = `rgba(${170 + rnd() * 80 | 0},${70 + rnd() * 90 | 0},255,${.05 + rnd() * .12})`; x.lineWidth = 1 + rnd() * 2.5; x.beginPath();
      for (let k = 0; k < 14; k++) { const rr = r0 * (1 - k * .045), aa = a + k * .09 * sp; const px = Math.cos(aa) * rr, py = Math.sin(aa) * rr; k ? x.lineTo(px, py) : x.moveTo(px, py); } x.stroke(); }
    const t = new TH.CanvasTexture(c); t.encoding = TH.sRGBEncoding; return cache.swirl = t; }

  /* ---------- shared materials and parts ---------- */
  function hullMat(key, opt = {}) { const P = plateTex(key, opt), m = new TH.MeshStandardMaterial({ map: P.map, roughnessMap: P.rough, normalMap: P.nrm, normalScale: new TH.Vector2(1.4, 1.4), metalness: opt.metal ?? .9, roughness: opt.rough ?? .32, emissive: 0xffffff, emissiveMap: P.emi, emissiveIntensity: opt.ei ?? 2.8, envMapIntensity: .9 });
    if (opt.rep) for (const t of [P.map, P.rough, P.emi, P.nrm]) { t.repeat.set(opt.rep[0], opt.rep[1]); } m.userData.P = P; rimOn(m, opt.rim ?? 1, opt.rc); if (opt.side) m.side = TH.DoubleSide; return m; }
  // violet rim light baked into the shader: edges facing away from the camera glow, so the bosses read in any scene
  function rimOn(m, k, rc) { m.customProgramCacheKey = () => "bossrim"; const prev = m.onBeforeCompile; m.onBeforeCompile = sh => { if (prev) prev(sh); sh.uniforms.uRim = { value: k }; sh.uniforms.uRimC = { value: new TH.Vector3(...(rc || [.62, .26, 1])) }; m.userData.rim = sh.uniforms.uRim;
      sh.fragmentShader = "uniform float uRim; uniform vec3 uRimC;\n" + sh.fragmentShader.replace("#include <emissivemap_fragment>", "#include <emissivemap_fragment>\n float fr = pow(1. - clamp(abs(dot(normalize(vViewPosition), normal)), 0., 1.), 4.5);\n totalEmissiveRadiance += uRimC * fr * .45 * uRim;"); }; }
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
    g.userData.flat = 1; return g; }
  function bandGlow(R, h, phi0 = 0, phiL = TAU, c = VIO2) { const g = new TH.Group(); g.add(new TH.Mesh(new TH.CylinderGeometry(R, R, h, 96, 1, true, phi0, phiL), glowMat(c, .95)));
    g.add(new TH.Mesh(new TH.CylinderGeometry(R, R, h * 2.0, 96, 1, true, phi0, phiL), glowMat(VIO, .1))); g.userData.flat = 1; return g; }
  function crystal(prof, sides = 6) { return new TH.Mesh(new TH.LatheGeometry(prof.map(([r, y]) => new TH.Vector2(r, y)), sides), crystalMat()); }
  function shard(r, h, mat) { const g = new TH.ConeGeometry(r, h, 4); g.translate(0, h / 2, 0); return new TH.Mesh(g, mat); }
  // lightning: jagged lines between point pairs, re-struck several times a second
  function bolts(grp, n, pick, col = VIO2) { const S = 13, g = new TH.BufferGeometry(), P = new Float32Array(n * S * 6), C = new Float32Array(n * S * 6), c0 = new TH.Color(col), nx = new Float32Array(n);
    g.setAttribute("position", new TH.BufferAttribute(P, 3)); g.setAttribute("color", new TH.BufferAttribute(C, 3));
    const l = new TH.LineSegments(g, new TH.LineBasicMaterial({ vertexColors: true, transparent: true, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); l.frustumCulled = false; grp.add(l); const q = [];
    return (t, rate = 1) => { let up = false; for (let i = 0; i < n; i++) { if (t < nx[i]) continue; nx[i] = t + (60 + rnd() * 220) / rate; up = true; const [a, b] = pick(), d = a.distanceTo(b), on = rnd() < .25 ? 0 : .55 + rnd() * .45;
        for (let k = 0; k < 14; k++) { const f = k / 13, j = (k === 0 || k === 13) ? 0 : d * .09; q[k * 3] = a.x + (b.x - a.x) * f + (rnd() - .5) * j; q[k * 3 + 1] = a.y + (b.y - a.y) * f + (rnd() - .5) * j; q[k * 3 + 2] = a.z + (b.z - a.z) * f + (rnd() - .5) * j; }
        for (let k = 0; k < S; k++) { const o = (i * S + k) * 6; for (let e = 0; e < 3; e++) { P[o + e] = q[k * 3 + e]; P[o + 3 + e] = q[k * 3 + 3 + e]; } for (let e = 0; e < 2; e++) { C[o + e * 3] = c0.r * on; C[o + e * 3 + 1] = c0.g * on; C[o + e * 3 + 2] = c0.b * on; } } }
      if (up) { g.attributes.position.needsUpdate = true; g.attributes.color.needsUpdate = true; } }; }
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
  function wave(par, R, sphere, col = VIO2) { const m = new TH.Mesh(sphere ? new TH.SphereGeometry(R, 32, 16) : new TH.RingGeometry(R * .9, R, 96), glowMat(col, 0)); m.userData.dyn = 1; if (!sphere) m.rotation.x = -Math.PI / 2; m.visible = false; par.add(m);
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
    const cr = crystal([[0, 0], [.75, .5], [1.25, 2.6], [1.5, 4.7], [1.3, 6.4], [.75, 7.9], [0, 10.2]], 6); cr.position.y = 1.9; cr.userData.dyn = 1; grp.add(cr);
    const inner = crystal([[0, 0], [.4, .6], [.7, 4.4], [.35, 7.6], [0, 9.2]], 6); inner.material = glowMat(0x9a40ff, .22); inner.userData.dyn = 1; inner.position.y = 2.0; grp.add(inner);
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
    [[3.45, .28], [2.8, .83], [2.12, 1.38]].forEach(([r, y]) => { for (let k = 0; k < 4; k++) for (let j = -1; j <= 1; j++) { const F = new TH.Group(); F.userData.flat = 1; F.rotation.y = k * Math.PI / 2; const v = box(.45, .22, .16, M); v.position.set(j * r * .5, y, r * Math.SQRT1_2 + .04); F.add(v); const vg = box(.3, .05, .04, glowMat(VIO2, .9)); vg.position.set(j * r * .5, y, r * Math.SQRT1_2 + .13); F.add(vg); grp.add(F); } });
    // light
    const core = sprite(7, "rgba(190,110,255,1)"); core.position.y = 5; grp.add(core); const base = sprite(6, "rgba(190,100,255,1)"); base.position.y = 1.2; grp.add(base);
    const crPts = () => { const y = 2.5 + rnd() * 6.5, a = rnd() * TAU; return V(Math.cos(a) * .9, y, Math.sin(a) * .9); };
    const ringPt = () => { const g = rings[rnd() * 3 | 0], a = rnd() * TAU, R = g === rings[1] ? 4.4 : g === rings[0] ? 3.2 : 3.8; return V(Math.cos(a) * R, g.position.y, Math.sin(a) * R); };
    const bt = bolts(grp, 22, () => rnd() < .75 ? [crPts(), ringPt()] : [ringPt(), V((rnd() - .5) * 5, .4, (rnd() - .5) * 5)]);
    // moves: charge (rings spin up and spread, the crown opens), discharge (a bolt up from the tip, a ring shockwave),
    // link (a feed beam out along +x: the Overlord's shield), hit
    const shk = new TH.Group(), body = new TH.Group(); body.add(...grp.children); shk.add(body); grp.add(shk);
    const up1 = new TH.Mesh(new TH.CylinderGeometry(.25, .7, 40, 16, 1, true), glowMat(0xd090ff, .6)), up2 = new TH.Mesh(new TH.CylinderGeometry(.1, .25, 40, 12, 1, true), glowMat(0xf6e6ff, .95)); for (const b of [up1, up2]) { b.position.y = 12.1 + 20; b.visible = false; b.userData.dyn = 1; body.add(b); }
    const tipS = sprite(5, "rgba(240,210,255,1)", "hot2"); tipS.position.y = 12; body.add(tipS);
    const lnk = new TH.Group(); lnk.position.y = 9; body.add(lnk); const lb = new TH.Mesh(new TH.CylinderGeometry(.18, .18, 1, 10, 1, true), glowMat(0xd090ff, .7)); lb.rotation.z = -Math.PI / 2; lb.userData.dyn = 1; lb.geometry.translate(0, .5, 0); lnk.add(lb); lnk.visible = false; lnk.userData.len = 30;
    const sw = wave(body, 5, false); body.children[body.children.length - 1].position.y = 5;
    const mv = moves({ charge: 2600, discharge: 1800, link: 4000, hit: 520 }), hit = hitKit(body, shk);
    const tick = t => { const fc = mv.f("charge", t), fd = mv.f("discharge", t), fl = mv.f("link", t), fh = mv.f("hit", t), ch = Math.max(bell(fc, 0, .7, .9, 1), bell(fd, 0, .01, .2, .5));
      const spin = 1 + ch * 9; rings[0].userData.a = (rings[0].userData.a || 0) + .00022 * 16 * spin; rings[1].userData.a = (rings[1].userData.a || 0) - .00015 * 16 * spin; rings[2].userData.a = (rings[2].userData.a || 0) + .0001 * 16 * spin;
      rings.forEach((r, i) => { r.rotation.y = r.userData.a; r.userData.y0 ??= r.position.y; r.position.y = r.userData.y0 + Math.sin(t * .0011 + i * 2) * .12 + (i - 1) * ch * .8 + (i === 2 ? ch * .9 : 0); });
      for (const ag of rings[2].userData.arcs) { const c = ag.userData.c, o = ch * .9 + Math.sin(t * .0013) * .05; ag.position.set(Math.sin(c) * o * 1.3, o * .4, Math.cos(c) * o * 1.3); ag.rotation.set(Math.cos(c) * o * .35, 0, -Math.sin(c) * o * .35); }
      const hov = Math.sin(t * .0012) * .15 + ch * .5; cr.position.y = 1.9 + hov; inner.position.y = 2.0 + hov; cr.rotation.y = t * .0002 + ch * t * .002;
      const p = .85 + Math.sin(t * .004) * .15 + ch * .9; cr.material.emissiveIntensity = .8 * p + .15; inner.material.opacity = Math.min(.9, .2 * p); core.material.opacity = Math.min(1, .35 * p); core.scale.setScalar(7 * (1 + ch * .5));
      const fire = bell(fd, .15, .2, .55, .9); for (const b of [up1, up2]) b.visible = fire > .01; up1.material.opacity = .6 * fire * (.8 + rnd() * .2); up2.material.opacity = fire; tipS.material.opacity = .3 + ch * .7; tipS.scale.setScalar(5 * (1 + fire * 1.5)); sw(fd < 0 ? -1 : (fd - .18) / .6);
      const lk = Math.max(bell(fl, 0, .1, .9, 1), api.feed ? .7 : 0); lnk.visible = lk > .01; if (lnk.visible) { lb.scale.set(1 + Math.sin(t * .03) * .25, lnk.userData.len * (fl >= 0 ? ss(0, .15, fl) : 1), 1 + Math.sin(t * .03) * .25); lb.material.opacity = .75 * lk * (.8 + Math.sin(t * .02) * .2); }
      bt(t, 1 + ch * 5 + lk * 2); hit(bell(fh, 0, .05, .4, 1), t); };
    const api = { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), link: lnk, feed: 0, r: 6.5, h: 11.5 }; bake(body); return api; }

  /* ---------- Void Warden: a black, crackling void sphere inside a gyroscope of plated rings (one carved with glyphs),
     two great horned crescents left and right, crystal pylons above and below, and small ring-satellites ---------- */
  function warden() { const grp = new TH.Group(), M = hullMat("ward", { rows: 5, bronze: .22, rep: [18, 1] }), MG = hullMat("wardg", { rows: 1, cols: 16, slits: 0, glyphs: 1, bronze: .3, rep: [3, 1] });
    const core = new TH.Mesh(new TH.SphereGeometry(2.0, 48, 32), new TH.MeshBasicMaterial({ color: 0x07000f })); core.userData.dyn = 1; grp.add(core); const cor = new TH.Mesh(new TH.RingGeometry(2.0, 3.1, 64), new TH.MeshBasicMaterial({ map: radial("corona", [[0, "rgba(255,255,255,0)"], [.62, "rgba(255,255,255,0)"], [.66, "rgba(230,170,255,1)"], [.75, "rgba(170,70,255,.7)"], [1, "rgba(90,20,200,0)"]]), transparent: true, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); cor.userData.dyn = 1; grp.add(cor);
    const shell = new TH.Mesh(new TH.SphereGeometry(2.15, 48, 32), new TH.MeshBasicMaterial({ map: swirlTex(), transparent: true, opacity: .95, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); shell.userData.dyn = 1; grp.add(shell);
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
    const b1 = new TH.Mesh(new TH.CylinderGeometry(1.2, 1.6, 44, 24, 1, true), glowMat(0xb060ff, .5)), b2 = new TH.Mesh(new TH.CylinderGeometry(.35, .5, 44, 16, 1, true), glowMat(0xf6e6ff, .9)); for (const b of [b1, b2]) { b.rotation.x = Math.PI / 2; b.position.z = 22; b.visible = false; b.userData.dyn = 1; body.add(b); }
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
    bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 10, h: 15 }; }

  /* ---------- Pyramid Overlord: a monumental pyramid of layered armour plates on six walking legs. Each face carries the
     ring-and-diamond sigil with a light channel down to the apex; the stepped underbelly pours a violet beam.
     Moves: walk (tripod gait), beam (rears back, the front sigil fires), stomp (front legs rise and slam, ground shockwave),
     summon (belly claws open, the down-beam surges), hit. ---------- */
  function overlord() { const grp = new TH.Group(), shk = new TH.Group(), body = new TH.Group(); grp.add(shk); shk.add(body);
    const M = hullMat("ovl", { rows: 6, bronze: .16, slits: .35, rep: [1, 1] }), MP = hullMat("ovlp", { rows: 3, slits: .55, bronze: .3, rep: [1, 1] }), ML = hullMat("ovl2", { rows: 5, slits: .4, rep: [2, 3] }), MD = hullMat("ovld", { rows: 8, base: "#26242c", slits: .2, rep: [3, 2] });
    const B = 4.3, H = 5.8, y0 = .45, Ls = Math.hypot(B, H), phi = Math.atan2(B, H);
    const core = new TH.Mesh(new TH.ConeGeometry(B * Math.SQRT2, H, 4, 1), MD); core.rotation.y = Math.PI / 4; core.position.y = y0 + H / 2; body.add(core);
    const sigils = [];
    for (let k = 0; k < 4; k++) { const F = new TH.Group(); F.userData.flat = 1; F.rotation.y = k * Math.PI / 2; body.add(F); const S = new TH.Group(); S.userData.flat = 1; S.position.set(0, y0, B); S.rotation.x = -phi; F.add(S);
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
      for (let k = 0; k < 4; k++) for (let j = -3; j <= 3; j++) { const F = new TH.Group(); F.userData.flat = 1; F.rotation.y = k * Math.PI / 2; const v = box(.7, .35, .25, M); v.position.set(j * 1.15, y0 - .25, B * 1.0 + .08); F.add(v); body.add(F); } }
    // stepped underbelly, emitter rings, eight hanging claws, and the beam
    const belly = new TH.Group(); belly.userData.flat = 1; body.add(belly);
    [[3.9, 3.3, .6, -.45], [3.1, 2.4, .6, -1.05], [2.3, 1.6, .5, -1.6]].forEach(([a, b, h, y]) => { const m = new TH.Mesh(new TH.CylinderGeometry(a, b, h, 8), ML); m.position.y = y; belly.add(m); const g = new TH.Mesh(new TH.CylinderGeometry(b * 1.01, b * 1.01, .06, 8, 1, true), glowMat(VIO2)); g.position.y = y - h / 2 + .04; belly.add(g); });
    const emit = new TH.Group(); emit.position.y = -1.9; belly.add(emit); for (const [R, w] of [[1.5, .09], [1.05, .07], [.6, .06]]) { const r = new TH.Mesh(new TH.TorusGeometry(R, w, 8, 48), glowMat(VIO2)); r.rotation.x = Math.PI / 2; emit.add(r); }
    const claws = []; for (let k = 0; k < 8; k++) { const a = k * TAU / 8 + TAU / 16, h = new TH.Group(); h.position.set(Math.cos(a) * 2.6, -1.4, Math.sin(a) * 2.6); h.rotation.y = -a; const c = horn(1.6, .5, .16, M); c.rotation.z = -Math.PI / 2 - .25; h.add(c); belly.add(h); claws.push(h); }
    const bm = new TH.Mesh(new TH.CylinderGeometry(.35, 1.1, 9, 24, 1, true), glowMat(0xc070ff, .45)); bm.position.y = -6.4; bm.userData.dyn = 1; belly.add(bm);
    const bm2 = new TH.Mesh(new TH.CylinderGeometry(.12, .32, 9, 16, 1, true), glowMat(0xf0d8ff, .8)); bm2.position.y = -6.4; bm2.userData.dyn = 1; belly.add(bm2); const em = sprite(4.5); em.position.y = -2.0; belly.add(em);
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
    const fb1 = new TH.Mesh(new TH.CylinderGeometry(.9, .55, 40, 24, 1, true), glowMat(0xc070ff, .5)), fb2 = new TH.Mesh(new TH.CylinderGeometry(.3, .2, 40, 16, 1, true), glowMat(0xf6e6ff, .9)); for (const b of [fb1, fb2]) { b.rotation.x = Math.PI / 2; b.position.z = 20; b.userData.dyn = 1; fBeam.add(b); }
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
    bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 12, h: 16 }; }

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
      const h = new TH.Group(); h.rotation.x = a; h.position.x = x; const m = new TH.Mesh(scy(len, 1.0 + rnd() * .8), MB); m.position.y = R - .2; m.rotation.z = Math.PI - (.35 + rnd() * .35); m.scale.y = -1; m.userData.dyn = 1; h.add(m); body.add(h); blades.push({ h, m, ph: rnd() * TAU, z0: m.rotation.z }); }
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
    const vort = new TH.Mesh(new TH.CircleGeometry(2.4, 48), vmat); vort.userData.dyn = 1; vort.rotation.y = Math.PI / 2; maw.add(vort); const vort2 = new TH.Mesh(vort.geometry, vmat.clone()); vort2.userData.dyn = 1; vort2.material.opacity = .6; vort2.rotation.y = Math.PI / 2; vort2.scale.setScalar(.72); vort2.position.x = .15; maw.add(vort2);
    const hot = sprite(4.2, "rgba(250,225,255,1)", "hot"); hot.position.x = .4; maw.add(hot); const glow = sprite(9); glow.position.x = .2; maw.add(glow);
    const mb1 = new TH.Mesh(new TH.CylinderGeometry(1.4, 1.9, 44, 24, 1, true), glowMat(0xc070ff, .5)), mb2 = new TH.Mesh(new TH.CylinderGeometry(.45, .6, 44, 16, 1, true), glowMat(0xf6e6ff, .9)); for (const b of [mb1, mb2]) { b.rotation.z = -Math.PI / 2; b.position.x = 22; b.visible = false; b.userData.dyn = 1; maw.add(b); }
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
    // galaxy-map build: each tentacle is one tapered tube that writhes in the vertex shader (lash and splay drive its amplitude)
    const TW = { t: 0, amp: 1, lash: 0 };
    if (LOD) { const TL = hullMat("tent", { rows: 3, cols: 4, bronze: .1, slits: .22, rep: [1, 1], ei: 2.4, base: "#34323c", rim: .6 }); TL.side = TH.DoubleSide; const rim = TL.onBeforeCompile; TL.customProgramCacheKey = () => "bossrim-tent"; TL.onBeforeCompile = sh => { rim(sh); sh.uniforms.uT = { value: 0 }; sh.uniforms.uA = { value: 1 }; sh.uniforms.uL = { value: 0 }; TL.userData.sh = sh;
        sh.vertexShader = "uniform float uT, uA, uL; attribute float aPh;\n" + sh.vertexShader.replace("#include <begin_vertex>", "#include <begin_vertex>\n float s = uv.x; transformed += vec3(uL * s * s * 6.0, sin(uT * 1.1 + s * 6.0 + aPh) * uA, cos(uT * .9 + s * 5.0 + aPh * 1.3) * uA) * s * s * 1.6;"); };
      const tube = (x0, dir, len, r0, k) => { const pts = [], d = V(dir.x, dir.y, dir.z).normalize(), side = V(0, -d.z, d.y).normalize(), R = rad(x0) * .88, o = V(x0, dir.y * R, dir.z * R), curl = (rnd() < .5 ? 1 : -1) * (2 + rnd() * 2);
        for (let i = 0; i <= 12; i++) { const f = i / 12, p = o.clone().addScaledVector(d, f * len).addScaledVector(side, Math.sin(f * curl) * len * .18); p.x -= f * f * len * .25; pts.push(p); }
        const g = new TH.TubeGeometry(new TH.CatmullRomCurve3(pts), 48, r0, 9, false), P = g.attributes.position;
        for (let i = 0; i <= 48; i++) { let cx = 0, cy = 0, cz = 0; for (let j = 0; j < 10; j++) { const q = i * 10 + j; cx += P.getX(q); cy += P.getY(q); cz += P.getZ(q); } cx /= 10; cy /= 10; cz /= 10;
          const sc = 1 - .85 * (i / 48); for (let j = 0; j < 10; j++) { const q = i * 10 + j; P.setXYZ(q, cx + (P.getX(q) - cx) * sc, cy + (P.getY(q) - cy) * sc, cz + (P.getZ(q) - cz) * sc); } }
        g.computeVertexNormals(); g.setAttribute("aPh", new TH.BufferAttribute(new Float32Array(P.count).fill(k * 1.7), 1)); const m = new TH.Mesh(g, TL); m.userData.dyn = 1; m.frustumCulled = false; body.add(m); };
      for (let k = 0; k < 8; k++) { const a = k * TAU / 8 + .3; tube(1.6 - (k % 4) * 1.9, V(-1.1, Math.cos(a) - .35, Math.sin(a)), 13 + rnd() * 5, .9, k); }
      for (let k = 0; k < 6; k++) { const a = k * TAU / 6; tube(2.9, V(.55, Math.cos(a), Math.sin(a)), 5 + rnd() * 2, .42, k + 8); }
      TW.mat = TL; }
    else for (let k = 0; k < 8; k++) { const a = k * TAU / 8 + .3, x0 = 1.6 - (k % 4) * 1.9; tent(12 + rnd() * 6, 15, .85 + rnd() * .2, x0, V(-1.1, Math.cos(a) - .35, Math.sin(a)), (rnd() < .5 ? 1 : -1) * (.1 + rnd() * .09), false); }
    if (!LOD) for (let k = 0; k < 6; k++) { const a = k * TAU / 6, x0 = 2.9; tent(4.5 + rnd() * 2, 9, .42, x0, V(.55, Math.cos(a), Math.sin(a)), (rnd() < .5 ? 1 : -1) * (.12 + rnd() * .08), true); }
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
      if (TW.mat && TW.mat.userData.sh) { const u = TW.mat.userData.sh.uniforms; u.uT.value = t * .001; u.uA.value = 1 + splay * .8 + (fl >= 0 ? bell(fl, .1, .3, .5, .9) * 1.2 : 0); u.uL.value = fl >= 0 ? -bell(fl, 0, .15, .2, .4) * .4 + bell(fl, .25, .4, .55, .9) : 0; }
      vort.rotation.x = -t * (.0012 + fire * .01); vort2.rotation.x = t * (.002 + fire * .012); hot.material.opacity = .8 + Math.sin(t * .007) * .2; hot.scale.setScalar(4.2 * (1 + fire * 1.4 + gapeM * .3)); glow.material.opacity = .7 + fire * .3;
      for (const b of [mb1, mb2]) b.visible = fire > .01; mb1.material.opacity = .5 * fire * (.85 + rnd() * .15); mb2.material.opacity = .9 * fire; mb1.scale.set(1 + fire * .25, 1, 1 + fire * .25);
      roarW(fr < 0 ? -1 : fr * 1.3); bt(t, 1 + flare * 5 + fire * 3); hit(bell(fh, 0, .05, .4, 1), t); };
    bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 15, h: 18 }; }

  /* ---------- helpers for the Wednesday bosses: instancing, soft particles, tapered tubes, painted textures ---------- */
  const _m = () => new TH.Matrix4(), _M = {}; let _sc = null;
  function scr() { if (!_sc) _sc = { m: new TH.Matrix4(), q: new TH.Quaternion(), p: new TH.Vector3(), s: new TH.Vector3(1, 1, 1), e: new TH.Euler(), v: new TH.Vector3(), w: new TH.Vector3(), c: new TH.Color(), Y: new TH.Vector3(0, 1, 0), Z: new TH.Vector3(0, 0, 1), X: new TH.Vector3(1, 0, 0) }; return _sc; }
  function inst(geo, mat, n) { const m = new TH.InstancedMesh(geo, mat, n); m.userData.dyn = 1; m.frustumCulled = false; m.instanceMatrix.setUsage(TH.DynamicDrawUsage); return m; }
  // soft round particles with their own size and alpha (smoke, flashes, droplets, eyes); sizes are in model units
  function puffs(n, col, add = true, tex = null) { const g = new TH.BufferGeometry(); g.setAttribute("position", new TH.BufferAttribute(new Float32Array(n * 3), 3)); g.setAttribute("aS", new TH.BufferAttribute(new Float32Array(n), 1)); g.setAttribute("aA", new TH.BufferAttribute(new Float32Array(n), 1));
    const m = new TH.ShaderMaterial({ uniforms: { map: { value: tex || radial("puff", [[0, "rgba(255,255,255,1)"], [.3, "rgba(255,255,255,.55)"], [1, "rgba(255,255,255,0)"]]) }, uC: { value: new TH.Color(col) }, uH: { value: 600 } },
      vertexShader: "attribute float aS, aA; varying float vA; uniform float uH; void main() { vA = aA; vec4 mv = modelViewMatrix * vec4(position, 1.); float k = length(modelViewMatrix[0].xyz); gl_PointSize = aA > .003 ? aS * k * projectionMatrix[1][1] * uH * .5 / max(.1, -mv.z) : 0.; gl_Position = projectionMatrix * mv; }",
      fragmentShader: "uniform sampler2D map; uniform vec3 uC; varying float vA; void main() { vec4 c = texture2D(map, gl_PointCoord); gl_FragColor = vec4(uC * c.rgb, c.a * vA); }",
      transparent: true, depthWrite: false, blending: add ? TH.AdditiveBlending : TH.NormalBlending });
    const p = new TH.Points(g, m), v2 = new TH.Vector2(); p.frustumCulled = false; p.userData.dyn = 1; const vp = new TH.Vector4(); p.onBeforeRender = r => { r.getDrawingBufferSize(v2); r.getCurrentViewport(vp); m.uniforms.uH.value = vp.w || v2.y; };
    const P = g.attributes.position.array, S = g.attributes.aS.array, A = g.attributes.aA.array;
    p.put = (i, x, y, z, s, a) => { P[i * 3] = x; P[i * 3 + 1] = y; P[i * 3 + 2] = z; S[i] = s; A[i] = a; }; p.done = () => { g.attributes.position.needsUpdate = true; g.attributes.aS.needsUpdate = true; g.attributes.aA.needsUpdate = true; }; return p; }
  // a tube along points that tapers to a tip
  function taper(pts, r0, seg = 22, rs = 7, end = .06) { const g = new TH.TubeGeometry(new TH.CatmullRomCurve3(pts), seg, r0, rs, false), P = g.attributes.position, k = rs + 1;
    for (let i = 0; i <= seg; i++) { let cx = 0, cy = 0, cz = 0; for (let j = 0; j < k; j++) { const q = i * k + j; cx += P.getX(q); cy += P.getY(q); cz += P.getZ(q); } cx /= k; cy /= k; cz /= k;
      const s = Math.max(end, 1 - i / seg); for (let j = 0; j < k; j++) { const q = i * k + j; P.setXYZ(q, cx + (P.getX(q) - cx) * s, cy + (P.getY(q) - cy) * s, cz + (P.getZ(q) - cz) * s); } }
    g.computeVertexNormals(); return g; }
  function bladeGeo(len, wid, th = .16) { const s = new TH.Shape(); s.moveTo(0, 0); s.quadraticCurveTo(len * .45, wid * 1.2, len, wid * .15); s.quadraticCurveTo(len * .5, wid * .45, 0, 0);
    const g = new TH.ExtrudeGeometry(s, { depth: th, bevelEnabled: true, bevelThickness: th * .35, bevelSize: th * .35, bevelSegments: 1, curveSegments: 14 }); g.translate(0, 0, -th / 2); return g; }
  function aimAt(o, a, b, axis) { const S = scr(); o.position.copy(a); S.v.copy(b).sub(a); const L = S.v.length() || 1e-3; o.quaternion.setFromUnitVectors(axis || S.Y, S.v.divideScalar(L)); return L; }
  function paint(key, N, fn, srgb = true) { if (cache[key]) return cache[key]; const c = cv(N, N), x = c.getContext("2d"); fn(x, N); const t = new TH.CanvasTexture(c); if (srgb) t.encoding = TH.sRGBEncoding; t.wrapS = t.wrapT = TH.RepeatWrapping; return cache[key] = t; }
  const veinTex = (key, bg, col, n) => paint(key, 256, (x, N) => { x.fillStyle = bg; x.fillRect(0, 0, N, N); x.strokeStyle = col;
    for (let i = 0; i < n; i++) { let px = rnd() * N, py = rnd() * N, a = rnd() * TAU; x.globalAlpha = .45 + rnd() * .55; x.lineWidth = .7 + rnd() * 2.6; x.beginPath(); x.moveTo(px, py); for (let k = 0; k < 30; k++) { a += (rnd() - .5) * .9; px += Math.cos(a) * 6; py += Math.sin(a) * 6; x.lineTo(px, py); } x.stroke(); } x.globalAlpha = 1; });
  // an accretion disc: concentric streaks of hot gas, white-gold inside fading to orange and violet at the rim (planar ring UVs)
  const accTex = () => paint("acc", 512, (x, N) => { x.fillStyle = "#000"; x.fillRect(0, 0, N, N); x.translate(N / 2, N / 2);
    for (let i = 0; i < 2600; i++) { const f = Math.pow(rnd(), .8), r = N * (.12 + f * .37), a = rnd() * TAU, L = .2 + rnd() * 1.1, hot = 1 - f;
      x.strokeStyle = hot > .7 ? `rgba(255,${235 + rnd() * 20 | 0},${200 + rnd() * 50 | 0},${.18 + rnd() * .3})` : hot > .35 ? `rgba(255,${130 + rnd() * 80 | 0},${40 + rnd() * 50 | 0},${.14 + rnd() * .25})` : `rgba(${170 + rnd() * 80 | 0},${60 + rnd() * 50 | 0},${200 + rnd() * 55 | 0},${.08 + rnd() * .2})`;
      x.lineWidth = .6 + rnd() * 2.4; x.beginPath(); x.arc(0, 0, r, a, a + L); x.stroke(); } });
  const galTex = () => paint("gal", 128, (x, N) => { x.fillStyle = "#000"; x.fillRect(0, 0, N, N); x.translate(N / 2, N / 2);
    const g = x.createRadialGradient(0, 0, 0, 0, 0, N / 2); g.addColorStop(0, "rgba(255,230,200,.95)"); g.addColorStop(.25, "rgba(255,140,90,.45)"); g.addColorStop(.6, "rgba(150,60,220,.25)"); g.addColorStop(1, "rgba(40,10,80,0)"); x.fillStyle = g; x.fillRect(-N, -N, 2 * N, 2 * N);
    for (let i = 0; i < 400; i++) { const r = rnd() * N * .48, a = r * .09 + (i % 2) * Math.PI + (rnd() - .5) * .6; x.fillStyle = `rgba(255,${180 + rnd() * 75 | 0},${200 + rnd() * 55 | 0},${.3 + rnd() * .6})`; x.fillRect(Math.cos(a) * r, Math.sin(a) * r, 1 + rnd() * 1.5, 1 + rnd() * 1.5); } });
  function ringSprite(sz, key, stops) { const s = new TH.Sprite(new TH.SpriteMaterial({ map: radial(key, stops), blending: TH.AdditiveBlending, depthWrite: false, transparent: true, toneMapped: false })); s.scale.set(sz, sz, 1); return s; }
  function cry(r, h, mat, sides = 6) { const m = crystal([[0, 0], [r, h * .12], [r * .9, h * .74], [0, h]], sides); if (mat) m.material = mat; return m; }

  /* ---------- Brood Matriarch: a Hive queen of black chitin split by toxic green veins, rising from a living nest mound. Behind her
     hangs a translucent egg sac with embryos moving inside; she has two great scythe forelimbs, six spider legs, a crowned skull
     with mandibles and a fan of antennae crackling with green lightning, brood eggs round the nest, and a swarm of drones.
     Moves: hatch (the sac squeezes and bursts a drone swarm out), acid (she rears and sprays a stream of acid), slam (the
     scythes rise and smash down in a shockwave), hit. ---------- */
  function matriarch() { const grp = new TH.Group(), shk = new TH.Group(), body = new TH.Group(); grp.add(shk); shk.add(body);
    const GRN = 0xa8ff3a, GRN2 = 0xe2ff9e, RC = [.5, 1, .16];
    const MC = hullMat("brd", { rows: 7, pal: ["#2e2b20", "#25231a", "#383322", "#1f1d16"], slits: .2, sc: "#e0ff90", sg: "#9dff2a", veins: 16, vc: "#a6e640", metal: .55, rough: .22, rc: RC, ei: 2.4, rep: [3, 2] });
    const MB = hullMat("brdb", { rows: 3, pal: ["#1b1a14", "#24221a", "#2e2a1c"], slits: .08, sc: "#e0ff90", sg: "#9dff2a", veins: 10, vc: "#a6e640", metal: .5, rough: .18, rc: RC, ei: 2.2, rep: [1, 2], side: 1 });
    // the nest mound she stands on: a hump of resin and chitin with roots hanging beneath and acid pools glowing on top
    const MN = hullMat("brdn", { rows: 5, pal: ["#16150f", "#1c1a12", "#121109"], slits: 0, sg: "#7ad020", veins: 22, vc: "#5e9a1c", metal: .15, rough: .8, rc: RC, rim: .4, ei: 1.6, rep: [5, 1] });
    { const pr = [[0, -3.4], [3.6, -3.1], [6.6, -2.3], [8.4, -1.2], [8.8, -.5], [8.2, -.1], [5, .2], [0, .3]]; body.add(new TH.Mesh(new TH.LatheGeometry(pr.map(([r, y]) => new TH.Vector2(r + (rnd() - .5) * .3, y)), 26), MN));
      for (let k = 0; k < 16; k++) { const a = rnd() * TAU, r = 3 + rnd() * 5, h = new TH.Mesh(new TH.IcosahedronGeometry(.6 + rnd() * .9, 0), MN); h.position.set(Math.cos(a) * r, .1, Math.sin(a) * r); h.scale.y = .5; body.add(h); }
      for (let k = 0; k < 11; k++) { const a = k * TAU / 11 + rnd() * .3, r = 5 + rnd() * 3, P = V(Math.cos(a) * r, -1.8, Math.sin(a) * r); body.add(new TH.Mesh(taper([P, P.clone().add(V(Math.cos(a) * 1.5, -2.4, Math.sin(a) * 1.5)), P.clone().add(V(Math.cos(a) * 1.2, -4.8 - rnd() * 2, Math.sin(a) * 1.2 + .8))], .45 + rnd() * .25, 12, 6), MN)); }
      for (let k = 0; k < 7; k++) { const a = rnd() * TAU, r = 2.5 + rnd() * 5.2, p = new TH.Mesh(new TH.CircleGeometry(.6 + rnd() * 1.1, 18), glowMat(0x5ac010, .35)); p.rotation.x = -Math.PI / 2; p.position.set(Math.cos(a) * r, .3 + (r < 5 ? .05 : -.08 * (r - 5)), Math.sin(a) * r); body.add(p); } }
    // brood eggs round the rim of the nest, some split open
    const eggM = new TH.MeshStandardMaterial({ color: 0x1e3406, emissive: 0x9cff30, emissiveIntensity: .5, emissiveMap: veinTex("eggv", "#081002", "#d8ff70", 30), metalness: .2, roughness: .2, transparent: true, opacity: .8, envMapIntensity: .5 });
    const eggs = new TH.Group(); body.add(eggs); const eggP = []; const NE = LOD === 1 ? 8 : 13;
    for (let k = 0; k < NE; k++) { const a = k * TAU / NE + rnd() * .25, r = 6.4 + rnd() * 2.2, s = .75 + rnd() * .6, y = r > 8.2 ? -.7 : -.15 + .25 * (8.2 - r) / 2, e = new TH.Mesh(new TH.SphereGeometry(1, 20, 14), eggM);
      e.scale.set(s, s * 1.35, s); e.position.set(Math.cos(a) * r, y + s * 1.15, Math.sin(a) * r); e.rotation.z = (rnd() - .5) * .3; eggs.add(e); eggP.push(e.position.clone());
      if (k % 3 === 1) for (let q = 0; q < 4; q++) { const sh = new TH.Mesh(new TH.SphereGeometry(s * 1.02, 8, 6, q * 1.6, 1.1, 0, 1.3), eggM); sh.position.copy(e.position).add(V(0, s * .2, 0)); sh.rotation.set(rnd() * .8, 0, (rnd() - .5) * .9); eggs.add(sh); } }
    const eggG = puffs(NE, GRN); body.add(eggG);
    // the egg sac: a veined translucent shell, a glowing interior and curled embryos that turn inside it
    const sac = new TH.Group(); sac.position.set(0, 5.2, -4.6); sac.scale.setScalar(1.12); body.add(sac);
    const emb = [], eM = new TH.MeshBasicMaterial({ color: 0x1a3006, transparent: true, opacity: .92 });
    for (let k = 0; k < 6; k++) { const g = new TH.Group(), a = k * TAU / 6; g.position.set(Math.cos(a) * 1.9, k % 2 ? .9 : -1, Math.sin(a) * 2.3); g.rotation.set(rnd() * TAU, rnd() * TAU, 0); g.userData.y0 = g.position.y;
      const b = new TH.Mesh(new TH.SphereGeometry(.85, 12, 8), eM); b.scale.set(1, .7, 1.35); g.add(b); const tl = new TH.Mesh(taper([V(0, 0, -.6), V(0, -.6, -1.3), V(0, -1.2, -.6), V(0, -.9, .2)], .32, 12, 6), eM); g.add(tl);
      for (let q = 0; q < 3; q++) { const l = new TH.Mesh(taper([V(0, -.2, .5 - q * .45), V(.7, -.5, .6 - q * .45), V(.5, -.9, .9 - q * .45)], .08, 6, 4), eM); g.add(l); const l2 = l.clone(); l2.scale.x = -1; g.add(l2); }
      sac.add(g); emb.push(g); }
    const sacI = new TH.Mesh(new TH.SphereGeometry(3.75, 28, 20), glowMat(0x6cff10, .22)); sacI.userData.dyn = 1; sac.add(sacI);
    const sacM = new TH.MeshStandardMaterial({ color: 0x4f8a14, emissive: 0x9cff30, emissiveIntensity: .9, emissiveMap: veinTex("sacv", "#0a1203", "#e0ff80", 46), metalness: .05, roughness: .1, transparent: true, opacity: .6, envMapIntensity: 1.5, depthWrite: false });
    const sacS = new TH.Mesh(new TH.SphereGeometry(4.25, 44, 30), sacM); sacS.userData.dyn = 1; sac.add(sacS); const SC = [1, .92, 1.22]; sacS.scale.set(...SC); sacI.scale.set(...SC);
    const sacG = sprite(15, "rgba(160,255,60,1)", "gsac"); sac.add(sacG);
    // chitin ribs gripping the top of the sac, spiked along their crests
    for (let k = 0; k < 5; k++) { const zz = -3.4 + k * 1.55, R = 4.25 * Math.sqrt(Math.max(.12, 1 - Math.pow(zz / (4.25 * 1.22), 2))) + .2, r = new TH.Mesh(new TH.TorusGeometry(R, .3, 7, 30, Math.PI * 1.1), MC); r.rotation.z = -.05 * Math.PI; r.scale.y = .92; r.position.z = zz; sac.add(r);
      for (let q = 0; q < 3; q++) { const a = Math.PI / 2 + (q - 1) * .55, s = shard(.22, 1 + rnd() * .9, MB); s.position.set(Math.cos(a) * R, Math.sin(a) * R * .92, zz); s.rotation.z = a - Math.PI / 2; sac.add(s); } }
    // thorax: a tall armoured body leaning forward, shell plates front and back, spines down the back and veins of light
    const tho = new TH.Group(); tho.position.set(0, 6.6, .4); tho.rotation.x = .28; tho.scale.setScalar(1.18); body.add(tho);
    { const pr = [[0, -2.8], [1.7, -2.4], [2.5, -1], [2.7, .6], [2.3, 2.4], [1.6, 3.6], [1, 4.4], [0, 4.7]]; tho.add(new TH.Mesh(new TH.LatheGeometry(pr.map(([r, y]) => new TH.Vector2(r, y)), 14), MC));
      for (let i = 0; i < 7; i++) { const y = -2.3 + i * 1, R = [2.5, 2.7, 2.8, 2.7, 2.4, 2.0, 1.5][i]; for (let q = 0; q < 9; q++) { const a = q * TAU / 9 + i * .35, pl = new TH.Mesh(bladeGeo(1.6 + rnd() * 1.2, .7, .16), MB);
          pl.position.set(Math.sin(a) * R, y, Math.cos(a) * R); pl.rotation.set(0, a - Math.PI / 2, 1.3 + rnd() * .3); tho.add(pl); } }
      for (let i = 0; i < 10; i++) { const s = shard(.42, 2.4 + rnd() * 2.6, MB); s.position.set(i % 2 ? .6 : -.6, -2.2 + i * .7, -2.2 + i * .1); s.rotation.set(-.8 - rnd() * .5, 0, (i % 2 ? -1 : 1) * .3); tho.add(s); }
      for (const sx of [-1, 1]) for (let i = 0; i < 4; i++) { const s = shard(.3, 1.3 + rnd() * 1.1, MB); s.position.set(sx * 2.55, -1.3 + i * 1.15, -.3); s.rotation.set(-.3, 0, -sx * (1.05 + rnd() * .35)); tho.add(s); }
      for (const sx of [-.8, 0, .8]) tho.add(strut(V(sx, -2.1, 2.6), V(sx * .55, 3.3, 1.55), .07, .04, glowMat(GRN, .9))); }
    // skull: elongated and crowned with swept-back spikes, four eyes, two hinged mandibles, a glowing throat
    const head = new TH.Group(); head.position.set(0, 4.5, .8); head.scale.setScalar(1.3); tho.add(head);
    { const pr = [[0, -.6], [1.15, -.2], [1.45, 1], [1.25, 2.4], [.75, 3.4], [.28, 4], [0, 4.15]], sk = new TH.Mesh(new TH.LatheGeometry(pr.map(([r, y]) => new TH.Vector2(r, y)), 12), MC); sk.rotation.x = Math.PI / 2 - .2; sk.scale.set(1, 1, .78); head.add(sk);
      for (let k = 0; k < 9; k++) { const s = shard(.26, 2.4 + rnd() * 2.6 - Math.abs(k - 4) * .25, MB); s.position.set((k - 4) * .28, .95, -.2); s.rotation.set(-1.15 - rnd() * .2, 0, (k - 4) * .14); head.add(s); }
      for (const sx of [-1, 1]) { const s = shard(.3, 2, MB); s.position.set(sx * 1.2, .2, .6); s.rotation.set(-1.4, 0, -sx * .7); head.add(s); } }
    const eyes = puffs(6, GRN2); head.add(eyes); [[-.5, .55, 2.85], [.5, .55, 2.85], [-.95, .3, 2.2], [.95, .3, 2.2], [-.3, .85, 2.3], [.3, .85, 2.3]].forEach((p, i) => eyes.put(i, ...p, i < 2 ? 1.6 : 1, 1)); eyes.done();
    const mand = []; for (const sx of [-1, 1]) { const g = new TH.Group(); g.position.set(sx * .75, -.45, 3.1); head.add(g); g.add(new TH.Mesh(taper([V(0, 0, 0), V(sx * .5, -.3, 1.2), V(sx * .1, -.7, 2.3), V(-sx * .45, -.9, 2.6)], .3, 14, 6), MB)); for (let q = 0; q < 3; q++) { const s = shard(.08, .4, MB); s.position.set(sx * .2 - sx * q * .12, -.4 - q * .15, 1 + q * .5); s.rotation.z = sx * 1.6; g.add(s); } mand.push(g); }
    const throat = sprite(3.4, "rgba(170,255,70,1)", "gsac"); throat.position.set(0, -.35, 3.1); head.add(throat);
    // antennae: long thin feelers fanning up and back from the crown
    const ant = []; for (let k = 0; k < 6; k++) { const sx = k < 3 ? -1 : 1, j = k % 3, g = new TH.Group(); g.position.set(sx * (.35 + j * .2), .9, .5 - j * .4); head.add(g);
      const L = .62 + j * .16, pts = [V(0, 0, 0), V(sx * 1.1 * L, 2.6 * L, -.4), V(sx * 2.6 * L, 4.8 * L, -2.2 * L), V(sx * 3.6 * L, 6 * L, -4.8 * L), V(sx * 4.4 * L, 6.3 * L, -7.2 * L)], cur = new TH.CatmullRomCurve3(pts);
      g.add(new TH.Mesh(taper(pts, .17, 26, 5, .15), MB)); for (let q = 1; q < 5; q++) { const s = shard(.07, .55, MB), p = cur.getPoint(q / 5); s.position.copy(p); s.rotation.set(-1, 0, sx * .6); g.add(s); } g.userData.cur = cur; ant.push(g); }
    // scythe forelimbs: shoulder, armoured upper arm, an elbow knuckle and a long curved blade with a glowing edge
    const arms = []; for (const sx of [-1, 1]) { const sh = new TH.Group(); sh.position.set(sx * 2.4, 3, 1.1); tho.add(sh);
      sh.add(new TH.Mesh(new TH.SphereGeometry(1, 12, 9), MC)); sh.add(beam(V(0, 0, 0), V(sx * 1.9, 3.1, 1.8), 1.15, .75, .85, MC)); { const s = shard(.4, 2.4, MB); s.position.set(sx * .4, .7, -.5); s.rotation.set(-.7, 0, -sx * .7); sh.add(s); }
      const el = new TH.Group(); el.position.set(sx * 1.9, 3.1, 1.8); sh.add(el); el.add(new TH.Mesh(new TH.SphereGeometry(.72, 12, 8), MC)); { const s = shard(.3, 1.6, MB); s.position.set(0, .4, -.3); s.rotation.x = -.9; el.add(s); }
      const bl = new TH.Group(); el.add(bl); bl.rotation.set(0, -Math.PI / 2 + sx * .75, 0);
      const bm = new TH.Mesh(bladeGeo(12, 3.4, .34), MB); bm.rotation.set(0, 0, -.95); bl.add(bm); const eg = new TH.Mesh(bladeGeo(12, 3.4, .05), glowMat(GRN, .5)); eg.rotation.copy(bm.rotation); eg.scale.set(1.005, 1.025, 1.8); eg.position.y = -.05; bl.add(eg);
      for (let q = 0; q < 4; q++) { const s = shard(.18, .9, MB); s.position.set(1.5 + q * 1.4, .3 + q * .2, 0); s.rotation.z = .9; bm.add(s); }
      bl.position.x = sx * .2; arms.push({ sh, el, sx }); }
    // six spider legs
    const legs = []; [[1, 1.3, .7], [1, -.3, 0], [1, -2, -.75], [-1, 1.3, .7], [-1, -.3, 0], [-1, -2, -.75]].forEach(([sx, z, zb], i) => { const L = new TH.Group(); L.position.set(sx * 2.1, 5, z); L.rotation.y = Math.atan2(-zb, sx); body.add(L);
      L.add(beam(V(-.3, -.2, 0), V(3.9, 3.3, 0), 1.25, .8, 1, MC)); for (let q = 0; q < 2; q++) { const s = shard(.3, 1.6 + q * .5, MB); s.position.set(1.2 + q * 1.4, 1.5 + q * 1.1, 0); s.rotation.z = -.4; L.add(s); }
      const kn = new TH.Group(); kn.position.set(3.9, 3.3, 0); L.add(kn); { const s = shard(.42, 2.8, MB); s.position.y = .2; s.rotation.z = -.25; kn.add(s); }
      kn.add(beam(V(-.2, .2, 0), V(2.2, -8.1, 0), 1.0, .14, .75, MB)); for (let q = 0; q < 3; q++) { const s = shard(.16, .9, MB); s.position.set(.5 + q * .5, -1.5 - q * 1.8, 0); s.rotation.z = -1.2; kn.add(s); } kn.add(strut(V(.3, -.4, 0), V(2.05, -7.4, 0), .05, .03, glowMat(GRN, .7))); legs.push({ L, kn, ph: i * 1.1 }); });
    // the drone swarm, and the eyes that glint on every drone
    const ND = LOD === 1 ? 26 : 54, dG = new TH.OctahedronGeometry(.5, 0); dG.scale(.95, .42, 1.45); const dM = new TH.MeshStandardMaterial({ color: 0x15140f, metalness: .3, roughness: .55, emissive: 0x7cff20, emissiveIntensity: .12, envMapIntensity: .3 });
    const drones = inst(dG, dM, ND); body.add(drones); const dE = puffs(ND, GRN2); body.add(dE); const dP = []; for (let i = 0; i < ND; i++) dP.push({ r: 8 + rnd() * 9, y: 2.5 + rnd() * 11, w: (.00025 + rnd() * .0005) * (rnd() < .5 ? 1 : -1), a: rnd() * TAU, b: rnd() * TAU });
    // the acid spray: a cone from the jaws plus droplets streaming along it
    const acid = new TH.Group(); acid.position.set(0, -.4, 3.3); head.add(acid); acid.visible = false;
    for (const [r0, r1, o, c] of [[.3, 3.4, .22, 0x6cff10], [.14, 1.5, .4, 0xb8ff60]]) { const g = new TH.CylinderGeometry(r0, r1, 22, 18, 1, true); g.translate(0, 11, 0); g.rotateX(Math.PI / 2 + .25); const m = new TH.Mesh(g, glowMat(c, o)); m.userData.dyn = 1; acid.add(m); }
    const drops = puffs(90, GRN); acid.add(drops); const acidS = sprite(6, "rgba(200,255,90,1)", "gacid"); acid.add(acidS);
    const slamW = wave(body, 11, false, GRN), hatchW = wave(sac, 5, true, GRN); body.children[body.children.length - 1].position.y = .4;
    const bt = bolts(head, 9, () => { const a = ant[rnd() * 6 | 0], b = ant[rnd() * 6 | 0]; a.updateMatrix(); b.updateMatrix(); return [a.userData.cur.getPoint(.4 + rnd() * .6).applyMatrix4(a.matrix), b.userData.cur.getPoint(.4 + rnd() * .6).applyMatrix4(b.matrix)]; }, GRN2);
    const bt2 = bolts(sac, 7, () => { const p = () => { const a = rnd() * TAU, b = rnd() * Math.PI; return V(Math.cos(a) * Math.sin(b) * 4.3, Math.cos(b) * 3.9, Math.sin(a) * Math.sin(b) * 5.2); }; return [p(), p()]; }, GRN2);
    const mv = moves({ hatch: 3000, acid: 2800, slam: 1900, hit: 520 }), hit = hitKit(body, shk); const S = scr(), sacC = V(0, 5.2, -4.6);
    const tick = t => { const fh = mv.f("hatch", t), fa = mv.f("acid", t), fs = mv.f("slam", t), fx = mv.f("hit", t);
      const squeeze = bell(fh, 0, .3, .34, .42), burst = bell(fh, .34, .42, .6, 1), rear = bell(fa, 0, .22, .28, .4), spray = bell(fa, .26, .34, .84, .97), raise = bell(fs, 0, .38, .44, .5), slam = bell(fs, .44, .5, .62, .95);
      const br = Math.sin(t * .0016), k1 = 1 + br * .03 - squeeze * .14 + burst * .1; sacS.scale.set(SC[0] * k1, SC[1] * (1 + br * .03 - squeeze * .1 + burst * .08), SC[2] * k1); sacI.scale.copy(sacS.scale);
      sacM.emissiveIntensity = .85 + br * .2 + squeeze * 1.6 + burst * .9; sacG.material.opacity = Math.min(1, .5 + br * .1 + squeeze * .5 + burst * .3); sacG.scale.setScalar(15 * (1 + burst * .45 + squeeze * .2));
      emb.forEach((e, i) => { e.rotation.y += .003 + squeeze * .05; e.rotation.x = Math.sin(t * .0011 + i) * .5; e.position.y = e.userData.y0 + Math.sin(t * .002 + i) * .2; });
      tho.rotation.x = .28 + Math.sin(t * .0011) * .03 - rear * .3 + spray * .14 - raise * .18 + slam * .22; tho.rotation.z = Math.sin(t * .0008) * .03;
      head.rotation.x = -rear * .45 + spray * .38 + Math.sin(t * .0013) * .05; head.rotation.y = Math.sin(t * .0007) * .16 * (1 - spray);
      mand.forEach((m, i) => m.rotation.y = (i ? -1 : 1) * (.12 + Math.sin(t * .004) * .05 + spray * .55 + rear * .35 + raise * .3));
      ant.forEach((a, i) => { a.rotation.x = Math.sin(t * .0017 + i) * .08 - rear * .25 + slam * .15; a.rotation.z = Math.sin(t * .0013 + i * 2) * .07; });
      for (const a of arms) { a.sh.rotation.set(-raise * 1.15 + slam * .75 + Math.sin(t * .0012 + a.sx) * .06, 0, a.sx * (Math.sin(t * .0009 + a.sx) * .05 - raise * .2)); a.el.rotation.x = -raise * .7 + slam * 1.0 + spray * -.2; }
      for (const l of legs) { l.L.rotation.z = Math.sin(t * .0014 + l.ph) * .045 + slam * .1 - raise * .05; l.kn.rotation.z = Math.sin(t * .0014 + l.ph + 1) * .05 - slam * .08; }
      body.position.y = -slam * .45 + raise * .25;
      acid.visible = spray > .01; if (acid.visible) { acid.children[0].material.opacity = .22 * spray * (.8 + rnd() * .2); acid.children[1].material.opacity = .4 * spray; acidS.material.opacity = spray; acidS.scale.setScalar(6 * (1 + spray * .5));
        for (let i = 0; i < 90; i++) { const z = ((t * .028 + i * 2.37) % 22), w = z / 22 * 3.1, a = i * 2.4 + t * .003; drops.put(i, Math.cos(a) * w * ((i * 7 % 10) / 10), Math.sin(a) * w * ((i * 3 % 10) / 10) - z * .25 - z * z * .006, z, .5 + z * .05, spray * (1 - z / 22) * 1.4); } drops.done(); }
      for (let i = 0; i < ND; i++) { const d = dP[i], a = d.a + t * d.w, e = fh < 0 ? 1 : ss(.34 + (i / ND) * .3, .5 + (i / ND) * .35, fh), wob = Math.sin(t * .003 + d.b) * .8;
        S.p.set(Math.cos(a) * d.r, d.y + wob + Math.sin(t * .0011 + d.b) * 1.2, Math.sin(a) * d.r).lerp(sacC, 1 - e); S.e.set(0, -a + (d.w > 0 ? Math.PI : 0), Math.sin(t * .004 + d.b) * .3); S.q.setFromEuler(S.e); S.s.setScalar(.25 + e * .75); S.m.compose(S.p, S.q, S.s); drones.setMatrixAt(i, S.m); dE.put(i, S.p.x, S.p.y + .1, S.p.z, .7 + e * .3, .5 + .5 * Math.sin(t * .01 + i)); }
      drones.instanceMatrix.needsUpdate = true; dE.done(); dM.emissiveIntensity = .12 + burst * .6;
      eggM.emissiveIntensity = .45 + Math.sin(t * .002) * .15 + burst * .7; eggP.forEach((p, i) => eggG.put(i, p.x, p.y, p.z, 2.6, .35 + .2 * Math.sin(t * .0025 + i * 1.3) + burst * .4)); eggG.done();
      throat.material.opacity = .5 + rear * .5 + spray * .5; slamW(fs < 0 ? -1 : (fs - .48) / .52); hatchW(fh < 0 ? -1 : (fh - .38) / .62);
      bt(t, 1 + spray * 3 + rear * 4 + raise * 2); bt2(t, 1 + squeeze * 6 + burst * 2); hit(bell(fx, 0, .05, .4, 1), t); };
    bake(body); sac.traverse(o => { if (o.material === eM) o.renderOrder = 1; }); sacI.renderOrder = 2; sacS.renderOrder = 3;
    return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 13, h: 17 }; }

  /* ---------- Iron Tyrant: a pirate super-dreadnought patched together from stolen hulls. Mismatched rusted plates, decks of
     shacks and red tarps, smokestacks venting fire and black smoke, masts flying the skull flag, rows of broadside cannon, a
     giant boarding claw at the bow, captured wrecks hanging from chains below, and a red-hot turbine engine at the stern.
     Moves: broadside (both gun decks ripple-fire), claw (the arm reaches out and clamps shut), mines (a wake of spiked mines),
     hit. ---------- */
  function tyrant() { const grp = new TH.Group(), shk = new TH.Group(), body = new TH.Group(); grp.add(shk); shk.add(body); body.position.x = -2;
    const RC = [1, .42, .12], PAL = ["#7a3420", "#8c4b22", "#9a7a2a", "#4a5a66", "#6a6e70", "#8a8478", "#5a2a1c", "#a08a50", "#3c4a3a"];
    const hm = (k, pal, sl) => { const m = hullMat(k, { rows: 3, cols: 3, pal, slits: sl, sc: "#ffe0a0", sg: "#ff9a30", rust: 1, metal: .5, rough: .7, rc: RC, ei: 2.2, rep: [1, 1] }); m.envMapIntensity = .45; return m; };
    const HM = [hm("tyrR", ["#6a2a16", "#5a2414", "#74321a"], .25), hm("tyrY", ["#74581e", "#66501a", "#806224"], .2), hm("tyrS", ["#3e4c58", "#46545e", "#36424c"], .3), hm("tyrW", ["#625c52", "#58524a", "#6c665a"], .15), hm("tyrB", ["#5a3a24", "#4a3020", "#64422a"], .2)];
    const pick = () => HM[rnd() * HM.length | 0], MP = HM[0], MQ = HM[1];
    const MD = hullMat("tyrd", { rows: 4, cols: 4, pal: ["#2e2a28", "#3a3430", "#24201e", "#443a32"], slits: .18, sc: "#ffc070", sg: "#ff7a20", rust: 1, metal: .7, rough: .6, rc: RC, ei: 2, rep: [1, 1] }); MD.envMapIntensity = .4;
    const W = x => x > 9 ? 4.2 * (1 - (x - 9) / 6.5) + .7 : x < -13 ? 3.4 : 4.2, H = x => x > 9 ? 5.8 - (x - 9) * .35 : 5.8;
    // the hull: slices of salvaged ships welded nose to tail, a ram prow, a keel and patch plates bolted on askew
    for (let x = -16; x < 15; x += 1.55) { const w = W(x) * (.94 + rnd() * .14), h = H(x) + rnd() * 1.1, b = box(1.62, h, w * 2, rnd() < .75 ? pick() : MD); b.position.set(x + .78, h / 2 - 3.1 + (rnd() - .5) * .3, (rnd() - .5) * .3); body.add(b); }
    { const pr = new TH.Mesh(new TH.ConeGeometry(2.6, 5.5, 4), MD); pr.rotation.set(Math.PI / 4, 0, -Math.PI / 2); pr.position.set(17.2, -1.4, 0); pr.scale.set(1, 1, .7); body.add(pr); const kl = box(30, 1.2, 3.6, MD); kl.position.set(-1, -3.7, 0); body.add(kl); }
    for (let i = 0; i < 90; i++) { const x = -15 + rnd() * 28, side = rnd() < .5 ? -1 : 1, d = .12 + rnd() * .25, w = 1 + rnd() * 2.6, h = .6 + rnd() * 1.8, b = box(w, h, d, rnd() < .8 ? pick() : MD); b.position.set(x, -2.6 + rnd() * 5, side * (W(x) + .05 + d / 2)); b.rotation.set((rnd() - .5) * .1, 0, (rnd() - .5) * .16); body.add(b); }
    // decks: shacks, cabins and gun towers stacked on top, red tarps, a bridge tower
    const deckY = 2.75; for (let i = 0; i < 14; i++) { const x = -13 + rnd() * 21, w = 1.8 + rnd() * 3, h = 1.2 + rnd() * 2.2, d = 2.4 + rnd() * 4, b = box(w, h, d, pick()); b.position.set(x, deckY + h / 2, (rnd() - .5) * (8 - d)); body.add(b);
      if (rnd() < .5) { const b2 = box(w * .7, h * .8, d * .6, pick()); b2.position.set(x + (rnd() - .5), deckY + h + h * .4, b.position.z); body.add(b2); } }
    const tarpM = new TH.MeshStandardMaterial({ color: 0x8a1c14, roughness: .9, metalness: 0, side: TH.DoubleSide, emissive: 0x200402 });
    for (let i = 0; i < 9; i++) { const t2 = box(2 + rnd() * 3, .06, 2 + rnd() * 2, tarpM); t2.position.set(-12 + rnd() * 20, deckY + 2 + rnd() * 2, (rnd() - .5) * 5); t2.rotation.set((rnd() - .5) * .5, rnd(), (rnd() - .5) * .4); body.add(t2); }
    { const tw = box(3, 5, 3.4, MP); tw.position.set(-9, deckY + 2.5, 0); body.add(tw); const tw2 = box(4.2, 1.4, 4.6, MD); tw2.position.set(-9, deckY + 5.6, 0); body.add(tw2); const wl = box(4.25, .25, 4.65, glowMat(0xffb050, .9)); wl.position.set(-9, deckY + 5.6, 0); body.add(wl); }
    // smokestacks with fire at the top
    const stacks = [[-12, 1.2, 5.2], [-6.5, -1.4, 4.4], [-4.5, 1.6, 5.8], [-1, -.6, 4.2], [2.5, 1, 3.6]].map(([x, z, h]) => { const c = new TH.Mesh(new TH.CylinderGeometry(.62, .78, h, 10), MD); c.position.set(x, deckY + h / 2, z); body.add(c);
      const r = new TH.Mesh(new TH.TorusGeometry(.66, .12, 6, 14), MD); r.rotation.x = Math.PI / 2; r.position.set(x, deckY + h, z); body.add(r); return V(x, deckY + h + .2, z); });
    const fire = puffs(stacks.length * 6, 0xff8a30), smoke = puffs(LOD === 1 ? 30 : 60, 0x2a2624, false, paint("smk", 64, (x, N) => { for (let i = 0; i < 26; i++) { const g = x.createRadialGradient(0, 0, 0, 0, 0, 1); const cx = N / 2 + (rnd() - .5) * N * .4, cy = N / 2 + (rnd() - .5) * N * .4, r = N * (.12 + rnd() * .2); const gg = x.createRadialGradient(cx, cy, 0, cx, cy, r); gg.addColorStop(0, "rgba(255,255,255,.35)"); gg.addColorStop(1, "rgba(255,255,255,0)"); x.fillStyle = gg; x.fillRect(0, 0, N, N); } }, false));
    body.add(smoke); body.add(fire);
    // masts and flags: the skull flag on black, and torn red banners
    const flagTex = paint("skull", 256, (x, N) => { x.fillStyle = "#0c0b0b"; x.fillRect(0, 0, N, N); x.fillStyle = "#e8e0d0"; x.strokeStyle = "#e8e0d0"; x.lineCap = "round";
      x.lineWidth = 16; x.beginPath(); x.moveTo(70, 180); x.lineTo(186, 222); x.moveTo(186, 180); x.lineTo(70, 222); x.stroke(); for (const [a, b] of [[70, 180], [186, 222], [186, 180], [70, 222]]) { x.beginPath(); x.arc(a, b, 11, 0, TAU); x.fill(); }
      x.beginPath(); x.arc(128, 104, 54, 0, TAU); x.fill(); x.fillRect(100, 140, 56, 34); x.fillStyle = "#0c0b0b"; x.beginPath(); x.arc(106, 104, 15, 0, TAU); x.arc(150, 104, 15, 0, TAU); x.fill(); x.beginPath(); x.moveTo(128, 120); x.lineTo(120, 136); x.lineTo(136, 136); x.fill(); for (let i = 0; i < 4; i++) x.fillRect(106 + i * 13, 150, 4, 22);
      x.globalCompositeOperation = "destination-out"; for (let i = 0; i < 14; i++) { x.beginPath(); x.moveTo(N, rnd() * N); x.lineTo(N - 20 - rnd() * 40, rnd() * N); x.lineTo(N, rnd() * N); x.fill(); } });
    const banTex = paint("ban", 128, (x, N) => { x.fillStyle = "#8c1a14"; x.fillRect(0, 0, N, N); x.fillStyle = "#e8e0d0"; x.beginPath(); x.arc(64, 54, 18, 0, TAU); x.fill(); x.fillStyle = "#8c1a14"; x.fillRect(54, 50, 8, 8); x.fillRect(66, 50, 8, 8); x.globalCompositeOperation = "destination-out"; for (let i = 0; i < 9; i++) { x.beginPath(); x.moveTo(i * 15, N); x.lineTo(i * 15 + 7, N - 16 - rnd() * 30); x.lineTo(i * 15 + 14, N); x.fill(); } });
    const flags = []; [[-6, 0, 9, flagTex, 5, 3.4], [1, 0, 8, flagTex, 4.4, 3], [6.5, 0, 6.5, banTex, 2.4, 3.6], [-14, 0, 5.5, banTex, 2, 3]].forEach(([x, z, h, tex, fw, fh], i) => {
      const m = new TH.Mesh(new TH.CylinderGeometry(.16, .22, h, 6), MD); m.position.set(x, deckY + h / 2, z); body.add(m); const cb = box(.18, .18, 5, MD); cb.position.set(x, deckY + h * .72, z); body.add(cb);
      const vert = tex === banTex, g = new TH.PlaneGeometry(fw, fh, 12, 6); g.translate(fw / 2, 0, 0); if (vert) { g.rotateZ(-Math.PI / 2); g.translate(.2, fw / 2, 0); }
      const f = new TH.Mesh(g, new TH.MeshStandardMaterial({ map: tex, side: TH.DoubleSide, roughness: .9, metalness: 0, alphaTest: .4, emissive: 0x1a0c08 })); f.position.set(x + .15, deckY + h - (vert ? fw + .3 : fh / 2 + .2), z); f.rotation.y = vert ? Math.PI / 2 : 0; f.userData.dyn = 1; body.add(f);
      flags.push({ g, b: Float32Array.from(g.attributes.position.array), ph: i * 1.7, vert, fw }); });
    // broadside batteries: two gun decks a side, barrels on one instanced mesh, muzzle flashes and tracers
    const gunX = [], NG = 11; for (let i = 0; i < NG; i++) gunX.push(-11 + i * 1.95);
    const guns = []; for (const side of [-1, 1]) for (const y of [-1.1, 1.0]) for (const x of gunX) { const z = side * (W(x) + .25); guns.push({ x, y, z, side, f: (x + 11) / 21 * .55 + (y > 0 ? .06 : 0) + (side > 0 ? .03 : 0) }); const hs = box(1.2, .9, .5, MD); hs.position.set(x, y, z); body.add(hs); }
    const bG = new TH.CylinderGeometry(.2, .26, 2.3, 8); bG.translate(0, 1.15, 0); bG.rotateX(Math.PI / 2); const barrels = inst(bG, MD, guns.length); body.add(barrels);
    const flash = puffs(guns.length, 0xffb050), shells = puffs(guns.length * 2, 0xffc070); body.add(flash); body.add(shells);
    const trG = new TH.BufferGeometry(), trP = new Float32Array(guns.length * 6), trC = new Float32Array(guns.length * 6); trG.setAttribute("position", new TH.BufferAttribute(trP, 3)); trG.setAttribute("color", new TH.BufferAttribute(trC, 3));
    const tracers = new TH.LineSegments(trG, new TH.LineBasicMaterial({ vertexColors: true, transparent: true, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); tracers.frustumCulled = false; body.add(tracers);
    // the boarding claw: a two-jointed arm on the bow with three hooked fingers
    const arm = new TH.Group(); arm.position.set(15.5, -.6, 0); arm.scale.setScalar(1.7); arm.rotation.z = -.62; body.add(arm); arm.add(box(3, 3, 3.2, MD)); { const r = new TH.Mesh(new TH.TorusGeometry(1.5, .2, 6, 18), glowMat(0xff7a20, .8)); r.position.x = 1.4; r.rotation.y = Math.PI / 2; arm.add(r); }
    const a1 = new TH.Group(); a1.position.x = 1; arm.add(a1); a1.add(beam(V(0, 0, 0), V(6, -1.8, 0), 1.7, 1.25, 1.5, MP)); a1.add(strut(V(.4, 1, .9), V(5, -.6, .9), .2, .2, MD, 8)); a1.add(strut(V(.4, 1, -.9), V(5, -.6, -.9), .2, .2, MD, 8));
    const a2 = new TH.Group(); a2.position.set(6, -1.8, 0); a1.add(a2); { const d = new TH.Mesh(new TH.CylinderGeometry(1.1, 1.1, 2.2, 14), MD); d.rotation.x = Math.PI / 2; a2.add(d); } a2.add(beam(V(0, 0, 0), V(5.2, -1.2, 0), 1.3, 1, 1.2, MQ));
    const hand = new TH.Group(); hand.position.set(5.2, -1.2, 0); a2.add(hand); hand.add(box(2, 2, 2, MD)); const fingers = [];
    for (let k = 0; k < 3; k++) { const g = new TH.Group(); g.rotation.x = k * TAU / 3; hand.add(g); const f = new TH.Group(); f.position.set(.8, .95, 0); g.add(f); f.add(horn(4.2, 2, .5, MQ)); { const s = shard(.2, .8, MD); s.position.set(1.6, .2, 0); f.add(s); } fingers.push(f); }
    // chains and the wrecks hanging from them
    const wrecks = []; [[-9, -10.5], [-3, -12.5], [3, -10], [9, -12]].forEach(([x, y], i) => { const g = new TH.Group(); g.position.set(x, y, 0); g.scale.setScalar(1.6); body.add(g); const hb = box(3.4, 1.1, 1.3, pick()); hb.rotation.z = .3; g.add(hb);
      const cab = box(1.1, .8, .9, MD); cab.position.set(-.6, .8, 0); g.add(cab); const fin = shard(.4, 1.4, MD); fin.position.set(-1.5, .2, 0); fin.rotation.z = 1.3; g.add(fin); const en = new TH.Mesh(new TH.CylinderGeometry(.4, .5, .8, 8), MD); en.rotation.z = Math.PI / 2; en.position.x = -1.9; g.add(en);
      wrecks.push({ g, top: V(x, -3.8, 0), ph: i * 1.9, y }); });
    const NL = 11, link = new TH.TorusGeometry(.22, .07, 5, 8), links = inst(link, MD, wrecks.length * 2 * NL + 2 * 7); body.add(links);
    // the stern turbine: an armoured drum, glowing red-hot throat with spinning vanes, and an exhaust plume
    const eng = new TH.Group(); eng.position.set(-18.4, .3, 0); body.add(eng);
    eng.scale.setScalar(1.25); for (const x of [-.75, .75]) { const r = new TH.Mesh(new TH.TorusGeometry(3.95, .16, 6, 30), glowMat(0xff3a10, .9)); r.rotation.y = Math.PI / 2; r.position.x = x; eng.add(r); }
    { const d = new TH.Mesh(new TH.CylinderGeometry(3.7, 3.9, 3.2, 22), MD); d.rotation.z = Math.PI / 2; eng.add(d); for (const x of [-1.5, 0, 1.5]) { const r = new TH.Mesh(new TH.TorusGeometry(3.9, .3, 6, 26), MD); r.rotation.y = Math.PI / 2; r.position.x = x; eng.add(r); }
      for (let k = 0; k < 8; k++) { const a = k * TAU / 8, p = box(1.6, .5, .5, MP); p.position.set(.4, Math.cos(a) * 4.1, Math.sin(a) * 4.1); p.rotation.x = a; eng.add(p); } }
    const throatM = glowMat(0xff3a10, .95), th1 = new TH.Mesh(new TH.CircleGeometry(3.1, 32), throatM); th1.rotation.y = -Math.PI / 2; th1.position.x = -1.62; th1.userData.dyn = 1; eng.add(th1);
    const th2 = new TH.Mesh(new TH.RingGeometry(2.4, 3.6, 32), glowMat(0xffa040, .7)); th2.rotation.y = -Math.PI / 2; th2.position.x = -1.66; th2.userData.dyn = 1; eng.add(th2);
    const vanes = new TH.Group(); vanes.position.x = -1.7; eng.add(vanes); for (let k = 0; k < 12; k++) { const v = box(.12, 2.9, .5, MD); v.position.set(0, Math.cos(k * TAU / 12) * 1.5, Math.sin(k * TAU / 12) * 1.5); v.rotation.x = -k * TAU / 12; v.rotation.y = .5; vanes.add(v); } vanes.add(new TH.Mesh(new TH.CylinderGeometry(.6, .6, .5, 12).rotateZ(Math.PI / 2), MD));
    const engS = sprite(14, "rgba(255,90,30,1)", "gred"); engS.position.x = -2.4; eng.add(engS); const engS2 = sprite(13, "rgba(255,80,30,1)", "gred"); engS2.material.opacity = .45; eng.add(engS2);
    const plume = new TH.Group(); plume.position.x = -1.8; eng.add(plume); for (const [r0, r1, o, c] of [[2.6, .4, .35, 0xff5a18], [1.3, .1, .7, 0xffd090]]) { const g = new TH.CylinderGeometry(r1, r0, 10, 16, 1, true); g.translate(0, -5, 0); g.rotateZ(-Math.PI / 2); const m = new TH.Mesh(g, glowMat(c, o)); m.userData.dyn = 1; plume.add(m); }
    // a few deck lights and window glows
    const lights = puffs(40, 0xffb060); body.add(lights); for (let i = 0; i < 40; i++) lights.put(i, -14 + rnd() * 26, deckY + .4 + rnd() * 5, (rnd() < .5 ? -1 : 1) * (1 + rnd() * 3.4), .6 + rnd() * .6, .6 + rnd() * .4); lights.done();
    // mines
    const NM = 8, mineG = (() => { const parts = [new TH.IcosahedronGeometry(.7, 0)]; for (let k = 0; k < 10; k++) { const g = new TH.ConeGeometry(.1, .7, 4); g.translate(0, .9, 0); const d = V(rnd() - .5, rnd() - .5, rnd() - .5).normalize(); g.applyMatrix4(new TH.Matrix4().makeRotationFromQuaternion(new TH.Quaternion().setFromUnitVectors(V(0, 1, 0), d))); parts.push(g); }
      const out = new TH.BufferGeometry(), P = [], N2 = []; for (const g of parts) { const n = g.index ? g.toNonIndexed() : g; n.computeVertexNormals(); P.push(...n.attributes.position.array); N2.push(...n.attributes.normal.array); } out.setAttribute("position", new TH.Float32BufferAttribute(P, 3)); out.setAttribute("normal", new TH.Float32BufferAttribute(N2, 3)); return out; })();
    const mines = inst(mineG, new TH.MeshStandardMaterial({ color: 0x3a2620, metalness: .8, roughness: .4, emissive: 0x400800 }), NM); body.add(mines); const mineL = puffs(NM, 0xff2a20); body.add(mineL); const mD = []; for (let i = 0; i < NM; i++) mD.push(V(-1 - rnd() * .6, (rnd() - .5) * 1.4, (rnd() - .5) * 1.8));
    const d0x = k => 2.5 + k * 30, mv = moves({ broadside: 2800, claw: 2600, mines: 3800, hit: 520 }), hit = hitKit(body, shk); const S = scr();
    const tick = t => { const fb = mv.f("broadside", t), fc = mv.f("claw", t), fm = mv.f("mines", t), fx = mv.f("hit", t);
      const reach = bell(fc, 0, .35, .7, 1), open = bell(fc, .1, .3, .45, .55), clamp_ = bell(fc, .5, .6, .85, 1), heat = Math.max(bell(fm, 0, .2, .8, 1), bell(fb, 0, .1, .7, 1) * .5);
      body.rotation.x = Math.sin(t * .0007) * .03 + (fb >= 0 ? Math.sin(fb * 40) * .006 * (1 - fb) : 0); body.rotation.z = Math.sin(t * .0005) * .015; body.position.y = Math.sin(t * .0009) * .2;
      a1.rotation.z = -.12 + reach * .15 + Math.sin(t * .0011) * .03; a2.rotation.z = .25 - reach * .7; hand.rotation.x = t * .0003 + reach * 1.2; for (const f of fingers) f.rotation.z = .1 + open * .7 - clamp_ * .45 + Math.sin(t * .002) * .03;
      flags.forEach(F => { const P = F.g.attributes.position.array, B = F.b; for (let i = 0; i < P.length; i += 3) { const u = F.vert ? (B[i + 1] - (B[i + 1] - 0)) : B[i]; const along = F.vert ? (F.fw - B[i + 1]) / F.fw : B[i] / F.fw; P[i + 2] = B[i + 2] + Math.sin(t * .006 + along * 6 + F.ph) * .35 * along + Math.sin(t * .011 + B[i + 1] * 2) * .08 * along; } F.g.attributes.position.needsUpdate = true; });
      let fi = 0; stacks.forEach((p, s) => { for (let k = 0; k < 6; k++, fi++) { const a = ((t * .0016 + k / 6 + s * .37) % 1); fire.put(fi, p.x + Math.sin(k * 3 + t * .004) * .3 - a * 1.6, p.y + a * 3, p.z + Math.cos(k * 5 + t * .003) * .3, (2.6 - a * 1.6) * (1.2 + heat * .5), (1 - a) * (.8 + rnd() * .2)); } }); fire.done();
      const NS = smoke.geometry.attributes.aS.count; for (let i = 0; i < NS; i++) { const p = stacks[i % stacks.length], a = ((t * .00022 + i / NS * 3.1) % 1); smoke.put(i, p.x - a * 9 - Math.sin(i) * .5, p.y + 1 + a * 7 + Math.sin(i * 2) * .4, p.z + Math.cos(i * 3) * a * 2, 2 + a * 6, .75 * Math.sin(a * Math.PI) * (a < .1 ? a * 10 : 1)); } smoke.done();
      guns.forEach((g, i) => { const k = fb < 0 ? -1 : (fb - .12 - g.f) / .14, rec = k > 0 && k < 1 ? Math.sin(k * Math.PI) * (1 - k) : 0, fl = k > 0 && k < .5 ? 1 - k * 2 : 0;
        S.p.set(g.x, g.y, g.z - g.side * rec * .8); S.q.setFromAxisAngle(S.Y, g.side > 0 ? 0 : Math.PI); S.s.set(1, 1, 1); S.m.compose(S.p, S.q, S.s); barrels.setMatrixAt(i, S.m);
        const mz = g.z + g.side * 2.5; flash.put(i, g.x, g.y, mz + g.side * .8, 6 * fl + .01, fl); shells.put(i * 2, g.x + .1, g.y, g.z + g.side * (d0x(k)), 1.6, k > 0 && k < 1.6 ? 1 - k / 1.6 : 0); shells.put(i * 2 + 1, g.x + .2, g.y, g.z + g.side * (d0x(k) + 4), 1, k > 0 && k < 1.6 ? .6 * (1 - k / 1.6) : 0);
        const tr = k > 0 && k < 1.6 ? 1 - k / 1.6 : 0, d0 = 2.5 + k * 30, d1 = d0 + 10; trP.set([g.x, g.y, g.z + g.side * d0, g.x + .5, g.y, g.z + g.side * d1], i * 6); for (let e = 0; e < 2; e++) trC.set([1 * tr, .62 * tr, .25 * tr], i * 6 + e * 3); });
      barrels.instanceMatrix.needsUpdate = true; flash.done(); shells.done(); trG.attributes.position.needsUpdate = true; trG.attributes.color.needsUpdate = true;
      let li = 0; const chain = (a, b, n, sag) => { for (let q = 0; q < n; q++, li++) { const f = (q + .5) / n; S.p.lerpVectors(a, b, f); S.p.y -= Math.sin(f * Math.PI) * sag; S.v.subVectors(b, a).normalize(); S.q.setFromUnitVectors(S.Y, S.v); S.w.set(0, 1, 0).applyQuaternion(S.q); S.e.set(0, q % 2 ? Math.PI / 2 : 0, 0); S.q.multiply(new TH.Quaternion().setFromEuler(S.e)); S.s.set(1, 1.6, 1); S.m.compose(S.p, S.q, S.s); links.setMatrixAt(li, S.m); } };
      for (const w of wrecks) { const sw = Math.sin(t * .0009 + w.ph) * .12 + reach * .05; w.g.rotation.z = sw * .6; w.g.position.set(w.top.x + Math.sin(sw) * (w.top.y - w.y), w.y, Math.sin(t * .0007 + w.ph) * .4); for (const dz of [-.5, .5]) chain(V(w.top.x + dz * 2, w.top.y, dz), V(w.g.position.x + dz * 1.6, w.y + .6, w.g.position.z + dz * .3), NL, .3); }
      { const h0 = V(17, -1, 0), hw = hand.getWorldPosition(new TH.Vector3()); body.worldToLocal(hw); chain(V(16.5, .8, .9), hw.clone().add(V(0, 1, .9)), 7, 1.4 - reach); chain(V(16.5, .8, -.9), hw.clone().add(V(0, 1, -.9)), 7, 1.4 - reach); }
      links.instanceMatrix.needsUpdate = true;
      vanes.rotation.x = t * (.004 + heat * .02); const hp = .8 + Math.sin(t * .006) * .1 + heat * .5; engS2.material.opacity = .35 * hp; throatM.opacity = Math.min(1, .8 * hp); engS.material.opacity = Math.min(1, .6 * hp); engS.scale.setScalar(12 * (1 + heat * .4)); plume.scale.set(1 + heat * .8 + Math.sin(t * .03) * .05, 1 + heat * .3, 1 + heat * .3); plume.children[0].material.opacity = .3 + heat * .3;
      for (let i = 0; i < NM; i++) { const k0 = fm < 0 ? -1 : (fm - i * .06) / .5, on = k0 > 0, k = Math.min(1, k0), fade = fm < 0 ? 0 : 1 - ss(.85, 1, fm), d = mD[i];
        S.p.set(-20 + d.x * k * 14, -2 + d.y * k * 6, d.z * k * 8); S.e.set(t * .001 + i, t * .0013, 0); S.q.setFromEuler(S.e); S.s.setScalar(on ? Math.min(1, k0 * 3) * fade + .001 : .001); S.m.compose(S.p, S.q, S.s); mines.setMatrixAt(i, S.m);
        mineL.put(i, S.p.x, S.p.y, S.p.z, 2.2, on ? fade * (Math.sin(t * .02 + i) > 0 ? 1 : .25) : 0); } mines.instanceMatrix.needsUpdate = true; mineL.done();
      hit(bell(fx, 0, .05, .4, 1), t); };
    bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 20, h: 14 }; }

  /* ---------- Event Horizon Wyrm: a serpent of floating black-hole rings with starlight caught inside each one, coiled round a
     small black hole of its own. Its head is an armoured skull with jaws lined in fangs, a white-hot throat, a black-hole eye
     ringed by an accretion disc, and a curved glowing blade for a tail. A few of its rings blaze brighter: those are the
     vulnerable segments, and they travel along the body. Moves: coil (it tightens round the hole and a gravity well pulls in),
     lens (the jaws gape and a lance of focused light fires), sweep (the tail swings round with a burning trail), hit. ---------- */
  function wyrm() { const grp = new TH.Group(), shk = new TH.Group(), body = new TH.Group(); grp.add(shk); shk.add(body);
    const RC = [1, .5, .3], ORA = 0xffa040;
    const MA = hullMat("wym", { rows: 4, pal: ["#1a1424", "#221a2e", "#140f1c", "#2c2234"], slits: .45, sc: "#ffe0b0", sg: "#ff9a40", metal: .92, rough: .26, rc: RC, ei: 2.6, rep: [6, 1] });
    const MJ = hullMat("wymj", { rows: 5, pal: ["#1a1424", "#251c30", "#14101c"], slits: .3, sc: "#ffe0b0", sg: "#ff8a30", metal: .9, rough: .28, rc: RC, ei: 2.4, rep: [2, 1], side: 1 });
    const N = LOD === 1 ? 30 : 42, accM = () => new TH.MeshBasicMaterial({ map: accTex(), transparent: true, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false });
    const photon = (sz) => ringSprite(sz, "photon", [[0, "rgba(255,255,255,0)"], [.42, "rgba(255,255,255,0)"], [.5, "rgba(255,230,190,1)"], [.58, "rgba(255,140,70,.55)"], [1, "rgba(160,60,220,0)"]]);
    // its own black hole: a black sphere, a tilted accretion disc and the bright photon ring
    const bh = new TH.Group(); bh.position.y = -1; body.add(bh); const hole = new TH.Mesh(new TH.SphereGeometry(2.4, 32, 20), new TH.MeshBasicMaterial({ color: 0 })); hole.userData.dyn = 1; bh.add(hole);
    const disc = new TH.Mesh(new TH.RingGeometry(2.9, 10.5, 72, 1), accM()); disc.rotation.x = -Math.PI / 2 + .22; disc.userData.dyn = 1; bh.add(disc); const disc2 = new TH.Mesh(disc.geometry, accM()); disc2.rotation.x = -Math.PI / 2 + .22; disc2.scale.setScalar(.75); disc2.material.opacity = .6; disc2.userData.dyn = 1; bh.add(disc2);
    const phR = photon(10); bh.add(phR); const bhG = sprite(22, "rgba(255,150,80,1)", "gora2"); bhG.material.opacity = .35; bh.add(bhG);
    // the body: armoured rings, a glowing rim on each face, a galaxy of starlight in the middle, a light spine through them, dorsal fins
    const segs = inst(new TH.TorusGeometry(1, .21, 8, 30), MA, N), rimM = new TH.MeshBasicMaterial({ color: 0xffffff, transparent: true, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false }), rims = inst(new TH.TorusGeometry(1, .06, 5, 34), rimM, N * 2);
    const cores = inst(new TH.CircleGeometry(.85, 24), new TH.MeshBasicMaterial({ map: galTex(), transparent: true, opacity: .6, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false }), N);
    const spG = new TH.CylinderGeometry(.36, .36, 1, 10, 1, true); spG.translate(0, .5, 0); const spine = inst(spG, glowMat(0xb060ff, .3), N); const finG = new TH.ConeGeometry(.3, 1.6, 4); finG.translate(0, 1.6, 0); const fins = inst(finG, MA, N);
    for (const m of [segs, rims, cores, spine, fins]) body.add(m); for (let i = 0; i < N * 2; i++) rims.setColorAt(i, new TH.Color(1, .5, .2));
    const vuln = puffs(N, 0xffd8ff); body.add(vuln);
    // the head
    const head = new TH.Group(); body.add(head); const hd = new TH.Group(); head.add(hd); hd.scale.setScalar(1.65);
    { const pr = [[0, -2.2], [1.7, -1.8], [2.1, -.2], [1.9, 1.8], [1.3, 3.4], [.5, 4.4], [0, 4.6]], sk = new TH.Mesh(new TH.LatheGeometry(pr.map(([r, y]) => new TH.Vector2(r, y)), 14), MA); sk.rotation.x = Math.PI / 2; sk.scale.set(1.05, 1, .55); sk.position.set(0, 1.3, -.6); hd.add(sk);
      for (let k = 0; k < 5; k++) { const s = shard(.3, 1.4 + k * .3, MA); s.position.set(0, 2.1, 2.6 - k * 1.1); s.rotation.x = -1.2; hd.add(s); }
      for (let k = 0; k < 6; k++) { const sx = k < 3 ? -1 : 1, j = k % 3, h = new TH.Mesh(taper([V(sx * .8, 1.4, -.5 - j * .5), V(sx * (1.4 + j * .3), 2.4 + j * .2, -2.2 - j * .5), V(sx * (1.7 + j * .4), 2.6, -4.6 - j * .6)], .34 - j * .06, 14, 6), MA); hd.add(h); } }
    const jaws = []; for (const up of [1, -1]) { const j = new TH.Group(); j.position.set(0, up > 0 ? .55 : .1, .3); j.scale.set(1, 1, 1.35); hd.add(j);
      const pr = [[2.1, 0], [2.0, 1.5], [1.6, 3.4], [.9, 5.1], [.25, 5.9]], sh = new TH.Mesh(new TH.LatheGeometry(pr.map(([r, y]) => new TH.Vector2(r, y)), 16, up > 0 ? Math.PI / 2 : -Math.PI / 2, Math.PI), MJ); sh.rotation.x = Math.PI / 2; sh.scale.y = up > 0 ? .62 : .5; j.add(sh);
      for (let q = 0; q < 8; q++) { const z = .4 + q * .68, r = (2.1 - z * .3) * .92; for (const sx of [-1, 1]) { const f = shard(.16, .9 - q * .05, MJ); f.position.set(sx * r * Math.cos(.15), 0, z); f.rotation.set(up > 0 ? Math.PI : 0, 0, sx * up * .3); j.add(f); } }
      { const f = shard(.2, 1.3, MJ); f.position.set(0, 0, 5.5); f.rotation.x = up > 0 ? Math.PI - .4 : .4; j.add(f); }
      jaws.push({ j, up }); }
    const maw = new TH.Mesh(new TH.CircleGeometry(1.6, 32), accM()); maw.position.set(0, .35, 1.1); maw.userData.dyn = 1; hd.add(maw); const mawS = sprite(5, "rgba(255,230,190,1)", "hot3"); mawS.position.set(0, .35, 1.6); hd.add(mawS);
    const eye = new TH.Group(); eye.position.set(0, 2.3, .6); hd.add(eye); eye.add(new TH.Mesh(new TH.SphereGeometry(.75, 20, 14), new TH.MeshBasicMaterial({ color: 0 }))); const eD = new TH.Mesh(new TH.RingGeometry(.9, 2.3, 48), accM()); eD.rotation.x = -1.2; eD.userData.dyn = 1; eye.add(eD); const eP = photon(3.6); eye.add(eP);
    // the lens beam and its travelling halo rings
    const lens = new TH.Group(); lens.position.set(0, .35, 7.4); hd.add(lens); lens.visible = false; for (const [r, o, c] of [[1.2, .35, ORA], [.35, .85, 0xfff2d8]]) { const g = new TH.CylinderGeometry(r * .7, r, 50, 20, 1, true); g.translate(0, 25, 0); g.rotateX(Math.PI / 2); const m = new TH.Mesh(g, glowMat(c, o)); m.userData.dyn = 1; lens.add(m); }
    const halos = []; for (let k = 0; k < 4; k++) { const h = new TH.Mesh(new TH.TorusGeometry(2.2, .1, 6, 40), glowMat(0xffe0b0, .8)); h.userData.dyn = 1; lens.add(h); halos.push(h); } const lensS = sprite(5, "rgba(255,240,210,1)", "hot2"); lens.add(lensS);
    // the tail blade
    const tail = new TH.Group(); body.add(tail); { const b = new TH.Mesh(bladeGeo(8, 2.6, .35), MA); b.rotation.set(Math.PI / 2, 0, -Math.PI / 2 + .3); tail.add(b); const e = new TH.Mesh(bladeGeo(8, 2.6, .06), glowMat(ORA, .7)); e.rotation.copy(b.rotation); e.scale.set(1.01, 1.03, 1.5); tail.add(e); const s = sprite(4, "rgba(255,170,90,1)", "gorange"); tail.add(s); }
    const trail = puffs(48, ORA); body.add(trail); const trH = []; for (let i = 0; i < 48; i++) trH.push(V(0, 0, 0));
    const well = new TH.Mesh(new TH.RingGeometry(1, 3.2, 64), new TH.MeshBasicMaterial({ map: swirlTex(), transparent: true, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false, opacity: 0 })); well.rotation.x = -Math.PI / 2 + .22; well.userData.dyn = 1; bh.add(well);
    const bt = bolts(bh, 8, () => { const a = rnd() * TAU, b = a + (rnd() - .5); return [V(Math.cos(a) * 2.6, 0, Math.sin(a) * 2.6), V(Math.cos(b) * (4 + rnd() * 5), (rnd() - .5) * 1.5, Math.sin(b) * (4 + rnd() * 5))]; }, 0xffd0a0);
    const st = { rot: 0, coil: 0, sweep: 0, strike: 0 }, pts = []; for (let i = 0; i <= N + 1; i++) pts.push(V(0, 0, 0));
    const path = (u, t, o) => { const rear = u < .3 ? Math.pow(1 - u / .3, 2) : 0, th = st.rot - u * TAU * 1.12 + (u > .55 ? st.sweep * Math.pow((u - .55) / .45, 1.5) * 2.2 : 0), R = (10 + 2.6 * Math.sin(u * Math.PI * 1.3 + .4) + rear * 2.5) * (1 - st.coil * .34 * (1 - u * .3));
      return o.set(Math.cos(th) * R, (1 - u) * 3 - 1.8 + rear * (9 + st.strike) + Math.sin(u * 10 - t * .0016) * 1.15 * (1 - st.coil * .6) * (1 - rear), Math.sin(th) * R); };
    const mv = moves({ coil: 3000, lens: 3000, sweep: 2200, hit: 520 }), hit = hitKit(body, shk); const S = scr(), c1 = new TH.Color(), tmp = V(0, 0, 0);
    const tick = t => { const fc = mv.f("coil", t), fl = mv.f("lens", t), fs = mv.f("sweep", t), fx = mv.f("hit", t);
      const coil = bell(fc, 0, .35, .75, 1), gape = bell(fl, 0, .22, .85, 1), fire = bell(fl, .25, .3, .82, .95), swing = fs < 0 ? 0 : Math.sin(ss(0, 1, fs) * Math.PI) * (fs < .5 ? 1 : 1);
      st.rot = t * .00011; st.coil = coil; st.sweep = swing * 1.4; st.strike = gape * 2 - fire * 1.5 + Math.sin(t * .0009) * .8;
      for (let i = 0; i <= N + 1; i++) path(i / N, t, pts[i]);
      for (let i = 0; i < N; i++) { const u = i / N, sc = 2.35 * (1 - u * .62) * (i === 0 ? 1.1 : 1); S.v.subVectors(pts[i + 1], i ? pts[i - 1] : pts[i]).normalize(); S.q.setFromUnitVectors(S.Z, S.v); S.q.multiply(tmpQ.setFromAxisAngle(S.Z, u * 6 + t * .0004));
        S.s.setScalar(sc); S.m.compose(pts[i], S.q, S.s); segs.setMatrixAt(i, S.m);
        for (const e of [0, 1]) { S.w.copy(S.v).multiplyScalar((e ? .3 : -.3) * sc).add(pts[i]); S.s.setScalar(sc * 1.04); S.m.compose(S.w, S.q, S.s); rims.setMatrixAt(i * 2 + e, S.m); }
        S.s.setScalar(sc * 1.05); S.m.compose(pts[i], S.q, S.s); cores.setMatrixAt(i, S.m);
        S.w.set(0, 1, 0).addScaledVector(S.v, -S.v.y).normalize(); tmpQ2.setFromUnitVectors(S.Y, S.w); S.s.setScalar(sc * .7); S.p.copy(pts[i]).addScaledVector(S.w, sc * .9); S.m.compose(S.p, tmpQ2, S.s); fins.setMatrixAt(i, S.m);
        const L = aimAt(tmp2, pts[i], pts[i + 1]); S.s.set(sc * .7, L, sc * .7); S.m.compose(tmp2.position, tmp2.quaternion, S.s); spine.setMatrixAt(i, S.m);
        let hot = 0; for (let k = 0; k < 3; k++) { const c = ((t * .00005 + k / 3) % 1) * N; hot = Math.max(hot, 1 - Math.min(1, Math.abs(i - c) / 1.6)); }
        const b = .5 + .2 * Math.sin(t * .004 - i * .5) + fire * .3 * (1 - u) + coil * .3; c1.setRGB(b * (1 + hot * .1), b * (.5 + hot * .5), b * (.22 + hot * .9)); rims.setColorAt(i * 2, c1); rims.setColorAt(i * 2 + 1, c1);
        vuln.put(i, pts[i].x, pts[i].y, pts[i].z, sc * 4.2 * hot, hot * (.75 + .25 * Math.sin(t * .012))); }
      for (const m of [segs, rims, cores, spine, fins]) m.instanceMatrix.needsUpdate = true; rims.instanceColor.needsUpdate = true; vuln.done();
      head.position.copy(pts[0]); S.v.subVectors(pts[0], pts[1]).normalize(); head.quaternion.setFromUnitVectors(S.Z, S.v); head.rotateX(.75 - gape * .35); head.rotateZ(Math.sin(t * .0008) * .1); hd.rotation.x = -gape * .25;
      for (const J of jaws) J.j.rotation.x = -J.up * (.05 + Math.sin(t * .0021) * .03 + gape * .55 + coil * .12);
      maw.rotation.z = -t * (.002 + fire * .01); mawS.material.opacity = .6 + gape * .4; mawS.scale.setScalar(5 * (1 + fire * 1.2 + gape * .4)); eD.rotation.z = t * .0012; eP.material.opacity = .8 + Math.sin(t * .003) * .2;
      lens.visible = fire > .01; if (lens.visible) { lens.children[0].material.opacity = .45 * fire * (.85 + rnd() * .15); lens.children[1].material.opacity = .95 * fire; halos.forEach((h, k) => { const z = ((t * .03 + k * 12.5) % 50); h.position.z = z; h.scale.setScalar(1 + z * .02); h.material.opacity = .8 * fire * (1 - z / 50); }); lensS.material.opacity = fire; }
      tail.position.copy(pts[N - 1]); S.v.subVectors(pts[N - 1], pts[N - 2]).normalize(); tail.quaternion.setFromUnitVectors(S.X, S.v);
      trH.unshift(trH.pop().copy(tail.position).addScaledVector(S.v, 6)); trH.forEach((p, i) => trail.put(i, p.x, p.y, p.z, 2.6 * (1 - i / 48), swing * (1 - i / 48) * .9)); trail.done();
      disc.rotation.z = t * .0005; disc2.rotation.z = -t * .0009; phR.material.opacity = .85 + Math.sin(t * .002) * .15 + coil * .3; phR.scale.setScalar(10 * (1 + coil * .2));
      well.material.opacity = coil * .9; well.scale.setScalar(fc < 0 ? 1 : 9 - 7 * ss(0, 1, fc)); well.rotation.z = -t * .004;
      bt(t, 1 + coil * 6 + fire * 2); hit(bell(fx, 0, .05, .4, 1), t); };
    const tmpQ = new TH.Quaternion(), tmpQ2 = new TH.Quaternion(), tmp2 = new TH.Object3D();
    bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 15, h: 11 }; }

  /* ---------- Shard Colossus: a golem of dark mine rock and violet and cyan crystal, grown up out of a Void Shard mine. Great
     crystal wings fan from its back round a fractured heart that burns pink-white; a crown of shards, clawed crystal hands, a
     floating chunk of the mine under its feet, and a storm of shards circling it.
     Moves: rain (it raises its arms and shards hail down), prism (a beam from its eyes that splits and bounces), shatter (it bursts
     apart, heart exposed, and pulls back together), hit. ---------- */
  function colossus() { const grp = new TH.Group(), shk = new TH.Group(), body = new TH.Group(); grp.add(shk); shk.add(body);
    const RC = [.62, .3, 1], MR = hullMat("col", { rows: 5, pal: ["#2c2a36", "#22202c", "#34303f", "#1c1a24"], slits: .05, sc: "#e0b0ff", sg: "#b050ff", veins: 18, vc: "#a868ff", metal: .25, rough: .62, rc: RC, ei: 2.6, rep: [2, 2] });
    const CV = crystalMat(); CV.color.setHex(0x3a0c90); CV.emissive.setHex(0x8a30ff); CV.emissiveIntensity = .4; CV.roughness = .1; CV.envMapIntensity = 1.2; const CC = new TH.MeshStandardMaterial({ color: 0x0a3a56, emissive: 0x28c8ff, emissiveIntensity: .42, metalness: .5, roughness: .14, flatShading: true, transparent: true, opacity: .95, envMapIntensity: .8 }); rimOn(CC, .5, [.3, .85, 1]);
    const rock = (r, det, sx, sy, sz) => { const g = new TH.IcosahedronGeometry(r, det), P = g.attributes.position; for (let i = 0; i < P.count; i++) { const x = P.getX(i), y = P.getY(i), z = P.getZ(i), h = Math.sin(Math.round(x * 97) * 12.9898 + Math.round(y * 97) * 78.233 + Math.round(z * 97) * 37.719) * 43758.5453, k = .8 + (h - Math.floor(h)) * .34; P.setXYZ(i, x * k * sx, y * k * sy, z * k * sz); } g.computeVertexNormals(); return new TH.Mesh(g, MR); };
    const cluster = (par, p, n, len, dir, spread, mats) => { for (let i = 0; i < n; i++) { const d = dir.clone().add(V((rnd() - .5) * spread, (rnd() - .5) * spread, (rnd() - .5) * spread)).normalize(), L = len * (.55 + rnd() * .6), c = cry(L * .16, L, mats[rnd() * mats.length | 0]); c.position.copy(p).addScaledVector(d, .2); c.quaternion.setFromUnitVectors(V(0, 1, 0), d); par.add(c); } };
    // the floating chunk of the mine, crystals breaking through it
    { const pl = rock(8.5, 2, 1, .3, 1); pl.position.y = -1.5; body.add(pl); for (let k = 0; k < 9; k++) { const a = k * TAU / 9 + rnd() * .3, r = 4.5 + rnd() * 3.2; cluster(body, V(Math.cos(a) * r, -.4, Math.sin(a) * r), 3 + (rnd() * 3 | 0), 2 + rnd() * 3, V(Math.cos(a) * .5, 1, Math.sin(a) * .5), .7, [CV, CC]); }
      for (let k = 0; k < 6; k++) { const a = rnd() * TAU; cluster(body, V(Math.cos(a) * 5, -3.2, Math.sin(a) * 5), 3, 2.5, V(0, -1, 0), .6, [CV, CC]); } }
    // legs
    const parts = [], part = (g, d) => { g.userData.p0 = g.position.clone(); g.userData.d = d.normalize(); parts.push(g); return g; };
    const legs = []; for (const sx of [-1, 1]) { const hip = new TH.Group(); hip.position.set(sx * 2, 6.7, 0); body.add(hip); part(hip, V(sx, -.3, 0));
      const th = rock(1.3, 1, .95, 2.2, .95); th.position.set(sx * .3, -1.6, 0); hip.add(th); cluster(hip, V(sx * 1, -1, -.4), 3, 1.8, V(sx, .4, -.5), .6, [CV]);
      const kn = new TH.Group(); kn.position.set(sx * .5, -3.3, .2); hip.add(kn); const sh = rock(1.25, 1, 1, 2.1, 1); sh.position.y = -1.6; kn.add(sh); cluster(kn, V(0, .2, .9), 3, 1.6, V(0, .4, 1), .5, [CV, CC]);
      const ft = rock(1.4, 1, 1.25, .6, 1.6); ft.position.set(0, -3.25, .5); kn.add(ft); cluster(kn, V(0, -3.3, 1.9), 3, 1, V(0, .1, 1), .6, [CV]); legs.push({ hip, kn, sx }); }
    // torso, wings of crystal on the back, the heart in its cage
    const T = new TH.Group(); T.position.set(0, 11, 0); body.add(T); { const c = rock(3.2, 1, 1.15, 1.05, .85); T.add(c); const pv = rock(1.9, 1, 1.3, .8, 1); pv.position.y = -3.6; T.add(pv); }
    const wings = new TH.Group(); wings.position.set(0, 1, -1.8); T.add(wings); part(wings, V(0, .4, -1));
    for (const sx of [-1, 1]) for (let k = 0; k < 6; k++) { const a = .35 + k * .22, d = V(sx * Math.cos(a), Math.sin(a) + .3, -.45).normalize(), L = 6 + rnd() * 5 - Math.abs(k - 2.5) * .6, c = cry(L * .14, L, k % 2 ? CC : CV); c.position.set(sx * .8, 0, 0); c.quaternion.setFromUnitVectors(V(0, 1, 0), d); wings.add(c); }
    cluster(wings, V(0, .5, 0), 5, 4, V(0, 1, -.6), .7, [CV, CC]);
    for (const sx of [-1, 1]) cluster(T, V(sx * 2.4, -1, 1.8), 3, 1.5, V(sx * .4, .2, 1), .5, [CV]);
    const heart = new TH.Group(); heart.position.set(0, .3, 2.5); T.add(heart); const hC = new TH.Mesh(new TH.IcosahedronGeometry(1.05, 1), new TH.MeshBasicMaterial({ color: 0xffd8ff, toneMapped: false })); hC.userData.dyn = 1; heart.add(hC);
    const hS = sprite(8, "rgba(255,110,255,1)", "gpink"); heart.add(hS); const hS2 = sprite(3.2, "rgba(255,240,255,1)", "hot"); heart.add(hS2);
    { const g = new TH.BufferGeometry(), P = []; for (let k = 0; k < 9; k++) { let a = k * TAU / 9, r = .4, x = 0, y = 0; for (let q = 0; q < 5; q++) { const r2 = r + .35 + rnd() * .3, a2 = a + (rnd() - .5) * .6; P.push(Math.cos(a) * r, Math.sin(a) * r, 1.05, Math.cos(a2) * r2, Math.sin(a2) * r2, 1.05 - q * .05); r = r2; a = a2; } }
      g.setAttribute("position", new TH.Float32BufferAttribute(P, 3)); heart.add(new TH.LineSegments(g, new TH.LineBasicMaterial({ color: 0xff80ff, transparent: true, blending: TH.AdditiveBlending, toneMapped: false }))); }
    const cage = []; for (let k = 0; k < 8; k++) { const a = k * TAU / 8, g = new TH.Group(); g.rotation.z = a; heart.add(g); const c = cry(.35, 2.2, k % 2 ? CC : CV); c.position.set(0, 1.1, 0); c.rotation.x = .5; g.add(c); cage.push(g); }
    // head with a crown of shards and glowing eyes
    const head = new TH.Group(); head.position.set(0, 3.9, .5); head.scale.setScalar(1.35); T.add(head); part(head, V(0, 1, .2)); { const h = rock(1.15, 1, 1, 1.1, 1); head.add(h); cluster(head, V(0, .8, -.2), 6, 2.4, V(0, 1, -.3), .9, [CV, CC]); }
    const eyeP = puffs(2, 0xb8f4ff); head.add(eyeP); eyeP.put(0, -.42, .2, 1.02, 1.1, 1); eyeP.put(1, .42, .2, 1.02, 1.1, 1); eyeP.done();
    // arms: boulder shoulders spiked with crystal, rock limbs crusted with shards, clawed crystal hands
    const arms = []; for (const sx of [-1, 1]) { const sh = new TH.Group(); sh.position.set(sx * 3.7, 1.7, 0); T.add(sh); part(sh, V(sx, .3, 0));
      sh.add(rock(1.5, 1, 1, 1, 1)); cluster(sh, V(sx * .6, .9, 0), 4, 3.4, V(sx * .6, 1, -.2), .6, [CV, CC]);
      const up = rock(1, 1, .85, 2.2, .85); up.position.set(sx * .8, -2, 0); up.rotation.z = sx * .2; sh.add(up);
      const el = new TH.Group(); el.position.set(sx * 1.3, -4, .3); sh.add(el); const fa = rock(1.05, 1, .95, 2.1, .95); fa.position.set(0, -1.9, .4); el.add(fa); cluster(el, V(sx * .7, -1.4, .2), 4, 1.8, V(sx, .1, .2), .6, [CV, CC]);
      const hand = new TH.Group(); hand.position.set(0, -3.9, .7); el.add(hand); hand.add(rock(.95, 1, 1, .9, 1)); for (let k = 0; k < 4; k++) { const c = cry(.32, 2.3, CV); c.position.set((k - 1.5) * .45, -.4, .3); c.quaternion.setFromUnitVectors(V(0, 1, 0), V((k - 1.5) * .25, -1, .5).normalize()); hand.add(c); }
      arms.push({ sh, el, sx }); }
    // the shard storm
    const shG = new TH.OctahedronGeometry(.5, 0); shG.scale(.5, 1.7, .5); const NS = LOD === 1 ? 36 : 80, storm = inst(shG, CV, NS); body.add(storm); const sD = []; for (let i = 0; i < NS; i++) sD.push({ r: 10 + rnd() * 6, y: 4 + rnd() * 11, w: .00018 + rnd() * .0003, a: rnd() * TAU, s: .6 + rnd() * 1.2, sp: rnd() * TAU });
    const NR = LOD === 1 ? 18 : 34, rain = inst(shG, CC, NR), rainF = puffs(NR, 0x9feaff); body.add(rain); body.add(rainF); const rD = []; for (let i = 0; i < NR; i++) rD.push({ x: (rnd() - .5) * 26, z: 4 + rnd() * 20, d: rnd() * .45, s: 1 + rnd() * 1.4 });
    const NF = LOD === 1 ? 16 : 30, frag = inst(new TH.TetrahedronGeometry(.6, 0), CV, NF); body.add(frag); const fD = []; for (let i = 0; i < NF; i++) fD.push(V(rnd() - .5, rnd() - .5, rnd() * .8).normalize().multiplyScalar(5 + rnd() * 9));
    // the prism beam: three legs, each a white core in a coloured sheath, a flash at every bounce
    const prism = new TH.Group(); body.add(prism); prism.visible = false; const legsB = [], PC = [0x9ff3ff, 0xff7aff, 0xffe08a];
    for (let k = 0; k < 3; k++) { const g = new TH.Object3D(); prism.add(g); for (const [r, o, c] of [[.9, .45, PC[k]], [.28, .95, 0xffffff]]) { const cg = new TH.CylinderGeometry(r, r, 1, 14, 1, true); cg.translate(0, .5, 0); const m = new TH.Mesh(cg, glowMat(c, o)); m.userData.dyn = 1; g.add(m); } legsB.push(g); }
    const bounce = puffs(4, 0xffffff); prism.add(bounce); const BP = [V(6, 4.5, 24), V(-11, 9, 31), V(5, 3, 42)];
    const shatW = wave(T, 6, true, 0xff80ff), stompW = wave(body, 10, false, 0xb070ff); body.children[body.children.length - 1].position.y = .2;
    const bt = bolts(T, 8, () => [V((rnd() - .5) * 1.5, .3 + (rnd() - .5) * 1.5, 2.6), V((rnd() - .5) * 6, (rnd() - .5) * 5, (rnd() - .2) * 3)], 0xe0a0ff);
    const mv = moves({ rain: 2800, prism: 3000, shatter: 2800, hit: 520 }), hit = hitKit(body, shk); const S = scr(), eyeW = V(0, 0, 0);
    const tick = t => { const fr = mv.f("rain", t), fp = mv.f("prism", t), fs = mv.f("shatter", t), fx = mv.f("hit", t);
      const lift = bell(fr, 0, .25, .7, .9), aim = bell(fp, 0, .2, .85, 1), fire = bell(fp, .22, .28, .82, .95), burst = bell(fs, .15, .3, .55, .85), crouch = bell(fs, 0, .15, .2, .3), br = Math.sin(t * .0012);
      T.position.y = 11 + br * .12 - crouch * .6; T.rotation.x = br * .02 - aim * .12 + crouch * .15; T.rotation.y = Math.sin(t * .0005) * .1;
      for (const a of arms) { a.sh.rotation.set(-lift * 2.2 - aim * .5 + Math.sin(t * .001 + a.sx) * .05, 0, a.sx * (.12 + lift * .5 + crouch * .4)); a.el.rotation.x = -lift * .4 - aim * .8; }
      for (const l of legs) { l.hip.rotation.x = Math.sin(t * .0009 + l.sx) * .03 + crouch * .3; l.kn.rotation.x = -crouch * .5; }
      head.rotation.x = -aim * .15 + Math.sin(t * .0011) * .04; head.rotation.y = Math.sin(t * .0006) * .15 * (1 - aim);
      for (const g of parts) { g.position.copy(g.userData.p0).addScaledVector(g.userData.d, burst * 3.2); } wings.rotation.x = burst * .4; for (const g of cage) g.children[0].rotation.x = .5 + burst * 1.3;
      const hb = 1 + Math.sin(t * .004) * .08 + burst * .6 + fire * .2; hC.scale.setScalar(hb); hS.scale.setScalar(8 * hb * (1 + burst * .8)); hS.material.opacity = .7 + burst * .3; hS2.scale.setScalar(3.2 * hb);
      for (let i = 0; i < NS; i++) { const d = sD[i], a = d.a + t * d.w * (1 + lift * 3 + burst * 4), R = d.r * (1 + burst * .4) * (1 - lift * .2); S.p.set(Math.cos(a) * R, d.y + Math.sin(t * .001 + d.sp) * .8 + lift * 6 * (i % 2), Math.sin(a) * R * .85); S.e.set(t * .001 + d.sp, t * .0013 + i, 0); S.q.setFromEuler(S.e); S.s.setScalar(d.s); S.m.compose(S.p, S.q, S.s); storm.setMatrixAt(i, S.m); } storm.instanceMatrix.needsUpdate = true;
      for (let i = 0; i < NR; i++) { const d = rD[i], k = fr < 0 ? -1 : (fr - .3 - d.d) / .3, on = k > 0 && k < 1.2; S.p.set(d.x, 40 - Math.min(1, k) * 40, d.z); S.q.setFromAxisAngle(S.X, .25); S.s.setScalar(on && k < 1 ? d.s : .001); S.m.compose(S.p, S.q, S.s); rain.setMatrixAt(i, S.m); rainF.put(i, d.x, .2, d.z, 6, k > .95 && k < 1.2 ? (1.2 - k) * 4 : 0); } rain.instanceMatrix.needsUpdate = true; rainF.done();
      for (let i = 0; i < NF; i++) { const e = fs < 0 ? 0 : bell(fs, .15, .35, .55, .9); S.p.set(0, 11.3, 2.5).addScaledVector(fD[i], e); S.e.set(t * .004 + i, t * .003, 0); S.q.setFromEuler(S.e); S.s.setScalar(e > .01 ? .6 + e * .8 : .001); S.m.compose(S.p, S.q, S.s); frag.setMatrixAt(i, S.m); } frag.instanceMatrix.needsUpdate = true;
      prism.visible = fire > .01; if (prism.visible) { head.updateWorldMatrix(true, false); eyeW.set(0, .2, 1.1); head.localToWorld(eyeW); body.worldToLocal(eyeW); const P = [eyeW, ...BP];
        legsB.forEach((g, k) => { const L = aimAt(g, P[k], P[k + 1]); const vis = ss(k * .12, k * .12 + .1, (fp - .25) / .6); g.scale.set(1 + Math.sin(t * .05 + k) * .1, L * vis + .001, 1 + Math.sin(t * .05 + k) * .1); g.children[0].material.opacity = .45 * fire; g.children[1].material.opacity = .95 * fire; });
        P.forEach((p, k) => bounce.put(k, p.x, p.y, p.z, k ? 7 : 4, fire * (k ? ss(k * .12, k * .12 + .1, (fp - .25) / .6) : 1))); bounce.done(); }
      eyeP.put(0, -.42, .2, 1.02, 1.1 + aim * 1.4, 1); eyeP.put(1, .42, .2, 1.02, 1.1 + aim * 1.4, 1); eyeP.done();
      shatW(fs < 0 ? -1 : (fs - .2) / .7); stompW(fs < 0 ? -1 : (fs - .62) / .38); bt(t, 1 + burst * 5 + fire * 2 + lift * 2); hit(bell(fx, 0, .05, .4, 1), t); };
    bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 14, h: 18 }; }

  // merge each group's static leaf meshes that share a material (same look), so a boss costs tens of draw calls, not hundreds
  function bake(root) { const fl = []; root.traverse(o => { if (o !== root && o.userData.flat && o.parent) fl.push(o); });
    for (const o of fl.reverse()) { o.updateMatrix(); const par = o.parent; for (const c of [...o.children]) { c.applyMatrix4(o.matrix); par.add(c); } par.remove(o); }
    const work = []; root.traverse(o => { if (o.children && o.children.length) work.push(o); });
    for (const o of work) { const G = new Map();
      for (const c of o.children) { if (!c.isMesh || c.userData.dyn || c.children.length || !c.geometry || !c.geometry.attributes.position) continue; const m = c.material;
        const k = m.isMeshBasicMaterial && !m.map ? `b${m.color.getHex()}|${m.opacity}|${m.blending}|${m.side}` : m.uuid; if (!G.has(k)) G.set(k, []); G.get(k).push(c); }
      for (const [, L] of G) { if (L.length < 2) continue; let n = 0; const parts = L.map(c => { c.updateMatrix(); const g = c.geometry.index ? c.geometry.toNonIndexed() : c.geometry.clone(); g.applyMatrix4(c.matrix);
          if (!g.attributes.normal) g.computeVertexNormals(); if (!g.attributes.uv) g.setAttribute("uv", new TH.BufferAttribute(new Float32Array(g.attributes.position.count * 2), 2)); n += g.attributes.position.count; return g; });
        const P = new Float32Array(n * 3), N = new Float32Array(n * 3), U = new Float32Array(n * 2); let q = 0;
        for (const g of parts) { P.set(g.attributes.position.array, q * 3); N.set(g.attributes.normal.array, q * 3); U.set(g.attributes.uv.array, q * 2); q += g.attributes.position.count; g.dispose(); }
        const g2 = new TH.BufferGeometry(); g2.setAttribute("position", new TH.BufferAttribute(P, 3)); g2.setAttribute("normal", new TH.BufferAttribute(N, 3)); g2.setAttribute("uv", new TH.BufferAttribute(U, 2)); g2.computeBoundingSphere();
        const mesh = new TH.Mesh(g2, L[0].material); for (const c of L) o.remove(c); o.add(mesh); } } }
  // light the boss's own materials from an environment map (the galaxy scene has none); count its draw calls
  function prep(b, env) { b.grp.traverse(o => { const m = o.material; if (m && m.isMeshStandardMaterial && env) { m.envMap = env; m.needsUpdate = true; } }); return b; }
  root.BOSS3D = { init(T) { TH = T; }, set lod(v) { LOD = v | 0; }, get lod() { return LOD; }, conduit, warden, overlord, devourer, matriarch, tyrant, wyrm, colossus, prep };
})(typeof window !== "undefined" ? window : globalThis);
