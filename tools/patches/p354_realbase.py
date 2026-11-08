# v354: a more realistic base view.
#  - Bloom (colBloom): the base renders into an off-screen target (tone mapped, sRGB, as on screen), its bright parts are pulled out at a
#    quarter of the resolution, blurred at two sizes and added back, so lights, glows and hot metal bleed light like a camera sees them.
#    WebGL2 only, Graphics > Effects on, not on WEAK phones; any failure falls back to the plain render. `?bloom=0` turns it off.
#  - Rocks: smooth, noise-displaced boulders and pebbles with a stone texture (cracks, grit, strata) instead of faceted dodecahedra.
#  - City domes: smooth domes with a panelled skin (seams, glass panes, a few lit windows) instead of 12-sided faceted ones.
#  - Ground: a finer regolith (1024 px on desktop, more octaves, cracks) and deeper relief.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)

# ---------- bloom ----------
rep("function drawColony(t) {", r'''/* v354 bloom for the base: render to a target, pull out the bright parts at 1/4 size, blur at two sizes, add back */
function colBloom(W) {
  if (W.bloom !== undefined) return W.bloom; W.bloom = null;
  try {
    const R = W.renderer; if (!R.capabilities.isWebGL2 || WEAK || gfx("fx") < 1 || /[?&]bloom=0/.test(location.search)) return null;
    const vs = "varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0., 1.); }";
    const mat = (fs, u) => new TH.ShaderMaterial({ uniforms: u, vertexShader: vs, fragmentShader: fs, depthTest: false, depthWrite: false, toneMapped: false });
    const bright = mat("uniform sampler2D tD; uniform float th; varying vec2 vUv; void main(){ vec3 c = texture2D(tD, vUv).rgb; float l = max(c.r, max(c.g, c.b)); gl_FragColor = vec4(c * smoothstep(th, th + .22, l), 1.); }", { tD: { value: null }, th: { value: .8 } });
    const blur = mat("uniform sampler2D tD; uniform vec2 dir; varying vec2 vUv; void main(){ vec3 s = texture2D(tD, vUv).rgb * .227; s += (texture2D(tD, vUv + dir).rgb + texture2D(tD, vUv - dir).rgb) * .195; s += (texture2D(tD, vUv + dir * 2.).rgb + texture2D(tD, vUv - dir * 2.).rgb) * .122; s += (texture2D(tD, vUv + dir * 3.).rgb + texture2D(tD, vUv - dir * 3.).rgb) * .054; s += (texture2D(tD, vUv + dir * 4.).rgb + texture2D(tD, vUv - dir * 4.).rgb) * .016; gl_FragColor = vec4(s, 1.); }", { tD: { value: null }, dir: { value: new TH.Vector2() } });
    const comp = mat("uniform sampler2D tS; uniform sampler2D tA; uniform sampler2D tB; uniform float k; varying vec2 vUv; void main(){ vec3 c = texture2D(tS, vUv).rgb; vec3 b = texture2D(tA, vUv).rgb * .7 + texture2D(tB, vUv).rgb * .9; gl_FragColor = vec4(c + b * k * (1. - c * .35), 1.); }", { tS: { value: null }, tA: { value: null }, tB: { value: null }, k: { value: MOBILE ? .5 : .62 } });
    const scene = new TH.Scene(), cam = new TH.OrthographicCamera(-1, 1, 1, -1, 0, 1), quad = new TH.Mesh(new TH.PlaneGeometry(2, 2), bright); quad.frustumCulled = false; scene.add(quad);
    const rt = (w, h, ms) => { const t = ms ? new TH.WebGLMultisampleRenderTarget(w, h, { format: TH.RGBAFormat }) : new TH.WebGLRenderTarget(w, h, { format: TH.RGBAFormat, minFilter: TH.LinearFilter, magFilter: TH.LinearFilter, depthBuffer: false }); if (ms) t.samples = 4; return t; };
    const B = { size: [0, 0], ms: GFX_AA || !MOBILE, quad, scene, cam, bright, blur, comp, rt, S: null, A: null, A2: null, C: null, C2: null };
    B.run = () => {
      const v = R.getDrawingBufferSize(new TH.Vector2()), w = Math.max(2, v.x | 0), h = Math.max(2, v.y | 0);
      if (B.size[0] !== w || B.size[1] !== h) { for (const k of ["S", "A", "A2", "C", "C2"]) if (B[k]) B[k].dispose();
        B.S = rt(w, h, B.ms); B.S.texture.encoding = TH.sRGBEncoding; const qw = Math.max(2, w >> 2), qh = Math.max(2, h >> 2), ew = Math.max(2, w >> 3), eh = Math.max(2, h >> 3);
        B.A = rt(qw, qh); B.A2 = rt(qw, qh); B.C = rt(ew, eh); B.C2 = rt(ew, eh); B.size = [w, h]; }
      const pass = (m, to) => { quad.material = m; R.setRenderTarget(to); R.render(scene, cam); };
      R.setRenderTarget(B.S); R.render(W.scene, W.cam);
      bright.uniforms.tD.value = B.S.texture; pass(bright, B.A);
      blur.uniforms.tD.value = B.A.texture; blur.uniforms.dir.value.set(1.2 / B.A.width, 0); pass(blur, B.A2);
      blur.uniforms.tD.value = B.A2.texture; blur.uniforms.dir.value.set(0, 1.2 / B.A.height); pass(blur, B.A);
      blur.uniforms.tD.value = B.A.texture; blur.uniforms.dir.value.set(1.6 / B.C.width, 0); pass(blur, B.C2);
      blur.uniforms.tD.value = B.C2.texture; blur.uniforms.dir.value.set(0, 1.6 / B.C.height); pass(blur, B.C);
      comp.uniforms.tS.value = B.S.texture; comp.uniforms.tA.value = B.A.texture; comp.uniforms.tB.value = B.C.texture; pass(comp, null);
    };
    W.bloom = B;
  } catch (e) { W.bloom = null; }
  return W.bloom;
}
function drawColony(t) {''')
rep("  W.renderer.render(W.scene, W.cam);\n  // building tags", "  { const B = colBloom(W); let ok = false; if (B) try { B.run(); ok = true; } catch (e) { W.bloom = null; W.renderer.setRenderTarget(null); } if (!ok) W.renderer.render(W.scene, W.cam); } // v354 bloom\n  // building tags")

