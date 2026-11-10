# v388: the Wednesday titans. Four new world bosses from the owner's concept art (Brood Matriarch, Iron Tyrant, Event Horizon Wyrm,
# Shard Colossus) on their own weekly cycle (Wednesdays 18:00 UTC), each with a mechanic of its own, their own event on the Events
# page (Titan Hunt: live board, feed, points, milestones, ranking), the cinematic scan with the Advisor narrating each attack as it is
# shown (for every boss), Advisor news and voice lines, map wreckage, materials and a FAQ entry.
import re
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)

# ---------- the bosses ----------
rep("""const WB_ATK = { ovl: ["beam", "stomp", "summon"], dev: ["bite", "lash", "beam", "roar"], war: ["pulse", "beam", "summon"], c0: ["discharge", "charge"] };""",
"""/* v388 the Wednesday titans: their own cycle (Wednesdays 18:00 UTC) and a mechanic each (see wbShOf, wbVault) */
Object.assign(WB, {
  brd: { k: "wbBrd", n: "Brood Matriarch", ic: "☣", col: "#a8ff3a", hp: 220000, atk: 150000, m3: "matriarch", sc: 1, bounty: { m: 56000, c: 38000, g: 18000 }, sh: 3, kill: 14, where: "Hive space · Far Reach", g: 2, cam: 110,
    d: "The Hive's queen, nesting in the Far Reach. Her drone swarm rebuilds while nobody fights her: left alone for six hours it soaks half of all damage. Keep the pressure on." },
  tyr: { k: "wbTyr", n: "Iron Tyrant", ic: "⚓", col: "#ff8a3a", hp: 260000, atk: 190000, m3: "tyrant", sc: .75, bounty: { m: 70000, c: 46000, g: 20000 }, sh: 3, kill: 16, where: "Pirate trade lanes", g: 2, cam: 150,
    d: "A pirate super-dreadnought patched together from stolen hulls, sailing from hideout to hideout. Its vault grows all week: the bounty per hit climbs from ×1 to ×2.5." },
  wym: { k: "wbWym", n: "Event Horizon Wyrm", ic: "❂", col: "#ffa040", hp: 320000, atk: 240000, m3: "wyrm", sc: 1, bounty: { m: 84000, c: 56000, g: 26000 }, sh: 4, kill: 20, where: "The Core", g: 2, cam: 125,
    d: "A serpent of black-hole rings coiled in the Core. Only its glowing segments can be hurt: for 20 minutes of every hour they are exposed and it takes full damage, the rest of the time half. Time your fleet's arrival." },
  col: { k: "wbCol", n: "Shard Colossus", ic: "◈", col: "#c070ff", hp: 200000, atk: 140000, m3: "colossus", sc: 1, bounty: { m: 50000, c: 40000, g: 16000 }, sh: 6, kill: 24, where: "Crystal fields · Middle Reach", g: 2, cam: 110,
    d: "A crystal golem grown out of a crystal field. Below half hull it shatters into fragments that shield it (×1.4, and ×1.8 below a quarter). It pays Void Shards in bulk." } });
const WB_ATK = { ovl: ["beam", "stomp", "summon"], dev: ["bite", "lash", "beam", "roar"], war: ["pulse", "beam", "summon"], c0: ["discharge", "charge"], brd: ["hatch", "acid", "slam"], tyr: ["broadside", "claw", "mines"], wym: ["lens", "coil", "sweep"], col: ["prism", "rain", "shatter"] };""")
rep("""for (const [k, u] of [["wbOvl", WB.ovl], ["wbDev", WB.dev], ["wbWar", WB.war], ["wbCon", WB.c0]])""", """for (const [k, u] of [["wbOvl", WB.ovl], ["wbDev", WB.dev], ["wbWar", WB.war], ["wbCon", WB.c0], ["wbBrd", WB.brd], ["wbTyr", WB.tyr], ["wbWym", WB.wym], ["wbCol", WB.col]])""")
rep("""const wbCyc = T => Math.floor((T - WB_BASE) / WEEK), wbEnd = c => WB_BASE + (c + 1) * WEEK;""",
"""const wbCyc = T => Math.floor((T - WB_BASE) / WEEK), wbEnd = c => WB_BASE + (c + 1) * WEEK;
const WB2_BASE = WB_BASE + 2 * 864e5, wbG2 = k => !!(WB[k] && WB[k].g === 2), wbCyc2 = T => Math.floor((T - WB2_BASE) / WEEK), wbEnd2 = c => WB2_BASE + (c + 1) * WEEK;
const wbCycOf = (k, T) => wbG2(k) ? wbCyc2(T) : wbCyc(T), wbEndOf = (k, c) => wbG2(k) ? wbEnd2(c) : wbEnd(c), wbStartOf = (k, T) => wbG2(k) ? WB2_BASE + wbCyc2(T) * WEEK : WB_BASE + wbCyc(T) * WEEK, stCyc = (st, k) => wbG2(k) ? st.cyc2 : st.cyc;
const wbKeys = g => Object.keys(WB).filter(k => (g === 2) === wbG2(k)), wbMain = g => g === 2 ? ["brd", "tyr", "wym", "col"] : ["ovl", "dev", "war"];
const wymOpen = T => ((T - WB2_BASE) % 3600e3 + 3600e3) % 3600e3 < 20 * 60e3, wymNext = T => { const ph = ((T - WB2_BASE) % 3600e3 + 3600e3) % 3600e3; return ph < 20 * 60e3 ? T - ph + 20 * 60e3 : T - ph + 3600e3; };
const wbVault = T => 1 + 1.5 * clamp((T - wbStartOf("tyr", T)) / WEEK, 0, 1);
/* how much tougher a boss is right now: the Overlord's conduits, the Matriarch's swarm, the Wyrm's hidden segments, the Colossus's fragments */
function wbShOf(key, st, at) { if (key === "ovl") return 1 + .75 * [0, 1, 2, 3].filter(i => (st.hp["c" + i] | 0) > 0).length;
  if (key === "brd") { const h = Math.max((st.hit || {}).brd || 0, wbStartOf("brd", at)); return 1 + clamp((at - h) / (6 * 3600e3), 0, 1); }
  if (key === "wym") return wymOpen(at) ? 1 : 2;
  if (key === "col") { const hp = st.hp.col | 0; return hp <= 10 ? 1.8 : hp <= 20 ? 1.4 : 1; } return 1; }
function wbTwist(key, T = now()) { const st = wbState(T), s = wbShOf(key, st, T);
  if (key === "brd") return s > 1.02 ? `Drone swarm soaking ${Math.round((1 - 1 / s) * 100)}% · it thins when attacked` : "Swarm thinned · full damage now";
  if (key === "tyr") return `Vault ×${wbVault(T).toFixed(2)} bounty · grows all week`;
  if (key === "wym") return wymOpen(T) ? `Segments exposed · full damage for ${ftime(wymNext(T) - T)}` : `Segments hidden · half damage · exposed in ${ftime(wymNext(T) - T)}`;
  if (key === "col") return s > 1 ? `Shattered · fragments shield it ×${s}` : "Whole · shatters below 50% hull";
  return ""; }""")
