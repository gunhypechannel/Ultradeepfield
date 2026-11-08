# v338: previews must match payouts. The pirate/monster/Cube card promised more Void Shards than a win pays (e.g. a Lv.15 pirate
# showed ◆3, pays ◆1), and the pyramid card promised runes (gone since v79) and the wrong shard count. One formula each now feeds both.
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep('''    { const sh = x.boss ? 1 + Math.floor(x.lvl / 5) : x.mon ? Math.floor(x.lvl / 6) : x.lvl >= 10 ? 1 : 0; /* v80: shards are scarce (Game of War gold, OGame Dark Matter) */''',
    '''    { const sh = xShards(x); /* v80: shards are scarce (Game of War gold, OGame Dark Matter); v338: one formula for the card and the payout */''')
rep('const xLoot0 = x =>', 'const xShards = x => x.boss ? 1 + Math.floor(x.lvl / 5) : x.mon ? Math.floor(x.lvl / 6) : x.lvl >= 10 ? 1 : 0; /* v338 */\nconst pyrShards = L => Math.max(1, Math.floor(L / 3));\nconst xLoot0 = x =>')
rep('''<dd>${costHTML(L)} + ◆${x.mon ? 2 + Math.floor(x.lvl / 4) : x.boss ? 3 + Math.floor(x.lvl / 3) : 1 + Math.floor(x.lvl / 6)}''', '''<dd>${costHTML(L)}${xShards(x) ? ` + ◆${xShards(x)}` : ""}''')
rep('''const sh = Math.max(1, Math.floor(y.lvl / 3)); S.shards = (S.shards || 0) + sh;''', '''const sh = pyrShards(y.lvl); S.shards = (S.shards || 0) + sh;''')
rep('''<dd>${costHTML(L)} + ◆${1 + Math.floor(y.lvl / 2)} · runes · a chance of items''', '''<dd>${costHTML(L)} + ◆${pyrShards(y.lvl)} · a chance of items''')
rep('''  else if (!Object.keys(avail).length) body = `${originBar()}<p class="note">No ships at ${esc(h ? h.name : S.homeName)}.</p>`;
  else { const cap = cargoOf(sel);
    body = `<h2 class="sec">Expedition</h2>''', '''  else if (!Object.keys(avail).length) body += `${originBar()}<p class="note">No ships at ${esc(h ? h.name : S.homeName)}.</p>`;
  else { const cap = cargoOf(sel);
    body += `<h2 class="sec">Expedition</h2>''')
open(p, 'w', encoding='utf-8').write(t); print('ok')
