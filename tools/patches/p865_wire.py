"""v865: the welcome-back care package (owner: "what can we do to offer players thank you for comming back after a a break from the game?
longer the break the larger the reward ... i dont want to promote inactivity ... a really helpful carepackage for players who were off for
like 2 weeks or more", then "yes build all of the rest"). Away 14+ days: tier 1, 30+: tier 2, 60+: tier 3 (nothing grows past 60 days).
Resources are hours of the player's own output (12 / 24 / 36 h, with a floor), plus boosts, repair kits, shards from tier 2, and three
days of "Back in Action": +25% metal, crystal and gas, the Commander (builds 15% faster) and a Shipyard Surge (ships build 30% faster).
Once every 90 days per account; players still in the tutorial keep the older one-off gift."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 864;", "const GAME_V = 865;")
rep('geologist: "Geologist", technocrat: "Technocrat" }', 'geologist: "Geologist", technocrat: "Technocrat", rsurge: "Shipyard Surge" }')
rep("const uTime = c => acadT(Math.max(1, ((c.m || 0) + (c.c || 0)) * 1.44 * ECON_TK / (UNI * (1 + S.b.shipyard)) / Math.pow(2, S.b.nanite || 0)) * 1000);",
    "const uTime = c => acadT(Math.max(1, ((c.m || 0) + (c.c || 0)) * 1.44 * ECON_TK / (UNI * (1 + S.b.shipyard)) / Math.pow(2, S.b.nanite || 0) * (buffOn(\"rsurge\") ? .7 : 1)) * 1000); /* v865 the Shipyard Surge */")
rep("function comeback() {", r'''/* v865 the welcome-back care package: for a commander back after 14 days or more (the tiers stop growing at 60), once in 90 days */
const RET_LINE = "You're back, Commander. The galaxy kept moving, but so did we. Fleet Command sent this to get you on your feet.";
function retPack() { try { if (!S || !S.intro || tutOn() || !(G.awayMs >= 14 * DAY) || battle) return; const T = now(); S.retPk = S.retPk || {}; if (S.retPk.at && T - S.retPk.at < 90 * DAY) return;
    if (!S.b || !(S.b.metalMine >= 3)) return; // an empire to come back to
    const days = Math.floor(G.awayMs / DAY), tier = days >= 60 ? 3 : days >= 30 ? 2 : 1, H = [12, 24, 36][tier - 1], R = rates(), fl = [1, 2, 4][tier - 1];
    const rw = { m: Math.max(Math.round(R.m * H), 20000 * fl), c: Math.max(Math.round(R.c * H), 12000 * fl), g: Math.max(Math.round((R.g || 0) * H), 6000 * fl), boosts: [10, 20, 30][tier - 1], shards: [0, 5, 15][tier - 1] };
    S.retPk = { at: T, tier, days }; grantRw(rw, "Welcome back care package"); giveItem("repairKit", tier);
    S.buffs = S.buffs || {}; const D3 = T + 3 * DAY; for (const k of ["bm", "bc", "bg"]) { const c = buffOn(k); if (!c || (c.pct || 0) <= 25) S.buffs[k] = { pct: 25, until: Math.max(c ? c.until : 0, D3) }; }
    for (const k of ["commander", "rsurge"]) { const c = buffOn(k); S.buffs[k] = { pct: k === "rsurge" ? 30 : null, until: Math.max(c ? c.until : 0, D3) }; } dirty();
    const ev = (() => { try { const E = evNow(T); return E ? ` Live right now: ${E.n}.` : ""; } catch (e) { return ""; } })();
    celebrate({ k: "comeback", kick: `Welcome back, Commander · ${days} days away`, t: tier === 3 ? "Veteran's Care Package" : "Care Package", art: "adv",
      s: `Fleet Command sent a care package to get you rebuilding.${ev} For the next three days, Back in Action: +25% metal, crystal and gas, the Commander on staff (builds 15% faster) and a Shipyard Surge (ships build 30% faster).`,
      say: RET_LINE, rw: `${fmt(rw.m)} metal, ${fmt(rw.c)} crystal, ${fmt(rw.g)} gas, ⚡${rw.boosts} boosts, ${tier} Repair Kit${tier > 1 ? "s" : ""}${rw.shards ? ` and ◆${rw.shards}` : ""}. Already in your stores.`, go: "Let's rebuild" });
  } catch (e) {} }
function comeback() {''')
rep("    comeback(); if (G.oldWait) oldOffer();", "    comeback(); retPack(); /* v865 */ if (G.oldWait) oldOffer();")
open(p, "w", encoding="utf-8").write(s); print("ok")
