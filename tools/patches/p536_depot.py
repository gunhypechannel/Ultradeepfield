# v536 the Supply Depot remastered (owner: "Can't we remaster this page to something more exciting and engaging? What is it missing?"
# then "Approved all"). Menu › Supply Depot is now:
#  - a depot banner with its quartermaster, Ondra Vey, and a line of hers (rotates, never the same twice in a row);
#  - a live market: each resource's value drifts ±12% by UTC day (depVal; base 1 gas = 2 crystal = 3 metal), with ▲/▼ against yesterday,
#    a 7-day sparkline and a "Hot today" tag on the resource that sells best;
#  - "Fix my shortage": the depot reads your stores (by trade value) and fills the trade that tops up your scarcest resource;
#  - a new trade panel: resource tiles with your stock, a ⇄ swap, a slider plus 25/50/100%, a live preview with the depot's cut, and a
#    "TRADED" stamp when it goes through;
#  - trader rank: lifetime volume (S.trVol, in metal value) raises your standing Bronze → Silver (10M) → Gold (100M) → Platinum (1B),
#    each one trims the depot's cut 10% → 9% → 8% → 7%;
#  - the Boost card: today's price, the next price, how many you can afford, and Buy ×5;
#  - a daily depot contract (S.depC): deliver 3 hours of one resource's production (at least 5,000) for ◆3 and a crate;
#  - the last six trades (S.trLog).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
i = s.index('function mShop() {'); j = s.index('/* ---------- the simulator test battle', i)
s = s[:i] + r'''/* v536 the Supply Depot */
const DEP_RANK = [["Bronze", 0, .10, "#d08a55"], ["Silver", 1e7, .09, "#cfd8df"], ["Gold", 1e8, .08, "#ffcf5a"], ["Platinum", 1e9, .07, "#b9f0ff"]];
const depRank = () => { const v = S.trVol || 0; let i = 0; while (i + 1 < DEP_RANK.length && v >= DEP_RANK[i + 1][1]) i++; return i; };
const depFee = () => DEP_RANK[depRank()][2];
const depDay = (d = 0) => { const t = new Date(Date.now() - d * 864e5); return t.getUTCFullYear() * 1e4 + (t.getUTCMonth() + 1) * 100 + t.getUTCDate(); };
const depF = (r, d = 0) => 1 + .12 * (((hash("dep" + r + depDay(d)) % 1000) / 1000) * 2 - 1);
const depVal = (r, d = 0) => TRADE_VAL[r] * depF(r, d);
const depGet = (from, to, amt) => Math.floor(amt * depVal(from) / depVal(to) * (1 - depFee()));
const depHot = () => ["m", "c", "g"].reduce((a, r) => depF(r) > depF(a) ? r : a, "m");
function depFix() { const R = ["m", "c", "g"], v = r => Math.max(0, S.res[r]) * TRADE_VAL[r], lo = R.reduce((a, r) => v(r) < v(a) ? r : a), hi = R.reduce((a, r) => v(r) > v(a) ? r : a), mean = (v("m") + v("c") + v("g")) / 3;
  if (lo === hi || v(hi) < v(lo) * 1.25 + 1000) return null; const give = Math.floor(Math.min(S.res[hi] * .5, (v(hi) - mean) / TRADE_VAL[hi] * .6)); return give > 0 ? { from: hi, to: lo, amt: give } : null; }
function depContract() { const day = depDay(), r = ["m", "c", "g"][hash("dc" + day) % 3], amt = Math.max(5000, Math.round(rates()[r] * 60 * 3 / 1000) * 1000), crate = { m: "crateC", c: "crateG", g: "crateM" }[r]; return { day, r, amt, crate, done: S.depC === day }; }
const DEP_LINES = [h => `Fresh crates in from the outer belts. ${RES_N[h]} is selling high today.`, () => "You bring it, I'll move it. The depot always takes its cut.", h => `Everyone wants ${RES_N[h].toLowerCase()} this morning. Sell while it lasts.`,
  () => "I've got a hauler that needs filling. Check today's contract.", () => "Prices move every day, Commander. Good traders watch the arrows.", () => "Trade enough with me and I'll trim my cut. That's a promise."];
function depLine() { const k = Math.floor(Date.now() / 90000); if (G.depLineK !== k) { G.depLineK = k; let n; do { n = (Math.random() * DEP_LINES.length) | 0; } while (n === G.depLineN && DEP_LINES.length > 1); G.depLineN = n; } return DEP_LINES[G.depLineN || 0](depHot()); }
function depSpark(r) { const v = []; for (let d = 6; d >= 0; d--) v.push(depF(r, d)); const W = 64, H = 20, mn = .86, mx = 1.14, pts = v.map((y, i) => `${(i / 6 * W).toFixed(1)},${(H - (y - mn) / (mx - mn) * H).toFixed(1)}`).join(" ");
  return `<svg class="dpsp" viewBox="0 0 ${W} ${H}" aria-hidden="true"><polyline points="${pts}"/><circle cx="${W}" cy="${(H - (v[6] - mn) / (mx - mn) * H).toFixed(1)}" r="2.2"/></svg>`; }
function mShop() {
  const tr = menu.tr, have = Math.floor(S.res[tr.from]), amt = clamp(Math.floor(tr.amt || 0), 0, have), fee = depFee(), get = depGet(tr.from, tr.to, amt), rk = depRank(), R = DEP_RANK[rk], nx = DEP_RANK[rk + 1], vol = S.trVol || 0, hot = depHot();
  const bp = boostPrice(), aff = Math.min(...["m", "c", "g"].map(r => bp[r] ? Math.floor(S.res[r] / bp[r]) : 99)), nextK = Math.min(12, Math.pow(1.15, (S.boostBuys || 0) + 1)) / Math.min(12, Math.pow(1.15, S.boostBuys || 0));
  const fix = depFix(), C = depContract(), stamp = G.depFx && performance.now() - G.depFx < 1400;
  const mk = r => { const f = depF(r), y = depF(r, 1), up = f >= y; return `<div class="dpm${r === hot ? " hot" : ""}"><span class="r-${r}">${RI[r]}</span><div><b>${RES_N[r]}</b><small>${(f * 100 - 100 >= 0 ? "+" : "") + (f * 100 - 100).toFixed(1)}% today</small></div>${depSpark(r)}<em class="${up ? "up" : "dn"}">${up ? "▲" : "▼"}</em>${r === hot ? '<i>HOT TODAY</i>' : ""}</div>`; };
  const tile = (key, act) => `<div class="dpt">${["m", "c", "g"].map(r => `<button class="${tr[key] === r ? "on" : ""}" data-act="${act}" data-r="${r}"><span class="r-${r}">${RI[r]}</span><b>${RES_N[r]}</b><small>${fmt(Math.floor(S.res[r]))}</small></button>`).join("")}</div>`;
  const log = (S.trLog || []).slice(0, 6);
  return `<div class="dpb"><div class="dpbn" style="background-image:url(art/allyDepot.webp)"></div><div class="dpq"><img src="avatars/pilot.webp" alt=""><div><small>QUARTERMASTER ONDRA VEY</small><p>${esc(depLine())}</p></div></div></div>
    <div class="dpc"><div class="dph"><b>Market today</b><span class="note">Base: 1 gas = 2 crystal = 3 metal</span></div><div class="dpmk">${["m", "c", "g"].map(mk).join("")}</div></div>
    ${fix ? `<button class="dpfix" data-act="depFix"><span>⚡ Fix my shortage</span><small>${RES_N[fix.to]} is your lowest. Swap ${fmt(fix.amt)} ${RES_N[fix.from].toLowerCase()} → ${fmt(depGet(fix.from, fix.to, fix.amt))} ${RES_N[fix.to].toLowerCase()}</small></button>` : `<div class="dpfix ok"><span>✓ Your stores are balanced</span><small>Nothing to fix right now.</small></div>`}
    <div class="dpc dptr${stamp ? " stamp" : ""}"><div class="dph"><b>Trade</b><span class="dprk" style="--rc:${R[3]}">${R[0]} trader · ${Math.round(fee * 100)}% cut</span></div>
      <span class="note">Give</span>${tile("from", "trFrom")}
      <div class="dpsw"><button data-act="depSwap" aria-label="Swap give and receive">⇅</button></div>
      <span class="note">Receive</span>${tile("to", "trTo")}
      <input class="dpsl" id="tramt" type="range" min="0" max="${have}" step="${Math.max(1, Math.floor(have / 400))}" value="${amt}" aria-label="Amount to trade">
      <div class="seg">${[25, 50, 100].map(p => `<button data-act="trPct" data-p="${p}">${p}%</button>`).join("")}</div>
      <div class="dppv"><div><small>You give</small><b class="r-${tr.from}" id="trgive">${fmt(amt)} ${RES_N[tr.from]}</b></div><span>→</span><div><small>You get</small><b class="r-${tr.to}" id="trget">${fmt(get)} ${RES_N[tr.to]}</b></div></div>
      <p class="note" id="trfee">Depot's cut: ${fmt(Math.floor(amt * depVal(tr.from) / depVal(tr.to) * fee))} ${RES_N[tr.to].toLowerCase()} (${Math.round(fee * 100)}%)</p>
      <button class="mbtn" data-act="trade" ${tr.from === tr.to || !amt ? "disabled" : ""}>Trade</button>${stamp ? '<i class="dpstamp">TRADED</i>' : ""}
      <div class="dprb"><div class="xp"><i style="width:${nx ? Math.min(100, (vol - R[1]) / (nx[1] - R[1]) * 100).toFixed(1) : 100}%;background:${R[3]}"></i></div><small>${nx ? `${fmt(Math.max(0, nx[1] - vol))} more traded (metal value) for ${nx[0]}: the cut drops to ${Math.round(nx[2] * 100)}%` : "Platinum trader: the lowest cut in the galaxy"}</small></div></div>
    <div class="dpc dpct${C.done ? " done" : ""}"><div class="dph"><b>📦 Today's contract</b><span class="note">ends in <b data-end="${shopDayEnd()}">${ftime(shopDayEnd() - now())}</b></span></div>
      <p>${C.done ? "Delivered. Ondra will have a new one tomorrow." : `Deliver <b class="r-${C.r}">${fmt(C.amt)} ${RES_N[C.r].toLowerCase()}</b> to the depot. Reward: <b class="shard">◆3</b> and a ${SHOP[C.crate].n}.`}</p>
      ${C.done ? "" : `<button class="btn amber" data-act="depContract" ${S.res[C.r] >= C.amt ? "" : "disabled"}>${S.res[C.r] >= C.amt ? "Deliver" : `Need ${fmt(C.amt - Math.floor(S.res[C.r]))} more`}</button>`}</div>
    <div class="dpc"><div class="dph"><b class="dpbo"><span>${MI.bolt}</span> Boost ×1</b><span class="note">${aff} affordable</span></div><p class="note">Cuts 5 minutes off a construction, research or shipyard job. Each one bought raises the price 15% (up to 12× the first). Next: ×${nextK.toFixed(2)}.</p>
      <div class="dpbt">${costHTML(bp)}<div><button class="btn amber" data-act="buyBoost" data-cost='${JSON.stringify(bp)}' ${aff >= 1 ? "" : "disabled"}>Buy</button><button class="btn ghost" data-act="buyBoost5" ${aff >= 5 ? "" : "disabled"}>Buy ×5</button></div></div></div>
    ${log.length ? `<div class="dpc"><div class="dph"><b>Recent trades</b></div><div class="dplog">${log.map(x => `<div><span class="r-${x.f}">${fmt(x.a)} ${RES_N[x.f]}</span><i>→</i><span class="r-${x.to}">${fmt(x.g)} ${RES_N[x.to]}</span><small>${ago(x.t)}</small></div>`).join("")}</div></div>` : ""}
    <p class="note" style="text-align:center">Everything here costs resources you earn in play. Nothing is sold for real money.</p>`;
}
''' + s[j:]
rep('''    const get = Math.floor(amt * TRADE_VAL[from] / TRADE_VAL[to] * .9);
    S.res[from] -= amt; S.res[to] += get; bump("trades"); menu.tr.amt = 0;''', '''    const get = depGet(from, to, amt), rk0 = depRank(); /* v536 the live market and the trader's cut */
    S.res[from] -= amt; S.res[to] += get; bump("trades"); menu.tr.amt = 0; S.trVol = (S.trVol || 0) + Math.round(amt * TRADE_VAL[from]); S.trLog = [{ t: now(), f: from, a: amt, to, g: get }].concat(S.trLog || []).slice(0, 6); G.depFx = performance.now();
    setTimeout(() => { if (G.depFx && performance.now() - G.depFx >= 1400) renderMenu(); }, 1450); if (depRank() > rk0) setTimeout(() => toast(`Depot standing: ${DEP_RANK[depRank()][0]} trader. Ondra's cut is now ${Math.round(depFee() * 100)}%.`, "win"), 600);''')
