# v647 Fleet captains (owner's friend: "fleet avatars with different outfits or races"; owner: "Build it all!"). Eight captains,
# painted from the commander portraits: the Admiral serves from the start, the rest are recruited once with shards. Pick one on any
# launch screen; each leads one fleet at a time and brings a perk (speed, fuel, cargo, loot, or a better chance of eggs on hunts).
# The captain's portrait rides on the fleet card.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)

rep('function fuelFor(from, to, n, pct = 100) {', r'''/* ---------- v647 fleet captains ---------- */
const CAPS = { admiral: { cost: 0, cargo: 1.1, perk: "+10% cargo" }, pilot: { cost: 40, spd: .15, perk: "15% faster flights" }, marine: { cost: 60, spd: .08, cargo: 1.1, perk: "8% faster, +10% cargo" },
  spy: { cost: 40, fuel: .25, perk: "−25% fuel" }, warlord: { cost: 90, loot: 1.15, perk: "+15% loot from pirates and monsters" }, mystic: { cost: 90, egg: 2, perk: "Double the chance of eggs on monster hunts" },
  cyborg: { cost: 70, cargo: 1.25, perk: "+25% cargo" }, android: { cost: 70, spd: .08, fuel: .15, perk: "8% faster, −15% fuel" } };
const capName = k => ((typeof AV_LIST !== "undefined" && AV_LIST.find(a => a[0] === k)) || [k, k])[1];
const capOwned = k => !!CAPS[k] && (CAPS[k].cost === 0 || !!((S && S.caps) || {})[k]);
const capBusy = k => !!(S && (S.fleets || []).some(f => f.cap === k));
const capCur = () => { if (!S) return null; const k = CAPS[S.capSel] ? S.capSel : "admiral"; return capOwned(k) && !capBusy(k) ? k : null; };
const capSpdNow = () => { const k = capCur(); return k ? CAPS[k].spd || 0 : 0; }, capFuelNow = () => { const k = capCur(); return k ? CAPS[k].fuel || 0 : 0; };
const fCargo = f => cargoOf(f.n) * ((f && CAPS[f.cap] && CAPS[f.cap].cargo) || 1);
const capLoot = (f, L) => { const m = (f && CAPS[f.cap] && CAPS[f.cap].loot) || 1; return m === 1 ? L : { m: Math.round(L.m * m), c: Math.round(L.c * m), g: Math.round(L.g * m) }; };
function capRow() { if (!S) return ""; const cur = CAPS[S.capSel] ? S.capSel : "admiral", act = capCur();
  return `<div class="caprow"><div class="caph"><span class="note">Captain</span><b>${act ? `${esc(capName(act))} · <em>${esc(CAPS[act].perk)}</em>` : capBusy(cur) ? `${esc(capName(cur))} is leading another fleet` : "No captain"}</b></div><div class="caps">`
    + Object.keys(CAPS).map(k => { const own = capOwned(k), busy = capBusy(k), on = k === cur, ak = "cap|" + k;
      return own ? `<button class="cap${on ? " on" : ""}${busy ? " busy" : ""}" data-act="capSel" data-k="${k}" title="${esc(capName(k) + ": " + CAPS[k].perk)}"><img src="avatars/${k}.webp" alt=""><small>${busy ? "In flight" : esc(capName(k).replace(/^The /, ""))}</small></button>`
        : `<button class="cap lk${buyArmed(ak) ? " pxarm" : ""}" data-act="capBuy" data-k="${k}" title="${esc(capName(k) + ": " + CAPS[k].perk)}"><img src="avatars/${k}.webp" alt=""><small>${buyArmed(ak) ? "Confirm" : "◆" + CAPS[k].cost}</small></button>`; }).join("") + `</div></div>`; }
function fuelFor(from, to, n, pct = 100) {''')
# perks: speed and fuel for the fleet being launched, cargo and loot for the fleet in flight
rep('* (r === S.r ? 1 + fsB("spd") / 100 + buffPct("bf") / 100 /* v534 */ : 1)', '* (r === S.r ? 1 + fsB("spd") / 100 + buffPct("bf") / 100 /* v534 */ + capSpdNow() /* v647 */ : 1)')
rep('* (1 - fsB("fuel") / 100));', '* (1 - fsB("fuel") / 100) * (1 - capFuelNow()));')
n0 = s.count('cargoOf(f.n)'); s = s.replace('cargoOf(f.n)', 'fCargo(f)'); print('cargo sites:', n0)
rep('const fCargo = f => fCargo(f) *', 'const fCargo = f => cargoOf(f.n) *')
rep('    const L = xLoot(x), cap = fCargo(f), ratio = Math.min(1, cap / total(L));', '    const L = capLoot(f, xLoot(x)), cap = fCargo(f), ratio = Math.min(1, cap / total(L));')
rep('if (x.mon) try { xsEggDrop(x, rep); } catch (e) {}', 'if (x.mon) try { xsEggDrop(x, rep, f); } catch (e) {}')
rep('function xsEggDrop(x, rep) {', 'function xsEggDrop(x, rep, f) {')
rep('if (Math.random() >= XS_DROP * (isElite(x) ? 2 : 1)) return;', 'if (Math.random() >= XS_DROP * (isElite(x) ? 2 : 1) * ((f && CAPS[f.cap] && CAPS[f.cap].egg) || 1)) return;')
rep('  if (!f.form && sheet && FORMS[sheet.form]) f.form = sheet.form; // v274', '  if (mission !== "spy" && !f.cap) { const ck = capCur(); if (ck) f.cap = ck; } /* v647 */\n  if (!f.form && sheet && FORMS[sheet.form]) f.form = sheet.form; // v274')
# launch screens and fleet cards
rep('''`<button class="${launchForm() === k ? "on" : ""}" data-act="launchForm" data-v="${k}" title="${esc(F.d)}">${F.ic} ${F.n}</button>`).join("")}</div></div>`;''',
    '''`<button class="${launchForm() === k ? "on" : ""}" data-act="launchForm" data-v="${k}" title="${esc(F.d)}">${F.ic} ${F.n}</button>`).join("")}</div>${capRow()}</div>`;''')