# ---------- rocks ----------
rep("const rockM = new TH.MeshStandardMaterial({ color: 0x6d4232, roughness: 1, flatShading: true }), rockG = new TH.DodecahedronGeometry(1, 0), r = rnd(44);",
    "const rockT = rockTex(), rockM = new TH.MeshStandardMaterial({ color: 0x6d4232, map: rockT.map, bumpMap: rockT.bump, bumpScale: .9, roughness: .96, metalness: 0 }), rockG = rockGeo(2, 44), r = rnd(44); // v354 smooth noise-displaced stone")
rep("{ const pg = new TH.DodecahedronGeometry(.28, 0), im = new TH.InstancedMesh(pg, rockM, 520)", "{ const pg = rockGeo(1, 515).scale(.28, .28, .28), im = new TH.InstancedMesh(pg, rockM, 520)")
rep("function initColony(host) {", r'''/* v354 a boulder: an icosphere pushed in and out by layered noise (lumpy, with flat-ish fracture faces), smooth shaded */
function rockGeo(detail, seed) {
  const g = new TH.IcosahedronGeometry(1, detail), P = g.attributes.position, r = rnd(seed), F = Array.from({ length: 5 }, () => [r() * 2 - 1, r() * 2 - 1, r() * 2 - 1, .6 + r() * .5]).map(([x, y, z, c]) => { const l = Math.hypot(x, y, z) || 1; return [x / l, y / l, z / l, c]; });
  for (let i = 0; i < P.count; i++) { const x = P.getX(i), y = P.getY(i), z = P.getZ(i), n = Math.sin(x * 4.1 + seed) * Math.cos(y * 3.7 - seed) * .09 + Math.sin(z * 7.3 + x * 2.1) * .045 + Math.sin(y * 13 + z * 11) * .02;
    let s = 1 + n; for (const [a, b, c, d] of F) { const dp = x * a + y * b + z * c; if (dp > d) s = Math.min(s, d / dp + n * .3); } P.setXYZ(i, x * s, y * s * .82, z * s); }
  g.computeVertexNormals(); return g;
}
/* v354 stone: neutral grey-buff grit with darker veins, pits and pale strata (tinted per planet by the material colour) */
function rockTex() {
  if (rockTex.T) return rockTex.T; const Z = MOBILE ? 256 : 512, r = rnd(4321), hgt = new Float32Array(Z * Z);
  const vn = (() => { const P = Array.from({ length: 1024 }, () => r()), at = (x, y) => P[((x & 31) * 32 + (y & 31)) & 1023], sm = q => q * q * (3 - 2 * q); return (x, y) => { const xi = Math.floor(x), yi = Math.floor(y), xf = sm(x - xi), yf = sm(y - yi), a = at(xi, yi), b = at(xi + 1, yi), c = at(xi, yi + 1), d = at(xi + 1, yi + 1); return a + (b - a) * xf + (c - a) * yf + (a - b - c + d) * xf * yf; }; })();
  for (let y = 0; y < Z; y++) for (let x = 0; x < Z; x++) { const u = x / Z * 32, v = y / Z * 32; let hh = vn(u * .25, v * .25) * .45 + vn(u * .5, v * .5) * .25 + vn(u, v) * .18 + vn(u * 2, v * 2) * .12; const vein = Math.abs(vn(u * .4 + 7, v * .4 + 3) - .5); if (vein < .025) hh -= .25 * (1 - vein / .025); hgt[y * Z + x] = hh; }
  const map = texCanvas(Z, Z, (x, W, H) => { const img = x.createImageData(W, H), D = img.data; for (let i = 0; i < W * H; i++) { const hh = hgt[i], k = 178 + (hh - .5) * 170, st = Math.sin((Math.floor(i / W) / H) * 40 + hh * 6) > .92 ? 18 : 0; D[i * 4] = clamp(k + st + 6, 0, 255); D[i * 4 + 1] = clamp(k + st, 0, 255); D[i * 4 + 2] = clamp(k + st - 8, 0, 255); D[i * 4 + 3] = 255; } x.putImageData(img, 0, 0);
    for (let i = 0; i < Z * 2; i++) { x.fillStyle = r() < .6 ? "rgba(30,26,22,.5)" : "rgba(240,232,220,.35)"; x.fillRect(r() * W, r() * H, 1 + r() * 1.5, 1 + r() * 1.5); } });
  const bump = texCanvas(Z, Z, (x, W, H) => { const img = x.createImageData(W, H), D = img.data; for (let i = 0; i < W * H; i++) { const k = clamp(hgt[i] * 255, 0, 255); D[i * 4] = D[i * 4 + 1] = D[i * 4 + 2] = k; D[i * 4 + 3] = 255; } x.putImageData(img, 0, 0); });
  for (const t of [map, bump]) { t.wrapS = t.wrapT = TH.RepeatWrapping; t.repeat.set(2, 2); t.anisotropy = 4; } map.encoding = TH.sRGBEncoding;
  return (rockTex.T = { map, bump });
}
/* v354 a habitat dome's skin: panels with seams, glass panes and a few lit windows */
function domeTex() {
  if (domeTex.T) return domeTex.T; const r = rnd(2468), Wd = 512, Hd = 256;
  const map = texCanvas(Wd, Hd, (x, W, H) => { x.fillStyle = "#c9d0d6"; x.fillRect(0, 0, W, H); const cols = 24, rows = 8;
    for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) { const v = r(), px = i * W / cols, py = j * H / rows; x.fillStyle = v < .07 ? "#5d7184" : `rgb(${200 + v * 22 | 0},${205 + v * 21 | 0},${210 + v * 20 | 0})`; x.fillRect(px + 1, py + 1, W / cols - 2, H / rows - 2); }
    x.strokeStyle = "rgba(110,120,130,.7)"; x.lineWidth = 1.5; for (let i = 0; i <= cols; i++) { x.beginPath(); x.moveTo(i * W / cols, 0); x.lineTo(i * W / cols, H); x.stroke(); } for (let j = 0; j <= rows; j++) { x.beginPath(); x.moveTo(0, j * H / rows); x.lineTo(W, j * H / rows); x.stroke(); }
    for (let i = 0; i < 600; i++) { x.fillStyle = `rgba(90,80,70,${r() * .12})`; x.fillRect(r() * W, r() * H, 2 + r() * 6, 1 + r() * 3); } });
  const emi = texCanvas(Wd, Hd, (x, W, H) => { x.fillStyle = "#000"; x.fillRect(0, 0, W, H); const cols = 24, rows = 8; for (let j = 5; j < rows; j++) for (let i = 0; i < cols; i++) if (r() < .3) { x.fillStyle = r() < .75 ? "rgba(255,190,110,.95)" : "rgba(150,220,255,.9)"; x.fillRect(i * W / cols + 4, j * H / rows + 6, W / cols - 8, H / rows - 12); } });
  for (const t of [map, emi]) { t.encoding = TH.sRGBEncoding; t.anisotropy = 4; }
  return (domeTex.T = { map, emi });
}
function initColony(host) {''')

