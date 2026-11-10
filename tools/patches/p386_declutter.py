# v386: less clutter. (1) Other commanders' fleet chevrons on the map are smaller and softer, shrink further as you zoom out, and their
# name tags only show once you're zoomed in. (2) World boss labels go through the normal label budget; zoomed out a boss is a small
# glowing marker. (3) Cinematic view hides the Advisor's path pill and the Feedback button. (4) The boss scan card is compact and sits
# at the bottom: name, hull, threat and the attack it's showing right now; tap it for the full analysis.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:90]); t = t.replace(a, b)

# (1) fleet chevrons
rep('col = ROUTE_CSS[rk], sz = 4 + Math.min(7, Math.log2(1 + v.m.n) * .9);',
    'col = ROUTE_CSS[rk], zk = clamp(280 / Math.max(1, W.cam.dist), .45, 1), sz = (2.6 + Math.min(4, Math.log2(1 + v.m.n) * .5)) * zk; /* v386: smaller, and smaller still zoomed out */')
rep('for (const [k, a] of [[1.7, .18], [1, 1]]) { ctx.globalAlpha = a;', 'for (const [k, a] of [[1.6, .1], [1, .72]]) { ctx.globalAlpha = a;')
rep('lbl(-4 - Math.log2(1 + v.m.n) * .5, ', 'if (W.cam.dist < 650 || (W.cam.followMv && W.cam.followMv.m === v.m)) lbl(-4 - Math.log2(1 + v.m.n) * .5, ')
# (2) boss labels
rep('if (D.con == null || sr > 5) lbl(D.con == null ? -1e8 : -sr - 3, ',
    'if (sr < 2.2 && G.find !== "ev") { ctx.save(); ctx.globalAlpha = .85; ctx.fillStyle = D.col; ctx.beginPath(); ctx.arc(s[0], s[1], D.con != null ? 2.2 : 3.6, 0, TAU); ctx.fill(); ctx.globalAlpha = .25; ctx.beginPath(); ctx.arc(s[0], s[1], D.con != null ? 5 : 8, 0, TAU); ctx.fill(); ctx.restore(); continue; } /* v386: far away, a small marker */\n      if (D.con == null || sr > 5) lbl(-sr - 3, ')
# (3) cinematic hides the path pill and Feedback
i = t.index('</style>', t.index('.fshero{'))
t = t[:i] + '''
/* v386 decluttered cinematic and boss scan */
#app.cine #coach,#app.cine ~ #fbBtn,body:has(#app.cine) #fbBtn{opacity:0;visibility:hidden;pointer-events:none}
#wbscan .ws-c{display:none}#wbscan .ws-ret{width:120px;height:120px;margin:-60px 0 0 -60px;opacity:.6}
#wbscan .ws-card{top:calc(env(safe-area-inset-top,0px) + 62px);left:12px;right:12px;margin:0 auto;bottom:auto;width:auto;max-width:430px;padding:9px 12px 10px;pointer-events:auto;cursor:pointer;background:rgba(6,8,18,.72)}
#wbscan .ws-card small{font-size:9px}#wbscan .ws-card>b{margin:3px 0 5px;font-size:15px}
#wbscan .ws-sum{display:flex;flex-wrap:wrap;gap:4px 12px;font:600 11px/1.3 ui-monospace,monospace;color:#c9d4ea}#wbscan .ws-sum em{font-style:normal;color:#ff7a6a}
#wbscan .ws-now{margin-top:6px;padding:5px 8px;border-radius:6px;background:rgba(255,77,106,.16);box-shadow:inset 3px 0 0 #ff4d6a;font-size:12px;line-height:1.35}#wbscan .ws-now b{color:#ffd0c8}
#wbscan .ws-more{display:none;max-height:44vh;overflow:auto;margin-top:6px}#wbscan .ws-card.open .ws-more{display:block}#wbscan .ws-tap{display:block;margin-top:5px;font-size:10px;color:#7f8cab;text-align:right}#wbscan .ws-card.open .ws-tap::after{content:" ▴"}#wbscan .ws-card:not(.open) .ws-tap::after{content:" ▾"}
#wbscan dl div,#wbscan .ws-att{animation:none;opacity:1}
@media (min-width:900px){#wbscan .ws-card{left:16px;right:auto;margin:0}}
''' + t[i:]
# (4) the compact card
rep('<div class="ws-card"><small>SCANNING · WORLD BOSS</small><b>${D.ic} ${esc(D.n)}</b><dl>',
    '<div class="ws-card" data-act="wsMore"><small>SCANNING · WORLD BOSS</small><b>${D.ic} ${esc(D.n)}</b><div class="ws-sum"><span id="wsHullS">…</span><span>Threat <em>${I[2]}</em></span>${key === "ovl" ? `<span id="wsShS">…</span>` : ""}</div><div class="ws-now" id="wsNow">Watching…</div><div class="ws-more"><dl>')
