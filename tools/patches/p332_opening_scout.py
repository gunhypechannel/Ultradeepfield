import sys, re
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# v332 (owner's order for the opening): a battle we LOSE, then rebuild; scout before the first attack.
# 1) the opening ambush is lost: the convoy is destroyed and the crew escapes to the homeworld
rep('''  let res = null, tech = 2; for (let i = 0; i < 16; i++) { res = simulate(stacksOf(hive, { hive: 9 }, null), stacksOf(ours, { weapons: tech, shields: tech, armor: tech }, G.me), { seed: 4100 + i }); if (res.winner === "d") break; if (i % 4 === 3) tech++; } // we always come through it''',
    '''  let res = null, tech = 2, best = null; for (let i = 0; i < 24; i++) { res = simulate(stacksOf(hive, { hive: 9 }, null), stacksOf(ours, { weapons: tech, shields: tech, armor: tech }, G.me), { seed: 4100 + i }); if (res.winner === "a") { if (!best || res.rounds.length > best.rounds.length) best = res; if (res.rounds.length >= 4) break; } if (i % 6 === 5 && !best) tech = Math.max(0, tech - 1); } // v332: the swarm wins: a long fight we lose
  if (best) res = best;''')
rep('''const INTRO_POST = ["The swarm is broken. We held, Commander.", "That swarm answered to Vael'Khor, the Hive Matriarch. She devours whole worlds, and now she knows our name.", "It cost us dearly, and our reactors were nearly dry. We set down on the nearest world we could reach."];''',
    '''const INTRO_POST = ["We lost them, Commander. The swarm tore through every ship in the convoy.", "That swarm answered to Vael'Khor, the Hive Matriarch. She devours whole worlds, and now she knows our name.", "Only our escape pods got clear. We came down on the nearest world we could reach, with nothing but the crew."]; // v332: the opening is a defeat''')
# 2) scout before the first attack: Fleet Command sends 4 probes, you spy on the garrison and read the report, then attack it
rep('''  /* v318: launch, then follow the fleet on the map, rush it and film it while it flies, then the win */''',
    '''  /* v332: scout first (the owner's order: fighters, espionage, the report, then the attack). Fleet Command sends 4 probes; they're yours to keep */
  { lv: 3, id: "scout0", t: "Spy on the Hive garrison", say: "Never attack blind. Fleet Command just sent us four Espionage Probes. I've marked a weak Hive garrison near us: tap Espionage on its card and send the probes.", ok: s => ((s.stats || {}).spies || 0) >= 1, hive: 1, path: () => [['.sheet [data-act="spyGo"]:not([disabled])', "Tap Send probes"], ['.sheet [data-act="spy"]', "Tap Espionage"], SHOWME], rw: { m: 600, c: 400, shards: 1 } },
  { lv: 3, id: "scoutR", t: "Read the espionage report", say: "The probes made it in. Open the report in Mail: it counts the defenders and tells you if your fighters would win.", ok: s => (s.tutSpyR || 0) >= 1, go: { v: "mail" }, path: () => [['[data-act="spyOpen"]', "Open the espionage report"], DOCKT("mail", "Open Mail")], rw: { m: 600, c: 400, g: 200 } },
  /* v318: launch, then follow the fleet on the map, rush it and film it while it flies, then the win */''')
rep('''  { lv: 3, t: "Attack a Hive garrison", say: "The amber worlds belong to Vael'Khor's Hive. I've marked a weak garrison near us: send the fighters and show her we bite back.",''',
    '''  { lv: 3, t: "Attack a Hive garrison", say: "Now we know what's waiting there. Send the fighters at that garrison and show Vael'Khor we bite back.",''')
# the later scouting run is a second one for new commanders (commanders who were already past this point need just one)
rep('''ok: s => own("spyProbe") >= 2 || ((s.stats || {}).spies || 0) >= 1, go: { v: "build", s: "ships" }, path: tutUnit("spyProbe", 2)''', '''ok: s => own("spyProbe") >= 2 || ((s.stats || {}).spies || 0) >= (s.tutScouted ? 2 : 1), go: { v: "build", s: "ships" }, path: tutUnit("spyProbe", 2)''')
rep('''{ lv: 6, id: "spy", t: "Spy on a Hive world", say: "I've marked the weakest Hive world near us. Tap Espionage on its card and send your probes.", ok: s => ((s.stats || {}).spies || 0) >= 1,''',
    '''{ lv: 6, id: "spy", t: "Spy on a Hive world", say: "I've marked the weakest Hive world near us. Tap Espionage on its card and send your probes.", ok: s => ((s.stats || {}).spies || 0) >= (s.tutScouted ? 2 : 1),''')
rep('''{ lv: 6, t: "Read the espionage report", say: "The probes are back. Open the report in Mail: it shows the defenders, their ships and the resources you could take home.", ok: s => !!s.tutSpyR,''',
    '''{ lv: 6, t: "Read the espionage report", say: "The probes are back. Open the report in Mail: it shows the defenders, their ships and the resources you could take home.", ok: s => (s.tutSpyR || 0) >= (s.tutScouted ? 2 : 1),''')
# reading a report counts each new report once (two Academy steps read one)
rep('''if (r && !S.tutSpyR) { S.tutSpyR = 1; dirty(); } // v301: the Academy's "read the report" step''',
    '''if (r && !(S.tutSpyRd || []).includes(r.at)) { S.tutSpyRd = (S.tutSpyRd || []).concat([r.at]).slice(-6); S.tutSpyR = (S.tutSpyR || 0) + 1; dirty(); } // v332: each report counts once (v301: the Academy's "read the report" steps)''')
# the Academy's spy runs send every probe you have (enough to see the defenders) and remember the target
rep('''n = clamp(Math.floor(+(($("#spyn") || {}).value) || sheet.pn || 1), 1, have);''', '''n = clamp(Math.floor(+(($("#spyn") || {}).value) || sheet.pn || (tutOn() ? have : 1)), 1, have);''')
rep('''if (tutAt("spy")) { S.tutSpyP = p.id; S.tutSpyW = (S.stats || {}).hiveWins || 0; tutMark(p.id); }''', '''if (tutAt("spy")) { S.tutSpyP = p.id; S.tutSpyW = (S.stats || {}).hiveWins || 0; tutMark(p.id); } if (tutAt("scout0")) { S.tutScouted = 1; tutMark(p.id); }''')
# the probes arrive when the scouting step opens (once per commander), and saves already past it keep their place
rep('''  if (!S.tutHop) { S.tutHop = 1; if (tutOn()) S.advHop = 0; dirty(); } /* v324: commanders mid-Academy go back to its path */''',
    '''  if (!S.tutHop) { S.tutHop = 1; if (tutOn()) S.advHop = 0; dirty(); } /* v324: commanders mid-Academy go back to its path */
  if (!S.tutScout) { S.tutScout = 1; if (S.tut.i > 12) S.tut.i = Math.min(TUT.length, S.tut.i + 2); dirty(); } /* v332: two scouting steps before the first attack; anyone past them keeps their place */
  if (tutAt("scout0") && !S.tutLoan) { S.tutLoan = 1; S.ships.spyProbe = (S.ships.spyProbe || 0) + 4; dirty(); note("Fleet Command sent 4 Espionage Probes for the Academy.", "win"); }''')
v = int(re.search(r"const GAME_V = (\d+)", t).group(1)); t = t.replace(f"const GAME_V = {v}", "const GAME_V = 332", 1)
open(p, 'w', encoding='utf-8', newline='').write(t); print('v332 from', v)
