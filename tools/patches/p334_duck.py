import sys
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# v334 (owner's request) the music dips while the Advisor speaks and fades back in after her line
rep('''AU.mus.gain.setTargetAtTime(AU.musicOn ? .1 * gainOf(AU.mv) / gainOf(50) : 0, t, .15);''',
    '''AU.mus.gain.setTargetAtTime(AU.musicOn ? .1 * gainOf(AU.mv) / gainOf(50) * (AU.duck || 1) : 0, t, AU.duck < 1 ? .12 : AU.ducked ? .55 : .15); AU.ducked = AU.duck < 1; // v334: ducked under the Advisor's voice''')
rep('''if (AU.direct) AU.file.volume = clamp((AU.muted ? 0 : gainOf(AU.vol) * 1.45) * (.1 * gainOf(AU.mv) / gainOf(50)) * 1.6, 0, 1);''',
    '''if (AU.direct) AU.file.volume = clamp((AU.muted ? 0 : gainOf(AU.vol) * 1.45) * (.1 * gainOf(AU.mv) / gainOf(50)) * 1.6 * (AU.duck || 1), 0, 1);''')
rep('''function voiceTalk(on) { const a = $("#adv"); if (a) a.classList.toggle("talk", !!on); }''',
    '''function voiceTalk(on) { const a = $("#adv"); if (a) a.classList.toggle("talk", !!on); if (typeof AU !== "undefined") { const d = on ? .22 : 1; if (AU.duck !== d) { AU.duck = d; try { applyAudio(); } catch (e) {} } } } // v334: music dips under her voice''')
rep('''a.onplay = () => voiceTalk(1); a.onended = a.onpause = () => voiceTalk(0);''', '''a.onplay = () => voiceTalk(1); a.onended = a.onpause = a.onerror = () => voiceTalk(0);''')
open(p, 'w', encoding='utf-8', newline='').write(t); print('ok')
