# v450 owner previews of the Ultimate Super Bosses on the galaxy map (p450_sbprev.js): Vaelthar and Aexion
import re, os
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
js = open(os.path.join(os.path.dirname(__file__), 'p450_sbprev.js')).read()
rep("/* v408 tapping the Super Cube */", js + "/* v408 tapping the Super Cube */")
rep("  try { dvTick(W, t, T); } catch (e) { mapErr(e); } // v430 Cube Devastation\n", "  try { dvTick(W, t, T); } catch (e) { mapErr(e); } // v430 Cube Devastation\n  try { sbTick(W, t); } catch (e) { mapErr(e); } // v450 the super boss previews\n")
rep('${G.dvSim ? "■ Stop the Cube Devastation preview" : "▶ Watch Cube Devastation (Omega Cube)"}</button>',
    '${G.dvSim ? "■ Stop the Cube Devastation preview" : "▶ Watch Cube Devastation (Omega Cube)"}</button><button class="btn ghost wide" data-act="${G.sbSim && G.sbSim.key === "vae" ? "sbStop" : "sbVae"}">${G.sbSim && G.sbSim.key === "vae" ? "■ Stop the Vaelthar preview" : "▶ Watch Vaelthar, the Celestial Ruin"}</button><button class="btn ghost wide" data-act="${G.sbSim && G.sbSim.key === "aex" ? "sbStop" : "sbAex"}">${G.sbSim && G.sbSim.key === "aex" ? "■ Stop the Aexion preview" : "▶ Watch Aexion, the Warform Sovereign"}</button>')
rep("  dvSim: () => dvSimStart(),", "  sbVae: () => sbSimStart(\"vae\"), sbAex: () => sbSimStart(\"aex\"), sbStop: () => { sbSimStop(); if (sheet) renderSheet(); }, /* v450 */\n  dvSim: () => dvSimStart(),")
rep("function dvCountdown(W, t, T, live) { const show = !live && view === \"galaxy\";", "function dvCountdown(W, t, T, live) { const show = !live && view === \"galaxy\" && !G.sbSim;")
s = re.sub(r"GAME_V = 449\b", "GAME_V = 450", s)
open(P, 'w').write(s)
