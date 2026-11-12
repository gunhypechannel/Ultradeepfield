# v472 Remaster step 2, Cube Devastation (live 2026-11-25): a cube that locks into the Omega Cube punches into place with a mechanical jolt;
# every locked cube is joined to the core by a green energy channel, pulses running down them in the order they locked, all of them flashing
# together as it activates; the activation is a galaxy-wide blast (flash, green shockwave rings and shell, the camera shaking as they pass);
# and when the Omega Cube falls its core overloads (the core swelling and flickering, beams bursting out of all six faces) and detonates
# in a second green blast, three minutes before it comes apart.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
# the lock jolt
rep("D3.updateMatrix(); X.inst.setMatrixAt(n, D3.matrix); c.ni = n; n++;",
    "if (o.st === \"locked\") { const la = (e - (o.lkT || c.lk)) / (1500 * (D.rate ? D.rate * 1000 / 1000 : 1)); if (la >= 0 && la < 1) D3.scale.multiplyScalar(1 + .09 * Math.sin(la * Math.PI) * (1 - la)); } D3.updateMatrix(); X.inst.setMatrixAt(n, D3.matrix); c.ni = n; n++;")
# channels, the activation blast, the overload
rep("  /* the Super Cube itself (W.nexus) is moved by the map's own Cube code (dvCore there) */",
"""  /* v472 the energy channels: every locked cube joined to the core, pulses running in the order they locked, all flashing at activation */
  if (!X.ch) { const g = new TH.BufferGeometry(); g.setAttribute("position", new TH.BufferAttribute(new Float32Array(104 * 6), 3)); g.setAttribute("color", new TH.BufferAttribute(new Float32Array(104 * 6), 3)); X.ch = new TH.LineSegments(g, new TH.LineBasicMaterial({ vertexColors: true, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false })); X.ch.frustumCulled = false; X.grp.add(X.ch); }
  { const cp2 = X.ch.geometry.attributes.position.array, cc2 = X.ch.geometry.attributes.color.array; let nc = 0; const sync = e >= DV.act && e < DV.erupt ? 0 : 1, fl = e >= DV.erupt ? 1.5 * eru : 0;
    if (!lite || nc < 40) for (const c of P.L) { if (!X.locked.has(c.i)) continue; const q = dvCube(c, e, D, X.tq), j = nc * 6, pul = Math.pow(.5 + .5 * Math.sin(t * .004 - (c.lk || 0) / 9000), 4) * .9 * sync + fl, rim = .25 * sync + fl;
      cp2[j] = q.x; cp2[j + 1] = q.y; cp2[j + 2] = q.z; cp2[j + 3] = 0; cp2[j + 4] = DV_Y; cp2[j + 5] = 0; cc2[j] = .25 * rim; cc2[j + 1] = rim; cc2[j + 2] = .4 * rim; cc2[j + 3] = .35 * pul; cc2[j + 4] = pul; cc2[j + 5] = .5 * pul; if (++nc >= 104) break; }
    X.ch.geometry.setDrawRange(0, nc * 2); X.ch.geometry.attributes.position.needsUpdate = X.ch.geometry.attributes.color.needsUpdate = true; }
  /* v472 the activation: a blast across the whole galaxy; and the overload when it falls */
  const stand = k => X[k] || (X[k] = (() => { const Y = { key: "omg", grp: X.grp, B: new TH.Vector3(0, DV_Y, 0), V: new TH.Vector3(), V2: new TH.Vector3(), ships: [], b: { pieces: [] }, booms: [], fleetBooms: 1, F: new TH.Vector3(0, 0, 1) }; Y.flash = new TH.Sprite(W.additive(W.glow.dv, new TH.Color("#b8ffc8"), 0)); Y.flash.material.depthTest = false; Y.flash.position.copy(Y.B); X.grp.add(Y.flash); return Y; })());
  { const se = D.sim ? (X.eruT0 = e >= DV.erupt ? (X.eruT0 || t) : 0, X.eruT0 ? (t - X.eruT0) / 1000 : -1) : (e - DV.erupt) / 1000; if (se > -1 && se < 15) sbBlast(W, stand("aB"), se, t); else if (X.aB) sbBlast(W, X.aB, -5, t); }
  { const killed = D.sim || omState(D.s0).dead > D.s0, de0 = DV.ret - 3 * DV_M, de = !killed ? -1 : D.sim ? (X.dieT0 = e >= de0 ? (X.dieT0 || t) : 0, X.dieT0 ? (t - X.dieT0) / 1000 : -1) : (e - de0) / 1000;
    if (de >= 0 && de < 4.2) { const k = de / 4.2; X.core.visible = true; X.core.position.set(0, DV_Y, 0); X.core.scale.setScalar(160 + 520 * k + 40 * Math.sin(t * .05)); X.core.material.opacity = Math.min(1, .5 + k * .6) * (Math.random() < .2 ? .5 : 1);
      if (!X.ob) { const g = new TH.Group(); for (const [x, y, z] of [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]) for (const [r, c, o] of [[16, 0x40ff80, .45], [6, 0xe0ffe8, .9]]) { const geo = new TH.CylinderGeometry(r * .5, r, 1, 16, 1, true); geo.translate(0, .5, 0); const m = new TH.Mesh(geo, new TH.MeshBasicMaterial({ color: c, transparent: true, opacity: 0, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false, side: TH.DoubleSide })); m.userData.o = o; m.quaternion.setFromUnitVectors(new TH.Vector3(0, 1, 0), new TH.Vector3(x, y, z)); m.frustumCulled = false; g.add(m); } g.position.set(0, DV_Y, 0); X.grp.add(g); X.ob = g; }
      X.ob.visible = true; X.ob.children.forEach(m => { m.material.opacity = m.userData.o * Math.min(1, k * 1.6) * (.8 + Math.random() * .2); m.scale.set(1 + k, 120 + 900 * k, 1 + k); }); }
    else if (X.ob) X.ob.visible = false;
    if (de >= 4.2 && de < 19) sbBlast(W, stand("dB"), de - 4.2, t); else if (X.dB) sbBlast(W, X.dB, -5, t); }
  /* the Super Cube itself (W.nexus) is moved by the map's own Cube code (dvCore there) */""")
# the blast in the Collective's green
rep("const vae = X.key === \"vae\", px = X.key === \"epx\", wc = X.key !== \"epx\" && typeof WB !== \"undefined\" && WB[X.key] ? new TH.Color(WB[X.key].col).getHex() : null,",
    "const vae = X.key === \"vae\", px = X.key === \"epx\", wc = X.key === \"omg\" ? 0x40ff80 : X.key !== \"epx\" && typeof WB !== \"undefined\" && WB[X.key] ? new TH.Color(WB[X.key].col).getHex() : null,")
s = re.sub(r"GAME_V = 471\b", "GAME_V = 472", s)
open(P, 'w').write(s)
