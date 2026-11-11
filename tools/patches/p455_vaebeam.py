# v455 Vaelthar remastered for Divine Annihilation (owner: sharper gold armour and violet glyphs; he leans forward and the wheel spins
# flat on his back like the reference video; far more charged particles and electric glow; an aura that glows brighter and brighter
# until he releases; a beam that nearly blankets the whole map; everything HDR with popping detail). Model changes here, the map-scale
# beam in p455_vaebeam.js.
import re, os
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
js = open(os.path.join(os.path.dirname(__file__), 'p455_vaebeam.js')).read()
rep("/* v408 tapping the Super Cube */", js + "/* v408 tapping the Super Cube */")
# sharper HDR materials: mirror gold with deep relief, obsidian scale carved with glowing violet sigils
rep('const MA = hullMat("vae", { rows: 7, pal: ["#140e1d", "#1b1326", "#100b17", "#22172e", "#181022"], slits: .18, sc: "#e8c8ff", sg: "#b45cff", veins: 10, vc: "#9a5cff", metal: .86, rough: .3, rc: RC, ei: 2.4, rep: [3, 1] });',
    'const MA = hullMat("vae", { rows: 7, pal: ["#140e1d", "#1b1326", "#100b17", "#22172e", "#181022"], slits: .2, sc: "#f0d8ff", sg: "#c070ff", veins: 18, vc: "#b878ff", glyphs: 1, metal: .9, rough: .2, rc: RC, ei: 3.8, rep: [3, 1] }); MA.normalScale.set(2.4, 2.4); MA.envMapIntensity = 1.5;')
rep('const MG = hullMat("vaeg", { rows: 3, pal: ["#b88a2a", "#d6ad4c", "#a07a22", "#e2bd5c"], bronze: 0, slits: .22, sc: "#fff2c8", sg: "#ffc65a", metal: 1, rough: .2, rc: [1, .78, .4], ei: 1.6, rep: [2, 1] }); MG.envMapIntensity = 1.6;',
    'const MG = hullMat("vaeg", { rows: 3, pal: ["#c8901e", "#e6b23c", "#a87418", "#f5c84a"], bronze: 0, slits: .26, sc: "#fff6d8", sg: "#ffd06a", metal: 1, rough: .11, rc: [1, .82, .45], ei: 2.4, rep: [2, 1] }); MG.envMapIntensity = 2.1; MG.normalScale.set(2.2, 2.2);')
rep('rc: [1, .7, .4], ei: 2.2, rep: [4, 1], glyphs: 1 }); MGd.envMapIntensity = 1.3;', 'rc: [1, .7, .4], ei: 3.4, rep: [4, 1], glyphs: 1 }); MGd.envMapIntensity = 2.0; MGd.normalScale.set(2, 2);')
# more charge: particles into the wheel, a second stream into his jaws, more lightning, and the aura
rep("const NP = LO ? 70 : 120, motes = puffs(NP, 0xd8b0ff);", "const NP = LO ? 140 : 300, motes = puffs(NP, 0xd8b0ff);")
rep("    const bt = bolts(body, 10, () => {", """    const NJ = LO ? 70 : 150, jet = puffs(NJ, 0xf0d8ff); body.add(jet); const jD = []; for (let k = 0; k < NJ; k++) jD.push({ a: rnd() * TAU, b: rnd() * TAU, r0: 6 + rnd() * 14, ph: rnd(), w: .00025 + rnd() * .0003 });
    const NA = Math.ceil(N / 2), aura = []; for (let k = 0; k < NA; k++) { const s = sprite(1, "rgba(150,70,255,1)", "vae_aura2"); s.material.opacity = 0; body.add(s); aura.push(s); }
    const btM = bolts(body, 10, () => { const a = ap.getWorldPosition(V(0, 0, 0)), m = mouth.getWorldPosition(V(0, 0, 0)); body.worldToLocal(a); body.worldToLocal(m); return [a, m]; }, 0xe8d0ff);
    const bt = bolts(body, 20, () => {""")
rep("const btW = bolts(wheel, 8,", "const btW = bolts(wheel, 16,")
rep("st.sway = fire * Math.sin((A - .66) / .2 * Math.PI * 1.2 - .6) * .35;", "st.sway = fire * Math.sin((A - .66) / .2 * Math.PI * 1.2 - .6) * .72; const lean = A < 0 ? 0 : ss(.05, .3, A) * (1 - ss(.9, 1, A)); out.lean = lean; out.fireK = fire; out.sway = st.sway;")
rep("tmpV.copy(P[0]).add(tmpV2.set(st.sway * .9 + Math.sin(t * .0005) * .08, -.28 + st.lift * .75 - st.recoil * .12, 1)); body.localToWorld(tmpV); head.lookAt(tmpV);",
    "tmpV.copy(P[0]).add(tmpV2.set(st.sway * .9 + Math.sin(t * .0005) * .08, -.28 + st.lift * .75 - st.recoil * .12 + out.lean * .5, 1)); body.localToWorld(tmpV); head.lookAt(tmpV);")
