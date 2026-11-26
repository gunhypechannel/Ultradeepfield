/* ---------- v800 the Aetherion Gateway: 3D (the gateway, Nhalis, the realms), the map layer, the Command Center, the crossing ---------- */
const AET_TEX = {};
function aetRadial(key, stops) { if (AET_TEX[key]) return AET_TEX[key]; const c = document.createElement("canvas"); c.width = c.height = 128; const x = c.getContext("2d"), g = x.createRadialGradient(64, 64, 0, 64, 64, 64);
  stops.forEach(([o, col]) => g.addColorStop(o, col)); x.fillStyle = g; x.fillRect(0, 0, 128, 128); return AET_TEX[key] = new TH.CanvasTexture(c); }
const aetGlowM = (c, o) => new TH.MeshBasicMaterial({ color: c, transparent: true, opacity: o == null ? .9 : o, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false, side: TH.DoubleSide });
function aetSprite(sz, col, key) { const s = new TH.Sprite(new TH.SpriteMaterial({ map: aetRadial(key || "aetg" + col, [[0, col], [.3, col.replace(/[\d.]+\)$/, ".35)")], [1, "rgba(0,0,0,0)"]]), blending: TH.AdditiveBlending, depthWrite: false, transparent: true, toneMapped: false })); s.scale.set(sz, sz, 1); return s; }
function aetGlyphTex() { if (AET_TEX.glyph) return AET_TEX.glyph; const c = document.createElement("canvas"); c.width = 1024; c.height = 64; const x = c.getContext("2d"); x.strokeStyle = "rgba(160,255,240,1)"; x.lineWidth = 2.2;
  for (let i = 0; i < 32; i++) { const cx = i * 32 + 16, h = hash("glyph" + i); x.beginPath(); for (let k = 0; k < 4; k++) { const b = (h >> (k * 4)) & 15; if (b & 1) { x.moveTo(cx - 9, 14 + k * 10); x.lineTo(cx + 9, 14 + k * 10); } if (b & 2) { x.moveTo(cx - 9 + (b & 12), 10 + k * 10); x.lineTo(cx - 9 + (b & 12), 20 + k * 10); } if (b & 4) x.arc(cx, 32, 4 + k * 3, b * .4, b * .4 + 1.6); } x.stroke(); }
  const t = new TH.CanvasTexture(c); t.wrapS = TH.RepeatWrapping; return AET_TEX.glyph = t; }
const AET_HZ_VS = "varying vec2 vU; void main(){ vU = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }";
const AET_HZ_FS = `uniform float uT, uS, uE; uniform vec3 uC, uD; varying vec2 vU;
  float h(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
  float n(vec2 p){ vec2 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f); return mix(mix(h(i), h(i + vec2(1, 0)), f.x), mix(h(i + vec2(0, 1)), h(i + vec2(1)), f.x), f.y); }
  void main(){ vec2 p = vU * 2. - 1.; float r = length(p); if (r > 1.) discard; float a = atan(p.y, p.x);
    float sw = a + 2.6 / (r + .25) - uT * (.25 + .9 * uE); float v = n(vec2(cos(sw), sin(sw)) * 2.3 + r * 5.) * .6 + n(vec2(sw * 1.7, r * 9. - uT)) * .4;
    float rim = smoothstep(.62, .99, r) * (.55 + .45 * sin(a * 12. + uT * 3.)) ; float core = 1. - smoothstep(0., .55, r);
    float on = uE; vec3 c = mix(uD, uC, clamp(v * on * (.35 + .9 * r) + rim * (.35 + .65 * on), 0., 1.));
    if (uS > 2.5) { float f = step(.92, h(vec2(floor(uT * 9.), floor(a * 4.)))); c = mix(c, vec3(.8, .2, .25), f * .6 * rim); }
    float al = mix(.92, .97, core) * smoothstep(1., .96, r); gl_FragColor = vec4(c * (1. - core * .7 * on), al); }`;
/* the Aetherion Gateway: a colossal segmented ring of obsidian and gunmetal, teal channels, four spires, a rotating inner ring, a field of
   glyphs and a dark event horizon that wakes with its state (0 dormant, 1 charging, 2 stable, 3 unstable). ~16 units across. */
