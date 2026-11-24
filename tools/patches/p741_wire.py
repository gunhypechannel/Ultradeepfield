"""v741: the Continuum's hulls remastered toward the owner's concept art; the Signal finale gets its Advisor lines; the new omens' lines queued for voicing."""
import sys, os, re
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:120]); s = s.replace(a, b)
rep("const GAME_V = 740;", "const GAME_V = 741;")
i = s.index("function buildCnt(k) {"); j = s.index("  g.userData.cnt = 1; return g; }", i) + len("  g.userData.cnt = 1; return g; }")
s = s[:i] + open(os.path.join(D, "p741_ships.js"), encoding="utf-8").read().strip() + s[j:]
rep("FIN_SET.om1 = om1Set; FIN_SET.om2 = om2Set; FIN_SET.om3 = om3Set;", 'FIN_SET.om1 = om1Set; FIN_SET.om2 = om2Set; FIN_SET.om3 = om3Set;\nFIN_SAY.om3 = { voices: "Commander, every listening post just lit up at once. Four signals, four directions.", cross: "They\'re crossing over the Cube. It sounds like they\'re talking to each other.", answer: "Something answered, Commander. One red pulse, from past the charted stars.", quiet: "Static now. But whatever answered knows we were listening." }; /* v741 */')
open(p, "w", encoding="utf-8").write(s)
print("ok")
