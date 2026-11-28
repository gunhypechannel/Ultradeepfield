"""v838: planets priced in six levels and listed cheapest first under level headers, premium worlds after them by tier; no free
planets for the owner or in solo galaxies (owner: "no more free planets so i can make sure the pricing is right before production
status"); hull colours moved to the top premium tiers (11-16), with every colour a player already had kept."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 837;", "const GAME_V = 838;")
# no free planets: premium worlds come only with the tier, shop worlds only when bought (or already on one of your planets)
rep("const pxOwned = k => PXS[k] && PXS[k].prem ? !!(ownerFree() || premT() >= PXS[k].prem) : !!(FREE_SKINS || ownerFree() || (S && S.pxOwn || {})[k] || pxKeep(k));",
    "const pxOwned = k => PXS[k] && PXS[k].prem ? premT() >= PXS[k].prem : !!(FREE_SKINS || (S && S.pxOwn || {})[k] || pxKeep(k)); /* v838 no free planets, the owner included */")
rep("` : ownerFree() ? `<p class=\"note\" style=\"color:#8affb4\">Every premium skin is unlocked for you", "` : false ? `<p class=\"note\" style=\"color:#8affb4\">Every premium skin is unlocked for you")
# the price levels, and the list sorted by them
rep("function pxGrid(mode) {", '''/* v838 the price levels: every shop planet sits on one of six; the story worlds are Mythic */
const PX_BANDS = [[300, "Common", "#9fb3c8"], [600, "Uncommon", "#6fe08a"], [1000, "Rare", "#5fb8ff"], [1500, "Epic", "#c07aff"], [2200, "Legendary", "#ffb347"], [3000, "Mythic", "#ff5a7a"]];
const PX_MYTHIC = new Set(["aeon", "ruin", "sphinx", "petrified", "omen", "abyssreef", "cntdebris", "mimichive", "countdown", "signal"]);
function pxBandOf(c, k) { return PX_MYTHIC.has(k) || c >= 2400 ? 5 : c <= 400 ? 0 : c <= 800 ? 1 : c <= 1200 ? 2 : c <= 1600 ? 3 : 4; }
function pxPrice() { if (pxPrice.done) return; pxPrice.done = 1; for (const k in PXS) { const s = PXS[k]; if (s.prem || !s.cost) continue; s.band = pxBandOf(s.cost, k); s.cost = PX_BANDS[s.band][0]; } }
function pxSorted() { pxPrice(); const E = Object.entries(PXS), shop = E.filter(([, s]) => !s.prem).sort((a, b) => a[1].cost - b[1].cost || a[1].n.localeCompare(b[1].n)), prem = E.filter(([, s]) => s.prem).sort((a, b) => a[1].prem - b[1].prem || a[1].n.localeCompare(b[1].n)), out = []; let last = -1;
  for (const e of shop) { const bd = e[1].band != null ? e[1].band : 0; if (bd !== last) { last = bd; const [c, n, col] = PX_BANDS[bd]; out.push(["~h", `<div class="pxband" style="--bc:${col}"><b>${n}</b><small><span class="shard">◆</span>${fmt(c)} each</small></div>`]); } out.push(e); }
  if (prem.length) out.push(["~h", `<div class="pxband" style="--bc:#ffd25a"><b>Premium worlds</b><small>Unlocked by Premium tier</small></div>`]); return out.concat(prem); }
setTimeout(() => { try { pxPrice(); const st = document.createElement("style"); st.textContent = ".pxband{grid-column:1/-1;display:flex;align-items:baseline;gap:10px;margin:10px 2px 0;padding:6px 10px;border-radius:9px;border-left:3px solid var(--bc);background:linear-gradient(90deg,color-mix(in srgb,var(--bc) 22%,transparent),transparent)}.pxband b{font:800 13px/1.2 Oxanium,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--bc);text-shadow:0 0 10px var(--bc)}.pxband small{color:#cfe0ee}"; document.head.appendChild(st); } catch (e) {} }, 0);
function pxGrid(mode) {''')
rep('<div class="pxlist">${Object.entries(PXS).map(([k, s]) => { const o = pxOwned(k), on = sel === k;', '<div class="pxlist">${pxSorted().map(([k, s]) => { if (k === "~h") return s; const o = pxOwned(k), on = sel === k;')
# hull colours only at the top premium tiers; their matching gold worlds stay where they were
rep("const premSkinsAt = t => PS_SKINS.filter(([, f]) => HULL_F[f].t === t).map(x => x[2]);", '''const premSkinsAt = t => PS_SKINS.filter(([k]) => PXS[k] && PXS[k].prem === t).map(x => x[2]);
/* v838 hull colours only for the top premium tiers (owner: "I want the hull color upgrades to be only for the last premium player levels") */
const HULL_T0 = {}; for (const k in HULL_F) HULL_T0[k] = HULL_F[k].t;
Object.entries({ copper: 11, silver: 11, diamond: 11, cobalt: 12, ruby: 12, gold: 13, pink: 13, emerald: 14, amethyst: 14, obsidian: 15 }).forEach(([k, t]) => { if (HULL_F[k]) HULL_F[k].t = t; });
/* every colour a player could already use stays theirs: the tier they had when this first runs, and anything already painted on */
function hullKeep(f) { if (!S) return false; if (!S.hullKeepV) { try { const t0 = premT(), K = {}; for (const k in HULL_T0) if (HULL_T0[k] < 99 && t0 >= HULL_T0[k]) K[k] = 1; for (const v of Object.values(S.hullF || {})) if (v && HULL_T0[v]) K[v] = 1; S.hullKeep = Object.assign({}, S.hullKeep, K); S.hullKeepV = 1; dirty(); } catch (e) {} } return !!(S.hullKeep || {})[f]; }''')
rep("const hullOk = f => !!HULL_F[f] && (premT() >= HULL_F[f].t || !!G.owner ||", "const hullOk = f => !!HULL_F[f] && (premT() >= HULL_F[f].t || !!G.owner || hullKeep(f) ||")
open(p, "w", encoding="utf-8").write(s); print("ok")
