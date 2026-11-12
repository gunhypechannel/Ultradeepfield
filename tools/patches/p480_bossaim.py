# v480 (owner: "make them look forward and then turn at like 45 degree angle towards the target they are attacking"; "the omega cube in
# battle simulation should look more like its final form, can we make a model to match it?")
# In every boss battle report the boss now faces forward, and on each attack it turns about 45 degrees toward a squad it is attacking,
# holds through the attack, then turns back. The Omega Cube's report draws a new 3D model of its final form instead of the flat Super
# Cube picture: a 5x5x5 shell of 98 green-gridded cubes round a glowing core, energy channels to the core, cubes that shift and lock,
# with three moves (a pulse, a face beam, a re-lock) and the same turn.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
# ---------------- the Omega Cube model ----------------
rep("  root.BOSS3D = { init(T) { TH = T; },",
r"""  /* v480 the Omega Cube's final form for battle reports: a 5x5x5 shell of 98 cubes (each one an Assimilation Cube, gridded in green
     light) round the Super Cube's glowing core, energy channels running out to the faces, a few cubes always shifting out and
     locking back. Moves: pulse (every cube pushes out, a green shock shell), beam (the front face opens and fires), lock (the cubes
     slide out and slam back in a wave), hit. */
  function omega() { const grp = new TH.Group(), shk = new TH.Group(), body = new TH.Group(); grp.add(shk); shk.add(body); const C = 2.4, GRN = 0x5dff7a, GRN2 = 0xc8ffd0;
    const gt = (() => { const c = cv(128, 128), x = c.getContext("2d"); x.fillStyle = "#000"; x.fillRect(0, 0, 128, 128); x.strokeStyle = "#7dff90"; x.lineWidth = 7; x.strokeRect(3, 3, 122, 122); x.lineWidth = 2.5; x.globalAlpha = .75; for (const v of [43, 85]) { x.beginPath(); x.moveTo(v, 6); x.lineTo(v, 122); x.moveTo(6, v); x.lineTo(122, v); x.stroke(); } x.globalAlpha = .9; x.fillStyle = "#b8ffc4"; for (const [a, b2] of [[20, 20], [100, 64], [62, 104]]) x.fillRect(a, b2, 7, 7); const t2 = new TH.CanvasTexture(c); t2.encoding = TH.sRGBEncoding; t2.anisotropy = 4; return t2; })();
    const cubeM = new TH.MeshStandardMaterial({ color: 0x0b120e, metalness: .85, roughness: .35, emissive: 0xffffff, emissiveMap: gt, emissiveIntensity: 1.6, envMapIntensity: .8 });
    const cells = []; for (let x = -2; x <= 2; x++) for (let y = -2; y <= 2; y++) for (let z = -2; z <= 2; z++) if (Math.max(Math.abs(x), Math.abs(y), Math.abs(z)) === 2) { const n = [0, 0, 0], ax = Math.abs(x) === 2 ? 0 : Math.abs(y) === 2 ? 1 : 2; n[ax] = [x, y, z][ax] > 0 ? 1 : -1; cells.push({ p: V(x * C, y * C, z * C), n: V(...n), ph: rnd() * TAU, sh: rnd() < .07, d: Math.hypot(x, y, z) }); }
    const NC = cells.length, cubes = inst(new TH.BoxGeometry(C * .94, C * .94, C * .94), cubeM, NC); body.add(cubes);
    const coreS = sprite(16, "rgba(110,255,140,1)", "omgcore"); body.add(coreS); const coreH = sprite(34, "rgba(60,255,110,1)", "omghalo"); coreH.material.opacity = .35; body.add(coreH);
    const core = new TH.Mesh(new TH.BoxGeometry(C * 2.6, C * 2.6, C * 2.6), glowMat(GRN, .35)); core.userData.dyn = 1; body.add(core);
    const chans = []; for (const d of [V(1, 0, 0), V(-1, 0, 0), V(0, 1, 0), V(0, -1, 0), V(0, 0, 1), V(0, 0, -1)]) { const m = new TH.Mesh(new TH.CylinderGeometry(.18, .18, C * 2.2, 8, 1, true), glowMat(GRN2, .6)); m.userData.dyn = 1; m.position.copy(d).multiplyScalar(C * 1.2); m.quaternion.setFromUnitVectors(V(0, 1, 0), d); body.add(m); chans.push(m); }
    const beam = new TH.Group(); beam.visible = false; body.add(beam); for (const [r, o, c] of [[2.2, .45, GRN], [.7, .95, GRN2]]) { const g = new TH.CylinderGeometry(r * .8, r, 60, 20, 1, true); g.translate(0, 30, 0); g.rotateX(Math.PI / 2); const m = new TH.Mesh(g, glowMat(c, o)); m.userData.dyn = 1; beam.add(m); } beam.position.z = C * 2.5;
    const shell = wave(body, 9, true, GRN), ring = wave(body, 12, false, GRN2); const bt = bolts(body, 12, () => { const a = cells[(rnd() * NC) | 0], b2 = cells[(rnd() * NC) | 0]; return [a.p.clone().multiplyScalar(1.02), b2.p.clone().multiplyScalar(1.02)]; }, GRN2);
    const mv = moves({ pulse: 2400, beam: 3000, lock: 2800, hit: 520 }), hit = hitKit(body, shk); const M4 = new TH.Matrix4(), Q0 = new TH.Quaternion(), S1 = V(1, 1, 1), P0 = V(0, 0, 0);
    const tick = t => { const fp = mv.f("pulse", t), fb = mv.f("beam", t), fl = mv.f("lock", t), fh = mv.f("hit", t);
      const push = bell(fp, 0, .3, .4, .7), charge = bell(fb, 0, .25, .3, .35), fire = bell(fb, .3, .36, .82, .95);
      body.rotation.y = t * .00012; body.rotation.x = Math.sin(t * .0003) * .06;
      cells.forEach((c, i) => { let o = push * .9 * (.6 + .4 * Math.sin(c.ph)); if (c.sh) o += Math.max(0, Math.sin(t * .0011 + c.ph)) * 1.4; if (fl >= 0) { const w = (fl - c.d * .06) * 2.2; o += w > 0 && w < 1 ? Math.sin(w * Math.PI) * 2 : 0; } if (charge > 0 && c.n.z > 0) o += charge * 1.2;
        P0.copy(c.p).addScaledVector(c.n, o); M4.compose(P0, Q0, S1); cubes.setMatrixAt(i, M4); }); cubes.instanceMatrix.needsUpdate = true;
      const glow = 1 + .15 * Math.sin(t * .003) + push * .8 + charge * 1.5 + fire * .6; coreS.scale.setScalar(16 * glow); coreS.material.opacity = Math.min(1, .7 * glow); coreH.material.opacity = .25 + .2 * glow; core.material.opacity = .25 + .2 * glow; cubeM.emissiveIntensity = 1.4 + .4 * Math.sin(t * .002) + push + fire;
      chans.forEach((m, i) => { m.material.opacity = (.35 + .35 * Math.sin(t * .006 + i * 1.3)) * glow; });
      beam.visible = fire > .01; if (beam.visible) { beam.children[0].material.opacity = .45 * fire * (.85 + rnd() * .15); beam.children[1].material.opacity = .95 * fire; }
      shell(fp < 0 ? -1 : (fp - .35) / .65); ring(fl < 0 ? -1 : fl); bt(t, 1 + push * 6 + fire * 4); hit(bell(fh, 0, .05, .4, 1), t); };
    bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 9, h: 12 }; }
  root.BOSS3D = { init(T) { TH = T; },""")
