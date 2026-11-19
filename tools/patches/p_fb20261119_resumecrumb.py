# fb-20261119: crash reports said "Closed unexpectedly after: background: 1 drawing buffers released" when the player had come
# back and played on for 23 more minutes (Android, v636): returning from the background left no line in the flight log, so the
# last line was the old background one. bgDiet(false) now writes "back from the background (N s)", so a report shows the
# player was back, and for how long they had been away. Diagnostics only; nothing else changes.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('  if (on) { if (G.bgDiet) return; G.bgDiet = 1; let n = 0;\n',
  '  if (on) { if (G.bgDiet) return; G.bgDiet = 1; G.bgDietT = Date.now(); let n = 0;\n'),
 ('  else if (G.bgDiet) { G.bgDiet = 0; for (const W of [G3, C3]) if (W) W.size = [0, 0];',
  '  else if (G.bgDiet) { G.bgDiet = 0; try { crumb("back from the background (" + Math.round((Date.now() - (G.bgDietT || Date.now())) / 1000) + " s)"); } catch (e) {} /* fb-20261119 */ for (const W of [G3, C3]) if (W) W.size = [0, 0];'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
