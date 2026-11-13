//@@SHOP
/* v525 the Void Shop remastered (owner: "remaster this page to make it more interesting and engaging"):
   a free daily claim and the inventory by the header; active boosts as glowing bars that drain; the deal of the day (a different
   item every UTC day, 35% off, with a countdown); "For you" picks from what your empire needs right now; one swipeable strip of
   tabs; one card per item with Bronze-to-Platinum chips (price, effect and value change with the chip), the building or research
   painting as its art, Best value / Popular badges and the saving against Bronze; buying sends the shards flying and flashes it. */
const SHOP_ART = { bm: "metalMine", bc: "crystalMine", bg: "gasSynth", be: "solar", xb: "robotics", xs: "shipyard", xr: "lab", pm: "metalStore", pc: "crystalStore", pg: "gasTank", pAll: "logistics",
  f: "terraformer", mf: "lunarBase", o_commander: "command", o_admiral: "flagDock", o_engineer: "energyT", o_geologist: "crystalMine", o_technocrat: "computer", o_staff: "command",
  cl_collector: "robotics", cl_general: "dreadnought", cl_discoverer: "astro", crateM: "metalStore", crateC: "crystalStore", crateG: "gasTank", boost5: "impulse", probe5: "spyProbe", chart: "radar",
  repairKit: "repairYard", pirIntel: "espionage", teleport: "jumpGate", moonSeed: "lunarBase" };
const shopArtOf = k => { const b = k.replace(/_(bronze|silver|gold|platinum|7|30)$/, ""), a = SHOP_ART[b] || SHOP_ART[b.replace(/_[a-z]+$/, "")]; return a ? `art/${a}.webp` : null; };
const SHOP_UNITS = { boost: i => i + 1, accel: i => [.5, 2, 8][i], res: i => [6, 24, 72][i], planet: i => [4, 9, 15][i] };
const SHOP_CI = { packs: "◆", vip: "♛", boost: "⇑", accel: "⏩", res: "⬢", forge: "⚒", planet: "⬚", officer: "✪", class: "⚔", special: "✦", skins: "◐" };
const shopDay = () => utcDay(), shopDayEnd = () => { const d = new Date(); return Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate() + 1); };
function shopDeal() { const L = Object.keys(SHOP).filter(k => { const s = SHOP[k]; return s.cost >= 10 && s.tier != null && ["boost", "accel", "res", "officer", "planet"].includes(s.cat); }).sort(); if (!L.length) return null;
  const k = L[hash("deal" + shopDay()) % L.length], s = SHOP[k]; return { k, s, cost: Math.max(1, Math.ceil(s.cost * .65)), bought: (S.dealDay || "") === shopDay() }; }
function shopForYou() { const out = [], T = now(), pick = (q, left) => { const ms = [30 * 60e3, 2 * HOUR, 8 * HOUR], ks = ["bronze", "silver", "gold"]; let i = 0; for (let j = 0; j < 3; j++) if (ms[j] <= left) i = j; return `x${q}_${ks[i]}`; };
  if (S.bq && S.bq.e - T > 20 * 60e3) out.push([pick("b", S.bq.e - T), `Your construction has ${ftime(S.bq.e - T)} to go`]);
  if (S.sq && S.sq[0]) { const e = Math.max(...S.sq.map(h => sqEnd(h))); if (e - T > 20 * 60e3) out.push([pick("s", e - T), `The shipyard queue runs ${ftime(e - T)}`]); }
  if (S.rq && S.rq.e - T > 20 * 60e3) out.push([pick("r", S.rq.e - T), `Research finishes in ${ftime(S.rq.e - T)}`]);
  const lo = ["m", "c", "g"].sort((a, b) => (S.res[a] || 0) / Math.max(1, rates()[a] || 1) - (S.res[b] || 0) / Math.max(1, rates()[b] || 1))[0]; if (lo) out.push([`p${lo}_silver`, `${RES_N[lo]} is your scarcest resource`]);
  for (const r of ["m", "c", "g", "e"]) if (!buffOn("b" + r) && out.length < 4) { out.push([`b${r}_silver`, `No ${BUFF_N["b" + r].replace(" Booster", "").toLowerCase()} booster running`]); break; }
  return out.filter(([k]) => SHOP[k]).slice(0, 3); }
