# v347: Meshy models for the Cube Destroyer (worldbreaker: an original armoured-cube design, not its card's sphere) and the Fusion Plant.
# The cube came out with its red emitter on +X and engines on +Z, so it turns a quarter (eye toward the battle camera, engines at the back).
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep('"guardian", "tender", "spyProbe"]);', '"guardian", "tender", "spyProbe", "worldbreaker"]);\nconst GLB_YAW = { worldbreaker: -Math.PI / 2 }; // turn from the model file to the hull pointing +X (default: half a turn)')
rep('"robotics", "lab", "radar"]);', '"robotics", "lab", "radar", "fusion"]);')
rep('pv.rotation.y = Math.PI; g.add(pv);', 'pv.rotation.y = GLB_YAW[k] !== undefined ? GLB_YAW[k] : Math.PI; g.add(pv);')
open(p, "w").write(h); print("ok")
