# v530 smooth start and a smooth map (owner, on his iPhone: stuck on "Loading Ultra Deep Field…", earlier a 5.8 s freeze opening
# the galaxy and a crash). Measured: opening the galaxy compiled 37 shader programs inside one frame; on an iPhone that is seconds of
# frozen screen. Now:
#  - the map compiles at most ~22 ms of new shaders per frame on phones (45 ms on computers); anything still waiting is drawn a frame
#    or two later instead of freezing the screen. Only the map's own scene is paced (never bloom, shots or shadows).
#  - the background map warm-up keeps going until every shader is ready, not a fixed 10 frames.
#  - after a crash the game never reopens straight onto the galaxy (it starts on the base).
#  - the loading screen can't hang silently: after 15 s it says what it's waiting for, with Try again and Safe start (no restored
#    screen, lighter graphics); the start is logged, so a start that dies is reported to the Crash & performance inbox.
#  - the studio warm-up (building and research pictures) waits while the map or a battle is on screen.
import sys, re, os
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('function glNew(o) { const r = new TH.WebGLRenderer(o); try { r.debug.checkShaderErrors = /[?&]gldebug/.test(location.search); } catch (e) {} return r; }',
    '''function glNew(o) { const r = new TH.WebGLRenderer(o); try { r.debug.checkShaderErrors = /[?&]gldebug/.test(location.search); } catch (e) {} try { glPace(r); } catch (e) {} return r; }
/* v530 shader pacing: a draw whose material has never been drawn may compile a shader (on an iPhone ~0.1 s each). While a scene is
   paced (r.pace.scene), once this frame has spent its compile budget the remaining never-drawn materials wait for the next frame. */
function glPace(r) { const gl = r.getContext(), lp = gl.linkProgram, rbd = r.renderBufferDirect, seen = new WeakSet(); let links = 0;
  gl.linkProgram = function (p) { links++; return lp.call(this, p); };
  r.pace = { scene: null, ms: 30, used: 0, skips: 0 };
  r.renderBufferDirect = function (cam, scene, geo, mat) { const B = r.pace, paced = !!B.scene && scene === B.scene;
    if (paced && mat && !seen.has(mat) && B.used >= B.ms) { B.skips++; return; }
    const l0 = links, t0 = paced ? performance.now() : 0, res = rbd.apply(this, arguments); if (mat) seen.add(mat); if (paced && links > l0) B.used += performance.now() - t0; return res; }; }''')
rep('''  W.renderer.render(W.scene, W.camera);
  if (W.snapReq)''', '''  { const B = W.renderer.pace; if (B) { B.scene = W.scene; B.used = 0; B.skips = 0; B.ms = MOBILE ? 22 : 45; } W.renderer.render(W.scene, W.camera); if (B) { B.scene = null; W.compSkip = B.skips; if (B.skips && !W.paceN) { W.paceN = 1; try { crumb("map shaders paced over several frames"); } catch (e) {} } } } /* v530 */
  if (W.snapReq)''')
rep('if (++n < 10) setTimeout(() => requestAnimationFrame(step), 300);', 'if (++n < 10 || (G3.compSkip > 0 && n < 120)) setTimeout(() => requestAnimationFrame(step), n < 10 ? 300 : 120); /* v530 until every shader is ready */')
rep('''  if (!o || o.me !== G.me || Date.now() - o.t > 12 * 3600e3 || !SESS_VIEWS.includes(o.view) || !S || !S.tut || S.tut.k !== "done" || battle) return;''',
    '''  if (!o || o.me !== G.me || Date.now() - o.t > 12 * 3600e3 || !SESS_VIEWS.includes(o.view) || !S || !S.tut || S.tut.k !== "done" || battle) return;
  if (o.view === "galaxy" && (G.crashBoot || G.safeStart)) { try { crumb("session not restored onto the galaxy (last session crashed)"); } catch (e) {} return; } /* v530 */''')
# boot log: a start that never finishes leaves an open session with a line in it, so it is reported as a crash
rep('''function start(data) {
  let fresh = false;''', '''function start(data) { const bt0 = performance.now(); window.__udfStage = "reading your save"; try { crumb("boot v" + GAME_V); } catch (e) {} /* v530 */
  try { if (localStorage.getItem("udf.safeStart")) { localStorage.removeItem("udf.safeStart"); localStorage.removeItem("udf.sess"); G.safeStart = 1; } } catch (e) {}
  let fresh = false;''')
rep('  rebuild(); render(); awaySummary();', '  window.__udfStage = "building the galaxy"; rebuild(); window.__udfStage = "drawing the screen"; render(); awaySummary(); try { crumb(`boot done in ${Math.round(performance.now() - bt0)} ms`); } catch (e) {}')
rep('  live = false; const before = S.log[0], away = now() - S.t;', '  window.__udfStage = "catching up on time away"; live = false; const before = S.log[0], away = now() - S.t;')
# the loading screen watchdog (in the startup guard, before the game's script)
rep('''addEventListener("error", function (e) { if (!window.__booted) window.__bootErr(''', '''/* v530 the loading screen never hangs silently: after 15 s it says what it is waiting for and offers a way out */
setTimeout(function () { try { if (window.__booted || document.getElementById("booterr")) return; var v = document.getElementById("view"); if (!v) return;
  var why = typeof THREE === "undefined" ? "downloading the 3D engine" : !window.__udfStage ? "loading the game" : window.__udfStage;
  v.innerHTML = '<div class="card hi" id="bootslow" style="display:flex;flex-direction:column;gap:10px"><h3 style="font-size:18px">Still starting…</h3><p class="note">Still ' + why + '. A slow connection or a busy phone can do this.</p>' +
    '<div style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn" id="bootre">Try again</button><button class="btn ghost" id="bootsafe">Safe start</button></div><p class="note">Safe start opens on your base with lighter graphics.</p></div>';
  document.getElementById("bootre").onclick = function () { location.reload(); };
  document.getElementById("bootsafe").onclick = function () { try { localStorage.setItem("udf.safeStart", "1"); localStorage.setItem("udf.safeUntil", String(Date.now() + 864e5)); } catch (e) {} location.reload(); };
} catch (e) {} }, 15000);
addEventListener("error", function (e) { if (!window.__booted) window.__bootErr(''')
rep('if (!document.hidden && (artBusy || G.sliding)) return idle(() => { steps.unshift(f); run(); });', 'if (!document.hidden && (artBusy || G.sliding || view === "galaxy" || battle)) return setTimeout(() => idle(() => { steps.unshift(f); run(); }), 1500); /* v530 never while the map or a battle is on screen */')
s2 = re.sub(r"GAME_V = 529\b", "GAME_V = 530", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
