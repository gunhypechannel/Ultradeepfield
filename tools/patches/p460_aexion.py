# v460 Aexion (owner: more active; the blade sweeps across, not down; the shield held up to guard; breathtakingly real; more missiles;
# he dies as crystal fading away like souls; the Advisor genuinely shocked when he transforms).
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
# materials: deeper reflections and sharper panel relief
rep('rep: [.14, .14], relief: 2.2 }); MA.envMapIntensity = .85;', 'rep: [.14, .14], relief: 2.2 }); MA.envMapIntensity = 1.35; MA.normalScale.set(2.2, 2.2);')
rep('rc: RC, ei: 3.6, rep: [.16, .16] });\n', 'rc: RC, ei: 3.6, rep: [.16, .16] }); MD.envMapIntensity = 1.5; MD.normalScale.set(2, 2);\n')
# more missiles, with glowing trails, flying out to the fleet
rep("const NM = LO ? 16 : 28, mis = puffs(NM, 0xbfe4ff); body.add(mis);", "const NM = LO ? 36 : 72, mis = puffs(NM, 0xdff2ff), misT = puffs(NM * 3, 0x6ab8ff); body.add(mis); body.add(misT);")
rep("""      for (let k = 0; k < NM; k++) { const m = mD[k], q = fm < 0 ? -1 : (fm - m.h * .4) / .5; if (q > 0 && q < 1) { const P = pods[m.s].p.getWorldPosition(S.p); body.worldToLocal(P); mis.put(k, P.x + Math.sin(m.a) * q * 6, P.y + q * 6 - q * q * 4 + Math.cos(m.a) * q * 2, P.z + q * 34 * m.d + q * 8, 1.6, 1 - q * .3); } else mis.put(k, 0, 0, 0, 0, 0); } mis.done();""",
"""      for (let k = 0; k < NM; k++) { const m = mD[k], q1 = fm < 0 ? -1 : (fm - m.h * .45) / .5, q2 = od > .05 && u > .99 ? ((t * .00045 + m.h) % 1) : -1, q = q1 > 0 && q1 < 1 ? q1 : q2; if (q > 0 && q < 1) { const P = pods[m.s].p.getWorldPosition(S.p); body.worldToLocal(P); const at = qq => [P.x + Math.sin(m.a) * qq * 16 * m.d, P.y + qq * 16 - qq * qq * 14 + Math.cos(m.a) * qq * 5, P.z + qq * 95 * m.d + qq * 12];
          const h = at(q); mis.put(k, h[0], h[1], h[2], 1.5, 1); for (let j = 1; j <= 3; j++) { const p2 = at(Math.max(0, q - j * .025)); misT.put(k * 3 + j - 1, p2[0], p2[1], p2[2], 1.6 + j * .5, (1 - j * .28) * .8); } } else { mis.put(k, 0, 0, 0, 0, 0); for (let j = 0; j < 3; j++) misT.put(k * 3 + j, 0, 0, 0, 0, 0); } } mis.done(); misT.done();""")
