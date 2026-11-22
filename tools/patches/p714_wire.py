# v714 (owner approved releasing fb-20261121-1059 and fb-20261121-1221): applies p_fb20261121_iospace.py (iOS builds at most
# 2 new shader programs a frame on the map and base) and p_fb20261121_memfresh.py (crash reports measure memory again right
# after a 3D world is released), then bumps GAME_V 713 -> 714.
import sys, os, subprocess
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
d = os.path.dirname(os.path.abspath(__file__))
for f in ('p_fb20261121_iospace.py', 'p_fb20261121_memfresh.py'):
    subprocess.run([sys.executable, os.path.join(d, f), p], check=True)
s = open(p, encoding='utf-8').read()
a = 'const GAME_V = 713;'; assert s.count(a) == 1, a
s = s.replace(a, 'const GAME_V = 714;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
