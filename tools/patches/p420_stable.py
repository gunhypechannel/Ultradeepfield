# v420: wreckage no longer flickers in and out. (1) Culling: wreck hulls come from the fleet kit, partly instanced, and are cut, cloned
# and offset, so their bounding spheres no longer matched what was drawn and three.js culled pieces as the camera turned; wreck sets
# and the Cube wreck field's derelicts now skip frustum culling. (2) Picking: which sites get wreck sets was re-chosen every second by
# distance alone, so two sites at similar range (one set on phones) or one at the edge of range swapped back and forth; a shown site now
# keeps its set until it is 30% beyond range, and wins ties by 250 units. (3) At most one new set is built per second, so building
# never lands as a burst in one frame.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("""  if (t - X.at > 1000) { X.at = t; const L = wbScars(T).filter(s => (!s.a || s.k === "dev") && Math.hypot(s.x - cam.x, s.y - cam.y, s.z - cam.z) < (MOBILE ? 450 : 700)); L.sort((a, b) => (b.b || 0) - (a.b || 0) || (a.a || 0) - (b.a || 0) || Math.hypot(a.x - cam.x, a.z - cam.z) - Math.hypot(b.x - cam.x, b.z - cam.z));""",
    """  if (t - X.at > 1000) { X.at = t; X.built = 0; const lim = MOBILE ? 450 : 700, held = new Set(X.sets.filter(S => S.site).map(S => S.site)), dist = s => Math.hypot(s.x - cam.x, s.y - cam.y, s.z - cam.z), key = s => (s.b ? 0 : s.a ? 2 : 1) * 1000 + dist(s) - (held.has(s.k + s.at) ? 250 : 0); /* v420 a shown site keeps its set */
    const L = wbScars(T).filter(s => (!s.a || s.k === "dev") && dist(s) < (held.has(s.k + s.at) ? lim * 1.3 : lim)); L.sort((a, b) => key(a) - key(b));""")
rep("""    if (!S && X.sets.length < (MOBILE ? 3 : 6)) { S = wbWreckSet(W, !!s.b, 1 + hash(s.k + ":" + s.at) % 99991, ty, pu); X.sets.push(S); }""",
    """    if (!S && X.sets.length < (MOBILE ? 3 : 6) && !X.built) { X.built = 1; S = wbWreckSet(W, !!s.b, 1 + hash(s.k + ":" + s.at) % 99991, ty, pu); X.sets.push(S); } /* v420 one new set per second */""")
rep("""  return S; }
function wbWrecks(W, t, T) {""", """  grp.traverse(o => { if (o.isMesh) o.frustumCulled = false; }); /* v420 cut, cloned and instanced hulls: their bounds no longer match */
  return S; }
function wbWrecks(W, t, T) {""")
rep("""d.brk = wreckBreak(W, d.g, r, null, false, grp, DK); /* v419 */ }""", """d.brk = wreckBreak(W, d.g, r, null, false, grp, DK); d.g.traverse(o => { if (o.isMesh) o.frustumCulled = false; }); /* v419, v420 */ }""")
t = t.replace("const GAME_V = 419;", "const GAME_V = 420;")
open(p, "w").write(t); print("ok")
