"""v792: Vaelthar's body bulked toward his painting (owner: "build it all"): a hunched, heavily muscled dragon rather than a slim
column. His chest and torso rings are about a third thicker with a stronger swell through the middle, his neck heavier, and his
shoulders broader and set wider, so the arms hang from a massive frame; his horned head is 40% bigger to match. Applies on top of v791."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 791;", "const GAME_V = 792;")
rep("SC[k] = 3.0 + Math.sin(u * Math.PI) * 1.3 - u * .4;", "SC[k] = 3.8 + Math.sin(u * Math.PI) * 2.1 - u * .6; /* v792 bulk */")
rep("SC[i] = 1.35 + u * 1.15;", "SC[i] = 1.65 + u * 1.7;")
rep("sh.position.set(sx * 2.5, 5.6, 2.0); sh.scale.setScalar(1.6);", "sh.position.set(sx * 3.4, 5.9, 2.0); sh.scale.setScalar(2.05);")
rep("const head = new TH.Group(); body.add(head); const hd = new TH.Group(); head.add(hd); hd.scale.setScalar(1.25);", "const head = new TH.Group(); body.add(head); const hd = new TH.Group(); head.add(hd); hd.scale.setScalar(1.75); /* v792 a dragon's head on that frame */")
open(p, "w", encoding="utf-8").write(s)
print("ok")
