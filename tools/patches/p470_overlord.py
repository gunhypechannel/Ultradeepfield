# v470 Remaster step 1, the Pyramid Overlord (live 2026-11-21), and a death for every world boss.
# Overlord: every footfall lands with a jolt and a ring of dust and violet light; its belly emitters turn, faster as it charges; a pyramid
# shield of up to four layers, one per living Energy Conduit, each layer cracking, flaring and bursting as its conduit falls; and its death,
# a fortress-core overload: all four sigils fire beams outward, the emitters scream round, then it blows apart (blast, scatter, crystal,
# spirits, glyph). Every other world boss and Elemental now dies the same way instead of vanishing (an overload flash, then the blast in its
# colour, the scatter, crystal and spirits, and a glyph); a conduit just shatters and dissolves. Boss Lab can preview any of these deaths.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
# --- the Overlord model ---
rep("const groundY = -.55 + 2.8 - 8.4 - .4, quake = wave(grp, 9, false);",
"""const groundY = -.55 + 2.8 - 8.4 - .4, quake = wave(grp, 9, false);
    /* v470 footfalls, the shield of four layers, the four-face beams of its overload */
    const steps = []; for (let k = 0; k < 6; k++) { const m = new TH.Mesh(new TH.RingGeometry(.55, 1, 40), glowMat(VIO2, 0)); m.rotation.x = -Math.PI / 2; m.userData.dyn = 1; m.visible = false; grp.add(m); const d = new TH.Mesh(new TH.CircleGeometry(1, 24), glowMat(0x9a80c0, 0)); d.rotation.x = -Math.PI / 2; d.userData.dyn = 1; d.visible = false; grp.add(d); steps.push({ m, d, t: -1e9 }); } let si = 0; const fw0 = V(0, 0, 0);
    const shM = () => new TH.ShaderMaterial({ uniforms: { uO: { value: 0 }, uC: { value: new TH.Color(0xb070ff) }, uT: { value: 0 } }, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, side: TH.DoubleSide, toneMapped: false,
      vertexShader: "varying vec3 vN; varying vec3 vV; varying vec3 vP; void main() { vec4 mv = modelViewMatrix * vec4(position, 1.); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); vP = position; gl_Position = projectionMatrix * mv; }",
      fragmentShader: "uniform float uO, uT; uniform vec3 uC; varying vec3 vN; varying vec3 vV; varying vec3 vP; void main() { float fr = pow(1. - abs(dot(vN, vV)), 2.); float hx = abs(sin(vP.x * 2.2 + uT) * sin(vP.y * 2.2) * sin(vP.z * 2.2 - uT)); float a = (fr * 1.1 + pow(hx, 6.) * .7 + .06) * uO; gl_FragColor = vec4(uC * a, a); }" });
    const shells = [0, 1, 2, 3].map(k => { const m = new TH.Mesh(new TH.ConeGeometry((B * Math.SQRT2 + 2.2 + k * .9), H + 3.4 + k * .9, 4, 1, true), shM()); m.rotation.y = Math.PI / 4; m.position.y = y0 + (H + 3.4 + k * .9) / 2 - 1.6; m.userData.dyn = 1; m.visible = false; body.add(m); return { m, on: 0, brk: -1 }; });
    const fBeams = [1, 2, 3].map(k => { const g = new TH.Group(); g.rotation.y = k * Math.PI / 2; body.add(g); const f = fBeam.clone(); f.visible = false; g.add(f); return f; });""")
