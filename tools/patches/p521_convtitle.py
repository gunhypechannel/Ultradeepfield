# v521 the Pentarch Convergence clock's title is white (owner); its rune rings keep the five Elementals' colours.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
a = 'let ci = 0; for (const ch of txt) { p.save(); if (N.multi && ch !== " ") p.fillStyle = p.shadowColor = N.multi[ci++ % N.multi.length];'
assert s.count(a) == 1; s = s.replace(a, 'for (const ch of txt) { p.save();')
s2 = re.sub(r"GAME_V = 520\b", "GAME_V = 521", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
