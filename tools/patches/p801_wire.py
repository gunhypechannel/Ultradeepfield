"""v801: the Interstice (behind the owner switch "aet"): its structures and neutral defenders (Gateway Anchors, Dimensional Fortresses,
Neural Transit Relays, Ancient Resource Fields, the Central Nexus and its four pylons, Sentinel wings, the Sleeping Intelligence),
missions from your arrival gate (attack, hold, gather, scout), the bonuses of what you hold, fragments and materials in the hold."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
C = open(os.path.join(D, "p801_aet.js"), encoding="utf-8").read()
rep("const GAME_V = 800;", "const GAME_V = 801;")
rep("\nconst PIRATES = PIRATES_ALL.filter(", "\n" + C + "\nconst PIRATES = PIRATES_ALL.filter(")
rep("CNT_PLATS, CRC_BOSSES).filter(x => !monGone(x));", "CNT_PLATS, CRC_BOSSES, AET_TGT).filter(x => !monGone(x));")
rep("let html = ({ aet: shAet,", "let html = ({ aet: shAet, aettgt: shAetTgt,")
# realm targets are drawn by the realm, never by the galaxy's markers and models
rep("CRC_M[it.mon] && crcHid(it, T) || CNT_M[it.mon] && cntHid(it, T))); A.aCol[j + 3]", "CRC_M[it.mon] && crcHid(it, T) || CNT_M[it.mon] && cntHid(it, T) || !!it.aetR)); A.aCol[j + 3]")
rep("CRC_M[it.mon] && crcHid(it, T) || CNT_M[it.mon] && cntHid(it, T))); /* v430 */", "CRC_M[it.mon] && crcHid(it, T) || CNT_M[it.mon] && cntHid(it, T) || !!it.aetR)); /* v430 */")
rep("function isElite(x) { return !!x && ", "function isElite(x) { return !!x && !x.aetR && ")
rep("CNT_M[x.mon] ? cntForce(x) :", "x.aetR ? aetForce(x) : CNT_M[x.mon] ? cntForce(x) :")
rep("if (MON[k] || k === \"snest\" || MIM_U[k] || CRC_U[k] || CNT_U[k]) { const s = .25", "if (MON[k] || k === \"snest\" || MIM_U[k] || CRC_U[k] || CNT_U[k] || AET_U[k]) { const s = .25")
rep("if (CNT_M[k]) return buildCnt(CNT_M[k]); /* v740 */", "if (CNT_M[k]) return buildCnt(CNT_M[k]); /* v740 */\n  if (AET_M[k]) return buildAet(AET_M[k]); /* v801 */")
rep("if (CNT_U[k]) return buildCnt(k); /* v740 */", "if (CNT_U[k]) return buildCnt(k); /* v740 */\n  if (AET_U[k]) return buildAet(k); /* v801 */")
rep("Object.assign(MIM_HULL, { cnint", "Object.assign(CPROF, { aetDrone: [\"interceptor\", \"laser\", .08, .25, 8, 0], aetWeaver: [\"frigate\", \"ion\", .14, .12, 5, 1], aetSentinel: [\"cruiser\", \"beam\", .22, .06, 4, 2], aetGuard: [\"battleship\", \"ion\", .28, .02, 2.5, 3],\n  aetWarden: [\"battleship\", \"beam\", .32, .02, 2.4, 3], aetPylon: [\"station\", \"ion\", .4, 0, 0, 4], aetNexus: [\"station\", \"beam\", .42, 0, 0, 6], aetIntel: [\"titan\", \"plasma\", .36, 0, 1, 6] }); /* v801 */\nObject.assign(MIM_HULL, { aetDrone: .8, aetWeaver: 1.1, aetSentinel: 1.6, aetGuard: 2, aetWarden: 2.6, aetPylon: 2.4, aetNexus: 4.4, aetIntel: 4 }); Object.assign(BOSS_GLOW, { aetNexus: \"191,255,244\", aetIntel: \"208,64,74\", aetPylon: \"159,246,234\" }); /* v801 */\nObject.assign(MIM_HULL, { cnint")
# fleets from a realm's arrival gate: their own arrival, gathering and homecoming; their home is the gate
rep("if (f.phase === \"out\") ev.push({ at: f.arrive, run: () => f.rj", "if (f.phase === \"out\") ev.push({ at: f.arrive, run: () => f.aet ? aetArrive(f) : f.rj")
rep("else if (f.phase === \"gather\") ev.push({ at: f.gend, run: () => gatherEnd(f) });", "else if (f.phase === \"gather\") ev.push({ at: f.gend, run: () => f.aet ? aetGatherEnd(f) : gatherEnd(f) });")
rep("else if (f.phase === \"back\") ev.push({ at: f.back, run: () => homecoming(f) });", "else if (f.phase === \"back\") ev.push({ at: f.back, run: () => f.aet ? aetHome(f) : homecoming(f) });")
rep("function fleetHome(f) { ", "function fleetHome(f) { if (f.aet) return aetBaseOf(f); /* v801 */ ")
rep("function originAvail() { ", "function originAvail() { if (sheet && sheet.type === \"aettgt\") { const x = aetS().tx[sheet.tx]; return x ? aetGateAvail(x) : {}; } /* v801 */ ")
open(p, "w", encoding="utf-8").write(s)
print("ok")
