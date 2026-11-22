# fb-20261122: iPhone crash reports (v721, the owner's phone). The session restore runs 4-20 s after launch (v426 lets the
# launch settle first). If the player had already moved in that time (e.g. tapped Map), the restore pulled them back to the
# saved screen anyway: crash report crash-mwrk0lnvvw63 shows boot, the player opens the map (base released, map built),
# then "session restored: base (0 min)" releases the map and rebuilds the base, the player taps Map again and the map is
# built a second time; killed seconds later (three 3D world builds in 12 s, the known iPhone memory kill).
# Now any navigation by the player (ACT.nav: dock, map button, shortcuts, quest/Advisor buttons) marks G.navUser, and the
# session restore then leaves the player where they are ("session not restored (player already moved)").
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('  nav: d => { let v = d.v, s = d.s;\n',
  '  nav: d => { let v = d.v, s = d.s; G.navUser = 1; /* fb-20261122 the session restore leaves a player who already moved */\n'),
 ('  try { if (typeof liveIntro === "function" && liveIntro(now())) return; } catch (e) {}\n  G.sessHold = 1;',
  '  try { if (typeof liveIntro === "function" && liveIntro(now())) return; } catch (e) {}\n'
  '  if (G.navUser) { try { crumb("session not restored (player already moved)"); } catch (e) {} return; } /* fb-20261122 */\n'
  '  G.sessHold = 1;'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
