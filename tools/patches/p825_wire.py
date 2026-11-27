"""v825 (part 1): the fleet that circled an attack target is gone (owner: "remove the fleet animation when an attack lands in map view a
wedge formation fleet circles the target, it uses outdated ship models and proportion scaling, i want it fixed or removed"). It was your own
fleet parked at its target (fleetPath park) orbiting it every 7.9 s, drawn with the travelling fleet model, on top of the battle's own
flagship-and-escort (v815). While a battle plays at that target the parked fleet is now hidden (the escort is the fleet); any other parked
fleet that is not mining or mustering orbits at the stately muster pace (.00011, was .0008: a turn in ~57 s)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 824;", "const GAME_V = 825;")
rep("    if (!path) continue; fseen.add(id);\n    // v174 during the Cube event",
    """    if (!path) continue; fseen.add(id);
    if (path.park && !path.cube && !hostile && f.phase !== "gather" && f.phase !== "muster" && G.clashes.some(c => c.loc === fleetTarget(f))) { const o0 = W.fleets.get(id); if (o0 && o0.grp.visible) { o0.grp.visible = false; o0.hidP = 1; } continue; } /* v825 the battle's escort is the fleet */
    // v174 during the Cube event""")
rep("    let pt, nx;\n    if (path.cube) {", "    if (o.hidP) { o.hidP = 0; o.grp.visible = true; }\n    let pt, nx;\n    if (path.cube) {")
rep("f.phase === \"muster\" ? .00009 : f.parkR ? .00011 : .0008) + (hash(id) % 10);", "f.phase === \"muster\" ? .00009 : .00011) + (hash(id) % 10); /* v825 a stately orbit (was .0008) */")
# v825 mobile building models simplified by tools/glb/cluster2.js (459k -> 211k triangles; main textures 1536 -> 1024, tools/glb/tex1024.py); their own cache fingerprints
rep('    new TH.GLTFLoader().load("models/" + (MOBILE ? "m/" : "") + k + ".glb?h=" + (GLB_V[k] || GAME_V), g => {',
    '    new TH.GLTFLoader().load("models/" + (MOBILE ? "m/" : "") + k + ".glb?h=" + (MOBILE && GLB_VM[k] || GLB_V[k] || GAME_V), g => {')
rep('; // v356 each model file\'s fingerprint (tools/glb_versions.json)', '; // v356 each model file\'s fingerprint (tools/glb_versions.json)\nconst GLB_VM = {"radar":"c3bdfefe","metalMine":"6c72614e","crystalMine":"b53df6c4","solar":"f4ad333e","gasSynth":"1c56bb66","metalStore":"721ccf2b","crystalStore":"40d3aef3","gasTank":"0d85a510","robotics":"61acfc50","shipyard":"d7614b96","lab":"f84fa884","fortress":"b5f29924","repairYard":"2765233b","fusion":"82b2937f","nanite":"cbe5cbde","terraformer":"bc6a890f","allyDepot":"c5d7ff15","phalanx":"aa74ec2f","lunarBase":"85755f65"}; // v825 the simplified mobile models')
# v825 the Eclipse Cage opens the Harbinger's fight (owner: "watched a battle report a few times and never seen harbingers new attacks").
# It came only on the 4th main-gun volley; the owner's fights end fast (a Void Shark hunt: 7.75 s, the Harbinger fired only its swarm).
# Now the cage is staged right before the Harbinger's first shot of any kind, then on every 4th main volley as before. Visual only.
rep("  battle.acc = battleAcc(r);\n", """  battle.acc = battleAcc(r);
  R.squads.forEach((q, i) => { if (q.k !== "harbinger") return; const v = (R.vols || []).find(v => v.s === i && v.e != null && v.e >= 0); if (v) battle.beams.push({ t0: Math.max(.6, v.t - 2.1), s: i, e: v.e, side: q.side, ti: "HC", charge: 0, life: 2.3, seed: hash("op|" + i) % 997, op: 1 }); }); /* v825 the Harbinger opens with the Eclipse Cage */
""")
# v825 the cage was sized by the Harbinger's own on-screen size: far from the camera it closed ~20 px wide under its target, unseen.
# It now spans the target (at least ~110 px); the reactor glow and the pylons' launch points keep the Harbinger's own size.
rep("""  HC(ctx, b, m, age, S0, E0, fc, Lg, d, lo, T, scr) { if (!E0) return; const aw""", """  HC(ctx, b, m, age, S0, E0, fc, Lg, d, lo, T, scr) { if (!E0) return; const LgS = Lg, qe = b.Q[m.e]; Lg = Math.min(Math.max(LgS, 420 * d), Math.max(Lg, qe ? Lg * bLen(qe.k) * (E0.s || 1) / Math.max(.2, bLen("harbinger") * (S0.s || 1)) * 1.25 : 0, 120 * d)); /* v825 the cage spans its target */ const aw""")
rep("""/* the reactor gathers, beating */ tx5.glow(ctx, S0.x, S0.y, Lg * .3""", """/* the reactor gathers, beating */ tx5.glow(ctx, S0.x, S0.y, LgS * .3""")
rep("""a0 = (i / 4) * TAU + .4, sx = S0.x + Math.cos(a0) * Lg * .34, sy = S0.y + Math.sin(a0) * Lg * .2;""", """a0 = (i / 4) * TAU + .4, sx = S0.x + Math.cos(a0) * LgS * .34, sy = S0.y + Math.sin(a0) * LgS * .2;""")
# v825 the base's per-frame work on phones: buildings off screen skip their machinery animation (it is all clock-driven, so they pick
# up exactly where they should when scrolled back in view); colonists step at 30 Hz on mobile; half the pebbles there, and the
# pebbles and the far boulders stop casting shadows (nobody sees those shadows at phone size).
rep("""  for (const m of [W.hq, W.dock].concat(Object.values(W.blds))) if (m) for (const [o, kind, p] of (m.userData.anim || [])) {""",
    """  const onV = colOnScreen(W); for (const m of [W.hq, W.dock].concat(Object.values(W.blds))) if (m && onV(m)) for (const [o, kind, p] of (m.userData.anim || [])) { /* v825 off-screen buildings rest */""")
