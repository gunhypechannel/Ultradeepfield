# v593 on the galaxy map the Cube event lives in the HUD strip too (owner, with a screenshot: the "CUBE LIVE · FINALE" panel floated at
# the bottom over the joint-strike card and the dock; he had asked for these bands to sit in the "Events · My own…" strip). While the
# Cube event runs, the galaxy's strip shows "● CUBE LIVE · <phase> <countdown> ▾"; tapping it drops the Cube details down just under
# the HUD. The floating bottom panel only remains when the strip is busy showing hostile fleets.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('{ let hb = ""; if (view === "base" && !battle) { hb = omenBand(T) + wheelBand(); }',
    '{ let hb = ""; if (view === "base" && !battle) { hb = omenBand(T) + wheelBand(); } else if (view === "galaxy" && !battle && !cineOn) hb = cubeHB(T); /* v593 */')
rep('function omenBand(T) {', '''function cubeHB(T) { const ph = typeof cubePhase === "function" && cubePhase(T); if (!ph) return ""; const end = ph.i === 6 ? ph.end : ph.t0 + EV_DUR; /* v593 the Cube event in the galaxy's HUD strip */
  return `<button class="omb cubeb" data-act="cubePanel"><i class="cpdot"></i><b>CUBE LIVE · ${esc(ph.n.toUpperCase())}</b><span class="cpt" data-end="${end}"></span><i class="cpx">${G.cubeOpen ? "▴" : "▾"}</i></button>`; }
function omenBand(T) {''')
rep('''setInterval(() => { try { const show = view === "galaxy" && G3 && !sheet && !battle && !(G3.cam.cine || G3.cam.live) && cubePhase(now()); /* v111: steps aside while a planet or other panel is open */ let el = $("#cubepanel"); if (!show) { if (el) el.remove(); return; }
  if (!el) { el = document.createElement("div"); el.id = "cubepanel"; $("#app").appendChild(el); }''',
    '''setInterval(() => { try { const T0 = now(), hb = $("#hud .cubeb"); if (hb) hb.querySelectorAll("[data-end]").forEach(x => { x.textContent = ftime(+x.dataset.end - T0); }); /* v593: the strip's countdown */
  const show = view === "galaxy" && G3 && !sheet && !battle && !(G3.cam.cine || G3.cam.live) && cubePhase(now()) && (!hb || G.cubeOpen); /* v111: steps aside while a planet or other panel is open */ /* v593: with the strip showing the Cube, only its opened details */ let el = $("#cubepanel"); if (!show) { if (el) el.remove(); return; }
  if (!el) { el = document.createElement("div"); el.id = "cubepanel"; $("#app").appendChild(el); } el.classList.toggle("top", !!hb);''')
rep('cubePanel: () => { G.cubeOpen = !G.cubeOpen;', 'cubePanel: () => { G.cubeOpen = !G.cubeOpen; try { omBand(); } catch (e) {} /* v593 the strip\'s ▾/▴ */')
rep('#cubepanel{position:fixed;', '''#cubepanel.top{top:calc(var(--hudH,150px) + 6px);bottom:auto}#cubepanel.top .cph{display:none}#cubepanel.top .cpbody{margin-top:0;box-shadow:0 10px 30px rgba(0,0,0,.5)}
.evbar.hb .omb.cubeb{border-color:rgba(93,255,138,.55);background:linear-gradient(90deg,rgba(4,30,14,.94),rgba(4,16,10,.94));color:#dfffe6}.evbar.hb .omb.cubeb .cpdot{width:8px;height:8px;border-radius:50%;background:#5dff8a;box-shadow:0 0 8px #5dff8a;animation:cpp 1.6s infinite;flex:none}.evbar.hb .omb.cubeb .cpt{color:#ffd36b;font-variant-numeric:tabular-nums;flex:none}.evbar.hb .omb.cubeb .cpx{font-style:normal;opacity:.7}
#cubepanel{position:fixed;''')
s2 = re.sub(r"GAME_V = 592\b", "GAME_V = 593", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
