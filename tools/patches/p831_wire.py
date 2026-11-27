"""v831: the Star Hive in the neon of its painting (art/mon/m/swasp*.bin, tools/sculpt/mon3_sculpt.py; the nest's glowing haze now loads
in battle too), and Premium Points (p831_prem.js)."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 830;", "const GAME_V = 831;")
rep('"swasp_nest":{"s":1}', '"swasp_nest":{"s":1,"g":1}')
# points on purchase and refund; 10 a day for logging in
rep("S.premUsd = +((S.premUsd || 0) + +P.priceUsd).toFixed(2); /* v626 lifetime support */", "S.premUsd = +((S.premUsd || 0) + +P.priceUsd).toFixed(2); /* v626 lifetime support */ try { premOnBuy(g.id, +P.priceUsd); } catch (e) {} /* v831 */")
rep("S.premUsd = Math.max(0, +((S.premUsd || 0) - +P.priceUsd).toFixed(2));", "S.premUsd = Math.max(0, +((S.premUsd || 0) - +P.priceUsd).toFixed(2)); try { premOnRefund(g.id); } catch (e) {} /* v831 */")
rep('vipAdd(Math.min(7, ls.next) * 50, "daily login");', 'vipAdd(Math.min(7, ls.next) * 50, "daily login"); S.premPP = (S.premPP || 0) + 10; /* v831 Premium Points */')
# the Premium page in points
rep('''${nx ? `<p class="note" style="text-align:center">${usd > 0 ? `$${usd.toFixed(2)} so far · ` : ""}Tier ${t + 1} at $${nx.usd} lifetime support</p>` : `<p class="note" style="text-align:center;color:#ffd25a">The top tier. You have everything.</p>`}`;''',
    '''${premBar("prem")}`; /* v831 points, not dollars */''')
rep('''<small>${sel > 10 ? "BEYOND $1,000 · " : ""}TIER ${sel} · $${P.usd.toLocaleString("en-US")} lifetime</small>''', '''<small>TIER ${sel} · ${fmt(P.pts)} PREMIUM POINTS</small>''')
rep('''"Premium tiers come with real purchases once the store opens on Google Play: every purchase counts toward your lifetime support. Until then, the game's owner can give tiers."''',
    '''"Every $1 of purchases earns 100 Premium Points, double on your first purchase each week and during the Battle for the Cube and the Convergence. Logging in earns 10 a day, and every 1,000 points opens a Premium Cache. Until the store opens, the game's owner can give tiers."''')
rep('''<span class="pkp">$${Number(p.priceUsd).toFixed(2)}</span>''', '''<span class="pkp">$${Number(p.priceUsd).toFixed(2)}</span>${+p.priceUsd > 0 ? `<span class="pkpp">+${fmt(Math.round(+p.priceUsd * PP_USD))} PP</span>` : ""}''', 2)
js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "p831_prem.js"), encoding="utf-8").read()
rep("const PXC = {}; // id → { surf, emi, art }", js + "\nconst PXC = {}; // id → { surf, emi, art }")
open(p, "w", encoding="utf-8").write(s); print("ok")
