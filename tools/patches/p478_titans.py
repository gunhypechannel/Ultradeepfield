# v478 Remaster step 6, the four titans: the Brood Matriarch, the Iron Tyrant, the Event Horizon Wyrm and the Shard Colossus.
# Matriarch: four brood pods stand round her nest and keep her swarm coming back. One bursts at every fifth of her hull lost (80, 60,
# 40, 20%), and each one gone makes her swarm regrow more slowly: 6 hours to full strength with all four, up to 30 with none.
# Tyrant: a new missile volley (racks on deck launch a salvo that arcs out on smoke trails); its stolen-resource vault sits on deck as a
# heap of gold that grows as the vault grows; and in a battle, fires break out across its hull as it takes damage.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
# ---------------- Matriarch ----------------
rep("    const eggG = puffs(NE, GRN); body.add(eggG);",
r"""    const eggG = puffs(NE, GRN); body.add(eggG);
    /* v478 four brood pods on stalks round the nest; out.pods says how many still stand */
    const podM = eggM.clone(); podM.emissiveIntensity = 1.1; const podD = new TH.MeshStandardMaterial({ color: 0x141a0a, emissive: 0x203a08, emissiveIntensity: .3, metalness: .3, roughness: .5 });
    const pods = [0, 1, 2, 3].map(k => { const a = k * TAU / 4 + .78, g = new TH.Group(); g.position.set(Math.cos(a) * 10.4, -.4, Math.sin(a) * 10.4); body.add(g);
      const st = new TH.Mesh(new TH.CylinderGeometry(.22, .5, 2.2, 7), podD); st.position.y = 1.1; g.add(st); const p = new TH.Mesh(new TH.SphereGeometry(1.5, 22, 16), podM); p.userData.dyn = 1; p.scale.set(1, 1.4, 1); p.position.y = 3.6; g.add(p);
      const gl = sprite(6, "rgba(160,255,60,1)", "podg"); gl.position.y = 3.6; g.add(gl); const bu = sprite(9, "rgba(190,255,90,1)", "podb"); bu.position.y = 3.6; bu.visible = false; g.add(bu); return { g, p, gl, bu, br: -1 }; });""")
rep("      eggM.emissiveIntensity = .45 + Math.sin(t * .002) * .15 + burst * .7;",
"""      { const n = out.pods == null ? 4 : out.pods; pods.forEach((P0, i) => { const gone = i >= n; if (gone && P0.br < 0) P0.br = t; if (!gone) P0.br = -1; const b = P0.br < 0 ? -1 : (t - P0.br) / 1300;
          P0.p.material = gone ? podD : podM; P0.p.scale.set(1, gone ? .45 : 1.4 + Math.sin(t * .003 + i) * .06 + burst * .2, 1); P0.gl.visible = !gone; P0.gl.material.opacity = .55 + .3 * Math.sin(t * .003 + i) + burst * .4;
          P0.bu.visible = b >= 0 && b < 1; if (P0.bu.visible) { P0.bu.material.opacity = 1 - b; P0.bu.scale.setScalar(9 + b * 26); } }); }
      eggM.emissiveIntensity = .45 + Math.sin(t * .002) * .15 + burst * .7;""")
rep("    bake(body); sac.traverse(o => { if (o.material === eM) o.renderOrder = 1; }); sacI.renderOrder = 2; sacS.renderOrder = 3;\n    return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 13, h: 17 }; }",
    "    bake(body); sac.traverse(o => { if (o.material === eM) o.renderOrder = 1; }); sacI.renderOrder = 2; sacS.renderOrder = 3;\n    const out = { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 13, h: 17, pods: null }; return out; }")
rep('if (key === "brd") { const h = Math.max((st.hit || {}).brd || 0, wbStartOf("brd", at)); return 1 + clamp((at - h) / (6 * 3600e3), 0, 1); }',
    'if (key === "brd") { const h = Math.max((st.hit || {}).brd || 0, wbStartOf("brd", at)); return 1 + clamp((at - h) / (6 * 3600e3 * (5 - brdPods(st))), 0, 1); }')
