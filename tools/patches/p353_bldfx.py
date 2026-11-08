# v353: living building models on the base. Each Meshy model is one textured mesh, so the effects are added around it, placed from the
# model itself when it loads (glbLights):
#  - Lit windows and lights: the bright, coloured texels of its colour map (painted windows, panels, tanks, furnaces) become a glow map
#    (emissiveMap), so they shine instead of being paint. White hull panels stay unlit (saturation weighting).
#  - Light halos: the triangles whose texels glow are found and clustered; additive halos sit on the strongest few, breathing slowly.
#  - The model's highest points carry chimney smoke, vapour or steam (per building, BLD_FX) and a blinking beacon.
#  - Shipyard, Repair Yard, Drone Works and Nanite Assembly get welding flashes at a lit spot.
# New base animation kind "smoke": a soft puff that rises, drifts, grows and fades. Slower Android phones (WEAK) keep the old buildings.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)

# 1) analysis after load, buildings only
rep("Promise.all(ps).then(() => { const bb = new TH.Box3().setFromObject(s); s.userData.bb = bb; GLB[k].scene = s; done(); glbReady(k); });",
    "Promise.all(ps).then(() => GLB_BLDS.has(k) ? glbLights(k, s) : null).then(() => { const bb = new TH.Box3().setFromObject(s); s.userData.bb = bb; GLB[k].scene = s; done(); glbReady(k); });")

rep("function glbNext() {", r'''/* v353 what each building breathes out: smoke colour (r,g,b), how many chimneys, a beacon, welding flashes */
const BLD_FX = {
  metalMine: { smoke: "150,144,138", n: 2, beacon: 1 }, crystalMine: { beacon: 1 }, gasSynth: { smoke: "150,232,165", n: 2 }, solar: { beacon: 1 },
  shipyard: { weld: 2, beacon: 1 }, metalStore: { beacon: 1 }, crystalStore: {}, gasTank: { smoke: "150,232,165", n: 1 }, robotics: { weld: 1, smoke: "150,146,140", n: 1 },
  lab: { beacon: 1 }, radar: { beacon: 1 }, fusion: { smoke: "232,238,244", n: 2 }, repairYard: { weld: 2 }, nanite: { smoke: "222,230,238", n: 1, weld: 1 },
  fortress: { beacon: 1 }, terraformer: { smoke: "232,238,244", n: 1 }, allyDepot: { beacon: 1 }, lunarBase: { beacon: 1 }, phalanx: { beacon: 1 } };
/* v353 read a building model's own lights: a glow map from its bright coloured texels, the lit spots on its surface, and its highest points */
async function glbLights(k, s) {
  try {
    let mesh = null; s.traverse(o => { if (o.isMesh && !mesh) mesh = o; }); if (!mesh) return;
    const m = mesh.material, img = m.map && m.map.image; if (!img || !m.isMeshStandardMaterial) return;
    const A = 512, c = document.createElement("canvas"); c.width = c.height = A; const x = c.getContext("2d"); x.drawImage(img, 0, 0, A, A);
    const id = x.getImageData(0, 0, A, A), D = id.data, Wt = new Float32Array(A * A);
    for (let i = 0; i < A * A; i++) { const r = D[i * 4] / 255, g = D[i * 4 + 1] / 255, b = D[i * 4 + 2] / 255, mx = Math.max(r, g, b), mn = Math.min(r, g, b), sat = mx > 0 ? (mx - mn) / mx : 0;
      const w = clamp((mx - .4) / .3, 0, 1) * clamp((sat - .16) / .3, 0, 1); Wt[i] = w; D[i * 4] *= w; D[i * 4 + 1] *= w; D[i * 4 + 2] *= w; D[i * 4 + 3] = 255; }
    x.putImageData(id, 0, 0);
    let et; if (window.createImageBitmap) { const bm = await createImageBitmap(c); et = new TH.Texture(bm); c.width = c.height = 0; } else et = new TH.CanvasTexture(c);
    et.flipY = false; et.encoding = TH.sRGBEncoding; et.needsUpdate = true; m.emissiveMap = et; m.emissive.set(0xffffff); m.emissiveIntensity = 2.6; m.envMapIntensity = 1.25; m.needsUpdate = true;
    // lit spots: triangles whose texels glow, clustered
    const g = mesh.geometry, P = g.attributes.position, U = g.attributes.uv, I = g.index; if (!P || !U) return;
    const n = I ? I.count / 3 : P.count / 3, tri = [], bb = new TH.Box3().setFromBufferAttribute(P), size = Math.max(bb.max.x - bb.min.x, bb.max.y - bb.min.y, bb.max.z - bb.min.z);
    const vi = j => I ? I.getX(j) : j;
    for (let t = 0; t < n; t++) { const a = vi(t * 3), b = vi(t * 3 + 1), c2 = vi(t * 3 + 2), u = (U.getX(a) + U.getX(b) + U.getX(c2)) / 3, v = (U.getY(a) + U.getY(b) + U.getY(c2)) / 3;
      const px = clamp(Math.floor(u * A), 0, A - 1), py = clamp(Math.floor(v * A), 0, A - 1), w = Wt[py * A + px]; if (w < .3) continue;
      tri.push([w, (P.getX(a) + P.getX(b) + P.getX(c2)) / 3, (P.getY(a) + P.getY(b) + P.getY(c2)) / 3, (P.getZ(a) + P.getZ(b) + P.getZ(c2)) / 3, px, py]); }
    tri.sort((p1, p2) => p2[0] - p1[0]); const spots = [], min = size * .14;
    for (const t of tri) { if (spots.length >= 9) break; if (spots.some(sp => Math.hypot(sp.p[0] - t[1], sp.p[1] - t[2], sp.p[2] - t[3]) < min)) continue;
      const o = (t[5] * A + t[4]) * 4, w = Math.max(t[0], .01), r = Math.min(255, D[o] / w), gg = Math.min(255, D[o + 1] / w), bl = Math.min(255, D[o + 2] / w), mx = Math.max(r, gg, bl, 1);
      spots.push({ p: [t[1], t[2], t[3]], c: [r, gg, bl].map(v => Math.round(140 + 115 * v / mx)).join(","), s: t[0], ph: spots.length * 1.7 }); }
    // highest points (chimneys, masts)
    const peaks = [], vs = []; for (let i = 0; i < P.count; i += 3) vs.push([P.getY(i), P.getX(i), P.getZ(i)]); vs.sort((p1, p2) => p2[0] - p1[0]);
    for (const v of vs.slice(0, Math.max(40, vs.length * .04 | 0))) { if (peaks.length >= 3) break; if (peaks.some(q => Math.hypot(q[0] - v[1], q[2] - v[2]) < size * .2)) continue; peaks.push([v[1], v[0], v[2]]); }
    s.userData.fx = { spots, peaks };
  } catch (e) {}
}
const PUFFT = {}; const puffTex = col => PUFFT[col] || (PUFFT[col] = new TH.CanvasTexture(puffSprite(col)));
function glbNext() {''')

