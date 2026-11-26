"""v804: Aetherion stage 4 (behind the owner switch "aet"): the Silent Dominion and the Primordial Tide, their targets and
cooperative bosses (event/aet_boss_<k>, weekly), the Silent Archive from the Central Nexus, and two new Archive records (drafts)."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
C = open(os.path.join(D, "p804_aet.js"), encoding="utf-8").read()
AR = open(os.path.join(D, "p804_arch.js"), encoding="utf-8").read()
rep("const GAME_V = 803;", "const GAME_V = 804;")
rep("\nconst PIRATES = PIRATES_ALL.filter(", "\n" + C + "\nconst PIRATES = PIRATES_ALL.filter(")
rep('ARCH_ORD.push("ae_vesper", "ae_living", "ae_nhalis", "ae_aperture", "ae_builders");', 'ARCH_ORD.push("ae_vesper", "ae_living", "ae_nhalis", "ae_aperture", "ae_builders");\n' + AR)
open(p, "w", encoding="utf-8").write(s)
print("ok")
