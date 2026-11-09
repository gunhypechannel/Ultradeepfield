# v367: "Use all" in the Void Shop inventory. Shown for items you hold more than one of whose effect adds up (resource crates and packs,
# production boosts, VIP time and points, officers, building fields, runes, +5 boosts). Material boxes open their picker once and the pick
# applies to every box. Speed-ups, licences, repair kits, Pirate Intel and Star Charts act once on one target, so they keep a single Use.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep('${s.use ? `<button class="btn sm" data-act="useItem" data-k="${k}">Use</button>` :',
    '${s.use ? `<span class="useb">${it[k] > 1 && useAllOk(k) ? `<button class="btn ghost sm" data-act="useAll" data-k="${k}">Use all</button>` : ""}<button class="btn sm" data-act="useItem" data-k="${k}">Use</button></span>` :')
rep("  useItem: d => act(() => {", r'''  useAll: d => act(() => { const s = SHOP[d.k]; if (!s || !s.use || !useAllOk(d.k)) return; const n0 = (S.items || {})[d.k] || 0; if (n0 < 1) return; // v367
    if (s.mbT) return openSheet({ type: "matbox", k: d.k, all: 1 });
    let n = 0, last = ""; while ((S.items[d.k] || 0) > 0 && n < 9999) { S.items[d.k]--; const msg = s.use(); if (!msg) { S.items[d.k]++; break; } n++; last = msg; }
    if (n) toast(n > 1 ? `Used ${n} × ${s.n}.` : last, "win"); }),
  useItem: d => act(() => {''')
rep("function grantRunes(n, why) {", '''/* v367 items whose effect adds up, so using them all at once is safe */
const USEALL_CAT = new Set(["res", "vip", "boost", "planet", "officer", "legacy", "forge"]);
const useAllOk = k => { const s = SHOP[k]; return !!(s && s.use && (USEALL_CAT.has(s.cat) || k === "boost5")); };
function grantRunes(n, why) {''')
# material boxes: the picker takes every box when opened from Use all
rep('<p class="note">Pick one: you get ${MB_N[tt]} × ${FS_TIER[tt][0]} of it.</p>',
    '<p class="note">${sheet.all && (S.items || {})[sheet.k] > 1 ? `Pick one for all ${S.items[sheet.k]} boxes: you get ${fmt(MB_N[tt] * S.items[sheet.k])} × ${FS_TIER[tt][0]} of it.` : `Pick one: you get ${MB_N[tt]} × ${FS_TIER[tt][0]} of it.`}</p>')
rep("S.items[k]--; dirty(); closeSheet(); fsDrop([[d.v, tt, MB_N[tt]]], s.n, { nocap: 1 }); },",
    "const n = sheet.all ? S.items[k] : 1; S.items[k] -= n; dirty(); closeSheet(); fsDrop([[d.v, tt, MB_N[tt] * n]], n > 1 ? `${n} × ${s.n}` : s.n, { nocap: 1 }); },")
open(p, "w").write(h); print("ok")
h = open(p).read()
rep(".sbuy .own{font-size:11px;color:var(--cyan)}", ".sbuy .own{font-size:11px;color:var(--cyan)}.sbuy .useb{display:flex;gap:6px;margin-left:auto}")
open(p, "w").write(h); print("ok css")