# positions
rep("""function wbPos(key, T, out) { const o = out || {}, c = wbCyc(T), H = wbHome(c);
  if (key === "dev")""", """let WB_LANE = null, WB_MINE = null;
function wbPos(key, T, out) { const o = out || {};
  if (wbG2(key)) { const c2 = wbCyc2(T);
    if (key === "brd") { const L = LAYERS[1], r = L.r0 + (L.r1 - L.r0) * (.3 + .4 * (hash("brd" + c2) % 1000) / 1000), a = (hash("brdA" + c2) % 6283) / 1000 + TAU * T / period(r); o.x = Math.cos(a) * r; o.z = Math.sin(a) * r; o.y = 3; return o; }
    if (key === "wym") { const r = LAYERS[5].r1 * .55, a = (hash("wym" + c2) % 6283) / 1000 + TAU * (T - WB2_BASE) / (9 * 3600e3); o.x = Math.cos(a) * r; o.z = Math.sin(a) * r; o.y = 7 * Math.sin(a * 3); return o; }
    if (key === "col") { if (!WB_MINE) { WB_MINE = NODES.filter(n => n.res === "c" && layerOf(n.r).n === 4); if (!WB_MINE.length) WB_MINE = NODES.slice(0, 50); }
      const q = P3(WB_MINE[hash("col" + c2) % WB_MINE.length], T, WBS), r = Math.hypot(q.x, q.z) || 1; o.x = q.x + q.x / r * 14; o.z = q.z + q.z / r * 14; o.y = q.y; return o; }
    if (!WB_LANE) { WB_LANE = PIRATES.filter(x => x.kind === "pirate" && [3, 4].includes(layerOf(x.r).n)).sort((a, b) => a.a0 - b.a0); if (!WB_LANE.length) WB_LANE = PIRATES.slice(0, 50); }
    const LEG = 8 * 3600e3, u = (T - WB2_BASE) / LEG, i = Math.floor(u), f = u - i, n = WB_LANE.length, at = j => WB_LANE[((hash("tyr" + c2) + j * 37) % n + n) % n]; // the Tyrant sails hideout to hideout, 8 hours a leg
    const A = P3(at(i), T, {}), B = P3(at(i + 1), T, {}), k = f * f * (3 - 2 * f); o.x = A.x + (B.x - A.x) * k; o.z = A.z + (B.z - A.z) * k; o.y = A.y + (B.y - A.y) * k + 4 + Math.sin(f * Math.PI) * 10; return o; }
  const c = wbCyc(T), H = wbHome(c);
  if (key === "dev")""")
# the shared record keeps two weekly cycles
rep("""function wbNorm(d, c) { const o = d && d.cyc === c ? d : { cyc: c, hp: {}, dmg: {}, dead: {}, last: {}, scar: d && Array.isArray(d.scar) ? d.scar : [] }; o.hp = o.hp || {}; o.scar = Array.isArray(o.scar) ? o.scar.filter(s => s && now() - s.at < WB_SCAR_MS).slice(-60) : []; o.dmg = o.dmg || {}; o.dead = o.dead || {}; o.last = o.last || {};""",
"""function wbNorm(d, c, T = now()) { const c2 = wbCyc2(T), o = d && typeof d === "object" ? d : {}, s1 = o.cyc === c, s2 = o.cyc2 === c2; // v388: the Monday bosses and the Wednesday titans reset on their own days
  for (const f of ["hp", "dmg", "dead", "last", "hit"]) { o[f] = o[f] && typeof o[f] === "object" ? o[f] : {}; for (const k in WB) if (wbG2(k) ? !s2 : !s1) delete o[f][k]; }
  o.cyc = c; o.cyc2 = c2; o.scar = Array.isArray(o.scar) ? o.scar.filter(s => s && now() - s.at < WB_SCAR_MS).slice(-80) : [];""")