function shopFx(k, cost) { try { const b = document.querySelector(`[data-act="buy"][data-k="${k}"], [data-act="buyDeal"]`), h = document.querySelector("#sheet .hd .shard"); if (!b) return; const r = b.getBoundingClientRect(), t = h ? h.getBoundingClientRect() : { left: r.left, top: 40 };
    for (let i = 0; i < Math.min(8, 2 + (cost / 6 | 0)); i++) { const e = document.createElement("i"); e.className = "shfly"; e.textContent = "◆"; e.style.left = r.left + r.width / 2 + "px"; e.style.top = r.top + r.height / 2 + "px"; document.body.appendChild(e);
      const dx = t.left + 8 - (r.left + r.width / 2), dy = t.top + 10 - (r.top + r.height / 2); e.animate([{ transform: "translate(0,0) scale(1)", opacity: 1 }, { transform: `translate(${dx * .5 + (Math.random() - .5) * 80}px,${dy * .5 - 40}px) scale(1.3)`, opacity: 1, offset: .5 }, { transform: `translate(${dx}px,${dy}px) scale(.5)`, opacity: .2 }], { duration: 650 + i * 70, easing: "cubic-bezier(.3,.6,.4,1)" }).onfinish = () => e.remove(); }
    setTimeout(() => { const c = document.querySelector(`[data-card="${k}"]`); if (c) { c.classList.remove("flash"); void c.offsetWidth; c.classList.add("flash"); } }, 60); try { SFX && SFX.ui && SFX.ui("win"); } catch (e) {} } catch (e) {} }
