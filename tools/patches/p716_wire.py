# v716 (owner): the Starhive (wasp nest) looked smooth and broken; boss-site debris looked low-res and flat ("it shouldn't look smooth");
# monsters "skip across areas rather than the slow back and forth they used to do", and Rock Eaters "are hard to click on and bounce all
# over the place on map".
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__)); R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
def block(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i); assert s.count(a) == 1; s = s[:i] + new + s[j:]

# 1. the Starhive: a layered paper wasp nest (p716_nest.js)
block('    if (part !== "swarm") { const nest = lathe(NP, C.nest, 40);', '    if (part !== "nest") for (let i = 0; i < 9; i++)', R('p716_nest.js'))

# 2. monsters on the map: they swam a figure-eight about 15 slots wide (7.5 x 5, times the marker scale), so on a phone's frame rate
#    they seemed to skip from place to place, and the tap target stayed at the centre of that loop, far from the monster. They now
#    hover close to their spot (a small, slow drift), and a tap lands on the monster itself.
rep('RX = 7.5, RZ = 5, sa = Math.sin(a), ca = Math.cos(a);', 'RX = 1.4, RZ = .9, sa = Math.sin(a), ca = Math.cos(a); /* v715 a small, slow drift round its spot (it was 7.5 x 5) */')
rep('''  for (const [xid0, o] of W.pirates) { const x = PB[xid0]; if (!x || (G.find && !findHit(x))) continue;
    if (o.fog || !o.grp.visible) continue; const s = proj(o.grp.position); if (!s) continue;''',
    '''  for (const [xid0, o] of W.pirates) { const x = PB[xid0]; if (!x || (G.find && !findHit(x))) continue;
    if (o.fog || !o.grp.visible) continue; const s = proj(o.mon && o.body ? o.body.getWorldPosition(W.hitV || (W.hitV = new TH.Vector3())) : o.grp.position); if (!s) continue; /* v715 tap the monster where it is drawn */''')

# 3. boss-site debris: wrecked hulls glowed gold all over (a white emissive through the scorch map), the rubble round a shattered
#    planetoid was 20-face blocks that read as flat pink slabs up close, and the slab torn off the Cube Destroyer was a smooth sphere
rep('m.emissive.set(purple ? 0xc77dff : 0xffffff); m.emissiveMap = DK.emi; m.emissiveIntensity = purple ? 1.9 : 1.4;',
    'm.emissive.set(purple ? 0xc77dff : 0xff6a24); m.emissiveMap = DK.emi; m.emissiveIntensity = purple ? 1.5 : .9; /* v715 embers in the wounds, not gold all over */', 2)
rep('const rocks = new TH.InstancedMesh(new TH.IcosahedronGeometry(1, 0), new TH.MeshStandardMaterial({ color: 0x5a4a44, roughness: 1, flatShading: true }), LITE ? 16 : 36);',
    'const rocks = new TH.InstancedMesh(DK.rock || (DK.rock = jagRock(LITE ? 1 : 2, 515)), DK.rockM || (DK.rockM = new TH.MeshStandardMaterial({ color: 0x2f2925, roughness: 1, metalness: .05, flatShading: true, envMapIntensity: .2 })), LITE ? 16 : 36); /* v715 jagged basalt */')
rep('const slab = new TH.Mesh(new TH.SphereGeometry(R * 1.01, 16, 10, 0, 1.3, .9, 1.1), DK.mat);',
    'const slab = new TH.Mesh(jagShell(R * 1.01, 616), DK.mat); /* v715 a torn, buckled plate, not a smooth cap */')
rep('/* v419 a wreck\'s destruction pattern:', '''/* v715 debris shapes: a jagged rock (an icosahedron knocked about by layered noise, a chunk sheared off) and a torn, buckled hull plate
   (a slice of sphere whose edge is ragged and whose surface is dented) */
function jagRock(det, seed) { const g = new TH.IcosahedronGeometry(1, det), P = g.attributes.position, v = new TH.Vector3(), r = rnd(seed), o = [r() * 9, r() * 9, r() * 9], cut = new TH.Vector3(r() - .5, r() - .5, r() - .5).normalize();
  for (let i = 0; i < P.count; i++) { v.fromBufferAttribute(P, i); const n = .22 * Math.sin(v.x * 3.1 + o[0]) * Math.sin(v.y * 2.7 + o[1]) + .14 * Math.sin(v.z * 5.3 + o[2] + v.x * 2) + .08 * Math.sin(v.x * 9 + v.y * 7 + v.z * 8), c = v.dot(cut);
    v.multiplyScalar(1 + n); if (c > .45) v.addScaledVector(cut, -(c - .45) * .8); v.y *= .78; P.setXYZ(i, v.x, v.y, v.z); }
  g.computeVertexNormals(); return g; }
function jagShell(R, seed) { const g = new TH.SphereGeometry(R, 22, 14, 0, 1.3, .9, 1.1), P = g.attributes.position, U = g.attributes.uv, v = new TH.Vector3(), r = rnd(seed);
  for (let i = 0; i < P.count; i++) { v.fromBufferAttribute(P, i); const u = U.getX(i), w = U.getY(i), edge = Math.min(u, 1 - u, w, 1 - w), dent = .05 * Math.sin(u * 23 + r() * .3) * Math.sin(w * 17) + .03 * (r() - .5);
    let k = 1 + dent; if (edge < .12) k *= 1 - (.12 - edge) * (1.5 + 2.5 * r()); v.multiplyScalar(k); P.setXYZ(i, v.x, v.y, v.z); }
  g.computeVertexNormals(); return g; }
/* v419 a wreck's destruction pattern:''')

# 4. the Starhive's swarm turned each vertex by an angle that grew with its distance from the nest, so over minutes every wasp smeared
#    into a long orange shard round the ring (the "broken" look). The swarm now turns as one, and bobs by its angle, not its radius.
rep('float th = mt * (1.5 - rr * .18), c = cos(th), sn = sin(th); transformed.xz = vec2(transformed.x * c - transformed.z * sn, transformed.x * sn + transformed.z * c); transformed.y += .28 * sin(mt * 3.1 + rr * 5.);',
    'float th = mt * 1.05, c = cos(th), sn = sin(th); transformed.xz = vec2(transformed.x * c - transformed.z * sn, transformed.x * sn + transformed.z * c); transformed.y += .28 * sin(mt * 3.1 + atan(position.z, position.x) * 3.);')
rep('const GAME_V = 715;', 'const GAME_V = 716;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
