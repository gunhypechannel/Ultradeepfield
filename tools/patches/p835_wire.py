"""v835: the Neural Corvette and Fabrication Carrier re-sculpted to match their new paintings (tools/sculpt/cnt_cor.py, cnt_fab.py)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 834;", "const GAME_V = 835;")
rep("cncor: { s: 1, eng: [[-2.3, 0, .2, .2], [-2.3, 0, -.2, .2]] }, cnfab: { s: 1, eng: [[-3.85, 0, .55, .32], [-3.85, 0, -.55, .32], [-3.85, .3, 0, .26]] },",
    "cncor: { s: 1, eng: [[-2.55, 0, .2, .2], [-2.55, 0, -.2, .2]] }, cnfab: { s: 1, col: [0xc8e6ff, 0x3a9cff], eng: [[-3.85, 0, .55, .32], [-3.85, 0, -.55, .32], [-3.85, .3, 0, .26]] },")
rep("g.userData.eng = D.eng.map(e => e.slice()); g.userData.engCol = [0xffc0c6, 0xff2a3a]; g.userData.cnt = 3;",
    "g.userData.eng = D.eng.map(e => e.slice()); g.userData.engCol = D.col || [0xffc0c6, 0xff2a3a]; g.userData.cnt = 3;")
open(p, "w", encoding="utf-8").write(s); print("ok")
