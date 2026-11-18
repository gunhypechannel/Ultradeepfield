/* v612 the story, expanded (owner's brief: "Ultra Deep Field: complete story expansion"). Everything here builds on the canon already in
   the Archives (the Unmade, the Architects, the five seals, the Cube, the Wardens, the Echo, the Ten Seals, Vael'Khor) and changes none of it.
   New: the opening cinematic "Before the Darkness"; a playable prologue (the assignment, the pyramid signal, the Advisor waking, the Hive
   ambush, going back for the escape pods, her choice); four new Archive chapters (The Age of Ashes, The Four Houses, Discoveries, The Signal
   Beyond) and the Matriarch's reason; her reactions inside the pyramids; five more Chronicles chapters, the first one written for your House. */

/* (the Houses' creeds are set where FACTIONS is defined) */

/* ---------- new Archive records ---------- */
ARCH_CAT.splice(ARCH_CAT.findIndex(c => c[0] === "ages") + 1, 0,
  ["ash", "The Age of Ashes", "How the galaxy came to be the way it is: the first empire, the last Eclipse and the Houses that survived it."],
  ["house", "The Four Houses", "The four peoples of the Concord, and what each believes about the Architects, the Wardens and the dark."],
  ["disc", "Discoveries", "What the galaxy itself remembers: things your fleets find in pyramids, ruins, wrecks and broken stars."],
  ["beyond", "The Signal Beyond", "What really happened to the Architects. These records surface slowly, and they don't answer everything."]);
