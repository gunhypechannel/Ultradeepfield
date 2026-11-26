"""v779: Aexion's shield corrected again (owner, with a battle screenshot: "Aexion's shield still bad placement in battle simulation").
v777 pushed it 6.4 out beside the forearm; with the disc 7.5 across and growing in the Aegis move, it hung detached far off his side.
Now it is worn on the forearm: centred just outside it (2.2) and in front of it (4.2) toward the enemy, so the arm sits behind the
disc's inner half, as in the warform painting. The dreadnought also turns slower (3.2 s, was 1.5 s) and only for about one attack
in four, when its target lies well off to a side (owner: "turn slower and way less frequently"). Applies on top of v778."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 778;", "const GAME_V = 779;")
rep("lp.set(lp.x + side * 6.4, lp.y - .6, lp.z + 1.6)", "lp.set(lp.x + side * 2.2, lp.y + .2, lp.z + 4.2)")
# the dreadnought (owner: "make Aexion's dreadnought form turn slower and way less frequently in battle simulation"): a turn takes
# 3.2 s (was 1.5 s), and it turns for only about one attack in four, and only when its target is well off to a side; otherwise it fires from where it lies
rep("const AEXD = { turn: 1500, hold: 500, rest: 2600 }", "const AEXD = { turn: 3200, hold: 700, rest: 2600 }")
rep("c.dir = Math.abs(dx) < W * .06 ? 0 : Math.sign(dx);", "c.dir = Math.abs(dx) < W * .15 || Math.random() > .25 ? 0 : Math.sign(dx); /* v779 rarely turns */")
open(p, "w", encoding="utf-8").write(s)
print("ok")
