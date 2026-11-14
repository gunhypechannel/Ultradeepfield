# v537 the iPhone memory plan (owner: "Game crashes and closes a lot, what are your ideas to fix it once and for all?" then "Yes").
# His crash reports: iOS closes the game when graphics memory runs out: crashes seconds after "map ready in the background" (the base and
# the galaxy both built), "GPU reset" lines, and the hidden map drawing at 1.89x on a 3x screen. Now:
#  1. one 3D world at a time on iPhone/iPad: no background map build (mapPrewarm off on iOS), and 8 s after you leave a world (base or
#     galaxy) for the other, the one you left is released (worldDrop); away from both, only the one used last stays. Rebuilds are paced
#     (the base's render is shader-paced now too, like the map since v530).
#  2. a memory budget on iOS: no supersampling (scale capped at 1), a pixel budget per memory tier (1.0M / .75M / .55M / .4M drawing-buffer
#     pixels: about 1.6x / 1.4x / 1.2x / 1.0x on an iPhone); the studio renderer is released 15 s after its last use and the boss art
#     renderer whenever no battle is open.
#  3. the memory tier adapts (MEMT, localStorage udf.memTier, phones and tablets): +1 after a session that crashed (max 3), -1 after three
#     clean sessions of 10+ minutes in a row. Tier 1+ turns antialiasing off (next launch); tier 2+ lowers effects and detail.
#  4. the memory meter: every crash beat now carries ctx (live 3D contexts), fbMB (their drawing buffers, MB, estimated) and mt (the tier).
#  5. tools/ios_memcheck.js checks a build like an iPhone (iPhone user agent): one world alive after switching, the studio released, the
#     pixel budget kept.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('''if (MOBILE) { try { if (G.crashBoot) localStorage.setItem("udf.safeUntil", String(Date.now() + 3 * 864e5)); if (+localStorage.getItem("udf.safeUntil") > Date.now()) G.glSafe = 1; } catch (e) {} } /* v445 */''',
    '''if (MOBILE) { try { if (G.crashBoot) localStorage.setItem("udf.safeUntil", String(Date.now() + 3 * 864e5)); if (+localStorage.getItem("udf.safeUntil") > Date.now()) G.glSafe = 1; } catch (e) {} } /* v445 */
/* v537 the memory tier: 0 normal .. 3 lightest; +1 after a session that crashed, -1 after three clean sessions of 10+ minutes in a row */
const MEMT = (() => { if (!MOBILE) return 0; try { const o = JSON.parse(localStorage.getItem("udf.memTier") || "{}") || {}; let t = clamp(+o.t || 0, 0, 3), ok = +o.ok || 0; if (G.crashBoot) { t = Math.min(3, t + 1); ok = 0; }
  localStorage.setItem("udf.memTier", JSON.stringify({ t, ok }));
  setTimeout(() => { try { const q = JSON.parse(localStorage.getItem("udf.memTier") || "{}") || {}; let n = (+q.ok || 0) + 1, tt = +q.t || 0; if (n >= 3 && tt > 0) { tt--; n = 0; } localStorage.setItem("udf.memTier", JSON.stringify({ t: tt, ok: n })); } catch (e) {} }, 600000);
  return t; } catch (e) { return 0; } })();''')
rep('function gfx(k) { if (G.glSafe && (k === "scale" || k === "fx" || k === "detail")) {', '''function gfx(k) { if (IOS && k === "scale") { const v0 = GFX.over && GFX.over.scale != null ? GFX.over.scale : GFX_PRESETS[gfxPreset()].scale; return Math.min(v0, 1); } /* v537 no supersampling on iPhone/iPad */
  if (MOBILE && MEMT >= 2 && (k === "fx" || k === "detail")) { const v0 = GFX.over && GFX.over[k] != null ? GFX.over[k] : GFX_PRESETS[gfxPreset()][k]; return Math.max(0, v0 - (MEMT - 1)); }
  if (G.glSafe && (k === "scale" || k === "fx" || k === "detail")) {''')
