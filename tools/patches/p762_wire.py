"""v762: World Bosses rebuilt to their paintings, hard-surface first (owner: "build them them all just as you described"). Adds the
hard-surface kit (tools/patches/p762_hs.js: crisp swept plates, grooves with glowing inlays, faceted crystals, crescent blades, runes)
and remodels the Void Warden to its painting (docs/art/boss/warden-skin.webp): the measured layout (core, upright ring, rune band,
lower ring, the wide outer ring, two tall crescent blades, the front crystal pylon and its pendant, the crown spire), rings that
spin about their own axes. BOSS3D's bake now carries vertex colours. Applies on top of v761."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 761;", "const GAME_V = 762;")
kit = open("tools/patches/p762_hs.js", encoding="utf-8").read()
rep("  function warden() {", kit + "  function warden() {")
# bake keeps vertex colours
rep("""        const P = new Float32Array(n * 3), N = new Float32Array(n * 3), U = new Float32Array(n * 2); let q = 0;
        for (const g of parts) { P.set(g.attributes.position.array, q * 3); N.set(g.attributes.normal.array, q * 3); U.set(g.attributes.uv.array, q * 2); q += g.attributes.position.count; g.dispose(); }
        const g2 = new TH.BufferGeometry(); g2.setAttribute("position", new TH.BufferAttribute(P, 3)); g2.setAttribute("normal", new TH.BufferAttribute(N, 3)); g2.setAttribute("uv", new TH.BufferAttribute(U, 2)); g2.computeBoundingSphere();""",
"""        const P = new Float32Array(n * 3), N = new Float32Array(n * 3), U = new Float32Array(n * 2), hc = parts.every(g => g.attributes.color), C = hc ? new Float32Array(n * 3) : null; let q = 0;
        for (const g of parts) { P.set(g.attributes.position.array, q * 3); N.set(g.attributes.normal.array, q * 3); U.set(g.attributes.uv.array, q * 2); if (C) C.set(g.attributes.color.array, q * 3); q += g.attributes.position.count; g.dispose(); }
        const g2 = new TH.BufferGeometry(); g2.setAttribute("position", new TH.BufferAttribute(P, 3)); g2.setAttribute("normal", new TH.BufferAttribute(N, 3)); g2.setAttribute("uv", new TH.BufferAttribute(U, 2)); if (C) g2.setAttribute("color", new TH.BufferAttribute(C, 3)); g2.computeBoundingSphere();""")
# the Warden's body, remodelled to the painting
i = s.index("  function warden() {"); a = s.index("    const gyro = [];", i); b = s.index("    // ring-satellites", i)
s = s[:a] + """    /* v760 remodelled to its painting, measured from it (painting px -> units: the core's 95 px radius is 2.0): an upright ring
       round the core, the rune band above it, a lower ring, the wide outer ring, two tall crescent blades whose tips curl toward you,
       the long crystal pylon in front with its pendant below and a crown spire above. Machined plates, glowing channels. */
    const gyro = [], MH = hsMat(0x080514, { hi: 0x5a3440, env: .22, rough: .42, metal: .55 }), GL = hsGlow(0xa448ff, 1.5);
    const ring = (R, w, h, rot, pos, o = {}) => { const g = new TH.Group(), sp = new TH.Group(); g.add(sp); sp.add(hsRing(R, w, h, MH, GL, o)); g.rotation.set(rot[0], rot[1], rot[2]); g.position.set(...pos); g.userData.spin = sp; grp.add(g); gyro.push(g); return g; };
    const glyph = ring(4.95, .34, .84, [-.12, 0, .02], [-.2, 1.84, 0], { n: 18, groove: 0 }); glyph.userData.spin.add(hsRunes("ward", 4.95 + .18, .42, 30));
    ring(4.37, .62, .5, [Math.PI / 2, 0, -.65], [0, .05, 0], { n: 16 }); ring(5.26, .42, .5, [.21, 0, -.03], [-.1, -1.6, 0], { n: 20 }); ring(10.1, .38, .44, [.157, 0, -.05], [-.3, -.9, 0], { n: 34 });
    // two tall crescent blades, left and right: thick plated arcs (outer radius 5.6 about a centre beside the core), tips curling forward
    const crs = []; for (const side of [-1, 1]) { const g = new TH.Group(), cx = side * 1.75, cy = -.29, R = 6.2, a0 = side < 0 ? 1.79 : Math.PI - 1.79, a1 = side < 0 ? 4.63 : Math.PI - 4.63, zf = u => 1.7 * Math.pow(Math.abs(u - .5) * 2, 2.2);
      g.add(hsCrescent(cx, cy, R, a0, a1, 1.55, 1.0, MH, GL, { plates: 8, zf }));
      for (const [u, L, r, out] of [[.16, .9, .2, 1], [.5, 1.1, .24, 1], [.84, .9, .2, 1], [.95, 1.7, .26, .4]]) { const a = a0 + (a1 - a0) * u, nx = Math.cos(a), ny = Math.sin(a), sp = hsSpike(L, r, MH); sp.position.set(cx + nx * (R - .15), cy + ny * (R - .15), zf(u));
        const d = new TH.Vector3(nx * out, ny * out - (1 - out), 0).normalize(); sp.quaternion.setFromUnitVectors(new TH.Vector3(0, 1, 0), d); g.add(sp); }
      grp.add(g); crs.push({ g, side }); }
    // the front pylon: a long crystal in a frame of two blades, its pendant hanging below; the crown spire on top
    const pyl = []; { const g = new TH.Group(); g.add(hsCrystal([[0, -2.3], [.42, -1.5], [.58, 0], [.42, 1.5], [0, 2.3]], 4)); for (const s2 of [-1, 1]) { const bl = new TH.Mesh(hsSweep([[0, 0], [-.3, .16], [-.55, 0], [-.3, -.16]], hsLine(new TH.Vector3(s2 * .62, -2.0, 0), new TH.Vector3(s2 * .62, 2.0, 0), 8), { base: MH.userData.hsBase, sc: u => [.4 + .6 * Math.sin(Math.PI * u), 1], hi: [1, 0, 1, 0] }), MH); bl.scale.x = -s2; g.add(bl); }
      g.add(hsRing(.75, .16, .22, MH, GL, { n: 6, caps: false, groove: 0 }));
      const pd = new TH.Group(); pd.position.set(.2, -3.7, -1.2); pd.add(hsCrystal([[0, -1.6], [.3, -.5], [.38, 0], [.3, .5], [0, .9]], 6)); pd.add(hsRing(.55, .2, .26, MH, GL, { n: 6, caps: false }));
      { const sp = hsSpike(1.1, .16, MH); sp.position.y = -1.5; sp.rotation.x = Math.PI; pd.add(sp); } g.add(pd);
      g.position.set(.1, -2.8, 2.6); grp.add(g); pyl.push({ g, s: -1, y0: -2.8 }); }
    { const g = new TH.Group(); g.add(hsCrystal([[0, -.5], [.3, 0], [.26, .7], [0, 1.4]], 6)); g.add(hsRing(.42, .14, .2, MH, GL, { n: 6, caps: false, groove: 0 })); g.position.set(0, 4.6, 0); grp.add(g); pyl.push({ g, s: 1, y0: 4.6 }); }
    { const c = hsCrystal([[0, 0], [.22, .5], [.18, 1.5], [0, 2.2]], 4); c.position.set(Math.sin(.21) * 5.1, .4, Math.cos(.21) * 5.1); glyph.userData.spin.add(c); }
