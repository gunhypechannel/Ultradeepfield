# v430: CUBE DEVASTATION, part 1 (owner: a monthly live event on the 11th; every Assimilation Cube in the galaxy, and the Super Cube,
#  assemble into the OMEGA CUBE, after the reference image). First run 11 Dec 2026, 11am Phoenix (18:00 UTC), then every 11th.
#  This part: the shared timeline (dvNow), the plan (dvPlan: slots, departures, arrivals, lock order), the migration, the puzzle
#  assembly and the core's eruption in the live galaxy map (dvTick), the Super Cube moving to the core, and the owner's 4-minute
#  preview (Menu > owner tools). Combat, rewards, sound, banner and the event panel follow in later parts. Nobody but the owner
#  sees anything until 11 Dec.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
CODE = open("tools/patches/p430_dv.js").read()
rep("/* v408 tapping the Super Cube */", CODE + "/* v408 tapping the Super Cube */")
rep("function wbScarFx(W, t, T) {", "function wbScarFx(W, t, T) {\n  try { dvTick(W, t, T); } catch (e) { mapErr(e); } // v430 Cube Devastation")
rep("if (LI) { const cp = liveCubePos(LI.s); np.set(cp.x, cp.y, cp.z); } else { const cw = PH && cubeWorldPos(T, PH); if (cw) np.set(cw.x, cw.y, cw.z); }",
    "if (LI) { const cp = liveCubePos(LI.s); np.set(cp.x, cp.y, cp.z); } else { const cw = PH && cubeWorldPos(T, PH); if (cw) np.set(cw.x, cw.y, cw.z); }\n    const DVn = dvNow(T), DVq = DVn && dvCore(DVn, {}); if (DVq) np.set(DVq.x, DVq.y, DVq.z); /* v430 the Super Cube goes to the heart of the Omega Cube */")
rep("W.nexus.rotation.x = .18; W.nexus.userData.r2.rotation.y = -t * .0012;",
    "W.nexus.rotation.x = .18; W.nexus.userData.r2.rotation.y = -t * .0012;\n    if (DVq && DVq.u > 0) { const al = dvEase(DVq.u); W.nexus.rotation.x = .18 * (1 - al); W.nexus.rotation.y = W.nexus.rotation.y * (1 - al) + dvRot(DVn.e) * al; W.nexus.userData.r2.visible = al < .5; } else W.nexus.userData.r2.visible = true; /* square to the Omega once it is home */")
rep('o.grp.visible = nf && !(G.vmode === "planet" && dc < 9 && !W.cam.cine);', 'o.grp.visible = nf && !(G.vmode === "planet" && dc < 9 && !W.cam.cine) && !(it.boss && dvLive(T)); /* v430 */')
rep("A.aCol[j + 3] = !nf || M.near.has(it.id) ? 0 :", "A.aCol[j + 3] = !nf || M.near.has(it.id) || (it.boss && dvLive(T)) ? 0 :")
rep('<button class="btn ghost wide" data-act="${G.convSim ? "convSimStop" : "convSim"}">${G.convSim ? "■ Stop the Convergence preview" : "▶ Watch the whole Elemental Convergence"}</button>',
    '<button class="btn ghost wide" data-act="${G.convSim ? "convSimStop" : "convSim"}">${G.convSim ? "■ Stop the Convergence preview" : "▶ Watch the whole Elemental Convergence"}</button><button class="btn ghost wide" data-act="${G.dvSim ? "dvSimStop" : "dvSim"}">${G.dvSim ? "■ Stop the Cube Devastation preview" : "▶ Watch Cube Devastation (Omega Cube)"}</button>')
rep("  convSim: () => convSimStart(),", "  convSim: () => convSimStart(),\n  dvSim: () => dvSimStart(), dvSimStop: () => { dvSimStop(); if (sheet) renderSheet(); }, /* v430 */")
t = t.replace("const GAME_V = 429;", "const GAME_V = 430;")
open(p, "w").write(t); print("ok")
