# v373: the Finder. The galaxy "Targets" page becomes the Finder: big friendly boxes for everything outside the base
# (gather, pirates, monsters, treasure stations, boss cubes, shard mines, salvage, coordinates), then the best picks near you.
# The Advisor walks a new player through it once (spotlight tour, replay with ?), and points at the Finder button on the map.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:90]); t = t.replace(a, b)

# map button
rep('<button class="tbtn" data-act="targets">Targets</button>',
    '<button class="tbtn${S && S.fTour ? "" : " fnew"}" data-act="targets" aria-label="Finder: find loot, pirates, monsters and treasure"><span class="tbi">🔭</span>Finder</button>')
# sheet header
rep('''function shTargets() {
  return `<div class="hd"><div><div class="chapter" style="color:var(--cyan)">Galaxy</div><h2>Targets and worlds</h2></div><button class="x" data-act="close" aria-label="Close">✕</button></div>${vGalaxyBelow()}`;
}''', '''function shTargets() { const fd = sub.gal === "targets";
  return `<div class="hd"><div><div class="chapter" style="color:var(--cyan)">${fd ? "🔭 Finder" : "Galaxy"}</div><h2>${fd ? "Everything out in space" : "Targets and worlds"}</h2>${fd ? '<p class="note">Loot, pirates, monsters and treasure. Tap a box to find the closest ones.</p>' : ""}</div><div class="fhdb">${fd ? '<button class="x fhelp" data-act="fTour" aria-label="Show me how the Finder works">?</button>' : ""}<button class="x" data-act="close" aria-label="Close">✕</button></div></div>${vGalaxyBelow()}`;
}
/* v373 the Finder's boxes: one per kind of thing to do outside the base, with how many are charted near you */
function finderTiles(T, h) { const ready = x => !isFogged(x, T);
  const n = { m: NODES.filter(x => x.res !== "s" && ready(x) && !occOf(x.id, T)).length, x: PIRATES.filter(x => !x.boss && !x.mon && pirDown(x) <= T && ready(x)).length,
    w: PIRATES.filter(x => x.mon && pirDown(x) <= T && ready(x)).length, y: PYRAMIDS.filter(y => pyrDown(y) <= T && ready(y)).length,
    q: PIRATES.filter(x => x.boss && !x.mon && pirDown(x) <= T && ready(x)).length, s: NODES.filter(x => x.res === "s" && ready(x) && !shardRest(x)).length,
    d: G.list.filter(p => p.debris && (p.debris.m || 0) + (p.debris.c || 0) > 0 && ready(p)).length };
  const L = [["m", "⛏", "Gather", "Free metal, crystal and gas for your base", "#5dff9a", "Easy"], ["x", "☠", "Pirates", "Beat them and keep their loot", "#ff6b5a", "Fight"],
    ["w", "🦈", "Monsters", "Hunt space beasts for rare treasure", "#7fd4ff", "Tough"], ["y", "▲", "Treasure", "Open old space station vaults", "#ffd36b", "Explore"],
    ["q", "■", "Boss Cubes", "Giant bosses. Team up with friends", "#5dff6a", "Team"], ["s", "◆", "Shard Mines", "Dig up rare Void Shards", NODE_T.s.col, "Rare"],
    ["d", "♻", "Salvage", "Scoop up wreckage after battles", "#9fe8d8", "Easy"], ["o", "⌖", "Coordinates", "Find any spot and jump there", "#5dffa8", "Travel"]];
  return `<div class="ftiles">${L.map(([r, ic, nm, d, c, tag]) => `<button class="ftile" data-ft="${r}" data-act="find" data-r="${r}" style="--fc:${c}"><span class="fi">${ic}</span><b>${nm}</b><small>${d}</small><span class="fb">${n[r] ? `${n[r] > 99 ? "99+" : n[r]} found` : r === "o" ? "Jump" : "Explore"}</span><i class="ftag">${tag}</i></button>`).join("")}</div>`; }
/* v373 the Advisor's first walk through the Finder: a spotlight on each part, her line beside it, Next or tap anywhere */
const FTOUR = [[".ftiles", "This is your Finder! Everything you need outside your base is right here."],
  ['[data-ft="m"]', "Need metal, crystal or gas? Tap Gather. Your cargo ships bring it home for free."],
  ['[data-ft="x"]', "Pirates hide loot. Beat them and the loot is yours!"],
  ['[data-ft="w"]', "Space monsters are tough, but they drop rare treasure."],
  ['[data-ft="y"]', "Old space stations have treasure vaults. Send ships to open them."],
  ['[data-ft="q"]', "Cubes are giant bosses. Team up with friends to beat one."],
  [".fnear", "Down here are the best picks near you right now. Tap one and go!"],
  [".fhelp", "Find the Finder button on the map any time. Tap the question mark to see this again."]];
function finderTour(i) { let w = $("#ftour");
  if (i >= FTOUR.length || !sheet || sheet.type !== "targets") { if (w) w.remove(); clearInterval(G.ftI); G.ftI = 0; if (i >= FTOUR.length && S) { S.fTour = 1; dirty(); const b = $(".tbtn"); if (b) b.classList.remove("fnew"); } voiceStop(); return; }
  if (sub.gal !== "targets") { sub.gal = "targets"; renderSheet(); }
  const el = $(FTOUR[i][0]); if (!el) return finderTour(i + 1);
  try { const sc = el.closest(".sheet"); if (sc) { const r = el.getBoundingClientRect(), sr = sc.getBoundingClientRect(); sc.scrollTo({ top: sc.scrollTop + Math.round(r.top + r.height / 2 - (sr.top + sr.height * .42)), behavior: "instant" }); } } catch (e) {} /* only the panel scrolls, never the page */
  if (!w) { w = document.createElement("div"); w.id = "ftour"; w.setAttribute("data-act", "fTourNext");
    w.innerHTML = `<div class="ftspot"></div><div class="ftcard" role="dialog" aria-live="polite" aria-label="${ADV} shows you the Finder"><img src="${ADV_ART}" alt=""><div class="fttx"><b>${ADV}</b><p></p><div class="ftnav"><span class="ftdots"></span><button class="btn ghost sm" data-act="fTourSkip">Skip</button><button class="btn sm ftgo" data-act="fTourNext"></button></div></div></div>`;
    $("#app").appendChild(w); G.ftI = setInterval(ftPlace, 250); }
  w.dataset.i = i; w.querySelector(".fttx p").textContent = FTOUR[i][1]; w.querySelector(".ftgo").textContent = i === FTOUR.length - 1 ? "Got it!" : "Next ›";
  w.querySelector(".ftdots").innerHTML = FTOUR.map((_, k) => `<i class="${k === i ? "on" : ""}"></i>`).join(""); speak(FTOUR[i][1]); ftPlace(); setTimeout(ftPlace, 60); }
function ftPlace() { const w = $("#ftour"); if (!w) { clearInterval(G.ftI); G.ftI = 0; return; } if (!sheet || sheet.type !== "targets") return finderTour(99);
  const el = $(FTOUR[+w.dataset.i][0]); if (!el) return; const r = el.getBoundingClientRect(), p = 7, s = w.querySelector(".ftspot"), c = w.querySelector(".ftcard"), H = innerHeight, ch = c.offsetHeight;
  s.style.left = (r.left - p) + "px"; s.style.top = (r.top - p) + "px"; s.style.width = (r.width + 2 * p) + "px"; s.style.height = (r.height + 2 * p) + "px";
  const below = H - r.bottom - p - 14, above = r.top - p - 14;
  if (below >= ch) { c.style.top = (r.bottom + p + 12) + "px"; c.style.bottom = "auto"; } else if (above >= ch) { c.style.top = "auto"; c.style.bottom = (H - r.top + p + 12) + "px"; } else { c.style.top = "auto"; c.style.bottom = "calc(14px + env(safe-area-inset-bottom,0px))"; } }''')
