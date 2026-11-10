# v412 (1): the home base on phones. Field reports show 11.6% of iPhone base frames over 34 ms (3.6% on the map): the base is GPU-bound
# (bloom = a 4x-multisampled full-screen scene target plus five passes, soft shadows, ~324k triangles). (a) On a phone that falls behind
# its frame target on the base, the resolution manager now sheds bloom first (two slow checks in a row), before any resolution is given
# up; bloom returns after 30 s with real headroom at full resolution. (b) The 140 background domes use 24x9 segments (lite 18x7) instead of
# 40x14 (28x10): 151k triangles down to about 60k, the same at the size they are seen.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("new TH.SphereGeometry(1, lite ? 28 : 40, lite ? 10 : 14, 0, TAU, 0, Math.PI / 2).translate(0, .28, 0), domeM, N)", "new TH.SphereGeometry(1, lite ? 18 : 24, lite ? 7 : 9, 0, TAU, 0, Math.PI / 2).translate(0, .28, 0), domeM, N)")
rep("{ const B = colBloom(W); let ok = false;", "{ const B = W.bloomOff ? null : colBloom(W); let ok = false;")
i = t.index("  const aim = Math.max(gfxAimMs(), 1000 / 125), A = adaptRes.s"); j = t.index("\n", i) + 1
t = t[:j] + """  if (W === C3 && MOBILE && !capped()) { /* v412: a phone sheds the base's bloom before any resolution */ if (!W.bloomOff && W.bloom && frame.ema > aim * 1.2) { if ((A.bb = (A.bb || 0) + 1) >= 2) { W.bloomOff = t; A.bb = 0; A.bad = 0; crumb("base bloom off (frame " + frame.ema.toFixed(1) + " ms)"); return; } } else A.bb = 0;
    if (W.bloomOff && frame.ema < aim * .75 && R.getPixelRatio() >= max - .01 && t - W.bloomOff > 30000) { W.bloomOff = 0; crumb("base bloom back"); } }
""" + t[j:]
t = t.replace("const GAME_V = 411;", "const GAME_V = 412;")
open(p, "w").write(t); print("ok")
