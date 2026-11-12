/* v502 THE ANCIENT ARCHIVES — echoes of Empire Origins (owner's brief "The Ancient Archives"). Every legendary entity in the galaxy
   matches a record the ancient empires left behind. A first encounter (scanning it, opening it, watching it in a battle report, or
   being on the map while it is live) recovers its fragment and the Advisor plays the discovery once; its fall (or a report where it
   is destroyed) recovers the modern interpretation and her defeat lines. Ten interpretations open the Final Testament. Text only
   where no voice clip exists yet. Proposed lore: nothing here overrides Empire Origins canon until the owner approves it. */
const ARCH_CAT = [["warn", "The First Warnings", "Ancient civilizations describing entities among the stars."], ["pan", "The Forbidden Pantheon", "Beings the ancients mistook for gods."], ["anom", "The Great Anomalies", "Accounts of impossible things in the sky."], ["exp", "The Lost Expeditions", "Later civilizations who went looking, and what they found."], ["conv", "The Convergence Prophecies", "Five powers bound together by a ring of ancient seals."], ["cube", "The Cube Codex", "Geometric objects and a mind made of many."], ["final", "The Final Testament", "What the ancient empires knew, and kept for us."]];
const ARCH = {
  war: { cat: "warn", t: "The Keeper of the Unseen Gate", era: "The First Empires", civ: "River-kingdom star priests", loc: "The deep layers of the galaxy", img: "warden-skin", th: "Severe",
    frag: "…it stands where the stars end, and does not sleep. Its rings turn though no wind moves them. The priests say it holds the door shut. They do not say from which side…",
    interp: "Not a monster but a sentinel: a mass held in shape by its own field, stationed at a gravitational boundary. The 'door' in the record lines up with the region it never leaves.",
    adv: "The archives describe it as a guardian. Every battle we've fought with it, it never came after us. It held its ground.",
    enc: ["Commander, we're detecting a gravitational anomaly. But something is maintaining its shape.", "Ancient imperial records described a guardian standing between the stars and the darkness beyond them.", "No... this is impossible. The orbital structures match the drawings exactly."],
    def: ["The Warden has fallen. But the archives describe it as a sentinel, not an invader.", "Commander... what was it protecting us from?"] },
  ovl: { cat: "pan", t: "The Walking Temple", era: "The First Empires", civ: "The pyramid builders (Imhotep's era)", loc: "The Void, ringed by its conduits", img: "overlord-skin", th: "Catastrophic",
    frag: "…and the mountain of stone rose from the sand and walked, and the sky above it burned white. We built ours to remember its shape, so the gods would know we had seen…",
    interp: "Its geometry matches the oldest monuments to within a fraction of a degree. The records suggest the monuments were copies, not the other way round.",
    adv: "We always assumed the pyramids came first. What if they were sketches of something that had already stood there?",
    enc: ["We've found a massive artificial structure. Its geometry is remarkably similar to ancient imperial monuments.", "The earliest records describe a pyramid that rose from the earth and walked beneath a burning sky.", "Commander... its legs are moving. The accounts were literal."],
    def: ["The structure is dormant. Its architecture predates everything in our database.", "Perhaps the ancient empires weren't its builders. Perhaps they were trying to imitate it."] },
  dev: { cat: "anom", t: "The Serpent That Swallowed the Moon", era: "The Classical Age", civ: "Coastal sky-watchers", loc: "The outer orbits", img: "devourer-skin", th: "Extreme",
    frag: "…on the third night the moon was gone, and in its place a ring of arms that closed like a hand. The fishermen would not sail for a generation…",
    interp: "A lunar disappearance recorded by three separate cultures in the same decade. The 'ring of arms' matches the Devourer's reach exactly.",
    adv: "The archives called it the Devourer. I always assumed that was a metaphor. I'm not assuming anything any more.",
    enc: ["Commander, a massive object has emerged from deep space. Initial scans suggest biological and mechanical structures of impossible scale.", "Ancient records speak of a creature whose limbs encircled entire celestial bodies.", "Those aren't orbital structures... they're appendages."],
    def: ["The entity is no longer moving.", "The archives called it the Devourer. I always assumed that was a metaphor."] },
  brd: { cat: "anom", t: "The Plague Beneath the Stars", era: "The Medieval Age", civ: "Chroniclers of the fallen kingdoms", loc: "The hive nebulae", img: "matriarch-skin", th: "Severe",
    frag: "…a black queen under a green sky, and from her came the swarm, and the swarm did not stop at the walls. The chronicle ends here. The next page is burned…",
    interp: "The green sky is consistent with her bioluminescent egg fields seen from a planet's surface. Several kingdoms recorded the same queen, decades apart.",
    adv: "Several ancient accounts describe her as one of many. That is the part of the record I like least.",
    enc: ["We've located an enormous biological structure surrounded by smaller moving signatures.", "Empire Origins records describe a black queen that brought entire kingdoms to ruin beneath a green sky.", "Those objects surrounding her... they're eggs. Commander, they're hatching."],
    def: ["The Matriarch is silent.", "Yet several ancient accounts describe her as one of many. We need to investigate that possibility."] },
  tyr: { cat: "exp", t: "The Iron Reaver", era: "The Early Space Age", civ: "The first spacefaring empires", loc: "The trade corridors", img: "tyrant-skin", th: "Severe",
    frag: "…it came after the colonies fell silent: a ship made of ships, wearing the hulls of everyone it had taken. Our convoy is the last. If you are reading this, change course…",
    interp: "A cargo log from a lost colonial convoy. Hull fragments on the Tyrant carry registry marks that match vessels the log lists as missing.",
    adv: "One of these ship fragments carries an insignia that should not exist in this era. Someone out there remembers the convoys.",
    enc: ["An enormous unidentified warship has entered the trade corridor.", "Historical accounts describe a raider that appeared after the fall of several early spacefaring empires.", "The hull is made of hundreds of separate ships. Commander, some of those designs are older than our recorded civilization."],
    def: ["The stolen cargo has been recovered.", "But one of these ship fragments carries an insignia that should not exist in this era."] },
  wym: { cat: "warn", t: "The Serpent That Encircled the Sun", era: "The Classical Age", civ: "Hypatia's star catalogues", loc: "The black hole's accretion ring", img: "wyrm-skin", th: "Extreme",
    frag: "…a serpent of broken rings, feeding on the light of dying stars. It does not die. It returns. Mark its return in the tables, so the ones after us are ready…",
    interp: "An astronomical tablet that predicts gravitational disturbances on a fixed cycle. The cycle matches the Wyrm's appearances to the week.",
    adv: "The archive does not describe its death. It describes its return. Someone counted the years for us.",
    enc: ["We are detecting movement within the black hole's accretion region.", "An ancient astronomical tablet describes a serpent made of broken rings, feeding on the light of dying stars.", "Commander... the black hole isn't producing the creature. The creature is moving through it."],
    def: ["The Wyrm has disappeared into the singularity.", "Commander, the archive does not describe its death. It describes its return."] },
  col: { cat: "warn", t: "The Mountain That Remembered", era: "The Bronze Age", civ: "Crystal-mine guilds", loc: "The Void Shard fields", img: "colossus-skin", th: "Severe",
    frag: "…we dug too deep, and the mountain woke, and its heart was purple fire. It spoke to us without a mouth. It remembered things none of us had told it…",
    interp: "Its central crystal is not random mineral growth: its internal structure resembles an artificial memory lattice. The miners may have heard it reading back their own thoughts.",
    adv: "Its central crystal resembles an artificial memory lattice. If it remembered the miners... what else does it remember?",
    enc: ["We've detected movement beneath the Void Shard mining site.", "Ancient miners described living mountains filled with purple fire.", "The crystal formations are assembling themselves. Commander, the entire deposit is alive."],
    def: ["The central crystal has stopped pulsing.", "But its internal structure resembles an artificial memory lattice."] },
  est: { cat: "conv", t: "The Storm Tablets", era: "The First Empires", civ: "Temple scribes of the five powers", loc: "The Convergence ring", img: "el-storm-skin", th: "Extreme",
    frag: "…thunder that moved without clouds, and walked the sky on legs of light. First of the Five. Bound by the seal of the crescent…",
    interp: "Electromagnetic signatures recorded on the tablets match Voltaris's discharge pattern. The 'seal of the crescent' is one of the five runes on the Convergence ring.",
    adv: "The ancient records called it a god. Our scanners are calling it an impossible energy structure. I'm not sure those are different answers.",
    enc: ["Commander, the electromagnetic signatures match the Storm Tablets of the First Empires.", "Those tablets described thunder that moved without clouds.", "The ancient records called it a god. Our scanners are calling it an impossible energy structure."],
    def: ["Voltaris is down. The storm readings are fading.", "The Storm Tablets end with one line: the first seal holds the others."] },
  efi: { cat: "conv", t: "The Burning Crown", era: "The Bronze Age", civ: "Sun-kingdom court astronomers", loc: "The Convergence ring", img: "el-fire-skin", th: "Extreme",
    frag: "…a crown of fire in the sky, and under it the kingdom burned. Second of the Five. Bound by the seal of the horn…",
    interp: "Court artwork of the burning crown matches Ignaroth's silhouette almost exactly, horns included.",
    adv: "The court painters got the horns right. They must have been looking straight at it.",
    enc: ["The temperature is rising across the entire region.", "Ancient civilizations described a burning celestial crown appearing before the destruction of entire kingdoms.", "Commander... the artwork matches the object before us almost perfectly."],
    def: ["Ignaroth's fire is out.", "The court astronomers drew it for a reason. I think they wanted us to recognize it."] },
  eli: { cat: "conv", t: "The Golden Guardian", era: "The Classical Age", civ: "The sacred cities", loc: "The Convergence ring", img: "el-light-skin", th: "Extreme",
    frag: "…a golden guardian above the sacred city, and the people sang to it every night, and every night it answered with light. Third of the Five. Bound by the seal of the ring…",
    interp: "Auricor emits a highly organized pattern of light. The songs may not have been worship: they may have been an attempt to answer it.",
    adv: "Those cities may not have been worshipping it. They may have been trying to communicate.",
    enc: ["The structure is emitting a highly organized pattern of light.", "Ancient records describe a golden guardian suspended above sacred cities.", "Those cities may not have been worshipping it. They may have been trying to communicate."],
    def: ["Auricor's light has gone dark.", "If it was speaking to them... I wish I knew what it said."] },
  eic: { cat: "conv", t: "The Darkness That Swallowed the Stars", era: "The Medieval Age", civ: "Monastery chroniclers", loc: "The Convergence ring", img: "el-ice-skin", th: "Extreme",
    frag: "…a purple darkness opened in the sky and the stars went into it, one by one, and did not come out. Fourth of the Five. Bound by the seal of the orb…",
    interp: "Gravemorn bends space until normal measurements fail. From the ground, nearby stars would have appeared to vanish.",
    adv: "I had classified that record as mythology. I am revising that assessment.",
    enc: ["Commander, we're detecting a region where normal spatial measurements are becoming unreliable.", "One ancient chronicle described a purple darkness that swallowed the stars.", "I had classified that record as mythology. I am revising that assessment."],
    def: ["Gravemorn has collapsed in on itself.", "The stars it swallowed are still there. They were simply bent out of view."] },
  ena: { cat: "conv", t: "The Living Emerald", era: "The Age of Discovery", civ: "Expedition cartographers", loc: "The Convergence ring", img: "el-nature-skin", th: "Extreme",
    frag: "…where the green star passed, the forest grew over our ships in a night. Fifth of the Five. Bound by the seal of the thorn…",
    interp: "Green celestial symbols appear at several ancient imperial sites. Viridrax's energy pattern matches them, and so does the overgrowth it leaves behind.",
    adv: "The ancient texts describe a living emerald presence that changed the world around it. The readings suggest that presence was here.",
    enc: ["The energy pattern resembles the green celestial symbols found throughout several ancient imperial sites.", "The ancient texts describe a living emerald presence that changed the world around it.", "Commander... the readings suggest that presence is here."],
    def: ["Viridrax is withering.", "The cartographers marked every place it touched. We have their maps now."] },
  epx: { cat: "conv", t: "The Five Seals of Creation", era: "The oldest surviving imperial archive", civ: "Unknown: older than every empire we know", loc: "Above the Void", img: "el-light-skin", th: "Catastrophic",
    frag: "…five powers bound together by a ring of seals. We drew the seals on every temple so that no one would forget them. If the seals fail, the Five become One…",
    interp: "We believed the symbols represented the five elements. They weren't symbols of worship. They were containment instructions.",
    adv: "Not a prophecy. A warning. Someone built that ring, and someone wanted us to know how to keep it closed.",
    enc: ["Commander, five separate energy signatures are beginning to synchronize.", "I've found something... a fragment from the oldest surviving imperial archive. It describes five celestial powers bound together by a ring of ancient seals.", "The runes... Commander, look at the runes. They're identical. They weren't symbols of worship. They were containment instructions."],
    def: ["The Convergence has collapsed. The surviving runes contain a message.", "Not a prophecy. A warning."] },
  aex: { cat: "exp", t: "The Sleeping War Machine", era: "The Industrial Age", civ: "A lost imperial observatory", loc: "Deep space, every fifth Wednesday", img: "aexion-warform", th: "Ultimate",
    frag: "…a ship that was not a ship. When it woke it stood up, and it carried a blade, and our telescope could not hold all of it in the glass…",
    interp: "The observatory's illustration matches Aexion's dreadnought hull. The record describes a weapon that could become a warrior. That was considered allegorical.",
    adv: "Its internal design suggests it was built to fight something much larger. I'd like to know what.",
    enc: ["Commander, the unidentified vessel matches an illustration recovered from a lost imperial observatory.", "The archive describes a weapon that could become a warrior. That description was considered allegorical.", "It wasn't a warship. It was a weapon wearing the shape of one."],
    def: ["Aexion's reactor is failing.", "But its internal design suggests it was built to fight something much larger."] },
  vae: { cat: "pan", t: "The Dragon Behind the Sun", era: "The First Empires", civ: "Temple carvers", loc: "Near the celestial anomaly", img: "vaelthar", th: "Ultimate",
    frag: "…a dragon of the sky carrying a golden wheel upon its back. When the wheel turned, armies became light. We carved it so our children would hide when they saw it…",
    interp: "The carvings show the wheel's stabilizer spokes in the right number and position. The 'breath' that erased armies matches the Divine Annihilation beam.",
    adv: "Ancient civilizations claimed this creature could erase armies with a single breath. I no longer consider that an exaggeration.",
    enc: ["A massive biological entity has appeared near the anomaly.", "Ancient carvings describe a celestial dragon carrying a golden wheel upon its back.", "Commander... the wheel is real."],
    def: ["The energy has faded. I'm analyzing the damage.", "Ancient civilizations claimed this creature could erase armies with a single breath. I no longer consider that an exaggeration."] },
  khz: { cat: "pan", t: "The Guardian of the Last Gate", era: "The First Empires", civ: "Desert-kingdom scribes", loc: "Around an ancient monument in the dark", img: "khezaroth", th: "Ultimate",
    frag: "…a lion that was a temple, and between its claws it held a piece of the night. It guards the last gate. Do not wake it. Do not look for the gate…",
    interp: "The 'piece of the night' is a contained singularity. The record names it a gate, and nothing we have found yet tells us where it leads.",
    adv: "The archives say it guarded a gateway. We've beaten the guardian. We still haven't found the gate.",
    enc: ["Commander, there's something ahead. A gravitational signature surrounding what looks like an enormous ancient monument.", "An imperial manuscript describes a lion-shaped guardian that held a piece of darkness between its claws.", "Commander, those are not carvings. That's a living entity."],
    def: ["The Sphinx has fallen silent. The archives say it guarded a gateway.", "Commander... where is the gate?"] },
  med: { cat: "pan", t: "The Face Beyond the Heavens", era: "The Classical Age", civ: "Island oracles", loc: "A petrified world", img: "medusara", th: "Ultimate",
    frag: "…a face among the stars, crowned with serpents, and where her eyes fell the soldiers stood still forever. The oracle wept and would not say more…",
    interp: "Her gaze is a focused energy discharge that leaves matter crystalline and inert. The armies 'turned to stone' were the technological equivalent.",
    adv: "I don't know whether we defeated her, or whether she simply closed her eyes.",
    enc: ["Commander, long-range scans are detecting an unusual geological formation on the planet.", "The ancient records describe a face among the stars, surrounded by serpents.", "Those aren't mountain ranges. They're serpents."],
    def: ["The planetary entity has become dormant.", "I don't know whether we defeated her, or whether she simply closed her eyes."] },
  cube: { cat: "cube", t: "The Many-Minded Stone", era: "The Age of Discovery", civ: "Navigators' guild", loc: "The heart of the galaxy", img: null, th: "Catastrophic",
    frag: "…a stone of perfect angles hung in the sky, and it spoke with a thousand voices that were one voice. It took our ships, and then it took our sailors, and then it took their names…",
    interp: "Accounts of a geometric object and a collective intelligence, centuries apart. The Collective's Cube fits every one of them, including the part about the names.",
    adv: "A thousand voices that were one voice. The navigators had no word for a collective. We do. It isn't any more comforting.",
    enc: ["Commander, the navigators' guild left records of a stone of perfect angles that spoke with a thousand voices.", "It's the Cube. They saw the Cube."],
    def: ["The Cube still stands, Commander. The navigators never said it could be destroyed.", "Only held."] },
  testament: { cat: "final", t: "The Final Testament", era: "Every age", civ: "All of them", loc: "Hidden across every archive", img: null, th: "Unknown",
    frag: "…they will come back. Not all at once. One by one, so that you think each is the last. We have left you the shapes, the names and the seals. Learn them. We could not finish what we began…",
    interp: "The same symbols appear in unrelated civilizations, and the same warnings survive across thousands of years. The ancient empires were not only afraid of these entities. They were preparing for their return.",
    adv: "We called them gods because we had no other word for what we saw. Our ancestors weren't telling stories, Commander. They were leaving instructions.",
    enc: ["Commander, the archive fragments are cross-referencing on their own.", "Every civilization. Every age. The same shapes, and the same warning.", "We called them gods because we had no other word for what we saw."], def: [] } };
