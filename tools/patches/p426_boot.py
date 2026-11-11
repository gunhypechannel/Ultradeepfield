# v426: fewer closes on iPhone right after launching and on the map (field reports, 2026-11-10: five closes 4 to 172 s after a launch).
#  1. The session restore (v409) waits for the launch to settle: until the 3D models have finished loading (the GLB queue is idle) and
#     at least 4 s have passed since the game was ready (at most 20 s), and a restored panel opens 2.5 s after the screen. It used to
#     jump straight into the map while models were still loading, so the map, the bosses, the wrecks and the panel all built at once;
#     two of the closes came seconds after "session restored" and one right after "model load cut off".
#  2. Wreck sets and the Devourer trail's hulls that have been out of view for 45 s are disposed (their charred materials freed and
#     removed from the scene), not cached for the session. Phones keep at most 2 wreck sets and 3 trail hulls.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("setInterval(() => { if (!G.sessDone && G.ready && S && G.me) { try { sessRestore(); } catch (e) { G.sessDone = 1; } } }, 500);",
    "setInterval(() => { if (!G.sessDone && G.ready && S && G.me) { const tn = performance.now(); G.sessT0 = G.sessT0 || tn; if (tn - G.sessT0 < 20000 && (tn - G.sessT0 < 4000 || GLB_RUN || GLB_Q.length)) return; /* v426 let the launch settle first */ try { sessRestore(); } catch (e) { G.sessDone = 1; } } }, 500);")
rep('if (o.sheet) setTimeout(() => { try { if (!sheet && !battle && !$("#adv")) openSheet(o.sheet); } catch (e) {} }, 1500); }',
    'if (o.sheet) setTimeout(() => { try { if (!sheet && !battle && !$("#adv")) openSheet(o.sheet); } catch (e) {} }, 2500); }')
rep("if (!S && X.sets.length < (MOBILE ? 3 : 6) && !X.built)", "if (!S && X.sets.length < (MOBILE ? 2 : 6) && !X.built)")
rep("if (!s && X.slots.length < (MOBILE ? 4 : FX_LITE() ? 6 : 10) && !X.built)", "if (!s && X.slots.length < (MOBILE ? 3 : FX_LITE() ? 6 : 10) && !X.built)")
rep("N = MOBILE ? 4 : FX_LITE() ? 6 : 10,", "N = MOBILE ? 3 : FX_LITE() ? 6 : 10,")
rep("if (!s) continue; used.add(s); s.id = pk.id;", "if (!s) continue; used.add(s); s.id = pk.id; s.seen = t;")
rep("if (!S) continue; used.add(S); S.site = s.k + s.at;", "if (!S) continue; used.add(S); S.site = s.k + s.at; S.seen = t;")
rep("for (const S of X.sets) if (!used.has(S)) { S.grp.visible = false; S.site = null; } }",
    "for (const S of X.sets) if (!used.has(S)) { S.grp.visible = false; S.site = null; } X.sets = X.sets.filter(S => { if (used.has(S) || t - (S.seen || t) < 45000) { S.seen = S.seen || t; return true; } wreckDispose(S.grp); return false; }); } /* v426 sets out of view for 45 s are freed */")
rep("for (const s of X.slots) if (!used.has(s)) { s.holder.visible = false; s.id = null; } }",
    "for (const s of X.slots) if (!used.has(s)) { s.holder.visible = false; s.id = null; } X.slots = X.slots.filter(s => { if (used.has(s) || t - (s.seen || t) < 45000) { s.seen = s.seen || t; return true; } wreckDispose(s.holder); return false; }); } /* v426 */")
rep("/* v419 a wreck's destruction pattern:", """/* v426 free a wreck group: its own (cloned) materials and sprites; geometry is shared with the fleet kit and the debris kit, so it stays */
function wreckDispose(grp) { try { grp.traverse(o => { const m = o.material; if (!m) return; for (const x of Array.isArray(m) ? m : [m]) { if (x && (o.isSprite || (x.userData && x.userData.wk))) try { x.dispose(); } catch (e) {} } }); /* only what the wreck made for itself */ if (grp.parent) grp.parent.remove(grp); } catch (e) {} }
/* v419 a wreck's destruction pattern:""")
rep("m = o.material.clone(); m.color.multiplyScalar(.4);", "m = o.material.clone(); m.userData.wk = 1; m.color.multiplyScalar(.4);", 2) # tag a wreck's own materials
rep("if (reduced || !X.pick.length) { for (const S of X.sets) S.grp.visible = false; return; }",
    "if (reduced || !X.pick.length) { for (const S of X.sets) { S.grp.visible = false; S.site = null; } X.sets = X.sets.filter(S => { if (t - (S.seen || t) < 45000) { S.seen = S.seen || t; return true; } wreckDispose(S.grp); return false; }); return; } /* v426 also when no site is near */")
t = t.replace("const GAME_V = 425;", "const GAME_V = 426;")
open(p, "w").write(t); print("ok")
