# v486 Aexion's Warform battle (owner: "don't make him too low, just low enough to give a convincing sword sweep, I want his battle to
# look amazing and authentic"; "also a good shielding pose with his shield reacting").
# Framing: the Warform replay camera has its own entry (WB_VIEW.aexW), set so his blade arc crosses the top of the attacking fleet.
# The sweep: wound high, he lunges and drops into it, knees bending, so the slash cuts down through the formation.
# The aegis: a braced guard, shield arm brought across the front, body crouched behind it, head tucked, sword drawn back, and the
# shield grows. The shield reacts: every hit that lands on his guard sends a ripple ring and a white impact flash through the hex
# cells with sparks, and kicks the shield and arm back; during the aegis a volley breaks across it, impact after impact.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
# --- framing ---
rep('V0 = m3 === "aexion" && battle && battle.r && battle.r.sbForm ? [-.4, [-26, 14, 70], [0, 14, 0]] : WB_VIEW[m3]',
    'V0 = m3 === "aexion" && battle && battle.r && battle.r.sbForm ? WB_VIEW.aexW : WB_VIEW[m3]')
rep('aexion: [-.4, [-26, 10, 64], [0, 9, 0]]', 'aexion: [-.4, [-26, 10, 64], [0, 9, 0]], aexW: [-.4, [-26, 16, 70], [0, 21, 0]] /* v486 Warform: the sweep crosses the fleet */')
# --- shield ripples (four impact slots) ---
rep('uHit: { value: new TH.Vector3(0, 0, -9) } }, transparent: true',
    'uHit: { value: new TH.Vector3(0, 0, -9) }, uR: { value: [0, 1, 2, 3].map(() => new TH.Vector4(0, 0, -1, 0)) } }, transparent: true')
rep('fragmentShader: "uniform vec3 uC; uniform float uO, uT; uniform vec3 uHit; varying vec2 vP;',
    'fragmentShader: "uniform vec3 uC; uniform float uO, uT; uniform vec3 uHit; uniform vec4 uR[4]; varying vec2 vP;')
rep('gl_FragColor = vec4(uC * k + vec3(w * .6), k); }" });\n    const shield = new TH.Mesh(new TH.CircleGeometry(6, 48), hexM);',
    'float rp = 0., ck = 0.; for (int i = 0; i < 4; i++) { vec4 R = uR[i]; if (R.z >= 0. && R.z < 1.) { float dd = length(vP - R.xy), a = 1. - R.z; rp += exp(-pow((dd - R.z * 7.5) / (.3 + R.z * .5), 2.)) * a * R.w; ck += exp(-dd * dd / (.1 + R.z * .9)) * a * a * R.w; } }\\n float im = e * (rp * (1.8 + h * 2.4) + ck * (.8 + h * 1.2)); k += im; gl_FragColor = vec4(uC * k + vec3(w * .6) + vec3(.8, .95, 1.) * e * (ck * .5 + rp * .15), k); }" });\n    const shield = new TH.Mesh(new TH.CircleGeometry(6, 48), hexM);')
# sparks that fly off the shield face where a shot lands
rep('shield.userData.dyn = 1; shield.position.set(-2.4, -3.2, .3); shield.rotation.y = -Math.PI / 2 + .2; LF.add(shield);',
    'shield.userData.dyn = 1; shield.position.set(-2.4, -3.2, .3); shield.rotation.y = -Math.PI / 2 + .2; LF.add(shield);\n    const shSp = Array.from({ length: 14 }, () => { const m = sprite(1.4, "rgba(215,240,255,1)", "aex_sp"); m.material.opacity = 0; m.visible = false; shield.add(m); return { m, t0: -1e9, x: 0, y: 0, vx: 0, vy: 0, vz: 0 }; }); /* v486 */')
