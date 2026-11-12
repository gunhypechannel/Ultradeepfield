# v475 Remaster step 4, the Void Warden (live 2026-12-05).
# Its void now bends light: a swirling accretion disc and a shimmering lensing ring around the black core. Three weak points ride its
# turning rings, glowing so a fleet can see what to hit; in a battle each one cracks and goes dark as its hull falls past 75%, 50% and
# 25%. A new move, the gravity well: the rings race, the disc spins up and light streams into the core before it lets go. Its death:
# the rings spin out of control and the void swells and swallows them, then it turns to crystal like every boss.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep("const gy0 = gyro.map(g => g.rotation.clone()), ga = gyro.map(() => 0);\n    const mv = moves({ pulse: 1800, beam: 3200, summon: 3000, hit: 520 }), hit = hitKit(body, shk);",
r"""const gy0 = gyro.map(g => g.rotation.clone()), ga = gyro.map(() => 0);
    /* v475 the lensing disc and ring, the weak points on the rings, the gravity well's inflow */
    const adM = new TH.ShaderMaterial({ uniforms: { uT: { value: 0 }, uI: { value: 1 } }, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, side: TH.DoubleSide, toneMapped: false,
      vertexShader: "varying vec2 vP; void main() { vP = position.xy; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }",
      fragmentShader: "uniform float uT, uI; varying vec2 vP; void main() { float r = length(vP), a = atan(vP.y, vP.x), k = (r - 2.4) / 7.; if (k < 0. || k > 1.) discard; float s1 = .5 + .5 * sin(a * 3. - uT * 2.4 + r * 1.7), s2 = .5 + .5 * sin(a * 8. + uT * 1.1 - r * 2.6); float f = pow(1. - k, 1.3) * smoothstep(0., .06, k); float lane = pow(.5 + .5 * sin(r * 5. - a * 2. + uT * 3.), 8.); vec3 c = mix(vec3(.55, .22, 1.), vec3(1., .9, 1.), pow(1. - k, 4.) + lane * .4); float al = f * (.5 + 1.2 * s1 * s2 + lane * .9) * uI * 1.3; gl_FragColor = vec4(c * al, al); }" });
    const disc = new TH.Mesh(new TH.RingGeometry(2.4, 9.4, 160, 12), adM); disc.rotation.x = -Math.PI / 2 + .6; disc.userData.dyn = 1; body.add(disc);
    const lens = new TH.Sprite(new TH.SpriteMaterial({ map: radial("lensR", [[0, "rgba(255,255,255,0)"], [.5, "rgba(255,255,255,0)"], [.56, "rgba(246,230,255,1)"], [.62, "rgba(190,110,255,.45)"], [.8, "rgba(120,40,255,.1)"], [1, "rgba(90,20,200,0)"]]), blending: TH.AdditiveBlending, depthWrite: false, transparent: true, toneMapped: false })); lens.scale.set(8.4, 8.4, 1); body.add(lens);
    const wk = [1, 2, 3].map((gi, i) => { const g = new TH.Group(), R = [2.9, 5.0, 5.8][i], a = [0, 2.1, 4.2][i]; g.position.set(Math.cos(a) * (R + .5), 0, Math.sin(a) * (R + .5)); gyro[gi].add(g);
      g.add(new TH.Mesh(new TH.TorusGeometry(.85, .16, 8, 28), M)); const c = new TH.Mesh(new TH.OctahedronGeometry(.8, 0), glowMat(0xff7ac0, 1)); c.userData.dyn = 1; g.add(c); const sp = sprite(4.4, "rgba(255,110,190,1)"); g.add(sp); const dk = sprite(4, "rgba(60,0,90,1)"); dk.visible = false; g.add(dk); return { g, c, sp, dk, br: -1 }; });
    const inflow = []; for (let k = 0; k < 26; k++) { const c = sprite(1.1, "rgba(236,210,255,1)"); c.visible = false; body.add(c); inflow.push({ c, a: rnd() * TAU, r: 10 + rnd() * 8, y: (rnd() - .5) * 6, ph: rnd() }); }
    const mv = moves({ pulse: 1800, beam: 3200, summon: 3000, well: 3600, hit: 520 }), hit = hitKit(body, shk);""")
rep("const tick = t => { const fp = mv.f(\"pulse\", t), fb = mv.f(\"beam\", t), fs = mv.f(\"summon\", t), fh = mv.f(\"hit\", t);\n      const clench = bell(fp, 0, .4, .45, .55), burst = bell(fp, .45, .55, .7, 1), lock = bell(fb, 0, .25, .85, 1), fire = bell(fb, .28, .34, .8, .95), wide = bell(fs, 0, .3, .7, 1);\n      const spd = [.00016, -.0004, .00025, -.0002]; gyro.forEach((g, i) => { ga[i] += spd[i] * 16 * (1 + clench * 4 + lock * 2);",
"""const tick = t => { const fp = mv.f("pulse", t), fb = mv.f("beam", t), fs = mv.f("summon", t), fh = mv.f("hit", t), fw = mv.f("well", t), ov = out.over || 0;
      const clench = bell(fp, 0, .4, .45, .55), burst = bell(fp, .45, .55, .7, 1), lock = bell(fb, 0, .25, .85, 1) * (1 - ov), fire = bell(fb, .28, .34, .8, .95), wide = bell(fs, 0, .3, .7, 1), pull = bell(fw, 0, .2, .72, .8), rel = bell(fw, .72, .78, .86, 1), swl = ov > .45 ? (ov - .45) / .55 : 0;
      const spd = [.00016, -.0004, .00025, -.0002]; gyro.forEach((g, i) => { ga[i] += spd[i] * 16 * (1 + clench * 4 + lock * 2 + pull * 6 + ov * ov * 40);""")