rep("function elCyc(at, L) {", "/* v478 the Matriarch's brood pods still standing: one bursts at every fifth of her hull lost */\nfunction brdPods(st) { const f = (st.hp.brd | 0) / WB_SEG; return 4 - [.8, .6, .4, .2].filter(x => f <= x + 1e-9).length; }\nfunction elCyc(at, L) {")
rep('if (key === "brd") { const I = wbInfect(T); return (s > 1.02 ? `Drone swarm ×${s.toFixed(1)} toughness · it thins when attacked` : "Swarm thinned · full damage now")',
    'if (key === "brd") { const I = wbInfect(T), pd = brdPods(st); return (s > 1.02 ? `Drone swarm ×${s.toFixed(1)} toughness · it thins when attacked` : "Swarm thinned · full damage now") + ` · ${pd} of 4 brood pods, the swarm regrows over ${(5 - pd) * 6} h`')
# ---------------- Tyrant ----------------
rep("    const d0x = k => 2.5 + k * 30, mv = moves({ broadside: 2800, claw: 2600, mines: 3800, hit: 520 }), hit = hitKit(body, shk); const S = scr();",
r"""    /* v478 the missile racks and their salvo, the vault's gold, and fires across the hull as it is damaged */
    const NMS = 14, msl = puffs(NMS * 7, 0xffc070); body.add(msl); const mR = []; for (let i = 0; i < NMS; i++) mR.push({ x: -7 + (i % 7) * 2.1, z: (i < 7 ? -1 : 1) * 1.6, sp: (rnd() - .5) * 10, h: 7 + rnd() * 6, d: .04 * (i % 7) + (i < 7 ? 0 : .02) });
    const racks = [-1, 1].map(sd => { const r = box(15, .7, 1.2, MD); r.position.set(-.7, deckY + .45, sd * 1.6); body.add(r); return r; });
    const gold = new TH.Group(); gold.position.set(9, deckY + .2, 0); body.add(gold); const GM = new TH.MeshStandardMaterial({ color: 0xffc040, metalness: 1, roughness: .25, emissive: 0x6a3a00, emissiveIntensity: .6 });
    const goldB = []; for (let i = 0; i < 18; i++) { const b = box(.9, .5, .55, GM); b.position.set((rnd() - .5) * 2.6, .25 + (i % 6) * .45, (rnd() - .5) * 2.2); b.rotation.y = rnd() * 3; b.userData.dyn = 1; gold.add(b); goldB.push(b); }
    const goldS = sprite(7, "rgba(255,200,80,1)", "tgold"); goldS.position.y = 1.4; gold.add(goldS);
    const burn = puffs(48, 0xff7a20); body.add(burn); const bP = [V(-6, deckY + 1, 3.4), V(2, deckY + 1.5, -3.4), V(7, deckY + .8, 3), V(-12, deckY + 1.2, -2.8)];
    const d0x = k => 2.5 + k * 30, mv = moves({ broadside: 2800, claw: 2600, mines: 3800, missiles: 3200, hit: 520 }), hit = hitKit(body, shk); const S = scr();""")
