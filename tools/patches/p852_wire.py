"""v852: planet skin tiers (owner: "abyssal reef, machine debris, neural hive, and signal lattice to epic, shattered bastion to rare")."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 851;", "const GAME_V = 852;")
rep('["venom ruby phoenix solar pr8 tidal rust hive petrified ruin sphinx singular"], ["spire sapphire ember forge pearl saturn lattice clockwork countdown magma bonemoon"],',
    '["venom ruby phoenix solar pr8 tidal rust hive petrified ruin sphinx singular shatter"], ["spire sapphire ember forge pearl saturn lattice clockwork countdown magma bonemoon abyssreef cntdebris mimichive signal"],')
rep('["glacier shatter thunder garden emerald hellgate abyssreef cntdebris mimichive signal"]', '["glacier thunder garden emerald hellgate"]')
open(p, "w", encoding="utf-8").write(s); print("ok")
