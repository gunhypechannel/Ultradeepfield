# v375: the Finder tab drops "Pirate hideouts · fast loot" and "Resource fields · safe to gather" (the boxes above cover both)
p = "docs/index.html"; t = open(p).read()
def cut(a, b=""):
    global t; assert t.count(a) == 1, a[:60]; t = t.replace(a, b)
i = t.index('      <h2 class="sec">Pirate hideouts · fast loot</h2>'); j = t.index('      <h2 class="sec">Worlds</h2>', i)
assert 'Resource fields · safe to gather' in t[i:j] and j - i < 2000; t = t[:i] + t[j:]
cut('    const fields = NODES.filter(n => { const q = pos(n, T); return fogSeen(q.x, q.y); }).sort((a, b) => dist(a) - dist(b)).slice(0, 6);\n')
open(p, "w").write(t)