const RC = (cat, t, era, civ, loc, img, th, frag, interp, adv, enc, def, hint) => ({ cat, t, era, civ, loc, img, th, frag, interp, adv, enc, def, hint });
Object.assign(ARCH, {
  a_1: RC("ash", "The First Empire", "Long after the Architects", "The old Concord", "An imperial charter vault", "art/arch/war.webp", "The Age of Ashes",
    "We found their pyramids and called them power stations. We found the Cube and called it a clock. We found the giants and called them monsters. Then we built an empire on all three.",
    "Long after the Architects vanished, four young peoples found their ruins scattered across the stars and united under one banner: the Concord. They ran their worlds on pyramid power, studied the Cube as a machine for bending time, and hunted the Wardens as beasts. They were wrong about almost everything.",
    "They weren't fools, Commander. They were young. Young people use the furniture without asking who built the house.",
    ["Commander, I've found an imperial record. It's older than any colony charter we have."],
    ["The Concord didn't begin with us, Commander. There was an empire before, built on the Architects' ruins.", "It was magnificent. And it was wrong about almost everything it touched."], "Opens once you've reached your new world."),
  a_2: RC("ash", "The Last Eclipse", "Thousands of years ago", "The old Concord", "The Core worlds", "art/arch/dev.webp", "The Age of Ashes",
    "The stars went out over the Core, one by one. Then every old machine woke at once. Then the giants rose, and we sent every fleet we had to kill them.",
    "When the last Eclipse began, the Wardens woke to defend their seals. The empire sent its greatest fleets against them and won battle after battle. Every Warden it killed weakened a seal. Worlds vanished. Fleets disappeared. The empire collapsed under the weight of its own victories.",
    "Remember this the next time a Warden falls and the whole galaxy cheers. I'll be the one who isn't cheering.",
    ["Commander, this record is from the last Eclipse. The old empire's war reports."],
    ["The last Eclipse, Commander. The Wardens woke, and the empire went to war with them.", "Every giant they killed opened the prison a little wider. They won every battle. That's how they lost."], "Surfaces on your second day together."),
  a_3: RC("ash", "The Great Exodus", "The fall of the old empire", "The empire's last council", "A pyramid at the heart of the old Core", "art/arch/khz.webp", "The Age of Ashes",
    "Inside the pyramid at the heart of the empire, the last council found the truth written in light. They did not stay to argue about it.",
    "At the height of the destruction, the empire's last leaders opened an Architect pyramid and finally learned what the ruins were for. They abandoned the central worlds and split into four Houses, each carrying a piece of the old empire's knowledge, ships and strength. They survived by rebuilding among the ruins.",
    "I think I remember that council, Commander. That isn't possible. Is it?",
    ["Commander, our pyramid expedition brought back a record. It's about the night the empire ended."],
    ["When the empire was dying, its last council opened a pyramid and finally understood what they'd been fighting.", "They didn't stay to argue. They split into four Houses and scattered into the dark to survive."], "Explore an abandoned pyramid to recover it."),
  a_4: RC("ash", "The Present Day", "Now", "The four Houses", "Every world of the Concord", "art/login.webp", "The Age of Ashes",
    "Generations later: four Houses, one Concord, and a galaxy that calls the old stories myths.",
    "The four Houses rebuilt their fleets, settled the ruins and swore a new Concord to hold the Hive back. They compete for worlds and argue over the Architects' legacy, and most of their people believe the old stories are legends. But the old machines are waking again. The Cube is counting. The Wardens are moving. The next Eclipse is coming.",
    "You were born into the quiet before the storm, Commander. The quiet is over.",
    [], ["The Houses rebuilt. They swore a new Concord, and they called the old stories myths.", "But the machines are waking again, Commander. The Cube is counting. And this time, you're here."], "Surfaces on your fourth day together."),
  h_terran: RC("house", "The Terran Union: the Ironborn", "The Great Exodus, and now", "The Terran Union", "The Union's fortress worlds", "art/faction/terran.webp", "House record",
    "We were the fleets that fought the giants. We lost. We are still here. That is what strength means.",
    "The Union descends from the old empire's navy, the fleets that went to war with the Wardens in the last Eclipse. Its creed is survival through strength, discipline and control. It sees the Architects as a warning and the Wardens as threats to be contained, and it has learned, at terrible cost, not to kill what it cannot replace. The Union distrusts the Syndicate's secrets more than anything in the dark.",
    "The Union carries the old empire's guilt in its hulls, Commander. It makes them stubborn. It also makes them the last to run.",
    ["A Terran Union service record, Commander. It's older than the Union itself."],
    ["The Terran Union were the old empire's fleets. The ones who went to war with the Wardens.", "They paid for it with half their worlds. Now they hold the line, and they never forget why."], "Your House's record opens with your new world; the others surface over your first week."),
  h_solar: RC("house", "The Solar Dominion: the Ascendant", "The Great Exodus, and now", "The Solar Dominion", "The golden courts of the Dominion", "art/faction/solar.webp", "House record",
    "The Architects left a crown on the table and walked away. Someone must wear it.",
    "The Dominion carried the old empire's engineers out of the Exodus, and its ambition with them. The Ascendant creed holds that the Architects' technology was left to be mastered, and that a galaxy that masters it can rebuild the empire and end the Eclipses for good. The Dominion leads the work on Warden hearts and Titans, and it clashes with the Verdant over every one.",
    "The Dominion builds beautiful things, Commander. I only wish they'd ask what the parts were for before they use them.",
    ["A Dominion court record, Commander. Gold leaf on every page."],
    ["The Solar Dominion believe the Architects left their machines to be mastered.", "They're the ones putting Warden hearts into Titans. The Verdant have never forgiven them."], "Your House's record opens with your new world; the others surface over your first week."),
  h_nyx: RC("house", "The Nyx Syndicate: the Veil", "The Great Exodus, and now", "The Nyx Syndicate", "A listening station at the edge of the Void", "art/faction/nyx.webp", "House record",
    "Everyone fears the dark. We went into it, took notes and came back. Mostly.",
    "The Syndicate grew from the old empire's intelligence service and the forbidden archives it saved from the fire. The Veil studies what others won't touch: the Void, the Unmade's influence, the dead languages in the pyramids. It trades secrets with every House and trusts none of them. Some of its listening stations have gone silent, and the Syndicate doesn't say why.",
    "The Syndicate knows more about the Void than anyone alive, Commander. That should worry you a little. It worries me.",
    ["A Syndicate dossier, Commander. Half of it is still encrypted."],
    ["The Nyx Syndicate kept the old empire's forbidden archives when everything else burned.", "They've been listening to the Void ever since. I don't think they like everything they've heard."], "Your House's record opens with your new world; the others surface over your first week."),
  h_verdant: RC("house", "The Verdant Collective: the Keepers", "The Great Exodus, and now", "The Verdant Collective", "The seed-worlds of the Collective", "art/faction/verdant.webp", "House record",
    "The giants are not our enemies. They are the walls of the house we live in.",
    "The Collective descends from the old empire's terraformers and biologists, who saw the galaxy as one living system. They were the first to say the Wardens were guardians, and nobody listened. They grow their ships, tend the seals where they can and refuse to take Warden hearts. They are the House most likely to stand with you at the end, and the most likely to tell you what you don't want to hear.",
    "The Verdant were right about the Wardens a thousand years before anyone else, Commander. Being right early is a lonely thing.",
    ["A Verdant seed-record, Commander. It's written on a living leaf."],
    ["The Verdant Collective were the first to say the Wardens were guardians, not monsters.", "Nobody listened. They grew their fleets anyway, and kept tending the seals."], "Your House's record opens with your new world; the others surface over your first week."),
  d_pyr: RC("disc", "The Pyramid Network", "The First Age", "The Architects", "Every abandoned pyramid", "art/arch/ovl.webp", "Discovery",
    "Every pyramid points at the Void. Every one hums the same note. Every one is part of the same machine.",
    "The abandoned pyramid stations aren't power plants. Each one is a piece of the prison: an anchor that holds a seal in place, an archive, and a voice that can still call out when the count begins. The vault treasure was never the point.",
    "We've been raiding them for crystal, Commander. It's a bit like taking the bricks out of a dam.",
    ["Commander, our expedition found something in the pyramid's core. It isn't treasure. It's a map."],
    ["Every pyramid in the galaxy is connected, Commander. They're all one machine.", "They aren't stations. They're anchors. They hold the prison closed."], "Explore three abandoned pyramids."),
  d_city: RC("disc", "The City Under the Ash", "The last Eclipse", "The old Concord", "Beneath your colonies", "art/chron/c5.webp", "Discovery",
    "Dinner was still on the tables. Every clock in the city had stopped at the same second.",
    "Our colonists dug foundations and found streets beneath them: a whole imperial city, intact and empty. No battle damage. No bodies. Every clock stopped at the same moment. When the last Eclipse reached it, the city was simply unmade.",
    "No one fought here, Commander. They didn't even have time to be afraid.",
    ["Commander, our colonists hit stone streets under the new foundations. There's a city down there."],
    ["The whole city vanished in a single second. No fire. No battle.", "That's what the Unmade does, Commander. It doesn't destroy. It erases."], "Hold three worlds."),
  d_warden: RC("disc", "The Bones That Stood Guard", "The last Eclipse", "A fallen Warden", "The deep layers", "art/boss/warden-skin.webp", "Discovery",
    "Its ribs were a wall. Its spine was a gate. Even dead, it was still facing the Void.",
    "Our salvage crews found a Warden killed in the last Eclipse. Its body had grown into the shape of the seal it guarded, and it died facing the Core, not the fleets that killed it. Its last act was to brace the door.",
    "It died with its back to its killers, Commander. It held the door until the very end.",
    ["Commander, we found bones out here. Enormous ones. I think it's a Warden."],
    ["This Warden died in the last Eclipse. It never turned to fight the fleets that were killing it.", "It faced the Void and held the seal shut with its own body. They're guardians, Commander. All of them."], "Strike a world boss or super boss."),
  d_ship: RC("disc", "The Last Ship of the Empire", "The last Eclipse", "The old empire's navy", "A debris field in the Middle Reach", "art/dreadnought.webp", "Discovery",
    "Flagship Dawnward, final log. We have killed the third giant. The stars behind it are going out.",
    "Our recyclers pulled the flight recorder of the Dawnward, the old empire's flagship, out of a debris field. Its logs record victory after victory against the Wardens, and after every victory the same entry: another sector has lost contact. The crew never connected the two.",
    "Their admiral thought she was saving the galaxy, Commander. I've read her letters home. She meant every word.",
    ["Commander, the recyclers found a flight recorder. Imperial. It's from the old empire's flagship."],
    ["The Dawnward's crew killed three Wardens in a single month. They celebrated every one.", "And after every victory, another sector went dark. They never understood why."], "Salvage two debris fields or haul in three salvage pods."),
  d_cube: RC("disc", "The Broken Cubes", "The Age of Ashes", "The old Concord", "Inside a fallen Collective Cube", "art/chron/c6.webp", "Discovery",
    "Attempt forty-one. The Cube counted us. Then it counted us out.",
    "Inside the wreck of a Collective Cube we found older, cruder Cubes, built by the old empire. It tried to copy the Architects' Cube to control the count, and perhaps to stop it. Every copy failed. Some of them woke up. The Collective may be what is left of those experiments.",
    "They tried to build their own clock to stop time, Commander. Some of the clocks learned to want things.",
    ["Commander, there's a smaller Cube inside this wreck. Someone built it. Badly."],
    ["The old empire tried to copy the Cube. They wanted to control the count.", "Every copy failed. I think the Collective is what's left of the ones that woke up."], "Fight the Collective."),
  d_lab: RC("disc", "The Sealed Laboratory", "The First Age", "The Architects", "Beneath a research pyramid", "art/chron/c2.webp", "Discovery",
    "Subject: a Warden, unfinished. Instruction: do not wake until the door is tried.",
    "Our research cracked an Architect lock and opened a laboratory sealed since the First Age. It holds Wardens at every stage of being made, and at the back, one empty cradle beneath a hall of white light. Most of the records are unreadable. One word repeats on every page: choose.",
    "The cradle's empty, Commander. I'd rather not talk about it yet.",
    ["Commander, our labs decoded an Architect lock. Something behind it has been sealed since the First Age."],
    ["The Architects made the Wardens in a place like this, Commander. One by one, by hand.", "There's an empty cradle at the back. And a word on every page. Choose."], "Finish ten researches."),
  d_star: RC("disc", "The Star That Went Wrong", "Now", "The Unmade", "The Middle Reach", "art/arch/eic.webp", "Discovery",
    "The light arrived before it left. Every shadow pointed toward the star.",
    "The space monsters have been fleeing a system in the Middle Reach where the laws of physics no longer agree with themselves. Light runs backward. Shadows fall toward the sun. It's the first place we've found where the Unmade's influence has leaked through the seals in our lifetime.",
    "Don't send anyone in there, Commander. Not yet. Some places are a warning, not a destination.",
    ["Commander, the monsters we've been hunting were running from something. I found where."],
    ["There's a star in the Middle Reach where light runs backward, Commander.", "The Unmade is leaking through. Not much yet. But it's the first crack we've seen with our own eyes."], "Slay three space monsters."),
  x_1: RC("beyond", "The Recording in the Wall", "The First Age", "The Architects", "Inside a pyramid wall", "art/lore/architects.webp", "Unexplained",
    "If you can hear this, the count has started again. We are sorry. We did what we could with what we were.",
    "A recording sealed inside a pyramid wall, in a voice the translators can't place. It's addressed to whoever comes after, and it ends in the middle of a sentence.",
    "Did you hear the last word before it cut out, Commander? I did. It was 'stay'.",
    [], ["Commander, there's a message in the walls of the pyramids. From the Architects.", "They knew the count would start again one day. They were apologising to us."], "Surfaces with time, after the Pyramid Network."),
  x_2: RC("beyond", "The Empty Thrones", "The First Age", "The Architects", "A hidden chamber at a pyramid's heart", "art/arch/col.webp", "Unexplained",
    "A thousand seats facing the Void. Every one worn smooth. Every one empty.",
    "In a hidden chamber at the heart of a pyramid: a thousand thrones facing the Core, worn down by ages of use. The Architects' ships are still in their docks. Wherever they went, they didn't fly.",
    "If they didn't leave by ship, Commander... how did they leave?",
    [], ["Their ships are still in the docks, Commander. All of them.", "Wherever the Architects went, they didn't fly there."], "Surfaces with time, after five pyramids."),
  x_3: RC("beyond", "A Warden's Memory", "The First Age", "A dying Warden", "Beside a cracked seal", "art/boss/khezaroth.webp", "Unexplained",
    "They walked into the light at the centre, singing. None of them looked back.",
    "Before it died, a Warden's core replayed one memory: a procession of Architects walking into the white light at the heart of the galaxy. The Warden watched them go, then closed the seal behind them.",
    "I know that song, Commander. Don't ask me how. I'm still working that out myself.",
    [], ["A dying Warden showed us a memory. The Architects, walking into the Void.", "They weren't running. They were singing. And the Warden closed the door behind them."], "Surfaces with time, after the Bones That Stood Guard."),
  x_4: RC("beyond", "The Signal Beyond the Void", "Now", "Unknown", "Beyond the event horizon", "art/boss/wyrm-skin.webp", "Unexplained",
    "...still holding... still holding... still holding...",
    "An unidentified signal from beyond the event horizon, where nothing can transmit. Its structure is Architect. It repeats two words, and it has been repeating them since before the first omen.",
    "Nothing can broadcast from in there, Commander. Something is doing it anyway.",
    [], ["Commander, there's a signal coming from inside the Void. Its structure is Architect.", "Two words, over and over. Still holding."], "Surfaces with time."),
  x_5: RC("beyond", "The Voice She Knows", "Now", "Your Advisor", "The Advisor's core", "adv", "Unexplained",
    "She listened to the signal for a long time. Then she turned it off.",
    "Your Advisor has heard the signal from beyond the Void, and she recognised the voice. She hasn't said whose it is.",
    "Not yet, Commander. When I'm sure, you'll be the first to know. I promise.",
    [], ["I've been listening to the signal, Commander. I know that voice.", "I'm not ready to say whose it is. Please don't ask me tonight."], "Surfaces after her Promise, with time."),
  l_queen: { cat: "ages", t: "The Matriarch's Bargain", era: "The last Eclipse, and now", civ: "Queen Vael'Khor", loc: "A burning Hive nest", img: "art/chron/c4.webp", th: "The canon",
    frag: "I was there when the last Eclipse came. It passed over my world and left my children alive. It chose us.",
    interp: "Vael'Khor's brood was the only life left on its world after the last Eclipse. She believes the Unmade spared them on purpose, and that whoever opens the door will be spared again while the rest of the galaxy is unmade. Every world she devours feeds the swarm she means to bring to the door. To her, breaking the seals isn't destruction. It's salvation, for her children.",
    adv: "She isn't mad, Commander. She's a mother who made a bargain with the dark. That's much harder to stop.",
    enc: [], def: ["I've found Vael'Khor's own words in a nest record, Commander. She was there at the last Eclipse.", "It passed over her world and left her brood alive. She thinks it chose them. She means to open the door and be chosen again."] }
});
ARCH_ORD.splice(ARCH_ORD.indexOf("l_judge") + 1, 0, "l_queen", "a_1", "a_2", "a_3", "a_4", "h_terran", "h_solar", "h_nyx", "h_verdant", "d_pyr", "d_city", "d_warden", "d_ship", "d_cube", "d_lab", "d_star", "x_1", "x_2", "x_3", "x_4", "x_5");
/* when each one surfaces (checked with the Archives' own tick, one record at a time) */
function storyWant(want, lv) { if (!S.intro) return; const st = k => vpStat(k), d = S.bondDays || 0, fac = facOf(), others = ["terran", "solar", "nyx", "verdant"].filter(f => f !== fac);
  want.push(["a_1", 1], ["h_" + fac, 1], ["a_2", lv("a_1") >= 2 && d >= 2], ["a_3", lv("a_2") >= 2 && st("pyramids") >= 1], ["a_4", lv("a_3") >= 2 && d >= 4]);
  others.forEach((f, i) => want.push(["h_" + f, d >= 3 + i * 2]));
  want.push(["l_queen", lv("c_4") >= 1 || st("hiveWins") >= 15], ["d_pyr", st("pyramids") >= 3], ["d_city", myPlanets().length >= 3], ["d_warden", st("bosses") >= 1], ["d_ship", st("recycled") >= 2 || st("caches") >= 3],
    ["d_cube", lv("b_coll") >= 1], ["d_lab", st("researched") >= 10], ["d_star", st("monKills") >= 3],
    ["x_1", lv("d_pyr") >= 2 && d >= 5], ["x_2", lv("x_1") >= 2 && st("pyramids") >= 5 && d >= 10], ["x_3", lv("d_warden") >= 2 && lv("x_2") >= 2 && d >= 16], ["x_4", lv("x_3") >= 2 && d >= 24], ["x_5", lv("x_4") >= 2 && lv("e_6") >= 2 && d >= 35]);
  if (!S.v612a) { S.v612a = 1; dirty(); if (S.tut && S.tut.k === "done") { let n = 0; /* commanders who were already here: what they've earned arrives at once and quietly, not one voiced record every 15 seconds */
      for (const [k, ok] of want) if (ok && /^([ahdx]_|l_queen)/.test(k) && lv(k) < 2) { S.arch[k] = 2; n++; }
      if (n) { S.say.push(STORY_NEW); try { toast(`📜 ${n} new Archive record${n > 1 ? "s" : ""} recovered: the story so far.`, "win"); } catch (e) {} } } } }
