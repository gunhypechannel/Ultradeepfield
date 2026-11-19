# v640: inventory sorted into categories (tabs + grouped "All"); teleport prices ◆200 aimed / ◆100 random, paid jumps need a confirm tap.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)

# ---- inventory categories ----
old_start = 'function invGridHTML() { const it = S.items || {}, inv = Object.keys(it).filter(k => it[k] > 0 && SHOP[k]);'
i = s.index(old_start); j = s.index("'<p class=\"note\">Your inventory is empty. Items you buy, and spoils from pirate raids, land here.</p>'; }", i)
body = s[i:j]
card = body[body.index('inv.map(k => { const s = SHOP[k]; return ') + len('inv.map(k => { const s = SHOP[k]; return '): body.index('; }).join("")}</div>` :')]
art = body[body.index('const art = '): body.index('\n  return inv.length')]
new = ('function invGridHTML() { const it = S.items || {}, ORD = Object.keys(SHOP), inv = Object.keys(it).filter(k => it[k] > 0 && SHOP[k]).sort((a, b) => ORD.indexOf(a) - ORD.indexOf(b)); ' + art + '\n'
       '  const card = k => { const s = SHOP[k]; return ' + card + '; };\n'
       '  if (!inv.length) return \'<p class="note">Your inventory is empty. Items you buy, and spoils from pirate raids, land here.</p>\';\n'
       '  /* v640 categories: the shop\'s own sections; anything outside them (old items) counts as Special */\n'
       '  const catOf = k => SHOP_CATS.some(x => x[0] === SHOP[k].cat) ? SHOP[k].cat : "special", lab = l => esc(l.replace(/^[♛◆]\\s*/, "")), cats = SHOP_CATS.filter(([c]) => inv.some(k => catOf(k) === c));\n'
       '  const n = c => inv.filter(k => !c || catOf(k) === c).reduce((a, k) => a + it[k], 0), sel = G.invCat && cats.some(x => x[0] === G.invCat) ? G.invCat : "";\n'
       '  const chips = cats.length > 1 ? `<div class="invcats" role="tablist">${[["", "All"], ...cats].map(([c, l]) => `<button role="tab" aria-selected="${c === sel}" class="${c === sel ? "on" : ""}" data-act="invCat" data-v="${c}"><i>${c ? SHOP_CI[c] || "✦" : "▦"}</i>${lab(l)}<em>${fmt(n(c))}</em></button>`).join("")}</div>` : "";\n'
       '  if (sel || cats.length < 2) return chips + `<div class="shopgrid">${inv.filter(k => !sel || catOf(k) === sel).map(card).join("")}</div>`;\n'
       '  return chips + cats.map(([c, l]) => `<div class="invsec"><h4><i>${SHOP_CI[c] || "✦"}</i>${lab(l)}<small>${fmt(n(c))}</small></h4><div class="shopgrid">${inv.filter(k => catOf(k) === c).map(card).join("")}</div></div>`).join(""); }')
s = s[:i] + new + s[j + len("'<p class=\"note\">Your inventory is empty. Items you buy, and spoils from pirate raids, land here.</p>'; }"):]
rep('  hullK: d => { G.hullK = d.k; render(true); },', '  hullK: d => { G.hullK = d.k; render(true); },\n  invCat: d => { G.invCat = d.v || ""; if (sheet) renderSheet(); else render(true); },')
rep('.hfp{flex-shrink:0;', '.invcats{flex-shrink:0;display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;margin:2px 0 12px;padding-bottom:2px}.invcats::-webkit-scrollbar{display:none}.invcats button{all:unset;flex:none;cursor:pointer;display:flex;align-items:center;gap:6px;font-size:12.5px;padding:7px 11px;border-radius:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);color:#cfe3ee}.invcats button.on{border-color:#55d6e8;color:#fff;background:rgba(85,214,232,.15)}.invcats i{font-style:normal;opacity:.85}.invcats em{font-style:normal;font-size:11px;padding:1px 6px;border-radius:8px;background:rgba(255,255,255,.08);color:#9fb6c4}\n'
    '.invsec{flex-shrink:0;display:flex;flex-direction:column;gap:8px;margin-bottom:16px}.invsec h4{margin:0;display:flex;align-items:center;gap:8px;font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:#7fe6f3}.invsec h4 i{font-style:normal;letter-spacing:0}.invsec h4 small{margin-left:auto;font-size:11px;letter-spacing:0;color:#9fb6c4}\n.hfp{flex-shrink:0;')

# ---- teleports: ◆200 to a chosen orbit, ◆100 random; a paid jump asks for a second tap ----
rep('const TELEPORT_SHARDS = 25, TELEPORT_CD = 24 * 3600e3;',
    'const TELEPORT_SHARDS = 200, TELEPORT_RAND = 100, TELEPORT_CD = 24 * 3600e3; /* v640 owner: aimed ◆200, random ◆100 (was ◆25 both) */\n'
    'const buyArmed = k => !!(G.buyArm && G.buyArm.k === k && Date.now() - G.buyArm.t < 8000);\n'
    'function armBuy(k, cost) { if (buyArmed(k)) { G.buyArm = null; return true; } G.buyArm = { k, t: Date.now() }; toast(`Tap again to spend ◆${fmt(cost)}.`); if (sheet) renderSheet(); else render(true);\n'
    '  setTimeout(() => { if (G.buyArm && G.buyArm.k === k && !buyArmed(k)) { G.buyArm = null; if (sheet) renderSheet(); else render(true); } }, 8100); return false; }')
