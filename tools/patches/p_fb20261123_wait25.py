# fb-20261123: two crash reports from the owner.
# (1) iPhone, v730: the game opened on the base (~195 MB), the saved session then switched to the galaxy, the base was
#     released, the v588 wait of 1 s ran, and the cold map build ("map shaders paced over several frames") was killed
#     about 2 s after the release. Same pattern v588 and fb-20261122 describe: Safari gives GPU memory back lazily.
#     The wait after a world is released is now 2.5 s (the same as after a battle, fb-20261122) instead of 1 s.
# (2) Android app (WebView), v729: map (162 MB) and base (253 MB) were both alive behind Mail while three boss replays
#     played; the renderer was killed as the third closed (~473 MB estimated). The v715 rule (opening a battle replay
#     releases the 3D worlds that are not on screen) now also applies in the Android app, not only on iPhone/iPad.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('if (glw0) G.glWait = performance.now() + 1000; /* v588 the wait starts once the release is done */',
  'if (glw0) G.glWait = Math.max(G.glWait || 0, performance.now() + 2500); /* v588 the wait starts once the release is done; fb-20261123 2.5 s, 1 s was not enough */'),
 ('if (IOS) { worldDrop("gal", "before a battle"); worldDrop("col", "before a battle"); } /* fb-20261120 only the world on screen stays */',
  'if (IOS || /UDFApp\\//.test(navigator.userAgent)) { worldDrop("gal", "before a battle"); worldDrop("col", "before a battle"); } /* fb-20261120 only the world on screen stays; fb-20261123 also in the Android app */'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
