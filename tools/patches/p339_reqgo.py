# v339: a missing requirement (red ✕) on any card is a link: research opens in Research (its category, then its card), a building opens
# its card in Structures. Tapping a Mission takes you straight to where it needs you.
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep('''const reqRows = (req, p) => Object.entries(req || {}).map(([k, l]) => { const have = lvlAt(k, p); return `<tr><td>${esc((ANY[k] || { n: k }).n)}</td><td class="nd">level ${l}</td><td class="hv">level ${have}</td><td>${have >= l || (k === "cmd" && acadFlag()) ? '<i class="ok">✓</i>' : '<i class="no">✕</i>'}</td></tr>`; }).join("");''',
'''const reqRows = (req, p) => Object.entries(req || {}).map(([k, l]) => { const have = lvlAt(k, p), ok = have >= l || (k === "cmd" && acadFlag()), go = !ok && (R[k] || B[k]); return `<tr${go ? ` class="rqgo" data-act="reqGo" data-k="${k}" title="Open ${esc(ANY[k].n)}"` : ""}><td>${esc((ANY[k] || { n: k }).n)}</td><td class="nd">level ${l}</td><td class="hv">level ${have}</td><td>${ok ? '<i class="ok">✓</i>' : `<i class="no">✕</i>${go ? '<b class="rqa">›</b>' : ""}`}</td></tr>`; }).join(""); /* v339: tap a ✕ to go to it */''')
rep('  rcat: d => {', '''  reqGo: d => { const k = d.k; if (!R[k] && !B[k]) return; closeSheet();
    if (R[k]) { ACT.nav({ v: "lab" }); sub.rcat = RCAT_OF(k); render(); } else ACT.nav({ v: "build", s: B[k].cat === "fac" ? "fac" : "res" });
    setTimeout(() => { ACT.detail({ kind: R[k] ? "r" : "b", k }); toast(`${ANY[k].n}: ${R[k] ? "research" : "build"} this next.`, ""); }, 120); }, /* v339 */
  rcat: d => {''')
# Missions: the pill goes straight there
rep('''data-act="${done ? "tutClaim" : "tutOpen"}" aria-label="${done ? "Collect the Academy reward" : "Open the Flight Academy"}"''',
    '''data-act="${done ? "tutClaim" : acadOn() ? "tutOpen" : "tutShow"}" aria-label="${done ? "Collect the reward" : acadOn() ? "Open the Flight Academy" : "Take me to this mission"}"''')
i = t.index('.cneed{'); t = t[:i] + 'tr.rqgo{cursor:pointer}tr.rqgo:hover td,tr.rqgo:active td{background:rgba(255,90,90,.12)}tr.rqgo .rqa{margin-left:6px;color:#ff8a8a;font-weight:800}\n' + t[i:]
open(p, 'w', encoding='utf-8').write(t); print('ok')
