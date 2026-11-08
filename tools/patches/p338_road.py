# v338: the Fleet Path shows the whole road to the next hull (every Shipyard level and research it needs, with ticks), explains the
# pattern, and its first three hulls get Fleet Command speed-ups like the Academy, so starting a build there means no wait
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep('function shipStep() {', '''/* v338: everything a hull needs, deepest first: [key, level, have] */
function reqRoad(req, out, d) { out = out || new Map(); for (const [k, l] of Object.entries(req || {})) { const D = B[k] || R[k]; if (!D) continue; if (D.req && (d || 0) < 6) reqRoad(D.req, out, (d || 0) + 1); if (!out.has(k) || out.get(k) < l) { out.delete(k); out.set(k, l); } } return out; }
const roadHTML = (k, nextK) => { const r = [...reqRoad(SH[k].req)]; if (!r.length) return ""; return `<div class="road"><small>ROAD TO ${esc(SH[k].n.toUpperCase())}</small>${r.map(([q, l]) => { const have = lvlOf(q), ok = have >= l; return `<span class="${ok ? "ok" : q === nextK ? "nx" : ""}">${ok ? "✓" : q === nextK ? "▸" : "·"} ${esc((B[q] || R[q]).n)} Lv.${l}${ok ? "" : ` <i>(Lv.${have})</i>`}</span>`; }).join("")}<em>Every stronger hull needs a bigger Shipyard and new research. Build up this road and the hull unlocks.</em></div>`; };
function pathBoostTopUp() { if (!S || tutOn()) return; const sp = shipStep(); if (!sp || sp.i > 2) return; const road = new Set([...reqRoad(sp.d.req).keys()]), T = now(), w = freeWin(); let need = 0;
  if (S.bq && road.has(S.bq.k) && S.bq.e - T > w) need += Math.ceil((S.bq.e - T - w) / 300000);
  if (S.rq && road.has(S.rq.k) && S.rq.e - T > w) need += Math.ceil((S.rq.e - T - w) / 300000);
  if (S.sq && S.sq[0] && S.sq[0].k === sp.k) { const rem = sqEnd(S.sq[0]) - T; if (rem > 60000) need += Math.ceil((rem - 60000) / 300000); }
  if (need > (S.boosts || 0)) { const add = need - (S.boosts || 0); S.boosts = need; S.pathBoostGiven = (S.pathBoostGiven || 0) + add; dirty(); note(`Fleet Command sent ${add} ⚡ speed-up${add > 1 ? "s" : ""} for the Fleet Path. Tap −5m to use them.`, "win"); } }
function shipStep() {''')
rep('  tutSupply();\n', '  tutSupply(); try { pathBoostTopUp(); } catch (e) {} /* v338: before the fleet-path branch returns */\n')
rep('''${!done && sp.need ? `<div class="cneed">Next step: <b>${esc(sp.need.n)} Lv.${sp.need.l}</b> <small>(you have Lv.${sp.need.cur})</small></div>` : ""}''',
'''${!done && sp.need ? `<div class="cneed">Next step: <b>${esc(sp.need.n)} Lv.${sp.need.l}</b> <small>(you have Lv.${sp.need.cur})</small></div>` : ""}${!done ? roadHTML(sp.k, sp.need && sp.need.k) : ""}''')
i = t.index('.cneed{'); t = t[:i] + '.road{margin:6px 0;padding:6px 10px;border-radius:8px;background:rgba(85,214,232,.07);display:flex;flex-wrap:wrap;gap:4px 10px;font-size:12px;color:#cfe6ef}.road small{flex-basis:100%;color:var(--cyan);letter-spacing:.1em}.road span.ok{color:var(--green)}.road span.nx{color:var(--amber);font-weight:700}.road i{font-style:normal;opacity:.7}.road em{flex-basis:100%;font-style:normal;opacity:.8}\n' + t[i:]
rep('(you have Lv.${sp.need.cur}).</p>` : ""}\n      <div class="rw"><span class="cost">${costHTML(sp.rw)}', '(you have Lv.${sp.need.cur}).</p>` : ""}${sp.ok() ? "" : roadHTML(sp.k, sp.need && sp.need.k)}\n      <div class="rw"><span class="cost">${costHTML(sp.rw)}')
open(p, 'w', encoding='utf-8').write(t); print('ok')