rep("""  if (!WBN || WBN.cyc !== c || WBN_SRC !== src) { WBN = wbNorm(src && src.cyc === c ? jcopy(src) : null, c); WBN_SRC = src; } return WBN; }""",
"""  if (!WBN || WBN.cyc !== c || WBN.cyc2 !== wbCyc2(T) || WBN_SRC !== src) { WBN = wbNorm(src ? jcopy(src) : null, c, T); WBN_SRC = src; } return WBN; }""")
rep("""const wbSegLoot = key => { const b = WB[key].bounty; return { m: Math.round(b.m / 4), c: Math.round(b.c / 4), g: Math.round(b.g / 4) }; };""",
"""const wbSegLoot = (key, T = now()) => { const b = WB[key].bounty, v = key === "tyr" ? wbVault(T) : 1; return { m: Math.round(b.m / 4 * v), c: Math.round(b.c / 4 * v), g: Math.round(b.g / 4 * v) }; };""")
# the fight
rep("""const snap = await ref.get(), cur = wbNorm(snap.exists ? snap.data() : null, c), n0 = cur.hp[key] | 0;""", """const snap = await ref.get(), cur = wbNorm(snap.exists ? snap.data() : null, c, at), n0 = cur.hp[key] | 0;""")
rep("""const shK = key === "ovl" ? 1 + .75 * [0, 1, 2, 3].filter(i => (cur.hp["c" + i] | 0) > 0).length : 1, mine0 = Object.assign({}, f.n);""", """const shK = wbShOf(key, cur, at), mine0 = Object.assign({}, f.n);""")
rep("""cur.scar = cur.scar.slice(-60); } // wreckage stays 48 h""", """cur.scar = cur.scar.slice(-80); } cur.hit[key] = at; // wreckage stays 48 h; the Matriarch's swarm thins""")
rep("""if (seg) { const per = wbSegLoot(key), L =""", """if (seg) { const per = wbSegLoot(key, at), L =""")
rep("""{ const mk = key === "dev" ? "bio" : key === "war" ? "void" : D.con != null ? "crystal" : "alloy",""", """{ const mk = { dev: "bio", war: "void", brd: "bio", tyr: "circuit", wym: "void", col: "crystal" }[key] || (D.con != null ? "crystal" : "alloy"),""")
rep("""if (!left) { bump("bosses"); note(`We brought down the ${D.n}!""", """if (key === "col" && seg) { const xs = seg * 2; S.shards = (S.shards || 0) + xs; rep.shards = (rep.shards || 0) + xs; } /* the Colossus pays shards in bulk */
    if (!left) { bump("bosses"); note(`We brought down the ${D.n}!""")
rep("""function wbClaim() { if (!S || !G.ready) return; const st = wbState(), c = st.cyc; S.wbGot = S.wbGot || {};""", """function wbClaim() { if (!S || !G.ready) return; const st = wbState(), c0 = st.cyc; S.wbGot = S.wbGot || {};""")
rep("""  for (const id in S.wbGot) if (+id.split(":")[0] < c - 1) delete S.wbGot[id];
  for (const key in WB) { const dm = st.dmg[key] || {}, my = dm[G.me] || 0, id = c + ":" + key;""", """  for (const id in S.wbGot) if (+id.split(":")[0] < c0 - 2) delete S.wbGot[id];
  for (const key in WB) { const c = stCyc(st, key), dm = st.dmg[key] || {}, my = dm[G.me] || 0, id = c + ":" + key;""")
rep("""if (WB_PREV && WB_PREV.cyc === st.cyc) for (const k in WB) if (st.hp[k] < WB_PREV.hp[k])""", """if (WB_PREV) for (const k in WB) if (stCyc(WB_PREV, k) === stCyc(st, k) && st.hp[k] < WB_PREV.hp[k])""")
# the map: the Tyrant faces where it sails, the Wyrm turns slowly
rep("""    if (key === "dev") { const q2 = wbPos("dev", T + 60000, {}); g.rotation.y = -Math.atan2(q2.z - q.z, q2.x - q.x); } else if (key === "war")""", """    if (key === "dev" || key === "tyr") { const q2 = wbPos(key, T + 60000, {}); g.rotation.y = -Math.atan2(q2.z - q.z, q2.x - q.x); } else if (key === "wym") g.rotation.y = -t * 2e-5; else if (key === "war")""")
# the battle report view
rep("""const WB_FRONT = { overlord: 0, devourer: -Math.PI / 2, warden: 0, conduit: 0 }; const WB_VIEW = { overlord: [-Math.PI / 2, [-10, 4, 32], [0, -1.5, 0]],""",
"""const WB_FRONT = { overlord: 0, devourer: -Math.PI / 2, warden: 0, conduit: 0, matriarch: 0, tyrant: -.55, wyrm: 0, colossus: 0 }; const WB_VIEW = { matriarch: [-.55, [-12, 8, 36], [0, 6.5, 0]], tyrant: [.08, [-4, 7, 56], [1, -2.5, 0]], wyrm: [0, [-5, 15, 40], [0, 2.5, 0]], colossus: [-.35, [-8, 8, 37], [0, 8.5, 0]], overlord: [-Math.PI / 2, [-10, 4, 32], [0, -1.5, 0]],""")
# the boss card
rep("""  const key = sheet.id, D = WB[key], O = WBO[key]; if (!D) return ""; const T = now(), st = wbState(T), hp = st.hp[key] | 0, pc = Math.round(hp / WB_SEG * 100), h = originPlanet(), avail = originAvail(), sel = selected(), end = wbEnd(st.cyc);
  const sent = S.fleets.some(f => f.wb === key && f.phase === "out"), my = (st.dmg[key] || {})[G.me] || 0, per = wbSegLoot(key), L = layerOf(O.r);
  const shield = key === "ovl" ? `<dt>Shield</dt><dd>${wbCons(T) ? `${wbCons(T)}/4 conduits · ${Math.round(100 / wbShield(T))}% damage` : "Down"}</dd>` : "";""",
"""  const key = sheet.id, D = WB[key], O = WBO[key]; if (!D) return ""; const T = now(), st = wbState(T), hp = st.hp[key] | 0, pc = Math.round(hp / WB_SEG * 100), h = originPlanet(), avail = originAvail(), sel = selected(), end = wbEndOf(key, stCyc(st, key));
  const sent = S.fleets.some(f => f.wb === key && f.phase === "out"), my = (st.dmg[key] || {})[G.me] || 0, per = wbSegLoot(key, T), L = layerOf(O.r);
  const shield = key === "ovl" ? `<dt>Shield</dt><dd>${wbCons(T) ? `${wbCons(T)}/4 conduits · ${Math.round(100 / wbShield(T))}% damage` : "Down"}</dd>` : wbG2(key) && hp ? `<dt>${{ brd: "Drone swarm", tyr: "Vault", wym: "Segments", col: "Fragments" }[key]}</dt><dd>${wbTwist(key, T)}</dd>` : "";""")
