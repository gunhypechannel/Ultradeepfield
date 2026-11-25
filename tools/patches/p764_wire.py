"""v764: the Pyramid Overlord reshaped to its painting (docs/art/boss/overlord-skin.webp, 1024x576; owner: "build them them all just as
you described"). The painting shows a low, wide armoured pyramid (half-width 4.2, rising 2.6 above its skirt) striding on four great
arched legs, two to a side, not six round it: each femur rises from a hip drum to a peaked knee about 6 out and 2.8 up, and a long
blade-shin slants out to a foot about 10 out on the ground 3.4 below. Shins carry a broad lit stripe, as painted; the belly's
down-beam rests dimmer. Applies on top of v763."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 763;", "const GAME_V = 764;")
i = s.index("  function overlord() {"); e = s.index("\n  function ", i + 30); o = s[i:e]
def r(a, b, n=1):
    global o
    c = o.count(a); assert c == n, (c, a[:120]); o = o.replace(a, b)
r("const B = 4.3, H = 5.8, y0 = .45,", "const B = 4.2, H = 2.6, y0 = .45, /* v764 low and wide, as painted */")
r("    for (let k = 0; k < 6; k++) { const a = k * TAU / 6, L = new TH.Group();", "    for (let k = 0; k < 4; k++) { const a = [.38, Math.PI - .38, Math.PI + .38, TAU - .38][k], L = new TH.Group(); /* v764 four legs, two to a side */")
r("const kp = V(3.4, 2.8, 0);", "const kp = V(2.4, 3.6, 0);")
r("const fp = V(1.7, -8.4, 0);", "const fp = V(5.0, -6.2, 0);")
r("""        for (let q = 1; q < 4; q++) { const p = V(0, 0, 0).lerp(fp, q / 5),""", """        { const st = new TH.Mesh(new TH.BoxGeometry(.12, fp.length() * .78, .62), glowMat(VIO, .9)); st.position.copy(fp).multiplyScalar(.5).add(V(.62, 0, 0)); st.rotation.z = Math.atan2(fp.x, -fp.y); kn.add(st); } /* the broad lit stripe down each shin */
        for (let q = 1; q < 4; q++) { const p = V(0, 0, 0).lerp(fp, q / 5),""")
r("const groundY = -.55 + 2.8 - 8.4 - .4,", "const groundY = -.55 + 3.6 - 6.2 - .4,")
r("fw0.set(1.7, -8.4, 0);", "fw0.set(5.0, -6.2, 0);")
r("bm.material.opacity = .4 * f; bm2.material.opacity = .75 * Math.min(1.3, f);", "bm.material.opacity = .4 * f * (.35 + surge * .65); bm2.material.opacity = .75 * Math.min(1.3, f) * (.35 + surge * .65);")
r('const M = hullMat("ovl", { rows: 6, bronze: .16, slits: .35, rep: [1, 1] }), MP = hullMat("ovlp", { rows: 3, slits: .55, bronze: .3, rep: [1, 1] }), ML = hullMat("ovl2", { rows: 5, slits: .4, rep: [2, 3] }),',
  'const M = hullMat("ovl", { rows: 6, bronze: .16, slits: .35, rep: [1, 1], base: "#1a1424" }), MP = hullMat("ovlp", { rows: 3, slits: .55, bronze: .3, rep: [1, 1], base: "#211830" }), ML = hullMat("ovl2", { rows: 5, slits: .4, rep: [2, 3], base: "#1a1424" }),')
r("const pk = shard(.6, 2.0, M);", "const pk = shard(.45, 1.1, M);")
s = s[:i] + o + s[e:]
open(p, "w", encoding="utf-8").write(s)
print("ok")
