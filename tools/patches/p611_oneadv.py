# v611: back to the Advisor's one portrait (owner: "I just want to go back to the one advisor image, we didn't exactly put her
# together the way I imagined"). The face frames, lip frames, blinks and full-body pose cameos from v608-v610 are switched off:
# afOn() is false, so every portrait (dialog, hologram, tour, celebrations) shows ADV_ART again and advPose never runs.
# The art files stay in docs/art/adv in case they are wanted later. Report a player and the new icon from v610 are unchanged.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('function afOn() { try {', 'function afOn() { return false; /* v611: one portrait */ try {')
s2 = re.sub(r"GAME_V = 610\b", "GAME_V = 611", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
