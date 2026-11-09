# v376: the Finder is only boxes. New boxes: Hive Worlds (raid Hive-held planets: a new list in the finder, r = "h") and Events
# (the Cube and every other event, opens the Events hub), plus Void Layers as a wide box (the guide had lived in the removed list).
# The tour covers the new boxes; a player who saw the old tour (S.fTour 1) gets just the new boxes once (S.fTour 2 = all seen).
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:90]); t = t.replace(a, b)

# Finder tab: the boxes only
i = t.index('    body = `${finderTiles(T, h)}<h2 class="sec fnear">'); j = t.index('`;', i)
assert 'Worlds</h2>' in t[i:j] and j - i < 3000
t = t[:i] + '    body = finderTiles(T, h);' + t[j + 2:]
rep('    const cand = G.list.filter(p => ["hive", "player", "razed"].includes(pStatus(p, T)) && !(p.owner && isAlly(p.owner)) && !isFogged(p, T));\n', '')
rep("!S.fTour && !G.ftQ && !$(\"#ftour\")", "(S.fTour || 0) < 2 && !G.ftQ && !$(\"#ftour\")")
rep("sub.gal === \"targets\" && !S.fTour && !$(\"#ftour\") && !advLines) finderTour(0); }, 700); }",
    "sub.gal === \"targets\" && (S.fTour || 0) < 2 && !$(\"#ftour\") && !advLines) finderTour(0, S.fTour === 1); }, 700); }")
# boxes
rep('''    d: G.list.filter(p => p.debris && (p.debris.m || 0) + (p.debris.c || 0) > 0 && ready(p)).length };''',
    '''    d: G.list.filter(p => p.debris && (p.debris.m || 0) + (p.debris.c || 0) > 0 && ready(p)).length, h: G.list.filter(p => pStatus(p, T) === "hive" && ready(p)).length };
  let evN = 0; try { for (const e of EVS) if (e[0] !== "gifts" || myAlly()) evN += evCount(e[0]) || 0; } catch (e) {} const evLive = (() => { try { return evActive(T) || gwLive(T); } catch (e) { return false; } })();''')
rep('''["q", "■", "Boss Cubes", "Giant bosses. Team up with friends", "#5dff6a", "Team"],''',
    '''["h", "⬢", "Hive Worlds", "Raid planets the Hive took over", "#f0a945", "Raid"], ["ev", "🏆", "Events", "The Cube and other prize events", "#c9a6ff", "Prizes", "events"],
    ["q", "■", "Boss Cubes", "Giant bosses. Team up with friends", "#5dff6a", "Team"],''')
rep('''["o", "⌖", "Coordinates", "Find any spot and jump there", "#5dffa8", "Travel"]];''',
    '''["o", "⌖", "Coordinates", "Find any spot and jump there", "#5dffa8", "Travel"], ["ly", "◎", "Void Layers", `Harder and richer toward the Core${h ? " · you're in " + zoneOf(h.r) : ""}`, "#c94ad6", "Guide", "layers", 1]];''')
rep('''return `<div class="ftiles">${L.map(([r, ic, nm, d, c, tag]) => `<button class="ftile" data-ft="${r}" data-act="find" data-r="${r}" style="--fc:${c}"><span class="fi">${ic}</span><b>${nm}</b><small>${d}</small><span class="fb">${n[r] ? `${n[r] > 99 ? "99+" : n[r]} found` : r === "o" ? "Jump" : "Explore"}</span><i class="ftag">${tag}</i></button>`).join("")}</div>`; }''',
    '''const badge = r => r === "ev" ? (evN ? `${evN} to claim` : evLive ? "Live!" : "See all") : r === "ly" ? "Guide" : n[r] ? `${n[r] > 99 ? "99+" : n[r]} found` : r === "o" ? "Jump" : "Explore";
  return `<div class="ftiles">${L.map(([r, ic, nm, d, c, tag, act, wide]) => `<button class="ftile${wide ? " fwide" : ""}${r === "ev" && (evN || evLive) ? " fhot" : ""}" data-ft="${r}" data-act="${act || "find"}" data-r="${r}" style="--fc:${c}"><span class="fi">${ic}</span><b>${nm}</b><small>${d}</small><span class="fb">${badge(r)}</span><i class="ftag">${tag}</i></button>`).join("")}</div>`; }''')
# tour: new steps, a short version for players who saw the old one
rep('''  ['[data-ft="q"]', "Cubes are giant bosses. Team up with friends to beat one."],
  [".fnear", "Down here are the best picks near you right now. Tap one and go!"],''',
    '''  ['[data-ft="q"]', "Cubes are giant bosses. Team up with friends to beat one."],
  ['[data-ft="h"]', "Hive Worlds are planets the Hive took over. Raid them for big piles of resources.", 1],
  ['[data-ft="ev"]', "Events are special battles and contests, like the Cube. Come here for prizes!", 1],
  ['[data-ft="ly"]', "The galaxy has layers. The closer to the Core, the tougher the fights and the bigger the rewards.", 1],''')
