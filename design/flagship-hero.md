# Flagship Command: the faction flagship as a hero (v298)

Design, data model and verification for the Faction Flagship Hero and Equipment System. Code lives in `docs/index.html`: search for `v298 FLAGSHIP COMMAND`. The economy model is `tools/flagship_econ.py`.

**Scope.** The flagship that already leads every fleet becomes a hero with levels, skills, equipment, a forge and materials. It is not an extra combat unit. Its bonuses go into the game's existing tech and economy multipliers. Nothing existing was replaced.

---

## 1. Data structure

Everything is stored in the existing save under `S.fs`. `fsOf()` creates it lazily, so old saves need no migration step.

```
S.fs = {
  v:    1,          // bump counter; invalidates the bonus cache (fsB)
  xp:   0,          // XP toward the next level
  lv:   1,          // 1..60 (FS_MAX)
  sk:   { war0: 3, def1: 5, ... },  // tree id + node index -> rank 0..5
  eq:   { weapon: "fq12", ... },    // slot -> item id
  inv:  [ { id, job, s: slot, t: tier 1..6, set, f: faction, lv: enhance 0..10 } ],
  mats: { alloy1: 40, cube5: 3, ... },  // kind + tier -> count
  q:    [ { id, s, t, set, f, ms, s0, e } ],  // forge queue, max 3 (FS_QMAX)
  loads:[ { n: name, eq: {...} } ],  // saved loadouts (max 3)
  seq:  1,          // item id counter
  day:  { d: "20261105", n: 0 },     // daily drop counter for the soft cap
  resp: 0           // time of the last free respec
}
```

**Static catalogs:**
- `FS_SLOTS`: 8 slots with name, icon, base stats, primary and secondary material.
- `FS_TIER`: names and colours.
- `FS_TMUL`: tier multipliers, `[1, 1.6, 2.4, 3.5, 5, 7]`.
- `FS_MATS`: 6 kinds.
- `FS_SETS`: 6 sets, with bonuses at 2, 4 and 6 pieces.
- `FS_FAC`: faction perks.
- `FS_NAMES`: faction item names.
- `FS_TREES`: 5 trees, 16 nodes, 5 ranks each.
- `FS_CAP`: a cap per stat.

| Slot | Base stats (Common) | Primary / secondary material |
|---|---|---|
| Main Weapon | +2% attack | Circuitry / Cube Fragment |
| Shield Generator | +2% shields | Quantum Crystal / Cube Fragment |
| Armor Plating | +2% hull | Alloy / Exotic Tissue |
| Reactor Core | +2% output, −3% fuel | Quantum Crystal / Void Essence |
| Command Bridge | +1% attack, +1% shields | Circuitry / Exotic Tissue |
| Engine System | +2% speed, +2% gathering | Alloy / Quantum Crystal |
| Tactical Computer | −2% research time, −1% build time | Circuitry / Quantum Crystal |
| Special Artifact | +2% vs pirates, monsters and Cubes, +2% cargo | Void Essence / Cube Fragment |

**Item stats** = base × tier multiplier × (1 + 5% per enhancement level, up to +10). A Mythic +10 weapon gives 2 × 7 × 1.5 = **+21% attack**.

**Faction perks.** Legendary and Mythic gear adds a small perk of the same size for every faction. For each Legendary item the perk is: Union +1% shields, Dominion +1% output, Nyx +1% attack, Verdant +2% gathering. Mythic doubles it.

## 2. Recipe catalog

Every slot can be forged at any tier, in any set.

| Tier | Materials | Resources (metal / crystal / gas) | Forge time |
|---|---|---|---|
| Common (1) | 3 primary T1, 2 secondary T1, 5 alloy T1 | 20k / 12k / 5k | 15 min |
| Uncommon (2) | 3 + 2 of T2, 5 alloy T1 | 60k / 36k / 15k | 33 min |
| Rare (3) | 3 + 2 of T3, 5 alloy T2 | 180k / 108k / 45k | 1 h 13 m |
| Epic (4) | 3 + 2 of T4, 5 alloy T3 | 540k / 324k / 135k | 2 h 40 m |
| Legendary (5) | 3 + 2 of T5, 5 alloy T4 | 1.62M / 972k / 405k | 5 h 52 m |
| Mythic (6) | 3 + 2 of T6, 5 alloy T5 | 4.86M / 2.92M / 1.22M | 12 h 54 m |

