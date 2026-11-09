# v369: the Crystal Refinery harvests. Its four hanging arms (gold nozzles at the diagonals, found from the model's gold texels) fire short
# red-orange laser bolts at the crystal clusters in the pool (found from its cyan texels): each arm alternates between the cluster beside it and the big
# centre cluster, in bursts, out of step with the other arms. A muzzle flash at the nozzle, and every crystal that is hit flares blue and fades.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep("/* v368 the Metal Extractor's moving conveyors,", r'''/* v369 the Crystal Refinery's harvesting lasers (model units): the four arm nozzles, the crystal clusters, and which clusters each arm works */
const CRY_ARMS = [[.29, -.04, .29], [.29, -.04, -.28], [-.28, -.04, .28], [-.27, -.04, -.28]], CRY_XTL = { e: [.405, -.5, 0], w: [-.42, -.5, 0], n: [0, -.56, -.44], s: [.02, -.6, .456], c: [0, -.5, -.02] };
const CRY_WORK = [["e", "s", "c"], ["e", "n", "c"], ["w", "s", "c"], ["w", "n", "c"]];
function crystalLasers(b, at, s, anim) {
  const neon = c => new TH.MeshBasicMaterial({ color: c, transparent: true, opacity: .95, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false });
  const glow = (c, sc, op) => { const o = new TH.Sprite(new TH.SpriteMaterial({ map: glowTex(c, 1), transparent: true, opacity: op, blending: TH.AdditiveBlending, depthWrite: false })); o.scale.setScalar(sc); o.userData.s0 = sc; return o; };
  const xt = {}; for (const k in CRY_XTL) { const g = glow("30,120,255", s * (k === "c" ? .6 : .48), .2); g.position.copy(at(CRY_XTL[k])); g.position.y += s * .06; g.userData.hit = -1e9; b.add(g); anim.push([g, "xtlGlow", 0]); xt[k] = g; }
  const boltG = new TH.CylinderGeometry(s * .026, s * .026, 1, 6).translate(0, .5, 0), M = neon(0xff5a2a);
  CRY_ARMS.forEach((a, i) => { const A = at(a), mz = glow("255,150,80", s * .16, 0); mz.position.copy(A); b.add(mz);
    for (let j = 0; j < 3; j++) { const k = CRY_WORK[i][j], B = xt[k].position.clone(), d = B.clone().sub(A), L = d.length(), o = new TH.Mesh(boltG, M); o.visible = false;
      o.quaternion.setFromUnitVectors(new TH.Vector3(0, 1, 0), d.clone().normalize()); o.scale.set(1, L * .24, 1); b.add(o);
      const hd = glow("255,120,60", s * .22, 0); b.add(hd); anim.push([o, "laserBolt", i * .27 + j * .13, null]); Object.assign(o.userData, { A, B, d, L, tgt: xt[k], mz, hd, cyc: -1 }); } });
}
/* v368 the Metal Extractor's moving conveyors,''')
rep('    if (k === "metalMine") try { mineBelts(src, b, at, s, anim); } catch (e) {} // v368 moving conveyors',
    '    if (k === "metalMine") try { mineBelts(src, b, at, s, anim); } catch (e) {} // v368 moving conveyors\n    if (k === "crystalMine") try { crystalLasers(b, at, s, anim); } catch (e) {} // v369 harvesting lasers')
rep('''    else if (kind === "beltScroll") {''', '''    else if (kind === "laserBolt") { const u = o.userData, z = T * .0011 + p, cyc = Math.floor(z), q = z - cyc, f = q / .13; // v369 a bolt crosses in ~.13 of its cycle
      if (f < 1) { o.visible = true; o.position.copy(u.A).addScaledVector(u.d, f * .76); u.hd.position.copy(u.A).addScaledVector(u.d, f * .76 + .24); u.hd.material.opacity = 1; u.mz.material.opacity = Math.max(u.mz.material.opacity, .95 * (1 - f)); }
      else { o.visible = false; u.hd.material.opacity = 0; if (u.cyc !== cyc) { u.cyc = cyc; u.tgt.userData.hit = T; } u.mz.material.opacity *= .9; } }
    else if (kind === "xtlGlow") { const u = o.userData, k2 = Math.exp(-(T - u.hit) / 380); o.material.opacity = .2 + .55 * k2; o.scale.setScalar(u.s0 * (1 + .9 * k2)); } // flares blue when hit, then fades
    else if (kind === "beltScroll") {''')
open(p, "w").write(h); print("ok")
