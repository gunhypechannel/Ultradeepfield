#!/usr/bin/env python3
"""Shrink a GLB's textures in place: base colour stays at `base` px, normal and metal-roughness maps drop to `aux` px.
Rebuilds the binary chunk with fresh offsets. Also prints the model's bounding box (POSITION min/max after node transforms are ignored:
Meshy exports a single mesh at the origin).
usage: glb_pack.py in.glb out.glb [base=1024] [aux=512] [quality=82]"""
import io, json, struct, sys
from PIL import Image


def read(path):
    d = open(path, 'rb').read()
    magic, ver, L = struct.unpack('<4sII', d[:12])
    assert magic == b'glTF', path
    jl, jt = struct.unpack('<II', d[12:20])
    j = json.loads(d[20:20 + jl])
    o = 20 + jl
    bl, bt = struct.unpack('<II', d[o:o + 8])
    return j, d[o + 8:o + 8 + bl]


def write(path, j, binb):
    js = json.dumps(j, separators=(',', ':')).encode()
    js += b' ' * ((4 - len(js) % 4) % 4)
    binb += b'\0' * ((4 - len(binb) % 4) % 4)
    total = 12 + 8 + len(js) + 8 + len(binb)
    with open(path, 'wb') as f:
        f.write(struct.pack('<4sII', b'glTF', 2, total))
        f.write(struct.pack('<II', len(js), 0x4E4F534A)); f.write(js)
        f.write(struct.pack('<II', len(binb), 0x004E4942)); f.write(binb)


def roles(j):
    r = {}
    for m in j.get('materials', []):
        p = m.get('pbrMetallicRoughness', {})
        if 'baseColorTexture' in p: r[j['textures'][p['baseColorTexture']['index']]['source']] = 'base'
        if 'metallicRoughnessTexture' in p: r.setdefault(j['textures'][p['metallicRoughnessTexture']['index']]['source'], 'aux')
        if 'normalTexture' in m: r.setdefault(j['textures'][m['normalTexture']['index']]['source'], 'aux')
        if 'emissiveTexture' in m: r.setdefault(j['textures'][m['emissiveTexture']['index']]['source'], 'base')
    return r


def pack(src, dst, base=1024, aux=512, q=82):
    j, b = read(src)
    rl = roles(j)
    imgviews = {img['bufferView']: (i, img) for i, img in enumerate(j.get('images', [])) if 'bufferView' in img}
    out = bytearray(); newviews = []
    for vi, bv in enumerate(j['bufferViews']):
        o = bv.get('byteOffset', 0); chunk = b[o:o + bv['byteLength']]
        if vi in imgviews:
            i, img = imgviews[vi]
            px = base if rl.get(i, 'aux') == 'base' else aux
            im = Image.open(io.BytesIO(chunk)); im = im.convert('RGB')
            if im.width > px: im = im.resize((px, px * im.height // im.width), Image.LANCZOS)
            bio = io.BytesIO(); im.save(bio, 'JPEG', quality=q, optimize=True); chunk = bio.getvalue(); img['mimeType'] = 'image/jpeg'
        while len(out) % 4: out.append(0)
        nb = dict(bv); nb['byteOffset'] = len(out); nb['byteLength'] = len(chunk); nb['buffer'] = 0
        out += chunk; newviews.append(nb)
    j['bufferViews'] = newviews; j['buffers'] = [{'byteLength': len(out)}]
    write(dst, j, bytes(out))
    return j


def bbox(j):
    mn = [1e9] * 3; mx = [-1e9] * 3; tris = 0
    for m in j['meshes']:
        for p in m['primitives']:
            a = j['accessors'][p['attributes']['POSITION']]
            mn = [min(x, y) for x, y in zip(mn, a['min'])]; mx = [max(x, y) for x, y in zip(mx, a['max'])]
            if 'indices' in p: tris += j['accessors'][p['indices']]['count'] // 3
    return mn, mx, tris


if __name__ == '__main__':
    a = sys.argv[1:]
    j = pack(a[0], a[1], *(int(x) for x in a[2:]))
    mn, mx, t = bbox(j)
    import os
    print(f"{os.path.basename(a[1])}: {os.path.getsize(a[1])/1e6:.2f} MB, {t} tris, size x{mx[0]-mn[0]:.2f} y{mx[1]-mn[1]:.2f} z{mx[2]-mn[2]:.2f}, nodes {[n.get('rotation') for n in j['nodes']][:2]}")
