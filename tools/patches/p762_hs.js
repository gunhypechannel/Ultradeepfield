  /* ---------- v760 hard-surface kit: crisp machined parts for the World Bosses, modelled to their paintings ----------
     Every part is a swept cross-section (chamfered, grooved, bladed) whose profile edges keep their own normals, so edges stay sharp
     at any size; chamfer faces carry a lighter vertex colour so the light catches them like the painted bevels; light channels are
     separate glowing inlays sitting in the grooves. No textures, no files: crisp on every screen. */
  function hsMat(base = 0x0b0812, opt = {}) { const m = new TH.MeshStandardMaterial({ color: 0xffffff, vertexColors: true, metalness: opt.metal ?? .8, roughness: opt.rough ?? .36, envMapIntensity: opt.env ?? .7 }); m.userData.hsBase = base; m.userData.hsHi = opt.hi ?? 0x3e2c3a; return m; }
  function hsGlow(c = 0xc27aff, k = 1) { return new TH.MeshBasicMaterial({ color: new TH.Color(c).multiplyScalar(k), toneMapped: false }); }
  // frames along a path: [{p, t, n, b}] (n and b span the cross-section: x of a profile point goes along n, y along b)
  function hsArc(R, a0, a1, N, plane = "xz", cx = 0, cy = 0, zf = null) { const F = [];
    for (let i = 0; i <= N; i++) { const u = i / N, a = a0 + (a1 - a0) * u, c = Math.cos(a), s = Math.sin(a);
      if (plane === "xz") F.push({ u, p: new TH.Vector3(s * R, 0, c * R), n: new TH.Vector3(s, 0, c), b: new TH.Vector3(0, 1, 0), t: new TH.Vector3(c, 0, -s).multiplyScalar(Math.sign(a1 - a0)) });
      else { const z = zf ? zf(u) : 0; F.push({ u, p: new TH.Vector3(cx + c * R, cy + s * R, z), n: new TH.Vector3(c, s, 0), b: new TH.Vector3(0, 0, 1), t: new TH.Vector3(-s, c, 0).multiplyScalar(Math.sign(a1 - a0)) }); } }
    return F; }
  function hsLine(a, b, N = 1, up = new TH.Vector3(0, 0, 1)) { const t = b.clone().sub(a).normalize(), n = new TH.Vector3().crossVectors(up, t); if (n.lengthSq() < 1e-6) n.set(1, 0, 0); n.normalize(); const bb = new TH.Vector3().crossVectors(t, n);
    const F = []; for (let i = 0; i <= N; i++) F.push({ u: i / N, p: a.clone().lerp(b, i / N), n: n.clone(), b: bb.clone(), t: t.clone() }); return F; }
  // sweep a closed profile [[x, y], ...] along frames; sc(u) scales the profile (a number or [sx, sy]); hi[j] tints edge j; caps close open ends
  function hsSweep(prof, F, opt = {}) { const m = prof.length, N = F.length, pos = [], nor = [], col = [], base = new TH.Color(opt.base ?? 0x0b0812), hiC = new TH.Color(opt.hiC ?? 0x3e2c3a), sc = opt.sc || (() => 1), cap = opt.cap !== false;
    const S = F.map(f => { const v = sc(f.u); return Array.isArray(v) ? v : [v, v]; }), off = opt.off || (() => 0);
    const P = (i, j) => { const f = F[i], [sx, sy] = S[i]; return f.p.clone().addScaledVector(f.n, prof[j][0] * sx + off(f.u)).addScaledVector(f.b, prof[j][1] * sy); };
    const HSV = new TH.Vector3(), tri = (a, b, c, na, nb, nc, cc) => { HSV.subVectors(b, a).cross(new TH.Vector3().subVectors(c, a)); const flip = HSV.dot(na.clone().add(nb).add(nc)) < 0;
      const L = flip ? [a, c, b] : [a, b, c], LN = flip ? [na, nc, nb] : [na, nb, nc]; for (let k = 0; k < 3; k++) { pos.push(L[k].x, L[k].y, L[k].z); nor.push(LN[k].x, LN[k].y, LN[k].z); col.push(cc.r, cc.g, cc.b); } };
    let ar = 0; for (let j = 0; j < m; j++) { const q = prof[j], r = prof[(j + 1) % m]; ar += q[0] * r[1] - r[0] * q[1]; } const wsg = ar > 0 ? 1 : -1; // outward = right of each edge for a counter-clockwise outline
    for (let j = 0; j < m; j++) { const j2 = (j + 1) % m, ex = prof[j2][0] - prof[j][0], ey = prof[j2][1] - prof[j][1], L = Math.hypot(ex, ey) || 1; const nx = wsg * ey / L, ny = -wsg * ex / L;
      const cc = base.clone().lerp(hiC, Math.min(1, opt.hi ? (opt.hi[j] || 0) : 0));
      for (let i = 0; i < N - 1; i++) { const a = P(i, j), b = P(i, j2), c = P(i + 1, j2), d = P(i + 1, j), [sx0, sy0] = S[i], [sx1, sy1] = S[i + 1];
        const n0 = F[i].n.clone().multiplyScalar(nx / (sx0 || 1e-3)).addScaledVector(F[i].b, ny / (sy0 || 1e-3)).normalize(), n1 = F[i + 1].n.clone().multiplyScalar(nx / (sx1 || 1e-3)).addScaledVector(F[i + 1].b, ny / (sy1 || 1e-3)).normalize();
        tri(a, b, c, n0, n0, n1, cc); tri(a, c, d, n0, n1, n1, cc); } }
    if (cap) { const tris = TH.ShapeUtils.triangulateShape(prof.map(q => new TH.Vector2(q[0], q[1])), []), cc = base.clone().lerp(hiC, .35);
      for (const [i, s] of [[0, -1], [N - 1, 1]]) { if (S[i][0] < 1e-3 && S[i][1] < 1e-3) continue; const nn = F[i].t.clone().multiplyScalar(s); for (const [a, b, c] of tris) tri(P(i, a), P(i, b), P(i, c), nn, nn, nn, cc); } }
    const g = new TH.BufferGeometry(); g.setAttribute("position", new TH.Float32BufferAttribute(pos, 3)); g.setAttribute("normal", new TH.Float32BufferAttribute(nor, 3)); g.setAttribute("color", new TH.Float32BufferAttribute(col, 3)); return g; }
  // chamfered box profile, optionally with a groove (for an inlay) centred on the outer (+x) face; returns [profile, edge tints]
  function hsProf(w, h, c = .18, groove = 0, gd = .3) { const W = w / 2, H = h / 2, C = Math.min(c * Math.min(w, h), W * .45, H * .45);
    if (!groove) return [[[-W, -H + C], [-W + C, -H], [W - C, -H], [W, -H + C], [W, H - C], [W - C, H], [-W + C, H], [-W, H - C]], [1, 0, 1, 0, 1, 0, 1, 0]];
    const G = h * groove / 2, D = w * gd; return [[[-W, -H + C], [-W + C, -H], [W - C, -H], [W, -H + C], [W, -G], [W - D, -G * .8], [W - D, G * .8], [W, G], [W, H - C], [W - C, H], [-W + C, H], [-W, H - C]], [1, 0, 1, 0, .6, 0, .6, 0, 1, 0, 1, 0]]; }
  // a ring of machined plates (gaps between them), its groove's light channel, raised caps on alternate plates; axis y
  function hsRing(R, w, h, M, G, opt = {}) { const g = new TH.Group(), n = opt.n || Math.max(8, Math.round(R * 2.2)), gap = opt.gap ?? Math.min(.06, .22 / R), each = TAU / n, sub = Math.max(3, Math.round(48 / n * (LOD === 1 ? .6 : 1)));
    const [pr, hi] = hsProf(w, h, .2, opt.groove ?? .34, .28), base = M.userData.hsBase;
    for (let i = 0; i < n; i++) { const a0 = i * each + gap / 2, a1 = (i + 1) * each - gap / 2; g.add(new TH.Mesh(hsSweep(pr, hsArc(R, a0, a1, sub), { hi, base, hiC: M.userData.hsHi }), M));
      if (opt.caps !== false && i % 2 === 0) { const [cp, ch] = hsProf(w * .55, h * .5, .3), am = (a0 + a1) / 2, da = (a1 - a0) * .32; g.add(new TH.Mesh(hsSweep(cp, hsArc(R + w * .5, am - da, am + da, 4), { hi: ch, base, hiC: M.userData.hsHi }), M)); } }
    if (G && (opt.groove ?? .34) > 0) { const gw = w * .22; g.add(new TH.Mesh(hsSweep(hsProf(gw, h * (opt.groove ?? .34) * .55, .05)[0], hsArc(R + w / 2 - w * .28 + gw * .45, 0, TAU, Math.max(48, n * 6)), { cap: false }), G)); }
    if (G && opt.faces !== false) for (const sy of [-1, 1]) g.add(new TH.Mesh(hsSweep([[-w * .035, -.01], [w * .035, -.01], [w * .035, .01], [-w * .035, .01]], hsArc(R + w * .12, 0, TAU, Math.max(48, n * 6)).map(f => (f.p.y += sy * (h / 2 + .006), f)), { cap: false }), G));
    if (opt.inner && G) g.add(new TH.Mesh(hsSweep(hsProf(.04, h * .2, 0)[0], hsArc(R - w / 2 - .02, 0, TAU, Math.max(48, n * 6)), { cap: false }), G));
    return g; }
  // runes on a band: a glowing strip of glyphs wrapped round radius R (axis y)
  function hsRunes(key, R, h, n = 24, col = "#e2b8ff") { const t = cache["rn_" + key] || (cache["rn_" + key] = (() => { const c = cv(1024, 64), x = c.getContext("2d"); x.clearRect(0, 0, 1024, 64); x.strokeStyle = col; x.lineWidth = 4; x.lineCap = "round"; x.shadowColor = col; x.shadowBlur = 6; const r = (() => { let s = 77; return () => (s = (s * 16807) % 2147483647) / 2147483647; })();
      for (let k = 0; k < 16; k++) { const cx = 32 + k * 64; x.beginPath(); x.arc(cx, 32, 18, 0, TAU); x.stroke(); x.beginPath(); for (let q = 0; q < 3; q++) { const a = r() * TAU, b = r() * TAU; x.moveTo(cx + Math.cos(a) * 14, 32 + Math.sin(a) * 14); x.lineTo(cx + Math.cos(b) * 6, 32 + Math.sin(b) * 6); } x.stroke(); }
      const tx = new TH.CanvasTexture(c); tx.wrapS = TH.RepeatWrapping; tx.encoding = TH.sRGBEncoding; return tx; })());
    const tx = t.clone(); tx.needsUpdate = true; tx.repeat.set(n / 16, 1); const m = new TH.Mesh(new TH.CylinderGeometry(R, R, h, 128, 1, true), new TH.MeshBasicMaterial({ map: tx, transparent: true, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); return m; }
  // a faceted crystal (n sides, flat facets) from a [radius, y] profile
  function hsCrystal(prof, sides = 6, col = 0x24064e, em = 0x5a14e0) { const g = new TH.LatheGeometry(prof.map(([r, y]) => new TH.Vector2(r, y)), sides); const m = new TH.MeshStandardMaterial({ color: col, emissive: em, emissiveIntensity: .55, metalness: .3, roughness: .16, flatShading: true, envMapIntensity: .4 }); return new TH.Mesh(g, m); }
  // a crescent blade in the XY plane: circle centre (cx, cy), outer radius R, from angle a0 to a1; its thickness T and depth D taper to the tips
  function hsCrescent(cx, cy, R, a0, a1, T, D, M, G, opt = {}) { const g = new TH.Group(), base = M.userData.hsBase, n = opt.plates || 7, N = LOD === 1 ? 10 : 18, zf = opt.zf || (() => 0), tp = u => Math.pow(Math.max(0, Math.sin(Math.PI * u)), opt.taper || .55);
    const prof = [[0, 0], [-.18, .42], [-.8, .5], [-1, .12], [-1, -.12], [-.8, -.5], [-.18, -.42]], hi = [1, 0, .6, 0, .6, 0, 1];
    for (let i = 0; i < n; i++) { const u0 = i / n + .004, u1 = (i + 1) / n - .004, A0 = a0 + (a1 - a0) * u0, A1 = a0 + (a1 - a0) * u1, F = hsArc(R, A0, A1, Math.ceil(N / n * 3) + 2, "xy", cx, cy, u => zf(u0 + (u1 - u0) * u));
      F.forEach(f => { f.u = u0 + (u1 - u0) * f.u; }); g.add(new TH.Mesh(hsSweep(prof, F, { hi, base, hiC: M.userData.hsHi, sc: u => [T * tp(u) + .02, D * (.35 + .65 * tp(u)) + .02] }), M)); }
    if (G) { const sc = u => [T * tp(u) + .02, D * (.35 + .65 * tp(u)) + .02]; // light channels: two along the front face, one along the inner face
      for (const [x0, x1] of [[-.6, -.555], [-.36, -.33], [-.86, -.84]]) g.add(new TH.Mesh(hsSweep([[x0, .47], [x1, .47], [x1, .53], [x0, .53]], hsArc(R, a0 + (a1 - a0) * .04, a1 - (a1 - a0) * .04, N * 3, "xy", cx, cy, zf), { sc, cap: false }), G));
      g.add(new TH.Mesh(hsSweep([[-1.02, -.07], [-.97, -.07], [-.97, .07], [-1.02, .07]], hsArc(R, a0, a1, N * 3, "xy", cx, cy, zf), { sc, cap: false }), G)); }
    return g; }
  function hsSpike(len, r, M, sides = 4) { const g = new TH.ConeGeometry(r, len, sides, 1); g.translate(0, len / 2, 0); const ng = g.toNonIndexed(); ng.computeVertexNormals(); const c = new TH.Color(M.userData.hsBase ?? 0x0b0812), a = []; for (let i = 0; i < ng.attributes.position.count; i++) a.push(c.r, c.g, c.b); ng.setAttribute("color", new TH.Float32BufferAttribute(a, 3)); return new TH.Mesh(ng, M); }
