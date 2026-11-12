# v500 one boss monster on the map at a time (besides the Super Cube): the last pre-rotation week showed the four g2 world
# bosses together; now one of them per week. Group events stay groups (Overlord + Conduits, the 5 Elementals, then the Pentarch).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
a = 'if (g === 2) return odd ? null : [s, s + WB_LIVE];'
assert s.count(a) == 1
s = s.replace(a, 'if (g === 2) { const L2 = ["brd", "tyr", "wym", "col"]; return odd || L2[(((c >> 1) % 4) + 4) % 4] !== k ? null : [s, s + WB_LIVE]; } // v500 one at a time')
s2 = re.sub(r"GAME_V = 499\b", "GAME_V = 500", s); assert s2 != s
open(P, 'w', encoding='utf-8').write(s2); print('ok')
