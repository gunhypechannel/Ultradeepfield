# Signed-distance sculpting for Ultra Deep Field hulls (v742): primitives, booleans, a marching-cubes mesher, and a baker that
# writes positions, normals and per-vertex material (albedo + roughness, emissive + metalness) with baked ambient occlusion.
# A model is a list of named parts; every part is (name, sdf(p) -> d, material). The mesh is the smooth union of the parts,
# minus the carves; each vertex takes the material of the nearest part. tools/sculpt/pack.js simplifies and packs it.
import numpy as np
from skimage.measure import marching_cubes
f32 = np.float32
def L(v): return np.sqrt(np.sum(v * v, axis=-1))
def smin(a, b, k):
    if k <= 0: return np.minimum(a, b)
    h = np.clip(.5 + .5 * (b - a) / k, 0, 1); return b * (1 - h) + a * h - k * h * (1 - h)
def smax(a, b, k): return -smin(-a, -b, k)
def V(*a): return np.array(a, f32)
def rot(ax, ang):
    c, s = np.cos(ang), np.sin(ang)
    if ax == 'x': return np.array([[1, 0, 0], [0, c, -s], [0, s, c]], f32)
    if ax == 'y': return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], f32)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], f32)
# ---- primitives (p: (..., 3)) ----
def box(p, c, h, r=0, R=None):
    q = p - V(*c)
    if R is not None: q = q @ R
    q = np.abs(q) - (V(*h) - r); return L(np.maximum(q, 0)) + np.minimum(np.max(q, -1), 0) - r
def sphere(p, c, r): return L(p - V(*c)) - r
def ell(p, c, r):
    q = (p - V(*c)) / V(*r); k0 = L(q); k1 = L(q / V(*r)); return k0 * (k0 - 1) / np.maximum(k1, 1e-6)
def rcone(p, a, b, r1, r2):
    a = V(*a); b = V(*b); ba = b - a; l2 = ba @ ba; rr = r1 - r2; a2 = l2 - rr * rr; il2 = 1 / l2
    pa = p - a; y = pa @ ba; z = y - l2; xv = pa * l2 - y[..., None] * ba; x2 = np.sum(xv * xv, -1); y2 = y * y * l2; z2 = z * z * l2
    k = np.sign(rr) * rr * rr * x2
    return np.where(np.sign(z) * a2 * z2 > k, np.sqrt(x2 + z2) * il2 - r2, np.where(np.sign(y) * a2 * y2 < k, np.sqrt(x2 + y2) * il2 - r1, (np.sqrt(np.maximum(x2 * a2 * il2, 0)) + y * rr) * il2 - r1))
def cap(p, a, b, r): return rcone(p, a, b, r, r)
def cyl(p, c, axis, r, h, rr=0):  # a capped cylinder along axis 'x'|'y'|'z', radius r, half-height h, edge rounding rr
    q = p - V(*c); i = 'xyz'.index(axis); a = q[..., i]; o = np.delete(q, i, axis=-1)
    d = np.stack([L(o) - (r - rr), np.abs(a) - (h - rr)], -1); return np.minimum(np.max(d, -1), 0) + L(np.maximum(d, 0)) - rr
def torus(p, c, axis, R, r):
    q = p - V(*c); i = 'xyz'.index(axis); a = q[..., i]; o = np.delete(q, i, axis=-1)
    return np.sqrt((L(o) - R) ** 2 + a * a) - r
def spike(p, base, tip, r): return rcone(p, base, tip, r, r * .04)
def poly2(x, z, P):
    # signed distance (planes, exact enough near the surface) to a convex outline P [(x, z)...]
    n = len(P); area = sum(P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1] for i in range(n)); sg = 1 if area > 0 else -1; d = None
    for i in range(n):
        x0, z0 = P[i]; x1, z1 = P[(i + 1) % n]; ex, ez = x1 - x0, z1 - z0; l = np.hypot(ex, ez)
        if l < 1e-6: continue
        nx, nz = sg * ez / l, -sg * ex / l; e = (x - x0) * nx + (z - z0) * nz; d = e if d is None else np.maximum(d, e)
    return d
def hull(p, pts, ytop, ybot, ch=.12, r=.02, c=(0, 0, 0), R=None):
    # an armour plate: a convex outline on the +z side (x, z), mirrored, extruded from ybot to ytop with chamfered top and bottom edges
    q = p - V(*c)
    if R is not None: q = q @ R
    P = [(x, z) for x, z in pts] + [(x, -z) for x, z in reversed(pts) if z > 0]
    x, y, z = q[..., 0], q[..., 1], q[..., 2]; d2 = poly2(x, z, P)
    d = np.maximum(np.maximum(d2, y - ytop), ybot - y); s2 = .7071
    d = np.maximum(d, (d2 + y - ytop + ch) * s2); d = np.maximum(d, (d2 + ybot - y + ch) * s2)
    return d - r
