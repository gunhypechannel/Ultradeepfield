# v638: the fb-20261119-0025 patch (p_fb20261119_resumecrumb.py: the flight log notes the return from the background, so a crash
# report no longer says "after: background ..." when the player had come back and played on) plus the version bump.
# Owner: "Release it" (feedback triage 2026-11-19).
import sys, re, subprocess, os
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
subprocess.check_call([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p_fb20261119_resumecrumb.py'), P])
s = open(P, encoding='utf-8').read()
s2 = re.sub(r"GAME_V = 637\b", "GAME_V = 638", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
