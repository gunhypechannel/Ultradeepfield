"""v770: Vaelthar posed and coloured from its painting (owner: "finish all the rest"). In vaelthar.webp the dragon is seen three-quarter,
dark armour edged in gold, great dark wings spread behind it with violet light in the membranes, the celestial wheel standing behind its
shoulder. In battle it faced the camera head-on (a narrow column of scale rings), its armour read pale lilac (mirror metal, env 2), its
wings were faint additive glow, and the wheel filled the frame in front of everything. Now: turned three-quarter, armour darker and less
mirror-like, gold less blinding, wing membranes solid dark violet with glowing veins, the wheel smaller and higher behind it.
Applies on top of v769."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 769;", "const GAME_V = 770;")
rep('slits: .2, sc: "#f0d8ff", sg: "#c070ff", veins: 18, vc: "#b878ff", glyphs: 1, metal: .9, rough: .2, rc: RC, ei: 3.8, rep: [3, 1] }); MA.normalScale.set(2.4, 2.4)',
    'slits: .2, sc: "#a060f0", sg: "#c070ff", veins: 18, vc: "#b878ff", glyphs: 1, metal: .6, rough: .4, rc: RC, ei: 2.4, rep: [3, 1], rim: .55 }); MA.envMapIntensity = .4; MA.normalScale.set(2.4, 2.4)')
rep('vc: "#9a5cff", metal: .88, rough: .28, rc: RC, ei: 2.0, rep: [1, 1], side: 1 });',
    'vc: "#9a5cff", metal: .6, rough: .42, rc: RC, ei: 2.0, rep: [1, 1], side: 1, rim: .55 }); MS.envMapIntensity = .4;')
rep('sg: "#ffd06a", metal: 1, rough: .11, rc: [1, .82, .45], ei: 2.4, rep: [2, 1] }); MG.envMapIntensity = 2.1', 'sg: "#ffd06a", metal: 1, rough: .18, rc: [1, .82, .45], ei: 2.0, rep: [2, 1], rim: .6 }); MG.envMapIntensity = 1.1')
rep('ei: 3.4, rep: [4, 1], glyphs: 1 }); MGd.envMapIntensity = 2.0', 'ei: 3.4, rep: [4, 1], glyphs: 1, rim: .6 }); MGd.envMapIntensity = 1.0')
# the wings: solid dark membranes lit from within
rep('const memM = new TH.MeshBasicMaterial({ map: memT, color: 0xffffff, transparent: true, opacity: .45, side: TH.DoubleSide, depthWrite: false, blending: TH.AdditiveBlending, toneMapped: false });',
    'const memM = new TH.MeshBasicMaterial({ map: memT, color: 0x9a86b8, transparent: true, opacity: .9, side: TH.DoubleSide, depthWrite: false, toneMapped: false });')
# the wheel: smaller, higher, further back
rep("const wheel = new TH.Group(); wheel.position.set(0, 11, -11); wheel.rotation.y = .12; body.add(wheel); const WR = 14.5;",
    "const wheel = new TH.Group(); wheel.position.set(0, 14, -14); wheel.rotation.y = .12; body.add(wheel); const WR = 11.5;")
rep("vaelthar: [-.35, [-21, 9, 50], [0, 9, 0]]", "vaelthar: [-.35, [-21, 9, 54], [3, 9.5, 0]]")
rep("const WB_FRONT = { medusara: 0, khezaroth: 0, supercube: 0, omega: 0, vaelthar: 0,", "const WB_FRONT = { medusara: 0, khezaroth: 0, supercube: 0, omega: 0, vaelthar: .75,")
# the forelimbs: great clawed arms reaching forward, as painted (they were little T-rex arms)
rep("const arms = []; for (const sx of [-1, 1]) { const sh = new TH.Group(); sh.position.set(sx * 2.3, 5.2, 2.0); body.add(sh);", "const arms = []; for (const sx of [-1, 1]) { const sh = new TH.Group(); sh.position.set(sx * 2.5, 5.6, 2.0); sh.scale.setScalar(1.6); body.add(sh);")
open(p, "w", encoding="utf-8").write(s)
print("ok")
