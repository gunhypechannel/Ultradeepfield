# v690: the Advisor's Titan lines in battle are retired (owner: "I think I want to retire the titans lines in battle simulation"):
# no opening line about your Titan or theirs, and no call-out when a Titan fires its ultimate. The ultimate's slow-motion moment stays,
# and so do the Advisor's Titan lines outside battle (a Titan commissioned, enough Titan Cores to build one).
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('setTimeout(() => titAdvBattle(battle), 2600); /* v606 */ ', '/* v690 the Advisor\'s Titan lines in battle are retired (v606 titAdvBattle) */ ')
rep('b.tUlt[qq.k] = 1; titAdv("ult", v.ab); }', 'b.tUlt[qq.k] = 1; /* v690 no Advisor call-out on a Titan ultimate */ }')
rep('const GAME_V = 689;', 'const GAME_V = 690;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
