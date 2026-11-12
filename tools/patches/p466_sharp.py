# v466 (1) one glyph, not three: a fallen boss leaves a single holo glyph of one random element, its own random design, crackling with that
# element's lightning (owner: "when the boss dies they should only leave behind a single random glyph"); (2) sharper map graphics on strong
# phones (owner: "do we have to settle for such low resolution in map view?"): their render resolution was capped at 2x even on 2.8x and 3x
# screens; strong phones now draw up to their screen's own resolution, inside a larger pixel budget, still dropped by adaptive resolution
# when frames slow and still lowered after any graphics reset; the perf log now records the resolution actually drawn.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
i = s.index("function sbGlyph(W, X, e, t) {"); j = s.index("function wbPentDie(", i)
s = s[:i] + r'''function sbGlyph(W, X, e, t) { if (e < 0) { if (X.gly) X.gly.g.visible = false; return; }
  if (!X.gly) { const seed = X.glySeed || (X.glySeed = (Math.random() * 1e9) | 0), r = cwRnd(hash(X.key + "glyph" + seed)), ELS = [["fire", "#ff8a3a", [1, .5, .15]], ["frost", "#8fe0ff", [.55, .9, 1]], ["storm", "#fff07a", [1, 1, .45]], ["void", "#c890ff", [.8, .45, 1]], ["life", "#7dff8a", [.45, 1, .55]]], EL = ELS[(r() * 5) | 0];
    const cv = document.createElement("canvas"); cv.width = cv.height = 512; const c = cv.getContext("2d"); c.translate(256, 256); c.strokeStyle = "#fff"; c.fillStyle = "#fff"; c.lineCap = c.lineJoin = "round";
    const ring = (R, w) => { c.lineWidth = w; c.beginPath(); c.arc(0, 0, R, 0, TAU); c.stroke(); }; ring(244, 6); if (r() < .7) ring(226, 2); const R2 = 150 + r() * 40; ring(R2, 3 + r() * 2); if (r() < .6) ring(R2 - 14, 1.5);
    const tk = [24, 36, 48, 60, 72][(r() * 5) | 0]; for (let k = 0; k < tk; k++) { const a = k / tk * TAU, l = k % 4 ? 8 : 18; c.lineWidth = k % 4 ? 1.5 : 3; c.beginPath(); c.moveTo(Math.cos(a) * 226, Math.sin(a) * 226); c.lineTo(Math.cos(a) * (226 - l), Math.sin(a) * (226 - l)); c.stroke(); }
    const nr = 5 + ((r() * 8) | 0); for (let k = 0; k < nr; k++) { c.save(); c.rotate(k / nr * TAU); c.translate(0, -(R2 + 226) / 2 - 4); c.lineWidth = 3; c.beginPath(); for (let q = 0; q < 3 + ((r() * 3) | 0); q++) { c.moveTo((r() - .5) * 26, (r() - .5) * 30); c.lineTo((r() - .5) * 26, (r() - .5) * 30); } c.stroke(); c.restore(); }
    const n = 5 + ((r() * 5) | 0), m = Math.max(2, Math.floor(n / 2) - ((r() * 2) | 0)); c.lineWidth = 4; c.beginPath(); for (let k = 0; k <= n; k++) { const a = k * m / n * TAU - Math.PI / 2, x = Math.cos(a) * (R2 - 18), y = Math.sin(a) * (R2 - 18); k ? c.lineTo(x, y) : c.moveTo(x, y); } c.stroke();
    const core = (r() * 4) | 0; c.lineWidth = 4; c.beginPath(); if (core === 0) c.arc(0, 0, 28, 0, TAU); else if (core === 1) { c.moveTo(0, -42); c.lineTo(36, 22); c.lineTo(-36, 22); c.closePath(); } else if (core === 2) { c.ellipse(0, 0, 50, 22, 0, 0, TAU); c.moveTo(14, 0); c.arc(0, 0, 14, 0, TAU); } else { c.rect(-26, -26, 52, 52); } c.stroke(); c.beginPath(); c.arc(0, 0, 9, 0, TAU); c.fill();
    const tex = new TH.CanvasTexture(cv), col = new TH.Color(EL[1]), g = new TH.Group(); g.position.copy(X.B).add(new TH.Vector3(0, 45, 0)); X.grp.add(g);
    const Cc = new TH.Mesh(new TH.PlaneGeometry(170, 170), new TH.MeshBasicMaterial({ map: tex, color: col, transparent: true, opacity: 1, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false })); Cc.frustumCulled = false; g.add(Cc);
    const NA = 12, SEG = 7, lg = new TH.BufferGeometry(); lg.setAttribute("position", new TH.BufferAttribute(new Float32Array(NA * SEG * 6), 3)); lg.setAttribute("color", new TH.BufferAttribute(new Float32Array(NA * SEG * 6), 3));
    const arcs = new TH.LineSegments(lg, new TH.LineBasicMaterial({ vertexColors: true, transparent: true, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); arcs.frustumCulled = false; g.add(arcs);
    const glow = new TH.Sprite(W.additive(W.glow.wh || (W.glow.wh = glowTex("255,255,255", .85)), col, .5)); glow.scale.setScalar(330); g.add(glow);
    X.gly = { g, Cc, arcs, glow, NA, SEG, lt: 0, ec: EL[2], el: EL[0] }; }
  const Z = X.gly, k = Math.min(1, e / 1.4), pk = 1 - Math.pow(1 - k, 3); Z.g.visible = true; Z.g.scale.setScalar(.2 + pk * .8);
  if (W.camera) Z.Cc.quaternion.copy(W.camera.quaternion); Z.Cc.rotateZ(-t * .0004); Z.arcs.quaternion.copy(Z.Cc.quaternion);
  const fl = .85 + .15 * Math.sin(t * .013) * Math.sin(t * .0031); Z.Cc.material.opacity = k * fl; Z.glow.material.opacity = .35 * k * (.8 + .2 * Math.sin(t * .004)); Z.g.position.y = X.B.y + 45 + Math.sin(t * .0007) * 5;
  if (t - Z.lt > 70) { Z.lt = t; const P = Z.arcs.geometry.attributes.position.array, Cl = Z.arcs.geometry.attributes.color.array, cc = Z.ec;
    for (let i = 0; i < Z.NA; i++) { const on = Math.random() < .75, a = Math.random() * TAU, r0 = 30 + Math.random() * 25, r1 = 85 + Math.random() * 55; let px = 0, py = 0;
      for (let j = 0; j < Z.SEG; j++) { const u0 = j / Z.SEG, u1 = (j + 1) / Z.SEG, R0 = r0 + (r1 - r0) * u0, R1 = r0 + (r1 - r0) * u1, jit = 12 * (1 - u1 * .5), o = (i * Z.SEG + j) * 6;
        const x0 = j ? px : Math.cos(a) * R0, y0 = j ? py : Math.sin(a) * R0; px = Math.cos(a) * R1 + (Math.random() - .5) * jit; py = Math.sin(a) * R1 + (Math.random() - .5) * jit;
        P.set(on ? [x0, y0, 1, px, py, 1] : [0, 0, 0, 0, 0, 0], o); const f = k * (1 - u0 * .6); Cl.set([cc[0] * f, cc[1] * f, cc[2] * f, cc[0] * f * .8, cc[1] * f * .8, cc[2] * f * .8], o); } }
    Z.arcs.geometry.attributes.position.needsUpdate = true; Z.arcs.geometry.attributes.color.needsUpdate = true; } }
''' + s[j:]
# live: the same glyph for everyone (seeded by the moment it died)
rep("let vf = -1; if (k === \"vae\" && dead) { vf = df - .8; sbGlyph(W, X, df - 8.6, t);", "let vf = -1; if (k === \"vae\" && dead) { vf = df - .8; X.glySeed = st.dead; sbGlyph(W, X, df - 8.6, t);")
rep("if (dead) { const be = df - 2; sbGlyph(W, X, be - 10.5, t);", "if (dead) { const be = df - 2; X.glySeed = st.dead; sbGlyph(W, X, be - 10.5, t);")
rep("const X = M.pd, sc = b.grp.scale.x;", "const X = M.pd, sc = b.grp.scale.x; X.glySeed = X.glySeed || Math.round(q.x * 7 + q.z * 13 + Math.floor(now() / 864e5));")
# sharper on strong phones
rep("const mobilePRCap = () => { if (!MOBILE) return 9; const px = Math.max(1, innerWidth * innerHeight); return clamp(Math.sqrt((WEAK ? 2e6 : G.glSafe ? 1.4e6 : 3.4e6) / px), 1, 2 * FZ()); };",
    "const STRONG = () => MOBILE && !WEAK && !G.glSafe && (navigator.deviceMemory || 8) >= 6 && (navigator.hardwareConcurrency || 8) >= 8; /* v466 */\nconst mobilePRCap = () => { if (!MOBILE) return 9; const px = Math.max(1, innerWidth * innerHeight), st = STRONG(); return clamp(Math.sqrt((WEAK ? 2e6 : G.glSafe ? 1.4e6 : st ? 4.6e6 : 3.4e6) / px), 1, (st ? Math.min(window.devicePixelRatio || 2, IOS ? 2.5 : 3) : 2) * FZ()); };")
rep("PF.errs = [...ERR_SEEN]; PF.gpu = gfxGpu(); PF.preset = gfxPreset(); PF.hz = gfxHz();", "PF.errs = [...ERR_SEEN]; PF.gpu = gfxGpu(); PF.preset = gfxPreset(); PF.hz = gfxHz(); try { if (G3 && G3.renderer) PF.pr = +G3.renderer.getPixelRatio().toFixed(2); } catch (e) {}")
rep('dpr: devicePixelRatio, gpu: P.gpu || "", preset: P.preset || "", hz: P.hz || 0,', 'dpr: devicePixelRatio, pr: P.pr || 0, gpu: P.gpu || "", preset: P.preset || "", hz: P.hz || 0,')
s = re.sub(r"GAME_V = 465\b", "GAME_V = 466", s)
open(P, 'w').write(s)
