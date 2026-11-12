# v465 Aexion, the spectacle (owner: you can't tell his thrusters fire, he only swings back and forth with no depth or sense of his grand
# scale; the transformation should be slower with many more small shifting parts; his debut should be spectacular).
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
# ---- the model: thrust plumes, and dozens of small armour plates that shift, flip and lock into place through the transformation ----
rep("const thr = [-1, 1].map(sx => {", """const plume = [-1, 1].map(sx => { const g = new TH.Group(); g.position.set(sx * 6.8, 5.4, -1.2); g.rotation.z = -sx * Math.PI / 2; chest.add(g);
      const mk = (r0, r1, col, op) => { const geo = new TH.CylinderGeometry(r1, r0, 1, 16, 1, true); geo.translate(0, .5, 0); const m = new TH.Mesh(geo, new TH.MeshBasicMaterial({ color: col, transparent: true, opacity: 0, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false, side: TH.DoubleSide })); m.userData.dyn = 1; m.userData.o = op; g.add(m); return m; };
      const sp = sprite(5, "rgba(170,220,255,1)", "aex_fl"); sp.material.opacity = 0; sp.position.copy(g.position); chest.add(sp); return { sx, g, sp, L: [mk(1.9, .3, 0x2f7cff, .45), mk(1.1, .12, 0x8fd0ff, .7), mk(.55, .04, 0xffffff, .95)] }; });
    const NPL = LO ? 44 : 96, plG = new TH.BoxGeometry(1, 1, 1), plM = [new TH.InstancedMesh(plG, MA, NPL), new TH.InstancedMesh(plG, MD, NPL)], aPl = []; for (const m of plM) { m.userData.dyn = 1; m.frustumCulled = false; m.count = 0; body.add(m); }
    { const bx = new TH.Box3(), tb = new TH.Box3(), cand = joints.filter(j => j.g.children.some(c => c.isMesh)), ax = ["x", "y", "z"];
      for (let i = 0; i < NPL * 2 && aPl.length < NPL * 2; i++) { const j = cand[(rnd() * cand.length) | 0]; if (!j) break; bx.makeEmpty(); { const ms = j.g.children.filter(c => c.isMesh && c.geometry && c.geometry.type === \"ExtrudeGeometry\"); const c = ms[(rnd() * ms.length) | 0]; if (c) { c.updateMatrix(); c.geometry.computeBoundingBox(); bx.copy(c.geometry.boundingBox).applyMatrix4(c.matrix); } } if (bx.isEmpty()) continue;
        const a = (rnd() * 3) | 0, sg = rnd() < .5 ? -1 : 1, p = new TH.Vector3(bx.min.x + rnd() * (bx.max.x - bx.min.x), bx.min.y + rnd() * (bx.max.y - bx.min.y), bx.min.z + rnd() * (bx.max.z - bx.min.z)); p[ax[a]] = sg > 0 ? bx.max[ax[a]] : bx.min[ax[a]];
        const n = new TH.Vector3(); n[ax[a]] = sg; const sz = new TH.Vector3(.5 + rnd() * 1.3, .5 + rnd() * 1.3, .5 + rnd() * 1.3); sz[ax[a]] = .16 + rnd() * .12; const mp = p.clone().addScaledVector(n, sz[ax[a]] * .5 + .02);
        const k = aPl.length % 2, idx = Math.floor(aPl.length / 2); if (idx >= NPL) break; const a0 = .05 + rnd() * .8;
        aPl.push({ j, m: plM[k], i: idx, mp, sp: mp.clone().addScaledVector(n, -1.4 - rnd() * 1.2).add(new TH.Vector3((rnd() - .5) * 1.4, (rnd() - .5) * 1.4, (rnd() - .5) * 1.4)), n, sz, sq: E((rnd() - .5) * 3, (rnd() - .5) * 3, (rnd() - .5) * 3), a0, a1: a0 + .04 + rnd() * .1, lift: .8 + rnd() * 1.6 }); } plM.forEach(m => { m.count = NPL; }); }
    const plT = { inv: new TH.Matrix4(), M: new TH.Matrix4(), L: new TH.Matrix4(), q: new TH.Quaternion(), q0: new TH.Quaternion(), p: new TH.Vector3() };
    const thr = [-1, 1].map(sx => {""")
