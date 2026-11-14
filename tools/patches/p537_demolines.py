# v537 (with p537_memory.py) the Cube demo's march lines (owner: "20vs 20 test did not show any lines marching towards cube"). v243 hid
# every demo army's course and trail (120 of them flickered white). The attackers' courses now show while they march on the Cube (and
# the stress test's reinforcements on their way in); parked and retreating demo fleets stay without lines.
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
a = 'noLine = (cubeB && (routeKind(f) === "joint" || path.cube) && (!mineF.has(f) || cineOn)) || (!!f.demo && cam.followFleet !== id) /* v243'
assert s.count(a) == 1
s = s.replace(a, 'noLine = (cubeB && !f.demo && (routeKind(f) === "joint" || path.cube) && (!mineF.has(f) || cineOn)) || (!!f.demo && cam.followFleet !== id && !(f.phase === "out" && !f.retreat && !path.park)) /* v537 the march on the Cube shows its lines; v243')
open(P, 'w', encoding='utf-8').write(s); print('ok')
