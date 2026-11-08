# v343 shop remaster: pack art, featured row, a preview sheet per pack, and the owner's pack tools (grant, revoke, testers).
p="docs/udf-supabase.js"; s=open(p).read()
a="    ackRevoke: function (id) { return need().then(function () { return run(sb.rpc(\"ack_revoke\", { p_id: id })); }); }"
assert s.count(a)==1
s=s.replace(a, a+""",
    adminList: function () { return need().then(function () { return run(sb.rpc("admin_list")); }); },
    adminGrant: function (uid, pack, key, note) { return need().then(function () { return run(sb.rpc("admin_grant", { p_uid: uid, p_pack: pack, p_key: key, p_note: note || null })); }); },
    adminRevoke: function (id, note) { return need().then(function () { return run(sb.rpc("admin_revoke", { p_id: id, p_note: note || null })); }); },
    testerSet: function (uid, on, note) { return need().then(function () { return run(sb.rpc("tester_set", { p_uid: uid, p_on: !!on, p_note: note || null })); }); }""")
open(p,"w").write(s)

p="docs/index.html"; h=open(p).read()
def rep(a,b,n=1):
    global h; c=h.count(a); assert c==n,(c,a[:80]); h=h.replace(a,b)
rep('const cat = sheet.cat || "boost"','const cat = sheet.cat = sheet.cat || (window.udfShop && G.mode === "online" ? "packs" : "boost")')
rep('shop: shShop','shop: shShop, pack: shPack, packadmin: shPackAdmin')
rep('SHEET_NAME = { ','SHEET_NAME = { shop: "shop", pack: "pack", packadmin: "owner tools", ')
# new body: featured row + art cards; card opens the preview
a=h[h.index("function packsBody() {"):h.index("function pkApply(")]
b='''const PK_TIER = { intro: ["Starter", "#9fd6ff"], starter: ["Starter", "#9fd6ff"], standard: ["Standard", "#55d6e8"], advanced: ["Advanced", "#b46cff"], premium: ["Premium", "#ffa63a"], ultimate: ["Ultimate", "#ffd36b"], pouch: ["", "#c9a6ff"], satchel: ["", "#c9a6ff"], crate: ["", "#c9a6ff"], vault: ["", "#c9a6ff"], hoard: ["", "#c9a6ff"], treasury: ["", "#ffd36b"] };
const PK_FEAT = ["starter_pack", "forge_adv", "ultimate"];
const pkArt = p => p.family === "shards" ? `art/packs/pack-shards-${p.tier}.webp?v=1` : `art/packs/pack-${p.family}.webp?v=1`;
function pkState() { const st = G.tstat || {}, tester = !!st.tester, claimed = st.claimed ? (G.packs || []).find(p => p.id === st.claimed) : null; return { st, tester, claimed }; }
function pkBtn(p, big) { const { tester, claimed } = pkState(), can = tester && !claimed && p.tester;
  return can ? `<button class="btn amber ${big ? "wide" : "sm"}" data-act="packClaim" data-k="${esc(p.id)}">Claim free</button>` : `<button class="btn ${big ? "wide" : "sm"}" disabled>${tester ? (claimed && claimed.id === p.id ? "Claimed ✓" : "Claimed this week") : "Coming soon"}</button>`; }
function pkCard(p, feat) { const t = PK_TIER[p.tier] || ["", "#55d6e8"];
  return `<div class="pkcard${feat ? " feat" : ""}" style="--pt:${t[1]}" data-act="packOpen" data-k="${esc(p.id)}" role="button" tabindex="0"><div class="pkart" style="background-image:url(${pkArt(p)})"><span class="pkp">$${Number(p.priceUsd).toFixed(2)}</span>${t[0] ? `<i class="pkt">${t[0]}</i>` : ""}</div>
    <div class="pkb"><b>${esc(p.name)}</b>${p.blurb ? `<small>${esc(p.blurb)}</small>` : ""}<div class="pkf"><span class="note">${p.valueShards ? `Worth ◆${fmt(p.valueShards)}` : ""}${p.once ? " · once" : ""}</span>${pkBtn(p)}</div></div></div>`; }
function packsBody() {
  if (!window.udfShop || G.mode !== "online") return `<p class="note">Packs are part of the online game. Sign in to see them.</p>`;
  if (!G.packs) { packsLoad(); return G.pkErr ? `<p class="note">Couldn't load the packs (${esc(G.pkErr)}). <button class="btn ghost sm" data-act="packsRetry">Try again</button></p>` : `<p class="note">Loading packs…</p>`; }
  const { st, tester, claimed } = pkState();
  const head = tester ? `<div class="pktest"><b>Tester perk</b><span>${claimed ? `This week's free pack: <b>${esc(claimed.name)}</b>. Next one in <b data-end="${Date.parse(st.next_at)}">${ftime(Date.parse(st.next_at) - now())}</b>.` : "Pick any one pack below, free, once a week. Real purchases open when the game is on Google Play."}</span></div>`
    : `<div class="pktest"><b>Coming soon</b><span>Packs go on sale when the game launches on Google Play.</span></div>`;
  const feat = PK_FEAT.map(id => G.packs.find(p => p.id === id)).filter(Boolean);
  return head + (feat.length ? `<h3 class="viph">Featured</h3><div class="pkfeat">${feat.map(p => pkCard(p, 1)).join("")}</div>` : "")
    + PK_FAM.map(([f, nm]) => { const L = G.packs.filter(p => p.family === f); return L.length ? `<h3 class="viph">${nm}</h3><div class="pkgrid">${L.map(p => pkCard(p)).join("")}</div>` : ""; }).join("")
    + (G.owner ? `<button class="btn ghost wide" data-act="packAdmin">Owner tools: grant, refund and testers</button>` : "");
}
function shPack() { const p = (G.packs || []).find(x => x.id === sheet.id); if (!p) return `<div class="hd"><h2>Pack</h2><button class="x" data-act="close" aria-label="Close">✕</button></div><p class="note">This pack isn't available.</p>`;
  const t = PK_TIER[p.tier] || ["", "#55d6e8"], c = p.contents || {};
  const rows = [];
  if (c.shards) rows.push(`<li><span class="pki shard">◆</span><b>${fmt(c.shards)}</b> Void Shards</li>`);
  for (const [k, n] of Object.entries(c.items || {})) { const s = SHOP[k]; rows.push(k === "boost" ? `<li><span class="pki">⚡</span><b>×${n}</b> Speed-ups (5 min each)</li>` : s ? `<li><span class="pki" style="color:${s.col || "#55d6e8"}">${s.ic.length === 1 && "mcg".includes(s.ic) ? RI[s.ic] : s.ic}</span><b>×${n}</b> ${esc(s.n)}<small>${typeof s.d === "function" ? s.d() : ""}</small></li>` : ""); }
  for (const [m, tt, n] of c.mats || []) if (FS_MATS[m]) rows.push(`<li><i class="fsmi lg fsmat-${m}" style="--tc:${FS_TIER[tt][1]}"></i><b>×${n}</b> ${FS_TIER[tt][0]} ${esc(FS_MATS[m][0])}</li>`);
  return `<div class="pkhero" style="--pt:${t[1]};background-image:url(${pkArt(p)})"><button class="x" data-act="close" aria-label="Close">✕</button><div><small>${esc(p.familyName || "")}${t[0] ? " · " + t[0] : ""}</small><h2>${esc(p.name)}</h2></div><span class="pkp">$${Number(p.priceUsd).toFixed(2)}</span></div>
    ${p.blurb ? `<p class="note">${esc(p.blurb)}</p>` : ""}<h3 class="viph">Contents</h3><ul class="pkcont">${rows.join("")}</ul>
    <p class="note">${p.valueShards ? `Worth about ◆${fmt(p.valueShards)} at shop prices.` : ""}${p.once ? " One per account." : ""}</p>${pkBtn(p, 1)}`; }
/* ---------- owner pack tools: give any commander a pack (compensation, prizes), take back a refunded one, manage the tester list ---------- */
function pkAdminLoad() { if (G.pkAdmBusy) return; G.pkAdmBusy = 1; udfShop.adminList().then(r => { G.pkAdm = r; G.pkAdmErr = 0; }, e => { G.pkAdmErr = (e && e.message) || "error"; }).then(() => { G.pkAdmBusy = 0; if (sheet && sheet.type === "packadmin") renderSheet(); }); }
function shPackAdmin() {
  const hd = `<div class="hd"><div><div class="chapter">Owner</div><h2>Pack tools</h2></div><button class="x" data-act="close" aria-label="Close">✕</button></div>`;
  if (!G.owner) return hd + `<p class="note">Only the game's owner can use these.</p>`;
  if (!G.pkAdm) { pkAdminLoad(); return hd + (G.pkAdmErr ? `<p class="note">Couldn't load (${esc(G.pkAdmErr)}).</p>` : `<p class="note">Loading…</p>`); }
  const A = G.pkAdm, T = new Set((A.testers || []).map(t => t.uid)), who = Object.entries(G.players || {}).filter(([u, v]) => v && !isBot(u)).map(([u, v]) => [u, v.name || G.names[u] || u.slice(0, 8)]).sort((a, b) => String(a[1]).localeCompare(String(b[1])));
  const opts = who.map(([u, n]) => `<option value="${esc(u)}">${esc(n)}</option>`).join(""), popts = (G.packs || []).map(p => `<option value="${esc(p.id)}">${esc(p.name)} ($${Number(p.priceUsd).toFixed(2)})</option>`).join("");
  return hd + `<section class="pkadm"><h3 class="viph">Give a pack</h3><select id="pkaU">${opts}</select><select id="pkaP">${popts}</select><input id="pkaN" maxlength="120" placeholder="Note (why), optional"><button class="btn amber wide" data-act="pkaGrant">Give pack</button>
    <p class="note">It arrives in their game within 10 minutes, or as soon as they open the shop.</p></section>
    <h3 class="viph">Recent grants</h3><div class="pkrows">${(A.grants || []).map(g => `<div class="pkrow ${g.status}"><span><b>${esc(g.commander)}</b> · ${esc(((G.packs || []).find(p => p.id === g.pack_id) || {}).name || g.pack_id)}<small>${esc(g.source)} · ${esc(g.status)} · ${new Date(g.created_at).toLocaleDateString()}${g.note ? " · " + esc(g.note) : ""}</small></span>${g.status !== "revoked" ? `<button class="btn ghost sm" data-act="pkaRevoke" data-id="${esc(g.id)}">Take back</button>` : ""}</div>`).join("") || `<p class="note">No grants yet.</p>`}</div>
    <h3 class="viph">Testers · ${T.size}</h3><div class="pkrows">${(A.testers || []).map(t => `<div class="pkrow"><span><b>${esc(t.commander)}</b></span><button class="btn ghost sm" data-act="pkaTester" data-u="${esc(t.uid)}" data-on="0">Remove</button></div>`).join("")}
    ${who.filter(([u]) => !T.has(u)).map(([u, n]) => `<div class="pkrow"><span>${esc(n)}</span><button class="btn sm" data-act="pkaTester" data-u="${esc(u)}" data-on="1">Make tester</button></div>`).join("")}</div>`;
}
'''
h=h.replace(a,b)
rep('  packsRetry: () => {','''  packOpen: d => { if (G.packs && G.packs.find(p => p.id === d.k)) openSheet({ type: "pack", id: d.k }); },
  packAdmin: () => { G.pkAdm = null; openSheet({ type: "packadmin" }); },
  pkaGrant: d => act(async () => { const u = ($("#pkaU") || {}).value, pk = ($("#pkaP") || {}).value, note = (($("#pkaN") || {}).value || "").trim(); if (!u || !pk) return;
    try { const r = await udfShop.adminGrant(u, pk, "owner:" + u + ":" + Date.now(), note || "owner gift"); toast(r && r.ok ? "Pack given." : "That grant already exists.", r && r.ok ? "win" : "warn"); } catch (e) { toast("Couldn't give the pack: " + ((e && e.message) || "error"), "warn"); }
    G.pkAdm = null; pkAdminLoad(); }),
  pkaRevoke: d => act(async () => { if (!confirm("Take this pack back? Its contents are removed from the player's game the next time it checks in.")) return;
    try { await udfShop.adminRevoke(d.id, "owner refund"); toast("Pack taken back.", "win"); } catch (e) { toast("Couldn't take it back.", "warn"); } G.pkAdm = null; pkAdminLoad(); }),
  pkaTester: d => act(async () => { try { await udfShop.testerSet(d.u, d.on === "1"); } catch (e) { toast("Couldn't change the tester list.", "warn"); } G.pkAdm = null; pkAdminLoad(); }),
  packsRetry: () => {''')
