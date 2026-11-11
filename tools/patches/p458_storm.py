# v458 Vaelthar: the wheel leans with him instead of folding into his body, and Divine Annihilation becomes a photon storm that bursts in
# every direction and blankets the map, with its own cinematic camera (see p458_storm.js).
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
JS = open('tools/patches/p458_storm.js').read()
# the wheel stays fixed to his back and tips forward with him (a little further than his body), drawn back so it clears his neck and wings
rep("body.rotation.x = Lg * .42; wheel.rotation.set(-Lg * (Math.PI / 2 + .42), 0, 0); wheel.rotateY(.12 * (1 - Lg)); wheel.position.set(0, 11 + Lg * 5, -11 + Lg * 5.5);",
    "body.rotation.x = Lg * .42; wheel.rotation.set(Lg * .22, .12 * (1 - Lg), 0); { const Lw = A < 0 ? 0 : ss(0, .1, A) * (1 - ss(.94, 1, A)); wheel.position.set(0, 12.2 + Lw * 5.5, -11 - Lg * 2.5); }")
rep("st.coil = bell(fr, 0, .2, .8, 1) * .6 + warn * .2;", "st.coil = bell(fr, 0, .2, .8, 1) * .6;")
rep("st.sway = fire * Math.sin((A - .66) / .2 * Math.PI * 1.2 - .6) * .72;", "st.sway = fire * Math.sin((A - .66) / .2 * Math.PI * 1.2 - .6) * .3;")
# the beam is gone: the storm takes its place
i = s.index("/* v455 Divine Annihilation at the scale of the galaxy"); j = s.index("function sbBoomTick(X, t) {"); s = s[:i] + JS + s[j:]
assert "sbVaeBeam(W, X, b, t, 1)" in s
rep("const A0 = 33, AL = 22, fa = (s - A0) / AL;", "const A0 = 33, AL = 24, fa = (s - A0) / AL;")
rep("else X.quiet = false; sbVaeBeam(W, X, b, t, 1); X.expK = 1 + (b.ph === \"beam\" ? (b.fireK || 0) * .35 : 0);",
    "else X.quiet = false; { const sk = sbVaeStorm(W, X, b, t, 1, fa >= 0 ? (fa - .66) * AL : -1, .26 * AL); X.expK = 1 + sk * .4; }")
rep("const K = s < 8 ? { y: 40, d: 900, th: .5, ph: .25 } :", "const K = fa >= .55 && fa < .97 ? sbVaeCam(X, fa) : s < 8 ? { y: 40, d: 900, th: .5, ph: .25 } :")
rep("b.drive(\"annihilate\", fa); sbVaeBeam(W, X, b, t, 0); sbBoomTick(X, t); X.expK = 1 + (b.ph === \"beam\" ? (b.fireK || 0) * .35 : 0);",
    "b.drive(\"annihilate\", fa); { const dt = Math.min(64, t - (X.lt || t)); X.lt = t; const sk = sbVaeStorm(W, X, b, t, 0, fa >= 0 ? (fa - .66) * 180 : -1, 45); sbVaeCine(X, W, fa, dt); X.expK = 1 + sk * .4; } sbBoomTick(X, t);")
assert "sbVaeBeam" not in s
s = re.sub(r"GAME_V = 457\b", "GAME_V = 458", s)
open(P, 'w').write(s)
