"""v784: fleets on the galaxy map no longer dwarf the planets (owner, with a map screenshot: "should we remove this fleet from attack
animation or resize it? it's way too big"). Each fleet's hull was sized by strength up to 2.1 planet diameters, and a joint strike's
armada grew by 5% per commander on top; the strongest fleets were bigger than the worlds they flew past. Now the tiers span .55, .7,
.85 and 1.0 of a planet's diameter (was 1.05, 1.35, 1.7, 2.1), never more than one planet, and a joint strike adds 2% per commander
(was 5%, from 1.15). The fleet still flies out so you see your attack underway. Applies on top of v783."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 783;", "const GAME_V = 784;")
rep("const FLEET_SPAN = [1.05, 1.35, 1.7, 2.1];", "const FLEET_SPAN = [.55, .7, .85, 1.0]; /* v784 never bigger than a planet (was 1.05 to 2.1) */")
rep("tgt = Math.min(2.6, FLEET_SPAN[fleetTier(n)] * (extra || 1)) * PL_D;", "tgt = Math.min(1.15, FLEET_SPAN[fleetTier(n)] * (extra || 1)) * PL_D;")
rep("grp.userData.size = fleetSzOf(f.n, grp, 1.15 + Math.min(.5, (f.cnt || 1) * .05));", "grp.userData.size = fleetSzOf(f.n, grp, 1.05 + Math.min(.15, (f.cnt || 1) * .02));")
open(p, "w", encoding="utf-8").write(s)
print("ok")