# tabs
rep('data-v="targets">Targets</button>', 'data-v="targets">🔭 Finder</button>')
# Finder tab body: boxes first, then the best picks near you
rep('''    body = `<button class="tgt" data-act="layers"><span class="lvl" style="color:#c94ad6;border-color:#c94ad6">6</span>''',
    '''    if (!S.fTour && !G.ftQ && !$("#ftour") && !advLines && !$("#adv") && !$("#celeb") && !(tutOn() && (TUT[S.tut.i] || {}).find)) { G.ftQ = 1; setTimeout(() => { G.ftQ = 0; if (sheet && sheet.type === "targets" && sub.gal === "targets" && !S.fTour && !$("#ftour") && !advLines) finderTour(0); }, 700); }
    body = `${finderTiles(T, h)}<h2 class="sec fnear">⭐ Best picks near you</h2><button class="tgt" data-act="layers"><span class="lvl" style="color:#c94ad6;border-color:#c94ad6">6</span>''')
rep('<button class="btn ghost wide" data-act="find" data-r="x">All pirate hideouts</button>',
    '<button class="btn ghost wide" data-act="find" data-r="x">☠ More pirate hideouts ›</button>')
# names
rep('targets: "targets"', 'targets: "Finder"'); rep('find: "search"', 'find: "Finder"')
n0 = t.count('>Locator</div>'); t = t.replace('>Locator</div>', '>🔭 Finder</div>'); assert n0 >= 5, n0
rep('">Resource finder</div>', '">🔭 Finder · gather</div>')
# actions
rep('  targets: () => { sub.gal = sub.gal || "targets"; openSheet({ type: "targets" }); },',
    '''  targets: () => { sub.gal = sub.gal || "targets"; openSheet({ type: "targets" }); },
  fTour: () => { if (S) S.fTour = 0; sub.gal = "targets"; if (!sheet || sheet.type !== "targets") openSheet({ type: "targets" }); finderTour(0); },
  fTourNext: () => { const w = $("#ftour"); finderTour(w ? +w.dataset.i + 1 : 99); },
  fTourSkip: () => finderTour(FTOUR.length),''')