**Other forge actions:**
- **Combine:** 5 materials of one tier make 1 of the next tier. Each combine also costs 1k×4^(t−1) metal and 600×4^(t−1) crystal.
- **Enhance:** each level costs 1 + ⌊lv/3⌋ primary materials of the item's tier, plus 5k×2^(t−1)×lv metal and 3k×2^(t−1)×lv crystal. The maximum is +10.
- **Dismantle:** tap twice to confirm. Returns half the recipe materials, rounded down.
- **Cancel:** a queued job refunds everything.
- **Queue:** 3 jobs. Each job starts when the one before it finishes.

## 3. Loot table

Each enemy type drops its own material. L is the target's level: pirates are 5, 10 or 15, and monsters, Cubes and fields are 1–30. t is the tier of the drop.

| Source | XP | Drops |
|---|---|---|
| Pirate hideout | 10 × L | Circuitry t = 1+⌊L/8⌋, ×(1+⌊L/5⌋); Alloy t, ×(1+⌊L/8⌋); 12% chance of 1 Circuitry at t+1 |
| Space monster | 20 × L | Exotic Tissue t = 1+⌊L/8⌋, ×(1+⌊L/8⌋); 35% chance of Void Essence t; 8% chance of a Cube Fragment t; 10% chance of Tissue t+1 |
| Cube boss (solo) | 40 × L | Cube Fragments t = 1+⌊L/7⌋ (2–5), ×(2+⌊L/10⌋); Void Essence ×1, with a 25% chance of a second; 10% chance of a Cube Fragment t+1 |
| Cube boss (joint strike) | 40 × L | As solo, plus 1 extra Cube Fragment and a 50% chance (instead of 25%) of the second Void Essence. Every member who joined gets their own roll. |
| Gathering a field | amount/5000, up to 200 | Crystal (crystal and gas fields) or Alloy (metal fields), t = 1+⌊field L/8⌋, ×⌈amount/60k⌉ up to 6; 12% chance of t+1 |
| Recycling wreckage | — | 25% chance of 1 Alloy, T1–T3 depending on the amount salvaged |
| Hive win | yes | Alloy and Crystal |
| PvP win | 300 | — |
| Daily directive | 80 | — |
| Academy | 50 | — |

**Daily soft cap.** After 70 drops in a UTC day, each further drop is kept with a chance of 0.5^(1+(n−70)/15). Steady play always progresses, but farming can't flood the economy.

**Alliance sources.** Joint strikes give the bonus rolls above. Alliance-only material events are not built yet; see §7.

## 4. Leveling and skill model

- **Unlock.** Commander Lv.15 (`flagOK`, the same rule that already gates the flagship). Below that, every bonus returns 0.
- **XP per level.** Going from level L to L+1 takes 200·L^1.5 XP. Cumulative totals:

| Level | 10 | 20 | 30 | 40 | 50 | 60 |
|---|---|---|---|---|---|---|
| Total XP | 22k | 134k | 378k | 784k | 1.38M | 2.18M |

  An active player earns about 7k XP a day, which reaches Lv.30 in about 2 months and Lv.60 in about 10 months.
- **Skill points.** One per level after the first, so 59 at Lv.60. The 5 trees hold 16 nodes × 5 ranks = 80 ranks, so a player must specialise.

| Tree | Nodes (per rank) |
|---|---|
| Warfare | Gun Crews +1% attack · Hunter Doctrine +1.5% vs pirates, monsters and Cubes · Overcharge +0.5% attack and +0.5% hull |
| Defense | Shield Harmonics +1% shields · Ablative Plating +1% hull · Bulwark +0.5% shields and +0.5% hull |
| Economy | Logistics Office +1% output · Drone Foremen −1% build time · Trade Routes +0.5% output and −0.5% build time |
| Research | Science Deck −1.2% research time · Field Labs −0.6% research time and −0.4% build time · Applied Science +0.4% output |
| Fleet Operations | Navigation +1% speed · Hold Masters +1.5% cargo · Prospectors +1.5% gathering · Efficient Drives −2% fuel |

- **Respec.** Free once every 7 days, otherwise ◆50. Tap twice to confirm.

**Set bonuses:**

| Set | 2 pieces | 4 pieces | 6 pieces |
|---|---|---|---|
| Conqueror | +3% attack | +3% attack | +4% attack, +2% shields |
| Guardian | +3% shields | +3% hull | +3% shields, +3% hull |
| Harvester | +5% gathering | +6% cargo | +5% gathering, +3% speed |
| Architect | −3% build time | +3% output | −3% build time, +3% output |
| Scientist | −3% research time | −3% research time | −4% research time, −2% build time |
| Void Hunter | +4% vs pirates, monsters and Cubes | +4% vs pirates, monsters and Cubes | +4% vs pirates, monsters and Cubes, +3% attack |

## 5. Combat and economy integration

**Formula.** For each stat, everything is added: skills, item stats, set bonuses and the faction perk. The sum is then capped:

