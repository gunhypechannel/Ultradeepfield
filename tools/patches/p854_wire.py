"""v854: Celestial Garden takes Premium Tier 3; Void Bloom goes to the shop's Mythic tier (owner: "switch celestial and void bloom premium planet skin")."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 853;", "const GAME_V = 854;")
rep('["glacier thunder garden emerald hellgate dread colossus amethyst inferno dragon"]]', '["glacier thunder voidbloom emerald hellgate dread colossus amethyst inferno dragon"]]')
rep("PREM_OLD.dragon = 2; } } /* v853 */", '''PREM_OLD.dragon = 2; } } /* v853 */
{ const P = PREM[3], s = PXS.garden, o = PXS.voidbloom; if (P && s && o && P.k === "voidbloom") { delete o.prem; o.cost = 1; o.r = "all"; s.prem = 3; s.cost = 0; s.r = "all"; s.b = +(.12 + .012 * 3).toFixed(3); P.k = "garden"; P.n = s.n; P.col = s.glow || P.col; PREM_OLD.voidbloom = 3; } } /* v854 */''')
rep("if (S.pxPKV !== 2) { try {", "if (S.pxPKV !== 3) { try {")
rep("S.pxPKV = 2; dirty();", "S.pxPKV = 3; dirty();")
open(p, "w", encoding="utf-8").write(s); print("ok")