function buildAetGate(lo) { const g = new TH.Group(), ring = new TH.Group(); g.add(ring); const U = { st: 0, e: 0 };
  const M = c => new TH.MeshStandardMaterial({ color: c, metalness: .82, roughness: .32, envMapIntensity: 1 });
  const dark = M(0x161b21), gun = M(0x2b333c), silver = M(0x8c9aa6); const teal = aetGlowM(0x5fe8d0, .95), tealD = aetGlowM(0x5fe8d0, .5);
  const hz = new TH.Mesh(new TH.CircleGeometry(6.15, lo ? 32 : 72), new TH.ShaderMaterial({ uniforms: { uT: { value: 0 }, uS: { value: 0 }, uE: { value: 0 }, uC: { value: new TH.Color(0x5fe8d0) }, uD: { value: new TH.Color(0x020607) } }, vertexShader: AET_HZ_VS, fragmentShader: AET_HZ_FS, transparent: true, depthWrite: false, side: TH.DoubleSide }));
  ring.add(hz); U.hz = hz;
  if (lo) { const t = new TH.Mesh(new TH.TorusGeometry(7.4, .9, 6, 36), gun); ring.add(t); const c = new TH.Mesh(new TH.TorusGeometry(6.4, .1, 4, 48), teal); ring.add(c); U.ch = [c]; }
  else { const segN = 32, blk = new TH.BoxGeometry(1.45, 1.1, 1.7), cap = new TH.BoxGeometry(.5, .3, 1.9), lit = new TH.BoxGeometry(.12, .5, .2);
    for (let i = 0; i < segN; i++) { const a = i / segN * TAU, big = i % 4 === 0, m = new TH.Mesh(blk, big ? gun : dark); m.position.set(Math.cos(a) * 7.6, Math.sin(a) * 7.6, 0); m.rotation.z = a; if (big) m.scale.set(1.15, 1.6, 1.25); ring.add(m);
      const c = new TH.Mesh(cap, silver); c.position.set(Math.cos(a) * 8.25 * (big ? 1.04 : 1), Math.sin(a) * 8.25 * (big ? 1.04 : 1), 0); c.rotation.z = a; ring.add(c);
      const l = new TH.Mesh(lit, teal); l.position.set(Math.cos(a + .09) * 7.6, Math.sin(a + .09) * 7.6, .9); l.rotation.z = a; ring.add(l); }
    for (const [r, w] of [[6.45, .12], [8.9, .06]]) { const c = new TH.Mesh(new TH.TorusGeometry(r, w, 6, 96), teal); ring.add(c); (U.ch = U.ch || []).push(c); }
    const inner = new TH.Group(); for (let i = 0; i < 24; i++) { const a = i / 24 * TAU, m = new TH.Mesh(new TH.BoxGeometry(.5, .5, 1.1), i % 3 ? dark : silver); m.position.set(Math.cos(a) * 6.75, Math.sin(a) * 6.75, 0); m.rotation.z = a; inner.add(m); }
    inner.add(new TH.Mesh(new TH.TorusGeometry(6.75, .2, 6, 96), gun)); ring.add(inner); U.inner = inner;
    for (let k = 0; k < 4; k++) { const a = k * Math.PI / 2 + Math.PI / 2, sp = new TH.Group(); sp.position.set(Math.cos(a) * 8.6, Math.sin(a) * 8.6, 0); sp.rotation.z = a - Math.PI / 2;
      const base = new TH.Mesh(new TH.CylinderGeometry(.9, 1.3, 2.4, 6), gun); base.position.y = 1; sp.add(base);
      for (const [x, h, r] of [[0, 4.6, .42], [-.65, 3, .26], [.65, 3, .26], [-1.1, 1.9, .18], [1.1, 1.9, .18]]) { const t = new TH.Mesh(new TH.ConeGeometry(r, h, 6), dark); t.position.set(x, 2.2 + h / 2, 0); sp.add(t);
        const s = new TH.Mesh(new TH.BoxGeometry(.06, h * .7, .06), teal); s.position.set(x, 2.2 + h * .45, r * .9); sp.add(s); }
      const tip = aetSprite(1.4, "rgba(255,80,90,1)", "aettip"); tip.position.set(0, 7.1, 0); sp.add(tip); ring.add(sp);
      for (const s of [-1, 1]) { const arm = new TH.Mesh(new TH.BoxGeometry(3.2, .35, .6), gun); arm.position.set(Math.cos(a) * 8.6 + Math.cos(a + Math.PI / 2) * s * 1.9, Math.sin(a) * 8.6 + Math.sin(a + Math.PI / 2) * s * 1.9, 0); arm.rotation.z = a + Math.PI / 2; ring.add(arm); } }
    const gl = new TH.Mesh(new TH.RingGeometry(9.3, 10.1, 128, 1), new TH.MeshBasicMaterial({ map: aetGlyphTex(), transparent: true, opacity: .35, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false }));
    ring.add(gl); U.glyph = gl;
    const halo = aetSprite(26, "rgba(95,232,208,1)", "aethalo"); halo.material.opacity = .18; ring.add(halo); U.halo = halo; }
  g.userData.U = U;
  g.userData.tick = (t, st, e) => { U.st += ((st || 0) - U.st) * .05; U.e += ((e == null ? (st >= 2 ? 1 : st === 1 ? .55 : .08) : e) - U.e) * .04; const u = hz.material.uniforms; u.uT.value = t * .001; u.uS.value = st; u.uE.value = U.e;
    if (U.inner) U.inner.rotation.z = t * .00012 * (.3 + U.e * 2.2) * (st === 3 ? 1 + .4 * Math.sin(t * .003) : 1);
    if (U.glyph) { U.glyph.rotation.z = -t * .00004; U.glyph.material.opacity = .08 + .3 * U.e; }
    if (U.halo) U.halo.material.opacity = .05 + .2 * U.e * (st === 3 ? .6 + .4 * Math.random() : 1);
    for (const c of U.ch || []) { c.material.opacity = (.25 + .7 * U.e) * (st === 1 ? .6 + .4 * Math.sin(t * .012) : 1); c.material.color.setHex(st === 3 && Math.sin(t * .02) > .6 ? 0xd0404a : 0x5fe8d0); } };
  return g; }
/* Nhalis: a dark world threaded with teal light (how much depends on the saga, v803) */
const AET_NH_FS = `uniform float uT, uK; varying vec3 vN, vP; float h(vec3 p){ return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453); }
  float n(vec3 p){ vec3 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f); return mix(mix(mix(h(i), h(i + vec3(1,0,0)), f.x), mix(h(i + vec3(0,1,0)), h(i + vec3(1,1,0)), f.x), f.y), mix(mix(h(i + vec3(0,0,1)), h(i + vec3(1,0,1)), f.x), mix(h(i + vec3(0,1,1)), h(i + vec3(1,1,1)), f.x), f.y), f.z); }
  void main(){ vec3 p = normalize(vP) * 3.; float rock = n(p * 2.) * .6 + n(p * 6.) * .4; float vein = 1. - smoothstep(.0, .06, abs(n(p * 3.1) - .5)); float spread = smoothstep(uK - .15, uK, n(p * 1.3) * .8 + .2);
    vec3 base = mix(vec3(.05, .07, .09), vec3(.2, .19, .17), rock); vec3 L = normalize(vec3(.4, .7, .5)); float d = max(.12, dot(normalize(vN), L));
    vec3 c = base * d + vec3(.37, .91, .82) * vein * spread * (.7 + .3 * sin(uT * 2. + rock * 9.)); float rim = pow(1. - abs(dot(normalize(vN), vec3(0, 0, 1))), 3.); c += vec3(.2, .6, .7) * rim * .35; gl_FragColor = vec4(c, 1.); }`;
function buildAetNhalis() { const m = new TH.Mesh(new TH.SphereGeometry(3.2, 48, 32), new TH.ShaderMaterial({ uniforms: { uT: { value: 0 }, uK: { value: 1 } }, vertexShader: "varying vec3 vN, vP; void main(){ vN = normalMatrix * normal; vP = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }", fragmentShader: AET_NH_FS }));
  const g = new TH.Group(); g.add(m); g.userData.mat = m.material; const at = aetSprite(9, "rgba(95,232,208,1)", "aetnh"); at.material.opacity = .25; g.add(at); g.userData.at = at; return g; }
/* the Interstice: a dark artificial universe under the galaxy; the scenery is drawn here, its targets live in AET_TGT (v801) */
const AET_BG_FS = `uniform float uT; uniform vec3 uC; varying vec3 vW; float h(vec3 p){ return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453); }
  float n(vec3 p){ vec3 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f); return mix(mix(mix(h(i), h(i + vec3(1,0,0)), f.x), mix(h(i + vec3(0,1,0)), h(i + vec3(1,1,0)), f.x), f.y), mix(mix(h(i + vec3(0,0,1)), h(i + vec3(1,0,1)), f.x), mix(h(i + vec3(0,1,1)), h(i + vec3(1,1,1)), f.x), f.y), f.z); }
  void main(){ vec3 d = normalize(vW); float neb = n(d * 3. + uT * .01) * .6 + n(d * 7.) * .4; float st = step(.996, h(floor(d * 300.))); float band = exp(-abs(d.y + .1) * 6.);
    vec3 c = vec3(.004, .012, .016) + uC * pow(neb, 3.) * .35 * (.4 + band) + vec3(.7, 1., .95) * st * .6; gl_FragColor = vec4(c, 1.); }`;