rep('return clamp(Math.sqrt((WEAK ? 2e6 : G.glSafe ? 1.4e6 : st ? 4.6e6 : 3.4e6) / px), 1,', 'return clamp(Math.sqrt((IOS ? [1e6, .75e6, .55e6, .4e6][MEMT] : (WEAK ? 2e6 : G.glSafe ? 1.4e6 : st ? 4.6e6 : 3.4e6) * [1, .75, .55, .4][MEMT]) / px), 1, /* v537 the iPhone budget */')
rep('const GFX_AA = !WEAK && !!gfx("aa");', 'const GFX_AA = !WEAK && !!gfx("aa") && !(MOBILE && MEMT >= 1); /* v537 */')
rep('function mapPrewarm() { if (mapHost || G3 ||', 'function mapPrewarm() { if (IOS) return; /* v537 one world at a time on iPhone/iPad */ if (mapHost || G3 ||')
rep('''function studio() {
  if (STU !== null) return STU || null;''', '''function studio() { G.stuT = Date.now(); /* v537 */
  if (STU !== null) return STU || null;''')
rep('''  { const B = W.bloomOff ? null : colBloom(W); let ok = false; if (B) try { B.run(); ok = true; } catch (e) { W.bloom = null; W.renderer.setRenderTarget(null); } if (!ok) W.renderer.render(W.scene, W.cam); } // v354 bloom''',
    '''  { const P = W.renderer.pace; if (P) { P.scene = W.scene; P.used = 0; P.skips = 0; P.ms = MOBILE ? 22 : 45; } /* v537 the base paces its shaders too */
    const B = W.bloomOff ? null : colBloom(W); let ok = false; if (B) try { B.run(); ok = true; } catch (e) { W.bloom = null; W.renderer.setRenderTarget(null); } if (!ok) W.renderer.render(W.scene, W.cam); if (P) P.scene = null; } // v354 bloom''')
# one world at a time, the studio and the boss art renderer released when idle
rep('function render(keepScroll) {', '''/* v537 one 3D world at a time on iPhone/iPad: 8 s after you leave a world for the other it is released; away from both, the last used stays */
setInterval(() => { try { if (!IOS || !G.ready || document.hidden) return; const T = Date.now(); if (view === "galaxy") G.lastGal = T; if (view === "base") G.lastCol = T;
  if (!battle) { const lg = G.lastGal || 0, lc = G.lastCol || 0;
    if (G3 && view !== "galaxy" && T - lg > 8000 && (view === "base" || lc > lg)) worldDrop("gal", "one world on iPhone");
    if (C3 && view !== "base" && T - lc > 8000 && (view === "galaxy" || lg > lc)) worldDrop("col", "one world on iPhone");
    if (typeof WBR !== "undefined" && WBR.r) wbArtFree(); }
  if (STU && !battle && T - (G.stuT || 0) > 15000) worldDrop("stu", "idle"); } catch (e) {} }, 2000);
function render(keepScroll) {''')
# the memory meter in every beat
rep('art: (() => { try { return STU && STU.cache ? Object.keys(STU.cache).length : null; } catch (e) { return null; } })(),', '''art: (() => { try { return STU && STU.cache ? Object.keys(STU.cache).length : null; } catch (e) { return null; } })(), mt: typeof MEMT !== "undefined" ? MEMT : null, /* v537 the memory meter */
    ...(() => { try { const rs = [G3 && G3.renderer, C3 && C3.renderer, STU && STU.renderer, typeof WBR !== "undefined" && WBR.r].filter(Boolean); let mb = 0; for (const r of rs) { const gl = r.getContext(), a = r.getContextAttributes ? r.getContextAttributes() : {}; mb += gl.drawingBufferWidth * gl.drawingBufferHeight * (4 + 4) * (a && a.antialias ? 4 : 1) * (a && a.preserveDrawingBuffer ? 2 : 1) / 1e6; } return { ctx: rs.length, fbMB: Math.round(mb) }; } catch (e) { return {}; } })(),''')
s2 = re.sub(r"GAME_V = 536\b", "GAME_V = 537", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
