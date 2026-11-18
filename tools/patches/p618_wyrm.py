# v618: the Event Horizon Wyrm becomes a ghost serpent, so it can no longer be mistaken for the Leviathan (owner: "Event horizon wyrm
# still looks like [the Leviathan]? ... Do it all"). Same lore, new body: glassy violet rings with starlight inside and no armour or spines,
# an eyeless lamprey mouth of turning rings of light teeth instead of the fanged skull, a comet wisp for a tail, cool violet light
# everywhere the Leviathan burns orange, and every so often it slides head-first into the black hole and comes out on the far side.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# materials: glass for the ghost's rings, its light cool violet
rep('    const RC = [1, .5, .3], ORA = 0xffa040;\n', '    const RC = [1, .5, .3], ORA = LV ? 0xffa040 : 0xb898ff, GH = LV ? null : new TH.MeshBasicMaterial({ color: 0x4a2a9a, transparent: true, opacity: .26, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false }); /* v618 the ghost\'s glass */\n')
rep('const segs = inst(new TH.TorusGeometry(1, .21, 8, 30), MA, N),', 'const segs = inst(new TH.TorusGeometry(1, LV ? .21 : .16, 8, 30), LV ? MA : GH, N),')
rep('new TH.MeshBasicMaterial({ map: galTex(), transparent: true, opacity: .6, blending', 'new TH.MeshBasicMaterial({ map: galTex(), transparent: true, opacity: LV ? .6 : .95, blending')
rep('const spine = inst(spG, glowMat(LV ? 0xff5a10 : 0xb060ff, LV ? .42 : .3), N);', 'const spine = inst(spG, glowMat(LV ? 0xff5a10 : 0x8a70ff, LV ? .42 : .22), N);')
rep('if (LV) { cores.visible = false; bh.visible = false; }', 'if (LV) { cores.visible = false; bh.visible = false; } else fins.visible = false; /* v618 no spines on the ghost */')
# the head: the Leviathan keeps the armoured skull and fanged jaws; the Wyrm gets an eyeless lamprey mouth
rep("    { const pr = [[0, -2.2], [1.7, -1.8], [2.1, -.2], [1.9, 1.8], [1.3, 3.4], [.5, 4.4], [0, 4.6]], sk =", "    if (LV) { const pr = [[0, -2.2], [1.7, -1.8], [2.1, -.2], [1.9, 1.8], [1.3, 3.4], [.5, 4.4], [0, 4.6]], sk =")
rep("    const jaws = []; for (const up of [1, -1]) {", "    const jaws = [], lamp = []; if (!LV) { /* v618 the lamprey mouth: a glass hood flaring to a rim of light, three rings of light teeth turning inside */\n"
    "      const hood = new TH.Mesh(new TH.LatheGeometry([[.9, -3], [1.3, -1.6], [1.9, -.2], [2.5, 1.1], [3, 2]].map(([r, y]) => new TH.Vector2(r, y)), 28), GH); hood.rotation.x = Math.PI / 2; hood.userData.dyn = 1; hd.add(hood);\n"
    "      const lip = new TH.Mesh(new TH.TorusGeometry(3, .14, 8, 48), glowMat(0xece4ff, 1)); lip.position.z = 2; lip.userData.dyn = 1; hd.add(lip); const tM = glowMat(0xffffff, 1);\n"
    "      for (const [z, r, n] of [[1.7, 2.6, 14], [1.05, 2, 12], [.4, 1.4, 10]]) { const g = new TH.Group(); g.position.z = z; hd.add(g); for (let q = 0; q < n; q++) { const a = q / n * TAU, f = shard(.13, .75, tM); f.position.set(Math.cos(a) * r, Math.sin(a) * r, 0); f.rotation.z = a + Math.PI / 2; g.add(f); } lamp.push(g); } }\n"
    "    if (LV) for (const up of [1, -1]) {")
rep("eye.add(eP);\n", "eye.add(eP); eye.visible = LV; /* v618 the ghost is eyeless */\n")
rep("const lens = new TH.Group(); lens.position.set(0, .35, 7.4);", "const lens = new TH.Group(); lens.position.set(0, .35, LV ? 7.4 : 2.4);")
# the tail: a blade for the Leviathan, a comet wisp for the ghost
rep("const tail = new TH.Group(); body.add(tail); { const b =", "const tail = new TH.Group(); body.add(tail); if (!LV) { const s = sprite(7, \"rgba(200,180,255,1)\", \"gwisp\"); tail.add(s); } else { const b =")
rep("}, 0xffd0a0);\n    const st = { rot: 0,", "}, LV ? 0xffd0a0 : 0xc8b0ff);\n    const st = { rot: 0, off: 0, ep: -1, dv: 0, last: 0,")
# the dive: every 22 s it slides head-first into the black hole and comes out on the far side (not while it is attacking)
rep("      st.rot = t * .00011; st.coil = coil;", "      st.rot = t * .00011 + st.off; st.coil = coil;\n"
    "      let dvE = -1; if (!LV) { const P_ = 22000, ep = Math.floor((t + 6000) / P_), g = ((t + 6000) % P_) / P_, busy = fc >= 0 || fl >= 0 || fs >= 0, dt = Math.min(100, Math.max(0, t - st.last)); st.last = t; st.dv = Math.min(1, Math.max(0, st.dv + (busy ? -dt / 500 : dt / 1500)));\n"
    "        if (g > .68) { dvE = (g - .68) / .32; if (dvE >= .5 && st.ep !== ep) { st.ep = ep; if (st.dv > .95) { st.off += Math.PI * .9; st.rot += Math.PI * .9; } } } }\n"
    "      const dvK = dvE < 0 ? -1 : dvE < .5 ? dvE * 2 * 1.35 - .2 : (dvE - .5) * 2 * 1.35 - .2, pull = u => dvE < 0 || st.dv <= 0 ? 0 : st.dv * ss(0, 1, (dvE < .5 ? dvK - u : u - dvK) / .18); /* how far into the hole each part of the body is */")