function aetRealmScene(k) { const R = AET_RB[k], g = new TH.Group(), c = aetRealmPos(k); g.position.set(c.x, c.y, c.z); const col = new TH.Color(R.col);
  const bg = new TH.Mesh(new TH.SphereGeometry(430, 32, 20), new TH.ShaderMaterial({ uniforms: { uT: { value: 0 }, uC: { value: col } }, vertexShader: "varying vec3 vW; void main(){ vW = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }", fragmentShader: AET_BG_FS, side: TH.BackSide }));
  bg.renderOrder = -10; g.add(bg); g.userData.bg = bg;
  const M = c2 => new TH.MeshStandardMaterial({ color: c2, metalness: .7, roughness: .45 }), rock = M(0x1c2126), dark = M(0x10151a);
  /* floating stone and machinery, drifting currents, dead rings in the distance */
  const rnd = (i, s) => (hash(k + s + i) % 1000) / 1000;
  const rg = new TH.IcosahedronGeometry(1, 0); for (let i = 0; i < 70; i++) { const a = rnd(i, "a") * TAU, r = 30 + rnd(i, "r") * 120, m = new TH.Mesh(rg, i % 7 ? rock : dark); m.position.set(Math.cos(a) * r, -18 + rnd(i, "y") * 26, Math.sin(a) * r); const s = .6 + rnd(i, "s") * (i % 9 ? 2.2 : 6); m.scale.set(s, s * (.6 + rnd(i, "q")), s); m.rotation.set(rnd(i, "x") * 3, rnd(i, "z") * 3, 0); g.add(m); }
  const cur = []; for (let j = 0; j < 6; j++) { const pts = []; const a0 = j / 6 * TAU; for (let i = 0; i <= 40; i++) { const u = i / 40, a = a0 + u * 2.2, r = 150 - u * 120; pts.push(new TH.Vector3(Math.cos(a) * r, -4 + Math.sin(u * 9 + j) * 3, Math.sin(a) * r)); }
    const l = new TH.Line(new TH.BufferGeometry().setFromPoints(pts), new TH.LineBasicMaterial({ color: col, transparent: true, opacity: .25, blending: TH.AdditiveBlending, depthWrite: false })); g.add(l); cur.push(l); } g.userData.cur = cur;
  if (k === "int") { for (const [x, y, z, s] of [[-190, 30, -150, 3.2], [210, 50, 120, 2.6], [40, 70, -230, 2.2], [-160, -20, 200, 2.8]]) { const d = buildAetGate(true); d.position.set(x, y, z); d.scale.setScalar(s); d.lookAt(0, 0, 0); d.userData.dead = 1; g.add(d); (g.userData.dead = g.userData.dead || []).push(d); } }
  const amb = new TH.PointLight(col, 1.4, 260, 1.6); amb.position.set(0, 60, 0); g.add(amb);
  return g; }
/* where a realm fleet waits: your arrival gate (this server's arrival zone) */
const AET_ARR = { int: [-80, 0, 70], shat: [-80, 0, 70], dom: [-80, 0, 70], tide: [-80, 0, 70] };
const aetArrPos = (k, out) => { const c = aetRealmPos(k), a = AET_ARR[k], o = out || {}; o.x = c.x + a[0]; o.y = c.y + a[1]; o.z = c.z + a[2]; return o; };
/* the map layer: the gateway beside Nhalis, the realm you are looking at, your fleets parked at its arrival gate */
function aetGateState(T) { if (!aetOpen(T)) return 0; const mine = aetOpenTx(); if (aetOff()) return 0; if (aetFlux(T)) return 3; if (mine.some(x => x.st === "RESERVED")) return 1; return 2; }
function aetMapTick(W, t, T) { if (!W || !W.scene) return; const show = aetOpen(T) || (aetSeen() && aetSaga(T) && typeof aetSagaShow === "function" && aetSagaShow(T)); let X = W.aetL;
  if (!show && !G.aetView) { if (X) { aetFreeL(W); } return; }
  if (!X) { X = W.aetL = { grp: new TH.Group(), q: {}, rs: {} }; W.scene.add(X.grp); }
  const cp = W.camera.position, nh = aetNhalis(T, X.q);
  if (!X.nh) { X.nh = buildAetNhalis(); X.grp.add(X.nh); }
  X.nh.position.set(nh.x, nh.y, nh.z); X.nh.userData.mat.uniforms.uT.value = t * .001; X.nh.userData.mat.uniforms.uK.value = typeof aetNhK === "function" ? aetNhK(T) : aetOpen(T) ? .35 : 1;
  const gp = aetGatePos(T, {}); const dc = Math.hypot(gp.x - cp.x, gp.y - cp.y, gp.z - cp.z), lo = dc > 260, gOn = aetOpen(T) || (typeof aetGateVis === "function" && aetGateVis(T));
  if (X.gLo !== lo || (!X.gate && gOn)) { if (X.gate) { X.grp.remove(X.gate); X.gate.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material && o.material.dispose) o.material.dispose(); }); } X.gate = gOn ? buildAetGate(lo) : null; X.gLo = lo; if (X.gate) X.grp.add(X.gate); }
  if (X.gate) { X.gate.visible = gOn; X.gate.position.set(gp.x, gp.y, gp.z); X.gate.lookAt(0, gp.y + 20, 0); X.gate.scale.setScalar(typeof aetGateScale === "function" ? aetGateScale(T) : 1); X.gate.userData.tick(t, aetGateState(T), typeof aetGateE === "function" ? aetGateE(T) : null);
    if (typeof aetGateBuild === "function") aetGateBuild(X.gate, T); }
  if (typeof aetSagaTick === "function") aetSagaTick(W, X, t, T);
  /* realms: built while you look at one or have fleets there; the backdrop only while you look (it would show from the galaxy) */
  for (const R of AET_REALMS) { const need = G.aetView === R.k || aetOpenTx().some(x => x.realm === R.k && x.st === "ACTIVE"); let rs = X.rs[R.k];
    if (need && !rs) { rs = X.rs[R.k] = { g: aetRealmScene(R.k), fl: {} }; X.grp.add(rs.g); const a = buildAetGate(false); a.scale.setScalar(.55); const ap = AET_ARR[R.k]; a.position.set(ap[0], ap[1] + 6, ap[2]); a.lookAt(0, 6, 0); rs.g.add(a); rs.arr = a; }
    if (!need && rs) { X.grp.remove(rs.g); rs.g.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material && o.material.dispose) o.material.dispose(); }); delete X.rs[R.k]; continue; }
    if (!rs) continue; rs.g.userData.bg.visible = G.aetView === R.k; rs.g.userData.bg.material.uniforms.uT.value = t * .001; rs.g.userData.bg.position.copy(G.aetView === R.k ? new TH.Vector3(cp.x - rs.g.position.x, cp.y - rs.g.position.y, cp.z - rs.g.position.z) : new TH.Vector3());
    for (const d of rs.g.userData.dead || []) d.userData.tick(t, 0, .06); rs.arr.userData.tick(t, aetOpenTx().some(x => x.realm === R.k && x.st === "IN_TRANSIT") ? 2 : 1, null);
    for (const l of rs.g.userData.cur) l.material.opacity = .12 + .1 * Math.sin(t * .001 + l.id);
    /* your fleets waiting at the arrival gate */
    const here = aetActive(R.k), keep = {}; here.forEach((x, i) => { keep[x.id] = 1; let f = rs.fl[x.id]; const sig = Object.entries(x.n).map(e => e.join(":")).join(",");
      if (!f || f.sig !== sig) { if (f) { rs.g.remove(f.g); } let g2; try { g2 = fleet3D(W, x.n, 0x5fe8d0, false, false, false, null); } catch (e) { g2 = new TH.Group(); } rs.g.add(g2); f = rs.fl[x.id] = { g: g2, sig }; }
      const ap = AET_ARR[R.k], sp = (f.g.userData.span || 20); f.g.position.set(ap[0] + 14 + i * 9, ap[1] + 2, ap[2] - 10 - i * 6); f.g.scale.setScalar(5 / sp); f.g.rotation.y = -.6; f.g.visible = !S.fleets.some(q => q.aet === x.id && q.all); });
    for (const id in rs.fl) if (!keep[id]) { rs.g.remove(rs.fl[id].g); delete rs.fl[id]; }
    if (typeof aetRealmTick === "function") aetRealmTick(W, rs, R, t, T); } }
