#!/usr/bin/env python3
"""Give an optimized GLB the full-size textures from Meshy's raw export.
usage: glb_retex.py opt.glb raw.glb out.glb [base=2048] [aux=1024] [q=85]
Images are matched by role (base colour / metal-roughness / normal) through the materials."""
import io, sys
from PIL import Image
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from glb_pack import read, write, bbox

def role_images(j):
    out = {}
    m = j['materials'][0]; p = m.get('pbrMetallicRoughness', {})
    if 'baseColorTexture' in p: out['base'] = j['textures'][p['baseColorTexture']['index']]['source']
    if 'metallicRoughnessTexture' in p: out['mr'] = j['textures'][p['metallicRoughnessTexture']['index']]['source']
    if 'normalTexture' in m: out['nrm'] = j['textures'][m['normalTexture']['index']]['source']
    return out

def img_bytes(j, b, i):
    bv = j['bufferViews'][j['images'][i]['bufferView']]; o = bv.get('byteOffset', 0); return b[o:o + bv['byteLength']]

def main(optp, rawp, outp, base=2048, aux=1024, q=85):
    jo, bo = read(optp); jr, br = read(rawp)
    ro, rr = role_images(jo), role_images(jr)
    newimg = {}
    for role, io_ in ro.items():
        src = img_bytes(jr, br, rr[role]) if role in rr else img_bytes(jo, bo, io_)
        im = Image.open(io.BytesIO(src)).convert('RGB'); px = base if role == 'base' else aux
        if im.width > px: im = im.resize((px, px * im.height // im.width), Image.LANCZOS)
        bio = io.BytesIO(); im.save(bio, 'JPEG', quality=q, optimize=True); newimg[io_] = bio.getvalue()
    views = {img['bufferView']: i for i, img in enumerate(jo['images'])}
    out = bytearray(); nv = []
    for vi, bv in enumerate(jo['bufferViews']):
        o = bv.get('byteOffset', 0); chunk = bo[o:o + bv['byteLength']]
        if vi in views and views[vi] in newimg: chunk = newimg[views[vi]]; jo['images'][views[vi]]['mimeType'] = 'image/jpeg'
        while len(out) % 4: out.append(0)
        n = dict(bv); n['byteOffset'] = len(out); n['byteLength'] = len(chunk); n['buffer'] = 0; out += chunk; nv.append(n)
    jo['bufferViews'] = nv; jo['buffers'] = [{'byteLength': len(out)}]
    write(outp, jo, bytes(out))

if __name__ == '__main__':
    a = sys.argv[1:]; main(a[0], a[1], a[2], *(int(x) for x in a[3:]))
    import os; print(os.path.basename(a[2]), f"{os.path.getsize(a[2])/1e6:.2f} MB")