# the warform's stance and the blade: alive every moment; the blade sweeps across; the shield up to guard
rep("""      if (fb >= 0 && u > .99) { const sw = ss(.25, .6, fb), back = bell(fb, 0, .2, .3, .45); arms[1].sh.rotation.x += -back * 1.6 + sw * 1.2; arms[1].sh.rotation.z += back * .5 - sw * 1.1; arms[1].el.rotation.x -= back * .4; }
      arcM.visible = fb >= 0 && u > .99; if (arcM.visible) { const k = bell(fb, .3, .4, .6, .85); arcM.material.opacity = k * .8; arcM.position.set(0, 4, 6); arcM.rotation.set(-Math.PI / 2 + .3, 0, -.6 + ss(.3, .6, fb) * 1.4); arcM.scale.setScalar(.6 + ss(.3, .9, fb) * .7); }""",
"""      const st0 = ss(.92, 1, u), g0 = t * .001; let gd = 0;
      if (st0 > 0) { /* v460 the warform is never still: weight shifting, torso and head tracking targets, knees bent, blade ready */
        root.rotation.y += Math.sin(g0 * .55) * .1 * st0; body.position.x = Math.sin(g0 * .4) * .8 * st0; chest.rotation.y += Math.sin(g0 * .75 + 1) * .13 * st0; chest.rotation.x += (.07 + Math.sin(g0 * .9) * .025) * st0;
        head.rotation.y += (Math.sin(g0 * .5) * .3 + Math.sin(g0 * 2.1) * .05) * st0; head.rotation.x += (Math.sin(g0 * 1.3) * .05 - .06) * st0;
        legs.forEach((L, k) => { const w = Math.sin(g0 * .55 + k * Math.PI) * .07; L.hip.rotation.x += (-.24 + w) * st0; L.kn.rotation.x += (.42 - w * 1.3) * st0; L.an.rotation.x += -.17 * st0; L.hip.rotation.z += L.sx * .07 * st0; });
        const A1 = arms[1]; A1.sh.rotation.x += (-.5 + Math.sin(g0 * 1.2) * .07) * st0; A1.sh.rotation.z += A1.sx * .18 * st0; A1.el.rotation.x += -.6 * st0;
        if (fb >= 0) { const back = bell(fb, 0, .18, .3, .42), sw = ss(.3, .52, fb), rec = ss(.72, 1, fb), up = Math.max(back, sw) * (1 - rec), th = 2.1 - sw * 3.0; /* a wide level slash: wound back, then swept across the front */
          chest.rotation.y += (back * .3 - sw * .3) * (1 - rec); root.rotation.y += -sw * .08 * (1 - rec); body.position.z = sw * (1 - rec) * 1.5;
          const aq = out._aq || (out._aq = [new TH.Vector3(), new TH.Quaternion(), new TH.Vector3(0, -1, 0), new TH.Quaternion()]); aq[0].set(Math.sin(th), -.06, Math.cos(th)).normalize(); aq[1].setFromUnitVectors(aq[2], aq[0]);
          A1.sh.quaternion.slerp(aq[1], up); A1.el.quaternion.slerp(aq[3], up); sword.rotation.x = Math.PI / 2 + .25 + (Math.PI / 2 - .25) * up; } else sword.rotation.x = Math.PI / 2 + .25;
        gd = Math.max(.85, bell(fa, 0, .12, .8, 1), od * .85) * st0; const A0 = arms[0], gq = out._gq || (out._gq = [new TH.Vector3(), new TH.Quaternion(), new TH.Vector3(0, -1, 0), new TH.Quaternion()]);
        gq[0].set(-A0.sx * .45, -.5, .75).normalize(); gq[1].setFromUnitVectors(gq[2], gq[0]); A0.sh.quaternion.slerp(gq[1], gd); gq[3].setFromEuler(new TH.Euler(-1.75, 0, 0)); A0.el.quaternion.slerp(gq[3], gd); A0.sh.rotation.x += Math.sin(g0 * 1.1) * .04; }
      arcM.visible = fb >= 0 && u > .99; if (arcM.visible) { const k = bell(fb, .28, .36, .58, .8); arcM.material.opacity = k * .9; arcM.position.set(arms[1].sx * 4, 7.5, 0); arcM.rotation.set(Math.PI / 2 + .06, 0, -.25); arcM.scale.setScalar(1.25 + ss(.3, .6, fb) * .35); }""")
# the shield, when guarding, turns to face the front squarely and grows
rep("shield.scale.setScalar(u < .7 ? .55 : .55 + ss(.7, .85, u) * .45);",
    "shield.scale.setScalar((u < .7 ? .55 : .55 + ss(.7, .85, u) * .45) * (1 + gd * .3)); if (gd > 0) { body.updateMatrixWorld(true); const qb = body.getWorldQuaternion(S.q.clone()), ql = LF.getWorldQuaternion(new TH.Quaternion()); const tq = ql.invert().multiply(qb); shield.quaternion.copy(shield.userData.q0 || (shield.userData.q0 = shield.quaternion.clone())).slerp(tq, Math.min(1, gd * 1.2)); shield.position.set(-2.4 + gd * 1.6, -3.2 - gd * .6, .3 + gd * 3.2); } else if (shield.userData.q0) { shield.quaternion.copy(shield.userData.q0); shield.position.set(-2.4, -3.2, .3); }")
# live: more missiles and blade sweeps in the rotation
rep('mv: ["broadside", "missiles", "rail"]', 'mv: ["broadside", "missiles", "rail", "missiles"]')
rep('mv2: ["aegis", "blade", "missiles", "lance"]', 'mv2: ["aegis", "blade", "missiles", "lance", "blade", "missiles", "aegis"]')
# the Advisor, caught off guard by the transformation
L1 = "Wait. What is that? Aexion's hull is shifting..."
L2 = "Wait... I think it's... transforming? It IS transforming! Its whole hull is splitting apart!"
rep('if (ft > 0) say("a2", "WARNING: Aexion is transforming! Its hull is splitting apart!");', 'if (ft > 0) say("a2", "%s"); if (ft > .2) say("a2b", "%s");' % (L1, L2))
rep('if (xf && T - xf < 60000) say(k + xf, "WARNING: Aexion is transforming! Its hull is splitting apart!");',
    'if (xf && T - xf < 60000) say(k + xf, "%s"); if (xf && T - xf > 10000 && T - xf < 60000) say(k + xf + "b", "%s"); if (xf && T - xf > 32000 && T - xf < 90000) say(k + xf + "c", "It\'s standing up. That thing is a Warform!");' % (L1, L2))
