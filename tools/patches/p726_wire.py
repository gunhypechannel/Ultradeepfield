# v726 (owner approved releasing fb-20261122-1715 on 2026-11-22): applies p_fb20261122_btwait.py (on iPhone/iPad, a cold
# build of the map or base waits until 2.5 s after a battle closes), then bumps GAME_V 725 -> 726.
import sys, os, subprocess
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
d = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(d, 'p_fb20261122_btwait.py'), p], check=True)
s = open(p, encoding='utf-8').read()
a = 'const GAME_V = 725;'; assert s.count(a) == 1, a
s = s.replace(a, 'const GAME_V = 726;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
