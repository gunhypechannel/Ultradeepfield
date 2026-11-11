# v451 the Ultimate Super Boss events (p451_sbevent.js): Vaelthar on the 25th, Aexion on the 5th; fleets, reports, panel, live record, map
import re, os
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
js = open(os.path.join(os.path.dirname(__file__), 'p451_sbevent.js')).read()
rep("/* v408 tapping the Super Cube */", js + "/* v408 tapping the Super Cube */")
# the preview builder can skip its fleet (the live boss has none), and the preview hands over to the live boss
rep("function sbBuild(W, key) {", "function sbBuild(W, key, noFleet) {")
rep("  if (K) SBX_FT.forEach(", "  if (K && !noFleet) SBX_FT.forEach(")
rep("const P = G.sbSim; if (!P) { if (W.sb) sbFree(W); return; } const D = SBX[P.key]; if (W.sb && W.sb.key !== P.key) sbFree(W);", "const P = G.sbSim; if (!P) { sbLiveTick(W, t); return; } const D = SBX[P.key]; if (W.sb && (W.sb.key !== P.key || W.sb.live)) sbFree(W);")
# fleets: the target, arrival, the fight
rep("f.wb ? WBO[f.wb] : f.om ? OMO :", "f.wb ? WBO[f.wb] : f.om ? OMO : f.sb ? SBO[f.sb] :")
rep('id === "omega" ? OMO : null', 'id === "omega" ? OMO : id && String(id).startsWith("sb_") ? SBO[String(id).slice(3)] || null : null')
rep('f.wb || f.om ? (f.phase = "resolving")', 'f.wb || f.om || f.sb ? (f.phase = "resolving")')
rep("else if (f.om) omResolve(f);", "else if (f.om) omResolve(f); else if (f.sb) sbResolve(f);")
# battle reports: the super boss fights as one, drawn as its own live 3D model (Aexion in the form it had then)
rep('battle.superSide = r.omega ? "d" :', 'battle.superSide = r.sbk || r.omega ? "d" :')
rep('const superSideOf = r => r ? (r.omega ? "d" :', 'const superSideOf = r => r ? (r.sbk || r.omega ? "d" :')
rep('const scName = r => r && r.omega ? "Omega Cube" :', 'const scName = r => r && r.sbk && SBW[r.sbk] ? SBW[r.sbk].n : r && r.omega ? "Omega Cube" :')
rep('r.wb ? `${WB[r.wb] ? WB[r.wb].n : r.dName} · World boss`', 'r.sbk && SBW[r.sbk] ? `${SBW[r.sbk].n} · Ultimate super boss` : r.wb ? `${WB[r.wb] ? WB[r.wb].n : r.dName} · World boss`')
rep("const wbk = b.r.wb, art", "const wbk = b.r.wb || b.r.sbk, art"); rep("Math.max(1, wbk ? WB_SEG :", "Math.max(1, b.r.wb ? WB_SEG :")
rep('if (typeof BOSS3D === "undefined" || !WB[key]) return null;', 'if (typeof BOSS3D === "undefined" || !(WB[key] || (typeof SBW !== "undefined" && SBW[key]))) return null;')
rep("const m3 = WB[key].m3", "const m3 = (WB[key] || SBW[key]).m3"); rep("BOSS3D[m3](WB[key].el ||", "BOSS3D[m3]((WB[key] || {}).el ||")
rep("    WBR.b.tick(t); if (WBR.b.lens", "    if (!WB[key] && WBR.b.drive) WBR.b.drive(\"transform\", battle && battle.r && battle.r.sbForm ? 1 : 0); /* v451 */\n    WBR.b.tick(t); if (WBR.b.lens")
rep("const wbMoves = key => WB_ATK[key] || WB_ATK.c0;", "const wbMoves = key => typeof SBW !== \"undefined\" && SBW[key] ? (SBW[key].mv2 && battle && battle.r && battle.r.sbForm ? SBW[key].mv2 : SBW[key].mv) : WB_ATK[key] || WB_ATK.c0;")
rep("const WB_FRONT = { elemental: 0,", "const WB_FRONT = { vaelthar: 0, aexion: 0, elemental: 0,")
rep("const WB_VIEW = { elemental:", "const WB_VIEW = { vaelthar: [-.35, [-30, 10, 74], [0, 8, 0]], aexion: [-.4, [-26, 2, 64], [0, -2, 0]], elemental:")
# the panel, the actions, the live record
rep("wboss: shWboss, omega: shOmega,", "wboss: shWboss, omega: shOmega, sboss: shSboss,")
rep("  omOpen: () => {", """  sbOpen: d => { const k = d.id; if (!SBW[k]) return; pick = {}; for (const q in S.ships) if (S.ships[q] && SH[q]) pick[q] = S.ships[q]; if (view !== "galaxy") { view = "galaxy"; render(); } const p = SBX[k].p; if (G3) { G3.cam.followFleet = null; G3.cam.follow = null; G3.cam.goal = { tx: p[0], ty: p[1] + 30, tz: p[2], dist: 640 }; } openSheet({ type: "sboss", id: k }); }, /* v451 */
  sbTgt: d => { const [k, id] = String(d.id).split(":"); S.sbTgt = S.sbTgt || {}; S.sbTgt[k] = id; renderSheet(); },
  sbGo: d => act(() => { const k = d.id; if (!canPlay() || !SBW[k]) return; if (!sbOn(k)) return toast(`${SBW[k].n} can't be attacked right now.`, "warn"); if (S.fleets.some(f => f.sb === k && f.phase === "out")) return toast("A fleet is already on its way there.", "warn"); if (slotsFull()) return;
    const n = takeShips(pick); if (!Object.keys(n).length) return; const f = sendFleet(SBO[k], n, "attack", { sb: k, sbT: (S.sbTgt && S.sbTgt[k]) || "core" }); if (!f) return; closeSheet(); toast(`Fleet launched at ${SBW[k].n}. Arrival in ${ftime(f.tt)}.`); }),
  omOpen: () => {""")