# ---------- domes ----------
rep("const domeM = new TH.MeshStandardMaterial({ color: 0xdde4ea, roughness: .32, metalness: .45, envMapIntensity: 1, flatShading: true });",
    "const DT = domeTex(), domeM = new TH.MeshStandardMaterial({ color: 0xffffff, map: DT.map, emissive: 0xffffff, emissiveMap: DT.emi, emissiveIntensity: 1.3, roughness: .3, metalness: .5, envMapIntensity: 1.1 }); // v354 panelled, smooth")
rep("spires = new TH.InstancedMesh(new TH.SphereGeometry(1, 12, 6, 0, TAU, 0, Math.PI / 2).translate(0, .28, 0), domeM, N);",
    "spires = new TH.InstancedMesh(new TH.SphereGeometry(1, lite ? 28 : 40, lite ? 10 : 14, 0, TAU, 0, Math.PI / 2).translate(0, .28, 0), domeM, N);")

# ---------- ground ----------
rep("const RW = 512, hgt = new Float32Array(RW * RW), rg = rnd(77);", "const RW = MOBILE ? 512 : 1024, hgt = new Float32Array(RW * RW), rg = rnd(77); // v354 finer on desktop")
rep("hgt[y * RW + x] = tn2(u * 8, v * 8, 8) * .5 + tn2(u * 16, v * 16, 16) * .3 + tn2(u * 32, v * 32, 32) * .2 + (rg() - .5) * .08; }",
    "{ let hh = tn2(u * 8, v * 8, 8) * .45 + tn2(u * 16, v * 16, 16) * .26 + tn2(u * 32, v * 32, 32) * .17 + tn2(u * 64, v * 64, 32) * .12 + (rg() - .5) * .06; const ck = Math.abs(tn2(u * 6 + 3.3, v * 6 + 1.7, 6) - .5); if (ck < .018) hh -= .22 * (1 - ck / .018); hgt[y * RW + x] = hh; } } // v354 a fourth octave and fine cracks")
rep("const ground = new TH.Mesh(gg, new TH.MeshStandardMaterial({ map: gt, bumpMap: gb, bumpScale: .06,", "const ground = new TH.Mesh(gg, new TH.MeshStandardMaterial({ map: gt, bumpMap: gb, bumpScale: .11,")
open(p, "w").write(h); print("ok")
