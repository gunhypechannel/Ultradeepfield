# v387: Super Boss Hunt, a weekly event in the Events tab built on the world bosses. A live board shows every boss's hull, who is
# hitting it right now and your own damage; a live feed lists the hits as they land; your Hunt points (hull you tore off, weighted per
# boss) unlock milestone rewards with forge materials; a weekly ranking. Every attack on a boss also drops forge materials.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:90]); t = t.replace(a, b)

blk = r'''/* ---------- v387 Super Boss Hunt: the world bosses as a weekly event, tracked live ---------- */
const SB_W = k => k === "ovl" || k === "dev" ? 3 : k === "war" ? 2 : 1; // Hunt points per hull section (2.5%) torn off
const SB_MILE = [[1, { shards: 2, mats: [["low", 2, 2]] }], [10, { shards: 5, mats: [["void", 3, 1], ["low", 3, 2]] }], [30, { shards: 10, item: "mb4", mats: [["cube", 4, 1]] }],
  [60, { shards: 20, mats: [["void", 5, 1], ["cube", 5, 1]] }], [120, { shards: 35, vip: 200, mats: [["void", 6, 1], ["cube", 5, 1]] }]];
const sbPts = (st, uid) => { let n = 0; for (const k in WB) n += ((st.dmg[k] || {})[uid] || 0) * SB_W(k); return n; };
function sbBoard(st) { const u = new Set(); for (const k in WB) for (const id in (st.dmg[k] || {})) u.add(id); return [...u].map(id => ({ id, pts: sbPts(st, id), me: id === G.me })).sort((a, b) => b.pts - a.pts); }
function sbMine(T = now()) { const st = wbState(T); S.sb = S.sb && typeof S.sb === "object" ? S.sb : { cyc: st.cyc, mile: [] };
  if (S.sb.cyc !== st.cyc) { const last = S.sb; // a new week: anything reached last week and not claimed is paid out now
    if (last.pts) { let got = 0; SB_MILE.forEach(([need, rw], i) => { if (last.pts >= need && !(last.mile || []).includes(i)) { grantRw(rw, "Super Boss Hunt"); got++; } }); if (got) note(`Super Boss Hunt: ${got} unclaimed milestone reward${got > 1 ? "s" : ""} from last week added to your stores.`, "win"); }
    S.sb = { cyc: st.cyc, mile: [] }; dirty(); }
  const pts = sbPts(st, G.me); if (pts !== S.sb.pts) { S.sb.pts = pts; dirty(); } return { st, pts, sb: S.sb }; }
const sbReady = () => { try { const { pts, sb } = sbMine(); return SB_MILE.filter(([need], i) => pts >= need && !sb.mile.includes(i)).length; } catch (e) { return 0; } };
/* the live feed: every hit the shared record reveals, newest first */
G.wbFeed = []; G.wbHitAt = {};
function sbFeedAdd(prev, st) { if (!prev || prev.cyc !== st.cyc) return; for (const k in WB) { const d0 = prev.dmg[k] || {}, d1 = st.dmg[k] || {};
    for (const id in d1) { const dd = (d1[id] || 0) - (d0[id] || 0); if (dd <= 0) continue; G.wbHitAt[k] = Date.now(); G.wbFeed.unshift({ t: Date.now(), id, k, pc: Math.round(dd / WB_SEG * 100), kill: !(st.hp[k] > 0) && prev.hp[k] > 0 }); } }
  G.wbFeed.length = Math.min(G.wbFeed.length, 12); }
let SB_ART = null, SB_ART_GO = 0;
function sbArt() { if (SB_ART || SB_ART_GO || typeof BOSS3D === "undefined" || battle) return SB_ART; SB_ART_GO = 1; // the banner: the Overlord, rendered once from its model
  setTimeout(() => { try { const c = wbArt("ovl", 760, 380, 5200, null); if (c) SB_ART = c.toDataURL("image/webp", .86); } catch (e) {} wbArtFree(); if (SB_ART) softRender(); }, 80); return null; }
function sbBanner(T) { const st = wbState(T), end = wbEnd(st.cyc), up = ["ovl", "dev", "war"].filter(k => st.hp[k] > 0).length, art = sbArt();
  return `<div class="evban ev-sboss sbban">${art ? `<img src="${art}" alt="The Pyramid Overlord">` : ""}<div class="sbtop"><span class="vlive on">● LIVE</span><b>Super Boss Hunt</b><small>${up ? `${up} of 3 world bosses still standing` : "Every world boss has fallen this week"}</small></div>
    <span class="evend">Bosses return in: <b data-end="${end}">${ftime(end - T)}</b></span></div>`; }
function sbOverview(T) { const { st, pts, sb } = sbMine(T), me = Date.now();
  const row = k => { const D = WB[k], hp = st.hp[k] | 0, pc = Math.round(hp / WB_SEG * 100), my = ((st.dmg[k] || {})[G.me] || 0), hot = me - (G.wbHitAt[k] || 0) < 90e3;
    return `<div class="sbrow${hp ? "" : " down"}${hot ? " hot" : ""}"><div class="sbn"><b style="color:${D.col}">${D.ic} ${esc(D.n)}</b><span class="sbst">${hp ? (hot ? "⚔ UNDER ATTACK" : "ALIVE") : "DEFEATED"}</span></div>
      <div class="wbbar"><i style="width:${pc}%;background:${D.col}"></i></div><div class="sbm"><span>${hp ? `${pc}% hull` : "Down"}${k === "ovl" && hp ? ` · shield ${wbCons(T)}/4` : ""}</span><span>You: ${my ? Math.round(my / WB_SEG * 100) + "%" : "—"}</span></div>
      ${hp ? `<div class="sbb"><button class="btn sm amber" data-act="wboss" data-id="${k}">⚔ Hunt</button><button class="btn sm ghost" data-act="cineObj" data-id="wb_${k}">◉ Scan</button></div>` : ""}</div>`; };
  const cons = [0, 1, 2, 3].map(i => { const c = "c" + i, hp = st.hp[c] | 0; return `<button class="sbcon${hp ? "" : " down"}" data-act="wboss" data-id="${c}" aria-label="Energy Conduit ${"ABCD"[i]}">◆ ${"ABCD"[i]} <small>${hp ? Math.round(hp / WB_SEG * 100) + "%" : "✕"}</small></button>`; }).join("");
  const feed = G.wbFeed.filter(f => me - f.t < 30 * 60e3).slice(0, 6).map(f => `<li><span>${esc(f.id === G.me ? "You" : nameOf(f.id))}</span> ${f.kill ? "destroyed" : `tore ${f.pc}% off`} the ${esc(WB[f.k].n)} <i>${ftime(me - f.t)} ago</i></li>`).join("");
  return `<div class="evinfo sbinfo"><h4>Live board</h4>${["ovl", "dev", "war"].map(row).join("")}<div class="sbcons"><span>Overlord's conduits</span>${cons}</div>
    ${feed ? `<h4>Live feed</h4><ul class="sbfeed">${feed}</ul>` : ""}
    <h4>Your Hunt points</h4><p><b class="evscore">${fmt(pts)}</b> · ${pts ? "every 2.5% of hull you destroy scores 3 on the Overlord or Devourer, 2 on the Warden, 1 on a conduit" : "attack any world boss to start scoring"}</p>
    <h4>Milestone rewards</h4>${SB_MILE.map(([need, rw], m) => `<div class="tier"><span class="tn">${fmt(need)} pts</span><span class="trw">${rwText(rw)}</span>${sb.mile.includes(m) ? '<span class="pill ok">Claimed</span>' : pts >= need ? '<span class="pill amb">Ready</span>' : '<span class="pill wait">—</span>'}</div>`).join("")}
    <h4>Event Rules</h4><p>The Pyramid Overlord, the Orbital Devourer and the Void Warden return every Monday at 18:00 UTC. Every attack, win or lose, pays a bounty for the hull it destroys and drops forge materials. Hunt points add up all week. When a boss falls, everyone who damaged it claims a share of its spoils, and milestones you reach but don't claim are paid out when the bosses return.</p></div>`; }
function sbRanking(T) { const st = wbState(T), rows = sbBoard(st), mi = rows.findIndex(r => r.me), show = rows.slice(0, 50); if (mi >= 50) show.push(rows[mi]);
  return `<div class="evrank"><div class="evrh"><span>Rank</span><span>Commander</span><span>Hunt points</span></div>${show.map(r => { const pos = rows.indexOf(r) + 1; return `<div class="evrr${r.me ? " me" : ""}"><span>${pos <= 3 ? ["🥇", "🥈", "🥉"][pos - 1] : pos + "."}</span><span>${esc(r.me ? (G.myName || "You") + " (you)" : nameOf(r.id))}</span><span>${fmt(r.pts)}</span></div>`; }).join("") || '<p class="note" style="padding:10px">Nobody has hit a world boss this week yet. Be the first.</p>'}</div>`; }
'''
rep("function shEvents() {", blk + "function shEvents() {")
rep('const EVS = [["gw", "Galaxy War", "⚔"],', 'const EVS = [["sboss", "Super Boss Hunt", "☠"], ["gw", "Galaxy War", "⚔"],')
rep('const T = now(), tab = sheet.evTab === "rk" ? "rk" : "ov", k = EVS.some(e => e[0] === sheet.ev) ? sheet.ev : "gw";', 'const T = now(), tab = sheet.evTab === "rk" ? "rk" : "ov", k = EVS.some(e => e[0] === sheet.ev) ? sheet.ev : "sboss";')
rep('  else if (k === "builder" || k === "online" || k === "lvlb") body = bonusBody(k, T);',
    '''  else if (k === "sboss") { body = tab === "ov" ? sbOverview(T) : sbRanking(T); const n = sbReady(); claim = `<button class="btn ${n ? "amber" : "ghost"} evclaim" data-act="sbClaim" ${n ? "" : "disabled"}>${n ? `Claim · ${n} milestone${n > 1 ? "s" : ""}` : "Claim"}</button>`; }
  else if (k === "builder" || k === "online" || k === "lvlb") body = bonusBody(k, T);''')
