# v615 (part two): the Supply Depot's own page with Quartermaster Ondra Vey voiced (premade ElevenLabs voice "Domi", eleven_v4, seed 11).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
js = open('tools/patches/p615_depot.js', encoding='utf-8').read()
a = s.index('function mShop() {'); s = s[:a] + js + s[a:]
css = '''.dph2{position:relative;border-radius:18px;overflow:hidden;min-height:220px;display:flex;align-items:flex-end;gap:12px;padding:12px;border:1px solid rgba(255,207,90,.4);margin-bottom:6px}
.dph2 .dpbn{filter:saturate(1.1) brightness(.8)}.dph2::after{content:"";position:absolute;inset:0;background:linear-gradient(transparent 35%,rgba(4,8,14,.85));pointer-events:none}
.dpport{position:relative;z-index:1;flex:none;width:118px;height:150px;padding:0;border-radius:14px;overflow:hidden;border:2px solid rgba(255,207,90,.7);box-shadow:0 0 22px rgba(255,207,90,.35);background:#0b1118;cursor:pointer}
.dpport img{width:100%;height:100%;object-fit:cover;object-position:50% 12%}
.dpsay{position:relative;z-index:1;flex:1;min-width:0;display:flex;flex-direction:column;gap:6px}.dpsay small{font-size:10px;letter-spacing:.16em;color:var(--amber)}
.dpsay p{margin:0;font-size:14px;line-height:1.4;color:#eef4f8;background:rgba(6,14,22,.82);border:1px solid rgba(255,255,255,.12);border-radius:4px 14px 14px 14px;padding:8px 11px}.dpsay .btn{align-self:flex-start}
'''
i = s.index('</style>', s.index('#celeb{position:fixed')); s = s[:i] + css + s[i:]
rep('archives: shArch,', 'archives: shArch, depot: shDepot,')
rep('    ${acc("depot", ic(MI.tag), "Supply Depot", "", mShop())}', '    <section class="acc"><button class="acch" data-act="depotOpen"><span class="ai">${ic(MI.tag)}</span><span class="at">Supply Depot</span><span class="pill amb">Open ›</span></button></section>')
rep('  mtab: d => { if (d.k === "msg") return ACT.nav({ v: "mail" });', '  depotOpen: () => depotOpen(), depTalk: () => { const L = depLines(); let l; do { l = L[(Math.random() * L.length) | 0]; } while (l === G.depSay && L.length > 1); depSay(l); }, /* v615 */\n  mtab: d => { if (d.k === "msg") return ACT.nav({ v: "mail" }); if (d.k === "depot" || d.k === "shop") return depotOpen();')
rep('function act(fn) { advance(now()); fn(); progress(); dirty(); render(true); saveSoon(); }', 'function act(fn) { advance(now()); fn(); progress(); dirty(); render(true); if (sheet && sheet.type === "depot") try { renderSheet(); } catch (e) {} saveSoon(); }')
rep('function renderMenu() { if (view === "cmd") render(true); }', 'function renderMenu() { if (view === "cmd") render(true); if (sheet && sheet.type === "depot") renderSheet(); }')
rep("    toast(`Traded ${fmt(amt)} ${RES_N[from].toLowerCase()} for ${fmt(get)} ${RES_N[to].toLowerCase()}.`, \"win\");", "    toast(`Traded ${fmt(amt)} ${RES_N[from].toLowerCase()} for ${fmt(get)} ${RES_N[to].toLowerCase()}.`, \"win\"); setTimeout(() => depSay(depRank() > rk0 ? DEP_RANKUP : DEP_TRADE[(Math.random() * DEP_TRADE.length) | 0]), 400);")
rep('toast(`Contract delivered: ◆3 and a ${SHOP[C.crate].n}.`, "win");', 'toast(`Contract delivered: ◆3 and a ${SHOP[C.crate].n}.`, "win"); setTimeout(() => depSay(DEP_CONTRACT), 400);')
rep('function advHolo(line, force) { if (!line || G.cineOn) return;', 'function advHolo(line, force) { if (!line || G.cineOn || (sheet && sheet.type === "depot")) return; /* v615 Ondra has the floor */')
open(P, 'w', encoding='utf-8').write(s); print('ok')
