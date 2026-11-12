# v476 Remaster step 5a, the five Elementals (the Convergence, 2026-12-09): each has its own mechanic and its own weak point, worked
# out from the shared clock and the hunt record so every player sees the same, and each shows it on the model:
#   Voltaris   storm nodes charge for 22 minutes (tougher up to x1.8), then it discharges and its core is exposed for 8 (x0.8)
#   Ignaroth   molten armour (x1.5) until its hull falls below 60%, then the armour cracks and its core is exposed (x0.9)
#   Auricor    a radiant shield for 8 minutes in every 12 (x1.8), down for 4 (its core exposed)
#   Gravemorn  gravity compression: just after it is hit it is crushed tight (up to x1.6), easing over 20 minutes; space your attacks
#   Viridrax   regrowth: the longer it goes unhit the more it regrows (up to x1.7 after 3 hours); keep it under fire
# On the model: a shell of its colour as strong as its toughness, three storm nodes on Voltaris that brighten as they charge, and a
# pulsing white target ring on the heart while its weak point is exposed. A battle shows the state it was fought in.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
# --- the mechanics ---
rep('if (key === "col") { const hp = st.hp.col | 0; return hp <= 10 ? 1.8 : hp <= 20 ? 1.4 : 1; } return 1; }',
r'''if (key === "col") { const hp = st.hp.col | 0; return hp <= 10 ? 1.8 : hp <= 20 ? 1.4 : 1; }
  if (key === "est") { const c = elCyc(at, 18e5); return c < 132e4 ? 1 + .8 * c / 132e4 : .8; }
  if (key === "efi") return (st.hp.efi | 0) > WB_SEG * .6 ? 1.5 : .9;
  if (key === "eli") return elCyc(at, 72e4) < 48e4 ? 1.8 : 1;
  if (key === "eic") { const h = (st.hit || {}).eic || 0; return 1 + .6 * clamp(1 - (at - h) / 12e5, 0, 1); }
  if (key === "ena") { const h = (st.hit || {}).ena || 0; return 1 + .7 * clamp((at - h) / (3 * 3600e3), 0, 1); } return 1; }
/* v476 an Elemental's cycle position (ms into it), the same for everyone */
function elCyc(at, L) { return ((at - ROT0) % L + L) % L; }
function elTwist(key, st, T) { const s = wbShOf(key, st, T), x = `×${s.toFixed(1)}`;
  if (key === "est") { const c = elCyc(T, 18e5); return c < 132e4 ? `Storm nodes charging · ${x} toughness · discharges in ${ftime(132e4 - c)}` : `Discharged · core exposed, ${x} for ${ftime(18e5 - c)}`; }
  if (key === "efi") return s > 1 ? `Molten armour ${x} · it cracks below 60% hull` : `Armour cracked · core exposed, ${x}`;
  if (key === "eli") { const c = elCyc(T, 72e4); return c < 48e4 ? `Radiant shield ${x} · drops in ${ftime(48e4 - c)}` : `Shield down · core exposed for ${ftime(72e4 - c)}`; }
  if (key === "eic") return s > 1.02 ? `Gravity compression ${x} · eases over 20 m, space your attacks` : "Uncompressed · full damage";
  if (key === "ena") return s > 1.02 ? `Regrown ${x} · keep it under fire to cut it back` : "Cut back · full damage"; return ""; }''')
rep('if (WB_EL.includes(key)) return `Fuses into the Pentarch in ${ftime(wbLiveEnd(key, T) - T)} · slay it first and the Pentarch is weaker`;',
    'if (WB_EL.includes(key)) return `${elTwist(key, st, T)} · fuses into the Pentarch in ${ftime(wbLiveEnd(key, T) - T)}`;')
rep('for (const k of WB_EL) add(k, "", 1);',
    'add("est", "nodes charged", 1.8); add("est", "discharged", .8); add("efi", "molten armour", 1.5); add("efi", "armour cracked", .9); add("eli", "radiant shield", 1.8); add("eli", "shield down", 1); add("eic", "compressed", 1.6); add("ena", "regrown", 1.7);')