rep('function evCount(k) { if (!S) return 0; try {', 'function evCount(k) { if (!S) return 0; try {\n  if (k === "sboss") return sbReady();')
rep('function evBanner(k, T) {', 'function evBanner(k, T) { if (k === "sboss") return sbBanner(T);')
rep("  cineObj: d => cineObjStart(d.id),", """  cineObj: d => cineObjStart(d.id),
  sbClaim: () => act(() => { const { pts, sb } = sbMine(); let n = 0; SB_MILE.forEach(([need, rw], i) => { if (pts >= need && !sb.mile.includes(i)) { sb.mile.push(i); grantRw(rw, "Super Boss Hunt"); n++; } }); if (n) toast(`Claimed ${n} Super Boss Hunt milestone${n > 1 ? "s" : ""}.`); }),""")
# the live feed and the "under attack" marks come from the shared record (and our own fights)
rep("wbNews(WB_PREV, st); WB_PREV = st;", "wbNews(WB_PREV, st); sbFeedAdd(WB_PREV, st); WB_PREV = st;")
rep("if (G.mode !== \"online\") { const pv = jcopy(cur); pv.hp[key] = n0; wbNews(pv, cur); } home();",
    "{ const pv = jcopy(cur); pv.hp[key] = n0; if (pv.dmg[key]) pv.dmg[key][G.me] = ((pv.dmg[key][G.me] || 0) - seg); if (G.mode !== \"online\") wbNews(pv, cur); sbFeedAdd(pv, cur); WB_PREV = wbNorm(jcopy(cur), cur.cyc); } home();")
