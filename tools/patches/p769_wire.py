"""v769: Khezaroth and Medusara coloured from their paintings; Medusara's serpents rise from her crown. Khezaroth (owner: "finish all the rest"). In khezaroth-skin.webp the sphinx is dark obsidian with violet
light in the cracks and gold on the nemes, collar and claws; the model read pale lavender because its stone was mirror-bright metal
reflecting the environment (env 1.1-1.9, metalness .9). The stone is now darker, less metallic and rougher, with a softer rim; gold keeps
its shine. Its rune rings stop crowding the frame and the battle camera comes in so it fills the view like its painting.
Applies on top of v768."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 768;", "const GAME_V = 769;")
rep('vc: "#a868ff", metal: .92, rough: .2, rc: RC, ei: 3.2, rep: [2, 1] }); MO.envMapIntensity = 1.7;',
    'vc: "#a868ff", metal: .6, rough: .4, rc: RC, ei: 3.2, rep: [2, 1], rim: .55 }); MO.envMapIntensity = .4;')
rep('vc: "#c48cff", metal: .4, rough: .52, rc: RC, ei: 3.0, rep: [2, 1], relief: 1.4 }); MB.envMapIntensity = 1.2;',
    'vc: "#c48cff", metal: .35, rough: .58, rc: RC, ei: 3.0, rep: [2, 1], relief: 1.4, rim: .55 }); MB.envMapIntensity = .35;')
rep('vc: "#8a58d8", metal: .7, rough: .48, rc: RC, ei: 2.6, rep: [1, 1], relief: .8 }); MF.envMapIntensity = 1.1;',
    'vc: "#8a58d8", metal: .45, rough: .55, rc: RC, ei: 2.6, rep: [1, 1], relief: .8, rim: .5 }); MF.envMapIntensity = .3;')
rep('emissiveIntensity: 2.4, metalness: .9, roughness: .24, side: TH.DoubleSide, envMapIntensity: 1.9 }); MS.userData.P = {}; rimOn(MS, 1, RC);',
    'emissiveIntensity: 2.4, metalness: .9, roughness: .26, side: TH.DoubleSide, envMapIntensity: .9 }); MS.userData.P = {}; rimOn(MS, .6, RC);')
rep("khezaroth: [0, [-24, 20, 96], [0, 13, 4]]", "khezaroth: [0, [-17, 15, 70], [0, 11.5, 4]]")
# the black hole between the paws: a violet whirl round true black, as painted, not a white-hot blaze that drowns the paws
rep('const accM = new TH.MeshBasicMaterial({ map: accTex(), color: 0xd0a0ff, transparent: true,', 'const accM = new TH.MeshBasicMaterial({ map: accTex(), color: 0x8a48e8, transparent: true, opacity: .8,')
rep('[.43, "rgba(235,215,255,.9)"], [.46, "rgba(170,120,255,.25)"]', '[.43, "rgba(200,150,255,.75)"], [.46, "rgba(150,90,255,.22)"]')
rep('const heartS = sprite(9, "rgba(206,150,255,1)", "khz_heart");', 'const heartS = sprite(6.5, "rgba(186,120,255,1)", "khz_heart");')
rep('const CORE = new TH.MeshBasicMaterial({ color: 0xf4e6ff, toneMapped: false }), GL = glowMat(VIOL, .85), BLK', 'const CORE = new TH.MeshBasicMaterial({ color: 0xc490ff, toneMapped: false }), GL = glowMat(VIOL, .85), BLK')
# Medusara, from medusara-skin.webp: the face is dark weathered stone (it read pale grey-lilac), the serpents dark bronze with gold
# between the scales (they read pale lilac), the rim light softer so the stone does not glow at its edges
rep('const MS = hullMat("med3", { rows: 1, cols: 1, pal: ["#57535e"],', 'const MS = hullMat("med3", { rows: 1, cols: 1, pal: ["#2c2930"], rim: .5,')
rep('const MSk = new TH.MeshStandardMaterial({ color: 0xb4b0bc, metalness: .7, roughness: .32, envMapIntensity: .6,', 'const MSk = new TH.MeshStandardMaterial({ color: 0x6b5236, metalness: .75, roughness: .34, envMapIntensity: .55,')
# her serpents rise from the crown and fan across the upper half of the head as painted, none hanging beneath her chin (they ringed her
# all the way round, like legs); darker bronze
rep("const NSN = 9, snakes = []; for (let i = 0; i < NSN; i++) { const a = -2.75 + i / (NSN - 1) * 5.5,", "const NSN = 9, snakes = []; for (let i = 0; i < NSN; i++) { const a = -1.95 + i / (NSN - 1) * 3.9,")
rep("color: 0x6b5236, metalness: .75, roughness: .34, envMapIntensity: .55, map: medScale(0), emissiveMap: medScale(1), emissive: 0xffa83a, emissiveIntensity: .9 })",
    "color: 0x4a3826, metalness: .75, roughness: .34, envMapIntensity: .55, map: medScale(0), emissiveMap: medScale(1), emissive: 0xffa83a, emissiveIntensity: .7 })")
open(p, "w", encoding="utf-8").write(s)
print("ok")
