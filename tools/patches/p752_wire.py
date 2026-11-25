"""v752: the space monsters sculpted after the owner's paintings (loader p752_mon.js, meshes docs/art/mon/m/<k>.bin listed in
tools/sculpt/mon_sc.json); merged battle masters no longer free a sculpt's shared geometry."""
import sys, os, json
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(D, "..", "..")
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 751;", "const GAME_V = 752;")
js = open(os.path.join(D, "p752_mon.js"), encoding="utf-8").read().strip()
sc = json.load(open(os.path.join(R, "tools", "sculpt", "mon_sc.json")))
have = {k: v for k, v in sc.items() if os.path.exists(os.path.join(R, "docs", "art", "mon", "m", k + ".bin"))}
js = js.replace("const MON_SC = {}, MON_GEO = {};", "const MON_SC = " + json.dumps(have, separators=(",", ":")) + ", MON_GEO = {};")
rep("\nfunction buildMonster(k, part) {\n", "\n" + js + "\nfunction buildMonster(k, part) {\n")
rep("""  if (/^alpha\\d$/.test(k)) return buildMimic("malpha" + k.slice(5)); if (k === "nexus") return buildMimic("mnexus"); if (k === "omega") return buildMimic("momega"); /* v665, v667 */
""", """  if (/^alpha\\d$/.test(k)) return buildMimic("malpha" + k.slice(5)); if (k === "nexus") return buildMimic("mnexus"); if (k === "omega") return buildMimic("momega"); /* v665, v667 */
  if (!part) { monSculptLoad(k); if (MON_GEO[k]) return monSculpted(k); } /* v752 */
""")
rep("""    s0.traverse(o => { if (o.geometry) o.geometry.dispose(); }); }""", """    s0.traverse(o => { if (o.geometry && !o.userData.sculpt) o.geometry.dispose(); }); } /* v752 a sculpt's geometry is shared */""")
open(p, "w", encoding="utf-8").write(s)
print("ok", len(have), "sculpted:", " ".join(sorted(have)))
