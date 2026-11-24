# The Resurrection War's item and reward art, sculpted in the Continuum's materials: python3 cnt_icons.py <outdir> [only]
# Each model is baked to <outdir>/<key>/ and packed by build_icons.sh, then rendered with transparency by the icon page.
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from cnt_lib import *
OUT = sys.argv[1]; ONLY = sys.argv[2] if len(sys.argv) > 2 else None
CYAN = {'c': (.02, .08, .1), 'r': .2, 'm': .1, 'e': (.04, .45, .9)}; GOLD = {'c': (.62, .45, .18), 'r': .22, 'm': 1}; CHROME = {'c': (.5, .5, .52), 'r': .14, 'm': 1}
def hexo(r, n=6, a0=0): return [(r * np.cos(a0 + i * 2 * np.pi / n), r * np.sin(a0 + i * 2 * np.pi / n)) for i in range(n)]
def model(k, lo, hi, vox, build):
    if ONLY and k != ONLY: return
    M = Model(lo, hi, vox); build(M); M.bake(f'{OUT}/{k}', lambda P, N, A, E, idx: None)
# Neural Echoes: a cluster of red crystal shards on a dark socket
def echo(M):
    for i, (x, z, h, r, tilt) in enumerate([(0, 0, 1.5, .32, 0), (.42, .15, 1.0, .24, -.35), (-.38, .2, .9, .22, .4), (.05, -.42, .8, .2, .3)]):
        R = rot('z', tilt) @ rot('x', tilt * .6)
        M.add(f's{i}', lambda p, x=x, z=z, h=h, r=r, R=R: smin(prism(p, hexo(r), h * .6, 0, .03, .01, c=(x, -.2, z), R=R), rcone(((p - V(x, -.2, z)) @ R) + V(x, -.2, z), (x, -.2 + h * .6, z), (x, -.2 + h, z), r * .95, .02), .02), GLASS)
    M.add('base', lambda p: cyl(p, (0, -.28, 0), 'y', .72, .1, .05), BLACK, .05); M.add('rim', lambda p: ring(p, (0, -.22, 0), 'y', .72, .03, .05), GUN)
# Machine Alloy: three stacked ingots with a crimson seam
def alloy(M):
    for i, (y, x, z, a) in enumerate([(0, -.32, 0, .1), (0, .36, .05, -.05), (.34, 0, 0, .5)]):
        M.add(f'i{i}', lambda p, y=y, x=x, z=z, a=a: prism(p, [(-.55, -.24), (.55, -.24), (.45, .24), (-.45, .24)], .16, -.16, .07, .02, c=(x, y, z), R=rot('y', a)), GUN)
        M.carve(f'g{i}', lambda p, y=y, x=x, z=z, a=a: box(p, (x, y + .17, z), (.36, .02, .02), 0, rot('y', a)), RED)
# Continuum Circuitry: a machine chip with pins, traces and a red core
def circ(M):
    M.add('chip', lambda p: box(p, (0, 0, 0), (.62, .09, .62), .04), BLACK)
    M.add('lid', lambda p: box(p, (0, .1, 0), (.42, .04, .42), .03), PLATE, .02)
    for s in (1, -1):
        for j in np.linspace(-.48, .48, 7):
            M.add(f'px{s}{j:.2f}', lambda p, s=s, j=j: box(p, (j, -.02, .7 * s), (.03, .025, .1), .01), CHROME)
            M.add(f'pz{s}{j:.2f}', lambda p, s=s, j=j: box(p, (.7 * s, -.02, j), (.1, .025, .03), .01), CHROME)
    M.add('core', lambda p: sphere(p, (0, .15, 0), .16), RED)
    for a in np.linspace(0, np.pi, 4, endpoint=False):
        M.carve(f't{a:.2f}', lambda p, a=a: box(p, (0, .14, 0), (.4, .012, .012), 0, rot('y', a)), RED)
# Crimson Reactor Cell: a canister with a glowing window and heavy caps
def cell(M):
    M.add('glass', lambda p: cyl(p, (0, 0, 0), 'y', .3, .5, .05), GLASS)
    for y in (.55, -.55): M.add(f'cap{y}', lambda p, y=y: cyl(p, (0, y, 0), 'y', .4, .12, .05), GUN, .03)
    for a in np.linspace(0, 2 * np.pi, 5)[:-1]: M.add(f'bar{a:.2f}', lambda p, a=a: cap(p, (np.cos(a) * .34, -.5, np.sin(a) * .34), (np.cos(a) * .34, .5, np.sin(a) * .34), .045), BLACK)
    M.add('pin', lambda p: cyl(p, (0, .74, 0), 'y', .12, .08, .03), CHROME)
