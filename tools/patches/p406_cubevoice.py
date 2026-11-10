# v406: the Advisor narrates the Cube. The 82-second Cube Live film gets a spoken line on each of its six shots (the captions stay),
# timed to the cut, heard only by those who join a shot near its start. The Super Cube siege camera (watching the battle live) gets a
# commentary: first who holds the Cube (or that the finale is on), then a line about what is on screen at every other cut (every ~32 s),
# never the same line twice in one viewing, quiet once she has said them all unless the Cube changes hands.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)

rep("""const easeIO = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;""", """const LIVE_SAY = ["Commander, a signal is coming from the heart of the galaxy. Something vast has woken in the dark.", "The Cube is leaving its orbit. Every sensor we have is locked on it.",
  "It is descending into the gravity well, straight for the Void at the centre of the galaxy.", "The Collective has taken the Void. Its tractor beams are reaching across the wreck field.",
  "Nothing survived the last fleet that stood here. This time, it will be different.", "The Battle for the Cube has begun. Take it, and hold it for your alliance."]; // v406: the Advisor narrates the film
const easeIO = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;""")
rep("""cap.textContent = LIVE_SHOTS[sh][1]; if (LIVE_SHOTS[sh][1]) cap.classList.add("on"); }""",
    """cap.textContent = LIVE_SHOTS[sh][1]; if (LIVE_SHOTS[sh][1]) cap.classList.add("on"); if (LI.s - LIVE_SHOTS[sh][0] < (sh ? 5000 : 8000)) speak(LIVE_SAY[sh]); }""")
rep("""  liveSkip: () => { if (G.liveReplay) G.liveReplay = 0; else S.liveSkip = evWeek(now()); dirty(); liveEnd(); }, // v98""",
    """  liveSkip: () => { if (G.liveReplay) G.liveReplay = 0; else S.liveSkip = evWeek(now()); dirty(); liveEnd(); if (VOICE.au && LIVE_SAY.some(l => voiceKey(l) && VOICE.au.src.includes(voiceKey(l)))) voiceStop(); }, // v98; v406 her line stops with the film""")
rep("""const SIEGE_SHOTS = ["Low orbit", "Attack run", "Capital ship", "Wreck field", "Flagship"];""", """const SIEGE_SHOTS = ["Low orbit", "Attack run", "Capital ship", "Wreck field", "Flagship"];
/* v406 the Advisor's commentary on the Super Cube battle */
const SIEGE_SAY = { open: "No alliance holds the Cube yet. The first to take it starts the clock.", ours: "Our alliance holds the Cube. Every minute counts. Hold the line, Commander.",
  theirs: "Another alliance holds the Cube. Rally the fleet, Commander. We can take it back.", finale: "These are the final hours, Commander. Whoever holds the Cube at the end takes the galaxy.",
  shots: [["Commander, the Cube sits on the Void, and every alliance in the galaxy is closing in.", "There it is, the Cube, anchored over the Void. Nothing in the galaxy is bigger."],
    ["Squadrons are making their attack runs. Watch the shields flare as they hit.", "Fighters are diving on the Cube in waves. Not all of them will make a second pass."],
    ["A capital ship is passing the Cube. That is where the real damage is done.", "The heavy ships are trading fire with the Cube now. Hold steady."],
    ["The wreck field grows by the minute. Every hulk out there was somebody's fleet.", "So much wreckage around the Void. The salvage crews will be busy for weeks."],
    ["That is a commander's flagship, leading its fleet into the fight.", "A flagship is leading the charge. Commanders are fighting on the front line today."]] };
function siegeSay(sh) { const T = now(), t = performance.now(), ph = cubePhase(T); if (!ph || !S) return; let h = null; try { h = nexusNow(T).holder || null; } catch (e) {}
  const changed = G.siegeN && G.siegeHolder !== h; if (!changed && G.siegeSaidAt && t - G.siegeSaidAt < 30000) return;
  let line; if (!G.siegeN || changed) line = ph.key === "finale" ? SIEGE_SAY.finale : S.ally && h === S.ally ? SIEGE_SAY.ours : h ? SIEGE_SAY.theirs : SIEGE_SAY.open;
  else { line = (SIEGE_SAY.shots[sh] || []).find(l => !G.siegeUsed.includes(l)); if (!line) return; }
  G.siegeUsed.push(line); G.siegeHolder = h; G.siegeN = (G.siegeN || 0) + 1; G.siegeSaidAt = t; advHolo(line); }""")
rep("""  if (c.siege.sh !== sh) { c.siege.sh = sh; c.tx = tx;""", """  if (c.siege.sh !== sh) { c.siege.sh = sh; try { siegeSay(sh); } catch (e) {} c.tx = tx;""")
rep("""function siegeStart(n) { closeSheet();""", """function siegeStart(n) { G.siegeN = 0; G.siegeUsed = []; G.siegeSaidAt = 0; G.siegeHolder = undefined; closeSheet();""")
t = t.replace("const GAME_V = 405;", "const GAME_V = 406;")
open(p, "w").write(t); print("ok")
