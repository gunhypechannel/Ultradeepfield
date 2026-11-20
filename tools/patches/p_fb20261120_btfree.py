# fb-20261120: four iPhone crash reports (v684, the owner's phone). Two were killed about 3 s after opening the replay
# "Joint strike on the Cube" from Mail: one with the galaxy map still built (95 MB of textures) plus the battle (40 MB of
# drawing buffers), the other with the base still built (186 MB) plus 31 MB of paintings. The v630/v636 Boss Lab kills had
# the same shape (base alive under a replay). Since v381 a battle keeps both 3D worlds, and v537's "away from both, the
# last used stays" keeps the one you came from even when you are on Mail. Now, on iPhone/iPad, opening a battle releases
# any 3D world that is not the current view (worldDrop already never drops the world on screen). It is built again the
# next time you open the base or the map (the v588 "Opening..." wait). Nothing changes on Android or desktop.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('crumb("battle replay: " + String((r && r.title) || "battle").slice(0, 40)); gpuNap(true);',
  'crumb("battle replay: " + String((r && r.title) || "battle").slice(0, 40)); if (IOS) { worldDrop("gal", "before a battle"); worldDrop("col", "before a battle"); } /* fb-20261120 only the world on screen stays */ gpuNap(true);'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
