# v564 the Titan models rebuilt to match the owner's paintings (owner: "The titan models have to match closer please").
# Armageddon (epic_sci_fi_space_scene_a_colossal_dark_metallic.jpg): a broad armoured wedge with serrated blades hanging off both flanks
#   (red light along their edges), a thick spinal cannon running the length of the hull with red-glowing ribs, a muzzle of concentric
#   rings far past the bow, three great engine drums at the stern, a gothic cathedral of spires at the stern centre, multi-barrel
#   turret batteries on the deck and small spires scattered over it.
# Sovereign Ark (a_hyper_detailed_sci_fi_space_scene_a_colossal_f.jpg): two angular arrow-bowed silver hulls with gold bow caps and
#   chevrons, blue-glowing bow "eyes" and keel lines, joined at the stern by a citadel crowned with white-and-gold spires around a blue
#   crystal spire, and a gold crest plate facing forward between the hulls.
# Eclipse Harbinger (a_cinematic_ultra_detailed_sci_fi_space_scene_a.jpg): four great scythe crescents (two forward, two aft, mirrored)
#   with green-lit hangar bays along their inner edges and violet lights, two smaller horns, a green reactor in a ring cage, a tall
#   cathedral spire above and a long spike below trailing a green beam.
# The animated parts keep their names (TI.cannon/coils/rings/plates/core, doors/lights/petals, arms x6/ringG), so the viewer sequences
# and battle effects work as before.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def cut(a, b):
    global s
    i = s.find(a); assert i >= 0 and s.count(a) == 1, a[:60]; j = s.find(b, i); assert j > i, b[:60]; return i, j