rep("bt(t, 1 + surge * 4 + fire * 2); hit(bell(fh, 0, .05, .4, 1), t); };",
"""      // footfalls: each foot that comes down lands with a jolt and a ring
      { let jolt = 0; for (const g of legs) { const p = t * sp + g.ph, up = Math.cos(p); if (g.upL > .05 && up <= .05 && W > .5) { const S0 = steps[si++ % steps.length]; g.kn.updateWorldMatrix(true, false); fw0.set(1.7, -8.4, 0); g.kn.localToWorld(fw0); grp.worldToLocal(fw0); S0.m.position.set(fw0.x, groundY + .05, fw0.z); S0.d.position.copy(S0.m.position); S0.t = t; jolt = 1; } g.upL = up; }
        if (jolt) out.jolt = t; const ja = (t - (out.jolt || -1e9)) / 260; if (ja < 1) body.position.y -= Math.sin(ja * Math.PI) * .14; }
      for (const S0 of steps) { const a = (t - S0.t) / 900; S0.m.visible = S0.d.visible = a >= 0 && a < 1; if (S0.m.visible) { S0.m.scale.setScalar(1 + a * 3.2); S0.m.material.opacity = (1 - a) * .7; S0.d.scale.setScalar(1.2 + a * 2.4); S0.d.material.opacity = (1 - a) * (1 - a) * .35; } }
      // the belly emitters turn, faster while it charges or summons
      emit.rotation.y += .004 + charge * .04 + surge * .03 + (out.over || 0) * .12; emit.children.forEach((r, k) => { r.rotation.y = Math.sin(t * .0007 + k) * .25; });
      // the shield: one layer per living conduit; a layer that loses its conduit cracks, flares and bursts
      shells.forEach((L, k) => { const want = k < (out.cons == null ? 0 : out.cons) ? 1 : 0; if (L.on && !want && L.brk < 0) L.brk = t; L.on = want;
        const b = L.brk >= 0 ? (t - L.brk) / 1400 : -1; if (b >= 1) L.brk = -1; const vis = want || (b >= 0 && b < 1); L.m.visible = vis; if (!vis) return; const U = L.m.material.uniforms; U.uT.value = t * .001 + k;
        if (b >= 0 && b < 1) { U.uO.value = (b < .45 ? (rnd() < .5 ? 1.6 : .2) : (1 - b) * 2.2); L.m.scale.setScalar(1 + Math.max(0, b - .45) * .9); U.uC.value.setRGB(1, .75, 1); } else { U.uO.value = .75 + .15 * Math.sin(t * .003 + k) + fire * .3; L.m.scale.setScalar(1); U.uC.value.setRGB(.69, .44, 1); } });
      // its death: the fortress core overloads, every face firing
      const ov = out.over || 0; if (ov > 0) { const f = Math.min(1, ov * 1.3); for (const s of sigils) { s.sp.material.opacity = 1; s.sp.scale.setScalar(3.4 * (1 + f * 2.5)); s.sgs.rotation.z += f * .2; } fBeam.visible = true; fb1.material.opacity = .5 * f; fb2.material.opacity = .9 * f; fbS.material.opacity = f; fBeam.position.set(0, y0 + Math.cos(phi) * Ls * .3 + .1, B - Math.sin(phi) * Ls * .3 + .7); fBeam.scale.set(1 + f, 1 + f, 1 + f * .8);
        fBeams.forEach(F => { F.visible = true; F.position.copy(fBeam.position); F.scale.copy(fBeam.scale); }); body.position.x = (rnd() - .5) * .25 * f; body.position.z = (rnd() - .5) * .25 * f; } else fBeams.forEach(F => { F.visible = false; });
      bt(t, 1 + surge * 4 + fire * 2 + (out.over || 0) * 10); hit(Math.max(bell(fh, 0, .05, .4, 1), (out.over || 0) * .8), t); };""")
rep("bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 12, h: 16 }; }",
    "bake(body); const out = { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 12, h: 16, cons: 0, over: 0 }; return out; }")
# --- the map: conduits feed the shield; every world boss dies on screen ---
rep("if (D.con != null) { const on = st.hp.ovl > 0;", "if (key === \"ovl\") M.b.cons = [0, 1, 2, 3].filter(i => st.hp[\"c\" + i] > 0 && wbOn(\"c\" + i, T)).length; if (D.con != null) { const on = st.hp.ovl > 0;")
rep("pdie = key === \"epx\" && st.dead && st.dead.epx && T >= st.dead.epx && T - st.dead.epx < 26000 && stCyc(st, \"epx\") === wbCyc2(T),",
    "dAt = G.wbFakeDead && G.wbFakeDead.k === key ? G.wbFakeDead.at : st.dead && st.dead[key] && stCyc(st, key) === wbCycOf(key, T) ? st.dead[key] : 0, pdie = !!dAt && T >= dAt && T - dAt < 26000,")
rep("if (!(pdie && wbPentDie(W, M, q, (T - st.dead.epx) / 1000, t))) M.b.tick(t); }",
    "if (!(pdie && (key === \"epx\" ? wbPentDie(W, M, q, (T - dAt) / 1000, t) : wbBossDie(W, M, q, (T - dAt) / 1000, t, key)))) M.b.tick(t); }")
