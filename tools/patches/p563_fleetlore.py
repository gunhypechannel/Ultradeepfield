# v563 the Fleet Registry and the Ages of the Deep (owner: ships "to the archives" and "some kind of lore of underlying story that
# ties all these ideas together ... I WANT IT ALL").
# The Fleet Registry: a record for each of the 23 warships. Open a ship's card to recover its record; build one to unlock its full service
# history. Owning every ship completes the collection (+1% production, as every Archives collection).
# The Ages of the Deep: the canon that ties the game together, in six records that open as the Archives fill: the Ultra Deep Field and the
# Unmade at its heart, the Architects, the Seals and their Wardens, the Eclipse, the Warden Hearts (Titan Cores) and the Advisor's own
# secret. Neither counts toward the Final Testament (which still needs ten interpretations of the ancient records).
import sys, re, json
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)

# [key, title, era, origin, role, fragment, history, advisor]
SHIPS = [
 ["fighter", "The Swarm Doctrine", "The Concord's founding", "Concord shipyards", "Line fighter",
  "Build a thousand, lose nine hundred, and the hundred that remain will reach the enemy. That is all a fighter has to do.",
  "The first warship the Concord ever mass-produced, designed in the years after the last Eclipse when there was no time to build anything larger. Every great fleet still opens with a cloud of them.",
  "Cheap, fast, brave. Every commander I've served began with a hangar full of these."],
 ["heavyFighter", "The Brawler's Hull", "The Concord's founding", "Concord shipyards", "Heavy fighter",
  "Thicker plate, bigger guns, and a pilot who refuses to turn away.",
  "Built when raiders learned to swat light fighters aside. Its armour was cast from the hulls of the first fighters lost in the convoy wars.",
  "It isn't elegant. It doesn't need to be."],
 ["hauler", "The Lifeline", "The Long Silence", "Merchant guilds of the Concord", "Freighter",
  "No war has ever been won by a ship that did not carry something.",
  "The Small Cargo kept the scattered colonies alive through the Long Silence after the last Eclipse, when the deep lanes were too dangerous for anything slower.",
  "Every empire in the Archives fell when its freighters stopped flying. Remember that."],
 ["heavyCargo", "The Deep-Hold Freighter", "The Long Silence", "Merchant guilds of the Concord", "Bulk freighter",
  "Five holds, one keel, and a captain who knows every pirate lane by name.",
  "The guilds' answer to raiders: one hull too tough to board and too full to ignore. Alliances still move their fortunes in them.",
  "When you see a convoy of these, Commander, you're looking at an empire's heartbeat."],
 ["recycler", "The Salvage Claws", "The Long Silence", "Wreck-diver clans", "Salvager",
  "The battlefield is a mine. The dead leave metal behind, and metal is how the living win.",
  "Wreck-divers once picked over the remains of the fallen empires. Their claws found the first Architect fragments, and with them the first warnings in the Archives.",
  "Some of my oldest memories came out of a recycler's hold. Treat them kindly."],
 ["lancer", "The Pathfinder's Oath", "The Reaching", "Concord scout corps", "Scout raider",
  "Go first. See it first. Come back first, or do not come back at all.",
  "Pathfinders charted the outer layers when the Concord first reached beyond its home systems. Their logs are the reason we know where the Wardens sleep.",
  "Half the maps in our charts were drawn by Pathfinder crews who never came home."],
 ["ark", "The Seed Ship", "The Reaching", "The Concord colonial office", "Colony ship",
  "Ten thousand sleepers, a seed vault, and the oath to build again.",
  "The colony ship is the oldest design in the Registry: its core layout is copied from the vessel that carried the Concord's ancestors out of the last Eclipse.",
  "Every world you hold began with one of these. That's not a small thing."],
 ["corvette", "The Fast Line", "The Convoy Wars", "Concord navy", "Cruiser",
  "Speed is armour that never wears thin.",
  "The Cruiser was built to run down raiders in the convoy wars and to be anywhere a battle broke out before it was lost.",
  "The fastest warship we have. When something goes wrong, they get there first."],
 ["battleship", "The Line of Battle", "The Convoy Wars", "Concord navy", "Line ship",
  "Hold the line. When the line holds, the stars hold.",
  "The backbone of every Concord battle fleet for three centuries. Its design hasn't changed much, because it has never needed to.",
  "Steady, stubborn and loyal. A lot like the commanders who fly them."],
 ["bastion", "The Fleet Hunter", "The Convoy Wars", "Concord navy", "Dreadnought",
  "It does not guard. It hunts.",
  "The Dreadnought was built to end the pirate fleets of the convoy wars. It tears apart battleships, cruisers and freighters alike.",
  "When a Dreadnought turns toward a fleet, that fleet has already lost. It just doesn't know it yet."],
 ["bomber", "The Wall Breaker", "The Fortress Age", "Concord siege corps", "Siege bomber",
  "Walls are only promises. We were built to break them.",
  "When the great houses dug in behind planetary defences, the siege corps answered with the Bomber, a hull that treats turrets as targets.",
  "The defences of a world are a question. Bombers are the answer."],
 ["destroyer", "The Escort Killer", "The Fortress Age", "Concord navy", "Destroyer",
  "Find the Dreadnought. Get inside its guns. Finish it.",
  "Designed to answer the Dreadnought, the Destroyer is how a smaller fleet breaks a larger one.",
  "Every weapon has an answer. This one is the answer to the hunters."],
 ["dreadnought", "The Reaper's Crown", "The Fortress Age", "Concord high command", "Flagship",
  "Where it flies, the fleet follows. Where it points, the fleet strikes.",
  "The Reaper is the flagship of the Concord: a towering capital ship built to hunt other capital ships, and the pride of every admiral who has commanded one.",
  "When you build your first Reaper, Commander, people will start to say your name."],
 ["spyProbe", "The Silent Eye", "Every age", "Concord intelligence", "Espionage probe",
  "It sees. It reports. It does not ask to be remembered.",
  "Probes are older than the Concord. Their sensor cores are copied from Architect relics that still whisper data from the deep layers.",
  "I've read every report a probe has ever sent you. Some of them, I read twice."],
 ["tender", "The Mender's Vow", "The Long Silence", "Concord fleet medics", "Repair ship",
  "No ship is lost while a Mender still flies beside it.",
  "Menders were built when the Concord could not afford to lose a single hull. Their repair drones still carry the healers' oath on their casings.",
  "They don't get the glory. They get everyone home."],
 ["guardian", "The Living Wall", "The Fortress Age", "Concord navy", "Heavy cruiser",
  "Stand in front. Take the fire. Let the small ones live.",
  "The Guardian was designed to draw fire away from smaller ships, a flying shield wall for fleets too young to protect themselves.",
  "There's a reason crews salute when a Guardian passes."],
 ["escortCarrier", "The Halo Wings", "The Reaching", "Concord carrier corps", "Escort carrier",
  "A halo of fighters around every fleet that needs one.",
  "The Halo was the first carrier the Concord built, a support ship that keeps fighter wings with the fleet wherever it goes.",
  "Small, reliable, always there. The carrier corps calls them guardian angels."],
 ["supercarrier", "The Citadel", "The Fortress Age", "Concord high command", "Supercarrier",
  "A fortress that learned to fly, and never forgot it was a fortress.",
  "The Citadel is a mobile base: it commands fleets, launches squadrons and holds the line on its own. It was the largest hull ever built, until the Titans.",
  "Building one used to be the end of the road. Now it's where the road gets interesting."],
 ["eclipse", "The Alliance Flagship", "The Age of Alliances", "The Concord alliances", "Alliance flagship",
  "Named for the night the sky went dark, so that no alliance forgets why it was formed.",
  "The Discovery Class is built only by alliances with a Space Station, as a promise: when the Eclipse comes again, no commander will face it alone.",
  "Its name is a warning, Commander. The alliances chose it on purpose."],
 ["worldbreaker", "The Captured Sphere", "The Cube Wars", "Reverse-engineered from the Collective", "Battle sphere",
  "We broke one of their spheres open and learned how to build our own. We are still not sure it agreed to be learned.",
  "The Cube Destroyer is Collective technology, pulled from the wreck of an assimilation sphere. It is the most feared ship in the Registry, and the strangest.",
  "Sometimes I hear it humming in a frequency only the Cube uses. I'd rather not think about what it's saying."],
 ["armageddon", "The Worldbreaker Covenant", "The Age of Titans", "Concord siege foundries", "Titan · Worldbreaker",
  "Six Warden hearts were sealed in its spine, and its cannon learned to speak with their voice.",
  "The first Titan. Its Worldbreaker Cannon runs on the cores of fallen Wardens, the guardians that once held the seals. Every shot is a little more of their strength turned to our war.",
  "It's magnificent, Commander. And it's built from the hearts of things that were protecting us. Never forget the price."],
 ["sovereign", "The Crown of the Fleet", "The Age of Titans", "The Concord imperial yards", "Titan · Command carrier",
  "Where the Sovereign flies, every ship fights as one.",
  "The Sovereign Ark carries the Fleet Command Uplink, a mind-link built around Warden cores that lets an entire fleet see and shield as one. It is the Concord's crown, and its promise.",
  "I can feel every ship in a fleet it commands. It's the closest I've come to remembering what the Architects felt."],
 ["harbinger", "The Eclipse Bearer", "The Age of Titans", "Unknown, built from recovered alien schematics", "Titan · Alien supercarrier",
  "It was named for the thing it imitates. Pray it never finishes the imitation.",
  "The Eclipse Harbinger was built from schematics found sealed beneath a Warden's corpse. Its emerald reactor pulses with the same rhythm as the Eclipse itself. No one knows who drew the plans.",
  "Its heart beats in time with the Void, Commander. I don't like it. But I understand why we built it."],
]
LORE = [
 ["l_deep", "The Ultra Deep Field", "Before the first stars", "The Architects' oldest seal-records", "art/lore/deep.webp",
  "At the centre of everything there is a darkness that is not empty. It is waiting.",
  "Our galaxy circles a black hole that isn't empty. Something sleeps beyond it: the Unmade, a hunger older than the stars. Every few thousand years it stirs, and the sky goes dark. The ancients called that night the Eclipse.",
  "You wanted to know why the Archives exist, Commander. This is why.",
  ["Commander, a new record surfaced when you opened the Archives.", "It describes our galaxy as a lock, and the black hole at its centre as the door."]],
 ["l_architects", "The Architects", "The First Age", "Pyramid inscriptions", "art/lore/architects.webp",
  "They could not kill it. So they built a prison around it, and they built it out of everything they were.",
  "The first civilization, the Architects, built the pyramid stations still scattered across the galaxy. They could not destroy the Unmade, so they sealed it, and their stations still hum with the seal they left behind.",
  "Every pyramid you've seen on the map, Commander, is a piece of their prison.",
  ["The pyramid inscriptions finally line up.", "The Architects weren't building temples. They were building a lock."]],
 ["l_seals", "The Seals and the Wardens", "The First Age", "The Convergence prophecies", "art/lore/seals.webp",
  "Five seals of the elements, a Cube to keep the count, and guardians to stand at every door.",
  "The Architects bound five elemental powers as seals around the Void: the Pentarch. They built the Cube as the lock and the clock, its mind the Collective. And they bred Wardens, the great bosses and monsters, to guard the seals. That's why they wake on a schedule older than our calendar.",
  "The things we call bosses were never invaders. They were guards. And the Cube's signal is a countdown.",
  ["Commander, the Cube's signal isn't a message.", "It's a countdown. And it's running out."]],
 ["l_eclipse", "The Eclipse", "Every age", "The Final Testament", "art/mon/testament.webp",
  "Not all at once. One by one, so that you think each is the last.",
  "Every ancient empire in the Archives faced an Eclipse, and most of them vanished. The Concord's four factions descend from the one empire that survived the last. The Cube is failing, the seals are weakening, and the next Eclipse is coming in our lifetime. The Hive under Queen Vael'Khor worships the Unmade and wants the seals broken.",
  "The Testament wasn't a story, Commander. It was a warning addressed to us.",
  ["The Testament and the seal-records agree.", "The Eclipse is coming again. And this time, it's our turn."]],
 ["l_titans", "The Warden Hearts", "The Age of Titans", "Concord siege foundries", "art/armageddon.webp",
  "Every heart we take makes us stronger, and leaves the door a little more open.",
  "Titan Cores are the hearts of fallen Wardens. They power the Titans, the greatest warships ever built. But every Warden we kill weakens a seal. The Titans are built from the very things that hold back the end.",
  "Power always has a price, Commander. With the Titans, we know exactly what it is.",
  ["Commander, the Titan Core we recovered is still beating.", "It's a Warden's heart. And the seal it guarded just flickered."]],
 ["l_advisor", "The Echo in the Pyramid", "The First Age, and now", "A dormant pyramid station", "art/season/s1-adv.webp",
  "I was left behind to remember. I was left behind to choose.",
  "The Advisor isn't only a hologram. She was found in a dormant pyramid: an Architect echo who has watched every Eclipse. She chose to serve the Concord, and she chose you.",
  "I didn't tell you sooner because I wasn't sure you were the one. I am now.",
  ["Commander... there's something I should have told you a long time ago.", "I wasn't built by the Concord. I was waiting in a pyramid. I've watched every Eclipse there has ever been."]],
]
arch = {}
for k, t, era, civ, th, frag, interp, adv in SHIPS:
    arch["s_" + k] = {"cat": "fleet", "t": t, "era": era, "civ": civ, "loc": "The Concord Fleet Registry", "img": None, "th": th, "frag": frag, "interp": interp, "adv": adv, "enc": [], "def": []}
