# v346: v345's building models showed as shredded spiky blobs. bakeStatic() merges a building's static parts into one mesh per material
# and copies each geometry's position/normal/uv arrays straight across. GLTFLoader gives Meshy models interleaved vertex attributes
# (position, normal and uv packed in one buffer), so those arrays held the whole interleaved buffer and the merge read normals and UVs
# as positions. The model is now left out of the merge (it is one mesh already, so there is nothing to gain).
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep("const walk = (o, M) => { for (const c of o.children) { if (moving.has(c) || c.isSprite || c.isPoints || c.isInstancedMesh) continue;",
    "const walk = (o, M) => { for (const c of o.children) { if (moving.has(c) || c.isSprite || c.isPoints || c.isInstancedMesh || c.userData.nobake) continue; /* v346 a loaded model (interleaved attributes) stays as it is */")
rep("const foot = big ? 6.2 : small ? 3.4 : 4.6, s = foot / Math.max(sz.x, sz.z, .01); m.scale.setScalar(s);",
    "const foot = big ? 6.2 : small ? 3.4 : 4.6, s = foot / Math.max(sz.x, sz.z, .01); m.scale.setScalar(s); m.userData.nobake = true;")
open(p, "w").write(h); print("ok")
