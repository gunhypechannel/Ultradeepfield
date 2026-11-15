# v579 Fixes from the real-GPU pass through every Boss Lab preview on the owner's PC (owner: "Complete all").
# 1) The event band (an omen, a finale, the Cube) no longer sits on top of a cinematic's scan card, or over the Judge's face in his
#    preview. 2) The Leviathan's Architects' wall (the gold hex wall it breaks through) was barely visible: brighter and taller.
# 3) Every Ten Seals preview shows the Judge with all six eyes open (it is after the prologue), not this week's count.
# 4) Starting any Boss Lab preview first ends whatever preview or cinematic was running (a stuck "Cinematic" bar, a boss left on
#    the map, two set pieces at once).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('if (view === "galaxy" && !sheet && !battle && !G.sbSim) { if (live)', 'const cineOn = !!(G3 && G3.cam && (G3.cam.cine || G3.cam.cineObj)) || !!G.judgeSim; /* v579 never over a cinematic */\n  if (view === "galaxy" && !sheet && !battle && !G.sbSim && !cineOn) { if (live)')
rep('if (!html && view === "galaxy" && !sheet && !battle && !G.sbSim) html = finBand(T);', 'if (!html && view === "galaxy" && !sheet && !battle && !G.sbSim && !cineOn) html = finBand(T);')
# the wall
rep('{ const op = .5 * fsm(e / (10 * 60e3)) * fade,', '{ const op = .85 * fsm(e / (10 * 60e3)) * fade,')
rep('X.wall = new TH.InstancedMesh(new TH.PlaneGeometry(pw, 64), new TH.MeshBasicMaterial({ map: finHexTex(), color: 0xffd890,', 'X.wall = new TH.InstancedMesh(new TH.PlaneGeometry(pw, 84), new TH.MeshBasicMaterial({ map: finHexTex(), color: 0xffe2a0,')
# the Judge in previews
rep('if (G.finSim && FIN_EV[G.finSim.k] && FIN_EV[G.finSim.k].typ === "omen") return G.finSim.k === "om2" ? 6 : 3;', 'if (G.finSim) return G.finSim.k === "om1" ? 3 : 6; if (G.sbSim || G.dvSim || G.convSim || G.wbShow || (G.labMap && performance.now() < G.labMap.until)) return G.labMap && G.labMap.omen ? Math.ceil((OMEN_K.indexOf(G.labMap.omen) + 1) * 6 / OMEN_K.length) : 6; /* v579 every preview shows him as he will be then (the Ten Seals come after the prologue) */')
# one preview at a time
rep('/* v578 every live event, grouped, each with its preview */', '''/* v579 a new preview first ends the one before (and any cinematic), so nothing is left on the map */
function labReset() { try { if (G.finSim) { G.finSim = null; if (G3 && G3.fin) finFree(G3); } } catch (e) {} try { if (G.sbSim) sbSimStop(); } catch (e) {} try { if (G.dvSim) dvSimStop(); } catch (e) {} try { if (G.convSim) G.convSim = null; } catch (e) {}
  G.wbShow = null; G.wbFakeDead = null; WBN = null; G.labMap = null; G.judgeSim = 0; try { cineEnd(); } catch (e) {} }
/* v578 every live event, grouped, each with its preview */''')
rep('labPrev: d => { if (!duelOwner()) return; const k = d.k;', 'labPrev: d => { if (!duelOwner()) return; labReset(); const k = d.k;')
rep('labDie: d => { if (!duelOwner()) return; const k = d.k;', 'labDie: d => { if (!duelOwner()) return; labReset(); const k = d.k;')
rep('labOmen: d => { if (!duelOwner()) return; const k = d.k;', 'labOmen: d => { if (!duelOwner()) return; labReset(); const k = d.k;')
rep('labScars: () => { if (!duelOwner()) return;', 'labScars: () => { if (!duelOwner()) return; labReset();')
rep('labJudge: () => { if (!duelOwner()) return;', 'labJudge: () => { if (!duelOwner()) return; labReset();')
rep('finOpen: d => FIN_EV[d.k] && FIN_EV[d.k].typ === "omen" ? finWatchGo(d.k) : openSheet({ type: "finale", k: d.k }), finSim: d => finSimStart(d.k),', 'finOpen: d => FIN_EV[d.k] && FIN_EV[d.k].typ === "omen" ? finWatchGo(d.k) : openSheet({ type: "finale", k: d.k }), finSim: d => { if (duelOwner()) labReset(); finSimStart(d.k); },')
# the Judge's closed eyes read as dim stone, not black holes; his eye glow takes a verdict's colour cleanly
rep('dot(J.glow, px, py, 10, "rgba(235,255,240,1)", "rgba(80,255,130,.55)")', 'dot(J.glow, px, py, 10, "rgba(255,255,255,1)", "rgba(215,255,225,.6)")')
rep('J.lid.s.material.opacity = e;', 'J.lid.s.material.opacity = e * .82;')
s2 = re.sub(r"GAME_V = 578\b", "GAME_V = 579", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
