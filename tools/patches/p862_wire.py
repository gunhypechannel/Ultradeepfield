"""v862: the Eternal Commander's Annihilation Barrage replaces its Annihilation Lance (see p862_barrage.js)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 861;", "const GAME_V = 862;")
rep('const CNT_E5 = ["eSwarm", "eLance", "eTalon", "eOrb", "eGrid", "eRes"];', 'const CNT_E5 = ["eSwarm", "eBarrage", "eTalon", "eOrb", "eGrid", "eRes"]; /* v862 the Barrage for the Lance */')
rep("eGrid: 2.2, eRes: 2.4, eSwarm: 3.4 };", "eGrid: 2.2, eRes: 2.4, eSwarm: 3.4, eBarrage: 3.6 };")
rep("function cntEterAtk(ctx, b, m, u, S0, E0, Lg, LE, d, T, t, scr, hit, rs, ws, W, H) { if (m.a === \"eSwarm\")",
    open(__file__.rsplit('/', 1)[0] + "/p862_barrage.js", encoding="utf-8").read() + "function cntEterAtk(ctx, b, m, u, S0, E0, Lg, LE, d, T, t, scr, hit, rs, ws, W, H) { if (m.a === \"eBarrage\") return cntEterBarrage(ctx, b, m, u, S0, E0, Lg, d, T, t, scr, hit, rs, W, H); if (m.a === \"eSwarm\")")
rep('/lance|execute|eLance|resurrect/.test(m.a) ? "omega"', '/lance|execute|eLance|eBarrage|resurrect/.test(m.a) ? "omega"')
open(p, "w", encoding="utf-8").write(s); print("ok")