rep('<p data-m="${m}"><b>${n}</b><span>${d}</span></p>`).join("")}</div></div>`;', '<p data-m="${m}"><b>${n}</b><span>${d}</span></p>`).join("")}</div></div><span class="ws-tap">Full analysis</span></div>`;')
rep('  if (a) a.textContent = hp ? `${Math.round(hp / WB_SEG * 100)}% · ${fmt(Math.round(hp / WB_SEG * WB[s.key].hp))} HP` : "Destroyed";',
    '  if (a) a.textContent = hp ? `${Math.round(hp / WB_SEG * 100)}% · ${fmt(Math.round(hp / WB_SEG * WB[s.key].hp))} HP` : "Destroyed"; { const x = $("#wsHullS"), y = $("#wsShS"); if (x) x.textContent = hp ? `Hull ${Math.round(hp / WB_SEG * 100)}%` : "Destroyed"; if (y) y.textContent = wbCons() ? `Shield ${wbCons()}/4` : "Shield down"; }')
rep('for (const p of document.querySelectorAll("#wbscan .ws-att p")) p.classList.toggle("hot", p.dataset.m === n); }',
    'for (const p of document.querySelectorAll("#wbscan .ws-att p")) p.classList.toggle("hot", p.dataset.m === n); { const A = (WB_ATT[WB[s.key].con != null ? "con" : s.key] || []).find(x => x[0] === n), el = $("#wsNow"); if (el) el.innerHTML = A ? `<b>⚠ ${A[1]}</b> · ${A[2]}` : `Observing: ${WB_MOVE_N[n] || n}`; } }')
rep("  cineObj: d => cineObjStart(d.id),", "  cineObj: d => cineObjStart(d.id),\n  wsMore: () => { const c = $(\"#wbscan .ws-card\"); if (c) c.classList.toggle(\"open\"); },")

# (5) the Advisor: never the same line twice within 30 s, and a new line waits for her to finish the one she's saying (no cut-offs)
rep('function advHolo(line) { if (!line) return; let w = $("#advh");',
    """function advHolo(line, force) { if (!line) return; const T0 = Date.now(); G.holoSaid = G.holoSaid || {}; for (const k in G.holoSaid) if (T0 - G.holoSaid[k] > 60000) delete G.holoSaid[k];
  if (!force && G.holoSaid[line] && T0 - G.holoSaid[line] < 30000) return; // v386: not the same thing again within 30 s
  { const a0 = VOICE.au; if (!force && a0 && !a0.paused && !a0.ended && G.holoCur && G.holoCur !== line && $("#advh.on")) { G.holoNext = { line, at: T0 }; // she finishes her sentence first
      if (!a0._q) { a0._q = 1; const go = () => { a0._q = 0; const n = G.holoNext; G.holoNext = null; if (n && Date.now() - n.at < 12000) setTimeout(() => advHolo(n.line), 400); }; a0.addEventListener("ended", go, { once: true }); a0.addEventListener("error", go, { once: true }); } return; } }
  G.holoSaid[line] = T0; G.holoCur = line; let w = $("#advh");""")
rep("advHolo(qa[1])", "advHolo(qa[1], true)")
open(p, "w").write(t); print("ok")
