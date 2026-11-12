# v463 the Pentarch's death, its own version of Aexion's (owner: "even the pentarch should have a similar unique death animation"): its
# five elements tear loose one by one, each in a burst of its own colour; then the core detonates in a prismatic blast across the map, every
# part of it is flung out and tumbling, turns to crystal and dissolves into rising spirits, and a holo glyph crackling with all five
# elements stays where it died. Timed from the record's moment of death, so everyone sees it together; then the model is rebuilt fresh.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
JS = r'''function wbPentDie(W, M, q, e, t) { const b = M.b, ELC = { fire: "#ff7a30", ice: "#8fe0ff", light: "#fff0a0", storm: "#c890ff", nature: "#7dff8a" };
  if (!M.pd) { const X = { key: "epx", grp: new TH.Group(), B: new TH.Vector3(q.x, q.y, q.z), V: new TH.Vector3(), V2: new TH.Vector3(), ships: [], b, F: new TH.Vector3(0, 0, 1) }; W.scene.add(X.grp);
    const wh = W.glow.wh || (W.glow.wh = glowTex("255,255,255", .85)); X.flash = new TH.Sprite(W.additive(wh, new TH.Color("#e2d4ff"), 0)); X.flash.position.copy(X.B); X.grp.add(X.flash);
    X.booms = []; for (let i = 0; i < (MOBILE ? 16 : 30); i++) { const s = new TH.Sprite(W.additive(W.glow.fire || (W.glow.fire = glowTex("255,190,120", .8)), 0xffd0a0, 0)); s.visible = false; X.grp.add(s); X.booms.push({ s, t: -1e9, sz: 30 }); } X.bi = 0;
    X.els = (b.alive && b.alive.length ? b.alive : ["ice", "fire", "light", "storm", "nature"]).slice(); X.ef = X.els.map(el => { const s = new TH.Sprite(W.additive(wh, new TH.Color(ELC[el] || "#ffffff"), 0)); X.grp.add(s); return s; }); M.pd = X; }
  const X = M.pd, sc = b.grp.scale.x;
  X.els.forEach((el, i) => { const a = e - (.3 + i * .45); if (a >= 0 && !X["s" + i]) { X["s" + i] = 1; try { b.shed(el); } catch (er) {} } const s = X.ef[i], an = i / X.els.length * TAU; s.position.set(X.B.x + Math.cos(an) * 22 * sc, X.B.y + 30 * sc, X.B.z + Math.sin(an) * 22 * sc); s.material.opacity = a > 0 && a < 1.4 ? Math.min(1, (1 - a / 1.4) * 1.3) : 0; s.scale.setScalar((110 + Math.max(0, a) * 520) * sc); });
  const ib = e - 2.7; if (ib < 0 && e > 2.1) { X.flash.material.opacity = (e - 2.1) / .6 * .7; X.flash.scale.setScalar(300 * sc * (1 - (e - 2.1) / .6 * .6)); } /* the core draws in on itself */
  sbShatter(X, b, ib); sbBlast(W, X, ib, t); sbVaeCrystal(W, X, b, ib - 1.2, t, 1); sbGlyph(W, X, ib - 9.5, t); return ib >= 0; }
'''
rep("function sbBoomTick(X, t) {", JS + "function sbBoomTick(X, t) {")
rep("const vae = X.key === \"vae\", r1 = mk(.03, vae ? 0xffe2a0 : 0xcfeeff), r2 = mk(.09, vae ? 0xa45cff : 0x58b8ff), r3 = mk(.025, 0xffffff), sh = new TH.Mesh(new TH.SphereGeometry(1, 40, 24), dvRim(vae ? 0xc890ff : 0x7ac8ff));",
    "const vae = X.key === \"vae\", px = X.key === \"epx\", r1 = mk(.03, px ? 0xfff0c0 : vae ? 0xffe2a0 : 0xcfeeff), r2 = mk(.09, px ? 0x7dffb0 : vae ? 0xa45cff : 0x58b8ff), r3 = mk(.025, px ? 0xff9a50 : 0xffffff), sh = new TH.Mesh(new TH.SphereGeometry(1, 40, 24), dvRim(px ? 0xe2d4ff : vae ? 0xc890ff : 0x7ac8ff));")
rep("const tex = new TH.CanvasTexture(cv), vae = X.key === \"vae\", C1 = vae ? 0xc890ff : 0x7ac8ff, C2 = vae ? 0xffd890 : 0xd0f0ff,",
    "const tex = new TH.CanvasTexture(cv), vae = X.key === \"vae\", px = X.key === \"epx\", C1 = px ? 0xe2d4ff : vae ? 0xc890ff : 0x7ac8ff, C2 = px ? 0xfff0c0 : vae ? 0xffd890 : 0xd0f0ff,")
# the map: the Pentarch stays on screen through its death, its live effects stop, and afterwards it is rebuilt fresh for the next Convergence
rep("alive = st.hp[key] > 0 && wbOn(key, T) && !(key === \"epx\" && wbSwept(T)), q = P3(WBO[key], T, WBQ), d = Math.hypot(q.x - cp.x, q.y - cp.y, q.z - cp.z), near = alive && d < 1400; let M = W.wbM[key];",
    "alive = st.hp[key] > 0 && wbOn(key, T) && !(key === \"epx\" && wbSwept(T)), pdie = key === \"epx\" && st.dead && st.dead.epx && T >= st.dead.epx && T - st.dead.epx < 26000 && stCyc(st, \"epx\") === wbCyc2(T), q = P3(WBO[key], T, WBQ), d = Math.hypot(q.x - cp.x, q.y - cp.y, q.z - cp.z), near = (alive || pdie) && d < 1400; let M = W.wbM[key];\n    if (M && M.pd && !pdie) { try { W.scene.remove(M.b.grp); W.scene.remove(M.pd.grp); } catch (e) {} delete W.wbM[key]; continue; }")
rep("if (t > M.next) { M.next = t + 9000 + Math.random() * 10000;", "if (t > M.next && !pdie) { M.next = t + 9000 + Math.random() * 10000;")
rep("if (key === \"epx\") wbPentFx(M, g, q, st, T, t);", "if (key === \"epx\" && !pdie) wbPentFx(M, g, q, st, T, t);")
rep("M.b.tick(t); }\n  try { wbScanFx(W, t);", "if (!(pdie && wbPentDie(W, M, q, (T - st.dead.epx) / 1000, t))) M.b.tick(t); }\n  try { wbScanFx(W, t);")
s = re.sub(r"GAME_V = 462\b", "GAME_V = 463", s)
open(P, 'w').write(s)