function aetFreeL(W) { const X = W.aetL; if (!X) return; W.scene.remove(X.grp); X.grp.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material && o.material.dispose) o.material.dispose(); }); W.aetL = null; }
/* labels and tap targets (drawn into the map's 2D overlay) */
function aetOverlay(W, hits, proj, label, cp, k, T) { const X = W.aetL; if (!X) return; if (!G.aetView && typeof aetSgOverlay === "function") aetSgOverlay(W, hits, proj, label, cp, k, T);
  if (X.gate && X.gate.visible && !G.aetView) { const s = proj(X.gate.position); if (s) { const sr = 10 / cp.distanceTo(X.gate.position) * k; hits.push({ aet: "gate", x: s[0], y: s[1], sr: Math.max(sr, 16), prio: 0 });
      const st = aetGateLbl(T); label(aetOpen(T) ? `AETHERION GATEWAY · ${st[0]}` : `THE FIRST APERTURE · ${Math.round((typeof aetBuildFrac === "function" ? aetBuildFrac(T) : 0) * 100)}% ASSEMBLED`, s[0], s[1] + Math.max(sr * 1.15, 14) + 12, st[1], 11); } }
  if (G.aetView) { const R = AET_RB[G.aetView], rs = X.rs[G.aetView]; if (rs && rs.arr) { const v = new TH.Vector3(); rs.arr.getWorldPosition(v); const s = proj(v); if (s) { hits.push({ aet: "arr:" + R.k, x: s[0], y: s[1], sr: 22 }); const n = aetActive(R.k).length; label(`YOUR ARRIVAL GATE${n ? ` · ${n} fleet${n > 1 ? "s" : ""}` : ""}`, s[0], s[1] + 26, AET_COL, 11); } }
    if (typeof aetRealmOverlay === "function") aetRealmOverlay(W, hits, proj, label, cp, k, T); } }
function aetGateLbl(T) { if (aetOff()) return ["RESTRICTED", "#ffb070"]; if (!aetOpen(T)) return ["LOCKED", "#8aa"]; const st = aetGateState(T), war = false;
  return st === 3 ? ["UNSTABLE", "#ff7a80"] : st === 1 ? ["CHARGING", "#bff"] : aetOpenTx().length ? ["ACTIVE", AET_COL] : war ? ["CROSS-SERVER WAR", "#ff5560"] : ["AVAILABLE", AET_COL]; }
function aetTap(id) { if (typeof aetTapS === "function" && aetTapS(id)) return; if (id === "gate") { openSheet({ type: "aet", tab: "gate" }); return; } if (id.startsWith("arr:")) { openSheet({ type: "aet", tab: "fleet" }); return; } if (typeof aetTapT === "function") aetTapT(id); }
/* the realm view: the camera goes down into the realm's pocket of space */
function aetEnter(k) { if (!AET_RB[k] || !G3) return; const lk = aetRealmLock(k), mine = aetOpenTx().some(x => x.realm === k); if (lk && !mine) { toast(lk, "warn"); return; }
  closeSheet(); if (view !== "galaxy") { view = "galaxy"; render(); } G.aetView = k; const c = G3.cam, p = aetArrPos(k, {}); c.follow = null; c.followFleet = null; c.vel = null; c.tx = p.x + 40; c.ty = p.y; c.tz = p.z - 40; c.dist = 240; c.ph = .95; c.goal = { dist: 190 }; aetFlash();
  aetS().seen[k] = 1; dirty(); softRender(); }
function aetLeave() { if (!G.aetView) return; G.aetView = null; const c = G3 && G3.cam; if (c) { const h = homePlanet(), q = h ? P3(h, now()) : { x: 0, y: 0, z: 0 }; c.follow = null; c.followFleet = null; c.tx = q.x; c.ty = 0; c.tz = q.z; c.dist = 140; c.goal = { dist: 90 }; aetFlash(); } softRender(); }
function aetFlash() { if (reduced) return; const el = document.createElement("div"); el.className = "aetflash"; $("#app").appendChild(el); setTimeout(() => el.remove(), 900); }
/* the band at the top of the map */
function aetBand(T) { if (!aetSeen()) return ""; if (G.aetView) { const R = AET_RB[G.aetView]; return `<button class="omb aetb" data-act="aetLeave"><b>◈ ${esc(R.n.toUpperCase())}</b><span>Back to the galaxy</span></button>`; }
  if (!aetOpen(T)) return typeof aetSgBand === "function" ? aetSgBand(T) : ""; const n = aetOpenTx().length; return `<button class="omb aetb" data-act="aetOpen"><b>◈ GATEWAY</b><span>${n ? `${n} fleet${n > 1 ? "s" : ""} beyond` : aetFlux(T) ? "Unstable" : "Available"}</span></button>`; }
