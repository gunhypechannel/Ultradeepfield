# v543 collection rewards and the starter alliance & buddies (owner: "Do it all", ideas #5 and #7).
#  - Collections: every chapter of the Ancient Archives (The First Warnings, The Forbidden Pantheon, ... The Bestiary) is a collection.
#    Its header shows how many records are fully recovered; when all are, "Claim" pays ◆10 per record (max ◆60) and a permanent +1%
#    production for every completed chapter (collPct, added to prodBonus), and the chapter wears a gold trophy. The Archives header counts
#    your trophies.
#  - Starter alliance: after the Academy, a commander with no alliance gets a one-time card offering Quick join (the strongest open
#    alliance with room) with a welcome gift for joining in the first week (◆10 and a Boost Pack ×5, once, S.welcomeAlly).
#  - Buddies: the Alliances page (no alliance yet) and the starter card suggest three active commanders near your level to add as friends;
#    your first three friends each pay a ◆3 buddy bonus (S.buddyN).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const prodBonus = () => 1 + (runePct("spirit") + allyPass().prod + fsB("prod")) / 100;', 'const collPct = () => S && S.coll ? Object.keys(S.coll).filter(k => S.coll[k]).length : 0; /* v543 +1% per completed Archives chapter */\nconst prodBonus = () => 1 + (runePct("spirit") + allyPass().prod + fsB("prod") + collPct()) / 100;')
rep('''    ${ARCH_CAT.map(([c, nm, d]) => { const ks = ARCH_ORD.filter(k => ARCH[k].cat === c); return `<h2 class="sec arsec">${esc(nm)}</h2><p class="note">${esc(d)}</p><div class="argrid">${ks.map(card).join("")}</div>`; }).join("")}`; }''',
    '''    <div class="colsum">🏆 <b>${collPct()}</b> of ${ARCH_CAT.filter(([c]) => ARCH_ORD.some(k => ARCH[k].cat === c)).length} collections complete · +${collPct()}% production on every world</div>
    ${ARCH_CAT.map(([c, nm, d]) => { const ks = ARCH_ORD.filter(k => ARCH[k].cat === c); if (!ks.length) return ""; const full = ks.filter(k => archLv(k) >= 2).length, done = full >= ks.length, got = !!(S.coll || {})[c]; /* v543 collections */
      return `<h2 class="sec arsec${got ? " coldone" : ""}">${got ? '<i class="coltro">🏆</i>' : ""}${esc(nm)}<span class="colct">${full}/${ks.length}</span></h2><p class="note">${esc(d)}</p>${done && !got ? `<div class="colclaim"><div><b>Collection complete!</b><small>◆${Math.min(60, ks.length * 10)} and +1% production on every world, for good.</small></div><button class="btn amber" data-act="collClaim" data-c="${c}">Claim</button></div>` : !done ? `<div class="colbar"><i style="width:${(full / ks.length * 100).toFixed(0)}%"></i><small>Recover every record (field notes too) to complete this collection: ◆${Math.min(60, ks.length * 10)} and +1% production for good.</small></div>` : ""}<div class="argrid">${ks.map(card).join("")}</div>`; }).join("")}`; }''')
rep('  allyQuick: () => {', '''  collClaim: d => act(() => { const ks = ARCH_ORD.filter(k => ARCH[k].cat === d.c); if (!ks.length || ks.some(k => archLv(k) < 2)) return; S.coll = S.coll || {}; if (S.coll[d.c]) return; S.coll[d.c] = now(); const n = Math.min(60, ks.length * 10); S.shards = (S.shards || 0) + n; toast(`Collection complete: ◆${n} and +1% production on every world, for good.`, "win"); try { SFX.fanfare(true); } catch (e) {} }), /* v543 */
  starterJoin: () => { const a = quickAlly(); const c = $("#starterask"); if (c) c.remove(); if (!a) return toast("No open alliance has room right now. Found your own from Alliances!", "warn"); G.welcomeAllyGo = 1; ACT.allyJoin({ id: a.id }); },
  starterLater: () => { const c = $("#starterask"); if (c) c.remove(); },
  allyQuick: () => {''')
# the welcome gift on joining (first week, once)
rep('''    G.db.doc("alliances/" + d.id).update({ members: { [G.me]: now() } }).then(() => toast(`You joined [${a.tag}] ${a.name}.`, "win"))''',
    '''    G.db.doc("alliances/" + d.id).update({ members: { [G.me]: now() } }).then(() => { toast(`You joined [${a.tag}] ${a.name}.`, "win"); if (!S.welcomeAlly && (G.welcomeAllyGo || (S.tut && S.tut.k !== "done") || cmdLevel(score()) < 15)) { S.welcomeAlly = now(); S.shards = (S.shards || 0) + 10; giveItem("boost5"); dirty(); setTimeout(() => toast("Welcome gift for joining an alliance: ◆10 and a Boost Pack ×5.", "win"), 1500); } }) /* v543 */''')