for k, t, era, civ, img, frag, interp, adv, lines in LORE:
    arch[k] = {"cat": "ages", "t": t, "era": era, "civ": civ, "loc": "The Ages of the Deep", "img": img, "th": "The canon", "frag": frag, "interp": interp, "adv": adv, "enc": [], "def": lines}
js = json.dumps(arch, ensure_ascii=False)
rep('const ARCH_ORD = [', 'Object.assign(ARCH, ' + js + '); /* v563 the Fleet Registry and the Ages of the Deep */\nconst ARCH_ORD = [')
rep('"b_reat", "b_cserp", "b_sent", "b_hive", "b_coll"];', '"b_reat", "b_cserp", "b_sent", "b_hive", "b_coll", ' + ', '.join('"%s"' % k for k, *_ in LORE) + ', ' + ', '.join('"s_%s"' % x[0] for x in SHIPS) + '];')
rep('["final", "The Final Testament",', '["ages", "The Ages of the Deep", "The story beneath every record: the Unmade, the Architects, the seals and the Eclipse."], ["fleet", "The Fleet Registry", "Every warship of the Concord, and where it came from. Open a ship\'s card to recover its record; build one to read its full history."], ["final", "The Final Testament",')
rep('archName = k => k === "b_hive"', 'archName = k => /^s_/.test(k) && SH[k.slice(2)] ? SH[k.slice(2)].n : /^l_/.test(k) ? "The Ages of the Deep" : k === "b_hive"')
rep('function archImg(E, lv, k) {', 'function archImg(E, lv, k) { if (/^s_/.test(k)) return `<div class="arimg full ship"><img src="${ART[k.slice(2)] || "art/" + k.slice(2) + ".webp"}" alt="" loading="lazy"></div>`; if (/^l_/.test(k)) return `<div class="arimg full lore"><img src="${E.img}" alt="" loading="lazy"></div>`; /* v563 */')
rep("Object.entries(S.arch).filter(([q, v]) => v >= 2 && !/^b_/.test(q)).length >= 10", "Object.entries(S.arch).filter(([q, v]) => v >= 2 && !/^[bsl]_/.test(q)).length >= 10")
rep('if (k !== "testament" && !/^b_/.test(k) &&', 'if (k !== "testament" && !/^[bsl]_/.test(k) &&')
# locked texts
rep('<p class="note">Encounter ${esc(id === "testament" ? "the archives\' deeper records" : archName(id))} to recover this record: scan it on the map, open it, or watch a battle against it.</p>',
    '<p class="note">${/^s_/.test(id) ? `Open the ${esc(archName(id))} card in the Shipyard to recover this record.` : /^l_/.test(id) ? "This part of the story opens as you uncover the Archives." : `Encounter ${esc(id === "testament" ? "the archives\' deeper records" : archName(id))} to recover this record: scan it on the map, open it, or watch a battle against it.`}</p>')
