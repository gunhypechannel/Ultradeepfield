# v698: a joint strike's report no longer lists every commander in the heading (owner screenshot: 40 names filling the screen,
# "can we clean this up and make it some kind of drop down or something else that's clever"). With more than three commanders the
# heading names the strike and a collapsed "N commanders" row opens to the list: you first, then by ships brought, each with a bar
# for their share and an ally tag.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('<h2 class="sec">${esc(aN)} · attacker</h2>', '${(r.aUids || []).length > 3 && r.kind !== "raid" ? repCmdrs(r) : `<h2 class="sec">${esc(aN)} · attacker</h2>`}')
rep('const findRep = id =>', '''/* v698 a big joint strike's commanders: a collapsed row instead of every name in the heading */
function repCmdrs(r) { const U = r.aUids || [], sh = {}; for (const x of (r.sim && r.sim.A) || []) if (x && x[5] != null) sh[x[5]] = (sh[x[5]] || 0) + (+x[1] || 0);
  const rows = U.map(u => ({ u, n: sh[u] || 0 })).sort((a, b) => (b.u === G.me) - (a.u === G.me) || b.n - a.n), top = Math.max(1, ...rows.map(x => x.n)), tot = rows.reduce((a, x) => a + x.n, 0), bots = U.filter(isBot).length, me = U.includes(G.me);
  const nm = u => { const n = nameOf(u); return n.replace(/ \\((ally|rival|hostile)\\)$/, ""); }, tag = u => isBot(u) ? (botFriend(u) ? "ally" : "rival") : u === G.me ? "you" : "commander";
  return `<h2 class="sec">${esc(r.aName || "Joint strike")} · attacker</h2><details class="cmdrs"><summary><b>${U.length} commanders</b><span>${me ? "You" : esc(nm(U[0]))}${U.length > 1 ? ` + ${U.length - 1} more` : ""}${bots ? ` · ${bots} bot${bots > 1 ? "s" : ""}` : ""}${tot ? ` · ${fmt(tot)} ships` : ""}</span><i aria-hidden="true">▾</i></summary>
    <ol>${rows.map(x => `<li class="${x.u === G.me ? "me" : ""}"><span class="cn">${esc(nm(x.u))}</span><span class="ct ${tag(x.u)}">${tag(x.u)}</span><span class="cb"><i style="width:${Math.max(2, Math.round(x.n / top * 100))}%"></i></span><span class="cs">${x.n ? fmt(x.n) : "–"}</span></li>`).join("")}</ol></details>`; }
const findRep = id =>''')
rep('#app.cine #cubepanel{display:none}', '''#app.cine #cubepanel{display:none}
.cmdrs{flex:none;margin:-4px 0 12px;border:1px solid var(--line);border-radius:12px;background:rgba(10,22,34,.55);overflow:hidden}.cmdrs summary{display:flex;align-items:center;gap:10px;padding:10px 12px;cursor:pointer;list-style:none}.cmdrs summary::-webkit-details-marker{display:none}
.cmdrs summary b{font-size:14px;white-space:nowrap}.cmdrs summary span{flex:1;min-width:0;color:var(--muted);font-size:12.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.cmdrs summary i{font-style:normal;color:var(--muted);transition:transform .2s}.cmdrs[open] summary i{transform:rotate(180deg)}
.cmdrs ol{list-style:none;margin:0;padding:4px 12px 10px;max-height:min(46vh,360px);overflow-y:auto;border-top:1px solid var(--line)}.cmdrs li{display:grid;grid-template-columns:minmax(0,1fr) auto 64px auto;align-items:center;gap:8px;padding:6px 0;font-size:13px;border-bottom:1px solid rgba(255,255,255,.04)}
.cmdrs li.me .cn{color:#7dffb0;font-weight:700}.cmdrs .cn{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.cmdrs .ct{font-size:10px;letter-spacing:.08em;text-transform:uppercase;padding:2px 6px;border-radius:999px;background:rgba(85,214,232,.12);color:#8fdcea}.cmdrs .ct.you{background:rgba(125,255,176,.14);color:#7dffb0}.cmdrs .ct.rival{background:rgba(255,120,100,.14);color:#ff9a8a}
.cmdrs .cb{height:5px;border-radius:3px;background:rgba(255,255,255,.07);overflow:hidden}.cmdrs .cb i{display:block;height:100%;background:linear-gradient(90deg,#38dfee,#7dffb0)}.cmdrs .cs{font-variant-numeric:tabular-nums;color:var(--muted);font-size:12px;min-width:44px;text-align:right}''')
rep('const GAME_V = 697;', 'const GAME_V = 698;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