ARM = r'''  if (k === "armageddon") { ud.engCol = [0xffe0b0, 0xff4a1a]; /* v564 rebuilt after the owner's painting */
    const W1 = [[4.3, .3], [3.3, 1.05], [-2.5, 2.25], [-3.95, 2.25], [-3.95, -2.25], [-2.5, -2.25], [3.3, -1.05], [4.3, -.3]], sc = (P2, sx, sz, dx) => P2.map(([x, z]) => [x * sx + (dx || 0), z * sz]);
    const hw = x => x <= -2.5 ? 2.25 : x <= 3.3 ? 2.25 + (x + 2.5) / 5.8 * (1.05 - 2.25) : 1.05 + (x - 3.3) * (.3 - 1.05);
    add(ext(W1, .62, MT.hull, .05), 0, -.35, 0); add(ext(sc(W1, .9, .8, -.2), .36, MT.hull, .04), 0, .32, 0); add(ext(sc(W1, .7, .52, -.5), .24, MT.dark, .03), 0, .72, 0);
    add(ext(sc(W1, .82, .72, -.3), .3, MT.dark, .03), 0, -.68, 0); add(ext([[3.9, .05], [1.0, .3], [-2.8, .34], [-2.8, -.34], [1.0, -.3], [3.9, -.05]], .5, MT.trim, .02), 0, -1.16, 0); // belly and keel blade
    for (const s of [1, -1]) for (let x = -3.7; x <= 3.2; x += .34) { const z = s * hw(x) * 1.0, L = .55 + .35 * Math.abs(Math.sin(x * 1.7)), fin = new TH.Group(); fin.position.set(x, -.2, z); fin.rotation.x = s * .38; fin.rotation.y = s * -.15; g.add(fin); /* the serrated blades hanging off its flanks */
      const bl = add(ext([[.16, 0], [-.16, 0], [-.1, L], [.02, L + .22]], .07, MT.hull, .01), 0, 0, 0, fin); bl.rotation.x = Math.PI / 2; box(.03, .02, L * .8, MT.glow, .1, .085, L * .45, bl); }
    for (let x = -3.4; x <= 2.6; x += .3) { const w = hw(x) * .7; for (const s of [1, -1]) { box(.18, .03, .05, MT.glow, x, .69, s * w); box(.05, .32, .05, MT.dark, x, .45, s * w * 1.25); } } for (const s of [1, -1]) { box(5.0, .035, .07, MT.glow, -.1, 1.0, s * .72); box(4.6, .02, .03, MT.win, -.4, 1.0, s * 1.12); } /* red vents and channels along the deck */
    for (let i = 0; i < 6; i++) { const x = -1.6 + i * .7, z = (i % 2 ? 1 : -1) * (1.05 - i * .1); cylY(.2, .24, .12, MT.dark, x, .98, z, 10); box(.26, .14, .24, MT.hull, x, 1.1, z); for (const dz of [-.07, 0, .07]) cylX(.025, .03, .5, MT.trim, x + .3, 1.12, z + dz, 8); } /* turret batteries */
    for (let i = 0; i < 18; i++) { const x = -3.4 + r() * 5.6, z = (r() - .5) * hw(x) * 1.3, h = .25 + r() * .5; add(mesh(new TH.ConeGeometry(.05 + r() * .04, h, 6), MT.dark), x, .96 + h / 2, z); } /* spires scattered over the deck */
    { const cx = -2.75; cylY(.62, .8, .5, MT.hull, cx, 1.2, 0, 8); cylY(.3, .42, 1.6, MT.dark, cx, 2.2, 0, 8); add(mesh(new TH.ConeGeometry(.24, 1.6, 8), MT.dark), cx, 3.8, 0); box(.04, 1.1, .04, MT.glow, cx + .3, 2.2, 0); add(mesh(new TH.SphereGeometry(.09, 10, 8), MT.core), cx + .32, 2.9, 0);
      for (let q = 0; q < 10; q++) { const a = q / 10 * TAU, rr = .55 + (q % 2) * .2, h = .7 + ((q * 7) % 5) * .22; cylY(.07, .1, h, MT.dark, cx + Math.cos(a) * rr, 1.45 + h / 2, Math.sin(a) * rr, 6); add(mesh(new TH.ConeGeometry(.09, .55, 6), MT.dark), cx + Math.cos(a) * rr, 1.45 + h + .27, Math.sin(a) * rr); if (q % 3 === 0) box(.02, h * .6, .02, MT.win, cx + Math.cos(a) * (rr + .09), 1.45 + h * .5, Math.sin(a) * (rr + .09)); } } /* the gothic cathedral at the stern */
    const C = new TH.Group(); g.add(C); C.position.set(0, .62, 0); C.scale.set(1, 1.3, 1.3); TI.cannon = C; // the Worldbreaker Cannon: a spine the length of the hull, glowing ribs, coils, armour and a muzzle of rings
    cylX(.3, .34, 7.4, MT.dark, 1.9, 0, 0, 24, C); cylX(.12, .12, 7.2, MT.glow, 1.9, 0, 0, 12, C); cylX(.44, .32, .5, MT.trim, 5.65, 0, 0, 24, C);
    for (let x = -1.6; x <= 2.1; x += .19) torX(.34, .035, MT.glow, x, 0, 0, C); for (let x = -1.7; x <= 2.2; x += .57) torX(.37, .06, MT.dark, x, 0, 0, C); /* the red-ribbed breech */
    TI.coils = []; for (const x of [2.5, 3.0, 3.5]) { const cg = new TH.Group(); cg.position.x = x; C.add(cg); torX(.6, .11, MT.dark, 0, 0, 0, cg); torX(.6, .035, MT.glow, 0, 0, 0, cg); for (let j = 0; j < 8; j++) { const a = j / 8 * TAU; box(.16, .16, .16, MT.trim, 0, Math.cos(a) * .6, Math.sin(a) * .6, cg); } TI.coils.push(cg); }
    TI.rings = []; for (const [x, R] of [[4.1, .42], [4.6, .5], [5.05, .58], [5.45, .66], [5.8, .74]]) { const rg = new TH.Group(); rg.position.x = x; C.add(rg); torX(R, .05, MT.trim, 0, 0, 0, rg); torX(R * .82, .03, MT.glow, 0, 0, 0, rg); for (let j = 0; j < 6; j++) { const a = j / 6 * TAU + .4; box(.06, .08, .08, MT.glow, 0, Math.cos(a) * R, Math.sin(a) * R, rg); } TI.rings.push(rg); }
    TI.plates = []; for (let j = 0; j < 4; j++) { const pg = new TH.Group(); pg.position.x = 3.0; pg.rotation.x = j / 4 * TAU + Math.PI / 4; C.add(pg); const pl = box(1.6, .07, .4, MT.hull, 0, .36, 0, pg); box(1.4, .02, .05, MT.win, 0, .41, 0, pg); TI.plates.push(pl); }
    TI.core = add(mesh(new TH.SphereGeometry(.22, 20, 14), MT.core), 6.05, 0, 0, C); TI.core.scale.setScalar(.01); TI.core.userData.fx = 2;
    for (const z of [1.45, 0, -1.45]) { const y = z ? .95 : -.1, cx = -3.75; cylX(.55, .55, 1.5, MT.hull, cx, y, z, 24); for (const dx of [-.5, 0, .5]) torX(.57, .04, MT.trim, cx + dx, y, z); torX(.57, .025, MT.glow, cx + .25, y, z); eng(-4.6, y, z, .44, .3); } /* three engine drums */
    greeb(-3.5, 2.6, .7, -1.3, 1.3, 50); greeb(-3.0, 1.8, -.88, -.9, .9, 30);
    TI.mats = [MT.glow, MT.win]; }
'''

