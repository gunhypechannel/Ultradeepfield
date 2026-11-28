# Shared look for the Continuum's sculpted hulls: the paintings' gunmetal and black-chrome plates, crimson light, blue vents.
import numpy as np
from sdf import *
HULL = {'c': (.06, .058, .06), 'r': .34, 'm': .85}; PLATE = {'c': (.095, .09, .09), 'r': .28, 'm': .9}; BLACK = {'c': (.03, .028, .03), 'r': .34, 'm': .85}
GUN = {'c': (.17, .165, .165), 'r': .22, 'm': 1}; DARK = {'c': (.012, .011, .012), 'r': .5, 'm': .5}
RED = {'c': (.2, .005, .008), 'r': .4, 'm': .1, 'e': (.72, .008, .012)}; GLASS = {'c': (.1, .004, .008), 'r': .12, 'm': .1, 'e': (.6, .01, .018)}
LITE = {'c': (.03, .05, .07), 'r': .4, 'm': .2, 'e': (.12, .45, .95)}; ROCK = {'c': (.034, .03, .028), 'r': .9, 'm': .1}
ORGAN = {'c': (.045, .045, .052), 'r': .38, 'm': .6}
def eye(M, n, c, axis, R, glow=RED):
    # the radial red eye: an armoured rim, eight vanes and a glowing core, facing along axis ('x', 'y' or 'z', sign in R's sign)
    s = 1 if R > 0 else -1; R = abs(R); i = 'xyz'.index(axis); cc = list(c)
    M.add(n + 'R', lambda p: ring(p, c, axis, R, R * .14, R * .17), GUN)
    co = list(c); co[i] += s * R * .12; M.add(n + 'C', lambda p: sphere(p, co, R * .48), glow); M.add(n + 'D', lambda p: cyl(p, c, axis, R * .86, R * .1), BLACK)
    u, v = [a for a in range(3) if a != i]
    for a in np.linspace(0, 2 * np.pi, 9)[:-1]:
        q = list(c); q[u] += np.cos(a) * R * .72; q[v] += np.sin(a) * R * .72; q[i] += s * R * .03
        h = [R * .04] * 3; h[u] = abs(np.cos(a)) * R * .14 + R * .035; h[v] = abs(np.sin(a)) * R * .14 + R * .035; h[i] = R * .07
        M.add(f'{n}V{a:.2f}', lambda p, q=q, h=h: box(p, q, h, .01), GUN)
def engine(M, n, x, y, z, r, L=.5):
    M.add(n, lambda p: cyl(p, (x - L / 2, y, z), 'x', r, L / 2, r * .15), GUN)
    M.add(n + 'b', lambda p: ring(p, (x - L * .2, y, z), 'x', r * 1.02, r * .14, r * .12), BLACK)
    M.carve(n + 't', lambda p: cyl(p, (x - L, y, z), 'x', r * .62, r * .25), RED)
def paint(P, N, A, E, idx, sx=.5, sy=.4, sz=.4):
    v = panels(P, sx, sy, sz); hullish = (A[:, 0] < .16) & (E[:, 0] < .01)
    A[hullish, :3] *= (.65 + .7 * v[hullish])[:, None]
    top = np.clip(N[:, 1], 0, 1); A[:, :3] *= (1 + .3 * top)[:, None]
def slit_rows(shell, bands, x0, x1, pitch=.26, h=.026, w=.08):
    # dashed crimson window rows cut into a shell at the given heights, between x0 and x1
    def f(p):
        q = p.copy(); q[..., 0] = np.mod(q[..., 0] + 40, pitch) - pitch / 2; q[..., 1] = 0; wv = box(q, (0, 0, 0), (w, 1, 9))
        band = np.min(np.stack([np.abs(p[..., 1] - b) for b in bands]), 0)
        return np.maximum(np.maximum(wv, band - h), np.maximum(np.abs(shell(p)) - .05, np.maximum(x0 - p[..., 0], p[..., 0] - x1)))
    return f
def seams(shell, pitch=.5):
    def f(p):
        q = p.copy(); q[..., 0] = np.mod(q[..., 0] + 40, pitch) - pitch / 2; return np.maximum(box(q, (0, 0, 0), (.012, 9, 9)), np.abs(shell(p)) - .05)
    return f
def ring_windows(c, R, h, y, pitch=.3, w=.07, hh=.03):
    # a dashed row of crimson windows round the outer face of a ring about y (radius R, radial half-thickness h)
    def f(p):
        q = p - np.array(c, np.float32); rr = np.hypot(q[..., 0], q[..., 2]); s = np.arctan2(q[..., 2], q[..., 0]) * (R + h)
        dash = np.abs(np.mod(s + 40, pitch) - pitch / 2) - w
        return np.maximum(np.maximum(dash, np.abs(q[..., 1] - y) - hh), np.abs(rr - (R + h)) - .05)
    return f
# v856 every Continuum hull gets a glow layer: each crimson part (and every crimson cut) grown a little and baked to <path>_g, which the
# game draws additively over the hull, so the red light blooms like the paintings'
_cnt_bake = Model.bake
def _cnt_bake_g(self, path, paint=None):
    _cnt_bake(self, path, paint)
    if getattr(self, 'noghost', False) or path.endswith('_g'): return
    G = Model(self.lo, self.hi, max(self.vox * 2, .05)); GG = {'c': (0, 0, 0), 'r': .2, 'm': 0, 'e': (.34, .012, .016)}
    for (n, f, m, k) in self.parts + self.carves:
        e = m.get('e')
        if e and e[0] > .3 and e[1] < .15: G.add(n, lambda p, f=f: f(p) - .07, GG)
    if G.parts: _cnt_bake(G, path + '_g', None)
Model.bake = _cnt_bake_g
