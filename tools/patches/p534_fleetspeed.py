# v534 fleet speed in the Void Shop (owner: "Where do players buy speed boost for flight time, those should be in item shop too or no?"
# then "do the rest"). Until now flight time could only be cut on the fleet itself (Afterburners and Arrive now for shards, or a
# general boost for 5 minutes). Now:
#  - Fleet Booster (Boosters tab, Bronze to Platinum): +10/20/30/40% flight speed for every fleet you send, for 7 days (buff "bf";
#    same rules as the resource boosters: the same tier extends, a stronger one replaces). Read in travelRaw for your own fleets.
#  - Afterburner Fuel (Accelerators tab, Bronze/Silver/Gold: 15 min, 1 h, 4 h for ◆2/6/15): cuts time off a fleet in flight. Used from
#    the fleet's own Fleet control panel (one button per tier you own), or from the inventory, where it goes to the fleet open in Fleet
#    control, or else the one that lands next.
#  - Fleet control's Speed section links to the fuel in the shop when you have none.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const BUFF_N = { bm: "Metal Booster",', 'const BUFF_N = { bf: "Fleet Booster", bm: "Metal Booster",')
rep('''  // accelerators: cut time off the running job (our take on KRAKEN, DETROID and NEWTRON)''', '''  // v534 the Fleet Booster: faster flights for 7 days
  ITIERS.forEach(([tk, tn, col], i) => { const pct = (i + 1) * 10;
    SHOP[`bf_${tk}`] = { cat: "boost", tier: i, col, n: "Fleet Booster", ic: "➤", cost: [6, 12, 20, 32][i], d: () => `+${pct}% flight speed for every fleet you send, for 7 days.`, use: () => activateBuff("bf", pct, 7 * DAY) && `Fleet Booster ${tn} active: your fleets fly ${pct}% faster for 7 days.` }; });
  // v534 Afterburner Fuel: time off a fleet already in flight
  ITIERS.slice(0, 3).forEach(([tk, tn, col], i) => { const ms = [15 * 60e3, HOUR, 4 * HOUR][i];
    SHOP[`xf_${tk}`] = { cat: "accel", tier: i, col, n: "Afterburner Fuel", ic: "🚀", cost: [2, 6, 15][i], fuelMs: ms, fuelL: ["15 min", "1 hour", "4 hours"][i], d: () => `Cuts ${ftime(ms)} off a fleet in flight. Use it from the fleet's controls, or from here for the fleet that lands next.`, use: () => fuelUse(ms) && `Afterburner Fuel ${tn}: ${ftime(ms)} cut.` }; });
  // accelerators: cut time off the running job (our take on KRAKEN, DETROID and NEWTRON)''')
rep('''function spdAdd(ms) {''', '''/* v534 Afterburner Fuel from the inventory: the fleet open in Fleet control, or else the one that lands next */
function fuelUse(ms) { const T = now(); let f = sheet && sheet.type === "fctl" ? S.fleets.find(x => x.id === sheet.id) : null;
  if (!f || f.assault || !fleetBounds(f) || fleetBounds(f)[1] <= T) f = S.fleets.filter(x => !x.assault && fleetBounds(x) && fleetBounds(x)[1] > T).sort((a, b) => fleetBounds(a)[1] - fleetBounds(b)[1])[0];
  if (!f) { toast("No fleet is in flight right now. Keep the fuel for your next one.", "warn"); return false; }
  if (!fleetSpeedUp(f, ms)) return false; spdAdd(ms); return true; }
function spdAdd(ms) {''')
rep('const spd = Math.min(...ks.map(k => spdOf(k, r))) * (r === S.r ? 1 + fsB("spd") / 100 : 1)', 'const spd = Math.min(...ks.map(k => spdOf(k, r))) * (r === S.r ? 1 + fsB("spd") / 100 + buffPct("bf") / 100 /* v534 */ : 1)')
rep('boost5: "impulse", probe5: "spyProbe",', 'boost5: "impulse", bf: "hyper", xf: "drive", probe5: "spyProbe",')
rep('''      <button class="btn ghost" data-act="fBoostItem" data-id="${f.id}" ${b && !f.assault && S.boosts > 0 ? "" : "disabled"}>Use a boost (−5 min) · ${S.boosts || 0} left</button>''',
    '''      <button class="btn ghost" data-act="fBoostItem" data-id="${f.id}" ${b && !f.assault && S.boosts > 0 ? "" : "disabled"}>Use a boost (−5 min) · ${S.boosts || 0} left</button>
      ${(() => { const own = ["xf_bronze", "xf_silver", "xf_gold"].filter(k => ((S.items || {})[k] || 0) > 0); return own.length ? own.map(k => `<button class="btn ghost" data-act="fFuel" data-id="${f.id}" data-k="${k}" ${b && !f.assault ? "" : "disabled"}>🚀 Fuel −${SHOP[k].fuelL} · ×${S.items[k]}</button>`).join("") : `<button class="btn ghost" data-act="shopFuel">🚀 Afterburner Fuel in the shop</button>`; })()}''')
rep('''  fBoostItem: d => act(() => {''', '''  fFuel: d => act(() => { const f = S.fleets.find(x => x.id === d.id), s = SHOP[d.k]; if (!f || f.assault || !s || !s.fuelMs || !((S.items || {})[d.k] > 0)) return; if (fleetSpeedUp(f, s.fuelMs)) { S.items[d.k]--; S.tutRush = 1; spdAdd(s.fuelMs); toast(`Afterburner Fuel burned: ${s.fuelL} cut.`, "win"); } }), /* v534 */
  shopFuel: () => openSheet({ type: "shop", cat: "accel" }),
  fBoostItem: d => act(() => {''')
s2 = re.sub(r"GAME_V = 533\b", "GAME_V = 534", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