rep("      hit(Math.max(bell(fx, 0, .05, .4, 1) + od * .15, xh), t); if (xb) bt(t, xb);",
"""      { body.updateMatrixWorld(true); plT.inv.copy(body.matrixWorld).invert(); for (const P of aPl) { const k = ss(P.a0, P.a1, u), w = Math.sin(k * Math.PI); plT.p.lerpVectors(P.sp, P.mp, k).addScaledVector(P.n, w * P.lift); plT.q.slerpQuaternions(P.sq, plT.q0, k);
          plT.L.compose(plT.p, plT.q, P.sz); plT.M.multiplyMatrices(plT.inv, P.j.g.matrixWorld).multiply(plT.L); P.m.setMatrixAt(P.i, plT.M); } plM.forEach(m => { m.instanceMatrix.needsUpdate = true; }); }
      hit(Math.max(bell(fx, 0, .05, .4, 1) + od * .15, xh), t); if (xb) bt(t, xb);""")
# the dodge: twice as far, with the thrusters on the far side firing long blue plumes and braking bursts on the near side
rep("if (fdg >= 0 && st0 > 0) { const k = bell(fdg, 0, .12, .5, 1), side = out.dside || 1, kick = bell(fdg, 0, .03, .18, .45); body.position.x += side * 12 * k;",
    "if (fdg >= 0 && st0 > 0) { const k = bell(fdg, 0, .1, .5, 1), side = out.dside || 1, kick = bell(fdg, 0, .03, .2, .45), brake = bell(fdg, .42, .55, .7, .9); body.position.x += side * 22 * k; plume.forEach(P => { const f = P.sx === -side ? Math.max(kick * 1.2, k * .3) : brake * .8; P.L.forEach(m => { m.material.opacity = m.userData.o * Math.min(1, f); }); P.g.scale.set(1 + f * .4, (4 + 20 * f) * (.85 + rnd() * .3), 1 + f * .4); P.sp.material.opacity = Math.min(1, f); P.sp.scale.setScalar(5 + f * 12); });")
rep("} else thr.forEach(s => { s.material.opacity = 0; });", "} else { thr.forEach(s => { s.material.opacity = 0; }); plume.forEach(P => { P.L.forEach(m => { m.material.opacity = 0; }); P.sp.material.opacity = 0; }); }")
# ---- the replay: a warp-in debut, a slower transformation, and a camera that shows his scale ----
WARP = r'''/* v465 Aexion drops out of warp: a rift tears open, he bursts through it at full size and brakes in over the next five seconds, a streak of
   blue light behind him; a = seconds since the replay or the hunt began */
function aexWarp(X, b, a, t) { const R = X.V2.copy(X.B).addScaledVector(X.F, -760); X.rift.position.copy(R); X.rift.lookAt(X.B);
  const aa = clamp((a - 1.2) / 5, 0, 1), pull = Math.pow(1 - aa, 3); b.grp.position.addScaledVector(X.F, -760 * pull); b.grp.position.y += 40 * pull;
  if (!X.aw) { const g = new TH.Group(), L = []; for (const [r, c, o] of [[34, 0x2f7cff, .35], [16, 0x9ad8ff, .6], [6, 0xffffff, .9]]) { const geo = new TH.CylinderGeometry(r * .2, r, 1, 18, 1, true); geo.translate(0, .5, 0); geo.rotateX(Math.PI / 2); const m = new TH.Mesh(geo, new TH.MeshBasicMaterial({ color: c, transparent: true, opacity: 0, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false, side: TH.DoubleSide })); m.userData.o = o; m.frustumCulled = false; g.add(m); L.push(m); } X.grp.add(g); X.aw = { g, L, boom: 0 }; }
  const W0 = X.aw, on = a > 1.2 && aa < 1; W0.g.visible = on; if (a > 1.25 && !W0.boom) { W0.boom = 1; sbBoom(X, R.clone(), t, 520); sbBoom(X, R.clone().addScaledVector(X.F, 60), t + 120, 380); }
  if (on) { const d = b.grp.position.distanceTo(R) + 1, sp = Math.pow(1 - aa, 2); W0.g.position.copy(b.grp.position); W0.g.lookAt(R); W0.g.scale.set(1 + sp, 1 + sp, d); W0.L.forEach(m => { m.material.opacity = m.userData.o * Math.min(1, sp * 1.6) * (.85 + Math.random() * .15); }); }
  if (a < 8) X.flash.position.copy(R); else X.flash.position.copy(X.B); return aa; }
'''
rep("function sbAex(X, W, b, s, t, dt, say, yaw, side) { const sc = SBX.aex.sc;",
    WARP + "function sbAex(X, W, b, s, t, dt, say, yaw, side) { const sc = SBX.aex.sc, sR = s; s = s < 24 ? s : s < 60 ? 24 + (s - 24) * 24 / 36 : s - 12; /* the transformation takes 36 s in the replay; everything after follows it */")
