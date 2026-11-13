# v525 the Void Shop remastered (owner: "what's missing?" ... "Yes to all"). See p525_shop.js: a free daily gift, inventory by the
# header, glowing active-boost bars, the deal of the day (35% off, a new item each UTC day), "For you" picks, one swipeable tab
# strip, one card per item with tier chips, painted art, value badges and savings, and flying shards when you buy.
import sys, re, os
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
J = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p525_shop.js'), encoding='utf-8').read().split('//@@SHOP\n')[1]
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
i = s.index('function shShop() {'); j = s.index('/* drifting salvage: glowing pods', i)
s = s[:i] + J + s[j:]
rep('toast(`${s.n} added to your inventory.`, "win"); }),', 'toast(`${s.n} added to your inventory.`, "win"); shopFx(d.k, s.cost); }),')
rep('  shopCat: d => { if (sheet && sheet.type === "shop") { sheet.cat = d.v; renderSheet(); } },', '''  shopCat: d => { if (sheet && sheet.type === "shop") { sheet.cat = d.v; renderSheet(); } },
  shopTier: d => { G.shopSel = G.shopSel || {}; G.shopSel[d.g] = +d.i; if (sheet && sheet.type === "shop") renderSheet(); }, /* v525 */
  shopFree: () => act(() => { if ((S.shopFree || "") === shopDay()) return; S.shopFree = shopDay(); const r = Math.random(); let msg;
    if (r < .4) { const n = 1 + (Math.random() < .35 ? 1 : 0); S.shards = (S.shards || 0) + n; msg = `◆${n} Void Shard${n > 1 ? "s" : ""}`; } else if (r < .7) { giveItem("boost5"); msg = SHOP.boost5.n; } else { const k = ["crateM", "crateC", "crateG"][(Math.random() * 3) | 0]; giveItem(k); msg = SHOP[k].n; }
    toast(`Free daily gift: ${msg}. Come back tomorrow for another.`, "win"); }),
  buyDeal: () => act(() => { const D = shopDeal(); if (!D || D.bought) return; if ((S.shards || 0) < D.cost) return toast(`That costs ◆${D.cost}.`, "warn"); S.shards -= D.cost; S.dealDay = shopDay(); giveItem(D.k); bump("shopBuys"); vipAdd(D.cost * 10); toast(`Deal of the day: ${D.s.n} added to your inventory.`, "win"); shopFx(D.k, D.cost); }),''')