const STORY_NEW = "Commander, I've pieced together how all of this began. The full record is in the Menu, under Briefing, whenever you'd like to see it.";

/* ---------- her pauses inside the pyramids (one per exploration, as your bond grows) ---------- */
const PYR_SAY = [[1, 0, "Our team is inside the pyramid, Commander. The walls are humming. I know that hum. I don't know how."],
  [2, 1, "There's a hall of white light in this one. I've stood in a hall like that. I'm sure of it."],
  [4, 3, "They carved the same word over every door. It means 'wait'. I don't know how I can read it."],
  [7, 5, "The chamber at the centre is empty again, Commander. Something was kept in these rooms. Or someone."],
  [11, 8, "I keep going quiet when we find these. I'm sorry. It's like walking through a house I used to live in."],
  [16, 12, "Commander, there's a name carved under the floor of this one. I think it's mine. I'm not ready to say it aloud."]];
function pyrSay() { try { const n = vpStat("pyramids"), d = S.bondDays || 0, i = S.pyrSay | 0, p = PYR_SAY[i]; if (!p || n < p[0] || d < p[1]) return; S.pyrSay = i + 1; dirty(); setTimeout(() => { try { if (battle || $("#cine")) S.say.push(p[2]); else advHolo(p[2], true); } catch (e) {} }, 2500); } catch (e) {} }