/* ---------- the crossing: a visual of what the ledger confirmed (never the other way round) ---------- */
function aetCine(x, kind) { if (document.hidden || !x) return; const R = AET_RB[x.realm]; let el = $("#aetcine"); if (el) el.remove(); el = document.createElement("div"); el.id = "aetcine"; el.className = "aetcine" + (reduced || S.aetLow ? " lite" : "");
  const t1 = kind === "out" ? "Gateway charging" : "Gateway transit complete", t2 = kind === "out" ? `Destination locked: ${R.n}. Departure in ${ftime(Math.max(0, (x.t.res || now()) + AET_CHARGE - now()))}.` : `${R.n} · ${aetShipsTxt(x.n)}`;
  el.innerHTML = `<canvas></canvas><div class="aetct"><small>APERTURE 001 · NHALIS</small><b>${t1}</b><span>${esc(t2)}</span><div class="aetcb">${kind === "arrive" ? `<button class="btn pri" data-act="aetView" data-k="${x.realm}">View ${esc(R.n)}</button>` : ""}<button class="btn" data-act="aetCineX">${kind === "arrive" ? "Later" : "Close"}</button></div></div>`;
  $("#app").appendChild(el); if (el.classList.contains("lite")) { setTimeout(() => { if (el.isConnected && kind === "out") el.remove(); }, 4000); return; }
  const cv = el.querySelector("canvas"), ctx = cv.getContext("2d"), t0 = performance.now(), stars = Array.from({ length: 220 }, (_, i) => ({ a: Math.random() * TAU, r: Math.random(), s: .3 + Math.random() * 1.6 }));
  const draw = () => { if (!el.isConnected) return; const w = cv.width = el.clientWidth * Math.min(2, devicePixelRatio || 1), h = cv.height = el.clientHeight * Math.min(2, devicePixelRatio || 1), cx = w / 2, cy = h / 2, s = (performance.now() - t0) / 1000, M = Math.max(w, h);
    ctx.fillStyle = "rgba(1,6,8,1)"; ctx.fillRect(0, 0, w, h); const sp = kind === "out" ? Math.min(1, s / 2.4) : Math.max(0, 1 - Math.max(0, s - 2.6) / 1.2);
    for (let i = 0; i < 9; i++) { const rr = ((s * (.25 + sp) + i / 9) % 1) * M * .75; ctx.strokeStyle = `rgba(95,232,208,${.08 + .35 * (1 - rr / (M * .75)) * (.3 + sp)})`; ctx.lineWidth = 1 + 3 * (1 - rr / (M * .75)); ctx.beginPath(); ctx.arc(cx, cy, rr, 0, TAU); ctx.stroke(); }
    for (const p of stars) { p.r += (.002 + .03 * sp) * p.s; if (p.r > 1) p.r = .02; const r0 = p.r * M * .7, r1 = r0 * (1 + .04 + .5 * sp); ctx.strokeStyle = `rgba(${170 + 60 * p.s | 0},255,240,${Math.min(1, p.r * 1.6)})`; ctx.lineWidth = p.s; ctx.beginPath(); ctx.moveTo(cx + Math.cos(p.a) * r0, cy + Math.sin(p.a) * r0); ctx.lineTo(cx + Math.cos(p.a) * r1, cy + Math.sin(p.a) * r1); ctx.stroke(); }
    const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, M * .25); g.addColorStop(0, `rgba(0,0,0,${.9 * sp})`); g.addColorStop(.6, `rgba(95,232,208,${.25 * sp})`); g.addColorStop(1, "rgba(0,0,0,0)"); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
    if (s < (kind === "out" ? 4.2 : 6)) requestAnimationFrame(draw); else if (kind === "out") el.remove(); };
  requestAnimationFrame(draw); }
/* ---------- the Command Center ---------- */
const AET_TABS = [["gate", "Gateway"], ["realms", "Realms"], ["war", "Nexus War"], ["fleet", "Deployment"], ["rewards", "Rewards"], ["more", "More"]];
function aetStatusRow(T) { const A = aetS(), st = aetGateLbl(T), op = aetOpenTx(), R = AET_RB[A.dest] || AET_RB.int, f = aetFlux(T);
  const disc = AET_REALMS.filter(r => !aetRealmLock(r.k, T)).length;
  return `<div class="aetstat"><div><small>Status</small><b style="color:${st[1]}">${st[0]}</b></div><div><small>Aperture</small><b>001 · Nhalis</b></div><div><small>Integrity</small><b${f ? ' class="warn"' : ""}>${aetInteg(T)}%</b></div>
    <div><small>Transit energy</small><b>${Math.floor(aetEn(T))}/${aetEnMax()}</b></div><div><small>Destination</small><b>${esc(R.n.replace("The ", ""))}</b></div><div><small>Realms charted</small><b>${disc}/${AET_REALMS.length}</b></div>
    <div><small>Event</small><b>${f ? "Flux hour" : "None"}</b></div><div><small>Home server</small><b>${esc(aetServer())}</b></div><div><small>Fleet slots</small><b>${op.length}/${aetSlots()}</b></div></div>`; }
const aetServer = () => { try { const v = (window.UDF_SUPABASE || {}).launch; return v ? `Origin · ${v.slice(0, 7)}` : "This server"; } catch (e) { return "This server"; } };
function aetHoloSVG(st) { const cls = ["dorm", "chg", "stab", "unst", "tran"][st] || "dorm", seg = Array.from({ length: 32 }, (_, i) => { const a = i / 32 * 360; return `<rect x="-3.2" y="-48" width="6.4" height="${i % 4 ? 7 : 10}" rx="1" transform="rotate(${a})"/>`; }).join("");
  return `<div class="aetholo ${cls}"><svg viewBox="-60 -60 120 120" aria-hidden="true"><defs><radialGradient id="aethz"><stop offset="0" stop-color="#010405"/><stop offset=".7" stop-color="#062a28"/><stop offset="1" stop-color="#5fe8d0"/></radialGradient></defs>
    <circle class="hz" r="36" fill="url(#aethz)"/><g class="sw"><path d="M0-30A30 30 0 0 1 26 15" /><path d="M0 22A22 22 0 0 1-19-11"/><path d="M-12-8A14 14 0 0 1 12 6"/></g>
    <g class="outer">${seg}</g><circle class="ch" r="41" /><g class="inner"><circle r="38.5" class="in"/>${Array.from({ length: 12 }, (_, i) => `<rect x="-1.6" y="-40.5" width="3.2" height="4" transform="rotate(${i * 30})"/>`).join("")}</g>
    <g class="glyph"><circle r="54" /><circle r="56.5" /></g>${[0, 90, 180, 270].map(a => `<path class="spire" d="M-3-49L0-60L3-49Z" transform="rotate(${a})"/>`).join("")}</svg></div>`; }
