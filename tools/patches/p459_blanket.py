# v459 Vaelthar: the photon storm now blankets the whole map (a plasma sheet over the galaxy floor and photons raining everywhere, many
# where you are looking), and when he falls he turns to clear crystal that dissolves into rising spirits (see p459_blanket.js).
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
JS = open('tools/patches/p459_blanket.js').read()
rep("function sbBoomTick(X, t) {", JS + "function sbBoomTick(X, t) {")
rep("const Z = X.vs; Z.g.visible = on; if (!on) { Z.hit.clear(); Z.killed = 0; return 0; }", "const Z = X.vs; Z.g.visible = on; if (!on) { Z.hit.clear(); Z.killed = 0; if (X.vbk) X.vbk.g.visible = false; return 0; }")
rep("  return k; }\n/* the storm's camera", "  sbVaeBlanket(W, X, O, t, sec, dur, k); return k; }\n/* the storm's camera")
# the fall, in the preview: no shrinking away; he turns to crystal, frozen, and dissolves; the relic appears once he is gone
rep('if (X.fall && s > X.fall) scl *= P.key === "vae" ? Math.max(.001, 1 - clamp((s - X.fall - .6) / 2.5, 0, 1)) : 1;', '')
rep("  if (P.key === \"vae\") sbVae(X, W, b, s, t, dt, say, yaw, side); else sbAex(X, W, b, s, t, dt, say, yaw, side);\n  b.tick(t);",
    "  if (P.key === \"vae\") sbVae(X, W, b, s, t, dt, say, yaw, side); else sbAex(X, W, b, s, t, dt, say, yaw, side);\n  if (!(P.key === \"vae\" && X.fall && sbVaeCrystal(W, X, b, s - X.fall, t))) b.tick(t);")
rep("if (X.fall && !X.relic && s > X.fall + 2) {", "if (X.fall && !X.relic && s > X.fall + 6.5) {")
rep(": s < 84 ? { y: 70, d: 460, th: .3, ph: -.45 + (s - 58) * .02 } : { y: 40, d: 1000, th: .55, ph: .3 };", ": s < 84 ? { y: 70, d: 460, th: .3, ph: -.45 + (s - 58) * .02 } : s < 93 ? { y: 55, d: 470, th: .26, ph: .4 + (s - 84) * .03 } : { y: 40, d: 900, th: .5, ph: .65 };")
# live: the same, timed from the record's moment of death
rep("if (k === \"vae\") { if (dead) scl *= Math.max(.001, 1 - clamp((df - .6) / 2.5, 0, 1)); b.grp.scale.setScalar(scl);",
    "if (k === \"vae\") { b.grp.scale.setScalar(scl); if (dead) { X.flash.material.opacity = Math.max(X.flash.material.opacity, bell01(df, .2, .55, 1.0, 3)); X.flash.scale.setScalar(D.sc * 60); }")
rep("  b.tick(t); W.renderer.toneMappingExposure = X.exp * (1 - (b.dark || 0) * .4) * (X.expK || 1); }",
    "  if (!(k === \"vae\" && dead && sbVaeCrystal(W, X, b, df, t))) b.tick(t); W.renderer.toneMappingExposure = X.exp * (1 - (b.dark || 0) * .4) * (X.expK || 1); }")
s = re.sub(r"GAME_V = 458\b", "GAME_V = 459", s)
open(P, 'w').write(s)
