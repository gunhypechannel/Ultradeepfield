#!/usr/bin/env python3
"""Sharpen a GLB's base-colour texture in place (unsharp mask), re-encoded as high-quality JPEG.
usage: glb_sharpen.py file.glb [radius=1.4] [percent=70] [threshold=2] [q=90]"""
import io, sys
from PIL import Image, ImageFilter
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from glb_pack import read, write
def main(p, radius=1.4, percent=70, threshold=2, q=90):
    j, b = read(p); m = j['materials'][0]['pbrMetallicRoughness']; bi = j['textures'][m['baseColorTexture']['index']]['source']
    out = bytearray(); nv = []
    for vi, bv in enumerate(j['bufferViews']):
        o = bv.get('byteOffset', 0); chunk = b[o:o + bv['byteLength']]
        if j['images'][bi]['bufferView'] == vi:
            im = Image.open(io.BytesIO(chunk)).convert('RGB').filter(ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold))
            bio = io.BytesIO(); im.save(bio, 'JPEG', quality=q, optimize=True, subsampling=0); chunk = bio.getvalue()
        while len(out) % 4: out.append(0)
        n = dict(bv); n['byteOffset'] = len(out); n['byteLength'] = len(chunk); n['buffer'] = 0; out += chunk; nv.append(n)
    j['bufferViews'] = nv; j['buffers'] = [{'byteLength': len(out)}]; write(p, j, bytes(out))
if __name__ == '__main__':
    a = sys.argv[1:]; main(a[0], *(float(x) for x in a[1:]))
