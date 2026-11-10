# v385: the Advisor is your go-to for everything. (1) She announces the galaxy's big moments live, with a Watch / Open button:
# the Battle for the Super Cube (start, siege, finale, end), Galaxy War, the world bosses' return, a boss under attack right now,
# a conduit falling, the Overlord's shield going down and each boss's fall. (2) Etc › How to play gets a searchable FAQ: every
# answer opens on tap and the Advisor speaks it.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:90]); t = t.replace(a, b)

FAQ = [
 ("Getting started", [
  ("What should I do first?", "Build your metal, crystal and gas extractors and solar power, then follow the quests on the Quests tab. I'll always point to the next step on your path, so you're never stuck."),
  ("What is the Academy?", "The Academy is your guided start. Each step teaches one system, from building your first extractor to winning your first battles, and pays a reward. Finish it and the whole galaxy opens up."),
  ("Does my empire grow while I'm away?", "Yes. Your extractors keep producing, and your building, research and shipyard queues keep running while you're offline, up to your storage limits."),
  ("Am I safe as a new commander?", "For your first three days, or until you reach 300 score, other commanders can't attack your colonies. Use that time to learn against the Hive and build your defenses."),
 ]),
 ("Resources and buildings", [
  ("What are the resources for?", "Metal and crystal build almost everything. Gas fuels your flights and advanced technology. Energy from solar and fusion plants keeps your extractors running at full speed."),
  ("Why is my production low?", "Check your energy. When your plants make less energy than your extractors need, every extractor slows down. Build more solar or a fusion reactor, and raise your storage so nothing overflows."),
  ("What are Void Shards?", "Void Shards are the rare currency. You earn them from bosses, pyramid vaults, shard mines and events, and spend them in the Void Shop on boosters, accelerators, items and VIP."),
  ("How do I get more planets?", "Research Astrophysics. Every two levels lets you hold one more world, up to ten. Then send a Colony Ship to settle or capture one. A new planet is shielded for seven days."),
 ]),
 ("Fleet and combat", [
  ("How do battles work?", "A battle lasts up to eight rounds. Every ship fires its own weapons; shields soak damage first, then armor and hull take the rest. You can watch every fight as a replay from Mail."),
  ("Which ships should I build?", "Every ship has a counter. Cruisers beat light fighters, dreadnoughts beat battleships, bombers beat defenses, destroyers beat dreadnoughts, and reapers beat capital ships. Mix your fleet."),
  ("What happens to ships I lose?", "Repair docks recover thirty percent of the ships you lose in any battle, and seventy percent of destroyed defenses are rebuilt. A bad fight hurts, but it won't end your empire."),
  ("Why can't I send another fleet?", "All your fleet slots are busy. Research Fleet Command, settle more colonies, or wait for a fleet to come home. Every colony adds a slot."),
  ("Why do flights cost gas?", "Every flight burns gas, more for long trips and heavy ships. Flying slower saves a lot of fuel, and the Coalition Depot cuts the fuel for every flight."),
  ("How do I spy on a planet?", "Build espionage probes, then tap Espionage on the planet's card. More probes reveal more: the fleet, then defenses, buildings and research. Better Espionage Technology helps too."),
  ("What is a joint strike?", "A joint strike lets allies attack together. Start one on a strong target, your allies join before the timer runs out, and every fleet fights as one."),
 ]),
 ("The map", [
  ("What is the Finder?", "The Finder is your map search. Tap a box, like pirates, Hive worlds, mines or map events, and I'll highlight the nearest targets for you."),
  ("What are the layers?", "The galaxy has six layers around the black hole. Each layer inward has stronger enemies and richer rewards. New commanders start in the outer layers."),
  ("What are pirate hideouts?", "Pirate hideouts are full of stolen cargo. Beat the crew and your holds fill with their loot. They regroup after a raid, so come back later."),
  ("What are pyramid stations?", "Derelict pyramid stations hold vaults of resources, shards and items. You can loot each one once a day, and from level three something still guards the halls."),
  ("How do Void Shard mines work?", "Shard mines are rare fields that pay Void Shards. A dig is slow, each mine rests for a day after your dig, and you can mine up to five shards a day."),
  ("What are space monsters?", "Space monsters roam the map. Slay them for resources, shards and time accelerators that speed up your queues."),
  ("What are Assimilation Cubes?", "Assimilation Cubes are fortresses. One fleet rarely breaks them, so call a joint strike. They drop runes and the rarest forge materials."),
  ("What is cinematic view?", "Tap Cinematic view on a target's card and the camera flies around it. Drag to look around, and switch the angles at the bottom. World bosses get a full scan."),
 ]),
 ("Events", [
  ("What is the Battle for the Super Cube?", "Every Friday at eighteen hundred UTC, for forty-eight hours, alliances fight to seize and hold the Super Cube. The longer your alliance holds it, the more glory and rewards you earn."),
  ("What are world bosses?", "The Pyramid Overlord, the Orbital Devourer and the Void Warden return every Monday at eighteen hundred UTC. Every hit pays a bounty, and when one falls, everyone who fought it shares the spoils."),
  ("What do the Energy Conduits do?", "Four conduits feed the Pyramid Overlord's shield. While all four stand, it takes only a quarter of the damage. Destroy them first."),
  ("What is Galaxy War?", "Galaxy War is a battle tournament every two weeks, from Monday to Wednesday UTC. Every battle point you earn counts toward milestones and rank rewards."),
  ("Where are my daily rewards?", "Open Events. Claim your daily login reward, the Online Bonus for time played, and the Level Bonus as you grow. The Daily Challenge adds more."),
 ]),
 ("Alliances", [
  ("Why join an alliance?", "Allies defend your worlds, join your strikes and fight beside you for the Super Cube. Alliance bonuses make every member stronger."),
  ("How do I join an alliance?", "Open the Alliance tab, browse the list and ask to join one, or found an alliance of your own and invite your friends."),
 ]),
 ("Upgrades and the shop", [
  ("What is VIP?", "VIP raises your production and gives you free speed-ups. Earn VIP points from daily logins, events and shard purchases, and switch VIP on in the Void Shop."),
  ("What are runes?", "Runes go into elemental rings. Fire boosts attack, water shields, earth armor, air speed, and spirit your resource output. They drop from Cube bosses and world bosses."),
  ("What is a Teleport Ticket?", "A Teleport Ticket moves one of your planets to an empty orbit. Tap an empty orbit on the map to use it."),
  ("What does my commander class do?", "The Warlord runs two extra fleets and flies warships faster on less fuel. The Industrialist carries more cargo and flies cargo ships faster. The Explorer flies frigates faster."),
  ("What is my flagship?", "Your flagship leads your fleets into battle. Upgrade it in Flagship Command with forge materials from monsters, Cubes and vaults."),
 ]),
 ("Your account", [
  ("Is my progress saved?", "Yes. When you play signed in, your empire saves to the cloud as you go, so you can carry on from another device."),
  ("The game feels slow. What can I do?", "Open Settings and lower the graphics: render scale and effects. Phones run smoother on lighter settings, and the game remembers your choice."),
  ("How do I turn your voice off?", "Open Settings and switch Advisor voice off. You can turn the music and sound effects on or off there too."),
  ("How do I report a problem?", "Tap Feedback, describe what happened, and send it. Crashes and slowdowns are reported to the team automatically as well."),
 ]),
]