SOV = r'''  else if (k === "sovereign") { ud.engCol = [0xffffff, 0x5fb8ff]; /* v564 rebuilt after the owner's painting */
    TI.doors = []; TI.lights = []; TI.petals = [];
    const HULL = [[4.7, 0], [3.5, .5], [2.6, .62], [-3.7, .62], [-4.15, .48], [-4.15, -.48], [-3.7, -.62], [2.6, -.62], [3.5, -.5]], sc = (P2, sx, sz, dx) => P2.map(([x, z]) => [x * sx + (dx || 0), z * sz]);
    for (const s of [1, -1]) { const z0 = s * 1.45;
      add(ext(sc(HULL, .96, .82, -.1), .3, MT.dark, .03), 0, -.62, z0); add(ext(HULL, .58, MT.hull, .04), 0, -.3, z0); add(ext(sc(HULL, .86, .62, -.25), .1, MT.hull, .03), 0, .3, z0); // keel, hull and deck: angular arrow hulls
      add(ext([[4.75, 0], [3.5, .54], [2.4, .66], [2.6, 0], [2.4, -.66], [3.5, -.54]], .06, MT.trim, .02), 0, .3, z0); // the gold bow cap
      for (const x of [1.3, -.6, -2.4]) for (const d of [1, -1]) { const ch = box(.7, .05, .06, MT.trim, x, .1, z0 + d * .64); ch.rotation.y = d * .25; }
      for (const d of [1, -1]) { const ey = box(.7, .1, .04, MT.glow, 3.75, .02, z0 + d * .43); ey.rotation.y = -d * .44; } box(6.4, .03, .03, MT.glow, -.5, -.36, z0 + s * .66); box(6.4, .03, .03, MT.glow, -.5, -.36, z0 - s * .66); // blue bow eyes and keel lines
      box(5.4, .24, .1, MT.dark, -.4, -.02, z0 + s * .66); for (let i = 0; i < 12; i++) TI.lights.push(box(.12, .05, .02, MT.win, -2.9 + i * .44, -.02, z0 + s * .715)); // the fighter launch corridor
      box(1.6, .08, .56, MT.dark, 2.0, .42, z0); const hl = box(1.5, .02, .46, MT.glow, 2.0, .465, z0); TI.lights.push(hl); for (let i = 0; i < 5; i++) TI.lights.push(box(.05, .022, .4, MT.win, 1.4 + i * .3, .47, z0)); // the hangar deck
      for (const dx of [-.39, .39]) TI.doors.push({ m: box(.78, .05, .54, MT.hull, 2.0 + dx, .5, z0), x0: 2.0 + dx, dx: Math.sign(dx) });
      for (const x of [3.0, .6, -1.0, -2.6]) { cylY(.1, .13, .1, MT.trim, x, .48, z0); box(.24, .16, .2, MT.hull, x, .58, z0); box(.2, .03, .21, MT.trim, x, .67, z0); cylX(.014, .014, .55, MT.dark, x + .3, .6, z0 + .04); cylX(.014, .014, .55, MT.dark, x + .3, .6, z0 - .04); } // lance turrets
      for (const x of [1.0, -1.8]) { const sg = new TH.Group(); sg.position.set(x, .44, z0); g.add(sg); add(mesh(new TH.SphereGeometry(.18, 18, 10, 0, TAU, 0, Math.PI / 2), MT.glow), 0, 0, 0, sg); torX(.22, .02, MT.trim, 0, .02, 0, sg).rotation.set(Math.PI / 2, 0, 0);
        for (let j = 0; j < 6; j++) { const pg = new TH.Group(); pg.rotation.y = j / 6 * TAU; sg.add(pg); box(.32, .02, .1, MT.hull, .26, .02, 0, pg); TI.petals.push(pg); } } // shield arrays
      for (const x of [-3.2, 3.6]) { cylY(.03, .04, .5, MT.trim, x, .62, z0); add(mesh(new TH.ConeGeometry(.04, .25, 6), MT.trim), x, 1.0, z0); } // pinnacle masts
      for (const yy of [.06, -.26]) for (const dz of [.3, -.3]) eng(-4.2, yy, z0 + dz, .17, .4); greeb(-3.2, 3, .42, z0 - .3, z0 + .3, 22, [MT.dark, MT.trim, MT.hull]); }
    for (const [x, len] of [[2.9, .4], [-1.6, 3.0]]) { box(len, .2, 2.3, MT.hull, x, .1, 0); box(len * .94, .04, 2.2, MT.trim, x, .21, 0); } // bridges between the hulls
    { const cx = -1.6; add(mesh(new TH.CylinderGeometry(1.0, 1.2, .34, 10), MT.hull), cx, .4, 0); torX(1.12, .04, MT.trim, cx, .52, 0).rotation.set(Math.PI / 2, 0, 0); add(mesh(new TH.CylinderGeometry(.62, .9, .32, 10), MT.hull), cx, .72, 0); torX(.66, .05, MT.trim, cx, .9, 0).rotation.set(Math.PI / 2, 0, 0); // the citadel
      for (let i = 0; i < 10; i++) box(.06, .1, .02, MT.win, cx + Math.cos(i / 10 * TAU) * .95, .45, Math.sin(i / 10 * TAU) * .95).rotation.y = -i / 10 * TAU;
      cylY(.07, .1, 2.1, MT.glow, cx, 1.95, 0, 8); add(mesh(new TH.ConeGeometry(.12, .5, 8), MT.glow), cx, 3.2, 0); // the blue crystal spire
      for (let q = 0; q < 8; q++) { const a = q / 8 * TAU, rr = .42, h = .7 + (q % 3) * .3; cylY(.05, .08, h, MT.hull, cx + Math.cos(a) * rr, .9 + h / 2, Math.sin(a) * rr, 6); add(mesh(new TH.ConeGeometry(.06, .36, 6), MT.trim), cx + Math.cos(a) * rr, .9 + h + .18, Math.sin(a) * rr); }
      const crest = new TH.Group(); crest.position.set(cx + 1.1, .55, 0); g.add(crest); box(.06, .9, .5, MT.trim, 0, 0, 0, crest); box(.07, .6, .26, MT.glow, .01, .02, 0, crest); add(ext([[0, .32], [.3, 0], [0, -.32]], .06, MT.trim, .01), .02, -.45, 0, crest).rotation.z = Math.PI / 2; } // the gold crest facing forward
    TI.mats = [MT.glow, MT.win]; }
'''

