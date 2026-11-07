import sys, re
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# v333 onboarding measurement, kept in the commander's own (private) save so it can be read from the database:
#   S.tutT  { step key: when it opened }, plus "done" when the Academy is finished
#   S.tutH  { step key: how many times "Show me" was tapped on it }
#   S.errs  the last 12 script errors (message, game version, Academy step), so crashes on real phones are visible
rep('''const tutAt = id => tutOn() && (TUT[S.tut.i] || {}).id === id;''', '''const tutAt = id => tutOn() && (TUT[S.tut.i] || {}).id === id;
const tutKey = i => { const s = TUT[i]; return s ? (s.id || s.t) : "done"; }; // v333: steps are recorded by a name that survives renumbering
function tutTrack() { if (!S || !S.tut) return; const k = tutKey(S.tut.i); S.tutT = S.tutT || {}; if (!S.tutT[k]) { S.tutT[k] = now(); dirty(); } }''')
rep('''function tutShow() {
  const st = TUT[S.tut.i]; if (!st) return;''', '''function tutShow() {
  const st = TUT[S.tut.i]; if (!st) return; { const k = tutKey(S.tut.i); S.tutH = S.tutH || {}; S.tutH[k] = (S.tutH[k] || 0) + 1; dirty(); } // v333''')
rep('''  if (open && !done && VOICE.lastStep !== S.tut.i''', '''  try { tutTrack(); } catch (e) {}
  if (open && !done && VOICE.lastStep !== S.tut.i''')
rep('''const ERR_SEEN = new Set(); function errCrumb(m) { try { m = String(m || "error").slice(0, 140); if (ERR_SEEN.has(m) || ERR_SEEN.size >= 8) return; ERR_SEEN.add(m); crumb("error: " + m); } catch (e) {} }''',
    '''const ERR_SEEN = new Set(); function errCrumb(m) { try { m = String(m || "error").slice(0, 140); if (ERR_SEEN.has(m) || ERR_SEEN.size >= 8) return; ERR_SEEN.add(m); crumb("error: " + m);
  if (typeof S !== "undefined" && S) { S.errs = (S.errs || []).concat([{ t: Date.now(), v: GAME_V, m, i: S.tut ? S.tut.i : -1 }]).slice(-12); try { dirty(); } catch (e) {} } } catch (e) {} } // v333: errors reach the cloud save''')
v = int(re.search(r"const GAME_V = (\d+)", t).group(1)); t = t.replace(f"const GAME_V = {v}", "const GAME_V = 333", 1)
open(p, 'w', encoding='utf-8', newline='').write(t); print('v333 from', v)
