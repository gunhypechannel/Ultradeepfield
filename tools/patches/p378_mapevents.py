# v378: the Finder's Events box opens Map Events: the Cube (fly to it) and drifting salvage pods (fly to one, tap to haul in),
# with room for future map events; the Events hub (rewards and rankings) is a button at the bottom.
p = "docs/index.html"; t = open(p).read()
def rep(a, b):
    global t; assert t.count(a) == 1, a[:90]; t = t.replace(a, b)
rep('["ev", "🏆", "Events", "The Cube and other prize events", "#c9a6ff", "Prizes", "events"],',
    '["ev", "🏆", "Events", "The Cube and other map events", "#c9a6ff", "Map"],')
rep('''const badge = r => r === "ev" ? (evN ? `${evN} to claim` : evLive ? "Live!" : "See all")''',
    '''const pods = (S.caches || []).filter(c => c.until > T).length;
  const badge = r => r === "ev" ? (evLive ? "Live!" : pods ? `${pods} pod${pods > 1 ? "s" : ""}` : evN ? `${evN} to claim` : "See all")''')
rep('''  if (r === "h") { /* v376 Hive Worlds''', '''  if (r === "ev") { /* v378 Map Events: things happening out on the map right now. New map events add a row here. */
    const live = evActive(T), cubeSub = live ? `Live now · ends in ${ftime(evStart(evWeek(T)) + EV_DUR - T)}` : `Next battle in ${ftime(evStart(evWeek(T) + 1) - T)} · every Friday`;
    const pods = (S.caches || []).filter(c => c.until > T).sort((a, b) => a.until - b.until);
    return `<div class="hd"><div><div class="chapter" style="color:#c9a6ff">🔭 Finder</div><h2>Map Events</h2><p class="note">Things happening out on the map. Tap one to fly there.</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
      <h2 class="sec">Weekly battle</h2><div class="list"><button class="tgt mev${live ? " mlive" : ""}" data-act="nexus"><span class="lvl" style="color:#c9a6ff;border-color:#c9a6ff">■</span><span><span class="nm">Battle for the Cube</span><br><span class="sub">${cubeSub}</span><br><span class="sub">Alliances fight to hold the giant Cube. Hold it longest to win.</span></span><span class="pill ${live ? "bad" : "go"}">${live ? "Live!" : "Fly there"}</span></button></div>
      <h2 class="sec">Drifting salvage</h2><div class="list">${pods.map(c => `<button class="tgt" data-act="podGo" data-id="${c.id}"><span class="lvl" style="color:${CACHE_T[c.kind][1]};border-color:${CACHE_T[c.kind][1]}">◇</span><span><span class="nm">${CACHE_T[c.kind][0]}</span><br><span class="sub">Free loot · gone in ${ftime(c.until - T)}</span></span><span class="pill ok">Go</span></button>`).join("") || '<p class="note">No salvage drifting near your worlds right now. New pods turn up every few minutes.</p>'}</div>
      <div class="mevsoon"><b>More map events are on the way</b><span>When a new one starts, it shows up right here.</span></div>
      <button class="btn ghost wide" data-act="events">🏆 Event rewards &amp; rankings</button>
      <button class="btn ghost wide" data-act="findClear">Clear highlight</button>`; }
  if (r === "h") { /* v376 Hive Worlds''')
rep('  grabCache: d => act(() => {', '''  podGo: d => { const c = (S.caches || []).find(x => x.id === d.id); if (!c) { toast("That pod drifted away."); renderSheet(); return; } closeSheet(); if (view !== "galaxy") { view = "galaxy"; render(); }
    let tries = 0; const fly = () => { const o = G3 && G3.cacheO && G3.cacheO.get(d.id); if (!G3 || !G3.cam || !o) { if (tries++ < 40) setTimeout(fly, 100); return; } G3.cam.followFleet = null; G3.cam.follow = null; const q = o.grp.position; G3.cam.goal = { tx: q.x, ty: q.y + 6, tz: q.z, dist: 110 }; };
    fly(); setTimeout(fly, 300); toast("Tap the glowing pod to haul it in!"); },
  grabCache: d => act(() => {''')
css = '''
/* v378 Map Events */
.tgt.mev.mlive{border-color:#c9a6ff;box-shadow:0 0 16px rgba(201,166,255,.35)}.mevsoon{flex:none;margin:12px 0;padding:12px 14px;border:1px dashed rgba(201,166,255,.5);border-radius:12px;display:flex;flex-direction:column;gap:3px;background:rgba(201,166,255,.05)}.mevsoon b{font-family:var(--f-display);letter-spacing:.05em;color:#d9c6ff}.mevsoon span{font-size:12.5px;color:var(--muted)}
'''
i = t.index('</style>', t.index('.fshero{')); t = t[:i] + css + t[i:]
open(p, "w").write(t)
