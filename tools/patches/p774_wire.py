"""v774: World Boss remaster, surface detail (owner: "add details to remaster all of these new models"). The v760+ remodels were
built from clean machined parts with no surface texture, so up close they read as smooth, plain plastic next to the older models.
Every remastered boss now carries a fine surface layer drawn in the shader (no files, crisp at any size): staggered armour panels
with recessed seams, rows of rivets, panels at slightly different heights and finishes, and soft grime in the recesses, so the light
breaks up across the hull the way it does in the paintings. Four finishes: machined plate (Warden, Conduit, Overlord, Devourer, Kraken,
Leviathan, Elementals, Vaelthar, Aexion), carved stone blocks (Khezaroth), battered scrap plate with rust (Iron Tyrant) and living
scales (Matriarch, Medusara). Shapes, colours and moves are unchanged. Applies on top of v773."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 773;", "const GAME_V = 774;")

DET = r'''
  /* v774 remaster: a fine surface layer for the remodelled World Bosses, drawn in the shader in the part's own space (triplanar):
     staggered panels with recessed seams, rivets, panels at slightly different heights and finishes, grime in the recesses.
     Styles: 0 machined plate, 1 carved stone, 2 living scales, 3 battered scrap plate. uDS = panel size in model units. */
  const DET_GLSL = `uniform float uDS; uniform float uDK; uniform float uDB; varying vec3 vDP; varying vec3 vDN;
float dH21(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float dVN(vec3 p) { vec3 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f); float n = dot(i, vec3(1., 57., 113.));
  vec4 a = fract(sin(vec4(n, n + 1., n + 57., n + 58.)) * 43758.5453), b = fract(sin(vec4(n + 113., n + 114., n + 170., n + 171.)) * 43758.5453);
  vec4 m = mix(a, b, f.z); vec2 q = mix(m.xy, m.zw, f.y); return mix(q.x, q.y, f.x); }
vec3 dPlane(vec2 p) { float aa = clamp(length(fwidth(p)), .0005, .5);
#if DSTYLE == 2
  p *= vec2(1., 1.4); float row = floor(p.y); p.x += mod(row, 2.) * .5; vec2 c = floor(p), f = fract(p); float id = dH21(c);
  vec2 d = f - vec2(.5, .15); float r = length(d * vec2(1., 1.25)); float sc = 1. - smoothstep(.62 - aa * 1.5, .62, r);
  float seam = 1. - smoothstep(.0, .1 + aa, .62 - r); return vec3(sc * (.35 + f.y * .5) - seam * .6, seam * .7, id);
#else
  float row = floor(p.y); p.x += dH21(vec2(row, 3.7)) * 2.3; p.x *= (DSTYLE == 1 ? .55 : .8); vec2 c = floor(p), f = fract(p); float id = dH21(c);
  if (DSTYLE != 1 && id > .62) { float h2 = step(.5, f.x); f.x = fract(f.x * 2.); c.x += h2 * .5; id = dH21(c + 1.7); }
  vec2 e = min(f, 1. - f); float w = DSTYLE == 1 ? .045 : .03, ed = min(e.x * (DSTYLE == 1 ? .55 : .8), e.y);
  float seam = 1. - smoothstep(w, w + aa * 1.8 + .012, ed);
  float rv = 0.; if (DSTYLE != 1) { vec2 rp = vec2(fract(f.x * 7.) - .5, (f.y - .12) * 7. * (DSTYLE == 3 ? 1. : .8)); rv = (1. - smoothstep(.16, .24 + aa * 7., length(rp))) * step(.45, fract(id * 7.31));
    vec2 rp2 = vec2(rp.x, (f.y - .88) * 7.); rv = max(rv, (1. - smoothstep(.16, .24 + aa * 7., length(rp2))) * step(.45, fract(id * 7.31))); }
  float inset = 0.; if (id < .22 && DSTYLE != 1) { vec2 e2 = min(f - .18, .82 - f); inset = smoothstep(0., .02 + aa, min(e2.x * .8, e2.y)) ; }
  return vec3((id - .5) * .3 - seam + rv * .55 - inset * .25, max(seam, inset * .25), id);
#endif
}
vec4 udfDet() { vec3 P = vDP / uDS, N = abs(normalize(vDN)); N = pow(N, vec3(4.)); N /= (N.x + N.y + N.z + 1e-4);
  vec3 a = dPlane(P.zy + vec2(.0, .0)), b = dPlane(P.xz + vec2(3.1, 1.3)), c = dPlane(P.xy + vec2(7.7, 5.2)); vec3 r = a * N.x + b * N.y + c * N.z;
  float g = dVN(vDP / uDS * .9) * .6 + dVN(vDP / uDS * 3.7) * .4; return vec4(r, g); }
`;
  function detOn(m, st, ds) { if (!m || m.userData.det) return; m.userData.det = 1; const prev = m.onBeforeCompile, pk = m.customProgramCacheKey ? m.customProgramCacheKey.bind(m) : null, k = m.normalMap && m.normalMap !== cache.flatN ? .6 : 1;
    m.extensions = Object.assign({}, m.extensions, { derivatives: true }); if (!m.normalMap) { if (!cache.flatN) { cache.flatN = new TH.DataTexture(new Uint8Array([128, 128, 255, 255]), 1, 1, TH.RGBAFormat); cache.flatN.needsUpdate = true; } m.normalMap = cache.flatN; m.normalScale = new TH.Vector2(1, 1); } /* a flat normal map turns on the derivative extension on WebGL1 phones */ m.customProgramCacheKey = () => (pk ? pk() : "") + "|det" + st;
    m.onBeforeCompile = (sh, r) => { if (prev) prev(sh, r); sh.uniforms.uDS = { value: ds }; sh.uniforms.uDK = { value: k }; sh.uniforms.uDB = { value: st === 1 ? .045 : st === 2 ? .03 : .035 };
      sh.vertexShader = "varying vec3 vDP; varying vec3 vDN;\n" + sh.vertexShader.replace("#include <begin_vertex>", "#include <begin_vertex>\n vDP = position; vDN = normal;");
      sh.fragmentShader = "#define DSTYLE " + st + "\n" + DET_GLSL + sh.fragmentShader
        .replace("#include <color_fragment>", "#include <color_fragment>\n vec4 DT = udfDet(); float DG = smoothstep(.35, .85, DT.w); diffuseColor.rgb *= (1. - DT.y * .5 * uDK) * (.9 + DT.z * .2 * uDK) * (1. - DG * " + (st === 3 ? ".35" : ".16") + " * uDK);" + (st === 3 ? " diffuseColor.rgb = mix(diffuseColor.rgb, vec3(.32, .14, .05) * (.5 + DT.w), smoothstep(.62, .9, DT.w) * .45);" : ""))
        .replace("#include <roughnessmap_fragment>", "#include <roughnessmap_fragment>\n roughnessFactor = clamp(roughnessFactor + (DT.z - .5) * .16 * uDK + DT.y * .3 * uDK + DG * " + (st === 3 ? ".3" : ".12") + " * uDK, .04, 1.);")
        .replace("#include <normal_fragment_maps>", "#include <normal_fragment_maps>\n { float DH = DT.x * uDS * uDB * uDK + DT.w * uDS * .006; vec3 sX = dFdx(-vViewPosition), sY = dFdy(-vViewPosition), R1 = cross(sY, normal), R2 = cross(normal, sX); float fD = dot(sX, R1); vec3 gr = sign(fD) * (dFdx(DH) * R1 + dFdy(DH) * R2); normal = normalize(abs(fD) * normal - gr); }"); }; }
  const DET_ST = { warden: [0, 26], conduit: [0, 26], overlord: [0, 30], devourer: [0, 34], kraken: [0, 34], leviathan: [0, 40], elemental: [0, 30], vaelthar: [0, 38], aexion: [0, 34], khezaroth: [1, 16], tyrant: [3, 30], matriarch: [2, 60], medusara: [2, 70] };
  function detail(b) { const st = b.det; if (!st || !b.grp) return; const box = new TH.Box3(); b.grp.updateMatrixWorld(true);
    b.grp.traverse(o => { if (o.isMesh && o.material && !Array.isArray(o.material) && !o.material.transparent && o.material.blending !== TH.AdditiveBlending) box.expandByObject(o); }); if (box.isEmpty()) return;
    const L = box.getSize(new TH.Vector3()).length(), ds = L / st[1];
    b.grp.traverse(o => { const ms = Array.isArray(o.material) ? o.material : [o.material]; for (const m of ms) if (m && m.isMeshStandardMaterial && !(m.transparent && m.opacity < .95) && m.blending !== TH.AdditiveBlending) detOn(m, st[0], ds); }); }
'''
rep("  function prep(b, env) { b.grp.traverse(o => { const m = o.material; if (m && m.isMeshStandardMaterial && env) { m.envMap = env; m.needsUpdate = true; } }); return b; }",
    DET + "  function prep(b, env) { if (b && b.det && env) try { detail(b); } catch (e) {} b.grp.traverse(o => { const m = o.material; if (m && m.isMeshStandardMaterial && env) { m.envMap = env; m.needsUpdate = true; } }); return b; }")
rep("""EL, prep };
})(typeof window !== "undefined" ? window : globalThis);""", """EL, prep };
  for (const k of Object.keys(DET_ST)) { const f = root.BOSS3D[k]; if (typeof f === "function") root.BOSS3D[k] = (...a) => { const o = f(...a); if (o && o.grp && !PAINT) o.det = DET_ST[k]; return o; }; } /* v774 */
})(typeof window !== "undefined" ? window : globalThis);""")
open(p, "w", encoding="utf-8").write(s)
print("ok")

# --- Vaelthar: the wing membranes get scalloped trailing edges between the finger bones (they read as flat boxes) and are shaded:
#     bright at the wrist, darker toward the edges, lighter ribs along each bone ---
s = open(p, encoding="utf-8").read()
rep("""      for (let k = 0; k < tips.length - 1; k++) { const a = J[2], b = tips[k], c = tips[k + 1], m1 = b.clone().lerp(c, .5).lerp(a, .18); for (const tri of [[a, b, m1], [a, m1, c]]) for (const p of tri) { pos.push(p.x, p.y, p.z); uv.push(...uvOf(p)); } }
      { const fl = V(sx * .4, -5.5, .3); for (const tri of [[J[0], J[1], tips[4]], [J[1], J[2], tips[4]], [J[0], tips[4], fl]]) for (const p of tri) { pos.push(p.x, p.y, p.z); uv.push(...uvOf(p)); } }
      const mg = new TH.BufferGeometry(); mg.setAttribute("position", new TH.Float32BufferAttribute(pos, 3)); mg.setAttribute("uv", new TH.Float32BufferAttribute(uv, 2)); mg.computeVertexNormals();""",
"""      const vc = [], put = (p, k) => { pos.push(p.x, p.y, p.z); uv.push(...uvOf(p)); vc.push(k, k, k); }, NS = LO ? 5 : 9; /* v774 scalloped trailing edges, shaded membrane */
      const scal = (a, b, c, dep, ka, kb, kc) => { let prev = b, pk = kb; for (let i = 1; i <= NS; i++) { const t = i / NS, q = b.clone().lerp(c, t).lerp(a, dep * Math.sin(Math.PI * t)), qk = (kb + (kc - kb) * t) * (1 - .3 * Math.sin(Math.PI * t)); put(a, ka); put(prev, pk); put(q, qk); prev = q; pk = qk; } };
      for (let k = 0; k < tips.length - 1; k++) scal(J[2], tips[k], tips[k + 1], .3, 1.25, .8, .8);
      { const fl = V(sx * .4, -5.5, .3); for (const [tri, ks] of [[[J[0], J[1], tips[4]], [.9, 1.1, .8]], [[J[1], J[2], tips[4]], [1.1, 1.25, .8]]]) tri.forEach((q, i) => put(q, ks[i])); scal(J[0], tips[4], fl, .26, .9, .8, .65); }
      const mg = new TH.BufferGeometry(); mg.setAttribute("position", new TH.Float32BufferAttribute(pos, 3)); mg.setAttribute("uv", new TH.Float32BufferAttribute(uv, 2)); mg.setAttribute("color", new TH.Float32BufferAttribute(vc, 3)); mg.computeVertexNormals();""")
rep("const memM = new TH.MeshBasicMaterial({ map: memT, color: 0x6e5e92,", "const memM = new TH.MeshBasicMaterial({ map: memT, vertexColors: true, color: 0x6e5e92,")
open(p, "w", encoding="utf-8").write(s)
print("ok2")

# --- Aexion: the dagger hull gets a working deck: turrets with twin barrels, armour plates along each edge, vent grilles,
#     sensor masts at the prow (they ride the wings in the warform) ---
s = open(p, encoding="utf-8").read()
rep("""      for (const y of [8, 1, -6, -12]) { const m = glowBar(Math.abs(O[2][0]) * .55, .12, .12); m.position.set(sx * Math.abs(O[2][0]) * .45, y, -2.12); h.add(m); }
      return h; });""", """      for (const y of [8, 1, -6, -12]) { const m = glowBar(Math.abs(O[2][0]) * .55, .12, .12); m.position.set(sx * Math.abs(O[2][0]) * .45, y, -2.12); h.add(m); }
      { /* v774 deck detail */ const ex = y => { const P = O.map(([x, yy]) => [Math.abs(x), yy]); for (let k = 0; k < P.length - 2; k++) { const [x0, y0] = P[k], [x1, y1] = P[k + 1]; if ((y <= y0 && y >= y1)) return x0 + (x1 - x0) * (y - y0) / ((y1 - y0) || 1); } return 4; };
        for (const [y, x] of [[15, 2.2], [7, 3.3], [-1, 3.9], [-8.5, 3.7]]) { const t = new TH.Group(); t.position.set(sx * x, y, -2.2); h.add(t); const bs = new TH.Mesh(new TH.CylinderGeometry(.8, .95, .45, 10), MD); bs.rotation.x = Math.PI / 2; t.add(bs);
          const hd = slab(1.0, 1.2, .55, MA, .3, .8); hd.position.z = -.45; t.add(hd); for (const dx of [-.26, .26]) { const br = new TH.Mesh(new TH.CylinderGeometry(.1, .12, 2.0, 6), MA); br.position.set(dx, 1.4, -.5); t.add(br); } const ey = glowBar(.5, .12, .1); ey.position.set(0, .3, -.75); t.add(ey); }
        for (let k = 0; k < 10; k++) { const y = 21 - k * 3.6, wx = ex(y); const pl = slab(.9, 2.6, .32, k % 2 ? MD : MA, .25, .85); pl.position.set(sx * Math.max(.8, wx - .95), y, -1.6); pl.rotation.z = sx * .06; h.add(pl); }
        for (const y0 of [11.5, -4]) for (let k = 0; k < 5; k++) { const v = slab(1.7, .2, .2, MD, .08, 1); v.position.set(sx * 1.6, y0 - k * .45, -2.05); h.add(v); }
        for (const [y, L] of [[23, 2.6], [20.5, 1.6]]) { const ms = new TH.Mesh(new TH.CylinderGeometry(.06, .1, L, 5), MA); ms.rotation.x = Math.PI / 2; ms.position.set(sx * .9, y, -1.9 - L / 2); h.add(ms); const tp = glowBar(.16, .16, .16); tp.position.set(sx * .9, y, -1.9 - L); h.add(tp); } }
      return h; });""")
open(p, "w", encoding="utf-8").write(s)
print("ok3")

# --- Overlord: armour collars with lit slits along each thigh, a second piston on the far side ---
s = open(p, encoding="utf-8").read()
rep("""      { const cyl = strut(V(.3, -.55, 0), V(2.0, 1.1, 0), .16, .16, MD, 8); cx.add(cyl); const rod = strut(V(2.0, 1.1, 0), V(2.9, 2.0, 0), .08, .08, M, 8); cx.add(rod); }""",
"""      { const cyl = strut(V(.3, -.55, 0), V(2.0, 1.1, 0), .16, .16, MD, 8); cx.add(cyl); const rod = strut(V(2.0, 1.1, 0), V(2.9, 2.0, 0), .08, .08, M, 8); cx.add(rod); }
      { /* v774 thigh armour collars and a second piston */ const th = Math.atan2(kp.y, kp.x); for (const q of [.3, .52, .74]) { const c = box(.42, 1.8, 1.3, q === .52 ? M : ML); c.position.copy(kp).multiplyScalar(q); c.rotation.z = th; cx.add(c); const g = box(.08, 1.1, 1.34, glowMat(VIO2, .8)); g.position.copy(c.position); g.rotation.z = th; g.translateX(.24); cx.add(g); }
        for (const z of [-.62, .62]) { const p2 = strut(V(-.2, .5, z), V(1.6, 2.6, z), .12, .12, MD, 8); cx.add(p2); } }""")
open(p, "w", encoding="utf-8").write(s)
print("ok4")
