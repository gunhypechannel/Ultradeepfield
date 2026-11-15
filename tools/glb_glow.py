#!/usr/bin/env python3
"""Recolour a GLB's emissive (glow) texture: every lit pixel keeps its brightness and takes the new hue.
usage: glb_glow.py in.glb out.glb RRGGBB [RRGGBB2]   (with a second colour, glow alternates by brightness: bright = colour 1, dim = colour 2)"""
import io, sys
import numpy as np
from PIL import Image
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from glb_pack import read, write
A = [x for x in sys.argv[1:] if not x.startswith('--')]; src, dst, c1 = A[:3]; c2 = A[3] if len(A) > 3 else c1
col = lambda h: np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255
j, b = read(src); m = j['materials'][0]; ti = m['emissiveTexture']['index']; ii = j['textures'][ti]['source']; vi = j['images'][ii]['bufferView']
out = bytearray(); views = []
for k, bv in enumerate(j['bufferViews']):
    o = bv.get('byteOffset', 0); ch = b[o:o + bv['byteLength']]
    if k == vi:
        a = np.asarray(Image.open(io.BytesIO(ch)).convert('RGB'), np.float32) / 255; L = a.max(2, keepdims=True)
        t = np.clip((L - .35) / .5, 0, 1); rgb = (col(c2) * (1 - t) + col(c1) * t) * L * 1.15
        bio = io.BytesIO(); Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).save(bio, 'JPEG', quality=86); ch = bio.getvalue()
    while len(out) % 4: out.append(0)
    nb = dict(bv); nb['byteOffset'] = len(out); nb['byteLength'] = len(ch); out += ch; views.append(nb)
j['bufferViews'] = views; j['buffers'] = [{'byteLength': len(out)}]; write(dst, j, bytes(out)); print('ok', dst)
# also turn the base colour's orange lights into the glow colour (--base)
if '--base' in sys.argv:
    j, b = read(dst); m = j['materials'][0]; vi = j['images'][j['textures'][m['pbrMetallicRoughness']['baseColorTexture']['index']]['source']]['bufferView']
    out = bytearray(); views = []
    for k, bv in enumerate(j['bufferViews']):
        o = bv.get('byteOffset', 0); ch = b[o:o + bv['byteLength']]
        if k == vi:
            im = Image.open(io.BytesIO(ch)).convert('RGB'); hsv = np.asarray(im.convert('HSV'), np.float32); h, s, v = hsv[..., 0] * 360 / 255, hsv[..., 1] / 255, hsv[..., 2] / 255
            sel = ((h < 55) | (h > 340)) & (s > .35) & (v > .25); a = np.asarray(im, np.float32) / 255
            tgt = col(c1)[None, None, :] * v[..., None] * 1.1; a[sel] = np.clip(tgt[sel], 0, 1)
            bio = io.BytesIO(); Image.fromarray((a * 255).astype(np.uint8)).save(bio, 'JPEG', quality=84); ch = bio.getvalue(); print('recoloured', int(sel.sum()), 'base pixels')
        while len(out) % 4: out.append(0)
        nb = dict(bv); nb['byteOffset'] = len(out); nb['byteLength'] = len(ch); out += ch; views.append(nb)
    j['bufferViews'] = views; j['buffers'] = [{'byteLength': len(out)}]; write(dst, j, bytes(out))