rep("""<dt>Your damage this week</dt><dd>${my ? Math.round(my / WB_SEG * 100) + "%" : "None yet"}</dd><dt>Returns</dt><dd>Mondays 18:00 UTC</dd></dl>""",
"""<dt>Your damage this week</dt><dd>${my ? Math.round(my / WB_SEG * 100) + "%" : "None yet"}</dd><dt>Returns</dt><dd>${wbG2(key) ? "Wednesdays" : "Mondays"} 18:00 UTC</dd></dl>${key === "wym" && hp && h ? `<p class="note">A fleet sent now arrives while the segments are ${wymOpen(T + travelMs(h, O, Object.keys(sel).length ? sel : { fighter: 1 })) ? "<b>exposed</b> (full damage)" : "<b>hidden</b> (half damage)"}.</p>` : ""}""")
rep("""It returns every Monday at full strength, in a new place.</p>""", """It returns every ${wbG2(key) ? "Wednesday" : "Monday"} at full strength, in a new place.</p>""")
# wreckage: every roaming boss leaves a trail
rep("""  for (const key of ["ovl", "dev", "war"]) { const step = (key === "dev" ? 3 : 4) * 3600e3;
    for (let tk = Math.ceil((T - WB_SCAR_MS) / step) * step; tk <= T; tk += step) { if (wbCyc(tk) === st.cyc && st.dead[key] && st.dead[key] < tk) continue;""",
"""  for (const key of ["ovl", "dev", "war", "brd", "tyr", "wym", "col"]) { const step = (key === "dev" || key === "tyr" ? 3 : 4) * 3600e3;
    for (let tk = Math.ceil((T - WB_SCAR_MS) / step) * step; tk <= T; tk += step) { if (wbCycOf(key, tk) === stCyc(st, key) && st.dead[key] && st.dead[key] < tk) continue;""")
rep("""hot = WB[s.k] && s.k === "dev" ? [1, .35, .9] : [1, .5, .18];""", """hot = { dev: [1, .35, .9], brd: [.5, 1, .15], col: [.8, .4, 1], wym: [1, .7, .3] }[s.k] || [1, .5, .18];""")
# the scan: sweep heights, attacks, intel, and the Advisor narrates each attack as it is shown
rep("""const WB_YR = { overlord: [-8, 7], devourer: [-6, 6], warden: [-7, 7], conduit: [0, 12.5] };""", """const WB_YR = { overlord: [-8, 7], devourer: [-6, 6], warden: [-7, 7], conduit: [0, 12.5], matriarch: [-3, 17], tyrant: [-12, 12], wyrm: [-3, 13], colossus: [-1, 19] };""")
rep("""const WB_ATT = {"ovl":""", """const WB_ATT = {"brd": [["hatch", "Hatch swarm", "Her egg sac squeezes and bursts, and a swarm of drones pours out to screen her."], ["acid", "Acid spray", "She rears back and sprays acid that eats through shields."], ["slam", "Carapace slam", "Her scythes rise and smash down in a shockwave."]], "tyr": [["broadside", "Broadside", "Both gun decks fire down its length, one cannon after another."], ["claw", "Boarding claw", "The claw on its bow reaches out, grabs a ship and drags it in."], ["mines", "Mine wake", "It drops a trail of spiked mines behind its stern."]], "wym": [["coil", "Gravity coil", "It tightens round its black hole, and the pull drags fleets in."], ["lens", "Lens beam", "Its jaws gape and fire a lance of focused light."], ["sweep", "Tail sweep", "Its bladed tail swings round through everything near it."]], "col": [["rain", "Crystal rain", "It raises its arms and shards hail down on the fleet."], ["prism", "Prism beam", "A beam from its eyes splits and bounces from ship to ship."], ["shatter", "Shatter", "It bursts apart into fragments, and its heart is exposed for a moment."]], "ovl":""")
rep("""WB_SCAN_SAY = {"ovl":""", """WB_SCAN_SAY = {"brd": "Scanning the Brood Matriarch. Beware the hatching swarm from her egg sac, her acid spray, and the slam of her scythes.", "tyr": "Scanning the Iron Tyrant. Beware its broadside, the boarding claw, and the mines in its wake. The engine at its stern runs hot.", "wym": "Scanning the Event Horizon Wyrm. Beware the gravity coil, the lens beam, and its tail sweep. Watch for the glowing segments: that's where it can be hurt.", "col": "Scanning the Shard Colossus. Beware the crystal rain, the prism beam, and the shatter. Its heart is exposed for a moment after it breaks apart.", "ovl":""")
rep("""const WB_MOVE_N = { walk: "Walk",""", """const WB_MOVE_N = { hatch: "Hatch swarm", acid: "Acid spray", slam: "Carapace slam", broadside: "Broadside", claw: "Boarding claw", mines: "Mine wake", coil: "Gravity coil", lens: "Lens beam", sweep: "Tail sweep", rain: "Crystal rain", prism: "Prism beam", shatter: "Shatter", walk: "Walk",""")
rep("""const WB_INTEL = { ovl:""", """const WB_INTEL = { brd: ["Hive queen · swarm carrier", "Her swarm thins while she's under attack. Hit her often.", "SEVERE"], tyr: ["Pirate super-dreadnought", "The overheating engine at its stern.", "EXTREME"], wym: ["Black-hole serpent", "The glowing segments, and its jaw when it opens to fire.", "CATASTROPHIC"], col: ["Crystal golem · shard storm", "Its heart, exposed for a moment after each shatter.", "SEVERE"], ovl:""")
rep("""<span>Threat <em>${I[2]}</em></span>${key === "ovl" ? `<span id="wsShS">…</span>` : ""}</div>""", """<span>Threat <em>${I[2]}</em></span>${key === "ovl" ? `<span id="wsShS">…</span>` : ""}${wbG2(key) ? `<span id="wsTw">…</span>` : ""}</div>""")
rep("""if (y) y.textContent = wbCons() ? `Shield ${wbCons()}/4` : "Shield down"; }""", """if (y) y.textContent = wbCons() ? `Shield ${wbCons()}/4` : "Shield down"; const z = $("#wsTw"); if (z) z.textContent = wbTwist(s.key); }""")
rep("""G.wbScan = { key, t0: performance.now(), seen: [], next: 0, i: 0 };""", """G.wbScan = { key, t0: performance.now(), seen: [], said: [], next: 0, i: 0 };""")
rep("""  if (t > s.next) { s.next = t + 4500; const mv = M.b.moves.filter(x => x !== "hit"), n = mv[s.i++ % mv.length]; M.b.act(n); if (!s.seen.includes(n)) s.seen.push(n);""",
"""  if (t > s.next) { s.next = t + 5200; const mv = M.b.moves.filter(x => x !== "hit"), n = mv[s.i++ % mv.length]; M.b.act(n); if (!s.seen.includes(n)) s.seen.push(n);
    { const A = (WB_ATT[WB[s.key].con != null ? "con" : s.key] || []).find(x => x[0] === n), a0 = VOICE.au; if (A && !s.said.includes(n) && t - s.t0 > 2500 && !(a0 && !a0.paused && !a0.ended) && !G.holoNext) { s.said.push(n); advHolo(`${A[1]}. ${A[2]}`); } } /* v388: the Advisor explains each attack as it is shown */""")