rep("    const tick = t => { const fb = mv.f(\"broadside\", t), fc = mv.f(\"claw\", t), fm = mv.f(\"mines\", t), fx = mv.f(\"hit\", t);",
"""    const tick = t => { const fb = mv.f("broadside", t), fc = mv.f("claw", t), fm = mv.f("mines", t), fx = mv.f("hit", t), fv = mv.f("missiles", t);
      // the salvo: each missile climbs out of its rack, arcs ahead of the bow and trails smoke
      for (let i = 0; i < NMS; i++) { const R = mR[i]; for (let j = 0; j < 7; j++) { const k = fv < 0 ? -1 : (fv - R.d - j * .025) / .55, on = k > 0 && k < 1; const kk = Math.max(0, Math.min(1, k));
          msl.put(i * 7 + j, R.x + kk * kk * 48, deckY + 1 + Math.sin(kk * Math.PI) * R.h + kk * 3, R.z + kk * R.sp, j ? 1.4 + j * .5 : 1.8, on ? (j ? .55 * (1 - j / 7) * (1 - kk) : 1) : 0); } } msl.done();
      { const v = Math.max(1, out.vault || 1), k = Math.min(1, (v - 1) / 1.5); goldB.forEach((b, i) => { b.visible = i < 4 + Math.round(k * 14); }); goldS.material.opacity = .4 + k * .5 + Math.sin(t * .003) * .08; goldS.scale.setScalar(7 + k * 10); }
      { const h = out.hp == null ? 1 : out.hp, n = h < .2 ? 4 : h < .45 ? 3 : h < .7 ? 2 : h < .9 ? 1 : 0; for (let i = 0; i < 48; i++) { const p = bP[i % 4], on = (i % 4) < n, a = ((t * .0011 + i / 48 * 5.3) % 1); burn.put(i, p.x - a * 3 + Math.sin(i) * .4, p.y + a * 3.5, p.z + Math.cos(i * 2) * .4, (4.2 - a * 2.4) * 1.3, on ? (1 - a) : 0); } burn.done(); }""")
rep("    bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 20, h: 14 }; }",
    "    bake(body); const out = { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 20, h: 14, vault: 1, hp: null, setHp: h => { out.hp = h; } }; return out; }")
rep('tyr: ["broadside", "claw", "mines"]', 'tyr: ["broadside", "missiles", "claw", "mines"]')
rep('tyr: { broadside: ["bolts", .25, .82, 10, 2800],', 'tyr: { broadside: ["bolts", .25, .82, 10, 2800], missiles: ["bolts", .3, .75, 8, 3200],')
rep('["mines", "Mine wake", "It drops a trail of spiked mines behind its stern."]]',
    '["mines", "Mine wake", "It drops a trail of spiked mines behind its stern."], ["missiles", "Missile volley", "The racks on its deck launch a salvo that arcs down on the fleet."]]')
# the map tells them their state; a battle shows the pods it was fought with
rep("if (WB_EL.includes(key)) M.b.mech = { s: wbShOf(key, st, T), k: 0 };", "if (WB_EL.includes(key)) M.b.mech = { s: wbShOf(key, st, T), k: 0 }; if (key === \"brd\") M.b.pods = brdPods(st); if (key === \"tyr\") M.b.vault = wbVault(T);")
rep("if (WB_EL.includes(key) && battle && battle.r) WBR.b.mech = { s: battle.r.wbSh || 1, k: 0 };",
    "if (WB_EL.includes(key) && battle && battle.r) WBR.b.mech = { s: battle.r.wbSh || 1, k: 0 }; if (key === \"brd\" && battle && battle.r && battle.r.wbSeg) WBR.b.pods = brdPods({ hp: { brd: battle.r.wbSeg[0] } }); if (key === \"tyr\" && battle && battle.r) WBR.b.vault = wbVault(battle.r.at || now());")
# ---------------- Wyrm ----------------
# Its vulnerable segments travel along its body as before, but now they only blaze while its segments are exposed; hidden, they are
# dim armour. A field of debris orbits its black hole, and it is flung wider while the Wyrm coils.
rep("    const mv = moves({ coil: 3000, lens: 3000, sweep: 2200, hit: 520 }), hit = hitKit(body, shk); const S = scr(), c1 = new TH.Color(), tmp = V(0, 0, 0);",
r"""    /* v478 the orbiting debris */
    const DN = LOD === 1 ? 40 : 70, deb = inst(new TH.DodecahedronGeometry(.6, 0), MA, DN); body.add(deb); const dD = []; for (let i = 0; i < DN; i++) dD.push({ r: 14 + rnd() * 12, a: rnd() * TAU, w: .00006 + rnd() * .00012, y: (rnd() - .5) * 5, s: .4 + rnd() * rnd() * 2.2, ax: V(rnd() - .5, rnd() - .5, rnd() - .5).normalize() });
    const mv = moves({ coil: 3000, lens: 3000, sweep: 2200, hit: 520 }), hit = hitKit(body, shk); const S = scr(), c1 = new TH.Color(), tmp = V(0, 0, 0);""")
