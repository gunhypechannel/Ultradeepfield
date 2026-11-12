# v462 Aexion fights like a duelist, and loses in stages (owner: "dodges with his thrusters then swipes across, dodges then shields then uses
# his launcher, gets staggered, loses his shield then his sword, then uses his centre beam before being slain"); and the super bosses come
# back stronger (owner: "when they show up next time the Advisor should say they are back, and appear even stronger now").
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
# new moves: a thruster dodge, a stagger, the shield breaking, the sword lost
rep("const mv = moves({ transform: 20000, broadside: 2200, missiles: 3000, rail: 2600, aegis: 2400, blade: 2600, lance: 2800, overdrive: 4200, hit: 520 })",
    "const mv = moves({ transform: 20000, broadside: 2200, missiles: 3000, rail: 2600, aegis: 2400, blade: 2600, lance: 3200, overdrive: 4200, hit: 520, dodge: 1500, stagger: 1700, sbreak: 2200, wbreak: 2400 })")
rep('const out = { grp, r: 22, h: 30, form: 0, ph: "ship", act: n => { if (n === "transform" && out.form > .99) return; mv.play(n); },',
    'const out = { grp, r: 22, h: 30, form: 0, ph: "ship", act: n => { if (n === "transform" && out.form > .99) return; if (n === "dodge") out.dside = -(out.dside || 1); mv.play(n); },')
rep("const arcM = new TH.Mesh(", "const thr = [-1, 1].map(sx => { const s = sprite(3, \"rgba(150,210,255,1)\", \"aex_fl\"); s.position.set(sx * 3.6, 4.5, -3.4); chest.add(s); s.material.opacity = 0; return s; }); const arcM = new TH.Mesh(")
rep("const st0 = ss(.92, 1, u), g0 = t * .001; let gd = 0;",
    "const st0 = ss(.92, 1, u), g0 = t * .001; let gd = 0; const fdg = f(\"dodge\", t), fst = f(\"stagger\", t), fsb = f(\"sbreak\", t), fwb = f(\"wbreak\", t), stg = fst >= 0 ? bell(fst, 0, .08, .4, 1) : 0;")
