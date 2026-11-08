# v355: day and night on the base, following the player's own clock.
#  - colDayNight(W) each frame: daylight 07:30-17:30, dawn from 05:30 and dusk until 19:30 (warm low light), moonlight at night
#    (cool, dim, still casting shadows). Sky and haze darken; exposure lifts a little so the night stays readable.
#  - Night brings the lights up: building models' lit windows (emissive), their light halos, the city domes' windows.
#  - Pools of light on the ground (additive discs, POOL_MATS): under every street lamp and around each building model's lights,
#    faint by day, strong at night. Shared materials, so the whole base costs a few draw calls.
#  - `?tod=22` (any hour) forces a time of day for testing.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)

rep("function colBloom(W) {", r'''/* v355 light pools: a soft additive disc lying on the ground; one material per colour, faded together by colDayNight */
const POOL_MATS = {}; let DN_NIGHT = 0;
function poolMat(rgb) { rgb = rgb.split(",").map(v => Math.min(255, Math.round(v / 40) * 40)).join(","); if (POOL_MATS[rgb]) return POOL_MATS[rgb]; const m = new TH.MeshBasicMaterial({ map: glowTex(rgb, .9), transparent: true, opacity: .3, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false, polygonOffset: true, polygonOffsetFactor: -2 }); m.userData.op = rgb === "255,200,160" ? .8 : .9; return (POOL_MATS[rgb] = m); }
const POOL_G = () => POOL_G.g || (POOL_G.g = new TH.PlaneGeometry(1, 1).rotateX(-Math.PI / 2));
const GLB_EMI = []; // building model materials whose lit windows brighten at night
/* v355 the base's time of day from the player's clock */
function colDayNight(W) {
  const q = /[?&]tod=(\d+(?:\.\d+)?)/.exec(location.search), d = new Date(), hr = q ? +q[1] % 24 : d.getHours() + d.getMinutes() / 60;
  const up = clamp((hr - 5.5) / 2, 0, 1) * clamp((19.5 - hr) / 2, 0, 1), n = 1 - up, dusk = Math.min(1, up * n * 4), key = Math.round(hr * 60);
  if (W.dnKey === key && W.dnBg === W.scene.background.getHex()) return;
  if (!W.L) { W.L = {}; for (const o of W.scene.children) { if (o.isHemisphereLight) W.L.hemi = o; else if (o.isDirectionalLight && o.castShadow !== undefined && o === G.c3sun) W.L.sun = o; else if (o.isDirectionalLight) W.L.rim = o; else if (o.isPointLight) W.L.fill = o; }
    W.L.sun0 = W.L.sun && W.L.sun.color.clone(); W.L.hemi0 = W.L.hemi && W.L.hemi.color.clone(); }
  if (W.dnBg !== W.scene.background.getHex() || !W.bg0) { W.bg0 = W.scene.background.clone(); }
  const L = W.L, moon = new TH.Color(0x8fa8d8), duskC = new TH.Color(0xff9a5a);
  if (L.sun) { L.sun.intensity = 1.7 * up + .16 * n; L.sun.color.copy(L.sun0).lerp(duskC, dusk * .55).lerp(moon, n); }
  if (L.hemi) { L.hemi.intensity = .45 * up + .09 * n; L.hemi.color.copy(L.hemi0).lerp(new TH.Color(0x3a4a78), n); }
  if (L.rim) L.rim.intensity = .6 * up + .22 * n; if (L.fill) L.fill.intensity = .5 + .25 * n;
  const bg = W.bg0.clone().lerp(new TH.Color(0x03050a), n * .92).lerp(new TH.Color(0x6a3a26), dusk * .25); W.scene.background.copy(bg); if (W.scene.fog) W.scene.fog.color.copy(bg);
  W.renderer.toneMappingExposure = .78 + .07 * n;
  for (const m of GLB_EMI) m.emissiveIntensity = 2.6 * (1 + 1.1 * n);
  for (const k in POOL_MATS) POOL_MATS[k].opacity = POOL_MATS[k].userData.op * (.22 + .78 * n);
  DN_NIGHT = n; W.dnKey = key; W.dnBg = W.scene.background.getHex();
}
function colBloom(W) {''')
# keep the planet tint as the day colour: re-read it after a planet change
rep("const tn = TINT[bt.type] || TINT.home; W.ground.material.color.set(tn[0]); W.rockM.color.set(tn[1]); W.scene.background.set(tn[2]); if (W.scene.fog) W.scene.fog.color.set(tn[2]);",
    "const tn = TINT[bt.type] || TINT.home; W.ground.material.color.set(tn[0]); W.rockM.color.set(tn[1]); W.scene.background.set(tn[2]); if (W.scene.fog) W.scene.fog.color.set(tn[2]); W.bg0 = W.scene.background.clone(); W.dnKey = null; // v355 the day colour")
rep("  { const B = colBloom(W); let ok = false;", "  try { colDayNight(W); } catch (e) {} // v355\n  { const B = colBloom(W); let ok = false;")
# night-sensitive halos: brighter at night
rep('''fx.spots.slice(0, MOBILE ? 5 : 9).forEach((sp, i) => { const o = spr(glowTex(sp.c, 1), 0xffffff, .75 + .25 * sp.s);''',
    '''fx.spots.slice(0, MOBILE ? 4 : 6).forEach(sp => { const pl = new TH.Mesh(POOL_G(), poolMat(sp.c)); const g0 = at(sp.p); pl.position.set(g0.x, .02 - b.position.y, g0.z); pl.scale.setScalar(span * (.55 + .35 * sp.s)); pl.userData.nomini = 1; b.add(pl); anim.push([pl, "still", 0]); }); // v355 their light on the ground
    fx.spots.slice(0, MOBILE ? 5 : 9).forEach((sp, i) => { const o = spr(glowTex(sp.c, 1), 0xffffff, .75 + .25 * sp.s);''')
rep("m.emissiveMap = et; m.emissive.set(0xffffff); m.emissiveIntensity = 2.6;", "m.emissiveMap = et; m.emissive.set(0xffffff); m.emissiveIntensity = 2.6 * (1 + 1.1 * DN_NIGHT); if (!GLB_EMI.includes(m)) GLB_EMI.push(m);")
# street lamp pools
rep("lamps.forEach(([x, z], i) => { dm.position.set(x, 0, z); dm.updateMatrix(); post.setMatrixAt(i, dm.matrix); head.setMatrixAt(i, dm.matrix); }); post.castShadow = true; g.add(post, head);",
    "lamps.forEach(([x, z], i) => { dm.position.set(x, 0, z); dm.updateMatrix(); post.setMatrixAt(i, dm.matrix); head.setMatrixAt(i, dm.matrix); }); post.castShadow = true; g.add(post, head);\n  { const pool = new TH.InstancedMesh(POOL_G(), poolMat(\"255,200,140\"), lamps.length); lamps.forEach(([x, z], i) => { dm.position.set(x, .025, z); dm.scale.setScalar(1.7); dm.updateMatrix(); pool.setMatrixAt(i, dm.matrix); }); dm.scale.setScalar(1); pool.renderOrder = 2; g.add(pool); } // v355 each lamp's pool of light")
open(p, "w").write(h); print("ok")
