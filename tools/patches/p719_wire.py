# v719 (owner): "Can we update omega cube event music, don't we have a song we made?" The whole Cube Devastation (the migration,
# the puzzle, the giant cube, the Last Stand and the Omega fight) and its preview now play our choral/orchestral piece
# (tools/orch_theme.py, made in v438 and unused since v439) as docs/music_cube.mp3. The boss theme stays for the super bosses.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# the boss theme no longer covers the Cube (and yields to it); the Convergence theme yields to it too
rep("if (G.sbSim || G.dvSim) return true; const k = sbLiveKey(); return !!(k && sbOn(k)) || omOn(); } catch (e) { return false; } }",
    "if (cubeWant()) return false; if (G.sbSim) return true; const k = sbLiveKey(); return !!(k && sbOn(k)); } catch (e) { return false; } }")
rep("if (!AU.ctx || !AU.musicOn || AU.muted || document.hidden || bossWant()) return null;",
    "if (!AU.ctx || !AU.musicOn || AU.muted || document.hidden || bossWant() || cubeWant()) return null;")
rep("AU.cduck = AU.conv ? 0 : 1; applyAudio(); } return; }", "AU.cduck = AU.conv || AU.cube ? 0 : 1; applyAudio(); } return; }")
rep("AU.cduck = AU.boss ? 0 : 1; applyAudio(); } return; }", "AU.cduck = AU.boss || AU.cube ? 0 : 1; applyAudio(); } return; }")
rep("for (const X of [AU.boss, AU.conv]) if (X && X.el.paused)", "for (const X of [AU.boss, AU.conv, AU.cube]) if (X && X.el.paused)")
CUBE = r'''
/* v719 the Cube Devastation's own theme: the choral/orchestral piece, for the whole event and its preview */
function cubeWant() { try { if (!AU.ctx || !AU.musicOn || AU.muted || document.hidden || !G.ready) return false; return !!(G.dvSim || dvNow(now())); } catch (e) { return false; } }
function cubeTheme() { const c = AU.ctx; if (!c) return;
  if (!cubeWant()) { if (AU.cube) { const B = AU.cube; AU.cube = null; B.out.gain.setTargetAtTime(0, c.currentTime, .9); setTimeout(() => { try { if (!(AU.cube && AU.cube.el === B.el)) B.el.pause(); } catch (e) {} try { B.out.disconnect(); } catch (e) {} }, 4500); AU.cduck = AU.conv || AU.boss ? 0 : 1; applyAudio(); } return; }
  if (!AU.cube) { let el = AU.cubeEl; if (!el) { el = AU.cubeEl = new Audio("music_cube.mp3?v=719"); el.loop = true; el.preload = "auto"; try { AU.cubeSrc = c.createMediaElementSource(el); } catch (e) { AU.cubeSrc = null; } }
    const out = c.createGain(); out.gain.value = 0; out.connect(AU.master); if (AU.cubeSrc) { try { AU.cubeSrc.disconnect(); } catch (e) {} AU.cubeSrc.connect(out); } try { el.currentTime = 0; } catch (e) {} el.play().catch(() => {}); AU.cube = { out, el }; AU.cduck = 0; applyAudio(); }
  const vv = .11 * gainOf(AU.mv) / gainOf(50) * (AU.duck || 1); AU.cube.out.gain.setTargetAtTime(vv, c.currentTime, AU.cube.on ? .3 : 1.6); if (!AU.cubeSrc) AU.cube.el.volume = clamp(vv * 8, 0, 1); AU.cube.on = 1;
  if (AU.cube.el.paused && !AU.cube.tried) { AU.cube.tried = 1; AU.cube.el.play().catch(() => { AU.cube.tried = 0; }); } }
setInterval(() => { try { cubeTheme(); } catch (e) {} }, 1000);'''
a = "setInterval(() => { try { bossTheme(); } catch (e) {} }, 1000);"
rep(a, a + CUBE)
rep('const GAME_V = 718;', 'const GAME_V = 719;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