NEWS = {
 "cube_arrival": "Commander, the Battle for the Super Cube has begun! The Cube is emerging from deep space. Rally our alliance and get ready to seize it.",
 "cube_assault": "Commander, the siege of the Super Cube is on! Alliances are attacking it right now. Join the battle, or watch it live.",
 "cube_finale": "Commander, the final two hours of the Cube battle have begun. Every minute we hold it counts now.",
 "cube_aftermath": "Commander, the Battle for the Super Cube is over. Let's see who was crowned.",
 "gw_start": "Commander, Galaxy War has begun! For three days, every battle point we earn counts toward milestones and rank rewards.",
 "wb_new": "Commander, the world bosses have returned! The Pyramid Overlord, the Orbital Devourer and the Void Warden are loose on the map. Open the Finder to hunt them.",
 "wb_live_ovl": "Commander, the Pyramid Overlord is under attack right now! Watch the fight live.",
 "wb_live_dev": "Commander, someone is fighting the Orbital Devourer right now! Watch it live.",
 "wb_live_war": "Commander, the Void Warden is under attack right now! Watch it live.",
 "wb_live_con": "Commander, an Energy Conduit is under attack right now! Watch it live.",
 "wb_con": "Commander, an Energy Conduit has fallen! The Pyramid Overlord's shield is weakening.",
 "wb_shield": "Commander, the Overlord's shield is down! Every fleet now hits it at full strength. This is our moment.",
 "wb_fall_ovl": "Commander, the Pyramid Overlord has fallen! If our fleets hurt it, our share of the spoils is waiting.",
 "wb_fall_dev": "Commander, the Orbital Devourer has fallen! If our fleets hurt it, our share of the spoils is waiting.",
 "wb_fall_war": "Commander, the Void Warden has fallen! If our fleets hurt it, our share of the spoils is waiting.",
}
import json
js_faq = json.dumps([[c, [[q, a] for q, a in L]] for c, L in FAQ], ensure_ascii=False)
js_news = json.dumps(NEWS, ensure_ascii=False)

