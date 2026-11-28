"""v853: planet skin tiers, and Dragon Scale leaves Premium Tier 2 for the shop's Mythic tier, The Watcher taking its place (owner:
"twilight amethyst, iron colossus, inferno core, and dread skull to mythic also move dragon scale to mythic and replace it with another
please, spiked aegis, magma core, and stone titan to legendary please")."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 852;", "const GAME_V = 853;")
rep('["spire sapphire ember forge pearl saturn lattice clockwork countdown magma bonemoon abyssreef cntdebris mimichive signal"],',
    '["sapphire ember forge pearl saturn lattice clockwork countdown abyssreef cntdebris mimichive signal"],')
rep('["dread warsphere cyber colossus amethyst aurum inferno watcher bloom nigiri"], ["glacier thunder garden emerald hellgate"]]',
    '["warsphere cyber aurum bloom nigiri spire magma bonemoon"], ["glacier thunder garden emerald hellgate dread colossus amethyst inferno dragon"]]')
# Premium Tier 2: The Watcher (a cracked ivory eye that turns with its world) for Dragon Scale. Anyone at Tier 2 or above keeps the Dragon.
rep("function pxPremKeep(k) {", '''{ const P = PREM[2], s = PXS.watcher, o = PXS.dragon; if (P && s && o && P.k === "dragon") { delete o.prem; o.cost = 1; o.r = "all"; s.prem = 2; s.cost = 0; s.r = "all"; s.b = +(.12 + .012 * 2).toFixed(3); P.k = "watcher"; P.n = s.n; P.col = s.glow || P.col; PREM_OLD.dragon = 2; } } /* v853 */
function pxPremKeep(k) {''')
rep("if (!S.pxPKV) { try {", "if (S.pxPKV !== 2) { try {")
rep("S.pxPK = Object.assign({}, S.pxPK, K); S.pxPKV = 1; dirty();", "S.pxPK = Object.assign({}, S.pxPK, K); S.pxPKV = 2; dirty();")
open(p, "w", encoding="utf-8").write(s); print("ok")