rep('''  buyBoost: () => act(() => {''', '''  depSwap: () => { const t = menu.tr; [t.from, t.to] = [t.to, t.from]; t.amt = 0; renderMenu(); }, /* v536 */
  depFix: () => { advance(now()); const f = depFix(); if (!f) return; Object.assign(menu.tr, f); renderMenu(); },
  depContract: () => act(() => { const C = depContract(); if (C.done || S.res[C.r] < C.amt) return; S.res[C.r] -= C.amt; S.depC = C.day; S.shards = (S.shards || 0) + 3; giveItem(C.crate); toast(`Contract delivered: ◆3 and a ${SHOP[C.crate].n}.`, "win"); try { SFX.research(); } catch (e) {} }),
  buyBoost5: () => act(() => { let n = 0; for (; n < 5; n++) { if (!pay(boostPrice())) break; S.boosts++; S.boostBuys = (S.boostBuys || 0) + 1; } if (n) toast(`${n} boost${n > 1 ? "s" : ""} added to your inventory.`, "win"); else toast("Not enough resources.", "warn"); }),
  buyBoost: () => act(() => {''')
rep('''    const g = $("#trget"); if (g) g.textContent = `${fmt(Math.floor(tr.amt * TRADE_VAL[tr.from] / TRADE_VAL[tr.to] * .9))} ${RES_N[tr.to]}`;''',
    '''    const g = $("#trget"); if (g) g.textContent = `${fmt(depGet(tr.from, tr.to, tr.amt))} ${RES_N[tr.to]}`; const gv = $("#trgive"); if (gv) gv.textContent = `${fmt(tr.amt)} ${RES_N[tr.from]}`; /* v536 */
    const fe = $("#trfee"); if (fe) fe.textContent = `Depot's cut: ${fmt(Math.floor(tr.amt * depVal(tr.from) / depVal(tr.to) * depFee()))} ${RES_N[tr.to].toLowerCase()} (${Math.round(depFee() * 100)}%)`;''')