rep("""  const base = (WB[s.key].con != null ? 45 : 105) * WB[s.key].sc;""", """  const base = (WB[s.key].con != null ? 45 : WB[s.key].cam || 105) * WB[s.key].sc;""")
rep("""c.cineObj.fit = 1; c.goal = { dist: (WB[it.wb].con != null ? 45 : 105) * WB[it.wb].sc };""", """c.cineObj.fit = 1; c.goal = { dist: (WB[it.wb].con != null ? 45 : WB[it.wb].cam || 105) * WB[it.wb].sc };""")
# battle profiles and side lengths
rep("""wbCon: ["station", "beam", .3, 0, 0, 4]
};""", """wbCon: ["station", "beam", .3, 0, 0, 4],
  wbBrd: ["titan", "acid", .34, 0, 1.4, 6], wbTyr: ["titan", "mass", .36, 0, 1.2, 7], wbWym: ["titan", "beam", .38, 0, 1.6, 7], wbCol: ["titan", "laser", .36, 0, 1, 6]
};""")
rep("""const SIDE_LEN = { wbOvl: 1.8, wbDev: 1.8, wbWar: 1.8, wbCon: 1.4,""", """const SIDE_LEN = { wbOvl: 1.8, wbDev: 1.8, wbWar: 1.8, wbCon: 1.4, wbBrd: 1.8, wbTyr: 1.8, wbWym: 1.8, wbCol: 1.8,""")