# --- the pose ---
rep('const st0 = ss(.92, 1, u), g0 = t * .001; let gd = 0;', 'const st0 = ss(.92, 1, u), g0 = t * .001; let gd = 0, ag = 0;')
# the sweep: wound high, lunges down through it
rep('chest.rotation.y += (back * .3 - sw * .3) * (1 - rec); root.rotation.y += -sw * .08 * (1 - rec); body.position.z = sw * (1 - rec) * 1.5;',
    'chest.rotation.y += (back * .3 - sw * .3) * (1 - rec); root.rotation.y += -sw * .08 * (1 - rec); body.position.z = sw * (1 - rec) * 1.5;\n          { const lg = Math.max(back * .35, sw) * (1 - rec); body.position.y += back * (1 - sw) * .6 - lg * 1.5; chest.rotation.x += lg * .14 - back * (1 - sw) * .08; head.rotation.x += lg * .06; legs.forEach(L => { L.kn.rotation.x += lg * .34; L.hip.rotation.x -= lg * .22; L.an.rotation.x -= lg * .1; }); } /* v486 */')
rep('aq[0].set(Math.sin(th), -.06, Math.cos(th)).normalize();', 'aq[0].set(Math.sin(th), .06 - sw * .26, Math.cos(th)).normalize();')
# the aegis: braced behind the shield
rep('gd = Math.max(.85, bell(fa, 0, .12, .8, 1), od * .85) * st0 * (1 - stg * .7) * (out.shieldGone && !(fsb >= 0 && fsb < .55) ? 0 : 1); const A0 = arms[0], gq = out._gq || (out._gq = [new TH.Vector3(), new TH.Quaternion(), new TH.Vector3(0, -1, 0), new TH.Quaternion()]);\n        gq[0].set(-A0.sx * .45, -.5, .75).normalize(); gq[1].setFromUnitVectors(gq[2], gq[0]); A0.sh.quaternion.slerp(gq[1], gd); gq[3].setFromEuler(new TH.Euler(-1.75, 0, 0)); A0.el.quaternion.slerp(gq[3], gd); A0.sh.rotation.x += Math.sin(g0 * 1.1) * .04; }',
    '''gd = Math.max(.85, bell(fa, 0, .12, .8, 1), od * .85) * st0 * (1 - stg * .7) * (out.shieldGone && !(fsb >= 0 && fsb < .55) ? 0 : 1); const A0 = arms[0], gq = out._gq || (out._gq = [new TH.Vector3(), new TH.Quaternion(), new TH.Vector3(0, -1, 0), new TH.Quaternion()]);
        ag = (fa >= 0 ? bell(fa, 0, .14, .8, 1) : 0) * st0 * (gd > .3 ? 1 : 0); const rc = Math.exp(-Math.max(0, t - (out._rht || -1e9)) / 170) * (gd > .3 ? 1 : 0); /* v486 the aegis guard; rc: a hit jolting the shield */
        gq[0].set(-A0.sx * (.45 - ag * .45), -.5 + ag * .3, .75 + ag * .4).normalize(); gq[1].setFromUnitVectors(gq[2], gq[0]); A0.sh.quaternion.slerp(gq[1], gd); gq[3].setFromEuler(new TH.Euler(-1.75 - ag * .25, -ag * A0.sx * .9, 0)); A0.el.quaternion.slerp(gq[3], gd); A0.sh.rotation.x += Math.sin(g0 * 1.1) * .04 * (1 - ag) + rc * .2;
        if (ag > 0) { body.position.y -= 1.7 * ag; chest.rotation.x += .16 * ag; head.rotation.x += .16 * ag; root.rotation.y -= A0.sx * .2 * ag; legs.forEach(L => { L.hip.rotation.x -= .24 * ag; L.kn.rotation.x += .42 * ag; L.an.rotation.x -= .16 * ag; L.hip.rotation.z += L.sx * .1 * ag; }); A1.sh.rotation.x -= .5 * ag; A1.sh.rotation.z += A1.sx * .3 * ag; /* the sword raised behind the guard, ready */ }
        if (rc > .02) { chest.rotation.x -= rc * .05; body.position.z -= rc * .5; } }''')
