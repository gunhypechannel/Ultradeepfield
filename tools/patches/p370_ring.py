# v370: planet rings were cut where they cross in front of their planet. All rings are one instanced batch whose object sits at the world origin,
# so three.js sorted it behind every planet's own transparent layers (clouds, atmosphere), which then painted over the ring's front arc.
# The ring batch now draws after them (renderOrder 3); the planet sphere still hides the ring's far side by depth.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep('const rings = instFor(W, "rings", W.ringGeo, W.ringMat, near.length + 33); let ringI = 0;',
    'const rings = instFor(W, "rings", W.ringGeo, W.ringMat, near.length + 33); let ringI = 0; rings.mesh.renderOrder = 3; // v370 after the planets\' clouds and atmospheres')
open(p, "w").write(h); print("ok")