rep('db.doc("event/omega").onSnapshot(s => { G.om = s.exists ? s.data() : null; OMN = null; omClaim(); softRender(); }, () => {});',
    'db.doc("event/omega").onSnapshot(s => { G.om = s.exists ? s.data() : null; OMN = null; omClaim(); softRender(); }, () => {});\n    for (const k of ["vae", "aex"]) db.doc("event/sb_" + k).onSnapshot(s => { G.sb[k] = s.exists ? s.data() : null; SBN[k] = null; sbClaim(); softRender(); }, () => {}); /* v451 the super bosses */')
rep("#omband{position:absolute;", "#sbband{position:absolute;left:50%;transform:translateX(-50%);top:calc(var(--hudH,150px) + 8px);z-index:24}.sbb{display:flex;align-items:center;gap:10px;padding:8px 14px;border-radius:14px;border:1px solid var(--c);background:rgba(10,8,22,.9);color:#eee6ff;font-family:var(--f-display);font-size:13px;white-space:nowrap;cursor:pointer;box-shadow:0 0 18px color-mix(in srgb,var(--c) 45%,transparent)}.sbb b{color:var(--c);letter-spacing:.06em}.sbb span{opacity:.85}.sbb i{font-style:normal;color:#ffd27a}.sbb.soon{opacity:.92}"
    ".sbart{position:relative;flex:none;height:min(62vw,320px);margin:4px 0 10px;border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,.12);background:#0a0814}.sbart img{width:100%;height:100%;object-fit:cover;object-position:center 35%;display:block}.sbph{position:absolute;left:10px;bottom:8px;padding:3px 9px;border-radius:9px;background:rgba(0,0,0,.6);font-family:var(--f-display);font-size:12px;letter-spacing:.06em}"
    ".sbtg{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,9.5em),1fr));gap:6px;margin:4px 0 8px}.sbt{display:flex;flex-direction:column;align-items:flex-start;gap:2px;padding:8px 10px;border-radius:10px;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.04);color:inherit;text-align:left;cursor:pointer}.sbt.on{border-color:#ffd27a;background:rgba(255,210,122,.12)}.sbt:disabled{opacity:.4}.sbt small{opacity:.7;font-size:11px}.sbwhy{color:#ffd27a}"
    ".sbpip{display:inline-block;width:9px;height:9px;border-radius:50%;background:#c890ff;box-shadow:0 0 6px #c890ff;margin-right:3px;vertical-align:middle}.sbpip.off{background:#2a2433;box-shadow:none}.sbab{list-style:none;padding:0;margin:4px 0 10px;display:grid;gap:6px}.sbab li{display:flex;flex-direction:column;gap:1px}.sbab b{font-size:13px}.sbab span{opacity:.75;font-size:12px}"
    ".sbmats{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,10em),1fr));gap:6px}.sbmat{display:grid;grid-template-columns:auto auto;grid-template-rows:auto auto;column-gap:7px;align-items:center;padding:6px 8px;border-radius:10px;background:rgba(255,255,255,.04)}.sbmat .sbmi{grid-row:1/3}.sbmat small{opacity:.7;font-size:11px;grid-column:2}\n#omband{position:absolute;")
s = re.sub(r"GAME_V = 450\b", "GAME_V = 451", s)
open(P, 'w').write(s)
