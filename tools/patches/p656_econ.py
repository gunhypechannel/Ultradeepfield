# v656 shop economy (owner: "It feels too easy to unlock all ships with shards", "Build the rest of the changes"). Resources were about
# seven times cheaper than time: a day of the whole empire's production cost 40 shards while an hour of speed-up costs 6-10. Now:
# (1) resources are priced like time, about three times what they were (Supply Pod 40 -> 150, crates 4/5/6 -> 12/14/16, pods
# 5/15/36 -> 15/45/110); (2) each resource item can be bought 3 times a UTC day; (3) a pod or crate fills storage up to its limit and
# no further, and waits in the inventory if storage is already full. Pods won from events, the wheel and packs are not limited.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
rep('const crateAmt = () =>', r'''/* v656 a pod or crate fills storage up to its limit, no further; nothing fits, nothing is used */
function podAdd(r, a) { let cap = Infinity; try { cap = caps()[r]; } catch (e) {} const room = Math.max(0, cap - (S.res[r] || 0)), g = Math.min(a, room); S.res[r] = (S.res[r] || 0) + g; return g; }
function podMsg(got, want, what) { if (got <= 0) { toast(`${RN_FULL(what)} storage is full. Build more storage, or spend some first.`, "warn"); return null; } return got < want ? `${fmt(got)} ${what} delivered. Storage is now full: the rest didn't fit.` : null; }
const RN_FULL = w => w.charAt(0).toUpperCase() + w.slice(1);
const POD_DAY = 3; /* v656 each resource item: three a day from the shop */
const podLeft = k => { const d = utcDay(), P = S.podBuy; return POD_DAY - (P && P.d === d ? P.n[k] || 0 : 0); };
const crateAmt = () =>''')
rep('''use: () => { S.res.m += crateAmt(); return "Metal crate unpacked."; } },''', '''use: () => { const a = crateAmt(), g = podAdd("m", a); return g > 0 ? podMsg(g, a, "metal") || "Metal crate unpacked." : podMsg(0, a, "metal"); } },''')
rep('''use: () => { S.res.c += Math.round(crateAmt() * .7); return "Crystal crate unpacked."; } },''', '''use: () => { const a = Math.round(crateAmt() * .7), g = podAdd("c", a); return g > 0 ? podMsg(g, a, "crystal") || "Crystal crate unpacked." : podMsg(0, a, "crystal"); } },''')
rep('''use: () => { S.res.g += Math.round(crateAmt() * .4); return "Gas crate unpacked."; } },''', '''use: () => { const a = Math.round(crateAmt() * .4), g = podAdd("g", a); return g > 0 ? podMsg(g, a, "gas") || "Gas crate unpacked." : podMsg(0, a, "gas"); } },''')
rep('crateM:   { n: "Metal Crate", ic: "m", cost: 4,', 'crateM:   { n: "Metal Crate", ic: "m", cost: 12,')
rep('crateC:   { n: "Crystal Crate", ic: "c", cost: 5,', 'crateC:   { n: "Crystal Crate", ic: "c", cost: 14,')
rep('crateG:   { n: "Gas Crate", ic: "g", cost: 6,', 'crateG:   { n: "Gas Crate", ic: "g", cost: 16,')
rep('''cost: [5, 15, 36][i], d: () => `${fmt(amt())} ${RN[r][0].toLowerCase()} (${h} hours of production) for your homeworld.`, use: () => { const a = amt(); S.res[r] += a; return `${fmt(a)} ${RN[r][0].toLowerCase()} delivered.`; } }; });''',
    '''cost: [15, 45, 110][i], /* v656 x3 */ d: () => `${fmt(amt())} ${RN[r][0].toLowerCase()} (${h} hours of production) for your homeworld, up to its storage limit.`, use: () => { const a = amt(), w = RN[r][0].toLowerCase(), g = podAdd(r, a); return g > 0 ? podMsg(g, a, w) || `${fmt(g)} ${w} delivered.` : podMsg(0, a, w); } }; });''')
rep('''SHOP.pAll_gold = { cat: "res", tier: 2, col: ITIERS[2][2], n: "Complete Supply Pod", ic: "▣", cost: 40, d: () => "24 hours of metal, crystal and gas production at once.", use: () => { const R0 = rates(); for (const r of ["m", "c", "g"]) S.res[r] += Math.max(6000, Math.round(R0[r] * 1440)); return "Complete supply pod unpacked."; } };''',
    '''SHOP.pAll_gold = { cat: "res", tier: 2, col: ITIERS[2][2], n: "Complete Supply Pod", ic: "▣", cost: 150, /* v656 (was 40) */ d: () => "24 hours of metal, crystal and gas production at once, up to your storage limits.", use: () => { const R0 = rates(); let got = 0, full = 0; for (const r of ["m", "c", "g"]) { const a = Math.max(6000, Math.round(R0[r] * 1440)), g = podAdd(r, a); got += g; if (g < a) full = 1; } if (got <= 0) { toast("Your storage is full. Build more storage, or spend some first.", "warn"); return null; } return full ? "Supply pod unpacked. Some storage is now full: what didn't fit was lost." : "Complete supply pod unpacked."; } };''')
rep('''  buy: d => act(() => { const s = SHOP[d.k]; if (!s || !s.cost) return; if ((S.shards || 0) < s.cost) return toast(`That costs ◆${s.cost}.`, "warn"); S.shards -= s.cost;''',
    '''  buy: d => act(() => { const s = SHOP[d.k]; if (!s || !s.cost) return; if (s.cat === "res" && podLeft(d.k) <= 0) return toast(`${s.n}: ${POD_DAY} a day from the shop. More tomorrow (UTC midnight).`, "warn"); if ((S.shards || 0) < s.cost) return toast(`That costs ◆${s.cost}.`, "warn"); S.shards -= s.cost;
    if (s.cat === "res") { const dd = utcDay(); if (!S.podBuy || S.podBuy.d !== dd) S.podBuy = { d: dd, n: {} }; S.podBuy.n[d.k] = (S.podBuy.n[d.k] || 0) + 1; } /* v656 */''')
rep("""  const buyBtn = (k, s, c) => s.cost ? `<button class="btn amber sm" data-act="buy" data-k="${k}" ${sh >= (c || s.cost) ? "" : "disabled"}>◆${c || s.cost}</button>` :""",
    """  const buyBtn = (k, s, c) => s.cost ? (s.cat === "res" ? `<small class="podl${podLeft(k) > 0 ? "" : " out"}">${Math.max(0, podLeft(k))}/${POD_DAY} today</small>` : "") + `<button class="btn amber sm" data-act="buy" data-k="${k}" ${sh >= (c || s.cost) && !(s.cat === "res" && podLeft(k) <= 0) ? "" : "disabled"}>◆${c || s.cost}</button>` :""")
rep('.chipq.met{', '.podl{display:block;font-size:10.5px;color:var(--muted);text-align:center;margin-bottom:2px;white-space:nowrap}.podl.out{color:#ff8a7a}\n.chipq.met{')
rep('const GAME_V = 655', 'const GAME_V = 656')
open(p, 'w', encoding='utf-8').write(s)
