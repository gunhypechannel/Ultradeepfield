# v481 (owner: "All the bosses and super bosses should be the same"; chose the Super Cube). The Super Cube's battle reports (the
# Collective Warden, and The Cube attacking) now draw it as a live 3D model, the same Collective fortress as on the map (borgCube, dense
# machinery and emerald lights), and it fends off attackers from three facings like every other boss: turn, hold, attack, hold, back to
# the front, rest. Its attacks: disruptor bolts from its faces, a charged disintegrator beam, and its hex shield flaring.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('const OMG_D = { m3: "omega" }, wbD = k => WB[k] || (typeof SBW !== "undefined" && SBW[k]) || (k === "omg" ? OMG_D : null); /* v480 */',
r'''const OMG_D = { m3: "omega" }, SCB_D = { m3: "supercube" }, wbD = k => WB[k] || (typeof SBW !== "undefined" && SBW[k]) || (k === "omg" ? OMG_D : k === "scb" ? SCB_D : null); /* v480, v481 */
/* v481 the Super Cube for battle reports: the Collective's fortress (the map's borgCube at full detail), a ring and a core light, its hex
   shield, green disruptor bolts from its faces, a charged disintegrator beam from its front face. Same shape of object as a BOSS3D model. */
function superCube3D() { const grp = new TH.Group(), shk = new TH.Group(), body = new TH.Group(); grp.add(shk); shk.add(body); const S0 = 5, GRN = 0x5dff6a;
  body.add(borgCube(S0, 3, 4242)); const glowM = (c, o) => new TH.MeshBasicMaterial({ color: c, transparent: true, opacity: o, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false, side: TH.DoubleSide });
  const ring = new TH.Mesh(new TH.TorusGeometry(S0 * .95, .05, 6, 72), glowM(GRN, .3)); ring.rotation.x = Math.PI / 2; body.add(ring);
  const sp = (c, sz, o) => { const m = new TH.Sprite(new TH.SpriteMaterial({ map: glowTex(c, .9), blending: TH.AdditiveBlending, depthWrite: false, transparent: true, opacity: o, toneMapped: false })); m.scale.setScalar(sz); return m; };
  const halo = sp("93,255,106", 15, .3); body.add(halo); const core = sp("200,255,210", 2.4, .9); core.position.set(0, 0, S0 / 2 + .05); body.add(core);
  const shM = new TH.ShaderMaterial({ uniforms: { uO: { value: 0 }, uT: { value: 0 } }, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, side: TH.DoubleSide, toneMapped: false,
    vertexShader: "varying vec3 vN; varying vec3 vV; varying vec3 vP; void main() { vec4 mv = modelViewMatrix * vec4(position, 1.); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); vP = position; gl_Position = projectionMatrix * mv; }",
    fragmentShader: "uniform float uO, uT; varying vec3 vN; varying vec3 vV; varying vec3 vP; void main() { float fr = pow(1. - abs(dot(vN, vV)), 2.); float hx = abs(sin(vP.x * 2.4 + uT) * sin(vP.y * 2.4) * sin(vP.z * 2.4 - uT)); float a = (fr * 1.2 + pow(hx, 6.) * .9 + .04) * uO; gl_FragColor = vec4(vec3(.36, 1., .45) * a, a); }" });
  const shield = new TH.Mesh(new TH.SphereGeometry(S0 * .98, 40, 28), shM); body.add(shield);
  const beam = new TH.Group(); beam.visible = false; body.add(beam); for (const [r, o, c] of [[.9, .45, GRN], [.3, .95, 0xeaffea]]) { const g = new TH.CylinderGeometry(r * .7, r, 60, 18, 1, true); g.translate(0, 30, 0); g.rotateX(Math.PI / 2); beam.add(new TH.Mesh(g, glowM(c, o))); } beam.position.z = S0 / 2;
  const bolts = []; for (let i = 0; i < 10; i++) { const b = sp("140,255,160", 1.3, 0); body.add(b); const f = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, 0, 1], [0, -1, 0]][i % 5]; bolts.push({ b, f: new TH.Vector3(...f), u: (i % 3 - 1) * 1.2, v: ((i * 7) % 3 - 1) * 1.2, d: i * .07 }); }
  const D = { disrupt: 2600, beam: 3000, shield: 2400, hit: 520 }, S = {}; const f = (n, t) => { const x = S[n]; if (!x) return -1; if (x.t0 < 0) x.t0 = t; const k = (t - x.t0) / D[n]; if (k >= 1) { delete S[n]; return -1; } return k; };
  const ss = (a, b, x) => { const u = Math.min(1, Math.max(0, (x - a) / (b - a))); return u * u * (3 - 2 * u); }, bell = (x, a, b, c, d) => x < 0 ? 0 : ss(a, b, x) * (1 - ss(c, d, x)); let hitT = -1e9;
  const tick = t => { const fd = f("disrupt", t), fb = f("beam", t), fs = f("shield", t), fh = f("hit", t); if (fh >= 0 && fh < .1) hitT = t;
    const charge = bell(fb, 0, .25, .3, .36), fire = bell(fb, .3, .36, .82, .95), flare = bell(fs, 0, .2, .7, 1), hh = Math.max(0, 1 - (t - hitT) / 500);
    body.rotation.y = Math.sin(t * .0004) * .05; body.rotation.x = Math.sin(t * .0003) * .04; shk.position.set((Math.random() - .5) * hh * .15, (Math.random() - .5) * hh * .15, 0);
    ring.rotation.z = t * .0004; ring.material.opacity = .25 + .15 * Math.sin(t * .003) + flare * .4; halo.material.opacity = .25 + charge * .5 + fire * .3 + flare * .2; halo.scale.setScalar(15 * (1 + charge * .4 + fire * .3));
    core.material.opacity = .7 + charge * .3; core.scale.setScalar(2.4 * (1 + charge * 2.2 + fire * 1.4));
    shM.uniforms.uT.value = t * .001; shM.uniforms.uO.value = .12 + flare * 1.1 + hh * .5;
    beam.visible = fire > .01; if (beam.visible) { beam.children[0].material.opacity = .45 * fire * (.85 + Math.random() * .15); beam.children[1].material.opacity = .95 * fire; }
    bolts.forEach(B => { const k = fd < 0 ? -1 : (fd - B.d) / .45, on = k > 0 && k < 1; B.b.material.opacity = on ? (1 - k) : 0; if (on) { const out = S0 / 2 + k * 26; B.b.position.copy(B.f).multiplyScalar(out); const ax = Math.abs(B.f.x) ? 1 : 0, ay = Math.abs(B.f.y) ? 1 : 0; B.b.position.x += ax ? 0 : B.u; B.b.position.y += ay ? 0 : B.v; B.b.position.z += !ax && !ay ? 0 : B.u * .7; B.b.scale.setScalar(1.3 + k * 1.5); } }); };
  return { grp, tick, act: n => { if (D[n]) S[n] = { t0: -1 }; }, moves: Object.keys(D), r: 5, h: 6 }; }''')
