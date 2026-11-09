# v379: iPhone memory diet. iOS kills a web app that holds too much graphics memory (most often while it sits in the background).
# The game kept every 3D world alive at once: the galaxy map, the base and the portrait studio. On iPhone/iPad now:
#  - the world you are not looking at is released (its whole graphics context) after 20 s away, at once when the app goes to the
#    background, and at once when a battle opens; it is rebuilt when you come back (the map keeps its camera spot);
#  - the portrait studio is released when the app goes to the background;
#  - the base now survives a lost graphics context (it rebuilds instead of staying black);
#  - a restart after time in the background is reported, so we can see how often iOS closes the game.
p = "docs/index.html"; t = open(p).read()
def rep(a, b):
    global t; assert t.count(a) == 1, a[:90]; t = t.replace(a, b)
rep('''function map3DRebuild() {''', '''/* v379 release one 3D world's graphics memory; it is built again the next time its view opens */
function glFree(r) { try { r.dispose(); } catch (e) {} try { r.forceContextLoss(); } catch (e) {} try { const c = r.domElement; if (c) { c.width = 1; c.height = 1; } } catch (e) {} }
function worldDrop(k, why) { try {
  if (k === "gal" && G3 && view !== "galaxy") { const old = G3, c = old.cam; G.camKeep = c ? { tx: c.tx, ty: c.ty, tz: c.tz, th: c.th, ph: c.ph, dist: c.dist } : G.camKeep; G3 = null; glFree(old.renderer);
    if (mapHost && mapHost.parentNode) mapHost.parentNode.removeChild(mapHost); mapHost = null; crumb("map released (" + why + ")"); }
  if (k === "col" && C3 && view !== "base") { const old = C3; C3 = null; glFree(old.renderer); if (colHost && colHost.parentNode) colHost.parentNode.removeChild(colHost); colHost = null; crumb("base released (" + why + ")"); }
  if (k === "stu" && STU) { const s = STU; STU = null; glFree(s.renderer); }
} catch (e) { try { crumb("release failed: " + (e && e.message)); } catch (er) {} } }
const MEM_DIET = IOS;
if (MEM_DIET) { setInterval(() => { const T = performance.now(); if (view === "galaxy") G.galAt = T; if (view === "base") G.colAt = T;
    if (G3 && view !== "galaxy" && T - (G.galAt || 0) > 20000) worldDrop("gal", "away 20 s"); if (C3 && view !== "base" && T - (G.colAt || 0) > 20000) worldDrop("col", "away 20 s"); }, 4000);
  document.addEventListener("visibilitychange", () => { if (document.hidden) { worldDrop("gal", "background"); worldDrop("col", "background"); worldDrop("stu", "background"); } }); }
function map3DRebuild() {''')
# the map comes back where you left it
rep('if (TH && !G3fail) { G3 = init3D(mapHost); if (G3) { bind3D($("#galaxyfx")); hoverBind($("#galaxyfx")); }',
    'if (TH && !G3fail) { G3 = init3D(mapHost); if (G3) { bind3D($("#galaxyfx")); hoverBind($("#galaxyfx")); if (G.camKeep && G3.cam) { Object.assign(G3.cam, G.camKeep, { goal: null, follow: null, followFleet: null }); G.camKeep = null; } }')
# a battle frees the world behind it on iPhone
rep('if (battle) closeBattle(); crumb("battle replay: " + String((r && r.title) || "battle").slice(0, 40)); gpuNap(true);',
    'if (battle) closeBattle(); crumb("battle replay: " + String((r && r.title) || "battle").slice(0, 40)); if (MEM_DIET) { worldDrop("gal", "battle"); worldDrop("col", "battle"); } gpuNap(true);')
# the base survives a lost graphics context
rep('''  let renderer; try { renderer = new TH.WebGLRenderer({ canvas: cv, antialias: GFX_AA || !MOBILE, powerPreference: "high-performance" }); } catch (e) { C3fail = true; return null; }''',
    '''  let renderer; try { renderer = new TH.WebGLRenderer({ canvas: cv, antialias: GFX_AA || !MOBILE, powerPreference: "high-performance" }); } catch (e) { C3fail = true; return null; }
  cv.addEventListener("webglcontextlost", e => { e.preventDefault(); crumb("base GPU reset"); setTimeout(() => { if (C3 && C3.renderer === renderer) { const old = C3; C3 = null; glFree(old.renderer); if (colHost && colHost.parentNode) colHost.parentNode.removeChild(colHost); colHost = null; if (view === "base") render(); } }, 1500); }, false); /* v379: rebuild instead of staying black */''')
