/* ---------- v831 Premium Points (owner: "some kind of addictive point system for void shard purchases so they use points to level up Premium
   player status ... how many points it would take", then "build it all"). Every $1 of purchases is 100 Premium Points (the tiers sit exactly
   where they were: tier 1 at 500, tier 16 at 750,000). On top: double points for the first purchase of each week and during the big events
   (the Battle for the Cube, the Convergence), 10 points for each daily login, and a Premium Cache (◆5) for every 1,000 points. A progress bar
   to the next tier sits on the Premium page, in the Void Shop and on the VIP page. Store prices stay in real money. ---------- */
const PP_USD = 100, PP_CACHE = 1000, PP_CACHE_RW = 5;
for (let t = 1; t <= PREM_TOP; t++) PREM[t].pts = PREM[t].usd * PP_USD;
function premPts() { return S ? Math.round((S.premUsd || 0) * PP_USD) + (S.premPP || 0) : 0; }
function premPtsTier(p) { let t = 0; for (let i = 1; i <= PREM_TOP; i++) if (p >= PREM[i].pts) t = i; return t; }
premT = function () { try { return S ? Math.min(PREM_TOP, Math.max(S.premT || 0, premUsdTier(S.premUsd || 0), premPtsTier(premPts()))) : 0; } catch (e) { return 0; } };
const premWeek = (T = now()) => Math.floor((T - 4 * 864e5) / (7 * 864e5)); /* weeks start Monday 00:00 UTC */
function premDblNow(T = now()) { try { return (S.premWk !== premWeek(T)) || evActive(T) || wbGroupOn(3, T); } catch (e) { return false; } }
function premOnBuy(id, usd) { try { if (!(usd > 0) || !S) return; const base = Math.round(usd * PP_USD), dbl = premDblNow(); S.premWk = premWeek(); if (dbl) { S.premPP = (S.premPP || 0) + base; (S.premPPg = S.premPPg || {})[id] = base; }
  setTimeout(() => { try { toast(`+${fmt(base * (dbl ? 2 : 1))} Premium Points${dbl ? " · DOUBLE" : ""}`, "win"); } catch (e) {} }, 1400); dirty(); } catch (e) {} }
function premOnRefund(id) { try { const b = (S.premPPg || {})[id]; if (b) { S.premPP = Math.max(0, (S.premPP || 0) - b); delete S.premPPg[id]; dirty(); } } catch (e) {} }
const premCaches = () => Math.max(0, Math.floor(premPts() / PP_CACHE) - (S.premCh || 0));
function premBar(where) { if (!S) return ""; const p = premPts(), t = premT(), nx = t < PREM_TOP ? PREM[t + 1] : null, lo = t ? PREM[t].pts : 0, k = nx ? Math.max(0, Math.min(1, (p - lo) / Math.max(1, nx.pts - lo))) : 1, c = premCaches(), cNext = PP_CACHE - p % PP_CACHE, col = (nx || PREM[t] || PREM[1]).col;
  return `<div class="ppbar ${where || ""}" style="--c:${col}"><div class="pph">${t ? premCrest(t, 26) : `<span class="ppnone">◇</span>`}<div><small>Premium Points</small><b>${fmt(p)}</b></div><button class="ppgo" data-act="premOpen">${t ? `Tier ${t}` : "Premium"} ›</button></div>
    <div class="ppt"><i style="width:${(k * 100).toFixed(1)}%"></i></div><div class="ppn">${nx ? `<span><b>${fmt(nx.pts - p)}</b> to Tier ${t + 1} · ${esc(nx.n)}</span>` : "<span>The top tier. Every point still fills caches.</span>"}<span>${c ? "" : `Cache in ${fmt(cNext)}`}</span></div>
    ${c ? `<button class="btn amber wide ppc" data-act="premCache">🎁 Open ${c} Premium Cache${c > 1 ? "s" : ""} · ◆${c * PP_CACHE_RW}</button>` : ""}${premDblNow() ? `<div class="ppdbl">✦ DOUBLE POINTS on your next purchase${(() => { try { return evActive(now()) || wbGroupOn(3, now()) ? " (event weekend)" : " (first this week)"; } catch (e) { return ""; } })()}</div>` : ""}</div>`; }