rep("vaelthar, aexion, EL, prep };", "vaelthar, aexion, omega, EL, prep };")
# ---------------- the battle report: face forward, turn to the target ----------------
rep("const WB_FACE = { devourer: 1 };", "const WB_FACE = { devourer: 1 }; const OMG_D = { m3: \"omega\" }, wbD = k => WB[k] || (typeof SBW !== \"undefined\" && SBW[k]) || (k === \"omg\" ? OMG_D : null); /* v480 */")
rep("const WB_FRONT = { vaelthar: 0,", "const WB_FRONT = { omega: 0, vaelthar: 0,")
rep("const WB_VIEW = { vaelthar:", "const WB_VIEW = { omega: [0, [-10, 7, 40], [0, 0, 0]], vaelthar:")
rep("function wbArt(key, w, h, t, b) { if (typeof BOSS3D === \"undefined\" || !(WB[key] || (typeof SBW !== \"undefined\" && SBW[key]))) return null;",
    "function wbArt(key, w, h, t, b) { if (typeof BOSS3D === \"undefined\" || !wbD(key)) return null;")
rep("const m3 = (WB[key] || SBW[key]).m3, V0 = WB_VIEW[m3], tall = h > w * .75 || !!WB_FACE[m3];",
    "const m3 = wbD(key).m3, V0 = WB_VIEW[m3], tall = true; /* v480: every boss faces the fleet, and turns to its target as it attacks */")
