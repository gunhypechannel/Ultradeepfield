# v352: more Meshy models. The Cube Destroyer gets a spherical model (an original design: a ball of interlocking cube-shaped armour blocks
# with a red core; not its card's look). Seven more buildings: Repair Yard, Nanite Assembly, Orbital Fortress, Geo-Former, Coalition
# Depot, Lunar Outpost, Phalanx Array. (Not modelled: Flagship Dock and Warp Gate, whose hand-built models carry their animations; the
# Missile Silo model only simplifies to 84k triangles.)
# Memory, now that a base can show 19 models: iOS Safari caps all canvas memory of a page (~384 MB) and the shrunk textures sat in canvases.
# A shrunk texture is now handed over as an ImageBitmap and its canvas freed. Phones give 1536 px colour maps to the first 8 building
# models loaded and 1024 px to the rest.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep('"guardian", "tender", "spyProbe"]); // v348: not the Cube Destroyer, which is a sphere (its hand-built model)', '"guardian", "tender", "spyProbe", "worldbreaker"]); // v352: the Cube Destroyer\'s model is a sphere')
rep("const GLB_YAW = { worldbreaker: -Math.PI / 2 };", "const GLB_YAW = {};")
rep('"robotics", "lab", "radar", "fusion"]);', '"robotics", "lab", "radar", "fusion", "repairYard", "nanite", "fortress", "terraformer", "allyDepot", "lunarBase", "phalanx"]);\nlet GLB_BN = 0; // building models loaded so far (phones: the first 8 keep 1536 px colour maps)')
rep('''  const x2 = c.getContext("2d"); x2.imageSmoothingEnabled = true; x2.imageSmoothingQuality = "high"; x2.drawImage(im, 0, 0, c.width, c.height); if (im.close) try { im.close(); } catch (e) {} tex.image = c; tex.needsUpdate = true;
}''', '''  const x2 = c.getContext("2d"); x2.imageSmoothingEnabled = true; x2.imageSmoothingQuality = "high"; x2.drawImage(im, 0, 0, c.width, c.height); if (im.close) try { im.close(); } catch (e) {} tex.image = c; tex.needsUpdate = true;
  /* v352 hand the texture over as an ImageBitmap and free the canvas: iOS Safari caps the canvas memory of a whole page */
  if (window.createImageBitmap) return createImageBitmap(c).then(bm => { tex.image = bm; tex.needsUpdate = true; c.width = c.height = 0; }).catch(() => {});
}''')
rep('''      const s = g.scene, big = MOBILE ? (GLB_BLDS.has(k) ? 1536 : 1024) : 2048, aux = MOBILE ? 512 : 1024, an = texAniso();
      s.traverse(o => { if (o.isMesh) { const m = o.material; if (m && m.isMeshStandardMaterial) { m.envMapIntensity = .9; glbShrink(m.map, big); for (const t of new Set([m.normalMap, m.roughnessMap, m.metalnessMap])) glbShrink(t, aux); for (const t of [m.map, m.normalMap]) if (t) t.anisotropy = an; } } });
      const bb = new TH.Box3().setFromObject(s); s.userData.bb = bb; GLB[k].scene = s; done(); glbReady(k);''',
'''      const s = g.scene, big = MOBILE ? (GLB_BLDS.has(k) && GLB_BN++ < 8 ? 1536 : 1024) : 2048, aux = MOBILE ? 512 : 1024, an = texAniso(), ps = [];
      s.traverse(o => { if (o.isMesh) { const m = o.material; if (m && m.isMeshStandardMaterial) { m.envMapIntensity = .9; ps.push(glbShrink(m.map, big)); for (const t of new Set([m.normalMap, m.roughnessMap, m.metalnessMap])) ps.push(glbShrink(t, aux)); for (const t of [m.map, m.normalMap]) if (t) t.anisotropy = an; } } });
      Promise.all(ps).then(() => { const bb = new TH.Box3().setFromObject(s); s.userData.bb = bb; GLB[k].scene = s; done(); glbReady(k); });''')
# tall, narrow models (a dish on a tower) were scaled by their footprint only and stood far above the base: cap their height too
rep("const foot = big ? 6.2 : small ? 3.4 : 4.6, s = foot / Math.max(sz.x, sz.z, .01);", "const foot = big ? 6.2 : small ? 3.4 : 4.6, hmax = big ? 6 : small ? 3.8 : 5.5, s = Math.min(foot / Math.max(sz.x, sz.z, .01), hmax / Math.max(sz.y, .01));")
open(p, "w").write(h); print("ok")
