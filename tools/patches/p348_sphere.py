# v348: the Cube Destroyer is a sphere (owner). Its Meshy cube model is retired; the hand-built battle sphere (v86, as on its card) is back.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep('"guardian", "tender", "spyProbe", "worldbreaker"]);', '"guardian", "tender", "spyProbe"]); // v348: not the Cube Destroyer, which is a sphere (its hand-built model)')
open(p, "w").write(h); print("ok")
