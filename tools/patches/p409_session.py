# v409 (2): pick up where you left off. iOS ends a web app in the background to free memory (the most common "crash" in the reports:
# "Restarted after N min in the background"), and the game came back on the base with the default camera. Progress was already saved
# on hide (dirty + flush); now the session is too: the view and its tab, the map camera, the selected world and a reopenable panel,
# saved on hide, on pagehide and every 15 s, and restored after a relaunch (same account, under 12 h old, Academy finished, no film).
p = "docs/index.html"; t = open(p).read()
i = t.index("function glNew(o) {")
t = t[:i] + """/* v409 the session: where the player was, restored after the phone closes the game in the background */
const SESS_K = "udf.sess", SESS_VIEWS = ["base", "galaxy", "build", "mail", "quests", "rank", "ally", "cmd"], SESS_SHEETS = ["events", "bld", "wboss", "cubepick", "stress"];
function sessSave() { try { if (!G.ready || !S || !G.me || G.sessHold || !G.sessDone) return; /* never before the last session was read back */ const o = { t: Date.now(), v: typeof GAME_V !== "undefined" ? GAME_V : 0, me: G.me, view, sub: jcopy(sub) };
    if (view === "galaxy" && G3 && G3.cam) { const c = G3.cam; if (!c.cine && !c.live && [c.tx, c.tz, c.dist, c.th, c.ph].every(Number.isFinite)) o.cam = { tx: c.tx, ty: c.ty || 0, tz: c.tz, dist: c.dist, th: c.th, ph: c.ph }; }
    if (G.sel) o.sel = G.sel; if (sheet && SESS_SHEETS.includes(sheet.type)) { try { o.sheet = JSON.parse(JSON.stringify(sheet)); } catch (e) {} }
    localStorage.setItem(SESS_K, JSON.stringify(o)); } catch (e) {} }
function sessRestore() { let o = null; try { o = JSON.parse(localStorage.getItem(SESS_K) || "null"); } catch (e) {} G.sessDone = 1;
  if (!o || o.me !== G.me || Date.now() - o.t > 12 * 3600e3 || !SESS_VIEWS.includes(o.view) || !S || !S.tut || S.tut.k !== "done" || battle) return;
  try { if (typeof liveIntro === "function" && liveIntro(now())) return; } catch (e) {}
  G.sessHold = 1; try { if (o.sub) Object.assign(sub, o.sub); if (view !== o.view) { view = o.view; render(); } crumb(`session restored: ${o.view}${o.cam ? " + camera" : ""}${o.sheet ? " + " + o.sheet.type : ""} (${Math.round((Date.now() - o.t) / 60000)} min)`); } catch (e) {}
  if (o.view === "galaxy" && o.cam) { let n = 0; const go = () => { if (G3 && G3.cam && !G3.cam.cine && !G3.cam.live) { const c = G3.cam; Object.assign(c, o.cam); c.goal = null; c.follow = null; c.followFleet = null; c.vel = null; if (o.sel && G.byId[o.sel]) G.sel = o.sel; G.sessHold = 0; } else if (n++ < 60) setTimeout(go, 250); else G.sessHold = 0; }; go(); } else G.sessHold = 0;
  if (o.sheet) setTimeout(() => { try { if (!sheet && !battle && !$("#adv")) openSheet(o.sheet); } catch (e) {} }, 1500); }
document.addEventListener("visibilitychange", () => { if (document.hidden) sessSave(); }); addEventListener("pagehide", sessSave); setInterval(sessSave, 15000);
setInterval(() => { if (!G.sessDone && G.ready && S && G.me) { try { sessRestore(); } catch (e) { G.sessDone = 1; } } }, 500);
""" + t[i:]
open(p, "w").write(t); print("ok")