# restarts after the background are reported
rep('''setInterval(hqFlush, 7000);''', '''setInterval(hqFlush, 7000);
/* v379: the app was in the background and then started fresh: on iPhone that is usually iOS closing it to free memory */
try { const bg = JSON.parse(localStorage.getItem("udf.bg") || "null"); localStorage.removeItem("udf.bg"); if (bg && bg.t && !(G.lastCrashFresh)) { const gone = Date.now() - bg.t;
  if (gone < 6 * 3600e3) hqPush({ kind: "crash", status: "new", at: Date.now(), now: typeof GAME_V !== "undefined" ? GAME_V : 0, bg: 1, text: `Restarted after ${Math.round(gone / 60000)} min in the background (on ${bg.view || "?"})`, beat: JSON.stringify(bg).slice(0, 1500), device: hqDev(), w: innerWidth, h: innerHeight }); } } catch (e) {}
document.addEventListener("visibilitychange", () => { try { if (document.hidden) localStorage.setItem("udf.bg", JSON.stringify(Object.assign({ t: Date.now() }, CRUMBS.beat || {}, { t: Date.now() }))); else localStorage.removeItem("udf.bg"); } catch (e) {} });
addEventListener("pagehide", e => { try { if (!e.persisted) localStorage.removeItem("udf.bg"); } catch (er) {} });''')
open(p, "w").write(t)
# a release we asked for is not a GPU reset (no safe mode, no lower detail, no rebuild); 30 s away before a release
t = open(p).read()
def rep2(a, b):
    global t; assert t.count(a) == 1, a[:80]; t = t.replace(a, b)
rep2('function glFree(r) { try { r.dispose(); } catch (e) {}', 'function glFree(r) { try { if (r.domElement) r.domElement._udfFree = 1; } catch (e) {} try { r.dispose(); } catch (e) {}')
rep2('cv.addEventListener("webglcontextlost", e => { e.preventDefault(); G.glLost = (G.glLost || 0) + 1;', 'cv.addEventListener("webglcontextlost", e => { e.preventDefault(); if (cv._udfFree) return; G.glLost = (G.glLost || 0) + 1;')
rep2('cv.addEventListener("webglcontextrestored", () => { if (G3 === W)', 'cv.addEventListener("webglcontextrestored", () => { if (!cv._udfFree && G3 === W)')
rep2('cv.addEventListener("webglcontextlost", e => { e.preventDefault(); crumb("base GPU reset");', 'cv.addEventListener("webglcontextlost", e => { e.preventDefault(); if (cv._udfFree) return; crumb("base GPU reset");')
rep2('T - (G.galAt || 0) > 20000) worldDrop("gal", "away 20 s"); if (C3 && view !== "base" && T - (G.colAt || 0) > 20000) worldDrop("col", "away 20 s");',
     'T - (G.galAt || 0) > 30000) worldDrop("gal", "away 30 s"); if (C3 && view !== "base" && T - (G.colAt || 0) > 30000) worldDrop("col", "away 30 s");')
open(p, "w").write(t)
# the studio's baked portraits are kept when its renderer is released, so nothing is baked twice
t = open(p).read()
def rep3(a, b):
    global t; assert t.count(a) == 1, a[:80]; t = t.replace(a, b)
rep3('if (k === "stu" && STU) { const s = STU; STU = null; glFree(s.renderer); }', 'if (k === "stu" && STU) { const s = STU; G.stuCache = s.cache; STU = null; glFree(s.renderer); }')
rep3('camera: new TH.PerspectiveCamera(28, 2, .1, 400), cache: {},', 'camera: new TH.PerspectiveCamera(28, 2, .1, 400), cache: G.stuCache || {},')
open(p, "w").write(t)
