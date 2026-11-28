"""v857: the Advisor's two Continuum lines (owner: "yes to all"): during the scan, the first time on this device; when the Eternal Commander
arrives, every time."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 856;", "const GAME_V = 857;")
rep("    if (!b.kScanSnd && T > .7) { b.kScanSnd = 1; try { mimSfx(\"hum\", 0); } catch (e) {} } }",
    "    if (!b.kScanSnd && T > .7) { b.kScanSnd = 1; try { mimSfx(\"hum\", 0); } catch (e) {} try { if (!them.some(i => b.Q[i].k === \"cneter\") && advOnce(\"cntScan\")) sbSay(CNT_SCAN_LINE); } catch (e) {} } } /* v857 */")
rep("        if (!b.kEsnd) { b.kEsnd = 1; try { mimSfx(\"omega\", 0); } catch (e2) {} } }",
    "        if (!b.kEsnd) { b.kEsnd = 1; try { mimSfx(\"omega\", 0); } catch (e2) {} try { sbSay(CNT_ETER_LINE); } catch (e2) {} } } /* v857 */")
rep("const cntQ = q => q && CNT_U[q.k];", '''const CNT_SCAN_LINE = "They're scanning us, Commander. Every hull, every crew. They're deciding what we're worth.", CNT_ETER_LINE = "That's the Eternal Commander. We've killed it before. It doesn't remember dying… it only remembers us."; /* v857 owner-approved */
const cntQ = q => q && CNT_U[q.k];''')
open(p, "w", encoding="utf-8").write(s); print("ok")
