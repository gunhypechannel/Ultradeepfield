# v760 (owner approved releasing fb-20261125-1522 on 2026-11-25: "Release it"): applies p_fb20261125_bgdrop.py (on Android,
# app and Chrome, going to the background releases the map and base when they are not on screen), then bumps GAME_V 759 -> 760.
# Supersedes the unreleased fb-20261124-0926 (p_fb20261124_bgdrop.py, Android app only): do not apply that one as well.
import sys, os, subprocess
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
d = os.path.dirname(os.path.abspath(__file__))
subprocess.run([sys.executable, os.path.join(d, 'p_fb20261125_bgdrop.py'), p], check=True)
s = open(p, encoding='utf-8').read()
a = 'const GAME_V = 759;'; assert s.count(a) == 1, a
s = s.replace(a, 'const GAME_V = 760;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
