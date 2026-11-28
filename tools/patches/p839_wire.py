"""v839: planet prices ◆200-1,000 and each planet's bonus set by its level (owner: "the most unique planets to be worth more and give
the best bonuses and then the more basic planets to be the more common ones with lower stats ... price range of planets to be 200-1000
shards max, scale accordingly")."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 838;", "const GAME_V = 839;")
rep('const PX_BANDS = [[300, "Common", "#9fb3c8"], [600, "Uncommon", "#6fe08a"], [1000, "Rare", "#5fb8ff"], [1500, "Epic", "#c07aff"], [2200, "Legendary", "#ffb347"], [3000, "Mythic", "#ff5a7a"]];',
    '''/* [price, name, colour, bonus to one resource, bonus to all three] */
const PX_BANDS = [[200, "Common", "#9fb3c8", .04, .02], [300, "Uncommon", "#6fe08a", .06, .03], [450, "Rare", "#5fb8ff", .08, .04], [600, "Epic", "#c07aff", .10, .05], [800, "Legendary", "#ffb347", .12, .06], [1000, "Mythic", "#ff5a7a", .15, .08]];''')
rep("s.band = pxBandOf(s.cost, k); s.cost = PX_BANDS[s.band][0]; }", "s.band = pxBandOf(s.cost, k); const B = PX_BANDS[s.band]; s.cost = B[0]; s.b = s.r === \"all\" ? B[4] : B[3]; }")
rep('<small><span class="shard">◆</span>${fmt(c)} each</small></div>`]); }', '<small><span class="shard">◆</span>${fmt(c)} each · +${Math.round(PX_BANDS[bd][3] * 100)}% to one resource or +${Math.round(PX_BANDS[bd][4] * 100)}% to all</small></div>`]); }')
open(p, "w", encoding="utf-8").write(s); print("ok")
