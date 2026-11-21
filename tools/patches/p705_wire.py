# v705: the Carcinid bosses each get their own silhouette (crests, reef, pearl crown, halo and floating eye, city, crystals, kraken arms,
# a molting shell), and the Advisor speaks through the Carcinid war (p705_vo.js; clips in docs/voice).
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__)); R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
def block(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i); assert s.count(a) == 1; s = s[:i] + new + s[j:]
block('/* ---------- v703/v704 the Carcinid on the battle screen and the map', 'function mimAtkAdd(b, v) {', R('p704_crcm.js').rstrip('\n') + '\n')
rep('Object.assign(AWE, AWE_MIM);', 'Object.assign(AWE, AWE_MIM);\n' + R('p705_vo.js').rstrip('\n'))
rep('if (ks.some(k => /^momega/.test(k))) return "momega";', '{ const c = crcVoiceKey(ks); if (c) return c; } /* v705 */ if (ks.some(k => /^momega/.test(k))) return "momega";')
rep('try { SFX.gong(); } catch (e) {} setTimeout(tick, 900); w.addEventListener("click", () => { if (n < q.length) n = q.length - 1;',
    'try { SFX.gong(); } catch (e) {} setTimeout(tick, 900); setTimeout(() => { try { if (document.body.contains(w)) sbSay(CRC_SAY["cine_" + k]); } catch (e) {} }, 2600); /* v705 */ w.addEventListener("click", () => { if (n < q.length) n = q.length - 1;')
rep('const GAME_V = 704;', 'const GAME_V = 705;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