function shAet() { const T = now(), A = aetS(), tab = sheet.tab || "gate", own = ownerFree() && G.mode !== "offline" || G.owner;
  if (!aetSeen()) return `<div class="hd"><div><div class="chapter">Aetherion</div><h2>Nothing here yet</h2></div><button class="x" data-act="close" aria-label="Close">✕</button></div>`;
  const body = tab === "realms" ? aetRealmsHTML(T) : tab === "war" ? aetWarHTML(T) : tab === "fleet" ? aetFleetHTML(T) : tab === "rewards" ? aetRewardsHTML(T) : tab === "more" ? aetMoreHTML(T) : aetGateHTML(T);
  return `<div class="hd aethd"><div style="flex:1;min-width:0"><div class="chapter" style="color:${AET_COL}">Aperture 001 · Nhalis</div><h2>Aetherion Command Center</h2></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
  <div class="aetcc">${aetStatusRow(T)}<div class="tabs aettabs">${AET_TABS.map(([k, n]) => `<button class="${k === tab ? "on" : ""}" data-act="aetTab" data-t="${k}">${n}</button>`).join("")}</div>${body}
  ${own ? `<div class="mimown aetown"><small>Owner preview (this device only; players see nothing until the Aetherion switch is on): pick a saga week or the open gateway.</small><div>${[["Off", "off"]].concat(AET_SAGA.flatMap((s, j) => [1, 2, 3, 4].map(w => [`S${j + 1} W${w}`, `s${j}_${w}`]))).concat([["Gateway open", "open"]]).map(([n, v]) => `<button class="btn${aetPrevKey() === v ? " pri" : ""}" data-act="aetPrev" data-v="${v}">${n}</button>`).join("")}</div></div>` : ""}</div>`; }
const aetPrevKey = () => { const p = S.aetPrev; return !p ? "off" : p.m === "open" ? "open" : `s${p.j}_${p.w}`; };
function aetGateHTML(T) { const A = aetS(), open = aetOpen(T), st = !open ? 0 : aetOpenTx().some(x => x.st === "IN_TRANSIT") ? 4 : aetGateState(T), R = AET_RB[A.dest] || AET_RB.int, f = aetFlux(T), op = aetOpenTx();
  const nf = aetNextFlux(T), lock = aetRealmLock(R.k, T);
  const sagaTxt = (() => { const sg = aetSaga(T); if (open) return ""; if (sg) return `<p class="note">${esc(AET_SAGA[sg.j][0])} · week ${sg.w}. ${esc(AET_SAGA[sg.j][2])} The Gateway opens when the First Aperture rises at the end of the fourth season.</p>`;
    return `<p class="note">The Gateway does not exist yet. Its story begins with ${esc(AET_SAGA[0][0])} on ${new Date(AET_T0()).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" })}; it opens on ${new Date(aetOpenAt()).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" })}.</p>`; })();
  return `<div class="aetgate">${aetHoloSVG(st)}<div class="aetgi"><b>${["Dormant", "Charging", "Stable", "Unstable", "In transit"][st]}</b><span>${!open ? "Locked" : f ? `Field unstable until ${new Date(f.end).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })}: crossings cost 50% more energy` : `Stable. Next flux hour ${nf ? "in " + ftime(nf - T) : "later"}`}</span></div></div>${sagaTxt}
  <dl class="kv aetkv"><dt>Identification</dt><dd>Aperture 001 · Nhalis</dd><dt>Status</dt><dd>${open ? (aetOff() ? "Restricted (maintenance)" : ["Online", "Charging", "Stable", "Unstable", "In transit"][st]) : "Locked"}</dd><dt>Integrity</dt><dd>${aetInteg(T)}%</dd><dt>Energy</dt><dd>${Math.floor(aetEn(T))} of ${aetEnMax()} · +12 an hour</dd>
    <dt>Destination</dt><dd>${esc(R.n)}${lock ? ` · <em class="aetlk">${esc(lock)}</em>` : ""}</dd><dt>Requirements</dt><dd>A crossing costs 15–60 energy by fleet size (+50% in the flux hour) and one of your ${aetSlots()} gateway slot${aetSlots() > 1 ? "s" : ""}. Coming home is always free.</dd><dt>Fleets beyond</dt><dd>${op.length ? op.map(x => `${AET_RB[x.realm].n.replace("The ", "")}: ${aetStName(x)}`).join(" · ") : "None"}</dd></dl>
  <div class="aetacts"><button class="btn" data-act="aetTab" data-t="realms">Select destination</button><button class="btn pri" data-act="aetTab" data-t="fleet"${open && !lock ? "" : " disabled"}>Initiate transit</button><button class="btn" data-act="aetTab" data-t="fleet">Active missions (${op.length})</button><button class="btn" data-act="aetTab" data-t="war">Nexus War</button>
    <button class="btn" data-act="aetRecallAll"${op.some(x => ["ACTIVE", "RESERVED"].includes(x.st)) ? "" : " disabled"}>${sheet.armAll ? "Confirm: recall every fleet" : "Return home"}</button>${G.aetView ? `<button class="btn" data-act="aetLeave">Back to the galaxy</button>` : ""}</div>
  <details class="crclore aetlore"><summary>How the Gateway works</summary><p>Pick a realm, pick ships, and confirm. The Gateway charges for 45 seconds, then your fleet crosses the corridor (a few minutes) and waits at your arrival gate in that realm. From there it can explore, fight neutral defenders and gather. Recall it any time it is waiting at the gate; the way home takes as long as the way out and costs nothing.</p><p>The server keeps the record of every crossing, so a fleet is always in exactly one place: if you lose connection, close the game or switch devices, the crossing carries on and your fleet is where the record says. If anything ever goes wrong, the fleet comes home.</p><p>Once a day, at a different hour each day, the Gateway's field goes unstable for an hour: crossings cost more energy then, but nothing is ever lost to it.</p></details>`; }
const aetStName = x => ({ RESERVED: "charging", IN_TRANSIT: "in the corridor", ARRIVED: "arriving", ACTIVE: "at the arrival gate", RETURNING: "coming home", HOME: "home", LOST: "lost", VOID: "cancelled" })[x.st] || x.st;
function aetRealmsHTML(T) { const A = aetS(); return `<p class="note">The Dimensional Atlas: every realm the Gateway can reach, charted or not. Tap one for its details.</p><div class="aetatlas">${AET_REALMS.map(R => { const lk = aetRealmLock(R.k, T), on = sheet.rx === R.k, n = aetOpenTx().filter(x => x.realm === R.k).length;
    return `<div class="aetrc${lk ? " lk" : ""}${on ? " on" : ""}" style="--rc:${R.col}"><button class="aetrh" data-act="aetRx" data-k="${R.k}"><span class="aetra" style="background-image:url(${R.art})"></span><span class="aetrt"><b>${esc(R.n)}</b><small>${esc(R.cat)}</small><em>${lk ? "Locked" : n ? `${n} of your fleets there` : "Charted"}</em></span></button>
    ${on ? `<div class="aetrd"><p>${esc(R.d)}</p>${lk ? `<p class="aetlk">${esc(lk)}</p>` : ""}<dl class="kv"><dt>Type</dt><dd>${esc(R.cat)}${R.sub ? ` · ${esc(R.sub)}` : ""}</dd><dt>Access</dt><dd>${lk ? "Locked" : "Open"}</dd><dt>Discovery</dt><dd>${esc(aetDiscTxt(R.k))}</dd><dt>Recommended</dt><dd>fleet power ${fmt(R.rec)}+</dd>
      <dt>Objectives</dt><dd>${R.has.map(esc).join(" · ")}</dd><dt>Gameplay</dt><dd>${esc(R.play)}</dd><dt>Rewards</dt><dd>${R.rew.map(esc).join(" · ")}</dd><dt>Modifiers</dt><dd>${R.mods.map(([a, b]) => `<b>${esc(a)}</b>: ${esc(b)}`).join("<br>")}</dd>
      <dt>Commanders there</dt><dd>${aetPopTxt(R.k)}</dd><dt>Event</dt><dd>${aetFlux(T) ? "Gateway flux hour" : "None"}</dd><dt>Restrictions</dt><dd>${R.k === "int" ? "Server-versus-server areas stay closed until the Nexus War. " : ""}Transit ${ftime(R.tt * 1000)} each way.</dd></dl>
      <div class="aetacts">${lk ? "" : `<button class="btn${A.dest === R.k ? " pri" : ""}" data-act="aetDest" data-k="${R.k}">${A.dest === R.k ? "Destination set" : "Set as destination"}</button>`}${!lk || n ? `<button class="btn" data-act="aetView" data-k="${R.k}">View realm</button>` : ""}</div></div>` : ""}</div>`; }).join("")}</div>`; }
