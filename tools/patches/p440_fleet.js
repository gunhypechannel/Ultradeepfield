/* v440 THE LAST STAND: once the Omega Cube wakes, the galaxy's grand fleet warps in and stages in formation against it (158-172 min),
   opens fire, and is wiped out (172-200 min): green beams that erase a squadron at a time, an Omega Pulse through the front ranks,
   and a final pulse. Then the Omega Cube comes apart and its cubes disperse (from 205 min). Scripted from the shared clock like the
   rest of the event: the same ship dies at the same moment for everyone. One instanced mesh per hull type (body + glow), so ~190
   ships cost about ten draw calls; tracers, impacts and beams are one call each. */
const DV_FT = [["corvette", 70], ["destroyer", 46], ["battleship", 50], ["dreadnought", 14], ["supercarrier", 6]], DV_SHIPK = 6.5, DV_PW = 60e3;
function dvFleet(s0) { if (G.dvF && G.dvF.s0 === s0) return G.dvF;
  const r = rnd(hash("fleet:" + s0)), ang = r() * TAU, fx = Math.cos(ang), fz = Math.sin(ang), C = [fx * 430, DV_Y - 20, fz * 430], sd = [-fz, 0, fx];
  const list = []; DV_FT.forEach(([k, n], ti) => { for (let i = 0; i < (MOBILE ? Math.ceil(n * .55) : n); i++) list.push(ti); });
  const N = list.length, rows = 4, per = Math.ceil(N / rows), tiers = 4, cols = Math.ceil(per / tiers), slots = [];
  for (let row = 0; row < rows; row++) for (let c = 0; c < cols; c++) for (let h = 0; h < tiers; h++) slots.push({ row, c: c - (cols - 1) / 2, h: h - (tiers - 1) / 2 });
  slots.sort((a, b) => a.row - b.row || Math.abs(a.c) - Math.abs(b.c) || Math.abs(a.h) - Math.abs(b.h));
  const S = list.map((ti, j) => { const sl = slots[j], wc = sl.c * 36 + (r() - .5) * 12, wh = sl.h * 30 + (r() - .5) * 10, back = sl.row * 44 + ti * 8 + (r() - .5) * 8;
    const p = [C[0] + sd[0] * wc + fx * back, C[1] + wh, C[2] + sd[2] * wc + fz * back];
    return { ti, p, arr: DV.stage + 12 * DV_M * Math.pow(r(), .8), kill: Infinity, fr: .45 + r() * .5, fs: r(), hit: null, dr: [r() - .5, (r() - .5) * .5, r() - .5], rs: [r() - .5, r() - .5, r() - .5] }; });
  for (const s of S) { const dx = s.p[0], dy = s.p[1] - DV_Y, dz = s.p[2], d = Math.hypot(dx, dy, dz); s.d = d; const k = 78 / d; s.hit = [dx * k + (r() - .5) * 60, DV_Y + dy * k + (r() - .5) * 60, dz * k + (r() - .5) * 60]; }
  /* who dies when: beams take a squadron at a time, the first pulse sweeps the front ranks, the second pulse takes the rest */
  const beams = [], pulses = [DV.war0 + 16 * DV_M, DV.war1 - 3 * DV_M], NB = MOBILE ? 22 : 34, perm = S.map((_, i) => i).sort(() => r() - .5); let pi = 0;
  const alive = (s, at) => s.kill > at;
  for (let b = 0; b < NB; b++) { const at = DV.war0 + 90e3 + b * (DV.war1 - DV.war0 - 6 * DV_M) / NB; if (Math.abs(at - pulses[0]) < 90e3) continue;
    while (pi < perm.length && !alive(S[perm[pi]], at)) pi++; if (pi >= perm.length) break; const T0 = S[perm[pi]]; beams.push({ at, to: T0.p });
    for (const s of S) if (alive(s, at) && Math.hypot(s.p[0] - T0.p[0], s.p[1] - T0.p[1], s.p[2] - T0.p[2]) < 44) s.kill = at + 1200; }
  const front = S.filter(s => alive(s, pulses[0])).map(s => s.d).sort((a, b) => a - b), cut = front[Math.floor(front.length * .55)] || 0;
  for (const s of S) { if (alive(s, pulses[0]) && s.d <= cut) s.kill = pulses[0] + DV_PW * (s.d - 80) / 820; }
  for (const s of S) { if (alive(s, pulses[1])) s.kill = pulses[1] + DV_PW * (s.d - 80) / 820; }
  return (G.dvF = { s0, S, beams, pulses, C, fwd: [fx, 0, fz] }); }
