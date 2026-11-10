# v389: the owner's concept art on the event pages. Super Boss Hunt and Titan Hunt banners are strips of the bosses' concept art,
# and every row on the live board has the boss's portrait. The art is embedded (small WebP data URIs built from
# assets/bosses/*/reference/), so it shows on the website and in the claude.ai artifact alike.
import json, sys
p = "docs/index.html"; t = open(p).read(); A = json.load(open(sys.argv[1]))
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("const SB_G = {", "const BOSS_ART = " + json.dumps(A) + "; // v389 concept art: banners g1/g2, portraits per boss\nconst SB_G = {")
rep("""function sbBanner(T, g = 1) { const E = SB_G[g], st = wbState(T), end = g === 2 ? wbEnd2(st.cyc2) : wbEnd(st.cyc), main = wbMain(g), up = main.filter(k => st.hp[k] > 0).length, art = sbArt(g);
  return `<div class="evban ev-sboss sbban${g === 2 ? " sb2" : ""}">${art ? `<img src="${art}" alt="${E.artN}">` : ""}""",
"""function sbBanner(T, g = 1) { const E = SB_G[g], st = wbState(T), end = g === 2 ? wbEnd2(st.cyc2) : wbEnd(st.cyc), main = wbMain(g), up = main.filter(k => st.hp[k] > 0).length, art = BOSS_ART["g" + g];
  return `<div class="evban ev-sboss sbban art${g === 2 ? " sb2" : ""}"><img src="${art}" alt="${main.map(k => WB[k].n).join(", ")}">""")
rep("""<div class="sbn"><b style="color:${D.col}">${D.ic} ${esc(D.n)}</b><span class="sbst">""", """<div class="sbn"><span class="sbnl"><img class="sbth" src="${BOSS_ART[k]}" alt="" style="border-color:${D.col}"><b style="color:${D.col}">${D.ic} ${esc(D.n)}</b></span><span class="sbst">""")
rep("""<button class="sbcon${hp ? "" : " down"}" data-act="wboss" data-id="${c}" aria-label="Energy Conduit ${"ABCD"[i]}">◆""", """<button class="sbcon${hp ? "" : " down"}" data-act="wboss" data-id="${c}" aria-label="Energy Conduit ${"ABCD"[i]}"><img src="${BOSS_ART.con}" alt="">""")
i = t.index('</style>', t.index('.fshero{'))
t = t[:i] + """
/* v389 concept art on the event pages */
.sbban.art{min-height:168px}.sbban.art img{left:0;right:auto;top:0;width:100%;height:100%;object-fit:cover;transform:none;opacity:.92}
.sbban.art::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(6,4,14,.55) 0,rgba(6,4,14,.05) 38%,rgba(6,4,14,.1) 62%,rgba(6,4,14,.85) 100%)}
.sbban.art .sbtop,.sbban.art .evend{position:relative;z-index:1}.sbban.art .sbtop b,.sbban.art .sbtop small{text-shadow:0 1px 4px #000}
.sbnl{display:flex;align-items:center;gap:9px;min-width:0}.sbth{width:44px;height:44px;flex:none;border-radius:9px;object-fit:cover;border:1px solid;box-shadow:0 0 10px rgba(0,0,0,.5)}.sbrow.down .sbth{filter:grayscale(1)}
.sbcon img{width:18px;height:18px;border-radius:4px;object-fit:cover;vertical-align:-4px;margin-right:4px}
""" + t[i:]
open(p, "w").write(t); print("ok")
