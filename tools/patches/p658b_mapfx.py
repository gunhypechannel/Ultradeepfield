# v658 map ships remaster (owner: "clean these ships up in map view ... clearer and HDR"; "remaster the other request").
# (1) sharper: while a cinematic camera runs, the phone's pixel budget grows by a third (and the 1.5x close-up limit lifts); far worlds
#     are trimmed to pay for it, and the jump happens at once. (2) HDR bloom on the map was tried and left out: the map draws in several passes and a single bloom pass greyed it. (3) clean finishes at map scale: the finish texture is blended with the finish's own colour, its speckle glints are
#     cut to a third, and the edge light is stronger, so a small ship reads as clean plating with a lit rim.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
rep('return clamp(Math.sqrt((IOS ?', 'return clamp(cineK() * Math.sqrt((IOS ?')
rep('const mobilePRCap = () =>', 'const cineK = () => { try { return MOBILE && view === "galaxy" && G3 && G3.cam && (G3.cam.cine || G3.cam.cineObj) ? 1.35 : 1; } catch (e) { return 1; } }; /* v658 */\nconst mobilePRCap = () =>')
rep('max = Math.min(gfxMaxPR(), mobilePRCap(), MOBILE && close ? 1.5 : 9);', 'max = Math.min(gfxMaxPR(), mobilePRCap(), MOBILE && close && cineK() === 1 ? 1.5 : 9);')
rep('W.nearK = clamp((W.nearK || 1) * (frame.ema > aim0 * 1.08 ? .85 : frame.ema < aim0 * .8 ? 1.08 : 1), .4, 1); }', 'W.nearK = clamp((W.nearK || 1) * (frame.ema > aim0 * 1.08 ? .85 : frame.ema < aim0 * .8 ? 1.08 : 1), .4, cineK() > 1 ? .6 : 1); }')
rep('function cineStart(m) {', 'function cineSharp() { setTimeout(() => { try { if (!G3 || !G3.renderer) return; const m = Math.min(gfxMaxPR(), mobilePRCap()); if (G3.renderer.getPixelRatio() < m - .01) { G3.renderer.setPixelRatio(m); G3.size = [0, 0]; } } catch (e) {} }, 60); } /* v658 */\nfunction cineStart(m) { cineSharp();')
rep('function cineObjStart(id, n) {', 'function cineObjStart(id, n) { cineSharp();')
rep('  { const B = W.renderer.pace; if (B) { B.scene = W.scene; B.used = 0; B.skips = 0; B.ms = MOBILE ? 22 : 45; } W.renderer.render(W.scene, W.camera);',
    '  { const B = W.renderer.pace; if (B) { B.scene = W.scene; B.used = 0; B.skips = 0; B.ms = MOBILE ? 22 : 45; } if (!mapBloom(W)) W.renderer.render(W.scene, W.camera);')
rep('function colBloom(W) {', '''/* v658 a cinematic raises the phone's resolution; when it ends, the resolution drops straight back to the safe budget */
function mapBloom(W) { const on = !!(W.cam && (W.cam.cine || W.cam.cineObj)); if (on) { W.cineWas = 1; return false; }
  if (W.cineWas) { W.cineWas = 0; try { const m = Math.min(gfxMaxPR(), mobilePRCap()); if (W.renderer.getPixelRatio() > m + .01) { W.renderer.setPixelRatio(m); W.size = [0, 0]; } } catch (e) {} } return false; }
function colBloom(W) {''')
rep('c${i} = t * (0.35 + 0.75 * smoothstep(0.0, 0.85, hl)); g${i} = t * pow(tl, 3.0) * uGl${i}; }`',
    'c${i} = t * (0.35 + 0.75 * smoothstep(0.0, 0.85, hl)); g${i} = t * pow(tl, 3.0) * uGl${i};${obj ? ` c${i} = mix(c${i}, uFin${i} * (0.3 + 0.8 * smoothstep(0.0, 0.85, hl)), .45); g${i} *= .3;` : ""} }`')
rep('''"#include <emissivemap_fragment>\\n { float hf = pow(1.0 - clamp(dot(normalize(normal), normalize(vViewPosition)), 0.0, 1.0), 2.2); totalEmissiveRadiance += uRim * hf * (" + (tex ? ".35" : ".85") + ")''',
    '''"#include <emissivemap_fragment>\\n { float hf = pow(1.0 - clamp(dot(normalize(normal), normalize(vViewPosition)), 0.0, 1.0), 2.2); totalEmissiveRadiance += uRim * hf * (" + (obj ? "1.1" : tex ? ".35" : ".85") + ")''')
rep('n.customProgramCacheKey = () => "hullfin2-" + f +', 'n.customProgramCacheKey = () => "hullfin3-" + f +')
open(p, 'w', encoding='utf-8').write(s)