# ---------- the events: Super Boss Hunt (Monday) and Titan Hunt (Wednesday) share one implementation ----------
a = t.index("const SB_W = k =>"); b = t.index("function shEvents() {")
t = t[:a] + r'''const SB_W = k => k === "ovl" || k === "dev" || wbG2(k) ? 3 : k === "war" ? 2 : 1; // Hunt points per hull section (2.5%) torn off
const SB_MILE = [[1, { shards: 2, mats: [["low", 2, 2]] }], [10, { shards: 5, mats: [["void", 3, 1], ["low", 3, 2]] }], [30, { shards: 10, item: "mb4", mats: [["cube", 4, 1]] }],
  [60, { shards: 20, mats: [["void", 5, 1], ["cube", 5, 1]] }], [120, { shards: 35, vip: 200, mats: [["void", 6, 1], ["cube", 5, 1]] }]];
const SB_G = { 1: { ev: "sboss", n: "Super Boss Hunt", day: "Monday", sk: "sb", art: "ovl", artN: "The Pyramid Overlord" }, 2: { ev: "tboss", n: "Titan Hunt", day: "Wednesday", sk: "sb2", art: "wym", artN: "The Event Horizon Wyrm" } };
const sbPts = (st, uid, g = 1) => { let n = 0; for (const k of wbKeys(g)) n += ((st.dmg[k] || {})[uid] || 0) * SB_W(k); return n; };
function sbBoard(st, g = 1) { const u = new Set(); for (const k of wbKeys(g)) for (const id in (st.dmg[k] || {})) u.add(id); return [...u].map(id => ({ id, pts: sbPts(st, id, g), me: id === G.me })).sort((a, b) => b.pts - a.pts); }
function sbMine(T = now(), g = 1) { const st = wbState(T), E = SB_G[g], cy = g === 2 ? st.cyc2 : st.cyc; let o = S[E.sk]; o = o && typeof o === "object" ? o : { cyc: cy, mile: [] }; S[E.sk] = o;
  if (o.cyc !== cy) { const last = o; // a new week: anything reached last week and not claimed is paid out now
    if (last.pts) { let got = 0; SB_MILE.forEach(([need, rw], i) => { if (last.pts >= need && !(last.mile || []).includes(i)) { grantRw(rw, E.n); got++; } }); if (got) note(`${E.n}: ${got} unclaimed milestone reward${got > 1 ? "s" : ""} from last week added to your stores.`, "win"); }
    o = S[E.sk] = { cyc: cy, mile: [] }; dirty(); }
  const pts = sbPts(st, G.me, g); if (pts !== o.pts) { o.pts = pts; dirty(); } return { st, pts, sb: o }; }
const sbReady = (g = 1) => { try { const { pts, sb } = sbMine(now(), g); return SB_MILE.filter(([need], i) => pts >= need && !sb.mile.includes(i)).length; } catch (e) { return 0; } };
/* the live feed: every hit the shared record reveals, newest first */
G.wbFeed = []; G.wbHitAt = {};
function sbFeedAdd(prev, st) { if (!prev) return; for (const k in WB) { if (stCyc(prev, k) !== stCyc(st, k)) continue; const d0 = prev.dmg[k] || {}, d1 = st.dmg[k] || {};
    for (const id in d1) { const dd = (d1[id] || 0) - (d0[id] || 0); if (dd <= 0) continue; G.wbHitAt[k] = Date.now(); G.wbFeed.unshift({ t: Date.now(), id, k, pc: Math.round(dd / WB_SEG * 100), kill: !(st.hp[k] > 0) && prev.hp[k] > 0 }); } }
  G.wbFeed.length = Math.min(G.wbFeed.length, 16); }
const SB_ART = {}, SB_ART_GO = {};
function sbArt(g = 1) { if (SB_ART[g] || SB_ART_GO[g] || typeof BOSS3D === "undefined" || battle) return SB_ART[g] || null; SB_ART_GO[g] = 1; // the banner, rendered once from the boss's model
  setTimeout(() => { try { const c = wbArt(SB_G[g].art, 760, 380, 5200, null); if (c) SB_ART[g] = c.toDataURL("image/webp", .86); } catch (e) {} wbArtFree(); if (SB_ART[g]) softRender(); }, 80); return null; }
function sbBanner(T, g = 1) { const E = SB_G[g], st = wbState(T), end = g === 2 ? wbEnd2(st.cyc2) : wbEnd(st.cyc), main = wbMain(g), up = main.filter(k => st.hp[k] > 0).length, art = sbArt(g);
  return `<div class="evban ev-sboss sbban${g === 2 ? " sb2" : ""}">${art ? `<img src="${art}" alt="${E.artN}">` : ""}<div class="sbtop"><span class="vlive on">● LIVE</span><b>${E.n}</b><small>${up ? `${up} of ${main.length} ${g === 2 ? "titans" : "world bosses"} still standing` : `Every ${g === 2 ? "titan" : "world boss"} has fallen this week`}</small></div>
    <span class="evend">${g === 2 ? "Titans" : "Bosses"} return in: <b data-end="${end}">${ftime(end - T)}</b></span></div>`; }
function sbOverview(T, g = 1) { const { st, pts, sb } = sbMine(T, g), me = Date.now(), keys = wbKeys(g);
  const row = k => { const D = WB[k], hp = st.hp[k] | 0, pc = Math.round(hp / WB_SEG * 100), my = ((st.dmg[k] || {})[G.me] || 0), hot = me - (G.wbHitAt[k] || 0) < 90e3;
    return `<div class="sbrow${hp ? "" : " down"}${hot ? " hot" : ""}"><div class="sbn"><b style="color:${D.col}">${D.ic} ${esc(D.n)}</b><span class="sbst">${hp ? (hot ? "⚔ UNDER ATTACK" : "ALIVE") : "DEFEATED"}</span></div>
      <div class="wbbar"><i style="width:${pc}%;background:${D.col}"></i></div><div class="sbm"><span>${hp ? `${pc}% hull` : "Down"}${k === "ovl" && hp ? ` · shield ${wbCons(T)}/4` : ""}</span><span>You: ${my ? Math.round(my / WB_SEG * 100) + "%" : "—"}</span></div>
      ${hp && wbG2(k) ? `<div class="sbtw">${wbTwist(k, T)}</div>` : ""}${hp ? `<div class="sbb"><button class="btn sm amber" data-act="wboss" data-id="${k}">⚔ Hunt</button><button class="btn sm ghost" data-act="cineObj" data-id="wb_${k}">◉ Scan</button></div>` : ""}</div>`; };
  const cons = g === 2 ? "" : `<div class="sbcons"><span>Overlord's conduits</span>${[0, 1, 2, 3].map(i => { const c = "c" + i, hp = st.hp[c] | 0; return `<button class="sbcon${hp ? "" : " down"}" data-act="wboss" data-id="${c}" aria-label="Energy Conduit ${"ABCD"[i]}">◆ ${"ABCD"[i]} <small>${hp ? Math.round(hp / WB_SEG * 100) + "%" : "✕"}</small></button>`; }).join("")}</div>`;
  const feed = G.wbFeed.filter(f => me - f.t < 30 * 60e3 && keys.includes(f.k)).slice(0, 6).map(f => `<li><span>${esc(f.id === G.me ? "You" : nameOf(f.id))}</span> ${f.kill ? "destroyed" : `tore ${f.pc}% off`} the ${esc(WB[f.k].n)} <i>${ftime(me - f.t)} ago</i></li>`).join("");
  const rules = g === 2 ? `The Brood Matriarch, the Iron Tyrant, the Event Horizon Wyrm and the Shard Colossus return every Wednesday at 18:00 UTC, each with a trick of its own: the Matriarch's swarm rebuilds while she's left alone, the Tyrant's bounty grows all week, the Wyrm takes full damage only while its glowing segments are exposed, and the Colossus shatters into shielding fragments but pays Void Shards in bulk. Every attack, win or lose, pays a bounty and drops forge materials, and every 2.5% of hull you destroy scores 3 Hunt points. When a titan falls, everyone who damaged it claims a share of its spoils.`
    : `The Pyramid Overlord, the Orbital Devourer and the Void Warden return every Monday at 18:00 UTC. Every attack, win or lose, pays a bounty for the hull it destroys and drops forge materials. Hunt points add up all week. When a boss falls, everyone who damaged it claims a share of its spoils, and milestones you reach but don't claim are paid out when the bosses return.`;
  return `<div class="evinfo sbinfo"><h4>Live board</h4>${wbMain(g).map(row).join("")}${cons}
    ${feed ? `<h4>Live feed</h4><ul class="sbfeed">${feed}</ul>` : ""}
    <h4>Your Hunt points</h4><p><b class="evscore">${fmt(pts)}</b> · ${pts ? (g === 2 ? "every 2.5% of hull you destroy scores 3" : "every 2.5% of hull you destroy scores 3 on the Overlord or Devourer, 2 on the Warden, 1 on a conduit") : `attack any ${g === 2 ? "titan" : "world boss"} to start scoring`}</p>
    <h4>Milestone rewards</h4>${SB_MILE.map(([need, rw], m) => `<div class="tier"><span class="tn">${fmt(need)} pts</span><span class="trw">${rwText(rw)}</span>${sb.mile.includes(m) ? '<span class="pill ok">Claimed</span>' : pts >= need ? '<span class="pill amb">Ready</span>' : '<span class="pill wait">—</span>'}</div>`).join("")}
    <h4>Event Rules</h4><p>${rules} Milestones you reach but don't claim are paid out when they return.</p></div>`; }
function sbRanking(T, g = 1) { const st = wbState(T), rows = sbBoard(st, g), mi = rows.findIndex(r => r.me), show = rows.slice(0, 50); if (mi >= 50) show.push(rows[mi]);
  return `<div class="evrank"><div class="evrh"><span>Rank</span><span>Commander</span><span>Hunt points</span></div>${show.map(r => { const pos = rows.indexOf(r) + 1; return `<div class="evrr${r.me ? " me" : ""}"><span>${pos <= 3 ? ["🥇", "🥈", "🥉"][pos - 1] : pos + "."}</span><span>${esc(r.me ? (G.myName || "You") + " (you)" : nameOf(r.id))}</span><span>${fmt(r.pts)}</span></div>`; }).join("") || `<p class="note" style="padding:10px">Nobody has hit a ${g === 2 ? "titan" : "world boss"} this week yet. Be the first.</p>`}</div>`; }
''' + t[b:]
rep("""const EVS = [["sboss", "Super Boss Hunt", "☠"], """, """const EVS = [["sboss", "Super Boss Hunt", "☠"], ["tboss", "Titan Hunt", "☣"], """)
rep("""  if (k === "sboss") return sbReady();""", """  if (k === "sboss") return sbReady();
  if (k === "tboss") return sbReady(2);""")
