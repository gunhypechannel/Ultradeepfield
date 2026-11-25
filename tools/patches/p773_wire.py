"""v773: Vaelthar closer to its painting, second pass (owner: "fix the rest, stay as close to the visual references"). v770's wing and
wheel changes were being undone every frame by the animation (it set the membranes back to faint glow and the wheel back to its old
place); now they hold. The wings rest spread wide and high as painted (they rested half folded), solid dark membranes; the wheel sits
higher and further back behind his shoulder; his scale armour is faceted (six-sided plates, hard edges) instead of smooth rings, and
his shoulders carry heavier gold pauldrons. Applies on top of v772."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 772;", "const GAME_V = 773;")
rep("wings.forEach(W => { const sp = .35 + st.spread * .65;", "wings.forEach(W => { const sp = .72 + st.spread * .28;")
rep("memM.opacity = .36 + st.spread * .16 + acc * .12 + fire * .15;", "memM.opacity = .8 + st.spread * .06 + acc * .06 + fire * .08;")
rep("wheel.position.set(0, 12.2 + Lw * 5.5, -11 - Lg * 2.5); }", "wheel.position.set(0, 14.5 + Lw * 5.5, -14 - Lg * 2.5); }")
rep("[[0, -.62], [.82, -.66], [1.04, -.28], [1.0, .3], [.76, .58], [0, .64]].map(([r, y]) => new TH.Vector2(r, y)), LO ? 10 : 14); scG.rotateX(Math.PI / 2);",
    "[[0, -.62], [.82, -.7], [1.1, -.3], [1.02, .34], [.7, .6], [0, .64]].map(([r, y]) => new TH.Vector2(r, y)), 6); scG.rotateX(Math.PI / 2); scG.rotateZ(Math.PI / 6); scG.computeVertexNormals(); { const g2 = scG.toNonIndexed(); g2.computeVertexNormals(); scG.copy(g2); }")
rep("const pd = new TH.Mesh(crescentGeo(1.9, .7, 1.1, .5), MG); pd.position.set(sx * .3, .5, -.1);", "const pd = new TH.Mesh(crescentGeo(2.4, 1.0, 1.15, .7), MG); pd.position.set(sx * .3, .7, -.1);")
rep("const memM = new TH.MeshBasicMaterial({ map: memT, color: 0x9a86b8,", "const memM = new TH.MeshBasicMaterial({ map: memT, color: 0x6e5e92,")
open(p, "w", encoding="utf-8").write(s)
print("ok")