| Stat | Cap |
|---|---|
| attack, shields, hull | 40% |
| vs pirates, monsters and Cubes | 30% |
| output, build time, research time, speed | 30% |
| cargo, gathering, fuel | 40% |

The capped total joins the game's existing system once:

- **Attack, shields and hull** become tech levels (10% = 1 level) inside `techOf(null)`. They add to research, runes, VIP and alliance passives, so Final = Base × (1 + all bonuses). Everything that uses `techOf` now includes them: solo attacks, defense, pirates, monsters, Cubes, joint strikes, the battle forecast and Efficient Fight.
- **The bonus vs pirates, monsters and Cubes** is added through `techVs(x)`, and only when the target is in `PB`. It applies in `pirateArrive`, the pirate forecast and `effPick`.
- **PvP.** `syncPlayer` publishes `tech.fsa`, `fss` and `fsh` (capped). Other players' tech reads them back, clamped to the caps, so the defender's and attacker's flagships both count in PvP.
- **No double application.** The bonus multiplies only its owner's own ships. In a joint strike, each member brings their own flagship's bonus for their own stacks. Cargo and speed use the own-fleet path only.
- **Economy hooks:**
  - output → `prodBonus`
  - build time → `bTimeMul`
  - research time → `rTimeMul`
  - cargo → `cargoOf`
  - speed → `travelMs`
  - gathering → `haulPlan`
  - fuel → `fuelFor`
- **Performance.** `fsB(k)` caches the totals per bump, because battles ask for tech many times a frame.

## 6. Economy simulation

`tools/flagship_econ.py` models the drop formulas above, the daily cap and the forge recipes. Materials are measured in tier-1 equivalents (5 of a tier = 1 of the next). The model asks how many days of income it takes to forge a full 8-slot set at one tier.

| Player | Daily play in the model | Drops/day | Rare set | Epic set | Legendary set | Mythic set |
|---|---|---|---|---|---|---|
| Casual | 6 pirates L10, 2 monsters L10, 4 gathers, a joint Cube every 3 days | 50 | 21 d | 103 d | 1.4 y | — |
| Active | 14 pirates L15, 6 monsters L22, 10 gathers, 1 joint Cube L21 | 92 | 2 d | 12 d | 61 d | 304 d |
| Hardcore | 60 pirates, 30 monsters L28, 30 gathers, 4 joint Cubes L28 | 127 (capped) | 1 d | 4 d | 22 d | 110 d |

- **Tuning.** The first pass, with tiers rising every 5–6 levels and a cap of 90 that decayed slowly, gave an active player a Mythic set in 43 days. Casual players were also blocked, because Cube Fragments and Void Essence came only from Cubes. v298 ships the tuned values:
  - tiers rise every 8 levels;
  - monsters drop Cube Fragments at 8% and Void Essence at 35%;
  - Cubes always drop Void Essence;
  - the cap is 70 and decays twice as fast.
- **Bottlenecks** are now Void Essence and Crystal, which come from monsters, Cubes and crystal fields. These are the activities the game wants to encourage, joint Cube strikes in particular.
- **Forge time for a Mythic set** is about 4.3 days with a queue of 3. Resource costs at Epic and above are a real sink for a mid-game economy.

## 7. Phased implementation and tests

| Phase | Content | Status |
|---|---|---|
| 1 | Data, XP, levels, skill trees, respec, Lv.15 gate | Done (v298) |
| 2 | 8 slots, items, tiers, equip and unequip, compare, loadouts | Done (v298) |
| 3 | Materials, loot from every source, combining, forge with queue, enhance, dismantle | Done (v298) |
| 4 | Sets, faction perks, combat and economy integration, PvP publishing | Done (v298) |
| 5 | 3D gear upgrades on the flagship model in map and battle | Partial: rarity glow in the UI portrait only |
| 6 | Alliance material events, server-side validation | Not started; see §8 |

**Tests** use the offline harness `gt/tfs.js` (v298, Playwright and SwiftShader, mobile viewport). Every check passed with no page errors:

- **Gate.** Below commander Lv.15: bonuses 0, and the screen says when the flagship takes command. At Lv.62 with 250k XP: flagship Lv.25 with 24 points.
- **Skills** (5 attack, 5 shields, 5 output, 6 research time, 4 speed): `techOf` weapons +0.5 levels.
- **Forge.** Mythic weapon and bridge crafted. The queue limit of 3 is enforced, cancel refunds, and each item is granted exactly once.
- **Equip.** Attack 29% (5 from skills, 14 weapon, 7 bridge, 3 Conqueror 2-piece) gives +2.9 weapon levels in `techOf` and in `myTech`. Caps hold.
- **Enhance, combine, dismantle.**
  - Enhance: 14 → 15.4 at +2.
  - Combine: 40 → 35 alloy T1, +1 alloy T2.
  - Dismantle returns half the materials.
  - A loadout saves and restores.