blk = '''/* ---------- v385 the Advisor's news: the galaxy's big moments, announced live with a button to watch or open them ---------- */
const ADV_NEWS = ''' + js_news + ''';
G.newsQ = [];
function advNews(id, once, act, lbl) { if (!S || !G.ready || !ADV_NEWS[id]) return; S.newsSeen = S.newsSeen || {}; if (once && S.newsSeen[once]) return; if (once) { S.newsSeen[once] = now(); dirty(); }
  for (const k in S.newsSeen) if (now() - S.newsSeen[k] > 21 * 864e5) delete S.newsSeen[k];
  G.newsQ = G.newsQ.filter(n => n.id !== id).concat({ id, act, lbl, at: now() }).slice(-3); newsPump(); }
function newsPump() { const n = G.newsQ[0]; if (!n) return; if (now() - n.at > 20 * 60e3) { G.newsQ.shift(); return newsPump(); }
  if (tutOn() || battle || advLines || $("#adv") || $("#celeb") || $("#advh.on") || (G3 && G3.cam && G3.cam.cine) || document.hidden) return; // wait for a calm moment
  G.newsQ.shift(); const L = ADV_NEWS[n.id]; note(L.replace(/^Commander, /, ""), "info"); advHolo(L);
  let el = $("#advnews"); if (el) el.remove(); if (!n.act) return; el = document.createElement("div"); el.id = "advnews"; el.innerHTML = `<b>LIVE</b><span>${esc(n.lbl || "Watch")}</span>`; el.setAttribute("role", "button"); el.tabIndex = 0; for (const k in n.act) el.dataset[k] = n.act[k]; el.addEventListener("click", () => setTimeout(() => el.remove(), 0));
  $("#app").appendChild(el); setTimeout(() => { if (el.isConnected) el.remove(); }, 16000); }
setInterval(() => { try { newsPump(); newsWatch(); } catch (e) {} }, 3000);
/* events the clock decides: the Cube's phases, Galaxy War, the world bosses' weekly return */
function newsWatch() { if (!S || !G.ready) return; const T = now();
  const ph = typeof cubePhase === "function" ? cubePhase(T) : null; if (ph) { const w = evWeek(T), k = ph.k; if (["arrival", "assault", "finale", "aftermath"].includes(k) && ph.s - CUBE_PH[ph.i].at < 30 * 60e3) advNews("cube_" + k, `cube:${w}:${k}`, k === "aftermath" ? null : { act: "nexus" }, k === "arrival" ? "See the Cube" : "Join or watch"); }
  if (gwLive(T) && T - gwStart(gwIdx(T)) < 12 * 3600e3) advNews("gw_start", "gw:" + gwIdx(T), { act: "events" }, "Open Events");
  const c = wbCyc(T); if (T - (WB_BASE + c * WEEK) < 24 * 3600e3) advNews("wb_new", "wb:" + c, { act: "find", r: "ev" }, "Hunt the bosses"); }
/* events the shared boss record reveals: someone is fighting a boss right now, a conduit fell, the shield went down, a boss fell */
function wbNews(prev, st) { if (!prev || prev.cyc !== st.cyc) return; const c = st.cyc, live = k => { const kk = WB[k].con != null ? "con" : k; if (now() - ((G.wbLiveAt || {})[kk] || 0) < 30 * 60e3) return; (G.wbLiveAt = G.wbLiveAt || {})[kk] = now(); advNews("wb_live_" + kk, null, { act: "cineObj", id: "wb_" + k }, "Watch live"); };
  for (const k in WB) { if (st.hp[k] >= prev.hp[k]) continue; if (st.hp[k] > 0) live(k);
    else if (WB[k].con != null) { if ([0, 1, 2, 3].every(i => !(st.hp["c" + i] > 0))) advNews("wb_shield", `wbsh:${c}`, { act: "wboss", id: "ovl" }, "Attack the Overlord"); else advNews("wb_con", `wbc:${c}:${k}`, { act: "wboss", id: "ovl" }, "See the Overlord"); }
    else advNews("wb_fall_" + k, `wbf:${c}:${k}`, { act: "wboss", id: k }, "See the spoils"); } }
/* ---------- v385 FAQ: every question a player asks, answered in writing and out loud ---------- */
const FAQ = ''' + js_faq + ''';
function faqHTML() { let i = 0; return `<div class="faq"><h3 class="faqh">Ask the Advisor</h3><p class="note">Tap a question. I'll answer it, out loud too.</p><input id="faqq" class="faqq" type="search" placeholder="Search questions" aria-label="Search questions" autocomplete="off">
  ${FAQ.map(([c, L]) => `<section class="faqc"><h4>${esc(c)}</h4>${L.map(([q, a]) => `<div class="faqi" data-q="${esc((q + " " + a).toLowerCase())}"><button class="faqb" data-act="faq" data-i="${i++}" aria-expanded="false"><span>${esc(q)}</span><i aria-hidden="true">▸</i></button><p>${esc(a)}</p></div>`).join("")}</section>`).join("")}<p class="note faqnone" hidden>No question matches. Try another word.</p></div>`; }
document.addEventListener("input", e => { if (!e.target || e.target.id !== "faqq") return; const v = e.target.value.trim().toLowerCase(), root = e.target.closest(".faq"); if (!root) return; let any = 0;
  for (const it of root.querySelectorAll(".faqi")) { const on = !v || it.dataset.q.includes(v); it.hidden = !on; if (on) any++; } for (const s of root.querySelectorAll(".faqc")) s.hidden = ![...s.querySelectorAll(".faqi")].some(x => !x.hidden); const no = root.querySelector(".faqnone"); if (no) no.hidden = !!any; });
'''