const aetDiscTxt = k => ({ int: "Reached when the First Aperture opens.", shat: "Chart it with Dimensional Navigation I (Aetherion Technology).", dom: "Decode the Dominion's coordinates: Ancient Signal Analysis III and a Silent Archive recovered in the Interstice.", tide: "Follow the Carcinid's old current: Dimensional Navigation III, after the Carcinid Tide has run." })[k] || "";
function aetPopTxt(k) { const n = aetOpenTx().filter(x => x.realm === k).length; return `${n ? `You (${n} fleet${n > 1 ? "s" : ""})` : "None of yours"}${G.aetPop && G.aetPop[k] ? ` · ${G.aetPop[k]} commander${G.aetPop[k] > 1 ? "s" : ""} in all` : ""}`; }
function aetWarHTML(T) { const n = Object.keys(G.players || {}).length;
  return `<div class="aetwar"><b>The Nexus War</b><p>A scheduled war inside the Interstice between whole servers: registration, balanced brackets of 2v2 or 4v4 servers, a protected breach, territory war over fortresses, relays, resource fields and gateway anchors, the assault on the Central Nexus, and a final reckoning that pays the winning servers and alliances.</p>
    <p class="aetlk">It needs other servers to fight. This galaxy is the only server for now, so no Nexus War is scheduled; nothing here asks you to register for one that cannot happen. It will open as its own extension once more servers are running.</p>
    <dl class="kv"><dt>Your server</dt><dd>${esc(aetServer())}${n ? ` · ${fmt(n)} commanders` : ""}</dd><dt>Bracket</dt><dd>None scheduled</dd><dt>Next war</dt><dd>Not scheduled</dd><dt>Your war marks</dt><dd>${fmt(aetS().mk || 0)} (earned only in a Nexus War)</dd></dl>
    <details class="crclore"><summary>How it will work</summary><p>Phases: Gateway Preparation (register, organise, prepare fleets), The Breach (fleets enter protected staging sectors), Territory War, Nexus Assault (capture the surrounding pylons, then hold the Nexus), Final Reckoning (scores settle, rewards pay, everyone is sent home safely).</p><p>Scoring rewards real contribution: objectives captured and held, structures defended, fleets destroyed (with protection against farming), convoys escorted, resources gathered and neutral threats defeated, so commanders of every size can help.</p></details></div>`; }