rep("alive = st.hp[key] > 0 && wbOn(key, T) && !(key === \"epx\" && wbSwept(T)),", "alive = st.hp[key] > 0 && wbOn(key, T) && !(key === \"epx\" && wbSwept(T)) && !(G.wbFakeDead && G.wbFakeDead.k === key),")
rep("function wbPentDie(W, M, q, e, t) {", r'''/* v470 a world boss's death: its core overloads (the Overlord's whole fortress firing), then it blows apart in its own colour, every part
   flung out tumbling, turning to crystal and dissolving into spirits, and a glyph stays; a conduit only shatters and dissolves */
function wbBossDie(W, M, q, e, t, key) { const b = M.b, D = WB[key], con = D.con != null;
  if (!M.pd) { const X = { key, grp: new TH.Group(), B: new TH.Vector3(q.x, q.y, q.z), V: new TH.Vector3(), V2: new TH.Vector3(), ships: [], b, F: new TH.Vector3(0, 0, 1) }; W.scene.add(X.grp);
    const wh = W.glow.wh || (W.glow.wh = glowTex("255,255,255", .85)); X.flash = new TH.Sprite(W.additive(wh, new TH.Color(D.col || "#e2d4ff"), 0)); X.flash.position.copy(X.B); X.grp.add(X.flash);
    X.booms = []; for (let i = 0; i < (MOBILE ? 12 : 24); i++) { const s = new TH.Sprite(W.additive(W.glow.fire || (W.glow.fire = glowTex("255,190,120", .8)), 0xffd0a0, 0)); s.visible = false; X.grp.add(s); X.booms.push({ s, t: -1e9, sz: 30 }); } X.bi = 0; M.pd = X; }
  const X = M.pd, sc = b.grp.scale.x, OV = con ? .8 : key === "ovl" ? 3 : 2;
  if (e < OV) { const k = e / OV; X.flash.material.opacity = k * .75; X.flash.scale.setScalar((con ? 60 : 220) * sc * (1 - k * .5)); b.over = k; if (Math.random() < .04 + k * .2) sbBoom(X, X.B.clone().add(new TH.Vector3((Math.random() - .5) * 20 * sc, Math.random() * 15 * sc, (Math.random() - .5) * 20 * sc)), t, (20 + k * 50) * sc); }
  const ib = e - OV; sbShatter(X, b, ib); if (!con) sbBlast(W, X, ib, t); else { X.flash.material.opacity = Math.max(0, 1 - ib / .6) * (ib >= 0 ? 1 : X.flash.material.opacity); for (const Bm of X.booms) { const a = (t - Bm.t) / 900; Bm.s.visible = a >= 0 && a < 1; if (Bm.s.visible) { Bm.s.material.opacity = (1 - a) * .95; Bm.s.scale.setScalar(Bm.sz * (.4 + a * 1.4)); } } }
  sbVaeCrystal(W, X, b, ib - 1.2, t, 1); if (!con) { X.glySeed = X.glySeed || Math.round(q.x * 7 + q.z * 13 + Math.floor(now() / 864e5)); sbGlyph(W, X, ib - 9.5, t); } return ib >= 0; }
function wbPentDie(W, M, q, e, t) {''')
# the blast in the world boss's own colour
rep("const vae = X.key === \"vae\", px = X.key === \"epx\", r1 = mk(.03, px ? 0xfff0c0 : vae ? 0xffe2a0 : 0xcfeeff), r2 = mk(.09, px ? 0x7dffb0 : vae ? 0xa45cff : 0x58b8ff), r3 = mk(.025, px ? 0xff9a50 : 0xffffff), sh = new TH.Mesh(new TH.SphereGeometry(1, 40, 24), dvRim(px ? 0xe2d4ff : vae ? 0xc890ff : 0x7ac8ff));",
    "const vae = X.key === \"vae\", px = X.key === \"epx\", wc = X.key !== \"epx\" && typeof WB !== \"undefined\" && WB[X.key] ? new TH.Color(WB[X.key].col).getHex() : null, r1 = mk(.03, px ? 0xfff0c0 : vae ? 0xffe2a0 : wc ? 0xffffff : 0xcfeeff), r2 = mk(.09, px ? 0x7dffb0 : vae ? 0xa45cff : wc || 0x58b8ff), r3 = mk(.025, px ? 0xff9a50 : 0xffffff), sh = new TH.Mesh(new TH.SphereGeometry(1, 40, 24), dvRim(px ? 0xe2d4ff : vae ? 0xc890ff : wc || 0x7ac8ff));")
# Boss Lab: preview a world boss's death
rep("labStop: () => { G.wbShow = null; WBN = null; if (sheet) renderSheet(); },",
    "labStop: () => { G.wbShow = null; G.wbFakeDead = null; WBN = null; if (sheet) renderSheet(); },\n  labDie: d => { if (!duelOwner()) return; const k = d.k; if (!WB[k]) return; G.wbShow = k; WBN = null; closeSheet(); setTimeout(() => { try { cineObjStart(\"wb_\" + k); } catch (e) {} }, 800); setTimeout(() => { G.wbFakeDead = { k, at: now() }; if (G3 && G3.cam && G3.cam.cineObj) { G3.cam.goal = { dist: (WB[k].cam || 105) * WB[k].sc * 3 }; } toast(`Owner preview: ${WB[k].n} falls (on this device only).`); }, 5000); clearTimeout(G.wbShowT); G.wbShowT = setTimeout(() => { G.wbShow = null; G.wbFakeDead = null; WBN = null; }, 45000); },")
rep("<button class=\"btn ghost\" data-act=\"labPrev\" data-k=\"${k}\">▶ Preview</button></div>`; }).join(\"\");",
    "<button class=\"btn ghost\" data-act=\"labPrev\" data-k=\"${k}\">▶ Preview</button>${WB[k] ? `<button class=\"btn ghost\" data-act=\"labDie\" data-k=\"${k}\">✝ Death</button>` : \"\"}</div>`; }).join(\"\");")
s = re.sub(r"GAME_V = 469\b", "GAME_V = 470", s)
open(P, 'w').write(s)
