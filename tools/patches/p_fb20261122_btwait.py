# fb-20261122: an iPhone crash report (v725) closed a boss replay opened from Mail and, about 2 s later, the galaxy map was
# built cold ("map shaders paced over several frames") and the game was killed. The battle's canvases and hull pictures
# are freed when it closes and the studio renderer only 0.8 s later, so the cold map build ran on top of memory Safari had
# not given back yet. On iPhone/iPad, closing a battle now starts the same short wait v588 uses after a world is released:
# a cold build of the map or the base right after a battle shows "Opening..." until 2.5 s after the close. Worlds already
# alive are not affected.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('G.btClosedAt = performance.now(); if (IOS) setTimeout(',
  'G.btClosedAt = performance.now(); if (IOS) G.glWait = Math.max(G.glWait || 0, G.btClosedAt + 2500); /* fb-20261122 no cold build while the battle is still being freed */ if (IOS) setTimeout('),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