setTimeout(() => Object.assign(ACT, {
  premOpen: () => openSheet({ type: "premium" }),
  premCache: () => act(() => { const c = premCaches(); if (!c) return; S.premCh = (S.premCh || 0) + c; grantRw({ m: 0, c: 0, g: 0, shards: c * PP_CACHE_RW }, `${c} Premium Cache${c > 1 ? "s" : ""}`); toast(`Premium Cache${c > 1 ? "s" : ""}: ◆${c * PP_CACHE_RW}`, "win"); try { const b = document.querySelector(".ppc"); if (b) evkBurst(b, true); } catch (e) {} if (sheet) renderSheet(); }) }), 0);
/* the bar on the shop and the VIP page, under their header */
const ppAfterHd = (h, bar) => { const i = h.indexOf('data-act="close"'); if (i < 0) return bar + h; const j = h.indexOf("</div>", i); return j < 0 ? bar + h : h.slice(0, j + 6) + bar + h.slice(j + 6); };
{ const b = shShop; shShop = function () { const h = b.apply(this, arguments); try { return ppAfterHd(h, premBar("shop")); } catch (e) { return h; } }; }
{ const b = shVip; shVip = function () { const h = b.apply(this, arguments); try { return ppAfterHd(h, premBar("vip")); } catch (e) { return h; } }; }
{ const st = document.createElement("style"); st.textContent = `
.ppbar{--c:#ffd25a;flex:0 0 auto;margin:6px 0 10px;padding:11px 12px;border-radius:14px;background:linear-gradient(135deg,color-mix(in srgb,var(--c) 18%,#0a0e16),#070a10 70%);border:1px solid color-mix(in srgb,var(--c) 45%,transparent);box-shadow:0 0 18px color-mix(in srgb,var(--c) 20%,transparent);position:relative;overflow:hidden}
.ppbar::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(105deg,transparent 40%,color-mix(in srgb,var(--c) 16%,transparent) 50%,transparent 60%);background-size:250% 100%;animation:ppSw 4.5s ease-in-out infinite}@keyframes ppSw{0%{background-position:130% 0}60%,100%{background-position:-130% 0}}
.pph{display:flex;align-items:center;gap:10px}.pph small{display:block;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:color-mix(in srgb,var(--c) 70%,#fff)}.pph b{font:800 20px/1.1 system-ui;color:#fff;text-shadow:0 0 10px var(--c)}.ppnone{font-size:22px;color:var(--c)}
.ppgo{margin-left:auto;padding:6px 10px;border-radius:10px;border:1px solid color-mix(in srgb,var(--c) 55%,transparent);background:rgba(0,0,0,.3);color:#fff;font:700 12px system-ui}
.ppt{margin:9px 0 5px;height:8px;border-radius:4px;background:rgba(255,255,255,.08);overflow:hidden}.ppt i{display:block;height:100%;border-radius:4px;background:linear-gradient(90deg,var(--c),#fff,var(--c));background-size:200% 100%;box-shadow:0 0 10px var(--c);animation:ppFl 2.4s linear infinite}@keyframes ppFl{to{background-position:-200% 0}}
.ppn{display:flex;justify-content:space-between;gap:8px;font-size:12px;color:#b8c7d3}.ppn b{color:#fff}.ppc{margin-top:8px;animation:ppC 1.4s ease-in-out infinite}@keyframes ppC{50%{box-shadow:0 0 24px rgba(255,200,90,.8)}}
.ppdbl{white-space:normal;margin-top:8px;text-align:center;font:800 11px system-ui;letter-spacing:.12em;color:#ffe27a;text-shadow:0 0 10px #ffb02a;animation:ppD 1.6s ease-in-out infinite}@keyframes ppD{50%{opacity:.65}}
.pkpp{position:absolute;left:6px;bottom:6px;padding:2px 7px;border-radius:8px;background:rgba(10,8,2,.75);border:1px solid rgba(255,210,90,.6);color:#ffe08a;font:700 10.5px system-ui;text-shadow:0 0 6px #ffb02a}
@media (prefers-reduced-motion:reduce){.ppbar *,.ppbar::after{animation:none!important}}`; document.head.appendChild(st); }
