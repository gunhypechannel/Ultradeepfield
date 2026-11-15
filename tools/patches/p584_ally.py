# v584 The alliance tab, simple and elegant (owner: "I don't like the alliance tab, it's way to long and does not seem simple or
# elegant"). Home: a compact header (emblem, tag and name, members and how many online, level bar), the bio, a "needs you" line only
# when something waits (Cube live, an ally asking for a speed-up, open joint strikes, a war), six tiles (Members, Chat, Defense,
# Strikes, Level & fund, Leader/Captain or Rankings) and a quiet link row (Alliance list, Rankings, Leave). Each tile opens its own
# short page with "‹ Alliance". Members open the existing member sheet (each row's ⋯ holds title, rank, kick, leadership), so the
# Leader page no longer lists every member with two buttons. Defense is two steps: your guards first, then pick an ally (avatars),
# then one of their worlds to Station on.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# the new home and pages
i = s.index('function vAlly() {'); j = s.index('\n}', s.index('${pactCard()}</div>`;', i)) + 2
old = s[i:j]
new = '''function vAlly() {
  if (sub.allyView === "list") return `<div class="gstack allyv">${allyListView()}</div>`;
  if (!myAlly()) return `<div class="gstack allyv">${sub.allyView === "create" ? allyCreateView() : allyInfoView()}</div>`;
  return `<div class="gstack allyv al2">${alPage(myAlly(), sub.alP || "")}</div>`; /* v584 */
}
''' + open('tools/patches/p584_ally.js', encoding='utf-8').read()
s = s[:i] + new + s[j:]
# Level & fund on its own page
rep('function allySection() {', 'function allySection(part) {')
rep('    return helpCards(a) + fundCard + `<div class="mcard"><h3 style="display:flex;align-items:center;gap:10px">', '    if (part === "fund") return helpCards(a) + fundCard; /* v584 */\n    return helpCards(a) + fundCard + `<div class="mcard"><h3 style="display:flex;align-items:center;gap:10px">')
# the leader page: no member list (it lives behind ⋯ in Members); the emblem and open/private here
rep('''    <h4 class="alh">Members · titles and ranks</h4><div class="altl">${mem.length ? mem.map(u => `<div class="altr">''', '''    <button class="btn ghost wide" data-act="allyOpen2" data-id="${a.id}">👥 Manage members</button>${allyCan(a, "open") ? `<button class="btn ghost wide" data-act="allyOpenSet" data-v="${a.open === false ? 1 : 0}">${a.open === false ? "🔒 Private: tap to open to new members" : "🔓 Open: tap to make private"}</button>` : ""}${a.leader === G.me ? `<h4 class="alh">Emblem</h4><button class="btn ghost wide" data-act="allyCrestOpen">${G.crestOpen ? "Close emblems" : "Change emblem"}</button>${G.crestOpen ? crestPicker(crestNo(a.id), "allyCrest") : ""}` : ""}<div hidden>${mem.length ? mem.map(u => `<div class="altr">''')
rep('''  allyCrestOpen: () => {''', '''  alPg: d => { sub.alP = d.v || ""; sub.depU = null; G.crestOpen = false; render(true); try { const v = document.querySelector("#view, main"); if (v) v.scrollTop = 0; } catch (e) {} }, alDepU: d => { sub.depU = d.u || null; render(true); }, /* v584 */
  allyCrestOpen: () => {''') if s.count('  allyCrestOpen: () => {') == 1 else rep('allyCrestOpen: () => {', 'alPg: d => { sub.alP = d.v || ""; sub.depU = null; G.crestOpen = false; render(true); try { const v = document.querySelector("#view, main"); if (v) v.scrollTop = 0; } catch (e) {} }, alDepU: d => { sub.depU = d.u || null; render(true); }, /* v584 */ allyCrestOpen: () => {')
