# fb-20261120: owner's iPhone (v665) closed 8 s after launch. Flight log: boot, "background: 1 drawing buffers released" 2 s later,
# no "back from the background", then 6 s later "base released", "map waits for the base", "session restored: galaxy + camera".
# The session-restore timer kept running while the game was hidden: it switched to the galaxy and built the 3D map in the
# background (undoing the background diet) and its crumbs reopened the flight log, so the page was killed and reported as a crash.
# Now the restore waits until the game is on screen again, and the 4 s settle time counts from that moment.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('setInterval(() => { if (!G.sessDone && G.ready && S && G.me) { const tn = performance.now(); G.sessT0 = G.sessT0 || tn;',
  'setInterval(() => { if (!G.sessDone && G.ready && S && G.me) { const tn = performance.now(); if (document.hidden) { G.sessT0 = 0; return; } /* fb-20261120 never restore (switch view, build the map) while hidden */ G.sessT0 = G.sessT0 || tn;'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
