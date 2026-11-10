# v405: a boss rises to meet a huge fleet. Above 0.75x the boss's power, the boss's hull, shields and attack scale with the fleet so the
# matchup only edges up (ratio 0.75 x (excess)^0.05): ten times past the threshold still destroys about a fifth of it in one attack,
# the 10-million-ship stress fleet about half, instead of the whole boss in a volley. Small fleets fight exactly as before.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("""function wbShOf(key, st, at) {""", """const WB_RISE = .75, WB_RISE_E = .05; // v405: where a boss starts to rise to meet a fleet, and how gently the fleet's edge grows beyond it
function wbRise(A, Dd) { const pw = st => st.reduce((a, s) => a + s.n * unitPow(s), 0), P = pw(A), B = pw(Dd); if (!(B > 0) || P <= B * WB_RISE) return 1;
  const x = P / (B * WB_RISE), F = x / Math.pow(x, WB_RISE_E); for (const s of Dd) { s.atk *= F; s.hull *= F; } return F; } // not the shields: a shot too weak for a shield is deflected, so scaled shields would make a big fleet harmless
function wbShOf(key, st, at) {""")
rep("""    const res = simulate(stacksOf(f.n, techOf(null), G.me), stacksOf({ [D.k]: n0 }, { wbSh: shK }, "wboss"));""",
    """    const A0 = stacksOf(f.n, techOf(null), G.me), D0 = stacksOf({ [D.k]: n0 }, { wbSh: shK }, "wboss"), rise = wbRise(A0, D0), res = simulate(A0, D0);""")
rep("""wb: key, wbSh: shK, wbSeg: [n0, left], lvl: 25,""", """wb: key, wbSh: shK, wbRise: rise > 1.01 ? Math.round(rise * 10) / 10 : undefined, wbSeg: [n0, left], lvl: 25,""")
rep("""    if (!left) { bump("bosses"); note(`We brought down the ${D.n}!""", """    if (rise > 1.01) note(`The ${D.n} rose to meet our fleet: ×${fmt(Math.round(rise))} toughness and firepower against a force this size.`, "warn");
    if (!left) { bump("bosses"); note(`We brought down the ${D.n}!""")
rep("""Dd = stacksOf({ [D.k]: c.n0 }, { wbSh: c.sh }, "wboss"), res = simulate(A, Dd), ms = performance.now() - t0;""", """Dd = stacksOf({ [D.k]: c.n0 }, { wbSh: c.sh }, "wboss"), rise = wbRise(A, Dd), res = simulate(A, Dd), ms = performance.now() - t0;""")
rep("""wb: c.key, wbSh: c.sh, wbSeg: [c.n0, left], lvl: 25,""", """wb: c.key, wbSh: c.sh, wbRise: rise > 1.01 ? Math.round(rise * 10) / 10 : undefined, wbSeg: [c.n0, left], lvl: 25,""")
rep("""      r = { c, ok: !bad.length, bad, ms, msR, rounds: res.rounds.length,""", """      r = { c, ok: !bad.length, bad, ms, msR, rise, rounds: res.rounds.length,""")
rep("""lost ${fmt(r.lost)} ships${r.cd ? `, ${r.cd} Cube Destroyers` : ""}` : ""}""", """lost ${fmt(r.lost)} ships${r.cd ? `, ${r.cd} Cube Destroyers` : ""}${r.rise > 1.01 ? ` · it rose ×${fmt(Math.round(r.rise))}` : ""}` : ""}""")
t = t.replace("const GAME_V = 404;", "const GAME_V = 405;")
open(p, "w").write(t); print("ok")
# (applied after, replacing wbRise): wbRiseK gives the starting factor; wbFightRise targets the outcome: past the threshold an attack destroys
# 20% of the full hull rising with log10 of the excess to at most 60%; an overshooting fight is re-fought with a tougher boss (up to 7 tries).
# Only hull and attack scale: scaled shields deflected every small ship's shots and made big fleets harmless.
# (applied after) the boss factor is bisected toward the target (9 tries, closest result kept)
# (applied after) threshold 0.5x the boss's power; target 30% of the hull at the threshold rising to 60%
