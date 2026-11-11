/* v459 (owner: "his attack doesn't blanket the map"; "when he falls he should turn into a transparent crystal that fades away like spirits").
   The blanket: while the storm rages, a sheet of living plasma (electric veins, rune ripples, a bright wavefront) rolls out from him
   across the whole galaxy floor, and photons rain down everywhere on the map in arcs, many of them right where you are looking, each
   bursting where it lands. Driven by the attack's own clock, like the rest of the storm. */
function sbVaeBlanket(W, X, O, t, sec, dur, k) { const on = k > .001;
  if (!X.vbk) { const g = new TH.Group(); X.grp.add(g); const r = cwRnd(5521), NR = MOBILE ? 200 : 460, NT = 3, R = [];
    for (let i = 0; i < NR; i++) R.push({ per: 1.2 + r() * 1.0, off: r() * 2.2, ft: .75 + r() * .55, h: 160 + r() * 260, near: r() < .42, sz: 12 + r() * 14, col: r() < .6 ? [.85, .65, 1] : r() < .85 ? [1, .85, .5] : [1, 1, 1], tg: new TH.Vector3(), tc: -1 });
    const n = NR * (NT + 2), pg = new TH.BufferGeometry(); pg.setAttribute("position", new TH.BufferAttribute(new Float32Array(n * 3), 3)); pg.setAttribute("color", new TH.BufferAttribute(new Float32Array(n * 3), 3)); pg.setAttribute("aS", new TH.BufferAttribute(new Float32Array(n), 1));
    const pts = new TH.Points(pg, X.vs.pts.material); pts.frustumCulled = false; g.add(pts);
    const lg = new TH.BufferGeometry(); lg.setAttribute("position", new TH.BufferAttribute(new Float32Array(NR * 6), 3)); lg.setAttribute("color", new TH.BufferAttribute(new Float32Array(NR * 6), 3)); const lines = new TH.LineSegments(lg, X.vs.lines.material); lines.frustumCulled = false; g.add(lines);
    const sheet = new TH.Mesh(new TH.CircleGeometry(1, 96), new TH.ShaderMaterial({ uniforms: { uO: { value: new TH.Vector2() }, uR: { value: 0 }, uK: { value: 0 }, uT: { value: 0 }, uE: { value: 900 } }, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, side: TH.DoubleSide, toneMapped: false,
      vertexShader: "varying vec2 vP; void main() { vec4 w = modelMatrix * vec4(position, 1.); vP = w.xz; gl_Position = projectionMatrix * viewMatrix * w; }",
      fragmentShader: "uniform vec2 uO; uniform float uR, uK, uT, uE; varying vec2 vP; float h(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); } float n(vec2 p) { vec2 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f); return mix(mix(h(i), h(i + vec2(1, 0)), f.x), mix(h(i + vec2(0, 1)), h(i + vec2(1, 1)), f.x), f.y); }" +
        "float fb(vec2 p) { float s = 0., a = .5; for (int i = 0; i < 4; i++) { s += a * n(p); p = p * 2.03 + 7.1; a *= .5; } return s; }" +
        "void main() { float d = length(vP - uO), c = length(vP); float inside = smoothstep(uR, uR - 90., d), front = exp(-pow((d - uR) / 30., 2.)), edge = 1. - smoothstep(uE * .82, uE, c);" +
        "vec2 q = vP * .006; float f = fb(q + vec2(uT * .25, -uT * .18)), f2 = fb(q * 2.3 - vec2(uT * .4, uT * .3)); float veins = pow(1. - abs(sin((f + f2 * .5) * 9.)), 5.), web = pow(1. - abs(sin(f2 * 14. + uT)), 10.);" +
        "float rip = pow(.5 + .5 * sin(d * .045 - uT * 7.), 6.) * .5; vec3 col = mix(vec3(.45, .18, 1.), vec3(1., .75, .35), f2 * .8) * (veins * 1.3 + web * .8 + rip + .35) + vec3(.9, .8, 1.) * front * 1.6;" +
        "float a = uK * edge * (inside * (.2 + .6 * veins + .4 * web + rip * .5) + front); gl_FragColor = vec4(col * a, a); }" }));
    sheet.rotation.x = -Math.PI / 2; sheet.frustumCulled = false; g.add(sheet);
    X.vbk = { g, R, NR, NT, pts, lines, sheet, v: new TH.Vector3(), hit: new Set() }; }
  const Z = X.vbk; Z.g.visible = on; if (!on) { Z.hit.clear(); return; }
  const cam = W.cam || { tx: 0, tz: 0 }, sh = Z.sheet, SY = Math.min(O.y - 50, 4); sh.position.set(0, SY - 6, 0); sh.scale.setScalar(980); sh.material.uniforms.uO.value.set(O.x, O.z); sh.material.uniforms.uR.value = 40 + 1700 * Math.min(1, Math.pow(Math.max(0, sec) / 2.6, .8)); sh.material.uniforms.uK.value = k; sh.material.uniforms.uT.value = t * .001; sh.material.uniforms.uE.value = 980;
  const pp = Z.pts.geometry.attributes.position.array, pc = Z.pts.geometry.attributes.color.array, ps = Z.pts.geometry.attributes.aS.array, lp = Z.lines.geometry.attributes.position.array, lc = Z.lines.geometry.attributes.color.array, V = Z.v;
  const arc = (q, u, out) => { out.copy(O).lerp(q.tg, u); out.y += Math.sin(Math.PI * u) * q.h; return out; };
  for (let i = 0; i < Z.NR; i++) { const q = Z.R[i], c = Math.floor((sec - q.off) / q.per), a = sec - q.off - c * q.per, l0 = q.off + c * q.per, j = i * (Z.NT + 2);
    const live = c >= 0 && l0 >= 0 && l0 <= dur && a < q.ft + .45;
    if (!live) { for (let m = 0; m < Z.NT + 2; m++) ps[j + m] = 0; lp.fill(0, i * 6, i * 6 + 6); continue; }
    if (q.tc !== c) { q.tc = c; const h1 = Math.abs(Math.sin((i + 1) * 12.9898 + c * 78.233) * 43758.5453) % 1, h2 = Math.abs(Math.sin((i + 1) * 39.346 + c * 11.135) * 24634.634) % 1;
      if (q.near) { const rr = 40 + Math.sqrt(h1) * 300, an = h2 * TAU; q.tg.set(cam.tx + Math.cos(an) * rr, SY, cam.tz + Math.sin(an) * rr); } else { const rr = Math.sqrt(h1) * 720, an = h2 * TAU; q.tg.set(Math.cos(an) * rr, SY, Math.sin(an) * rr); } }
    if (a < q.ft) { const u = a / q.ft, f = Math.min(1, a / .06) * k;
      for (let m = 0; m <= Z.NT; m++) { arc(q, Math.max(0, u - m * .035), V); pp.set([V.x, V.y, V.z], (j + m) * 3); const ff = f * (1 - m / (Z.NT + 1)); pc.set([q.col[0] * ff, q.col[1] * ff, q.col[2] * ff], (j + m) * 3); ps[j + m] = q.sz * (1 - m * .2); }
      arc(q, u, V); lp.set([V.x, V.y, V.z], i * 6); arc(q, Math.max(0, u - .12), V); lp.set([V.x, V.y, V.z], i * 6 + 3); lc.set([q.col[0] * f, q.col[1] * f, q.col[2] * f, 0, 0, 0], i * 6); ps[j + Z.NT + 1] = 0; }
    else { const b = (a - q.ft) / .45, f = (1 - b) * (1 - b) * k; for (let m = 0; m <= Z.NT; m++) ps[j + m] = 0; lp.fill(0, i * 6, i * 6 + 6); pp.set([q.tg.x, q.tg.y + 4, q.tg.z], (j + Z.NT + 1) * 3); pc.set([f, f * .85, f * 1.0], (j + Z.NT + 1) * 3); ps[j + Z.NT + 1] = 40 + b * 110;
      if (i % 9 === 0 && !Z.hit.has(i * 1000 + c)) { Z.hit.add(i * 1000 + c); sbBoom(X, q.tg.clone(), t, 40 + q.sz * 3); } } }
  for (const A of [Z.pts.geometry.attributes.position, Z.pts.geometry.attributes.color, Z.pts.geometry.attributes.aS, Z.lines.geometry.attributes.position, Z.lines.geometry.attributes.color]) A.needsUpdate = true; }
