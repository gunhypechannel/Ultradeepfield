# v473 Remaster step 3, the Orbital Devourer (live 2026-11-28).
# A field of debris orbits it and its storms fling the rocks wide. Its lash is now a sweep of the whole body. A new grab: the tentacles
# reach far out in front of the maw, clutch, and drag their catch in before the claws snap shut. The vortex beam charges first, motes of
# light spiralling into the maw. A new plasma storm: it clenches, then vents a shell of plasma and lightning in every direction.
# Its own death: the vortex spins up, the tentacles thrash, the debris is sucked into the maw, the maw implodes, and only then the blast.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
# tentacles remember the way forward, out of the maw
rep("body.add(root); tents.push({ root, base, J, curl, ph: rnd() * TAU, w: .0009 + rnd() * .0006, front }); };",
    "body.add(root); const qR = new TH.Quaternion().setFromUnitVectors(V(0, 1, 0), V(1.3, d.y * .45, d.z * .45).normalize().applyQuaternion(root.quaternion.clone().invert())); tents.push({ root, base, J, curl, ph: rnd() * TAU, w: .0009 + rnd() * .0006, front, qR }); };")
# the galaxy-map tentacles: reach (uG) and clutch (uC) in the shader
rep("sh.uniforms.uL = { value: 0 }; TL.userData.sh = sh;", "sh.uniforms.uL = { value: 0 }; sh.uniforms.uG = { value: 0 }; sh.uniforms.uC = { value: 0 }; TL.userData.sh = sh;")
rep('sh.vertexShader = "uniform float uT, uA, uL; attribute float aPh;\\n"', 'sh.vertexShader = "uniform float uT, uA, uL, uG, uC; attribute float aPh;\\n"')
rep("* uA) * s * s * 1.6;\"); };", "* uA) * s * s * 1.6; transformed.yz *= 1.0 - uC * s * s * .6; transformed.x += uG * s * s * 26.0;\"); };")
rep("const roarW = wave(maw, 3.5, true);\n    const mv = moves({ bite: 1100, lash: 1600, beam: 3000, roar: 2400, hit: 520 }), hit = hitKit(body, shk);",
r"""const roarW = wave(maw, 3.5, true);
    /* v473 the debris field, the beam's charge, the grab's catch, the plasma storm */
    const DN = LOD ? 34 : 24, deb = new TH.InstancedMesh(new TH.DodecahedronGeometry(1, 0), MS, DN); deb.userData.dyn = 1; deb.frustumCulled = false; grp.add(deb);
    const dD = []; for (let i = 0; i < DN; i++) dD.push({ r: 17 + rnd() * 13, a: rnd() * TAU, w: (.00009 + rnd() * .00016) * (rnd() < .8 ? 1 : -1), y: (rnd() - .5) * 6, s: .3 + rnd() * rnd() * 1.7, sp: rnd() * TAU, ax: V(rnd() - .5, rnd() - .5, rnd() - .5).normalize() });
    const dM = new TH.Matrix4(), dQ = new TH.Quaternion(), dP = V(0, 0, 0), dS = V(1, 1, 1), mawW = V(4, 0, 0);
    const chg = []; for (let k = 0; k < 22; k++) { const c = sprite(1.3, "rgba(236,205,255,1)"); c.visible = false; maw.add(c); chg.push({ c, a: rnd() * TAU, r: 8 + rnd() * 10, x: 5 + rnd() * 9, ph: rnd() }); }
    const prey = sprite(5, "rgba(255,214,176,1)"); prey.visible = false; maw.add(prey);
    const stG = new TH.Group(); body.add(stG); stG.visible = false; const stB = bolts(stG, 16, () => { const a = rnd() * TAU, R = 15 + rnd() * 18, p = V(-7 + rnd() * 10, Math.cos(a) * 2.7, Math.sin(a) * 2.7), b = a + (rnd() - .5) * .9; return [p, V(p.x + (rnd() - .5) * 14, Math.cos(b) * R, Math.sin(b) * R)]; }, 0xe0b0ff);
    const stS = new TH.Mesh(new TH.SphereGeometry(8, 40, 24), vmat.clone()); stS.material.opacity = 0; stS.material.color.set(0xe0a8ff); stS.userData.dyn = 1; stS.visible = false; stS.position.x = -3; body.add(stS); const stW = wave(body, 11, true, 0xc070ff), imp = wave(maw, 6, true, 0xc070ff);
    const mv = moves({ bite: 1100, lash: 1900, beam: 3800, roar: 2400, grab: 3000, storm: 4200, hit: 520 }), hit = hitKit(body, shk), _q = new TH.Quaternion();""")