rep('shield.scale.setScalar((u < .7 ? .55 : .55 + ss(.7, .85, u) * .45) * (1 + gd * .3));', 'shield.scale.setScalar((u < .7 ? .55 : .55 + ss(.7, .85, u) * .45) * (1 + gd * .3 + ag * .3));')
rep("hexM.uniforms.uO.value = u < .99 ? sh : .5 + bell(fa, 0, .15, .8, 1) * .7 + od * .4;", "hexM.uniforms.uO.value = u < .99 ? sh : .5 + bell(fa, 0, .15, .8, 1) * .35 + od * .4; /* v486 calmer, so the impacts read */")
# the sweep's arc follows the cut down through the fleet
rep("arcM.position.set(arms[1].sx * 4, 7.5, 0); arcM.rotation.set(Math.PI / 2 + .06, 0, -.25);", "arcM.position.set(arms[1].sx * 4, 6.5, 0); arcM.rotation.set(Math.PI / 2 + .06, .2 * arms[1].sx, -.25);")
# the shield reacting: ripples, flashes, sparks, the kick
rep('const hq = fa >= 0 ? (fa * 3) % 1 : -1; hexM.uniforms.uHit.value.set(Math.sin(t * .001) * 2.5, Math.cos(t * .0013) * 2, hq);',
    '''const hq = fa >= 0 ? (fa * 3) % 1 : -1; hexM.uniforms.uHit.value.set(Math.sin(t * .001) * 2.5, Math.cos(t * .0013) * 2, hq);
      { const R = out._rip || (out._rip = { a: [0, 1, 2, 3].map(() => ({ x: 0, y: 0, t0: -1e9, s: 0 })), i: 0, nx: 0, si: 0 }), on = shield.visible && gd > .3 && u > .99 && !(fsb >= 0); /* v486 the shield reacts */
        const land = (s0, x, y) => { const P = R.a[R.i++ % 4]; P.x = x; P.y = y; P.t0 = t; P.s = s0; for (let k = 0; k < (s0 > 1 ? 6 : 3); k++) { const Q = shSp[R.si++ % shSp.length], a = rnd() * 6.283, v = (.006 + rnd() * .012) * (s0 > 1 ? 1.4 : 1); Object.assign(Q, { t0: t, x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, vz: .004 + rnd() * .01, l: 260 + rnd() * 260 }); } };
        const spot = (r0) => { const a = rnd() * 6.283, r = Math.sqrt(rnd()) * r0; return [Math.cos(a) * r, Math.sin(a) * r]; };
        if (on && fx >= 0 && fx < .25 && t - (out._rht || -1e9) > 380) { out._rht = t; const [x, y] = spot(3.6); land(1.5, x, y); land(.6, x * .4 + (rnd() - .5) * 3, y * .4 + (rnd() - .5) * 3); }
        if (on && ag > .4 && t > R.nx) { R.nx = t + 110 + rnd() * 170; const [x, y] = spot(4.6); land(.55 + rnd() * .55, x, y); if (rnd() < .18) out._rht = t - 60; }
        R.a.forEach((P, k) => hexM.uniforms.uR.value[k].set(P.x, P.y, (t - P.t0) / 850, P.s));
        const rc = Math.exp(-Math.max(0, t - (out._rht || -1e9)) / 170) * (on ? 1 : 0); if (rc > .01) { hexM.uniforms.uO.value += rc * .9; shield.scale.multiplyScalar(1 + rc * .07); shield.position.z -= rc * 1.1; }
        shSp.forEach(Q => { const e = (t - Q.t0) / (Q.l || 1); Q.m.visible = e >= 0 && e < 1; if (Q.m.visible) { const a = t - Q.t0; Q.m.position.set(Q.x + Q.vx * a, Q.y + Q.vy * a, .2 + Q.vz * a); Q.m.material.opacity = (1 - e) * (1 - e); Q.m.scale.setScalar(1.6 * (1 - e * .6)); } }); }''')
# the Orbital Devourer's battle replay without its debris field (owner: "I don't like all the rocks and stuff around orbital devourer")
rep("const out = { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 15, h: 18, over: 0 }; return out; }", "const out = { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 15, h: 18, over: 0, debris: deb }; return out; }")
rep('WBR.b.grp.rotation.y = WBR.y0 = WB_FRONT[m3]', 'if (WBR.b.debris) WBR.b.debris.visible = false; /* v486 */ WBR.b.grp.rotation.y = WBR.y0 = WB_FRONT[m3]')
s = re.sub(r"GAME_V = 485\b", "GAME_V = 486", s)
open(P, 'w').write(s)
