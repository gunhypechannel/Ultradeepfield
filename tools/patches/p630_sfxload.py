# v630: no round gong; recorded sounds load wherever the game runs (owner: "Sounds not fixed" ... "Just in battle simulation").
# Each file is tried with its ?v= tag and, if that fails (the claude.ai artifact's file host), without it; a reply that is
# the game's HTML page is refused; and missing sounds are fetched again at the start of every battle instead of once a session.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('  SB.f = SB.f || {}; for (const k of Object.keys(SFX_F)) fetch(`sfx/${k}.mp3?v=621`).then(r => r.ok ? r.arrayBuffer() : null).then(ab => ab && new Promise((ok, no) => c.decodeAudioData(ab, ok, no))).then(b => { if (b) SB.f[k] = [b]; }).catch(() => {}); /* v620 the recorded sounds */\n}',
    '  sfxLoadF(); /* v620 the recorded sounds (v630 loader) */\n}\n'
    'function sfxGet(path, v) { const go = u => fetch(u).then(r => r.ok && !/html/.test(r.headers.get("content-type") || "") ? r.arrayBuffer() : Promise.reject(r.status));\n'
    '  return go(path + "?v=" + v).catch(() => go(path)).then(ab => new Promise((ok, no) => AU.ctx.decodeAudioData(ab, ok, no))); }\n'
    'function sfxLoadF() { if (!AU.ctx) return; SB.f = SB.f || {}; SB.fTry = SB.fTry || {}; const T = performance.now(); for (const k of Object.keys(SFX_F)) { if (SB.f[k] || T - (SB.fTry[k] || -1e9) < 8000) continue; SB.fTry[k] = T; sfxGet(`sfx/${k}.mp3`, 621).then(b => { SB.f[k] = [b]; }).catch(e => { try { crumb("sfx load failed: " + k + " " + e); } catch (er) {} }); } }')
rep('function wsLoad() { if (!AU.ctx || WBUF._l) return; WBUF._l = 1; for (const k in WSND) fetch(`sfx/w_${k}.mp3?v=625`).then(r => r.ok ? r.arrayBuffer() : null).then(ab => ab && new Promise((ok, no) => AU.ctx.decodeAudioData(ab, ok, no))).then(b => { if (b) WBUF[k] = b; }).catch(() => {}); }',
    'function wsLoad() { if (!AU.ctx) return; const T = performance.now(); WBUF._t = WBUF._t || {}; for (const k in WSND) { if (WBUF[k] || T - (WBUF._t[k] || -1e9) < 8000) continue; WBUF._t[k] = T; sfxGet(`sfx/w_${k}.mp3`, 625).then(b => { WBUF[k] = b; }).catch(() => {}); } } /* v630 */')
rep('sbPrep(); SFX.att = 1;', 'sbPrep(); sfxLoadF(); SFX.att = 1;')
# no gong at each new battle round (owner: "I never asked for that round gong sound")
rep('b.roundShown = rnd_; b.roundAt = t; if (rnd_ > 1) SFX.round(); }', 'b.roundShown = rnd_; b.roundAt = t; } /* v630 no round gong */')
s2 = re.sub(r"GAME_V = 629\b", "GAME_V = 630", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
