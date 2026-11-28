"""v843: Magma Egg's painting repaired (its top was sliced flat) and its sphere map rebuilt; Magma Egg to Epic, Hellgate to Mythic
(owner: "fix magma egg skin being cut off up top and then we need to move that one and hellgate to a higher tier like epic or mythical")."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 842;", "const GAME_V = 843;")
rep('["atoll singular magma obsidian eden mirror hive tidal rust reef hellgate pr1 pr2 pr4 pr6 pr8 aeon ruin sphinx petrified omen"]', '["atoll singular obsidian eden mirror hive tidal rust reef pr1 pr2 pr4 pr6 pr8 aeon ruin sphinx petrified omen"]')
rep('["spire sapphire ember forge pearl saturn lattice clockwork countdown"]', '["spire sapphire ember forge pearl saturn lattice clockwork countdown magma"]')
rep('["glacier shatter thunder garden emerald abyssreef cntdebris mimichive signal pr3"]', '["glacier shatter thunder garden emerald hellgate abyssreef cntdebris mimichive signal pr3"]')
open(p, "w", encoding="utf-8").write(s); print("ok")