# Resurrection Core: a red core in a cage of three rings
def core(M):
    M.add('core', lambda p: sphere(p, (0, 0, 0), .42), RED)
    for i, R in enumerate([rot('x', 0), rot('x', np.pi / 2), rot('z', np.pi / 2) @ rot('x', .6)]):
        M.add(f'r{i}', lambda p, R=R: torus(p @ R, (0, 0, 0), 'y', .62, .05), CHROME)
    for s in (1, -1): M.add(f'n{s}', lambda p, s=s: spike(p, (0, .55 * s, 0), (0, .9 * s, 0), .08), GUN)
# Quantum Neural Matrix: a lattice cube with a cyan core
def matrix(M):
    e = .55
    for a in (-e, e):
        for b in (-e, e):
            M.add(f'x{a}{b}', lambda p, a=a, b=b: cap(p, (-e, a, b), (e, a, b), .045), CHROME); M.add(f'y{a}{b}', lambda p, a=a, b=b: cap(p, (a, -e, b), (a, e, b), .045), CHROME); M.add(f'z{a}{b}', lambda p, a=a, b=b: cap(p, (a, b, -e), (a, b, e), .045), CHROME)
    M.add('in', lambda p: box(p, (0, 0, 0), (.3, .3, .3), .05, rot('y', .7) @ rot('x', .6)), CYAN)
    for a in (-e, e):
        for b in (-e, e):
            for c in (-e, e): M.add(f'k{a}{b}{c}', lambda p, a=a, b=b, c=c: sphere(p, (a, b, c), .09), RED)
# Elite Flagship Materials: a gold-trimmed hexagonal case with a cyan seal
def elite(M):
    M.add('case', lambda p: prism(p, hexo(.62, 6, np.pi / 6), .3, -.3, .08, .02), BLACK)
    M.add('trim', lambda p: np.maximum(prism(p, hexo(.66, 6, np.pi / 6), .32, -.32, .08, .02), -prism(p, hexo(.58, 6, np.pi / 6), .5, -.5, 0, 0)), GOLD)
    M.add('seal', lambda p: cyl(p, (0, .33, 0), 'y', .2, .04, .02), CYAN); M.add('ring', lambda p: ring(p, (0, .33, 0), 'y', .26, .04, .04), GOLD)
# The Arkbreaker Badge: a chrome shield with a broken red ring
def badge(M):
    sh = lambda p: prism(p, [(0, -.85), (.6, -.35), (.6, .55), (-.6, .55), (-.6, -.35)], .08, -.08, .05, .02, R=XYZ_XZY)
    M.add('shield', sh, BLACK); M.add('rim', lambda p: np.maximum(prism(p, [(0, -.93), (.68, -.38), (.68, .62), (-.68, .62), (-.68, -.38)], .1, -.1, .05, .02, R=XYZ_XZY), -prism(p, [(0, -.84), (.59, -.34), (.59, .54), (-.59, .54), (-.59, -.34)], .5, -.5, 0, 0, R=XYZ_XZY)), CHROME)
    M.add('ring', lambda p: np.maximum(torus(p, (0, .02, .1), 'z', .3, .055), -box(p, (.12, .14, .1), (.05, .2, .2), 0, rot('z', -.5))), RED)
    M.add('bolt', lambda p: box(p, (.1, .05, .13), (.025, .3, .03), 0, rot('z', -.5)), CHROME)
# The Prime Ark Trophy: the citadel in miniature on a gold plinth
def trophy(M):
    M.add('plinth', lambda p: cyl(p, (0, -.75, 0), 'y', .55, .12, .04), BLACK); M.add('plinth2', lambda p: cyl(p, (0, -.58, 0), 'y', .42, .06, .03), GOLD)
    M.add('stem', lambda p: rcone(p, (0, -.5, 0), (0, .1, 0), .12, .2), GOLD)
    M.add('cit', lambda p: rcone(p, (0, .05, 0), (0, .45, 0), .26, .2), BLACK); M.add('crown', lambda p: spike(p, (0, .4, 0), (0, 1.0, 0), .12), GUN)
    M.add('rU', lambda p: ring(p, (0, .55, 0), 'y', .42, .03, .04), GOLD); M.add('rL', lambda p: ring(p, (0, .12, 0), 'y', .5, .04, .05), GOLD)
    for a in np.linspace(0, 2 * np.pi, 7)[:-1]: M.add(f'ch{a:.2f}', lambda p, a=a: cap(p, (np.cos(a) * .25, .1, np.sin(a) * .25), (np.cos(a) * .22, .38, np.sin(a) * .22), .06), GLASS)
    M.add('core', lambda p: spike(p, (0, -.1, 0), (0, -.45, 0), .06), RED)
