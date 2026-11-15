# v580 (1) The week's omen band shows on the planet (base) view only, not over the galaxy map (owner: "Can we add this only to base
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
# (2) iPhone/iPad crashes (owner: "Lots of crashes, what else can we do to fix?"). The crash reports showed the phone closing the game
# seconds after the galaxy map was built while the base world was still alive (it was released 8 s later): two 3D worlds at the
# peak of a cold build. On iPhone/iPad the other world is now released before a cold build of either. After a battle closes on
# iPhone/iPad, the studio renderer (an extra WebGL context) is released at once instead of after 15 s idle.
rep('    mapMount(m); { const pk = $("#mappark"); if (pk && !pk.firstChild) pk.remove(); }', '    if (IOS && !mapHost && C3) worldDrop("col", "before the map is built"); /* v580 never two worlds at a cold build */\n    mapMount(m); { const pk = $("#mappark"); if (pk && !pk.firstChild) pk.remove(); }')
rep('if (!colHost.dataset.init) { colHost.dataset.init = "1"; if (use3) { C3 = initColony(colHost);', 'if (!colHost.dataset.init) { colHost.dataset.init = "1"; if (use3) { if (IOS && G3) worldDrop("gal", "before the base is built"); /* v580 */ C3 = initColony(colHost);')
rep('function closeBattle() { if (battle) { crumb("battle closed"); battleFree(battle); wbArtFree(); G.btClosedAt = performance.now(); }', 'function closeBattle() { if (battle) { crumb("battle closed"); battleFree(battle); wbArtFree(); G.btClosedAt = performance.now(); if (IOS) setTimeout(() => { try { if (!battle && STU) worldDrop("stu", "battle closed"); } catch (e) {} }, 800); /* v580 */ }')
s2 = re.sub(r"GAME_V = 579\b", "GAME_V = 580", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
