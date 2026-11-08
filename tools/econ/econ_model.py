# U.D.F. crafting and shard economy model (v338). Mirrors LOOT, lootRoll (with the pity counter), fsDrop's daily cap, fsRecipe and the
# shard sources in docs/index.html. Monte Carlo over 90 days for free (casual, active, hardcore) and paying players.
# Writes model_out.json (read by packs.py) and model_report.md. Run: python3 econ_model.py
import random, json, math
random.seed(338)
CAP, PITY = 70, 15
EQ = lambda t: 5 ** (t - 1)
def cl(v, a, b): return max(a, min(b, v))
def tierL(L, per=8): return cl(1 + L // per, 1, 5)
def pirate(L, el): t, k = tierL(L), (2 if el else 1); return [("circuit", t, (1 + L // 5) * k), ("alloy", t, (1 + L // 8) * k), ("circuit", t + 1, 1, min(1, .12 * (3 if el else 1)), 1)]
def monster(L, el): t, k = tierL(L), (2 if el else 1); return [("bio", t, (1 + L // 8) * k), ("void", t, k, .35), ("cube", t, 1, .08), ("bio", t + 1, 1, min(1, .1 * (3 if el else 1)), 1)]
def cube(L, rally): t = cl(1 + L // 7, 2, 5); return [("cube", t, 2 + L // 10 + (1 if rally else 0)), ("void", t, 1), ("void", t, 1, .5 if rally else .25), ("cube", t + 1, 1, .1, 1)]
def gather(L, amt, res): t = tierL(L); m = "crystal" if res in "cg" else "alloy"; return [(m, t, cl(math.ceil(amt / 60000), 1, 6)), (m, t + 1, 1, .12, 1)]
def hive(L): t = cl(1 + L // 6, 1, 4); return [("alloy", t, 1), ("crystal", t, 1 if L >= 5 else 0), ("bio", t, 1, .25)]
def pyramid(L): t = tierL(L * 3); return [("crystal", t, 1 + L // 4), ("circuit", t, 1, .3), ("void", t, 1, .12, 1)]
KINDS = ["alloy", "circuit", "crystal", "bio", "cube", "void"]
class Player:
    def __init__(s): s.m = {}; s.pity = {}; s.day_n = 0; s.shards = 0
    def low(s, t): return min(KINDS, key=lambda k: s.m.get((k, t), 0))
    def roll(s, rolls, nocap=False):
        for r in rolls:
            k, t, n = r[0], cl(r[1], 1, 6), r[2]; p = r[3] if len(r) > 3 else 1; up = len(r) > 4
            if n <= 0: continue
            if k == "low": k = s.low(t)
            ok = p >= 1 or random.random() < p
            if up:
                if ok: s.pity[k] = 0
                else:
                    s.pity[k] = s.pity.get(k, 0) + 1
                    if s.pity[k] >= PITY: ok, s.pity[k] = True, 0
            if not ok: continue
            for _ in range(n):
                if not nocap:
                    if s.day_n >= CAP and random.random() > .5 ** (1 + (s.day_n - CAP) / 15): continue
                    s.day_n += 1
                s.m[(k, t)] = s.m.get((k, t), 0) + 1
    def eq(s, k=None): return sum(v * EQ(t) for (kk, t), v in s.m.items() if k is None or kk == k)
# daily activity per profile: (activity, level, count per day). Elites are 1 in 9 at Lv.10+ for pirates and monsters.
PROF = {
 "casual":   dict(pir=(10, 6), mon=(10, 2), gath=(10, 4), cube=(11, 1 / 3), hive=(6, 2), pyr=(4, .5), daily=2, bonus=.5, weekly=2, event_tier=1, P=1),
 "active":   dict(pir=(15, 14), mon=(22, 6), gath=(20, 10), cube=(21, 1), hive=(12, 4), pyr=(8, 1), daily=3, bonus=1, weekly=3, event_tier=2, P=2),
 "hardcore": dict(pir=(15, 60), mon=(28, 30), gath=(28, 30), cube=(28, 4), hive=(20, 8), pyr=(10, 3), daily=3, bonus=1, weekly=3, event_tier=3, P=3)}
SHARDS = {"casual": 6, "active": 14, "hardcore": 24}   # shards a day from tasks, directives, logins, wins, pyramids (observed: a new account made 95 in its first day)
def cnt(x): return int(x) + (1 if random.random() < x % 1 else 0)
def day(pl, pr, dn):
    pl.day_n = 0; L, n = pr["pir"]
    for _ in range(cnt(n)): pl.roll(pirate(L, random.random() < 1 / 9 and L >= 10))
    L, n = pr["mon"]
    for _ in range(cnt(n)): pl.roll(monster(L, random.random() < 1 / 9))
    L, n = pr["gath"]
    for _ in range(cnt(n)): pl.roll(gather(L, 120000, random.choice("mcg")))
    L, n = pr["cube"]
    for _ in range(cnt(n)): pl.roll(cube(L, True))
    L, n = pr["hive"]
    for _ in range(cnt(n)): pl.roll(hive(L))
    L, n = pr["pyr"]
    for _ in range(cnt(n)): pl.roll(pyramid(L))
    P = pr["P"]
    for _ in range(pr["daily"]): pl.roll([("low", P, 1)], True)
    if random.random() < pr["bonus"]: pl.roll([("low", P, 2), ("void", P, 1, .3)], True)
    if pr["event_tier"] >= 2: pl.roll([("low", P, 3)], True)
    if pr["event_tier"] >= 3: pl.roll([("void", P, 1), ("cube", P, 1)], True)
    if dn % 7 == 6:
        for _ in range(pr["weekly"]): pl.roll([("low", P, 3)], True)
        if pr["weekly"] >= 3: pl.roll([("void", P, 1), ("cube", P, 1), ("low", min(6, P + 1), 1)], True)
    pl.shards += SHARDS[[k for k, v in PROF.items() if v is pr][0]]
SLOTS = {"weapon": ("circuit", "cube"), "shield": ("crystal", "cube"), "armor": ("alloy", "bio"), "reactor": ("crystal", "void"), "bridge": ("circuit", "bio"), "engine": ("alloy", "crystal"), "computer": ("circuit", "crystal"), "artifact": ("void", "cube")}
def need(t):
    o = {}
    for p, s in SLOTS.values(): o[p] = o.get(p, 0) + 3 * EQ(t); o[s] = o.get(s, 0) + 2 * EQ(t); o["alloy"] = o.get("alloy", 0) + 5 * EQ(max(1, t - 1))
    return o
packs = {p["id"]: p for p in json.load(open("packs.json"))} if __import__("os").path.exists("packs.json") else {}
MBN = [0, 5, 5, 3, 2, 1, 1]
def pack_eq(pid):  # selection boxes go to whatever the set needs most: spread evenly over kinds as an upper bound on usefulness
    c = packs[pid]["contents"]; e = sum(MBN[int(k[2:])] * EQ(int(k[2:])) * n for k, n in c.get("items", {}).items() if k.startswith("mb")) + sum(EQ(t) * n for _, t, n in c.get("mats", []))
    return e
PAYERS = {"free": [], "$10/month": [("forge_std", 30)], "$20/month": [("forge_adv", 30)], "$100/month": [("ultimate", 30)], "$250/month": [("ultimate", 30), ("forge_prem", 30), ("legend_prem", 30)]}
res, report = {}, []
for name, pr in PROF.items():
    runs = []
    for _ in range(40):
        pl = Player()
        for d in range(90): day(pl, pr, d)
        runs.append(pl)
    eq_day = sum(p.eq() for p in runs) / len(runs) / 90
    per = {k: sum(p.eq(k) for p in runs) / len(runs) / 90 for k in KINDS}
    res[name] = {"eq_day": round(eq_day), "per_kind": {k: round(v) for k, v in per.items()}, "shards_day": SHARDS[name]}
    for payer, buys in PAYERS.items():
        extra = sum(pack_eq(pid) / every for pid, every in buys) if packs else 0
        days = {}
        for t, nm in [(3, "Rare"), (4, "Epic"), (5, "Legendary"), (6, "Mythic")]:
            nd = need(t); tot = sum(nd.values())
            bott = max(nd, key=lambda k: nd[k] / max(1e-9, per[k] + extra / 6))   # box materials are picked, so they spread where needed
            days[nm] = round(nd[bott] / max(1e-9, per[bott] + extra / 6))
        res[name].setdefault("sets", {})[payer] = days
    report.append(name)
json.dump(res, open("model_out.json", "w"), indent=1)
with open("model_report.md", "w") as f:
    f.write("Days to forge a full 8-slot set, by player type and spending (90-day Monte Carlo, 40 runs each).\n\n| Player | Spend | Rare | Epic | Legendary | Mythic |\n|---|---|---|---|---|---|\n")
    for name in PROF:
        for payer, d in res[name]["sets"].items(): f.write(f"| {name} | {payer} | {d['Rare']} | {d['Epic']} | {d['Legendary']} | {d['Mythic']} |\n")
    f.write("\n| Player | Material income (Common-eq/day) | Shards/day |\n|---|---|---|\n")
    for name in PROF: f.write(f"| {name} | {res[name]['eq_day']} | {res[name]['shards_day']} |\n")
print(json.dumps({k: {"eq_day": v["eq_day"], "sets": v["sets"]} for k, v in res.items()}, indent=1))
