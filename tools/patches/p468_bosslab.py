# v468 the owner's Boss Lab (owner: "all of their previews should be available to me as well as their battle reports so I can perfect all
# of them"): one sheet with the whole Wednesday rotation (dates, live/next), a preview for every boss (the four great events play their
# replays; every world boss can be called onto the map on this device with the camera on it), and the battle tests, which now cover the
# super bosses (Vaelthar, Aexion in both forms) and the Omega Cube as well as every world boss, each with a playable battle report.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
# a world boss shown on the map for the owner only
rep("const wbPrev = k => G.elePrev && WB[k] && WB[k].g >= 2 ? ", "const wbPrev = k => G.wbShow && WB[k] ? (G.wbShow === k || (G.wbShow === \"ovl\" && WB[k].con != null)) : G.elePrev && WB[k] && WB[k].g >= 2 ? ")
# battle tests: super bosses and the Omega Cube too
rep('for (const L of [["ice", "fire", "light", "storm", "nature"], ["ice", "fire", "light"], ["fire"], []]) add("epx", `${L.length} of 5 elements`, .25 + .15 * L.length, WB_SEG, L);',
    'for (const L of [["ice", "fire", "light", "storm", "nature"], ["ice", "fire", "light"], ["fire"], []]) add("epx", `${L.length} of 5 elements`, .25 + .15 * L.length, WB_SEG, L);\n  C.push({ key: "vae", t: "sb", form: "full hull", sh: 1, n0: 100 }, { key: "vae", t: "sb", form: "last quarter", sh: 1, n0: 25 }, { key: "aex", t: "sb", form: "dreadnought", sh: 1, n0: 100, sbForm: 0 }, { key: "aex", t: "sb", form: "Warform", sh: 1, n0: 55, sbForm: 1 }, { key: "omg", t: "om", form: "", sh: 1, n0: OM_SEG });')
rep("for (const c of C) { await sleep(40); const D = WB[c.key]; let r = { c, ok: false };", "for (const c of C) { await sleep(40); const D = c.t === \"sb\" ? { n: SBW[c.key].n, k: SBW[c.key].u } : c.t === \"om\" ? { n: \"Omega Cube\", k: \"wbOmg\" } : WB[c.key]; let r = { c, ok: false };")
rep('const rep = mkRep({ at: now(), kind: "attack", test: 1, title: `Stress test · ${D.n}${c.form ? ` (${c.form})` : ""}`, aUids: [G.me], aName: S.homeName + " Fleet", dName: D.n, wb: c.key, wbSh: c.sh,',
    'const rep = mkRep({ at: now(), kind: "attack", test: 1, title: `Stress test · ${D.n}${c.form ? ` (${c.form})` : ""}`, aUids: [G.me], aName: S.homeName + " Fleet", dName: D.n, ...(c.t === "sb" ? { sbk: c.key, sbForm: c.sbForm || 0, sbSeg: [c.n0, left], sbT: "core" } : c.t === "om" ? { omega: 1, omSeg: [c.n0, left] } : { wb: c.key }), wbSh: c.sh,')
rep('const rows = out.map((r, i) => { const D = WB[r.c.key], pct = r.rep ? Math.round((r.c.n0 - r.left) / WB_SEG * 100) : 0;',
    'const rows = out.map((r, i) => { const D = r.c.t === "sb" ? { ic: "✦", n: SBW[r.c.key].n } : r.c.t === "om" ? { ic: "◼", n: "Omega Cube" } : WB[r.c.key], pct = r.rep ? Math.round((r.c.n0 - r.left) / (r.c.t ? r.c.n0 : WB_SEG) * 100) : 0;')
# the Boss Lab sheet
rep("stressOpen: () => { if (!duelOwner()) return; openSheet({ type: \"stress\" }); },",
"""stressOpen: () => { if (!duelOwner()) return; openSheet({ type: "stress" }); },
  labOpen: () => { if (!duelOwner()) return; openSheet({ type: "bosslab" }); },
  labPrev: d => { if (!duelOwner()) return; const k = d.k; if (k === "vae" || k === "aex") return sbSimStart(k); if (k === "dv") return dvSimStart(); if (k === "conv") return convSimStart();
    G.wbShow = k; WBN = null; clearTimeout(G.wbShowT); G.wbShowT = setTimeout(() => { G.wbShow = null; WBN = null; }, 5 * 60e3); toast(`Owner preview: ${WB[k].n} is on the map for 5 minutes, on this device only.`); setTimeout(() => { try { cineObjStart("wb_" + k); } catch (e) {} }, 1200); },
  labStop: () => { G.wbShow = null; WBN = null; if (sheet) renderSheet(); },""")
rep("stress: shStress,", "stress: shStress, bosslab: shBossLab,")
rep("function shStress() {", """function shBossLab() { const T = now(), w0 = Math.max(0, rotW(T)), NM = { vae: ["✦", "Vaelthar, the Celestial Ruin"], aex: ["✦", "Aexion, the Warform Sovereign"], dv: ["◼", "Cube Devastation (Omega Cube)"], conv: ["✪", "The Elemental Convergence"] };
  const nm = k => NM[k] || [WB[k].ic, WB[k].n], live = k => k === "vae" || k === "aex" ? sbLiveKey(T) === k : k === "dv" ? !!dvNow(T) : k === "conv" ? wbGroupOn(3, T) : wbOn(k, T) && !G.wbShow;
  const rows = ROT.map((k, i) => { let w = w0; while (rotKey(w) !== k) w++; const at = ROT0 + w * WEEK, [ic, n] = nm(k);
    return `<div class="strow"><div style="flex:1;min-width:0"><b>${ic} ${esc(n)}</b><div class="note">${live(k) ? "<b style=\\"color:#7dff9a\\">● live now</b>" : `${new Date(at).toLocaleDateString([], { weekday: "short", month: "short", day: "numeric" })}, ${new Date(at).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })} · in ${ftime(at - T)}`}</div></div><button class="btn ghost" data-act="labPrev" data-k="${k}">▶ Preview</button></div>`; }).join("");
  return `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter">Owner</div><h2>Boss Lab</h2><p class="note">The Wednesday boss rotation, one boss a week at 18:00 UTC, each back every ${ROT.length} weeks. Preview any of them on this device only; nothing is saved or shared.</p></div><div class="fhdb"><button class="x" data-act="close" aria-label="Close">✕</button></div></div>
    ${G.wbShow ? `<button class="btn wide" data-act="labStop">■ Stop the ${esc(WB[G.wbShow].n)} preview</button>` : ""}<button class="btn ghost wide" data-act="stressOpen">⚔ Battle tests and reports (every boss)</button><div class="strows">${rows}</div>`; }
function shStress() {""")
rep('data-act="stressOpen">⚔ Stress-test battles</button>', 'data-act="labOpen">📅 Boss Lab: the rotation, previews and battle reports</button><button class="btn ghost wide" data-act="stressOpen">⚔ Stress-test battles</button>')
s = re.sub(r"GAME_V = 467\b", "GAME_V = 468", s)
open(P, 'w').write(s)
