# v457 the boss battle theme (tools/battle_theme.py -> docs/music_boss.mp3): an original driving battle piece that plays while a super boss
# (Vaelthar, Aexion) is live and still standing, while Cube Devastation's fight is on, and during the owner's previews of either. It takes
# over from the main song and from the Convergence theme, streamed and looped the same way, and fades out when the fight ends.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep("function convWant() { if (!AU.ctx || !AU.musicOn || AU.muted || document.hidden) return null;",
    "function convWant() { if (!AU.ctx || !AU.musicOn || AU.muted || document.hidden || bossWant()) return null;")
rep("setTimeout(() => { try { if (!(AU.conv && AU.conv.el === C.el)) C.el.pause(); } catch (e) {} try { C.out.disconnect(); } catch (e) {} }, 4000); AU.cduck = 1; applyAudio(); } return; }",
    "setTimeout(() => { try { if (!(AU.conv && AU.conv.el === C.el)) C.el.pause(); } catch (e) {} try { C.out.disconnect(); } catch (e) {} }, 4000); AU.cduck = AU.boss ? 0 : 1; applyAudio(); } return; }")
rep("setInterval(() => { try { convTheme(); } catch (e) {} }, 1000);",
"""setInterval(() => { try { convTheme(); } catch (e) {} }, 1000);
function bossWant() { try { if (!AU.ctx || !AU.musicOn || AU.muted || document.hidden || !G.ready) return false; if (G.sbSim || G.dvSim) return true; const k = sbLiveKey(); return !!(k && sbOn(k)) || omOn(); } catch (e) { return false; } }
function bossTheme() { const c = AU.ctx; if (!c) return; /* v457 the boss battle theme */
  if (!bossWant()) { if (AU.boss) { const B = AU.boss; AU.boss = null; B.out.gain.setTargetAtTime(0, c.currentTime, .9); setTimeout(() => { try { if (!(AU.boss && AU.boss.el === B.el)) B.el.pause(); } catch (e) {} try { B.out.disconnect(); } catch (e) {} }, 4500); AU.cduck = AU.conv ? 0 : 1; applyAudio(); } return; }
  if (!AU.boss) { let el = AU.bossEl; if (!el) { el = AU.bossEl = new Audio("music_boss.mp3?v=457"); el.loop = true; el.preload = "auto"; try { AU.bossSrc = c.createMediaElementSource(el); } catch (e) { AU.bossSrc = null; } }
    const out = c.createGain(); out.gain.value = 0; out.connect(AU.master); if (AU.bossSrc) { try { AU.bossSrc.disconnect(); } catch (e) {} AU.bossSrc.connect(out); } try { el.currentTime = 0; } catch (e) {} el.play().catch(() => {}); AU.boss = { out, el }; AU.cduck = 0; applyAudio(); }
  const vv = .12 * gainOf(AU.mv) / gainOf(50) * (AU.duck || 1); AU.boss.out.gain.setTargetAtTime(vv, c.currentTime, AU.boss.on ? .3 : 1.2); if (!AU.bossSrc) AU.boss.el.volume = clamp(vv * 8, 0, 1); AU.boss.on = 1;
  if (AU.boss.el.paused && !AU.boss.tried) { AU.boss.tried = 1; AU.boss.el.play().catch(() => { AU.boss.tried = 0; }); } }
setInterval(() => { try { bossTheme(); } catch (e) {} }, 1000);""")
rep("  if (AU.ctx.state !== \"running\") AU.ctx.resume().catch(() => {});\n",
    "  if (AU.ctx.state !== \"running\") AU.ctx.resume().catch(() => {});\n  for (const X of [AU.boss, AU.conv]) if (X && X.el.paused) X.el.play().catch(() => {}); /* v457 the event themes start inside a tap too */\n")
s = re.sub(r"GAME_V = 456\b", "GAME_V = 457", s)
open(P, 'w').write(s)
