# v708: the Omega Cube turns slowly in the owner preview too (owner, about the video of it spinning: "That's only for omega cube event
# right? That's where my video was from"). The finished Omega turns once every 40 event-minutes; the preview plays the event 30-65x
# faster, so it whirled once every 8-9 seconds. In the preview its turn is now 30x slower (about once every 4-5 minutes, like the Cube);
# the live event is unchanged (once every 40 minutes). Both the cubes' positions (dvCube) and the haze/nexus (dvRot) use the same turn.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('TAU / (40 * DV_M)', 'TAU / (40 * DV_M) / (G.dvSim ? 30 : 1)', 2)
rep('const GAME_V = 707;', 'const GAME_V = 708;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
