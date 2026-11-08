# v338 Stage 1 of the crafting economy: every material source in one LOOT table (same numbers as v298 for the old sources), new sources
# (Hive fights, Hive raids defended, pyramid vaults, daily and weekly missions, achievements, events), elite pirates and monsters,
# first-kill bonuses and a pity counter on rare upgrade rolls. Quest-type rewards don't count toward the daily farming cap.
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)

# ---- the table, rollers and grants (replaces the three v298 loot functions) ----
i = t.index('function fsLootPB(x, rally) {'); j = t.index('/* combining: five of a tier make one of the next')
NEW = r'''/* v338 LOOT: every material source in one place. An entry returns rolls [kind, tier, count, chance?, up?]: count units with the
   given chance (1 if absent); up marks a rare upgrade roll, which the pity counter guarantees after LOOT_PITY misses. The previews on
   target cards are built from these same rolls, so what a card promises is what the fight pays. Old sources keep their v298 numbers. */
const LOOT_PITY = 15, ELITE_K = { force: 1.6, loot: 2, up: 3, res: 1.5 };
const fsTierL = (L, per) => clamp(1 + Math.floor(L / per), 1, 5);
const fsPT = () => clamp(1 + Math.floor(cmdLevel(score()) / 12), 1, 5); // the player's own tier, for mission and event rewards
const LOOT = {
  pirate: (L, el) => { const t = fsTierL(L, 8), k = el ? ELITE_K.loot : 1; return [["circuit", t, (1 + Math.floor(L / 5)) * k], ["alloy", t, (1 + Math.floor(L / 8)) * k], ["circuit", t + 1, 1, Math.min(1, .12 * (el ? ELITE_K.up : 1)), 1]]; },
  monster: (L, el) => { const t = fsTierL(L, 8), k = el ? ELITE_K.loot : 1; return [["bio", t, (1 + Math.floor(L / 8)) * k], ["void", t, k, .35], ["cube", t, 1, .08], ["bio", t + 1, 1, Math.min(1, .1 * (el ? ELITE_K.up : 1)), 1]]; },
  cube: (L, rally) => { const t = clamp(1 + Math.floor(L / 7), 2, 5); return [["cube", t, 2 + Math.floor(L / 10) + (rally ? 1 : 0)], ["void", t, 1], ["void", t, 1, rally ? .5 : .25], ["cube", t + 1, 1, .1, 1]]; },
  gather: (L, amt, res) => { const t = fsTierL(L, 8), m = res === "c" || res === "g" ? "crystal" : "alloy"; return [[m, t, clamp(Math.ceil(amt / 60000), 1, 6)], [m, t + 1, 1, .12, 1]]; },
  salvage: amt => [["alloy", clamp(1 + Math.floor(Math.log10(1 + amt) - 4), 1, 3), 1, .25]],
  pod: () => [["alloy", 1, 1, .175], ["crystal", 1, 1, .175]],
  hive: L => { const t = clamp(1 + Math.floor(L / 6), 1, 4); return [["alloy", t, 1], ["crystal", t, L >= 5 ? 1 : 0], ["bio", t, 1, .25]]; },       // v338: the Hive is biological
  hiveDef: L => { const t = clamp(1 + Math.floor(L / 6), 1, 4); return [["alloy", t, 1], ["bio", t, 1, .4]]; },                                     // v338: a raid beaten off
  pyramid: L => { const t = fsTierL(L * 3, 8); return [["crystal", t, 1 + Math.floor(L / 4)], ["circuit", t, 1, .3], ["void", t, 1, .12, 1]]; },     // v338: ancient vaults
  first: (kind, L) => { const t = Math.min(6, (kind === "cube" ? clamp(1 + Math.floor(L / 7), 2, 5) : fsTierL(L, 8)) + 1), m = kind === "cube" ? "cube" : kind === "mon" ? "bio" : "circuit"; return [[m, t, 2], ["void", t - 1, 1]]; },
  daily: () => [["low", fsPT(), 1]],
  dailyBonus: () => [["low", fsPT(), 2], ["void", fsPT(), 1, .3]],
  weekly: () => [["low", fsPT(), 3]],
  weeklyBonus: () => [["void", fsPT(), 1], ["cube", fsPT(), 1], ["low", Math.min(6, fsPT() + 1), 1]]
};
/* "low": whichever material you hold the fewest of at that tier, so mission rewards fill gaps instead of piling onto what you have */
const fsLowKind = t => { const f = fsOf(); return Object.keys(FS_MATS).reduce((a, k) => (f.mats[k + t] || 0) < (f.mats[a + t] || 0) ? k : a, "alloy"); };
function lootRoll(rolls) { const f = fsOf(); f.pity = f.pity && typeof f.pity === "object" ? f.pity : {}; const out = [];
  for (const [k0, t0, n, p, up] of rolls) { if (!(n > 0) || !(t0 >= 1)) continue; const k = k0 === "low" ? fsLowKind(clamp(t0, 1, 6)) : k0, t = clamp(t0, 1, 6); let ok = p == null || p >= 1 || Math.random() < p;
    if (up) { if (ok) f.pity[k] = 0; else if ((f.pity[k] = (f.pity[k] || 0) + 1) >= LOOT_PITY) { ok = true; f.pity[k] = 0; } }
    if (ok) out.push([k, t, n]); }
  return out; }
/* expected units per roll, for previews and the balance tests */
const lootEV = rolls => rolls.filter(r => r[2] > 0).map(([k, t, n, p]) => [k, clamp(t, 1, 6), n * (p == null ? 1 : p)]);
/* elites: about one pirate crew (Lv.10+) or monster in nine each week hits 60% harder and pays double, with triple the rare roll */
function weekNo() { return Math.floor((Date.now() - Date.UTC(2026, 0, 5)) / (7 * 864e5)); }
function isElite(x) { return !!x && !x.boss && !!(x.mon || x.lvl >= 10) && !trainingPir(x) && hash(x.id + ":" + weekNo()) % 9 === 0; }
const xLootK = x => x.boss ? "cube" : x.mon ? "mon" : "pir";
function fsLootPB(x, rally) { if (!x) return; const L = x.lvl || 1, el = isElite(x), kind = xLootK(x);
  fsXP((kind === "cube" ? 40 : kind === "mon" ? 20 : 10) * L * (el ? 1.5 : 1), x.name);
  fsDrop(lootRoll(kind === "cube" ? LOOT.cube(L, rally) : kind === "mon" ? LOOT.monster(L, el) : LOOT.pirate(L, el)), (el ? "Elite " : "") + x.name);
  S.fk = S.fk && typeof S.fk === "object" ? S.fk : {}; const fk = kind + ":" + L; /* v338: the first win at each level of each kind pays a bonus once */
  if (!S.fk[fk]) { S.fk[fk] = 1; S.shards = (S.shards || 0) + 2; fsDrop(lootRoll(LOOT.first(kind, L)), `first ${kind === "cube" ? "Cube" : kind === "mon" ? "monster" : "pirate"} kill at Lv.${L} (+◆2)`, { nocap: 1 }); } }
function fsLootGather(n, amt) { if (!n || !(amt > 0)) return; fsXP(Math.min(200, amt / 5000), "gathering"); fsDrop(lootRoll(LOOT.gather(n.lvl || 1, amt, n.res)), n.name); }
function fsLootSalvage(amt) { if (!(amt > 0)) return; fsDrop(lootRoll(LOOT.salvage(amt)), "salvage"); }
'''
t = t[:i] + NEW + t[j:]

