# v414 (3): the Cube Destroyer turns as a real 3D station. Its battle sprite is baked from the 3D model; the sphere is now also baked
# turned round the camera's line of sight in 12 steps of 30 degrees with the lights fixed (accent "~rN", N = 0..11, baked on demand when a
# Cube Destroyer first fires). Turning, a hull draws the nearest baked step and makes up only the last few degrees (at most 15) by turning
# the picture, so the dish swings round the surface while the light, shadow and equator ring stay true. The turn is slower and heavier
# (eased over about 0.6 s, starting 0.6 s before the charge) and the beam still leaves the dish.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
CD_S = -1
# shipArt: the turned bakes
rep("""  const S = studio(); if (!S || !kind) return null; const key = k + "|" + accent + "|" + view; if (S.cache[key] !== undefined) return S.cache[key];
  try {""", """  const S = studio(); if (!S || !kind) return null; const key = k + "|" + accent + "|" + view; if (S.cache[key] !== undefined) return S.cache[key];
  let rotK = 0; { const mr = /~r(\\d+)$/.exec(String(accent)); if (mr) { rotK = +mr[1]; accent = String(accent).slice(0, mr.index); } } /* v414 a Cube Destroyer turned rotK x 30 degrees round the line of sight */
  try {""")
rep("""    const ex0 = S.renderer.toneMappingExposure; if (FG) S.renderer.toneMappingExposure = .72; S.renderer.render(S.scene, S.camera);""",
    """    if (rotK) { const ax = S.camera.position.clone().normalize(), an = rotK * Math.PI / 6; ship.position.applyAxisAngle(ax, an); ship.rotateOnWorldAxis(ax, an); }
    const ex0 = S.renderer.toneMappingExposure; if (FG) S.renderer.toneMappingExposure = .72; S.renderer.render(S.scene, S.camera);""")
# the hull loop: nearest turned bake + a small residual turn
rep("""+ (q.k === "worldbreaker" ? (j ? (b.cdRot || {})[i] || 0 : cdTurn(b, i, cx, cy, face, scr, T, real)) : 0); if (!j && q.k === "worldbreaker") (b.cdAng || (b.cdAng = {}))[i] = ba; if (ba) { ctx.translate(sx, sy); ctx.rotate(ba); ctx.translate(-sx, -sy); } }""",
    """+ (q.k === "worldbreaker" ? (j ? (b.cdRot || {})[i] || 0 : cdTurn(b, i, cx, cy, face, scr, T, real)) : 0); if (!j && q.k === "worldbreaker") (b.cdAng || (b.cdAng = {}))[i] = ba;
          let rb = ba; acc3 = null; if (q.k === "worldbreaker" && Math.abs((b.cdRot || {})[i] || 0) > .02) { const st = Math.PI / 6, w = CD_S * face * ba, kk = ((Math.round(w / st) % 12) + 12) % 12, base = (q.acc || b.acc[q.side]); if (kk && shipArtSoon("worldbreaker", base + "~r" + kk, "side")) { acc3 = base + "~r" + kk; rb = ba - CD_S * face * Math.round(w / st) * st; } } /* v414 the nearest turned bake, the rest by turning the picture */
          if (rb) { ctx.translate(sx, sy); ctx.rotate(rb); ctx.translate(-sx, -sy); } }""")
t = t.replace("drawSide(ctx, q.k, sx, sy, sz, (q.acc || b.acc[q.side]), fs2, true", "drawSide(ctx, q.k, sx, sy, sz, acc3 || (q.acc || b.acc[q.side]), fs2, true")
t = t.replace("drawSide(ctx, q.k, sx - .9 * d, sy - .9 * d, sz, (q.acc || b.acc[q.side]), fs2, true", "drawSide(ctx, q.k, sx - .9 * d, sy - .9 * d, sz, acc3 || (q.acc || b.acc[q.side]), fs2, true")
rep("""      for (let j = vc - 1; j >= 0; j--) { const o = OFFS[j], sz = L * (j ? .8 : 1),""", """      let acc3 = null; for (let j = vc - 1; j >= 0; j--) { const o = OFFS[j], sz = L * (j ? .8 : 1),""")
# a heavier turn
rep("""m = (b.beams || []).find(m => m.wb && m.s === i && T - m.t0 > -.3 && T - m.t0 < m.charge + m.life);""", """m = (b.beams || []).find(m => m.wb && m.s === i && T - m.t0 > -.6 && T - m.t0 < m.charge + m.life);""")
rep("""A[i] = cur + d * Math.min(1, (real || 16) / 200); return A[i]; }""", """A[i] = cur + d * Math.min(1, (real || 16) / 600); return A[i]; }""")
rep("const CD_S_PLACE = 0;", "") if "const CD_S_PLACE = 0;" in t else None
t = t.replace("function cdTurn(b, i,", "const CD_S = %d; // v414 which way a turned bake turns on screen\nfunction cdTurn(b, i," % CD_S, 1)
open(p, "w").write(t); print("ok", t.count("acc3 || (q.acc"))