function shShop() {
  if (sheet.cat === "packs" && !G.pkSeen) { G.pkSeen = 1; packsDeliver(); }
  const cat = sheet.cat = sheet.cat || (window.udfShop && G.mode === "online" ? "packs" : "boost"), it = S.items || {}, T = now(), inv = Object.keys(it).filter(k => it[k] > 0 && SHOP[k]), invN = inv.reduce((a, k) => a + it[k], 0), sh = S.shards || 0;
  const bars = Object.keys(BUFF_N).filter(k => buffOn(k)).map(k => { const u = buffs()[k].until, span = k[0] === "b" && k.length === 2 ? 7 * DAY : 30 * DAY; return `<div class="sbar"><i style="width:${Math.min(100, (u - T) / span * 100).toFixed(1)}%"></i><b>${esc(BUFF_N[k])}${buffPct(k) ? ` +${buffPct(k)}%` : ""}</b><span data-end="${u}">${ftime(u - T)}</span></div>`; })
    .concat(cmdClass() ? [`<div class="sbar cls"><i style="width:100%"></i><b>${esc(SHOP["cl_" + cmdClass()].n)}</b><span>Permanent</span></div>`] : []);
  const free = (S.shopFree || "") !== shopDay();
  const strip = `<div class="shopstrip" role="tablist">${[["packs", "Packs"]].concat(SHOP_CATS).concat([["skins", "Planet skins"]]).map(([k, l]) => `<button role="tab" aria-selected="${k === cat}" class="${k === cat ? "on" : ""}" data-act="shopCat" data-v="${k}"><i>${SHOP_CI[k] || "✦"}</i>${esc(l.replace(/^[♛◆]\s*/, ""))}</button>`).join("")}</div>`;
  const art = (k, s) => { const a = shopArtOf(k); return a ? `<span class="sart" style="background-image:url(${a})"></span>` : `<span class="sart g" style="--tc:${s.col || "#55d6e8"}">${s.ic.length === 1 && "mcg".includes(s.ic) ? RI[s.ic] : s.ic}</span>`; };
  const buyBtn = (k, s, c) => s.cost ? `<button class="btn amber sm" data-act="buy" data-k="${k}" ${sh >= (c || s.cost) ? "" : "disabled"}>◆${c || s.cost}</button>` : `<span class="note">Packs & events</span>`;
  const one = (k, s, extra) => `<div class="scard" data-card="${k}" style="--tc:${s.col || "#55d6e8"}">${art(k, s)}<div class="sbody"><b>${esc(s.n)}</b>${extra || ""}<small>${s.d()}</small><div class="sbuy">${it[k] ? `<span class="own">Owned ×${it[k]}${s.use ? ` · <a data-act="useItem" data-k="${k}">Use now</a>` : ""}</span>` : "<span></span>"}${buyBtn(k, s)}</div></div></div>`;
  const grouped = list => { const G2 = new Map(); for (const [k, s] of list) { const g = s.tier != null ? s.cat + "|" + s.n : k; if (!G2.has(g)) G2.set(g, []); G2.get(g).push([k, s]); }
    return [...G2.entries()].map(([g, L]) => { if (L.length < 2) return one(L[0][0], L[0][1]); L.sort((a, b) => a[1].tier - b[1].tier); const sel = clamp((G.shopSel || {})[g] != null ? G.shopSel[g] : Math.min(1, L.length - 1), 0, L.length - 1), [k, s] = L[sel], U = SHOP_UNITS[s.cat];
      let best = -1; if (U) { let bv = 0; L.forEach(([, x], i) => { const v = U(x.tier) / x.cost; if (v > bv * 1.001) { bv = v; best = i; } }); }
      const save = U && sel > 0 ? Math.round((1 - (s.cost / U(s.tier)) / (L[0][1].cost / U(L[0][1].tier))) * 100) : 0;
      const chips = `<div class="schips">${L.map(([, x], i) => `<button class="${i === sel ? "on" : ""}" style="--cc:${x.col}" data-act="shopTier" data-g="${esc(g)}" data-i="${i}">${/_(\d+)$/.test(L[i][0]) ? L[i][0].match(/_(\d+)$/)[1] + " days" : ITIERS[x.tier] ? ITIERS[x.tier][1] : x.tier}</button>`).join("")}</div>`;
      const badge = best === sel ? `<em class="sbadge best">Best value</em>` : sel === 1 && L.length > 2 ? `<em class="sbadge pop">Popular</em>` : save > 0 ? `<em class="sbadge sv">Save ${save}%</em>` : "";
      return one(k, s, chips + badge); }).join(""); };
  let body;
  if (cat === "packs") body = packsBody();
  else if (cat === "skins") body = `<p class="note">Premium looks for any world you hold. Buy once with Void Shards, then apply from Rename & reskin on the planet. Each adds a small production perk to the world wearing it.</p>${pxGrid("shop")}`;
  else if (cat === "inv") body = inv.length ? `<div class="shopgrid">${inv.map(k => { const s = SHOP[k]; return `<div class="sitem" style="--tc:${s.col || "#55d6e8"}"><div class="sit">${art(k, s)}${s.tier != null && ITIERS[s.tier] ? `<i class="tier">${ITIERS[s.tier][1]}</i>` : ""}</div><b>${esc(s.n)} ×${it[k]}</b><small>${s.d()}</small><div class="sbuy"><span></span>${s.use ? `<span class="useb">${it[k] > 1 && useAllOk(k) ? `<button class="btn ghost sm" data-act="useAll" data-k="${k}">Use all</button>` : ""}<button class="btn sm" data-act="useItem" data-k="${k}">Use</button></span>` : `<span class="own">${k === "probe5" ? "Used when you launch probes" : k === "teleport" ? "Use from an empty orbit" : "Use from a planet card"}</span>`}</div></div>`; }).join("")}</div>` : '<p class="note">Your inventory is empty. Items you buy, and spoils from pirate raids, land here.</p>';
  else if (cat === "vip") body = vipShopBody();
  else body = `<div class="sgrid2">${grouped(Object.entries(SHOP).filter(([, s]) => s.cat === cat))}</div>`;
  const D = shopDeal(), deal = D && cat !== "inv" ? `<div class="sdeal" style="--tc:${D.s.col || "#ffcf5a"}">${shopArtOf(D.k) ? `<span class="sdart" style="background-image:url(${shopArtOf(D.k)})"></span>` : ""}<div class="sdtx"><small>DEAL OF THE DAY · ends in <b data-end="${shopDayEnd()}">${ftime(shopDayEnd() - T)}</b></small><b>${esc(D.s.n)}${ITIERS[D.s.tier] ? ` · ${ITIERS[D.s.tier][1]}` : ""}</b><span>${D.s.d()}</span></div>
    <div class="sdbuy"><s>◆${D.s.cost}</s>${D.bought ? `<span class="pill ok">Bought today</span>` : `<button class="btn amber" data-act="buyDeal" ${sh >= D.cost ? "" : "disabled"}>◆${D.cost}</button>`}<em>−35%</em></div></div>` : "";
  const fy = ["boost", "accel", "res", "special"].includes(cat) ? shopForYou() : [], forYou = fy.length ? `<h3 class="viph">For you</h3><div class="sfy">${fy.map(([k, why]) => `<div class="sfyc" data-card="${k}" style="--tc:${SHOP[k].col || "#55d6e8"}">${art(k, SHOP[k])}<div><small>${esc(why)}</small><b>${esc(SHOP[k].n)}${ITIERS[SHOP[k].tier] ? ` · ${ITIERS[SHOP[k].tier][1]}` : ""}</b></div>${buyBtn(k, SHOP[k])}</div>`).join("")}</div>` : "";
  return `<div class="hd"><div><div class="chapter">Void Shop</div><h2><span class="shard">◆</span> ${fmt(sh)} Void Shards</h2></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
    <div class="shead"><button class="btn ${free ? "amber" : "ghost"} sm" data-act="shopFree" ${free ? "" : "disabled"}>${free ? "🎁 Free daily gift" : "✓ Gift claimed · back tomorrow"}</button><button class="btn ghost sm${cat === "inv" ? " on" : ""}" data-act="shopCat" data-v="inv">Inventory · ${invN}</button></div>
    ${bars.length ? `<div class="sbars">${bars.join("")}</div>` : ""}${deal}${strip}${forYou}${body}`;
}
