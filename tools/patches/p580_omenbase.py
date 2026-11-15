# v580 The week's omen band shows on the planet (base) view only, not over the galaxy map (owner: "Can we add this only to base
# view"). Tapping it still flies to the omen on the map and opens its Archives page. Event bands (finales, the Cube) stay on the map.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('  { const ok = omenKey(T), j = OMEN_K.indexOf(ok), E = ARCH["o_" + (j + 1)]; if (ok && E) return `', '  return ""; }\nfunction omenBand(T) { { const ok = omenKey(T), j = OMEN_K.indexOf(ok), E = ARCH["o_" + (j + 1)]; if (ok && E) return `')
rep('if (!html && view === "galaxy" && !sheet && !battle && !G.sbSim && !cineOn) html = finBand(T); /* v571 */',
    'if (!html && view === "galaxy" && !sheet && !battle && !G.sbSim && !cineOn) html = finBand(T); /* v571 */\n  if (!html && view === "base" && !sheet && !battle) html = omenBand(T); /* v580 the week\'s omen: on the planet only */')
s2 = re.sub(r"GAME_V = 579\b", "GAME_V = 580", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
