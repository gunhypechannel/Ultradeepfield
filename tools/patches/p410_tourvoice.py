# v410 (2): the Advisor talks you through the neighbourhood tour. Each of its six steps has a spoken line (TOUR_SAY, no names in them so
# one recording serves everyone; the caption still names your world and layer). A step now waits for her line to finish (at least its old
# 4 to 4.8 s, at most 14 s) before the camera moves on; skipping or leaving the tour stops her.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("""let tourT = null;
function tourStop() { clearTimeout(tourT); tourT = null; const el = $("#tourcap"); if (el) el.hidden = true; }""",
"""let tourT = null;
const TOUR_SAY = ["This is your homeworld, Commander. Everything you build starts here.",
  "These are your neighbours, the worlds orbiting closest to you. Some will be friends. Some will be targets.",
  "This is your layer of the galaxy. Every layer further in is richer, and more dangerous.",
  "And this is the whole galaxy. The colour around each world shows which alliance controls it.",
  "At the very heart lies the Void, and the Cube that every alliance fights for each weekend.",
  "Tap any world to spy on it, attack it, send it cargo, or add it to your favourites. The galaxy is yours to take, Commander."]; // v410 the Advisor narrates the tour
const tourVoiceOn = () => { const a = VOICE.au; return !!(a && !a.paused && !a.ended && TOUR_SAY.some(l => a.src.includes(voiceKey(l)))); };
function tourStop() { clearTimeout(tourT); tourT = null; const el = $("#tourcap"); if (el) el.hidden = true; if (tourVoiceOn()) voiceStop(); }""")
rep("""  steps[i][0](); el.innerHTML = `<span>${steps[i][1]}</span><small>${i + 1} / ${steps.length} · tap to skip</small>`; el.hidden = false;
  tourT = setTimeout(() => tourRun(i + 1), i === 3 ? 4800 : 4000);""",
"""  steps[i][0](); el.innerHTML = `<span>${steps[i][1]}</span><small>${i + 1} / ${steps.length} · tap to skip</small>`; el.hidden = false;
  try { speak(TOUR_SAY[i]); } catch (e) {} const t0 = performance.now(); let heard = 0;
  const wait = () => { if (tourVoiceOn() && performance.now() - t0 < 14000) { heard = 1; tourT = setTimeout(wait, 250); } else tourT = setTimeout(() => tourRun(i + 1), heard ? 450 : 0); }; // v410: the camera moves on when she has finished
  tourT = setTimeout(wait, i === 3 ? 4800 : 4000);""")
open(p, "w").write(t); print("ok")
