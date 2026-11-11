# v440: the Omega Cube assembles into one giant cube (owner: "it was supposed to assemble into an even bigger cube!"). 5 x 5 x 5 cells
#  the size of the Super Cube (30 units; each Assimilation Cube grows to that size as it locks), the Super Cube at the centre: the two
#  cubes inside lock first, above and below the core while the walls are still open, then the 98 of the shell, from the bottom face
#  up, layer by layer, round each layer. 150 units a side (was a 105-unit cross of blocks). Holding ring, approach, flares and haze
#  scaled to match. And the Last Stand (owner: "against a massive staged fleet formation, and the cubes wipe them out and then disperse
#  again"): the grand fleet warps in and forms up (158-172 min), fires, and is wiped out by beams and two Omega Pulses (172-200 min);
#  the Omega Cube comes apart at 205 min and the cubes are home by 250 min (it stood for 24 h before). p440_fleet.js. Plus a giant 3D countdown over the Void to the next event (p440_countdown.js; owner: "a big 3d countdown timer to the event, elemental glow,
#  power surges, green electricity sparks").
import json
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
OLD = json.load(open("tools/patches/p440_old.json"))
rep(OLD, """  /* v440 one giant cube: 5x5x5 cells the size of the Super Cube, the Super Cube at its centre. The two cubes inside lock first (above
     and below the core, while the walls are still open), then the 98 of the shell, from the bottom face up, layer by layer */
  const cells = [], cell = (c, m) => cells.push({ c, m, p: [c[0] * DV_CELL, c[1] * DV_CELL, c[2] * DV_CELL] }); cell([0, -1, 0], -1); cell([0, 1, 0], -1);
  const sh = []; for (let x = -2; x <= 2; x++) for (let y = -2; y <= 2; y++) for (let z = -2; z <= 2; z++) if (Math.max(Math.abs(x), Math.abs(y), Math.abs(z)) === 2) sh.push([x, y, z]);
  sh.sort((u, v) => u[1] - v[1] || Math.atan2(u[2], u[0]) - Math.atan2(v[2], v[0]) || Math.hypot(u[0], u[2]) - Math.hypot(v[0], v[2])); sh.forEach(c => cell(c, 0));
  const occ = new Set(cells.map(s => s.c.join())); occ.add("0,0,0");""")
rep("DV_CELL = 15, DV_Y = 150, DV_HOLD = 200,", "DV_CELL = 30, DV_Y = 170, DV_HOLD = 320, /* v440 */")
rep("st.x = c.s.p[0] + c.s.n[0] * 40; st.y = c.s.p[1] + c.s.n[1] * 40; st.z = c.s.p[2] + c.s.n[2] * 40;", "st.x = c.s.p[0] + c.s.n[0] * 75; st.y = c.s.p[1] + c.s.n[1] * 75; st.z = c.s.p[2] + c.s.n[2] * 75;")
rep("st.x = c.s.p[0] + c.s.n[0] * 60; st.y = c.s.p[1] + c.s.n[1] * 60; st.z = c.s.p[2] + c.s.n[2] * 60;", "st.x = c.s.p[0] + c.s.n[0] * 110; st.y = c.s.p[1] + c.s.n[1] * 110; st.z = c.s.p[2] + c.s.n[2] * 110;")
rep("f.f.scale.setScalar(70 * f.big * (.4 + a));", "f.f.scale.setScalar(130 * f.big * (.4 + a));")
rep("f.ring.position.set(f.p[0] - f.n[0] * 7, f.p[1] - f.n[1] * 7, f.p[2] - f.n[2] * 7);", "f.ring.position.set(f.p[0] - f.n[0] * 15, f.p[1] - f.n[1] * 15, f.p[2] - f.n[2] * 15);")
rep("f.ring.scale.setScalar(6 + 90 * dvEase(a));", "f.ring.scale.setScalar(12 + 170 * dvEase(a));")
rep("Math.cos(a) * 55, (i % 3 - 1) * 35, Math.sin(a) * 55, 220 + (i * 37) % 120", "Math.cos(a) * 110, (i % 3 - 1) * 70, Math.sin(a) * 110, 400 + (i * 37) % 200")
rep("dist: 520", "dist: 760")

