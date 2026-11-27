"""v818: monsters stop jumping on the map (owner video: the camera on a Celestial Serpent cut across the map; "monsters are still jumping
around on map view"; "Kraken eggs, sentinel, rock eaters, shouldn't move at all only float in space"). Cause, measured with a 60 fps
virtual clock in Free view: v619's avoidance (monAvoid) pushed a monster out of every planet and monster it overlapped; in a dense cluster
those pushes stacked, so the Serpent's body sat 8 units aside and 17 units above its spot, and whenever planets entered or left the near
set the push changed and the monster lurched (131 of 400 frames moved it more than 0.15 of the screen). Now the push is capped at about
one body length and eases in slowly, and the Kraken Egg Clutch, Petrified Sentinel and Rock Eaters hold their spot like event units:
no swim, no shove, only a slow bob and sway."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 817;", "const GAME_V = 818;")
rep('const evStay = !!(MIM_BOSS[it.id] || CNT_M[it.mon] || CRC_M[it.mon] || it.mon === "mimic");',
    'const evStay = !!(MIM_BOSS[it.id] || CNT_M[it.mon] || CRC_M[it.mon] || it.mon === "mimic" || MON_STILL.has(it.mon)); /* v818 the egg clutch, the Sentinel and the Rock Eaters float where they are */')
rep("const OBV = { x: 0, y: 0, z: 0 }, OBV2 = { x: 0, y: 0, z: 0 };",
    'const OBV = { x: 0, y: 0, z: 0 }, OBV2 = { x: 0, y: 0, z: 0 }, MON_STILL = new Set(["kegg", "sent", "reat"]);')
# the shove: capped near one body length and eased in over about a second, so a crowd can neither fling a monster nor snap it
rep("P = obPush(W.obG, x, y, z, rM, OBV, null, .35), k = o.cl ? 0 : 1, f = 1 - Math.pow(.8, W.dtk || 1);",
    "P = obPush(W.obG, x, y, z, rM, OBV, null, .35), k = o.cl ? 0 : 1, f = 1 - Math.pow(.965, W.dtk || 1); { const pl = Math.hypot(P.x, P.y, P.z), cap = Math.max(1.2, rM * .9); if (pl > cap) { const c = cap / pl; P.x *= c; P.y *= c; P.z *= c; } } /* v818 */")
open(p, "w", encoding="utf-8").write(s); print("ok")