rep('return `<div class="fcard"><div class="top"><b>${fleetLabel(f)} · ${esc(tg ? tg.name : "—")}</b>',
    'return `<div class="fcard"><div class="top"><b>${CAPS[f.cap] ? `<img class="fcap" src="avatars/${f.cap}.webp" alt="" title="${esc(capName(f.cap))}">` : ""}${fleetLabel(f)} · ${esc(tg ? tg.name : "—")}</b>')
rep('  hullK: d => { G.hullK = d.k; render(true); },', r'''  hullK: d => { G.hullK = d.k; render(true); },
  capSel: d => { if (!CAPS[d.k] || !capOwned(d.k)) return; if (capBusy(d.k)) return toast(`${capName(d.k)} is leading another fleet.`, "warn"); S.capSel = d.k; dirty(); if (sheet) renderSheet(); else render(true); },
  capBuy: d => { const C = CAPS[d.k]; if (!C || capOwned(d.k)) return; if ((S.shards || 0) < C.cost) return toast(`${capName(d.k)} joins for ◆${C.cost}.`, "warn"); if (!armBuy("cap|" + d.k, C.cost)) return;
    act(() => { S.shards -= C.cost; S.caps = Object.assign({}, S.caps, { [d.k]: 1 }); S.capSel = d.k; }); toast(`${capName(d.k)} joins your fleet. ${C.perk}.`, "win"); try { advHolo(`${capName(d.k)} reporting, Commander. Give them a fleet and they'll earn their keep.`, true); } catch (e) {} },''')
rep('.hfp{flex-shrink:0;', r'''.caprow{margin-top:10px;display:flex;flex-direction:column;gap:6px}.caph{display:flex;justify-content:space-between;align-items:baseline;gap:8px}.caph b{font-size:12.5px;text-align:right}.caph em{font-style:normal;color:#8affb4;font-weight:500}
.caps{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}.caps::-webkit-scrollbar{display:none}.cap{all:unset;cursor:pointer;flex:none;width:58px;display:flex;flex-direction:column;align-items:center;gap:3px}.cap img{width:52px;height:52px;border-radius:12px;object-fit:cover;object-position:top;border:2px solid rgba(255,255,255,.14);background:#0a1420}
.cap small{font-size:10px;color:#cfdbe6;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}.cap.on img{border-color:#ffd25a;box-shadow:0 0 10px rgba(255,210,90,.6)}.cap.on small{color:#ffd25a;font-weight:700}.cap.busy img{filter:grayscale(.8) brightness(.6)}.cap.lk img{filter:grayscale(.9) brightness(.45)}.cap.lk small{color:#ffd25a}
.fcap{width:22px;height:22px;border-radius:6px;object-fit:cover;object-position:top;vertical-align:-6px;margin-right:6px;border:1px solid rgba(255,210,90,.5)}
.hfp{flex-shrink:0;''')
rep('const GAME_V = 646', 'const GAME_V = 647')
open(p, 'w', encoding='utf-8').write(s)
