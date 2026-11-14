# v548 one tab bar in the Events hub (owner, with a screenshot of the two stacked bars "Events | Rankings" and "Overview | Ranking":
# "What is this why are there two? I want them some how all combined"). The hub's own Events | Rankings switch is gone; the event bar
# under it now has three tabs: Overview and Ranking (the chosen event's) and Leaderboards (the galaxy rankings that used to be the
# Rankings side). On the Leaderboards tab the same bar stays on top, so one tap goes back to the events.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('''  const tabs = `<div class="evtabs"><button class="${tab === "ov" ? "on" : ""}" data-act="evTab" data-v="ov">Overview</button><button class="${tab === "rk" ? "on" : ""}" data-act="evTab" data-v="rk">Ranking</button></div>`;''',
    '''  const tabs = evTabsHTML(inline ? tab : tab, inline); /* v548 one bar */''')
rep('function shEvents(inline) {', '''/* v548 the single tab bar: the event's Overview and Ranking, and (in the hub) the galaxy Leaderboards */
const evTabsHTML = (tab, hub) => `<div class="evtabs${hub ? " ev3" : ""}"><button class="${tab === "ov" ? "on" : ""}" data-act="evTab" data-v="ov">Overview</button><button class="${tab === "rk" ? "on" : ""}" data-act="evTab" data-v="rk">Ranking</button>${hub ? `<button class="${tab === "lb" ? "on" : ""}" data-act="hubTab" data-v="rk">🏆 Leaderboard</button>` : ""}</div>`;
function shEvents(inline) {''')
i = s.index('function vRank() {'); j = s.index('\n', s.index('\n', i) + 1)
s = s[:i] + '''function vRank() { sub.rk = sub.rk || { tab: "players" }; const h = sub.hub === "rk" ? "rk" : "ev"; /* v539 the hub; v548 one tab bar */
  return `<div class="gstack rankv">${h === "rk" ? `${evTabsHTML("lb", true)}${shRanks(sub.rk)}` : `<div class="evhubv sheet-like">${shEvents(true)}</div>`}</div>`; }''' + s[j:]
rep('  evTab: d => { evState().evTab = d.v; sheet && sheet.type === "events" ? renderSheet() : render(true); },', '  evTab: d => { evState().evTab = d.v; if (!(sheet && sheet.type === "events")) sub.hub = "ev"; sheet && sheet.type === "events" ? renderSheet() : render(true); },')
rep('.hubsw{display:grid;', '.ev3{gap:6px}.ev3 button{flex:1 1 0;min-width:0;padding-left:4px;padding-right:4px;white-space:nowrap;font-size:14px;letter-spacing:0;overflow:hidden;text-overflow:ellipsis}\n.hubsw{display:grid;')
s2 = re.sub(r"GAME_V = 547\b", "GAME_V = 548", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
