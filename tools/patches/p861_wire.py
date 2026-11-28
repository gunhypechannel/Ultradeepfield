"""v861: our fleets clear the escorts before the great ships (combat v10), and the Prime Resurrection Ark remastered (see p861_prime.js).
Owner: "in boss crab battles the fleet should always try to destroy the smaller ships first and then leave the big ships, same is true for
the continuums eternal commander and the prime resurrection ark, prime resurrection ark should have more spectacular and unique firing
animations and attacks also as well as turrets similar to the flag ship that target up to 6 ships at once", then "yes build it all please"
(escorts first, and +50% damage on the great ship once its escorts are gone, so the events keep about their pace)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 860;", "const GAME_V = 861;")
# combat v10: escorts first in a Carcinid boss's, the Eternal Commander's and the Prime Ark's battles; +30% on the great ship once alone
rep("const CB_V = 9, CB_OK = v => v === 3 || v === 4 || v === 5 || v === 6 || v === 7 || v === 8 || v === 9,", "const CB_V = 10, CB_OK = v => v === 3 || v === 4 || v === 5 || v === 6 || v === 7 || v === 8 || v === 9 || v === 10, /* v861 v10: escorts before the great ships */")
rep("V9 = (o.v || CB_V) >= 9, rngOf =", "V9 = (o.v || CB_V) >= 9, V10 = (o.v || CB_V) >= 10, bossK = k => V10 && ((typeof CRC_BK !== \"undefined\" && CRC_BK.has(k)) || k === \"cneter\" || k === \"cnprime\"), rngOf =")
rep("    const myBig = dc === \"guard\" ? sq.filter(f => f.side === s.side && active(f) && BIG_R.has(f.role)) : null;",
    "    const myBig = dc === \"guard\" ? sq.filter(f => f.side === s.side && active(f) && BIG_R.has(f.role)) : null;\n    const escUp = V10 && sq.some(f => f.side !== s.side && active(f) && !bossK(f.k)); /* v10 escorts first */")
rep("      if (gs && dc !== \"swarm\") sc *= e.cl === \"cruiser\" ? 2.2 : e.cl === \"frigate\" || e.cl === \"utility\" ? .2 : 1;",
    "      if (gs && dc !== \"swarm\") sc *= e.cl === \"cruiser\" ? 2.2 : e.cl === \"frigate\" || e.cl === \"utility\" ? .2 : 1;\n      if (escUp && bossK(e.k)) sc *= .08;")
rep("      * (s.cl === \"battlecruiser\" && (e.role === \"turret\" || e.role === \"station\") ? 1.25 : s.cl === \"battleship\" && e.role !== \"turret\" && e.role !== \"station\" ? 1.15 : 1);",
    "      * (s.cl === \"battlecruiser\" && (e.role === \"turret\" || e.role === \"station\") ? 1.25 : s.cl === \"battleship\" && e.role !== \"turret\" && e.role !== \"station\" ? 1.15 : 1)\n      * (V10 && bossK(e.k) && !sq.some(f => f.side === e.side && active(f) && !bossK(f.k)) ? 1.5 : 1); /* v10 the great ship alone takes more */")
# the Prime Ark's attacks and effects
js = open(__file__.rsplit('/', 1)[0] + "/p861_prime.js", encoding="utf-8").read()
rep("/* the Eternal Commander's five */", js + "/* the Eternal Commander's five */")
rep("  let a = CNT_XA[q.k]; if (q.k === \"cneter\") {", "  let a = CNT_XA[q.k]; if (q.k === \"cnprime\") { const ph = cntEterPh(b, v.s), n = (b.kPN = (b.kPN || 0) + 1); a = CNT_P5[(n - 1) % CNT_P5.length]; const gap = ph >= 2 ? 1.3 : ph >= 1 ? 2 : 2.7; if (last[v.s] != null && v.t - last[v.s] < gap) { b.kPN--; return; } } else if (q.k === \"cneter\") {")
rep("    else if (CNT_E5.includes(m.a)) cntEterAtk(", "    else if (CNT_P5.includes(m.a)) cntPrimeAtk(ctx, b, m, u, S0, E0, Lg, LE, d, T, t, scr, hit, rs, ws, W, H);\n    else if (CNT_E5.includes(m.a)) cntEterAtk(")
rep("try { cntAtkDraw(ctx, b, scr, T, W, H, d, t); cntDread(ctx, b, scr, T, W, H, d, t, lo); } catch (e) {} /* v856 */", "try { cntAtkDraw(ctx, b, scr, T, W, H, d, t); cntPrimeFx(ctx, b, scr, T, W, H, d, t); cntDread(ctx, b, scr, T, W, H, d, t, lo); } catch (e) {} /* v856, v861 */")
open(p, "w", encoding="utf-8").write(s); print("ok")
