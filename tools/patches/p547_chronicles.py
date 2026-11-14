# v547 the Chronicles, a voiced story campaign (owner: "Do it all", idea #4: "Yes I want it all"). Six chapters about the signal under
# the Hive's chatter, the Ancient Archives, the monsters, Vael'Khor, the great bosses and the Cube. Each chapter has an Advisor briefing
# (voiced), three missions measured from when the chapter began, a reward, and a voiced closing line. The card sits in Quests under
# "Ready to claim". The last chapter gives the "Chronicler" title; the story continues with later seasons.
import sys, re, json
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
CH = [
 ("The Silent Signal", "Commander, our listening posts caught a signal under the Hive's chatter. It's old. Older than the Hive. Clear the garrisons around us so we can trace it.",
  [["hiveWins", 3, "Beat 3 Hive garrisons"], ["built", 3, "Finish 3 constructions"], ["fleetsSent", 3, "Send 3 fleets"]], {"shards": 15, "item": "xb_silver"},
  "The signal points inward, toward the Void. Something out there is still broadcasting."),
 ("Echoes in the Archives", "The signal matches records in the Ancient Archives. The old empires heard it too. Recover what they left behind.",
  [["arch", 2, "Recover 2 Archive records"], ["researched", 2, "Finish 2 researches"], ["caches", 2, "Haul in 2 salvage pods"]], {"shards": 20, "item": "xr_silver"},
  "Every civilization that heard the signal left the same warning. Then they went silent."),
 ("Hunters of the Deep", "The space monsters are drawn to the signal like moths to a star. Thin their numbers and we'll learn where they're heading.",
  [["monKills", 2, "Slay 2 space monsters"], ["battlesWon", 5, "Win 5 battles"], ["shipsBuilt", 50, "Build 50 ships or defences"]], {"shards": 25, "item": "mb2"},
  "They're circling something in the inner layers. Not hunting, Commander. Guarding."),
 ("The Queen's Shadow", "Vael'Khor's swarm is massing along the lanes the signal travels. She knows we're listening. Push her back.",
  [["hiveWins", 8, "Beat 8 Hive garrisons"], ["fleetsSent", 10, "Send 10 fleets"], ["worlds", 3, "Hold 3 worlds"]], {"shards": 30, "item": "bf_silver"},
  "Her drones carry fragments of the same code. The Hive didn't create the signal. It answers to it."),
 ("Gods of the Old Sky", "The great bosses wake on a schedule older than our calendar. I think the signal is their clock. Strike them and listen.",
  [["bosses", 2, "Strike a boss 2 times"], ["researched", 4, "Finish 4 researches"], ["monKills", 4, "Slay 4 space monsters"]], {"shards": 40, "item": "mb3"},
  "Every boss we strike makes the signal stutter. They're tied to it, Commander. All of them."),
 ("The Cube Awakens", "The signal's source is the Cube. It isn't calling for help. It's counting down. Make us ready.",
  [["battlesWon", 15, "Win 15 battles"], ["built", 10, "Finish 10 constructions"], ["joints", 1, "Join an alliance joint strike"]], {"shards": 50, "item": "pAll_gold", "title": "Chronicler"},
  "We've heard the countdown, Commander. When it ends, we'll be ready. The story continues next season."),
]
js = json.dumps([{"t": t, "say": a, "m": m, "rw": rw, "end": e} for t, a, m, rw, e in CH], ensure_ascii=False)
JS = r'''
/* ---------- v547 the Chronicles ---------- */
const CHRON = ''' + js + r''';
const chStat = k => k === "arch" ? ARCH_ORD.filter(x => archLv(x)).length : k === "worlds" ? myPlanets().length : vpStat(k);
function chState() { if (!S.chron) { S.chron = { c: 0, base: {} }; for (const m of CHRON[0].m) S.chron.base[m[0]] = chStat(m[0]); dirty(); } return S.chron; }
const chProg = (C, m) => m[0] === "worlds" ? Math.min(m[1], chStat("worlds")) : Math.min(m[1], Math.max(0, chStat(m[0]) - (C.base[m[0]] || 0)));
function chronHTML() { if (!S || !S.tut || S.tut.k !== "done") return ""; const C = chState(); if (C.c >= CHRON.length) return `<article class="card chron done"><header>📖 Chronicles · complete</header><p>${esc(CHRON[CHRON.length - 1].end)}</p></article>`;
  const ch = CHRON[C.c], ms = ch.m.map(m => [m, chProg(C, m)]), all = ms.every(([m, p]) => p >= m[1]);
  return `<article class="card chron${all ? " hi" : ""}"><header><span>📖 Chronicles · Chapter ${C.c + 1} of ${CHRON.length}</span><b>${esc(ch.t)}</b></header>
    <div class="chsay"><img src="${ADV_ART}" alt=""><p>${esc(ch.say)}</p><button class="btn ghost sm" data-act="chPlay" aria-label="Hear the briefing">▶</button></div>
    ${ms.map(([m, p]) => `<div class="vpm${p >= m[1] ? " done" : ""}"><div><b>${esc(m[2])}</b><div class="vpmb"><i style="width:${(p / m[1] * 100).toFixed(0)}%"></i></div></div><span>${p >= m[1] ? "✓" : `${fmt(p)}/${fmt(m[1])}`}</span></div>`).join("")}
    <div class="rw"><span class="cost"><span class="shard">◆${ch.rw.shards}</span> · ${esc(SHOP[ch.rw.item] ? SHOP[ch.rw.item].n : "")}${ch.rw.title ? ` · Title “${esc(ch.rw.title)}”` : ""}</span><button class="btn ${all ? "amber" : "ghost"}" data-act="chClaim" ${all ? "" : "disabled"}>${all ? "Complete chapter" : "In progress"}</button></div></article>`; }
'''
rep('function vQuests() {', JS + 'function vQuests() {')
rep('''    ${S.retGift ? `<article class="card quest${S.retGift.at <= T ? " done hi" : ""}">''', '''    ${chronHTML()}${S.retGift ? `<article class="card quest${S.retGift.at <= T ? " done hi" : ""}">''')
rep('  vpBuyTier: () => act(() => {', '''  chPlay: () => { const C = chState(); if (C.c < CHRON.length) { speak(CHRON[C.c].say); advHolo(CHRON[C.c].say, true); } }, /* v547 */
  chClaim: () => act(() => { const C = chState(), ch = CHRON[C.c]; if (!ch || !ch.m.every(m => chProg(C, m) >= m[1])) return; S.shards = (S.shards || 0) + ch.rw.shards; if (SHOP[ch.rw.item]) giveItem(ch.rw.item); if (ch.rw.title) { S.vpTitles = S.vpTitles || []; if (!S.vpTitles.includes(ch.rw.title)) S.vpTitles.push(ch.rw.title); }
    toast(`Chapter ${C.c + 1} complete: ◆${ch.rw.shards} and a ${SHOP[ch.rw.item] ? SHOP[ch.rw.item].n : "reward"}.`, "win"); C.c++; C.base = {}; if (C.c < CHRON.length) for (const m of CHRON[C.c].m) C.base[m[0]] = chStat(m[0]);
    setTimeout(() => { say([ch.end].concat(C.c < CHRON.length ? [CHRON[C.c].say] : [])); }, 500); try { SFX.fanfare(true); } catch (e) {} }),
  vpBuyTier: () => act(() => {''')