CSS = '''.al2 .alh2{display:flex;align-items:center;gap:14px;padding:14px;border-radius:18px;border:1px solid rgba(85,214,232,.35);background:radial-gradient(120% 140% at 0 0,rgba(85,214,232,.16),transparent 60%),linear-gradient(180deg,#112334,#08121c);box-shadow:0 0 24px rgba(85,214,232,.12)}
.al2 .alh2 .alcrest{flex:none}.alh2t{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px}.alh2t small{font:600 10.5px var(--f-display);letter-spacing:.2em;color:var(--cyan)}.alh2t b{font:700 20px/1.15 var(--f-display);color:#f2fbff;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.alh2t b em{font-style:normal;color:#ffd36b}
.alh2t>span{font-size:13px;color:#a9c4d4;display:flex;align-items:center;gap:5px;flex-wrap:wrap}.alh2t .xp{height:5px;margin-top:4px}.alb2{margin:0;padding:10px 14px;border-left:3px solid rgba(255,211,107,.6);background:rgba(255,255,255,.03);border-radius:0 12px 12px 0;color:#d6e6ee;font-style:italic}
.alneed{display:flex;align-items:center;justify-content:space-between;gap:10px;width:100%;padding:12px 14px;border-radius:14px;border:1px solid rgba(255,199,106,.55);background:linear-gradient(90deg,rgba(255,170,60,.16),rgba(255,170,60,.03));color:#ffe3a6;font:600 14px var(--f-body);text-align:left;cursor:pointer}.alneed.cube{border-color:rgba(93,255,138,.6);background:linear-gradient(90deg,rgba(93,255,138,.16),rgba(93,255,138,.03));color:#c9ffd9}.alneed span{opacity:.85;white-space:nowrap}
.altiles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.altile{display:flex;flex-direction:column;align-items:flex-start;gap:4px;min-height:96px;padding:14px;border-radius:16px;border:1px solid rgba(85,214,232,.28);background:linear-gradient(160deg,rgba(85,214,232,.1),rgba(8,18,28,.92) 70%);color:#eaf7fc;text-align:left;cursor:pointer;transition:transform .12s,border-color .2s}
.altile:active{transform:scale(.97)}.altile svg{width:28px;height:28px;color:var(--cyan);filter:drop-shadow(0 0 6px rgba(85,214,232,.55))}.altile b{font:700 15.5px var(--f-display);letter-spacing:.02em}.altile small{font-size:12.5px;color:#93b2c3}.altile em{font-style:normal;color:var(--green)}.altile em.red{color:#ff7a6a}
.altile[data-v="lead"] svg{color:#ffd36b;filter:drop-shadow(0 0 6px rgba(255,211,107,.6))}.altile[data-v="war"] svg{color:#ff8a6a;filter:drop-shadow(0 0 6px rgba(255,120,90,.5))}.altile[data-v="def"] svg{color:#5dff8a;filter:drop-shadow(0 0 6px rgba(93,255,138,.5))}
.allinks{display:flex;justify-content:center;flex-wrap:wrap;gap:4px 16px;padding:4px 0 8px}.allinks button{background:none;border:0;color:#7d9bb0;font:500 13px var(--f-body);text-decoration:underline;text-underline-offset:3px;cursor:pointer;padding:6px}.allinks .alleave{color:#ffb3a8;font-size:13px}.allinks .alleave .red{color:#ff6a5a;font-weight:700}
.alpgh{display:flex;align-items:center;gap:12px}.alpgh b{font:700 19px var(--f-display);color:#f2fbff}
.aldepu{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:8px}.aldepu button{display:flex;flex-direction:column;align-items:center;gap:4px;padding:10px 6px;border-radius:14px;border:1px solid rgba(85,214,232,.25);background:rgba(10,26,40,.7);color:#eaf7fc;cursor:pointer;min-width:0}.aldepu .avc{width:52px!important;height:52px!important;border-radius:50%}.aldepu b{font-size:13px;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.aldepu small{font-size:11.5px;color:#93b2c3}
'''
rep('.alframe{display:flex;flex-direction:column;gap:10px}', CSS + '.alframe{display:flex;flex-direction:column;gap:10px}')
s2 = re.sub(r"GAME_V = 583\b", "GAME_V = 584", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