# 2) effects placed with the building
rep("function glbBld(k, b, big, small) {", "function glbBld(k, b, big, small, anim) {")
rep("  b.add(m); return true;\n}", r'''  b.add(m);
  const fx = src.userData.fx, F = BLD_FX[k] || {}; if (fx && anim && !WEAK) {
    const at = v => new TH.Vector3(v[0] * s + m.position.x, v[1] * s + m.position.y, v[2] * s + m.position.z), span = Math.max(sz.x, sz.z) * s, add = (o, kind, ph) => { b.add(o); anim.push([o, kind, ph || 0]); return o; };
    const spr = (map, col, op) => new TH.Sprite(new TH.SpriteMaterial({ map, color: col || 0xffffff, transparent: true, opacity: op == null ? 1 : op, blending: TH.AdditiveBlending, depthWrite: false }));
    fx.spots.slice(0, MOBILE ? 5 : 9).forEach((sp, i) => { const o = spr(glowTex(sp.c, 1), 0xffffff, .75 + .25 * sp.s); o.position.copy(at(sp.p)); const sc = span * (.2 + .16 * sp.s); o.scale.setScalar(sc); o.userData.s0 = sc; add(o, "glowP", sp.ph); });
    if (F.smoke) fx.peaks.slice(0, F.n || 1).forEach((pk, j) => { for (let i = 0; i < 4; i++) { const o = new TH.Sprite(new TH.SpriteMaterial({ map: puffTex(F.smoke), transparent: true, opacity: 0, depthWrite: false }));
      o.position.copy(at(pk)); const sc = span * .26; o.scale.setScalar(sc); Object.assign(o.userData, { s0: sc, rise: span * .9, drift: span * .3, op: /^2/.test(F.smoke) ? .7 : .85 }); add(o, "smoke", i / 4 + j * .13); } });
    if (F.beacon && fx.peaks[0]) { const o = spr(glowTex("255,70,50", 1), 0xffffff, .95); o.position.copy(at(fx.peaks[0])); o.position.y += span * .03; o.scale.setScalar(span * .16); add(o, "blink", hash(k) % 7); }
    for (let i = 0; i < (F.weld || 0) && i < fx.spots.length; i++) { const o = spr(glowTex("200,230,255", 1), 0xffffff, .95); o.position.copy(at(fx.spots[i].p)); o.position.y += span * .02; const sc = span * .14; o.scale.setScalar(sc); o.userData.s0 = sc; add(o, "flick", i * 2.3); }
  }
  return true;
}''')
rep("  if (!glbBld(k, b, big, small) && !artBld(k, b, era, C, anim)) switch (k) {", "  if (!glbBld(k, b, big, small, anim) && !artBld(k, b, era, C, anim)) switch (k) {")

# 3) the smoke animation
rep('''    else if (kind === "puff") { const u = o.userData; if (u.y0 == null) u.y0 = o.position.y;''',
    '''    else if (kind === "smoke") { const u = o.userData; if (u.y0 == null) { u.y0 = o.position.y; u.x0 = o.position.x; } const q = (T * .00016 + p) % 1; o.position.y = u.y0 + q * u.rise; o.position.x = u.x0 + q * u.drift; o.scale.setScalar(u.s0 * (.55 + q * 2.4)); o.material.opacity = u.op * Math.sin(Math.PI * Math.min(1, q * 1.15)); o.material.rotation = q * 1.2 + p * 6; } // v353 chimney smoke and steam
    else if (kind === "puff") { const u = o.userData; if (u.y0 == null) u.y0 = o.position.y;''')
open(p, "w").write(h); print("ok")