rep('<button class="btn amber sm" data-act="teleport" data-pay="buy" data-id="${p.id}" data-tile="${loc.id}" ${shards >= TELEPORT_SHARDS && canPlay() ? "" : "disabled"}>Buy ◆${TELEPORT_SHARDS}</button>',
    '<button class="btn amber sm${buyArmed("tp|" + p.id + "|" + loc.id) ? " pxarm" : ""}" data-act="teleport" data-pay="buy" data-id="${p.id}" data-tile="${loc.id}" ${shards >= TELEPORT_SHARDS && canPlay() ? "" : "disabled"}>${buyArmed("tp|" + p.id + "|" + loc.id) ? "Confirm" : "Buy"} ◆${TELEPORT_SHARDS}</button>')
rep('<button class="btn amber sm" data-act="tpRandom" data-pay="buy" data-id="${p.id}" ${shards >= TELEPORT_SHARDS && canPlay() ? "" : "disabled"}>◆${TELEPORT_SHARDS}</button>',
    '<button class="btn amber sm${buyArmed("tpr|" + p.id) ? " pxarm" : ""}" data-act="tpRandom" data-pay="buy" data-id="${p.id}" ${shards >= TELEPORT_RAND && canPlay() ? "" : "disabled"}>${buyArmed("tpr|" + p.id) ? "Confirm " : ""}◆${TELEPORT_RAND}</button>')
rep('<button class="btn amber sm" data-act="teleport" data-pay="buy" data-id="${p.id}" data-tile="${e.id}" ${taken || !canPlay() || (S.shards || 0) < TELEPORT_SHARDS ? "disabled" : ""}>Buy ◆${TELEPORT_SHARDS}</button>',
    '<button class="btn amber sm${buyArmed("tp|" + p.id + "|" + e.id) ? " pxarm" : ""}" data-act="teleport" data-pay="buy" data-id="${p.id}" data-tile="${e.id}" ${taken || !canPlay() || (S.shards || 0) < TELEPORT_SHARDS ? "disabled" : ""}>${buyArmed("tp|" + p.id + "|" + e.id) ? "Confirm" : "Buy"} ◆${TELEPORT_SHARDS}</button>')
rep('<dl class="kv"><dt>Teleport</dt><dd>Ticket (${tickets} owned) or ◆${TELEPORT_SHARDS} · you have ◆${fmt(shards)}</dd></dl>',
    '<dl class="kv"><dt>Teleport</dt><dd>Ticket (${tickets} owned) or ◆${TELEPORT_SHARDS} to a chosen orbit, ◆${TELEPORT_RAND} for a random jump · you have ◆${fmt(shards)}</dd></dl>')
rep('Jump a planet to a random free orbit anywhere in the galaxy, in any layer. Same price and 24-hour recharge as a normal teleport.',
    'Jump a planet to a random free orbit anywhere in the galaxy, in any layer. Half the price of an aimed jump (◆${TELEPORT_RAND}, or a ticket); same 24-hour recharge.')
rep('  tpRandom: d => { const taken = tileTaken();',
    '  tpRandom: d => { if (d.pay === "buy") { if ((S.shards || 0) < TELEPORT_RAND) return toast(`A random jump costs ◆${TELEPORT_RAND}.`, "warn"); if (!armBuy("tpr|" + d.id, TELEPORT_RAND)) return; } const taken = tileTaken();')
rep('ACT.teleport({ id: d.id, tile: e.id, pay: d.pay }); return;', 'ACT.teleport({ id: d.id, tile: e.id, pay: d.pay, rnd: 1 }); return;')
rep('''    const tk = (S.items || {}).teleport > 0, sh = (S.shards || 0) >= TELEPORT_SHARDS;
    if (d.pay === "ticket") { if (!tk) return toast("You have no Teleport Tickets. Buy one in the Void Shop or pay with shards.", "warn"); S.items.teleport--; }
    else if (d.pay === "buy") { if (!sh) return toast(`That jump costs ◆${TELEPORT_SHARDS}.`, "warn"); S.shards -= TELEPORT_SHARDS; }
    else if (tk) S.items.teleport--; else if (sh) S.shards -= TELEPORT_SHARDS; else return toast(`Teleporting needs a Teleport Ticket or ◆${TELEPORT_SHARDS}.`, "warn");''',
'''    const cost = d.rnd ? TELEPORT_RAND : TELEPORT_SHARDS, tk = (S.items || {}).teleport > 0, sh = (S.shards || 0) >= cost;
    if (!d.rnd && (d.pay === "buy" || (d.pay !== "ticket" && !tk)) && sh && !armBuy("tp|" + d.id + "|" + d.tile, cost)) return; /* v640 a paid jump asks for a second tap (the random one asked in tpRandom) */
    if (d.pay === "ticket") { if (!tk) return toast("You have no Teleport Tickets. Buy one in the Void Shop or pay with shards.", "warn"); S.items.teleport--; }
    else if (d.pay === "buy") { if (!sh) return toast(`That jump costs ◆${cost}.`, "warn"); S.shards -= cost; }
    else if (tk) S.items.teleport--; else if (sh) S.shards -= cost; else return toast(`Teleporting needs a Teleport Ticket or ◆${cost}.`, "warn");''')
rep('const GAME_V = 639', 'const GAME_V = 640')
open(p, 'w', encoding='utf-8').write(s)
