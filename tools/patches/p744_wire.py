"""v744: the Resurrection War's live finale, Extinction Protocol (phases 1-6), its map battle, cinematics, rewards and Archive records."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
fin = open(os.path.join(D, "p744_fin.js"), encoding="utf-8").read(); i = fin.index("const CNT_FMIN"); data, rest = fin[:i].strip(), fin[i:].strip()
arch = open(os.path.join(D, "p744_arch.js"), encoding="utf-8").read().strip()
rep("const GAME_V = 743;", "const GAME_V = 744;")
rep("\n/* the clock: stage 1-7 in a run, 0 before, 8 after;", "\n" + data + "\n/* the clock: stage 1-7 in a run, 0 before, 8 after;")
rep("CRC_KRAK, CNT_NET, CNT_PATS, CNT_PLATS, CRC_BOSSES)", "CRC_KRAK, CNT_NET, [CNT_PX], CNT_PATS, CNT_PLATS, CRC_BOSSES)")
rep("function cntHid(x, T) { const B = CNT_BOSS[x.id]; if (B) {", "function cntHid(x, T) { const B = CNT_BOSS[x.id]; if (B && B.cnt === \"prime\") return !cntFinOn(T); /* v744 */ if (B) {")
rep("function cntBossOn(B, T) { if (!cntOn(T)) return false;", "function cntBossOn(B, T) { if (B.cnt === \"prime\") return cntFinOn(T); /* v744 */ if (!cntOn(T)) return false;")
rep("function cntBossInfo(x, T) { const B = CNT_BOSS[x.id],", "function cntBossInfo(x, T) { if (CNT_BOSS[x.id].cnt === \"prime\") return cntFinInfo(x, T); /* v744 */ const B = CNT_BOSS[x.id],")
rep("async function cntBossResolve(f) { const B = CNT_BOSS[f.xid],", "async function cntBossResolve(f) { if (CNT_BOSS[f.xid] && CNT_BOSS[f.xid].cnt === \"prime\") return cntFinResolve(f); /* v744 */ const B = CNT_BOSS[f.xid],")
rep("    const f = sendFleet(x, n, \"pirate\", MIM_BOSS[x.id] && MIM_BOSS[x.id].om === 1 ? { xid: x.id, omT: S.moTgt || \"core\" } : { xid: x.id });",
    "    if (x.id === \"kx0\" && !cntFinCanSend(now())) return toast(\"The battle for the Prime Ark isn't open right now.\", \"warn\"); /* v744 */\n    const f = sendFleet(x, n, \"pirate\", MIM_BOSS[x.id] && MIM_BOSS[x.id].om === 1 ? { xid: x.id, omT: S.moTgt || \"core\" } : x.id === \"kx0\" ? { xid: x.id, cntT: S.cntTgt || \"\", warp: 1, arrive: now() + cntFinTravel(), tt: cntFinTravel() } : { xid: x.id });")
rep("  try { cntMapTick(W, t, T); } catch (e) { mapErr(e); } /* v740 */", "  try { cntMapTick(W, t, T); } catch (e) { mapErr(e); } /* v740 */\n  try { cntFinTick(W, t, T); } catch (e) { mapErr(e); } /* v744 */")
rep("it.mon === \"nexus\" ? 1.5 : 1.8)); } /* v665 the Alphas and Nexuses loom */", "it.mon === \"nexus\" ? 1.5 : 1.8)); if (it.cnt === \"prime\") o.body.scale.setScalar((.6 + it.lvl * .0082) * it.sc); } /* v665 the Alphas and Nexuses loom; v744 the Prime Ark */")
rep("if (!down || inClash) monAvoid(W, o, q); /* v619 round planets and other monsters */ o.body.visible = !down || inClash;", "if ((!down || inClash) && it.cnt !== \"prime\") monAvoid(W, o, q); /* v619 round planets and other monsters */ o.body.visible = !down || inClash; if (it.cnt === \"prime\") try { cntPrimePose(o, it, t, T); } catch (e) {} /* v744 */")
rep("function cntBossForce(x, T) { T = T || now(); const B = CNT_BOSS[x.id],", "function cntBossForce(x, T) { T = T || now(); if (CNT_BOSS[x.id].cnt === \"prime\") return cntFinForce(T); /* v744 */ const B = CNT_BOSS[x.id],")
rep("</button></div>${CRC_M[x.mon] ? (CRC_ART[x.mon] ?", "</button></div>${CNT_M[x.mon] ? cntHeadArt(x) : CRC_M[x.mon] ? (CRC_ART[x.mon] ?")  # v744 the Continuum's targets showed a broken image
# War Command: the finale card, and the owner's previews of stage 7 and of the finale itself
rep("<div class=\"mimwks cntwks\">${stg}</div>${find}", "<div class=\"mimwks cntwks\">${stg}</div>${cntFinHub(T)}${find}")
rep("<div>${[0, 1, 2, 3, 4, 5, 6].map(k => `<button class=\"btn${((S.cntPrev || {}).s || 0) === k ? \" pri\" : \"\"}\" data-act=\"cntPrev\" data-s=\"${k}\">${k ? \"Stage \" + k : \"Off\"}</button>`).join(\"\")}</div>",
    "<div>${[0, 1, 2, 3, 4, 5, 6, 7].map(k => `<button class=\"btn${((S.cntPrev || {}).s || 0) === k && !(S.cntPrev || {}).fin ? \" pri\" : \"\"}\" data-act=\"cntPrev\" data-s=\"${k}\">${k ? \"Stage \" + k : \"Off\"}</button>`).join(\"\")}<button class=\"btn${(S.cntPrev || {}).fin ? \" pri\" : \"\"}\" data-act=\"cntFinPrev\">Finale now ×4</button></div>")
rep("[1, 2, 3, 4, 5, 6].map(s => b(\"cntLabStage\", String(s), \"S\" + s)).join(\"\") + b(\"cntLabStage\", \"0\", \"Off\")", "[1, 2, 3, 4, 5, 6, 7].map(s => b(\"cntLabStage\", String(s), \"S\" + s)).join(\"\") + b(\"cntFinPrev\", \"\", \"Finale ×4\") + b(\"cntLabStage\", \"0\", \"Off\")")
# the rest of the finale, and the Continuum's Archive records and Advisor lines, before the hulls
rep("\n/* ---------- the Continuum's hulls:", "\n" + arch + "\n" + rest + "\n/* ---------- the Continuum's hulls:")
# Archive unlocks on the way: decrypting a signal finds the first record, scanning a relay the second, an Ark's death completes it
rep("if (x.mon === \"cnpat\" && cntLive(x, T)) { M.sv[key] = 1; W.sig++; dirty();", "if (x.mon === \"cnpat\" && cntLive(x, T)) { M.sv[key] = 1; W.sig++; dirty(); try { archUnlock(\"cn_cont\", W.sig >= 2 ? 2 : 1, true); } catch (e) {}")
rep("else if (x.mon === \"cnrelay\" && s >= 3) { M.sv[key] = 1; W.scan++; dirty();", "else if (x.mon === \"cnrelay\" && s >= 3) { M.sv[key] = 1; W.scan++; dirty(); try { archUnlock(\"cn_ark\", 1, true); } catch (e) {}")
rep("S.medals = S.medals || {}; S.medals.ark = (S.medals.ark || 0) + 1; cntGrant(r, `${nm} destroyed`);", "S.medals = S.medals || {}; S.medals.ark = (S.medals.ark || 0) + 1; cntGrant(r, `${nm} destroyed`); try { archUnlock(\"cn_ark\", 2, true); } catch (e) {}")
# actions
rep("  cntFind: d => {", """  cntTgt: d => { S.cntTgt = d.t; renderSheet(); }, /* v744 */
  cntWatch: () => cntWatch(),
  cntFinal: () => cntFinal(), cntCineR: d => cntCine(d.k || "arr"),
  cntFinPrev: () => { if (!ownerFree() && !duelOwner()) return; S.cntPrev = { s: 7, at: now(), fin: now() + 20e3, fs: 4 }; CNTC = {}; const M = cntS(); M.cine = {}; delete M.got.fin; delete M.finEnd; dirty(); toast("Previewing Extinction Protocol at ×4: the gateway opens in 20 seconds (this device only).", "win"); renderSheet(); },
  cntFind: d => {""")
CSS = open(os.path.join(D, "p744.css"), encoding="utf-8").read().replace("\n", "")  # the head is one line
i = s.index("</style>"); s = s[:i] + CSS + s[i:]
open(p, "w", encoding="utf-8").write(s)
print("ok")