rep("      lens.visible = fire > .01; if (lens.visible) { bm.forEach(([m, o], k) => {", "      lens.visible = fire > .01 && !out.noLens; if (lens.visible) { bm.forEach(([m, o], k) => {")
# he leans into it; the wheel tips down to lie flat across his back and spins there
rep("      const dt = Math.min(64, t - (out.lt || t)); out.lt = t; const crack = out.crack;",
"""      const dt = Math.min(64, t - (out.lt || t)); out.lt = t; const crack = out.crack, Lg = out.lean || 0;
      body.rotation.x = Lg * .42; wheel.rotation.set(-Lg * (Math.PI / 2 + .42), 0, 0); wheel.rotateY(.12 * (1 - Lg)); wheel.position.set(0, 11 + Lg * 5, -11 + Lg * 5.5);
      // the aura: a violet glow along his whole body, brighter and brighter through the charge, peaking as he fires
      const au = A < 0 ? .12 + .05 * Math.sin(t * .002) : .15 + warn * .25 + runes * .35 + acc * .8 + align * 1.5 + fire * 1.1 - after * .9;
      for (let k = 0; k < NA; k++) { const i = k * 2, p = P[i], s = aura[k]; s.position.copy(p); const z = SC[i] * (2.4 + au * 1.1) * (1 + .12 * Math.sin(t * .006 + k)); s.scale.setScalar(z); s.material.opacity = Math.min(.42, .06 + au * .11); }
      const pull = Math.max(acc, align * 1.2, fire * .6); if (pull > .01 || jet.visible) { mouth.getWorldPosition(tmpV); body.worldToLocal(tmpV); for (let k = 0; k < NJ; k++) { const m = jD[k], ph = (m.ph + t * m.w * (1 + pull * 3)) % 1, r = m.r0 * (1 - ph), a = m.a + ph * 5;
        jet.put(k, tmpV.x + Math.cos(a) * Math.sin(m.b) * r, tmpV.y + Math.sin(a) * r * .8, tmpV.z + Math.cos(m.b) * r * .6, .5 + (1 - ph) * .5, pull * Math.min(1, ph * 6) * (.4 + .6 * ph)); } jet.done(); }
      btM(t, acc * 5 + align * 8 + fire * 4);""")
rep('moves: ["claw", "wing", "judge", "seal", "rebirth", "annihilate"] };', 'moves: ["claw", "wing", "judge", "seal", "rebirth", "annihilate"] }; out.lensDir = v => v.set(0, 0, 1).applyQuaternion(lens.getWorldQuaternion(new TH.Quaternion()));')
# on the map: the model's own small beam gives way to the map-scale one, in the preview and live
rep("X.b = BOSS3D.prep(BOSS3D[D.m3](), wbEnv(W.renderer));", "X.b = BOSS3D.prep(BOSS3D[D.m3](), wbEnv(W.renderer)); if (key === \"vae\") X.b.noLens = 1;")
rep("if (b.lens && b.lens.visible) { b.mouth.getWorldPosition(X.V); const o = X.V.clone(), d = new TH.Vector3(0, 0, 1).applyQuaternion(b.lens.getWorldQuaternion(new TH.Quaternion())); sbBeamKill(X, o, d, 4.2 * sc, 80 * sc, t); } }",
    "}")
rep("  else X.quiet = false;", "  else X.quiet = false; sbVaeBeam(W, X, b, t, 1); X.expK = 1 + (b.ph === \"beam\" ? (b.fireK || 0) * .35 : 0);")
rep(": s < A0 + AL * .9 ? { y: 30, d: 760, th: .42, ph: Math.PI / 2 + .55, tx: X.B.x + X.F.x * 160, tz: X.B.z + X.F.z * 160 }", ": s < A0 + AL * .9 ? { y: 40, d: 1350, th: .62, ph: .95, tx: X.B.x + X.F.x * 520, tz: X.B.z + X.F.z * 520 }")
rep('b.drive("annihilate", fa); const d = Math.min(6', 'b.drive("annihilate", fa); sbVaeBeam(W, X, b, t, 0); sbBoomTick(X, t); X.expK = 1 + (b.ph === "beam" ? (b.fireK || 0) * .35 : 0); const d = Math.min(6')
s = re.sub(r"GAME_V = 454\b", "GAME_V = 455", s)
open(P, 'w').write(s)
