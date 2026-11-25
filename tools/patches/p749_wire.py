"""v749: the map no longer stalls every half second. Each world near the camera finds its nearest neighbour (v264, so crowded worlds
shrink to fit) by checking every other near world: 3000 x 3000 distances every 450 ms on the Balanced preset, a 40-50 ms freeze
that made the map jump. Now the worlds are bucketed on a 5-unit grid and each looks only at its own and the 8 neighbouring cells:
the same sizes (a neighbour farther than 5 units never shrinks a world), about a fifteenth of the work."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 748;", "const GAME_V = 749;")
rep("""    for (let a = 0; a < L.length; a++) { let nn = 1e9; const qa = L[a][1]; for (let b2 = 0; b2 < L.length; b2++) { if (a === b2) continue; const qb = L[b2][1], d2 = (qa.x - qb.x) ** 2 + (qa.y - qb.y) ** 2 + (qa.z - qb.z) ** 2; if (d2 < nn) nn = d2; }""",
    """    const NNC = 5, NNG = new Map(), nnK = (x, z) => (x + 50000) * 100000 + (z + 50000); /* v749 a 5-unit grid: only neighbouring cells are compared */
    for (let a = 0; a < L.length; a++) { const q = L[a][1], k = nnK(Math.floor(q.x / NNC), Math.floor(q.z / NNC)); let bk = NNG.get(k); if (!bk) NNG.set(k, bk = []); bk.push(a); }
    for (let a = 0; a < L.length; a++) { let nn = 1e9; const qa = L[a][1], cx = Math.floor(qa.x / NNC), cz = Math.floor(qa.z / NNC);
      for (let dx = -1; dx <= 1; dx++) for (let dz = -1; dz <= 1; dz++) { const bk = NNG.get(nnK(cx + dx, cz + dz)); if (bk) for (const b2 of bk) { if (a === b2) continue; const qb = L[b2][1], d2 = (qa.x - qb.x) ** 2 + (qa.y - qb.y) ** 2 + (qa.z - qb.z) ** 2; if (d2 < nn) nn = d2; } }""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