# ---- fsDrop: quest-type rewards skip the daily farming cap, and it returns what was granted ----
rep('''function fsDrop(list, why) { if (!S) return; const f = fsOf(), d = utcDay(); if (!f.day || f.day.d !== d) f.day = { d, n: 0 }; const got = [];
  for (const [m, t, n] of list) for (let i = 0; i < n; i++) { if (f.day.n >= FS_DAY_CAP && Math.random() > Math.pow(.5, 1 + (f.day.n - FS_DAY_CAP) / 15)) continue; const k = fsMatKey(m, t); f.mats[k] = (f.mats[k] || 0) + 1; f.day.n++; got.push(k); }
  if (!got.length) return; fsBump();''',
'''function fsDrop(list, why, opt) { if (!S) return {}; const f = fsOf(), d = utcDay(); if (!f.day || f.day.d !== d) f.day = { d, n: 0 }; const got = [], nocap = opt && opt.nocap;
  for (const [m, t, n] of list) for (let i = 0; i < n; i++) { if (!nocap && f.day.n >= FS_DAY_CAP && Math.random() > Math.pow(.5, 1 + (f.day.n - FS_DAY_CAP) / 15)) continue; const k = fsMatKey(m, t); f.mats[k] = (f.mats[k] || 0) + 1; if (!nocap) f.day.n++; got.push(k); }
  if (!got.length) return {}; fsBump();''')