rep("function shHowTo() {", blk + "function shHowTo() {")
rep('<div class="howto">${mEtc()}</div>`; }', '<div class="howto">${mEtc()}${faqHTML()}</div>`; }')
# her answers
rep("  cineObj: d => cineObjStart(d.id),", """  cineObj: d => cineObjStart(d.id),
  faq: d => { const n = +d.i, all = FAQ.flatMap(c => c[1]), qa = all[n], b = document.querySelector(`.faqb[data-i="${n}"]`); if (!qa || !b) return; const it = b.closest(".faqi"), open = !it.classList.contains("on");
    for (const x of document.querySelectorAll(".faqi.on")) { x.classList.remove("on"); x.querySelector(".faqb").setAttribute("aria-expanded", "false"); }
    if (open) { it.classList.add("on"); b.setAttribute("aria-expanded", "true"); advHolo(qa[1]); } else { try { voiceStop(); } catch (e) {} } },""")
# the boss record tells her what just happened
rep("function wbSeen(d) { try { const st = wbNorm(d ? jcopy(d) : null, wbCyc(now())); if (WB_PREV && WB_PREV.cyc === st.cyc) for (const k in WB) if (st.hp[k] < WB_PREV.hp[k]) wbFight(k, WB_PREV.hp[k] - st.hp[k], !st.hp[k]); WB_PREV = st; } catch (e) {} }",
    "function wbSeen(d) { try { const st = wbNorm(d ? jcopy(d) : null, wbCyc(now())); if (WB_PREV && WB_PREV.cyc === st.cyc) for (const k in WB) if (st.hp[k] < WB_PREV.hp[k]) wbFight(k, WB_PREV.hp[k] - st.hp[k], !st.hp[k]); wbNews(WB_PREV, st); WB_PREV = st; } catch (e) {} }")