# buddy bonus for the first three friends
rep('  befriend: d => { if (!d.u || d.u === G.me) return; S.friends = S.friends || []; if (S.friends.includes(d.u)) return;', '  befriend: d => { if (!d.u || d.u === G.me) return; S.friends = S.friends || []; if (S.friends.includes(d.u)) return; if ((S.buddyN || 0) < 3 && S.friends.length < 100) { S.buddyN = (S.buddyN || 0) + 1; S.shards = (S.shards || 0) + 3; setTimeout(() => toast("Buddy bonus: ◆3 for making a friend in the galaxy.", "win"), 900); } /* v543 */')
# buddies on the no-alliance page, and the starter card after the Academy
rep('function allyInfoView() {', '''/* v543 commanders near your level who played this week, to befriend */
function buddyPicks(n = 3) { const lv = cmdLevel(score()), fr = new Set(S.friends || []), T = now(); return Object.entries(G.players || {}).filter(([id, p]) => id !== G.me && !isBot(id) && !fr.has(id) && p && (p.last || p.joined || 0) > T - 7 * 864e5).map(([id, p]) => [id, p, Math.abs(cmdLevel(p.score || 0) - lv)]).sort((a, b) => a[2] - b[2]).slice(0, n); }
const buddyHTML = () => { const L = buddyPicks(); return L.length ? `<div class="mcard buddy"><h3>🤝 Commanders near your level</h3><p>Add a friend to see their worlds, send gifts and help each other. Your first three friends each bring a ◆3 buddy bonus.</p>${L.map(([id, p]) => `<div class="bdr">${avCanvas(id, "avc lbav")}<span><b>${esc(nameOf(id))}</b><small>Commander Lv.${cmdLevel(p.score || 0)}</small></span><button class="btn sm" data-act="befriend" data-u="${id}">Add friend</button></div>`).join("")}</div>` : ""; };
setInterval(() => { try { if (!S || !G.ready || G.mode !== "online" || S.ally || S.starterAsk || tutOn() || sheet || battle || advLines || !S.tut || S.tut.k !== "done" || $("#starterask") || $("#pushask")) return; const a = quickAlly(); if (!a) return;
  S.starterAsk = 1; dirty(); const w = document.createElement("div"); w.id = "starterask"; w.className = "toast rmd busy pushask";
  w.innerHTML = `<span class="ric">🛡</span><span class="rtx"><small>Stronger together</small><b>Join [${esc(a.tag)}] ${esc(a.name)}?</b><em>An active alliance with room for you. Join now for a welcome gift: ◆10 and a Boost Pack ×5.</em></span><span class="rbt"><button class="btn sm amber" data-act="starterJoin">Join</button><button class="rx" data-act="starterLater" aria-label="Not now">✕</button></span>`;
  const box = $("#toasts"); if (box) box.appendChild(w); setTimeout(() => { if (w.isConnected) w.remove(); }, 25000); } catch (e) {} }, 60000);
function allyInfoView() {''')
rep('''    <div class="mcard qjoin"><h3>⚡ Quick join</h3>''', '''    ${G.mode === "online" ? buddyHTML() : ""}<div class="mcard qjoin"><h3>⚡ Quick join</h3>''')
css = '''
/* v543 collections and buddies */
.colsum{margin:8px 0 2px;padding:9px 12px;border-radius:12px;border:1px solid rgba(255,207,90,.45);background:linear-gradient(90deg,rgba(255,207,90,.14),rgba(8,14,22,.8));font-size:13px}.colsum b{color:#ffcf5a;font-size:16px}
.arsec{display:flex;align-items:center;gap:8px}.colct{margin-left:auto;font-size:12px;letter-spacing:.06em;color:var(--muted);font-family:var(--f-ui,inherit)}.coldone{color:#ffcf5a}.coltro{font-style:normal;filter:drop-shadow(0 0 6px #ffcf5a)}
.colbar{position:relative;display:flex;flex-direction:column;gap:4px;margin:4px 0 8px}.colbar i{display:block;height:6px;border-radius:3px;background:linear-gradient(90deg,#e2c48a,#ffcf5a);max-width:100%}.colbar::before{content:"";position:absolute;left:0;right:0;top:0;height:6px;border-radius:3px;background:rgba(255,255,255,.08);z-index:-1}.colbar small{font-size:11.5px;color:var(--muted)}
.colclaim{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;align-items:center;padding:10px 12px;border-radius:12px;border:1px solid #ffcf5a;background:linear-gradient(110deg,rgba(255,207,90,.2),rgba(8,14,22,.9));margin:4px 0 8px;box-shadow:0 0 16px rgba(255,207,90,.25)}.colclaim b{color:#ffcf5a}.colclaim small{display:block;font-size:12px;color:var(--muted)}
.buddy .bdr{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:10px;align-items:center;padding:6px 0;border-top:1px solid var(--line)}.buddy .bdr small{display:block;font-size:11.5px;color:var(--muted)}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 542\b", "GAME_V = 543", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