rep("        if (fb >= 0) { const back = bell(fb, 0, .18, .3, .42)", "        if (fb >= 0 && !out.swordGone) { const back = bell(fb, 0, .18, .3, .42)")
rep("gd = Math.max(.85, bell(fa, 0, .12, .8, 1), od * .85) * st0;", "gd = Math.max(.85, bell(fa, 0, .12, .8, 1), od * .85) * st0 * (1 - stg * .7) * (out.shieldGone && !(fsb >= 0 && fsb < .55) ? 0 : 1);")
rep("arcM.visible = fb >= 0 && u > .99;", "arcM.visible = fb >= 0 && u > .99 && !out.swordGone;")
# the centre beam: much bigger, with a long charge in the reactor first
rep("m.scale.set(1 + Math.sin(t * .05) * .05, 1 + Math.sin(t * .06) * .05, ss(.3, .4, fl));", "m.scale.set(2.6 * (1 + Math.sin(t * .05) * .07), 2.6 * (1 + Math.sin(t * .06) * .07), 3.2 * ss(.3, .38, fl));")
# dodges, staggers and the losses, before the hit kit runs
rep("      hit(bell(fx, 0, .05, .4, 1) + od * .15, t);",
"""      let xh = 0, xb = 0;
      if (fdg >= 0 && st0 > 0) { const k = bell(fdg, 0, .12, .5, 1), side = out.dside || 1, kick = bell(fdg, 0, .03, .18, .45); body.position.x += side * 12 * k; body.position.y += 1.5 * k; root.rotation.z += -side * .32 * k; chest.rotation.z += -side * .14 * k; head.rotation.y += side * .3 * k;
        thr.forEach(s => { s.material.opacity = Math.min(1, kick * 1.4 + k * .25); s.scale.setScalar(3 + kick * 10); }); legs.forEach(L => L.fl.forEach(s => { s.material.opacity = Math.min(1, s.material.opacity + kick); s.scale.setScalar(s.scale.x + kick * 7); })); } else thr.forEach(s => { s.material.opacity = 0; });
      if (stg > 0) { body.position.z -= 5 * stg; body.position.y -= 1.2 * stg; chest.rotation.x -= .55 * stg; head.rotation.x -= .45 * stg; root.rotation.x -= .15 * stg; arms.forEach(A => { A.sh.rotation.x += .5 * stg; A.sh.rotation.z += A.sx * .45 * stg; }); xh = Math.max(xh, stg * .9); xb += stg * 6; }
      if (fsb >= 0) { const pop = ss(.45, .7, fsb); shield.visible = fsb < .72; hexM.uniforms.uO.value = (rnd() < .5 ? 1.5 : .15) * (1 - pop) + pop * (1 - pop) * 4; shield.scale.multiplyScalar(1 + pop * .9); xh = Math.max(xh, bell(fsb, .38, .46, .6, .9)); xb += (1 - pop) * 8; }
      else shield.visible = !out.shieldGone;
      if (fwb >= 0) { const k = ss(.45, 1, fwb); blade.scale.y *= (rnd() < .4 ? .25 : 1) * (1 - ss(.35, .5, fwb)); sword.visible = fwb < .97; sword.position.set(k * 9, -1.6 - k * 24, .2 + k * 11); sword.rotation.z = k * 13; xh = Math.max(xh, bell(fwb, .3, .4, .55, .8)); xb += 6 * (1 - k); }
      else if (out.swordGone) { sword.visible = false; bladeS.material.opacity = 0; } else { sword.visible = true; sword.position.set(0, -1.6, .2); sword.rotation.z = 0; }
      hit(Math.max(bell(fx, 0, .05, .4, 1) + od * .15, xh), t); if (xb) bt(t, xb);""")
# the preview encounter, phase 3: a duel, then the losses, then the last stand and the centre beam
rep('for (const [at, mv, kn, near] of [[50, "aegis", 0], [54, "blade", 7, 1], [59, "missiles", 6], [63.5, "lance", 0], [68, "blade", 6, 1]]) if (s > at && !X["w" + at]) { X["w" + at] = 1; b.act(mv);',
    'for (const [at, mv, kn, near] of [[49.5, "dodge", 0], [51.2, "blade", 7, 1], [54, "dodge", 0], [55.6, "aegis", 0], [58.6, "missiles", 6], [62.2, "dodge", 0], [63.6, "stagger", 0], [64.9, "sbreak", 0], [67.4, "stagger", 0], [68.6, "wbreak", 0], [71, "missiles", 5], [80.2, "lance", 0]]) if (s > at && !X["w" + at]) { X["w" + at] = 1; b.act(mv); if (mv === "sbreak") b.shieldGone = 1; if (mv === "wbreak") b.swordGone = 1;')
rep("if (s > 63.5 && s < 66.5 && b.reactor) { const o = b.reactor.getWorldPosition(X.V).clone(), d = X.F.clone(); sbBeamKill(X, o, d, 3.5 * sc, 70 * sc, t); }",
    "if (s > 81.2 && s < 83.4 && b.reactor) { const o = b.reactor.getWorldPosition(X.V).clone(), d = X.F.clone(); sbBeamKill(X, o, d, 9 * sc, 190 * sc, t); X.quiet = 1; }")
rep("const od = (s - 72) / 10; if (od >= 0 && od < 1) {", "const od = (s - 72) / 8; if (od >= 0 && od < 1) {")
C1 = "Direct hit! It's staggering... its shield is breaking!"; C2 = "Its blade is gone! Keep up the pressure!"; C3 = "Its core is charging... it's going to fire! Brace yourselves!"
rep('if (s > 72) say("a5", "Reactor Overdrive! Its core is exposed. Everything we have, now!");',
    'if (s > 64) say("a4b", "%s"); if (s > 68.7) say("a4c", "%s"); if (s > 72) say("a5", "Reactor Overdrive! Its core is exposed. Everything we have, now!"); if (s > 79.6) say("a5b", "%s");' % (C1, C2, C3))
