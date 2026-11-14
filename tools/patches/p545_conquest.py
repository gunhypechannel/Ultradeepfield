# v545 Alliance Conquest (owner: "Do it all", idea #6). A weekly alliance war over the map: the galaxy is cut into 48 sectors (its six
# layers × eight lanes, by each world's orbit lane a0). Every world a member of an alliance holds counts for its sector (homeworld 3,
# colony 1, +1 per 10 Commander levels of its owner); the alliance with the most weight in a sector controls it (a tie: nobody). The core
# sectors count double. The Events hub shows it as "Alliance Conquest": a live sector map in each controller's colour, the standings,
# your alliance's sectors, and the rules. When the week ends (Monday 00:00 UTC), members of every alliance that holds sectors claim ◆2 per
# point of control (max ◆40), and the top three alliances' members get a booster too (claimable during the following week; the standing
# at claim time counts).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
JS = r'''
/* ---------- v545 Alliance Conquest ---------- */
const CQ_SL = 8, cqWeek = (T = now()) => Math.floor((T - VP_BASE) / (7 * 864e5)), cqEnd = (w = cqWeek()) => VP_BASE + (w + 1) * 7 * 864e5;
const CQ_PAL = ["#ffcf5a", "#55d6e8", "#ff5ac8", "#5dff9a", "#ff8a3a", "#9a7bff", "#ff5a5a", "#c8ff5a", "#5a9aff", "#ffffff", "#ffa0d0", "#7affe0"];
const cqCol = aid => (G.cqPal && G.cqPal[aid]) || `hsl(${hash("cq" + aid) % 360} 70% 60%)`;
function cqMap() { const own = {}; for (const a of Object.values(G.alliances || {})) for (const u in a.members || {}) own[u] = a.id;
  const sec = {}; for (const p of G.list || []) { if (!p.owner || p.owner === "pirates") continue; const aid = p.owner === G.me ? S.ally : own[p.owner]; if (!aid) continue; const L = layerOf(p.r || 0), sl = Math.floor(((((p.a0 || 0) % TAU) + TAU) % TAU) / TAU * CQ_SL) % CQ_SL, k = L.n + ":" + sl;
    const pl = p.owner === G.me ? myPub() : (G.players || {})[p.owner] || {}, w = (p.kind === "home" ? 3 : 1) + Math.floor(cmdLevel(pl.score || 0) / 10); (sec[k] = sec[k] || {})[aid] = (sec[k][aid] || 0) + w; }
  const ctl = {}, pts = {}; for (const k in sec) { const e = Object.entries(sec[k]).sort((a, b) => b[1] - a[1]); if (e.length && (e.length === 1 || e[0][1] > e[1][1])) { ctl[k] = e[0][0]; pts[e[0][0]] = (pts[e[0][0]] || 0) + (+k.split(":")[0] >= 5 ? 2 : 1); } }
  const rank = Object.entries(pts).sort((a, b) => b[1] - a[1]); G.cqPal = {}; rank.forEach(([aid], i) => { if (i < CQ_PAL.length) G.cqPal[aid] = CQ_PAL[i]; }); return { sec, ctl, pts, rank }; }
function cqSvg(M) { const R = [0, 32, 55, 80, 110, 140, 172], cx = 180, cy = 180, k = 1.02, arc = (r0, r1, a0, a1) => { const p = (r, a) => `${(cx + Math.cos(a) * r * k).toFixed(1)},${(cy + Math.sin(a) * r * k).toFixed(1)}`; return `M${p(r0, a0)} L${p(r1, a0)} A${r1 * k},${r1 * k} 0 0 1 ${p(r1, a1)} L${p(r0, a1)} A${r0 * k},${r0 * k} 0 0 0 ${p(r0, a0)}Z`; };
  let out = ""; for (let ln = 1; ln <= 6; ln++) { const r1 = R[7 - ln], r0 = R[6 - ln]; for (let sl = 0; sl < CQ_SL; sl++) { const a0 = sl / CQ_SL * TAU, a1 = (sl + 1) / CQ_SL * TAU - .02, aid = M.ctl[ln + ":" + sl], mine = aid && aid === S.ally;
    out += `<path d="${arc(Math.max(r0, 6), r1 - 1.5, a0, a1)}" fill="${aid ? cqCol(aid) : "rgba(255,255,255,.04)"}" fill-opacity="${aid ? (mine ? .85 : .55) : 1}" stroke="${mine ? "#fff" : "rgba(122,244,255,.18)"}" stroke-width="${mine ? 1.6 : .6}"><title>${esc(LAYERS[ln - 1].name)} · lane ${sl + 1}${aid && G.alliances[aid] ? " · [" + esc(G.alliances[aid].tag) + "]" : " · unclaimed"}</title></path>`; } }
  return `<svg class="cqmap" viewBox="0 0 360 360" role="img" aria-label="Sector control map">${out}<circle cx="${cx}" cy="${cy}" r="6" fill="#c94ad6"/></svg>`; }
function cqBanner(T) { const M = cqMap(), top = M.rank.slice(0, 3);
  return `<div class="evban cqban">${cqSvg(M)}<div class="cqtx"><span class="vlive on">⚑ WEEK ${cqWeek(T) + 1}</span><b>Alliance Conquest</b><small>Ends in <b data-end="${cqEnd()}">${ftime(cqEnd() - T)}</b></small>
    <div class="cqleg">${top.map(([aid, p], i) => `<span><i style="background:${cqCol(aid)}"></i>${["🥇", "🥈", "🥉"][i]} [${esc((G.alliances[aid] || {}).tag || "?")}] ${p}</span>`).join("") || "<span>No sector held yet</span>"}</div></div></div>`; }
function cqBody(T, tab) { const M = cqMap(), my = S.ally && M.pts[S.ally] || 0, myR = S.ally ? M.rank.findIndex(r => r[0] === S.ally) + 1 : 0, lw = cqWeek(T) - 1, cl = S.cq === lw;
  if (tab === "rk") return `<div class="evrank"><div class="evrh"><span>Rank</span><span>Alliance</span><span>Control</span></div>${M.rank.slice(0, 50).map(([aid, p], i) => `<div class="evrr${aid === S.ally ? " me" : ""}"><span>${i < 3 ? ["🥇", "🥈", "🥉"][i] : i + 1 + "."}</span><span><i class="cqdot" style="background:${cqCol(aid)}"></i>[${esc((G.alliances[aid] || {}).tag || "?")}] ${esc((G.alliances[aid] || {}).name || "")}</span><span>${p}</span></div>`).join("") || '<p class="note" style="padding:10px">No alliance holds a sector yet.</p>'}</div>`;
  return `<div class="evinfo"><h4>Your alliance:</h4><p>${S.ally ? (my ? `<b class="evscore">${my}</b> points of control · rank #${myR} of ${M.rank.length}` : "No sectors held yet. Settle worlds, or take them from rivals, to claim sectors.") : "Join an alliance to fight for sectors."}</p>
    <h4>Event Info:</h4><p>Every week alliances fight for the galaxy's 48 sectors: six layers, eight lanes each. The alliance whose members hold the most in a sector controls it. Inner Belt and Core sectors count double.</p>
    <h4>Event Rules:</h4><p>A homeworld counts 3 in its sector, a colony 1, and every world adds 1 per 10 Commander levels of its owner. Ties leave a sector unclaimed. Take colonies from rival alliances to swing sectors your way.</p>
    <h4>Weekly rewards:</h4><p>When the week ends (Monday 00:00 UTC), every member of an alliance that holds sectors claims ◆2 per point of control (up to ◆40). The top three alliances' members also get a Metal, Crystal or Gas Booster (Gold, Silver, Bronze).</p></div>`; }
function cqClaimable(T = now()) { const lw = cqWeek(T) - 1; if (!S.ally || S.cq === lw || lw < 0) return null; const M = cqMap(), p = M.pts[S.ally] || 0; if (!p) return null; const r = M.rank.findIndex(x => x[0] === S.ally) + 1; return { lw, p, r, sh: Math.min(40, p * 2), item: r === 1 ? "bm_gold" : r === 2 ? "bc_silver" : r === 3 ? "bg_bronze" : null }; }
'''
rep('/* v539 Events lives in the hub', JS + '/* v539 Events lives in the hub')
rep('const EVS = [["pass", "Void Pass", "❖"],', 'const EVS = [["pass", "Void Pass", "❖"], ["conq", "Alliance Conquest", "⚑"],')
rep('  if (k === "pass") return vpReady(); /* v542 */', '  if (k === "pass") return vpReady(); /* v542 */\n  if (k === "conq") return cqClaimable() ? 1 : 0; /* v545 */')
rep('function evBanner(k, T) { if (k === "pass") return vpBanner(T);', 'function evBanner(k, T) { if (k === "pass") return vpBanner(T); if (k === "conq") return cqBanner(T); /* v545 */')
rep('  else if (k === "pass") {', '''  else if (k === "conq") { body = cqBody(T, tab); const c = cqClaimable(T); claim = `<button class="btn ${c ? "amber" : "ghost"} evclaim" data-act="cqClaim" ${c ? "" : "disabled"}>${c ? `Claim last week · ◆${c.sh}${c.item ? " + " + SHOP[c.item].n : ""}` : "Claim (after the week ends)"}</button>`; } /* v545 */
  else if (k === "pass") {''')
