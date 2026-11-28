"""v841: the owner's ten Common planets, every other shop planet graded by uniqueness; six premium planets replaced by the most unique
shop worlds; the last six premium tiers given themed sets (every gold-jewel world, matched to that tier's hull colours); nothing a
player already has is taken away."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 840;", "const GAME_V = 841;")
# hull colours re-paired with the top tiers' themes (still the last five tiers, two each, the rest at the top)
rep("Object.entries({ copper: 12, silver: 12, cobalt: 13, gold: 13, pink: 14, amethyst: 14, diamond: 15, ruby: 15, emerald: 16, obsidian: 16, glyph: 16 })",
    "Object.entries({ ruby: 12, copper: 12, gold: 13, silver: 13, emerald: 14, amethyst: 14, pink: 15, cobalt: 15, diamond: 16, obsidian: 16, glyph: 16 })")
rep("for (const k in PX_IMG) if (PXS[k]) { PXS[k].img = 1; if (PX_IMG[k]) { PXS[k].n = PX_IMG[k][0]; PXS[k].d = PX_IMG[k][1]; } }", '''for (const k in PX_IMG) if (PXS[k]) { PXS[k].img = 1; if (PX_IMG[k]) { PXS[k].n = PX_IMG[k][0]; PXS[k].d = PX_IMG[k][1]; } }
/* ---------- v841 the premium worlds reshuffled (owner: "Replace aurora veil, frost fire, and celestial tide Molton core, nebula heart, void
   emperor out of premium planet skin zone and replace them with a more unique replacement from of the other tiers like upgrade its status
   and create a better premium planet combination for the last 6 levels"). Six tiers take the most unique shop worlds instead; the worlds
   they replace go to the shop (the premium Frostfire is retired: the shop has its own). The gold-jewel worlds all move up to tiers 11-16,
   each with the hull colours of its tier. Whatever a player could already use stays theirs (pxPremKeep). ---------- */
const PREM_OLD = {}; for (const k in PXS) if (PXS[k].prem) PREM_OLD[k] = PXS[k].prem;
for (const [t, k] of [[1, "cosmicegg"], [2, "dragon"], [3, "voidbloom"], [4, "metropolis"], [6, "magnetar"], [8, "blacksun"]]) { const P = PREM[t], old = P.k, s = PXS[k], o = PXS[old]; if (!s || !o) continue;
  delete o.prem; o.cost = 1; o.r = "all"; if (old === "pr3") o.retired = 1; s.prem = t; s.cost = 0; s.r = "all"; s.b = +(.12 + .012 * t).toFixed(3); P.k = k; P.n = s.n; P.col = s.glow || P.col; }
for (const [k, t] of Object.entries({ ps8: 11, ps12: 11, ps2: 12, ps10: 12, ps6: 12, ps14: 12, ps1: 13, ps9: 13, ps7: 14, ps15: 14, ps16: 14, ps5: 15, ps13: 15, ps3: 15, ps11: 15, ps4: 16, ps17: 16 })) if (PXS[k]) { PXS[k].prem = t; PXS[k].b = +(.12 + .012 * t).toFixed(3); }
/* the shop's six levels, by how unique each world is (owner: "Common planet skins are: aurora glacier, crimson dune, lava lamp, abyssal ocean,
   plague world, ancient ruins, kraken deep, storm titan, frost fire, spectral ghost, move the rest out and scale them") */
const PX_BAND_OF = {}; [["aurora dune lavalamp abyss plague ruins kraken stormtitan frostfire ghost"], ["warsphere rust bonemoon dread spire colossus thunder tidal reef glacier nigiri watcher"],
  ["ruby sapphire emerald amethyst garden clockwork cyber venom bloom shatter ember obsidian pr1 pr2"], ["atoll aurum inferno magma forge pearl eden mirror lattice phoenix hive hellgate saturn singular pr4"],
  ["solar pr6 pr8"], ["aeon ruin sphinx petrified omen countdown signal abyssreef cntdebris mimichive pr3"]].forEach(([l], i) => l.split(" ").forEach(k => PX_BAND_OF[k] = i));
function pxPremKeep(k) { if (!S) return false; if (!S.pxPKV) { try { const t0 = premT(), K = {}; for (const q in PREM_OLD) if (t0 >= PREM_OLD[q]) K[q] = 1; if (typeof myPlanets === "function") for (const p of myPlanets()) if (p && p.px) K[p.px] = 1; S.pxPK = Object.assign({}, S.pxPK, K); S.pxPKV = 1; dirty(); } catch (e) {} } return !!(S.pxPK || {})[k]; }''')
rep("const pxOwned = k => PXS[k] && PXS[k].prem ? premT() >= PXS[k].prem : !!(FREE_SKINS || (S && S.pxOwn || {})[k] || pxKeep(k));",
    "const pxOwned = k => PXS[k] && PXS[k].prem ? !!(premT() >= PXS[k].prem || (S && S.pxOwn || {})[k] || pxPremKeep(k)) : !!(FREE_SKINS || (S && S.pxOwn || {})[k] || pxKeep(k) || pxPremKeep(k));")
rep("function pxBandOf(c, k) { return PX_MYTHIC.has(k) ||", "function pxBandOf(c, k) { if (PX_BAND_OF[k] != null) return PX_BAND_OF[k]; return PX_MYTHIC.has(k) ||")
rep("shop = E.filter(([, s]) => !s.prem)", "shop = E.filter(([k, s]) => !s.prem && !(s.retired && !pxOwned(k)))")
open(p, "w", encoding="utf-8").write(s); print("ok")
