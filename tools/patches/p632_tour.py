# v632: the map tour starts every time (owner: "Neighborhood tour does not work now"). A tapped button passes itself as the second
# argument, which mapTour took for its retry count, so when the map wasn't ready at once (the Handbook opened from the Menu) it
# never retried. It now counts its own tries and waits up to 12 s for the map.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('    if (!G3 || !$("#tourcap")) { if ((n || 0) < 20) setTimeout(() => ACT.mapTour(d, (n || 0) + 1), 300); return; }',
    '    const k = typeof n === "number" ? n : 0; if (!G3 || !$("#tourcap")) { if (k < 40) setTimeout(() => ACT.mapTour(d, k + 1), 300); return; } /* v632 */')
s2 = re.sub(r"GAME_V = 631\b", "GAME_V = 632", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