rep("const creep = clamp(s / 22, 0, 1); b.grp.position.copy(X.B).addScaledVector(X.F, creep * 40);",
    "const creep = clamp(s / 22, 0, 1); b.grp.position.copy(X.B).addScaledVector(X.F, creep * 40); const aa = aexWarp(X, b, sR, t); b.grp.scale.setScalar(sR > 1.2 ? sc : .001);")
rep('aex: { n: "Aexion", t: "The Warform Sovereign", m3: "aexion", p: [360, 40, -250], sc: 4.3, dur: 98,', 'aex: { n: "Aexion", t: "The Warform Sovereign", m3: "aexion", p: [360, 40, -250], sc: 4.3, dur: 110,')
OLDK = "const K = s < 8 ? { y: 30, d: 620, th: .45, ph: .6 } : s < T0 ?"
NEWK = """const bp = b.grp.position, tb = { tx: bp.x, tz: bp.z }, P2 = Math.PI / 2, R0 = X.rift.position;
  const K = sR < 1.2 ? { tx: R0.x, tz: R0.z, ty: X.B.y + 40, d: 640, th: .06, ph: P2 + .55 } : sR < 7.5 ? { tx: bp.x, tz: bp.z, ty: bp.y + 34, d: 230 + aa * 170, th: -.1 + aa * .22, ph: P2 - .25 + aa * .3 } : s < 8 ? { y: 30, d: 520, th: .3, ph: .6 }
    : s >= 48 && s < 84 ? Object.assign(tb, s < 49.5 ? { y: 34, d: 240, th: -.12, ph: .35 } : s < 53 ? { y: 30, d: 270, th: -.06, ph: .9 + (s - 49.5) * .06 } : s < 58 ? { y: 36, d: 215, th: -.1, ph: .15 + (s - 53) * .03 }
      : s < 62 ? { y: 62, d: 340, th: .3, ph: 2.6 } : s < 70 ? { y: 32, d: 205, th: .02, ph: .5 + (s - 62) * .04 } : s < 79.5 ? { y: 34, d: 265, th: -.1, ph: 1.0 + (s - 70) * .06 } : { y: 30, d: 600, th: .12, ph: 1.5 }) : s < T0 ?"""
rep(OLDK, NEWK)
# live: the same warp-in when the hunt begins
rep("else { const xf = aexXf(st); {", "else { if (e < 9) { b.grp.position.copy(X.B); aexWarp(X, b, e, t); if (e > 1.2) scl = D.sc * (back ? 1.08 : 1); } const xf = aexXf(st); {")
s = re.sub(r"GAME_V = 464\b", "GAME_V = 465", s)
open(P, 'w').write(s)
