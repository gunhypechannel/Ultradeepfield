# Hull silhouettes of the user's 3D prototypes: per slice along the length, top, bottom and half-width of the main shells
import json, struct, numpy as np, re
P = 'art-src/flagship-3d/'; N = 40; rng = np.random.default_rng(3); out = {}
SHELL = {'hull', 'upper_hull', 'lower_keel', 'superstructure', 'grand_deck', 'sun_deck', 'black_deck', 'stealth_bridge'}
for fac, f in [('terran', 'flag-terran.glb'), ('solar', 'flag-solar.glb'), ('nyx', 'flag-nyx-red.glb'), ('verdant', 'flag-verdant.glb')]:
    b = open(P + f, 'rb').read(); L = struct.unpack('<I', b[12:16])[0]; j = json.loads(b[20:20 + L]); bn = b[20 + L + 8:]
    def acc(i):
        a = j['accessors'][i]; bv = j['bufferViews'][a['bufferView']]; o = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
        dt = {5126: np.float32, 5125: np.uint32}[a['componentType']]; n = {'SCALAR': 1, 'VEC3': 3}[a['type']]
        return np.frombuffer(bn, dtype=dt, count=a['count'] * n, offset=o).reshape(-1, n)
    pts = []
    for nd in j['nodes']:
        if 'mesh' not in nd or re.sub(r'_\d+$', '', nd['name']) not in SHELL: continue
        for pr in j['meshes'][nd['mesh']]['primitives']:
            p = acc(pr['attributes']['POSITION']).astype(float); t = acc(pr['indices']).reshape(-1, 3)
            A, B, C = p[t[:, 0]], p[t[:, 1]], p[t[:, 2]]; area = np.linalg.norm(np.cross(B - A, C - A), axis=1) / 2
            for k in range(len(t)):
                n = int(min(400, 8 + area[k] * 30)); u = rng.random((n, 2)); m = u.sum(1) > 1; u[m] = 1 - u[m]
                pts.append(A[k] + u[:, :1] * (B[k] - A[k]) + u[:, 1:] * (C[k] - A[k]))
    pts = np.concatenate(pts); x0, x1 = pts[:, 0].min(), pts[:, 0].max(); top, bot, half = [], [], []
    for i in range(N):
        a, c = x0 + (x1 - x0) * i / N, x0 + (x1 - x0) * (i + 1) / N; s = pts[(pts[:, 0] >= a) & (pts[:, 0] <= c)]
        top.append(round(float(s[:, 2].max()), 3)); bot.append(round(float(s[:, 2].min()), 3)); half.append(round(float(np.abs(s[:, 1]).max()), 3))
    out[fac] = {'x0': round(float(x0), 3), 'x1': round(float(x1), 3), 't': top, 'b': bot, 'h': half}
    print(fac, out[fac]['x0'], out[fac]['x1'], 'top', top[::8], 'bot', bot[::8], 'half', half[::8])
open('prof.json', 'w').write(json.dumps(out, separators=(',', ':'))); print(len(json.dumps(out)))
