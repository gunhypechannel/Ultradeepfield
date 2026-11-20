# v675 the v674 minimum-size boost read the map's size (W.size), which adaptRes zeroes to force a resize: pxC was 0 and the fleet's
# scale went to infinity for a frame (owner's iPhone: a huge smeared red flagship in a white blow-out). It also misjudged the size in
# normal frames. Now it measures from the canvas itself, ignores a zero reading and boosts at most 4x.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
rep('pxC = (o.grp.userData.span || 20) * ws0 * (pxS / W.renderer.getPixelRatio()) / Math.max(1, W.camera.position.distanceTo(o.grp.position)), ws = ws0 * (wk > .9 && pxC < 30 ? 30 / pxC : 1) /* v674 never under 30 px */;',
    'pxC = (o.grp.userData.span || 20) * ws0 * ((W.renderer.domElement.clientHeight || innerHeight || 800) / 2 / Math.tan(W.camera.fov * Math.PI / 360)) / Math.max(1, W.camera.position.distanceTo(o.grp.position)), ws = ws0 * (wk > .9 && pxC > .5 && pxC < 30 ? Math.min(4, 30 / pxC) : 1) /* v674 never under 30 px; v675 measured from the canvas, never from a zeroed W.size, at most 4x */;')
# owner: remove the fleets in flight from the Finder (they stay in the Fleets tab)
rep('return `${banner}${fl ? `<h2 class="sec">Fleets in flight</h2><div class="queue">${fl}</div>` : ""}', 'return `${banner}${fl && sub.gal !== "targets" ? `<h2 class="sec">Fleets in flight</h2><div class="queue">${fl}</div>` : ""}')
rep('const GAME_V = 674;', 'const GAME_V = 675;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