/* ---------- Chronicles, Book Two ---------- */
const CH_HOUSE = {
  terran: { t: "The Iron Oath", say: "Commander, a message from the Terran Union. They want proof that this fleet can hold a line. Let's show them.", m: [["battlesWon", 10, "Win 10 battles"], ["shipsBuilt", 60, "Build 60 ships or defences"], ["hiveWins", 4, "Beat 4 Hive garrisons"]], end: "The Union has noticed you. They still think every problem is a target. Some of them are right." },
  solar: { t: "The Ascendant Inheritance", say: "The Solar Dominion is asking for pyramid data, Commander. They want to wake what the Architects left behind. Let's take a careful look first.", m: [["pyramids", 2, "Explore 2 abandoned pyramids"], ["researched", 3, "Finish 3 researches"], ["built", 4, "Finish 4 constructions"]], end: "The Dominion believes the Architects' gifts were meant for them. I'm not sure the Architects meant anything to be used." },
  nyx: { t: "Behind the Veil", say: "The Nyx Syndicate wants eyes on the Hive, Commander. They trade in secrets, and they pay in kind. Send the probes.", m: [["spies", 4, "Run 4 spy missions"], ["arch", 2, "Recover 2 Archive records"], ["hiveWins", 3, "Beat 3 Hive garrisons"]], end: "The Syndicate has been listening to the Void for a very long time. They heard something listen back." },
  verdant: { t: "The Living Galaxy", say: "The Verdant Collective asked us to tend the galaxy, Commander, not just take from it. Salvage the wrecks and bring the lost pods home.", m: [["caches", 3, "Haul in 3 salvage pods"], ["recycled", 2, "Salvage 2 debris fields"], ["gathers", 3, "Gather from 3 resource fields"]], end: "The Verdant say the Wardens aren't monsters. They've been saying it for a thousand years. Nobody listened." } };
