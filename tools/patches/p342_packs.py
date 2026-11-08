# v342: Packs tab (catalog from the server), weekly free tester claims, and delivery of every grant (tester, admin, later purchases)
p="docs/udf-supabase.js"; s=open(p).read()
a="  var signingOut = false;\n  window.udfAccount = {"
assert s.count(a)==1
s=s.replace(a,"""  /* v342 premium packs: the catalog, tester claims and grant delivery. Purchases are not wired: only the owner or a store-verifying
     server function can create a purchase grant; the game only reads, claims tester packs and acknowledges what it applied. */
  function need() { if (!sb || !me) return Promise.reject(Object.assign(new Error("Sign in first."), { code: "unavailable" })); return Promise.resolve(); }
  window.udfShop = {
    packs: function () { return need().then(function () { return run(sb.from("shop_packs").select("id,data,once_per_account,tester_eligible,sort").order("sort")); }); },
    status: function () { return need().then(function () { return run(sb.rpc("tester_status")); }); },
    claim: function (id) { return need().then(function () { return run(sb.rpc("claim_tester_pack", { p_pack: id })); }); },
    mine: function () { return need().then(function () { return run(sb.rpc("my_grants")); }); },
    ack: function (id) { return need().then(function () { return run(sb.rpc("ack_grant", { p_id: id })); }); },
    ackRevoke: function (id) { return need().then(function () { return run(sb.rpc("ack_revoke", { p_id: id })); }); }
  };
""" + a)
open(p,"w").write(s)

p="docs/index.html"; h=open(p).read()
def rep(a,b):
    global h; assert h.count(a)==1,(h.count(a),a[:80]); h=h.replace(a,b)
rep('const tabs = `<div class="shipcls shoptabs" role="tablist">${SHOP_CATS.concat([["skins", "Planet skins"]',
    'const tabs = `<div class="shipcls shoptabs" role="tablist">${[["packs", "◆ Packs"]].concat(SHOP_CATS).concat([["skins", "Planet skins"]')
