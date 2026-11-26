"""v812: the fast start for brand-new commanders (shorter opening film and prologue, no second battle, build first, name later)."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
C = open(os.path.join(D, "p812_fast.js"), encoding="utf-8").read()
rep("const GAME_V = 811;", "const GAME_V = 812;")
i = s.index("/* v612 the prologue */ // veterans just get"); j = s.index("\n", i) + 1; s = s[:j] + C + s[j:]
rep("if (!S.faction) { S.facAsked = 1; dirty(); if (!S.cinSeen && score() <= 200) cinWhenClear(", "if (!S.faction) { S.facAsked = 1; if (!S.cinSeen && score() <= 200 && !S.proDone) S.fst = 1; /* v812 a brand-new commander: the fast start */ dirty(); if (!S.cinSeen && score() <= 200) cinWhenClear(")
open(p, "w", encoding="utf-8").write(s)
print("ok")
