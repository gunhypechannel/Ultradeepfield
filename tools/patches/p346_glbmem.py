# v346: v345's models crashed iPhone Safari ("A problem repeatedly occurred"): a base loads 11 building models, each with a 2048 px
# colour map and two 1024 px maps; decoded and uploaded that is ~30 MB of graphics memory per model, past what iOS allows one page.
#  - Textures are shrunk as each model loads: phones keep a 1024 px colour map and 512 px detail maps (desktop 2048/1024).
#  - Models load one at a time, so two big decodes never overlap.
#  - Ship models free their graphics memory after each portrait (they only draw into the cached sprite).
#  - Crash guard: while a model is loading, a note is kept in localStorage. If the page dies before the note is cleared (a crash
#    while loading), the next start turns models off on that device for 3 days and the hand-built models are used. `?glb=1` forces them on.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)

rep('function glbOn() { return !!(TH && TH.GLTFLoader) && !/[?&]glb=0/.test(location.search); }',
    r'''function glbOn() {
  if (!(TH && TH.GLTFLoader) || /[?&]glb=0/.test(location.search)) return false; if (/[?&]glb=1/.test(location.search)) return true;
  if (glbOn.v !== undefined) return glbOn.v;
  let ok = true; try { const busy = +localStorage.getItem("udfGlbBusy") || 0, off = +localStorage.getItem("udfGlbOff") || 0;
    if (busy && Date.now() - busy < 864e5) { localStorage.setItem("udfGlbOff", Date.now()); localStorage.removeItem("udfGlbBusy"); ok = false; try { crumb("models off: the last session ended while a model was loading"); } catch (e) {} }
    else if (off && Date.now() - off < 3 * 864e5) ok = false; } catch (e) {}
  return (glbOn.v = ok);
}
const GLB_Q = []; let GLB_RUN = 0;
function glbMark(on) { try { if (on) localStorage.setItem("udfGlbBusy", Date.now()); else localStorage.removeItem("udfGlbBusy"); } catch (e) {} }
/* shrink a loaded texture to px (keeps the decoded copy small and the upload small) */
function glbShrink(tex, px) {
  const im = tex && tex.image; if (!im) return; const w = im.width || 0, h = im.height || 0; if (w <= px && h <= px) return;
  const s = px / Math.max(w, h), c = document.createElement("canvas"); c.width = Math.round(w * s); c.height = Math.round(h * s);
  c.getContext("2d").drawImage(im, 0, 0, c.width, c.height); if (im.close) try { im.close(); } catch (e) {} tex.image = c; tex.needsUpdate = true;
}
function glbNext() {
  if (GLB_RUN || !GLB_Q.length) { if (!GLB_RUN && !GLB_Q.length) { clearTimeout(glbNext.t); glbNext.t = setTimeout(() => { if (!GLB_RUN && !GLB_Q.length) glbMark(false); }, 45000); } return; }
  const k = GLB_Q.shift(); GLB_RUN = 1; glbMark(true);
  const done = () => { GLB_RUN = 0; setTimeout(glbNext, 120); };
  try {
    new TH.GLTFLoader().load("models/" + k + ".glb?v=" + GAME_V, g => {
      const s = g.scene, big = MOBILE ? 1024 : 2048, aux = MOBILE ? 512 : 1024;
      s.traverse(o => { if (o.isMesh) { const m = o.material; if (m && m.isMeshStandardMaterial) { m.envMapIntensity = .9; glbShrink(m.map, big); for (const t of new Set([m.normalMap, m.roughnessMap, m.metalnessMap])) glbShrink(t, aux); if (m.map) m.map.anisotropy = 4; } } });
      const bb = new TH.Box3().setFromObject(s); s.userData.bb = bb; GLB[k].scene = s; done(); glbReady(k);
    }, undefined, () => { GLB[k].fail = true; done(); });
  } catch (e) { GLB[k].fail = true; done(); }
}''')

rep('''  GLB[k] = {};
  try {
    new TH.GLTFLoader().load("models/" + k + ".glb?v=" + GAME_V, g => {
      const s = g.scene; s.traverse(o => { if (o.isMesh) { const m = o.material; if (m && m.isMeshStandardMaterial) { m.envMapIntensity = .9; if (m.map) m.map.anisotropy = 4; } } });
      const bb = new TH.Box3().setFromObject(s); s.userData.bb = bb; GLB[k].scene = s; glbReady(k);
    }, undefined, () => { GLB[k].fail = true; });
  } catch (e) { GLB[k].fail = true; }
  return null;''', '''  GLB[k] = {}; GLB_Q.push(k); glbNext();
  return null;''')

# a ship model only draws into its cached portrait: free its textures' graphics memory afterwards (three re-uploads them if it is drawn again)
rep('S.scene.remove(ship); ship.traverse(o => { if (o.geometry && !ship.userData.glb) o.geometry.dispose(); if (o.isSprite) o.material.dispose(); });',
    'S.scene.remove(ship); ship.traverse(o => { if (o.geometry && !ship.userData.glb) o.geometry.dispose(); if (o.isSprite) o.material.dispose(); if (ship.userData.glb && o.isMesh && o.material) for (const t of [o.material.map, o.material.normalMap, o.material.roughnessMap, o.material.metalnessMap]) if (t) t.dispose(); });')

open(p, "w").write(h); print("ok")
