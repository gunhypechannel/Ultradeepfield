import sys, re
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# the Advisor's welcome lines no longer open behind the "Played before the move?" card; they follow once it is answered
rep('''function flushSay0() { if (S.say.length && !battle && !(sheet && sheet.type === "faction")) {''',
    '''function flushSay0() { if (S.say.length && !battle && !(sheet && sheet.type === "faction") && !$("#oldw")) { /* v330: not behind the old-server card */''')
v = int(re.search(r"const GAME_V = (\d+)", t).group(1)); t = t.replace(f"const GAME_V = {v}", "const GAME_V = 330", 1)
open(p, 'w', encoding='utf-8', newline='').write(t); print('v330 from', v)
t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# waiting on a fleet while already on the Fleets screen: the guide pointed at the Fleets tab you were on, so it showed nothing at
# all; it now points at the fleet in flight with the waiting message
rep('''  for (const [sel, label, when] of path) { if (when && !when()) continue; for (const el of document.querySelectorAll(sel)) { if (el.classList.contains("on") || (el.disabled && /^(boost|finish)$/.test(el.dataset.act || ""))) continue;''',
    '''  let waitLab = ""; for (const [sel, label, when] of path) { if (when && !when()) continue; for (const el of document.querySelectorAll(sel)) { if (el.classList.contains("on") && el.dataset.act === "nav" && /on its way|flying home|gathering|Wait/.test(label)) waitLab = waitLab || label; // v330
      if (el.classList.contains("on") || (el.disabled && /^(boost|finish)$/.test(el.dataset.act || ""))) continue;''')
rep('''  const cx = sheet && document.querySelector('.sheet [data-act="close"]'); const cv = cx && guideVisible(cx); if (cv) return { el: cx, label: st.ok(S) ? "Close this to collect your reward" : "Close this to continue", v: cv };''',
    '''  if (waitLab && !sheet) { const fc = [...document.querySelectorAll("#view .fcard")].find(e => guideVisible(e)); if (fc) return { el: fc, label: waitLab, v: guideVisible(fc) }; } // v330: the fleet you're waiting for
  const cx = sheet && document.querySelector('.sheet [data-act="close"]'); const cv = cx && guideVisible(cx); if (cv) return { el: cx, label: st.ok(S) ? "Close this to collect your reward" : "Close this to continue", v: cv };''')
open(p, 'w', encoding='utf-8', newline='').write(t); print('ok2')
t = open(p, encoding='utf-8', newline='').read()
# found by the online run: the Academy's first attack target (the lowest-level Hive world) can sit in uncharted space, depending
# on where your homeworld lands in the shared galaxy; its card then shows "Uncharted space" with no Attack button and the guide
# looped "Close this to continue". The Academy now charts the target it shows you (as Find already does).
rep('''    if (sheet) closeSheet(); if (view !== "galaxy") { view = "galaxy"; render(); } if (p) ACT.planet({ id: p[0].id }); }''',
    '''    if (p && isFogged(p[0], T)) { const q = pos(p[0], T); reveal(q.x, q.y, 24); fogSave(); } // v330: never an uncharted target
    if (sheet) closeSheet(); if (view !== "galaxy") { view = "galaxy"; render(); } if (p) ACT.planet({ id: p[0].id }); }''')
open(p, 'w', encoding='utf-8', newline='').write(t); print('ok3')
