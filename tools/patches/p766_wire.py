"""v766: the Leviathan's body made solid, as painted (docs/art/boss/leviathan-skin.webp: a black-scaled serpent with molten light between
its scales). Its body was a chain of thin rings; each segment is now a faceted armoured barrel (ten scale facets, a lip at the back
so segments overlap like scales; flat-shaded, crisp), the molten rims between them stay, and the dorsal fins are faceted blades.
The Event Horizon Wyrm keeps its ghost-glass body (the owner's v618 choice to tell it apart from the Leviathan). Applies on top of v765."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 765;", "const GAME_V = 766;")
rep("""    const segs = inst(new TH.TorusGeometry(1, LV ? .21 : .16, 8, 30), LV ? MA : GH, N),""",
    """    const LVM = LV ? hsMat(0x050404, { hi: 0x1c120c, metal: .65, rough: .3, env: .35 }) : null, lvSeg = () => { /* v766 a faceted armoured barrel, its back lip overlapping the next */ const g = new TH.LatheGeometry([[0, -.78], [.86, -.74], [.96, -.35], [1.0, .2], [1.12, .62], [.9, .78], [0, .8]].map(([r, z]) => new TH.Vector2(r, z)), 10); g.rotateX(Math.PI / 2); return hsFlat(g, LVM, .35).geometry; };
    const segs = inst(LV ? lvSeg() : new TH.TorusGeometry(1, .16, 8, 30), LV ? LVM : GH, N),""")
rep("""const finG = LV ? new TH.ConeGeometry(.38, 2.7, 4) : new TH.ConeGeometry(.3, 1.6, 4); finG.translate(0, LV ? 2.1 : 1.6, 0); const fins = inst(finG, MA, N);""",
    """const finG = LV ? hsFlat(new TH.ConeGeometry(.42, 2.9, 4), LVM, .6).geometry : new TH.ConeGeometry(.3, 1.6, 4); finG.translate(0, LV ? 2.1 : 1.6, 0); if (LV) finG.scale(.45, 1, 1.3); const fins = inst(finG, LV ? LVM : MA, N);""")
rep("if (LV) c1.setRGB(b * 1.2, b * (.4 + hot * .35), b * (.08 + hot * .2));", "if (LV) c1.setRGB(b * .85, b * (.22 + hot * .35), b * (.03 + hot * .2)); /* v766 molten light between dark scales, not gold bands */")
rep("""for (const e of [0, 1]) { S.w.copy(S.v).multiplyScalar((e ? .3 : -.3) * sc).add(pts[i]); S.s.setScalar(sc * 1.04);""", """for (const e of [0, 1]) { S.w.copy(S.v).multiplyScalar((e ? .3 : -.3) * sc * (LV ? 2.4 : 1)).add(pts[i]); S.s.setScalar(sc * (LV ? .99 : 1.04));""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