function dvFleetBuild(W, X) { const K = fleetKit(W, "terran"); if (!K) return null; const F = { types: [], booms: [], bi: 0, dead: new Set(), seen: new Set() }, gt = W.glow.dv;
  DV_FT.forEach(([k, n]) => { const G0 = shipGeo(K, k), cap = MOBILE ? Math.ceil(n * .55) : n, T = { k, body: null, glow: null };
    if (G0.midB) { T.body = new TH.InstancedMesh(G0.midB, midMat(K, 0), cap); T.body.setColorAt(0, new TH.Color(1, 1, 1)); }
    if (G0.midG) T.glow = new TH.InstancedMesh(G0.midG, midMat(K, 1), cap);
    for (const m of [T.body, T.glow]) if (m) { m.frustumCulled = false; m.count = 0; m.userData.keep = 1; X.grp.add(m); } F.types.push(T); });
  const lg = new TH.BufferGeometry(), NS = 260; lg.setAttribute("position", new TH.BufferAttribute(new Float32Array(NS * 6), 3)); lg.setAttribute("color", new TH.BufferAttribute(new Float32Array(NS * 6), 3));
  F.bolts = new TH.LineSegments(lg, new TH.LineBasicMaterial({ vertexColors: true, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false })); F.bolts.frustumCulled = false; X.grp.add(F.bolts);
  const pg = new TH.BufferGeometry(); pg.setAttribute("position", new TH.BufferAttribute(new Float32Array(NS * 3), 3)); pg.setAttribute("color", new TH.BufferAttribute(new Float32Array(NS * 3), 3));
  F.hits = new TH.Points(pg, new TH.PointsMaterial({ map: W.glow.fire || (W.glow.fire = glowTex("255,190,120", .8)), size: 16, vertexColors: true, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false })); F.hits.frustumCulled = false; X.grp.add(F.hits);
  F.beams = []; for (let i = 0; i < 4; i++) { const m = new TH.Mesh(new TH.CylinderGeometry(1, 1, 1, 10, 1, true), new TH.MeshBasicMaterial({ color: 0x6dff86, transparent: true, opacity: 0, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false })); m.visible = false; X.grp.add(m); F.beams.push(m); }
  F.pulse = new TH.Mesh(new TH.SphereGeometry(1, 48, 24), dvRim(0x4dff70)); F.pulse.visible = false; X.grp.add(F.pulse);
  for (let i = 0; i < (MOBILE ? 14 : 28); i++) { const s = new TH.Sprite(W.additive(W.glow.fire, 0xffd0a0, 0)); s.visible = false; X.grp.add(s); F.booms.push({ s, t: -1e9 }); }
  F.D3 = new TH.Object3D(); F.V = new TH.Vector3(); F.Y = new TH.Vector3(0, 1, 0); F.dark = new TH.Color(.16, .1, .08); F.white = new TH.Color(1, 1, 1); return F; }