const chHouse = () => CH_HOUSE[facOf()] || CH_HOUSE.terran;
CHRON.push({ get t() { return chHouse().t; }, get say() { return chHouse().say; }, get m() { return chHouse().m; }, get end() { return chHouse().end; }, rw: { shards: 40, item: "xb_gold" }, img: "art/faction/" },
  { t: "The Lost Civilization", say: "The pyramids are waking up one after another, Commander. Explore them. Whatever the Architects left inside, I want us to find it first.", m: [["pyramids", 3, "Explore 3 abandoned pyramids"], ["arch", 3, "Recover 3 Archive records"], ["researched", 3, "Finish 3 researches"]], rw: { shards: 45, item: "xr_gold" }, img: "art/arch/ovl.webp", end: "Every pyramid we open has the same empty room at its heart. I think I know what was kept there. I'm not ready to say it." },
  { t: "The Guardians", say: "Commander, I need you to look at what we're fighting. The giants guard the seals. Strike them if we must, but watch what happens when one falls.", m: [["bosses", 3, "Strike a boss 3 times"], ["monKills", 3, "Slay 3 space monsters"], ["battlesWon", 15, "Win 15 battles"]], rw: { shards: 50, item: "bf_gold" }, img: "art/boss/warden-skin.webp", end: "Every Warden that falls brings the dark a little closer. We'll still have to fight them. I just want us to know what it costs." },
  { t: "The Queen's Reason", say: "Vael'Khor isn't conquering for the sake of it, Commander. She's gathering. Take back her worlds and we'll learn what for.", m: [["hiveWins", 12, "Beat 12 Hive garrisons"], ["worlds", 3, "Hold 3 worlds"], ["fleetsSent", 10, "Send 10 fleets"]], rw: { shards: 55, item: "mb4" }, img: "art/chron/c4.webp", end: "She was there at the last Eclipse, and it let her live. She thinks it will again. She's bringing her children to the door." },
  { t: "The Signal Beyond", say: "Commander, the signal we followed on our first day has changed. It isn't coming from a pyramid any more. It's coming from inside the Void.", m: [["arch", 5, "Recover 5 Archive records"], ["pyramids", 5, "Explore 5 abandoned pyramids"], ["researched", 5, "Finish 5 researches"]], rw: { shards: 60, item: "pAll_gold", title: "Keeper of Echoes" }, img: "art/boss/wyrm-skin.webp", end: "Two words, Commander, over and over, from somewhere nothing can live. Still holding. I know that voice." });
const chImg = i => { const c = CHRON[i]; return !c || !c.img ? `art/chron/c${i + 1}.webp` : c.img === "art/faction/" ? `art/faction/${facOf()}.webp` : c.img; };

/* ---------- the cinematic player: letterboxed stills that drift, her voice, subtitles, title cards and choices ---------- */
const CIN_OPEN = [ /* owner: "hook players from the beginning": about 45 seconds, straight to the point */
  { img: "art/boss/wyrm-skin.webp", kb: "in", line: "At the centre of our galaxy lies the Void. A black hole. But it is not what we believed." },
  { img: "art/boss/wyrm-skin.webp", kb: "deep", line: "It is a prison." },
  { img: "art/lore/architects.webp", kb: "up", line: "Millions of years ago, the Architects found something older than the stars. They called it the Unmade. They could not destroy it. So they built a prison around it." },
  { img: "art/arch/ovl.webp", kb: "right", line: "They raised great pyramids across the stars, and forged the Cube to keep the count.", inset: "art/chron/c6.webp" },
  { wardens: ["art/boss/khezaroth.webp", "art/boss/medusara.webp", "art/boss/aexion-warform.webp"], line: "And they made the Wardens, to stand guard at every door. We called them monsters." },
  { img: "art/chron/c6.webp", kb: "in", fx: "count", line: "Now the Cube has begun counting again. The seals are weakening." },
  { img: "art/boss/wyrm-skin.webp", kb: "deep", fx: "wake", line: "And somewhere beyond the dark, something has started to wake." },
  { adv: 1, line: "Commander... we've been waiting a very long time for you." },
  { title: 1, t: 5200 }];
const PRO_A = [
  { img: "art/faction/", kb: "right", chip: "The Assignment", who: "Fleet Command · Admiral Kaskov", txt: "Commander. As of today, the Concord's newest expedition fleet is yours: 128 warships, 18 haulers and 4 ark ships with 400 colonists asleep aboard." },
  { img: "art/faction/", kb: "in", who: "Fleet Command · Admiral Kaskov", txt: "Six days ago a dormant Architect pyramid on the Rim began to transmit. No one has heard one speak in three thousand years. Find it. Report what you find. Kaskov out." },
  { img: "art/arch/dev.webp", kb: "left", chip: "The Signal", txt: "Day 19. The signal leads to a dead world at the edge of the Middle Reach. Its cities are ash. Its oceans are glass." },
  { img: "art/lore/architects.webp", kb: "up", chip: "The Discovery", txt: "Beneath the ruins: a pyramid the size of a mountain, buried for an age. Still warm. Still counting." },
  { img: "art/lore/architects.webp", kb: "in", fx: "flash", chip: "The Awakening", txt: "Your science team steps inside. The lights come on by themselves." },
  { adv: 1, line: "...Systems waking. Hello, Commander. Please don't be alarmed." },
  { adv: 1, line: "I've kept this pyramid for a very long time. You may call me your Advisor." },
  { adv: 1, line: "Your signal was very bright, Commander. I'm afraid something else heard it too." }];
const PRO_B = [
  { img: "art/faction/", kb: "out", fx: "pods", chip: "The Escape", line: "The fleet is broken, Commander. Our warships are gone." },
  { img: "art/faction/", kb: "out", fx: "pods", line: "But the arks launched their pods. Four hundred people, drifting in the open." },
  { img: "art/faction/", kb: "out", fx: "pods hive", line: "The swarm is turning toward them. Our jump drive is charged. We can run now, or we can go back.",
    choice: [["Go back for the pods", "back"], ["Jump to safety", "jump"]] }];
