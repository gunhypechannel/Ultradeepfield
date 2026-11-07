# Advisor voice lines

The game plays `docs/voice/<key>.mp3` for an Advisor line when `docs/voice/index.json` lists that key; any line without a clip falls back to the device's own female voice.

**To add recorded clips**

1. Generate each line below with an AI voice (ElevenLabs or similar). Suggested direction: a confident, warm female officer, mid-30s, slight urgency, clean studio sound, no music. Keep the wording exactly as written.
2. Export each as MP3 (mono, 64-96 kbps keeps them small) named `<key>.mp3`.
3. Put them in `docs/voice/` and add `docs/voice/index.json` listing the keys you have, for example `{"1a2b3c": 1, "4d5e6f": 1}`.
4. If a line's wording ever changes in the game, its key changes too: rerun the export (see handoff) and record the new line.

| key | where | line |
|---|---|---|
| `tt9plo` | Opening ambush | Commander, on your feet! A Hive swarm just dropped out of the dark, right across the convoy's course. |
| `br883n` | Opening ambush | They don't take prisoners and they don't bargain. Every gun we have: weapons free! |
| `xkmf72` | After the ambush | The swarm is broken. We held, Commander. |
| `13gbtlr` | After the ambush | That swarm answered to Vael'Khor, the Hive Matriarch. She devours whole worlds, and now she knows our name. |
| `c4wp9p` | After the ambush | It cost us dearly, and our reactors were nearly dry. We set down on the nearest world we could reach. |
| `hftg0t` | Briefing | Commander. We made it, barely. The convoy is gone, and this world is all we have left. |
| `1kcj9id` | Briefing | Every planet here orbits the Void, a black hole at the heart of the galaxy. The Hive holds most of them. |
| `1nkrgxh` | Briefing | We're not alone either. Other commanders orbit the Void, and any colony can change hands. |
| `10tmlvy` | Briefing | Now we rebuild, and we grow strong enough to end Vael'Khor. I'll post directives on the Base tab. Complete them and Fleet Command will send supplies. |
| `19d9s90` | Academy step 1: Choose your commander name | First things first, Commander: what should the galaxy call you? Every commander sees this name. Type it and tap Save. |
| `1bboqsh` | Academy step 2: Name your homeworld | This world is ours now. Give our capital a name worthy of an empire, then tap Save. |
| `cqyvrx` | Academy step 3: Build a Metal Extractor | Everything starts with metal. Open Structures and build your first Metal Extractor. |
| `4twm22` | Academy step 4: Build a Solar Array | Extractors need power. A Solar Array keeps them running at full speed. |
| `1761hpu` | Academy step 5: Build a Crystal Refinery | Crystal pays for research and better hulls. Get a refinery going. |
| `s1tekx` | Academy step 6: Upgrade the Metal Extractor to Lv.2 | Upgrades multiply your income. Jobs under five minutes finish for free: tap Free when it appears. |
| `1e9qva0` | Academy step 7: Build a Gas Synthesizer | Drones, ships and research all burn gas. Get a synthesizer running. |
| `1hb4kg4` | Academy step 8: Build Drone Works | Drone Works speeds up every construction and unlocks the Shipyard. You'll find it under Facility. |
| `1ozdgao` | Academy step 9: Build the Shipyard | No fleet, no empire. Build the Shipyard. |
| `jvnh7y` | Academy step 10: Build the Research Center | Ships need engines, and engines need research. Build a Research Center under Facility. |
| `9nji2f` | Academy step 11: Research Energy Technology | Energy Technology is the root of the tech tree, and Combustion Drive needs it. Start it now. |
| `1sfzgy7` | Academy step 12: Research Combustion Drive | Combustion Drive powers your first warships. Once it is done, the Shipyard can build Light Fighters. |
| `lngo7s` | Academy step 13: Build 3 Light Fighters | Light Fighters are cheap and fast: perfect for your first raids. Queue three of them. Academy crews build them in a minute each. |
| `1g3l9fn` | Academy step 14: Attack a Hive garrison | The amber worlds belong to Vael'Khor's Hive. I've marked a weak garrison near us: send the fighters and show her we bite back. |
| `1u7wd6o` | Academy step 15: Tap your fleet on the map | Our fighters are under way. Find them on the Galaxy map and tap them: the camera follows your fleet and its control bar opens. |
| `ifvyi7` | Academy step 16: Rush the attack | Every minute in transit is a minute the Hive digs in. Tap ⚡ to light the afterburners: the rest of the trip is 50% faster. This first burn is on the Academy. |
| `d0prjb` | Academy step 17: Watch it in cinematic view | Now sit back, Commander. Tap 🎥 and the camera rides in with your fighters, right into the fight. |
| `p8h80b` | Academy step 18: Defeat a Hive garrison | Our fighters are closing on the garrison. Win the fight and the report lands in Mail. If they lost, send them again. |
| `v1h151` | Academy step 19: Gather from a resource field | Resource fields pay out to whoever holds them. Fields already held by a rival must be fought for, so pick a free one. |
| `1hf786y` | Academy step 20: Explore a pyramid space station | Derelict pyramid stations drift all over the map. Low-level vaults are unguarded: free shards and relics. |
| `1u03me1` | Academy step 21: Read your reports in Mail | Every battle, espionage report and message lands in Mail. Replays show you exactly why you won or lost. |
| `17p2ovv` | Academy step 22: Raid a Lv.5 pirate hideout | Pirates hoard loot and drop rare items. This first crew is a small one: send every fighter you have. |
| `1yzz0d0` | Academy step 23: Upgrade the Crystal Refinery to Lv.5 | Crystal is the rarest thing we mine, and research runs on it. Take the Crystal Refinery to Lv.5: every level digs faster. The Academy covers the cost. |
| `qnrsdj` | Academy step 24: Upgrade the Research Center to Lv.3 | Next goal: a second world. Astrophysics decides how many planets we can hold, and it needs Research Center Lv.3, Espionage Technology Lv.4 and Impulse Drive Lv.3. Start with the Research Center. |
| `12wx2hx` | Academy step 25: Research Impulse Drive to Lv.3 | Impulse Drive speeds up Colony Ships and heavier hulls, and Astrophysics needs Lv.3. Find it under Engine Research. |
| `27eszz` | Academy step 26: Research Espionage Technology to Lv.4 | Better probes, and the last thing Astrophysics needs. Take Espionage Technology to Lv.4 under Advanced Research. |
| `wn92mc` | Academy step 27: Research Astrophysics Lv.1 | Everything is in place. Start Astrophysics under Advanced Research: it charts stable orbits for settlers. |
| `1unzxmi` | Academy step 28: Research Astrophysics Lv.2 | One more level and we can hold a second world. Every 2 levels of Astrophysics adds a planet, up to 10. |
| `qs3puc` | Academy step 29: Build 2 Espionage Probes | Never attack blind. Espionage Probes fly in, count the defenders and come home with a report. They need Shipyard Lv.3 and Espionage Technology Lv.2. |
| `libyi9` | Academy step 30: Spy on a Hive world | I've marked the weakest Hive world near us. Tap Espionage on its card and send your probes. |
| `1c3bbn` | Academy step 31: Read the espionage report | The probes are back. Open the report in Mail: it shows the defenders, their ships and the resources you could take home. |
| `1y54ujo` | Academy step 32: Attack the world you scouted | Now we know what's there. Send a fleet that outguns its garrison: the report shows exactly what you're up against. |
| `zqulky` | Academy step 33: Build a Colony Ship | Astrophysics Lv.2 lets us hold a second world. A Colony Ship needs Shipyard Lv.4 and Impulse Drive Lv.3. |
| `goz2p7` | Academy step 34: Settle your first colony | Send the Colony Ship along with your warships to a Hive world you can beat. Win the battle and the world becomes ours: our second planet, and the first world we take back from Vael'Khor. |
| `1yrvw5p` | Academy step 35: Raid pirates for flagship materials | Our flagship is built from rare materials, and pirates hoard them. Raid another hideout: what they drop goes to the Flagship Dock. After that, the Academy clears you to build the Dock. |
| `1tcw2cb` | Academy step 36: Build the Flagship Dock | The Flagship Dock is where our flagship is commissioned and where its gear is forged. Find it under Structures → Facility. |
| `tk2daa` | Academy step 37: Commission your flagship | Everything's ready, Commander. Commission the flagship: from now on it leads every fleet we send, gains experience and wears the gear the Dock forges. |
| `299sx4` | Story | Clean work, Commander. That garrison won't trouble us for a while. |
| `jkjerv` | Story | Vael'Khor felt that. Once your Academy training is done, expect her raiders over our homeworld. |
| `tghpbu` | Story | Build defenses and keep some ships at home. Chapter 2: Hold the Line. |
| `vzhfwk` | Story | The worlds nearer the Void are richer, and the Hive guards them harder. |
| `z62a55` | Story | Check the tech tree in Research. Heavier hulls need lasers, ion and hyperspace tech. Chapter 3: Into the Reach. |
| `d7fz3o` | Story | Scouts found Hive breeding grounds along the event rim. Leviathans guard them. |
| `12i581b` | Story | Plasma weapons and Reapers will break them. Chapter 4: Breaking the Hive. |
| `pnb9wt` | Story | That's the Academy done, Commander. Our flagship leads the fleet now: it earns experience in every fight, and the Flagship Dock forges its gear. |
| `19zk6q` | Story | Every 2 Astrophysics levels lets us hold another world: build more Colony Ships and send them with escorts to Hive worlds we can beat. I'll keep pointing you at the next directive on your path. |
| `sgmume` | Story | And Commander: Fleet Command's supply convoy lands in 8 hours. Come back then and claim it on the Quests tab. |
