# v594 the Super Cube is a gate, not a wall (owner: "The super cube should have been easier for us to beat, since its an alliance vs
# alliance fight after all"). Week 45 ended with the Cube never taken: the Warden was worn to 52% integrity but could only be broken at
# 25%, and until then it rose to meet every fleet so one attack took only 30-60% of it. Now: every attack on the Warden destroys at
# least half of it (50% rising to 75% for the largest fleets), its integrity can be worn down to 10% (was 20%), and once it is at
# half strength or less it no longer rises: the next fleet fights it as it stands and can seize the Cube. Then the battle is the
# alliances' own: holding it against each other.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('function riseFight(mkA, mkD, frac, worn) { let { F, x } = wbRiseK(mkA(), mkD()); if (F <= 1 || worn) return { res: simulate(mkA(), mkD()), rise: 1 };\n  const tgt = clamp(.3 + .09 * Math.log10(x), .3, .6);',
    'function riseFight(mkA, mkD, frac, worn, t0) { let { F, x } = wbRiseK(mkA(), mkD()); if (F <= 1 || worn) return { res: simulate(mkA(), mkD()), rise: 1 };\n  const tgt = t0 ? clamp(t0 + .08 * Math.log10(x), t0, .75) : clamp(.3 + .09 * Math.log10(x), .3, .6); /* v594 t0: the Cube\'s floor */')
rep('riseFight(A0, () => nexusDefense(cur).stacks, cubeKilled, cubeIntegrity(cur) <= .25)', 'riseFight(A0, () => nexusDefense(cur).stacks, cubeKilled, cubeIntegrity(cur) <= CUBE_BREAK, .5)')
rep('const cubeIntegrity = cur => 1 - clamp(+(cur && cur.wd) || 0, 0, .8);', 'const CUBE_BREAK = .5; /* v594 at half strength the Warden stops rising */\nconst cubeIntegrity = cur => 1 - clamp(+(cur && cur.wd) || 0, 0, .9);')
rep('cur.wd = clamp(1 - cubeIntegrity(cur) * left, 0, .8); }', 'cur.wd = clamp(1 - cubeIntegrity(cur) * left, 0, .9); }')
s2 = re.sub(r"GAME_V = 593\b", "GAME_V = 594", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