rep('  const body = cat === "skins" ? `<p class="note">Premium looks','  const body = cat === "packs" ? packsBody() : cat === "skins" ? `<p class="note">Premium looks')
rep('function shShop() {','''/* ---------- v342 premium packs ----------
   The catalog lives on the server (shop_packs). Testers claim one pack a week for free (claim_tester_pack: the server refuses a second
   claim). Every grant (tester, owner, and later store purchases) arrives through my_grants and is applied here exactly once:
   S.grants remembers it before the save, and the server is told only after the save (ack), so a crash can't lose or double it. */
const PK_FAM = [["starter", "Starter"], ["shards", "Void Shards"], ["empire", "Empire Development"], ["fleet", "Fleet Warfare"], ["forge", "Flagship Forge"], ["hunter", "Boss Hunter"], ["legend", "Legendary Crafting"], ["cube", "Cube Event"], ["ultimate", "Ultimate Combination"]];
function pkLines(c) { const out = []; if (c.shards) out.push(`◆${fmt(c.shards)} Void Shards`);
  for (const [k, n] of Object.entries(c.items || {})) out.push(k === "boost" ? `${n} speed-ups (5 min)` : SHOP[k] ? `${esc(SHOP[k].n)}${n > 1 ? ` ×${n}` : ""}` : `${esc(k)} ×${n}`);
  for (const [m, t, n] of c.mats || []) if (FS_MATS[m]) out.push(`${FS_TIER[t][0]} ${esc(FS_MATS[m][0])} ×${n}`); return out; }
function packsLoad(force) { if (!window.udfShop || G.mode !== "online") return; if (G.pkBusy || (G.packs && !force && now() - G.packsAt < 60000)) return; G.pkBusy = 1;
  Promise.all([udfShop.packs(), udfShop.status()]).then(([P, st]) => { G.packs = (P || []).map(r => Object.assign({}, r.data, { id: r.id, once: r.once_per_account, tester: r.tester_eligible })); G.tstat = st || {}; G.packsAt = now(); G.pkErr = 0; },
    e => { G.pkErr = (e && e.message) || "offline"; }).then(() => { G.pkBusy = 0; if (sheet && sheet.type === "shop" && sheet.cat === "packs") renderSheet(); }); }
function packsBody() {
  if (!window.udfShop || G.mode !== "online") return `<p class="note">Packs are part of the online game. Sign in to see them.</p>`;
  if (!G.packs) { packsLoad(); return G.pkErr ? `<p class="note">Couldn't load the packs (${esc(G.pkErr)}). <button class="btn ghost sm" data-act="packsRetry">Try again</button></p>` : `<p class="note">Loading packs…</p>`; }
  const st = G.tstat || {}, tester = !!st.tester, claimed = st.claimed ? G.packs.find(p => p.id === st.claimed) : null;
  const head = tester ? `<div class="pktest"><b>Tester perk</b><span>${claimed ? `This week's free pack: <b>${esc(claimed.name)}</b>. Next one in <b data-end="${Date.parse(st.next_at)}">${ftime(Date.parse(st.next_at) - now())}</b>.` : "Pick any one pack below, free, once a week. Real purchases open when the game is on Google Play."}</span></div>`
    : `<div class="pktest"><b>Coming soon</b><span>Packs go on sale when the game launches on Google Play.</span></div>`;
  const card = p => { const c = p.contents || {}, ln = pkLines(c), can = tester && !claimed && p.tester;
    return `<div class="pkcard${p.family === "ultimate" ? " ult" : ""}"><div class="pkh"><b>${esc(p.name)}</b><span class="pkp">$${Number(p.priceUsd).toFixed(2)}</span></div>${p.blurb ? `<small>${esc(p.blurb)}</small>` : ""}
      <ul>${ln.map(l => `<li>${l}</li>`).join("")}</ul><div class="pkf"><span class="note">${p.valueShards ? `Worth ◆${fmt(p.valueShards)}` : ""}${p.once ? " · one per account" : ""}</span>
      ${can ? `<button class="btn amber sm" data-act="packClaim" data-k="${esc(p.id)}">Claim free</button>` : `<button class="btn sm" disabled>${tester ? "Claimed this week" : "Soon"}</button>`}</div></div>`; };
  return head + PK_FAM.map(([f, nm]) => { const L = G.packs.filter(p => p.family === f); return L.length ? `<h3 class="viph">${nm}</h3><div class="pkgrid">${L.map(card).join("")}</div>` : ""; }).join("");
}
function pkApply(c, sign) { const got = [];
  if (c.shards) { S.shards = Math.max(0, (S.shards || 0) + sign * c.shards); got.push(`◆${fmt(c.shards)}`); }
  for (const [k, n] of Object.entries(c.items || {})) { if (k === "boost") S.boosts = Math.max(0, (S.boosts || 0) + sign * n); else if (SHOP[k]) { if (sign > 0) giveItem(k, n); else { S.items = S.items || {}; S.items[k] = Math.max(0, (S.items[k] || 0) - n); } } else continue; got.push(k === "boost" ? `${n} speed-ups` : `${SHOP[k].n}${n > 1 ? ` ×${n}` : ""}`); }
  const mats = c.mats || []; if (mats.length) { if (sign > 0) fsDrop(mats, "a pack", { nocap: true }); else { const f = fsOf(); for (const [m, t, n] of mats) { const key = fsMatKey(m, t); f.mats[key] = Math.max(0, (f.mats[key] || 0) - n); } } }
  return got; }
async function packsDeliver() { if (!window.udfShop || G.mode !== "online" || !S || G.pkDel) return; G.pkDel = 1;
  try { const L = (await udfShop.mine()) || []; S.grants = S.grants || {}; S.grantsRev = S.grantsRev || {};
    for (const g of L) { const P = (G.packs || []).find(p => p.id === g.pack_id), nm = P ? P.name : g.pack_id;
      if (g.status === "granted") { if (!S.grants[g.id]) { const got = pkApply(g.contents || {}, 1); S.grants[g.id] = now(); dirty(); await flush(); note(`${nm} delivered: ${got.join(", ")}.`, "win"); try { SFX.fanfare(); } catch (e) {} }
        await udfShop.ack(g.id); }
      else if (g.status === "revoked") { if (!S.grantsRev[g.id]) { pkApply(g.contents || {}, -1); S.grantsRev[g.id] = now(); dirty(); await flush(); note(`${nm} was refunded, so its contents were taken back.`, "warn"); }
        await udfShop.ackRevoke(g.id); } }
  } catch (e) {} finally { G.pkDel = 0; } }
function shShop() {''')
# actions
rep('  dMore: () => {','''  packsRetry: () => { G.pkErr = 0; packsLoad(true); renderSheet(); },
  packClaim: d => act(async () => { const P = (G.packs || []).find(p => p.id === d.k); if (!P || G.pkClaiming) return; G.pkClaiming = 1;
    try { const r = await udfShop.claim(d.k); if (r && r.ok === false && r.reason === "already_claimed") toast("You've already claimed this week's tester pack.", "warn"); await packsDeliver(); }
    catch (e) { toast(e && e.code === "not_granted" ? "Only testers can claim free packs." : "Couldn't claim the pack. Check your connection and try again.", "warn"); }
    finally { G.pkClaiming = 0; G.packs = null; packsLoad(true); } }),
  dMore: () => {''')
# when the shop opens on packs, and a delivery check on start and every 10 minutes
rep('function shShop() {\n  const cat = sheet.cat || "boost",','function shShop() {\n  if (sheet.cat === "packs" && !G.pkSeen) { G.pkSeen = 1; packsDeliver(); }\n  const cat = sheet.cat || "boost",')
rep('window.udfBeforeSignOut = async () =>','setInterval(() => { try { packsDeliver(); } catch (e) {} }, 600000); setTimeout(() => { try { packsDeliver(); } catch (e) {} }, 20000); /* v342: owner grants and refunds arrive even if the shop is never opened */\nwindow.udfBeforeSignOut = async () =>')
# css
rep('.dmore{background:none;','.pktest{display:flex;flex-direction:column;gap:2px;padding:10px 12px;border-radius:12px;border:1px solid rgba(255,211,107,.5);background:linear-gradient(160deg,rgba(80,60,10,.35),rgba(6,18,30,.6));margin-bottom:6px}.pktest b{color:#ffd36b}.pkgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:8px}.pkcard{display:flex;flex-direction:column;gap:4px;padding:10px 12px;border-radius:12px;border:1px solid rgba(85,214,232,.35);background:linear-gradient(160deg,rgba(20,60,90,.35),rgba(6,18,30,.6))}.pkcard.ult{border-color:#ffd36b;box-shadow:0 0 14px rgba(255,211,107,.25)}.pkh{display:flex;justify-content:space-between;gap:8px;align-items:baseline}.pkh b{font-family:var(--f-display);font-size:15px}.pkp{color:#ffd36b;font-weight:700}.pkcard ul{margin:2px 0;padding-left:18px;font-size:12.5px;color:#cfe7f3}.pkf{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:auto}.dmore{background:none;')
open(p,"w").write(h); print("ok")
