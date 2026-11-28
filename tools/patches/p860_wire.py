"""v860: the Eternal Commander opens with its Swarm, which fights like turrets before diving in (see p860_swarm.js)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 859;", "const GAME_V = 860;")
rep('const CNT_E5 = ["eLance", "eTalon", "eSwarm", "eOrb", "eGrid", "eRes"];', 'const CNT_E5 = ["eSwarm", "eLance", "eTalon", "eOrb", "eGrid", "eRes"]; /* v860 the swarm first */')
rep("eGrid: 2.2, eRes: 2.4, eSwarm: 2.2 };", "eGrid: 2.2, eRes: 2.4, eSwarm: 3.4 };")
a = s.index("function cntEterSwarm("); b = s.index("function cntEterAtk(")
s = s[:a] + open(__file__.rsplit('/', 1)[0] + "/p860_swarm.js", encoding="utf-8").read() + s[b:]
open(p, "w", encoding="utf-8").write(s); print("ok")
