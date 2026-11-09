# v368: the Metal Extractor's conveyors move. The model is one solid mesh, so two animated belts are laid over its own ore conveyors (found
# from a top-down render with a grid: one along z at x .126 from z .48 to .10, one along x at z .30 from x .88 to .24, in model units). Each
# belt follows the model's surface (heights measured by casting rays down onto it), and its slats and glowing ore scroll toward the building.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep("/* v367 each building's signature animation,", r'''/* v368 the Metal Extractor's moving conveyors, laid over the model's own belts (model units: from the outer end to the building, width) */
const MINE_BELTS = [[[.126, .48], [.126, .1], .15], [[.88, .30], [.24, .30], .13]];
let BELT_M = null;
function beltMat() { if (BELT_M) return BELT_M; const t = texCanvas(256, 64, (x, W, H) => { const r = rnd(808); x.fillStyle = "#1b1d20"; x.fillRect(0, 0, W, H);
    for (let i = 0; i < W; i += 16) { x.fillStyle = "#2e3236"; x.fillRect(i, 0, 3, H); } // the slats
    for (let i = 0; i < 46; i++) { const cx = r() * W, cy = 12 + r() * (H - 24), rr = 3 + r() * 6, g = x.createRadialGradient(cx, cy, 0, cx, cy, rr); const hot = r() < .55;
      g.addColorStop(0, hot ? "#ffd08a" : "#b58a6a"); g.addColorStop(.6, hot ? "#ff7a2a" : "#6a4a3a"); g.addColorStop(1, "rgba(40,20,10,0)"); x.fillStyle = g; x.beginPath(); x.arc(cx, cy, rr, 0, TAU); x.fill(); }
    x.fillStyle = "#3a3f45"; x.fillRect(0, 0, W, 4); x.fillRect(0, H - 4, W, 4); }); // the belt's edges
  t.wrapS = TH.RepeatWrapping; t.encoding = TH.sRGBEncoding;
  return (BELT_M = new TH.MeshStandardMaterial({ map: t, emissive: 0xffffff, emissiveMap: t, emissiveIntensity: .75, roughness: .7, metalness: .3, polygonOffset: true, polygonOffsetFactor: -2 })); }
function mineBelts(src, b, at, s, anim) {
  const rc = new TH.Raycaster(), dn = new TH.Vector3(0, -1, 0), M = beltMat(); src.updateMatrixWorld(true);
  const yAt = (x, z, prev) => { rc.set(new TH.Vector3(x, 5, z), dn); const hit = rc.intersectObject(src, true)[0]; return hit ? hit.point.y : prev; };
  for (const [[x0, z0], [x1, z1], w] of MINE_BELTS) { const N = 10, len = Math.hypot(x1 - x0, z1 - z0), ux = (x1 - x0) / len, uz = (z1 - z0) / len, px = -uz * w / 2, pz = ux * w / 2, pos = [], uv = [], idx = []; let y = 0;
    for (let i = 0; i <= N; i++) { const f = i / N, cx = x0 + (x1 - x0) * f, cz = z0 + (z1 - z0) * f; y = Math.max(yAt(cx + px * .6, cz + pz * .6, y), yAt(cx - px * .6, cz - pz * .6, y)) + .012;
      for (const sd of [-1, 1]) { const v = at([cx + px * sd, y, cz + pz * sd]); pos.push(v.x, v.y, v.z); uv.push(f * len / w * .5, sd < 0 ? 0 : 1); }
      if (i < N) { const a = i * 2; idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); } }
    const g = new TH.BufferGeometry(); g.setAttribute("position", new TH.Float32BufferAttribute(pos, 3)); g.setAttribute("uv", new TH.Float32BufferAttribute(uv, 2)); g.setIndex(idx); g.computeVertexNormals();
    const m = new TH.Mesh(g, M); m.receiveShadow = true; m.userData.nobake = true; b.add(m); }
  anim.push([M, "beltScroll", 1]); }
/* v367 each building's signature animation,''')
rep("    try { bldUniq(k, b, anim, sz.y * s, span / 2); } catch (e) {} // v367 the building's own animation",
    "    try { bldUniq(k, b, anim, sz.y * s, span / 2); } catch (e) {} // v367 the building's own animation\n    if (k === \"metalMine\") try { mineBelts(src, b, at, s, anim); } catch (e) {} // v368 moving conveyors")
rep('''    else if (kind === "orbitF") {''', '''    else if (kind === "beltScroll") { if (o.map && o.userData.t !== T) { o.userData.t = T; o.map.offset.x = 1 - (T * .00045 * p) % 1; } } // v368 the conveyors run toward the building
    else if (kind === "orbitF") {''')
open(p, "w").write(h); print("ok")
# the conveyors' scroll animates a material: bakeStatic only walks animated 3D objects
h = open(p).read()
rep("  for (const [o] of anim) if (!o.isMesh && !o.isSprite && o.children.length && !o.userData.baked && o !== root)", "  for (const [o] of anim) if (o.isObject3D && !o.isMesh && !o.isSprite && o.children.length && !o.userData.baked && o !== root)")
open(p, "w").write(h); print("ok2")