rep("WBR.b.grp.rotation.y = tall ? WB_FRONT[m3] : V0[0]; WBR.sc.add(WBR.b.grp);", "WBR.b.grp.rotation.y = WBR.y0 = WB_FRONT[m3] != null ? WB_FRONT[m3] : V0[0]; WBR.yaw = WBR.y0; WBR.lt = 0; WBR.sc.add(WBR.b.grp);")
rep("if (b.live && t > WBR.next) { WBR.next = t + 2400 + Math.random() * 1400; const m = wbMoves(key), mv = m[(Math.random() * m.length) | 0]; WBR.b.act(mv); WBR.mv = { m: mv, t0: t }; } }",
    "wbFend(key, b, t); }")
rep("function wbArt(key, w, h, t, b) {", r"""/* v480 a boss fending off attackers on every side: three facings (front, 45 degrees left, 45 degrees right). Each beat: turn toward a
   side (0.65 s, eased), hold a second, attack (the move and its strike on the fleet), hold a second, turn back to the front, rest about
   a second, then the next facing, chosen at random but never the same twice running and leaning toward where its targets are */
const WBF = { turn: 650, hold: 900, atk: 2600, rest: 1000 };
function wbFend(key, b, t) { const F = WBF, C = WBR.cy, T2 = F.turn + F.hold, T3 = T2 + F.atk, T4 = T3 + F.hold, T5 = T4 + F.turn;
  if (!b.live) { WBR.cy = null; WBR.face = 0; return; }
  if (!C || t >= C.end) { const tg = b.tg || [], L = tg.filter(v => v < -.04).length, R = tg.filter(v => v > .04).length, last = C ? C.dir : 0;
    const opts = [-1, 0, 1].filter(d => d !== last), w = opts.map(d => d === 0 ? .6 : 1 + (d < 0 ? L : R) / Math.max(1, tg.length)); let r = Math.random() * w.reduce((a, v) => a + v, 0), dir = opts[0]; for (let i = 0; i < opts.length; i++) { r -= w[i]; if (r <= 0) { dir = opts[i]; break; } }
    WBR.cy = { t0: t, dir, fired: 0, end: t + T5 + F.rest * (.8 + Math.random() * .5) }; }
  const c = WBR.cy, e = t - c.t0, sm = u => u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u);
  if (!c.fired && e >= T2) { c.fired = 1; const m = wbMoves(key), mv = m[(Math.random() * m.length) | 0]; WBR.b.act(mv); WBR.mv = { m: mv, t0: t }; }
  WBR.face = c.dir * (e < F.turn ? sm(e / F.turn) : e < T4 ? 1 : 1 - sm((e - T4) / F.turn)); }
function wbArt(key, w, h, t, b) {""")
rep("WBR.b.tick(t); if (WBR.b.lens && WBR.b.mouth)", "{ const k = WBR.lt ? 1 - Math.pow(.985, Math.min(200, t - WBR.lt)) : 1, goal = WBR.y0 + (WBR.face || 0) * Math.PI / 4; WBR.yaw += (goal - WBR.yaw) * k; WBR.lt = t; WBR.b.grp.rotation.y = WBR.yaw; } /* v480 the facing, smoothed once more so a turn never snaps */\n    WBR.b.tick(t); if (WBR.b.lens && WBR.b.mouth)")
# drawSq: the Omega Cube gets its model; every boss is told where its targets are on screen
rep("const wbk = b.r.wb || b.r.sbk, art = wbk ? null : shipArtSoon(\"cube\", b.acc[b.superSide], \"side\"),",
    "const wbk = b.r.wb || b.r.sbk || (b.r.omega ? \"omg\" : null), art = wbk ? null : shipArtSoon(\"cube\", b.acc[b.superSide], \"side\"),")
rep("const A = wbArt(wbk, aw, ah, t, { hp, live: alive.length > 0 });",
    "const A = wbArt(wbk, aw, ah, t, { hp, live: alive.length > 0, tg: Q.map((q2, k) => q2.side !== b.superSide && b.n[k] > 0 && scr[k] ? (scr[k].x - cx) / W : null).filter(v => v != null) });")
rep('ctx.fillStyle = wbk ? (WB[wbk] || SBW[wbk] || { col: "#c890ff" }).col : "#5dff6a";', 'ctx.fillStyle = wbk ? (WB[wbk] || SBW[wbk] || { col: wbk === "omg" ? "#5dff7a" : "#c890ff" }).col : "#5dff6a";')
rep("const wbMoves = key =>", "WB_ATK.omg = [\"pulse\", \"beam\", \"lock\"]; const wbMoves = key =>")
s = re.sub(r"GAME_V = 479\b", "GAME_V = 480", s)
open(P, 'w').write(s)