# live: the shield breaks when it falls to 45%, the sword at 30%, the beam joins the rotation; every player sees a break they are there for
rep("const L = xf ? SBW.aex.mv2 : SBW.aex.mv;", "const L = (xf ? SBW.aex.mv2 : SBW.aex.mv).filter(n => !(b.shieldGone && n === \"aegis\") && !(b.swordGone && n === \"blade\"));")
rep('mv2: ["aegis", "blade", "missiles", "lance", "blade", "missiles", "aegis"]', 'mv2: ["dodge", "blade", "dodge", "aegis", "missiles", "dodge", "blade", "missiles", "lance"]')
rep("else { const xf = aexXf(st); b.drive(\"transform\"",
    "else { const xf = aexXf(st); { const sg = xf && st.hp && st.hp <= 45 ? 1 : 0, wg = xf && st.hp && st.hp <= 30 ? 1 : 0; if (X.sgP != null && sg && !X.sgP) { b.act(\"sbreak\"); say(k + s0 + \"sb\", \"%s\"); } if (X.wgP != null && wg && !X.wgP) { b.act(\"wbreak\"); say(k + s0 + \"wb\", \"%s\"); } X.sgP = sg; X.wgP = wg; b.shieldGone = sg || (dead ? 1 : 0); b.swordGone = wg; } b.drive(\"transform\"" % (C1, C2))
# they come back stronger: from their second appearance on, the warnings and arrival say so (and they are drawn a little larger)
R = {"vaeA": "They're back... Vaelthar has returned, and its energy readings are even stronger than before!",
     "aexA": "It's back... Aexion has returned, and it's even stronger than before. All fleets, battle stations!",
     "vaeS": "Long-range sensors have found Vaelthar's signature again. It's coming back stronger, within three days.",
     "aexS": "Aexion's signature is back on our scanners, stronger than before. It arrives within three days."}
rep('if (e < 600) say(k + s0 + "a", k === "vae" ? "WARNING: a celestial anomaly is tearing open beyond the Rim. Vaelthar has arrived!" : "WARNING: a dreadnought-class signature is dropping out of warp. Aexion has arrived!");',
    'const back = s0 > SBW[k].first + 864e5; if (e < 600) say(k + s0 + "a", back ? (k === "vae" ? "%s" : "%s") : k === "vae" ? "WARNING: a celestial anomaly is tearing open beyond the Rim. Vaelthar has arrived!" : "WARNING: a dreadnought-class signature is dropping out of warp. Aexion has arrived!");' % (R["vaeA"], R["aexA"]))
rep("let scl = D.sc * Math.max(.001, 1 - Math.pow(1 - arr, 3)); const dead = st.dead && st.dead < T, df = dead ? (T - st.dead) / 1000 : 0;",
    "let scl = D.sc * (back ? 1.08 : 1) * Math.max(.001, 1 - Math.pow(1 - arr, 3)); const dead = st.dead && st.dead < T, df = dead ? (T - st.dead) / 1000 : 0;")
