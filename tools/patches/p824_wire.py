"""v824: the base on phones and tablets, lighter and steadier (owner: "the app still feels a little laggy especially in base view ... any
suggestions on how we can get 60 fps stable"; then "Do that"). From the owner's own performance reports (Android app, Mali-G68 tablet,
v822): the base drew 9-17 fps with frames of ~60 ms at pixel ratio 1 (the resolution manager had already given up all it could) and
~2 million triangles on screen; it is geometry and script bound, not pixel bound. In the harness the colonists alone were ~300k triangles
(46 figures of ~3,000 each, a few pixels tall) and the ground grid 51k. Now on phones and tablets: colonists are built with 35% of the
segments (min 5) and at most 22 of them, the ground grid is 96x96 (was 160x160), and a device that cannot hold 60 fps at its lowest
resolution locks to a steady 30 (fpsCap: the player's own cap, else the automatic one; retried every 2 minutes) instead of swinging."""
import sys, re
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 823;", "const GAME_V = 824;")
# colonists: fewer and lighter on mobile
rep("N = clamp(6 + Math.round(lv * .9), 6, 46)", "N = clamp(6 + Math.round(lv * .9), 6, MOBILE ? 22 : 46)", 2)
i = s.index("function folkBuild(W, bt) {"); j = s.index("\nfunction ", i + 10); body = s[i:j]
def sg(m):
    args = [a.strip() for a in m.group(2).split(",")]
    idx = {"CylinderGeometry": [3], "SphereGeometry": [1, 2], "TorusGeometry": [2, 3], "ConeGeometry": [2], "CapsuleGeometry": [2, 3]}.get(m.group(1), [])
    for k in idx:
        if k < len(args) and re.fullmatch(r"\d+", args[k]): args[k] = f"FSG({args[k]})"
    return f"new TH.{m.group(1)}({', '.join(args)})"
body2 = re.sub(r"new TH\.(CylinderGeometry|SphereGeometry|TorusGeometry|ConeGeometry|CapsuleGeometry)\(([^()]*)\)", sg, body)
n = body2.count("FSG("); assert n > 20, n
s = s[:i] + body2 + s[j:]
rep("function folkBuild(W, bt) {", "const FSG = n => MOBILE ? Math.max(5, Math.round(n * .35)) : n; /* v824 colonists with fewer segments on phones and tablets */\nfunction folkBuild(W, bt) {")
# the ground grid
rep("const gg = new TH.PlaneGeometry(220, 220, 160, 160)", "const gg = new TH.PlaneGeometry(220, 220, MOBILE ? 96 : 160, MOBILE ? 96 : 160) /* v824 */")
# one frame cap: the player's, else the automatic 30 fps lock
rep('{ const cap = gfx("fps"); if (cap && cap < gfxHz() - 3 && !battle && t - (frame.drawn || 0) < 1000 / cap - 1.5)', '{ const cap = fpsCap(); if (cap && cap < gfxHz() - 3 && !battle && t - (frame.drawn || 0) < 1000 / cap - 1.5)')
rep('const capped = () => { const c = gfx("fps");', 'const capped = () => { const c = fpsCap();')
rep('function gfxAimMs() { const cap = gfx("fps"),', 'function fpsCap() { return gfx("fps") || (G && G.autoCap) || 0; } /* v824 */\nfunction gfxAimMs() { const cap = fpsCap(),')
rep("function adaptRes(t) {\n  const dt = t - (frame.last || t); frame.last = t; if (dt > 0 && dt < 200) frame.ema = (frame.ema || 16.7) * .94 + dt * .06;",
    """function adaptRes(t) {
  const dt = t - (frame.last || t); frame.last = t; if (dt > 0 && dt < 200) frame.ema = (frame.ema || 16.7) * .94 + dt * .06;
  /* v824 a phone or tablet that cannot hold 60 fps even at its lowest resolution locks to a steady 30 (judder between 40 and 60 feels worse
     than a smooth 30); every 2 minutes the lock lifts once to see whether 60 has become possible */
  if (MOBILE && !gfx("fps") && !battle && (view === "base" || view === "galaxy")) { const L = adaptRes.lk || (adaptRes.lk = { slow: 0, at: 0 }), W0 = view === "galaxy" ? G3 : C3, low = !W0 || !W0.renderer || W0.renderer.getPixelRatio() <= 1.05;
    if (!G.autoCap) { if (frame.ema > 23 && low) { if (++L.slow >= 90) { G.autoCap = 30; L.at = t; crumb("auto 30 fps lock (frame " + frame.ema.toFixed(1) + " ms)"); } } else L.slow = Math.max(0, L.slow - 2); }
    else if (t - L.at > 120000) { G.autoCap = 0; L.slow = 0; crumb("auto 30 fps lock lifted to retry"); } }""")
open(p, "w", encoding="utf-8").write(s); print("ok", n, "segment counts scaled")