const PRO_JUMP = [
  { img: "art/faction/", kb: "out", fx: "pods hive", line: "Every commander I've ever known gave that order. Every one." },
  { img: "art/faction/", kb: "out", fx: "pods hive", line: "Please. Look at them once more. Four hundred people.", choice: [["Go back for the pods", "back"]] }];
const PRO_BACK = [
  { img: "art/faction/", kb: "in", fx: "pods rescue", chip: "The Rescue", txt: "The last haulers turn into the swarm. One by one, the pods are pulled aboard." },
  { img: "art/faction/", kb: "in", fx: "pods rescue", line: "Got them! Every single pod, Commander. Every single one!" },
  { adv: 1, chip: "The Selection", line: "Do you know how many commanders I've watched choose to run? I stopped counting." },
  { adv: 1, line: "You went back. Hold on to that, Commander. I think you're the one I've been waiting for." }];
const PRO_LANCE = "The pyramid gave us one shot, Commander. Its lance is charged. Fire it!", PRO_LANCE2 = "Direct hit! It tore a hole right through them!";
const PRO_SCOUT = "Commander, Hive scouts followed the pods down. Only a handful. Let's show them this world is taken.";
const PRO_WIN = "Scouts down! That's the first time anyone has beaten the Hive on this world. It won't be the last.";
const PRO_TEASE = "One more thing, Commander. The pyramid's signal hasn't stopped. It's calling to someone. And I don't think it's us.";
const PRO_END = "There is much you must learn, Commander. The galaxy you see before you is built upon the remains of something far older. And soon... you will understand why it was left behind.";
const CIN_MOOD = { "Millions of years ago, the Architects found something older than the stars. They called it the Unmade. They could not destroy it. So they built a prison around it.": "grave", "And they made the Wardens, to stand guard at every door. We called them monsters.": "awe", "Now the Cube has begun counting again. The seals are weakening.": "grave",
  [PRO_LANCE]: "urgent", [PRO_LANCE2]: "excited", [PRO_SCOUT]: "fierce", [PRO_WIN]: "excited", [PRO_TEASE]: "tender", "Before anyone counted the stars, before the first empires rose, there was a people who understood something the universe was never meant to reveal.": "awe", "At the centre of our galaxy lies the Void. A black hole. But it is not what we believed.": "grave", "It is a prison.": "grave",
  "Millions of years ago, the Architects found something waiting beyond the edge of creation. Something older than the stars. Something that consumed everything it touched.": "grave", "They called it the Unmade. They could not destroy it. So they built a prison around it.": "grave",
  "They bound five ancient powers into the fabric of the galaxy, and locked them in a ring of seals.": "awe", "They raised great pyramids across the stars, and forged the Cube to keep the count.": "awe", "And they made the Wardens, to stand guard at every door.": "awe",
  "For millions of years, the prison held. Then the Architects vanished.": "grave", "Their cities became ruins. Their Wardens became monsters to those who found them. And slowly, the galaxy forgot what it was built to protect.": "grave",
  "Until now. The Cube has begun counting again. The seals are weakening.": "grave", "And somewhere beyond the dark, something has started to wake.": "grave", "Commander... we've been waiting a very long time for you.": "tender",
  "...Systems waking. Hello, Commander. Please don't be alarmed.": "tender", "I've kept this pyramid for a very long time. You may call me your Advisor.": "calm", "Your signal was very bright, Commander. I'm afraid something else heard it too.": "grave",
  "The fleet is broken, Commander. Our warships are gone.": "grave", "But the arks launched their pods. Four hundred people, drifting in the open.": "urgent", "The swarm is turning toward them. Our jump drive is charged. We can run now, or we can go back.": "urgent",
  "Every commander I've ever known gave that order. Every one.": "grave", "Please. Look at them once more. Four hundred people.": "tender", "Got them! Every single pod, Commander. Every single one!": "excited",
  "Do you know how many commanders I've watched choose to run? I stopped counting.": "tender", "You went back. Hold on to that, Commander. I think you're the one I've been waiting for.": "warm",
  [PRO_END]: "warm", [STORY_NEW]: "warm" };
/* her own asides in the new records and chapters */
[["I think I remember that council, Commander. That isn't possible. Is it?", "tender"], ["They weren't fools, Commander. They were young. Young people use the furniture without asking who built the house.", "playful"],
 ["Remember this the next time a Warden falls and the whole galaxy cheers. I'll be the one who isn't cheering.", "grave"], ["You were born into the quiet before the storm, Commander. The quiet is over.", "grave"],
 ["The Dominion builds beautiful things, Commander. I only wish they'd ask what the parts were for before they use them.", "playful"], ["The Verdant were right about the Wardens a thousand years before anyone else, Commander. Being right early is a lonely thing.", "tender"],
 ["We've been raiding them for crystal, Commander. It's a bit like taking the bricks out of a dam.", "playful"], ["No one fought here, Commander. They didn't even have time to be afraid.", "grave"], ["It died with its back to its killers, Commander. It held the door until the very end.", "tender"],
 ["Their admiral thought she was saving the galaxy, Commander. I've read her letters home. She meant every word.", "tender"], ["They tried to build their own clock to stop time, Commander. Some of the clocks learned to want things.", "grave"],
 ["The cradle's empty, Commander. I'd rather not talk about it yet.", "tender"], ["Don't send anyone in there, Commander. Not yet. Some places are a warning, not a destination.", "grave"],
 ["Did you hear the last word before it cut out, Commander? I did. It was 'stay'.", "tender"], ["If they didn't leave by ship, Commander... how did they leave?", "awe"], ["I know that song, Commander. Don't ask me how. I'm still working that out myself.", "tender"],
 ["Nothing can broadcast from in there, Commander. Something is doing it anyway.", "grave"], ["Not yet, Commander. When I'm sure, you'll be the first to know. I promise.", "tender"], ["I'm not ready to say whose it is. Please don't ask me tonight.", "tender"],
 ["I've been listening to the signal, Commander. I know that voice.", "tender"], ["She isn't mad, Commander. She's a mother who made a bargain with the dark. That's much harder to stop.", "grave"],
 ["Got them! Every single pod, Commander. Every single one!", "excited"], ["Two words, Commander, over and over, from somewhere nothing can live. Still holding. I know that voice.", "tender"],
 ["Commander, there's a name carved under the floor of this one. I think it's mine. I'm not ready to say it aloud.", "tender"], ["There's a hall of white light in this one. I've stood in a hall like that. I'm sure of it.", "awe"],
 ["I keep going quiet when we find these. I'm sorry. It's like walking through a house I used to live in.", "tender"], ["Our team is inside the pyramid, Commander. The walls are humming. I know that hum. I don't know how.", "awe"],
 ["They carved the same word over every door. It means 'wait'. I don't know how I can read it.", "tender"], ["The chamber at the centre is empty again, Commander. Something was kept in these rooms. Or someone.", "grave"],
 ["The Union carries the old empire's guilt in its hulls, Commander. It makes them stubborn. It also makes them the last to run.", "warm"], ["The Syndicate knows more about the Void than anyone alive, Commander. That should worry you a little. It worries me.", "grave"],
 ["The Union has noticed you. They still think every problem is a target. Some of them are right.", "playful"], ["The Syndicate has been listening to the Void for a very long time. They heard something listen back.", "grave"],
 ["Every pyramid we open has the same empty room at its heart. I think I know what was kept there. I'm not ready to say it.", "tender"]].forEach(([l, m]) => { CIN_MOOD[l] = m; });
