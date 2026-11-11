# v419: wrecks break in different ways. Every derelict hull at a boss or super boss wreck site (and in the Cube event's wreck field)
# now gets a destruction pattern: broken in half (two halves drifting apart, turning slowly), the bow snapped off (the tip tumbling away
# ahead), the stern blown off (the engines drifting behind), or gutted (whole, holed and burning). Made with clipping planes on the
# hull's own model (no new geometry): the hull and a clone of it are cut at one plane across its long axis, each keeping one side; the cut
# shows the dark interior (double-sided), a glow at the fracture (purple at the Devourer's sites) and fires along it.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("""/* v415 boss wreck sites: real hulls, a destroyed Cube Destroyer and a shattered planetoid */""", """/* v419 a wreck's destruction pattern: split in half, bow snapped off, stern blown off, or gutted (null) */
function wreckBreak(W, g, r, kind, purple, grp, DK) { const pats = ["split", "bow", "stern", "gutted", "split", "bow"]; kind = kind || pats[(r() * pats.length) | 0]; if (kind === "gutted") return null;
  try { W.renderer.localClippingEnabled = true; } catch (e) { return null; }
  g.updateMatrixWorld(true); const bb = new TH.Box3().setFromObject(g), sz = bb.getSize(new TH.Vector3()), ax = sz.x >= sz.y && sz.x >= sz.z ? 0 : sz.z >= sz.y ? 2 : 1, lo = bb.min.getComponent(ax), L = sz.getComponent(ax); if (!(L > 0)) return null;
  const f = kind === "split" ? .42 + r() * .16 : kind === "bow" ? .7 + r() * .1 : .2 + r() * .1, c = lo + L * f, n = new TH.Vector3().setComponent(ax, 1);
  const B = g.clone(true), cm = new Map(); B.traverse(o => { if (o.isMesh && o.material && !Array.isArray(o.material)) { let m = cm.get(o.material); if (!m) { m = o.material.clone(); cm.set(o.material, m); } o.material = m; } });
  const cut = (obj, high) => { const l = new TH.Plane(high ? n.clone() : n.clone().negate(), high ? -c : c), w = l.clone(); obj.traverse(o => { if (o.isMesh && o.material && !Array.isArray(o.material)) { o.material.clippingPlanes = [w]; o.material.side = TH.DoubleSide; o.material.needsUpdate = true; } }); return { obj, l, w }; };
  const P = [cut(g, false), cut(B, true)], ctr = bb.getCenter(new TH.Vector3()).setComponent(ax, c), piv = new TH.Group(), gap = L * (kind === "split" ? .12 + r() * .12 : .18 + r() * .2);
  piv.position.copy(ctr).add(n.clone().multiplyScalar(gap)); B.position.copy(ctr).negate(); piv.add(B); g.add(piv); piv.userData.r0 = new TH.Euler((r() - .5) * .6, (r() - .5) * .6, (r() - .5) * .6); piv.userData.sp = [(r() - .5) * 3e-5, (r() - .5) * 3e-5, (r() - .5) * 3e-5];
  const cross = Math.max(sz.getComponent((ax + 1) % 3), sz.getComponent((ax + 2) % 3)), gt = glowTex(purple ? "200,120,255" : "255,140,60", 1), col = purple ? 0xc77dff : 0xff8a40;
  for (const o of [g, B]) { const s = new TH.Sprite(W.additive(gt, col, .85)); s.position.copy(ctr); s.scale.setScalar(cross * 1.2); o.add(s); } // the fracture glows
  const fr = []; for (let i = 0; i < 3; i++) { const s = fireSprite(W, grp, DK); if (purple) s.material.color.set(0xe8c2ff); fr.push({ s, o: i % 2 ? B : g, p: ctr.clone().add(new TH.Vector3((r() - .5) * cross * .7, (r() - .5) * cross * .7, (r() - .5) * cross * .7).setComponent(ax, c)) }); }
  return { P, piv, fr, sz: cross * .45, kind }; }
function wreckTick(d, t, T, toLocal) { const K = d.brk; if (!K) return; const u = K.piv.userData; K.piv.rotation.set(u.r0.x + T * u.sp[0], u.r0.y + T * u.sp[1], u.r0.z + T * u.sp[2]); d.g.updateMatrixWorld(true);
  for (const p of K.P) p.w.copy(p.l).applyMatrix4(p.obj.matrixWorld); const V = wreckTick.V || (wreckTick.V = new TH.Vector3());
  for (const f of K.fr) fireTick(f.s, t, toLocal(f.o.localToWorld(V.copy(f.p))), Math.min(2.6, K.sz * d.k * .55)); }
/* v415 boss wreck sites: real hulls, a destroyed Cube Destroyer and a shattered planetoid */""")
rep("""    S.ders.push(d); return d; };""", """    if (k !== "worldbreaker") d.brk = wreckBreak(W, g, r, null, purple, grp, DK); /* v419 */ S.ders.push(d); return d; };""")
rep("""S.grp.visible = true; S.grp.position.set(s.x, s.y, s.z);""", """S.grp.visible = true; S.grp.position.set(s.x, s.y, s.z); S.grp.updateMatrixWorld();""")
rep("""d.g.scale.setScalar(d.k);\n      d.g.updateMatrix(); d.fl.forEach((lp, k) =>""", """d.g.scale.setScalar(d.k); wreckTick(d, t, T, v => S.grp.worldToLocal(v));\n      d.g.updateMatrix(); d.fl.forEach((lp, k) =>""")
# the Cube event's wreck field
rep("""m.emissiveIntensity = 1.3; done.set(o.material, m); } o.material = m; }); }""", """m.emissiveIntensity = 1.3; done.set(o.material, m); } o.material = m; }); d.brk = wreckBreak(W, d.g, r, null, false, grp, DK); /* v419 */ }""")
rep("""d.g.updateMatrixWorld(); d.fl.forEach((lp, k) => fireTick(d.fires[k], t, d.g.localToWorld(V2.copy(lp)), d.fs * d.k));""",
    """d.g.updateMatrixWorld(); wreckTick(d, t, T, v => v); d.fl.forEach((lp, k) => fireTick(d.fires[k], t, d.g.localToWorld(V2.copy(lp)), d.fs * d.k));""")
rep("const char = g => { g.userData.noBatch = 1; const done = new Map(); g.traverse(o => { if (!o.isMesh", "const char = g => { g.userData.noBatch = 1; const done = new Map(); g.traverse(o => { if (o.isMesh && o.material && o.material.isMeshBasicMaterial) { o.visible = false; return; } /* v419 a wreck's engines and lights are dead */ if (!o.isMesh")
rep("const done = new Map(); d.g.traverse(o => { if (!o.isMesh", "const done = new Map(); d.g.traverse(o => { if (o.isMesh && o.material && o.material.isMeshBasicMaterial) { o.visible = false; return; } /* v419 */ if (!o.isMesh")
t = t.replace("const GAME_V = 418;", "const GAME_V = 419;")
open(p, "w").write(t); print("ok")