function dvFleetTick(W, X, D, t) { const e = D.e; if (e < DV.stage - DV_M || e > DV.end) return; const P = dvFleet(D.s0), F = X.fl || (X.fl = dvFleetBuild(W, X)); if (!F) return;
  const rate = D.rate || 1, D3 = F.D3, cx = 0, cy = DV_Y, cz = 0, n = F.types.map(() => 0), bp = F.bolts.geometry.attributes.position.array, bc = F.bolts.geometry.attributes.color.array, hp = F.hits.geometry.attributes.position.array, hc = F.hits.geometry.attributes.color.array; let nb = 0, nh = 0;
  const fade = e > DV.ret ? clamp(1 - (e - DV.ret) / (30 * DV_M), 0, 1) : 1; /* the wrecks fade out as the cubes disperse */
  for (const s of P.S) { const T = F.types[s.ti]; if (e < s.arr || fade <= 0) continue; const i = n[s.ti]++, dead = e >= s.kill, u = clamp((e - s.arr) / (3000 * rate), 0, 1), w = 1 - Math.pow(1 - u, 3);
    let x = s.p[0] - P.fwd[0] * (1 - w) * 260, y = s.p[1], z = s.p[2] - P.fwd[2] * (1 - w) * 260; /* warps in from behind the line */
    if (dead) { const a = (e - s.kill) / 60e3; x += s.dr[0] * a * 6; y += s.dr[1] * a * 6; z += s.dr[2] * a * 6; }
    D3.position.set(x, y, z); D3.lookAt(cx, y, cz); if (dead) { const a = (e - s.kill) / 20e3; D3.rotateX(s.rs[0] * a); D3.rotateY(s.rs[1] * a); D3.rotateZ(s.rs[2] * a); }
    D3.scale.setScalar(DV_SHIPK * (u > 0 ? 1 : 0)); D3.updateMatrix(); if (T.body) { T.body.setMatrixAt(i, D3.matrix); T.body.setColorAt(i, dead ? F.dark : F.white); }
    if (T.glow) { if (dead) { D3.scale.setScalar(0); D3.updateMatrix(); } T.glow.setMatrixAt(i, D3.matrix); }
    const key = P.S.indexOf(s); if (u > .02 && !F.seen.has(key)) { F.seen.add(key); if (e - s.arr < 8000 * rate) dvBoom(F, x, y, z, t, .6, 0x9fd8ff); }
    if (dead && !F.dead.has(key)) { F.dead.add(key); if (e - s.kill < 6000 * rate) dvBoom(F, x, y, z, t, 1, 0xffc890); }
    /* firing: each live ship sends volleys at the cube's face */
    if (!dead && e > DV.war0 && u >= 1 && nb < 258) { const ph = (t / 1000 * s.fr + s.fs) % 1, hx = s.hit[0], hy = s.hit[1], hz = s.hit[2], dx = hx - x, dy = hy - y, dz = hz - z, L = Math.hypot(dx, dy, dz) || 1, px = x + dx * ph, py = y + dy * ph, pz = z + dz * ph, j = nb * 6, g = s.ti === 1 ? [.5, .8, 1] : [1, .62, .25];
      bp[j] = px; bp[j + 1] = py; bp[j + 2] = pz; bp[j + 3] = px + dx / L * 16; bp[j + 4] = py + dy / L * 16; bp[j + 5] = pz + dz / L * 16; for (let q = 0; q < 6; q += 3) { bc[j + q] = g[0]; bc[j + q + 1] = g[1]; bc[j + q + 2] = g[2]; } nb++;
      if (ph > .9) { const k = nh * 3, a = (ph - .9) * 10; hp[k] = hx; hp[k + 1] = hy; hp[k + 2] = hz; hc[k] = 1 - a * .5; hc[k + 1] = .7 - a * .4; hc[k + 2] = .4 - a * .3; nh++; } } }
  F.types.forEach((T, i) => { for (const m of [T.body, T.glow]) if (m) { m.count = n[i]; m.instanceMatrix.needsUpdate = true; if (m.instanceColor) m.instanceColor.needsUpdate = true; } });
  F.bolts.geometry.setDrawRange(0, nb * 2); F.bolts.geometry.attributes.position.needsUpdate = F.bolts.geometry.attributes.color.needsUpdate = true;
  F.hits.geometry.setDrawRange(0, nh); F.hits.geometry.attributes.position.needsUpdate = F.hits.geometry.attributes.color.needsUpdate = true;
  /* the Omega Cube's beams: from the face that looks at the target, a green lance that holds for a breath */
  let bi = 0; for (const b of P.beams) { const a = (e - b.at) / rate; if (a < -1500 || a > 2500 || bi >= F.beams.length) continue; const m = F.beams[bi++], dx = b.to[0] - cx, dy = b.to[1] - cy, dz = b.to[2] - cz, L = Math.hypot(dx, dy, dz) || 1, o = 78 / L;
    const fx = cx + dx * o, fy = cy + dy * o, fz = cz + dz * o, len = L - 78; m.visible = !reduced; m.position.set(fx + dx / L * len / 2, fy + dy / L * len / 2, fz + dz / L * len / 2); F.V.set(dx / L, dy / L, dz / L); m.quaternion.setFromUnitVectors(F.Y, F.V);
    const k = a < 0 ? .25 * (1 + a / 1500) : 1 - Math.max(0, a - 1500) / 1000, wdt = a < 0 ? .8 : 3.2 + 1.2 * Math.sin(t * .03); m.scale.set(wdt, len, wdt); m.material.opacity = .85 * Math.max(0, k); }
  for (let i = bi; i < F.beams.length; i++) F.beams[i].visible = false;
  /* the Omega Pulse: a sphere of green fire that rolls out through the fleet */
  let pv = false; for (const pt of P.pulses) { const a = (e - pt) / DV_PW; if (a < 0 || a > 1) continue; pv = !reduced; F.pulse.position.set(cx, cy, cz); F.pulse.scale.setScalar(80 + 820 * a); F.pulse.material.uniforms.uA.value = 1.1 * (1 - a) * (a < .05 ? a / .05 : 1); } F.pulse.visible = pv;
  for (const b of F.booms) { const a = (t - b.t) / 1300; if (a < 0 || a > 1) { b.s.visible = false; continue; } b.s.visible = true; b.s.position.set(b.p[0], b.p[1], b.p[2]); b.s.scale.setScalar(b.k * 34 * (.3 + a)); b.s.material.opacity = Math.pow(1 - a, 1.6); }
}
/* a shockwave shell: bright where you look along its surface, clear where you look through it */
function dvRim(col) { return new TH.ShaderMaterial({ uniforms: { uC: { value: new TH.Color(col) }, uA: { value: 0 } }, transparent: true, depthWrite: false, side: TH.DoubleSide, blending: TH.AdditiveBlending, toneMapped: false,
  vertexShader: "varying vec3 vN, vV; void main(){ vec4 mv = modelViewMatrix * vec4(position, 1.0); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }",
  fragmentShader: "uniform vec3 uC; uniform float uA; varying vec3 vN, vV; void main(){ float f = 1.0 - abs(dot(vN, vV)); gl_FragColor = vec4(uC * (0.25 + 1.6 * pow(f, 3.0)), pow(f, 2.2) * uA); }" }); }
function dvBoom(F, x, y, z, t, k, col) { const b = F.booms[F.bi++ % F.booms.length]; b.t = t; b.p = [x, y, z]; b.k = k; b.s.material.color.setHex(col); }
