# v586 The three Titans get real 3D models from the Meshy community, chosen by the owner as the closest to their paintings
# ("Are there any better matches for the ships? I want the closest"): Armageddon = "Obsidian Dragon Dreadnought", Sovereign =
# "Citadel Starship", Harbinger = "Voidbound Dreadnought" (all CC0). Harbinger was 1.2 M triangles: cut to 70 k (30 k on phones) by
# tools/glb_decimate.py; its orange lights recoloured to the Harbinger green (tools/glb_glow.py). The hand-built Titan stays
# underneath, invisible, so every firing animation, engine flame and viewer sequence keeps its anchor points; until the model has
# loaded (or on devices with models off) the hand-built Titan shows as before.
import sys, re, json
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
V = {"armageddon": "5935b307", "sovereign": "9d0e7099", "harbinger": "96444209"}
rep('const GLB_V = {', 'const GLB_V = {' + json.dumps(V)[1:-1] + ', ')
rep('  if (TITAN_INFO[k]) return titanModel(k, g); /* v556 */', '  if (TITAN_INFO[k]) { titanModel(k, g); try { titanSkin(k, g); } catch (e) {} return g; } /* v556, v586 the Meshy model over it */')
rep('function glbShip(k) {', '''/* v586 a Titan's Meshy model, fitted over the hand-built one (kept invisible for its anchor points). TITAN_ROT turns the file's
   prow to +X: Armageddon and Sovereign point -X in the file, Harbinger stands on end with its prow up (+Y). */
const TITAN_ROT = { armageddon: [0, Math.PI, 0], sovereign: [0, Math.PI, 0], harbinger: [0, 0, -Math.PI / 2] }, TITAN_GLOW = { armageddon: 2.6, sovereign: 1.4, harbinger: 3.2 };
let TITAN_HIDE = null;
function titanSkin(k, g) { if (!TITAN_ROT[k]) return; const src = glbGet(k); if (!src) return;
  const hb = new TH.Box3().setFromObject(g), L = Math.max(.1, hb.max.x - hb.min.x), hc = hb.getCenter(new TH.Vector3());
  TITAN_HIDE = TITAN_HIDE || new TH.MeshBasicMaterial({ visible: false }); g.traverse(o => { if (o.isMesh) o.material = TITAN_HIDE; });
  const m = src.clone(true), bb = src.userData.bb, c = bb.getCenter(new TH.Vector3()); m.position.set(-c.x, -c.y, -c.z);
  const pv = new TH.Group(); pv.add(m); const R = TITAN_ROT[k]; pv.rotation.set(R[0], R[1], R[2]); pv.updateMatrixWorld(true);
  const b2 = new TH.Box3().setFromObject(pv), len = Math.max(.01, b2.max.x - b2.min.x), sc = L * 1.04 / len; pv.scale.setScalar(sc); pv.position.copy(hc);
  pv.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; o.userData.nobake = true; } }); g.add(pv); g.userData.glb = true; g.userData.skin = pv; }
function glbShip(k) {''')
# load and refresh like the ships: their portraits rebuild once the model is in, and owned Titans load early
rep('Promise.all(ps).then(() => GLB_BLDS.has(k) ? glbLights(k, s) : GLB_SHIPS.has(k) ? glbHull(k, s) : null)',
    'Promise.all(ps).then(() => GLB_BLDS.has(k) ? glbLights(k, s) : GLB_SHIPS.has(k) ? glbHull(k, s) : TITAN_GLOW[k] ? s.traverse(o => { if (o.isMesh && o.material && o.material.emissiveMap) { o.material.emissive.set(0xffffff); o.material.emissiveIntensity = TITAN_GLOW[k]; o.material.needsUpdate = true; } }) : null)')
rep('  if (GLB_SHIPS.has(k)) { const S = STU || null; if (S && S.cache)', '  if (GLB_SHIPS.has(k) || TITAN_ROT[k]) { const S = STU || null; if (S && S.cache)')
rep('  for (const k in (S.ships || {})) if (S.ships[k] > 0 && GLB_SHIPS.has(k)) glbGet(k);\n}', '  for (const k in (S.ships || {})) if (S.ships[k] > 0 && (GLB_SHIPS.has(k) || TITAN_ROT[k])) glbGet(k);\n}')
s2 = re.sub(r"GAME_V = 584\b", "GAME_V = 586", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
