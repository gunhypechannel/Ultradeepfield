# v474 No boss explodes any more (owner: "I don't want any of them explode... each should fade out a different crystal color and leave a
# single glyph behind"). Vaelthar, the Pentarch and every world boss and Elemental now die like Aexion: a soft flash in their colour, then
# they freeze whole in their last pose as clear crystal, the crystal dissolves from the bottom up and spirits rise from it, and a single
# glyph stays. No blast, no flying wreckage. Each boss has its own crystal colour (the Pentarch's is prismatic). Aexion is unchanged.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
# --- the crystal takes each boss's own colours ---
rep("function sbVaeCrystal(W, X, b, e, t, moving) { if (e < .55) return false;",
r"""const SB_CRY = { vae: [[.8, .55, .12], [1, .92, .6]], ovl: [[.55, .2, .95], [.95, .78, 1]], dev: [[.85, .15, .55], [1, .72, .9]], war: [[.16, .06, .4], [.8, .66, 1]],
  brd: [[.42, .8, .08], [.9, 1, .6]], tyr: [[.82, .08, .14], [1, .62, .6]], wym: [[.8, .3, .04], [1, .7, .38]], col: [[.72, .48, .86], [1, .9, 1]],
  eic: [[.42, .05, .62], [.82, .42, 1]], efi: [[.95, .4, .05], [1, .82, .45]], eli: [[.95, .8, .35], [1, 1, .86]], est: [[.05, .38, 1], [.6, .9, 1]], ena: [[.05, .7, .3], [.65, 1, .75]],
  con: [[.6, .4, .95], [.9, .85, 1]], epx: [[.6, .5, .8], [1, .95, 1]] };
const sbCryOf = k => SB_CRY[k] || (k && k[0] === "c" && /^c\d$/.test(k) ? SB_CRY.con : [[.35, .25, .85], [.7, .9, 1]]);
/* v474 the soft flash that covers a boss turning to crystal, in its crystal colour (no blast) */
function sbCryFlash(W, X, b, e) { if (!X.cf) { const bs = new TH.Box3().setFromObject(b.grp).getBoundingSphere(new TH.Sphere()), c = sbCryOf(X.key)[1]; X.cfR = Math.max(10, bs.radius); X.cf = new TH.Sprite(W.additive(W.glow.wh || (W.glow.wh = glowTex("255,255,255", .85)), new TH.Color(c[0], c[1], c[2]), 0)); X.cf.position.copy(bs.center); X.grp.add(X.cf); }
  const a = e < .55 ? Math.max(0, e / .55) : Math.max(0, 1 - (e - .55) / .9); X.cf.visible = a > .01; X.cf.material.opacity = a * .8; X.cf.scale.setScalar(X.cfR * (2.2 + Math.max(0, e) * .8)); }
function sbVaeCrystal(W, X, b, e, t, moving) { if (e < .55) return false;""")
rep("const m = new TH.ShaderMaterial({ uniforms: { uT: { value: 0 }, uD: { value: 0 }, uO: { value: 1 }, uB: { value: 1 }, uY: { value: new TH.Vector2(-40, 120) } },",
    "const CP = sbCryOf(X.key), m = new TH.ShaderMaterial({ uniforms: { uT: { value: 0 }, uD: { value: 0 }, uO: { value: 1 }, uB: { value: 1 }, uY: { value: new TH.Vector2(-40, 120) }, uC1: { value: new TH.Vector3(...CP[0]) }, uC2: { value: new TH.Vector3(...CP[1]) }, uP: { value: X.key === \"epx\" ? 1 : 0 } },")
rep('fragmentShader: "uniform float uT, uD, uO, uB; uniform vec2 uY;', 'fragmentShader: "uniform float uT, uD, uO, uB, uP; uniform vec2 uY; uniform vec3 uC1, uC2;')
rep('vec3 col = mix(vec3(.35, .25, .85), vec3(.7, .9, 1.), fr) + vec3(1., .9, 1.) * (fr2 * .5 + gl) + vec3(.7, .9, 1.) * edge * 1.3 * step(.001, uD);',
    'vec3 c1 = mix(uC1, .5 + .45 * cos(6.2832 * (vW.y * .012 + vW.x * .007 + uT * .08 + vec3(0., .33, .67))), uP); vec3 col = mix(c1, uC2, fr) + vec3(1., .95, 1.) * (fr2 * .5 + gl) + mix(uC2, c1 + .3, uP) * edge * 1.3 * step(.001, uD);')
rep("sz: 7 + r() * 10, c: r() < .5 ? [.75, .9, 1] : r() < .8 ? [.85, .7, 1] : [1, 1, 1] }); }",
    "sz: 7 + r() * 10, c: (u => X.key === \"epx\" && u < .8 ? [.6 + .4 * Math.cos(TAU * u * 1.25), .6 + .4 * Math.cos(TAU * (u * 1.25 + .33)), .6 + .4 * Math.cos(TAU * (u * 1.25 + .67))] : u < .5 ? CP[1] : u < .8 ? CP[0].map((v, i) => (v + CP[1][i]) / 2 + .15) : [1, 1, 1])(r()) }); }")
