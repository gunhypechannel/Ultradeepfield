# v539 Events and Rankings in one place, boss events only in their week, and a banner for every boss (owner: "Make boss events banners
# hidden until the week of the event, it should only show event of the week"; "Make each boss have their own remastered banner, find
# some way to combine events and rankings tab into one").
#  - The dock's Rankings tab is now Events: one hub (view "rank") with an Events | Rankings switch at the top (sub.hub). The Events side is
#    the old Events sheet drawn inline (shEvents(true)); every way into Events (ACT.events, evCube) and Menu › Rankings land on the hub.
#  - Boss events (Super Boss Hunt, Titan Hunt, Convergence) show only while live, within 7 days of starting, or with rewards to claim
#    (evShow). The hub opens on the first event shown.
#  - A boss event's banner is now per boss: the boss's painting (art/arch/<k>.webp) in its colour, its name and epithet, a health bar and
#    LIVE / rises-in / defeated, with a strip of the group's bosses below to switch between them (evState().sbK, ACT.sbPick).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# the state: the sheet when Events is a sheet, sub.ev when it is the hub
rep('function shEvents() {\n  const T = now(), tab = sheet.evTab === "rk" ? "rk" : "ov", k = EVS.some(e => e[0] === sheet.ev) ? sheet.ev : "sboss";',
    '''/* v539 Events lives in the hub (the dock's Events tab); a boss event shows only in its week, while live, or with rewards waiting */
const evState = () => sheet && sheet.type === "events" ? sheet : (sub.ev = sub.ev || {});
const evShow = (key, T = now()) => { const g = key === "eboss" ? 3 : key === "tboss" ? 2 : key === "sboss" ? 1 : 0; if (!g) return true; try { return wbGroupOn(g, T) || wbGroupNext(g, T) - T <= 7 * 864e5 || sbReady(g) > 0; } catch (e) { return true; } };
function shEvents(inline) {
  const T = now(), E = evState(), tab = E.evTab === "rk" ? "rk" : "ov", VIS = EVS.filter(e => (e[0] !== "gifts" || myAlly()) && evShow(e[0], T)), k = VIS.some(e => e[0] === E.ev) ? E.ev : (VIS[0] || ["cube"])[0];''')
rep('const chips = `<div class="evchips evhub">${EVS.filter(e => e[0] !== "gifts" || myAlly()).map(', 'const chips = `<div class="evchips evhub">${VIS.map(')
rep('return `<div class="hd evhd"><div><h2>Events</h2></div><button class="x" data-act="close" aria-label="Close">✕</button></div>${tabs}${chips}${evBanner(k, T)}${body}${claim}`;',
    'return `${inline ? "" : `<div class="hd evhd"><div><h2>Events</h2></div><button class="x" data-act="close" aria-label="Close">✕</button></div>`}${tabs}${chips}${evBanner(k, T)}${body}${claim}`;')
rep('  evPick: d => { sheet.ev = d.v; renderSheet(); },\n  evTab: d => { sheet.evTab = d.v; renderSheet(); },',
    '''  evPick: d => { evState().ev = d.v; sheet && sheet.type === "events" ? renderSheet() : render(true); },
  evTab: d => { evState().evTab = d.v; sheet && sheet.type === "events" ? renderSheet() : render(true); },
  sbPick: d => { evState().sbK = d.k; sheet && sheet.type === "events" ? renderSheet() : render(true); }, /* v539 */
  hubTab: d => { sub.hub = d.v === "rk" ? "rk" : "ev"; render(); },''')
