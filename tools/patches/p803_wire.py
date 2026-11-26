"""v803: the Aetherion saga (behind the owner switch "aet"): four seasons after the first year, Vesper Station, the living station's
crossing, Nhalis's transformation and the First Aperture's assembly on the map; lattice growths, assembler swarms, Nhalis spires and
unstable echoes as targets; weekly beats, orders, the galaxy's shared effort (event/aet_saga), Saturday finales with cinematic cards;
the Aetherion Records in the Archives and the saga's Advisor lines (drafts for the owner)."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
C = open(os.path.join(D, "p803_aet.js"), encoding="utf-8").read()
AR = open(os.path.join(D, "p803_arch.js"), encoding="utf-8").read()
CSS = open(os.path.join(D, "p803.css"), encoding="utf-8").read().replace("\n", "")
rep("const GAME_V = 802;", "const GAME_V = 803;")
rep("\nconst PIRATES = PIRATES_ALL.filter(", "\n" + C + "\nconst PIRATES = PIRATES_ALL.filter(")
rep("CNT_PLATS, CRC_BOSSES, AET_TGT).filter(x => !monGone(x));", "CNT_PLATS, CRC_BOSSES, AET_TGT, AET_SG).filter(x => !monGone(x));")
rep('ARCH_ORD.push("cn_cont", "cn_ark", "cn_prime", "cn_signal");', 'ARCH_ORD.push("cn_cont", "cn_ark", "cn_prime", "cn_signal");\n' + AR)
rep("let html = ({ aet: shAet,", "let html = ({ aetsaga: shAetSaga, aet: shAet,")
rep("|| !!it.aetR)); A.aCol[j + 3]", "|| !!it.aetR || it.aetSg != null && aetSgHid(it, T))); A.aCol[j + 3]")
rep("|| !!it.aetR)); /* v430 */", "|| !!it.aetR || it.aetSg != null && aetSgHid(it, T))); /* v430 */")
rep("x.aetR ? aetForce(x) : CNT_M[x.mon] ? cntForce(x) :", "x.aetR || x.aetSg != null ? aetForce(x) : CNT_M[x.mon] ? cntForce(x) :")
rep("const xRegroup = x => CNT_M[x.mon] ? CNT_REGROW :", "const xRegroup = x => x.aetSg != null ? 3 * 3600e3 : CNT_M[x.mon] ? CNT_REGROW :")
rep('if (CNT_M[x.mon] && !cntLive(x, f.arrive)) { note(`${x.name} is gone. Fleet returning, nothing lost.`, "warn"); return; } /* v740 */',
    'if (CNT_M[x.mon] && !cntLive(x, f.arrive)) { note(`${x.name} is gone. Fleet returning, nothing lost.`, "warn"); return; } /* v740 */\n  if (x.aetSg != null && !aetSgLive(x, f.arrive)) { note(`${x.name} is gone. Fleet returning, nothing lost.`, "warn"); return; } /* v803 */')
rep("    if (CNT_M[x.mon]) try { cntWin(x, rep, f.arrive); } catch (e) {} /* v740 */", "    if (CNT_M[x.mon]) try { cntWin(x, rep, f.arrive); } catch (e) {} /* v740 */\n    if (x.aetSg != null) try { aetSgWin(x, rep, f.arrive); } catch (e) {} /* v803 */")
# the saga's targets are announced to everyone: no fog
rep("nf = fogSeen(x, z) || !!CNT_BOSS[it.id];", "nf = fogSeen(x, z) || !!CNT_BOSS[it.id] || it.aetSg != null;")
rep("nf = fogSeen(q.x, q.z) || !!CNT_BOSS[it.id];", "nf = fogSeen(q.x, q.z) || !!CNT_BOSS[it.id] || it.aetSg != null;")
rep("if (!fogSeen(q.x, q.y) && !CNT_BOSS[x.id]) return shUnexplored(x); }", "if (!fogSeen(q.x, q.y) && !CNT_BOSS[x.id] && x.aetSg == null) return shUnexplored(x); }")
rep("function isFogged(p, T) { if (!p || p.owner === G.me || CNT_BOSS[p.id]) return false;", "function isFogged(p, T) { if (!p || p.owner === G.me || CNT_BOSS[p.id] || p.aetSg != null) return false;")
i = s.index("</style>"); s = s[:i] + CSS + s[i:]
open(p, "w", encoding="utf-8").write(s)
print("ok")
