# v573 The Ten Seals, fixes found on a real GPU (the owner's PC):
# 1) Watch during the map's opening film left the map black: finWatchGo now waits for the opening to end and never cancels a film
#    other than an object cinematic; riding with the set piece eases the camera itself instead of re-arming a fly-to goal every frame.
# 2) The Events hub's season finale card called any finale boss a chapter (Season 1's Wednesday Khezaroth read "Chapter 9"): only
#    the chapter's own season is labelled and opens the chapter.
# 3) The Gaze frames the galaxy a little closer.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('function finWatchGo(k) { closeSheet(); if (view !== "galaxy") { view = "galaxy"; render(); } setTimeout(() => { try { const F = finNow(now()), X = G3 && G3.fin, c = G3.cam; c.follow = null; c.followFleet = null; c.cineObj = null; c.cine = null; G.finFollow = performance.now() + 90000;',
    'function finWatchGo(k, n) { if (!n) { closeSheet(); if (view !== "galaxy") { view = "galaxy"; render(); } } setTimeout(() => { try { if (!G3 || (G3.cam.cine && !G3.cam.cineObj) || G3.cam.live) { if ((n || 0) < 30) finWatchGo(k, (n || 0) + 1); return; } /* v573 the map is still filming its opening: wait for it */ const F = finNow(now()), X = G3.fin, c = G3.cam; c.follow = null; c.followFleet = null; if (c.cineObj) { c.cineObj = null; c.cine = null; } G.finFollow = performance.now() + 90000;')
rep("c.goal = { tx: q.x, ty: q.y, tz: q.z, dist: X && X.dist || 900, th: .7 }; } catch (e) {} }, 300); }", "c.goal = { tx: q.x, ty: q.y, tz: q.z, dist: X && X.dist || 900, th: .7 }; } catch (e) {} }, n ? 1000 : 300); }")
rep("  if (G.finFollow && performance.now() < G.finFollow && X.foc && G3 && G3.cam && G3.cam.goal && !G3.cam.follow && !G3.cam.cineObj) Object.assign(G3.cam.goal, { tx: X.foc.x, ty: X.foc.y, tz: X.foc.z });",
    "  if (G.finFollow && performance.now() < G.finFollow && X.foc && G3 && G3.cam && !G3.cam.follow && !G3.cam.cineObj && !G3.cam.cine) { const c = G3.cam; if (c.goal && c.goal.dist == null) c.goal = null; if (!c.goal && c.tx != null) { c.tx += (X.foc.x - c.tx) * .04; c.ty += (X.foc.y - c.ty) * .04; c.tz += (X.foc.z - c.tz) * .04; } } // v573 ride with it (eased; the fly-to goal goes first)")
rep('X.foc = new TH.Vector3(P1.x * .4, P1.y * .4, P1.z * .4); X.dist = 1400; }', 'X.foc = new TH.Vector3(P1.x * .5, P1.y * .5, P1.z * .5); X.dist = 1150; }')
rep('<div${FIN_EV[a] && FIN_EV[a].st ? ` class="finrow" data-act="finOpen" data-k="${a}"` : ""}><span>${FIN_EV[a] && FIN_EV[a].st ? `Chapter', '<div${FIN_EV[a] && FIN_EV[a].st && FIN_EV[a].ch - 1 === x ? ` class="finrow" data-act="finOpen" data-k="${a}"` : ""}><span>${FIN_EV[a] && FIN_EV[a].st && FIN_EV[a].ch - 1 === x ? `Chapter')
rep('<div${FIN_EV[b] ? ` class="finrow" data-act="finOpen" data-k="${b}"` : ""}><span>${FIN_EV[b] ? `Chapter', '<div${FIN_EV[b] && FIN_EV[b].ch - 1 === x ? ` class="finrow" data-act="finOpen" data-k="${b}"` : ""}><span>${FIN_EV[b] && FIN_EV[b].ch - 1 === x ? `Chapter')
s2 = re.sub(r"GAME_V = 572\b", "GAME_V = 573", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
