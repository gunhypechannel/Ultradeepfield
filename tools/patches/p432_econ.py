# v432: prices back to OGame's own (owner: "go back to near OGame original cost of light fighters": 3,000 metal + 1,000 crystal).
#  ECON_K 1.5 -> 1 (every building, research, ship, defence and missile at its OGame price again). Job times stay 1.15x OGame's
#  (ECON_T, the "slightly slower" of v431). Jobs queued during v431 keep what they paid and refund that.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("const ECON_K = 1.5, ECON_T = 1.15,", "const ECON_K = 1, ECON_T = 1.15, /* v432 OGame prices again; times stay 1.15x */")
t = t.replace("const GAME_V = 431;", "const GAME_V = 432;")
open(p, "w").write(t); print("ok")
