# v362: "Claim free" looked broken: the claim worked, but nothing changed on screen for ~20 s (the server call, then a full cloud save
# before the pack was shown as delivered), and the button kept saying Claim free (a second tap was silently ignored).
#  - The tap answers at once: the button turns to "Claiming…" (disabled), then "Claimed ✓" as soon as the server confirms, with a toast.
#  - The pack's contents land in the empire right away and the "delivered" message shows at once; the cloud save follows, and the server
#    is still told only after the save (same crash safety: S.grants marks the grant, and an unsaved one is simply delivered again once).
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep('function pkBtn(p, big) { const { tester, claimed } = pkState(), can = tester && !claimed && p.tester;\n  return can ?',
    'function pkBtn(p, big) { const { tester, claimed } = pkState(), can = tester && !claimed && p.tester;\n  if (G.pkClaiming && G.pkClaimId === p.id) return `<button class="btn amber ${big ? "wide" : "sm"}" disabled>Claiming…</button>`; // v362\n  return can ?')
rep('''  packClaim: d => act(async () => { const P = (G.packs || []).find(p => p.id === d.k); if (!P || G.pkClaiming) return; G.pkClaiming = 1;
    try { const r = await udfShop.claim(d.k); if (r && r.ok === false && r.reason === "already_claimed") toast("You've already claimed this week's tester pack.", "warn"); await packsDeliver(); }
    catch (e) { toast(e && e.code === "not_granted" ? "Only testers can claim free packs." : "Couldn't claim the pack. Check your connection and try again.", "warn"); }
    finally { G.pkClaiming = 0; const keep = G.packs; packsLoad(true); G.packs = keep; } }),''',
    '''  packClaim: d => act(async () => { const k = d.k, P = (G.packs || []).find(p => p.id === k); if (!P) return; if (G.pkClaiming) return toast("Claiming your pack…"); // the button's data changes when the card redraws: read it first
    G.pkClaiming = 1; G.pkClaimId = k; if (sheet) renderSheet(); // v362 the tap answers at once
    try { const r = await udfShop.claim(k);
      if (r && r.ok === false && r.reason === "already_claimed") toast("You've already claimed this week's tester pack.", "warn");
      else { G.tstat = Object.assign({}, G.tstat, { claimed: k }); toast(`${P.name} claimed! Adding it to your empire…`, "win"); }
      G.pkClaiming = 0; if (sheet) renderSheet(); await packsDeliver(); }
    catch (e) { toast(e && e.code === "not_granted" ? "Only testers can claim free packs." : "Couldn't claim the pack. Check your connection and try again.", "warn"); }
    finally { G.pkClaiming = 0; G.pkClaimId = null; const keep = G.packs; packsLoad(true); G.packs = keep; if (sheet) renderSheet(); } }),''')
rep('if (!S.grants[g.id]) { const got = pkApply(g.contents || {}, 1); S.grants[g.id] = now(); dirty(); await flush(); note(`${nm} delivered: ${got.join(", ")}.`, "win"); try { SFX.fanfare(); } catch (e) {} }',
    'if (!S.grants[g.id]) { const got = pkApply(g.contents || {}, 1); S.grants[g.id] = now(); dirty(); note(`${nm} delivered: ${got.join(", ")}.`, "win"); try { SFX.fanfare(); } catch (e) {} render(true); if (sheet) renderSheet(); await flush(); } // v362 shown at once, saved right after')
# the security check reversed any pack worth over 2,500 shards ("Void Shards jumped… reversed"): a pack's shards move its baseline too
rep('function pkApply(c, sign) { const got = [];\n  if (c.shards) { S.shards = Math.max(0, (S.shards || 0) + sign * c.shards); got.push(`◆${fmt(c.shards)}`); }',
    'function pkApply(c, sign) { const got = [];\n  if (c.shards) { S.shards = Math.max(0, (S.shards || 0) + sign * c.shards); if (SEC.base) SEC.base.sh = Math.max(0, SEC.base.sh + sign * c.shards); got.push(`◆${fmt(c.shards)}`); } // v362 a pack is no cheat')
# one-time repair: give back shards that check took from a pack delivered just before it, and drop the strike
rep('async function packsDeliver() {', r'''/* v362 repair, once: the security check reversed the shards of packs worth over 2,500. Each "jumped" reversal logged within two minutes of a
   pack delivery is credited back and its strike removed. */
function packShardFix() { if (!S || S.pkShFix || G.mode !== "online" || !(store && store.ready)) return; S.pkShFix = 1; const inc = (S.sec && S.sec.inc) || [], gt = Object.values(S.grants || {}); let back = 0;
  for (const x of inc) { if (x.kind !== "shards" || x.fixed) continue; const m = /jumped by ([\d,]+)/.exec(x.txt || ""); if (!m) continue; const n = +m[1].replace(/,/g, "");
    if (!gt.some(t => Math.abs(t - x.t) < 120000)) continue; S.shards = (S.shards || 0) + n; if (SEC.base) SEC.base.sh += n; back += n; x.fixed = 1; x.fix = "Restored: it was a pack, not a cheat."; S.sec.strikes = Math.max(0, (S.sec.strikes || 0) - 1); }
  if (back) { note(`Restored ◆${fmt(back)} Void Shards from your pack that the security check had wrongly taken back. Sorry about that!`, "win"); dirty(); } }
async function packsDeliver() { try { packShardFix(); } catch (e) {}''')
open(p, "w").write(h); print("ok")
