# v444 elemental runes come only from super bosses (owner: "make runes only accessible for super boss fights not even normal cube
# fights, they should be rare and prestigious"). Collective Cube kills and joint strikes no longer drop runes. When a world boss falls
# its top three damage dealers (top five on the Pentarch) earn a rune, the top damage one more and the final blow one more (up to 3);
# each Elemental gives its own element (Ignis Fire, Glacius Water, Verdanth Earth, Voltaris Air, Solara Spirit). The Omega Cube keeps 2-5.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
# the rune rules
rep("""/* v270: runes are much rarer. A Cube core only sometimes holds one: a 15% chance at Lv.1, +1.5% per level up to 50%,
   +10% on a joint strike against a Lv.10+ Cube. A Lv.25+ core that holds runes holds 2 */
const runeChance = (lvl, rally) => Math.min(.5, .15 + .015 * ((lvl || 1) - 1)) + (rally && lvl >= 10 ? .1 : 0);
const cubeRunes = (lvl, rally) => Math.random() < runeChance(lvl, rally) ? (lvl >= 25 ? 2 : 1) : 0;""",
"""/* v444 runes are prestige: only super bosses hold them. When a world boss falls its top three damage dealers (five on the Pentarch)
   earn one, the top damage one more and the final blow one more; an Elemental gives its own element. The Omega Cube gives 2 to 5 */
const WB_RUNE_EL = { efi: "fire", eic: "water", ena: "earth", est: "air", eli: "spirit" };
function wbRunes(key, dm, last) { const D = WB[key]; if (!D || D.con != null) return 0; const i = Object.entries(dm || {}).sort((a, b) => b[1] - a[1]).map(x => x[0]).indexOf(G.me);
  return (i >= 0 && i < (key === "epx" ? 5 : 3) ? 1 : 0) + (i === 0 ? 1 : 0) + (last === G.me ? 1 : 0); }""")
rep("""function grantRunes(n, why) {
  if (n <= 0) return; S.runes = S.runes || {}; const ks = Object.keys(ELEM), got = [];
  for (let i = 0; i < n; i++) { const e = ks[(Math.random() * ks.length) | 0];""",
"""function grantRunes(n, why, el) {
  if (n <= 0) return; S.runes = S.runes || {}; const ks = Object.keys(ELEM), got = [];
  for (let i = 0; i < n; i++) { const e = ELEM[el] ? el : ks[(Math.random() * ks.length) | 0];""")
# Collective Cubes: no more runes
rep("runes: x.boss ? (rep.runes = cubeRunes(x.lvl)) : 0, kind:", "kind:")
rep("""    if (x.boss) { if (rep.runes) grantRunes(rep.runes, `${x.name} core`); else note(`${x.name}'s core held no runes this time.`); } // v79: elemental runes come only from Cube bosses
""", "")
rep("""  if (x.boss) { const n = cubeRunes(x.lvl, true); if (n) grantRunes(n, `${x.name} core (joint strike)`); else note(`${x.name}'s core held no runes this time.`); }
""", "")
# world bosses
rep("""    if (D.con == null) { const rn = cubeRunes(25); if (rn) grantRunes(rn, `${D.n} core`); }
    logReward(`Boss defeated · ${D.n}`, null, { shards: sh, item: it, kind: "battle" });""",
"""    const rn = wbRunes(key, dm, st.last[key]); if (rn) { grantRunes(rn, `${D.n} core`, WB_RUNE_EL[key]); extra += `, ${rn} ${WB_RUNE_EL[key] ? ELEM[WB_RUNE_EL[key]].n + " " : ""}rune${rn > 1 ? "s" : ""}`; }
    logReward(`Boss defeated · ${D.n}`, null, { shards: sh, item: it, runes: rn, kind: "battle" });""")
rep("""claims Void Shards and an item${D.con == null ? ", and the top damage dealer wins a Teleport Ticket" : ""}.""",
"""claims Void Shards and an item${D.con == null ? `, and the top damage dealer wins a Teleport Ticket. Its top ${key === "epx" ? "five" : "three"} damage dealers earn ${WB_RUNE_EL[key] ? `a ${ELEM[WB_RUNE_EL[key]].n} rune` : "an elemental rune"}, the top damage and the final blow one more each` : ""}.""")
# texts
rep("""Elemental runes are rare: they are torn from the cores of Collective Cubes. Only some Cube cores hold one: a ${Math.round(runeChance(1) * 100)}% chance at Lv.1, rising to ${Math.round(runeChance(30) * 100)}% at Lv.25+, where a lucky core holds 2. A joint strike on a Lv.10+ Cube adds +10%. The Omega Cube""",
"""Elemental runes are rare and prestigious: only super bosses hold them. When a world boss falls, its top three damage dealers (top five on the Pentarch) earn a rune, the top damage one more and the final blow one more. Each Elemental gives its own element: Ignis Fire, Glacius Water, Verdanth Earth, Voltaris Air, Solara Spirit. The Omega Cube""")
rep('runeBuy: () => toast("Elemental runes now only come from destroying Collective Cubes.", "warn")', 'runeBuy: () => toast("Elemental runes only come from super bosses: the world bosses and the Omega Cube.", "warn")')
rep("They drop runes and the rarest forge materials.", "They drop the rarest forge materials.")
rep("They drop from Cube bosses and world bosses.", "Only super bosses drop them: the top damage dealers and the final blow on a world boss, and everyone who breaks the Omega Cube.")
rep("each gets the full shard, rune and ${x.mon", "each gets the full shard and ${x.mon")
rep("everyone gets the full shard, rune and item rewards", "everyone gets the full shard and item rewards")
assert "cubeRunes" not in s and "runeChance" not in s
s, k = re.subn(r"GAME_V = 443\b", "GAME_V = 444", s); assert k == 1
open(P, 'w').write(s)
