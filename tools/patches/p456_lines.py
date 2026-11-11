# v456 the Advisor's missing live lines for the great events: each super boss phase as you find it, Divine Annihilation firing, Vaelthar's
# fall, and the three-day warnings for Vaelthar, Aexion and Cube Devastation (once per event on each device). All voiced with the rest.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep("function sbBand() {", """const SBL = { vae: [null, "Vaelthar's wheel is waking. Its stabilizers are exposed: break four of them before it charges!", "Divine Judgment. The wheel is charging harder now. Keep those stabilizers down!", "Final Eclipse! The wheel is fracturing and its core is exposed. Finish it!"],
  aex: [null, "Aexion stands in its Warform. Target the shield emitters to break its Aegis.", "Reactor Overdrive! Its core is exposed. Every fleet, strike the reactor now!"] };
const SB_SOON = { vae: "Long-range sensors have found a celestial anomaly. Vaelthar arrives within three days.", aex: "A dreadnought-class signature is closing on our galaxy. Aexion arrives within three days." };
const DV_SOON = "Every Assimilation Cube in the galaxy is stirring. Cube Devastation begins within three days.";
const annOnce = (k, at, line) => { try { if (!S || !G.ready) return; S.ann = S.ann || {}; if (S.ann[k] === at) return; S.ann[k] = at; dirty(); advHolo(line, 1); } catch (e) {} }; /* v456 once per event, on this device */
function sbBand() {""")
rep("else for (const k2 in SBW) { const nx = sbNext(k2, T); if (nx - T < 72 * SB_H) { const D = SBW[k2]; html =",
    "else for (const k2 in SBW) { const nx = sbNext(k2, T); if (nx - T < 72 * SB_H) { annOnce(\"sb\" + k2, nx, SB_SOON[k2]); const D = SBW[k2]; html =")
rep('else if (nx - T < 72 * 3600e3) html = `<button class="omb soon"', 'else if (nx - T < 72 * 3600e3) { annOnce("dv", nx, DV_SOON); } if (!live && nx - T < 72 * 3600e3) html = `<button class="omb soon"')
rep("  let scl = D.sc * Math.max(.001, 1 - Math.pow(1 - arr, 3)); const dead = st.dead && st.dead < T, df = dead ? (T - st.dead) / 1000 : 0;",
    "  let scl = D.sc * Math.max(.001, 1 - Math.pow(1 - arr, 3)); const dead = st.dead && st.dead < T, df = dead ? (T - st.dead) / 1000 : 0;\n  { const ph = sbPhase(k, st.hp); if (st.hp && ph > 0 && e > 600) say(k + s0 + \"p\" + ph, SBL[k][ph]); } if (dead && k === \"vae\") say(k + st.dead + \"x\", \"Vaelthar has fallen! The wheel collapses. A celestial relic drifts where it died.\");")
rep('if (res === "interrupted" && f > .58) say(k + ce + "i", "The charge collapsed! Its core is exposed: strike now!"); }',
    'if (res === "interrupted" && f > .58) say(k + ce + "i", "The charge collapsed! Its core is exposed: strike now!"); if (res !== "interrupted" && f > .66 && f < .9) say(k + ce + "f", "It\'s firing! Divine Annihilation is sweeping across the galaxy!"); }')
s = re.sub(r"GAME_V = 455\b", "GAME_V = 456", s)
open(P, 'w').write(s)
