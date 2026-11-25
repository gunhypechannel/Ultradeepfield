"""v768: the Elementals' horns made chunky and sculptural, as painted (owner: "finish all the rest"). Every crescent in the Elemental
builds (and the few other bosses that use crescentGeo) was a flat extruded band; in the paintings they are heavy horns, thick in the
middle and tapering to points, faceted with sharp ridges. crescentGeo now sweeps a six-sided ridged section along the arc (hard-
surface kit), thick in both directions at the middle and drawn to a point at each tip, with UVs so the elements' liquid-metal veins
run along each horn; the glowing copy becomes a lit ridge along the outer edge. hsSweep now writes UVs (u along the path, v round the
section). Applies on top of v767."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 767;", "const GAME_V = 768;")
# hsSweep writes uvs
rep("""  function hsSweep(prof, F, opt = {}) { const m = prof.length, N = F.length, pos = [], nor = [], col = [],""", """  function hsSweep(prof, F, opt = {}) { const m = prof.length, N = F.length, pos = [], nor = [], col = [], uvs = [], UVQ = [],""")
rep("""      const L = flip ? [a, c, b] : [a, b, c], LN = flip ? [na, nc, nb] : [na, nb, nc]; for (let k = 0; k < 3; k++) { pos.push(L[k].x, L[k].y, L[k].z); nor.push(LN[k].x, LN[k].y, LN[k].z); col.push(cc.r, cc.g, cc.b); } };""",
    """      const L = flip ? [a, c, b] : [a, b, c], LN = flip ? [na, nc, nb] : [na, nb, nc], LU = UVQ.length ? (flip ? [UVQ[0], UVQ[2], UVQ[1]] : UVQ) : null; for (let k = 0; k < 3; k++) { pos.push(L[k].x, L[k].y, L[k].z); nor.push(LN[k].x, LN[k].y, LN[k].z); col.push(cc.r, cc.g, cc.b); uvs.push(LU ? LU[k][0] : 0, LU ? LU[k][1] : 0); } };""")
rep("""        tri(a, b, c, n0, n0, n1, cc); tri(a, c, d, n0, n1, n1, cc); } }""",
    """        const u0 = F[i].u * (opt.uvL || 1), u1 = F[i + 1].u * (opt.uvL || 1), v0 = j / m, v1 = (j + 1) / m;
        UVQ.length = 0; UVQ.push([u0, v0], [u0, v1], [u1, v1]); tri(a, b, c, n0, n0, n1, cc); UVQ.length = 0; UVQ.push([u0, v0], [u1, v1], [u1, v0]); tri(a, c, d, n0, n1, n1, cc); UVQ.length = 0; } }""")
rep("""g.setAttribute("color", new TH.Float32BufferAttribute(col, 3)); return g; }
  // chamfered box profile""", """g.setAttribute("color", new TH.Float32BufferAttribute(col, 3)); g.setAttribute("uv", new TH.Float32BufferAttribute(uvs, 2)); return g; }
  // chamfered box profile""")
# the horn
i = s.index("  function crescentGeo(R, th, span = 1.25, d = .6) {"); e = s.index("\n", s.index("return g; }", i)) + 1
s = s[:i] + """  function crescentGeo(R, th, span = 1.25, d = .6) { /* v768 a heavy ridged horn (horns toward +y): a six-sided section swept along the arc, thick at the middle, drawn to a point at each tip */
    const N = 30, F = hsArc(R, -Math.PI / 2 - span, -Math.PI / 2 + span, N, "xy"), tp = u => Math.pow(Math.max(0, Math.sin(Math.PI * u)), .55), D = Math.max(d, th * .85);
    return hsSweep([[0, 0], [-.22, .42], [-.7, .5], [-1, .1], [-1, -.1], [-.7, -.5], [-.22, -.42]], F, { sc: u => [th * tp(u) + .01, D * (.3 + .7 * tp(u)) + .01], uvL: 3 }); }
""" + s[e:]
# the fire elemental's layout, measured from el-fire-skin.webp: the crown is a U (horns up) and the great horns are two wide U's,
# one inside the other, sweeping out and up from behind the heart (they were four separate horns turned sideways)
rep("""      { const c = cres(4.2, 1.4, 1.2, 1.1); c.position.y = 13; c.rotation.z = Math.PI; body.add(c); parts.cres.push({ g: c, base: c.position.clone(), r0: c.rotation.clone(), dir: new TH.Vector3(0, 1, 0) }); }
      { const d = dia(2.6, 3.6); d.position.y = 3.2;""", """      { const c = cres(3.2, 1.3, 1.25, 1.1); c.position.y = 13.2; body.add(c); parts.cres.push({ g: c, base: c.position.clone(), r0: c.rotation.clone(), dir: new TH.Vector3(0, 1, 0) }); }
      { const d = dia(2.6, 3.6); d.position.y = 3.2;""")
