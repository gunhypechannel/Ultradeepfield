# U.D.F. premium packs (v338). One source of truth: this file writes packs.json (read by the game and seeded into Supabase
# table shop_packs) and packs_report.md (the value math). Prices are proposals, not approved prices. Purchases stay off.
import json, math
# Void Shard value of every item, from the Void Shop price (SHOP in docs/index.html). Boxes and loose materials are valued per
# Common-equivalent (5 of a rarity = 1 of the next) at the Common box rate: 5 Common for 4 shards = 0.8 shard each.
EQ = lambda t: 5 ** (t - 1)
SH_PER_EQ = 0.8
MB_N = [0, 5, 5, 3, 2, 1, 1]
V = {"boost": 1.6, "xb_bronze": 4, "xb_silver": 10, "xb_gold": 24, "xs_bronze": 4, "xs_silver": 10, "xs_gold": 24, "xr_bronze": 4, "xr_silver": 10, "xr_gold": 24,
     "pm_bronze": 5, "pm_silver": 15, "pm_gold": 36, "pc_gold": 36, "pg_gold": 36, "pAll_gold": 40, "repairKit": 6, "probe5": 5, "pirIntel": 8, "chart": 6, "teleport": 22,
     "vipPts500": 35, "vipAct7": 150, "vipAct30": 500, "o_commander_7": 15, "o_technocrat_7": 15, "o_admiral_7": 15, "o_admiral_30": 45, "o_staff_7": 60, "o_staff_30": 180,
     "bm_gold": 20, "bc_gold": 20, "bm_platinum": 32, "bc_platinum": 32, "f_silver": 45, "cl_general": 30}
for t in range(1, 7): V[f"mb{t}"] = round(MB_N[t] * EQ(t) * SH_PER_EQ)
def mat_v(k, t, n): return n * EQ(t) * SH_PER_EQ
PRICE = {"intro": 0.99, "starter": 4.99, "standard": 9.99, "advanced": 19.99, "premium": 49.99, "ultimate": 99.99}
TARGET_PER_USD = {"intro": 60, "starter": 72, "standard": 80, "advanced": 85, "premium": 90, "ultimate": 95}   # value climbs gently with size
FAM = {"starter": "Starter Commander Pack", "empire": "Empire Development Pack", "fleet": "Fleet Warfare Pack", "forge": "Flagship Forge Pack",
       "hunter": "Boss Hunter Pack", "legend": "Legendary Crafting Pack", "cube": "Cube Event Pack", "ultimate": "Ultimate Combination Pack"}
