# v367: a street grid on the bigger deck (the user's suggestion). Two avenues each way (x = +-5.4, +-15.6; z = +-4.6, +-12.8) make 24 blocks round
# the HQ; each building moved to a block near where it was (an optimal assignment, most moves 1-7 units); the two small buildings take the
# cut corners. Roads, energy lanes and street lights follow the grid, short links join the HQ ring road to the avenues, the crew's
# path-finding prefers the grid roads, and the cargo clutter keeps off them.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep("/* v367 the deck outline:", r'''/* v367 the street grid and the block each building stands in */
const GRID_X = [-15.6, -5.4, 5.4, 15.6], GRID_Z = [-12.8, -4.6, 4.6, 12.8];
Object.assign(BPOS, { repairYard: [-19, -15.8], crystalMine: [-10.5, -16.7], flagDock: [0, -16.7], gasSynth: [10.5, -16.7], missileSilo: [19, -15.8],
  terraformer: [-20.05, -8.7], metalMine: [-10.5, -8.7], solar: [0, -8.7], radar: [10.5, -8.7], fusion: [20.05, -8.7],
  metalStore: [-20.05, 0], crystalStore: [-10.5, 0], gasTank: [10.5, 0], phalanx: [20.05, 0],
  allyDepot: [-20.05, 8.7], lab: [-10.5, 8.7], robotics: [0, 8.7], shipyard: [10.5, 8.7], fortress: [20.05, 8.7],
  lunarBase: [-10.5, 16.7], nanite: [0, 16.7], jumpGate: [10.5, 16.7] });
const onRoad = (x, z, pad) => { pad = pad || 0; const w = .625 + pad; return (GRID_X.some(v => Math.abs(x - v) < w) || GRID_Z.some(v => Math.abs(z - v) < w)) && deckIn(x, z) > .7 - pad; };
/* v367 the deck outline:''')
# the roads
rep('''  for (const k of keys) { const [x, z] = BPOS[k], len = Math.hypot(x, z) - 2.5 - 4.3, ang = Math.atan2(z, x), r0 = 4.3, mx = Math.cos(ang) * (len / 2 + r0), mz = Math.sin(ang) * (len / 2 + r0); if (len <= .2) continue;''',
'''  /* v367 the street grid: each avenue runs edge to edge of the deck, lamps along both sides away from buildings and crossings */
  const segs = []; const inDeck = (x, z) => deckIn(x, z) > 1.1;
  for (const v of GRID_X) { let a = 0, b = 0; while (inDeck(v, a - .2)) a -= .2; while (inDeck(v, b + .2)) b += .2; segs.push([v, (a + b) / 2, b - a, Math.PI / 2]); }
  for (const v of GRID_Z) { let a = 0, b = 0; while (inDeck(a - .2, v)) a -= .2; while (inDeck(b + .2, v)) b += .2; segs.push([(a + b) / 2, v, b - a, 0]); }
  for (const [ax, az] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const r1 = ax ? Math.abs(GRID_X[2]) : Math.abs(GRID_Z[2]), len = r1 - 4.2 + .2; if (len > .1) segs.push([ax * (4.2 + len / 2), az * (4.2 + len / 2), len, ax ? 0 : Math.PI / 2]); } // the HQ ring road to the avenues
  const nearB = (x, z, r) => keys.some(k => BPOS[k] && Math.hypot(x - BPOS[k][0], z - BPOS[k][1]) < r);
  for (const [mx, mz, len, ang] of segs) {''')
rep('''    for (let d = 1.2; d < len - .6; d += 2.6) for (const s of [-1, 1]) { const px = Math.cos(ang) * (r0 + d) - Math.sin(ang) * s * .78, pz = Math.sin(ang) * (r0 + d) + Math.cos(ang) * s * .78; lamps.push([px, pz]); } }''',
'''    for (let d = -len / 2 + 1.3; d < len / 2 - .6; d += 2.6) for (const s of [-1, 1]) { const px = mx + Math.cos(ang) * d - Math.sin(ang) * s * .78, pz = mz + Math.sin(ang) * d + Math.cos(ang) * s * .78;
      if (nearB(px, pz, 3.3) || Math.hypot(px, pz) < 4.8 || GRID_X.some(v => Math.abs(px - v) < 1.1) && GRID_Z.some(v => Math.abs(pz - v) < 1.1)) continue; lamps.push([px, pz]); } }''')
rep("  for (const k of keys) { const [x, z] = BPOS[k], ang = Math.atan2(z, x); for (let i = -2; i <= 2; i++) { const s = new TH.Mesh(new TH.PlaneGeometry(.5, .12), zebra), r = 4.0;",
    "  for (const ang of [0, Math.PI / 2, Math.PI, -Math.PI / 2]) { for (let i = -2; i <= 2; i++) { const s = new TH.Mesh(new TH.PlaneGeometry(.5, .12), zebra), r = 4.0;")
# path-finding: the grid roads are the roads
rep("if (rr >= 3.4 && rr <= 4.35) road[n] = 1; else for (const k in W.keys) { if (!BPOS[k]) continue; const [bx, bz] = BPOS[k], L = Math.hypot(bx, bz), ux = bx / L, uz = bz / L, d = x * ux + z * uz; if (d > 4.3 && d < L - 2.5 && Math.abs(-x * uz + z * ux) < .62) { road[n] = 1; break; } } }",
    "if (rr >= 3.4 && rr <= 4.35) road[n] = 1; else if (onRoad(x, z) || (Math.abs(x) < .62 || Math.abs(z) < .62) && rr < 5.5) road[n] = 1; } // v367 the street grid")
rep("const free = (x, z, own) => deckIn(x, z) > 2.4 && Math.hypot(x, z) > 4.8", "const free = (x, z, own) => deckIn(x, z) > 2.4 && !onRoad(x, z, .35) && Math.hypot(x, z) > 4.8")
open(p, "w").write(h); print("ok")
