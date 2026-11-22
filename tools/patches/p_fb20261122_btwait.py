# fb-20261122: iPhone crash reports (v719, the owner's phone). Twice the game was killed right after
# "battle replay: ... / map released (before a battle)" when a replay was opened from Mail; once within about a second.
# v715 releases the off-screen 3D world before a battle, but the battle then builds its canvases and ship pictures at
# once, while Safari still holds the released world's memory (it frees GPU memory lazily: the v588 problem between the map
# and the base). Now, on iPhone/iPad, a replay opened from a report that had to release a 3D world first waits one second
# ("Opening the battle...", the same card as the map/base wait) before it starts. Only the Mail/report "replay" button
# waits; the tutorial, the lab tools and "replay again" are unchanged. Nothing changes on Android or desktop.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('function playBattle(r) {\n',
  'function btFreeFirst(go) { /* fb-20261122 iOS: release the off-screen 3D world, give Safari a second to free it, then open the battle */\n'
  '  if (G.btWaitT) return; /* a second tap while waiting */\n'
  '  if (!IOS || !((G3 && view !== "galaxy") || (C3 && view !== "base"))) return go();\n'
  '  worldDrop("gal", "before a battle"); worldDrop("col", "before a battle"); crumb("battle waits for the 3D world to be freed");\n'
  '  const app = $("#app"), w = document.createElement("div"); w.className = "glwait"; w.style.position = "fixed"; w.style.zIndex = "90"; w.innerHTML = "<i></i><span>Opening the battle\\u2026</span>"; if (app) app.appendChild(w);\n'
  '  G.btWaitT = setTimeout(() => { G.btWaitT = 0; try { w.remove(); } catch (e) {} go(); }, 1000); }\n'
  'function playBattle(r) {\n'),
 ('if (r) { if (!S.tutReplay) { S.tutReplay = 1; dirty(); } playBattle(r); } },',
  'if (r) { if (!S.tutReplay) { S.tutReplay = 1; dirty(); } btFreeFirst(() => playBattle(r)); } }, /* fb-20261122 */'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
