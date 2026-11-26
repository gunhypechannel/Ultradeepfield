"""v780: Vaelthar's wheel attacks (owner approved: "build it all"). Five new attacks built round the celestial wheel on his back, each
a 3D move on the model and a strike drawn across the fleet in battle:
- Wheel Throw: the gold outer ring tears free, spins out through the fleet like a saw and swings back to lock on.
- Orrery Lock: the inner rings spin faster and faster until their runes align with a click; a gold rune pattern flies out over the
  fleet, freezes every ship inside it, then shatters.
- Eclipse Gate: the wheel's heart opens into a black gate that drags the fleet's light in, then bursts everything back out.
- Stabilizer Lances: the six stabilizer nodes fly out round the fleet and fire beams that cross in a six-pointed star.
- Falling Sun: he lifts the wheel high overhead and brings it down on the fleet in a ring of golden fire.
His fight now cycles Starfall (the meteor shower), Wheel Throw, Celestial Judgment, Orrery Lock, Starfall, Stabilizer Lances,
Eclipse Gate, Falling Sun, with the Divine wheel beam still his signature. Applies on top of v779."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 779;", "const GAME_V = 780;")
rep("const mv = moves({ claw: 1500, wing: 2400, judge: 3200, seal: 3600, rebirth: 3400, annihilate: 18000, hit: 520 })",
    "const mv = moves({ claw: 1500, wing: 2400, judge: 3200, seal: 3600, rebirth: 3400, annihilate: 18000, hit: 520, throw: 3400, orrery: 3600, gate: 3800, lances: 3400, sun: 3600 })")
rep('moves: ["claw", "wing", "judge", "seal", "rebirth", "annihilate"] };', 'moves: ["claw", "wing", "judge", "seal", "rebirth", "annihilate", "throw", "orrery", "gate", "lances", "sun"] };')
W3 = r'''
    { /* v780 the wheel's own attacks: Wheel Throw, Orrery Lock, Eclipse Gate, Stabilizer Lances, Falling Sun */
      const Yv = V(0, 1, 0), lockC = runeShader(WR * 1.3, GOLD, 0); lockC.visible = false; wheel.add(lockC);
      const gateD = new TH.Mesh(new TH.CircleGeometry(WR * .26, 48), new TH.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0, depthWrite: false, side: TH.DoubleSide })); gateD.position.z = .45; gateD.userData.dyn = 1; wheel.add(gateD);
      const gateR = new TH.Mesh(new TH.TorusGeometry(WR * .27, .28, 6, 64), glowMat(0xffd890, 1)); gateR.position.z = .55; gateR.userData.dyn = 1; gateR.visible = false; wheel.add(gateR);
      const flash = sprite(30, "rgba(255,240,210,1)", "vae_flash"); flash.material.opacity = 0; flash.position.z = 2; wheel.add(flash);
      const thrT = sprite(18, "rgba(255,210,120,1)", "vae_thr"); thrT.material.opacity = 0; R0.r.add(thrT);
      const lanceB = stabs.map(() => { const g = new TH.Group(); for (const [r, o, c] of [[.9, .3, 0xc890ff], [.3, 1, 0xffffff]]) { const geo = new TH.CylinderGeometry(r, r, 1, 8, 1, true); geo.translate(0, .5, 0); const m = new TH.Mesh(geo, glowMat(c, o)); m.userData.dyn = 1; m.userData.o = o; g.add(m); } g.visible = false; wheel.add(g); return g; });
      const shock = new TH.Mesh(new TH.RingGeometry(.9, 1, 96), glowMat(0xffc860, 1)); shock.userData.dyn = 1; shock.visible = false; shock.rotation.x = -Math.PI / 2; body.add(shock);
      const shock2 = sprite(40, "rgba(255,220,140,1)", "vae_sunf"); shock2.material.opacity = 0; body.add(shock2);
      const stab0 = stabs.map(s0 => s0.n.position.clone()), tick0 = out.tick;
      out.tick = t => { tick0(t); const ft = f("throw", t), fo = f("orrery", t), fg = f("gate", t), fl = f("lances", t), fu = f("sun", t);
        // Wheel Throw: the outer ring flies out and swings back
        if (ft >= 0 && ft < 1) { const go = ss(.12, .5, ft) * (1 - ss(.55, .92, ft)); R0.r.position.set(Math.sin(go * Math.PI) * 9 * (ft < .55 ? 1 : -1), -go * 7, go * 64); R0.r.rotation.z += ft * 48; thrT.material.opacity = go * .9; R0.ch.material.opacity = Math.max(R0.ch.material.opacity, go); }
        else { R0.r.position.set(0, 0, 0); thrT.material.opacity = 0; }
        // Orrery Lock: the inner rings wind up, click into line, and throw a gold rune pattern over the fleet that shatters
        if (fo >= 0 && fo < 1) { const sp = ss(0, .5, fo), lk = ss(.5, .56, fo); ringsW.forEach((o, k) => { if (!k) return; o.r.rotation.z += (k % 2 ? -1 : 1) * sp * sp * 16 * (1 - lk); o.rr.forEach(r => { r.material.uniforms.uSw.value = 1.04; r.material.uniforms.uHot.value = Math.max(r.material.uniforms.uHot.value, sp * 1.2 + lk); }); });
          const g = ss(.45, .6, fo), fly = ss(.6, .8, fo), br = ss(.82, .96, fo); lockC.visible = fo > .45; lockC.position.z = 2 + fly * 44; lockC.scale.setScalar(.5 + g * .4 + fly * .7 + br * .7); lockC.rotation.z = t * .002 * (1 - lk); lockC.material.uniforms.uSw.value = 1.04; lockC.material.uniforms.uO.value = .55 * g * (1 - br); lockC.material.uniforms.uHot.value = lk * .3 + br * .6; }
        else lockC.visible = false;
        // Eclipse Gate: the aperture opens black and wide, then bursts
        if (fg >= 0 && fg < 1) { const op = ss(.05, .35, fg) * (1 - ss(.72, .78, fg)), bu = bell(fg, .7, .74, .8, .95); gateD.material.opacity = op * .95; gateD.scale.setScalar(1 + op * 2); gateR.visible = op > .01; gateR.scale.setScalar(1 + op * 2); gateR.material.opacity = op; ap.scale.setScalar(1 + op * 2); field.material.opacity = Math.max(field.material.opacity, op * .7); flash.material.opacity = bu; flash.scale.setScalar(30 + bu * 70); apS.scale.setScalar(apS.scale.x * (1 + op)); }
        else { gateD.material.opacity = 0; gateR.visible = false; ap.scale.setScalar(1); flash.material.opacity = 0; }
        // Stabilizer Lances: the six nodes fly out and forward, then fire beams that cross in a six-pointed star
        if (fl >= 0 && fl < 1) { const go = ss(.05, .35, fl) * (1 - ss(.86, 1, fl)), fi = bell(fl, .4, .48, .78, .86); stabs.forEach((s0, k) => { const R = WR + .3 + go * 15; s0.n.position.set(Math.sin(s0.a) * R, Math.cos(s0.a) * R, go * 28); });
          lanceB.forEach((g, k) => { const on = fi > .01 && out.stab[k] && out.stab[(k + 2) % 6]; g.visible = !!on; if (!on) return; const A = stabs[k].n.position, B = stabs[(k + 2) % 6].n.position; tmpV.subVectors(B, A); const L = tmpV.length(); R0.r.updateMatrix(); g.position.copy(A).applyMatrix4(R0.r.matrix); tmpV2.copy(B).applyMatrix4(R0.r.matrix).sub(g.position); g.quaternion.setFromUnitVectors(Yv, tmpV2.clone().normalize()); g.scale.set(1 + fi * .4, tmpV2.length(), 1 + fi * .4); g.children.forEach(m => { m.material.opacity = m.userData.o * fi * (.85 + rnd() * .15); }); }); }
        else { stabs.forEach((s0, k) => s0.n.position.copy(stab0[k])); lanceB.forEach(g => { g.visible = false; }); }
        // Falling Sun: the wheel rises overhead, then slams down ahead of him in a ring of golden fire
        if (fu >= 0 && fu < 1) { const up = ss(.05, .38, fu) * (1 - ss(.42, .5, fu)), dn = ss(.42, .52, fu) * (1 - ss(.8, 1, fu)), imp = (fu - .52) / .4; wheel.position.set(0, 14.5 + up * 18 - dn * 22, -14 + dn * 36); wheel.rotation.x = -dn * 1.35 - up * .3; wheel.scale.setScalar(1 + up * .15);
          shock.visible = imp > 0 && imp < 1; if (shock.visible) { shock.position.set(0, -7, 22); shock.scale.setScalar(3 + imp * 70); shock.material.opacity = .9 * (1 - imp); } shock2.position.set(0, -6, 22); shock2.material.opacity = imp > 0 && imp < .3 ? .55 * (1 - imp / .3) : 0; shock2.scale.setScalar(30 + Math.max(0, imp) * 60); }
        else { shock.visible = false; shock2.material.opacity = 0; wheel.scale.setScalar(1); } }; }
'''
rep("      hit(bell(fx, 0, .05, .4, 1), t); };\n    out.tick = tick; tick(0); bake(body); return out; }",
    "      hit(bell(fx, 0, .05, .4, 1), t); };\n    out.tick = tick; tick(0); bake(body);" + W3 + "    return out; }")
# the fight: new attacks, their timing, the model's moves, their strikes across the fleet
rep('vae: { rain: "wing", halo: "judge", wheel: "seal" }', 'vae: { rain: "wing", halo: "judge", wheel: "seal", throw: "throw", orrery: "orrery", gate: "gate", lances: "lances", sun: "sun" }')
rep('vae: { col: "255,210,122", seq: ["rain", "halo"], sig: "wheel" }', 'vae: { col: "255,210,122", seq: ["rain", "throw", "halo", "orrery", "rain", "lances", "gate", "sun"], sig: "wheel" }')
rep("rain: 1.8, halo: 1.5, wheel: 2.6,", "rain: 1.8, halo: 1.5, wheel: 2.6, throw: 2.2, orrery: 2.4, gate: 2.4, lances: 2.2, sun: 2.4,")
rep("else if (/rain|shards|crush|wave/.test(m.a))", "else if (/rain|shards|crush|wave|throw|orrery|gate|lances|sun/.test(m.a))")
D2 = r'''    else if (m.a === "throw") { /* v780 Wheel Throw: a spinning gold ring out through the fleet and back */ const tgt = fx.length ? fx.reduce((a, p) => Math.hypot(p.x - cx, p.y - cy) > Math.hypot(a.x - cx, a.y - cy) ? p : a, fx[0]) : { x: mx, y: my }, k2 = clamp((u - .12) / .8, 0, 1), go = Math.sin(Math.PI * k2), sd = m.seed % 2 ? 1 : -1;
      const px = cx + (tgt.x - cx) * go * 1.15 + sd * Math.sin(Math.PI * k2 * 2) * W * .08, py = cy + (tgt.y - cy) * go * 1.15, rr = 26 * d, rot = t * .02;
      if (k2 > 0 && k2 < 1) { for (const [lw, al, c2] of [[14, .25, C(1)], [4, .95, "#ffe6a8"]]) { ctx.globalAlpha = al; ctx.strokeStyle = c2; ctx.lineWidth = lw * d; ctx.beginPath(); ctx.arc(px, py, rr, 0, TAU); ctx.stroke(); }
        ctx.globalAlpha = .9; ctx.strokeStyle = "#ffd070"; ctx.lineWidth = 2.5 * d; ctx.beginPath(); for (let q = 0; q < 12; q++) { const a = rot + q / 12 * TAU; ctx.moveTo(px + Math.cos(a) * rr, py + Math.sin(a) * rr); ctx.lineTo(px + Math.cos(a + .18) * rr * 1.35, py + Math.sin(a + .18) * rr * 1.35); } ctx.stroke();
        ctx.globalAlpha = .6; ctx.drawImage(gl, px - rr * 1.6, py - rr * 1.6, rr * 3.2, rr * 3.2); sweepHit(p => Math.hypot(p.x - px, p.y - py) < rr * 1.8, 1.4); } }
    else if (m.a === "orrery") { /* v780 Orrery Lock: rings over the fleet spin, lock, freeze the ships inside, then shatter */ const Rr = Math.max(R * .55, 90 * d), sp = clamp(u / .55, 0, 1), lk = u > .55, br = clamp((u - .82) / .18, 0, 1);
      if (br < 1) { [1, .72, .46].forEach((q, i) => { const rot = lk ? 0 : (i % 2 ? -1 : 1) * sp * sp * 9; ctx.globalAlpha = Math.min(1, u * 5) * (1 - br); ctx.strokeStyle = i === 1 ? C(1) : "#ffd070"; ctx.lineWidth = (lk ? 4 : 2.5) * d; ctx.beginPath(); ctx.arc(mx, my, Rr * q * (1 + br * .5), 0, TAU); ctx.stroke();
          ctx.beginPath(); for (let k = 0; k < 12; k++) { const a = rot + k / 12 * TAU; ctx.moveTo(mx + Math.cos(a) * Rr * q * .93, my + Math.sin(a) * Rr * q * .93); ctx.lineTo(mx + Math.cos(a) * Rr * q * 1.07, my + Math.sin(a) * Rr * q * 1.07); } ctx.stroke(); });
        if (lk) { once("lock", () => big(6)); ctx.globalAlpha = .8 * (1 - br); ctx.strokeStyle = "#ffe6a8"; ctx.lineWidth = 2 * d; ctx.beginPath(); for (let k = 0; k < 6; k++) { const a = k / 6 * TAU, b2 = (k + 2) / 6 * TAU; ctx.moveTo(mx + Math.cos(a) * Rr, my + Math.sin(a) * Rr); ctx.lineTo(mx + Math.cos(b2) * Rr, my + Math.sin(b2) * Rr); } ctx.stroke();
          fx.forEach(p => { if (Math.hypot(p.x - mx, p.y - my) > Rr) return; ctx.globalAlpha = .9 * (1 - br); ctx.beginPath(); for (let q = 0; q <= 6; q++) { const aa = q * Math.PI / 3; ctx[q ? "lineTo" : "moveTo"](p.x + Math.cos(aa) * 9 * d, p.y + Math.sin(aa) * 9 * d); } ctx.stroke(); }); } }
      if (br > 0) { once("bang", () => big(12)); sweepHit(p => Math.hypot(p.x - mx, p.y - my) < Rr, 1.5); } }
    else if (m.a === "gate") { /* v780 Eclipse Gate: a black gate opens at the wheel and drags the fleet's light in, then bursts */ const op = clamp(u / .35, 0, 1), rg = B.aw * .22 * (.3 + op * .7);
      if (u < .72) { ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = .85 * op; ctx.fillStyle = "#000"; ctx.beginPath(); ctx.arc(cx, cy, rg, 0, TAU); ctx.fill(); ctx.globalCompositeOperation = "lighter"; ctx.globalAlpha = op; ctx.strokeStyle = "#ffd890"; ctx.lineWidth = 4 * d; ctx.stroke();
        fx.forEach((p, j) => { const q = (t * .0012 + j * .137) % 1, sx2 = p.x + (cx - p.x) * q, sy2 = p.y + (cy - p.y) * q; ctx.globalAlpha = .6 * op * (1 - q); ctx.strokeStyle = C(1); ctx.lineWidth = 2 * d; ctx.beginPath(); ctx.moveTo(sx2, sy2); ctx.lineTo(sx2 + (cx - p.x) * .08, sy2 + (cy - p.y) * .08); ctx.stroke(); }); }
      else { const k2 = clamp((u - .72) / .28, 0, 1), rr = R * 1.4 * k2; once("bang", () => big(18)); ctx.globalAlpha = 1 - k2; for (const [lw, c2] of [[30, C(.4)], [8, C(1)], [2.5, "#ffffff"]]) { ctx.strokeStyle = c2; ctx.lineWidth = lw * d; ctx.beginPath(); ctx.arc(cx, cy, rr, 0, TAU); ctx.stroke(); }
        if (k2 < .3) { ctx.globalAlpha = 1 - k2 / .3; const r2 = B.aw * .4; ctx.drawImage(wh, cx - r2, cy - r2, r2 * 2, r2 * 2); } sweepHit(p => Math.hypot(p.x - cx, p.y - cy) < rr, 1.6); } }
    else if (m.a === "lances") { /* v780 Stabilizer Lances: six nodes round the fleet fire beams that cross in a star */ const Rr = Math.max(R * .6, 110 * d), go = clamp(u / .3, 0, 1), pts = []; for (let k = 0; k < 6; k++) { const a = k / 6 * TAU + Math.PI / 6, tx = mx + Math.cos(a) * Rr, ty = my + Math.sin(a) * Rr * .7; pts.push([cx + (tx - cx) * go, cy + (ty - cy) * go]); }
      pts.forEach(([x, y]) => { ctx.globalAlpha = .9 * (u > .9 ? (1 - u) / .1 : 1); ctx.drawImage(gl, x - 14 * d, y - 14 * d, 28 * d, 28 * d); ctx.drawImage(wh, x - 5 * d, y - 5 * d, 10 * d, 10 * d); });
      if (u > .42 && u < .9) { const fa = u > .82 ? (.9 - u) / .08 : 1; once("bang", () => big(12)); for (let k = 0; k < 6; k++) { const A = pts[k], P2 = pts[(k + 2) % 6]; for (const [lw, al, c2] of [[16, .3, C(1)], [4, .95, "#ffffff"]]) { ctx.globalAlpha = al * fa; ctx.strokeStyle = c2; ctx.lineWidth = lw * d; ctx.beginPath(); ctx.moveTo(A[0], A[1]); ctx.lineTo(P2[0], P2[1]); ctx.stroke(); } }
        sweepHit(p => Math.hypot((p.x - mx) / Rr, (p.y - my) / (Rr * .7)) < 1, 1.5); } }
    else if (m.a === "sun") { /* v780 Falling Sun: the wheel rises over him, then falls on the fleet in a ring of golden fire */ const rs = B.aw * .16, up = clamp(u / .4, 0, 1), dn = clamp((u - .42) / .12, 0, 1), sx2 = cx + (mx - cx) * dn, sy2 = (cy - H * .25 * up) + (my - (cy - H * .25)) * dn;
      if (u < .56) { ctx.globalAlpha = .9; ctx.drawImage(gl, sx2 - rs * 1.8, sy2 - rs * 1.8, rs * 3.6, rs * 3.6); ctx.strokeStyle = "#ffd070"; ctx.lineWidth = 5 * d; ctx.beginPath(); ctx.arc(sx2, sy2, rs, 0, TAU); ctx.stroke(); ctx.drawImage(wh, sx2 - rs * .6, sy2 - rs * .6, rs * 1.2, rs * 1.2); }
      else { const k2 = clamp((u - .54) / .46, 0, 1), rr = R * 1.5 * k2; once("bang", () => big(20)); ctx.globalAlpha = 1 - k2; for (const [lw, c2] of [[34, "rgba(255,200,90,.35)"], [9, "rgba(255,215,120,1)"], [3, "#ffffff"]]) { ctx.strokeStyle = c2; ctx.lineWidth = lw * d; ctx.beginPath(); ctx.ellipse(mx, my, rr, rr * .55, 0, 0, TAU); ctx.stroke(); }
        if (k2 < .25) { ctx.globalAlpha = 1 - k2 / .25; const r2 = rs * 3; ctx.drawImage(wh, mx - r2, my - r2, r2 * 2, r2 * 2); } sweepHit(p => Math.hypot(p.x - mx, (p.y - my) / .55) < rr, 1.7); } }
    else if (m.a === "tractor") {'''
rep('    else if (m.a === "tractor") {', D2)
rep('["Golden Seal", "Runic circles bind fleets inside the wheel\'s reach."],', '["Golden Seal", "Runic circles bind fleets inside the wheel\'s reach."], ["Wheel Throw", "The gold outer ring tears free and spins through the fleet like a saw, then swings back."], ["Orrery Lock", "The inner rings spin until their runes align, freezing every ship in the pattern before it shatters."], ["Eclipse Gate", "The wheel\'s heart opens into a black gate that drags ships in, then hurls everything back out."], ["Stabilizer Lances", "The six stabilizer nodes fly out round the fleet and fire beams that cross in a star."], ["Falling Sun", "He lifts the wheel overhead and brings it down on the fleet in a ring of golden fire."],')
open(p, "w", encoding="utf-8").write(s)
print("ok")