rep("let hot = 0; for (let k = 0; k < 3; k++) { const c = ((t * .00005 + k / 3) % 1) * N; hot = Math.max(hot, 1 - Math.min(1, Math.abs(i - c) / 1.6)); }",
    "let hot = 0; for (let k = 0; k < 3; k++) { const c = ((t * .00005 + k / 3) % 1) * N; hot = Math.max(hot, 1 - Math.min(1, Math.abs(i - c) / 1.6)); } hot *= out.open === false ? .18 : 1;")
rep("      bt(t, 1 + coil * 6 + fire * 2); hit(bell(fx, 0, .05, .4, 1), t); };\n    const tmpQ = new TH.Quaternion(), tmpQ2 = new TH.Quaternion(), tmp2 = new TH.Object3D();\n    bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 15, h: 11, own: [hole, disc, disc2, phR, bhG], mouth, lens }; }",
"""      for (let i = 0; i < DN; i++) { const d = dD[i], a = d.a + t * d.w * (1 + coil * 3), R = d.r * (1 + coil * .25); S.p.set(Math.cos(a) * R, d.y + Math.sin(t * .0007 + i) * .6, Math.sin(a) * R); S.q.setFromAxisAngle(d.ax, t * .0007 + i); S.s.setScalar(d.s); S.m.compose(S.p, S.q, S.s); deb.setMatrixAt(i, S.m); } deb.instanceMatrix.needsUpdate = true;
      bt(t, 1 + coil * 6 + fire * 2); hit(bell(fx, 0, .05, .4, 1), t); };
    const tmpQ = new TH.Quaternion(), tmpQ2 = new TH.Quaternion(), tmp2 = new TH.Object3D();
    bake(body); const out = { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 15, h: 11, own: [hole, disc, disc2, phR, bhG], mouth, lens, open: null }; return out; }""")
# ---------------- Colossus ----------------
# Smaller crystal drones break off and fly round it, more as it shatters (none whole, five cracked, ten shattered). Once shattered, its
# heart is exposed for 2 minutes in every 10 (full damage instead of the fragments' shield): a white target ring on the heart.
rep("    const mv = moves({ rain: 2800, prism: 3000, shatter: 2800, hit: 520 }), hit = hitKit(body, shk); const S = scr(), eyeW = V(0, 0, 0);",
r"""    /* v478 the crystal drones and the exposed heart's target ring */
    const NDR = 10, drn = inst(new TH.OctahedronGeometry(.9, 0).scale(.7, 1.4, .7), CC, NDR); body.add(drn); const drG = puffs(NDR, 0x9feaff); body.add(drG); const drD = []; for (let i = 0; i < NDR; i++) drD.push({ r: 9 + rnd() * 7, y: 6 + rnd() * 12, w: (.0005 + rnd() * .0005) * (i % 2 ? 1 : -1), a: rnd() * TAU, ph: rnd() * TAU });
    const hT = new TH.Sprite(new TH.SpriteMaterial({ map: radial("elwkR", [[0, "rgba(255,255,255,0)"], [.68, "rgba(255,255,255,0)"], [.76, "rgba(255,255,255,1)"], [.84, "rgba(255,255,255,0)"], [1, "rgba(255,255,255,0)"]]), blending: TH.AdditiveBlending, depthWrite: false, depthTest: false, transparent: true, toneMapped: false })); hT.visible = false; heart.add(hT);
    const mv = moves({ rain: 2800, prism: 3000, shatter: 2800, hit: 520 }), hit = hitKit(body, shk); const S = scr(), eyeW = V(0, 0, 0);""")