rep('annOnce("sb" + k2, nx, SB_SOON[k2])', 'annOnce("sb" + k2, nx, nx > SBW[k2].first + 864e5 ? (k2 === "vae" ? "%s" : "%s") : SB_SOON[k2])' % (R["vaeS"], R["aexS"]))
GL = r"""/* v462 what a fallen super boss leaves behind: a holographic glyph hanging where it died, its rings turning, crackling with elemental
   lightning (fire, frost, storm, void and life in turn), in that boss's colours. e = seconds since it formed. */
function sbGlyph(W, X, e, t) { if (e < 0) { if (X.gly) X.gly.g.visible = false; return; }
  if (!X.gly) { const cv = document.createElement("canvas"); cv.width = cv.height = 512; const c = cv.getContext("2d"), r = cwRnd(hash(X.key + "glyph")); c.translate(256, 256); c.strokeStyle = "#fff"; c.fillStyle = "#fff"; c.lineCap = "round";
    const ring = (R, w) => { c.lineWidth = w; c.beginPath(); c.arc(0, 0, R, 0, TAU); c.stroke(); }; ring(246, 6); ring(232, 2); ring(168, 4); ring(150, 1.5); ring(60, 3);
    for (let k = 0; k < 72; k++) { const a = k / 72 * TAU, l = k % 6 ? 8 : 18; c.lineWidth = k % 6 ? 1.5 : 3; c.beginPath(); c.moveTo(Math.cos(a) * 232, Math.sin(a) * 232); c.lineTo(Math.cos(a) * (232 - l), Math.sin(a) * (232 - l)); c.stroke(); }
    for (let k = 0; k < 12; k++) { c.save(); c.rotate(k / 12 * TAU); c.translate(0, -196); c.lineWidth = 3; c.beginPath(); for (let j = 0; j < 4; j++) { const x0 = (r() - .5) * 26, y0 = (r() - .5) * 30, x1 = (r() - .5) * 26, y1 = (r() - .5) * 30; c.moveTo(x0, y0); c.lineTo(x1, y1); } c.stroke(); c.restore(); }
    c.lineWidth = 4; c.beginPath(); for (let k = 0; k <= 7; k++) { const a = k * 3 / 7 * TAU - Math.PI / 2; k ? c.lineTo(Math.cos(a) * 150, Math.sin(a) * 150) : c.moveTo(Math.cos(a) * 150, Math.sin(a) * 150); } c.stroke(); c.beginPath(); c.arc(0, 0, 22, 0, TAU); c.fill();
    const tex = new TH.CanvasTexture(cv), vae = X.key === "vae", C1 = vae ? 0xc890ff : 0x7ac8ff, C2 = vae ? 0xffd890 : 0xd0f0ff, g = new TH.Group(); g.position.copy(X.B).add(new TH.Vector3(0, 45, 0)); X.grp.add(g);
    const mk = (sz, col, op) => { const m = new TH.Mesh(new TH.PlaneGeometry(sz, sz), new TH.MeshBasicMaterial({ map: tex, color: col, transparent: true, opacity: op, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false })); m.frustumCulled = false; m.userData.o = op; g.add(m); return m; };
    const A = mk(150, C1, .95), B = mk(240, C2, .55), Cc = mk(95, 0xffffff, .8); B.rotation.x = -Math.PI / 2;
    const NA = 14, SEG = 7, lg = new TH.BufferGeometry(); lg.setAttribute("position", new TH.BufferAttribute(new Float32Array(NA * SEG * 6), 3)); lg.setAttribute("color", new TH.BufferAttribute(new Float32Array(NA * SEG * 6), 3));
    const arcs = new TH.LineSegments(lg, new TH.LineBasicMaterial({ vertexColors: true, transparent: true, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); arcs.frustumCulled = false; g.add(arcs);
    const glow = new TH.Sprite(W.additive(W.glow.wh || (W.glow.wh = glowTex("255,255,255", .85)), new TH.Color(C1), .5)); glow.scale.setScalar(380); g.add(glow);
    X.gly = { g, A, B, Cc, arcs, glow, NA, SEG, lt: 0 }; }
  const Z = X.gly, k = Math.min(1, e / 1.4), pk = 1 - Math.pow(1 - k, 3); Z.g.visible = true; Z.g.scale.setScalar(.2 + pk * .8);
  Z.A.rotation.set(0, t * .0004, 0); Z.B.rotation.z = t * .00018; if (W.camera) Z.Cc.quaternion.copy(W.camera.quaternion); Z.Cc.rotateZ(-t * .0006);
  const fl = .85 + .15 * Math.sin(t * .013) * Math.sin(t * .0031); for (const m of [Z.A, Z.B, Z.Cc]) m.material.opacity = m.userData.o * k * fl; Z.glow.material.opacity = .35 * k * (.8 + .2 * Math.sin(t * .004)); Z.g.position.y = X.B.y + 45 + Math.sin(t * .0007) * 5;
  if (t - Z.lt > 70) { Z.lt = t; const EL = [[1, .5, .15], [.55, .9, 1], [1, 1, .45], [.8, .45, 1], [.45, 1, .55]], P = Z.arcs.geometry.attributes.position.array, Cl = Z.arcs.geometry.attributes.color.array, el = EL[Math.floor(t / 1800) % 5];
    for (let i = 0; i < Z.NA; i++) { const on = Math.random() < .75, a = Math.random() * TAU, b = (Math.random() - .5) * 1.2, r0 = 20 + Math.random() * 30, r1 = 90 + Math.random() * 60, cc = Math.random() < .3 ? EL[(Math.random() * 5) | 0] : el; let px = 0, py = 0, pz = 0;
      for (let j = 0; j < Z.SEG; j++) { const u0 = j / Z.SEG, u1 = (j + 1) / Z.SEG, R0 = r0 + (r1 - r0) * u0, R1 = r0 + (r1 - r0) * u1, jit = 12 * (1 - u1 * .5), o = (i * Z.SEG + j) * 6;
        const x0 = j ? px : Math.cos(a) * Math.cos(b) * R0, y0 = j ? py : Math.sin(b) * R0, z0 = j ? pz : Math.sin(a) * Math.cos(b) * R0; px = Math.cos(a) * Math.cos(b) * R1 + (Math.random() - .5) * jit; py = Math.sin(b) * R1 + (Math.random() - .5) * jit; pz = Math.sin(a) * Math.cos(b) * R1 + (Math.random() - .5) * jit;
        P.set(on ? [x0, y0, z0, px, py, pz] : [0, 0, 0, 0, 0, 0], o); const f = k * (1 - u0 * .6); Cl.set([cc[0] * f, cc[1] * f, cc[2] * f, cc[0] * f * .8, cc[1] * f * .8, cc[2] * f * .8], o); } }
    Z.arcs.geometry.attributes.position.needsUpdate = true; Z.arcs.geometry.attributes.color.needsUpdate = true; } }
"""
rep("function sbBoomTick(X, t) {", GL + "function sbBoomTick(X, t) {")
i = s.index("if (X.fall && !X.relic && s > X.fall + 9.5) {"); j = s.index("X.grp.add(X.relic); }", i) + len("X.grp.add(X.relic); }"); s = s[:i] + "if (X.fall) sbGlyph(W, X, s - X.fall - 8.6, t);" + s[j:]
rep("if (X.relic) { X.relic.rotation.set(t * .0002, t * .0003, t * .0001); }", "")
rep("if (X.fall) { const be = s - X.fall - 2;", "if (X.fall) { const be = s - X.fall - 2; sbGlyph(W, X, be - 10.5, t);")
rep("if (dead) { const be = df - 2;", "if (dead) { const be = df - 2; sbGlyph(W, X, be - 10.5, t);")
rep('let vf = -1; if (k === "vae" && dead) { vf = df - .8;', 'let vf = -1; if (k === "vae" && dead) { vf = df - .8; sbGlyph(W, X, df - 8.6, t);')
F1 = "Vaelthar has fallen! The wheel collapses... and a holo glyph crackles where it died."
rep("Vaelthar has fallen! The wheel collapses. A celestial relic drifts where it died.", F1, 2)
s = re.sub(r"GAME_V = 461\b", "GAME_V = 462", s)
open(P, 'w').write(s)
