# v383: (1) the first trip to the map no longer stalls: the galaxy is built quietly in the background a few seconds after the game is
# ready (hidden, off-screen, with a few frames drawn so shaders, ships and planet textures are ready); tapping Map then only moves it on
# screen. (2) In Chrome's desktop-site frame (Fold) the game runs inside a zoomed frame where the page reports ~7x pixel density; the
# map, base and overlays capped their resolution at 2x of the frame's big CSS pixels, so everything was drawn at under half the needed
# resolution and stretched (blocky, oversized). The caps now scale with the frame's zoom.
p = "docs/index.html"; t = open(p).read()
def rep(a, b):
    global t; assert t.count(a) == 1, a[:90]; t = t.replace(a, b)
# (2) resolution caps follow the frame's zoom
rep('const DPR = () => Math.min(window.devicePixelRatio || 1, 2);',
    'const FZ = () => { try { const f = window.frameElement; return f ? Math.max(1, parseFloat(f.style.zoom) || 1) : 1; } catch (e) { return 1; } }; // v383: the desktop-site frame zooms the page\nconst DPR = () => Math.min(window.devicePixelRatio || 1, 2 * FZ());')
rep('const gfxMaxPR = () => clamp((window.devicePixelRatio || 1) * gfx("scale"), .6, 2.5);', 'const gfxMaxPR = () => clamp((window.devicePixelRatio || 1) * gfx("scale"), .6, 2.5 * FZ());')
rep('return clamp(Math.sqrt((WEAK ? 2e6 : G.glSafe ? 2.4e6 : 3.4e6) / px), 1, 2); };', 'return clamp(Math.sqrt((WEAK ? 2e6 : G.glSafe ? 2.4e6 : 3.4e6) / px), 1, 2 * FZ()); };')
# (1) the map mount becomes a function, used by render and by the background build
i = t.index('    if (!mapHost) { const tmp = document.createElement("div"); tmp.innerHTML = mapShell(!!TH && !G3fail); mapHost = tmp.firstElementChild; }')
j = t.index('    mapOverlay();\n    if (render.last !== "galaxy" && !reduced)', i)
blk = t[i:j]
t = t[:i] + '    mapMount(m); { const pk = $("#mappark"); if (pk && !pk.firstChild) pk.remove(); } /* v383: a map built in the background just moves on screen */\n' + t[j:]
fn = "/* v383 mount the galaxy map in container m (the main view, or the hidden park while it is built in the background) */\nfunction mapMount(m) {\n" + blk + "}\n"
fn += '''/* v383: build the map quietly before the first tap: after 6 s of calm on the base, park it off-screen, build it and draw a few frames */
function mapPrewarm() { if (mapHost || G3 || !TH || G3fail || view === "galaxy" || battle || sheet || document.hidden || !G.ready) return;
  const pk = document.createElement("div"); pk.id = "mappark"; pk.setAttribute("aria-hidden", "true"); { const vr = ($("#view") || document.body).getBoundingClientRect(); /* the map's exact box (view width, full height): a different size would mean a full resize on the first frame */ pk.style.cssText = `position:fixed;left:${vr.left}px;top:0;width:${vr.width}px;height:${innerHeight}px;display:flex;flex-direction:column;visibility:hidden;pointer-events:none;z-index:-1;overflow:hidden`; /* the map box is a flex child */ } document.body.appendChild(pk);
  const t0 = performance.now(); try { mapMount(pk); } catch (e) { try { crumb("map prewarm failed: " + e.message); } catch (er) {} }
  let n = 0; const step = () => { if (!G3 || view === "galaxy" || !$("#mappark") || !$("#mappark").firstChild) return; try { draw3D(performance.now()); if (n === 6 && !G3.warmed) { G3.warmed = 1; mapWarm(performance.now()); } } catch (e) {} if (++n < 10) setTimeout(() => requestAnimationFrame(step), 300); else try { crumb(`map ready in the background (${Math.round(performance.now() - t0)} ms)`); } catch (e) {} };
  requestAnimationFrame(step); }
setInterval(() => { try { if (mapHost || !G.ready || view !== "base" || sheet || battle || document.hidden || advLines) { G.mpCalm = 0; return; } if (++G.mpCalm >= 3) (window.requestIdleCallback || setTimeout)(mapPrewarm, { timeout: 1500 }); } catch (e) {} }, 2000);
'''
k = t.index('function render(')
t = t[:k] + fn + t[k:]
open(p, "w").write(t)
# (3) a light that appears later recompiles every lit material on the map (a multi-second stall on first open and the first time
# anything explodes, or the Cube event shows/hides). The missile/explosion light now exists from the start, and the Cube's key light
# lives in the scene all the time (zero brightness while the Cube is hidden), so the light count never changes.
t = open(p).read()
rep('  scene.add(new TH.PointLight(0xffd2a6, 2.1, 0));', '  scene.add(new TH.PointLight(0xffd2a6, 2.1, 0));\n  scene.userData.cubeSun = new TH.PointLight(0xffd0a0, 0, 520, 1.2); scene.add(scene.userData.cubeSun); /* v383: the Cube\'s key light, always in the scene */')
rep('rock.position.set(-150, 6, 115); const sun = new TH.PointLight(0xffd0a0, 2.4, 520, 1.2); sun.position.set(-80, 70, 30); grp.add(sun);',
    'rock.position.set(-150, 6, 115); /* v383: its key light is scene.userData.cubeSun (always in the scene), lit by cubeLiveFx */')
rep('if (!X) X = W.cubeX = cubeLiveBuild(W); X.grp.visible = true;', 'if (!X) X = W.cubeX = cubeLiveBuild(W); X.grp.visible = true; { const L = W.scene.userData.cubeSun; if (L) { L.intensity = 2.4; L.position.set(-80, 70, 30); X.grp.localToWorld(L.position); } }')
rep('const ph = cubePhase(T); let X = W.cubeX; if (!ph) { if (X) X.grp.visible = false; return; }', 'const ph = cubePhase(T); let X = W.cubeX; if (!ph) { if (X) X.grp.visible = false; if (W.scene.userData.cubeSun) W.scene.userData.cubeSun.intensity = 0; return; }')
rep('if (TH && !G3fail) { G3 = init3D(mapHost); if (G3) {', 'if (TH && !G3fail) { G3 = init3D(mapHost); if (G3) { try { misKit(G3); } catch (e) {} /* v383: its light exists from the start */')
open(p, "w").write(t)