# our own hits on a conduit or a kill also count as news (the solo galaxy has no shared record)
rep("    addReport(rep); wbFight(key, seg, !left); wbClaim(); home();", "    addReport(rep); wbFight(key, seg, !left); wbClaim(); if (G.mode !== \"online\") { const pv = jcopy(cur); pv.hp[key] = n0; wbNews(pv, cur); } home();")
# styles
i = t.index('</style>', t.index('.fshero{'))
t = t[:i] + '''
/* v385 the Advisor's news button and the FAQ */
#advnews{position:fixed;left:50%;transform:translateX(-50%);top:calc(env(safe-area-inset-top,0px) + 74px);z-index:90;display:flex;align-items:center;gap:10px;padding:9px 16px 9px 10px;border-radius:999px;background:rgba(18,10,30,.92);border:1px solid #c9a6ff;box-shadow:0 0 22px rgba(201,166,255,.45);color:#fff;font:600 14px/1 var(--f-display,system-ui);cursor:pointer;animation:anIn .4s ease}
#advnews b{background:#ff4d6a;color:#fff;font:700 10px/1 ui-monospace,monospace;letter-spacing:.12em;padding:4px 6px;border-radius:4px;animation:fbHot 1.4s ease-in-out infinite}@keyframes anIn{from{opacity:0;transform:translate(-50%,-8px)}to{opacity:1;transform:translateX(-50%)}}
.faq{margin-top:14px}.faqh{margin:0;font-size:17px}.faqq{width:100%;margin:8px 0 4px;padding:10px 12px;border-radius:10px;border:1px solid rgba(127,230,243,.3);background:rgba(4,10,20,.6);color:inherit;font:inherit}
.faqc h4{margin:14px 0 6px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#7fe6f3}.faqi{border:1px solid rgba(127,230,243,.16);border-radius:10px;margin:5px 0;overflow:hidden;background:rgba(127,230,243,.04)}
.faqb{all:unset;box-sizing:border-box;width:100%;display:flex;justify-content:space-between;gap:10px;padding:11px 12px;cursor:pointer;font-weight:600;font-size:14px}.faqb:focus-visible{outline:2px solid #7fe6f3;outline-offset:-2px}.faqb i{font-style:normal;color:#7fe6f3;transition:transform .2s}
.faqi p{display:none;margin:0;padding:0 12px 12px;font-size:13.5px;line-height:1.5;color:#c9d6ea}.faqi.on p{display:block}.faqi.on .faqb i{transform:rotate(90deg)}.faqi.on{border-color:rgba(127,230,243,.45)}
''' + t[i:]

# v385b: the Advisor and the scan warn about each boss's attacks
import re as _re
HOLO = {
 "wbovl": "Commander, the Pyramid Overlord walks the middle layers. Beware its sigil beam, the stomp that shakes everything near it, and the surge from the beam beneath it. Four Energy Conduits feed its shield, so take them down first.",
 "wbdev": "Commander, the Orbital Devourer never stops moving. Beware its snapping claws, the tentacle lash that sweeps through a fleet, and the vortex beam from its maw. Strike it with our heaviest ships.",
 "wbwar": "Commander, the Void Warden guards the deep layers. Beware its void pulse, the core beam, and the satellite storm that rains lightning. Send a strong fleet, and bring our allies.",
 "wbcon": "Commander, this conduit feeds the Overlord's shield. Beware its discharge, a lightning column and a shockwave when it overcharges. Destroy all four, and the Overlord takes full damage.",
}
for k, v in HOLO.items():
    m = _re.search(k + r': "[^"]*",', t); assert m, k; t = t[:m.start()] + k + ': ' + json.dumps(v) + ',' + t[m.end():]
