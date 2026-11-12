# v482 (owner: "Super cubes attack animations should be 3 different, long hold green tractor beams, green burst energy weapons, and
# energy wave"). The Super Cube's battle-report model gets three attacks in place of the old three:
#   tractor: its front face opens and a wide green tractor beam locks on and holds for over three seconds, rings of light running back
#            down it toward the Cube as it pulls, the beam flickering and swelling;
#   burst:   four emitters on its front face fire three rapid volleys of green energy bolts down the line, each with a muzzle flash;
#   wave:    the core draws in light, then the Cube releases an energy wave: a green shell and a flat ring racing out, every light flaring.
# Its hex shield still flares when it is hit. The Omega Cube gets the same three, scaled to it, plus a cube storm (owner: "Maybe the same for
# omega cube except also add cube storm where cubes fly around it").
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
i = s.find('function superCube3D()'); j = s.find('r: 5, h: 6 }; }', i) + len('r: 5, h: 6 }; }'); assert i > 0 and j > i
s = s[:i] + r'''function superCube3D() { const grp = new TH.Group(), shk = new TH.Group(), body = new TH.Group(); grp.add(shk); shk.add(body); const S0 = 5, GRN = 0x5dff6a, F = S0 / 2;
  body.add(borgCube(S0, 3, 4242)); const glowM = (c, o) => new TH.MeshBasicMaterial({ color: c, transparent: true, opacity: o, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false, side: TH.DoubleSide });
  const ring = new TH.Mesh(new TH.TorusGeometry(S0 * .95, .05, 6, 72), glowM(GRN, .3)); ring.rotation.x = Math.PI / 2; body.add(ring);
  const sp = (c, sz, o) => { const m = new TH.Sprite(new TH.SpriteMaterial({ map: glowTex(c, .9), blending: TH.AdditiveBlending, depthWrite: false, transparent: true, opacity: o, toneMapped: false })); m.scale.setScalar(sz); return m; };
  const halo = sp("93,255,106", 15, .3); body.add(halo); const core = sp("200,255,210", 2.4, .9); core.position.set(0, 0, F + .05); body.add(core);
  const shM = new TH.ShaderMaterial({ uniforms: { uO: { value: 0 }, uT: { value: 0 } }, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, side: TH.DoubleSide, toneMapped: false,
    vertexShader: "varying vec3 vN; varying vec3 vV; varying vec3 vP; void main() { vec4 mv = modelViewMatrix * vec4(position, 1.); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); vP = position; gl_Position = projectionMatrix * mv; }",
    fragmentShader: "uniform float uO, uT; varying vec3 vN; varying vec3 vV; varying vec3 vP; void main() { float fr = pow(1. - abs(dot(vN, vV)), 2.); float hx = abs(sin(vP.x * 2.4 + uT) * sin(vP.y * 2.4) * sin(vP.z * 2.4 - uT)); float a = (fr * 1.2 + pow(hx, 6.) * .9 + .04) * uO; gl_FragColor = vec4(vec3(.36, 1., .45) * a, a); }" });
  const shield = new TH.Mesh(new TH.SphereGeometry(S0 * .98, 40, 28), shM); body.add(shield);
  // the tractor beam: a wide translucent cone, a bright core line, rings that run back toward the Cube
  const trac = new TH.Group(); trac.visible = false; trac.position.z = F; body.add(trac); const TL = 46;
  const cone = new TH.Mesh(new TH.CylinderGeometry(1.4, 4.2, TL, 28, 1, true).translate(0, TL / 2, 0).rotateX(Math.PI / 2), glowM(GRN, .22)); trac.add(cone);
  const cone2 = new TH.Mesh(new TH.CylinderGeometry(.9, 2.4, TL, 20, 1, true).translate(0, TL / 2, 0).rotateX(Math.PI / 2), glowM(0x9dffb0, .3)); trac.add(cone2);
  const tcore = new TH.Mesh(new TH.CylinderGeometry(.16, .3, TL, 10, 1, true).translate(0, TL / 2, 0).rotateX(Math.PI / 2), glowM(0xeaffea, .9)); trac.add(tcore);
  const trings = []; for (let k = 0; k < 7; k++) { const r = new TH.Mesh(new TH.TorusGeometry(1, .07, 6, 40), glowM(0xc8ffd0, .8)); trac.add(r); trings.push(r); }
  const tflare = sp("140,255,160", 7, 0); tflare.position.z = F + .2; body.add(tflare);
  // the burst emitters and their bolts
  const EM = [[-1.5, 1.5], [1.5, 1.5], [-1.5, -1.5], [1.5, -1.5]].map(([x, y]) => { const m = sp("170,255,180", 1.4, 0); m.position.set(x, y, F + .1); body.add(m); return m; });
  const NB = 12, bol = []; for (let i = 0; i < NB; i++) { const g = new TH.Group(); const h = sp("120,255,140", 2.4, 0), tl = new TH.Mesh(new TH.CylinderGeometry(.14, .04, 6, 6, 1, true).translate(0, -3, 0).rotateX(Math.PI / 2), glowM(0x9dffb0, 0)); g.add(h); g.add(tl); body.add(g); const e = i % 4, v = (i / 4) | 0; bol.push({ g, h, tl, e, d: v * .26 + e * .035, sx: (Math.random() - .5) * 3, sy: (Math.random() - .5) * 2.4 }); }
  // the energy wave
  const shell = new TH.Mesh(new TH.SphereGeometry(1, 32, 20), glowM(GRN, 0)); shell.visible = false; body.add(shell); const wring = new TH.Mesh(new TH.RingGeometry(.9, 1, 96), glowM(0xc8ffd0, 0)); wring.rotation.x = Math.PI / 2; wring.visible = false; body.add(wring);
  const D = { tractor: 3400, burst: 2600, wave: 2400, hit: 520 }, S = {}; const f = (n, t) => { const x = S[n]; if (!x) return -1; if (x.t0 < 0) x.t0 = t; const k = (t - x.t0) / D[n]; if (k >= 1) { delete S[n]; return -1; } return k; };
  const ss = (a, b, x) => { const u = Math.min(1, Math.max(0, (x - a) / (b - a))); return u * u * (3 - 2 * u); }, bell = (x, a, b, c, d) => x < 0 ? 0 : ss(a, b, x) * (1 - ss(c, d, x)); let hitT = -1e9;
  const tick = t => { const ft = f("tractor", t), fb = f("burst", t), fw = f("wave", t), fh = f("hit", t); if (fh >= 0 && fh < .1) hitT = t;
    const open = bell(ft, 0, .12, .9, 1), hold = bell(ft, .1, .18, .86, .97), gather = bell(fw, 0, .3, .34, .4), wv = fw < .34 ? -1 : (fw - .34) / .66, hh = Math.max(0, 1 - (t - hitT) / 500);
    body.rotation.y = Math.sin(t * .0004) * .05; body.rotation.x = Math.sin(t * .0003) * .04; shk.position.set((Math.random() - .5) * (hh * .15 + (wv > 0 && wv < .2 ? .25 : 0)), (Math.random() - .5) * hh * .15, 0);
    // tractor
    trac.visible = hold > .01; if (trac.visible) { const fl = .85 + .15 * Math.sin(t * .05) * Math.sin(t * .023); trac.scale.set(1 + hold * .15 + Math.sin(t * .006) * .05, 1 + hold * .15 + Math.sin(t * .006) * .05, Math.min(1, hold * 1.6)); cone.material.opacity = .2 * hold * fl; cone2.material.opacity = .3 * hold * fl; tcore.material.opacity = .9 * hold;
      trings.forEach((r, k) => { const u = 1 - ((t * .0006 + k / trings.length) % 1), z = u * TL; r.position.z = z; r.scale.setScalar(1.4 + 2.8 * u); r.material.opacity = .8 * hold * Math.sin(u * Math.PI); }); }
    tflare.material.opacity = Math.max(open * .9, hold); tflare.scale.setScalar(7 * (1 + hold * .5 + Math.sin(t * .02) * .08));
    // bursts
    EM.forEach((m, e) => { let fl = 0; for (let v = 0; v < 3; v++) { const k = fb < 0 ? -1 : (fb - v * .26 - e * .035) / .08; if (k > 0 && k < 1) fl = Math.max(fl, 1 - k); } m.material.opacity = fl; m.scale.setScalar(1.4 + fl * 3); });
    bol.forEach(B => { const k = fb < 0 ? -1 : (fb - B.d) / .3, on = k > 0 && k < 1, p = EM[B.e].position; B.h.material.opacity = on ? 1 - k * .5 : 0; B.tl.material.opacity = on ? .8 * (1 - k * .5) : 0; if (on) B.g.position.set(p.x + B.sx * k, p.y + B.sy * k, F + k * 44); });
    // the wave
    shell.visible = wv > 0 && wv < 1; wring.visible = shell.visible; if (shell.visible) { shell.scale.setScalar(S0 * .6 + wv * 20); shell.material.opacity = .14 * (1 - wv) * (1 - wv); wring.scale.setScalar(S0 + wv * 26); wring.material.opacity = .6 * (1 - wv); }
    const flare = gather + (wv > 0 && wv < .35 ? 1 - wv / .35 : 0);
    ring.rotation.z = t * (.0004 + gather * .004); ring.material.opacity = .25 + .15 * Math.sin(t * .003) + flare * .5; halo.material.opacity = .25 + flare * .6 + hold * .2; halo.scale.setScalar(15 * (1 + gather * .5 + flare * .3));
    core.material.opacity = .7 + Math.max(gather, hold) * .3; core.scale.setScalar(2.4 * (1 + gather * 2.6 + hold * .8));
    shM.uniforms.uT.value = t * .001; shM.uniforms.uO.value = .1 + hh * .6 + (wv > 0 && wv < .3 ? .6 * (1 - wv / .3) : 0); };
  return { grp, tick, act: n => { if (D[n]) S[n] = { t0: -1 }; }, moves: Object.keys(D), r: 5, h: 6 }; }''' + s[j:]
