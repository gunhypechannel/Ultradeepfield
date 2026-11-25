"""v772: Aexion rebuilt toward its paintings (owner: "fix the rest, stay as close to the visual references"). Pass 1: the surface.
Its hull plates were tiled with a small square-panel texture full of lit windows, so every slab read as a pile of boxes (a voxel look);
in aexion-ship.webp and aexion-warform.webp the armour is clean polished silver and dark navy gunmetal, broken only by hard blue light
lines. The armour now has no tiled texture: polished silver and deep gunmetal, crisp chamfered edges catching the light, blue rim.
Applies on top of v771."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 771;", "const GAME_V = 772;")
rep("""    const CORE = new TH.MeshBasicMaterial({ color: 0xe8f6ff, toneMapped: false }), GL = glowMat(BLUE, .85), GW = glowMat(0xcfeeff, .95);
    // angular armour: a chamfered slab, and a pointed blade""", """    /* v772 clean armour: polished silver and navy gunmetal, no tiled panel texture */
    for (const [m, c, mt, rg, en] of [[MA, 0x2a323e, .75, .3, .38], [MD, 0x060a14, .7, .36, .3]]) { for (const k of ["map", "emissiveMap"]) m[k] = null; m.normalScale.set(.8, .8); m.color.setHex(c); m.emissive.setHex(0x000000); m.metalness = mt; m.roughness = rg; m.envMapIntensity = en; m.needsUpdate = true; }
    const CORE = new TH.MeshBasicMaterial({ color: 0xe8f6ff, toneMapped: false }), GL = glowMat(BLUE, .85), GW = glowMat(0xcfeeff, .95);
    // angular armour: a chamfered slab, and a pointed blade""")
# Pass 2: the shape. As a ship it read as a heap of the mech's blocks under a standing rune arch; aexion-ship.webp is one long dagger
# hull, a pointed prow, the deck flat and armoured, blue light along its edges. Two great hull halves (left and right) now close over the
# folded mech's back as the dagger's deck; as it stands they swing up behind its shoulders as the two great blade-wings of the
# Warform painting (still nothing swapped or hidden: they are the hull, then the wings). The rune halo lies flat in the deck as a ship
# and only stands up behind the head in the warform.
rep("""    const halo = J(chest, [0, 7.4, -3.4], [0, 5.6, -3.2], [0, 0, 0], [-Math.PI / 2, 0, 0], .6, .76);""",
    """    /* v772 the dagger hull: its two halves are the ship's deck, then the warform's blade-wings */
    const hullH = [-1, 1].map(sx => { const h = J(chest, [sx * 2.2, 6.0, -3.8], [0, 0, -2.6], [.5, sx * -.2, sx * -.85], [0, 0, 0], .2, .46), O = [[0, 28], [1.6, 22], [4.4, 11], [6.8, 2], [6.9, -8], [5.6, -15.5], [0, -14.5]].map(([x, y]) => [sx * x, y]);
      const sh = new TH.Shape(); O.forEach(([x, y], k) => k ? sh.lineTo(x, y) : sh.moveTo(x, y)); sh.closePath(); const g = new TH.ExtrudeGeometry(sh, { depth: 1.1, bevelEnabled: true, bevelThickness: .3, bevelSize: .3, bevelSegments: 1 }); g.translate(0, 0, -1.1); if (sx < 0) { const ix = g.index; } h.add(new TH.Mesh(g, MA));
      const sh2 = new TH.Shape(), I = O.map(([x, y]) => [x * .62 + sx * .5, y * .86 - .8]); I.forEach(([x, y], k) => k ? sh2.lineTo(x, y) : sh2.moveTo(x, y)); sh2.closePath(); const g2 = new TH.ExtrudeGeometry(sh2, { depth: .5, bevelEnabled: true, bevelThickness: .15, bevelSize: .15, bevelSegments: 1 }); g2.translate(0, 0, -1.8); h.add(new TH.Mesh(g2, MD));
      for (let k = 1; k < O.length - 1; k++) { const a = V(O[k][0], O[k][1], -1.5), b = V(O[k + 1][0], O[k + 1][1], -1.5), m = glowBar(.16, a.distanceTo(b), .16); m.position.copy(a).add(b).multiplyScalar(.5); m.rotation.z = Math.atan2(-(b.x - a.x), b.y - a.y); h.add(m); }
      { const sp = slab(1.3, 36, 1.8, MA, .5, .3); sp.rotation.z = Math.PI; sp.position.set(sx * .62, 5.5, -2.6); h.add(sp); const gl = glowBar(.12, 30, .12); gl.position.set(sx * 1.32, 6.5, -2.9); h.add(gl); }
      { const tw = slab(2.6, 6.5, 2.6, MD, .6, .6); tw.position.set(sx * 2.3, -9.5, -3.2); h.add(tw); const tw2 = spike(1.4, 4.2, .9, MA); tw2.position.set(sx * 2.3, -11.5, -4.6); tw2.rotation.x = -Math.PI / 2 + .35; h.add(tw2); for (const yy of [-8, -10.5]) { const w = glowBar(2.2, .14, .14); w.position.set(sx * 2.3, yy, -4.55); h.add(w); } }
      for (const y of [8, 1, -6, -12]) { const m = glowBar(Math.abs(O[2][0]) * .55, .12, .12); m.position.set(sx * Math.abs(O[2][0]) * .45, y, -2.12); h.add(m); }
      return h; });
    const halo = J(chest, [0, 7.4, -3.4], [0, 3.0, -4.6], [0, 0, 0], [0, 0, 0], .6, .76);""")
# the battle camera looks down on the deck, as the painting does
rep("aexion: [-.5, [-30, 12, 70], [-8, 5, 0]]", "aexion: [-.5, [-30, 42, 64], [-8, 2, 0]]")
open(p, "w", encoding="utf-8").write(s)
print("ok")
