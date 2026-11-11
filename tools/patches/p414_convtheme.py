# v414 (2): the Convergence theme is the game's own song, reworked (tools/conv_theme.py): the loud part played 3 semitones deeper and
# slower, a long dark hall, a sub drone on the new root, deep brass "braams" and taiko hits timed to the song's own kicks, looped. It
# replaces the synthesised element layers. While it plays the game song is muted (cduck 0); it follows the music volume and the Advisor's
# ducking, fades in over a few seconds and out when the event view ends. Loaded only the first time it is needed (music_conv.mp3, 2.2 MB).
p = "docs/index.html"; t = open(p).read()
i = t.index("function convTheme() { const want = convWant(), c = AU.ctx; if (!c) return;"); j = t.index("setInterval(() => { try { convTheme(); } catch (e) {} }, 1000);")
t = t[:i] + """function convTheme() { const want = convWant(), c = AU.ctx; if (!c) return; /* v414 the game's song, reworked deeper and cinematic */
  if (!want) { if (AU.conv) { const C = AU.conv; AU.conv = null; C.out.gain.setTargetAtTime(0, c.currentTime, .8); setTimeout(() => { try { C.src.stop(); } catch (e) {} try { C.out.disconnect(); } catch (e) {} }, 4000); AU.cduck = 1; applyAudio(); } return; }
  if (!AU.convBuf) { if (!AU.convLd) { AU.convLd = 1; fetch("music_conv.mp3").then(r => { if (!r.ok) throw 0; return r.arrayBuffer(); }).then(b => c.decodeAudioData(b)).then(b => { AU.convBuf = b; }, () => { setTimeout(() => { AU.convLd = 0; }, 60000); }); } return; }
  if (!AU.conv) { const out = c.createGain(); out.gain.value = 0; out.connect(AU.master); const src = c.createBufferSource(); src.buffer = AU.convBuf; src.loop = true; src.connect(out); src.start(); AU.conv = { out, src }; AU.cduck = 0; applyAudio(); }
  AU.conv.out.gain.setTargetAtTime(AU.musicOn && !AU.muted ? .12 * gainOf(AU.mv) / gainOf(50) * (AU.duck || 1) : 0, c.currentTime, AU.conv.on ? .3 : 2); AU.conv.on = 1; }
""" + t[j:]
n = t.count("(AU.cduck || 1)"); assert n == 2, n; t = t.replace("(AU.cduck || 1)", "(AU.cduck == null ? 1 : AU.cduck)") # 0 must mute the song
open(p, "w").write(t); print("ok")
