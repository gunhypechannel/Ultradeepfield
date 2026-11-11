# v425: the game holds far less memory in the background, so iOS (and Android) are much less likely to close it there.
#  1. Drawing buffers: when the page hides, the map's and the base's WebGL drawing buffers shrink to 1 x 1 and the base's bloom targets
#     are released (full-screen, anti-aliased, at up to 2x: well over 100 MB on an iPhone); on return they are sized again on the next
#     frame. Nothing is rebuilt and no shader recompiles (v381: rebuilding whole worlds on return froze and crashed; this does not).
#  2. The battle report's boss renderer is freed and the picture studio is released on every phone (it was iPhone only), and its baked
#     battle-view sprites (up to ~100 canvases) are dropped unless a battle is open; they bake again when a battle opens.
#  3. The Convergence theme (v414) streams from a media element instead of a fully decoded buffer (139 s of stereo float: ~49 MB kept
#     for the whole session once heard).
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("""setTimeout(() => { try { C.src.stop(); } catch (e) {} try { C.out.disconnect(); } catch (e) {} }, 4000);""",
    """setTimeout(() => { try { if (!(AU.conv && AU.conv.el === C.el)) C.el.pause(); } catch (e) {} try { C.out.disconnect(); } catch (e) {} }, 4000);""")
rep("""  if (!AU.convBuf) { if (!AU.convLd) { AU.convLd = 1; fetch("music_conv.mp3").then(r => { if (!r.ok) throw 0; return r.arrayBuffer(); }).then(b => c.decodeAudioData(b)).then(b => { AU.convBuf = b; }, () => { setTimeout(() => { AU.convLd = 0; }, 60000); }); } return; }
  if (!AU.conv) { const out = c.createGain(); out.gain.value = 0; out.connect(AU.master); const src = c.createBufferSource(); src.buffer = AU.convBuf; src.loop = true; src.connect(out); src.start(); AU.conv = { out, src }; AU.cduck = 0; applyAudio(); }
  AU.conv.out.gain.setTargetAtTime(AU.musicOn && !AU.muted ? .12 * gainOf(AU.mv) / gainOf(50) * (AU.duck || 1) : 0, c.currentTime, AU.conv.on ? .3 : 2); AU.conv.on = 1; }""",
    """  if (!AU.conv) { let el = AU.convEl; if (!el) { el = AU.convEl = new Audio("music_conv.mp3"); el.loop = true; el.preload = "auto"; try { AU.convSrc = c.createMediaElementSource(el); } catch (e) { AU.convSrc = null; } } /* v425 streamed, not decoded into memory */
    const out = c.createGain(); out.gain.value = 0; out.connect(AU.master); if (AU.convSrc) { try { AU.convSrc.disconnect(); } catch (e) {} AU.convSrc.connect(out); } try { el.currentTime = 0; } catch (e) {} el.play().catch(() => {}); AU.conv = { out, el }; AU.cduck = 0; applyAudio(); }
  const vv = AU.musicOn && !AU.muted ? .12 * gainOf(AU.mv) / gainOf(50) * (AU.duck || 1) : 0; AU.conv.out.gain.setTargetAtTime(vv, c.currentTime, AU.conv.on ? .3 : 2); if (!AU.convSrc) AU.conv.el.volume = clamp(vv * 8, 0, 1); AU.conv.on = 1; }""")
rep("""const MEM_DIET = IOS;""", """const MEM_DIET = IOS;
/* v425 the background diet: shed what comes back for free (drawing buffers, bloom targets, the boss renderer, the studio and its battle
   sprites) the moment the page hides, so the phone is far less likely to close the game in the background; sized again on return */
function bgDiet(on) { try {
  if (on) { if (G.bgDiet) return; G.bgDiet = 1; let n = 0;
    for (const W of [G3, C3]) { if (!W || !W.renderer) continue; try { W.renderer.setSize(1, 1, false); W.size = [1, 1]; n++; const B = W.bloom; if (B) { for (const k of ["S", "A", "A2", "C", "C2"]) if (B[k]) { B[k].dispose(); B[k] = null; } B.size = [0, 0]; } } catch (e) {} }
    try { wbArtFree(); } catch (e) {}
    if (MOBILE) { try { worldDrop("stu", "background"); } catch (e) {} if (!battle && G.stuCache) for (const k in G.stuCache) if (/\\|side$/.test(k)) delete G.stuCache[k]; }
    try { crumb("background: " + n + " drawing buffers released"); } catch (e) {} }
  else if (G.bgDiet) { G.bgDiet = 0; for (const W of [G3, C3]) if (W) W.size = [0, 0]; if (battle) try { gpuNap(true); } catch (e) {} try { startAnim(); } catch (e) {} }
} catch (e) {} }
document.addEventListener("visibilitychange", () => bgDiet(document.hidden)); addEventListener("pagehide", () => bgDiet(true)); addEventListener("pageshow", () => { if (!document.hidden) bgDiet(false); });""")
t = t.replace("const GAME_V = 424;", "const GAME_V = 425;")
open(p, "w").write(t); print("ok")
