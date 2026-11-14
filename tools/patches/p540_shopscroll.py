# v540 the Void Shop as one long scroll of tiles (owner: "Make the item shop have tiles but also just scroll down and down until the end
# of shop"). Every section (Packs when the store is open, VIP, Boosters, Accelerators, Resources, Forge, Planet, Officers, Commander
# class, Special, Planet skins) now sits one after another on a single page, each under its own header; items are tiles (picture on
# top, name, tier chips, a short description, owned count and price), two or more to a row. The tab strip stays pinned at the top: a tap
# scrolls to that section, and it lights up the section you're reading as you scroll. Inventory stays its own page (the button by the
# header). Links that open a shop section (ACT.shopFuel and the like) land on it.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('''  const strip = `<div class="shopstrip" role="tablist">${[["packs", "Packs"]].concat(SHOP_CATS).concat([["skins", "Planet skins"]]).map(([k, l]) => `<button role="tab" aria-selected="${k === cat}" class="${k === cat ? "on" : ""}" data-act="shopCat" data-v="${k}"><i>${SHOP_CI[k] || "✦"}</i>${esc(l.replace(/^[♛◆]\\s*/, ""))}</button>`).join("")}</div>`;''',
    '''  const SECS = (window.udfShop && G.mode === "online" ? [["packs", "Packs"]] : []).concat(SHOP_CATS.filter(([k]) => k === "vip" || Object.values(SHOP).some(x => x.cat === k))).concat([["skins", "Planet skins"]]); /* v540 one long page */
  const strip = `<div class="shopstrip sticky" role="tablist">${SECS.map(([k, l]) => `<button role="tab" aria-selected="${k === cat}" class="${k === cat ? "on" : ""}" data-act="shopCat" data-v="${k}" data-sec="${k}"><i>${SHOP_CI[k] || "✦"}</i>${esc(l.replace(/^[♛◆]\\s*/, ""))}</button>`).join("")}</div>`;''')
rep('''  let body;
  if (cat === "packs") body = packsBody();''', '''  let body; const secBody = k => k === "packs" ? packsBody() : k === "skins" ? `<p class="note">Premium looks for any world you hold. Buy once with Void Shards, then apply from Rename & reskin on the planet. Each adds a small production perk to the world wearing it.</p>${pxGrid("shop")}` : k === "vip" ? vipShopBody() : `<div class="sgrid2 stiles">${grouped(Object.entries(SHOP).filter(([, s]) => s.cat === k))}</div>`;
  if (cat !== "inv") body = SECS.map(([k, l]) => `<section class="ssec" id="ssec-${k}" data-sec="${k}"><h3 class="ssech"><i>${SHOP_CI[k] || "✦"}</i>${esc(l.replace(/^[♛◆]\\s*/, ""))}</h3>${secBody(k)}</section>`).join("") + `<p class="note send">That's the whole shop. New items arrive with updates.</p>`;
  else if (cat === "packs") body = packsBody();''')
rep('  const fy = ["boost", "accel", "res", "special"].includes(cat) ? shopForYou() : [],', '  const fy = cat !== "inv" ? shopForYou() : [],')
rep('  shopCat: d => { if (sheet && sheet.type === "shop") { sheet.cat = d.v; renderSheet(); } },',
    '''  shopCat: d => { if (!(sheet && sheet.type === "shop")) return; const was = sheet.cat; sheet.cat = d.v; if (d.v === "inv" || was === "inv") { sheet.jump = d.v === "inv" ? null : d.v; renderSheet(); } else shopJump(d.v); }, /* v540 the strip scrolls the long page */''')
