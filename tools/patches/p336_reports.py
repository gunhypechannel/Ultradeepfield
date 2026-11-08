# v336: the Academy walks through the espionage report (resources, defenders, battle forecast) and has you watch your first battle replay
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
# report sections get a "Got it" stop during the scouting step
rep('''  const sec = (title, body) => `<section class="spys"><h3>${title}</h3>${body}</section>`, plunder''',
'''  const tour = tutAt("scoutR") && (S.tutTour || 0) < 3 ? S.tutTour || 0 : -1; /* v336: three stops through your first report */
  const sec = (title, body) => { const k = SPY_TOUR.findIndex(x => x[0].test(title)), on = k >= 0 && k === tour; return `<section class="spys${on ? " tourOn" : ""}"><h3>${title}</h3>${body}${on ? `<p class="tourtip">💡 ${SPY_TOUR[k][1]}</p><button class="btn amber sm" data-act="tutTour">Got it ›</button>` : ""}</section>${on && k === 2 ? `<div style="height:55vh"></div>` : ""}`; }, plunder''')
rep('function shSpyRep() {', '''const SPY_TOUR = [[/^Resources$/, "What's stored there. Win the fight and your ships carry part of it home."], [/^(Hive swarm|Fleet)$/, "The ships guarding it. Compare them with your own fleet."], [/^Battle forecast$/, "The verdict: a simulated battle against your fleet. Green means attack."]];
function shSpyRep() {''')
rep('''{ lv: 3, id: "scoutR", t: "Read the espionage report", say: "The probes made it in. Open the report in Mail: it counts the defenders and tells you if your fighters would win.", ok: s => (s.tutSpyR || 0) >= 1, go: { v: "mail" }, path: () => [''',
'''{ lv: 3, id: "scoutR", t: "Read the espionage report", say: "The probes made it in. Open the report in Mail and I'll walk you through it: what's stored there, what's guarding it, and whether your fighters would win.", ok: s => (s.tutSpyR || 0) >= 1 && (s.tutTour || 0) >= 3, go: { v: "mail" }, path: () => [['.sheet [data-act="tutTour"]', ["Resources you could take: tap Got it", "The defenders: tap Got it", "Will you win? Read the forecast, then tap Got it"][S.tutTour || 0]], ''')
rep('''  repSave: d => {''', '''  tutTour: () => { S.tutTour = Math.min(3, (S.tutTour || 0) + 1); dirty(); renderSheet(); setTimeout(() => { const n = $(".sheet .tourOn"); if (n) n.scrollIntoView({ block: "start", behavior: "smooth" }); }, 60); /* the tip then sits below the Got it button, not over what you're reading */ coachRender(true); }, // v336
  repSave: d => {''')
# battle replay step
rep('''{ lv: 4, t: "Read your reports in Mail", say: "Every battle, espionage report and message lands in Mail. Replays show you exactly why you won or lost.", ok: s => !!s.tutMail, go: { v: "mail" }, path: () => [DOCKT("mail", "Open Mail")],''',
'''{ lv: 4, id: "read-your-reports-in-mail", t: "Watch your battle replay", say: "Every battle lands in Mail with a full report. Open the report of your Hive victory and tap Watch the battle: the replay shows exactly why you won.", ok: s => !!s.tutReplay || !(s.reports || []).some(r => r.rounds && r.rounds.length), go: { v: "mail" }, /* v336: was "open Mail" */
    path: () => [['.sheet [data-act="replay"]', "Tap Watch the battle"], ['.mrowc.good[data-act="mreport"]', "Open your battle report"], ['[data-act="mreport"]', "Open your battle report"], DOCKT("mail", "Open Mail")],''')
rep('''  replay: d => { const r = findRep(d.id); closeSheet(); if (r) playBattle(r); },''',
'''  replay: d => { const r = findRep(d.id); closeSheet(); if (r) { if (!S.tutReplay) { S.tutReplay = 1; dirty(); } playBattle(r); } },''')
# styles
i = t.index('\n</style>', t.index('<style>\n')) + 1; t = t[:i] + '.spys.tourOn{border-color:var(--amber)!important;box-shadow:0 0 0 1px var(--amber),0 0 18px rgba(255,190,80,.25)}.tourtip{margin:8px 0 6px;color:var(--amber);font-size:14px;line-height:1.35}\n' + t[i:]
open(p, 'w', encoding='utf-8').write(t); print('ok')
