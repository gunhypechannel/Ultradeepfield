# v409 (3): the background map warm-up (mapPrewarm) compiles shaders at each step, a stall of up to a second on a phone. Its steps now
# wait while a panel is open, a battle runs, the page is hidden, or the player touched the screen in the last 2.5 s (G.lastIn, set by
# a capture-phase pointerdown listener), so the stall lands in idle time instead of right after a tap.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("""  let n = 0; const step = () => { if (!G3 || view === "galaxy" || !$("#mappark") || !$("#mappark").firstChild) return; try { draw3D(""",
    """  let n = 0; const step = () => { if (!G3 || view === "galaxy" || !$("#mappark") || !$("#mappark").firstChild) return; if (sheet || battle || document.hidden || performance.now() - (G.lastIn || 0) < 2500) { setTimeout(() => requestAnimationFrame(step), 700); return; } /* v409: each step compiles shaders (a stall); never while a panel is open or the player is tapping */ try { draw3D(""")
rep("""/* v409 every 3D renderer is made here:""", """document.addEventListener("pointerdown", () => { G.lastIn = performance.now(); }, { capture: true, passive: true }); // v409 the last touch, for mapPrewarm
/* v409 every 3D renderer is made here:""")
t = t.replace("const GAME_V = 408;", "const GAME_V = 409;")
open(p, "w").write(t); print("ok")