# his fall: after the blast scatters him, every piece turns to crystal and dissolves into rising souls
rep("sbBlast(W, X, be, t); if (be > .2) say(\"a7\"", "sbBlast(W, X, be, t); sbVaeCrystal(W, X, b, be - 1.2, t, 1); if (be > .2) say(\"a7\"")
rep("sbBlast(W, X, be, t); if (be > -1 && be < 60)", "sbBlast(W, X, be, t); sbVaeCrystal(W, X, b, be - 1.2, t, 1); if (be > -1 && be < 60)")
# the crystal works for any boss: souls drawn from points on the real surface, glow pieces kept hidden while the wreck still moves
rep("function sbVaeCrystal(W, X, b, e, t) { if (e < .55) return false;", "function sbVaeCrystal(W, X, b, e, t, moving) { if (e < .55) return false;")
rep("const m = new TH.ShaderMaterial({ uniforms: { uT: { value: 0 }, uD: { value: 0 }, uO: { value: 1 }, uY: { value: new TH.Vector2(-40, 120) } }",
    "const hide = []; const m = new TH.ShaderMaterial({ uniforms: { uT: { value: 0 }, uD: { value: 0 }, uO: { value: 1 }, uY: { value: new TH.Vector2(-40, 120) } }")
rep("if (add) { o.visible = false; return; } o.userData.om = mt; o.material = m; keep.push(o); }\n      else if (o.isSprite || o.isPoints || o.isLine) o.visible = false; });",
    "if (add) { o.visible = false; hide.push(o); return; } o.userData.om = mt; o.material = m; keep.push(o); }\n      else if (o.isSprite || o.isPoints || o.isLine) { o.visible = false; hide.push(o); } });")
rep("src.push(Vp.clone()); } }", "src.push({ w: Vp.clone() }); } }")
rep("else src.push(o.getWorldPosition(new TH.Vector3())); }",
    "else { const pa = o.geometry.attributes.position, nn = Math.min(8, pa.count); for (let i = 0; i < nn; i++) { const l = new TH.Vector3().fromBufferAttribute(pa, (Math.random() * pa.count) | 0); src.push({ o, l, w: l.clone().applyMatrix4(o.matrixWorld) }); } } }")
rep("const p = src[(r() * src.length) | 0] || bb.getCenter(new TH.Vector3()); S.push({ p:", "const sr = src[(r() * src.length) | 0] || { w: bb.getCenter(new TH.Vector3()) }, p = sr.w; S.push({ sr, p:")
rep("pp.set([q.p.x + Math.sin(w) * 22 * a * q.sw, q.p.y + y, q.p.z + Math.cos(w) * 22 * a], i * 3);",
    "let bx = q.p.x, by = q.p.y, bz = q.p.z; if (q.sr.o) { const ww = q.sr.o.localToWorld(C.v.copy(q.sr.l)); bx += ww.x - q.sr.w.x; by += ww.y - q.sr.w.y; bz += ww.z - q.sr.w.z; } pp.set([bx + Math.sin(w) * 22 * a * q.sw, by + y, bz + Math.cos(w) * 22 * a], i * 3);")
rep("X.cry = { m, S, pts, keep }; }", "X.cry = { m, S, pts, keep, hide, v: new TH.Vector3() }; if (moving) m.uniforms.uB.value = 2.6; }")
rep("uO: { value: 1 }, uY: { value: new TH.Vector2(-40, 120) } }", "uO: { value: 1 }, uB: { value: 1 }, uY: { value: new TH.Vector2(-40, 120) } }")
rep("fragmentShader: \"uniform float uT, uD, uO; uniform vec2 uY; varying vec3 vW;", "fragmentShader: \"uniform float uT, uD, uO, uB; uniform vec2 uY; varying vec3 vW;")
rep("+ edge * .3) * uO;", "+ edge * .3) * uO * uB;")
rep("const C = X.cry, D = clamp((e - 1.8) / 4.6, 0, 1);", "const C = X.cry, D = clamp((e - 1.8) / 4.6, 0, 1); if (moving) for (const o of C.hide) o.visible = false;")
s = re.sub(r"GAME_V = 459\b", "GAME_V = 460", s)
open(P, 'w').write(s)
