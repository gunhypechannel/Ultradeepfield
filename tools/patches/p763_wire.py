"""v763: the Energy Conduit remodelled to its painting (docs/art/boss/conduit-skin.webp; owner: "build them them all just as you
described"). Measured from the painting (1024 px wide; ground at 880 px, the crown crystal's tip at 10 px = 12.1 units): the stepped
plinth rises to 3.3, the three rings sit at 5.0 / 7.2 / 9.6 (radii 3.9 / 4.6 / 4.0, the top one split into two horned arcs), a slim
crystal shaft opens into the great crown crystal (widest at 10.6), shard collars of tall blades at 3.2 / 5.0 / 8.1. Hard-surface kit
parts: crisp flat-shaded plinth tiers, chamfered buttress legs, machined rings with glowing inlays, bronze-edged dark steel.
Kit additions: hsFlat (any geometry flat-shaded and vertex-coloured), hsRing arcs (a0, al), hsBeam (a chamfered tapered beam).
Applies on top of v762."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 762;", "const GAME_V = 763;")
# kit additions
rep("""  function hsSpike(len, r, M, sides = 4) {""", """  // any geometry, flat-shaded, coloured: steep faces in the base colour, sloped ones lighter (the light catches bevels)
  function hsFlat(geo, M, k = .45) { const g = geo.index ? geo.toNonIndexed() : geo; g.computeVertexNormals(); const b = new TH.Color(M.userData.hsBase ?? 0x0b0812), h = new TH.Color(M.userData.hsHi ?? 0x3e2c3a), N = g.attributes.normal, a = [];
    for (let i = 0; i < N.count; i++) { const y = Math.abs(N.getY(i)), c = b.clone().lerp(h, y > .15 && y < .9 ? k : 0); a.push(c.r, c.g, c.b); } g.setAttribute("color", new TH.Float32BufferAttribute(a, 3)); return new TH.Mesh(g, M); }
  // a straight chamfered beam from a to b, w x h at a tapering by k at b
  function hsBeam(a, b, w, h, M, k = .7, up) { const [pr, hi] = hsProf(w, h, .22); return new TH.Mesh(hsSweep(pr, hsLine(a, b, 1, up || new TH.Vector3(0, 1, 0).cross(b.clone().sub(a)).lengthSq() < 1e-6 ? new TH.Vector3(1, 0, 0) : new TH.Vector3(0, 1, 0)), { hi, base: M.userData.hsBase, hiC: M.userData.hsHi, sc: u => 1 - (1 - k) * u }), M); }
  function hsSpike(len, r, M, sides = 4) {""")
rep("""  function hsRing(R, w, h, M, G, opt = {}) { const g = new TH.Group(), n = opt.n || Math.max(8, Math.round(R * 2.2)), gap = opt.gap ?? Math.min(.06, .22 / R), each = TAU / n,""",
    """  function hsRing(R, w, h, M, G, opt = {}) { const g = new TH.Group(), A0 = opt.a0 || 0, AL = opt.al || TAU, n = opt.n || Math.max(8, Math.round(R * 2.2 * AL / TAU)), gap = opt.gap ?? Math.min(.06, .22 / R), each = AL / n,""")
rep("""    for (let i = 0; i < n; i++) { const a0 = i * each + gap / 2, a1 = (i + 1) * each - gap / 2; g.add(new TH.Mesh(hsSweep(pr, hsArc(R, a0, a1, sub), { hi, base, hiC: M.userData.hsHi }), M));""",
    """    for (let i = 0; i < n; i++) { const a0 = A0 + i * each + gap / 2, a1 = A0 + (i + 1) * each - gap / 2; g.add(new TH.Mesh(hsSweep(pr, hsArc(R, a0, a1, sub), { hi, base, hiC: M.userData.hsHi }), M));""")
for a in ["hsArc(R + w / 2 - w * .28 + gw * .45, 0, TAU, Math.max(48, n * 6))", "hsArc(R + w * .12, 0, TAU, Math.max(48, n * 6))", "hsArc(R - w / 2 - .02, 0, TAU, Math.max(48, n * 6))"]:
    rep(a, a.replace("0, TAU, Math.max(48, n * 6)", "A0, A0 + AL, Math.max(24, Math.round(n * 6 * AL / TAU) + 2)"))
rep("""{ cap: false }), G)); }
    if (G && opt.faces !== false)""", """{ cap: AL < TAU }), G)); }
    if (G && opt.faces !== false)""")
# the Conduit
i = s.index("  function conduit() {"); e = s.index("    // light\n", i); body = s[i:e]
new = """  function conduit() { const grp = new TH.Group(), M = hullMat("cond", { rows: 6, bronze: .2, rep: [14, 1] }), M2 = hullMat("cond2", { rows: 6, slits: .5, rep: [4, 1] });
    /* v763 remodelled to its painting (see p763): bronze-edged dark steel, glowing inlays, one long crystal opening into the crown */
    const MH = hsMat(0x08070c, { hi: 0x4a3420, env: .35, rough: .38, metal: .6 }), GL = hsGlow(0xa448ff, 1.5);
    // the stepped plinth: five square tiers to 3.3, each riser lit
    [[3.0, 3.4, .7, .35], [2.42, 2.85, .7, 1.05], [1.85, 2.28, .7, 1.75], [1.3, 1.7, .7, 2.45], [.85, 1.12, .55, 3.05]].forEach(([a, b, h, y]) => { const m = hsFlat(new TH.CylinderGeometry(a, b, h, 4), MH, .12); m.rotation.y = Math.PI / 4; m.position.y = y; grp.add(m);
      const gl = new TH.Mesh(new TH.CylinderGeometry(a * 1.006, a * 1.006, .06, 4, 1, true), GL); gl.rotation.y = Math.PI / 4; gl.position.y = y + h / 2 - .07; grp.add(gl);
      const fw = (a + b) / 2 * Math.SQRT1_2; for (let f = 0; f < 4; f++) for (const j of [-.55, 0, .55]) { const F = new TH.Group(); F.userData.flat = 1; F.rotation.y = f * Math.PI / 2; const bar = new TH.Mesh(new TH.BoxGeometry(.07, h * .55, .03), GL); bar.position.set(j * fw, y, fw + .02); bar.rotation.x = Math.atan2(b - a, h) * .7; F.add(bar); grp.add(F); } });
    // four buttress legs leaning in to the crystal's base, a blade cap at each top, a light line down each
    for (let k = 0; k < 4; k++) { const a = k * TAU / 4 + TAU / 8, c = Math.cos(a), s = Math.sin(a), foot = V(c * 4.6, 0, s * 4.6), top = V(c * 1.9, 3.4, s * 1.9);
      grp.add(hsBeam(foot, top, .62, .5, MH, .7)); const cap = hsSpike(1.5, .34, MH); cap.position.copy(top).add(V(c * .3, -.1, s * .3)); cap.rotation.set(-s * .5, 0, c * .5); grp.add(cap);
      const ft = hsFlat(new TH.BoxGeometry(1.0, .5, 1.0), MH); ft.position.copy(foot).add(V(0, .25, 0)); ft.rotation.y = -a; grp.add(ft);
      const st = new TH.Mesh(hsSweep([[-.03, -.03], [.03, -.03], [.03, .03], [-.03, .03]], hsLine(foot.clone().add(V(0, .1, 0)), top.clone().add(V(0, -.05, 0)), 1)), GL); st.position.add(V(c * .02, .27, s * .02)); grp.add(st); }
    // front spine: a tall plated blade down the middle of the plinth, lit
    { const sp = hsFlat(new TH.BoxGeometry(.6, 2.9, .4), MH); sp.position.set(0, 1.5, 2.05); grp.add(sp); const sg = new TH.Mesh(new TH.BoxGeometry(.1, 2.5, .04), GL); sg.position.set(0, 1.55, 2.27); grp.add(sg); }
    // the crystal: a slim shaft from the plinth opening into the great crown crystal
    const cr = crystal([[0, 0], [.48, .35], [.58, 2.6], [.7, 4.6], [.55, 5.7], [1.18, 7.4], [1.05, 8.2], [0, 9.1]], 6); cr.position.y = 3.0; cr.userData.dyn = 1; cr.material.color.setHex(0x2a0874); cr.material.emissive.setHex(0x5a18e8); grp.add(cr);
    const inner = crystal([[0, 0], [.3, .5], [.4, 4.4], [.75, 7.3], [0, 8.6]], 6); inner.material = glowMat(0x9a40ff, .22); inner.userData.dyn = 1; inner.position.y = 3.05; grp.add(inner);
    // shard collars of tall dark blades: low, mid (with the emblem), and the crown's cradle
    const collar = (y, n, R, h, lean, r = .26) => { for (let k = 0; k < n; k++) { const a = k * TAU / n + .3, sp = hsSpike(h, r, MH); sp.position.set(Math.cos(a) * R, y, Math.sin(a) * R); sp.rotation.set(Math.sin(a) * lean, 0, -Math.cos(a) * lean); grp.add(sp); } };
    collar(3.2, 8, .95, 1.9, .16); collar(5.0, 6, .85, 1.5, .1); collar(8.1, 7, 1.0, 2.1, .22, .3);
    const emb = hsFlat(new TH.BoxGeometry(.75, 1.4, .32), MH); emb.position.set(0, 5.6, .9); emb.rotation.z = Math.PI / 4; grp.add(emb); const eg = new TH.Mesh(new TH.BoxGeometry(.16, .9, .05), GL); eg.position.set(0, 5.6, 1.08); grp.add(eg);
    // three rings, measured: low r3.9 at 5.0, middle r4.6 at 7.2, the split horned crown ring r4.0 at 9.6
    const rings = [];
    const mk = (R, y, w, h, tilt, arcs) => { const g = new TH.Group(); g.position.y = y; g.rotation.x = tilt;
      g.userData.arcs = []; for (const [p0, pl] of arcs) { const ag = new TH.Group(); ag.userData.c = p0 + pl / 2; ag.add(hsRing(R, w, h, MH, GL, { a0: p0, al: pl })); g.add(ag); g.userData.arcs.push(ag); }
      grp.add(g); rings.push(g); return g; };
    mk(3.9, 5.0, .5, .42, .04, [[0, TAU]]); mk(4.6, 7.2, .58, .5, -.03, [[0, TAU]]);
    const top = mk(4.0, 9.6, .52, .46, .05, [[.25, Math.PI - .5], [Math.PI + .25, Math.PI - .5]]);
    for (const a of [.25, Math.PI - .25, Math.PI + .25, TAU - .25]) { const h = hsSpike(1.5, .3, MH); h.position.set(Math.sin(a) * 4.0, .1, Math.cos(a) * 4.0); h.rotation.set(0, a, (a % Math.PI < 1 ? -1 : 1) * .9); top.userData.arcs[a < Math.PI ? 0 : 1].add(h); }
"""
# keep the cables and vents block (after the rings in the old body)
k = body.index("    // detail: conduit cables")
s = s[:i] + new + body[k:] + s[e:]
rep("""    const crPts = () => { const y = 2.5 + rnd() * 6.5, a = rnd() * TAU; return V(Math.cos(a) * .9, y, Math.sin(a) * .9); };
    const ringPt = () => { const g = rings[rnd() * 3 | 0], a = rnd() * TAU, R = g === rings[1] ? 4.4 : g === rings[0] ? 3.2 : 3.8;""",
    """    const crPts = () => { const y = 3.5 + rnd() * 7.5, a = rnd() * TAU; return V(Math.cos(a) * .7, y, Math.sin(a) * .7); };
    const ringPt = () => { const g = rings[rnd() * 3 | 0], a = rnd() * TAU, R = g === rings[1] ? 4.3 : g === rings[0] ? 3.6 : 3.7;""")
rep("cr.material.emissiveIntensity = .8 * p + .15;", "cr.material.emissiveIntensity = .42 * p + .12;")
rep("const hov = Math.sin(t * .0012) * .15 + ch * .5; cr.position.y = 1.9 + hov; inner.position.y = 2.0 + hov;", "const hov = Math.sin(t * .0012) * .15 + ch * .5; cr.position.y = 3.0 + hov; inner.position.y = 3.05 + hov;")
open(p, "w", encoding="utf-8").write(s)
print("ok")