rep('''note(`Flagship materials${why ? ` from ${why}` : ""}: ${Object.entries(c).map(([k, n]) => `${FS_TIER[+k.slice(-1)][0]} ${FS_MATS[k.slice(0, -1)][0]} ×${n}`).join(", ")}.`, "win"); }''',
'''note(`Flagship materials${why ? ` from ${why}` : ""}: ${Object.entries(c).map(([k, n]) => `${FS_TIER[+k.slice(-1)][0]} ${FS_MATS[k.slice(0, -1)][0]} ×${n}`).join(", ")}.`, "win"); return c; }''')

# ---- old inline drops now go through the table ----
rep('''  if (Math.random() < .35) fsDrop([[Math.random() < .5 ? "alloy" : "crystal", 1, 1]], "a salvage pod"); // v299''',
    '''  fsDrop(lootRoll(LOOT.pod()), "a salvage pod"); // v299; v338: from the LOOT table''')
rep('''fsDrop([["alloy", clamp(1 + Math.floor(p.lvl / 6), 1, 4), 1], ["crystal", clamp(1 + Math.floor(p.lvl / 6), 1, 4), p.lvl >= 5 ? 1 : 0]], p.name); }''',
    '''fsDrop(lootRoll(LOOT.hive(p.lvl)), p.name); }''')
rep('''    if (res.winner === "d" && Math.random() < .25) { S.shards = (S.shards || 0) + 1; }''',
    '''    if (res.winner === "d" && Math.random() < .25) { S.shards = (S.shards || 0) + 1; }
    if (res.winner === "d") fsDrop(lootRoll(LOOT.hiveDef(lvl)), "the Hive raiders we beat off"); /* v338 */''')
rep('''  /* v79: pyramids no longer drop runes */''', '''  /* v79: pyramids no longer drop runes */ fsDrop(lootRoll(LOOT.pyramid(y.lvl)), y.name); /* v338: vault materials */''')

# ---- elites hit harder and pay more resources ----
rep('const xForce = x => trainingPir(x) ? { fighter: 1 } : x.mon ? monForce(x.mon, x.lvl) : pirateForce(x.lvl, x.boss);',
    'const xForce0 = x => trainingPir(x) ? { fighter: 1 } : x.mon ? monForce(x.mon, x.lvl) : pirateForce(x.lvl, x.boss);\nconst xForce = x => { const o = xForce0(x); try { if (isElite(x)) for (const k in o) o[k] = Math.max(1, Math.round(o[k] * 1.6)); } catch (e) {} return o; }; /* v338 elites: ELITE_K.force */')
rep('const xLoot = x => x.mon ? monLoot(x.lvl) : pirLoot(x.lvl, x.boss);',
    'const xLoot0 = x => x.mon ? monLoot(x.lvl) : pirLoot(x.lvl, x.boss);\nconst xLoot = x => { const o = xLoot0(x); try { return isElite(x) ? mul(o, 1.5) : o; } catch (e) { return o; } }; /* v338 elites: ELITE_K.res */')
rep('''title: x.mon ? `Hunt: ${x.name} (${MON[x.mon].n} Lv.${x.lvl})`''', '''title: x.mon ? `Hunt: ${isElite(x) ? "Elite " : ""}${x.name} (${MON[x.mon].n} Lv.${x.lvl})`''')
rep(''': `Raid on ${x.name} (Pirates Lv.${x.lvl})`''', ''': `Raid on ${isElite(x) ? "Elite " : ""}${x.name} (Pirates Lv.${x.lvl})`''')