# first time on the map after the Academy: she points at the Finder button
rep('''  updateVbtn();
}
/* rename and reskin any planet you hold */''', '''  updateVbtn();
  if (S && !S.fTour && !S.fHint && G.ready && !sheet && !battle && !advLines && !$("#adv") && !$("#celeb") && !$("#advh.on") && !tutOn()) { S.fHint = 1; dirty(); setTimeout(() => { if (view === "galaxy" && !sheet && !advLines) advHolo("Tap the Finder button to find loot, pirates, monsters and treasure!"); }, 900); }
}
/* rename and reskin any planet you hold */''')
# styles
css = '''
/* v373 the Finder */
.tbtn{display:inline-flex;align-items:center;gap:6px}.tbtn .tbi{font-size:16px;line-height:1}
.tbtn.fnew{animation:tbPulse 1.6s ease-in-out infinite}@keyframes tbPulse{0%,100%{box-shadow:0 6px 20px rgba(85,214,232,.25),0 0 0 0 rgba(85,214,232,.6)}50%{box-shadow:0 6px 20px rgba(85,214,232,.35),0 0 0 9px rgba(85,214,232,0)}}
.fhdb{display:flex;gap:6px;flex:none}.sheet .x.fhelp{color:var(--cyan);border-color:var(--cyan);font-family:var(--f-display);font-weight:700}
.ftiles{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0 6px}@media (min-width:640px){.ftiles{grid-template-columns:repeat(4,1fr)}}
.ftile{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:3px;padding:12px 12px 30px;min-height:112px;border-radius:14px;border:1px solid color-mix(in srgb,var(--fc) 60%,transparent);background:linear-gradient(160deg,color-mix(in srgb,var(--fc) 20%,#0a1826),#06101b 80%);color:#eaf6ff;text-align:left;cursor:pointer;box-shadow:inset 0 0 18px color-mix(in srgb,var(--fc) 16%,transparent);font:inherit}
.ftile:active{transform:scale(.97)}.ftile .fi{font-size:28px;line-height:1;color:var(--fc);filter:drop-shadow(0 0 6px color-mix(in srgb,var(--fc) 70%,transparent))}
.ftile b{font-family:var(--f-display);font-size:16px;letter-spacing:.04em;margin-top:4px}.ftile small{font-size:12.5px;color:#a9c4d6;line-height:1.3}
.ftile .fb{position:absolute;top:9px;right:9px;font-family:var(--f-display);font-size:10.5px;letter-spacing:.07em;text-transform:uppercase;padding:2px 8px;border-radius:999px;border:1px solid var(--fc);color:var(--fc);background:rgba(4,12,20,.6)}
.ftile .ftag{position:absolute;left:12px;bottom:9px;font-style:normal;font-family:var(--f-display);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#04121c;background:var(--fc);padding:1px 7px;border-radius:5px}
#ftour{position:fixed;inset:0;z-index:300;cursor:pointer}
#ftour .ftspot{position:fixed;border-radius:16px;border:2px solid #7fe9ff;box-shadow:0 0 0 9999px rgba(2,8,16,.72),0 0 22px rgba(127,233,255,.7);transition:left .3s,top .3s,width .3s,height .3s;pointer-events:none;animation:ftGlow 1.4s ease-in-out infinite}
@keyframes ftGlow{50%{border-color:#fff;box-shadow:0 0 0 9999px rgba(2,8,16,.72),0 0 34px rgba(127,233,255,.95)}}
#ftour .ftcard{position:fixed;left:max(10px,env(safe-area-inset-left,0px));right:max(10px,env(safe-area-inset-right,0px));margin:0 auto;max-width:520px;display:flex;gap:10px;align-items:flex-end;padding:10px 12px;border-radius:16px;border:1px solid #57dcff;background:linear-gradient(180deg,rgba(14,44,66,.97),rgba(6,20,34,.98));box-shadow:0 10px 30px rgba(0,0,0,.5),0 0 18px rgba(70,200,255,.3);cursor:default}
#ftour .ftcard img{width:64px;height:84px;object-fit:cover;object-position:50% 12%;border-radius:10px;flex:none;filter:drop-shadow(0 0 8px rgba(90,210,255,.6))}
#ftour .fttx{flex:1;min-width:0}#ftour .fttx b{font-family:var(--f-display);font-size:12px;letter-spacing:.14em;color:#7fe9ff;text-transform:uppercase}#ftour .fttx p{margin:3px 0 8px;font-size:16px;line-height:1.35;color:#f2fbff}
#ftour .ftnav{display:flex;align-items:center;gap:8px}#ftour .ftdots{flex:1;display:flex;gap:4px}#ftour .ftdots i{width:7px;height:7px;border-radius:50%;background:rgba(127,233,255,.25)}#ftour .ftdots i.on{background:#7fe9ff}
.sbkb{background:rgba(8,22,34,.94)}
'''
rep('</style>', css + '</style>', t.count('</style>')) if t.count('</style>') == 1 else None
if css not in t:
    i = t.index('</style>'); t = t[:i] + css + t[i:]
open(p, "w").write(t)
