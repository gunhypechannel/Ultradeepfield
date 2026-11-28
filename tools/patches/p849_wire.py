"""v849: the Mimics glow: breathing lights, wind-ups, elements, lingering hits, halos, and the Omega link (see p849_glow.js)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 848;", "const GAME_V = 849;")
js = open(__file__.rsplit('/', 1)[0] + "/p849_glow.js", encoding="utf-8").read()
rep("/* the tethers to Omega, and a Pylon's dying snap */", js + "/* the tethers to Omega, and a Pylon's dying snap */")
# 1 the breathing lights, in the sculpt material (per structure: the Node's brain ripples, the Pylon's lights climb, the Nexus's eye swells)
rep('''function mimSculptMat() { if (mimSculptMat.M) return mimSculptMat.M; const b = cntMeshMat(), m = b.clone(); m.envMapIntensity = .85;''',
    '''const MIM_BREATH = { mnode: "(.7 + .9 * pow(.5 + .5 * sin(uMT * 2.0944 - length(vMP - vec3(0., 1.3, 0.)) * 3.), 4.))", mpylon: "(.7 + 1.1 * pow(.5 + .5 * sin(uMT * 1.0472 - vMP.y * 1.4), 6.))", mnexus: "(.8 + .7 * (.5 + .5 * sin(uMT * 1.0472)) * (1. + 1.5 * (1. - smoothstep(.6, 1.6, length(vMP - vec3(0., 3.6, 0.))))))" };
function mimSculptMat(k) { const B = MIM_BREATH[k] ? k : ""; mimSculptMat.C = mimSculptMat.C || {}; if (mimSculptMat.C[B]) return mimSculptMat.C[B]; const b = cntMeshMat(), m = b.clone(); m.envMapIntensity = .85;''')
rep('''.replace("totalEmissiveRadiance += vEm;", "totalEmissiveRadiance += vEm * 1.9; { float fr''', '''.replace("totalEmissiveRadiance += vEm;", "totalEmissiveRadiance += vEm * 2.3; { float fr''')
rep('''m.onBeforeCompile = obc; m.userData.obc = obc; m.userData.pulse = "(1. + 1.5 * pow(.5 + .5 * sin(uMT * 1.6 + vMP.x * 1.1), 10.) + .8 * pow(.5 + .5 * sin(uMT * 1.6 + vMP.x * 1.1 - .9), 10.))"; m.customProgramCacheKey = () => "mimsculpt4"; return mimSculptMat.M = m; }''',
    '''m.onBeforeCompile = obc; m.userData.obc = obc; m.userData.pulse = B ? MIM_BREATH[B] : "(.8 + .45 * (.5 + .5 * sin(uMT * 1.0472)) + 1.5 * pow(.5 + .5 * sin(uMT * 1.6 + vMP.x * 1.1), 10.) + .8 * pow(.5 + .5 * sin(uMT * 1.6 + vMP.x * 1.1 - .9), 10.))"; m.customProgramCacheKey = () => "mimsculpt5" + B; return mimSculptMat.C[B] = m; }''')
rep("const g = new TH.Group(), m = new TH.Mesh(MIM_GEO[k], mimSculptMat());", "const g = new TH.Group(), m = new TH.Mesh(MIM_GEO[k], mimSculptMat(k));")
# 2 the wind-ups, 4 the marks
rep("big ? .28 : .1); m.hx = x; m.hy = y; m.ht = T; };", "big ? .28 : .1); m.hx = x; m.hy = y; m.ht = T; try { mimMark(b, m, T); } catch (e) {} };")
rep("    if (MIMX_DUR[m.a]) { if (alive) mimAtkX(", "    if (alive && u < .25 && !/^(synapse|command|adapt)$/.test(m.a)) mimCharge(ctx, b, m, u, S0, E0, Lg, d, T); /* v849 the wind-up */\n    if (MIMX_DUR[m.a]) { if (alive) mimAtkX(")
rep('''function mimStructX(ctx, b, m, u, S0, E0, Lg, C, gl, d, T, t, scr, hit, pan) {
  const side = b.Q[m.s].side; ctx.save(); ctx.globalCompositeOperation = "lighter";''', '''function mimStructX(ctx, b, m, u, S0, E0, Lg, C, gl, d, T, t, scr, hit, pan) {
  mimStructCharge(ctx, b, m, u, S0, E0, Lg, d, T); const side = b.Q[m.s].side; ctx.save(); ctx.globalCompositeOperation = "lighter";''')
rep('''ctx.globalAlpha = 1 - k; ctx.strokeStyle = `rgba(${col},1)`; ctx.lineWidth = wd; ctx.beginPath(); ctx.moveTo(cy.x, cy.y); ctx.lineTo(E0.x, E0.y); ctx.stroke(); ctx.strokeStyle = "rgba(255,255,255,1)"; ctx.lineWidth = wd * .3; ctx.stroke();''',
    '''mimPrismBeam(ctx, cy.x, cy.y, E0.x, E0.y, k, d); ctx.globalAlpha = 1 - k; ctx.strokeStyle = `rgba(${col},1)`; ctx.lineWidth = wd; ctx.beginPath(); ctx.moveTo(cy.x, cy.y); ctx.lineTo(E0.x, E0.y); ctx.stroke(); ctx.strokeStyle = "rgba(255,255,255,1)"; ctx.lineWidth = wd * .3; ctx.stroke();''')
# 5 the halos and the structures at rest (with the marks), beside the drips and mist
rep("if (!lo) try { mimAmbient(ctx, b, scr, T, d); } catch (e) {}", "if (!lo) try { mimAmbient(ctx, b, scr, T, d); mimGlow(ctx, b, scr, T, d); } catch (e) {}")
# 6 the Omega link: a charging Node or Pylon sends a fast bright pulse up its tether, and Omega flares
rep('''  const was = b.tAlive || (b.tAlive = {}); ctx.save(); ctx.globalCompositeOperation = "lighter";''', '''  const was = b.tAlive || (b.tAlive = {}); ctx.save(); ctx.globalCompositeOperation = "lighter";
  const chg = {}; for (const m of b.mAtk || []) { const u = (T - m.t0) / (MIM_DUR[m.a] || 1); if ((m.a === "synapse" || m.a === "adapt") && u >= 0 && u < .5) chg[m.s] = u / .5; }''')
rep('''      ctx.globalAlpha = .8 * Math.sin(Math.PI * k); ctx.drawImage(glowSprite(`rgba(${col},1)`), x - r, y - r, r * 2, r * 2); } } /* the pulses run toward Omega, slowly */''',
    '''      ctx.globalAlpha = .8 * Math.sin(Math.PI * k); ctx.drawImage(glowSprite(`rgba(${col},1)`), x - r, y - r, r * 2, r * 2); } /* the pulses run toward Omega, slowly */
    if (chg[i] != null) { const k = chg[i], x = (1 - k) * (1 - k) * sx + 2 * (1 - k) * k * ((sx + O.x) / 2) + k * k * O.x, y = (1 - k) * (1 - k) * sy + 2 * (1 - k) * k * (Math.min(sy, O.y) - LO * .3) + k * k * O.y, r = Math.max(5 * d, Lg * .16);
      ctx.globalAlpha = .55; ctx.lineWidth = 2.6 * d; ctx.beginPath(); ctx.moveTo(sx, sy); ctx.quadraticCurveTo((sx + O.x) / 2, Math.min(sy, O.y) - LO * .3, O.x, O.y); ctx.stroke(); ctx.globalAlpha = 1; ctx.drawImage(glowSprite(`rgba(${col},1)`), x - r, y - r, r * 2, r * 2); ctx.drawImage(glowSprite("#ffffff"), x - r * .35, y - r * .35, r * .7, r * .7);
      if (k > .75) { const f = (k - .75) / .25, R = LO * (.35 + .25 * f); ctx.globalAlpha = Math.sin(Math.PI * f) * .7; ctx.drawImage(glowSprite(`rgba(${col},1)`), O.x - R, O.y - R, R * 2, R * 2); } } } /* v849 the charge races up the line, and Omega flares in answer */''')
open(p, "w", encoding="utf-8").write(s); print("ok")