# ---- quest-type grants can carry materials: rw.mats = [[kind|"low", tier, n, chance?]] ----
rep('''  if (rw.shards) S.shards = (S.shards || 0) + rw.shards; if (rw.boosts) S.boosts += rw.boosts; if (rw.item) giveItem(rw.item); if (rw.vip) vipAdd(rw.vip);
  logReward(src, res, { shards: rw.shards || 0, item: rw.item || null, boosts: rw.boosts || 0, kind: "quest" });''',
'''  if (rw.shards) S.shards = (S.shards || 0) + rw.shards; if (rw.boosts) S.boosts += rw.boosts; if (rw.item) giveItem(rw.item); if (rw.vip) vipAdd(rw.vip);
  if (rw.mats) fsDrop(lootRoll(typeof rw.mats === "function" ? rw.mats() : rw.mats), src, { nocap: 1 }); /* v338 */
  logReward(src, res, { shards: rw.shards || 0, item: rw.item || null, boosts: rw.boosts || 0, kind: "quest" });''')
rep('''rw.vip ? `<span class="rwi">VIP +${rw.vip}</span>` : ""].join(" ");''',
    '''rw.vip ? `<span class="rwi">VIP +${rw.vip}</span>` : "", rw.mats ? matsText(typeof rw.mats === "function" ? rw.mats() : rw.mats) : ""].join(" ");
/* v338: material rewards in a reward line ("2 × Rare material", "Epic Void Essence") */
const matsText = rolls => rolls.map(([k, tt, n, p]) => { const tn = FS_TIER[clamp(tt, 1, 6)]; return `<span class="rwi" style="color:${tn[1]}">${n > 1 ? n + " × " : ""}${tn[0]} ${k === "low" ? "material" : FS_MATS[k][0]}${p != null && p < 1 ? ` (${Math.round(p * 100)}%)` : ""}</span>`; }).join(" ");''')
rep('const SOLO_TIERS = [[300, { m: 30000, c: 18000, g: 6000, shards: 2 }], [1200, { boosts: 3, shards: 4 }], [4000, { shards: 10, item: "pAll_gold", vip: 200 }]];',
    'const SOLO_TIERS = [[300, { m: 30000, c: 18000, g: 6000, shards: 2 }], [1200, { boosts: 3, shards: 4, mats: () => [["low", fsPT(), 3]] }], [4000, { shards: 10, item: "pAll_gold", vip: 200, mats: () => [["void", fsPT(), 1], ["cube", fsPT(), 1]] }]]; /* v338: event tiers pay materials */')
rep('''const achRw = (key, t) => key === "glory" ? { shards: [3, 5, 8, 12, 20][t] || 20, vip: 100 * (t + 1) } : { m: 15000 * (t + 1) * (t + 1), c: 9000 * (t + 1) * (t + 1), g: 3000 * (t + 1) * (t + 1), shards: ACH_SHARD[t] || 8 };''',
    '''const achRw = (key, t) => key === "glory" ? { shards: [3, 5, 8, 12, 20][t] || 20, vip: 100 * (t + 1) } : { m: 15000 * (t + 1) * (t + 1), c: 9000 * (t + 1) * (t + 1), g: 3000 * (t + 1) * (t + 1), shards: ACH_SHARD[t] || 8, mats: [["low", Math.min(6, t + 1), 2]] }; /* v338: each achievement tier pays 2 materials of that rarity */''')

# ---- daily tasks pay a material; the daily bonus pays more ----
rep('''t.claimed = true; S.shards = (S.shards || 0) + 1; logReward("Daily task", r, { shards: 1, kind: "quest" });''',
    '''t.claimed = true; S.shards = (S.shards || 0) + 1; logReward("Daily task", r, { shards: 1, kind: "quest" }); fsDrop(lootRoll(LOOT.daily()), "a daily task", { nocap: 1 }); /* v338 */''')
rep('''S.daily.bonus = true; S.boosts++; S.shards = (S.shards || 0) + 3''', '''S.daily.bonus = true; S.boosts++; fsDrop(lootRoll(LOOT.dailyBonus()), "the daily bonus", { nocap: 1 }); S.shards = (S.shards || 0) + 3''')
open(p, 'w', encoding='utf-8').write(t); print('ok')
