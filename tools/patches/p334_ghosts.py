import sys
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# v334 no more ghost boxes on the base. Unbuilt slots were a dozen identical grey "Name · build" tags over see-through outlines.
# Now: an unbuilt slot reads "＋ Name"; during the Academy only the building the current step asks for is tagged (in amber,
# "Tap to build ..."), and the other empty slots stay quiet so a new player sees one clear thing to tap.
rep('''    const txt = busy ? `${B[k].n} → Lv.${bq.lvl} · ${ftime(bq.e - TT)}` : L ? `${B[k].n} Lv.${L}` : `${B[k].n} · build`;''',
    '''    const want = tutOn() && tutBld() === k; if (!L && !busy && tutOn() && !want) continue; // v334: during the Academy, only the empty slot the step needs is labelled
    const txt = busy ? `${B[k].n} → Lv.${bq.lvl} · ${ftime(bq.e - TT)}` : want ? (L ? `Tap ${B[k].n} to upgrade` : `＋ Tap to build ${B[k].n}`) : L ? `${B[k].n} Lv.${L}` : `＋ ${B[k].n}`;''')
rep('''    ctx.fillStyle = busy ? "rgba(60,36,8,.88)" : L ? "rgba(6,32,42,.86)" : "rgba(10,18,26,.7)"; ctx.fill();
    ctx.strokeStyle = busy ? "rgba(255,184,90,.9)" : L ? "rgba(85,214,232,.8)" : "rgba(125,149,165,.6)"; ctx.lineWidth = 1; ctx.setLineDash(L || busy ? [] : [3, 3]); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = busy ? "#ffd59a" : L ? "#c9f6fc" : "#93a8b6";''',
    '''    ctx.fillStyle = want && !busy ? "rgba(255,196,84,.95)" : busy ? "rgba(60,36,8,.88)" : L ? "rgba(6,32,42,.86)" : "rgba(10,18,26,.78)"; ctx.fill();
    ctx.strokeStyle = want && !busy ? "#fff1c2" : busy ? "rgba(255,184,90,.9)" : L ? "rgba(85,214,232,.8)" : "rgba(160,190,205,.75)"; ctx.lineWidth = want ? 2 : 1; ctx.stroke();
    ctx.fillStyle = want && !busy ? "#241503" : busy ? "#ffd59a" : L ? "#c9f6fc" : "#b8cad6";''')
# which building the current Academy step is about ("Build a Metal Extractor", "Upgrade the Crystal Refinery to Lv.5" ...)
rep('''const tutKey = i => {''', '''function tutBld() { const st = tutOn() ? TUT[S.tut.i] : null; if (!st || !/^(Build|Upgrade)/.test(st.t)) return null; let best = null; for (const k in B) if (st.t.includes(B[k].n) && (!best || B[k].n.length > B[best].n.length)) best = k; return best; } // v334
const tutKey = i => {''')
# the guide never frames something that isn't fully on screen yet (a card still fading or sliding in): it waits for it
rep('''  if (!el) { g.style.display = "none"; return requestAnimationFrame(guideFrame); }''',
    '''  if (el) { let op = 1; for (let n = el; n && n.nodeType === 1 && op > .5; n = n.parentElement) op *= +getComputedStyle(n).opacity; if (op < .9) { g.style.display = "none"; return requestAnimationFrame(guideFrame); } } // v334: no frame around a card that's still fading in
  if (!el) { g.style.display = "none"; return requestAnimationFrame(guideFrame); }''')
open(p, 'w', encoding='utf-8', newline='').write(t); print('ok')
import sys
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# v334 during the Academy the see-through outlines of empty slots are hidden too, except the one the step asks for
rep('''      W.blds[k] = m; W.keys[k] = key; W.renderer.shadowMap.needsUpdate = true; }
  }''', '''      W.blds[k] = m; W.keys[k] = key; W.renderer.shadowMap.needsUpdate = true; }
  }
  { const on = tutOn(), want = on ? tutBld() : null; for (const k of bt.keys) { const m = W.blds[k]; if (!m) continue; const show = !on || bt.lv(k) > 0 || !!bt.busy(k) || k === want; if (m.visible !== show) { m.visible = show; W.renderer.shadowMap.needsUpdate = true; } } } // v334''')
open(p, 'w', encoding='utf-8', newline='').write(t); print('ok')