css = '''
/* v547 the Chronicles */
.chron{border-color:rgba(226,196,138,.55);background:linear-gradient(160deg,rgba(226,196,138,.12),rgba(8,14,22,.92) 55%)}.chron header{display:flex;flex-direction:column;gap:2px}.chron header span{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#e2c48a}.chron header b{font:800 19px var(--f-display,sans-serif)}
.chsay{display:grid;grid-template-columns:44px minmax(0,1fr) auto;gap:10px;align-items:start;margin:8px 0}.chsay img{width:44px;height:44px;border-radius:50%;object-fit:cover;object-position:50% 15%;border:1px solid rgba(226,196,138,.6)}.chsay p{margin:0;font-size:13.5px;font-style:italic;color:#e9f1f7}
.chron .vpm{margin-top:6px}.chron .rw{margin-top:10px}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 546\b", "GAME_V = 547", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
# the voice lines for the lab
def h(t):
    x = 2166136261
    for ch in t: x ^= ord(ch); x = (x * 16777619) & 0xffffffff
    return x
def b36(n):
    d = '0123456789abcdefghijklmnopqrstuvwxyz'; o = ''
    while n: o = d[n % 36] + o; n //= 36
    return o or '0'
out = []
for i, (t, a, m, rw, e) in enumerate(CH):
    out += [{"key": b36(h(a)), "where": f"Chronicles {i + 1} · briefing", "line": a}, {"key": b36(h(e)), "where": f"Chronicles {i + 1} · closing", "line": e}]
if len(sys.argv) > 2: json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
