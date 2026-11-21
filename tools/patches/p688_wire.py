# v688: the white glare on a long flight (the warp flare lasted the first and last 3% of the trip: 27 minutes on a 15-hour joint strike
# march), and speed-ups for joint-strike fleets in the Fleets tab, the top-bar chip and alliance help (see p688_flight.js)
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__)); R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('return { a, b, k: clamp((T - f.out) / Math.max(1, f.arrive - f.out), 0, 1) }; }', 'return { a, b, k: clamp((T - f.out) / Math.max(1, f.arrive - f.out), 0, 1), d: f.arrive - f.out }; }')
rep('b: hp, k: clamp((T - (f.back - tt)) / tt, 0, 1) }; }', 'b: hp, k: clamp((T - (f.back - tt)) / tt, 0, 1), d: tt }; }')
rep('const wk = path.park || path.k >= 1 ? 1 : Math.min(clamp(path.k / .03, 0, 1), id === "raid" ? 1 : clamp((1 - path.k) / .03, 0, 1))',
    'const wk = path.park || path.k >= 1 ? 1 : path.d > 0 ? Math.min(clamp(path.k * path.d / 4000, 0, 1), id === "raid" ? 1 : clamp((1 - path.k) * path.d / 4000, 0, 1)) /* v688 the warp flare lasts 4 s, not 3% of the trip */ : Math.min(clamp(path.k / .03, 0, 1), id === "raid" ? 1 : clamp((1 - path.k) / .03, 0, 1))')
rep(R('p687_home.js'), R('p688_flight.js'))
rep('${fhelpBtn(f)}${canHurry && rem > 0 ?', '${strikeRowBtns(f)}${fhelpBtn(f)}${canHurry && rem > 0 ?')
rep('askFHelp: d => { const a = myAlly(), f = S.fleets.find(x => x.id === d.id); if (!a || !G.db || !f || f.phase !== "back" || f.assault) return toast("Join an alliance to ask for help.", "warn");\n    const tg = fleetTarget(f), req = { id: fhId(f), k: `${fmt(sumShips(f.n))} ships from ${tg && tg.name ? tg.name : "a mission"}`.slice(0, 60), e: Math.round(f.back), t: now(), by: null };',
    'askFHelp: d => { const a = myAlly(), f = S.fleets.find(x => x.id === d.id); if (!a || !G.db || !fhOK(f)) return toast("Join an alliance to ask for help.", "warn");\n    const tg = fleetTarget(f), sa = fhStrike(f), tn = tg && tg.name ? tg.name : "a mission", req = { id: fhId(f), k: (sa ? `Joint strike on ${tn}` : f.phase === "back" ? `${fmt(sumShips(f.n))} ships home from ${tn}` : `${fmt(sumShips(f.n))} ships to ${tn}`).slice(0, 60), e: Math.round(fhEnd(f)), t: now(), by: null };')
rep('<small>↩ ${esc(r.k)} · home in <b data-end="${r.e}">', '<small>${esc(r.k)} · lands in <b data-end="${r.e}">')
rep('strikeBoost: d => act(() => strikeBoost(d.id, d.k)),', '''strikeBoost: d => act(() => strikeBoost(d.id, d.k)),
  strikeHurry: d => act(() => { const a = G.assaults[d.id], T = now(); if (!a || !(a.members || {})[G.me] || a.disb) return; const left = strikeMarchLeft(a); if (left < 45000) return toast("The joint strike is about to hit the target.", "warn");
    const c = shardCost(left); if ((S.shards || 0) < c) return toast(`Hurrying needs ◆${c}. You have ◆${S.shards || 0}.`, "warn"); S.shards -= c; const saved = strikeCut(a, left); toast(`⚡ Joint strike hurried: ${ftime(saved)} saved. It strikes in ${ftime(a.arrive - T)}.`, "win"); }), /* v688 */''')
rep('const GAME_V = 687;', 'const GAME_V = 688;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
