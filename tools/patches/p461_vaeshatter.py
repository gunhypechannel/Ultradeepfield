# v461 Vaelthar's death in the manner of Aexion's (owner: "make all super boss deaths like their own version of Aexion, his was perfect"):
# a last roar, then the wheel overloads in a celestial detonation (gold and violet shockwaves across the map, a blinding flash), every part
# of him (wheel rings, spokes, wings, head, arms, every scale of his body) flung out across the galaxy, tumbling; then each piece turns to
# clear crystal and dissolves while spirits rise from it as it drifts. Timed from the moment he fell, the same for everyone.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
JS = r'''/* v461 break a boss model apart: every visible mesh, and every instance of an instanced mesh, flies out from the body's centre on its own
   path and tumbles, easing out like Aexion's wreck; e = seconds since the detonation; deterministic, so every player sees the same */
function sbShatter(X, b, e) { if (e < 0) return;
  if (!X.shp) { const P = [], r = cwRnd(4242), M = new TH.Matrix4(), inv = new TH.Matrix4(); b.grp.updateMatrixWorld(true); const C0 = new TH.Box3().setFromObject(b.grp).getCenter(new TH.Vector3());
    const dirOf = w => { const d = w.clone().sub(C0); d.y += 4; d.normalize(); d.x += (r() - .5) * .7; d.y += (r() - .25) * .6; d.z += (r() - .5) * .7; return d.normalize(); };
    b.grp.traverse(o => { if (!o.isMesh || !o.visible) return;
      if (o.isInstancedMesh) { inv.copy(o.matrixWorld).invert(); const I = []; for (let i = 0; i < o.count; i++) { o.getMatrixAt(i, M); const p = new TH.Vector3(), q = new TH.Quaternion(), sc = new TH.Vector3(); M.decompose(p, q, sc);
          I.push({ p, q, sc, dl: dirOf(p.clone().applyMatrix4(o.matrixWorld)).transformDirection(inv), d: 55 + r() * 130, ax: new TH.Vector3(r() - .5, r() - .5, r() - .5).normalize(), sp: 2 + r() * 9 }); } P.push({ o, I }); return; }
      if (!o.geometry.boundingSphere) o.geometry.computeBoundingSphere(); const w = o.geometry.boundingSphere.center.clone().applyMatrix4(o.matrixWorld); inv.copy(o.parent.matrixWorld).invert();
      P.push({ o, p0: o.position.clone(), q0: o.quaternion.clone(), dl: dirOf(w).transformDirection(inv), d: 55 + r() * 130, ax: new TH.Vector3(r() - .5, r() - .5, r() - .5).normalize(), sp: 2 + r() * 9 }); });
    b.pieces = P.filter(x => !x.I).map(x => x.o); X.shp = P; X.shT = { p: new TH.Vector3(), q: new TH.Quaternion(), r: new TH.Quaternion(), M: new TH.Matrix4() }; }
  const k = 1 - Math.exp(-e / 2.2), rk = 1 - Math.exp(-e / 2.6), T = X.shT;
  for (const x of X.shp) { if (x.I) { for (let i = 0; i < x.I.length; i++) { const q = x.I[i]; T.p.copy(q.p).addScaledVector(q.dl, q.d * k + e * .22); T.r.setFromAxisAngle(q.ax, q.sp * rk + e * .035); T.q.copy(q.q).multiply(T.r); T.M.compose(T.p, T.q, q.sc); x.o.setMatrixAt(i, T.M); } x.o.instanceMatrix.needsUpdate = true; }
    else { x.o.position.copy(x.p0).addScaledVector(x.dl, x.d * k + e * .22); x.o.quaternion.copy(x.q0); x.o.rotateOnAxis(x.ax, x.sp * rk + e * .035); } } }
'''
rep("function sbBoomTick(X, t) {", JS + "function sbBoomTick(X, t) {")
# the blast in each boss's own colours: gold and violet for Vaelthar
rep("const r1 = mk(.03, 0xcfeeff), r2 = mk(.09, 0x58b8ff), r3 = mk(.025, 0xffffff), sh = new TH.Mesh(new TH.SphereGeometry(1, 40, 24), dvRim(0x7ac8ff));",
    "const vae = X.key === \"vae\", r1 = mk(.03, vae ? 0xffe2a0 : 0xcfeeff), r2 = mk(.09, vae ? 0xa45cff : 0x58b8ff), r3 = mk(.025, 0xffffff), sh = new TH.Mesh(new TH.SphereGeometry(1, 40, 24), dvRim(vae ? 0xc890ff : 0x7ac8ff));")
# preview: roar, detonation, scatter, crystal, spirits; the relic once he is gone; a wider camera to see the pieces fly
rep("  if (!(P.key === \"vae\" && X.fall && sbVaeCrystal(W, X, b, s - X.fall, t))) b.tick(t);",
    "  let vf = -1; if (P.key === \"vae\" && X.fall) { vf = s - X.fall - .8; sbShatter(X, b, vf); sbBlast(W, X, vf, t); sbVaeCrystal(W, X, b, vf - 1.2, t, 1); } if (!(vf >= 0)) b.tick(t);")
rep("if (X.fall && !X.relic && s > X.fall + 6.5) {", "if (X.fall && !X.relic && s > X.fall + 9.5) {")
rep(": s < 93 ? { y: 55, d: 470, th: .26, ph: .4 + (s - 84) * .03 } : { y: 40, d: 900, th: .5, ph: .65 };", ": s < 97 ? { y: 50, d: 760, th: .34, ph: .4 + (s - 84) * .02 } : { y: 40, d: 900, th: .5, ph: .65 };")
# live
rep("  if (!(k === \"vae\" && dead && sbVaeCrystal(W, X, b, df, t))) b.tick(t);",
    "  let vf = -1; if (k === \"vae\" && dead) { vf = df - .8; sbShatter(X, b, vf); sbBlast(W, X, vf, t); sbVaeCrystal(W, X, b, vf - 1.2, t, 1); } if (!(vf >= 0)) b.tick(t);")
# spirits follow scattered instances too
rep("src.push({ w: Vp.clone() }); } }", "src.push({ w: Vp.clone(), im: o, ii: i }); } }")
rep("if (q.sr.o) { const ww = q.sr.o.localToWorld(C.v.copy(q.sr.l)); bx += ww.x - q.sr.w.x; by += ww.y - q.sr.w.y; bz += ww.z - q.sr.w.z; }",
    "if (q.sr.o) { const ww = q.sr.o.localToWorld(C.v.copy(q.sr.l)); bx += ww.x - q.sr.w.x; by += ww.y - q.sr.w.y; bz += ww.z - q.sr.w.z; } else if (moving && q.sr.im) { q.sr.im.getMatrixAt(q.sr.ii, C.M); const ww = C.v.setFromMatrixPosition(C.M).applyMatrix4(q.sr.im.matrixWorld); bx += ww.x - q.sr.w.x; by += ww.y - q.sr.w.y; bz += ww.z - q.sr.w.z; }")
rep("X.cry = { m, S, pts, keep, hide, v: new TH.Vector3() };", "X.cry = { m, S, pts, keep, hide, v: new TH.Vector3(), M: new TH.Matrix4() };")
s = re.sub(r"GAME_V = 460\b", "GAME_V = 461", s)
open(P, 'w').write(s)