rep("""function drawColony(t) {""", """/* v825 is a base structure near the screen? (its plot centre projected through the base camera, with a generous margin) */
function colOnScreen(W) { const v = colOnScreen.v || (colOnScreen.v = new TH.Vector3()); W.cam.updateMatrixWorld(); return m => { if (m.userData.alwaysAnim) return true; v.setFromMatrixPosition(m.matrixWorld); v.project(W.cam); return Math.abs(v.x) < 1.35 && Math.abs(v.y) < 1.45; }; }
function drawColony(t) {""")
rep("""if (!W.folk || W.folk.key !== bt.key + "|" + N + "|" + sp + "|" + facOf()) folkBuild(W, bt); folkStep(W, t); }""",
    """if (!W.folk || W.folk.key !== bt.key + "|" + N + "|" + sp + "|" + facOf()) folkBuild(W, bt); if (!MOBILE || !(t - (W.folkT || 0) < 31)) { W.folkT = t; folkStep(W, t); } } /* v825 30 Hz on phones */""")
rep("""im = new TH.InstancedMesh(pg, rockM, 520), dm = new TH.Object3D(), pr = rnd(515); let c = 0;
    for (let i = 0; i < 4000 && c < 520; i++) {""", """im = new TH.InstancedMesh(pg, rockM, 520), dm = new TH.Object3D(), pr = rnd(515), NP = MOBILE ? 260 : 520; let c = 0; /* v825 half on phones */
    for (let i = 0; i < 4000 && c < NP; i++) {""")
rep("""    im.count = c; im.castShadow = true; im.receiveShadow = true; im.frustumCulled = false; scene.add(im); }""", """    im.count = c; im.castShadow = !MOBILE; im.receiveShadow = true; im.frustumCulled = false; scene.add(im); }""")
rep("""m.scale.set(1.5 + r() * 4, 1 + r() * 4, 1.5 + r() * 4); m.rotation.set(r(), r() * 3, r()); m.castShadow = true; scene.add(m); }""", """m.scale.set(1.5 + r() * 4, 1 + r() * 4, 1.5 + r() * 4); m.rotation.set(r(), r() * 3, r()); m.castShadow = !MOBILE; scene.add(m); }""")
open(p, "w", encoding="utf-8").write(s); print("ok")
