"""v832: the invasion pages remastered (Mimic, Carcinid, Continuum) and the Finder's Nearest strip (p832_inv.js)."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 831;", "const GAME_V = 832;")
# the Carcinid's element: bubbles rising through the tide
rep('''      else if (el === "banner") {''', '''      else if (el === "tide") { p.y -= dt * (14 + p.v * 26); p.x += Math.sin(p.l * 3 + p.a) * dt * 8; if (p.y < -8) { p.y = H + 8; p.x = R() * W; } const rr = 1.5 + p.v * 4; x.strokeStyle = p.v > .5 ? c2 : c1; x.globalAlpha = .35 + .4 * p.v; x.lineWidth = 1; x.beginPath(); x.arc(p.x, p.y, rr, 0, 6.28); x.stroke(); x.globalAlpha = .5; x.fillStyle = c2; x.beginPath(); x.arc(p.x - rr * .35, p.y - rr * .35, rr * .25, 0, 6.28); x.fill(); }
      else if (el === "banner") {''')
js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "p832_inv.js"), encoding="utf-8").read()
rep("/* the other events keep their existing panels, shown under their banner */", js + "\n/* the other events keep their existing panels, shown under their banner */")
open(p, "w", encoding="utf-8").write(s); print("ok")