P = [
 ("starter_intro", "starter", "intro", "Starter Spark", 1, {"shards": 30, "items": {"boost": 10, "mb1": 1, "pm_bronze": 1, "xb_bronze": 1}}, "One per account. Your first week, faster."),
 ("starter_pack", "starter", "starter", "Starter Commander", 1, {"shards": 150, "items": {"boost": 20, "xb_silver": 2, "xr_silver": 2, "xs_silver": 1, "mb2": 2, "pAll_gold": 1, "vipPts500": 1, "repairKit": 1, "probe5": 1}}, "One per account. Speed-ups, supplies and a first Rare box."),
 ("empire_std", "empire", "standard", "Empire Development", 0, {"shards": 350, "items": {"pAll_gold": 3, "xb_gold": 4, "xr_gold": 3, "o_commander_7": 1, "o_technocrat_7": 1, "bm_gold": 1, "bc_gold": 1, "boost": 40, "pm_silver": 2}}, "Resources, construction and research speed."),
 ("empire_adv", "empire", "advanced", "Empire Development+", 0, {"shards": 700, "items": {"pAll_gold": 6, "xb_gold": 8, "xr_gold": 8, "xs_gold": 4, "o_staff_7": 1, "bm_platinum": 1, "bc_platinum": 1, "boost": 60, "f_silver": 1}}, "A week of command staff and serious speed."),
 ("fleet_std", "fleet", "standard", "Fleet Warfare", 0, {"shards": 350, "items": {"xs_gold": 8, "xs_silver": 6, "boost": 50, "repairKit": 5, "pirIntel": 2, "o_admiral_7": 1, "mb2": 2, "pg_gold": 1}}, "Ship production speed and fleet support."),
 ("fleet_adv", "fleet", "advanced", "Fleet Warfare+", 0, {"shards": 700, "items": {"xs_gold": 16, "boost": 100, "repairKit": 10, "pirIntel": 4, "o_admiral_30": 1, "cl_general": 1, "pg_gold": 3, "mb3": 2, "probe5": 5, "chart": 5}}, "A month of Admiral and the Warlord license."),
 ("forge_std", "forge", "standard", "Flagship Forge", 0, {"shards": 300, "items": {"mb2": 5, "mb3": 4, "mb4": 1}}, "Material Selection Boxes for your next gear tier."),
 ("forge_adv", "forge", "advanced", "Flagship Forge+", 0, {"shards": 600, "items": {"mb2": 4, "mb3": 8, "mb4": 3}}, "Rare and Epic boxes: pick exactly what the forge needs."),
 ("forge_prem", "forge", "premium", "Flagship Forge Elite", 0, {"shards": 1500, "items": {"mb3": 6, "mb4": 8, "mb5": 2, "boost": 45}}, "Epic and Legendary boxes."),
 ("hunter_std", "hunter", "standard", "Boss Hunter", 0, {"shards": 350, "items": {"repairKit": 8, "pirIntel": 4, "boost": 60, "xs_gold": 4, "mb2": 4, "mb3": 2}}, "Repairs, intel and speed for hunting."),
 ("hunter_adv", "hunter", "advanced", "Boss Hunter+", 0, {"shards": 700, "items": {"repairKit": 15, "pirIntel": 8, "boost": 120, "xs_gold": 8, "mb3": 6, "o_admiral_7": 1, "teleport": 1, "chart": 5, "probe5": 10}}, "Everything a hunting season needs."),
 ("legend_prem", "legend", "premium", "Legendary Crafting", 0, {"shards": 1400, "items": {"mb5": 4, "mb4": 4, "mb3": 5, "vipPts500": 1}}, "Late-game crafting: Legendary boxes."),
 ("cube_adv", "cube", "advanced", "Cube Event", 0, {"shards": 700, "mats": [["cube", 4, 4], ["void", 4, 2]], "items": {"repairKit": 10, "boost": 100, "xs_gold": 5, "pirIntel": 5}}, "Cube Fragments, Void Essence and repairs for Cube fights."),
 ("cube_prem", "cube", "premium", "Cube Event Elite", 0, {"shards": 1500, "mats": [["cube", 5, 3], ["void", 5, 1], ["cube", 4, 4]], "items": {"repairKit": 15, "boost": 200, "o_staff_7": 1, "xs_gold": 4}}, "Legendary Cube materials for the event."),
 ("ultimate", "ultimate", "ultimate", "Ultimate Combination", 0, {"shards": 3500, "items": {"mb6": 1, "mb5": 3, "mb4": 4, "o_staff_30": 1, "vipAct30": 1, "pAll_gold": 5, "xb_gold": 5, "xr_gold": 5, "xs_gold": 5}}, "The full set: a Mythic box, a month of VIP and the command staff."),
]
def value(c):
    v = c.get("shards", 0) + sum(V[k] * n for k, n in c.get("items", {}).items()) + sum(mat_v(*m) for m in c.get("mats", []))
    eq = sum(MB_N[int(k[2:])] * EQ(int(k[2:])) * n for k, n in c.get("items", {}).items() if k.startswith("mb")) + sum(EQ(t) * n for _, t, n in c.get("mats", []))
    return round(v), eq
# An active player's material income in Common-equivalents per day (from tools/econ_model.py, v338 sources). A pack's materials
# should stay under 14 days of that per $100: buying never skips more than about two weeks of an active player's crafting.
ACTIVE_EQ_DAY = None
try: ACTIVE_EQ_DAY = json.load(open("model_out.json"))["active"]["eq_day"]
except Exception: pass
rows, out = [], []
for pid, fam, tier, name, once, c, blurb in P:
    v, eq = value(c); price = PRICE[tier]; tgt = round(price * TARGET_PER_USD[tier])
    days = round(eq / ACTIVE_EQ_DAY, 1) if ACTIVE_EQ_DAY else None
    rows.append((pid, FAM[fam], name, tier, price, v, tgt, round(v / price), eq, days, once))
    out.append({"id": pid, "family": fam, "familyName": FAM[fam], "name": name, "tier": tier, "priceUsd": price, "oncePerAccount": bool(once), "testerEligible": True, "contents": c, "valueShards": v, "blurb": blurb,
                "store": {"play": f"udf_{pid}", "apple": f"udf.{pid}"}, "art": f"pack-{pid.replace('_', '-')}", "sort": len(out)})
json.dump(out, open("packs.json", "w"), indent=1)
with open("packs_report.md", "w") as f:
    f.write("| Pack | Family | Price | Value (◆) | Target (◆) | ◆ per $ | Materials (Common-eq) | Days of active income |\n|---|---|---|---|---|---|---|---|\n")
    for r in rows: f.write(f"| {r[2]} | {r[1]} | ${r[4]} | {r[5]} | {r[6]} | {r[7]} | {r[8]} | {r[9]} |\n")
for r in rows: print(f"{r[0]:14s} ${r[4]:6} value {r[5]:5} target {r[6]:5} ({r[5]/r[6]*100:4.0f}%)  {r[7]:3}/$  mats {r[8]:5} eq  {r[9]} days")