rep('function shShop() {', '''/* v540 the long shop: scroll to a section, and light up the section being read */
function shopJump(k, instant) { const el = document.getElementById("ssec-" + k); if (!el) return; const sc = shopScroller(el); if (!sc) return el.scrollIntoView({ block: "start" }); const strip = document.querySelector(".shopstrip.sticky"), off = strip ? strip.offsetHeight + 8 : 8;
  G.shopJ = performance.now(); sc.scrollTo({ top: sc.scrollTop + el.getBoundingClientRect().top - sc.getBoundingClientRect().top - off, behavior: instant ? "instant" : "smooth" }); shopLight(k); }
function shopScroller(el) { for (let p = el.parentElement; p; p = p.parentElement) { const cs = getComputedStyle(p); if (/(auto|scroll)/.test(cs.overflowY) && p.scrollHeight > p.clientHeight + 4) return p; } return null; }
function shopLight(k) { for (const b of document.querySelectorAll(".shopstrip.sticky button")) { const on = b.dataset.sec === k; b.classList.toggle("on", on); b.setAttribute("aria-selected", on); if (on && b.parentElement) { const st = b.parentElement, x = b.offsetLeft - st.clientWidth / 2 + b.offsetWidth / 2; st.scrollTo({ left: x, behavior: "smooth" }); } } if (sheet && sheet.type === "shop" && sheet.cat !== "inv") sheet.cat = k; }
function shopWire() { const first = document.querySelector(".ssec"); if (!first) return; const sc = shopScroller(first); if (!sc || sc._shopW) { if (sheet && sheet.jump) { const j = sheet.jump; sheet.jump = null; [30, 350, 800].forEach(d => setTimeout(() => shopJump(j, true), d)); } return; } sc._shopW = 1;
  sc.addEventListener("scroll", () => { if (performance.now() - (G.shopJ || 0) < 700) return; const top = sc.getBoundingClientRect().top + 90; let cur = null; for (const e of document.querySelectorAll(".ssec")) if (e.getBoundingClientRect().top <= top) cur = e.dataset.sec; if (cur && cur !== G.shopCur) { G.shopCur = cur; shopLight(cur); } }, { passive: true });
  if (sheet && sheet.jump) { const j = sheet.jump; sheet.jump = null; [30, 350, 800].forEach(d => setTimeout(() => shopJump(j, true), d)); } }
function shShop() { setTimeout(shopWire, 0);''')
# links into a section: opening the shop with a cat jumps to it
rep('  shopFuel: () => openSheet({ type: "shop", cat: "accel" }),', '  shopFuel: () => openSheet({ type: "shop", cat: "accel", jump: "accel" }),')
css = '''
/* v540 the long shop */
.shopstrip.sticky{position:sticky;top:-1px;z-index:5;margin:0 -2px;padding:6px 2px 8px;background:#08121c;box-shadow:0 -40px 0 0 #08121c,0 8px 12px -6px rgba(0,0,0,.7)}
.ssec{display:flex;flex-direction:column;gap:9px;scroll-margin-top:70px;margin-top:6px}
.ssech{display:flex;align-items:center;gap:8px;margin:8px 0 0;font:700 15px var(--f-display,sans-serif);letter-spacing:.1em;text-transform:uppercase;color:#e9f1f7}
.ssech i{font-style:normal;color:var(--cyan)}.ssech::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,rgba(85,214,232,.5),transparent)}
.stiles{grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px}
.stiles .scard{grid-template-columns:1fr;gap:6px;padding:8px;align-content:start}
.stiles .scard>.sart{width:100%;height:auto;aspect-ratio:4/3;font-size:38px;border-radius:10px}
.stiles .sbody{gap:4px;height:100%}.stiles .sbody>b{font-size:13.5px;line-height:1.2}
.stiles .sbody small{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;font-size:11.5px}
.stiles .schips button{font-size:8.5px;padding:2px 5px}
.stiles .sbuy{margin-top:auto;flex-wrap:wrap;gap:4px}.stiles .sbuy .btn{flex:1 0 auto}
.stiles .sbadge{top:12px;right:12px;font-size:9px}
.send{text-align:center;padding:14px 0 6px}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 539\b", "GAME_V = 540", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
