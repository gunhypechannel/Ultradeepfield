# v715 (owner approved releasing fb-20261120-2122 on 2026-11-22): applies p_fb20261120_btfree.py (on iPhone/iPad, opening a
# battle replay releases any 3D world that is not on screen, e.g. the map or base kept alive behind Mail), then bumps
# GAME_V 714 -> 715.
import sys, os, subprocess
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
d = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(d, 'p_fb20261120_btfree.py'), p], check=True)
s = open(p, encoding='utf-8').read()
a = 'const GAME_V = 714;'; assert s.count(a) == 1, a
s = s.replace(a, 'const GAME_V = 715;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