# every attack drops forge materials: the boss's own kind, more for more hull torn off
rep("    if (!left) { bump(\"bosses\"); note(`We brought down the ${D.n}!",
    """    { const mk = key === "dev" ? "bio" : key === "war" ? "void" : D.con != null ? "crystal" : "alloy", rolls = [[mk, seg >= 4 ? 3 : 2, 1 + Math.floor(seg / 6)]]; if (seg >= 8) rolls.push(["void", 4, 1]); if (!left) rolls.push([D.con != null ? "cube" : "void", D.con != null ? 4 : 5, 1]);
      rep.mats = fsDrop(lootRoll(rolls), `the ${D.n}`, { nocap: 1 }); } /* v387: every fight pays materials */
    if (!left) { bump("bosses"); note(`We brought down the ${D.n}!""")
rep('  events: () => openSheet({ type: "events" }),', '  events: d => openSheet({ type: "events", ev: d && d.ev ? d.ev : undefined }),')
# the World bosses rows in Finder › Map Events point at the event too
rep('      <h2 class="sec">World bosses</h2><div class="list">', '      <h2 class="sec">World bosses</h2><button class="btn ghost wide" data-act="events" data-ev="sboss" style="margin:0 0 8px">☠ Super Boss Hunt · live board, points and rewards</button><div class="list">')
i = t.index('</style>', t.index('.fshero{'))
t = t[:i] + '''
/* v387 Super Boss Hunt */
.sbban{position:relative;min-height:150px;overflow:hidden;background:radial-gradient(120% 90% at 70% 40%,rgba(155,80,255,.35),rgba(6,4,14,.95) 70%)}.sbban img{position:absolute;right:-4%;top:50%;transform:translateY(-50%);width:78%;max-width:none;opacity:.95;pointer-events:none}
.sbtop{position:relative;display:flex;flex-direction:column;gap:3px;padding:12px 14px;max-width:62%}.sbtop b{font-size:20px;letter-spacing:.04em;text-shadow:0 0 14px rgba(197,139,255,.7)}.sbtop small{color:#cdbff0;font-size:12px}.sbban .evend{position:relative}
.sbrow{padding:9px 10px;margin:6px 0;border-radius:10px;border:1px solid rgba(201,166,255,.2);background:rgba(201,166,255,.05);display:flex;flex-direction:column;gap:6px}.sbrow.down{opacity:.55}
.sbrow.hot{border-color:#ff5d7a;box-shadow:0 0 14px rgba(255,77,106,.3)}.sbn{display:flex;justify-content:space-between;align-items:center;gap:8px}.sbst{font:700 10px/1 ui-monospace,monospace;letter-spacing:.1em;color:#9fe0b0}.sbrow.hot .sbst{color:#ff6a82;animation:fbHot 1.2s ease-in-out infinite}.sbrow.down .sbst{color:#8b8fa3}
.sbm{display:flex;justify-content:space-between;font-size:12px;color:#c9d4ea;font-variant-numeric:tabular-nums}.sbb{display:flex;gap:6px}.sbb .btn{flex:1}
.sbcons{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:4px 0 6px;font-size:12px;color:#a9b4cc}.sbcons span{flex-basis:100%}.sbcon{padding:5px 9px;border-radius:999px;border:1px solid rgba(217,160,255,.45);background:rgba(217,160,255,.08);color:#ecd9ff;font:600 12px/1 inherit;cursor:pointer}.sbcon.down{opacity:.45;text-decoration:line-through}
.sbfeed{list-style:none;margin:4px 0 8px;padding:0;display:flex;flex-direction:column;gap:4px}.sbfeed li{font-size:12.5px;padding:5px 8px;border-radius:7px;background:rgba(255,77,106,.08)}.sbfeed li span{font-weight:700;color:#ffd0c8}.sbfeed li i{font-style:normal;color:#7f8cab;float:right}
''' + t[i:]
open(p, "w").write(t); print("ok")
