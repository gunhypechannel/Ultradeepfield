"""v810: a cloud save that loads in after boot (sign-in, new phone, reinstall) re-asks the faction / starts the prologue when that save
never got that far. Before, the question had already been spent on the empty boot save, so a player who had left during the opening
film came back to a base with no faction, no prologue and no guidance (seen: Drave, 2026-11-26, Android app, v779)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 809;", "const GAME_V = 810;")
rep("""render(true); toast(foreign ? "Signed in. Loaded this account's empire." : "Loaded your saved empire.", "win"); }""",
    """render(true); toast(foreign ? "Signed in. Loaded this account's empire." : "Loaded your saved empire.", "win");
            if ((!S.faction || !S.intro) && G.askFac0) { if (!S.faction) S.facAsked = 0; G.askFac = G.askFac0; setTimeout(() => { if (G.askFac && !(sheet && sheet.type === "faction")) G.askFac(); }, 700); } } /* v810 a save that never got past the faction or the prologue picks up there */""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
