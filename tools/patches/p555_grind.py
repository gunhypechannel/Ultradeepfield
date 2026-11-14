# v555 reasons to keep grinding the Void Pass (owner: "I want it all").
# Prestige: every 2,000 XP past tier 40 earns a Void Cache (up to 50 a season). Caches and every cosmetic claim open with a reveal: a
# glowing chest you tap open, a burst of light and the reward card, coloured by rarity. Void Tokens (⟡): one for every reward
# claimed; spent in the Vault on Void Caches, pass tiers and past seasons' cosmetics. Tier skip: +10 tiers for ◆150. Gift Premium to
# an alliance member for ◆500 (sent through the alliance; if they already have it they get the ◆500). Premium perks: a second Glyph
# Wheel spin each day, the gold name in chat (v553), and a preview of every cosmetic reward (tap it). Season set progress is shown.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)

JS = r'''
/* ---------- v555 prestige caches, the reveal, Void Tokens and the Vault, gifting ---------- */
const VP_PCAP = 50, VT = "⟡";
const vpCaches = (v = vpState()) => Math.max(0, Math.min(VP_PCAP, Math.floor(v.xp / VP_XP) - VP_TIERS) - (v.pc || 0)) + (S.vcache || 0);
function vpCacheRoll() { const r = Math.random(), sx = cosSx(), C = cosOf(), pool = []; for (let si = 0; si <= sx; si++) for (const k of COS_ORDER) for (const id of [k + si, k + "F" + si]) { const d = cosDef(id); if (d && k !== "skinx" && (!d.free || k === "frame" || k === "trail") && !C.own[id]) pool.push(id); }
  if (r < .04 && pool.length) { const id = pool[Math.floor(Math.random() * pool.length)]; cosGive(id, 1); return { cos: id, rar: "epic" }; }
  if (r < .1) { S.shards = (S.shards || 0) + 25; return { t: "◆25 Void Shards", ic: "◆", rar: "epic" }; }
  if (r < .3) { const n = 5 + Math.floor(Math.random() * 6); S.shards = (S.shards || 0) + n; return { t: `◆${n} Void Shards`, ic: "◆", rar: "rare" }; }
  if (r < .55) { const k = ["mb2", "xf_gold", "xb_silver", "xs_silver", "xr_silver", "bf_silver", "bm_gold", "bc_gold"][Math.floor(Math.random() * 8)]; giveItem(k); return { t: wheelName({ k }), ic: "🎁", rar: "rare" }; }
  if (r < .75) { const k = ["crateM", "crateC", "crateG", "boost5", "mb1"][Math.floor(Math.random() * 5)]; giveItem(k); return { t: SHOP[k].n, ic: "📦", rar: "common" }; }
  if (r < .9) { S.vtok = (S.vtok || 0) + 3; return { t: `${VT}3 Void Tokens`, ic: VT, rar: "rare" }; }
  S.vtok = (S.vtok || 0) + 1; S.shards = (S.shards || 0) + 3; return { t: `◆3 Void Shards and ${VT}1 Void Token`, ic: "◆", rar: "common" }; }
const RV_COL = { common: "#7af4ff", rare: "#c88aff", epic: "#ffcf5a" };
function revealShow(list) { if (!list || !list.length) return; G.rvQ = (G.rvQ || []).concat(list); if (!document.getElementById("rvbox")) revealNext(); }
function revealNext() { const it = (G.rvQ || []).shift(); let w = document.getElementById("rvbox"); if (!it) { if (w) w.remove(); return; }
  const d = it.cos ? cosDef(it.cos) : null, rar = it.rar || (d ? (d.set || d.k === "skinx" ? "epic" : d.free ? "rare" : "epic") : "rare"), col = d ? d.col : RV_COL[rar], more = G.rvQ.length;
  if (!w) { w = document.createElement("div"); w.id = "rvbox"; document.body.appendChild(w); w.addEventListener("click", rvTap); }
  const art = COS_ART.cache, parts = Array.from({ length: 30 }, (_, i) => `<i class="rvp" style="--a:${(i * 37) % 360}deg;--d:${110 + (i * 53) % 150}px;--dl:${(i % 6) * .03}s"></i>`).join("");
  w.className = "rv" + (it.prev ? " open prev" : ""); w.style.setProperty("--rc", col); w.style.setProperty("--rc2", d ? d.col2 : "#ffffff"); w.dataset.st = it.prev ? "open" : "closed"; w.dataset.t = Date.now();
  w.innerHTML = `<div class="rvbg"></div><div class="rvrays"></div>${it.prev ? "" : `<div class="rvchest">${art ? `<img src="${art}" alt="">` : `<i class="rvbody"></i><i class="rvlid"></i><i class="rvgem"></i>`}</div>${parts}`}
    <div class="rvcard"><small>${it.prev ? `PREVIEW${d && d.tier ? ` · ${d.free ? "FREE" : "PREMIUM"} TIER ${d.tier}` : ""}` : rar.toUpperCase()}${d ? " · " + COS_K[d.k][0].toUpperCase() : ""}</small>${d ? cosPreview(d) : `<div class="rvic">${it.ic || "◆"}</div>`}<b>${esc(d ? d.n : it.t)}</b><em>${more ? `Tap for the next (${more} more)` : "Tap to close"}</em></div><p class="rvhint">Tap to open</p>${more ? `<button class="rvskip" type="button">Skip all ›</button>` : ""}`;
  if (!it.prev) try { SFX.click(); } catch (e) {} }
function rvTap(e) { const w = document.getElementById("rvbox"); if (!w) return; if (e && e.target && e.target.closest && e.target.closest(".rvskip")) { G.rvQ = []; w.remove(); return; } const age = Date.now() - (+w.dataset.t || 0);
  if (w.dataset.st === "closed") { if (age < 350) return; w.dataset.st = "open"; w.dataset.t = Date.now(); w.classList.add("open"); try { (w.style.getPropertyValue("--rc") === RV_COL.epic || /epic/i.test(w.querySelector(".rvcard small").textContent) ? SFX.fanfare(true) : SFX.research()); } catch (e) {} }
  else if (age > 550) revealNext(); }
function vpGiftCheck() { const a = myAlly(); if (!a || !a.passGifts) return; const v = vpState(), si = vpSeason(); S.vpGG = S.vpGG || [];
  for (const [id, g] of Object.entries(a.passGifts)) { if (!g || g.to !== G.me || g.s !== si || S.vpGG.includes(id)) continue; S.vpGG.push(id); const who = nameOf(g.by) || "An ally";
    if (!v.pr) { v.pr = 1; toast(`${who} gifted you Void Pass Premium! Claim your premium rewards in Events.`, "win"); try { SFX.fanfare(true); } catch (e) {} } else { S.shards = (S.shards || 0) + VP_PREM; toast(`${who} gifted you Void Pass Premium. You already had it, so you get ◆${VP_PREM}.`, "win"); } dirty(); } }
function vpExtrasHTML(v, lv) { const C = cosOf(), sx = cosSx(), have = COS_ORDER.filter(k => C.own[k + sx]).length, n = vpCaches(v), past = Math.max(0, Math.floor(v.xp / VP_XP) - VP_TIERS);
  const a = myAlly(), mem = a && G.mode === "online" ? Object.keys(a.members || {}).filter(u => u !== G.me && !cosPrem(u) && !isBot(u)) : [];
  return `<div class="vpx">
    <div class="vpxr"><span>${lv < VP_TIERS ? "Need a push?" : "Every tier unlocked."}</span>${lv < VP_TIERS ? `<button class="btn ghost sm" data-act="vpBuyTier" ${(S.shards || 0) >= 20 ? "" : "disabled"}>+1 tier · ◆20</button><button class="btn ghost sm" data-act="vpSkip10" ${(S.shards || 0) >= 150 ? "" : "disabled"}>+10 tiers · ◆150</button>` : ""}</div>
    <div class="vpxp2${n ? " hot" : ""}"><div><b>✦ Prestige · Void Caches</b><small>${lv < VP_TIERS ? `After tier ${VP_TIERS}, every ${fmt(VP_XP)} XP earns a Void Cache: shards, boosters, tokens, and a chance at a cosmetic you don't own.` : `${past} prestige tier${past === 1 ? "" : "s"} this season. Next cache in ${fmt(VP_XP - (v.xp % VP_XP))} XP.`}</small></div><button class="btn ${n ? "amber" : "ghost"}" data-act="vpCache" ${n ? "" : "disabled"}>${n ? `Open · ${n}` : "No caches"}</button></div>
    <div class="vpxr"><span>${VT} <b>${fmt(S.vtok || 0)}</b> Void Tokens <small class="note">· one for every reward you claim</small></span><button class="btn ghost sm" data-act="vault">🏛 Vault</button></div>
    <div class="vpxr"><span>Season set <b>${have}/${COS_ORDER.length}</b>${have >= COS_ORDER.length ? " · Ascendant aura unlocked" : " · own them all for the Ascendant aura"}</span><button class="btn ghost sm" data-act="wardrobe">👗 Wardrobe</button></div>
    ${mem.length ? `<div class="vpxr gift"><span>🎁 Gift Premium to an ally</span><select id="vpgto" class="minput">${mem.map(u => `<option value="${esc(u)}">${esc(nameOf(u))}</option>`).join("")}</select><button class="btn ghost sm" data-act="vpGift" ${(S.shards || 0) >= VP_PREM ? "" : "disabled"}>◆${VP_PREM}</button></div>` : ""}
  </div>`; }
function shVault() { const sx = cosSx(), C = cosOf(), tok = S.vtok || 0, v = vpState(), lv = Math.min(VP_TIERS, Math.floor(v.xp / VP_XP)), past = [];
  for (let si = 0; si < sx; si++) for (const k of COS_ORDER) for (const id of [k + si, k + "F" + si]) { const d = cosDef(id); if (d && (!d.free || k === "frame" || k === "trail") && !C.own[id]) past.push(d); }
  const row = (ic, n, sub, cost, act, ok, extra = "") => `<div class="vtr"><span class="vtic">${ic}</span><div><b>${n}</b><small>${sub}</small></div><button class="btn ${ok ? "amber" : "ghost"} sm" data-act="${act}" ${extra} ${ok ? "" : "disabled"}>${VT}${cost}</button></div>`;
  return `<div class="hd vthd"><div><div class="chapter">Void Tokens · ${VT}${fmt(tok)}</div><h2>The Vault</h2><p class="note">Spend the tokens you earn from Void Pass rewards and caches.</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
    <div class="vtl">${row("✦", "Void Cache", "Open it at once: shards, boosters, tokens or a cosmetic.", 8, "vtBuy", tok >= 8, 'data-k="cache"')}${lv < VP_TIERS ? row("⇪", "+1 Void Pass tier", "Jump to the next tier of this season.", 5, "vtBuy", tok >= 5, 'data-k="tier"') : ""}</div>
    <h2 class="sec">Past seasons</h2>${past.length ? `<div class="cwgrid">${past.map(d => `<div class="cwc" style="--c1:${d.col};--c2:${d.col2}">${cosPreview(d)}<b>${esc(d.n)}</b><small>Season ${d.si + 1}</small><button class="btn ${tok >= (d.free ? 15 : 40) ? "amber" : "ghost"} sm" data-act="vtBuy" data-k="${d.id}" ${tok >= (d.free ? 15 : 40) ? "" : "disabled"}>${VT}${d.free ? 15 : 40}</button></div>`).join("")}</div>` : `<p class="note">When a season ends, its cosmetics come to the Vault, so late arrivals can still collect them. Season ${sx + 1}'s arrive here when it ends.</p>`}`; }
'''
rep('const vpRwText = ', JS + 'const vpRwText = ')
rep('profile: shProfile, wardrobe: shWardrobe', 'profile: shProfile, wardrobe: shWardrobe, vault: shVault')
# the pass body: tiers, prestige, tokens, set progress, gifting
rep('${lv < VP_TIERS ? `<div class="vptier"><span>Need a push? Buy the next tier.</span><button class="btn ghost sm" data-act="vpBuyTier" ${(S.shards || 0) >= 20 ? "" : "disabled"}>+1 tier · ◆20</button></div>` : ""}', '${vpExtrasHTML(v, lv)}')
rep('<button class="btn ghost wide sm cwopen" data-act="wardrobe">👗 Wardrobe · ${Object.keys(cosOf().own).length} cosmetics</button>', '<p class="note cwnote">Tap a cosmetic reward to preview it.</p>')
rep('<div class="vpc${prem ? " p" : ""}${got ? " got" : open && !lock ? " ready" : ""}${lock ? " lock" : ""}">', '<div class="vpc${prem ? " p" : ""}${got ? " got" : open && !lock ? " ready" : ""}${lock ? " lock" : ""}${r.cos ? " cos" : ""}"${r.cos ? ` data-act="cosPrev" data-id="${r.cos}" role="button"` : ""}>')
# the reveal for cosmetics you claim, and tokens
rep('function vpGrant(r) { if (r.cos) cosGive(r.cos);', 'function vpGrant(r) { if (r.cos) { cosGive(r.cos); (G.rvPend = G.rvPend || []).push({ cos: r.cos }); clearTimeout(G.rvT); G.rvT = setTimeout(() => { const L = G.rvPend; G.rvPend = []; revealShow(L); }, 400); }')
rep('if (n) { toast(`Void Pass: ${n} reward${n > 1 ? "s" : ""} claimed${sh ? ` (◆${sh} among them)` : ""}.`, "win");', 'if (n) S.vtok = (S.vtok || 0) + n; /* v555 tokens */\n    if (n) { toast(`Void Pass: ${n} reward${n > 1 ? "s" : ""} claimed${sh ? ` (◆${sh} among them)` : ""} · +${n} ${VT}.`, "win");')
rep('setInterval(vpTick, 5000);', 'setInterval(vpTick, 5000); setInterval(() => { try { if (S && G.ready) vpGiftCheck(); } catch (e) {} }, 15000); /* v555 */')
# premium: a second wheel spin a day
rep('function wheelHTML(T) { const own = !!G.owner, can = (own || (S.shopFree || "") !== shopDay()) && S.wheelPend == null,', 'function wheelHTML(T) { const own = !!G.owner, bon = (S.shopFree || "") === shopDay() && cosPrem(G.me) && (S.shopFree2 || "") !== shopDay(), can = (own || (S.shopFree || "") !== shopDay() || bon) && S.wheelPend == null,')
rep(': can ? "Free daily spin" : "Spun today"}', ': can ? (bon && !own ? "♛ Premium bonus spin" : "Free daily spin") : "Spun today"}')
rep('function wheelPull() { if (G.wheel || (!G.owner && (S.shopFree || "") === shopDay()) || S.wheelPend != null) return;', 'function wheelPull() { const bon = (S.shopFree || "") === shopDay() && cosPrem(G.me) && (S.shopFree2 || "") !== shopDay(); if (G.wheel || (!G.owner && (S.shopFree || "") === shopDay() && !bon) || S.wheelPend != null) return;')
rep('act(() => { S.shopFree = shopDay(); S.wheelPend = idx; bump("wheelSpins"); })', 'act(() => { if ((S.shopFree || "") === shopDay() && !G.owner) S.shopFree2 = shopDay(); S.shopFree = shopDay(); S.wheelPend = idx; bump("wheelSpins"); })')
# actions
rep('  wardrobe: () => {', '''  vault: () => { openSheet({ type: "vault" }); }, /* v555 */
  vpSkip10: () => act(() => { const v = vpState(); if ((S.shards || 0) < 150 || v.xp >= VP_TIERS * VP_XP) return; S.shards -= 150; v.xp = Math.min(VP_TIERS, Math.floor(v.xp / VP_XP) + 10) * VP_XP; toast(`Tier ${Math.floor(v.xp / VP_XP)} reached. Claim your rewards.`, "win"); try { SFX.research(); } catch (e) {} }),
  vpCache: () => { const v = vpState(); if (!vpCaches(v)) return; const earned = Math.max(0, Math.min(VP_PCAP, Math.floor(v.xp / VP_XP) - VP_TIERS)); if (earned > (v.pc || 0)) v.pc = (v.pc || 0) + 1; else S.vcache = Math.max(0, (S.vcache || 0) - 1); const it = vpCacheRoll(); dirty(); revealShow([it]); sheet ? renderSheet() : render(true); },
  vtBuy: d => { const tok = S.vtok || 0; if (d.k === "cache") { if (tok < 8) return; S.vtok -= 8; S.vcache = (S.vcache || 0) + 1; ACT.vpCache(); }
    else if (d.k === "tier") { const v = vpState(); if (tok < 5 || v.xp >= VP_TIERS * VP_XP) return; S.vtok -= 5; v.xp = (Math.floor(v.xp / VP_XP) + 1) * VP_XP; toast(`Tier ${Math.floor(v.xp / VP_XP)} reached.`, "win"); }
    else { const c = cosDef(d.k); if (!c || cosOf().own[c.id] || c.si >= cosSx()) return; const cost = c.free ? 15 : 40; if (tok < cost) return; S.vtok -= cost; cosGive(c.id, 1); revealShow([{ cos: c.id }]); }
    dirty(); try { syncPlayer(); } catch (e) {} renderSheet(); },
  vpGift: () => { const a = myAlly(), sel = document.getElementById("vpgto"), to = sel && sel.value; if (!a || !to || !G.db || (S.shards || 0) < VP_PREM || cosPrem(to)) return; S.shards -= VP_PREM; const id = "pg" + (S.seq++) + (now() % 1e6).toString(36);
    G.db.doc("alliances/" + a.id).update({ passGifts: { [id]: { by: G.me, to, s: vpSeason(), at: now() } } }).catch(() => {}); dirty(); toast(`Void Pass Premium sent to ${nameOf(to)}.`, "win"); try { SFX.fanfare(true); } catch (e) {} renderSheet ? (sheet ? renderSheet() : render(true)) : 0; },
  cosPrev: d => { if (cosDef(d.id)) revealShow([{ cos: d.id, prev: 1 }]); },
  wardrobe: () => {''')
