# Flight Academy audit (v331, 2026-11-07)

Generated from the live `TUT` array (37 steps). Columns: step, permanent id (only some steps have one), commander level shown, title, the real completion check, how "Show me" finds the target, whether the step pays for what it asks, reward.

| # | id | Lv | Step | Completion check | Show me | Funded | Reward |
|---|---|---|---|---|---|---|---|
| 1 |  | 1 | Choose your commander name | `s => !!s.tutNm` | open |  | m 200, c 100 |
| 2 |  | 1 | Name your homeworld | `s => !!s.tutHw` | open |  | m 200, c 150 |
| 3 |  | 1 | Build a Metal Extractor | `s => s.b.metalMine >= 1` | go {"v":"build","s":"res"} |  | m 300, c 150 |
| 4 |  | 1 | Build a Solar Array | `s => s.b.solar >= 1` | go {"v":"build","s":"res"} |  | m 300, c 200 |
| 5 |  | 1 | Build a Crystal Refinery | `s => s.b.crystalMine >= 1` | go {"v":"build","s":"res"} |  | m 400, c 250 |
| 6 |  | 1 | Upgrade the Metal Extractor to Lv.2 | `s => s.b.metalMine >= 2` | go {"v":"build","s":"res"} |  | m 500, c 300 |
| 7 |  | 1 | Build a Gas Synthesizer | `s => s.b.gasSynth >= 1` | go {"v":"build","s":"res"} |  | m 300, c 150, g 450 |
| 8 |  | 2 | Build Drone Works | `s => s.b.robotics >= 1` | go {"v":"build","s":"fac"} |  | m 600, c 300, g 150 |
| 9 |  | 2 | Build the Shipyard | `s => s.b.shipyard >= 1` | go {"v":"build","s":"fac"} |  | m 1200, c 500 |
| 10 |  | 2 | Build the Research Center | `s => s.b.lab >= 1` | go {"v":"build","s":"fac"} |  | m 800, c 1000, g 300 |
| 11 |  | 3 | Research Energy Technology | `s => s.r.energyT >= 1` | go {"v":"lab"} |  | m 2500, c 1200, g 700, shards 1 |
| 12 |  | 3 | Research Combustion Drive | `s => s.r.drive >= 1` | go {"v":"lab"} |  | m 3500, c 1200, g 300 |
| 13 |  | 3 | Build 3 Light Fighters | `() => own("fighter") >= 3` | go {"v":"build","s":"ships"} |  | m 800, c 400, shards 2 |
| 14 |  | 3 | Attack a Hive garrison | `s => s.wins >= 1 // !!tutFleet()` | hive target |  | m 600, c 300, shards 1 |
| 15 | tap | 3 | Tap your fleet on the map | `s => !!s.tutTap` | fly |  | m 400, c 300, g 100 |
| 16 | rush | 3 | Rush the attack | `s => !!s.tutRush` | fly |  | m 500, c 400, g 200, shards 1 |
| 17 | cine | 3 | Watch it in cinematic view | `s => !!s.tutCine` | fly |  | m 500, c 400, g 200 |
| 18 |  | 3 | Defeat a Hive garrison | `s => s.wins >= 1` | hive target |  | m 1200, c 700, g 300, shards 3 |
| 19 |  | 3 | Gather from a resource field | `s => (s.stats // {}).gathers >= 1 // s.fleets.some(f => f.nid)` | find m |  | m 1000, c 600, g 300 |
| 20 |  | 3 | Explore a pyramid space station | `s => (s.stats // {}).pyramids >= 1 // s.fleets.some(f => f.yid)` | find y |  | m 800, c 800, g 400, shards 1 |
| 21 |  | 4 | Read your reports in Mail | `s => !!s.tutMail` | go {"v":"mail"} |  | m 500, c 500, g 500 |
| 22 |  | 5 | Raid a Lv.5 pirate hideout | `s => (s.stats // {}).pirates >= 1` | find x | yes | m 1500, c 1000, g 500, shards 2 |
| 23 |  | 4 | Upgrade the Crystal Refinery to Lv.5 | `() => lvlOf("crystalMine") >= 5` | go {"v":"build","s":"res"} | yes | m 3000, c 2000, g 1000, shards 5 |
| 24 |  | 5 | Upgrade the Research Center to Lv.3 | `() => lvlOf("lab") >= 3` | go {"v":"build","s":"fac"} | yes | m 2500, c 4000, g 1500, shards 1 |
| 25 |  | 5 | Research Impulse Drive to Lv.3 | `s => (s.r.impulse // 0) >= 3` | go {"v":"lab"} | yes | m 6000, c 10000, g 2000, shards 2 |
| 26 |  | 5 | Research Espionage Technology to Lv.4 | `s => (s.r.espionage // 0) >= 4` | go {"v":"lab"} | yes | m 3000, c 9000, g 2000, shards 2 |
| 27 |  | 5 | Research Astrophysics Lv.1 | `s => (s.r.astro // 0) >= 1` | go {"v":"lab"} | yes | m 4000, c 8000, g 4000, shards 3 |
| 28 |  | 5 | Research Astrophysics Lv.2 | `s => (s.r.astro // 0) >= 2` | go {"v":"lab"} | yes | m 8000, c 12000, g 6000, shards 5 |
| 29 |  | 6 | Build 2 Espionage Probes | `s => own("spyProbe") >= 2 // ((s.stats // {}).spies // 0) >= 1` | go {"v":"build","s":"ships"} | yes | m 3000, c 4000, g 1000, shards 2 |
| 30 | spy | 6 | Spy on a Hive world | `s => ((s.stats // {}).spies // 0) >= 1` | hive target |  | m 2000, c 3000, g 1000, shards 2 |
| 31 |  | 6 | Read the espionage report | `s => !!s.tutSpyR` | go {"v":"mail"} |  | m 2000, c 2000, g 1000, shards 1 |
| 32 | scouted | 6 | Attack the world you scouted | `s => ((s.stats // {}).hiveWins // 0) >= (s.tutSpyW != null ? s.tutSpyW : 1) + 1` | hive target | yes | m 6000, c 4000, g 2000, shards 3 |
| 33 |  | 6 | Build a Colony Ship | `s => own("ark") >= 1 // (s.captures // 0) >= 1 // myPlanets().length >= 2` | go {"v":"build","s":"ships"} | yes | m 10000, c 12000, g 6000, shards 3 |
| 34 |  | 6 | Settle your first colony | `s => (s.captures // 0) >= 1 // myPlanets().length >= 2` | hive target | yes | m 15000, c 15000, g 8000, shards 5 |
| 35 |  | 6 | Raid pirates for flagship materials | `s => ((s.stats // {}).pirates // 0) >= 2` | find x | yes | m 40000, c 30000, g 12000, shards 5, fs {'alloy1': 6, 'circuit1': 4, 'crystal1': 3} |
| 36 | dock | 6 | Build the Flagship Dock | `s => (s.b.flagDock // 0) >= 1` | go {"v":"build","s":"fac"} | yes | m 20000, c 15000, g 8000, shards 3, fs {'alloy1': 4, 'circuit1': 2, 'crystal1': 1} |
| 37 |  | 6 | Commission your flagship | `s => !!(s.fs && s.fs.built)` | open | yes | m 15000, c 10000, g 5000, shards 10 |