# claim from the preview sheet: refresh both
rep('finally { G.pkClaiming = 0; G.packs = null; packsLoad(true); } }),','finally { G.pkClaiming = 0; const keep = G.packs; packsLoad(true); G.packs = keep; } }),')
# css
rep('.pkgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:8px}.pkcard{display:flex;flex-direction:column;gap:4px;padding:10px 12px;border-radius:12px;border:1px solid rgba(85,214,232,.35);background:linear-gradient(160deg,rgba(20,60,90,.35),rgba(6,18,30,.6))}.pkcard.ult{border-color:#ffd36b;box-shadow:0 0 14px rgba(255,211,107,.25)}.pkh{display:flex;justify-content:space-between;gap:8px;align-items:baseline}.pkh b{font-family:var(--f-display);font-size:15px}.pkp{color:#ffd36b;font-weight:700}.pkcard ul{margin:2px 0;padding-left:18px;font-size:12.5px;color:#cfe7f3}.pkf{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:auto}',
 '.pkgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}.pkfeat{display:grid;grid-auto-flow:column;grid-auto-columns:min(82%,340px);gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:4px}.pkfeat>.pkcard{scroll-snap-align:start}'
 '.pkcard{display:flex;flex-direction:column;border-radius:14px;overflow:hidden;border:1px solid color-mix(in srgb,var(--pt) 60%,transparent);background:linear-gradient(160deg,rgba(20,60,90,.35),rgba(6,18,30,.7));box-shadow:0 0 14px color-mix(in srgb,var(--pt) 22%,transparent);cursor:pointer}.pkcard:active{transform:scale(.985)}'
 '.pkart{position:relative;aspect-ratio:16/9;background:#05090f center/cover no-repeat}.pkcard.feat .pkart{aspect-ratio:16/8}.pkart .pkp{position:absolute;right:8px;bottom:8px;padding:3px 9px;border-radius:999px;background:rgba(3,10,18,.78);border:1px solid rgba(255,211,107,.6);color:#ffd36b;font-weight:800;font-size:14px}'
 '.pkt{position:absolute;left:8px;top:8px;padding:2px 8px;border-radius:6px;background:var(--pt);color:#06121c;font-style:normal;font-weight:800;font-size:11px;letter-spacing:.06em;text-transform:uppercase}'
 '.pkb{display:flex;flex-direction:column;gap:3px;padding:9px 11px 10px;flex:1}.pkb b{font-family:var(--f-display);font-size:15.5px}.pkb small{color:#a9c4d8;font-size:12.5px}.pkf{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-top:auto;padding-top:4px}'
 '.pkhero{position:relative;display:flex;align-items:flex-end;justify-content:space-between;gap:10px;min-height:190px;margin:-16px -16px 0;padding:14px 16px;background:#05090f center/cover no-repeat;border-bottom:2px solid var(--pt)}.pkhero:before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 35%,rgba(3,8,16,.92))}.pkhero>*{position:relative}.pkhero .x{position:absolute;top:10px;right:10px}.pkhero small{color:var(--pt);font-weight:700;letter-spacing:.05em;text-transform:uppercase;font-size:11.5px}.pkhero h2{margin:2px 0 0}.pkhero .pkp{color:#ffd36b;font-weight:800;font-size:18px}'
 '.pkcont{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px}.pkcont li{display:grid;grid-template-columns:30px auto 1fr;align-items:center;gap:8px;padding:6px 8px;border-radius:10px;background:rgba(6,18,30,.55);border:1px solid rgba(85,214,232,.18);font-size:13.5px}.pkcont li small{grid-column:2/-1;color:#8fb1c6;font-size:11.5px}.pki{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;font-size:18px}.pki svg{width:24px;height:24px}.pki.shard{color:#c9a6ff}'
 '.pkadm{display:flex;flex-direction:column;gap:8px}.pkadm select,.pkadm input{width:100%;padding:9px 10px;border-radius:10px;border:1px solid rgba(85,214,232,.35);background:rgba(0,0,0,.35);color:#e8f6ff;font:inherit}.pkrows{display:flex;flex-direction:column;gap:6px}.pkrow{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:7px 10px;border-radius:10px;background:rgba(6,18,30,.55);border:1px solid rgba(85,214,232,.18)}.pkrow small{display:block;color:#8fb1c6;font-size:11.5px}.pkrow.revoked{opacity:.55}')
rep('if (sheet && sheet.type === "shop" && sheet.cat === "packs") renderSheet(); }); }','if (sheet && ((sheet.type === "shop" && sheet.cat === "packs") || sheet.type === "pack")) renderSheet(); }); }')
open(p,"w").write(h); print("ok")