function aetFleetHTML(T) { const A = aetS(), R = AET_RB[A.dest] || AET_RB.int, lk = aetRealmLock(R.k, T), avail = originAvail(), sel = Object.fromEntries(Object.entries(pick).filter(([k, v]) => v > 0 && SH[k] && k !== "spyProbe")), cost = aetCost(sel, T), en = aetEn(T), op = aetOpenTx(), slots = aetSlots();
  delete avail.spyProbe; const can = !lk && sumShips(sel) && en >= cost && op.length < slots && !A.busy && !aetOff();
  const dests = AET_REALMS.map(r => { const l = aetRealmLock(r.k, T); return `<button class="${r.k === R.k ? "on" : ""}" data-act="aetDest" data-k="${r.k}"${l ? " disabled" : ""}>${esc(r.n.replace("The ", ""))}${l ? " 🔒" : ""}</button>`; }).join("");
  const list = op.length ? op.map(x => aetTxCard(x, T)).join("") : `<p class="note">No fleets beyond the Gateway.</p>`;
  return `<h3>Active missions</h3><div class="aettxs">${list}</div><h3>Send a fleet</h3><div class="note">Destination</div><div class="segc aetdest">${dests}</div>${lk ? `<p class="aetlk">${esc(lk)}</p>` : ""}
    ${(sheet.from && sheet.from !== "home") ? `<p class="note">Fleets cross from ${esc(S.homeName)}: the Gateway is linked to your homeworld's shipyards.</p>` : ""}${picker(avail)}
    <dl class="kv aetkv"><dt>Fleet</dt><dd>${fmt(sumShips(sel))} ships · power ${fmt(aetPow(sel))}${R.rec ? ` (recommended ${fmt(R.rec)}+)` : ""}</dd><dt>Departure</dt><dd>${esc(S.homeName)} → Aperture 001 → ${esc(R.n)}</dd><dt>Travel</dt><dd>charge ${ftime(AET_CHARGE)} + corridor ${ftime(R.tt * 1000)}</dd><dt>Energy</dt><dd>${cost} of ${Math.floor(en)}${aetFlux(T) ? " (flux hour +50%)" : ""}</dd><dt>Slots</dt><dd>${op.length}/${slots} in use</dd><dt>Return</dt><dd>any time it waits at the arrival gate · free · ${ftime(R.tt * 1000)}</dd></dl>
    <button class="btn wide amber" data-act="aetGo"${can ? "" : " disabled"}>${A.busy ? "Contacting the Gateway…" : sheet.arm ? `Confirm: send ${fmt(sumShips(sel))} ships to ${esc(R.n)}` : "Initiate transit"}</button>
    ${!can && sumShips(sel) && en < cost ? `<p class="note">Not enough transit energy: ${Math.floor(en)}/${cost}. It recharges 12 an hour.</p>` : ""}`; }
function aetTxCard(x, T) { const R = AET_RB[x.realm], t = x.t || {}, end = x.st === "RESERVED" ? (t.res || T) + AET_CHARGE : x.st === "IN_TRANSIT" ? t.eta : x.st === "RETURNING" ? t.reta : null, out = S.fleets.filter(f => f.aet === x.id).length;
  const btns = x.st === "ACTIVE" ? `<button class="btn" data-act="aetView" data-k="${x.realm}">View</button>${typeof aetMissionBtns === "function" ? aetMissionBtns(x) : ""}<button class="btn" data-act="aetRecall" data-id="${x.id}"${out ? " disabled" : ""}>Recall</button>` : x.st === "RESERVED" ? `<button class="btn" data-act="aetRecall" data-id="${x.id}">Cancel</button>` : "";
  return `<div class="aettx st-${x.st.toLowerCase()}"><div><b>${esc(R.n)} · ${aetStName(x)}${x.prev ? " · preview" : ""}</b><small>${aetShipsTxt(x.n)} · power ${fmt(aetPow(x.n))}</small>${end ? `<small>${x.st === "RETURNING" ? "Home" : x.st === "RESERVED" ? "Departs" : "Arrives"} in <span data-end="${end}">${ftime(end - T)}</span></small>` : ""}${out ? `<small>${out} squadron${out > 1 ? "s" : ""} out on missions in the realm</small>` : ""}${x.hold && (total(x.hold) || x.hold.fr) ? `<small>Hold: ${aetMatTxt(x.hold)}</small>` : ""}${x.err ? `<small class="aetlk">Waiting for the server (${esc(x.err)}); retrying.</small>` : ""}</div><div class="aetbtns">${btns}</div></div>`; }
function aetRewardsHTML(T) { const A = aetS(); return `<h3>Aetherion stores</h3><div class="mimmats">${Object.entries(AET_MAT).map(([k, [nm, col]]) => `<div class="mimmat"><i class="aetmi" style="--c:${col}"></i><b>${fmt(k === "fr" ? A.fr || 0 : A.m[k] || 0)}</b><small>${nm}</small></div>`).join("")}<div class="mimmat"><i class="aetmi" style="--c:#ff5a66"></i><b>${fmt(A.mk || 0)}</b><small>Nexus War Marks</small></div></div>
  ${typeof aetShopHTML === "function" ? aetShopHTML(T) : `<p class="note">Fragments and materials come home in your fleets' holds from the realms.</p>`}`; }
function aetMoreHTML(T) { const A = aetS(), hist = A.hist.slice(0, 20);
  return `${typeof aetResearchHTML === "function" ? aetResearchHTML(T) : ""}${typeof aetMissionsHTML === "function" ? aetMissionsHTML(T) : ""}
  <h3>Travel history</h3>${hist.length ? `<div class="aethist">${hist.map(h => `<div><b>${esc(AET_RB[h.realm] ? AET_RB[h.realm].n.replace("The ", "") : h.realm)}</b><span>${esc(({ reserved: "Departure booked", departed: "Entered the corridor", arrived: "Arrived", recalled: "Recalled", home: "Back home", lost: "Lost in battle" })[h.what] || h.what)} · ${fmt(h.n)} ships</span><em>${new Date(h.at).toLocaleString([], { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" })}</em></div>`).join("")}</div>` : `<p class="note">No crossings yet.</p>`}
  <h3>Help</h3><details class="crclore"><summary>How the Gateway unlocks</summary><p>It is the end of a story: the four Aetherion seasons after the first year of seasons tell how a fragment infected Vesper Station, how the station came alive and descended on Nhalis, how the planet was remade, and how the First Aperture rose from it. When the fourth season's finale ends, the Gateway opens for everyone, for good.</p></details>
  <details class="crclore"><summary>Travel, return and recovery</summary><p>A crossing is booked with the server before anything moves: your ships leave your homeworld only once the server has accepted it, and are back the moment it says the fleet is home. If the game closes, loses connection or the server restarts, the crossing carries on from the record. If the server ever has no record of a crossing your save remembers, the fleet is brought home automatically.</p></details>
  <details class="crclore"><summary>Realms and rewards</summary><p>Each realm has its own objectives and rewards (see Realms). Resources come home in your fleet's hold; Aetherion Fragments and materials go into the Aetherion stores, spent in the exchange and on Aetherion Technology.</p></details>
  <label class="aetlow"><input type="checkbox" data-act="aetLow"${S.aetLow ? " checked" : ""}> Reduced crossing effects</label>`; }
/* actions */
const AET_ACT = {
  aetOpen: d => openSheet({ type: "aet", tab: (d && d.t) || "gate" }),
  aetTab: d => { sheet.tab = d.t; sheet.arm = 0; sheet.armAll = 0; renderSheet(); },
  aetRx: d => { sheet.rx = sheet.rx === d.k ? null : d.k; renderSheet(); },
  aetDest: d => { if (aetRealmLock(d.k)) return; aetS().dest = d.k; sheet.arm = 0; dirty(); if (sheet.tab !== "fleet") sheet.tab = "fleet"; renderSheet(); },
  aetGo: async () => { const A = aetS(); if (A.busy) return; if (!sheet.arm) { sheet.arm = 1; renderSheet(); setTimeout(() => { if (sheet && sheet.arm) { sheet.arm = 0; renderSheet(); } }, 6000); return; } sheet.arm = 0;
    const sel = Object.fromEntries(Object.entries(pick).filter(([k, v]) => v > 0 && SH[k] && k !== "spyProbe")); if (await aetDeploy(A.dest, sel)) { for (const k in pick) delete pick[k]; sheet.pkSeen = 1; } },
  aetRecall: d => aetRecall(d.id),
  aetRecallAll: async () => { if (!sheet.armAll) { sheet.armAll = 1; renderSheet(); setTimeout(() => { if (sheet && sheet.armAll) { sheet.armAll = 0; renderSheet(); } }, 6000); return; } sheet.armAll = 0; for (const x of aetOpenTx()) if (["ACTIVE", "RESERVED"].includes(x.st)) await aetRecall(x.id); },
  aetView: d => { const c = $("#aetcine"); if (c) c.remove(); aetEnter(d.k); },
  aetLeave: () => aetLeave(),
  aetCineX: () => { const c = $("#aetcine"); if (c) c.remove(); },
  aetLow: () => { S.aetLow = !S.aetLow; dirty(); renderSheet(); },
  aetPrev: d => { if (!ownerFree()) return; const v = d.v; if (v === "off") S.aetPrev = null; else if (v === "open") S.aetPrev = { m: "open", at: now() }; else { const m = /^s(\d)_(\d)$/.exec(v); if (!m) return; S.aetPrev = { m: "saga", j: +m[1], w: +m[2], at: now() }; }
    dirty(); toast(v === "off" ? "Aetherion preview off." : `Previewing ${v === "open" ? "the open Gateway" : `${AET_SAGA[S.aetPrev.j][0]}, week ${S.aetPrev.w}`} (this device only).`); renderSheet(); },
  aetSyncNow: () => { aetSync(true); toast("Checking the Gateway's record…"); } };