rep('  events: d => openSheet({ type: "events", ev: d && d.ev ? d.ev : undefined }),', '  events: d => { if (sheet) closeSheet(); sub.hub = "ev"; sub.ev = sub.ev || {}; if (d && d.ev) sub.ev.ev = d.ev; ACT.nav({ v: "rank" }); }, /* v539 the hub */')
rep('  evCube: () => openSheet({ type: "events", ev: "cube" }),', '  evCube: () => ACT.events({ ev: "cube" }),')
rep('  ranks: () => openSheet({ type: "ranks", tab: "players" }),', '  ranks: () => { if (sheet) closeSheet(); sub.hub = "rk"; ACT.nav({ v: "rank" }); }, /* v539 the hub */')
rep('function vRank() { sub.rk = sub.rk || { tab: "players" }; return `<div class="gstack rankv">${shRanks(sub.rk)}</div>`; }',
    '''function vRank() { sub.rk = sub.rk || { tab: "players" }; const h = sub.hub === "rk" ? "rk" : "ev", n = EVS.reduce((a, e) => a + (evShow(e[0]) ? evCount(e[0]) : 0), 0); /* v539 Events and Rankings in one hub */
  return `<div class="gstack rankv"><div class="hubsw"><button class="${h === "ev" ? "on" : ""}" data-act="hubTab" data-v="ev">🏆 Events${n ? `<i>${n}</i>` : ""}</button><button class="${h === "rk" ? "on" : ""}" data-act="hubTab" data-v="rk">📊 Rankings</button></div>${h === "rk" ? shRanks(sub.rk) : `<div class="evhubv sheet-like">${shEvents(true)}</div>`}</div>`; }''')
rep('["rank", "Rankings"]', '["rank", "Events"]')
# a banner for every boss
i = s.index('function sbBanner(T, g = 1) {'); j = s.index('\n/* v513 the reward track', i)
s = s[:i] + '''function sbBanner(T, g = 1) { const E = SB_G[g], st = wbState(T), main = wbMain(g), live = wbGroupOn(g, T), ES = evState(); /* v539 a banner for every boss */
  const sel = main.includes(ES.sbK) ? ES.sbK : main.find(k => wbOn(k, T) && st.hp[k] > 0) || main.slice().sort((a, b) => wbNext(a, T) - wbNext(b, T))[0];
  const stat = k => { const on = wbOn(k, T), hp = Math.max(0, st.hp[k] || 0); return on ? (hp > 0 ? "live" : "down") : "wait"; };
  const B = WB[sel], A = ARCH[sel] || {}, on = wbOn(sel, T), hp = Math.max(0, st.hp[sel] || 0), pc = on ? clamp(hp / B.hp * 100, 0, 100) : 100, end = on ? wbLiveEnd(sel, T) : wbNext(sel, T), sx = stat(sel), up = main.filter(k => stat(k) === "live").length;
  return `<div class="evban bossban ${sx}" style="--bc:${B.col}"><img src="art/arch/${sel}.webp?v=1" alt="${esc(B.n)}" loading="lazy"><i class="bbglow"></i>
    <div class="bbtop"><span class="vlive${on && hp > 0 ? " on" : ""}">${sx === "live" ? "● LIVE" : sx === "down" ? "✓ DEFEATED" : "NEXT"}</span><small>${esc(E.n)}${live ? ` · ${up} of ${main.length} standing` : ""}</small></div>
    <div class="bbbot"><b>${esc(B.n)}</b>${A.t ? `<em>${esc(A.t)}</em>` : ""}<div class="bbhp"><i style="width:${pc.toFixed(1)}%"></i><span>${sx === "live" ? `${fmt(hp)} / ${fmt(B.hp)} HP` : sx === "down" ? "Brought down this week" : `${fmt(B.hp)} HP · ${esc(B.where || "")}`}</span></div>
      <span class="evend">${sx === "wait" ? "Rises in" : sx === "live" ? "Leaves in" : "Gone for"}: <b data-end="${end}">${ftime(end - T)}</b></span></div></div>
  <div class="bbstrip">${main.map(k => { const x = stat(k); return `<button class="bbs ${x}${k === sel ? " on" : ""}" style="--bc:${WB[k].col}" data-act="sbPick" data-k="${k}" aria-label="${esc(WB[k].n)}"><img src="art/arch/${k}.webp?v=1" alt="" loading="lazy"><b>${esc(WB[k].n)}</b><small>${x === "live" ? "● Live" : x === "down" ? "✓ Down" : ftime(wbNext(k, T) - T)}</small></button>`; }).join("")}</div>`; }''' + s[j:]
