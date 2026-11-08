# v337: (1) an Academy step that shows building cards have tabs (Shipyard: Repair, then Production);
#       (2) a one-time hologram transmission the first time you open any building's or ship's card
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
i = t.index('  { lv: 2, t: "Build the Research Center"'); j = t.index('\n', i) + 1
TABS = '''  /* v337: building cards hold more than an upgrade button */
  { lv: 2, id: "tabs", t: "Explore the Shipyard's tabs", say: "Some building cards hold more than an upgrade. Open the Shipyard: its Repair tab rebuilds ships wrecked in battle, and its Production tab is where every ship is built. The Research Center's Research tab works the same way.", ok: s => ((s.tutTabs || 0) & 3) === 3,
    path: () => sheet && sheet.type === "detail" && sheet.k === "shipyard" && !sheet.pid ? [(S.tutTabs || 0) & 1 ? ['.sheet [data-act="dtab"][data-i="1"]', "Tap the Production tab: ships are built here"] : ['.sheet [data-act="dtab"][data-i="2"]', "Tap the Repair tab: wrecked ships are rebuilt here"]]
      : [['article.bn[data-kind="b"][data-k="shipyard"]', "Choose Shipyard: open its card"], ['[data-act="bcat"][data-v="fac"]', "Open Facility"], ['[data-act="sub"][data-g="build"][data-v="bld"]', "Open Structures"], DOCKT("build", "Tap Build")], rw: { m: 600, c: 400, g: 200 } },
'''
t = t[:j] + TABS + t[j:]
rep('const TUT_BASICS = 18;', 'const TUT_BASICS = 19; /* v337: + the tabs step */')
rep('  dtab: d => { if (!sheet) return; const i = +d.i;', '  dtab: d => { if (!sheet) return; const i = +d.i; if (sheet.type === "detail" && sheet.k === "shipyard" && !sheet.pid && (i === 1 || i === 2)) { S.tutTabs = (S.tutTabs || 0) | (i === 2 ? 1 : 2); dirty(); } /* v337 */')
rep('  if (!S.tutEcon) {', '  if (!S.tutTabs0) { S.tutTabs0 = 1; if (!S.tut.k && S.tut.i >= 10) S.tut.i = Math.min(TUT.length, S.tut.i + 1); dirty(); } /* v337: the tabs step; saves that know their step id are placed by it */\n  if (!S.tutEcon) {')
# first-open transmissions
rep('const tutAt = id =>', '''/* v337: the first time you open a building's or ship's card, the Advisor's hologram says what it is for and how to use it */
const HOLO = {
  metalMine: "The Metal Extractor. Metal pays for almost everything we build, so keep this our highest extractor, about two levels above crystal.",
  crystalMine: "The Crystal Refinery. Research and better hulls run on crystal. Keep it about two levels behind metal.",
  gasSynth: "The Gas Synthesizer. Gas fuels every flight and most research. It draws the most power, so raise the Solar Array first.",
  solar: "The Solar Array powers every extractor. When the Power shortage card turns red, upgrade this before anything else.",
  metalStore: "The Metal Silo. When it is full, the Metal Extractor stops. Raise it whenever metal sits at the cap.",
  crystalStore: "The Crystal Vault. A full vault stops the refinery. Keep it ahead of your crystal income.",
  gasTank: "The Gas Tank. A full tank stops the synthesizer. Raise it as your gas income grows.",
  robotics: "Drone Works. Every level speeds up all construction on this world. Keep it rising with your economy.",
  shipyard: "The Shipyard. Its Production tab builds ships, and its Repair tab rebuilds wrecks. Higher levels unlock heavier hulls.",
  lab: "The Research Center. Its Research tab opens the whole tech tree, and every level speeds research up.",
  radar: "The Radar Station. Its Warning tab shows enemy fleets on their way. Every level spots them five minutes sooner.",
  repairYard: "The Repair Yard. Ships wrecked in battle are towed home and rebuilt here, and it puts out fires on our worlds.",
  missileSilo: "The Missile Silo stores interceptors that shoot down incoming missiles, and ballistic missiles that strike enemy defenses.",
  fortress: "The Orbital Fortress fights for this world when it is attacked. Build it on the worlds we cannot afford to lose.",
  fusion: "The Fusion Plant burns gas to make a lot of power. Use it when the Solar Array can't keep up, and watch your gas.",
  nanite: "The Nanite Assembly halves every build time on this world with each level. It is the biggest speed-up we have.",
  terraformer: "The Geo-Former opens new ground: five more building fields per level. Build it when a world runs out of room.",
  allyDepot: "The Coalition Depot fuels allied fleets and cuts the fuel of every flight. Its Fleets tab shows allies stationed here.",
  lunarBase: "The Lunar Outpost opens building room on this world's moon. Every level adds three moon fields.",
  phalanx: "The Phalanx Array scans the space around this moon and adds a radar level for every level we build.",
  flagDock: "The Flagship Dock is where our flagship is commissioned and equipped. Its Flagship tab holds its gear.",
  jumpGate: "The Warp Gate moves ships instantly between two gated worlds. It recharges after each jump.",
  fighter: "Light Fighters are cheap, fast and the backbone of an early fleet. Build them in numbers.",
  hauler: "Small Cargos carry plunder and supplies. Send them with your warships so a win brings the loot home.",
  heavyFighter: "Heavy Fighters carry real armour and shred Small Cargos. A strong step up from Light Fighters.",
  heavyCargo: "Large Cargos hold five Small Cargos' worth. Best for pirate raids and for moving resources between worlds.",
  recycler: "Recyclers collect debris fields at full efficiency. Send them wherever a big battle just ended.",
  lancer: "Pathfinders are fast long-range raiders with deep holds, deadly against Cruisers and fighters.",
  ark: "The Colony Ship settles a new world. Send it with warships against a Hive world we can beat, and that world becomes ours.",
  corvette: "Cruisers are our fastest warships and the counter to any fighter swarm.",
  battleship: "Battleships are heavy line ships: thick hulls, big guns, and deadly against Pathfinders.",
  bastion: "Dreadnoughts hunt fleets. They punish lines of Battleships, Cruisers and Heavy Fighters.",
  bomber: "Bombers break defenses. Send them at fortified worlds full of turrets.",
  destroyer: "Destroyers are escort killers, best against Dreadnoughts and Laser Turrets.",
  dreadnought: "The Reaper is the king of the fleet. It hunts capital ships: Battleships, Bombers and Destroyers.",
  worldbreaker: "The Cube Destroyer is the rarest weapon in the galaxy. Only a very large fleet stands a chance against one.",
  spyProbe: "Espionage Probes scout before every attack. Send more of them, or raise Espionage Technology, and the report shows more.",
  tender: "Mender Repair Ships patch up the fleet after every battle, and speed up the Repair Yard while parked at home.",
  guardian: "The Guardian Heavy Cruiser is a flying shield wall that draws enemy fire away from smaller ships.",
  escortCarrier: "The Halo Escort Carrier launches fighter wings and protects the fleet. Deadly against fighters.",
  supercarrier: "The Citadel Supercarrier is a mobile base: it commands fleets and launches squadrons.",
  eclipse: "The Discovery Class Destroyer is an alliance flagship. One per commander, and its command aura lifts the whole fleet." };
function holoFirst(kind, k) { if (!S || !HOLO[k] || (kind !== "b" && kind !== "s")) return; S.holoSeen = S.holoSeen || {}; if (S.holoSeen[k]) return;
  const st = tutOn() ? TUT[S.tut.i] : null, nm = (B[k] || SH[k] || {}).n; if (st && nm && (st.t.includes(nm) || st.say.includes(nm))) return; /* the step's own line covers it; it plays next time */
  if ($("#advh.on") || advLines || $("#adv")) return; S.holoSeen[k] = 1; dirty(); setTimeout(() => advHolo(HOLO[k]), 400); }
const tutAt = id =>''')
rep('''  detail: d => { if (d.kind === "b") SFX.tapB(d.k); openSheet({''', '''  detail: d => { if (d.kind === "b") SFX.tapB(d.k); holoFirst(d.kind, d.k); openSheet({''')
open(p, 'w', encoding='utf-8').write(t); print('ok')