# v440 the Last Stand: the staged fleet, the battle, then the cubes disperse
FLEET = open("tools/patches/p440_fleet.js").read()
rep("const DV = { mig: 30 * DV_M, lock0: 90 * DV_M, lock1: 148 * DV_M, act: 150 * DV_M, erupt: 153 * DV_M, combat: 156 * DV_M, ret: 24 * DV_H, end: 25 * DV_H };",
    "const DV = { mig: 30 * DV_M, lock0: 90 * DV_M, lock1: 148 * DV_M, act: 150 * DV_M, erupt: 153 * DV_M, combat: 156 * DV_M, stage: 158 * DV_M, war0: 172 * DV_M, war1: 200 * DV_M, ret: 205 * DV_M, end: 250 * DV_M }; /* v440 the fleet stages, is wiped out, and the cubes disperse */")
rep('const dvPhase = e => e < DV.mig ? "awake" : e < DV.lock0 ? "mig" : e < DV.act ? "asm" : e < DV.combat ? "act" : e < DV.ret ? "combat" : "ret";',
    'const dvPhase = e => e < DV.mig ? "awake" : e < DV.lock0 ? "mig" : e < DV.act ? "asm" : e < DV.combat ? "act" : e < DV.war0 ? "stage" : e < DV.war1 ? "war" : e < DV.ret ? "after" : "ret";')
rep("const DV_SIM = [[0, 0], [15, DV.mig], [165, DV.act], [190, DV.combat], [205, DV.combat + 3 * DV_H], [207, DV.ret], [240, DV.end]];",
    "const DV_SIM = [[0, 0], [15, DV.mig], [140, DV.act], [160, DV.combat], [176, DV.war0], [230, DV.war1], [238, DV.ret], [270, DV.end]];")
rep("return { e, s0: C.s0, ph: dvPhase(e), sim: 1 }; }", "return { e, s0: C.s0, ph: dvPhase(e), sim: 1, rate: (eb - ea) / ((b - a) * 1000) }; }")
rep("X.grp.traverse(o => { try { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); } catch (e) {} }); W.dv = null; G.dvP = null; }",
    "X.grp.traverse(o => { if (o.userData.keep) return; /* v440 the fleet's hulls and materials are the map's shared ones */ try { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); } catch (e) {} }); W.dv = null; G.dvP = null; G.dvF = null; }")
rep("  /* the core: silent and dark,", "  try { dvFleetTick(W, X, D, t); } catch (e) { mapErr(e); } /* v440 the Last Stand */\n  /* the core: silent and dark,")
rep("/* the owner's preview: the whole event", FLEET + open("tools/patches/p440_countdown.js").read() + "/* the owner's preview: the whole event")
rep("G.dvP = null; G.dvSim = { t0: performance.now(),", "G.dvP = null; G.dvF = null; G.dvSim = { t0: performance.now(),")
rep("Cube Devastation in four minutes.", "Cube Devastation in four and a half minutes.")
rep("function dvTick(W, t, T) { const D = dvNow(T); if (!D) {", "function dvTick(W, t, T) { const D = dvNow(T); try { dvCountdown(W, t, T, !!D); } catch (e) { mapErr(e); } /* v440 */ if (!D) {")
rep("X.wave = new TH.Mesh(new TH.SphereGeometry(1, 32, 16), new TH.MeshBasicMaterial({ color: 0x5dff6a, transparent: true, opacity: 0, side: TH.BackSide, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false }));",
    "X.wave = new TH.Mesh(new TH.SphereGeometry(1, 48, 24), dvRim(0x5dff6a)); /* v440 a shell of light, not a green fill */")
rep("X.wave.material.opacity = .55 * (1 - wa);", "X.wave.material.uniforms.uA.value = 1.2 * (1 - wa);")
t = t.replace("const GAME_V = 439;", "const GAME_V = 440;")
open(p, "w").write(t); print("ok")
