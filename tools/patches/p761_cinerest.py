"""v761: the 3D scene rests behind full-screen story films (onboarding stutter on low-end Android).
Daily Academy check (2026-11-25): every new commander since 2026-11-24 stopped before Academy step 1, during the opening film
"Before the Darkness" or the faction picker right after it. A new player's perf report (Android 10, Mali-G77) showed freezes of
1.0-2.7 s every second or two through that time. The film (#cine) covers the whole screen in black, yet the colony's 3D base kept
drawing at full rate behind it (measured in the harness: ~200 draw calls a second, the same as with the base on screen), while the
models were still loading. Now, like the 3D Sanctuary (v758), a story film caps the scene behind it at 3 fps; it picks up again the
moment the film ends. Battles are untouched (the prologue's ambush is its own screen). Applies on top of v760."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 760;", "const GAME_V = 761;")
rep("""function sheetCap() { if (G.xs3 && !battle) return 3; /* v758 the 3D Sanctuary covers the screen */""",
    """function sheetCap() { if (G.xs3 && !battle) return 3; /* v758 the 3D Sanctuary covers the screen */ if (!battle && document.getElementById("cine")) return 3; /* v761 a story film covers the screen: the base or map behind it rests */""")
open(p, "w", encoding="utf-8").write(s)
