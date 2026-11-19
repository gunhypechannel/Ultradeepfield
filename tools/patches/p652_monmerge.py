# v652 (owner: "Void shark looks strange like it's phasing in and out and void manta loses his tail tip when his tail moves").
# The v651 battle frames ran the body motion on the monster's separate parts, each measured from its own centre, so the parts moved
# out of step with the body (the shark's fins and turrets sank in and out of it; the manta's stinger stayed put while the tail swept
# away). The map merges the model into one piece first, so every vertex is measured from the body; the battle frames now do the same.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
rep('kind === "a" ? buildAlien(k) : kind === "m"', 'kind === "a" ? (mfr >= 0 && MON_WAVE[k] ? monMerged(k) : buildAlien(k)) : kind === "m"')
rep('function monBatPose(root, kind, f) {', '''const MMERGE = {};
function monMerged(k) { let M = MMERGE[k]; if (!M) { const s0 = buildAlien(k); M = MMERGE[k] = mergeGroup(s0); M.userData = s0.userData; M.position.copy(s0.position); M.quaternion.copy(s0.quaternion); M.scale.copy(s0.scale);
    s0.traverse(o => { if (o.geometry) o.geometry.dispose(); }); }
  const c = M.clone(); c.userData = Object.assign({}, M.userData, { keepGeo: 1 }); return c; } /* v652 one piece, as on the map, so the body motion moves every part with the body; merged once per species */
function monBatPose(root, kind, f) {''')
rep('if (o.geometry && !ship.userData.glb) o.geometry.dispose();', 'if (o.geometry && !ship.userData.glb && !ship.userData.keepGeo) o.geometry.dispose();')
rep('const st = add(new TH.Mesh(new TH.ConeGeometry(.08, .5, 10), C.glowM), -6.85, .36, 0);', 'const st = add(new TH.Mesh(new TH.ConeGeometry(.08, .5, 10), C.glowM), -6.85, .02, 0); /* v652 on the tail\'s tip, not floating above it */')
rep('const GAME_V = 651', 'const GAME_V = 652')
open(p, 'w', encoding='utf-8').write(s)
