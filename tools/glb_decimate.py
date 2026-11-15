#!/usr/bin/env python3
"""Cut a single-mesh GLB (Meshy export) down to about `target` triangles by vertex clustering, without breaking its texture:
vertices are merged only when they share a grid cell in space AND in UV space, so UV seams stay sharp. Normals are re-averaged.
usage: glb_decimate.py in.glb out.glb target_tris"""
import sys, struct, json
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from glb_pack import read, write

CT = {5126: np.float32, 5125: np.uint32, 5123: np.uint16, 5121: np.uint8}
NC = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}


def get(j, b, i):
    a = j['accessors'][i]; v = j['bufferViews'][a['bufferView']]; dt = CT[a['componentType']]; n = NC[a['type']]
    off = v.get('byteOffset', 0) + a.get('byteOffset', 0); st = v.get('byteStride', 0) or np.dtype(dt).itemsize * n
    raw = np.frombuffer(b, dtype=np.uint8, count=st * (a['count'] - 1) + np.dtype(dt).itemsize * n, offset=off)
    if st == np.dtype(dt).itemsize * n: return np.frombuffer(raw.tobytes(), dtype=dt).reshape(a['count'], n)
    return np.stack([np.frombuffer(raw[k * st:k * st + np.dtype(dt).itemsize * n].tobytes(), dtype=dt) for k in range(a['count'])])


def cluster(P, UV, F, cell, uvq):
    q = np.floor((P - P.min(0)) / cell).astype(np.int64); u = np.floor(UV * uvq).astype(np.int64)
    key = np.concatenate([q, u], 1); _, lab = np.unique(key, axis=0, return_inverse=True); lab = lab.ravel()
    T = lab[F]; T = T[(T[:, 0] != T[:, 1]) & (T[:, 1] != T[:, 2]) & (T[:, 0] != T[:, 2])]
    _, first = np.unique(np.sort(T, 1), axis=0, return_index=True); return lab, T[np.sort(first)]


def main(src, dst, target):
    j, b = read(src); prim = j['meshes'][0]['primitives'][0]; at = prim['attributes']
    P = get(j, b, at['POSITION']).astype(np.float64); UV = get(j, b, at['TEXCOORD_0']).astype(np.float64); F = get(j, b, prim['indices']).astype(np.int64).reshape(-1, 3)
    ext = (P.max(0) - P.min(0)).max(); lo, hi = ext / 2000, ext / 40
    for _ in range(18):
        cell = (lo * hi) ** .5; lab, T = cluster(P, UV, F, cell, max(64, int(1 / cell * ext * .25)))
        if len(T) > target: lo = cell
        else: hi = cell
    lab, T = cluster(P, UV, F, hi, max(64, int(1 / hi * ext * .25)))
    n = lab.max() + 1; cnt = np.bincount(lab, minlength=n)[:, None]
    P2 = np.zeros((n, 3)); np.add.at(P2, lab, P); P2 /= cnt; U2 = np.zeros((n, 2)); np.add.at(U2, lab, UV); U2 /= cnt
    used = np.unique(T); remap = -np.ones(n, np.int64); remap[used] = np.arange(len(used)); T = remap[T]; P2 = P2[used]; U2 = U2[used]
    e1 = P2[T[:, 1]] - P2[T[:, 0]]; e2 = P2[T[:, 2]] - P2[T[:, 0]]; fn = np.cross(e1, e2); N = np.zeros_like(P2)
    for k in range(3): np.add.at(N, T[:, k], fn)
    N /= np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-12)
    P2 = P2.astype(np.float32); U2 = U2.astype(np.float32); N = N.astype(np.float32); I = T.astype(np.uint32).ravel()
    # rebuild: keep the image buffer views, replace geometry
    imgs = [(im, b[j['bufferViews'][im['bufferView']].get('byteOffset', 0):][:j['bufferViews'][im['bufferView']]['byteLength']]) for im in j.get('images', [])]
    out = bytearray(); bvs = []; accs = []
    def put(arr, target=None):
        while len(out) % 4: out.append(0)
        o = len(out); out.extend(arr.tobytes()); bv = {'buffer': 0, 'byteOffset': o, 'byteLength': arr.nbytes}
        if target: bv['target'] = target
        bvs.append(bv); return len(bvs) - 1
    def acc(arr, t, ct, target, mm=False):
        a = {'bufferView': put(arr, target), 'componentType': ct, 'count': len(arr), 'type': t}
        if mm: a['min'] = arr.min(0).tolist(); a['max'] = arr.max(0).tolist()
        accs.append(a); return len(accs) - 1
    pa = acc(P2, 'VEC3', 5126, 34962, True); na = acc(N, 'VEC3', 5126, 34962); ua = acc(U2, 'VEC2', 5126, 34962); ia = acc(I, 'SCALAR', 5125, 34963)
    for im, data in imgs: im['bufferView'] = put(np.frombuffer(data, np.uint8))
    prim['attributes'] = {'POSITION': pa, 'NORMAL': na, 'TEXCOORD_0': ua}; prim['indices'] = ia
    j['accessors'] = accs; j['bufferViews'] = bvs; j['buffers'] = [{'byteLength': len(out)}]
    write(dst, j, bytes(out)); print('tris', len(F), '->', len(T), 'verts', len(P), '->', len(P2))


if __name__ == '__main__': main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
