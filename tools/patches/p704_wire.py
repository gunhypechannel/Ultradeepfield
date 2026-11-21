# v704: Tide of the Carcinid, complete (weeks 2-4, the Claw Admirals, the Deep Guardians, the Abyssal Crown and the Great Molting,
# the six Abyssal tactics, eight materials, the Abyssal Forge, reward track and cosmetics, the wild Kraken), and every Carcinid model
# rebuilt after the owner's paintings. See p704_crc.js and p704_crcm.js.
import sys, os, re
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__)); R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
def block(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i); assert s.count(a) == 1; s = s[:i] + new + s[j:]

# the models and battle tables
block('/* ---------- v703 the Carcinid on the battle screen and the map', 'function mimAtkAdd(b, v) {', R('p704_crcm.js').rstrip('\n') + '\n')
# the battle portrait turns the crabs three-quarters toward us (the face, the fangs and both pincers, as in the paintings) and the ships a little
rep('try { if (MIM_ATK[(b.Q[v.s] || {}).k]) mimAtkAdd(b, v); } catch (e) {} /* v676 */', 'try { if (MIM_ATK[(b.Q[v.s] || {}).k]) mimAtkAdd(b, v); } catch (e) {} /* v676 */ try { crcAtkAdd(b, v); crcShAdd(b, v); } catch (e) {} /* v704 */')
rep('try { mimAtkDraw(ctx, b, scr, T, W, d, lo, t, H); } catch (e) {} /* v676, v677 */', 'try { mimAtkDraw(ctx, b, scr, T, W, d, lo, t, H); } catch (e) {} /* v676, v677 */ try { crcAtkDraw(ctx, b, scr, T, W, d, lo, t); } catch (e) {} /* v704 */')
rep('if ((kind === "d" || kind === "m") && view === "side") ship.rotation.y = -.5;', 'if ((kind === "d" || kind === "m") && view === "side") ship.rotation.y = -.5; if (view === "side" && kind === "a" && typeof CRC_FACE !== "undefined" && CRC_FACE[k]) ship.rotation.y = CRC_FACE[k]; /* v704 */')
if os.path.exists(os.path.join(D, 'p704_crc.js')):
    block('/* ---------- v703 TIDE OF THE CARCINID, phase 1', 'const PIRATES = PIRATES_ALL', R('p704_crc.js').rstrip('\n') + '\n')
    exec(R('p704_hooks.py'))
rep('const GAME_V = 703;', 'const GAME_V = 704;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