- **Loot.** Cube Alpha-26 gives +1,040 XP and materials, and the daily counter advances.
- **Economy.** `prodBonus` 1.05 and `rTimeMul` 0.94 with the skills above.
- **UI.** All 5 tabs render on an iPhone 13 viewport.
- **Battle regression** (`gt/suite.js`): duel and 10v10 play, replay, end and close with no page errors. The only console messages are the harness's usual blocked-font messages.

## 8. Save migration and security

- **Migration.** Older saves have no `S.fs`. `fsOf()` fills every field with a safe default and repairs wrong types (non-object maps, non-array lists, NaN numbers), clamping the level to 1–60. Nothing else in the save changes. Saves still go through the existing cloud save; the v293 split that keeps reports separate is unchanged.
- **Client-side checks.** These are what the client enforces:
  - materials and resources are checked before every craft, combine or enhance, and taken in the same step;
  - forge jobs become items exactly once, keyed by job id;
  - stats are capped;
  - the published PvP values are clamped on read.
- **Security, stated plainly.** UDF is client-authoritative. The save signature catches casual edits but is **not** server-side protection. A player who edits their own save could give themselves materials or levels. Clamping published values limits how far a cheat can move another player's battle: at most the cap, +4 tech levels. It does not stop the cheat. Server-side validation still needs to be built:
  1. a Supabase RPC or edge function that grants drops from a server-side battle record and recomputes `fsa`, `fss` and `fsh` from a stored equipment list;
  2. row-level security so a client can't write those fields directly;
  3. server timestamps for forge jobs.

## 9. Verification report

- **Not yet verified:**
  - frame rate on real phones (SwiftShader frame rates don't mean anything);
  - two real accounts in PvP, to see published flagship bonuses both ways;
  - drop rates over weeks of real play.
- **Known gaps:**
  - 3D visual gear evolution (Phase 5);
  - alliance-exclusive material events;
  - server-side validation (§8).

---

## v299: Flagship Dock, Lv.10 unlock, Academy steps

- **Unlock moved to commander Lv.10.** The flagship starts at Lv.1 with no skills or gear, so at Lv.10 its bonuses are near 0. They grow only with play: Common gear gives +2%, and reaching flagship Lv.10 takes about 2 weeks. This keeps the new players' edge small. Commanders already at Lv.15+ keep their flagship automatically.
- **The flagship must be commissioned.** This happens at the new **Flagship Dock**, a homeworld Facility building that needs commander Lv.10 and Shipyard Lv.2.
  - Dock cost: 20k metal, 15k crystal, 6k gas, ×1.8 per level.
  - Commissioning cost: 30k metal, 20k crystal, 10k gas, plus 10 Alloy T1, 6 Circuitry T1 and 4 Crystal T1.
- **The Forge moved into the Dock.**

| Gear tier | Common | Uncommon | Rare | Epic | Legendary | Mythic |
|---|---|---|---|---|---|---|
| Dock level needed | 1 | 2 | 4 | 6 | 9 | 12 |

  Forge queue slots are 1 + ⌊Dock level/4⌋, up to 3. Forging gets 3% faster per Dock level, up to 30%.
- **Materials drop from day one.** Pirates, monsters, Cubes, fields, wreckage and salvage pods all drop materials before the flagship exists; pods have a 35% chance of 1 T1 Alloy or Crystal. Flagship XP still starts only once it is commissioned.
- **Academy.** Three steps were added after Astrophysics Lv.2: Reach Commander Level 10, Build the Flagship Dock, Commission your flagship. Their rewards pay every commissioning material: alloy 6+4, circuitry 4+2, crystal 3+1. They also pay 75k metal, 55k crystal and 25k gas in total, which covers the Dock and most of the commissioning. Normal drops along the way are left over for the first Common gear. Commanders who had already finished the Academy get the new steps unless they have both a Dock and a flagship.
- **Tested** with `tools/t299.js`:
  - the gate at Lv.1 (Dock locked: "Commander Level 10, Shipyard 2");
  - materials but no XP before the flagship;
  - the three Academy steps end to end: the rewards cover the commission exactly and nothing is left over;
  - Forge gates: Rare blocked at Dock Lv.1, queue 1; at Dock Lv.9, queue 3, Legendary allowed, forging 24% faster;
  - grandfathering and the `tech.fl` rule for other players;
  - the Academy migration.

  No page errors.
