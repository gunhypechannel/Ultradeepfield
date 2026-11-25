"""v767: the Iron Tyrant and the Brood Matriarch coloured from their paintings. The Tyrant's painting is one rusted beast of scrap,
dark rust and burnt brown lit by fire; its welded hull slices were bright red, ochre, steel blue and white. They are now five rust
browns (dark iron, burnt umber, oxide, scorched steel, tar), the tarps a dried blood brown. The Matriarch's painting is near-black
olive chitin lit by acid green; her shell read as pale glass. Her chitin is darker and less mirror-like, the green veins and the
egg light kept. Applies on top of v766."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 766;", "const GAME_V = 767;")
rep("""const HM = [hm("tyrR", ["#6a2a16", "#5a2414", "#74321a"], .25), hm("tyrY", ["#74581e", "#66501a", "#806224"], .2), hm("tyrS", ["#3e4c58", "#46545e", "#36424c"], .3), hm("tyrW", ["#625c52", "#58524a", "#6c665a"], .15), hm("tyrB", ["#5a3a24", "#4a3020", "#64422a"], .2)];""",
    """const HM = [hm("tyrR", ["#3c1a0e", "#33170c", "#462011"], .25), hm("tyrY", ["#4a3214", "#3e2a10", "#563a18"], .2), hm("tyrS", ["#2a2420", "#322a24", "#241e1a"], .3), hm("tyrW", ["#3a3028", "#332a22", "#42362c"], .15), hm("tyrB", ["#2e1e14", "#26180f", "#36241a"], .2)]; /* v767 rust and burnt iron, as painted */""")
rep("MeshStandardMaterial({ color: 0x8a1c14", "MeshStandardMaterial({ color: 0x4a1a0c")
# the Matriarch's chitin: darker, less glassy
rep("""const MC = hullMat("brd", { rows: 7, pal: ["#2e2b20", "#25231a", "#383322", "#1f1d16"], slits: .2, sc: "#e0ff90", sg: "#9dff2a", veins: 16, vc: "#a6e640", metal: .55, rough: .22, rc: RC, ei: 2.4, rep: [3, 2] });""",
    """const MC = hullMat("brd", { rows: 7, pal: ["#16150e", "#121109", "#1c1a10", "#0e0d08"], slits: .2, sc: "#e0ff90", sg: "#9dff2a", veins: 16, vc: "#a6e640", metal: .35, rough: .38, rc: RC, ei: 2.6, rep: [3, 2] }); MC.envMapIntensity = .45; /* v767 near-black olive chitin, as painted */""")
rep("""const MB = hullMat("brdb", { rows: 3, pal: ["#1b1a14", "#24221a", "#2e2a1c"], slits: .08, sc: "#e0ff90", sg: "#9dff2a", veins: 10, vc: "#a6e640", metal: .5, rough: .18, rc: RC, ei: 2.2, rep: [1, 2], side: 1 });""",
    """const MB = hullMat("brdb", { rows: 3, pal: ["#100f0a", "#16150e", "#1c1a10"], slits: .08, sc: "#e0ff90", sg: "#9dff2a", veins: 10, vc: "#a6e640", metal: .35, rough: .32, rc: RC, ei: 2.4, rep: [1, 2], side: 1 }); MB.envMapIntensity = .45;""")
rep("""const MN = hullMat("brdn", { rows: 5, pal: ["#16150f", "#1c1a12", "#121109"], slits: 0, sg: "#7ad020", veins: 22, vc: "#5e9a1c", metal: .15, rough: .8, rc: RC, rim: .4, ei: 1.6, rep: [5, 1] });""", """const MN = hullMat("brdn", { rows: 5, pal: ["#0e0d08", "#12110a", "#0a0906"], slits: 0, sg: "#7ad020", veins: 22, vc: "#5e9a1c", metal: .1, rough: .9, rc: RC, rim: .15, ei: 1.8, rep: [5, 1] }); MN.envMapIntensity = .3;""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
