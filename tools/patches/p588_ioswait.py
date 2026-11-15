# v588 iPhone/iPad: a breath between releasing one 3D world and building the next. The owner's crash logs (v586 memory readout)
# show WebKit closing the tab seconds after "base released (before the map is built)" + "map shaders paced": the base's ~220 MB of
# textures are released, but Safari frees GPU memory lazily, so for a moment both worlds count. Now, on iOS, the next world is built
# 1 s after the release (a short "Opening…" card shows meanwhile). Both directions: base → map and map → base.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
GL_WAIT = 1000
rep('''  if (k === "gal" && G3 && view !== "galaxy") { const old = G3, c = old.cam;''', '''  const glw0 = IOS && ((k === "gal" && G3 && view !== "galaxy") || (k === "col" && C3 && view !== "base")); /* v588 */
  if (k === "gal" && G3 && view !== "galaxy") { const old = G3, c = old.cam;''')
rep('''  if (k === "stu" && STU) { const s = STU; G.stuCache = s.cache; STU = null; glFree(s.renderer); }
} catch (e) {''', '''  if (k === "stu" && STU) { const s = STU; G.stuCache = s.cache; STU = null; glFree(s.renderer); }
  if (glw0) G.glWait = performance.now() + %d; /* v588 the wait starts once the release is done */
} catch (e) {''' % GL_WAIT)
rep('''    if (IOS && !mapHost && C3) worldDrop("col", "before the map is built"); /* v580 never two worlds at a cold build */
    mapMount(m); { const pk = $("#mappark"); if (pk && !pk.firstChild) pk.remove(); } /* v383: a map built in the background just moves on screen */
    mapOverlay();''', '''    if (IOS && !mapHost && C3) worldDrop("col", "before the map is built"); /* v580 never two worlds at a cold build */
    const glw = IOS && !mapHost && G.glWait && performance.now() < G.glWait; /* v588 let Safari free the base first */
    if (glw) { if (!m.querySelector(".glwait")) { crumb("map waits for the base to be freed"); m.innerHTML = '<div class="glwait"><i></i><span>Opening the galaxy…</span></div>'; } clearTimeout(G.glWaitT); G.glWaitT = setTimeout(() => { try { if (view === "galaxy") render(true); } catch (e) {} }, G.glWait - performance.now() + 30); }
    else { mapMount(m); { const pk = $("#mappark"); if (pk && !pk.firstChild) pk.remove(); } /* v383: a map built in the background just moves on screen */
    mapOverlay(); }''')
rep('''if (use3) { if (IOS && G3) worldDrop("gal", "before the base is built"); /* v580 */ C3 = initColony(colHost); if (C3) bindColony(colHost.querySelector("#colfx")); else colHost.innerHTML = '<canvas id="planet"></canvas><div class="meta" id="cmeta"></div>'; } }''',
    '''if (use3) { if (IOS && G3) worldDrop("gal", "before the base is built"); /* v580 */ if (IOS && G.glWait && performance.now() < G.glWait) { colHost.dataset.init = ""; if (!colHost.querySelector(".glwait")) { crumb("base waits for the map to be freed"); colHost.insertAdjacentHTML("beforeend", '<div class="glwait"><i></i><span>Opening your base…</span></div>'); } clearTimeout(G.glWaitT); G.glWaitT = setTimeout(() => { try { if (view === "base") { const w = colHost && colHost.querySelector(".glwait"); if (w) w.remove(); render(true); } } catch (e) {} }, G.glWait - performance.now() + 30); } /* v588 */ else { C3 = initColony(colHost); if (C3) bindColony(colHost.querySelector("#colfx")); else colHost.innerHTML = '<canvas id="planet"></canvas><div class="meta" id="cmeta"></div>'; } } }''')
rep('.evbar{background:transparent;border-top-color:rgba(85,214,232,.14)}', '.evbar{background:transparent;border-top-color:rgba(85,214,232,.14)}\n.glwait{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;color:#9fd8e8;font:600 14px var(--f-display);letter-spacing:.08em;background:radial-gradient(circle,#0c1a2a,#03070d 70%);z-index:2}.glwait i{width:34px;height:34px;border-radius:50%;border:3px solid rgba(85,214,232,.25);border-top-color:#55d6e8;animation:glw .9s linear infinite}@keyframes glw{to{transform:rotate(360deg)}}')
s2 = re.sub(r"GAME_V = 587\b", "GAME_V = 588", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