rep("const WB_FRONT = { omega: 0,", "const WB_FRONT = { supercube: 0, omega: 0,")
rep("const WB_VIEW = { omega: [0, [-10, 7, 40], [0, 0, 0]],", "const WB_VIEW = { supercube: [0, [-6, 3, 31], [0, .6, 0]], omega: [0, [-10, 7, 40], [0, 0, 0]],")
rep("WBR.b = BOSS3D.prep(BOSS3D[m3](", "WBR.b = m3 === \"supercube\" ? BOSS3D.prep(superCube3D(), wbEnv(WBR.r)) : BOSS3D.prep(BOSS3D[m3](")
rep("const wbk = b.r.wb || b.r.sbk || (b.r.omega ? \"omg\" : null),", "const wbk = b.r.wb || b.r.sbk || (b.r.omega ? \"omg\" : b.superSide ? \"scb\" : null),")
rep('{ col: wbk === "omg" ? "#5dff7a" : "#c890ff" }', '{ col: wbk === "omg" || wbk === "scb" ? "#5dff7a" : "#c890ff" }')
rep("ctx.drawImage(glowSprite(wbk ? \"rgba(180,92,255,1)\" : \"rgba(93,255,106,1)\")", "ctx.drawImage(glowSprite(wbk && wbk !== \"scb\" && wbk !== \"omg\" ? \"rgba(180,92,255,1)\" : \"rgba(93,255,106,1)\")")
rep('WB_ATK.omg = ["pulse", "beam", "lock"];', 'WB_ATK.omg = ["pulse", "beam", "lock"]; WB_ATK.scb = ["disrupt", "beam", "shield"];')
s = re.sub(r"GAME_V = 480\b", "GAME_V = 481", s)
open(P, 'w').write(s)
