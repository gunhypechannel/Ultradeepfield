/* v458 Divine Annihilation becomes a photon storm (owner: "can't he release some kinda photon energy storm that launches every direction and
   blankets the map, give a really good cinematic camera angle for that"). From the wheel on his back and from his jaws, hundreds of photons
   burst in every direction across the galaxy in curling streaks, each ending in a flash where it strikes; great shells of light and flat
   shock rings race outward over the whole map, god rays wheel round the core and the galaxy floods with violet and gold. It is driven by
   the attack's own clock (sec = seconds since it fired), so every commander sees the same storm at the same moment.
   The camera: low behind him as the wheel aligns, his silhouette against the charging wheel; it holds there as the storm erupts toward
   the map, then cranes up and out over the galaxy to show the whole map blanketed in light. Live, it plays only while you leave the
   map alone; touch it and the camera is yours again. */
function sbVaeStorm(W, X, b, t, kill, sec, dur) { const on = sec >= 0 && sec < dur + 3.2;
  if (!X.vs) { const NP = MOBILE ? 260 : 560, NT = 4, g = new TH.Group(); g.frustumCulled = false; X.grp.add(g);
    const r = cwRnd(9137), P = []; for (let i = 0; i < NP; i++) { let y = -.55 + r() * .85; const a = r() * TAU, h = Math.sqrt(1 - y * y), burst = i < NP * .3;
      const c = r(); P.push({ d: new TH.Vector3(Math.cos(a) * h, y, Math.sin(a) * h), v: 650 + r() * 750, L: 700 + r() * 1100, off: burst ? r() * .25 : r() * 1.6, ph: r() * TAU, cw: (r() - .5) * 2.4, sz: 10 + r() * 16, src: r() < .72 ? 0 : 1, col: c < .55 ? [.82, .62, 1] : c < .85 ? [1, .82, .45] : [1, 1, 1], boom: r() < .22 }); }
    const n = NP * (NT + 1), pg = new TH.BufferGeometry(); pg.setAttribute("position", new TH.BufferAttribute(new Float32Array(n * 3), 3)); pg.setAttribute("color", new TH.BufferAttribute(new Float32Array(n * 3), 3)); pg.setAttribute("aS", new TH.BufferAttribute(new Float32Array(n), 1));
    const pm = new TH.ShaderMaterial({ transparent: true, depthWrite: false, blending: TH.AdditiveBlending, vertexColors: true, toneMapped: false,
      vertexShader: "attribute float aS; varying vec3 vC; varying float vA; void main() { vC = color; vA = step(.01, aS); vec4 mv = modelViewMatrix * vec4(position, 1.); gl_Position = projectionMatrix * mv; gl_PointSize = clamp(aS * 520. / -mv.z, 0., 72.); }",
      fragmentShader: "varying vec3 vC; varying float vA; void main() { vec2 c = gl_PointCoord - .5; float d = length(c) * 2.; float a = (exp(-d * d * 4.) + exp(-d * d * 40.) * 1.6) * vA; if (a < .01) discard; gl_FragColor = vec4(mix(vC, vec3(1.), exp(-d * d * 30.)) * a, a); }" });
    const pts = new TH.Points(pg, pm); pts.frustumCulled = false; g.add(pts);
    const lg = new TH.BufferGeometry(); lg.setAttribute("position", new TH.BufferAttribute(new Float32Array(NP * 6), 3)); lg.setAttribute("color", new TH.BufferAttribute(new Float32Array(NP * 6), 3));
    const lines = new TH.LineSegments(lg, new TH.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: .9, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); lines.frustumCulled = false; g.add(lines);
    // the shells: great spheres of light racing outward, bright at the rim; and flat shock rings across the map beneath them
    const shellM = () => new TH.ShaderMaterial({ uniforms: { uO: { value: 0 }, uC: { value: new TH.Color(.75, .5, 1) } }, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, side: TH.DoubleSide, toneMapped: false,
      vertexShader: "varying float vR; void main() { vec4 mv = modelViewMatrix * vec4(position, 1.); vec3 n = normalize(normalMatrix * normal); vR = 1. - abs(dot(n, normalize(-mv.xyz))); gl_Position = projectionMatrix * mv; }",
      fragmentShader: "uniform float uO; uniform vec3 uC; varying float vR; void main() { float a = pow(vR, 3.) * uO; gl_FragColor = vec4(mix(uC, vec3(1.), pow(vR, 8.)) * a, a); }" });
    const shells = [], rings = []; for (let j = 0; j < 3; j++) { const m = new TH.Mesh(new TH.SphereGeometry(1, 40, 24), shellM()); m.frustumCulled = false; g.add(m); shells.push(m);
      const rg = new TH.Mesh(new TH.RingGeometry(.86, 1, 96, 1), new TH.MeshBasicMaterial({ color: j % 2 ? 0xffd890 : 0xc890ff, transparent: true, opacity: 0, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false })); rg.rotation.x = -Math.PI / 2; rg.frustumCulled = false; g.add(rg); rings.push(rg); }
    // god rays wheeling round the core, the core flash itself, and the light flooding the galaxy
    const rays = [], rayG = new TH.CylinderGeometry(0, 1, 1, 6, 1, true); rayG.translate(0, .5, 0); for (let j = 0; j < (MOBILE ? 10 : 16); j++) { const m = new TH.Mesh(rayG, new TH.MeshBasicMaterial({ color: j % 3 ? 0xd8b0ff : 0xffe0a0, transparent: true, opacity: 0, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); m.frustumCulled = false; m.userData.a = r() * TAU; m.userData.b = (r() - .5) * 1.4; m.userData.w = (r() - .5) * .5; m.userData.l = .6 + r() * .7; g.add(m); rays.push(m); }
    const wh = W.glow.wh || (W.glow.wh = glowTex("255,255,255", .85)), core = new TH.Sprite(W.additive(wh, new TH.Color("#f4e8ff"), 0)), core2 = new TH.Sprite(W.additive(wh, new TH.Color("#a050ff"), 0)); g.add(core); g.add(core2);
    const flood = []; for (let j = 0; j < 6; j++) { const s = new TH.Sprite(W.additive(wh, new TH.Color(j % 2 ? "#e0a040" : "#8a40ff"), 0)); s.renderOrder = 2; g.add(s); flood.push(s); }
    X.vs = { g, P, NP, NT, pts, lines, shells, rings, rays, core, core2, flood, src: [new TH.Vector3(), new TH.Vector3()], v: new TH.Vector3(), s: new TH.Vector3(), u: new TH.Vector3(), hit: new Set(), killed: 0 }; }
  const Z = X.vs; Z.g.visible = on; if (!on) { Z.hit.clear(); Z.killed = 0; return 0; }
  b.wheel.getWorldPosition(Z.src[0]); b.mouth.getWorldPosition(Z.src[1]); const O = Z.src[0], sc = b.grp.scale.x / 4.4;
  const k = Math.min(1, sec / .35) * (sec < dur ? 1 : Math.max(0, 1 - (sec - dur) / 3.2)), fireOn = sec < dur, PER = 1.6;
  const pp = Z.pts.geometry.attributes.position.array, pc = Z.pts.geometry.attributes.color.array, ps = Z.pts.geometry.attributes.aS.array, lp = Z.lines.geometry.attributes.position.array, lc = Z.lines.geometry.attributes.color.array;
  const at = (q, a, o, out) => { const rr = q.v * a, w = q.ph + rr * .006 * q.cw; Z.s.set(-q.d.z, 0, q.d.x).normalize(); Z.u.crossVectors(q.d, Z.s); const cu = rr * .14 * Math.min(1, rr / 300);
    return out.copy(o).addScaledVector(q.d, rr).addScaledVector(Z.s, Math.sin(w) * cu).addScaledVector(Z.u, Math.cos(w) * cu * .5); };
  for (let i = 0; i < Z.NP; i++) { const q = Z.P[i], c = Math.floor((sec - q.off) / PER), a = sec - q.off - c * PER, l0 = q.off + c * PER, o = Z.src[q.src];
    const live = c >= 0 && l0 <= dur && l0 >= 0 && q.v * a < q.L; let j = i * (Z.NT + 1);
    if (!live) { for (let m = 0; m <= Z.NT; m++) ps[j + m] = 0; lp.fill(0, i * 6, i * 6 + 6); if (q.boom && c >= 0 && l0 <= dur && q.v * a >= q.L && !Z.hit.has(i * 1000 + c)) { Z.hit.add(i * 1000 + c); if (sec - l0 < PER * 1.5) sbBoom(X, at(q, q.L / q.v, o, Z.v).clone(), t, (50 + q.sz * 6) * (.6 + sc * .4)); } continue; }
    const fade = Math.min(1, a / .08) * (1 - Math.pow(q.v * a / q.L, 4));
    for (let m = 0; m <= Z.NT; m++) { const am = Math.max(0, a - m * .05); at(q, am, o, Z.v); pp[(j + m) * 3] = Z.v.x; pp[(j + m) * 3 + 1] = Z.v.y; pp[(j + m) * 3 + 2] = Z.v.z; const f = fade * (1 - m / (Z.NT + 1)) * k;
      pc.set([q.col[0] * f, q.col[1] * f, q.col[2] * f], (j + m) * 3); ps[j + m] = q.sz * (1 - m * .17) * (.5 + .5 * k) * sc; }
    at(q, a, o, Z.v); lp.set([Z.v.x, Z.v.y, Z.v.z], i * 6); at(q, Math.max(0, a - .3), o, Z.v); lp.set([Z.v.x, Z.v.y, Z.v.z], i * 6 + 3); lc.set([q.col[0] * fade * k, q.col[1] * fade * k, q.col[2] * fade * k, 0, 0, 0], i * 6); }
  for (const A of [Z.pts.geometry.attributes.position, Z.pts.geometry.attributes.color, Z.pts.geometry.attributes.aS, Z.lines.geometry.attributes.position, Z.lines.geometry.attributes.color]) A.needsUpdate = true;
  // shells and rings: one every .55 s while it fires, each crossing the map in 2.2 s
  Z.shells.forEach((m, jj) => { const c = Math.floor((sec - jj * .55) / 1.65), l0 = jj * .55 + c * 1.65, a = (sec - l0) / 2.2, ok = c >= 0 && l0 <= dur && a < 1; m.visible = Z.rings[jj].visible = ok; if (!ok) return;
    const R = 30 + Math.pow(a, .7) * 1900; m.position.copy(O); m.scale.setScalar(R); m.material.uniforms.uO.value = (1 - a) * (1 - a) * 1.3 * Math.min(1, a * 8); const rg = Z.rings[jj]; rg.position.set(O.x, Math.min(O.y - 40, 10), O.z); rg.scale.setScalar(R * .96); rg.material.opacity = (1 - a) * .55;
    if (kill && c === 0 && jj === 0) for (let si = 0; si < X.ships.length; si++) { const sh = X.ships[si]; if (sh.dead < 0 && sh.p.distanceTo(O) < R && (si * 7919) % 10 < 8) sbKill(X, sh, t + Math.random() * 300, 44); } });
  Z.rays.forEach((m, jj) => { const u = m.userData, a = u.a + t * .00025 * (1 + jj % 3) * (jj % 2 ? -1 : 1); m.position.copy(O); m.rotation.set(Math.PI / 2 + u.b + Math.sin(t * .001 + jj) * .2, 0, a); const L = 900 * u.l * (.4 + .6 * k) * (1 + .15 * Math.sin(t * .007 + jj)); m.scale.set(5 + 9 * k, L * 1.4, 5 + 9 * k); m.material.opacity = .26 * k * (.6 + .4 * Math.sin(t * .011 + jj * 2)); });
  Z.core.position.copy(O); Z.core.scale.setScalar((120 + 40 * Math.sin(t * .03)) * (.6 + .6 * k) * sc); Z.core.material.opacity = .9 * k; Z.core2.position.copy(O); Z.core2.scale.setScalar(420 * (.6 + .6 * k) * sc); Z.core2.material.opacity = .4 * k;
  Z.flood.forEach((s, jj) => { const a = jj / 6 * TAU + t * .00005, rr = 260 + (jj % 3) * 180; s.position.set(O.x * .4 + Math.cos(a) * rr, 0, O.z * .4 + Math.sin(a) * rr); s.scale.setScalar(1300 + jj * 120); s.material.opacity = .2 * k * (.8 + .2 * Math.sin(t * .002 + jj)); });
  const cam = W.camera; if (cam && fireOn) { const amp = (sec < 1 ? (1 - sec) * 10 : 0) + 1.6 * k; cam.position.x += (Math.random() - .5) * amp; cam.position.y += (Math.random() - .5) * amp; cam.position.z += (Math.random() - .5) * amp; }
  return k; }
/* the storm's camera, by the attack's progress fa (0..1): low behind him as the wheel aligns, held as it erupts, then up and out over the galaxy */
function sbVaeCam(X, fa) { const sc = X.b.grp.scale.x || 4.4, ss2 = (a, b, x) => { const u = clamp((x - a) / (b - a), 0, 1); return u * u * (3 - 2 * u); }, P = Math.PI;
  const al = ss2(.55, .66, fa), er = ss2(.66, .72, fa), cr = ss2(.71, .86, fa), wy = 14 * sc;
  const th = .3 - al * .24 + cr * 1.0, d = 440 - al * 130 - er * 50 + cr * 2050, ph = P - .55 + al * .3 + er * .1 + cr * .5;
  return { y: wy * (1 - cr), d, th, ph, tx: X.B.x * (1 - cr * .8), tz: X.B.z * (1 - cr * .8), ty: (X.B.y + wy) * (1 - cr) }; }
/* live: the cinematic plays while the map is left alone, and hands the camera back afterwards */
function sbVaeCine(X, W, fa, dt) { const c = W.cam; if (!c) return; const want = fa >= .56 && fa < .93 && view === "galaxy" && !sheet && !(typeof battle !== "undefined" && battle) && performance.now() - (G.camTouch || 0) > 5000;
  if (want) { if (!X.cine) X.cine = { tx: c.tx, ty: c.ty, tz: c.tz, dist: c.dist, ph: c.ph, th: c.th, out: 0 }; SBX_CAM(X, W, 0, dt, sbVaeCam(X, fa)); return; }
  const C = X.cine; if (!C) return; if (performance.now() - (G.camTouch || 0) < 5000) { X.cine = null; return; } /* they took the camera: leave it where it is */
  C.out += dt; const e = 1 - Math.pow(.95, (dt || 16) / 16.7); for (const kk of ["tx", "ty", "tz", "dist", "ph"]) c[kk] += (C[kk] - c[kk]) * e; let dp = C.th - c.th; while (dp > Math.PI) dp -= TAU; while (dp < -Math.PI) dp += TAU; c.th += dp * e; if (C.out > 3500) X.cine = null; }
addEventListener("pointerdown", () => { G.camTouch = performance.now(); }, true); addEventListener("wheel", () => { G.camTouch = performance.now(); }, { capture: true, passive: true });
