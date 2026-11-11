# v413: the Cube Destroyer turns to face its target while it fires. During the charge and the beam (and 0.3 s before), each hull of a
# firing Cube Destroyer formation rotates so its red dish points straight at the target (it is a sphere, so the turn reads as the
# station swinging its dish round); it eases there at about a fifth of a second and eases back once the beam is spent. The beam's
# origin follows the rotated dish (b.cdAng, the lead hull's full turn including its bank).
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("""        ctx.save(); { const ba = bang + (small ? Math.cos(t * .0024 + i * 1.7 + j * 2.3) * .2 * face : 0); if (ba) { ctx.translate(sx, sy); ctx.rotate(ba); ctx.translate(-sx, -sy); } }""",
    """        ctx.save(); { const ba = bang + (small ? Math.cos(t * .0024 + i * 1.7 + j * 2.3) * .2 * face : 0) + (q.k === "worldbreaker" ? (j ? (b.cdRot || {})[i] || 0 : cdTurn(b, i, cx, cy, face, scr, T, real)) : 0); if (!j && q.k === "worldbreaker") (b.cdAng || (b.cdAng = {}))[i] = ba; if (ba) { ctx.translate(sx, sy); ctx.rotate(ba); ctx.translate(-sx, -sy); } }""")
rep("""m.ox = S0.x + fc * Lg * .47; m.oy = S0.y + Lg * .152;""",
    """const ra = (b.cdAng || {})[m.s] || 0, dx0 = fc * Lg * .47, dy0 = Lg * .152; m.ox = S0.x + Math.cos(ra) * dx0 - Math.sin(ra) * dy0; m.oy = S0.y + Math.sin(ra) * dx0 + Math.cos(ra) * dy0; /* v413 the dish turns with the hull */""")
rep("""function drawBattle(t) {""", """/* v413 how far a Cube Destroyer formation has turned so its dish (0.47 L forward, 0.152 L down on the sprite) faces the target it is firing at */
function cdTurn(b, i, cx, cy, face, scr, T, real) { const A = b.cdRot || (b.cdRot = {}), m = (b.beams || []).find(m => m.wb && m.s === i && T - m.t0 > -.3 && T - m.t0 < m.charge + m.life);
  let want = 0; if (m) { const E = scr[m.e] || (m.ix != null ? { x: m.ix, y: m.iy } : null); if (E) { const a0 = Math.atan2(.152, face * .47); want = Math.atan2(E.y - cy, E.x - cx) - a0; want = Math.atan2(Math.sin(want), Math.cos(want)); } }
  const cur = A[i] || 0, d = Math.atan2(Math.sin(want - cur), Math.cos(want - cur)); A[i] = cur + d * Math.min(1, (real || 16) / 200); return A[i]; }
function drawBattle(t) {""")
t = t.replace("const GAME_V = 412;", "const GAME_V = 413;")
open(p, "w").write(t); print("ok")