HAR = r'''  else { ud.engCol = [0xd6ffe8, 0x3dff9a]; TI.arms = []; TI.ringG = []; /* v564 rebuilt after the owner's painting */
    add(mesh(new TH.SphereGeometry(.62, 32, 20), MT.glow), 0, .5, 0); TI.core = g.children[g.children.length - 1]; // the emerald reactor, raised in its cage
    for (const [rx, ry] of [[Math.PI / 2, 0], [0, 0], [0, Math.PI / 2]]) { const c = add(mesh(new TH.TorusGeometry(.78, .05, 8, 48), MT.trim), 0, .5, 0); c.rotation.set(rx, ry, 0); } // its ring cage
    add(mesh(new TH.CylinderGeometry(1.3, 1.0, .4, 12), MT.hull), 0, -.3, 0); add(mesh(new TH.CylinderGeometry(.7, 1.15, .22, 12), MT.dark), 0, -.02, 0); for (let j = 0; j < 12; j++) { const a = j / 12 * TAU; const p = box(.36, .08, .2, MT.trim, Math.cos(a) * 1.18, -.08, Math.sin(a) * 1.18); p.rotation.y = -a; box(.12, .06, .04, j % 2 ? MT.win : MT.glow, Math.cos(a) * 1.31, -.3, Math.sin(a) * 1.31).rotation.y = -a; }
    cylY(.26, .42, .6, MT.dark, 0, 1.38, 0, 8); add(mesh(new TH.ConeGeometry(.26, 2.0, 8), MT.dark), 0, 2.65, 0); box(.03, 1.5, .03, MT.win, .17, 2.2, 0); // the cathedral spire
    for (let q = 0; q < 8; q++) { const a = q / 8 * TAU + .2, rr = .45 + (q % 2) * .15, h = .5 + (q % 3) * .35; add(mesh(new TH.ConeGeometry(.07, h, 6), MT.dark), Math.cos(a) * rr, 1.15 + h / 2, Math.sin(a) * rr); }
    { const t = add(mesh(new TH.ConeGeometry(.34, 2.6, 8), MT.dark), 0, -1.8, 0); t.rotation.x = Math.PI; cylY(.025, .025, 2.4, MT.glow, 0, -3.4, 0, 6); box(.03, 1.8, .03, MT.glow, .17, -1.4, 0); /* the tail spike and its green beam */
      for (let q = 0; q < 10; q++) { const a = q / 10 * TAU, rr = .5 + r() * .5, L = .4 + r() * .8; const sp = add(mesh(new TH.ConeGeometry(.05, L, 6), MT.dark), Math.cos(a) * rr, -.3 - L / 2, Math.sin(a) * rr); sp.rotation.x = Math.PI; } }
    const crescent = (w0, sweep, r0, r1) => { const L = [], R = [], N = 22; for (let i = 0; i <= N; i++) { const u = i / N, rr = r0 + (r1 - r0) * u, th = sweep * Math.pow(u, 1.4), x = rr * Math.cos(th), z = rr * Math.sin(th), nx = -Math.sin(th), nz = Math.cos(th), w = w0 * Math.sin(Math.PI * Math.min(1, .25 + u * .85)) * Math.pow(1 - u, .35) + .03; L.push([x + nx * w / 2, z + nz * w / 2]); R.unshift([x - nx * w / 2, z - nz * w / 2]); } return L.concat(R); };
    const ARMS = [[.78, -1.15, 1.1, 4.7, 1.55], [-.78, 1.15, 1.1, 4.7, 1.55], [Math.PI - .78, 1.15, 1.1, 4.5, 1.45], [Math.PI + .78, -1.15, 1.1, 4.5, 1.45], [0, .55, 1.0, 2.5, .45], [Math.PI, -.55, 1.0, 2.5, .45]]; // four scythes and two horns
    ARMS.forEach(([a, sw, r0, r1, w0], i) => { const ag = new TH.Group(); ag.rotation.y = -a; ag.rotation.z = i < 4 ? -.16 : .1; g.add(ag); const blade = new TH.Group(); ag.add(blade); const big = i < 4, th = big ? .5 : .2, y0 = big ? -.35 : .2;
      add(ext(crescent(w0, sw, r0, r1), th, MT.hull, .04), 0, y0, 0, blade); add(ext(crescent(w0 * .55, sw, r0 + .15, r1 - .25), th * .5, MT.dark, .02), 0, y0 + th, 0, blade); add(ext(crescent(w0 * .12, sw, r0 + .3, r1 - .6), .02, MT.glow, 0), 0, y0 + th * 1.5 + .03, 0, blade); // the scythe, its armoured ridge and its emerald seam
      if (big) { const inner = Math.sign(sw); for (let q = 0; q < 9; q++) { const u = .12 + q * .085, rr = r0 + (r1 - r0) * u, t2 = sw * Math.pow(u, 1.4), w = w0 * Math.sin(Math.PI * Math.min(1, .25 + u * .85)) * Math.pow(1 - u, .35) * .38, bx = rr * Math.cos(t2) - Math.sin(t2) * w * inner, bz = rr * Math.sin(t2) + Math.cos(t2) * w * inner;
          const bay = box(.34, th * .6, .06, MT.glow, bx, y0 + th * .5, bz, blade); bay.rotation.y = -t2; if (q % 2) box(.07, .05, .06, MT.win, rr * Math.cos(t2) + Math.sin(t2) * w * inner * 1.2, y0 + th + .02, rr * Math.sin(t2) - Math.cos(t2) * w * inner * 1.2, blade); } /* green hangar bays and violet lights */
        for (let q = 0; q < 4; q++) { const u = .3 + q * .15, rr = r0 + (r1 - r0) * u, t2 = sw * Math.pow(u, 1.4); const sp = add(mesh(new TH.ConeGeometry(.05, .4, 5), MT.dark), rr * Math.cos(t2), y0 - .2, rr * Math.sin(t2), blade); sp.rotation.x = Math.PI; } }
      const tt = sw, tr = r1; TI.arms.push({ g: ag, blade, a: -a, tip: [tr * Math.cos(tt), y0, tr * Math.sin(tt)] }); });
    for (let j = 0; j < 6; j++) { const a = j / 6 * TAU + .5; ud.eng.push([Math.cos(a) * 1.3, -.25, Math.sin(a) * 1.3, .12]); }
    for (const [R, tilt, n] of [[1.75, .3, 12], [2.15, -.24, 16]]) { const rg = new TH.Group(); rg.rotation.x = tilt; g.add(rg); const t0 = add(mesh(new TH.TorusGeometry(R, .045, 10, 80), MT.trim), 0, 0, 0, rg); t0.rotation.x = Math.PI / 2; for (let j = 0; j < n; j++) { const a = j / n * TAU; add(mesh(new TH.SphereGeometry(.05, 8, 6), j % 3 ? MT.glow : MT.win), Math.cos(a) * R, 0, Math.sin(a) * R, rg); } TI.ringG.push(rg); }
    TI.mats = [MT.glow, MT.win]; }
'''
s = s.replace('color: 0x0b0c0e, roughness: .4, metalness: .55, clearcoat: .15, envMapIntensity: .8 }', 'color: 0x060607, roughness: .6, metalness: .45, clearcoat: .1, envMapIntensity: .3 }', 1)
i, j = cut('  if (k === "armageddon") { ud.engCol = [0xffe0b0, 0xff4a1a];', '  else if (k === "sovereign") {'); s = s[:i] + ARM + s[j:]
i, j = cut('  else if (k === "sovereign") { ud.engCol = [0xffffff, 0x5fb8ff];', '  else { ud.engCol = [0xd6ffe8, 0x3dff9a];'); s = s[:i] + SOV + s[j:]
i, j = cut('  else { ud.engCol = [0xd6ffe8, 0x3dff9a]; TI.arms = []; TI.ringG = [];', '  g.userData.titan = k; return g; }'); s = s[:i] + HAR + s[j:]
s2 = re.sub(r"GAME_V = 563\b", "GAME_V = 564", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