rep("const pul = 1 + Math.sin(t * .0025) * .03 - clench * .18 + burst * .25 + fire * .1; core.scale.setScalar(pul);",
    "const pul = 1 + Math.sin(t * .0025) * .03 - clench * .18 + burst * .25 + fire * .1 - pull * .12 + rel * .3; core.scale.setScalar(pul * (1 + swl * 1.9));")
rep("vw(fp < 0 ? -1 : (fp - .45) / .55); vw2(fp < 0 ? -1 : (fp - .47) / .5);",
"""vw(fp >= 0 ? (fp - .45) / .55 : fw >= .72 ? (fw - .72) / .28 : -1); vw2(fp < 0 ? -1 : (fp - .47) / .5);
      // the void bends the light round it; the gravity well spins it up and draws light in; dying, the void swells and swallows its rings
      adM.uniforms.uT.value = (TW.dt = (TW.dt || 0) + .016 * (1 + pull * 5 + ov * 8)); adM.uniforms.uI.value = (1 + pull * 1.2 + rel * .8 + ov * 1.5) * (1 - swl * .9); disc.scale.setScalar((1 - pull * .18 + rel * .25) * (1 - swl * .75)); disc.rotation.z = t * .0001;
      lens.material.opacity = Math.min(1, .75 + Math.sin(t * .004) * .12 + pull * .3 + ov * .4); lens.scale.setScalar(8.4 * (1 + Math.sin(t * .0017) * .03 - pull * .1 + rel * .45 + ov * .6 + swl * 1.2));
      for (const I of inflow) { I.c.visible = pull > .02 || ov > .05; if (!I.c.visible) continue; const u = (t * .0009 + I.ph) % 1, k = 1 - u; I.c.position.set(Math.cos(I.a + u * 4) * I.r * k, I.y * k, Math.sin(I.a + u * 4) * I.r * k); I.c.material.opacity = Math.max(pull, ov) * Math.min(1, u * 3) * (1 - swl); }
      const hpN = out.hp == null ? 1 : out.hp; wk.forEach((W0, i) => { const dead = hpN < [.75, .5, .25][i] || swl > .3; if (dead && W0.br < 0) W0.br = t; const b = W0.br < 0 ? -1 : (t - W0.br) / 1400;
        W0.c.visible = W0.br < 0; W0.sp.material.opacity = W0.br < 0 ? .75 + .25 * Math.sin(t * .006 + i * 2) + bell(fh, 0, .05, .3, .8) * .6 : b < .25 ? 1 : 0; W0.sp.scale.setScalar(W0.br < 0 ? 4.4 : 4.4 + b * 14); W0.dk.visible = b >= 0 && b < 1; if (W0.dk.visible) { W0.dk.scale.setScalar(2 + b * 6); W0.dk.material.opacity = (1 - b) * .9; }
        W0.g.rotation.y = t * .002 + i; W0.g.scale.setScalar(1 - swl * .8); });
      for (const c of crs) c.g.position.x *= 1 - swl * .55; gyro.forEach(g => g.scale.setScalar(1 - swl * .55));""")
rep("bt(t, 1 + clench * 4 + fire * 3 + wide * 3); hit(bell(fh, 0, .05, .4, 1), t); };\n    bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 10, h: 15 }; }",
    "bt(t, 1 + clench * 4 + fire * 3 + wide * 3 + pull * 4 + ov * 8); hit(Math.max(bell(fh, 0, .05, .4, 1), ov * .6 * (1 - swl)), t); };\n    const TW = {}; bake(body); const out = { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 10, h: 15, over: 0, hp: null, setHp: h => { out.hp = h; } }; return out; }")
# a battle tells the boss its hull, so the Warden's weak points crack as it falls
rep("WBR.hp = b.hp;", "WBR.hp = b.hp; if (WBR.b.setHp) WBR.b.setHp(b.hp);")
# the fight: its new move
rep('war: ["pulse", "beam", "summon"]', 'war: ["pulse", "beam", "well", "summon"]')
rep('war: { pulse: ["wave", .2, .75, 0, 1800], beam: ["beam", .35, .82, 0, 3200] },', 'war: { pulse: ["wave", .2, .75, 0, 1800], beam: ["beam", .35, .82, 0, 3200], well: ["wave", .72, .95, 0, 3600] },')
rep('["summon", "Satellite storm", "Its satellites fly wide and rain lightning."]], "con":',
    '["well", "Gravity well", "Its rings race, light streams into the void, and then it lets go in a crushing wave."], ["summon", "Satellite storm", "Its satellites fly wide and rain lightning."]], "con":')
# its death: a longer overload while the void swells
rep('key === "dev" ? 3.6 : 2;', 'key === "dev" ? 3.6 : key === "war" ? 3.2 : 2;')
s = re.sub(r"GAME_V = 474\b", "GAME_V = 475", s)
open(P, 'w').write(s)
