# v356: building models without the wait and the swap.
#  - Phones download phone-sized files (docs/models/m/: buildings 1536 px colour, ships 1024, 512 px detail maps), made ahead of time,
#    instead of 2048 px files shrunk on the phone. Desktop keeps the full files.
#  - Every file carries its own content fingerprint (GLB_V, from tools/glb_versions.json) instead of the game version, and the service
#    worker keeps models cache-first in their own cache ("udf-models") that survives updates: a model downloads once, ever, per change.
#  - Preload: the models of every building you own (all your worlds) and your fleet's hulls start loading as soon as the game is
#    ready, buildings first, before you open the base.
#  - No swap: while a building's model is still on its way, its plot shows the hand-built building as a hologram that resolves into
#    the model (the same look as the upgrade preview). If the model takes over 10 s (or fails), the plain building shows instead.
import json
V = json.load(open("tools/glb_versions.json"))
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep('new TH.GLTFLoader().load("models/" + k + ".glb?v=" + GAME_V, g => {',
    'GLB[k].t0 = performance.now(); setTimeout(() => { if (GLB[k] && !GLB[k].scene) { GLB[k].slow = true; if (C3 && C3.keys) C3.keys[k] = null; } }, 10000); // v356 too slow: show the plain building\n    new TH.GLTFLoader().load("models/" + (MOBILE ? "m/" : "") + k + ".glb?h=" + (GLB_V[k] || GAME_V), g => {')
rep("}, undefined, () => { GLB[k].fail = true; done(); });", "}, undefined, () => { GLB[k].fail = true; done(); if (C3 && C3.keys) C3.keys[k] = null; });")
rep("const GLB_Q = []; let GLB_RUN = 0;", "const GLB_Q = []; let GLB_RUN = 0;\nconst GLB_V = " + json.dumps(V, separators=(",", ":")) + "; // v356 each model file's fingerprint (tools/glb_versions.json)\n" + r'''/* v356 start loading your buildings' and hulls' models as soon as the game is ready, before the base is opened */
function glbPreload() {
  if (glbPreload.done || !G.ready || typeof S === "undefined" || !S || !S.b) return; glbPreload.done = true; if (!glbOn() || WEAK) return;
  const want = new Set(); for (const k in S.b) if (S.b[k] > 0 && GLB_BLDS.has(k)) want.add(k);
  try { for (const p of myPlanets()) for (const k in (p.b || {})) if (p.b[k] > 0 && GLB_BLDS.has(k)) want.add(k); } catch (e) {}
  for (const k of want) glbGet(k);
  for (const k in (S.ships || {})) if (S.ships[k] > 0 && GLB_SHIPS.has(k)) glbGet(k);
}
setInterval(() => { if (!glbPreload.done) try { glbPreload(); } catch (e) {} }, 1000);''')
# a building whose model is still coming: hologram
rep("  if (!GLB_BLDS.has(k) || WEAK) return false; /* slower Android phones keep the light hand-built buildings */ const src = glbGet(k);",
    "  if (!GLB_BLDS.has(k) || WEAK) return false; /* slower Android phones keep the light hand-built buildings */ const src = glbGet(k);\n  if (!src) { const e = GLB[k]; return e && !e.fail && !e.slow ? \"wait\" : false; } // v356 on its way: bModel shows a hologram")
rep("  if (!glbBld(k, b, big, small, anim) && !artBld(k, b, era, C, anim)) switch (k) {",
    "  const gw = glbBld(k, b, big, small, anim); // v356 true: the model; \"wait\": it is loading (shown as a hologram)\n  if (gw !== true && !artBld(k, b, era, C, anim)) switch (k) {")
# after the switch: turn the hand-built stand-in into a hologram while the model loads
rep("  if (!ART_B[k]) eraSpecific(k, b, era, C, anim); eraKit(g, k, L, era, C, anim, big ? 3.3 : small ? 1.9 : 2.5, !!ART_B[k]);",
    "  if (gw === \"wait\") { const HM = HOLO_WIRE(); b.traverse(o => { if (o.isMesh) { o.material = HM; o.castShadow = false; } }); }\n  if (!ART_B[k]) eraSpecific(k, b, era, C, anim); eraKit(g, k, L, era, C, anim, big ? 3.3 : small ? 1.9 : 2.5, !!ART_B[k]);")
open(p, "w").write(h)
s = open("docs/sw.js").read()
a = 'self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });'
assert s.count(a) == 1; s = s.replace(a, 'self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE && k !== MODELS).map(k => caches.delete(k)))).then(() => self.clients.claim())); });')
a = 'const CACHE = "'; i = s.index(a); j = s.index('\n', i); s = s[:j + 1] + 'const MODELS = "udf-models"; // v356 3D models: fingerprinted file names, kept across updates\n' + s[j + 1:]
a = '  if (same && !u.pathname.startsWith("/__/")) {'
assert s.count(a) == 1; s = s.replace(a, '''  if (same && /\\/models\\/.+\\.glb$/.test(u.pathname)) { // v356 cache-first: a model file only changes with its fingerprint
    e.respondWith(caches.open(MODELS).then(c => c.match(r).then(m => m || fetch(r).then(res => { if (res.ok) { c.put(r, res.clone()); c.keys().then(ks => { const name = u.pathname.split("/").pop(), sub = u.pathname.includes("/m/"); ks.filter(q => { const qu = new URL(q.url); return qu.pathname.split("/").pop() === name && qu.pathname.includes("/m/") === sub && qu.search !== u.search; }).forEach(q => c.delete(q)); }); } return res; })))); return; }
  if (same && !u.pathname.startsWith("/__/")) {''')
open("docs/sw.js", "w").write(s); print("ok")
