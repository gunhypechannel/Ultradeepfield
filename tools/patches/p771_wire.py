"""v771: Aexion's ship form posed and coloured from its painting (owner: "finish all the rest"). In aexion-ship.webp the dreadnought is
seen three-quarter from above the bow, bright silver plating over dark gunmetal, cut through with hard blue light. In battle it sat
nose-on (a stubby block), far off and small, and its plating read lilac-grey (violet rim, env 1.35). Now it turns three-quarter, the
camera comes in, the silver is cleaner with a blue rim and stronger blue running lights. Applies on top of v770."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 770;", "const GAME_V = 771;")
rep('const MA = hullMat("aex", { rows: 3, pal: ["#7c8592", "#6c7482", "#8e97a4", "#5e6672", "#868e9a"], bronze: 0, slits: .42, sc: "#d8f4ff", sg: "#3aa8ff", metal: .92, rough: .3, rc: RC, ei: 3.4, rep: [.14, .14], relief: 2.2 }); MA.envMapIntensity = 1.35',
    'const MA = hullMat("aex", { rows: 3, pal: ["#5c6470", "#4c5460", "#6c7480", "#3e4652", "#646c78"], bronze: 0, slits: .42, sc: "#bfeaff", sg: "#2a9cff", metal: .85, rough: .26, rc: RC, ei: 3.8, rep: [.14, .14], relief: 2.2, rim: .6 }); MA.envMapIntensity = .8')
rep('rc: RC, ei: 3.6, rep: [.16, .16] }); MD.envMapIntensity = 1.5', 'rc: RC, ei: 3.6, rep: [.16, .16], rim: .6 }); MD.envMapIntensity = .7')
rep("supercube: 0, omega: 0, vaelthar: .75, aexion: 0,", "supercube: 0, omega: 0, vaelthar: .75, aexion: null,")
rep("aexion: [-.4, [-26, 10, 64], [0, 9, 0]]", "aexion: [-.5, [-30, 12, 70], [-8, 5, 0]]")
open(p, "w", encoding="utf-8").write(s)
print("ok")
