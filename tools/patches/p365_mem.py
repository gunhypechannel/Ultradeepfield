# v365: stability on iPhone. iOS Safari ends a tab that holds too much memory (crash log: "model load cut off"). Measured with an iPhone
# user agent, all models loaded: decoded textures 370 MB (v358: 295 MB), JS peak 150 MB (v358: 121 MB); the v359 hull glow maps added ~4 MB per ship.
#  - Phones: the ship glow map and its working buffers are 512 px (the battle portraits are ~450 px wide), not 1024.
#  - iPhone/iPad: building colour maps are 1024 px for every building (Android keeps 1536 for the first eight).
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep("const A = 1024, E = new Float32Array(A * A * 3), SA = 512", "const A = MOBILE ? 512 : 1024, E = new Float32Array(A * A * 3), SA = 512, UP = A / SA")
rep("if (w > 0) for (let dy = 0; dy < 2; dy++) for (let dx = 0; dx < 2; dx++) { const o = ((y * 2 + dy) * A + x * 2 + dx) * 3;",
    "if (w > 0) for (let dy = 0; dy < UP; dy++) for (let dx = 0; dx < UP; dx++) { const o = ((y * UP + dy) * A + x * UP + dx) * 3;")
rep("big = MOBILE ? (GLB_BLDS.has(k) && GLB_BN++ < 8 ? 1536 : 1024) : 2048", "big = MOBILE ? (GLB_BLDS.has(k) && !IOS && GLB_BN++ < 8 ? 1536 : 1024) : 2048")
open(p, "w").write(h); print("ok")
