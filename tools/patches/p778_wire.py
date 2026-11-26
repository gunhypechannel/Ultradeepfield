"""v778: Vaelthar faces the fleet head-on in battle (owner: "Vaelthar should have more of a head-on view in battle simulation").
He stood turned three-quarters away (v770 yaw .75); now he faces the camera with the wheel framed behind him and both wings spread
either side, the camera a little above his eye line. Applies on top of v777."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 777;", "const GAME_V = 778;")
rep("omega: 0, vaelthar: .75, aexion: null,", "omega: 0, vaelthar: 0, aexion: null,")
rep("vaelthar: [-.35, [-21, 9, 54], [3, 9.5, 0]]", "vaelthar: [0, [-3, 13, 64], [0, 11.5, 0]]")
open(p, "w", encoding="utf-8").write(s)
print("ok")
