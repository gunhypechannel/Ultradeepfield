# v454 Aexion's death: reactor overload, a supermassive detonation with map-wide shockwaves, and his real parts scattered across the map (p454_aexboom.js)
import re, os
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
js = open(os.path.join(os.path.dirname(__file__), 'p454_aexboom.js')).read()
rep("/* v408 tapping the Super Cube */", js + "/* v408 tapping the Super Cube */")
# the model: boomE (seconds since detonation; -2..0 the overload) detaches every jointed part into the body and flings it out
rep("    const tick = t => { const ft = f(\"transform\", t); if (ft >= 0) out.form = ft;",
"""    let BM = null; const boomInit = () => { BM = []; body.updateMatrixWorld(true); const parts = joints.map(j => j.g), dep = o => { let d = 0; while (o && o !== body) { d++; o = o.parent; } return d; }, r = k => { const x = Math.sin(k * 127.1 + 3.7) * 43758.5453; return x - Math.floor(x); };
      parts.sort((a, b) => dep(b) - dep(a)); parts.forEach((g, i) => { body.attach(g); const p0 = g.position.clone(), q0 = g.quaternion.clone(), dir = p0.clone().sub(V(0, 1, 0)); if (dir.lengthSq() < .5) dir.set(r(i) - .5, .4, r(i + 9) - .5); dir.normalize();
        dir.x += (r(i * 3 + 1) - .5) * .9; dir.y += (r(i * 5 + 2) - .35) * .7; dir.z += (r(i * 7 + 3) - .5) * .9; dir.normalize(); BM.push({ g, p0, q0, dir, d: 45 + r(i * 11 + 4) * 190, ax: V(r(i * 13) - .5, r(i * 17) - .5, r(i * 19) - .5).normalize(), sp: 2 + r(i * 23) * 9 }); });
      out.pieces = parts; }; /* v454 */
    const tick = t => { const ft = f("transform", t); if (ft >= 0) out.form = ft;""")
rep("      hit(bell(fx, 0, .05, .4, 1) + od * .15, t); };\n    out.tick = tick; tick(0); bake(body); return out; }",
"""      hit(bell(fx, 0, .05, .4, 1) + od * .15, t);
      const be = out.boomE; if (be != null && be > -2.2) { if (be < 0) { hit(.25 + (be + 2) * .2, t); seams.forEach(m => m.material.opacity = .8 + .2 * Math.sin(t * .08)); coreS.material.opacity = 1; coreS.scale.setScalar(8 + (be + 2) * 6 + Math.sin(t * .09) * 2); }
        else { if (!BM) boomInit(); for (const P of BM) { const k = 1 - Math.exp(-be / 2.2); P.g.position.copy(P.p0).addScaledVector(P.dir, P.d * k + be * .22); P.g.quaternion.copy(P.q0); P.g.rotateOnAxis(P.ax, P.sp * (1 - Math.exp(-be / 2.6)) + be * .035); }
          const hot = Math.max(0, 1 - be / 7); seams.forEach(m => m.material.opacity = .15 + hot * .7); coreS.material.opacity = Math.max(0, 1 - be / 1.2); coreS.scale.setScalar(10 + be * 40); blade.visible = false; bladeS.material.opacity = 0; hexM.uniforms.uO.value = 0;
          eyes.forEach(e => e.material.opacity = 0); legs.forEach(L => L.fl.forEach(s => s.material.opacity = hot * .4)); } } };
    out.tick = tick; tick(0); bake(body); return out; }""")
# the preview: the fall becomes the detonation, seen wide; survivors are thrown outward by the wave
rep('if (X.fall) { const f = clamp((s - X.fall) / 5, 0, 1); b.grp.rotation.x = -f * .9; b.grp.position.y = X.B.y - f * 40; b.drive("overdrive", f < .4 ? (f * 6) % 1 : -1); }',
    'if (X.fall) { const be = s - X.fall - 2; b.boomE = be; b.drive("overdrive", be < 0 ? ((s - X.fall) * 2.4) % 1 : -1); X.fleetBooms = 1; sbBlast(W, X, be, t); if (be > .2) say("a7", "Its reactor went critical! The blast is tearing across the whole map!"); }')
rep("    : s < T0 + TL ? { y: 40, d: 330 + ft * 90, th: .18, ph: .35, tx: b.grp.position.x, tz: b.grp.position.z } : s < 84 ? { y: 50, d: 420, th: .32, ph: .6 + Math.sin(s * .08) * .5, tx: b.grp.position.x, tz: b.grp.position.z } : { y: 20, d: 640, th: .45, ph: .8 };",
    "    : s < T0 + TL ? { y: 40, d: 330 + ft * 90, th: .18, ph: .35, tx: b.grp.position.x, tz: b.grp.position.z } : s < 84 ? { y: 50, d: 420, th: .32, ph: .6 + Math.sin(s * .08) * .5, tx: b.grp.position.x, tz: b.grp.position.z } : s < 86 ? { y: 40, d: 480, th: .3, ph: .5, tx: b.grp.position.x, tz: b.grp.position.z } : { y: 60, d: 1150, th: .55, ph: .7 };")
rep("    D3.position.copy(sh.p).addScaledVector(X.F, (1 - w) * 260); if (dead)", "    D3.position.copy(sh.p).addScaledVector(X.F, (1 - w) * 260); if (X.bR) { const dd = sh.p.distanceTo(X.B); if (dd < X.bR) D3.position.add(X.V2.copy(sh.p).sub(X.B).normalize().multiplyScalar(Math.min(90, (X.bR - dd) * .2))); } if (dead)")
rep("  W.renderer.toneMappingExposure = X.exp * (1 - (b.dark || 0) * .55); }", "  W.renderer.toneMappingExposure = X.exp * (1 - (b.dark || 0) * .55) * (X.expK || 1); }")
# live: the same detonation from the record's moment of death
rep("if (dead) { const ff = clamp(df / 5, 0, 1); b.grp.rotation.x = -ff * .9; b.grp.position.y = X.B.y - ff * 40; } b.grp.scale.setScalar(scl); }",
    "if (dead) { const be = df - 2; b.boomE = be; if (be < 0) b.drive(\"overdrive\", (df * 2.4) % 1); sbBlast(W, X, be, t); if (be > -1 && be < 60) say(k + st.dead + \"x\", \"Aexion's reactor went critical! The blast is tearing across the whole map. Its wreckage is everywhere!\"); } b.grp.scale.setScalar(scl); }")
rep("  b.tick(t); W.renderer.toneMappingExposure = X.exp * (1 - (b.dark || 0) * .4); }", "  b.tick(t); W.renderer.toneMappingExposure = X.exp * (1 - (b.dark || 0) * .4) * (X.expK || 1); }")
s = re.sub(r"GAME_V = 453\b", "GAME_V = 454", s)
open(P, 'w').write(s)
