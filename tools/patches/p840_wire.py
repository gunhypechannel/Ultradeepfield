"""v840: hull colours on the last five premium tiers only, two per tier and the rest at the top (owner: "Release hull color changes to
last 5 premium levels only two per level and remaining in final level")."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 839;", "const GAME_V = 840;")
rep("Object.entries({ copper: 11, silver: 11, diamond: 11, cobalt: 12, ruby: 12, gold: 13, pink: 13, emerald: 14, amethyst: 14, obsidian: 15 }).forEach(([k, t]) => { if (HULL_F[k]) HULL_F[k].t = t; });",
    "Object.entries({ copper: 12, silver: 12, cobalt: 13, gold: 13, pink: 14, amethyst: 14, diamond: 15, ruby: 15, emerald: 16, obsidian: 16, glyph: 16 }).forEach(([k, t]) => { if (HULL_F[k]) HULL_F[k].t = t; }); /* v840 the last five tiers, two each, the rest at the top */")
open(p, "w", encoding="utf-8").write(s); print("ok")
