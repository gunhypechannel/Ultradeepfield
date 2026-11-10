# v411: the Wyrm breathes its beam from its mouth in the battle report. The model gets a `mouth` anchor between its jaws; wbArt projects it
# through the report camera each frame (WBR.mouth, 0..1 across the art) and the report records where the art is drawn (b.wbBox), so
# wbStrike can start the Wyrm's beams at its mouth instead of the middle of the boss. Its own attack: the jaws gape and a golden charge
# swells in the mouth, then a thick beam with travelling halo rings (like its lens on the map) runs from the mouth to the fleet; the
# sweep rakes that beam across the fleet from the mouth. The model's own 3D lens beam is hidden in the report, so only the aimed beam shows.
import sys
def patch(p, reps):
    t = open(p).read()
    for a, b in reps:
        assert t.count(a) == 1, (p, t.count(a), a[:90]); t = t.replace(a, b)
    open(p, "w").write(t)
model = [("const lens = new TH.Group(); lens.position.set(0, .35, 7.4); hd.add(lens);", "const mouth = new TH.Object3D(); mouth.position.set(0, .33, 2.6); hd.add(mouth); const lens = new TH.Group(); lens.position.set(0, .35, 7.4); hd.add(lens);"),
         ("bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 15, h: 11, own: [hole, disc, disc2, phR, bhG] };", "bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 15, h: 11, own: [hole, disc, disc2, phR, bhG], mouth, lens };")]
patch("assets/bosses/model/boss3d.js", model)
patch("docs/index.html", model + [
 ("    WBR.b.tick(t); WBR.r.render(WBR.sc, WBR.cam); return WBR.r.domElement; } catch (e) { return null; } }",
  "    WBR.b.tick(t); if (WBR.b.lens && WBR.b.mouth) WBR.b.lens.visible = false; WBR.r.render(WBR.sc, WBR.cam); if (WBR.b.mouth) { const v = (WBR.mv3 || (WBR.mv3 = new TH.Vector3())); WBR.b.mouth.getWorldPosition(v).project(WBR.cam); WBR.mouth = { u: (v.x + 1) / 2, v: (1 - v.y) / 2 }; } else WBR.mouth = null; /* v411 the Wyrm's mouth, for its beams */ return WBR.r.domElement; } catch (e) { return null; } }"),
 ("if (A) ctx.drawImage(wbSoft(A), -aw / 2, -ah / 2, aw, ah); }", "if (A) ctx.drawImage(wbSoft(A), -aw / 2, -ah / 2, aw, ah); b.wbBox = { cx, cy, aw, ah }; }"),
 ("""  const S = (WB_STRIKE[k] || {})[M.m]; if (!S) return; const f = (t - M.t0) / S[4]; if (f < S[1] || f > S[2]) return; const u = (f - S[1]) / (S[2] - S[1]), env = Math.sin(Math.min(1, u) * Math.PI);""",
  """  const S = (WB_STRIKE[k] || {})[M.m]; if (!S) return; const f = (t - M.t0) / S[4], MO = k === "wym" && WBR.mouth && b.wbBox ? { x: b.wbBox.cx + (WBR.mouth.u - .5) * b.wbBox.aw, y: b.wbBox.cy + (WBR.mouth.v - .5) * b.wbBox.ah } : null; /* v411 the Wyrm fires from its mouth */
  if (MO && f < S[1] && f > S[1] - .16) { const q = 1 - (S[1] - f) / .16, r = (8 + 46 * q) * d; ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.globalAlpha = .4 + .6 * q; ctx.drawImage(glowSprite("rgba(255,170,60,1)"), MO.x - r * 2, MO.y - r * 2, r * 4, r * 4); ctx.drawImage(glowSprite("#fff2d8"), MO.x - r * .6, MO.y - r * .6, r * 1.2, r * 1.2); ctx.strokeStyle = "#ffcf7a"; ctx.lineWidth = 2 * d; for (let j = 0; j < 3; j++) { const rr = r * (2.6 - ((q * 1.8 + j / 3) % 1) * 2); ctx.globalAlpha = .7 * q; ctx.beginPath(); ctx.ellipse(MO.x, MO.y, rr, rr * .7, 0, 0, TAU); ctx.stroke(); } ctx.restore(); return; }
  if (f < S[1] || f > S[2]) return; const u = (f - S[1]) / (S[2] - S[1]), env = Math.sin(Math.min(1, u) * Math.PI);"""),
 ("""  const cx = b.scC.x, cy = b.scC.y, F = M.fx""", """  const cx = MO ? MO.x : b.scC.x, cy = MO ? MO.y : b.scC.y, F = M.fx"""),
 ("""    if (k === "epx") els.forEach((c, j) => {""", """    if (MO) { const dx = x1 - cx, dy = y1 - cy, Ln = Math.hypot(dx, dy) || 1, nx = -dy / Ln, ny = dx / Ln; for (let j = 0; j < 5; j++) { const p = ((t * .0012 + j / 5) % 1) * grow, hx = cx + dx * p, hy = cy + dy * p, rr = (16 + 22 * p) * d; ctx.globalAlpha = .75 * env * (1 - p * .5); ctx.strokeStyle = "#ffe0b0"; ctx.lineWidth = 2.5 * d; ctx.beginPath(); ctx.ellipse(hx, hy, rr, rr * .32, Math.atan2(ny, nx), 0, TAU); ctx.stroke(); } glow(cx, cy, W * .09, "#fff2d8", env); } /* v411 the Wyrm's halo rings ride its beam out of the mouth */
    if (k === "epx") els.forEach((c, j) => {"""),
])
t = open("docs/index.html").read().replace("const GAME_V = 410;", "const GAME_V = 411;"); a = "wyrm: [0, [-5, 15, 40], [0, 2.5, 0]]"; assert t.count(a) == 1; t = t.replace(a, "wyrm: [0, [-6, 21, 52], [0, 10, 0]]")  # its head stays in frame
open("docs/index.html", "w").write(t); print("ok")