rep("""function evBanner(k, T) { if (k === "sboss") return sbBanner(T);""", """function evBanner(k, T) { if (k === "sboss") return sbBanner(T); if (k === "tboss") return sbBanner(T, 2);""")
rep("""  else if (k === "sboss") { body = tab === "ov" ? sbOverview(T) : sbRanking(T); const n = sbReady(); claim = `<button class="btn ${n ? "amber" : "ghost"} evclaim" data-act="sbClaim" ${n ? "" : "disabled"}>""",
"""  else if (k === "sboss" || k === "tboss") { const g = k === "tboss" ? 2 : 1; body = tab === "ov" ? sbOverview(T, g) : sbRanking(T, g); const n = sbReady(g); claim = `<button class="btn ${n ? "amber" : "ghost"} evclaim" data-act="sbClaim" data-g="${g}" ${n ? "" : "disabled"}>""")
rep("""  sbClaim: () => act(() => { const { pts, sb } = sbMine(); let n = 0; SB_MILE.forEach(([need, rw], i) => { if (pts >= need && !sb.mile.includes(i)) { sb.mile.push(i); grantRw(rw, "Super Boss Hunt"); n++; } }); if (n) toast(`Claimed ${n} Super Boss Hunt milestone${n > 1 ? "s" : ""}.`); }),""",
"""  sbClaim: d => act(() => { const g = +(d && d.g) === 2 ? 2 : 1, E = SB_G[g], { pts, sb } = sbMine(now(), g); let n = 0; SB_MILE.forEach(([need, rw], i) => { if (pts >= need && !sb.mile.includes(i)) { sb.mile.push(i); grantRw(rw, E.n); n++; } }); if (n) toast(`Claimed ${n} ${E.n} milestone${n > 1 ? "s" : ""}.`); }),""")
# the Finder's Map Events: the titans get their own section
rep("""<div class="list">${["ovl", "dev", "war"].map(k => { const D = WB[k], st = wbState(T), hp = st.hp[k] | 0; return `<button class="tgt mev${hp ? " mlive" : ""}" data-act="wboss" data-id="${k}"><span class="lvl" style="color:${D.col};border-color:${D.col}">${D.ic}</span><span><span class="nm">${D.n}</span><br><span class="sub">${hp ? `${Math.round(hp / WB_SEG * 100)}% hull · ${D.where}${k === "ovl" ? ` · shield ${wbCons(T)}/4 conduits` : ""}` : `Defeated · back in ${ftime(wbEnd(st.cyc) - T)}`}</span></span><span class="pill ${hp ? "bad" : "wait"}">${hp ? "Hunt" : "Down"}</span></button>`; }).join("")}</div>""",
"""${[1, 2].map(g => `${g === 2 ? `<h2 class="sec">Wednesday titans</h2><button class="btn ghost wide" data-act="events" data-ev="tboss" style="margin:0 0 8px">☣ Titan Hunt · live board, points and rewards</button>` : ""}<div class="list">${wbMain(g).map(k => { const D = WB[k], st = wbState(T), hp = st.hp[k] | 0; return `<button class="tgt mev${hp ? " mlive" : ""}" data-act="wboss" data-id="${k}"><span class="lvl" style="color:${D.col};border-color:${D.col}">${D.ic}</span><span><span class="nm">${D.n}</span><br><span class="sub">${hp ? `${Math.round(hp / WB_SEG * 100)}% hull · ${D.where}${k === "ovl" ? ` · shield ${wbCons(T)}/4 conduits` : ""}` : `Defeated · back in ${ftime(wbEndOf(k, stCyc(st, k)) - T)}`}</span>${hp && wbG2(k) ? `<br><span class="sub">${wbTwist(k, T)}</span>` : ""}</span><span class="pill ${hp ? "bad" : "wait"}">${hp ? "Hunt" : "Down"}</span></button>`; }).join("")}</div>`).join("")}""")
i = t.index('</style>', t.index('.fshero{'))
t = t[:i] + "\n/* v388 Titan Hunt */\n.sbtw{margin:4px 0 2px;font:600 11px/1.35 ui-monospace,monospace;color:#ffd9a8}.sb2 img{object-position:50% 40%}.ec-tboss .eci{color:#c8ff60}\n" + t[i:]

