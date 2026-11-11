# v441: the Omega Cube assembles in two stages (owner: "it should still get assembled like a puzzle piece, but then end up being an
#  even bigger cube"). Every cube first locks into the v430 puzzle (twelve interlocking blocks of 2x2x2 15-unit cells and a crown, round
#  the Super Cube) between 90 and 130 min; the finished puzzle holds until 134 min; then it bursts apart, every piece grows to the Super
#  Cube's size (30), and each flies to the slot of the 5x5x5 giant cube on its own side and slides home, bottom face first (141-149
#  min), before the silence and the eruption at 150-153 min. dvPlan/dvCube replaced (p441_twostage.js); lock flares fire on both locks.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
a = t.index("function dvPlan(s0) {"); b = t.index("const dvEase = ")
c = t.index("function dvCube(c, e, D, o) {"); d = t.index("const dvRot = ")
NEW = open("tools/patches/p441_twostage.js").read()
assert a < b < c < d
t = t[:a] + t[b:c] + NEW + t[d:]
rep("DV_CELL = 30, DV_Y = 170,", "DV_CELL = 30, DV_CELLP = 15, DV_LOCK2 = 40e3, DV_Y = 170,")
rep("lock0: 90 * DV_M, lock1: 148 * DV_M,", "lock0: 90 * DV_M, lock1: 130 * DV_M, ex0: 134 * DV_M, ex1: 136.5 * DV_M, rb0: 141 * DV_M, rb1: 149 * DV_M, /* v441 the puzzle, then the giant cube */")
rep("if (e - c.lk < 8000 * (D.sim ? 1 : 3)) dvFx(X, o, c.s.n, 1, t);", "if (e - (o.lkT || c.lk) < 8000 * (D.rate || 1) * 3) dvFx(X, o, o.lkT === c.lk2 ? c.s2.n : c.s.n, o.lkT === c.lk2 ? 1.6 : 1, t);")
rep('o.st === "slide" || o.st === "align" ? .3 + .7 * o.al :', 'o.st === "shift" ? .9 + .5 * Math.sin(t * .012 + c.i) : o.st === "slide" || o.st === "align" ? .3 + .7 * o.al :')
t = t.replace("const GAME_V = 440;", "const GAME_V = 441;")
open(p, "w").write(t); print("ok")
