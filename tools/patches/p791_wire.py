"""v791: the Brood Matriarch and the Iron Tyrant closer to their paintings (owner: "build it all").
- Brood Matriarch: the battle camera turns her to a three-quarter profile as painted (she faced the camera square on, a spider on a
  dish); her brood eggs and her four brood pods are smaller, the eggs darker and dimmer, so the glowing egg sac and her black chitin carry the picture.
- Iron Tyrant: its boarding claw, the painting's centrepiece, is a third bigger and hangs lower under the bow; the battle
  camera turns the bow toward you so the claw is in view; the junk crates' lit slits are dimmed to rusted iron (they read as a
  stack of bright painted containers). Its broadsides are unchanged.
Applies on top of v790."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 790;", "const GAME_V = 791;")
rep("matriarch: 0, tyrant: -.55,", "matriarch: .85, tyrant: -.75,")
rep("r = 6.4 + rnd() * 2.2, s = .75 + rnd() * .6,", "r = 6.4 + rnd() * 2.2, s = .45 + rnd() * .35,")
rep("const eggM = new TH.MeshStandardMaterial({ color: 0x1e3406, emissive: 0x9cff30, emissiveIntensity: .5,", "const eggM = new TH.MeshStandardMaterial({ color: 0x0e1a03, emissive: 0x9cff30, emissiveIntensity: .32,")
rep('hm = (k, pal, sl) => { const m = hullMat(k, { rows: 3, cols: 3, pal, slits: sl, sc: "#ffe0a0", sg: "#ff9a30", rust: 1, metal: .5, rough: .7, rc: RC, ei: 2.2,',
    'hm = (k, pal, sl) => { const m = hullMat(k, { rows: 3, cols: 3, pal, slits: sl, sc: "#ffe0a0", sg: "#ff9a30", rust: 1, metal: .5, rough: .7, rc: RC, ei: 1.2,')
rep("rust: 1, metal: .7, rough: .6, rc: RC, ei: 2, rep: [1, 1] }); MD.envMapIntensity = .4;", "rust: 1, metal: .7, rough: .6, rc: RC, ei: 1.3, rep: [1, 1] }); MD.envMapIntensity = .4;")
rep("arm.position.set(15.5, -.6, 0); arm.scale.setScalar(1.7); arm.rotation.z = -.62;", "arm.position.set(15.8, -2.2, 0); arm.scale.setScalar(2.3); arm.rotation.z = -.75; /* v791 the painting's great claw */")
rep("g.position.set(Math.cos(a) * 10.4, -.4, Math.sin(a) * 10.4); body.add(g);\n", "g.position.set(Math.cos(a) * 10.4, -.4, Math.sin(a) * 10.4); g.scale.setScalar(.62); body.add(g); /* v791 smaller brood pods */\n")
open(p, "w", encoding="utf-8").write(s)
print("ok")
