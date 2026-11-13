# v509 Vaelthar's wheel winds up before Divine Annihilation (owner: it should spin more before it unleashes the ultimate): from
# the warning its rings spin faster and faster, up to about 30x their idle speed right before the beam, instead of slowing to
# align early; they lock into alignment only as it fires, then wind down.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const spin = 1 + warn * 2 + runes * 3 + acc * 4 + align * 2 - after * 2.5,', 'const wind = A < 0 ? 0 : ss(.08, .64, A) ** 1.6 * (1 - ss(.67, .76, A)), spin = 1 + warn * 2 + runes * 2 + wind * 28 - after * 2.5,')
rep('o.ang += base * dt * spin; if (align > .01) {', 'o.ang += base * dt * spin; if (align > .01 && fire > .01) {')
s2 = re.sub(r"GAME_V = 508\b", "GAME_V = 509", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
