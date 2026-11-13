# v508 the Advisor reads the whole record (owner: she should read all the archive lines): on any recovered record one button has
# her read the fragment, then (once interpreted) the modern interpretation and her commentary, then her account of the encounter;
# tap it again to stop her. Every line is voiced.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('${lv >= 2 && (E.enc.length || E.def.length) ? `<button class="btn ghost wide" data-act="archPlay" data-id="${id}">🔊 Hear the Advisor\'s account</button>` : ""}',
    '<button class="btn ghost wide" data-act="archPlay" data-id="${id}">${G.archRd === id ? "■ Stop reading" : "🔊 Have the Advisor read this record"}</button>')
rep('archPlay: d => { const E = ARCH[d.id]; if (E) archSeq(E.enc.concat(E.def)); },',
    '''archPlay: d => { const E = ARCH[d.id], lv = archLv(d.id); G.archTok = (G.archTok || 0) + 1; if (G.archRd === d.id || !E || !lv) { G.archRd = null; try { voiceStop(); } catch (e) {} const h = $("#advh"); if (h) h.classList.remove("on"); if (sheet && sheet.type === "archives") renderSheet(); return; }
    G.archRd = d.id; const L = [archFragLine(E)].concat(lv >= 2 ? [E.interp, E.adv] : [], E.enc, lv >= 2 ? E.def : []); archSeq(L, G.archTok, () => { if (G.archRd === d.id) { G.archRd = null; if (sheet && sheet.type === "archives") renderSheet(); } }); if (sheet && sheet.type === "archives") renderSheet(); },''')
rep('function archSeq(L) { let i = 0, tries = 0; const step = () => { if (i >= L.length) return;', 'const archFragLine = E => E.frag.replace(/^…/, "").replace(/…$/, "..."); /* v508 the fragment as she reads it */\nfunction archSeq(L, tok, done) { let i = 0, tries = 0; const step = () => { if (tok && tok !== G.archTok) return; if (i >= L.length) { if (done) done(); return; }')
s2 = re.sub(r"GAME_V = 507\b", "GAME_V = 508", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