# ---- the mesher and baker ----
class Model:
    def __init__(self, lo, hi, vox):
        self.lo, self.hi, self.vox = np.array(lo, f32), np.array(hi, f32), vox; self.parts = []; self.carves = []
    def add(self, name, f, mat, k=0): self.parts.append((name, f, mat, k)); return self
    def carve(self, name, f, mat, k=0): self.carves.append((name, f, mat, k)); return self
    def field(self, p, labels=False):
        d = None; best = None; idx = None
        for i, (n, f, m, k) in enumerate(self.parts):
            di = f(p).astype(f32)
            if labels: (best, idx) = (di, np.zeros(di.shape, np.int32)) if best is None else (np.minimum(best, di), np.where(di < best, i, idx))
            d = di if d is None else smin(d, di, k)
        for j, (n, f, m, k) in enumerate(self.carves):
            c = f(p).astype(f32); d = smax(d, -c, k) if k else np.maximum(d, -c)
            if labels: idx = np.where(np.abs(c) < max(self.vox * 1.6, .03), 1000 + j, idx)
        return (d, idx) if labels else d
    def mesh(self):
        n = np.ceil((self.hi - self.lo) / self.vox).astype(int) + 1; xs = [self.lo[i] + np.arange(n[i], dtype=f32) * self.vox for i in range(3)]
        D = np.empty(n, f32); Y, Z = np.meshgrid(xs[1], xs[2], indexing='ij')
        for i, x in enumerate(xs[0]):
            p = np.stack([np.full(Y.shape, x, f32), Y, Z], -1); D[i] = self.field(p)
        Pv, F, Nv, _ = marching_cubes(D, 0, spacing=(self.vox,) * 3, allow_degenerate=False)
        Pv = (Pv + self.lo).astype(f32); F = F[:, ::-1].copy()
        # normals from the field's gradient, materials from the nearest part, ambient occlusion along the normal
        e = self.vox * .5; g = np.stack([self.field(Pv + V(*o)) - self.field(Pv - V(*o)) for o in ((e, 0, 0), (0, e, 0), (0, 0, e))], -1); Nv = g / np.maximum(L(g)[:, None], 1e-6)
        _, idx = self.field(Pv, True); ao = np.ones(len(Pv), f32)
        for s in range(1, 6):
            h = .05 * s * s; ao -= np.clip((h - self.field(Pv + Nv * h)) / h, 0, 1) * (.42 / s)
        return Pv, Nv.astype(f32), F.astype(np.uint32), idx, np.clip(ao, .25, 1)
    def bake(self, path, paint=None):
        P, N, F, idx, ao = self.mesh(); mats = [m for (_, _, m, _) in self.parts]; cm = [m for (_, _, m, _) in self.carves]
        A = np.zeros((len(P), 4), f32); E = np.zeros((len(P), 4), f32)
        for i in np.unique(idx):
            sel = idx == i; m = cm[i - 1000] if i >= 1000 else mats[i]
            A[sel, :3] = m['c']; A[sel, 3] = m.get('r', .5); E[sel, :3] = m.get('e', (0, 0, 0)); E[sel, 3] = m.get('m', .7)
        if paint: paint(P, N, A, E, idx)
        A[:, :3] *= ao[:, None] ** 1.2; E[:, :3] *= np.clip(ao[:, None] * 1.3, 0, 1)
        import os; os.makedirs(path, exist_ok=True)
        for k, a in (('P', P), ('N', N), ('A', A), ('E', E)): np.ascontiguousarray(a, f32).tofile(f'{path}/{k}.bin')
        np.ascontiguousarray(F, np.uint32).tofile(f'{path}/F.bin'); print(path, len(P), 'verts', len(F), 'tris')
def hashf(i, j, k):
    h = (i * 73856093) ^ (j * 19349663) ^ (k * 83492791); h = (h ^ (h >> 13)) * 1274126177; return ((h ^ (h >> 16)) & 0xffff) / 65535.0
def panels(P, sx, sy, sz):
    # one value per armour panel, so plates read as separate pieces
    i = np.floor(P[:, 0] / sx).astype(np.int64); j = np.floor(P[:, 1] / sy).astype(np.int64); k = np.floor(np.abs(P[:, 2]) / sz).astype(np.int64)
    return hashf(i, j, k)
def ring(p, c, axis, R, w, h, r=.02):
    # a ring with a rounded-box cross-section: w half-width along the axis, h half-thickness radially
    q = p - V(*c); i = 'xyz'.index(axis); a = q[..., i]; o = np.delete(q, i, axis=-1)
    d = np.stack([np.abs(L(o) - R) - (h - r), np.abs(a) - (w - r)], -1); return np.minimum(np.max(d, -1), 0) + L(np.maximum(d, 0)) - r