rep("      else for (let i = 0; i <= N + 1; i++) path(i / N, t, pts[i]);", "      else for (let i = 0; i <= N + 1; i++) { path(i / N, t, pts[i]); if (!LV) { const pl = pull(i / N); if (pl > 0) pts[i].lerp(tmp.set(0, -1, 0), pl); } }")
rep("const u = i / N, sc = (RG ? RG.s * (1 - u * .55) : 2.35 * (1 - u * .62)) * (i === 0 ? 1.1 : 1);", "const u = i / N, sc = (RG ? RG.s * (1 - u * .55) : 2.35 * (1 - u * .62)) * (i === 0 ? 1.1 : 1) * (LV ? 1 : Math.max(.001, 1 - pull(u)));")
rep("if (LV) c1.setRGB(b * 1.2, b * (.4 + hot * .35), b * (.08 + hot * .2)); else c1.setRGB(b * (1 + hot * .1), b * (.5 + hot * .5), b * (.22 + hot * .9));",
    "if (LV) c1.setRGB(b * 1.2, b * (.4 + hot * .35), b * (.08 + hot * .2)); else c1.setRGB(b * (.55 + hot * .45), b * (.48 + hot * .5), b * (1.05 + hot * .1)); /* v618 cool violet starlight */")
rep("head.scale.setScalar(RG ? RG.s * 1.1 / 2.35 : 1); tail.scale.setScalar(RG ? RG.s * .45 / 1.05 : 1);",
    "head.scale.setScalar(RG ? RG.s * 1.1 / 2.35 : LV ? 1 : Math.max(.001, 1 - pull(0))); tail.scale.setScalar(RG ? RG.s * .45 / 1.05 : LV ? 1 : Math.max(.001, 1 - pull(1)));")
rep("      for (const J of jaws) J.j.rotation.x =", "      lamp.forEach((g, k) => { g.rotation.z = t * .0007 * (k % 2 ? -1 : 1) * (1 + gape * 3); g.scale.setScalar(1 + gape * .35 - coil * .1); });\n      for (const J of jaws) J.j.rotation.x =")
rep("trail.put(i, p.x, p.y, p.z, 2.6 * (1 - i / 48), swing * (1 - i / 48) * .9));", "trail.put(i, p.x, p.y, p.z, 2.6 * (1 - i / 48), (LV ? swing : Math.max(swing, .3 * Math.max(.001, 1 - pull(1)))) * (1 - i / 48) * .9));")
rep("well.material.opacity = coil * .9;", "well.material.opacity = Math.max(coil * .9, dvE < 0 ? 0 : st.dv * .75 * Math.sin(dvE * Math.PI));")
rep("const DN = LOD === 1 ? 40 : 70, deb = inst(new TH.DodecahedronGeometry(.6, 0), MA, DN);", "const DN = LOD === 1 ? 40 : 70, deb = inst(new TH.DodecahedronGeometry(.6, 0), LV ? MA : hullMat(\"wymd\", { rows: 3, pal: [\"#1a1424\", \"#221a2e\", \"#140f1c\"], slits: .2, sc: \"#d8c8ff\", sg: \"#9a70ff\", metal: .9, rough: .3, rc: [.6, .5, 1], ei: 1.6, rep: [1, 1] }), DN);")
rep('wym: { k: "wbWym", n: "Event Horizon Wyrm", ic: "❂", col: "#ffa040"', 'wym: { k: "wbWym", n: "Event Horizon Wyrm", ic: "❂", col: "#b898ff"')
# words: the Bestiary line and the code comment
rep('d: "A serpent of black-hole rings coiled round the black hole at the centre of the galaxy. Only its glowing segments',
    'd: "A ghost serpent of glass rings with starlight inside, coiled round the black hole at the centre of the galaxy, sliding in and out of the event horizon. Only its glowing segments')
s2 = re.sub(r"GAME_V = 617\b", "GAME_V = 618", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