rep('WB_ATK.scb = ["disrupt", "beam", "shield"];', 'WB_ATK.scb = ["tractor", "burst", "wave"];')
s = re.sub(r"GAME_V = 481\b", "GAME_V = 482", s)
open(P, 'w').write(s)
# ---------------- the Omega Cube: the same three attacks, scaled to it, and a cube storm ----------------
# Its front face holds still now (no slow spin) so its attacks leave it toward the target it turned to.
#   storm: thirty of its cubes break out of the shell, whirl round it in a storm, and slot back in.
s = open(P).read()
i = s.find('function omega()'); j = s.find('r: 9, h: 12 }; }', i) + len('r: 9, h: 12 }; }'); assert i > 0 and j > i
s = s[:i] + r'''function omega() { const grp = new TH.Group(), shk = new TH.Group(), body = new TH.Group(); grp.add(shk); shk.add(body); const C = 2.4, GRN = 0x5dff7a, GRN2 = 0xc8ffd0, F = C * 2.5;
    const gt = (() => { const c = cv(128, 128), x = c.getContext("2d"); x.fillStyle = "#000"; x.fillRect(0, 0, 128, 128); x.strokeStyle = "#fff"; x.lineWidth = 6; x.strokeRect(3, 3, 122, 122); x.lineWidth = 2.5; x.globalAlpha = .55; for (const v of [43, 85]) { x.beginPath(); x.moveTo(v, 6); x.lineTo(v, 122); x.moveTo(6, v); x.lineTo(122, v); x.stroke(); } x.globalAlpha = .9; x.fillStyle = "#fff"; for (const [a, b2] of [[20, 20], [100, 64], [62, 104]]) x.fillRect(a, b2, 7, 7); const t2 = new TH.CanvasTexture(c); t2.encoding = TH.sRGBEncoding; t2.anisotropy = 4; return t2; })();
    const cubeM = new TH.MeshStandardMaterial({ color: 0x070d09, metalness: .7, roughness: .5, emissive: 0x3dff6a, emissiveMap: gt, emissiveIntensity: 1.6, envMapIntensity: .25 });
    const cells = []; for (let x = -2; x <= 2; x++) for (let y = -2; y <= 2; y++) for (let z = -2; z <= 2; z++) if (Math.max(Math.abs(x), Math.abs(y), Math.abs(z)) === 2) { const n = [0, 0, 0], ax = Math.abs(x) === 2 ? 0 : Math.abs(y) === 2 ? 1 : 2; n[ax] = [x, y, z][ax] > 0 ? 1 : -1; cells.push({ p: V(x * C, y * C, z * C), n: V(...n), ph: rnd() * TAU, sh: rnd() < .07, st: -1 }); }
    const NC = cells.length, box = new TH.BoxGeometry(C * .94, C * .94, C * .94), cubes = inst(box, cubeM, NC); body.add(cubes);
    const NS = 30, storm = inst(box, cubeM, NS); body.add(storm); const sD = []; { const pick = cells.map((c, i) => i).sort(() => rnd() - .5).slice(0, NS); pick.forEach((ci, k) => { cells[ci].st = k; sD.push({ ci, r: 11 + rnd() * 8, a: rnd() * TAU, y: (rnd() - .5) * 12, w: (.0016 + rnd() * .0014) * (rnd() < .5 ? 1 : -1), tl: V(rnd() - .5, rnd() - .5, rnd() - .5).normalize(), d: rnd() * .12 }); }); }
    const stT = puffs(NS, GRN); body.add(stT);
    const coreS = sprite(16, "rgba(110,255,140,1)", "omgcore"); body.add(coreS); const coreH = sprite(34, "rgba(60,255,110,1)", "omghalo"); coreH.material.opacity = .35; body.add(coreH);
    const core = new TH.Mesh(new TH.BoxGeometry(C * 2.6, C * 2.6, C * 2.6), glowMat(GRN, .35)); core.userData.dyn = 1; body.add(core);
    const chans = []; for (const d of [V(1, 0, 0), V(-1, 0, 0), V(0, 1, 0), V(0, -1, 0), V(0, 0, 1), V(0, 0, -1)]) { const m = new TH.Mesh(new TH.CylinderGeometry(.18, .18, C * 2.2, 8, 1, true), glowMat(GRN2, .6)); m.userData.dyn = 1; m.position.copy(d).multiplyScalar(C * 1.2); m.quaternion.setFromUnitVectors(V(0, 1, 0), d); body.add(m); chans.push(m); }
    // the tractor beam: wide translucent cones, a white core, rings running back toward the Cube
    const trac = new TH.Group(); trac.visible = false; trac.position.z = F; body.add(trac); const TL = 70, cyl = (r0, r1, mat) => { const m = new TH.Mesh(new TH.CylinderGeometry(r0, r1, TL, 28, 1, true).translate(0, TL / 2, 0).rotateX(Math.PI / 2), mat); m.userData.dyn = 1; trac.add(m); return m; };
    const cone = cyl(2.6, 7, glowMat(GRN, .2)), cone2 = cyl(1.6, 4, glowMat(0x9dffb0, .28)), tcore = cyl(.28, .5, glowMat(0xeaffea, .9));
    const trings = []; for (let k = 0; k < 8; k++) { const r = new TH.Mesh(new TH.TorusGeometry(1, .1, 6, 40), glowMat(GRN2, .8)); r.userData.dyn = 1; trac.add(r); trings.push(r); } const tflare = sprite(12, "rgba(140,255,160,1)", "omgtf"); tflare.position.z = F + .3; body.add(tflare);
    // the burst emitters and their bolts
    const EM = [[-3.6, 3.6], [3.6, 3.6], [-3.6, -3.6], [3.6, -3.6]].map(([x, y]) => { const m = sprite(2.4, "rgba(170,255,180,1)", "omgem"); m.position.set(x, y, F + .2); body.add(m); return m; });
    const NB = 12, bol = []; for (let i = 0; i < NB; i++) { const g = new TH.Group(); const h = sprite(3.6, "rgba(120,255,140,1)", "omgbh"), tl = new TH.Mesh(new TH.CylinderGeometry(.22, .06, 9, 6, 1, true).translate(0, -4.5, 0).rotateX(Math.PI / 2), glowMat(0x9dffb0, 0)); tl.userData.dyn = 1; g.add(h); g.add(tl); body.add(g); const e = i % 4, v = (i / 4) | 0; bol.push({ g, h, tl, e, d: v * .26 + e * .035, sx: (rnd() - .5) * 6, sy: (rnd() - .5) * 5 }); }
    // the energy wave
    const shell = wave(body, 9, true, GRN), wring = wave(body, 14, false, GRN2); const bt = bolts(body, 12, () => { const a = cells[(rnd() * NC) | 0], b2 = cells[(rnd() * NC) | 0]; return [a.p.clone().multiplyScalar(1.02), b2.p.clone().multiplyScalar(1.02)]; }, GRN2);
    const mv = moves({ tractor: 3400, burst: 2600, wave: 2400, storm: 3600, hit: 520 }), hit = hitKit(body, shk); const M4 = new TH.Matrix4(), Q0 = new TH.Quaternion(), Q1 = new TH.Quaternion(), S1 = V(1, 1, 1), S0v = V(.001, .001, .001), P0 = V(0, 0, 0), P1 = V(0, 0, 0);
    const tick = t => { const ft = mv.f("tractor", t), fb = mv.f("burst", t), fw = mv.f("wave", t), fs = mv.f("storm", t), fh = mv.f("hit", t);
      const open = bell(ft, 0, .12, .9, 1), hold = bell(ft, .1, .18, .86, .97), gather = bell(fw, 0, .3, .34, .4), wv = fw < .34 ? -1 : (fw - .34) / .66, sto = bell(fs, 0, .2, .78, 1);
      body.rotation.y = Math.sin(t * .0004) * .05; body.rotation.x = Math.sin(t * .0003) * .04;
      cells.forEach((c, i) => { let o = gather * -.4 + (wv > 0 && wv < .25 ? (1 - wv / .25) * 1.2 : 0); if (c.sh) o += Math.max(0, Math.sin(t * .0011 + c.ph)) * 1.4; if (open > 0 && c.n.z > 0) o += open * 1.1;
        const out = c.st >= 0 && fs >= 0 && sto > .02; P0.copy(c.p).addScaledVector(c.n, o); M4.compose(P0, Q0, out ? S0v : S1); cubes.setMatrixAt(i, M4); }); cubes.instanceMatrix.needsUpdate = true;
      sD.forEach((d, k) => { const c = cells[d.ci], e = fs < 0 ? 0 : Math.min(1, Math.max(0, (sto - d.d) / (1 - d.d))), on = fs >= 0 && sto > .02; if (!on) { M4.compose(c.p, Q0, S0v); storm.setMatrixAt(k, M4); stT.put(k, 0, 0, 0, 1, 0); return; }
        const a = d.a + t * d.w; P1.set(Math.cos(a) * d.r, d.y + Math.sin(t * .002 + k) * 1.5, Math.sin(a) * d.r); P0.copy(c.p).lerp(P1, e * e * (3 - 2 * e)); Q1.setFromAxisAngle(d.tl, t * .004 * e + k); M4.compose(P0, Q1, S1); storm.setMatrixAt(k, M4); stT.put(k, P0.x, P0.y, P0.z, 3.2, .5 * e); });
      storm.instanceMatrix.needsUpdate = true; stT.done();
      trac.visible = hold > .01; if (trac.visible) { const fl = .85 + .15 * Math.sin(t * .05) * Math.sin(t * .023); trac.scale.set(1 + hold * .15 + Math.sin(t * .006) * .05, 1 + hold * .15 + Math.sin(t * .006) * .05, Math.min(1, hold * 1.6)); cone.material.opacity = .2 * hold * fl; cone2.material.opacity = .28 * hold * fl; tcore.material.opacity = .9 * hold;
        trings.forEach((r, k) => { const u = 1 - ((t * .0005 + k / trings.length) % 1); r.position.z = u * TL; r.scale.setScalar(2.4 + 5 * u); r.material.opacity = .8 * hold * Math.sin(u * Math.PI); }); }
      tflare.material.opacity = Math.max(open * .9, hold); tflare.scale.setScalar(12 * (1 + hold * .5 + Math.sin(t * .02) * .08));
      EM.forEach((m, e) => { let fl = 0; for (let v = 0; v < 3; v++) { const k = fb < 0 ? -1 : (fb - v * .26 - e * .035) / .08; if (k > 0 && k < 1) fl = Math.max(fl, 1 - k); } m.material.opacity = fl; m.scale.setScalar(2.4 + fl * 5); });
      bol.forEach(B => { const k = fb < 0 ? -1 : (fb - B.d) / .3, on = k > 0 && k < 1, p = EM[B.e].position; B.h.material.opacity = on ? 1 - k * .5 : 0; B.tl.material.opacity = on ? .8 * (1 - k * .5) : 0; if (on) B.g.position.set(p.x + B.sx * k, p.y + B.sy * k, F + k * 64); });
      const glow = 1 + .15 * Math.sin(t * .003) + gather * 1.6 + hold * .6 + sto * .4; coreS.scale.setScalar(16 * glow); coreS.material.opacity = Math.min(1, .7 * glow); coreH.material.opacity = .25 + .2 * glow; core.material.opacity = .25 + .2 * glow; cubeM.emissiveIntensity = 1.4 + .4 * Math.sin(t * .002) + gather + (wv > 0 && wv < .4 ? 1 : 0) + sto * .4;
      chans.forEach((m, i) => { m.material.opacity = (.35 + .35 * Math.sin(t * .006 + i * 1.3)) * glow; });
      shell(wv); wring(wv < 0 ? -1 : wv * .9); bt(t, 1 + gather * 6 + sto * 5 + hold * 2); hit(bell(fh, 0, .05, .4, 1), t); };
    bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 9, h: 12 }; }''' + s[j:]
rep('WB_ATK.omg = ["pulse", "beam", "lock"];', 'WB_ATK.omg = ["tractor", "burst", "wave", "storm"];')
open(P, 'w').write(s)