const ARCH_ORD = ["war", "wym", "col", "ovl", "vae", "khz", "med", "dev", "brd", "tyr", "aex", "est", "efi", "eli", "eic", "ena", "epx", "cube", "testament"];
/* her lines one after another: each stays up until its voice clip ends, or long enough to read when it has none */
function archSeq(L) { let i = 0; const step = () => { if (i >= L.length) return; const l = L[i++], t0 = Date.now(), minT = Math.max(3200, l.length * 62); try { advHolo(l, 1); } catch (e) {}
    const wait = () => { const a = VOICE.au, busy = a && !a.paused && !a.ended; if (busy || Date.now() - t0 < (busy ? 0 : minT)) setTimeout(wait, 300); else setTimeout(step, 350); }; setTimeout(wait, 600); }; step(); }
const archName = k => k === "cube" ? "The Cube" : k === "testament" ? "The Final Testament" : SBW[k] ? `${SBW[k].n}, ${SBW[k].t.replace(/^The /, "the ")}` : WB[k] ? WB[k].n : k;
const archLv = k => ((S && S.arch) || {})[k] | 0;
const archUnread = () => { const A = (S && S.arch) || {}, R = (S && S.archR) || {}; return Object.keys(A).filter(k => (A[k] | 0) > (R[k] | 0)).length; };
function archUnlock(k, lv, quiet) { if (!S || !ARCH[k]) return; S.arch = S.arch || {}; const was = S.arch[k] | 0; if (lv <= was) return; if (lv === 2 && was < 1) archUnlock(k, 1, true); S.arch[k] = lv; dirty();
  const E = ARCH[k]; crumb("archive " + k + " " + lv);
  if (!quiet) archSeq(lv === 1 ? E.enc : E.def);
  try { toast(`📜 Archive ${lv === 1 ? "fragment recovered" : "interpretation unlocked"}: ${E.t}`, "win"); } catch (e) {}
  if (k !== "testament" && Object.values(S.arch).filter(v => v >= 2).length >= 10 && !S.arch.testament) setTimeout(() => archUnlock("testament", 2), 9000);
  try { if (typeof trayRender === "function") trayRender(); if (sheet && sheet.type === "archives") renderSheet(); } catch (e) {} }
