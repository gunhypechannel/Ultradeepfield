"""v815: map battles show each side as its flagship and a small escort. Owner: the battle drawn over a target showed two whole fleets
as wide as planets ("im wondering if its worth just removing that fleet and keeping just the flagship") -> "Flagship + small escort".
Outside the Battle for the Cube, each side's squadron is now its flagship (commanders only, as before) and 4 escorts of its two
strongest classes, drawn at about a third of a planet across. Losses still thin the escort round by round; bolts and blasts are
unchanged. The Cube's battle keeps its full squadrons."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 814;", "const GAME_V = 815;")
rep("const mk = (n, col, hostile, fg, sd) => { const ff0 = FLEET_FIN, sn = clashShips(n);",
    "const esc = c.loc !== NEXUS, mk = (n, col, hostile, fg, sd) => { const ff0 = FLEET_FIN, sn0 = clashShips(n), sn = esc ? clashEscort(sn0 || genComp(clashCnt(n))) : sn0; /* v815 a flagship and a small escort */")
rep("g.userData.size = fleetSzOf(sn || genComp(clashCnt(n)), g); /* v674 */",
    "g.userData.size = fleetSzOf(sn || genComp(clashCnt(n)), g, esc ? .6 : 1); /* v674; v815 the escort at about a third of a planet */")
rep("const genComp = n => {", """/* v815 the escort that stands for a side in a map battle: 4 ships of its two strongest classes */
const clashEscort = n => { const ks = Object.keys(n || {}).filter(k => SH[k] && n[k] > 0).sort((a, b) => unitCost(b) - unitCost(a)); if (!ks.length) return n; const o = {};
  if (ks.length === 1) o[ks[0]] = Math.min(4, n[ks[0]]); else { o[ks[0]] = Math.min(2, n[ks[0]]); o[ks[1]] = Math.min(4 - o[ks[0]], n[ks[1]]); } return o; };
const genComp = n => {""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
