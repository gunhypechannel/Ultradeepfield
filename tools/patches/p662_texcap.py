# v662 (feedback triage 2026-11-19; owner: "Release + Android cap").
# (1) p_fb20261119_stuorder.py: the studio's picture cache keeps its eviction order when iOS rebuilds the studio after a battle
#     (owner's iPhone v651: 110 pictures / 74 MB after seven hunt replays, then killed).
# (2) Android texture cap: Czo's Android (v646) lost its graphics context with the base at ~208 MB of textures; only iOS had the
#     v608 cap. Weak Android phones (WEAK) now get the iPhone caps (map 512, base 768); other Android phones 1024 for both.
#     Desktop unchanged. glNew applies the cap on any platform where iosTexCap gives one.
import sys, subprocess, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
here = os.path.dirname(os.path.abspath(__file__))
subprocess.check_call([sys.executable, os.path.join(here, 'p_fb20261119_stuorder.py'), p])
t = open(p, encoding='utf-8').read()
R = [
 ('function iosTexCap(k) { return k === "gal" ? 512 : 768; }',
  'function iosTexCap(k) { const ios = typeof IOS !== "undefined" && IOS, mob = typeof MOBILE !== "undefined" && MOBILE, weak = typeof WEAK !== "undefined" && WEAK; if (ios || weak) return k === "gal" ? 512 : 768; return mob ? 1024 : 0; } /* v662 Android phones capped too (weak ones like iPhone) */'),
 ('function glNew(o, cap) { if (cap && IOS && o && o.canvas)',
  'function glNew(o, cap) { if (cap && o && o.canvas)'),
 ('const GAME_V = 661;', 'const GAME_V = 662;'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