const archKeyOf = k => !k ? null : String(k)[0] === "c" && /^c\d$/.test(k) ? "ovl" : ARCH[k] ? k : null;
function archFromRep(r) { try { if (!r) return; const k = archKeyOf(r.sbk || r.wb || (r.omega ? "cube" : null)); if (!k) return; archUnlock(k, 1); const sg = r.sbSeg || r.omSeg || r.wbSeg;
    if (!r.test && sg && sg[1] === 0 && r.winner === "a") setTimeout(() => archUnlock(k, 2), 4000); } catch (e) {} }
function archTick() { try { if (!S || !G.ready || battle) return; const T = now(), onMap = view === "galaxy";
    if (onMap) { for (const k of Object.keys(WB)) { const a = archKeyOf(k); if (a && !archLv(a) && wbOn(k, T) && !G.wbShow && !G.convSim) { archUnlock(a, 1); return; } }
      const sk = sbLiveKey(T); if (sk && ARCH[sk] && !archLv(sk)) { archUnlock(sk, 1); return; } }
    const st = wbState(T); for (const k of Object.keys(st.dead || {})) { const a = archKeyOf(k); if (a && archLv(a) === 1 && st.dead[k] > 0 && !G.convSim) { archUnlock(a, 2); return; } }
    for (const k of Object.keys(SBW)) if (ARCH[k] && archLv(k) === 1) { const s0 = sbStartOf(k, T), sst = sbState(k, s0); if (sst && sst.dead && sst.dead > s0) { archUnlock(k, 2); return; } }
    if (archLv("cube") === 1) { const nx = nexusNow(T); if (nx.garrison && nx.garrison[G.me]) archUnlock("cube", 2); } } catch (e) {} }
