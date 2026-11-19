# v660 (owner: "Cube destroyer still slides back and forth"; "When we have less than 10 can't they be represented as one ship? ... I just
# want all ships to have enough space to be brilliantly represented"). A squadron was drawn as up to six hulls side by side, and several
# Cube Destroyer squadrons on one side were each drawn with their own hulls, pushed apart and regrouped as the fight moved, so the
# Destroyers jostled and slid across the field. Now: under 10 ships a squadron is one hull, 10-99 two, 100+ three at most; and a side's
# Cube Destroyers and each Titan type are always drawn as one ship carrying the combined count. Fewer hulls on the field means the fit
# draws every ship bigger.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
rep('const visN = (role, n) => n <= 0 ? 0 : Math.min(role === "titan" || role === "station" ? 1 : BIG_R.has(role) ? 2 : role === "turret" ? 1 : role === "support" || role === "cruiser" || role === "frigate" ? 3 : 4, 1 + Math.floor(Math.log2(n) / 1.6));',
    'const visN = (role, n) => n <= 0 ? 0 : Math.min(role === "titan" || role === "station" || role === "turret" ? 1 : BIG_R.has(role) ? 2 : 3, n < 10 ? 1 : n < 100 ? 2 : 3); /* v660 one hull under 10, two under 100, three at most */')
rep('const grp = busy ? new Map() : null, tot = [], rep = []; if (busy) { const cell = W * (W < H ? .3 : .21); for (let o = b.ord.length - 1; o >= 0; o--) { const i = b.ord[o], q = Q[i]; if (b.n[i] <= 0 || (pos[i].fl & 6)) continue;',
    'const grp = new Map(), tot = [], rep = [], giant = k => k === "worldbreaker" || !!TITAN_LEN[k]; { const cell = W * (W < H ? .3 : .21); for (let o = b.ord.length - 1; o >= 0; o--) { const i = b.ord[o], q = Q[i]; if (b.n[i] <= 0 || (pos[i].fl & 6)) continue; if (!busy && !giant(q.k)) continue; /* v660 a side\'s giants are always one ship */')
rep('const key = q.side + q.k + "|" + Math.round(scr[i].x / cell) + "|" + Math.round(scr[i].y / cell), g = grp.get(key);', 'const key = q.side + q.k + (giant(q.k) ? "" : "|" + Math.round(scr[i].x / cell) + "|" + Math.round(scr[i].y / cell)), g = grp.get(key);')
rep('const n = busy && tot[i] > 0 ? tot[i] : Math.max(1, b.n[i]), vc = MON[q.k] ? 1 : Math.min(busy ? 3 : 6, Math.max(1, visN(q.role, n))),', 'const n = tot[i] > 0 ? tot[i] : Math.max(1, b.n[i]), vc = MON[q.k] || giant(q.k) ? 1 : Math.min(3, Math.max(1, visN(q.role, n))),')
rep('&& !(busy && tot[i] === -1));', '&& !(tot[i] === -1));')
rep('    if (busy) Q.forEach((q, i) => { if (tot[i] === -1 && rep[i] != null) scr[i] = scr[rep[i]]; }); }', '    Q.forEach((q, i) => { if (tot[i] === -1 && rep[i] != null) scr[i] = scr[rep[i]]; }); }')
rep('    if (busy && tot[i] === -1) return; // merged into a nearby formation of the same type', '    if (tot[i] === -1) return; // merged into a nearby formation of the same type')
rep('    const p = pos[i], n = busy && tot[i] > 0 ? tot[i] : b.n[i]; if (p.fl & 6) return;', '    const p = pos[i], n = tot[i] > 0 ? tot[i] : b.n[i]; if (p.fl & 6) return;')
rep('(busy && tot[i] === -1)) continue;', '(tot[i] === -1)) continue;')
rep('n = busy && tot[i] > 0 ? tot[i] : b.n[i];', 'n = tot[i] > 0 ? tot[i] : b.n[i];')
rep('/* v645 */ vc = MON[q.k] ? 1 : Math.min(busy ? 3 : 6, Math.max(1, visN(q.role, Math.max(n, 1)))),', '/* v645 */ vc = MON[q.k] || giant(q.k) ? 1 : Math.min(3, Math.max(1, visN(q.role, Math.max(n, 1)))),')
rep('const GAME_V = 659', 'const GAME_V = 660')
open(p, 'w', encoding='utf-8').write(s)
