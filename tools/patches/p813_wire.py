"""v813: the Void Shop / skin lists stop exhausting the phone's graphics memory. Owner's screenshot (Z Fold 6, unfolded): skin cards
with no text, a black box over the header, the page beneath showing through: the browser had run out of tile memory and dropped
paints. Measured at that screen (844x980 @2.3): 490 composited layers, 213 running animations (152 of them gold-skin sparkles), ~1.2 GB
of tiles if all painted. Now: skin cards off screen are skipped (content-visibility), 3 sparkles per gold card instead of
8, the gold halo glows without re-filtering every frame."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 812;", "const GAME_V = 813;")
CSS = ("/* v813 graphics memory: skip what is off screen, fewer animated layers */"
  ".pxcard{content-visibility:auto;contain-intrinsic-size:auto 132px}"
  ".pxspk s:nth-child(n+4){display:none}"
  ".pxgw canvas{animation:none;filter:drop-shadow(0 0 12px rgba(255,210,100,.6))}")
i = s.index("</style>"); s = s[:i] + CSS + s[i:]
open(p, "w", encoding="utf-8").write(s)
print("ok")