rep('''function finderTour(i) { let w = $("#ftour");''', '''const FTOUR_NEW = ["Your Finder has new boxes! Let me show you."];
function finderTour(i, upd) { let w = $("#ftour"); if (i === 0 && !w) G.ftSteps = upd ? [[".ftiles", FTOUR_NEW[0]]].concat(FTOUR.filter(s => s[2]), [FTOUR[FTOUR.length - 1]]) : FTOUR; const FTOUR_ = G.ftSteps || FTOUR;''')
# inside finderTour/ftPlace use the active list
i = t.index('function finderTour(i, upd)'); j = t.index('function ftPlace()', i); k = t.index('\n', t.index('c.style.bottom = "calc(14px', j))
seg = t[i:k]; head = seg[:seg.index('const FTOUR_ = G.ftSteps || FTOUR;') + len('const FTOUR_ = G.ftSteps || FTOUR;')]; rest = seg[len(head):]
rest = rest.replace('FTOUR.length', 'FTOUR_.length').replace('FTOUR[', 'FTOUR_[').replace('FTOUR.map', 'FTOUR_.map')
rest = rest.replace('function ftPlace() { const w = $("#ftour");', 'function ftPlace() { const w = $("#ftour"), FTOUR_ = G.ftSteps || FTOUR;')
rest = rest.replace('if (i >= FTOUR_.length && S) { S.fTour = 1;', 'if (i >= FTOUR_.length && S) { S.fTour = 2;')
assert 'S.fTour = 2;' in rest and 'FTOUR_ = G.ftSteps || FTOUR;' in rest, rest[:300]
t = t[:i] + head + rest + t[k:]
rep('fTourSkip: () => finderTour(FTOUR.length),', 'fTourSkip: () => finderTour((G.ftSteps || FTOUR).length),')
rep('fTour: () => { if (S) S.fTour = 0; sub.gal = "targets";', 'fTour: () => { sub.gal = "targets";')
# the hint and pulse key off "seen any tour"
rep('<button class="tbtn${S && S.fTour ? "" : " fnew"}"', '<button class="tbtn${S && S.fTour >= 2 ? "" : " fnew"}"')
# Hive Worlds list
rep('''  if (r === "s") { // v135: Void Shard Mines''', '''  if (r === "h") { /* v376 Hive Worlds: planets the Hive holds, nearest first, with what a raid carries home */
    const hv = G.list.filter(p => pStatus(p, T) === "hive" && !isFogged(p, T)).sort((a, b) => dist(a) - dist(b)).slice(0, 12);
    return `<div class="hd"><div><div class="chapter" style="color:#f0a945">🔭 Finder</div><h2>Hive Worlds</h2><p class="note">Planets the Hive took over. Beat the garrison and your ships carry home half of what's stored there. Nearest to ${esc(h ? h.name : S.homeName)} first.</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
      <div class="list">${hv.map(p => `<button class="tgt" data-act="planet" data-id="${p.id}"><span class="lvl" style="color:#f0a945;border-color:#f0a945">${p.lvl}</span><span><span class="nm">⬢ ${esc(p.name)}</span><br><span class="sub">~${fmt(total(stock(p.lvl)) / 2)} loot · ${h ? ftime(travelMs(h, p, { fighter: 1 })) : "–"} by Light Fighter</span></span><span class="pill amb">Raid</span></button>`).join("") || '<p class="note">No Hive worlds charted near you yet. Build a Radar Station or explore to find more.</p>'}</div>
      <button class="btn ghost wide" data-act="findClear">Clear highlight</button>`; }
  if (r === "s") { // v135: Void Shard Mines''')
css = '''
/* v376 Finder: wide box, live badge */
.ftile.fwide{grid-column:1/-1;min-height:84px}.ftile.fhot .fb{background:var(--fc);color:#120a1e;animation:fbHot 1.4s ease-in-out infinite}@keyframes fbHot{50%{box-shadow:0 0 12px var(--fc)}}
'''
i = t.index('</style>', t.index('.fshero{')); t = t[:i] + css + t[i:]
open(p, "w").write(t)
# a closed panel stops the tour without counting it as seen; the tour follows the grid order (Hive, Events, then Cubes)
t = open(p).read()
def rep2(a, b):
    global t; assert t.count(a) == 1, a[:80]; t = t.replace(a, b)
rep2('if (!sheet || sheet.type !== "targets") return finderTour(99);', 'if (!sheet || sheet.type !== "targets") return finderTour(-1);')
rep2('if (i >= FTOUR_.length || !sheet || sheet.type !== "targets") { if (w) w.remove();', 'if (i < 0 || i >= FTOUR_.length || !sheet || sheet.type !== "targets") { if (w) w.remove();')
q = '''  ['[data-ft="q"]', "Cubes are giant bosses. Team up with friends to beat one."],\n'''
rep2(q, ''); rep2('''  ['[data-ft="ly"]''', q + '''  ['[data-ft="ly"]''')
open(p, "w").write(t)
