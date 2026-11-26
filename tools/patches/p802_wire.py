"""v802: Dimensional Expeditions (behind the owner switch "aet"): the Shattered Expanse (harvesting stations, mining platforms, anomalies,
Aetherion deposits, predator packs), Aetherion Technology (six branches), the Aetherion Exchange, daily expedition orders, the alliance
weekly gathering objective, reward claims recorded once by the server (aet_claim)."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
C = open(os.path.join(D, "p802_aet.js"), encoding="utf-8").read()
CSS = open(os.path.join(D, "p802.css"), encoding="utf-8").read().replace("\n", "")
rep("const GAME_V = 801;", "const GAME_V = 802;")
rep("\nconst PIRATES = PIRATES_ALL.filter(", "\n" + C + "\nconst PIRATES = PIRATES_ALL.filter(")
i = s.index("</style>"); s = s[:i] + CSS + s[i:]
open(p, "w", encoding="utf-8").write(s)
print("ok")
