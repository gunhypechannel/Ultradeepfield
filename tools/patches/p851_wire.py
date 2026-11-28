"""v851: Recyclers at your home world can clear the debris over it; planet skin tiers (owner)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 850;", "const GAME_V = 851;")
# owner: "why cant i recycle my homeplanet from my homeplanet ships? only shows colony worlds ships". recPlan skipped the world the field
# hangs over, so a field over your home could only be cleared from a colony. Now that world's own Recyclers count (and go first: they are nearest).
rep(".filter(w => w.have > 0 && w.p.id !== tg.id).map(w =>", ".filter(w => w.have > 0).map(w =>")
rep("No Recyclers on your other worlds. This field needs", "No Recyclers on any of your worlds. This field needs")
# owner: "frost fire planet skin needs to be taken out of mythic category because its already in another, also need to move planet skins
# void emperor, tidal lock, rust bolt and golden hive to rare and stone titan to epic or mythic, petrified star, ruin of vaelthar, sphinx
# sands, and singularity to rare". The old premium Frostfire (pr3) leaves the shop (kept by anyone who owns it; the Common Frostfire stays).
rep('''  ["atoll singular obsidian eden mirror hive tidal rust reef pr1 pr2 pr4 pr6 pr8 aeon ruin sphinx petrified omen"],
  ["venom bonemoon ruby phoenix solar"], ["spire sapphire ember forge pearl saturn lattice clockwork countdown magma"],''',
    '''  ["atoll obsidian eden mirror reef pr1 pr2 pr4 pr6 aeon omen"],
  ["venom ruby phoenix solar pr8 tidal rust hive petrified ruin sphinx singular"], ["spire sapphire ember forge pearl saturn lattice clockwork countdown magma bonemoon"],''')
rep('["glacier shatter thunder garden emerald hellgate abyssreef cntdebris mimichive signal pr3"]', '["glacier shatter thunder garden emerald hellgate abyssreef cntdebris mimichive signal"]')
rep("function pxPrice() { if (pxPrice.done) return; pxPrice.done = 1;", "function pxPrice() { if (pxPrice.done) return; pxPrice.done = 1; if (PXS.pr3) PXS.pr3.retired = 1; /* v851 a second Frostfire */")
open(p, "w", encoding="utf-8").write(s); print("ok")
