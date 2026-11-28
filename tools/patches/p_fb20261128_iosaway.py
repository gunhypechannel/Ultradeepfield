# fb-20261128: two crash reports from the owner's iPhone (v835): the game was closed on the Mail screen with a 3D world still
# built behind it, first the galaxy map (~70 MB, 3 min after it was built), then the base (~173 MB, built at boot, the Shop
# sheet open, 44 s after a reload). v537 kept the last used world alive while away from both worlds. Owner: "lets do what we
# can to fix it for iphone". Now on iPhone/iPad:
# (1) away from both the map and the base (Mail, Quests, Rank, ...) for 15 s, both worlds are released; they are built
#     again when opened (with the v588 "Opening the galaxy/your base" wait), so coming back costs a short load.
# (2) as the page goes to the background, the worlds not on screen are released, as on Android since v760.
# The world on screen is never dropped (worldDrop checks the view). No version bump.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('    if (C3 && view !== "base" && T - lc > 8000 && (view === "galaxy" || lg > lc)) worldDrop("col", "one world on iPhone");\n',
  '    if (C3 && view !== "base" && T - lc > 8000 && (view === "galaxy" || lg > lc)) worldDrop("col", "one world on iPhone");\n'
  '    if ((G3 || C3) && view !== "galaxy" && view !== "base" && T - Math.max(lg, lc) > 15000) { worldDrop("gal", "away from both worlds"); worldDrop("col", "away from both worlds"); } /* fb-20261128 iPhone: no world kept behind Mail and other screens */\n'),
 ('    if (ANDROID && !battle) { try { worldDrop("gal", "background, not on screen");',
  '    if ((ANDROID || IOS) && !battle) { try { worldDrop("gal", "background, not on screen");'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