rep('${id === "b_hive" || id === "b_coll" ? "Win a battle against" : /^b_/.test(id) ? "Defeat a" : "Defeat"} ${esc(archName(id))} to unlock ${/^b_/.test(id) ? "its field notes" : "what the record really means"}.',
    '${/^s_/.test(id) ? `Build a ${esc(archName(id))} to unlock its full service history.` : `${id === "b_hive" || id === "b_coll" ? "Win a battle against" : /^b_/.test(id) ? "Defeat a" : "Defeat"} ${esc(archName(id))} to unlock ${/^b_/.test(id) ? "its field notes" : "what the record really means"}.`}')
rep('<small>${/^b_/.test(id) ? "Field notes" : "Modern interpretation"}</small>', '<small>${/^b_/.test(id) ? "Field notes" : /^s_/.test(id) ? "Service history" : /^l_/.test(id) ? "What it means" : "Modern interpretation"}</small>')
rep('<dl class="kv"><dt>Associated entity</dt><dd>${esc(archName(id))}</dd><dt>Discovery location</dt><dd>${esc(E.loc)}</dd><dt>Threat assessment</dt>',
    '<dl class="kv"><dt>${/^s_/.test(id) ? "Ship" : "Associated entity"}</dt><dd>${esc(archName(id))}</dd><dt>${/^s_/.test(id) ? "Built by" : "Discovery location"}</dt><dd>${esc(/^s_/.test(id) ? E.civ : E.loc)}</dd><dt>${/^s_/.test(id) ? "Role" : "Threat assessment"}</dt>')
