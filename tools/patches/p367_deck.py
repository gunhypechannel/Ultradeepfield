# v367: the base deck was a 38 x 31 slab, but v-era spacing (BSP 1.35) put the outer plots at its edge or past it (Fusion Plant, Phalanx,
# Geo-Former, Coalition Depot, Lunar Outpost, Warp Gate), so they hung off. The deck is now an octagon 49 x 41.2 with its corners cut on a
# 28.4 circle (inside the transit ring at 30); every plot centre is >= 4.25 inside it. The border light, struts, pebble field, clutter area and
# the turret ring follow the new outline; turrets step aside from buildings near the edge.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep("const BSP = 1.35; for (const k in BPOS) BPOS[k] = [BPOS[k][0] * BSP, BPOS[k][1] * BSP];", r'''const BSP = 1.35; for (const k in BPOS) BPOS[k] = [BPOS[k][0] * BSP, BPOS[k][1] * BSP];
/* v367 the deck outline: an octagon, its corners cut on a circle inside the transit ring. deckPoly(inset) gives its corners, deckIn the distance inside it */
const DECK = { X: 24.5, Z: 20.6, R: 28.4 };
function deckPoly(ins) { ins = ins || 0; const X = DECK.X - ins, Z = DECK.Z - ins, R = DECK.R - ins * 1.08, zc = Math.sqrt(Math.max(1, R * R - X * X)), xc = Math.sqrt(Math.max(1, R * R - Z * Z));
  return [[X, -zc], [X, zc], [xc, Z], [-xc, Z], [-X, zc], [-X, -zc], [-xc, -Z], [xc, -Z]]; }
function deckIn(x, z) { const P = deckPoly(); let m = 1e9; for (let i = 0; i < 8; i++) { const [ax, az] = P[i], [bx, bz] = P[(i + 1) % 8], ex = bx - ax, ez = bz - az, L = Math.hypot(ex, ez), nx = ez / L, nz = -ex / L;
    let d = (x - ax) * nx + (z - az) * nz; if (-ax * nx - az * nz < 0) d = -d; m = Math.min(m, d); } return m; }''')
rep("  dt.wrapS = dt.wrapT = TH.RepeatWrapping; dt.repeat.set(2.7, 2.2);", "  dt.wrapS = dt.wrapT = TH.RepeatWrapping; dt.repeat.set(.0711, .0711); // v367 the deck's UVs are in world units")
rep("  const deck = new TH.Mesh(new TH.BoxGeometry(38, 1.3, 31), [side, side, top, side, side, side]); deck.position.y = -.65; deck.receiveShadow = true; scene.add(deck);",
    "  const deckSh = new TH.Shape(deckPoly().map(([x, z]) => new TH.Vector2(x, -z))), deckG = new TH.ExtrudeGeometry(deckSh, { depth: 1.3, bevelEnabled: false }).rotateX(-Math.PI / 2).translate(0, -1.3, 0);\n  const deck = new TH.Mesh(deckG, [top, side]); deck.receiveShadow = true; scene.add(deck); // v367 the octagon deck")
rep("    for (const [x, z] of [[-18, -14.5], [18, -14.5], [-18, 14.5], [18, 14.5], [0, -15], [0, 15], [-18.5, 0], [18.5, 0], [-9, -15], [9, 15]]) {",
    "    const PV = deckPoly(.8); for (const [x, z] of PV.concat(PV.map((v, i) => [(v[0] + PV[(i + 1) % 8][0]) / 2, (v[1] + PV[(i + 1) % 8][1]) / 2]))) {")
rep("  for (const [w, d, x, z] of [[38, .12, 0, 15.5], [38, .12, 0, -15.5], [.12, 31, 19, 0], [.12, 31, -19, 0]]) scene.add(cbox(w, .1, d, C.cyan, x, -.02, z));",
    "  { const PV = deckPoly(.06); PV.forEach(([ax, az], i) => { const [bx, bz] = PV[(i + 1) % 8], L = Math.hypot(bx - ax, bz - az), m = cbox(L, .1, .12, C.cyan, (ax + bx) / 2, -.02, (az + bz) / 2); m.rotation.y = -Math.atan2(bz - az, bx - ax); scene.add(m); }); } // v367 the border light")
rep("const x = (pr() - .5) * 52, z = (pr() - .5) * 46; if (Math.abs(x) < 19.6 && Math.abs(z) < 16.1) continue; if (Math.hypot(x * .82, z) > 24.5) continue;",
    "const x = (pr() - .5) * 62, z = (pr() - .5) * 54; if (deckIn(x, z) > -.6) continue; if (Math.hypot(x * .82, z) > 25.5) continue;")
rep("const free = (x, z, own) => Math.abs(x) < 17.4 && Math.abs(z) < 13.8 && Math.hypot(x, z) > 4.8", "const free = (x, z, own) => deckIn(x, z) > 2.4 && Math.hypot(x, z) > 4.8")
rep("  for (let i = 0; i < n; i++) { const t = i / n, per = 2 * (26 + 20), d = t * per; let x, z;\n    if (d < 26) { x = (-13 + d) * 1.38; z = -14.6; } else if (d < 46) { x = 18.2; z = (-10 + (d - 26)) * 1.42; } else if (d < 72) { x = (13 - (d - 46)) * 1.38; z = 14.6; } else { x = -18.2; z = (10 - (d - 72)) * 1.42; }",
    '''  const PV = deckPoly(1.1), segL = PV.map((v, i) => Math.hypot(PV[(i + 1) % 8][0] - v[0], PV[(i + 1) % 8][1] - v[1])), per = segL.reduce((a, b) => a + b, 0);
  const atD = d => { d = ((d % per) + per) % per; for (let s = 0; s < 8; s++) { if (d <= segL[s]) { const [ax, az] = PV[s], [bx, bz] = PV[(s + 1) % 8], f = d / segL[s]; return [ax + (bx - ax) * f, az + (bz - az) * f]; } d -= segL[s]; } return PV[0]; };
  const clear = (x, z) => Object.values(BPOS).every(([bx, bz]) => Math.hypot(x - bx, z - bz) > 3.7);
  for (let i = 0; i < n; i++) { let x, z, d0 = (i + .5) / n * per; [x, z] = atD(d0); // v367 along the new deck edge, stepping aside from buildings
    for (let k = 1; k < 12 && !clear(x, z); k++) [x, z] = atD(d0 + (k % 2 ? 1 : -1) * Math.ceil(k / 2) * .7);''')
open(p, "w").write(h); print("ok")