css = '''
/* v525 the Void Shop */
.shead{display:flex;gap:8px;flex-wrap:wrap;flex-shrink:0}.shead .btn.on{border-color:var(--cyan);color:var(--cyan)}
.sbars{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:6px;flex-shrink:0}
.sbar{position:relative;overflow:hidden;display:flex;justify-content:space-between;gap:6px;padding:6px 9px;border-radius:9px;border:1px solid rgba(85,214,232,.4);background:rgba(8,20,30,.85);font-size:12px}
.sbar i{position:absolute;inset:0 auto 0 0;background:linear-gradient(90deg,rgba(85,214,232,.28),rgba(85,214,232,.08));box-shadow:inset -2px 0 8px rgba(85,214,232,.5);pointer-events:none}
.sbar b,.sbar span{position:relative;white-space:nowrap}.sbar span{color:var(--cyan);font-variant-numeric:tabular-nums}.sbar.cls{border-color:rgba(255,207,90,.45)}.sbar.cls i{background:linear-gradient(90deg,rgba(255,207,90,.2),rgba(255,207,90,.05))}
.sdeal{position:relative;flex-shrink:0;display:grid;grid-template-columns:96px minmax(0,1fr) auto;gap:10px;align-items:center;padding:10px;border-radius:14px;overflow:hidden;border:1px solid color-mix(in srgb,var(--tc) 70%,transparent);background:linear-gradient(120deg,color-mix(in srgb,var(--tc) 22%,#081420),#06101a 70%);box-shadow:0 0 18px color-mix(in srgb,var(--tc) 30%,transparent)}
.sdeal::after{content:"";position:absolute;inset:0;background:linear-gradient(100deg,transparent 30%,rgba(255,255,255,.12) 45%,transparent 60%);transform:translateX(-100%);animation:sdsh 4.5s ease-in-out infinite;pointer-events:none}@keyframes sdsh{60%,100%{transform:translateX(100%)}}
.sdart{width:96px;height:76px;border-radius:10px;background:center/cover no-repeat;box-shadow:0 0 0 1px rgba(255,255,255,.12)}
.sdtx{display:flex;flex-direction:column;gap:2px;min-width:0}.sdtx small{font-size:10.5px;letter-spacing:.12em;color:var(--tc)}.sdtx small b{color:#fff;letter-spacing:0}.sdtx>b{font-size:15px}.sdtx span{font-size:12px;color:var(--muted);line-height:1.3}
.sdbuy{display:flex;flex-direction:column;align-items:center;gap:4px}.sdbuy s{font-size:12px;color:var(--muted)}.sdbuy em{font-style:normal;font-weight:800;font-size:11px;color:#06101a;background:var(--tc);border-radius:6px;padding:1px 6px}
@media (max-width:420px){.sdeal{grid-template-columns:70px minmax(0,1fr) auto}.sdart{width:70px;height:60px}}
.shopstrip{display:flex;gap:6px;overflow-x:auto;flex-shrink:0;padding:2px 0 6px;scrollbar-width:none;-webkit-overflow-scrolling:touch}.shopstrip::-webkit-scrollbar{display:none}
.shopstrip button{flex:0 0 auto;display:flex;flex-direction:column;align-items:center;gap:2px;min-width:74px;padding:7px 10px;border-radius:12px;border:1px solid var(--line);background:rgba(8,18,28,.8);color:var(--muted);font-size:11.5px}
.shopstrip button i{font-style:normal;font-size:18px;color:var(--fg)}.shopstrip button.on{border-color:var(--cyan);color:var(--cyan);background:rgba(85,214,232,.12);box-shadow:0 0 12px rgba(85,214,232,.25)}.shopstrip button.on i{color:var(--cyan)}
.sfy{display:flex;flex-direction:column;gap:6px;flex-shrink:0}.sfyc{display:grid;grid-template-columns:48px minmax(0,1fr) auto;gap:10px;align-items:center;padding:7px 9px;border-radius:12px;border:1px solid color-mix(in srgb,var(--tc) 45%,transparent);background:linear-gradient(90deg,color-mix(in srgb,var(--tc) 14%,transparent),rgba(8,18,28,.9))}
.sfyc .sart{width:48px;height:48px}.sfyc small{display:block;font-size:11px;color:var(--cyan)}.sfyc b{font-size:13.5px}
.sgrid2{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:9px}
.scard{position:relative;display:grid;grid-template-columns:78px minmax(0,1fr);gap:10px;padding:10px;border-radius:14px;border:1px solid color-mix(in srgb,var(--tc) 45%,transparent);background:linear-gradient(150deg,color-mix(in srgb,var(--tc) 14%,transparent),rgba(8,18,28,.92) 60%)}
.scard.flash{animation:scfl .7s ease-out}@keyframes scfl{0%{box-shadow:0 0 0 2px var(--tc),0 0 26px var(--tc)}100%{box-shadow:0 0 0 0 transparent}}
.sart{display:grid;place-items:center;width:78px;height:78px;border-radius:12px;background:center/cover no-repeat;box-shadow:0 0 0 1px color-mix(in srgb,var(--tc,#55d6e8) 50%,transparent),0 4px 14px rgba(0,0,0,.4);font-size:30px}
.sart.g{background:radial-gradient(circle at 50% 40%,color-mix(in srgb,var(--tc) 40%,transparent),rgba(8,18,28,.9));color:var(--tc)}
.sbody{display:flex;flex-direction:column;gap:5px;min-width:0}.sbody>b{font-size:15px}.sbody small{font-size:12px;color:var(--muted);line-height:1.35}
.schips{display:flex;gap:4px;flex-wrap:wrap}.schips button{font-family:var(--f-display);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;padding:3px 7px;border-radius:6px;border:1px solid color-mix(in srgb,var(--cc) 55%,transparent);color:var(--cc);background:transparent}.schips button.on{background:var(--cc);color:#06101a;box-shadow:0 0 10px color-mix(in srgb,var(--cc) 60%,transparent)}
.sbadge{position:absolute;top:8px;right:8px;font-style:normal;font-size:10px;font-weight:800;letter-spacing:.06em;padding:2px 7px;border-radius:7px}.sbadge.best{background:#ffcf5a;color:#1a1000}.sbadge.pop{background:#c88aff;color:#14051f}.sbadge.sv{background:#5dff9a;color:#04170b}
.scard .sbuy{display:flex;justify-content:space-between;align-items:center;gap:8px}.scard .own a{color:var(--cyan);text-decoration:underline;cursor:pointer}
.sitem .sit .sart{width:54px;height:54px;font-size:22px}
.shfly{position:fixed;z-index:9999;pointer-events:none;color:#c88aff;font-style:normal;font-size:16px;text-shadow:0 0 8px #c88aff,0 0 2px #fff}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 524\b", "GAME_V = 525", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