## Before step 1 (online)
Sign-in → (new account, no cloud save) "Played before the move?" card → faction choice → opening ambush briefing (2 lines) → opening battle (`introBattle`, seed 4100+, the convoy survives) → 3 lines after → 4-line briefing → step 1.

## Findings against the remaster brief (to fix)
1. **The opening battle is won, not lost.** `introBattle` retries seeds until the defender wins ("we always come through it"); the owner asked for a battle we lose and then rebuild.
2. **First attack happens without scouting.** Steps 13–18 send fighters at a Hive garrison; espionage comes at steps 29–32. The owner's order: build fighters → espionage → read the report → attack → upgrades/research → Astrophysics 2 → colony.
3. **No onboarding measurement.** Where players stop is only visible by reading saves by hand (2026-11-07: 9 of 10 accounts stopped mid-Academy: steps 1, 11, 11, 12, 12, 15, 15, 18, 28).
4. **Only 9 of 37 steps have a permanent id**; the rest are tracked by array index, which is why old saves needed index-shifting migrations (`tutFx`, `tutSC`, `TUT_V2`).
5. **Commander level labels go backwards** (step 22 shows Lv5, step 23 Lv4).
6. Fixed in v329–v331 (regression-tested online): hidden guide, old-server card over the opening, faction skipped on account switch, uncharted targets (steps 14, 30, 32), returning-fleet guidance (step 22), taken commander name.
