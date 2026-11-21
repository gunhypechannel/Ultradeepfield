# fb-20261121: an iPhone crash report (v703) showed "base released" in the flight log, yet the last heartbeat, 7 s later, still
# counted the base at 161 MB and the total at 199 MB. memEst() keeps its estimate for 12 s, so a heartbeat right after a
# 3D world is released reports memory that is already gone. worldDrop() now drops the kept estimate, so the next heartbeat
# measures again. Diagnostics only; nothing else changes.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('  if (glw0) G.glWait = performance.now() + 1000; /* v588 the wait starts once the release is done */\n',
  '  if (glw0) G.glWait = performance.now() + 1000; /* v588 the wait starts once the release is done */\n  G.memEst = null; /* fb-20261121 the next heartbeat measures again instead of reporting the released world */\n'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
