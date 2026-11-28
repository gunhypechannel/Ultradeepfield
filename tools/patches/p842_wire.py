"""v842: the shop's levels by silhouette (owner: "Dread skull should be an epic or legendary? Anything that exceeds past the planets normal
circle or sphere shape is consider more unique and should be the higher cost skins and others should be in the uncommon tier")."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 841;", "const GAME_V = 842;")
rep('''const PX_BAND_OF = {}; [["aurora dune lavalamp abyss plague ruins kraken stormtitan frostfire ghost"], ["warsphere rust bonemoon dread spire colossus thunder tidal reef glacier nigiri watcher"],
  ["ruby sapphire emerald amethyst garden clockwork cyber venom bloom shatter ember obsidian pr1 pr2"], ["atoll aurum inferno magma forge pearl eden mirror lattice phoenix hive hellgate saturn singular pr4"],
  ["solar pr6 pr8"], ["aeon ruin sphinx petrified omen countdown signal abyssreef cntdebris mimichive pr3"]]''',
'''/* v842 by silhouette: plain spheres are Uncommon; the more a world breaks out of its sphere (spikes, rings, cannons, faces, a dragon,
   floating islands), the higher it sits. The four forged event worlds (drawn in code, no painting yet) stay Mythic. */
const PX_BAND_OF = {}; [["aurora dune lavalamp abyss plague ruins kraken stormtitan frostfire ghost"],
  ["atoll singular magma obsidian eden mirror hive tidal rust reef hellgate pr1 pr2 pr4 pr6 pr8 aeon ruin sphinx petrified omen"],
  ["venom bonemoon ruby phoenix solar"], ["spire sapphire ember forge pearl saturn lattice clockwork countdown"],
  ["dread warsphere cyber colossus amethyst aurum inferno watcher bloom nigiri"], ["glacier shatter thunder garden emerald abyssreef cntdebris mimichive signal pr3"]]''')
open(p, "w", encoding="utf-8").write(s); print("ok")