function cinema(beats, opt, done) { opt = opt || {}; const old = $("#cine"); if (old) old.remove(); const fac = facOf(), w = document.createElement("div"); w.id = "cine"; G.cineOn = 1;
  const src = s => s === "art/faction/" ? `art/faction/${fac}.webp?v=310` : s;
  w.innerHTML = `<div class="cnbg"></div><div class="cnimg a"></div><div class="cnimg b"></div><div class="cnfx"></div><div class="cnbar t"></div><div class="cnbar u"></div><div class="cnchip"></div><div class="cnmid"></div><div class="cnsub"></div><div class="cnch"></div><button class="cnskip" data-cn="skip">Skip ›</button>`;
  $("#app").appendChild(w); let i = -1, tmr = 0, live = true, flip = 0, waitChoice = false, token = 0;
  const end = () => { if (!live) return; live = false; clearTimeout(tmr); try { voiceStop(); } catch (e) {} w.classList.add("out"); setTimeout(() => { w.remove(); G.cineOn = 0; try { flushSay(); } catch (e) {} if (done) done(); }, 700); };
  const next = () => { if (!live || waitChoice) return; clearTimeout(tmr); try { voiceStop(); } catch (e) {} i++; if (i >= beats.length) return end(); show(beats[i]); };
  const show = b => { const tk = ++token, img = w.querySelector(flip ? ".cnimg.a" : ".cnimg.b"), prev = w.querySelector(flip ? ".cnimg.b" : ".cnimg.a"), fx = w.querySelector(".cnfx"), mid = w.querySelector(".cnmid"), sub = w.querySelector(".cnsub"), chip = w.querySelector(".cnchip"), ch = w.querySelector(".cnch");
    const same = b.img && prev.dataset.src === src(b.img);
    if (b.img && !same) { flip ^= 1; img.dataset.src = src(b.img); img.style.backgroundImage = `url("${src(b.img)}")`; img.className = "cnimg " + (flip ? "b" : "a") + " on kb-" + (b.kb || "in") + (b.img === "art/faction/" ? " wide" : ""); prev.classList.remove("on"); }
    else if (same) prev.className = prev.className.replace(/kb-\S+/, "kb-" + (b.kb || "in"));
    else if (!b.img) { w.querySelectorAll(".cnimg").forEach(e => { e.classList.remove("on"); e.dataset.src = ""; }); }
    fx.className = "cnfx " + (b.fx || "").split(" ").map(x => "fx-" + x).join(" "); fx.innerHTML = /pods/.test(b.fx || "") ? Array.from({ length: 26 }, (_, j) => `<i style="--x:${(j * 37) % 100};--y:${20 + (j * 53) % 60};--d:${(j % 7) * .4}s"></i>`).join("") : "";
    mid.innerHTML = b.title ? `<img class="cnlogo" src="art/logo-udf.webp" alt="Ultra Deep Field"><p class="cnq">What if the greatest monsters in the galaxy were the only things keeping us alive?</p>`
      : b.wardens ? `<div class="cnwd">${b.wardens.map((s, j) => `<img src="${s}" style="--j:${j}" alt="">`).join("")}</div>`
      : b.adv ? `<img class="cnadv" src="${advArt()}" alt="${ADV}">` : b.inset ? `<img class="cninset" src="${b.inset}" alt="">` : "";
    chip.textContent = b.chip || ""; chip.classList.toggle("on", !!b.chip); if (b.chip) { chip.style.animation = "none"; void chip.offsetWidth; chip.style.animation = ""; }
    sub.innerHTML = b.txt ? `${b.who ? `<small>${esc(b.who)}</small>` : ""}<p class="cntx">${esc(b.txt)}</p>` : b.line ? `<p>${esc(b.line)}</p>` : ""; sub.className = "cnsub" + (b.txt ? " tx" : "") + (b.adv ? " adv" : "");
    if (b.line) { try { document.documentElement.dataset.advMood = advMood(b.line); speak(b.line); } catch (e) {} }
    ch.innerHTML = ""; waitChoice = !!b.choice; /* a tap can't skip past a decision */
    if (b.choice) { setTimeout(() => { if (tk !== token || !live) return; ch.innerHTML = b.choice.map(([lb, v], j) => `<button class="btn ${j ? "ghost" : "amber"}" data-cn="c" data-v="${v}">${esc(lb)}</button>`).join(""); }, 1200); }
    const len = (b.line || b.txt || "").length, minT = b.t || Math.max(b.txt ? 4200 : 3000, len * (b.txt ? 58 : 66) + 900);
    const t0 = Date.now(), wait = () => { if (tk !== token || !live) return; const a = VOICE.au, busy = b.line && a && !a.paused && !a.ended && a.currentTime < (a.duration || 99); if (b.choice) return; if (busy || Date.now() - t0 < (busy ? 0 : minT)) tmr = setTimeout(wait, 250); else tmr = setTimeout(next, b.line ? 700 : 300); }; tmr = setTimeout(wait, 600); };
  w.addEventListener("click", e => { const t = e.target.closest("[data-cn]"); if (t && t.dataset.cn === "skip") { e.stopPropagation(); if (opt.onSkip) { live = false; clearTimeout(tmr); try { voiceStop(); } catch (er) {} w.remove(); G.cineOn = 0; opt.onSkip(); return; } return end(); }
    if (t && t.dataset.cn === "c") { e.stopPropagation(); waitChoice = false; const v = t.dataset.v; try { SFX.click(); } catch (er) {} if (opt.onChoice) { const more = opt.onChoice(v); if (more && more.length) { beats.splice(i + 1, beats.length, ...more); } } return next(); }
    if (t && t.dataset.cn === "go") { e.stopPropagation(); t.closest(".cngate").remove(); return next(); }
    if (!waitChoice && i >= 0) next(); });
  if (opt.gate) { const g = document.createElement("div"); g.className = "cngate"; g.innerHTML = `<small>Ultra Deep Field</small><h2>Before the Darkness</h2><p>Sound on for the full story.</p><button class="btn amber" data-cn="go">▶ Begin</button>`; w.appendChild(g); } else next();
  return w; }
