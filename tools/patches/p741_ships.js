/* v741 the Continuum's hulls, remastered toward the owner's concept paintings: layered black-chrome armour plates, blade prows,
   rows of crimson window slits, a radial red "eye" reactor, reactor hoops, spires on top and stalactite spikes hanging below the
   capital ships, the Ark's chamber row, the Relay's ringed tower on its rock, the Prime Ark's citadel with its anchor pylons, and the
   Eternal Commander's four blades. Every hull points along +x; engines sit at the stern. */
function buildCnt(k) { const C = cntMats(), g = new TH.Group(), r = rnd(hash("cnt2" + k)); g.userData.eng = []; g.userData.engCol = [0xffc0c6, 0xff2a3a];
  const V = (x, y, z) => new TH.Vector3(x, y, z), add = (m, x, y, z) => { m.position.set(x || 0, y || 0, z || 0); g.add(m); return m; };
  const box = (w, h, d, mat, x, y, z, rx, ry, rz) => { const m = add(new TH.Mesh(new TH.BoxGeometry(w, h, d), mat), x, y, z); m.rotation.set(rx || 0, ry || 0, rz || 0); return m; };
  const cyl = (r0, r1, h, mat, x, y, z, ax, seg) => { const m = add(new TH.Mesh(new TH.CylinderGeometry(r1, r0, h, seg || 12), mat), x, y, z); if (ax === "x") m.rotation.z = -Math.PI / 2; if (ax === "z") m.rotation.x = Math.PI / 2; return m; };
  const ring = (rr, t, mat, x, y, z, ax, seg) => { const m = add(new TH.Mesh(new TH.TorusGeometry(rr, t, 6, seg || 40), mat), x, y, z); if (ax === "x") m.rotation.y = Math.PI / 2; if (ax === "y") m.rotation.x = Math.PI / 2; return m; };
  const ball = (rr, mat, x, y, z) => add(new TH.Mesh(new TH.SphereGeometry(rr, 16, 12), mat), x, y, z);
  /* a cone from p toward dir */
  const spike = (p, dir, len, rad, mat) => { const geo = new TH.ConeGeometry(rad, len, 5); geo.translate(0, len / 2, 0); const m = add(new TH.Mesh(geo, mat || C.hull), p.x, p.y, p.z); m.quaternion.setFromUnitVectors(V(0, 1, 0), dir.clone().normalize()); return m; };
  /* an armour plate: the outline [x, z] on one side (mirrored), extruded hTop up and hBot down, its top and bottom pulled in by inset */
  const prism = (pts, hTop, hBot, inset, mat, x, y, z) => { const full = pts.concat(pts.slice().reverse().map(([a, b]) => [a, -b])).filter((p, i, A) => i === 0 || p[0] !== A[i - 1][0] || p[1] !== A[i - 1][1]);
    const n = full.length, P = [], I = [], ring3 = (yy, k2) => full.forEach(([a, b]) => P.push(a * (1 - (1 - k2) * .25), yy, b * k2));
    ring3(hTop, inset); ring3(0, 1); ring3(-hBot, inset);
    const tri = TH.ShapeUtils.triangulateShape(full.map(([a, b]) => new TH.Vector2(a, b)), []);
    for (const [a, b, c] of tri) { I.push(a, c, b); I.push(2 * n + a, 2 * n + b, 2 * n + c); }
    for (let i = 0; i < n; i++) { const j = (i + 1) % n; I.push(i, j, n + i, j, n + j, n + i, n + i, n + j, 2 * n + i, n + j, 2 * n + j, 2 * n + i); }
    const geo = new TH.BufferGeometry(); geo.setAttribute("position", new TH.Float32BufferAttribute(P, 3)); geo.setIndex(I); const ng = geo.toNonIndexed(); ng.computeVertexNormals(); return add(new TH.Mesh(ng, mat), x, y, z); };
  /* a row of crimson window slits along the hull side, dashed like lit decks */
  const slits = (x0, x1, y, z, h, gap, mat) => { const L = x1 - x0, n = Math.max(2, Math.round(L / (gap || .34))); for (let i = 0; i < n; i++) { if (r() < .22) continue; const w = L / n * (.45 + r() * .3); box(w, h || .05, .03, mat || C.red, x0 + (i + .5) * L / n, y, z); } };
  /* the radial red eye: a chrome housing, a glowing core, and spokes */
  const eye = (x, y, z, rr, ax) => { ring(rr, rr * .16, C.chrome, x, y, z, ax || "z"); ball(rr * .45, C.red, x, y, z); ring(rr * .72, rr * .05, C.red, x, y, z, ax || "z");
    for (let i = 0; i < 8; i++) { const a = i / 8 * TAU, s = box(rr * .55, rr * .06, rr * .06, C.redDim, x + (ax === "y" ? Math.cos(a) * rr * .55 : Math.cos(a) * rr * .55), y + (ax === "y" ? 0 : Math.sin(a) * rr * .55), z + (ax === "y" ? Math.sin(a) * rr * .55 : 0)); s.rotation.set(ax === "y" ? 0 : 0, ax === "y" ? -a : 0, ax === "y" ? 0 : a); } };
  /* stalactites under a capital hull, and spires on its back */
  const hang = (x0, x1, y, n, len, w) => { for (let i = 0; i < n; i++) { const x = x0 + (x1 - x0) * (i + .5) / n, z = (r() - .5) * w; spike(V(x, y, z), V(-.15, -1, 0), len * (.5 + r() * .8), len * .09, r() < .5 ? C.hull : C.chrome); } };
  const spires = (x0, x1, y, n, len, w) => { for (let i = 0; i < n; i++) { const x = x0 + (x1 - x0) * (i + .5) / n, z = (r() - .5) * w, l = len * (.5 + r() * .9); spike(V(x, y, z), V(0, 1, 0), l, len * .06, C.chrome); if (r() < .35) ball(len * .035, C.red, x, y + l * .9, z); } };
  const eng = (x, y, z, rr) => { g.userData.eng.push([x, y, z, rr]); cyl(rr * 1.15, rr * .95, rr * 1.4, C.joint, x + rr * .5, y, z, "x", 10); ring(rr * .95, rr * .12, C.red, x - rr * .15, y, z, "x", 20); };
  if (k === "cnint") { /* the interceptor: a forward-swept dart, wings angled up, one radial red eye amidships, twin red thrusters */
    prism([[2.6, 0], [1.2, .28], [.2, .42], [-1.2, .5], [-1.5, .3], [-1.5, 0]], .34, .24, .5, C.hull); prism([[2.1, 0], [.6, .2], [-1.2, .26], [-1.3, 0]], .34, .04, .3, C.chrome, 0, .16);
    prism([[.7, 0], [-.8, .1], [-1.7, 2.1], [-2.05, 2.15], [-1.7, .3], [-1.7, 0]], .08, .06, .7, C.hull, 0, .05, 0); prism([[0, 0], [-1, .1], [-1.6, 1.7], [-1.8, 1.7], [-1.6, 0]], .12, .02, .6, C.chrome, 0, .14, 0);
    for (const s of [1, -1]) { spike(V(-1.75, .2, 2.05 * s), V(-.3, 1, .2 * s), .8, .07, C.chrome); slits(-1.5, -.3, .17, 1.0 * s, .04, .2); }
    eye(.35, .16, .48, .26, "z"); for (const s of [1, -1]) slits(.6, 2, -.04, .3 * s, .035, .22); for (const s of [1, -1]) spike(V(2.1, -.1, .12 * s), V(1, -.05, .15 * s), .9, .06, C.chrome); eng(-1.55, .05, .28, .2); eng(-1.55, .05, -.28, .2); }
  else if (k === "cncor") { /* the corvette: a slim hull under a tall folding antenna array and two jamming dishes */
    prism([[2.2, 0], [1, .42], [-1.4, .55], [-1.8, .32], [-1.8, 0]], .36, .3, .5, C.hull); prism([[1.5, 0], [.4, .3], [-1.4, .38], [-1.5, 0]], .6, .04, .45, C.chrome, 0, .2);
    cyl(.07, .04, 2, C.joint, -.1, 1.4, 0, null, 6); for (const [y, w] of [[.9, 1.2], [1.45, .9], [1.95, .6]]) { box(.05, .05, w, C.chrome, -.1, y, 0); spike(V(-.1, y, w / 2), V(0, .3, 1), .25, .03, C.chrome); spike(V(-.1, y, -w / 2), V(0, .3, -1), .25, .03, C.chrome); }
    for (const s of [1, -1]) { const d = add(new TH.Mesh(new TH.SphereGeometry(.46, 18, 8, 0, TAU, 0, Math.PI / 2.6), C.chrome), -.55, .6, .68 * s); d.rotation.x = s * 1.15; const rr = ring(.4, .035, C.red, -.55, .62, .76 * s); rr.rotation.x = s * 1.15 + Math.PI / 2; ball(.07, C.red, -.55, .6, .95 * s); }
    for (const s of [1, -1]) slits(-1.5, 1, .02, .55 * s, .04); spike(V(2, -.05, 0), V(1, 0, 0), .7, .08, C.chrome); hang(-1, 1, -.25, 4, .4, .5); eng(-1.85, 0, .18, .22); eng(-1.85, 0, -.18, .22); }
  else if (k === "cnexe") { /* the destroyer: a long blade prow, plates layered back to a big reactor hoop, twin turrets, fins below */
    prism([[3.6, 0], [2, .32], [.4, .62], [-1.8, .78], [-2.4, .55], [-2.4, 0]], .42, .36, .55, C.hull); prism([[3.2, 0], [1.4, .22], [-1.9, .42], [-2.1, 0]], .5, .04, .35, C.chrome, 0, .24);
    prism([[1.4, 0], [.2, .26], [-1.4, .42], [-1.5, 0]], .55, .04, .35, C.hull, 0, .55); for (const s of [1, -1]) { const p = prism([[2.4, 0], [.6, .1], [-.4, .25], [-.2, 0]], .1, .1, .6, C.hull, 0, .1, .55 * s); p.rotation.x = s * .3; }
    for (const [x, z] of [[1.1, 0], [.1, 0]]) { box(.55, .22, .55, C.gun, x, 1.1, z); for (const dz of [.13, -.13]) cyl(.06, .06, 1.2, C.gun, x + .8, 1.15, z + dz, "x", 8); }
    ring(.78, .13, C.hull, -1.15, .15, 0, "x"); ring(.6, .06, C.red, -1.25, .15, 0, "x"); eye(-1.3, .15, 0, .36, "x"); eye(-1.25, .1, .62, .3, "z"); for (const s of [1, -1]) { slits(-2, 2.2, .05, .66 * s, .05); slits(-1.6, 1.2, .45, .5 * s, .04); }
    hang(-1.8, 1.8, -.3, 5, .7, .5); eng(-2.45, 0, .35, .27); eng(-2.45, 0, -.35, .27); }
  else if (k === "cnfab") { /* the carrier: a long barge with three open bays of crimson light, cranes on top, drones in the bays */
    prism([[3.3, 0], [2.6, .95], [-2.8, 1.05], [-3.3, .75], [-3.3, 0]], .48, .55, .7, C.hull); prism([[2.4, 0], [1.4, .55], [-2.6, .6], [-2.7, 0]], .85, .04, .6, C.chrome, 0, .3);
    for (const x of [1.5, 0, -1.5]) { box(1.1, .62, .3, C.hull, x, 0, 1.08); box(.95, .44, .05, C.redDim, x, 0, 1.22); for (const dx of [-.25, .1]) { const d = prism([[.18, 0], [-.1, .1], [-.18, 0]], .05, .03, .6, C.chrome, x + dx, .05, 1.34); d.rotation.x = Math.PI / 2; } }
    for (const x of [1.6, .2, -1.2]) { box(.14, .9, .14, C.joint, x, .95, -.55); box(.9, .1, .1, C.joint, x + .4, 1.4, -.55); }
    for (const s of [1, -1]) slits(-2.8, 2.6, .5, .78 * s, .04); spires(-2, 1, .85, 4, .9, .5); hang(-2.5, 2.4, -.45, 7, .7, 1.3); eng(-3.35, 0, .55, .32); eng(-3.35, 0, -.55, .32); eng(-3.35, .3, 0, .26); }
  else if (k === "cnasm") { /* the assimilation cruiser: a mantis hull, salvage arms folded forward, a dome of icy-blue processors */
    prism([[2.8, 0], [1.6, .48], [-.6, .8], [-2.2, .62], [-2.5, 0]], .5, .42, .55, C.hull); prism([[2.1, 0], [.8, .36], [-1.9, .46], [-2, 0]], .78, .04, .5, C.chrome, 0, .24);
    add(new TH.Mesh(new TH.SphereGeometry(.62, 20, 10, 0, TAU, 0, Math.PI / 2), C.blue), -.7, .72, 0).scale.set(1.35, .62, 1); ring(.66, .05, C.chrome, -.7, .74, 0, "y");
    for (const s of [1, -1]) for (const x of [1.3, .1]) { const a = V(x, 0, .7 * s), b = V(x + .9, -.15, 1.35 * s), c = V(x + 1.8, -.2, .95 * s), d = V(x + 2.1, -.1, .75 * s);
      for (const [p, q] of [[a, b], [b, c], [c, d]]) { const dv = q.clone().sub(p), m = cyl(.075, .06, dv.length(), C.joint, (p.x + q.x) / 2, (p.y + q.y) / 2, (p.z + q.z) / 2, null, 6); m.quaternion.setFromUnitVectors(V(0, 1, 0), dv.normalize()); } ball(.1, C.chrome, b.x, b.y, b.z); spike(d, V(1, -.2, -.3 * s), .3, .05, C.chrome); }
    eye(2.15, .2, 0, .22, "x"); for (const s of [1, -1]) slits(-2, 1.3, .2, .82 * s, .045); hang(-1.6, 1.2, -.35, 4, .5, .6); eng(-2.55, 0, .35, .28); eng(-2.55, 0, -.35, .28); }
  else if (k === "cndre" || k === "cncom") { /* the dreadnought: a wedge of armour slabs, heavy turrets, a caged crimson reactor eye, spikes beneath */
    prism([[3.9, 0], [2.4, .95], [-.4, 1.55], [-2.9, 1.65], [-3.4, 1.15], [-3.4, 0]], .72, .62, .6, C.hull); prism([[3.4, 0], [1.6, .7], [-2.4, 1.1], [-2.6, 0]], .7, .04, .4, C.chrome, 0, .42);
    prism([[1.6, 0], [.3, .5], [-1.9, .7], [-2.1, 0]], .8, .04, .35, C.hull, 0, 1); for (const s of [1, -1]) { const p = prism([[2.6, 0], [.5, .2], [-1.5, .4], [-1.3, 0]], .14, .14, .6, C.hull, -.2, .2, 1.2 * s); p.rotation.x = s * .35; }
    for (const [x, z] of [[1.5, .5], [1.5, -.5], [-.3, .95], [-.3, -.95], [.6, 0]]) { box(.6, .26, .55, C.gun, x, 1.05 + (z ? 0 : .5), z); for (const dz of [.12, -.12]) cyl(.07, .07, 1.25, C.gun, x + .8, 1.12 + (z ? 0 : .5), z + dz, "x", 8); }
    ring(1.05, .15, C.hull, -1.1, .2, 0, "x"); ring(.85, .08, C.red, -1.2, .2, 0, "x"); eye(-1.25, .2, 0, .55, "x"); eye(.6, .1, 1.05, .38, "z"); for (const s of [1, -1]) { slits(-3, 2.6, 0, 1.28 * s, .06); slits(-2.4, 1.8, .6, .95 * s, .05); }
    hang(-2.8, 2.6, -.55, 9, 1.1, 2); if (k === "cncom") { spires(-1.6, -.4, 1.6, 5, 1.6, .6); ball(.2, C.red, -1, 2.5, 0); }
    eng(-3.45, 0, .7, .38); eng(-3.45, 0, -.7, .38); eng(-3.45, .5, 0, .32); }
  else if (k === "cnrel") { /* the relay: a ringed transmission tower on its rock, a crimson column inside, a beam from the tip */
    add(new TH.Mesh(new TH.DodecahedronGeometry(1.7, 1), new TH.MeshStandardMaterial({ color: 0x060505, roughness: 1, metalness: 0, flatShading: true, envMapIntensity: 0 })), 0, -1.5, 0).scale.set(1.5, .62, 1.3);
    box(2.6, .2, 1.6, C.hull, 0, -.75, 0); for (const s of [1, -1]) box(.8, .5, .4, C.hull, .9 * s, -.45, .7 * s);
    cyl(.75, .32, 4.2, C.hull, 0, 1.4, 0, null, 8); cyl(.36, .05, 1.8, C.chrome, 0, 4.4, 0, null, 8); cyl(.13, .13, 4.4, C.red, 0, 1.6, .36, null, 6);
    for (const [y, rr] of [[.9, 1.85], [2.2, 1.45]]) { ring(rr, .16, C.hull, 0, y, 0, "y", 48); ring(rr, .05, C.red, 0, y + .1, 0, "y", 48); for (let i = 0; i < 6; i++) { const a = i / 6 * TAU; box(rr, .07, .07, C.joint, Math.cos(a) * rr / 2, y, Math.sin(a) * rr / 2, 0, -a); } }
    spires(-.5, .5, 3, 5, 1.2, .8); cyl(.04, .04, 2.4, C.red, 0, 6.3, 0, null, 6); ball(.24, C.red, 0, 5.3, 0); }
  else if (k === "cnark") { /* the Ark: a long armoured spine through three hoops, a row of chambers holding machine frames and red cores, cathedral spires, stalactites */
    prism([[5.6, 0], [3.8, .7], [-3.8, .95], [-4.8, .65], [-4.8, 0]], .95, .95, .7, C.hull); prism([[4.6, 0], [3.1, .5], [-4, .62], [-4.2, 0]], 1.45, .04, .6, C.chrome, 0, .5);
    for (const s of [1, -1]) { const p = prism([[5, 0], [2, .2], [-3, .4], [-3.4, 0]], .2, .2, .6, C.hull, 0, -.2, .9 * s); p.rotation.x = s * .25; }
    for (const x of [2.8, -.1, -3.1]) { ring(2.05, .24, C.hull, x, .3, 0, "x", 48); ring(2.05, .07, C.red, x - .26, .3, 0, "x", 48); ring(1.7, .05, C.joint, x + .2, .3, 0, "x", 48); }
    for (let i = 0; i < 6; i++) { const x = 2.2 - i * 1.0; cyl(.34, .34, 1.05, C.glass, x, .25, 1.02, null, 12); ring(.34, .04, C.chrome, x, .78, 1.02, "y", 16); ring(.34, .04, C.chrome, x, -.28, 1.02, "y", 16); box(.08, .55, .06, C.joint, x, .25, 1.06); box(.32, .06, .06, C.joint, x, .38, 1.06); ball(.11, C.red, x, .2, 1.16); }
    eye(4.6, .45, .7, .42, "z"); for (const s of [1, -1]) slits(-4.4, 4.6, -.35, .95 * s, .06, .28); slits(-3.8, 3.8, .9, .62, .05); spires(-3.2, 3, 1.4, 10, 2, .8); hang(-4.2, 4.6, -.9, 12, 1.6, 1.2);
    for (const x of [1, -1.6]) box(1.5, .5, .32, C.redDim, x, -.65, -.88); eng(-4.9, 0, .5, .46); eng(-4.9, 0, -.5, .46); eng(-4.9, .55, 0, .36); }
  else if (k === "cnprime") { /* the Prime Ark: a citadel column with a crimson reactor running its height, two great rings, three anchor pylons, spires and stalactites */
    cyl(1.25, .95, 7.2, C.hull, 0, 0, 0, null, 10); cyl(.42, .42, 7.8, C.red, 0, 0, 0, null, 8); for (let i = 0; i < 10; i++) { const a = i / 10 * TAU; box(.12, 6.6, .12, C.chrome, Math.cos(a) * 1.08, 0, Math.sin(a) * 1.08); }
    for (const [y, rr] of [[1.7, 3.8], [-1.5, 3.35]]) { ring(rr, .34, C.hull, 0, y, 0, "y", 64); ring(rr, .1, C.red, 0, y + .22, 0, "y", 64); for (let i = 0; i < 8; i++) { const a = i / 8 * TAU; box(rr - 1, .16, .16, C.joint, Math.cos(a) * (rr + 1) / 2, y, Math.sin(a) * (rr + 1) / 2, 0, -a); } }
    for (let i = 0; i < 3; i++) { const a = i * TAU / 3 + .3, x = Math.cos(a) * 4.8, z = Math.sin(a) * 4.8; box(4.8, .28, .28, C.joint, x / 2, .3, z / 2, 0, -a); cyl(.42, .1, 2.8, C.hull, x, .6, z, null, 6); spike(V(x, -.8, z), V(0, -1, 0), 1.4, .3, C.hull); ball(.28, C.red, x, 2.1, z); ring(.5, .05, C.red, x, 1.2, z, "y", 16); }
    spires(-1, 1, 3.6, 9, 2.6, 2); for (let i = 0; i < 14; i++) { const a = i / 14 * TAU, rr = 1.2 + r() * 1.6; spike(V(Math.cos(a) * rr, -3.4, Math.sin(a) * rr), V(0, -1, 0), 1 + r() * 2.2, .22, C.hull); } }
  else if (k === "cneter") { /* the Eternal Commander: four long tapering blades from a ribbed hub, machinery along their undersides, a crimson heart */
    for (const [a, l] of [[.52, 4.6], [-.52, 4.6], [Math.PI - .5, 3.8], [-(Math.PI - .5), 3.8]]) { const p = prism([[l, 0], [l * .4, .26], [0, .44], [-.5, 0]], .3, .24, .45, C.hull); p.rotation.y = -a; const q = prism([[l * .85, 0], [l * .3, .16], [0, .26], [-.3, 0]], .46, .02, .4, C.chrome); q.rotation.y = -a; q.position.y = .1;
      for (let i = 1; i < 6; i++) { const t = i / 6 * l * .75, x = Math.cos(a) * t, z = -Math.sin(a) * t; box(.28, .12, .2, C.joint, x, -.28, z, 0, -a); if (i % 2) box(.16, .04, .04, C.red, x, -.2, z + .14, 0, -a); } }
    prism([[1.4, 0], [.6, .6], [-.6, .7], [-1.3, .4], [-1.3, 0]], .5, .4, .45, C.hull); prism([[1, 0], [.3, .4], [-.9, .45], [-1, 0]], .75, .02, .4, C.chrome, 0, .1); eye(.1, .05, .72, .34, "z");
    ball(.2, C.red, .2, .6, 0); for (const s of [1, -1]) slits(-1, 1.8, .12, .62 * s, .04); eng(-1.5, 0, .38, .3); eng(-1.5, 0, -.38, .3); }
  g.userData.cnt = 2; return g; }
