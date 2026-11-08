# v351: sharper buildings on the base. (1) Model textures used anisotropy 4; the base camera sees buildings at a slant, where low
# anisotropy smears them. They now use texAniso() like the rest of the game (up to 16). (2) Phones kept a 1024 px colour map; buildings
# now keep 1536 px (ships stay 1024: they are only drawn into small battle sprites). (3) The shrink used the canvas default (low) resampling;
# now high quality. (4) The building colour maps in docs/models were sharpened once (tools/glb_sharpen.py: unsharp mask, JPEG q90 4:4:4).
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep('c.getContext("2d").drawImage(im, 0, 0, c.width, c.height);', 'const x2 = c.getContext("2d"); x2.imageSmoothingEnabled = true; x2.imageSmoothingQuality = "high"; x2.drawImage(im, 0, 0, c.width, c.height);')
rep('const s = g.scene, big = MOBILE ? 1024 : 2048, aux = MOBILE ? 512 : 1024;', 'const s = g.scene, big = MOBILE ? (GLB_BLDS.has(k) ? 1536 : 1024) : 2048, aux = MOBILE ? 512 : 1024, an = texAniso();')
rep('if (m.map) m.map.anisotropy = 4; } } });', 'for (const t of [m.map, m.normalMap]) if (t) t.anisotropy = an; } } });')
open(p, "w").write(h); print("ok")