css = '''
/* v539 the Events hub and the boss banners */
.hubsw{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:4px;border-radius:14px;border:1px solid var(--line);background:rgba(6,14,22,.7);margin-bottom:8px}
.hubsw button{position:relative;padding:10px 6px;border-radius:10px;border:0;background:transparent;color:var(--muted);font:700 14px var(--f-display,sans-serif);letter-spacing:.04em}
.hubsw button.on{background:linear-gradient(180deg,rgba(85,214,232,.22),rgba(85,214,232,.08));color:var(--cyan);box-shadow:inset 0 0 0 1px rgba(85,214,232,.5)}
.hubsw i{position:absolute;top:4px;right:10px;font-style:normal;font-size:10px;min-width:16px;height:16px;line-height:16px;border-radius:8px;background:var(--red,#ff5a4a);color:#fff}
.evhubv{display:flex;flex-direction:column;gap:8px}
.bossban{height:auto;min-height:220px;aspect-ratio:16/10;max-height:330px;border:1.5px solid color-mix(in srgb,var(--bc) 75%,transparent);border-radius:14px;background:#05080e;box-shadow:0 0 22px color-mix(in srgb,var(--bc) 35%,transparent)}
.bossban>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 30%;filter:saturate(1.1)}
.bossban .bbglow{position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,7,12,.55),transparent 28%,transparent 45%,rgba(4,7,12,.93) 86%),radial-gradient(90% 60% at 50% 100%,color-mix(in srgb,var(--bc) 30%,transparent),transparent 70%)}
.bossban.wait>img{filter:saturate(.75) brightness(.8)}.bossban.down>img{filter:grayscale(.7) brightness(.6)}
.bbtop{position:absolute;top:10px;left:12px;right:12px;display:flex;align-items:center;gap:8px}.bbtop small{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#e9f1f7;text-shadow:0 1px 3px #000}
.bbbot{position:absolute;left:12px;right:12px;bottom:10px;display:flex;flex-direction:column;gap:3px}
.bbbot>b{font:800 24px var(--f-display,sans-serif);letter-spacing:.04em;color:#fff;text-shadow:0 0 14px var(--bc),0 2px 4px #000;line-height:1.05}
.bbbot>em{font-style:normal;font-size:12.5px;color:color-mix(in srgb,var(--bc) 60%,#fff)}
.bbhp{position:relative;height:16px;border-radius:8px;overflow:hidden;background:rgba(0,0,0,.6);border:1px solid color-mix(in srgb,var(--bc) 60%,transparent);margin-top:4px}
.bbhp i{position:absolute;inset:0 auto 0 0;background:linear-gradient(90deg,color-mix(in srgb,var(--bc) 70%,#fff 0%),var(--bc));box-shadow:0 0 10px var(--bc)}.bossban.down .bbhp i{width:0!important}
.bbhp span{position:relative;display:block;text-align:center;font-size:10.5px;line-height:14px;color:#fff;text-shadow:0 1px 2px #000;font-variant-numeric:tabular-nums}
.bbbot .evend{position:static;align-self:flex-start;font-size:12px;color:#d6e2ea;background:rgba(4,7,12,.6);border-radius:7px;padding:2px 8px;margin-top:2px}
.bbstrip{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding:2px 0 4px}.bbstrip::-webkit-scrollbar{display:none}
.bbs{position:relative;flex:1 0 84px;min-width:84px;height:84px;border-radius:12px;overflow:hidden;border:1px solid color-mix(in srgb,var(--bc) 45%,transparent);background:#05080e;padding:0;color:#fff;text-align:left}
.bbs img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 30%;opacity:.75}.bbs::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 35%,rgba(4,7,12,.92))}
.bbs b,.bbs small{position:absolute;left:6px;right:4px;z-index:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.bbs b{bottom:16px;font-size:11px}.bbs small{bottom:3px;font-size:10px;color:#c7d3dc}
.bbs.on{border-color:var(--bc);box-shadow:0 0 12px color-mix(in srgb,var(--bc) 60%,transparent),inset 0 0 0 1px var(--bc)}.bbs.on img{opacity:1}.bbs.live small{color:#5dff9a}.bbs.down img{filter:grayscale(.8)}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 538\b", "GAME_V = 539", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
