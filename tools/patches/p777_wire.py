"""v777: Aexion's Holographic Aegis sits on the outside of his forearm (owner: "shouldn't Aexion's holo shield be on the outside of
his arm?"). When he raised his guard the shield slid toward the middle of his chest, behind his own forearm and fist, so his arm
crossed in front of it. Now it is carried beside the forearm on the outer side and a little forward, facing the enemy, the
arm alongside its inner edge, as in the warform painting. Aexion's v774 surface panels are made finer (at the old size the warform
read as a tile grid). Applies on top of v776."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 776;", "const GAME_V = 777;")
rep("shield.position.set(-2.4 + gd * 1.6, -3.2 - gd * .6, .3 + gd * 3.2); }",
    "{ const W = out._shw || (out._shw = [new TH.Vector3(), new TH.Vector3()]), lp = LF.getWorldPosition(W[0]); body.worldToLocal(lp); const side = Math.sign(lp.x) || -1; /* v777 beside the forearm, on its outer side */\n"
    "          lp.set(lp.x + side * 6.4, lp.y - .6, lp.z + 1.6); body.localToWorld(lp); LF.worldToLocal(lp); W[1].set(-2.4, -3.2, .3); shield.position.copy(W[1].lerp(lp, Math.min(1, gd * 1.2))); } }")
rep("aexion: [0, 34], khezaroth", "aexion: [0, 64], khezaroth") # finer panels: at 34 the warform read as a tile grid
open(p, "w", encoding="utf-8").write(s)
print("ok")