SCAN = {
 "ovl": "Scanning the Pyramid Overlord. Beware the sigil beam on its face, the stomp of its front legs, and the surge from the beam beneath it.",
 "dev": "Scanning the Orbital Devourer. Beware its snapping claws, the tentacle lash, and the vortex beam when its maw opens.",
 "war": "Scanning the Void Warden. Beware the void pulse when its crescents clench, the core beam, and its satellite storm.",
 "con": "Scanning an Energy Conduit. Beware the discharge when its rings spin up. It feeds the Overlord's shield.",
}
ATT = {
 "ovl": [["beam", "Sigil beam", "It rears up and fires the sigil on its face straight through a fleet."], ["stomp", "Stomp", "Its front legs slam down in a shockwave that hits everything close."], ["summon", "Beam surge", "Its belly claws open and the beam beneath it surges."]],
 "dev": [["bite", "Bite", "Its claws snap shut on anything near the maw."], ["lash", "Tentacle lash", "A whip of tentacles sweeps through the fleet."], ["beam", "Vortex beam", "The maw gapes and fires the vortex."], ["roar", "Roar", "Lightning crackles through everything around it."]],
 "war": [["pulse", "Void pulse", "Its crescents clench, then burst out in a void shockwave."], ["beam", "Core beam", "The rings lock and the core fires."], ["summon", "Satellite storm", "Its satellites fly wide and rain lightning."]],
 "con": [["discharge", "Discharge", "A lightning column and a ring shockwave."], ["charge", "Overcharge", "Its rings spin up and the crystal overheats before it discharges."]],
}
rep('<div style="--d:3.4s"><dt>Observed</dt><dd id="wsMv">…</dd></div></dl></div>`;',
    '</dl><div class="ws-att" style="--d:3.4s"><h5>⚠ Beware</h5>${(WB_ATT[D.con != null ? "con" : key] || []).map(([m, n, d]) => `<p data-m="${m}"><b>${n}</b><span>${d}</span></p>`).join("")}</div></div>`;')
rep('  $("#app").appendChild(el); G.wbScan = { key, t0: performance.now(), seen: [], next: 0, i: 0 }; wbScanTick(); }',
    '  $("#app").appendChild(el); G.wbScan = { key, t0: performance.now(), seen: [], next: 0, i: 0 }; wbScanTick(); setTimeout(() => { if (G.wbScan && G.wbScan.key === key) advHolo(WB_SCAN_SAY[D.con != null ? "con" : key]); }, 900); }')
rep('M.b.act(n); if (!s.seen.includes(n)) s.seen.push(n); }',
    'M.b.act(n); if (!s.seen.includes(n)) s.seen.push(n); for (const p of document.querySelectorAll("#wbscan .ws-att p")) p.classList.toggle("hot", p.dataset.m === n); }')
rep("const WB_MOVE_N = {", "const WB_ATT = " + json.dumps(ATT, ensure_ascii=False) + ", WB_SCAN_SAY = " + json.dumps(SCAN, ensure_ascii=False) + ";\nconst WB_MOVE_N = {")
i = t.index('</style>', t.index('.fshero{'))
t = t[:i] + '#wbscan .ws-att{margin-top:9px;padding-top:8px;border-top:1px solid rgba(255,122,106,.3);opacity:0;animation:wsIn .4s ease forwards;animation-delay:var(--d)}#wbscan .ws-att h5{margin:0 0 5px;font:700 10px/1 ui-monospace,monospace;letter-spacing:.14em;color:#ff7a6a}\n#wbscan .ws-att p{margin:0 0 5px;padding:4px 6px;border-radius:6px;display:flex;flex-direction:column;gap:1px;transition:background .3s}#wbscan .ws-att b{font-size:12px;color:#ffd0c8}#wbscan .ws-att span{font-size:11px;color:#a9b4cc;line-height:1.3}\n#wbscan .ws-att p.hot{background:rgba(255,77,106,.22);box-shadow:inset 3px 0 0 #ff4d6a}#wbscan .ws-att p.hot b::before{content:"⚠ ";color:#ff4d6a}\n' + t[i:]
open(p, "w").write(t)
# voice lines for the lab
def h(s):
    x = 2166136261
    for ch in s: x ^= ord(ch); x = (x * 16777619) & 0xffffffff
    return x
def b36(n):
    d = '0123456789abcdefghijklmnopqrstuvwxyz'; s = ''
    while True:
        s = d[n % 36] + s; n //= 36
        if not n: return s
out = [{"key": b36(h(v)), "where": "Boss card · " + k, "line": v} for k, v in HOLO.items()] + [{"key": b36(h(v)), "where": "Boss scan · " + k, "line": v} for k, v in SCAN.items()] + [{"key": b36(h(a)), "where": "FAQ · " + q, "line": a} for c, L in FAQ for q, a in L] + [{"key": b36(h(v)), "where": "News · " + k, "line": v} for k, v in NEWS.items()]
json.dump(out, open("tools/patches/p385_voice.json", "w"), ensure_ascii=False, indent=1)
print("ok", len(out), "voice lines")