# --- the model shows it ---
rep("const sw = wave(body, 10, true, E.c1), sw2 = wave(body, 14, false, E.c2);",
r"""const sw = wave(body, 10, true, E.c1), sw2 = wave(body, 14, false, E.c2);
    /* v476 its mechanic on the model: a shell as strong as its toughness, storm nodes, the exposed weak point */
    const mS = new TH.ShaderMaterial({ uniforms: { uO: { value: 0 }, uC: { value: new TH.Color(E.c1) }, uT: { value: 0 }, uH: { value: kind === "light" ? 1 : kind === "fire" ? .4 : .7 } }, transparent: true, depthWrite: false, blending: TH.AdditiveBlending, side: TH.DoubleSide, toneMapped: false,
      vertexShader: "varying vec3 vN; varying vec3 vV; varying vec3 vP; void main() { vec4 mv = modelViewMatrix * vec4(position, 1.); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); vP = position; gl_Position = projectionMatrix * mv; }",
      fragmentShader: "uniform float uO, uT, uH; uniform vec3 uC; varying vec3 vN; varying vec3 vV; varying vec3 vP; void main() { float fr = pow(1. - abs(dot(vN, vV)), 2.); float hx = abs(sin(vP.x * .9 + uT) * sin(vP.y * .9) * sin(vP.z * .9 - uT)); float a = (pow(fr, 1.5) * 1.6 + pow(hx, 5.) * 1.1 * uH + .07) * uO; gl_FragColor = vec4(mix(uC, vec3(1.), fr * .35) * a, a); }" });
    const mSh = new TH.Mesh(new TH.SphereGeometry(12, 48, 32), mS); mSh.scale.set(1.1, 1.55, .9); mSh.userData.dyn = 1; mSh.visible = false; body.add(mSh);
    const wkS = sprite(8, "rgba(255,255,255,1)", "elwkS"); wkS.visible = false; body.add(wkS);
    const wkR = new TH.Sprite(new TH.SpriteMaterial({ map: radial("elwkR", [[0, "rgba(255,255,255,0)"], [.68, "rgba(255,255,255,0)"], [.76, "rgba(255,255,255,1)"], [.84, "rgba(255,255,255,0)"], [1, "rgba(255,255,255,0)"]]), blending: TH.AdditiveBlending, depthWrite: false, transparent: true, toneMapped: false })); wkR.visible = false; body.add(wkR);
    const nodes = kind === "storm" ? [0, 1, 2].map(() => { const n = sprite(5, `rgba(${E.rgb},1)`, "elnode"); body.add(n); return n; }) : [];""")
rep("      if (bt) bt(t, 1 + (A + B + C) * 6); hit(bell(fx0, 0, .05, .4, 1), t); };\n    bake(body); return { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 16, h: 30, kind }; }",
"""      const Mc = out.mech || { s: 1, k: 0 }, arm = Math.min(1, Math.max(0, (Mc.s - 1) / .8)), open = Mc.s <= 1.001 && Mc.k !== -1;
      mSh.visible = arm > .02; if (mSh.visible) { mS.uniforms.uT.value = t * .001; mS.uniforms.uO.value = arm * (1.1 + .2 * Math.sin(t * .003)) * (1 + B * .3); mSh.rotation.y = t * (kind === "light" ? .0004 : .00012); }
      wkS.visible = wkR.visible = open; if (open) { const p = .5 + .5 * Math.sin(t * .005); wkS.position.copy(core.position); wkR.position.copy(core.position); wkS.material.opacity = .45 + p * .45; wkS.scale.setScalar(9 + p * 4); wkR.material.opacity = 1 - p * .3; wkR.scale.setScalar(17 - p * 5); }
      nodes.forEach((n, i) => { const a = t * .0006 + i * TAU / 3, k = Mc.s > 1 ? arm : 0; n.position.set(Math.cos(a) * 13, Math.sin(a * 1.3 + i) * 6, Math.sin(a) * 5); n.material.opacity = .15 + k * .85; n.scale.setScalar(2.5 + k * 6 + (k > .95 ? rnd() * 3 : 0)); });
      if (bt) bt(t, 1 + (A + B + C) * 6 + (kind === "storm" ? arm * 5 : 0)); hit(bell(fx0, 0, .05, .4, 1), t); };
    bake(body); const out = { grp, tick, act: n => mv.play(n), moves: Object.keys(mv.dur), r: 16, h: 30, kind, mech: null }; return out; }""")
# the map tells each Elemental its state; a battle shows the state it was fought in
rep('if (key === "ovl") M.b.cons = [0, 1, 2, 3].filter(i => st.hp["c" + i] > 0 && wbOn("c" + i, T)).length;',
    'if (key === "ovl") M.b.cons = [0, 1, 2, 3].filter(i => st.hp["c" + i] > 0 && wbOn("c" + i, T)).length; if (WB_EL.includes(key)) M.b.mech = { s: wbShOf(key, st, T), k: 0 };')
rep("WBR.hp = b.hp; if (WBR.b.setHp) WBR.b.setHp(b.hp);", "WBR.hp = b.hp; if (WBR.b.setHp) WBR.b.setHp(b.hp); if (WB_EL.includes(key) && battle && battle.r) WBR.b.mech = { s: battle.r.wbSh || 1, k: 0 };")
# the guide
rep("At every fifth of its hull the Pentarch tears one element loose, and you can aim at a wing to break it sooner.",
    "Each Elemental fights its own way: Voltaris charges storm nodes and then discharges, open for eight minutes in every thirty; Ignaroth's molten armour cracks below 60% hull; Auricor's radiant shield drops for four minutes in every twelve; Gravemorn crushes tight just after each hit, so space your attacks; Viridrax regrows while nobody hits it. A white ring on its heart means its core is exposed. At every fifth of its hull the Pentarch tears one element loose, and you can aim at a wing to break it sooner.")
s = re.sub(r"GAME_V = 475\b", "GAME_V = 476", s)
open(P, 'w').write(s)