# --- world bosses: the overload, then crystal; no booms, no blast, no scatter ---
rep("if (e < OV) { const k = e / OV; X.flash.material.opacity = k * .75; X.flash.scale.setScalar((con ? 60 : 220) * sc * (1 - k * .5)); b.over = k; if (Math.random() < .04 + k * .2) sbBoom(X, X.B.clone().add(new TH.Vector3((Math.random() - .5) * 20 * sc, Math.random() * 15 * sc, (Math.random() - .5) * 20 * sc)), t, (20 + k * 50) * sc); }",
    "if (e < OV) { const k = e / OV; X.flash.material.opacity = k * .35; X.flash.scale.setScalar((con ? 60 : 200) * sc * (1 - k * .5)); b.over = k; } else X.flash.visible = false;")
rep("""  const ib = e - OV; sbShatter(X, b, ib); if (!con) sbBlast(W, X, ib, t); else { X.flash.material.opacity = Math.max(0, 1 - ib / .6) * (ib >= 0 ? 1 : X.flash.material.opacity); for (const Bm of X.booms) { const a = (t - Bm.t) / 900; Bm.s.visible = a >= 0 && a < 1; if (Bm.s.visible) { Bm.s.material.opacity = (1 - a) * .95; Bm.s.scale.setScalar(Bm.sz * (.4 + a * 1.4)); } } }
  sbVaeCrystal(W, X, b, ib - 1.2, t, 1); if (!con) { X.glySeed = X.glySeed || Math.round(q.x * 7 + q.z * 13 + Math.floor(now() / 864e5)); sbGlyph(W, X, ib - 9.5, t); } return ib >= 0; }""",
"""  const ib = e - OV; if (ib > -.6) sbCryFlash(W, X, b, ib + .6); if (ib >= 0) b.over = 0;
  sbVaeCrystal(W, X, b, ib + .55, t, 1); if (!con) { X.glySeed = X.glySeed || Math.round(q.x * 7 + q.z * 13 + Math.floor(now() / 864e5)); sbGlyph(W, X, ib - 6.2, t); } return ib >= 0; }""")
# --- the Pentarch: it sheds its elements, then the crystal ---
rep("  sbShatter(X, b, ib); sbBlast(W, X, ib, t); sbVaeCrystal(W, X, b, ib - 1.2, t, 1); sbGlyph(W, X, ib - 9.5, t); return ib >= 0; }",
    "  if (ib >= 0) X.flash.visible = false; if (ib > -.6) sbCryFlash(W, X, b, ib + .6); sbVaeCrystal(W, X, b, ib + .55, t, 1); sbGlyph(W, X, ib - 6.2, t); return ib >= 0; }")
rep("X.flash.material.opacity = (e - 2.1) / .6 * .7; X.flash.scale.setScalar(300 * sc * (1 - (e - 2.1) / .6 * .6)); } /* the core draws in on itself */",
    "X.flash.material.opacity = (e - 2.1) / .6 * .35; X.flash.scale.setScalar(260 * sc * (1 - (e - 2.1) / .6 * .6)); } /* the core draws in on itself */")
# --- Vaelthar, in the event and on the map ---
rep("let vf = -1; if (P.key === \"vae\" && X.fall) { vf = s - X.fall - .8; sbShatter(X, b, vf); sbBlast(W, X, vf, t); sbVaeCrystal(W, X, b, vf - 1.2, t, 1); } if (!(vf >= 0)) b.tick(t);",
    "let vf = -1; if (P.key === \"vae\" && X.fall) { vf = s - X.fall - .8; if (vf > -.6) sbCryFlash(W, X, b, vf + .6); sbVaeCrystal(W, X, b, vf + .55, t, 1); } if (!(vf >= 0)) b.tick(t);")
rep("let vf = -1; if (k === \"vae\" && dead) { vf = df - .8; X.glySeed = st.dead; sbGlyph(W, X, df - 8.6, t); sbShatter(X, b, vf); sbBlast(W, X, vf, t); sbVaeCrystal(W, X, b, vf - 1.2, t, 1); } if (!(vf >= 0)) b.tick(t);",
    "let vf = -1; if (k === \"vae\" && dead) { vf = df - .8; X.glySeed = st.dead; sbGlyph(W, X, vf - 6.2, t); if (vf > -.6) sbCryFlash(W, X, b, vf + .6); sbVaeCrystal(W, X, b, vf + .55, t, 1); } if (!(vf >= 0)) b.tick(t);")
s = re.sub(r"GAME_V = 473\b", "GAME_V = 474", s)
open(P, 'w').write(s)
# --- the super bosses' battle replays: the hull bar asked WB for Vaelthar's and Aexion's colour and every frame failed, so the battle
# showed nothing; it takes their own colour now ---
s = open(P).read()
rep('ctx.fillStyle = wbk ? WB[wbk].col : "#5dff6a";', 'ctx.fillStyle = wbk ? (WB[wbk] || SBW[wbk] || { col: "#c890ff" }).col : "#5dff6a";')
open(P, 'w').write(s)
