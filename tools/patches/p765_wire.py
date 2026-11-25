"""v765: the Abyssal Kraken rebuilt to its painting (docs/art/boss/kraken-skin.webp; owner: "build them them all just as you described").
The Kraken was the Devourer's worm hull in purple; the painting is a true kraken: a great armoured mantle (dark violet plates, a
crested dorsal ridge, brow horns over two burning eyes) and eight thick curling tentacles with glowing sucker rings down their
undersides. devourer("krk") now builds that body: a lathed mantle swept back and up behind the face, a ridge of crisp spines, brow
horns, light seams round the mantle, eyes as lit almonds; the eight tentacles grow from a ring under the head, thicker and more
tightly curled, each segment carrying a sucker; the beak's claws are smaller. Moves, beam and storm are the Devourer's own.
Applies on top of v764."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 764;", "const GAME_V = 765;")
i = s.index("  function devourer(o) {"); e = s.index("\n  /* ---------- helpers for the Wednesday bosses", i); o = s[i:e]
def r(a, b, n=1):
    global o
    c = o.count(a); assert c == n, (c, a[:120]); o = o.replace(a, b)
# the worm hull, its scales, blades, spines and tail are the Devourer's only
r("""    { const pr = []; for (let x = -11.5; x <= 3.5; x += .25)""", """    if (!KR) { const pr = []; for (let x = -11.5; x <= 3.5; x += .25)""")
r("""    for (let x = 2.5, row = 0; x > -10.5; x -= .62, row++) { const R = rad(x),""", """    if (!KR) for (let x = 2.5, row = 0; x > -10.5; x -= .62, row++) { const R = rad(x),""")
r("""    for (let i = 0; i < 34; i++) { const x = 2.4 - i * .34,""", """    if (!KR) for (let i = 0; i < 34; i++) { const x = 2.4 - i * .34,""")
r("""    for (let i = 0; i < 14; i++) { const x = 2.0 - i * .72, sp = shard(""", """    if (!KR) for (let i = 0; i < 14; i++) { const x = 2.0 - i * .72, sp = shard(""")
r("""    { const t1 = horn(3.4, .3, .32, MB); t1.rotation.z = Math.PI;""", """    if (!KR) { const t1 = horn(3.4, .3, .32, MB); t1.rotation.z = Math.PI;""")
# the Kraken's mantle, ridge, horns and eyes
r("""    // the maw: armoured collar,""", """    if (KR) { /* v765 the mantle: swept back and up behind the face, armoured, crested, seamed with light */
      const man = new TH.Group(); man.position.set(-.4, 1.6, 0); man.rotation.z = -1.12; man.scale.setScalar(1.25); body.add(man);
      const pr = [[0, 3.3], [1.7, 3.05], [2.7, 2.2], [3.25, .7], [3.45, -1.2], [3.15, -3.4], [2.45, -5.3], [1.35, -6.8], [.35, -7.6], [0, -7.8]].map(([r0, x]) => new TH.Vector2(r0, x));
      const ml = new TH.Mesh(new TH.LatheGeometry(new TH.SplineCurve(pr).getPoints(40).reverse(), 40), M); ml.rotation.z = -Math.PI / 2; man.add(ml);
      for (const [x, R] of [[1.4, 3.05], [-.8, 3.42], [-3.0, 3.2], [-5.0, 2.55]]) { const g = new TH.Mesh(new TH.TorusGeometry(R * 1.005, .045, 6, 48), glowMat(VIO, .6)); g.rotation.y = Math.PI / 2; g.position.x = x; man.add(g); }
      const rad0 = x => { const q = pr.map(v => [v.y, v.x]); for (let k = 0; k < q.length - 1; k++) if (x <= q[k][0] && x >= q[k + 1][0]) { const f = (q[k][0] - x) / (q[k][0] - q[k + 1][0]); return q[k][1] + (q[k + 1][1] - q[k][1]) * f; } return 0; };
      for (let k = 0; k < 13; k++) { const x = 2.4 - k * .75, R = rad0(x), sp = hsSpike(.7 + Math.sin(k / 12 * Math.PI) * 1.1, .22, hsMat(0x14081f, { hi: 0x5a2c70, metal: .5 })); sp.position.set(x, R - .1, 0); sp.rotation.z = .55; man.add(sp); } // the dorsal crest
      for (const sz of [-1, 1]) for (let k = 0; k < 4; k++) { const sp = hsSpike(1.4 - k * .22, .2, hsMat(0x14081f, { hi: 0x5a2c70, metal: .5 })); sp.position.set(2.2 - k * .5, 2.2 - k * .15, sz * (1.5 + k * .25)); sp.rotation.set(sz * (.7 + k * .1), 0, .4 + k * .2); man.add(sp); } // brow horns
      for (const sz of [-1, 1]) { const ey = new TH.Mesh(new TH.SphereGeometry(.42, 20, 12), glowMat(0xe8a8ff)); ey.scale.set(.6, .55, 1.25); ey.position.set(4.05, 3.65, sz * 1.15); ey.rotation.x = sz * .35; body.add(ey);
        const lid = hsFlat(new TH.ConeGeometry(.6, 1.6, 4), hsMat(0x14081f, { hi: 0x5a2c70, metal: .5 })); lid.position.set(3.95, 4.15, sz * 1.15); lid.rotation.set(Math.PI / 2, 0, sz > 0 ? .3 : -.3); lid.scale.set(1, 1, .35); body.add(lid); } }
    // the maw: armoured collar,""")
r("""      const c = horn(4.6 + (k % 2) * .9, 1.9, .5, MB); hg.add(c);""", """      const c = horn((4.6 + (k % 2) * .9) * (KR ? .55 : 1), 1.9 * (KR ? .55 : 1), .5 * (KR ? .7 : 1), MB); hg.add(c);""")
# tentacles: thicker, curled, sucker rings along their insides
r("""        const rg = new TH.Mesh(new TH.TorusGeometry(r * .86, Math.max(.02, r * .06), 6, 18), glowMat(VIO, .55)); rg.rotation.x = Math.PI / 2; rg.position.y = L * .97; j.add(rg);""",
  """        const rg = new TH.Mesh(new TH.TorusGeometry(r * .86, Math.max(.02, r * .06), 6, 18), glowMat(VIO, .55)); rg.rotation.x = Math.PI / 2; rg.position.y = L * .97; j.add(rg);
        if (KR && i < n - 1) { const sk = new TH.Group(), sd = -Math.sign(curl || 1); sk.position.set(sd * r * .93, L * .5, 0); sk.rotation.z = sd * Math.PI / 2; const ring = new TH.Mesh(new TH.TorusGeometry(r * .34, r * .09, 6, 16), glowMat(0xd070ff, .95)); ring.rotation.x = Math.PI / 2; sk.add(ring); const cup = new TH.Mesh(new TH.CircleGeometry(r * .26, 14), glowMat(0x7a20c8, .9)); cup.rotation.x = -Math.PI / 2; cup.position.y = .01; sk.add(cup); j.add(sk); } /* v765 suckers */""")
r("""    else for (let k = 0; k < 8; k++) { const a = k * TAU / 8 + .3, x0 = 1.6 - (k % 4) * 1.9; tent(12 + rnd() * 6, 15, .85 + rnd() * .2, x0, V(-1.1, Math.cos(a) - .35, Math.sin(a)), (rnd() < .5 ? 1 : -1) * (.1 + rnd() * .09), false); }
    if (!LOD) for""", """    else for (let k = 0; k < 8; k++) { const a = k * TAU / 8 + .3, x0 = KR ? 1.3 : 1.6 - (k % 4) * 1.9; tent(KR ? 14 + rnd() * 5 : 12 + rnd() * 6, 15, KR ? 1.15 + rnd() * .2 : .85 + rnd() * .2, x0, KR ? V(-.25, Math.cos(a) * 1.1 - .7, Math.sin(a) * 1.3) : V(-1.1, Math.cos(a) - .35, Math.sin(a)), (rnd() < .5 ? 1 : -1) * (KR ? .17 + rnd() * .08 : .1 + rnd() * .09), false); }
    if (!LOD && !KR) for""")
r("""      for (let k = 0; k < 8; k++) { const a = k * TAU / 8 + .3; tube(1.6 - (k % 4) * 1.9, V(-1.1, Math.cos(a) - .35, Math.sin(a)), 13 + rnd() * 5, .9, k); }
      for (let k = 0; k < 6; k++) {""", """      for (let k = 0; k < 8; k++) { const a = k * TAU / 8 + .3; tube(KR ? 1.3 : 1.6 - (k % 4) * 1.9, KR ? V(-.25, Math.cos(a) * 1.1 - .7, Math.sin(a) * 1.3) : V(-1.1, Math.cos(a) - .35, Math.sin(a)), 13 + rnd() * 5, KR ? 1.15 : .9, k); }
      if (!KR) for (let k = 0; k < 6; k++) {""")
r("""    const TM = hullMat("tent", { rows: 3, cols: 4, bronze: .1, slits: .22, rep: [1, 1], ei: 2.4, base: "#34323c", rim: .6 });""", """    const TM = KR ? hullMat("krkt", { rows: 3, cols: 4, slits: .12, rep: [1, 1], ei: 1.6, rim: .5, ...KP, base: "#160a22" }) : hullMat("tent", { rows: 3, cols: 4, bronze: .1, slits: .22, rep: [1, 1], ei: 2.4, base: "#34323c", rim: .6 });""")
r("""const rg = new TH.Mesh(new TH.TorusGeometry(r * .86, Math.max(.02, r * .06), 6, 18), glowMat(VIO, .55));""", """const rg = new TH.Mesh(new TH.TorusGeometry(r * .86, Math.max(.02, r * .06), 6, 18), glowMat(VIO, KR ? .22 : .55));""")
r("""    if (LOD) { const TL = hullMat("tent", { rows: 3, cols: 4, bronze: .1, slits: .22, rep: [1, 1], ei: 2.4, base: "#34323c", rim: .6 });""", """    if (LOD) { const TL = KR ? hullMat("krkt", { rows: 3, cols: 4, slits: .12, rep: [1, 1], ei: 1.6, rim: .5, ...KP, base: "#160a22" }) : hullMat("tent", { rows: 3, cols: 4, bronze: .1, slits: .22, rep: [1, 1], ei: 2.4, base: "#34323c", rim: .6 });""")
r("""M = KR ? hullMat("krk", { rows: 12, slits: .6, rep: [12, 3], ...KP })""", """M = KR ? hullMat("krk", { rows: 12, slits: .6, rep: [12, 3], ...KP, base: "#140920" })""")
r("""    { const col = band(2.85, .5, .7, M, 0, TAU, 96, 18); col.rotation.z = Math.PI / 2; maw.add(col);""", """    if (!KR) { const col = band(2.85, .5, .7, M, 0, TAU, 96, 18); col.rotation.z = Math.PI / 2; maw.add(col);""")
r("""    for (let k = 0; k < 18; k++) { const a = k * TAU / 18, s = shard(.14, .7, MB);""", """    if (!KR) for (let k = 0; k < 18; k++) { const a = k * TAU / 18, s = shard(.14, .7, MB);""")
r("""maw.add(vort2);""", """maw.add(vort2); if (KR) { vort.scale.setScalar(.5); vort.userData.k = .5; } /* v765 the Kraken's beak is small under its eyes */""")
r("const vs = (1 + ov * .5) * (1 - implo * .97);", "const vs = (1 + ov * .5) * (1 - implo * .97) * (KR ? .5 : 1);")
r("glow.scale.setScalar(9 * (", "glow.scale.setScalar((KR ? 4.5 : 9) * (")
r("hot.scale.setScalar(4.2 * (", "hot.scale.setScalar((KR ? 2.2 : 4.2) * (")
r(""": hullMat("dev", { rows: 12, bronze: .12, slits: .55, rep: [12, 3] })""", """: hullMat("dev", { rows: 12, slits: .55, rep: [12, 3], ...KP, base: "#120a1c" })""")
o = o.replace(""": hullMat("devs", { rows: 2, cols: 2, bronze: .15, slits: .45, rep: [1, 1] })""", """: hullMat("devs", { rows: 2, cols: 2, slits: .45, rep: [1, 1], ...KP, base: "#1a0e28" })""")
o = o.replace(""": hullMat("devb", { rows: 4, bronze: .35, slits: .15, rep: [1, 1] })""", """: hullMat("devb", { rows: 4, slits: .15, rep: [1, 1], ...KP, base: "#140a20" })""")
r(""": hullMat("tent", { rows: 3, cols: 4, bronze: .1, slits: .22, rep: [1, 1], ei: 2.4, base: "#34323c", rim: .6 });
    const tents""", """: hullMat("tent", { rows: 3, cols: 4, slits: .22, rep: [1, 1], ei: 2.4, rim: .6, ...KP, base: "#1a1026" });
    const tents""")
s = s[:i] + o + s[e:]
open(p, "w", encoding="utf-8").write(s)
print("ok")