setInterval(archTick, 15000);
function archSheetSeen(s) { try { if (!s) return; if (s.type === "wboss" && s.id) archUnlock(archKeyOf(s.id), 1); else if (s.type === "sboss" && s.id) archUnlock(s.id, 1); else if (s.type === "nexus" || (s.type === "events" && s.ev === "cube")) archUnlock("cube", 1); } catch (e) {} }
function archImg(E, lv) { if (!E.img) return `<div class="arimg glyph">${E.cat === "cube" ? "◼" : "✦"}</div>`; return `<div class="arimg${lv >= 2 ? " full" : ""}"><img src="art/boss/${E.img}.webp" alt="" loading="lazy"></div>`; }
function shArch() { const id = sheet.id; S.archR = S.archR || {};
  if (id && ARCH[id]) { const E = ARCH[id], lv = archLv(id); if (lv) { S.archR[id] = Math.max(S.archR[id] | 0, lv); dirty(); setTimeout(() => { try { trayRender(); } catch (e) {} }, 0); }
    const cat = ARCH_CAT.find(c => c[0] === E.cat);
    return `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter" style="color:#e2c48a">${esc(cat[1])}</div><h2>${lv ? esc(E.t) : "Sealed record"}</h2><p class="note">${lv ? `${esc(E.era)} · ${esc(E.civ)}` : "Not yet recovered"}</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
      ${lv ? archImg(E, lv) : `<div class="arimg glyph lock">🔒</div>`}
      ${lv ? `<div class="arfrag"><small>Fragment of the original record</small><p>${esc(E.frag)}</p></div>` : `<p class="note">Encounter ${esc(id === "testament" ? "the archives' deeper records" : archName(id))} to recover this record: scan it on the map, open it, or watch a battle against it.</p>`}
      ${lv >= 2 ? `<div class="arint"><small>Modern interpretation</small><p>${esc(E.interp)}</p></div><div class="aradv"><img src="${ADV_ART}" alt=""><p><b>${ADV}</b>${esc(E.adv)}</p></div>` : lv ? `<div class="arint lock"><small>Modern interpretation · sealed</small><p>${id === "testament" ? "" : `Defeat ${esc(archName(id))} to unlock what the record really means.`}</p></div>` : ""}
      ${lv ? `<dl class="kv"><dt>Associated entity</dt><dd>${esc(archName(id))}</dd><dt>Discovery location</dt><dd>${esc(E.loc)}</dd><dt>Threat assessment</dt><dd class="arth">${esc(E.th)}</dd></dl>${lv >= 2 && (E.enc.length || E.def.length) ? `<button class="btn ghost wide" data-act="archPlay" data-id="${id}">🔊 Hear the Advisor's account</button>` : ""}` : ""}`; }
  const n2 = ARCH_ORD.filter(k => archLv(k) >= 2).length, n1 = ARCH_ORD.filter(k => archLv(k)).length;
  const card = k => { const E = ARCH[k], lv = archLv(k), nu = lv > (S.archR[k] | 0); return `<button class="arcard lv${lv}" data-act="archEntry" data-id="${k}">${lv ? archImg(E, lv) : `<div class="arimg glyph lock">?</div>`}<span><b>${lv ? esc(E.t) : k === "testament" ? "A sealed testament" : "Unrecovered record"}</b><small>${lv ? esc(archName(k)) : k === "testament" ? "Unlocks after 10 interpretations" : "Encounter the entity to recover it"}</small><em>${lv >= 2 ? "Interpreted" : lv ? "Fragment" : "Sealed"}</em></span>${nu ? `<i class="arnew">NEW</i>` : ""}</button>`; };
  return `<div class="hd archd"><div style="flex:1;min-width:0"><div class="chapter" style="color:#e2c48a">Echoes of Empire Origins</div><h2>The Ancient Archives</h2><p class="note">The oldest empires left records of things they saw in the sky. We called them myths. ${n1} of ${ARCH_ORD.length} records recovered · ${n2} interpreted.</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
    ${ARCH_CAT.map(([c, nm, d]) => { const ks = ARCH_ORD.filter(k => ARCH[k].cat === c); return `<h2 class="sec arsec">${esc(nm)}</h2><p class="note">${esc(d)}</p><div class="argrid">${ks.map(card).join("")}</div>`; }).join("")}`; }