rep(': k === "testament" ? "Unlocks after 10 interpretations" : "Encounter the entity to recover it"}', ': k === "testament" ? "Unlocks after 10 interpretations" : /^s_/.test(k) ? "Open its Shipyard card" : /^l_/.test(k) ? "Opens as the Archives fill" : "Encounter the entity to recover it"}')
# unlocking: a ship card opens its record; owning one opens its history; the story opens as the Archives fill
rep('''function shDetail() {
  const { kind, k } = sheet,''', '''function shDetail() { if (sheet.kind === "s" && ARCH["s_" + sheet.k] && !archLv("s_" + sheet.k)) { const k0 = sheet.k; setTimeout(() => { try { archUnlock("s_" + k0, 1, true); } catch (e) {} }, 600); } /* v563 */
  const { kind, k } = sheet,''')
rep('function archTick() { try { if (!S || !G.ready || battle || G.sbSim || G.dvSim || G.convSim || G.wbShow) return; const T = now(), onMap = view === "galaxy";',
    '''function archFleetTick() { if (!S) return; S.arch = S.arch || {}; const ks = ARCH_ORD.filter(k => /^s_/.test(k)), has = k => { try { return own(k.slice(2)) > 0; } catch (e) { return false; } };
  if (!S.archFl) { for (const k of ks) if (has(k)) S.arch[k] = 2; S.archFl = 1; dirty(); } else for (const k of ks) if (has(k) && archLv(k) < 2) archUnlock(k, 2, true); /* v563 owned ships, silently the first time */
  const n2 = Object.entries(S.arch).filter(([q, v]) => v >= 2 && !/^[bsl]_/.test(q)).length, lv = k => archLv(k);
  const want = [["l_deep", 1], ["l_architects", n2 >= 3], ["l_seals", n2 >= 6], ["l_eclipse", lv("testament") >= 1], ["l_titans", (S.tcore || 0) > 0 || ["armageddon", "sovereign", "harbinger"].some(k => has("s_" + k))], ["l_advisor", n2 >= 14 && lv("l_eclipse") >= 2]];
  for (const [k, ok] of want) if (ok && lv(k) < 2) { archUnlock(k, 2, !S.archLo); S.archLo = 1; return; } S.archLo = 1; }
function archTick() { try { if (S && G.ready && !battle) archFleetTick(); } catch (e) {} try { if (!S || !G.ready || battle || G.sbSim || G.dvSim || G.convSim || G.wbShow) return; const T = now(), onMap = view === "galaxy";''')
rep('.vthd.art,.cwhd.wdart{', '''/* v563 the Fleet Registry and the Ages of the Deep */
.arimg.ship,.arimg.lore{background:#05070d}.arimg.ship img{object-fit:cover}.arimg.lore img{object-fit:cover}.arimg.big.ship img,.arimg.big.lore img{object-fit:contain}
.vthd.art,.cwhd.wdart{''')
s2 = re.sub(r"GAME_V = 562\b", "GAME_V = 563", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