# ---------- the Advisor ----------
rep("""  wbcon: "Commander, this conduit feeds""", """  wbbrd: "Commander, the Brood Matriarch is nesting in the Far Reach. Beware her hatching swarm, the acid she sprays, and the slam of her scythes. Her drones rebuild while she's left alone, so keep up the attack.",
  wbtyr: "Commander, the Iron Tyrant is sailing the pirate trade lanes. Beware its broadside, the boarding claw that tears into our ships, and the mines it drops behind it. Its vault grows all week, so the later we hit it, the richer the bounty.",
  wbwym: "Commander, the Event Horizon Wyrm is coiled in the Core. Beware its gravity coil, the lens beam from its jaws, and the sweep of its tail. Strike while its glowing segments are exposed, or our fleet does only half damage.",
  wbcol: "Commander, the Shard Colossus has woken in the crystal fields. Beware its crystal rain, the prism beam that bounces between our ships, and the shatter when it breaks apart. It pays Void Shards in bulk.",
  wbcon: "Commander, this conduit feeds""")
rep("""const ADV_NEWS = {""", """const ADV_NEWS = {"wb2_new": "Commander, the Wednesday titans have arrived! The Brood Matriarch, the Iron Tyrant, the Event Horizon Wyrm and the Shard Colossus are loose on the map. The Titan Hunt is on in Events.", "wb_live_brd": "Commander, the Brood Matriarch is under attack right now! Watch it live.", "wb_live_tyr": "Commander, someone is fighting the Iron Tyrant right now! Watch it live.", "wb_live_wym": "Commander, the Event Horizon Wyrm is under attack right now! Watch it live.", "wb_live_col": "Commander, the Shard Colossus is under attack right now! Watch it live.", "wb_fall_brd": "Commander, the Brood Matriarch has fallen! Everyone who fought her can claim the spoils.", "wb_fall_tyr": "Commander, the Iron Tyrant has been sunk! Its vault is open, and everyone who fought it can claim the spoils.", "wb_fall_wym": "Commander, the Event Horizon Wyrm is destroyed! Everyone who fought it can claim the spoils.", "wb_fall_col": "Commander, the Shard Colossus has shattered for good! Everyone who fought it can claim the spoils.", """)
rep("""  const c = wbCyc(T); if (T - (WB_BASE + c * WEEK) < 24 * 3600e3) advNews("wb_new", "wb:" + c, { act: "find", r: "ev" }, "Hunt the bosses"); }""",
"""  const c = wbCyc(T); if (T - (WB_BASE + c * WEEK) < 24 * 3600e3) advNews("wb_new", "wb:" + c, { act: "find", r: "ev" }, "Hunt the bosses");
  const c2 = wbCyc2(T); if (T - (WB2_BASE + c2 * WEEK) < 24 * 3600e3) advNews("wb2_new", "wb2:" + c2, { act: "events", ev: "tboss" }, "Titan Hunt"); }""")
rep("""function wbNews(prev, st) { if (!prev || prev.cyc !== st.cyc) return; const c = st.cyc, live = k =>""", """function wbNews(prev, st) { if (!prev) return; const live = k =>""")
rep("""  for (const k in WB) { if (st.hp[k] >= prev.hp[k]) continue; if (st.hp[k] > 0) live(k);""", """  for (const k in WB) { const c = stCyc(st, k); if (stCyc(prev, k) !== c || st.hp[k] >= prev.hp[k]) continue; if (st.hp[k] > 0) live(k);""")
# FAQ
rep("""Every hit pays a bounty, and when one falls, everyone who fought it shares the spoils."]""", """Every hit pays a bounty, and when one falls, everyone who fought it shares the spoils."], ["What are the Wednesday titans?", "The Brood Matriarch, the Iron Tyrant, the Event Horizon Wyrm and the Shard Colossus return every Wednesday at eighteen hundred UTC, each with its own trick. The Matriarch's swarm rebuilds if she's left alone, the Tyrant's bounty grows all week, the Wyrm takes full damage only while its glowing segments are exposed, and the Colossus shatters into shielding fragments. The Titan Hunt in Events tracks them live."]""")
open(p, "w").write(t); print("ok")
