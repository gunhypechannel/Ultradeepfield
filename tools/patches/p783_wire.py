"""v783: Medusara's serpent teeth set right (owner: "look at the snakes' teeth on Medusara, they look unnaturally positioned"). The
upper row pointed up into the skull and the lower row down into the jaw (flipped); now upper teeth hang down and lower teeth stand
up along the jaw line. The two fangs stuck out sideways past the lips like blades; now they hang from the front of the upper jaw,
curving back, inside the mouth, a little shorter. The flat box brows are now small pointed scale ridges. Applies on top of v782."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 782;", "const GAME_V = 783;")
rep("put(jaw, new TH.Mesh(TOOTH, IVO), [sx * (.36 - q * .03), .2, 2.05 - q * .26], [.15, 0, 0], [.75, .8 - q * .07, .75])",
    "put(jaw, new TH.Mesh(TOOTH, IVO), [sx * (.33 - q * .03), .16, 2.0 - q * .24], [Math.PI - .12, 0, 0], [.75, .8 - q * .07, .75])")
rep("put(hd, new TH.Mesh(FANG, IVO), [sx * .4, -.12, 2.0], [.25, 0, sx * .1]);", "put(hd, new TH.Mesh(FANG, IVO), [sx * .26, -.08, 1.92], [-.3, 0, sx * -.06], .72);")
rep("put(hd, new TH.Mesh(TOOTH, IVO), [sx * (.34 - q * .03), -.16, 1.75 - q * .26], [Math.PI - .15, 0, 0], [.7, .7 - q * .06, .7])",
    "put(hd, new TH.Mesh(TOOTH, IVO), [sx * (.31 - q * .03), -.12, 1.72 - q * .24], [.12, 0, 0], [.7, .7 - q * .06, .7])")
rep("put(hd, new TH.Mesh(new TH.BoxGeometry(.5, .14, .55), MSk), [sx * .6, .6, .72], [.25, sx * -.35, sx * .2]);",
    "put(hd, new TH.Mesh(new TH.ConeGeometry(.14, .62, 4), MSk), [sx * .5, .56, .8], [Math.PI / 2 + .35, 0, sx * .3]);")
open(p, "w", encoding="utf-8").write(s)
print("ok")
