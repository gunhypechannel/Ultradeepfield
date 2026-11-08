# v339: the Flight Academy ends at Astrophysics Lv.2 (step 40). The steps after it (probes, scouting, the colony, pirates, the Dock and
# the flagship) carry on as Missions: same steps, rewards and hologram briefings, but no pointer or guide ring, no free speed-ups,
# no Academy build times. The Fleet Path no longer hands out speed-ups either.
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep('const tutOn = () => S && S.tut && !S.tut.off && S.tut.i < TUT.length;', '''const tutOn = () => S && S.tut && !S.tut.off && S.tut.i < TUT.length;
const ACAD_END = TUT.findIndex(s => s.id === "research-astrophysics-lv-2"), MIS_N = TUT.length - ACAD_END - 1; /* v339 */
const acadOn = () => tutOn() && S.tut.i <= ACAD_END; // the Academy proper: guide, speed-ups, Academy build times
const tutCount = () => acadOn() ? `Flight Academy · step ${S.tut.i + 1} of ${ACAD_END + 1}` : `Mission ${S.tut.i - ACAD_END} of ${MIS_N}`;''')
rep('const acadT = t => { if (!(S && S.tut && tutOn())) return t;', 'const acadT = t => { if (!(S && S.tut && acadOn())) return t;')
rep('const aca = tutOn()', 'const aca = acadOn()')
rep('document.body.classList.toggle("acadon", tutOn())', 'document.body.classList.toggle("acadon", acadOn())')
rep('g.classList.toggle("acad", tutOn())', 'g.classList.toggle("acad", acadOn())')
rep('function tutBoostTopUp() { if (!tutOn()) return;', 'function tutBoostTopUp() { if (!acadOn()) return;')
rep('function pathBoostTopUp() { if (!S || tutOn()) return;', 'function pathBoostTopUp() { return; /* v339: off. Free speed-ups end with the Academy */ if (!S || tutOn()) return;')
# no pointer on Missions
rep('(m => m === "tut" ? TUT[S.tut.i] : m === "ship" ? shipStep() : null)(advPick())', '(m => m === "tut" ? (acadOn() ? TUT[S.tut.i] : null) : m === "ship" ? shipStep() : null)(advPick())')
# labels
rep('<small>ADVISOR · FLIGHT ACADEMY · STEP ${S.tut.i + 1} OF ${TUT.length}</small>', '<small>ADVISOR · ${esc(tutCount().toUpperCase())}</small>')
rep('<div class="cbar"><i style="width:${Math.min(100, S.tut.i / TUT.length * 100)}%"></i></div>', '<div class="cbar"><i style="width:${Math.min(100, acadOn() ? S.tut.i / (ACAD_END + 1) * 100 : (S.tut.i - ACAD_END - 1) / MIS_N * 100)}%"></i></div>')
rep('<span>${done ? "★" : `${S.tut.i + 1}/${TUT.length}`}</span><b class="cpt"><small>${done ? "STEP DONE" : "NEXT TASK"}</small>', '<span>${done ? "★" : acadOn() ? `${S.tut.i + 1}/${ACAD_END + 1}` : `M${S.tut.i - ACAD_END}`}</span><b class="cpt"><small>${done ? "STEP DONE" : acadOn() ? "NEXT TASK" : "MISSION"}</small>')
rep('<h2 class="sec">Flight Academy · step ${S.tut.i + 1} of ${TUT.length}</h2>', '<h2 class="sec">${tutCount()}</h2>')
# the Academy ends at Astrophysics Lv.2: the celebration and the convoy move there; the last mission gets its own send-off
rep('''  if (nx || back) toast(`Academy step done:''', '''  const fin = st.id === "research-astrophysics-lv-2" && !S.acadDone; /* v339 */
  if (fin) { S.acadDone = 1; if (!S.retGift) S.retGift = { at: now() + 8 * 3600e3, rw: { m: 30000, c: 20000, g: 10000, shards: 10 } };
    celebrate({ k: "acad", kick: "Flight Academy", t: "Academy Complete", art: "adv", s: "You've built a balanced homeworld, won your first battles and can now hold a second world. From here, Missions carry on with my briefings, but you lead the way.", rw: "Fleet Command is sending a supply convoy: 30K metal, 20K crystal, 10K gas and ◆10. It lands in 8 hours.", chat: 1, go: "Onward, Commander" });
    S.say.push("That's the Academy finished, Commander. From here, missions keep coming with my briefings, but you lead the way: no more pointers, and no more free speed-ups.", "For stronger ships, follow the Fleet Path: every new hull needs a bigger Shipyard and new research, and its card shows the whole road with a tick for each step.", "And Commander: Fleet Command's supply convoy lands in 8 hours. Come back then and claim it on the Quests tab."); flushSay(); }
  if ((nx || back) && !fin) toast(`${nx && TUT.indexOf(nx) > ACAD_END + 1 ? "Mission" : "Academy step"} done:''')
rep('''  if (!nx && !back) { S.retGift = { at: now() + 8 * 3600e3, rw: { m: 30000, c: 20000, g: 10000, shards: 10 } }; // v328
    celebrate({ k: "acad", kick: "Flight Academy", t: "Academy Complete",''', '''  if (!nx && !back && S.acadDone) { celebrate({ k: "missions", kick: "Missions", t: "Flagship Commissioned", art: "adv", s: "Every mission done: a second world taken from the Hive, pirates raided and our flagship in command. The galaxy is yours to take.", rw: "Your flagship earns experience in every fight. Equip it at the Flagship Dock.", chat: 1, go: "Onward, Commander" });
    S.say.push("Our flagship is commissioned, Commander. It leads every fleet now, earns experience in every fight, and the Flagship Dock forges its gear.", "Every 2 Astrophysics levels lets us hold another world: build more Colony Ships and send them with escorts to Hive worlds we can beat. I'll keep pointing you at the next directive on your path."); S.pathOpen = 1; flushSay(); }
  else if (!nx && !back) { S.retGift = { at: now() + 8 * 3600e3, rw: { m: 30000, c: 20000, g: 10000, shards: 10 } }; // v328 (commanders who were past Astrophysics Lv.2 before v339)
    celebrate({ k: "acad", kick: "Flight Academy", t: "Academy Complete",''')
for a, b in [('${nx && TUT.indexOf(nx) > ACAD_END + 1 ? "Mission" : "Academy step"} done:', '${TUT.indexOf(st) > ACAD_END ? "Mission" : "Academy step"} done:'), ('(m => m === "tut" ? (acadOn() ? TUT[S.tut.i] : null)', '(m => m === "tut" ? (acadOn() || window.__botGuide ? TUT[S.tut.i] : null)')]: rep(a, b)
rep('The Academy is right where you left it: step ${S.tut.i + 1} of ${TUT.length}.', 'Your ${acadOn() ? "Academy" : "missions"} are right where you left them: ${tutCount()}.')
open(p, 'w', encoding='utf-8').write(t); print('ok')