rep("""      for (const sx of [-1, 1]) for (const [y, R, sp] of [[6, 9, .95], [0, 11, 1.0]]) { const c = cres(R, 1.9, sp, 1.2); c.rotation.z = sx * (Math.PI / 2 + .35); c.position.set(sx * 2, y, 0); body.add(c); parts.cres.push({ g: c, base: c.position.clone(), r0: c.rotation.clone(), dir: new TH.Vector3(sx, .3, 0), big: 1 }); }""",
    """      for (const [y, R, sp, th] of [[9.5, 9.5, 1.45, 1.6], [3.1, 12.1, 1.5, 1.75]]) { const c = cres(R, th, sp, 1.2); c.position.set(0, y, -.6); body.add(c); parts.cres.push({ g: c, base: c.position.clone(), r0: c.rotation.clone(), dir: new TH.Vector3(0, .4, 0), big: 1 }); }""")

# framing: the creature should fill the battle view as it fills its painting. The rune circles were drawn far outside the body
# (out to R 22) and the camera stood back to fit them, so the creature read small and thin. Runes pulled in, camera brought closer.
rep("for (const [R, rx, y, sp] of [[19, Math.PI / 2 - .35, -2, .00012], [13.5, Math.PI / 2 + .3, 3, -.0002], [9, .12, 0, .0003], [22, .02, 0, -.00006]])",
    "for (const [R, rx, y, sp] of [[15.5, Math.PI / 2 - .35, -2, .00012], [11.5, Math.PI / 2 + .3, 3, -.0002], [7.5, .12, 0, .0003], [16.5, .02, 0, -.00006]])")
rep("const halo = sprite(44, `rgba(${E.rgb},1)`, \"hel\" + kind); halo.material.opacity = .32;", "const halo = sprite(36, `rgba(${E.rgb},1)`, \"hel\" + kind); halo.material.opacity = .26;")
rep("elemental: [-.2, [-8, 4, 86], [0, 0, 0]]", "elemental: [-.2, [-6, 3, 64], [0, 0, 0]]")
# light: the four claws are big sickles in the painting, nearly touching the diamonds
rep("const a = Math.PI / 4 + i * Math.PI / 2, c = cres(4.2, 1.5, 1.1, 1.0); c.position.set(Math.cos(a) * 5.4, Math.sin(a) * 5.4, 0);",
    "const a = Math.PI / 4 + i * Math.PI / 2, c = cres(5.6, 1.9, 1.2, 1.2); c.position.set(Math.cos(a) * 5.0, Math.sin(a) * 5.0, 0);")
# nature: broad leaf-blades, not needles
rep("L = i % 2 ? 9 : 12.5, b = new TH.Mesh(bladeGeo(L, L * .28, .5), MD);", "L = i % 2 ? 9.5 : 13, b = new TH.Mesh(bladeGeo(L, L * .4, .9), MD);")
rep("const e = new TH.Mesh(bladeGeo(L, L * .28, .06), G2);", "const e = new TH.Mesh(bladeGeo(L, L * .4, .08), G2);")

# the Overlord's pyramid gets its point back (owner: "the top of the pyramid is cut off, it was better last time"). v764 squashed it to
# H 2.6 to match the low painting; it is a pyramid again at its old height, and the battle camera steps back so the legs and tip fit.
rep("const B = 4.2, H = 2.6, y0 = .45, /* v764 low and wide, as painted */", "const B = 4.2, H = 5.8, y0 = .45, /* v768 the full pointed pyramid (owner) */")
rep("overlord: [-Math.PI / 2, [-10, 4, 32], [0, -1.5, 0]]", "overlord: [-Math.PI / 2, [-12, 5, 43], [0, -.8, 0]]")
rep("overlord: [-8, 7],", "overlord: [-8, 10],")
open(p, "w", encoding="utf-8").write(s)
print("ok")
