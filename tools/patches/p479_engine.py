# v479 Remaster step 7, the shared event engine.
# One camera director: camAuto() decides, for every live event, whether the camera may take itself over (never while you are touching
# it, in a panel or a battle, or when you have turned cinematics off). A new Graphics setting, Cinematic camera On/Off, turns every
# automatic event camera off; owner previews still play their films.
# Named event stages: evNow(T) names the live event and its stage (Vaelthar "Wheel Awakening", Cube Devastation "Migration", the
# Convergence "Fusion", a world boss and its hull...), shown in Boss Lab.
# Per-event metrics: every frame drawn while an event is live is counted against "event:stage" (frames, time, slow frames, freezes)
# with the attacks sent at it, kept with the session's performance record and sent with it (ev).
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
# --- the camera director ---
rep("function sbVaeCine(X, W, fa, dt) { const c = W.cam; if (!c) return; const want = fa >= .56 && fa < .93 && view === \"galaxy\" && !sheet && !(typeof battle !== \"undefined\" && battle) && performance.now() - (G.camTouch || 0) > 5000;",
r"""/* v479 the camera director: may an event take the camera right now? Not while it is being touched (5 s), in a panel or a battle, off
   the galaxy, or with Cinematic camera turned off in Graphics */
function camAuto() { return !GFX.noCine && view === "galaxy" && !sheet && !(typeof battle !== "undefined" && battle) && performance.now() - (G.camTouch || 0) > 5000; }
function sbVaeCine(X, W, fa, dt) { const c = W.cam; if (!c) return; const want = fa >= .56 && fa < .93 && camAuto();""")
rep('<button class="btn ${GFX.showFps ? "amber" : "ghost"}" data-act="gfxFps">${GFX.showFps ? "Hide" : "Show"} FPS counter</button></div>',
    '<button class="btn ${GFX.showFps ? "amber" : "ghost"}" data-act="gfxFps">${GFX.showFps ? "Hide" : "Show"} FPS counter</button></div>\n    <h2 class="sec">Cinematic camera</h2><div class="segc"><button class="${GFX.noCine ? "" : "on"}" data-act="gfxCine" data-v="0">On</button><button class="${GFX.noCine ? "on" : ""}" data-act="gfxCine" data-v="1">Off</button></div><p class="note">During live events the camera can swing in for the big moments. Turn it off to keep the camera where you put it.</p>')
rep("gfxFps: () => { GFX.showFps = GFX.showFps ? 0 : 1; gfxSave(); if (sheet) renderSheet(); },",
    "gfxFps: () => { GFX.showFps = GFX.showFps ? 0 : 1; gfxSave(); if (sheet) renderSheet(); },\n  gfxCine: d => { GFX.noCine = +d.v ? 1 : 0; gfxSave(); if (sheet) renderSheet(); toast(`Cinematic camera ${GFX.noCine ? \"off\" : \"on\"}.`); },")
# --- named event stages ---
rep("function shBossLab() {",
r"""/* v479 the live event and its stage, by name (the same for everyone: worked out from the shared clock and the hunt records) */
const DV_STAGE = { awake: "Awakening", mig: "Migration", asm: "Assembly", act: "Activation", stage: "The grand fleet stages", war: "The last stand", after: "Aftermath", fight: "The Omega Cube", ret: "Collapse" };
function evNow(T = now()) { try {
  const k = sbLiveKey(T); if (k) { const s0 = sbStartOf(k, T), st = sbState(k, s0), dead = st.dead && st.dead > s0; return { id: k, n: SBW[k].n, stage: dead ? "Fallen" : T < s0 + SB_ARR ? "Arrival" : SBW[k].ph[sbPhase(k, st.hp)][1] }; }
  const d = dvNow(T); if (d) return { id: "dv", n: "Cube Devastation", stage: DV_STAGE[d.ph] || d.ph };
  if (wbGroupOn(3, T)) { const fz = wbFuse(T); return { id: "conv", n: "The Convergence", stage: wbSwept(T) ? "Clean Sweep" : fz.form >= .99 ? "The Pentarch" : fz.form > .01 ? "Fusion" : "The Elementals" }; }
  const st = wbState(T); for (const w of ROTS) if (wbOn(w, T)) { const h = Math.round((st.hp[w] | 0) / WB_SEG * 100); return { id: w, n: WB[w].n, stage: h > 75 ? "Hull above 75%" : h > 50 ? "Hull 50-75%" : h > 25 ? "Hull 25-50%" : h > 0 ? "Hull below 25%" : "Fallen" }; }
} catch (e) {} return null; }
setInterval(() => { try { const E = evNow(); G.evCur = E ? `${E.id}:${E.stage}` : null; } catch (e) {} }, 2000);
function shBossLab() {""")
rep("${G.wbShow ? `<button class=\"btn wide\" data-act=\"labStop\">■ Stop the ${esc(WB[G.wbShow].n)} preview</button>` : \"\"}<button class=\"btn ghost wide\" data-act=\"stressOpen\">",
    "${(E => E ? `<p class=\"note\"><b style=\"color:#7dff9a\">● Now:</b> ${esc(E.n)} · ${esc(E.stage)}</p>` : \"\")(evNow(T))}${evMetricsHTML()}${G.wbShow ? `<button class=\"btn wide\" data-act=\"labStop\">■ Stop the ${esc(WB[G.wbShow].n)} preview</button>` : \"\"}<button class=\"btn ghost wide\" data-act=\"stressOpen\">")
