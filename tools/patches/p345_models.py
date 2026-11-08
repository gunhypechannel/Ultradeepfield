# v345: Meshy-made 3D models. 18 ship hulls and 11 base buildings are now textured models (docs/models/<id>.glb, made from each card's art).
# Ships: the studio portrait (card hero shot and the battle sprite) uses the model in place of the hand-built hull once it has loaded.
# Buildings: the base shows the model on its plot from Lv.1 (it grows with each era, the same way the old model did).
# Each model loads the first time it is needed (about 0.7 MB a ship, 1 to 3 MB a building), so nothing extra downloads up front; until it
# arrives the old model is shown and it swaps in when ready. Anything that fails to load keeps the old model.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)

rep('<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>',
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n'
    '<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>')

rep('function bModel(k, L, busy) {', r'''/* ---------- v345 Meshy models: textured hulls and buildings made from the card art (docs/models/<id>.glb) ----------
   Meshy exports each model about 1.9 units long, Y up; ships face -X (the game's hulls face +X, so they turn half a circle). */
const GLB_SHIPS = new Set(["fighter", "heavyFighter", "hauler", "heavyCargo", "recycler", "lancer", "ark", "corvette", "battleship", "bastion", "bomber", "destroyer", "dreadnought", "escortCarrier", "supercarrier", "guardian", "tender", "spyProbe"]);
const GLB_BLDS = new Set(["metalMine", "crystalMine", "gasSynth", "solar", "shipyard", "metalStore", "crystalStore", "gasTank", "robotics", "lab", "radar"]);
const GLB = {};
function glbOn() { return !!(TH && TH.GLTFLoader) && !/[?&]glb=0/.test(location.search); }
function glbGet(k) {
  const e = GLB[k]; if (e) return e.scene || null; if (!glbOn()) return null;
  GLB[k] = {};
  try {
    new TH.GLTFLoader().load("models/" + k + ".glb?v=" + GAME_V, g => {
      const s = g.scene; s.traverse(o => { if (o.isMesh) { const m = o.material; if (m && m.isMeshStandardMaterial) { m.envMapIntensity = .9; if (m.map) m.map.anisotropy = 4; } } });
      const bb = new TH.Box3().setFromObject(s); s.userData.bb = bb; GLB[k].scene = s; glbReady(k);
    }, undefined, () => { GLB[k].fail = true; });
  } catch (e) { GLB[k].fail = true; }
  return null;
}
function glbReady(k) {
  if (GLB_SHIPS.has(k)) { const S = STU || null; if (S && S.cache) for (const key of Object.keys(S.cache)) if (key.startsWith(k + "|")) { delete S.cache[key]; ART_PEND.delete(key); for (const o of [S.order, S.orderSide]) if (o) { const i = o.indexOf(key); if (i >= 0) o.splice(i, 1); } }
    clearTimeout(glbReady.t); glbReady.t = setTimeout(() => { if (!battle && !sheet && typeof render === "function") try { render(); } catch (e) {} }, 400); }
  if (GLB_BLDS.has(k) && C3 && C3.keys) C3.keys[k] = null; // the base rebuilds that plot on its next frame
}
/* a hull for the studio: the model turned nose-first along +X, centred, with an engine glow at its tail */
function glbShip(k) {
  if (!GLB_SHIPS.has(k)) return null; const src = glbGet(k); if (!src) return null;
  const g = new TH.Group(), m = src.clone(true), bb = src.userData.bb, c = bb.getCenter(new TH.Vector3()), sz = bb.getSize(new TH.Vector3());
  m.position.set(-c.x, -c.y, -c.z); const pv = new TH.Group(); pv.add(m); pv.rotation.y = Math.PI; g.add(pv);
  const sc = 3 / Math.max(sz.x, .01); g.scale.setScalar(sc); // about the length of the hand-built hulls, so lights and glow sizes still fit
  g.userData.eng = k === "spyProbe" ? [] : [[-sz.x / 2 * .97, 0, 0, Math.max(.05, Math.min(sz.y, sz.z) * .16)]]; g.userData.glb = true;
  g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  return g;
}
/* a building on its plot: the model scaled to the plot, standing on it */
function glbBld(k, b, big, small) {
  if (!GLB_BLDS.has(k) || WEAK) return false; /* slower Android phones keep the light hand-built buildings */ const src = glbGet(k); if (!src) return false;
  const m = src.clone(true), bb = src.userData.bb, c = bb.getCenter(new TH.Vector3()), sz = bb.getSize(new TH.Vector3());
  const foot = big ? 6.2 : small ? 3.4 : 4.6, s = foot / Math.max(sz.x, sz.z, .01); m.scale.setScalar(s); m.position.set(-c.x * s, -bb.min.y * s, -c.z * s);
  b.add(m); return true;
}
function bModel(k, L, busy) {''')

rep('  if (!artBld(k, b, era, C, anim)) switch (k) { // v177 the card-art buildings have their own models',
    '  if (!glbBld(k, b, big, small) && !artBld(k, b, era, C, anim)) switch (k) { // v177 the card-art buildings have their own models (v345: and the Meshy models before them)')

rep('const ship = kind === "s" ? buildShip(k, M) : kind === "a"', 'const ship = kind === "s" ? (glbShip(k) || buildShip(k, M)) : kind === "a"')
rep('if (view === "side" && kind === "s" && k !== "eclipse" && k !== "flagship") { const P = cardPal(k);',
    'if (view === "side" && kind === "s" && k !== "eclipse" && k !== "flagship" && !ship.userData.glb) { const P = cardPal(k);')

rep('S.scene.remove(ship); ship.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.isSprite) o.material.dispose(); });',
    'S.scene.remove(ship); ship.traverse(o => { if (o.geometry && !ship.userData.glb) o.geometry.dispose(); if (o.isSprite) o.material.dispose(); }); /* v345 a model shares its geometry with the loaded copy */')
open(p, "w").write(h); print("ok")
