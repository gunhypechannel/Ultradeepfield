# fb-20261121: iPhone crash reports (owner, v682-v699) keep dying 1-3 s after "map shaders paced over several frames", often after a
# 1.2-1.7 s freeze, even with little texture memory in use (v699: ~21 MB). The v530 pacing spends a time budget per frame (22 ms on
# phones), but on iOS Safari compiles shaders in its GPU process, mostly outside the time we measure, so the budget barely bites and
# dozens of programs still build at once. On iOS a paced scene now also builds at most 2 new shader programs per frame (map and base);
# the rest wait for the next frames, so the map fills in over a fraction of a second instead of one big spike.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('  r.pace = { scene: null, ms: 30, used: 0, skips: 0 };\n',
  '  r.pace = { scene: null, ms: 30, used: 0, skips: 0, n: 0, max: IOS ? 2 : 0 }; /* fb-20261121 iOS: at most 2 new programs a frame */\n'),
 ('    if (paced && mat && !seen.has(mat) && B.used >= B.ms) { B.skips++; return; }\n',
  '    if (paced && mat && !seen.has(mat) && (B.used >= B.ms || (B.max && B.n >= B.max))) { B.skips++; return; }\n'),
 ('if (paced && links > l0) B.used += performance.now() - t0; return res; }; }',
  'if (paced && links > l0) { B.used += performance.now() - t0; B.n += links - l0; } return res; }; }'),
 ('B.scene = W.scene; B.used = 0; B.skips = 0; B.ms = MOBILE ? 22 : 45; }',
  'B.scene = W.scene; B.used = 0; B.n = 0; B.skips = 0; B.ms = MOBILE ? 22 : 45; }'),
 ('P.scene = W.scene; P.used = 0; P.skips = 0; P.ms = MOBILE ? 22 : 45; }',
  'P.scene = W.scene; P.used = 0; P.n = 0; P.skips = 0; P.ms = MOBILE ? 22 : 45; }'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