# --- per-event metrics ---
rep("function pfFrame(rd) { if (!(rd > 0) || rd > 20000 || !G.ready || performance.now() - (G.pfOk || (G.pfOk = performance.now())) < 4000) return; /* start-up loading is not play */ const k = pfKey(), s = PF.vw[k] || (PF.vw[k] = [0, 0, 0, 0, 0]); s[0]++; s[1] += rd; if (rd > 34) s[2]++; if (rd > 50) s[3]++; if (rd > s[4]) s[4] = rd;",
    "function pfFrame(rd) { if (!(rd > 0) || rd > 20000 || !G.ready || performance.now() - (G.pfOk || (G.pfOk = performance.now())) < 4000) return; /* start-up loading is not play */ const k = pfKey(), s = PF.vw[k] || (PF.vw[k] = [0, 0, 0, 0, 0]); s[0]++; s[1] += rd; if (rd > 34) s[2]++; if (rd > 50) s[3]++; if (rd > s[4]) s[4] = rd;\n  if (G.evCur) { const e = (PF.ev || (PF.ev = {}))[G.evCur] || (PF.ev[G.evCur] = [0, 0, 0, 0, 0]); e[0]++; e[1] += rd; if (rd > 34) e[2]++; if (rd > 700) e[3]++; } /* v479 per event and stage */")
rep("pr: P.pr || 0, gpu: P.gpu || \"\", preset: P.preset || \"\", hz: P.hz || 0, mem }; }",
    "pr: P.pr || 0, gpu: P.gpu || \"\", preset: P.preset || \"\", hz: P.hz || 0, mem, ev: JSON.stringify(P.ev || {}).slice(0, 900) }; }\n/* v479 this session's per-event numbers, for Boss Lab: [frames, ms, slow, freezes, attacks] per event:stage */\nfunction evMetricsHTML() { const E = PF.ev || {}, ks = Object.keys(E); if (!ks.length) return \"\"; return `<details class=\"note\" style=\"margin:4px 0 8px\"><summary>This session, by event</summary>${ks.map(k => { const e = E[k]; return `${esc(k.replace(\":\", \" · \"))}: ${Math.round(e[1] / 1000)} s · ${e[1] ? (e[0] * 1000 / e[1]).toFixed(0) : 0} fps · ${e[2]} slow · ${e[3]} freezes · ${e[4] || 0} attacks`; }).join(\"<br>\")}</details>`; }")
rep("function mkRep(o) { return Object.assign({ id: \"r\" + (S.seq++), loot: { m: 0, c: 0, g: 0 } }, o); }",
    "function mkRep(o) { if (!o.test && (o.wb || o.sbk || o.omega) && G.evCur) try { const e = (PF.ev || (PF.ev = {}))[G.evCur] || (PF.ev[G.evCur] = [0, 0, 0, 0, 0]); e[4] = (e[4] || 0) + 1; } catch (er) {} /* v479 attacks per event */ return Object.assign({ id: \"r\" + (S.seq++), loot: { m: 0, c: 0, g: 0 } }, o); }")
s = re.sub(r"GAME_V = 478\b", "GAME_V = 479", s)
open(P, 'w').write(s)
