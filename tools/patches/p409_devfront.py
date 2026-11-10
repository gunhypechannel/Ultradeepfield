# v409 (4): the Orbital Devourer faces your fleet in the battle report on every screen shape. On a wide report (an open Fold, a tablet,
# landscape) it was drawn side-on (WB_VIEW), so its maw and its main beam pointed off the right edge of the screen; only tall phone
# reports used the front view (WB_FRONT). WB_FACE lists the bosses whose weapon fires from the front, which now always use the front view.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("""const m3 = WB[key].m3, V0 = WB_VIEW[m3], tall = h > w * .75;""", """const m3 = WB[key].m3, V0 = WB_VIEW[m3], tall = h > w * .75 || !!WB_FACE[m3];""")
rep("""const WBR = {}; const WB_FRONT = {""", """const WB_FACE = { devourer: 1 }; // v409: bosses whose main weapon fires from the front face the fleet on wide reports too
const WBR = {}; const WB_FRONT = {""")
open(p, "w").write(t); print("ok")
