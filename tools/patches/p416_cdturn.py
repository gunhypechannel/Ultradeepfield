# v416: the Cube Destroyer turns like a real station, not a spinning picture. v414 turned it round the line of sight (a roll: the
# equator ring swung to vertical, so it read as a disc spinning). Now it yaws its dish across its front face and pitches toward the
# target with no roll, so the ring stays level as the whole station swings round. The dish always keeps the same depth toward the
# viewer (screen offset 0.85 of the radius): aim phi (on screen, up positive) maps to yaw psi and pitch theta with cos(psi) = 0.85 cos(phi)
# (psi < 0: the dish passes across the front) and sin(theta) = 0.85 sin(phi) / sin(psi). The rest pose is phi0 = -18 degrees (the baked
# sprite: dish 0.47 L forward, 0.152 L down), so 12 bakes at phi0 + k x 30 degrees ("~pK") include the rest pose as K = 0. A turning hull
# cross-fades the two nearest bakes; the dish (and the beam's origin) sits at 0.491 L x (cos phi, -sin phi). All 12 bake at the start of
# a battle with a Cube Destroyer (during the intro), not when it first fires; until a bake is ready the nearest ready one is used.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("""  let rotK = 0; { const mr = /~r(\\d+)$/.exec(String(accent)); if (mr) { rotK = +mr[1]; accent = String(accent).slice(0, mr.index); } } /* v414 a Cube Destroyer turned rotK x 30 degrees round the line of sight */""",
    """  let rotK = 0; { const mr = /~p(\\d+)$/.exec(String(accent)); if (mr) { rotK = +mr[1]; accent = String(accent).slice(0, mr.index); } } /* v416 a Cube Destroyer turned to aim rotK x 30 degrees round from its rest pose */""")
rep("""    if (rotK) { const ax = S.camera.position.clone().normalize(), an = rotK * Math.PI / 6; ship.position.applyAxisAngle(ax, an); ship.rotateOnWorldAxis(ax, an); }""",
    """    if (rotK) { const R = phi => { const yp = cdYawPitch(phi); return new TH.Matrix4().makeRotationX(yp[1]).multiply(new TH.Matrix4().makeRotationY(yp[0])); }, M = R(CD_PHI0 + rotK * Math.PI / 6).multiply(R(CD_PHI0).invert());
      const qc = S.camera.quaternion, qW = qc.clone().multiply(new TH.Quaternion().setFromRotationMatrix(M)).multiply(qc.clone().invert()); ship.position.applyQuaternion(qW); ship.quaternion.premultiply(qW); } /* in camera space: yaw, then pitch, no roll */""")
rep("""const CD_S = -1; // v414 which way a turned bake turns on screen
function cdTurn(b, i, cx, cy, face, scr, T, real) { const A = b.cdRot || (b.cdRot = {}), m = (b.beams || []).find(m => m.wb && m.s === i && T - m.t0 > -.6 && T - m.t0 < m.charge + m.life);
  let want = 0; if (m) { const E = scr[m.e] || (m.ix != null ? { x: m.ix, y: m.iy } : null); if (E) { const a0 = Math.atan2(.152, face * .47); want = Math.atan2(E.y - cy, E.x - cx) - a0; want = Math.atan2(Math.sin(want), Math.cos(want)); } }
  const cur = A[i] || 0, d = Math.atan2(Math.sin(want - cur), Math.cos(want - cur)); A[i] = cur + d * Math.min(1, (real || 16) / 600); return A[i]; }""",
    """const CD_PHI0 = -.314; // v416 the Cube Destroyer's rest aim: its baked dish points 18 degrees below forward
function cdYawPitch(phi) { const cy = .85 * Math.cos(phi), sy = -Math.sqrt(Math.max(1e-6, 1 - cy * cy)); return [Math.atan2(sy, cy), Math.asin(clamp(.85 * Math.sin(phi) / sy, -1, 1))]; }
/* the aim (on screen, up positive, in the sprite's own facing) a Cube Destroyer formation has turned to, eased toward the target it fires at */
function cdTurn(b, i, cx, cy, face, scr, T, real) { const A = b.cdPhi || (b.cdPhi = {}), m = (b.beams || []).find(m => m.wb && m.s === i && T - m.t0 > -.6 && T - m.t0 < m.charge + m.life);
  let want = CD_PHI0; if (m) { const E = scr[m.e] || (m.ix != null ? { x: m.ix, y: m.iy } : null); if (E) want = Math.atan2(-(E.y - cy), face * (E.x - cx)); }
  const cur = A[i] == null ? CD_PHI0 : A[i], d = Math.atan2(Math.sin(want - cur), Math.cos(want - cur)); A[i] = cur + d * Math.min(1, (real || 16) / 600); return A[i]; }
/* the two baked poses either side of an aim, and how far between them */
function cdPose(phi, base) { const st = Math.PI / 6, u = (phi - CD_PHI0) / st, k0 = Math.floor(u), w = u - k0, A = ((k0 % 12) + 12) % 12, B = (A + 1) % 12, got = k => !k || !!shipArtSoon("worldbreaker", base + "~p" + k, "side"), acc = k => k ? base + "~p" + k : base;
  if (got(A) && got(B)) return [acc(A), acc(B), w]; if (got(A)) return [acc(A), null, 0]; if (got(B)) return [acc(B), null, 0]; return [base, null, 0]; }""")