# the tick: new phases
rep("const tick = t => { const fb = mv.f(\"bite\", t), fl = mv.f(\"lash\", t), fm = mv.f(\"beam\", t), fr = mv.f(\"roar\", t), fh = mv.f(\"hit\", t);\n      const gapeB = bell(fb, 0, .4, .45, .55), snap = bell(fb, .45, .55, .7, 1), gapeM = bell(fm, 0, .2, .85, 1), fire = bell(fm, .25, .3, .82, .95), flare = bell(fr, 0, .15, .7, 1);\n      const open = .12 + Math.sin(t * .0015) * .06 + gapeB * .85 + gapeM * .7 + flare * .5 - snap * .25;",
"""const tick = t => { const fb = mv.f("bite", t), fl = mv.f("lash", t), fm = mv.f("beam", t), fr = mv.f("roar", t), fh = mv.f("hit", t), fg = mv.f("grab", t), fs = mv.f("storm", t), ov = out.over || 0;
      const gapeB = bell(fb, 0, .4, .45, .55), snap = bell(fb, .45, .55, .7, 1), gapeM = bell(fm, 0, .3, .88, 1), fire = bell(fm, .36, .42, .86, .96), chargeK = bell(fm, 0, .06, .36, .42), flare = Math.max(bell(fr, 0, .15, .7, 1), ov * .8);
      const reach = bell(fg, 0, .28, .42, .55), clutch = bell(fg, .42, .52, .8, .95), snap2 = bell(fg, .8, .86, .93, 1), clench = bell(fs, 0, .22, .3, .36), burst = bell(fs, .3, .36, .7, 1), sweep = fl < 0 ? 0 : -bell(fl, 0, .18, .28, .5) * .35 + bell(fl, .28, .45, .62, 1) * .6;
      const implo = ov > .62 ? (ov - .62) / .38 : 0;
      const open = .12 + Math.sin(t * .0015) * .06 + gapeB * .85 + gapeM * .7 + flare * .5 - snap * .25 + reach * .8 + clutch * .3 - snap2 * .45 - clench * .3 + burst * .6 + ov * .6 - implo * 1.1;""")
rep("body.position.x = snap * 1.4 - gapeB * .3 - fire * .4 * (.6 + rnd() * .4); body.rotation.x = Math.sin(t * .00035) * .12; body.rotation.z = Math.sin(t * .0006) * .04 + Math.sin(t * .00023) * .03;",
    "body.position.x = snap * 1.4 - gapeB * .3 - fire * .4 * (.6 + rnd() * .4) + reach * 1.6 - clutch * 1.1 + snap2 * 1.2 - clench * .8 + (rnd() - .5) * (ov * .5 + burst * .25); body.rotation.x = Math.sin(t * .00035) * .12; body.rotation.z = Math.sin(t * .0006) * .04 + Math.sin(t * .00023) * .03; body.rotation.y = sweep; body.scale.setScalar(1 - clench * .05 + burst * .03);")
rep("const splay = Math.max(gapeM, flare);", "const splay = Math.max(gapeM, flare, burst), hold = Math.min(1, reach + clutch);")
rep("""          if (T.front) z += Math.sin(t * .006 + i + T.ph) * .08 * (gapeB + flare);
          j.rotation.set(x, 0, z); });""", """          if (T.front) z += Math.sin(t * .006 + i + T.ph) * .08 * (gapeB + flare);
          if (hold) z = z * (1 - reach * .85) + clutch * (u > .35 ? .3 : .06) * (T.curl < 0 ? -1 : 1);
          z += clench * .1 * (T.curl < 0 ? -1 : 1) + Math.sin(t * .02 + i * 1.3 + T.ph) * .22 * ov * (1 - implo);
          j.rotation.set(x, 0, z); });""")
rep("T.base.rotation.z = -splay * .45 * Math.sign(T.curl) + (whip ? -bell(fl, 0, .2, .3, .6) * .4 + bell(fl, .3, .45, .6, 1) * .9 : 0); }",
    "T.base.rotation.z = -splay * .45 * Math.sign(T.curl) + (whip ? -bell(fl, 0, .2, .3, .6) * .4 + bell(fl, .3, .45, .6, 1) * .9 : 0); if (hold) T.base.quaternion.slerp(T.qR, hold * (T.front ? .55 : .8)); }")
rep("u.uA.value = 1 + splay * .8 + (fl >= 0 ? bell(fl, .1, .3, .5, .9) * 1.2 : 0); u.uL.value = fl >= 0 ? -bell(fl, 0, .15, .2, .4) * .4 + bell(fl, .25, .4, .55, .9) : 0; }",
    "u.uA.value = (1 + splay * .8 + (fl >= 0 ? bell(fl, .1, .3, .5, .9) * 1.6 : 0) + ov * 2.2 * (1 - implo)) * (1 - reach * .7) * (1 - clench * .5); u.uL.value = fl >= 0 ? -bell(fl, 0, .15, .2, .4) * .4 + bell(fl, .25, .4, .55, .9) : 0; u.uG.value = reach + clutch * .75 - implo * .3; u.uC.value = clutch * .9 + clench * .5 + implo; }")