rep('  vpClaim: () => act(() => {', '''  cqClaim: () => act(() => { const c = cqClaimable(); if (!c) return; S.cq = c.lw; S.shards = (S.shards || 0) + c.sh; if (c.item) giveItem(c.item); toast(`Alliance Conquest: ◆${c.sh}${c.item ? " and a " + SHOP[c.item].n : ""} for last week's ${c.p} points of control.`, "win"); }), /* v545 */
  vpClaim: () => act(() => {''')
css = '''
/* v545 Alliance Conquest */
.cqban{height:auto;min-height:200px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:8px;align-items:center;padding:10px;border:1.5px solid rgba(122,244,255,.5);border-radius:14px;background:radial-gradient(90% 90% at 25% 50%,#10203a,#04070e 75%)}
.cqmap{width:100%;max-width:220px;justify-self:center;filter:drop-shadow(0 0 10px rgba(122,244,255,.25))}
.cqtx{display:flex;flex-direction:column;gap:4px;min-width:0}.cqtx>b{font:800 21px var(--f-display,sans-serif);letter-spacing:.04em;color:#fff}.cqtx>small{font-size:12px;color:#c8d6e0}
.cqleg{display:flex;flex-direction:column;gap:3px;margin-top:4px}.cqleg span{font-size:12px;color:#e9f1f7;display:flex;align-items:center;gap:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.cqleg i,.cqdot{display:inline-block;width:10px;height:10px;border-radius:3px;flex:none;margin-right:4px}
@media (max-width:380px){.cqban{grid-template-columns:1fr}}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 544\b", "GAME_V = 545", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
