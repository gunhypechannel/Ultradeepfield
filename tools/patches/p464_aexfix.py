# v464 fixes from the owner's Aexion replay: he vanished while staggered (the stagger pushed his body back a little more every frame, so it
# drifted ~1000 units off, taking the cinematic with it), and some Advisor lines were cut off by the next one. Now the body's depth is set
# fresh each frame, and the great-event lines queue: each waits for the one she is saying to finish instead of cutting it short.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep("const st0 = ss(.92, 1, u), g0 = t * .001; let gd = 0;", "const st0 = ss(.92, 1, u), g0 = t * .001; let gd = 0; body.position.z = 0;")
# a queue for the event lines
rep("function sbBand() {", """function sbSay(line) { /* v464 she finishes each line before the next; nothing is cut off or lost */ G.sbQ = G.sbQ || []; const a0 = typeof VOICE !== "undefined" && VOICE.au;
  if (a0 && !a0.paused && !a0.ended && G.holoCur && G.holoCur !== line) { G.sbQ.push({ line, at: Date.now() }); sbQWatch(); return; } try { advHolo(line, 1); } catch (e) { try { toast(line); } catch (e2) {} } setTimeout(sbQWatch, 300); }
function sbQWatch() { const a = typeof VOICE !== "undefined" && VOICE.au; if (!G.sbQ || !G.sbQ.length) return; if (!a || a.paused || a.ended) { const n = G.sbQ.shift(); if (n) sbSay(n.line); return; } if (a._sbq) return; a._sbq = 1;
  const go = () => { a._sbq = 0; G.sbQ = (G.sbQ || []).filter(n => Date.now() - n.at < 25000); const n = G.sbQ.shift(); if (n) setTimeout(() => sbSay(n.line), 350); }; a.addEventListener("ended", go, { once: true }); a.addEventListener("error", go, { once: true }); }
function sbBand() {""")
rep("try { advHolo(line, 1); } catch (e) { toast(line); } };", "sbSay(line); };")
rep("const say = (id, line) => { G.sbSaid = G.sbSaid || {}; if (G.sbSaid[id]) return; G.sbSaid[id] = 1; try { advHolo(line, 1); } catch (er) {} };", "const say = (id, line) => { G.sbSaid = G.sbSaid || {}; if (G.sbSaid[id]) return; G.sbSaid[id] = 1; sbSay(line); };")
rep("G.dvSaid[id] = 1; try { advHolo(line, 1); } catch (er) {} };", "G.dvSaid[id] = 1; sbSay(line); };")
# and spaced so each has room
rep('if (ft > .2) say("a2b"', 'if (ft > .23) say("a2b"')
rep('if (ft > .5) say("a3"', 'if (ft > .6) say("a3"')
rep('if (s > 68.7) say("a4c"', 'if (s > 69.6) say("a4c"')
rep('if (s > 79.6) say("a5b"', 'if (s > 78.2) say("a5b"')
rep('if (be > .2) say("a7"', 'if (be > 2.4) say("a7"')
s = re.sub(r"GAME_V = 463\b", "GAME_V = 464", s)
open(P, 'w').write(s)
