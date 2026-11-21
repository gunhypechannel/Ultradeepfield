# v699 (owner: "During super cube fight why does advisor say there is nothing like this in the archives when there is and also when
# fighting an omega she says the omega is big as a moon but its way larger?"): two of the Advisor's boss-fight lines were wrong.
# "Nothing in the archives looks like this" sat in the shared pool every boss draws from, and every boss has an archive record;
# Omega's "It's the size of a moon" undersells a cube far larger than a moon. Both are out of the rotation (they stay in the voice
# index, unused); replacements can be recorded if the owner wants them.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('"Nothing in the archives looks like this. Nothing.", ', '')
rep('"omg": ["It\'s the size of a moon and it\'s still growing. This is insane.", ', '"omg": [')
rep('const GAME_V = 698;', 'const GAME_V = 699;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