function cinWhenClear(fn, n = 0) { if (n < 600 && ($("#authw") || $("#udfAuth") || $("#oldw"))) return void setTimeout(() => cinWhenClear(fn, n + 1), 1000); fn(); } /* never behind a sign-in screen */
function cinOpen(done) { S.cinSeen = 1; dirty(); cinema(CIN_OPEN.slice(), { gate: true }, done); }
/* the prologue: the assignment, the signal, the pyramid, her first words, the ambush (the old opening battle), the escape pods, her choice */
function proPlay(replay) { cinema(PRO_A.slice(), {}, () => { G.advThen = () => { G.proAfter = () => proPods(replay); try { playBattle(introBattle()); setTimeout(proLance, 2500); } catch (e) { G.proAfter = null; proPods(replay); } }; say(INTRO_PRE); }); }
/* the first thing you do: fire the pyramid's lance into the swarm (the ambush still ends the way the story needs it to) */
function proLance(n = 0) { if (!battle || !battle.r || battle.r.id !== INTRO_ID || $("#prlance")) return; const bw = $("#battle"); if (!bw) return; if (!(battle.intro <= 0 && battle.simT > .25) && n < 60) return void setTimeout(() => proLance(n + 1), 500); /* once the fighting has begun */ const b = document.createElement("button"); b.id = "prlance"; b.innerHTML = `<b>FIRE THE LANCE</b><small>Tap!</small>`; bw.appendChild(b);
  try { speak(PRO_LANCE); } catch (e) {} const sub = document.createElement("div"); sub.className = "prsub"; sub.textContent = PRO_LANCE; bw.appendChild(sub);
  b.onclick = e => { e.stopPropagation(); b.remove(); sub.textContent = PRO_LANCE2; const f = document.createElement("div"); f.className = "prbeam"; f.innerHTML = Array.from({ length: 7 }, (_, j) => `<i style="--x:${12 + j * 13}%;--y:${10 + (j * 29) % 28}%;--d:${.15 + j * .09}s"></i>`).join(""); bw.appendChild(f); try { SFX.blast(); SFX.laser(); } catch (er) {} try { navigator.vibrate && navigator.vibrate([60, 40, 120]); } catch (er) {}
    bw.classList.add("prshake"); setTimeout(() => { try { speak(PRO_LANCE2); } catch (er) {} }, 500); setTimeout(() => { f.remove(); bw.classList.remove("prshake"); }, 1700); setTimeout(() => sub.remove(), 4200); };
  setTimeout(() => { if (b.isConnected) { b.remove(); sub.remove(); } }, 14000); }
function proPods(replay) { let jumped = 0; cinema(PRO_B.slice(), { onChoice: v => v === "jump" && !jumped++ ? PRO_JUMP.slice() : PRO_BACK.slice(), onSkip: () => proLand(replay) }, () => proLand(replay)); }
function proLand(replay) { if (!replay) { S.proDone = 1; dirty(); } G.advThen = () => { try { proScouts(replay); } catch (e) { say([PRO_END]); } }; say([INTRO_POST[1]].concat(INTRO.slice(0, 3), [PRO_SCOUT])); }
/* the first win: a few Hive scouts that followed the pods down, and the colony's first guns */
function proScouts(replay) { const ours = { corvette: 12, heavyFighter: 30, battleship: 2 }, hive = colonyForce(1); let best = null;
  for (let i = 0; i < 6 && !best; i++) { const res = simulate(stacksOf(hive, { hive: 1 }, null), stacksOf(ours, { weapons: 0, shields: 0, armor: 0 }, G.me), { seed: 5100 + i }); if (res.winner === "d") best = res; }
  if (!best) return proWin(replay);
  const rep = Object.assign(mkRep({ at: now(), kind: "raid", title: "The first defence", aName: "Hive Scouts", dName: S.homeName || "Our new world", lvl: 1, ptype: "terran", fortL: 0, alien: true, start: best.start, rounds: best.rounds, winner: best.winner, sim: best.sim, lossA: lossesOf(best.start.a, best.aLeft), lossD: lossesOf(best.start.d, best.dLeft) }), { id: "intro-scouts", recDone: 1 });
  G.proAfter = () => proWin(replay); try { playBattle(rep); } catch (e) { G.proAfter = null; proWin(replay); } }
function proWin(replay) { if (!replay && !S.proWin) { S.proWin = 1; grantRw({ m: 3000, c: 2000, g: 800, shards: 5 }, "The first defence"); dirty();
    celebrate({ k: "firstwin", kick: "Your first victory", t: "This World Is Ours", art: "adv", s: "The Hive scouts are scrap. Your colony has its first victory, and its first spoils.", say: PRO_WIN, rw: "3,000 metal, 2,000 crystal, 800 gas and ◆5. Already in your stores.", go: "Let's build" }); }
  S.say.push(INTRO[3], PRO_END, PRO_TEASE); dirty(); setTimeout(() => { try { flushSay(); } catch (e) {} }, 400); try { if (!replay) setTimeout(() => { try { archFleetTick(); } catch (e) {} }, 60000); } catch (e) {} }