/* his fall: under a blinding flash he turns to clear crystal, frozen in his last pose, faceted and glinting; then the crystal dissolves from
   the tail up and pale spirits rise from it and drift away until nothing is left. e = seconds since he fell (the same for everyone). */
function sbVaeCrystal(W, X, b, e, t) { if (e < .55) return false;
  if (!X.cry) { const m = new TH.ShaderMaterial({ uniforms: { uT: { value: 0 }, uD: { value: 0 }, uO: { value: 1 }, uY: { value: new TH.Vector2(-40, 120) } }, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, side: TH.DoubleSide, toneMapped: false,
      vertexShader: "varying vec3 vW; varying vec3 vN; void main() { vec4 p = vec4(position, 1.); vec3 nn = normal;\n#ifdef USE_INSTANCING\np = instanceMatrix * p; nn = mat3(instanceMatrix) * nn;\n#endif\nvec4 w = modelMatrix * p; vW = w.xyz; vN = normalize(mat3(modelMatrix) * nn); gl_Position = projectionMatrix * viewMatrix * w; }",
      fragmentShader: "uniform float uT, uD, uO; uniform vec2 uY; varying vec3 vW; varying vec3 vN; float h(vec3 p) { return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453); }" +
        "void main() { vec3 fn = normalize(cross(dFdx(vW), dFdy(vW))); vec3 v = normalize(cameraPosition - vW); float fr = pow(1. - abs(dot(fn, v)), 2.2), fr2 = pow(1. - abs(dot(normalize(vN), v)), 3.);" +
        "float ht = clamp((vW.y - uY.x) / (uY.y - uY.x), 0., 1.), nz = h(floor(vW * .35)), th = ht * .55 + nz * .45; if (th < uD * 1.12 - .06) discard; float edge = 1. - smoothstep(0., .035, th - (uD * 1.12 - .06));" +
        "float gl = step(.985, h(floor(vW * .9) + floor(uT * 3.))) * 2.5; vec3 col = mix(vec3(.35, .25, .85), vec3(.7, .9, 1.), fr) + vec3(1., .9, 1.) * (fr2 * .5 + gl) + vec3(.7, .9, 1.) * edge * 1.3 * step(.001, uD);" +
        "float a = (.04 + fr * .32 + fr2 * .16 + gl * .25 + edge * .3) * uO; gl_FragColor = vec4(col * a, a); }" });
    m.extensions = { derivatives: true }; const keep = [];
    b.grp.traverse(o => { if (o.isMesh && !o.userData.cryKeep) { const mt = o.material, add = mt && (mt.blending === TH.AdditiveBlending || mt.isSpriteMaterial); if (add) { o.visible = false; return; } o.userData.om = mt; o.material = m; keep.push(o); }
      else if (o.isSprite || o.isPoints || o.isLine) o.visible = false; });
    // the spirits: pale wisps that rise out of the dissolving crystal, drawn from points all over his body
    b.grp.updateMatrixWorld(true); const src = [], M = new TH.Matrix4(), Vp = new TH.Vector3(); for (const o of keep) { if (o.isInstancedMesh) { for (let i = 0; i < o.count; i += 1) { o.getMatrixAt(i, M); Vp.setFromMatrixPosition(M).applyMatrix4(o.matrixWorld); src.push(Vp.clone()); } } else src.push(o.getWorldPosition(new TH.Vector3())); }
    const bb = new TH.Box3().setFromObject(b.grp); m.uniforms.uY.value.set(bb.min.y, bb.max.y);
    const r = cwRnd(777), NS = MOBILE ? 160 : 380, S = []; for (let i = 0; i < NS; i++) { const p = src[(r() * src.length) | 0] || bb.getCenter(new TH.Vector3()); S.push({ p: p.clone().add(new TH.Vector3((r() - .5) * 30, (r() - .5) * 16, (r() - .5) * 30)), t0: 1.6 + ((p.y - bb.min.y) / Math.max(1, bb.max.y - bb.min.y)) * 3.2 + r() * 1.4, life: 2.2 + r() * 2.2, rise: 60 + r() * 120, sw: (r() - .5) * 2, ph: r() * TAU, sz: 7 + r() * 10, c: r() < .5 ? [.75, .9, 1] : r() < .8 ? [.85, .7, 1] : [1, 1, 1] }); }
    const pg = new TH.BufferGeometry(); pg.setAttribute("position", new TH.BufferAttribute(new Float32Array(NS * 3), 3)); pg.setAttribute("color", new TH.BufferAttribute(new Float32Array(NS * 3), 3)); pg.setAttribute("aS", new TH.BufferAttribute(new Float32Array(NS), 1));
    const pm = new TH.ShaderMaterial({ transparent: true, depthWrite: false, blending: TH.AdditiveBlending, vertexColors: true, toneMapped: false,
      vertexShader: "attribute float aS; varying vec3 vC; void main() { vC = color; vec4 mv = modelViewMatrix * vec4(position, 1.); gl_Position = projectionMatrix * mv; gl_PointSize = clamp(aS * 520. / -mv.z, 0., 90.); }",
      fragmentShader: "varying vec3 vC; void main() { vec2 c = gl_PointCoord - .5; c.y *= .55; float d = length(c) * 2.; float a = exp(-d * d * 3.) * .8 + exp(-d * d * 30.) * .6; if (a < .01) discard; gl_FragColor = vec4(vC * a, a); }" });
    const pts = new TH.Points(pg, pm); pts.frustumCulled = false; pts.userData.cryKeep = 1; X.grp.add(pts);
    X.cry = { m, S, pts, keep }; }
  const C = X.cry, D = clamp((e - 1.8) / 4.6, 0, 1); C.m.uniforms.uT.value = t * .001; C.m.uniforms.uD.value = D; C.m.uniforms.uO.value = clamp((e - .55) / .5, 0, 1) * (1 - clamp((e - 6.6) / .6, 0, 1));
  b.grp.visible = e < 7.3; const pp = C.pts.geometry.attributes.position.array, pc = C.pts.geometry.attributes.color.array, ps = C.pts.geometry.attributes.aS.array; let any = 0;
  C.S.forEach((q, i) => { const a = (e - q.t0) / q.life; if (a < 0 || a >= 1) { ps[i] = 0; return; } any = 1; const y = q.rise * a + 6 * a * a * q.rise / 10, w = q.ph + a * 4; pp.set([q.p.x + Math.sin(w) * 22 * a * q.sw, q.p.y + y, q.p.z + Math.cos(w) * 22 * a], i * 3);
    const f = Math.sin(Math.PI * Math.min(1, a * 1.4)) * (1 - a) * .75; pc.set([q.c[0] * f, q.c[1] * f, q.c[2] * f], i * 3); ps[i] = q.sz * (.6 + a * .9); });
  C.pts.visible = any || e < 8; for (const A of [C.pts.geometry.attributes.position, C.pts.geometry.attributes.color, C.pts.geometry.attributes.aS]) A.needsUpdate = true; return true; }