""" + s[b:]
rep("""      const spd = [.00016, -.0004, .00025, -.0002]; gyro.forEach((g, i) => { ga[i] += spd[i] * 16 * (1 + clench * 4 + lock * 2 + pull * 6 + ov * ov * 40); g.rotation.set(gy0[i].x * (1 - lock), ga[i] * (1 - lock) + (i % 2 ? Math.PI / 2 : 0) * lock, gy0[i].z * (1 - lock)); });""",
    """      const spd = [.00016, -.0004, .00025, -.0002]; gyro.forEach((g, i) => { ga[i] += spd[i] * 16 * (1 + clench * 4 + lock * 2 + pull * 6 + ov * ov * 40); g.rotation.set(gy0[i].x * (1 - lock), gy0[i].y * (1 - lock) + (i % 2 ? Math.PI / 2 : 0) * lock, gy0[i].z * (1 - lock)); g.userData.spin.rotation.y = ga[i]; });""")
rep("""      for (const p of pyl) { p.g.position.y = p.s * (4.4 + Math.sin(t * .0013) * .25 + lock * 1.2 + wide * .8); p.g.rotation.y = t * .0006 * p.s; }""",
    """      for (const p of pyl) { p.g.position.y = p.y0 + p.s * (Math.sin(t * .0013) * .25 + lock * 1.2 + wide * .8); p.g.rotation.y = Math.sin(t * .0006) * .3 * p.s; }""")
rep("""    const wk = [1, 2, 3].map((gi, i) => { const g = new TH.Group(), R = [2.9, 5.0, 5.8][i],""", """    const wk = [1, 2, 3].map((gi, i) => { const g = new TH.Group(), R = [4.37, 5.26, 10.1][i],""")
rep("halo.material.opacity = Math.min(1, .7 + Math.sin(t * .003) * .2", "halo.material.opacity = Math.min(1, .42 + Math.sin(t * .003) * .12")  # the painting's void is dark, ringed, not a white flare
rep("lens.material.opacity = Math.min(1, .75 + Math.sin(t * .004) * .12", "lens.material.opacity = Math.min(1, .5 + Math.sin(t * .004) * .1")
rep("adM.uniforms.uI.value = (1 + pull * 1.2", "adM.uniforms.uI.value = (.5 + pull * 1.2")  # less haze over the rings
open(p, "w", encoding="utf-8").write(s)
print("ok")
