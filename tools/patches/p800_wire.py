"""v800: the Aetherion Gateway, stage 1 (behind the owner switch "aet"): the four Aetherion saga seasons placed after the first
ten-season year (calendar and cosmetics sets 15-18), the gateway beside Nhalis on the map, the Aetherion Command Center (Gateway,
Realms, Nexus War, Deployment, Rewards, More), the Dimensional Atlas, fleet crossings recorded in the server's ledger (aet_tx), the
realm view (the Interstice's scenery), the crossing effect. Owner preview of every saga week and of the open gateway."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
A = open(os.path.join(D, "p800_aet_a.js"), encoding="utf-8").read()
B = open(os.path.join(D, "p800_aet_b.js"), encoding="utf-8").read()
CSS = open(os.path.join(D, "p800.css"), encoding="utf-8").read().replace("\n", "")
rep("const GAME_V = 799;", "const GAME_V = 800;")
# the calendar: after the ten story seasons of the first year come the four Aetherion seasons (once); then the year repeats
rep("const seaCyc = si => si < PRO ? -1 : (si - PRO) % 10, seaCos = si => si < PRO ? PRO_COS[Math.max(0, si)] : seaCyc(si);",
    "const seaCyc = si => si < PRO ? -1 : si < PRO + 10 ? si - PRO : si < PRO + 14 ? si - PRO : (si - PRO - 4) % 10, seaCos = si => si < PRO ? PRO_COS[Math.max(0, si)] : seaCyc(si) >= 10 ? seaCyc(si) + 5 : seaCyc(si); /* v800 seasons 14-17 (cycle 10-13) are the Aetherion saga, cosmetics sets 15-18 */")
rep('["Season of the Signal", "#5fe8d0", "signal", "Signal Keeper"]];',
    '["Season of the Signal", "#5fe8d0", "signal", "Signal Keeper"], ["The Continuum", "#ff3346", "signal", "Continuum Veteran"], ["The First Contamination", "#7ff0dc", "signal", "Vesper Witness"], ["The Living Station", "#5fe8d0", "signal", "Station Hunter"], ["The Planet That Awoke", "#3fd8c0", "signal", "Nhalis Survivor"], ["The First Aperture", "#9ff6ea", "signal", "Aperture Keeper"]];')
rep('"Carcinid", "Signal", "Continuum"], COS_C2 = [', '"Carcinid", "Signal", "Continuum", "Contamination", "Living Station", "Awakening", "Aperture"], COS_C2 = [')
rep('"#3fe8f0", "#d8fff6", "#5fd0ff"];', '"#3fe8f0", "#d8fff6", "#5fd0ff", "#c8fff4", "#e6fffb", "#b6f4ea", "#ffffff"];')
rep("cosNo = cx => PRO_COS.includes(cx) ? PRO_COS.indexOf(cx) + 1 : cx >= 10 ? cx - 9 : cx + 1 + PRO, cosLive = (cx, cur) => PRO_COS.includes(cx) ? cur >= PRO_COS.indexOf(cx) : cx >= 10 ? cur >= cx - 10 : cur >= PRO + cx;",
    "cosNo = cx => PRO_COS.includes(cx) ? PRO_COS.indexOf(cx) + 1 : cx >= 15 && cx <= 18 ? PRO + 10 + cx - 15 + 1 : cx >= 10 ? cx - 9 : cx + 1 + PRO, cosLive = (cx, cur) => PRO_COS.includes(cx) ? cur >= PRO_COS.indexOf(cx) : cx >= 15 && cx <= 18 ? cur >= PRO + 10 + cx - 15 : cx >= 10 ? cur >= cx - 10 : cur >= PRO + cx; /* v800 the saga sets */")
rep("const NF = SEA_FIN.length, x = seaCyc(si), L = sat ? ROTS : ROT, fin = SEA_FIN[x][sat ? 1 : 0], pf = SEA_FIN[(x + NF - 1) % NF][sat ? 1 : 0], pool",
    "const NF = SEA_FIN.length, x = seaCyc(si), L = sat ? ROTS : ROT, fin = x >= 10 ? null : SEA_FIN[x][sat ? 1 : 0], pf = x >= 10 ? (x === 10 ? SEA_FIN[NF - 1][sat ? 1 : 0] : null) : SEA_FIN[(x + NF - 1) % NF][sat ? 1 : 0], pool /* v800 the saga's finales are its own */")
rep("  const NM = { vae: \"Vaelthar, the Celestial Ruin\",", "  if (x >= 10) return typeof aetFinHTML === \"function\" ? aetFinHTML(T, x - 10) : \"\"; /* v800 */\n  const NM = { vae: \"Vaelthar, the Celestial Ruin\",")
# the code
rep("const PIRATES = PIRATES_ALL.filter(", A + "\n" + B + "\nconst PIRATES = PIRATES_ALL.filter(")
rep("let html = ({ mimic: shMimic,", "let html = ({ aet: shAet, mimic: shMimic,")
rep("const ACT = {\n", "const ACT = { ...AET_ACT,\n")
rep("  try { cntMapTick(W, t, T); } catch (e) { mapErr(e); } /* v740 */", "  try { cntMapTick(W, t, T); } catch (e) { mapErr(e); } /* v740 */\n  try { aetMapTick(W, t, T); } catch (e) { mapErr(e); } /* v800 */")
rep('  MAPPROF.mark("labels and 2D overlay");', '  try { aetOverlay(W, hits, proj, label, cp, k, T); } catch (e) {} /* v800 */\n  MAPPROF.mark("labels and 2D overlay");')
rep("  if (best && best.nexus) { openSheet({ type: \"cubepick\" }); return; }", "  if (best && best.aet) { aetTap(best.aet); return; } /* v800 */\n  if (best && best.nexus) { openSheet({ type: \"cubepick\" }); return; }")
rep("  const cineOn = !!(G3 && G3.cam && (G3.cam.cine || G3.cam.cineObj)) || !!G.judgeSim; /* v579 never over a cinematic */",
    "  const cineOn = !!(G3 && G3.cam && (G3.cam.cine || G3.cam.cineObj)) || !!G.judgeSim; /* v579 never over a cinematic */\n  if (G.aetView && view === \"galaxy\" && !sheet && !battle && !cineOn) html = aetBand(T); /* v800 inside a realm */")
rep("html = crcBand(T) || cntBand(T); /* v703 */ /* v740 */", "html = crcBand(T) || cntBand(T) || aetBand(T); /* v703 */ /* v740 */ /* v800 */")
rep("+ mimBand(T) + crcBand(T) + cntBand(T) + wheelBand();", "+ mimBand(T) + crcBand(T) + cntBand(T) + aetBand(T) + wheelBand();")
# double tap inside a realm zooms onto the realm's plane
rep("const s = -o.y / dy, gx = o.x + (V3.x - o.x) * s, gz = o.z + (V3.z - o.z) * s; if (s < 0) return;",
    "const Y0 = G.aetView ? aetRealmPos(G.aetView).y : 0, s = (Y0 - o.y) / dy, gx = o.x + (V3.x - o.x) * s, gz = o.z + (V3.z - o.z) * s; if (s < 0) return; /* v800 */")
rep("c.goal = { tx: clamp(gx, -MAP_R, MAP_R), ty: 0, tz: clamp(gz, -MAP_R, MAP_R), dist: Math.max(14, c.dist * .45) };",
    "c.goal = { tx: clamp(gx, -MAP_R, MAP_R), ty: Y0, tz: clamp(gz, -MAP_R, MAP_R), dist: Math.max(14, c.dist * .45) };")
rep("const wx = (lx * Math.cos(a) - ly * Math.sin(a)) / k, wz = (lx * Math.sin(a) + ly * Math.cos(a)) / k, cm = G3.cam; cm.follow = null;", "const wx = (lx * Math.cos(a) - ly * Math.sin(a)) / k, wz = (lx * Math.sin(a) + ly * Math.cos(a)) / k, cm = G3.cam; if (G.aetView) { G.aetView = null; softRender(); } /* v800 the minimap is the galaxy's */ cm.follow = null;")
i = s.index("</style>"); s = s[:i] + CSS + s[i:]
open(p, "w", encoding="utf-8").write(s)
# the server bridge
q = os.path.join(os.path.dirname(p), "udf-supabase.js")
if os.path.exists(q):
    u = open(q, encoding="utf-8").read()
    if "window.udfAet" not in u:
        a = "  window.udfStory = {"
        assert u.count(a) == 1
        u = u.replace(a, '''  /* v800 the Aetherion Gateway's ledger: every crossing is a server row (aet_tx), every reward claim too (aet_claim) */
  window.udfAet = {
    tx: function (op, id, p) { return need().then(function () { return run(sb.rpc("aet_tx", { p_op: op, p_txid: id, p: p || {} })); }); },
    mine: function () { return need().then(function () { return run(sb.rpc("aet_mine")); }); },
    claim: function (cid, v) { return need().then(function () { return run(sb.rpc("aet_claim", { p_cid: cid, p: v || null })); }); },
    state: function () { return need().then(function () { return run(sb.rpc("aet_state")); }); }
  };
''' + a)
        open(q, "w", encoding="utf-8").write(u)
print("ok")