rep("vort.rotation.x = -t * (.0012 + fire * .01); vort2.rotation.x = t * (.002 + fire * .012); hot.material.opacity = .8 + Math.sin(t * .007) * .2; hot.scale.setScalar(4.2 * (1 + fire * 1.4 + gapeM * .3)); glow.material.opacity = .7 + fire * .3;",
"""vort.rotation.x = -t * (.0012 + fire * .01) - (TW.sp = (TW.sp || 0) + ov * .25); vort2.rotation.x = t * (.002 + fire * .012) + TW.sp * 1.3; hot.material.opacity = .8 + Math.sin(t * .007) * .2; hot.scale.setScalar(4.2 * (1 + fire * 1.4 + gapeM * .3 + chargeK * 1.1 + ov * 2.2) * (1 - implo * .9)); glow.material.opacity = Math.min(1, .7 + fire * .3 + chargeK * .3 + ov);
      { const vs = (1 + ov * .5) * (1 - implo * .97); vort.scale.setScalar(vs); vort2.scale.setScalar(.72 * vs); glow.scale.setScalar(9 * (1 + ov * 1.5) * (1 - implo * .8)); imp(implo > 0 && implo < 1 ? 1 - implo : -1); }
      for (const C of chg) { C.c.visible = chargeK > .01; if (!C.c.visible) continue; const u = (t * .0012 + C.ph) % 1, k = 1 - u; C.c.position.set(.5 + C.x * k, Math.cos(C.a + u * 3) * C.r * k, Math.sin(C.a + u * 3) * C.r * k); C.c.material.opacity = chargeK * Math.min(1, u * 3); C.c.scale.setScalar(1.3 * (.5 + k)); }
      prey.visible = fg >= .45 && fg < .86; if (prey.visible) { const u = (fg - .45) / .41; prey.position.set(.6 + (1 - u * u) * 16, 0, 0); prey.material.opacity = .9 - u * .4; prey.scale.setScalar(5 * (1 - u * .6)); }
      stG.visible = burst > .02; stS.visible = burst > .01; if (stS.visible) { stS.scale.setScalar(1 + burst * 1.5 + (fs - .3) * 1.2); stS.material.opacity = burst * .3; stS.rotation.x = t * .002; stS.rotation.y = -t * .0013; } stW(fs < .3 ? -1 : (fs - .3) / .7);
      // the debris field: flung wide by its storms, drawn into the maw as it dies
      grp.updateMatrixWorld(); mawW.set(1, 0, 0); maw.localToWorld(mawW); grp.worldToLocal(mawW);
      for (let i = 0; i < DN; i++) { const d = dD[i], a = d.a + t * d.w, R = d.r * (1 + burst * .35 - clench * .12) + Math.sin(t * .0009 + d.sp) * .6;
        dP.set(Math.cos(a) * R, d.y + Math.sin(a) * R * .3 + Math.sin(t * .0005 + d.sp) * .8, Math.sin(a) * R);
        const pull = Math.min(1, Math.max(0, ov * 1.7 - (i % 7) * .1)); if (pull > 0) dP.lerp(mawW, pull * pull);
        dQ.setFromAxisAngle(d.ax, t * (.0006 + ov * .01) + d.sp); dS.setScalar(d.s * (1 - pull * pull * .9)); dM.compose(dP, dQ, dS); deb.setMatrixAt(i, dM); }
      deb.instanceMatrix.needsUpdate = true;""")
rep("roarW(fr < 0 ? -1 : fr * 1.3); bt(t, 1 + flare * 5 + fire * 3); hit(bell(fh, 0, .05, .4, 1), t); };\n    bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 15, h: 18 }; }",
    "roarW(fr < 0 ? -1 : fr * 1.3); bt(t, 1 + flare * 5 + fire * 3 + clutch * 3 + ov * 8); if (stG.visible) stB(t, .4 + burst * 4); hit(Math.max(bell(fh, 0, .05, .4, 1), ov * .7 * (1 - implo)), t); };\n    bake(body); const out = { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 15, h: 18, over: 0 }; return out; }")
# the fight: its new moves, their strikes and callouts
rep('dev: ["bite", "lash", "beam", "roar"]', 'dev: ["bite", "lash", "beam", "grab", "storm", "roar"]')
rep('dev: { lash: ["bolts", .3, .65, 4, 1600], beam: ["beam", .35, .85, 0, 3000], roar: ["wave", .3, .85, 0, 2400] },',
    'dev: { lash: ["bolts", .3, .65, 4, 1900], beam: ["beam", .42, .88, 0, 3800], roar: ["wave", .3, .85, 0, 2400], grab: ["bolts", .45, .75, 3, 3000], storm: ["bolts", .32, .85, 9, 4200] },')
rep('["roar", "Roar", "Lightning crackles through everything around it."]]',
    '["roar", "Roar", "Lightning crackles through everything around it."], ["grab", "Tentacle grab", "Its tentacles reach out ahead of the maw, seize ships and drag them in."], ["storm", "Plasma storm", "It clenches, then vents a storm of plasma and lightning in every direction."]]')
rep('["lash", "Tentacle lash", "A whip of tentacles sweeps through the fleet."]', '["lash", "Tentacle lash", "It swings its whole body and its tentacles sweep through the fleet."]')
# its death: a longer overload, the maw implodes before the blast
rep('OV = con ? .8 : key === "ovl" ? 3 : 2;', 'OV = con ? .8 : key === "ovl" ? 3 : key === "dev" ? 3.6 : 2;')
s = re.sub(r"GAME_V = 472\b", "GAME_V = 473", s)
open(P, 'w').write(s)
