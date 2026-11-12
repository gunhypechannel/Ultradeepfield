# v488 (owner: "when a super boss dies it should drop a single glyph symbol with matching color, disappears after a few hours").
# The glyph a boss leaves takes its own colour (its crystal colour, SB_CRY; Aexion's is ice blue), and a super boss's glyph stays on the
# map for 3 hours after it falls (the hunt's map presence lasts that long), fading out over the last 10 minutes. Khezaroth leaves its
# glyph (no relic) once its implosion is over.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep("const sbLiveKey = (T = now()) => { for (const k in SBW) { const s0 = sbStartOf(k, T); if (s0 != null && T >= s0 && T < sbEnd(k, s0) + 10 * 60e3) return k; } return null; };",
    "const SB_GLY = 3 * SB_H; /* v488 a fallen super boss's glyph stays this long */\nconst sbGlyEnd = (k, s0) => { const st = sbState(k, s0); return st.dead && st.dead > s0 ? st.dead + SB_GLY : 0; };\nconst sbLiveKey = (T = now()) => { for (const k in SBW) { const s0 = sbStartOf(k, T); if (s0 != null && T >= s0 && T < Math.max(sbEnd(k, s0) + 10 * 60e3, sbGlyEnd(k, s0))) return k; } return null; };")
rep("function sbGlyph(W, X, e, t) { if (e < 0) { if (X.gly) X.gly.g.visible = false; return; }", "function sbGlyph(W, X, e, t, fade = 1) { if (e < 0 || fade <= 0) { if (X.gly) X.gly.g.visible = false; return; }")
rep("const tex = new TH.CanvasTexture(cv), col = new TH.Color(EL[1]), g = new TH.Group();", "const CY = X.key && (SB_CRY[X.key] || (X.key[0] === \"c\" && /^c\\d$/.test(X.key) ? SB_CRY.con : null)), col = CY ? new TH.Color(...CY[1]).lerp(new TH.Color(...CY[0]), .3) : new TH.Color(EL[1]); if (CY) EL[2] = CY[1].map((v, i) => Math.min(1, v * .6 + CY[0][i] * .6)); /* v488 its own colour */\n    const tex = new TH.CanvasTexture(cv), g = new TH.Group();")
rep("Z.Cc.material.opacity = k * fl; Z.glow.material.opacity = .35 * k * (.8 + .2 * Math.sin(t * .004));", "Z.Cc.material.opacity = k * fl * fade; Z.glow.material.opacity = .35 * k * fade * (.8 + .2 * Math.sin(t * .004));")
rep("const f = k * (1 - u0 * .6);", "const f = k * fade * (1 - u0 * .6);")
rep("con: [[.6, .4, .95], [.9, .85, 1]], epx: [[.6, .5, .8], [1, .95, 1]], khz: [[.45, .16, .85], [.92, .78, 1]] };", "con: [[.6, .4, .95], [.9, .85, 1]], epx: [[.6, .5, .8], [1, .95, 1]], khz: [[.45, .16, .85], [.92, .78, 1]], aex: [[.2, .5, 1], [.75, .92, 1]] };")
# the super bosses' glyphs fade out at the end of their 3 hours
rep("if (dead) { const be = df - 2; X.glySeed = st.dead; sbGlyph(W, X, be - 10.5, t);", "if (dead) { const be = df - 2; X.glySeed = st.dead; sbGlyph(W, X, be - 10.5, t, clamp((st.dead + SB_GLY - T) / 600e3, 0, 1));")
rep("if (k === \"vae\" && dead) { vf = df - .8; X.glySeed = st.dead; sbGlyph(W, X, vf - 6.2, t);", "if (k === \"vae\" && dead) { vf = df - .8; X.glySeed = st.dead; sbGlyph(W, X, vf - 6.2, t, clamp((st.dead + SB_GLY - T) / 600e3, 0, 1));")
# Khezaroth: its glyph, not a relic
rep('if (dead) { const dd = df / 10; b.drive("die", dd < 1 ? dd : -1); b.relic = dd >= 1 ? 1 : 0; b.anchOn = 0; if (dd < 2) say(k + st.dead + "x", "Its singularity is collapsing... Khezaroth is breaking apart! It\'s imploding!"); if (dd > 1.2 && dd < 8) say(k + st.dead + "r", "It\'s gone. Only a relic of the sphinx is left, drifting where it fell."); } else b.relic = 0; }',
    'b.relic = 0; if (dead) { const dd = df / 10; b.drive("die", dd < 1 ? dd : -1); b.anchOn = 0; X.glySeed = st.dead; sbGlyph(W, X, df - 9, t, clamp((st.dead + SB_GLY - T) / 600e3, 0, 1)); if (dd < 2) say(k + st.dead + "x", "Its singularity is collapsing... Khezaroth is breaking apart! It\'s imploding!"); if (dd > 1.2 && dd < 8) say(k + st.dead + "r", "It\'s gone. Only its glyph is left, burning where it fell."); } }')
rep('if (X.fall) { const dd = (s - X.fall) / 10; b.drive("die", dd < 1 ? dd : -1); b.relic = dd >= 1 ? 1 : 0; b.anchOn = 0; b.drive("heart", -1); if (dd > 1.1) say("k8", "It\'s gone. Only a relic of the sphinx is left, drifting where it fell."); }',
    'if (X.fall) { const dd = (s - X.fall) / 10; b.drive("die", dd < 1 ? dd : -1); b.anchOn = 0; b.drive("heart", -1); sbGlyph(W, X, s - X.fall - 9, t); if (dd > 1.1) say("k8", "It\'s gone. Only its glyph is left, burning where it fell."); }')
rep('k === "khz" ? "An ancient sphinx relic drifts where it fell."', 'k === "khz" ? "Its glyph burns where it fell, for a few hours."')
open(P, 'w').write(s)
# the Cube Devastation countdown hologram (it rides the rim in front of the camera) no longer floats over a live super boss
s = open(P).read()
a = 'function dvCountdown(W, t, T, live) { const show = !live && view === "galaxy" && !G.sbSim;'
assert s.count(a) == 1; s = s.replace(a, 'function dvCountdown(W, t, T, live) { const show = !live && view === "galaxy" && !G.sbSim && !sbLiveKey(T); /* v488 */')
open(P, 'w').write(s)