rep("""+ (q.k === "worldbreaker" ? (j ? (b.cdRot || {})[i] || 0 : cdTurn(b, i, cx, cy, face, scr, T, real)) : 0); if (!j && q.k === "worldbreaker") (b.cdAng || (b.cdAng = {}))[i] = ba;
          let rb = ba; acc3 = null; if (q.k === "worldbreaker" && Math.abs((b.cdRot || {})[i] || 0) > .02) { const st = Math.PI / 6, w = CD_S * face * ba, kk = ((Math.round(w / st) % 12) + 12) % 12, base = (q.acc || b.acc[q.side]); if (kk && shipArtSoon("worldbreaker", base + "~r" + kk, "side")) { acc3 = base + "~r" + kk; rb = ba - CD_S * face * Math.round(w / st) * st; } } /* v414 the nearest turned bake, the rest by turning the picture */
          if (rb) { ctx.translate(sx, sy); ctx.rotate(rb); ctx.translate(-sx, -sy); } }""",
    """; acc3 = null; acc3b = null;
          if (q.k === "worldbreaker") { const base = (q.acc || b.acc[q.side]); if (!b.cdPre) { b.cdPre = 1; for (let k = 1; k < 12; k++) shipArtSoon("worldbreaker", base + "~p" + k, "side"); } /* v416 bake every pose up front */
            const phi = j ? ((b.cdPhi || {})[i] == null ? CD_PHI0 : b.cdPhi[i]) : cdTurn(b, i, cx, cy, face, scr, T, real); if (Math.abs(phi - CD_PHI0) > .01) { const P = cdPose(phi, base); acc3 = P[0]; acc3b = P[1]; w3 = P[2]; } }
          if (ba) { ctx.translate(sx, sy); ctx.rotate(ba); ctx.translate(-sx, -sy); } }""")
rep("""        drawSide(ctx, q.k, sx, sy, sz, acc3 || (q.acc || b.acc[q.side]), fs2, true);""",
    """        drawSide(ctx, q.k, sx, sy, sz, acc3 || (q.acc || b.acc[q.side]), fs2, true); if (acc3b && w3 > .02) { const ga = ctx.globalAlpha; ctx.globalAlpha = ga * w3; drawSide(ctx, q.k, sx, sy, sz, acc3b, fs2, true); ctx.globalAlpha = ga; } // v416 cross-fade to the next pose""")
rep("""      let acc3 = null; for (let j = vc - 1; j >= 0; j--) {""", """      let acc3 = null, acc3b = null, w3 = 0; for (let j = vc - 1; j >= 0; j--) {""")
rep("""const ra = (b.cdAng || {})[m.s] || 0, dx0 = fc * Lg * .47, dy0 = Lg * .152; m.ox = S0.x + Math.cos(ra) * dx0 - Math.sin(ra) * dy0; m.oy = S0.y + Math.sin(ra) * dx0 + Math.cos(ra) * dy0; /* v413 the dish turns with the hull */""",
    """const ph = (b.cdPhi || {})[m.s] == null ? CD_PHI0 : b.cdPhi[m.s]; m.ox = S0.x + fc * Lg * .491 * Math.cos(ph); m.oy = S0.y - Lg * .491 * Math.sin(ph); /* v416 the dish where the turned station holds it */""")
t = t.replace("const GAME_V = 415;", "const GAME_V = 416;")
open(p, "w").write(t); print("ok")
