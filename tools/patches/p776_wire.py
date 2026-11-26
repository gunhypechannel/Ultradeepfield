"""v776: Medusara toward her painting (owner: "update Medusara, we need to do better at that one"). Built on her old (v761) model,
which the owner prefers to v769's. The painted face skin stays. Her serpents are thick dark bronze-and-gold, rise from behind her
crown and coil out round her upper half with jaws open, red mouths and red eyes (they were thin, pale pink, fanned evenly all round
her like spider legs). Tall gold crown spikes stand above her brow again (the skin had hidden them). The flat white glyph rings are
gone: the gold rail rings return with gothic ruin arches standing on the main ring and broken stone drifting along it, as painted.
Violet storm clouds boil round her lower half with a bright glow beneath. The battle camera comes in so her face fills the view.
Applies on top of v775."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 775;", "const GAME_V = 776;")
# serpents: rooted behind the crown, coiling round her upper half; thicker, longer, bigger heads
rep("const NSN = 9, snakes = []; for (let i = 0; i < NSN; i++) { const a = -2.75 + i / (NSN - 1) * 5.5, root = V(Math.sin(a) * 9.5, 14 + Math.cos(a) * 10.5, -5.5),",
    "const NSN = 9, snakes = []; for (let i = 0; i < NSN; i++) { const a = [-2.2, -1.65, -1.1, -.55, -.05, .5, 1.05, 1.6, 2.15][i], root = V(Math.sin(a) * 8.6, 14 + Math.cos(a) * 9.4, -6.5),")
rep("const L = 17 + (i % 3) * 3.5", "const L = 16 + (i % 3) * 3.5")
rep("r = 2.4 * (1 - u * .52) * (1 + .06 * Math.sin(u * 40))", "r = 2.6 * (1 - u * .5) * (1 + .05 * Math.sin(u * 40))")
rep("hd = put(g, new TH.Group(), tip.toArray(), null, 3.0)", "hd = put(g, new TH.Group(), tip.toArray(), null, 3.1)")
rep("const MSk = new TH.MeshStandardMaterial({ color: 0xb4b0bc, metalness: .7, roughness: .32, envMapIntensity: .6, map: medScale(0), emissiveMap: medScale(1), emissive: 0xffa83a, emissiveIntensity: .9 })",
    "const MSk = new TH.MeshStandardMaterial({ color: 0x4a3a28, metalness: .7, roughness: .32, envMapIntensity: .55, map: medScale(0), emissiveMap: medScale(1), emissive: 0xffa83a, emissiveIntensity: .16 })")
rep("MOU = new TH.MeshStandardMaterial({ color: 0x160205, roughness: .8, metalness: 0, envMapIntensity: .08 })", "MOU = new TH.MeshStandardMaterial({ color: 0x220103, emissive: 0x9a0a0a, emissiveIntensity: .08, roughness: .6, metalness: 0, envMapIntensity: .08 })")
rep("SEYE = new TH.MeshBasicMaterial({ color: 0xffa020, toneMapped: false })", "SEYE = new TH.MeshBasicMaterial({ color: 0xff2a14, toneMapped: false })")
rep('"rgba(255,150,40,1)", "med_se2"', '"rgba(255,50,30,1)", "med_se3"')
rep("Sn.jaw.rotation.x = .14 + ", "Sn.jaw.rotation.x = .2 + ")
rep("w = Math.sin(u * Math.PI * 2 + i * 1.3) * 3.2 * (1 - u * .35)", "w = Math.sin(u * Math.PI * (1.6 + (i % 3) * .35) + i * 1.3) * 5.2 * (1 - u * .3)")
# the crown: taller spikes gathered over the brow, kept when the painted skin loads
rep("const u = (k - 4) * .2,", "const u = (k - 4) * .11,")
rep("new TH.ConeGeometry(.5, 3.2 - Math.abs(k - 4) * .45, 4), MG)", "new TH.ConeGeometry(.75, 6 - Math.abs(k - 4) * 1.05, 4), MG)")
rep("(c.material === MG || (c.material.color", "((c.material === MG && !(c.geometry && c.geometry.type === \"ConeGeometry\")) || (c.material.color")
# the rings: gold rails with gothic ruins and drifting stone (in place of v493's glyph rings), and the storm clouds below her
a = s.index("    { // v493 glyph rings in place"); b = s.index("G2.material.opacity = .5 * aw * live * (1 + rg); }; }\n", a) + len("G2.material.opacity = .5 * aw * live * (1 + rg); }; }\n")
s = s[:a] + r'''    { /* v776 as painted: gold rails, gothic ruins standing on the main ring, broken stone drifting along it; storm clouds round her lower half */
      rr2.visible = false; const MR = MSd, LOq = LO ? .5 : 1;
      towers.forEach((w, i) => { const t = w.t; t.clear(); t.scale.setScalar(.65); const hgt = 1 + (i % 3) * .25;
        put(t, new TH.Mesh(new TH.DodecahedronGeometry(2.6, 0), MR), [0, -1.2, 0], [i, i * 2, 0], [1.2, .7, 1]);
        for (const sx of [-1, 1]) { put(t, new TH.Mesh(new TH.BoxGeometry(.9, 7 * hgt, .9), MR), [sx * 1.7, 3 * hgt, 0]); put(t, new TH.Mesh(new TH.ConeGeometry(.55, 2.4, 4), MR), [sx * 1.7, 6.5 * hgt + 1.2, 0], [0, Math.PI / 4, 0]);
          }
        put(t, new TH.Mesh(new TH.TorusGeometry(1.7, .32, 4, 12, Math.PI), MR), [0, 6.5 * hgt, 0]);
        put(t, new TH.Mesh(new TH.BoxGeometry(4.2, .5, 1.1), MR), [0, 6.5 * hgt - 1.2, 0]); if (i % 2) put(t, new TH.Mesh(new TH.BoxGeometry(.9, 4.5, .9), MR), [3.4, 1.6, -.6], [0, 0, -.35]);
        w.w.position.set(0, 3.6 * hgt, .7); w.w.scale.setScalar(3); t.add(w.w); });
      const DB = new TH.DodecahedronGeometry(1, 0); for (let i = 0; i < 40 * LOq; i++) { const a = rnd() * TAU, r = ringR + (rnd() - .5) * 6, d = put(RR, new TH.Mesh(DB, MR), [Math.sin(a) * r, (rnd() - .5) * 5, Math.cos(a) * r], [rnd() * 3, rnd() * 3, rnd() * 3], .3 + rnd() * rnd() * 1.4); d.userData.dyn = 1; }
      const clT = paint("med_cloud", 128, (x, N) => { x.clearRect(0, 0, N, N); for (let k = 0; k < 22; k++) { const px = N / 2 + (rnd() - .5) * N * .5, py = N / 2 + (rnd() - .5) * N * .36, r = N * (.12 + rnd() * .16), g = x.createRadialGradient(px, py, 0, px, py, r); g.addColorStop(0, "rgba(255,255,255,.55)"); g.addColorStop(.6, "rgba(255,255,255,.22)"); g.addColorStop(1, "rgba(255,255,255,0)"); x.fillStyle = g; x.beginPath(); x.arc(px, py, r, 0, TAU); x.fill(); } });
      const clouds = put(body, new TH.Group(), [0, 14, 0], null, 1.25); head.scale.setScalar(1.25); /* her face is the planet: the head fills the frame as painted */ const _c0 = 0, CL = [], cA = new TH.Color(0x8040e0), cB = new TH.Color(0x2e0c70);
      for (let i = 0; i < 26 * LOq; i++) { const th = rnd() * TAU, el = -.55 - rnd() * .75, r = 11.5 + rnd() * 2.5, m = new TH.SpriteMaterial({ map: clT, color: cB.clone().lerp(cA, rnd()), transparent: true, opacity: .8, depthWrite: false }), sp = new TH.Sprite(m);
        sp.position.set(Math.sin(th) * Math.cos(el) * r, Math.sin(el) * r, Math.cos(th) * Math.cos(el) * r); const z = 8 + rnd() * 9; sp.scale.set(z * 1.4, z, 1); sp.material.rotation = rnd() * TAU; clouds.add(sp); CL.push({ sp, o: .55 + rnd() * .35, ph: rnd() * 6 }); }
      const under = sprite(20, "rgba(170,90,255,1)", "med_under2"); under.position.set(0, -12, 2); under.material.opacity = .4; clouds.add(under);
      const tick1 = out.tick; out.tick = t => { tick1(t); const T = t * .001, fd = f("die", t), die = fd < 0 ? 0 : fd, aw = drv.awake != null ? drv.awake : 1, live = 1 - ss(.15, .5, die), fs = f("storm", t), st = 1 + bell(fs, 0, .2, .7, 1) * .6;
        clouds.rotation.y = T * .03; CL.forEach(c => { c.sp.material.opacity = c.o * aw * live * (.85 + .15 * Math.sin(T * .6 + c.ph)) * Math.min(1.2, st); }); under.material.opacity = (.3 + .1 * Math.sin(T * 1.3)) * aw * live * st; }; }
''' + s[b:]
rep("out0.MF.emissiveIntensity = .34 * (.4 + .6 * aw)", "out0.MF.emissiveIntensity = .2 * (.4 + .6 * aw)") # darker stone, as painted
rep("medusara: [0, [-20, 22, 104], [0, 16, 0]]", "medusara: [0, [-14, 18, 92], [0, 15, 0]]")
open(p, "w", encoding="utf-8").write(s)
print("ok")