css = r'''
/* v555 prestige, the reveal, the Vault */
.vpx{display:flex;flex-direction:column;gap:6px;margin:8px 0}
.vpxr{display:flex;align-items:center;gap:6px;flex-wrap:wrap;padding:7px 10px;border-radius:10px;background:rgba(8,16,28,.7);border:1px solid rgba(122,244,255,.18);font-size:12.5px}.vpxr>span{flex:1;min-width:140px}.vpxr .minput{flex:1 1 120px;min-width:0;height:32px;padding:2px 8px}
.vpxp2{display:flex;align-items:center;gap:10px;padding:10px;border-radius:12px;border:1px solid rgba(255,207,90,.35);background:linear-gradient(120deg,rgba(255,207,90,.1),rgba(8,14,24,.9))}.vpxp2>div{flex:1;display:flex;flex-direction:column;gap:2px}.vpxp2 small{font-size:11.5px;color:var(--muted)}
.vpxp2.hot{box-shadow:0 0 18px rgba(255,207,90,.35);animation:vph 2s ease-in-out infinite}@keyframes vph{50%{box-shadow:0 0 28px rgba(255,207,90,.6)}}
.vpc.cos{cursor:pointer;outline:1px dashed rgba(255,207,90,.45);outline-offset:-3px}.cwnote{margin:2px 0 4px}
.vthd{background:radial-gradient(120% 140% at 0% 0%,rgba(255,207,90,.25),transparent 60%),linear-gradient(90deg,#0b1020,#100c1c);border-radius:14px;padding:12px;border:1px solid rgba(255,207,90,.4)}
.vtl{display:flex;flex-direction:column;gap:8px;margin:10px 0}.vtr{display:flex;align-items:center;gap:10px;padding:10px;border-radius:12px;border:1px solid rgba(255,207,90,.3);background:rgba(10,14,24,.85)}.vtr>div{flex:1;display:flex;flex-direction:column}.vtr small{font-size:11.5px;color:var(--muted)}.vtic{font-size:24px;color:#ffcf5a;text-shadow:0 0 10px #ffcf5a;width:32px;text-align:center}
#rvbox{position:fixed;inset:0;z-index:10000;display:grid;place-items:center;cursor:pointer;-webkit-user-select:none;user-select:none}
.rvbg{position:absolute;inset:0;background:radial-gradient(circle at 50% 46%,color-mix(in srgb,var(--rc) 30%,transparent),rgba(2,4,10,.94) 62%)}
.rvrays{position:absolute;left:50%;top:46%;width:160vmax;height:160vmax;margin:-80vmax;background:repeating-conic-gradient(color-mix(in srgb,var(--rc) 35%,transparent) 0 6deg,transparent 6deg 18deg);-webkit-mask:radial-gradient(circle,#000 0,transparent 45%);mask:radial-gradient(circle,#000 0,transparent 45%);opacity:0;transition:opacity .6s;animation:rvspin 14s linear infinite}
.rv.open .rvrays{opacity:1}@keyframes rvspin{to{transform:rotate(360deg)}}
.rvchest{position:relative;width:min(56vw,230px);aspect-ratio:1.15;animation:rvshake 1.4s ease-in-out infinite;filter:drop-shadow(0 0 26px var(--rc))}.rvchest img{width:100%;height:100%;object-fit:contain}
.rvbody{position:absolute;left:6%;right:6%;bottom:6%;height:52%;border-radius:10px 10px 14px 14px;background:linear-gradient(180deg,#2a3448,#121826 60%,#0a0e18);border:2px solid color-mix(in srgb,var(--rc) 70%,#fff);box-shadow:inset 0 0 22px color-mix(in srgb,var(--rc) 55%,transparent)}
.rvbody::before{content:"";position:absolute;left:0;right:0;top:34%;height:5px;background:var(--rc);box-shadow:0 0 14px var(--rc)}
.rvlid{position:absolute;left:3%;right:3%;top:16%;height:32%;border-radius:40% 40% 8px 8px/70% 70% 8px 8px;background:linear-gradient(180deg,#3a4660,#18202f);border:2px solid color-mix(in srgb,var(--rc) 70%,#fff);transform-origin:50% 100%;transition:transform .55s cubic-bezier(.3,1.5,.5,1),opacity .5s}
.rvgem{position:absolute;left:50%;top:44%;width:16%;aspect-ratio:1;transform:translate(-50%,-50%) rotate(45deg);background:radial-gradient(circle,#fff,var(--rc) 55%);box-shadow:0 0 18px var(--rc),0 0 40px var(--rc);animation:rvgem 1s ease-in-out infinite}
@keyframes rvgem{50%{box-shadow:0 0 30px var(--rc),0 0 70px var(--rc)}}@keyframes rvshake{0%,70%,100%{transform:none}75%{transform:rotate(-4deg)}80%{transform:rotate(4deg)}85%{transform:rotate(-3deg)}90%{transform:rotate(2deg)}}
.rv.open .rvchest{animation:none;transform:scale(.8) translateY(30vh);opacity:.0;transition:transform .7s ease .35s,opacity .5s ease .45s}.rv.open .rvlid{transform:translateY(-70%) rotate(-28deg);opacity:0}
.rvp{position:absolute;left:50%;top:46%;width:10px;height:10px;margin:-5px;border-radius:50%;background:radial-gradient(circle,#fff,var(--rc) 50%,transparent 72%);opacity:0}
.rvp:nth-child(3n){background:radial-gradient(circle,#fff,var(--rc2) 50%,transparent 72%)}.rv.open .rvp{animation:rvp .9s ease-out var(--dl) forwards}
@keyframes rvp{0%{opacity:1;transform:rotate(var(--a)) translateX(0) scale(1.4)}100%{opacity:0;transform:rotate(var(--a)) translateX(var(--d)) scale(.3)}}
.rvcard{position:absolute;left:50%;top:46%;width:min(78vw,300px);transform:translate(-50%,-30%) scale(.6);opacity:0;display:flex;flex-direction:column;gap:6px;padding:12px;border-radius:16px;text-align:center;border:2px solid var(--rc);background:linear-gradient(180deg,rgba(14,20,36,.96),rgba(6,9,18,.98));box-shadow:0 0 34px color-mix(in srgb,var(--rc) 60%,transparent);transition:transform .55s cubic-bezier(.3,1.5,.5,1) .3s,opacity .3s .3s;pointer-events:none}
.rv.open .rvcard{transform:translate(-50%,-50%) scale(1);opacity:1}.rv.prev .rvcard{transition:none}
.rvcard small{font-size:10.5px;letter-spacing:.14em;color:var(--rc)}.rvcard b{font:800 19px var(--f-display,sans-serif);color:#fff}.rvcard em{font-style:normal;font-size:11.5px;color:var(--muted)}.rvic{font-size:64px;color:var(--rc);text-shadow:0 0 22px var(--rc);padding:14px 0}
.rvskip{position:absolute;z-index:3;top:calc(env(safe-area-inset-top,0px) + 14px);right:14px;padding:7px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.35);background:rgba(6,10,20,.7);color:#e9f6ff;font-size:12.5px;letter-spacing:.06em}
.rvhint{margin:0;background:none;position:absolute;bottom:14%;left:0;right:0;text-align:center;color:#d6e2ea;font-size:13px;letter-spacing:.1em;animation:rvgem 1.4s ease-in-out infinite}.rv.open .rvhint{display:none}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 554\b", "GAME_V = 555", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
