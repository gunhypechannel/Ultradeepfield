# v371: Flagship Dock remaster, in code (the user chose this over a Meshy model). The block warship in the cradles is replaced by the
# player's own flagship (the same 3D build as its portrait, in the faction's plating), shown as a cyan wireframe hologram until it is
# commissioned; the old blocks stay only as a fallback. Added: window grids on both gantry towers,
# floodlight beams sweeping the hull, maintenance drones circling it with welding flashes, and pulsing energy collars on the docking arms.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep('''      const hg = new TH.Group(); hg.position.set(0, .72, hz); b.add(hg); const hm = built ? C.dark : C.holo, hp = built ? C.steel : C.holo, put = m => (hg.add(m), m);''',
'''      let shipM = null; try { const fac = facOf(), F = FACTIONS[fac] || FACTIONS.terran, M0 = shipMats("#" + new TH.Color(F.glow).getHexString() + "@" + fac), M = Object.assign(Object.create(M0), flagMats(M0.fac, 2.9)); Object.defineProperty(M, "fac", { value: M0.fac }); // v371 your own flagship in the cradles, in your faction's plating
        shipM = buildShip("flagship", M); shipM.traverse(o => { if (o.userData && o.userData.fx) o.visible = false; }); } catch (e) { shipM = null; }
      if (shipM) { const bb0 = new TH.Box3().setFromObject(shipM), k0 = 3.1 / Math.max(.01, bb0.max.x - bb0.min.x); shipM.scale.multiplyScalar(k0); const bb1 = new TH.Box3().setFromObject(shipM);
        shipM.position.set(-.05, .42 - bb1.min.y, hz); if (!built) shipM.traverse(o => { if (o.isMesh) { o.material = HOLO_WIRE(); o.castShadow = false; } }); b.add(shipM);
        if (built) { const g1 = new TH.Sprite(new TH.SpriteMaterial({ map: glowTex("120,200,255", 1), transparent: true, opacity: .8, blending: TH.AdditiveBlending, depthWrite: false })); g1.position.set(-1.65, .42 + (bb1.max.y - bb1.min.y) * .45, hz); g1.scale.setScalar(.7); g1.userData.s0 = .7; b.add(g1); anim.push([g1, "glowP", 0]); } }
      const hg = new TH.Group(); hg.position.set(0, .72, hz); if (!shipM) b.add(hg); const hm = built ? C.dark : C.holo, hp = built ? C.steel : C.holo, put = m => (hg.add(m), m);''')
rep('''      if (e >= 4) { const s2 = dot(-.9, 1.0, -.36, A.white0, 2.2); anim.push([s2, "blink", 2.4]); for (let x = -1.6; x <= 1.6; x += .8) dot(x, .1, 1.32, C.cyan, 1.1); }
      break; }
    case "repairYard":''', '''      if (e >= 4) { const s2 = dot(-.9, 1.0, -.36, A.white0, 2.2); anim.push([s2, "blink", 2.4]); for (let x = -1.6; x <= 1.6; x += .8) dot(x, .1, 1.32, C.cyan, 1.1); }
      { // v371 the working dock: window grids on the towers, floodlights sweeping the hull, drones welding round it, energy collars on the arms
        const wm = new TH.MeshBasicMaterial({ color: 0xffd9a0, transparent: true, opacity: .9, toneMapped: false });
        for (const s of [-1, 1]) for (let y = .35; y < H - .2; y += .26) for (let i = 0; i < 3; i++) if (hash("dk" + s + y.toFixed(2) + i) % 5) { const w = new TH.Mesh(new TH.PlaneGeometry(.09, .1), wm); w.position.set(s * X - .13 + i * .13, y, -.195); b.add(w); const w2 = w.clone(); w2.position.z = -.705; w2.rotation.y = Math.PI; b.add(w2); }
        const beamM = new TH.MeshBasicMaterial({ color: 0xffe2b0, transparent: true, opacity: .13, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false });
        for (const s of [-1, 1]) { const piv = new TH.Group(); piv.position.set(s * X, H - .05, .05); const cone = new TH.Mesh(new TH.ConeGeometry(.42, 1.9, 18, 1, true).translate(0, -.95, 0), beamM); piv.add(cone); piv.rotation.z = s * .55; piv.userData.z0 = s * .55; b.add(piv); anim.push([piv, "flood", s]);
          const hd = new TH.Sprite(new TH.SpriteMaterial({ map: glowTex("255,226,170", 1), transparent: true, opacity: .9, blending: TH.AdditiveBlending, depthWrite: false })); hd.position.copy(piv.position); hd.scale.setScalar(.45); b.add(hd); }
        if (built || shipM) for (let i = 0; i < (MOBILE ? 2 : 3); i++) { const d = new TH.Group(); d.add(new TH.Mesh(new TH.BoxGeometry(.12, .05, .12), C.steel)); const wl = new TH.Sprite(new TH.SpriteMaterial({ map: glowTex("200,235,255", 1), transparent: true, opacity: 1, blending: TH.AdditiveBlending, depthWrite: false })); wl.position.y = -.08; wl.scale.setScalar(.22); wl.userData.s0 = .22; d.add(wl); anim.push([wl, "flick", i * 1.9]);
          b.add(d); anim.push([d, "orbitF", i * 2.1]); Object.assign(d.userData, { r: 1.25 + i * .18, y0: 1.05 + i * .12, w: (i % 2 ? -1 : 1) * (.45 + i * .1), tilt: .12 }); }
        for (const s of [-1, 1]) for (const f of [.35, .7]) { const t = new TH.Mesh(new TH.TorusGeometry(.075, .014, 6, 20), new TH.MeshBasicMaterial({ color: 0x66ddff, transparent: true, opacity: .8, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false }));
          const a = [s * (X - .25), 1.6, -.2], c2 = [s * .95, .98, -.1]; t.position.set(a[0] + (c2[0] - a[0]) * f, a[1] + (c2[1] - a[1]) * f, a[2] + (c2[2] - a[2]) * f); t.quaternion.setFromUnitVectors(new TH.Vector3(0, 0, 1), new TH.Vector3(c2[0] - a[0], c2[1] - a[1], c2[2] - a[2]).normalize()); t.userData.op = .8; b.add(t); anim.push([t, "pulseO", f * 4 + s]); } }
      break; }
    case "repairYard":''')
rep('''    else if (kind === "laserBolt") {''', '''    else if (kind === "flood") { o.rotation.z = o.userData.z0 + Math.sin(T * .0007 + p * 1.3) * .28; o.rotation.x = Math.sin(T * .0005 + p) * .2; } // v371 floodlights sweeping the hull
    else if (kind === "laserBolt") {''')
open(p, "w").write(h); print("ok")