# The Neural Crown frame: a chrome ring, red neural nodes, a crown of spikes on top (seen face-on)
def crown(M):
    M.add('ring', lambda p: ring(p, (0, 0, 0), 'z', 1.0, .06, .07, .02), CHROME)
    M.add('ring2', lambda p: ring(p, (0, 0, -.02), 'z', 1.09, .05, .03, .01), BLACK)
    for a in np.linspace(0, 2 * np.pi, 13)[:-1]: M.add(f'n{a:.2f}', lambda p, a=a: sphere(p, (np.cos(a) * 1.0, np.sin(a) * 1.0, .07), .045), RED)
    for i, a in enumerate(np.linspace(np.pi * .18, np.pi * .82, 7)):
        L = .95 if i == 3 else .62 if i in (2, 4) else .38
        M.add(f'sp{i}', lambda p, a=a, L=L: spike(p, (np.cos(a) * 1.02, np.sin(a) * 1.02, 0), (np.cos(a) * (1.02 + L), np.sin(a) * (1.02 + L), 0), .07), GUN)
    M.add('gem', lambda p: sphere(p, (0, 1.12, .06), .11), RED)
    for s in (1, -1): M.add(f'claw{s}', lambda p, s=s: spike(p, (.75 * s, -.66, 0), (.55 * s, -1.05, 0), .06), GUN)
# The Continuum Commander: a machine head with one red eye
def bust(M):
    head = lambda p: smin(ell(p, (0, .55, 0), (.5, .62, .55)), box(p, (0, .25, .1), (.36, .25, .4), .12), .15)
    M.add('head', head, BLACK)
    M.add('face', lambda p: ell(p, (0, .5, .22), (.38, .45, .36)), PLATE, .04)
    M.add('brow', lambda p: box(p, (0, .72, .48), (.36, .05, .06), .03), GUN, .03)
    M.add('eyeR', lambda p: ring(p, (0, .55, .53), 'z', .13, .04, .04), GUN); M.add('eye', lambda p: sphere(p, (0, .55, .53), .1), RED)
    for s in (1, -1):
        M.add(f'ear{s}', lambda p, s=s: cyl(p, (.5 * s, .55, 0), 'x', .17, .06, .03), GUN)
        M.add(f'fin{s}', lambda p, s=s: spike(p, (.32 * s, 1.05, -.05), (.55 * s, 1.5, -.3), .07), GUN)
        for j in range(3): M.add(f'c{s}{j}', lambda p, s=s, j=j: cap(p, (.14 * s + .06 * j * s, .05, -.05 - .08 * j), (.2 * s + .1 * j * s, -.45, -.1 - .05 * j), .045), BLACK)
        M.add(f'sh{s}', lambda p, s=s: ell(p, (.62 * s, -.62, -.05), (.48, .26, .4)), PLATE, .08)
        M.add(f'shr{s}', lambda p, s=s: spike(p, (.75 * s, -.45, -.1), (1.0 * s, -.1, -.2), .07), GUN)
    M.add('neck', lambda p: cyl(p, (0, -.1, -.05), 'y', .2, .25, .05), GUN)
    M.add('chest', lambda p: box(p, (0, -.75, 0), (.6, .22, .36), .1), BLACK, .1)
    M.add('chestC', lambda p: sphere(p, (0, -.68, .34), .07), RED)
    M.carve('mouth', lambda p: box(p, (0, .28, .58), (.18, .012, .06)), RED)
    for y in (.42, .36): M.carve(f'grill{y}', lambda p, y=y: box(p, (0, y - .1, .56), (.12, .008, .06)), DARK)
model('echo', (-.9, -.5, -.9), (.9, 1.4, .9), .012, echo); model('alloy', (-1, -.4, -.8), (1, .8, .8), .012, alloy)
model('circ', (-.95, -.2, -.95), (.95, .4, .95), .011, circ); model('cell', (-.55, -.8, -.55), (.55, .95, .55), .011, cell)
model('core', (-.8, -1.05, -.8), (.8, 1.05, .8), .012, core); model('matrix', (-.75, -.75, -.75), (.75, .75, .75), .011, matrix)
model('elite', (-.8, -.45, -.8), (.8, .5, .8), .011, elite); model('badge', (-.8, -1.0, -.3), (.8, .75, .3), .011, badge)
model('trophy', (-.7, -.95, -.7), (.7, 1.1, .7), .011, trophy); model('crown', (-1.4, -1.3, -.25), (1.4, 2.15, .3), .013, crown)
model('bust', (-1.2, -1.05, -.6), (1.2, 1.65, .75), .012, bust)
