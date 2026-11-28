"""v858 (owner: "when starting the stress test continuum fabrication battle the scan starts across the screen then skips back and forth and
then starts again, can we clean it up for all and make sure it always starts from the same side of the screen? it should identify all as
targets and then fade away, also fabrication platform should have more ships launching"). The scan ran on the replay's clock (which can
jump back) and picked its side from the first two ships' positions (which change as they move): now its own clock, once per battle,
always left to right, every ship marked TARGET, then a fade. The Eternal Commander's entrance on the same clock. The Fabrication Carrier
launches twelve drones from both flanks (was five) and launches more often."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 857;", "const GAME_V = 858;")
a = s.index("  /* the scan (the first 3.4 s) */"); b = s.index("  /* the dread: a red haze")
s = s[:a] + open(__file__.rsplit('/', 1)[0] + "/p858_scan.js", encoding="utf-8").read() + s[b:]
rep("if (alive && P && sn[i] == null) sn[i] = T;\n    if (alive && P) { const e = T - sn[i], ph = cntEterPh(b, i);", "if (alive && P && sn[i] == null && !(b.intro > 0)) sn[i] = t;\n    if (alive && P && sn[i] != null) { const e = (t - sn[i]) / 1000, ph = cntEterPh(b, i); /* v858 its own clock */")
# the Fabrication Carrier: twelve drones from both flanks, launched more often
rep("for (let j = 0; j < 5; j++) { const kk = clamp(k * 1.3 - j * .08, 0, 1), sx = S0.x + (j - 2) * Lg * .1, sy = S0.y + (j % 2 ? 1 : -1) * Lg * .16,",
    "for (let j = 0; j < 12; j++) { const kk = clamp(k * 1.6 - j * .05, 0, 1), sx = S0.x + ((j >> 1) % 3 - 1) * Lg * .14, sy = S0.y + (j % 2 ? 1 : -1) * Lg * .18,")
rep("{ cnint: .9, cncor: 1.6, cnexe: 1.8, cnfab: 2,", "{ cnint: .9, cncor: 1.6, cnexe: 1.8, cnfab: 1.4,")
# the Eternal Commander's sixth attack, its drone swarm on up to eight targets at once
rep('const CNT_E5 = ["eLance", "eTalon", "eOrb", "eGrid", "eRes"];', 'const CNT_E5 = ["eLance", "eTalon", "eSwarm", "eOrb", "eGrid", "eRes"];')
rep("a = CNT_E5[(n - 1) % 5];", "a = CNT_E5[(n - 1) % CNT_E5.length];")
rep("eGrid: 2.2, eRes: 2.4 };", "eGrid: 2.2, eRes: 2.4, eSwarm: 2.2 };")
rep("function cntEterAtk(ctx, b, m, u, S0, E0, Lg, LE, d, T, t, scr, hit, rs, ws, W, H) {", open(__file__.rsplit('/', 1)[0] + "/p858_swarm.js", encoding="utf-8").read() + "function cntEterAtk(ctx, b, m, u, S0, E0, Lg, LE, d, T, t, scr, hit, rs, ws, W, H) { if (m.a === \"eSwarm\") return cntEterSwarm(ctx, b, m, u, S0, E0, Lg, d, T, scr, hit, rs);")
open(p, "w", encoding="utf-8").write(s); print("ok")