css = '''
/* v536 the Supply Depot */
.dpb{position:relative;border-radius:16px;overflow:hidden;min-height:150px;display:flex;align-items:flex-end;border:1px solid rgba(255,207,90,.35)}
.dpbn{position:absolute;inset:0;background:center/cover no-repeat;filter:saturate(1.1)}.dpbn::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(5,9,15,.05),rgba(5,9,15,.92) 78%)}
.dpq{position:relative;display:flex;gap:10px;align-items:flex-end;padding:10px 12px}.dpq img{width:58px;height:58px;border-radius:12px;border:1px solid rgba(255,207,90,.6);box-shadow:0 0 12px rgba(255,207,90,.3);object-fit:cover;flex:none}
.dpq small{font-size:10px;letter-spacing:.14em;color:var(--amber)}.dpq p{margin:2px 0 0;font-size:13.5px;line-height:1.35;color:#e9f1f7;background:rgba(6,14,22,.75);border:1px solid rgba(255,255,255,.1);border-radius:4px 12px 12px 12px;padding:6px 9px}
.dpc{position:relative;display:flex;flex-direction:column;gap:8px;margin-top:10px;padding:12px;border-radius:16px;border:1px solid var(--line);background:linear-gradient(180deg,rgba(85,214,232,.05),rgba(255,255,255,.01) 40%),var(--panel,#121a22)}
.dph{display:flex;justify-content:space-between;align-items:baseline;gap:8px;flex-wrap:wrap}.dph>b{font-size:15px}
.dpmk{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
.dpm{position:relative;display:grid;grid-template-columns:auto minmax(0,1fr);grid-template-rows:auto auto;gap:2px 6px;align-items:center;padding:8px;border-radius:12px;border:1px solid rgba(255,255,255,.08);background:rgba(4,10,16,.5)}
.dpm>span{grid-row:1}.dpm>span img,.dpm>span svg{width:22px;height:22px}.dpm b{font-size:13px;display:block}.dpm small{font-size:11px;color:var(--muted)}
.dpsp{grid-column:1/3;width:100%;height:22px}.dpsp polyline{fill:none;stroke:var(--cyan);stroke-width:1.6;stroke-linejoin:round}.dpsp circle{fill:var(--cyan)}
.dpm em{position:absolute;top:7px;right:8px;font-style:normal;font-size:12px}.dpm em.up{color:#5dff9a}.dpm em.dn{color:#ff6b5a}
.dpm.hot{border-color:rgba(255,207,90,.7);box-shadow:0 0 14px rgba(255,207,90,.25)}.dpm.hot .dpsp polyline{stroke:var(--amber)}.dpm.hot .dpsp circle{fill:var(--amber)}
.dpm i{position:absolute;left:50%;bottom:-7px;transform:translateX(-50%);font-style:normal;font-size:8.5px;font-weight:800;letter-spacing:.1em;padding:1px 6px;border-radius:5px;background:var(--amber);color:#1a1000;white-space:nowrap}
.dpfix{display:flex;flex-direction:column;align-items:flex-start;gap:2px;width:100%;margin-top:12px;padding:11px 13px;border-radius:14px;border:1px solid rgba(93,255,154,.5);background:linear-gradient(90deg,rgba(93,255,154,.16),rgba(8,18,28,.9));color:var(--fg);text-align:left}
.dpfix span{font-weight:700;font-size:14.5px;color:#5dff9a}.dpfix small{font-size:12px;color:var(--muted)}.dpfix.ok{border-color:var(--line);background:rgba(8,18,28,.6)}.dpfix.ok span{color:var(--muted)}
.dprk{font-size:11px;font-weight:700;letter-spacing:.06em;color:var(--rc);border:1px solid var(--rc);border-radius:7px;padding:2px 7px}
.dpt{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}.dpt button{display:flex;flex-direction:column;align-items:center;gap:1px;padding:8px 4px;border-radius:12px;border:1px solid var(--line);background:rgba(4,10,16,.55);color:var(--fg)}
.dpt button.on{border-color:var(--cyan);background:rgba(85,214,232,.14);box-shadow:0 0 12px rgba(85,214,232,.25)}.dpt button span img,.dpt button span svg{width:24px;height:24px}.dpt b{font-size:13px}.dpt small{font-size:11px;color:var(--muted)}
.dpsw{display:flex;justify-content:center;margin:-4px 0}.dpsw button{width:36px;height:36px;border-radius:50%;border:1px solid var(--cyan);background:rgba(85,214,232,.12);color:var(--cyan);font-size:18px}
.dpsl{width:100%;accent-color:var(--cyan);height:28px}
.dppv{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);align-items:center;gap:8px;padding:10px;border-radius:12px;background:rgba(4,10,16,.6)}.dppv small{display:block;font-size:11px;color:var(--muted)}.dppv b{font-size:16px}.dppv>div:last-child{text-align:right}.dppv>span{color:var(--muted)}
.dptr.stamp{animation:dpfl 1s ease-out}@keyframes dpfl{0%{box-shadow:0 0 0 2px #5dff9a,0 0 30px rgba(93,255,154,.5)}100%{box-shadow:none}}
.dpstamp{position:absolute;left:50%;top:44%;transform:translate(-50%,-50%) rotate(-12deg);font-style:normal;font:800 34px var(--f-display,sans-serif);letter-spacing:.12em;color:#5dff9a;border:3px solid #5dff9a;border-radius:10px;padding:4px 16px;text-shadow:0 0 12px rgba(93,255,154,.7);pointer-events:none;animation:dpst 1.3s ease-out forwards}
@keyframes dpst{0%{opacity:0;transform:translate(-50%,-50%) rotate(-12deg) scale(2.2)}18%{opacity:1;transform:translate(-50%,-50%) rotate(-12deg) scale(1)}75%{opacity:1}100%{opacity:0}}
.dprb small{font-size:11.5px;color:var(--muted)}.dprb .xp{margin-bottom:4px}
.dpct{border-color:rgba(255,207,90,.4)}.dpct p{margin:0;font-size:13.5px}.dpct.done{opacity:.7}
.dpbt{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}.dpbt>div:last-child{display:flex;gap:6px}
.dpbo{display:flex;align-items:center;gap:6px}.dpbo span{color:var(--amber);display:inline-flex}.dpbo svg{width:20px;height:20px}
.dplog{display:flex;flex-direction:column;gap:4px}.dplog>div{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr) auto;gap:6px;align-items:center;font-size:12.5px;padding:5px 8px;border-radius:8px;background:rgba(4,10,16,.45)}.dplog i{font-style:normal;color:var(--muted)}.dplog small{color:var(--muted);font-size:11px}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 535\b", "GAME_V = 536", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
