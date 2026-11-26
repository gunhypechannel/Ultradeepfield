"""v814: the base's 3D models hold far less memory on phones. Owner's Fold: 2-3 s freezes opening the base and the game restarted after a
moment in the background; its reports showed 215 base textures / 253 MB (447 MB with everything) at the moment it was killed. Measured:
the 40 building and ship models of a grown base held 159 textures, ~426 MB on Android (first 8 buildings' colour maps at 1536, the rest
1024, ships 1024, detail maps 512). Now on phones: buildings' colour 1024, normal 512, roughness/metalness 256; ships 512 and 256 (as iPhones
already had). The first upload on opening the base shrinks with it."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 813;", "const GAME_V = 814;")
rep("""const shipIOS = IOS && GLB_SHIPS.has(k), s = g.scene, big = shipIOS ? 512 : MOBILE ? (GLB_BLDS.has(k) && !IOS && GLB_BN++ < 8 ? 1536 : 1024) : 2048, aux = shipIOS ? 256 : MOBILE ? 512 : 1024, /* v381: iPhone ships at a quarter */ an = texAniso(), ps = [];
      s.traverse(o => { if (o.isMesh) { const m = o.material; if (m && m.isMeshStandardMaterial) { m.envMapIntensity = .9; ps.push(glbShrink(m.map, big)); for (const t of new Set([m.normalMap, m.roughnessMap, m.metalnessMap])) ps.push(glbShrink(t, aux)); for (const t of [m.map, m.normalMap]) if (t) t.anisotropy = an; } } });""",
    """const shipIOS = MOBILE && GLB_SHIPS.has(k), s = g.scene, big = shipIOS ? 512 : MOBILE ? 1024 : 2048, aux = shipIOS ? 256 : MOBILE ? 512 : 1024, aux2 = MOBILE ? 256 : aux, /* v381: iPhone ships at a quarter; v814 every phone: ships 512/256, buildings 1024/512/256 (was 1536 for 8 of them) */ an = texAniso(), ps = [];
      s.traverse(o => { if (o.isMesh) { const m = o.material; if (m && m.isMeshStandardMaterial) { m.envMapIntensity = .9; ps.push(glbShrink(m.map, big)); if (m.normalMap) ps.push(glbShrink(m.normalMap, aux)); for (const t of new Set([m.roughnessMap, m.metalnessMap])) if (t && t !== m.normalMap) ps.push(glbShrink(t, aux2)); for (const t of [m.map, m.normalMap]) if (t) t.anisotropy = an; } } });""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