rep("      shatW(fs < 0 ? -1 : (fs - .2) / .7); stompW(fs < 0 ? -1 : (fs - .62) / .38); bt(t, 1 + burst * 5 + fire * 2 + lift * 2); hit(bell(fx, 0, .05, .4, 1), t); };\n    bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 14, h: 18 }; }",
"""      { const nd = out.phase === 2 ? 10 : out.phase === 1 ? 5 : 0; for (let i = 0; i < NDR; i++) { const d = drD[i], on = i < nd, a = d.a + t * d.w, sw = Math.sin(t * .0013 + d.ph); S.p.set(Math.cos(a) * d.r * (1 + sw * .25), d.y + sw * 2, Math.sin(a) * d.r); S.e.set(0, -a, sw * .4); S.q.setFromEuler(S.e); S.s.setScalar(on ? 1 : .001); S.m.compose(S.p, S.q, S.s); drn.setMatrixAt(i, S.m); drG.put(i, S.p.x, S.p.y, S.p.z, 3.2, on ? .55 + .3 * Math.sin(t * .01 + i) : 0); } drn.instanceMatrix.needsUpdate = true; drG.done(); }
      hT.visible = !!out.heart; if (hT.visible) { const q = .5 + .5 * Math.sin(t * .005); hT.material.opacity = 1 - q * .3; hT.scale.setScalar(7 - q * 2); }
      shatW(fs < 0 ? -1 : (fs - .2) / .7); stompW(fs < 0 ? -1 : (fs - .62) / .38); bt(t, 1 + burst * 5 + fire * 2 + lift * 2); hit(bell(fx, 0, .05, .4, 1), t); };
    bake(body); const out = { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 14, h: 18, phase: 0, heart: 0 }; return out; }""")
rep('if (key === "col") { const hp = st.hp.col | 0; return hp <= 10 ? 1.8 : hp <= 20 ? 1.4 : 1; }',
    'if (key === "col") { const hp = st.hp.col | 0; return hp <= 20 && colHeart(at) ? 1 : hp <= 10 ? 1.8 : hp <= 20 ? 1.4 : 1; }')
rep("function elCyc(at, L) {", "/* v478 the shattered Colossus's heart is exposed for 2 minutes in every 10 */\nconst colHeart = at => elCyc(at, 6e5) < 12e4;\nfunction elCyc(at, L) {")
rep('if (key === "col") return s > 1 ? `Shattered · fragments shield it ×${s}` : "Whole · shatters below 50% hull";',
    'if (key === "col") { const hp = st.hp.col | 0, c = elCyc(T, 6e5); return hp <= 20 ? (c < 12e4 ? `Heart exposed · full damage for ${ftime(12e4 - c)}` : `Shattered · fragments shield it ×${s} · heart exposed in ${ftime(6e5 - c)}`) : "Whole · shatters below 50% hull"; }')
rep('if (key === "brd") M.b.pods = brdPods(st);', 'if (key === "brd") M.b.pods = brdPods(st); if (key === "wym") M.b.open = wymOpen(T); if (key === "col") { const h = st.hp.col | 0; M.b.phase = h <= 10 ? 2 : h <= 20 ? 1 : 0; M.b.heart = h <= 20 && colHeart(T) ? 1 : 0; }')
rep('if (key === "brd" && battle && battle.r && battle.r.wbSeg) WBR.b.pods = brdPods({ hp: { brd: battle.r.wbSeg[0] } });',
    'if (key === "brd" && battle && battle.r && battle.r.wbSeg) WBR.b.pods = brdPods({ hp: { brd: battle.r.wbSeg[0] } }); if (key === "wym" && battle && battle.r) WBR.b.open = (battle.r.wbSh || 1) < 1.3; if (key === "col" && battle && battle.r && battle.r.wbSeg) { const h = battle.r.wbSeg[0]; WBR.b.phase = h <= 10 ? 2 : h <= 20 ? 1 : 0; WBR.b.heart = h <= 20 && (battle.r.wbSh || 1) <= 1 ? 1 : 0; }')
s = re.sub(r"GAME_V = 477\b", "GAME_V = 478", s)
open(P, 'w').write(s)
