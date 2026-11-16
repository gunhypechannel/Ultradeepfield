# fb-20261115: iPhone/iPad memory crashes (owner's iPhone, v589 and v592, 5 reports). The v586 readout shows the v588 wait
# works (only one 3D world alive), but each world alone is heavy: map ~145-160 MB of textures, base ~165-220 MB.
# Owner chose option 1: lower-resolution pictures on iPhone only.
# glNew(o, cap): on iOS the renderer's canvas reports MAX_TEXTURE_SIZE = cap, so three.js scales every larger picture down
# when it uploads it to the GPU (its built-in resizeImage). Only that renderer is affected; the source pictures are untouched.
# iosTexCap: map 512 (planet surfaces 1024x512 -> 512x256), base 768 (building models 1024 -> 768). Desktop/Android unchanged.
# memEst counts textures at the capped size and reports the cap (galC / colC) so the next crash reports show the effect.
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('function glNew(o) { const r = new TH.WebGLRenderer(o);',
  'function iosTexCap(k) { return k === "gal" ? 512 : 768; } /* fb-20261115 iPhone/iPad: largest texture side per 3D world (map, base); a function so it is ready before this line runs */\n'
  'function glCap(cv, cap) { const g0 = cv.getContext; cv.getContext = function (n, a) { const gl = g0.call(this, n, a); if (gl && !gl.__udfCap) { const gp = gl.getParameter; gl.__udfCap = cap; gl.getParameter = function (q) { const v = gp.call(this, q); return q === 3379 ? Math.min(v, cap) : v; }; } return gl; }; } /* 3379 = MAX_TEXTURE_SIZE */\n'
  'function glNew(o, cap) { if (cap && IOS && o && o.canvas) try { glCap(o.canvas, cap); } catch (e) {} const r = new TH.WebGLRenderer(o);'),
 ('try { renderer = glNew({ canvas: cv, antialias: GFX_AA, powerPreference: "high-performance" });',
  'try { renderer = glNew({ canvas: cv, antialias: GFX_AA, powerPreference: "high-performance" }, iosTexCap("gal"));'),
 ('renderer = glNew({ canvas: cv, antialias: GFX_AA || !MOBILE, powerPreference: "high-performance" });',
  'renderer = glNew({ canvas: cv, antialias: GFX_AA || !MOBILE, powerPreference: "high-performance" }, iosTexCap("col"));'),
 ('const seen = new Set(); let b = 0;\n',
  'const seen = new Set(); let b = 0; const cap = W.renderer && W.renderer.capabilities && W.renderer.capabilities.maxTextureSize || 1e9; /* fb-20261115 count at the size the GPU holds */\n'),
 ('b += px(t.image) * 4',
  'b += (t.image && !Array.isArray(t.image) ? (() => { const w = t.image.naturalWidth || t.image.width || 0, h = t.image.naturalHeight || t.image.height || 0, s = Math.min(1, cap / Math.max(w, h, 1)); return Math.floor(w * s) * Math.floor(h * s); })() : px(t.image)) * 4'),
 ('v[k] = Math.round(b / 1e6); v[k + "N"] = seen.size; }',
  'v[k] = Math.round(b / 1e6); v[k + "N"] = seen.size; if (cap < 2048) v[k + "C"] = cap; /* only when capped */ }'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
