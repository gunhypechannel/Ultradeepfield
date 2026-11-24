"""v746: joint strikes on the resurrection network (relays, Arks, commanders, the Eternal Commander, the Prime Ark)."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__))
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 745;", "const GAME_V = 746;")
js = open(os.path.join(D, "p746_joint.js"), encoding="utf-8").read().strip()
rep("\n/* ---------- the Continuum's hulls:", "\n" + js + "\n/* ---------- the Continuum's hulls:")
# the launch screen offers a joint strike on the network too
rep("${(x.boss || x.mon) && !MIM_BOSS[x.id] && G.mode === \"online\" ? `<button class=\"toggle${sheet.joint ? \" on\" : \"\"}\" data-act=\"jointToggle\">",
    "${(x.boss || x.mon) && (!MIM_BOSS[x.id] || CNT_BOSS[x.id]) && G.mode === \"online\" ? `<button class=\"toggle${sheet.joint ? \" on\" : \"\"}\" data-act=\"jointToggle\">")
rep("    if (sheet && sheet.joint && (x.boss || x.mon) && !MIM_BOSS[x.id]) {",
    "    if (sheet && sheet.joint && CNT_BOSS[x.id]) { const T = now(), why = x.id === \"kx0\" ? (cntFinCanSend(T) ? null : \"The battle for the Prime Ark isn't open right now.\") : cntBlock(CNT_BOSS[x.id], cntStC(T), T); if (why) return toast(why, \"warn\"); } /* v746 */\n    if (sheet && sheet.joint && (x.boss || x.mon) && (!MIM_BOSS[x.id] || CNT_BOSS[x.id])) {")
rep("const pirate = tgt.kind === \"pirate\", launch = T + mins * 60000, march = travelMs(h, tgt, n, S.r, spdPct());",
    "const pirate = tgt.kind === \"pirate\", launch = T + mins * 60000, march = tgt.id === \"kx0\" ? cntFinTravel() : travelMs(h, tgt, n, S.r, spdPct()); /* v746 the staging gate */")
# teamwork in the network fights and the finale
rep("const Z = cntBossSet(B, cur, at), n0 = Math.max(1, Z.n0);\n    const mkA = () => { const st = stacksOf(f.n, techVs(x), G.me); for (const s of st) { s.atk *= Z.mods.pA; s.sh *= Z.mods.pS; } return st; };",
    "const Z = cntBossSet(B, cur, at), n0 = Math.max(1, Z.n0);\n    const tw = cntTeam(f), mkA = () => { const st = stacksOf(f.n, techVs(x), G.me); for (const s of st) { s.atk *= Z.mods.pA * tw; s.sh *= Z.mods.pS * tw; } return st; };")
rep("const Z = cntFinSet(o, tg, fe), mine0 = Object.assign({}, f.n), bonus = 1 + Math.min(.5, .05 * o.esc);",
    "const Z = cntFinSet(o, tg, fe), mine0 = Object.assign({}, f.n), bonus = (1 + Math.min(.5, .05 * o.esc)) * cntTeam(f);")
rep("for (const q of s) { q.atk *= Z.mods.pA * bonus; q.sh *= Z.mods.pS; } return s; };", "for (const q of s) { q.atk *= Z.mods.pA * bonus; q.sh *= Z.mods.pS * cntTeam(f); } return s; };")
# War Command lists the open strikes
rep("${find}${net}${obj}", "${find}${net}${s >= 3 && s <= 7 ? cntStrikesHTML(T) : \"\"}${obj}")
CSS = ".cntjs{display:flex;align-items:center;gap:10px;padding:8px 10px;margin:6px 0;border:1px solid rgba(255,51,70,.3);border-radius:10px;background:rgba(30,6,10,.45)}.cntjs>div{flex:1;min-width:0}.cntjs small{display:block;color:var(--dim,#9aa4b2)}"
i = s.index("</style>"); s = s[:i] + CSS + s[i:]
open(p, "w", encoding="utf-8").write(s)
print("ok")
