# v722 (owner: "Build it, It def needs a overhaul in battle simulation"): the Celestial Serpent's battle overhaul and its storyline
# (p722_serp.js + p722_case.js on v721's monster attacks).
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__))
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
# the Serpent alternates Coil Strike and Constrict; after shedding it strikes more often
rep("function beastAtkAdd(b, v) { const q = b.Q[v.s]; if (!q) return; const a = BEAST_ATK[q.k];", "function beastAtkAdd(b, v) { const q = b.Q[v.s]; if (!q) return; let a = BEAST_ATK[q.k];")
rep("v.t - last[v.s] < Math.max(2.4, BEAST_DUR[a] * 1.2)) return; /* a rewound replay starts over */ last[v.s] = v.t;\n  L.push({ s: v.s, e: v.e, t0: v.t, a,",
    "v.t - last[v.s] < Math.max(b.shed && b.shed[v.s] ? 1.5 : 2.4, BEAST_DUR[a] * 1.2)) return; /* a rewound replay starts over */ last[v.s] = v.t;\n  let e = v.e; if (q.k === \"cserp\") { const e2 = serpPick(b, v, q); if (e2 != null) { a = \"constrict\"; e = e2; } } /* v722 */\n  L.push({ s: v.s, e, t0: v.t, a,")
rep('case "coil": f = u < .45', 'case "constrict": f = u < .2 ? 1.1 * u / .2 : u < .8 ? 1.1 : 1.1 * (1 - (u - .8) / .2); break; /* v722 */\n        case "coil": f = u < .45')
rep('      case "fist": {', R('p722_case.js') + '      case "fist": {')
# the module, before the monster attack draw is used
rep("function beastAtkDraw(ctx, b, scr, T, W, d, lo, t) {", R('p722_serp.js') + "\nfunction beastAtkDraw(ctx, b, scr, T, W, d, lo, t) {")
rep("try { beastAtkDraw(ctx, b, scr, T, W, d, lo, t); } catch (e) {} /* v721 */", "try { beastAtkDraw(ctx, b, scr, T, W, d, lo, t); } catch (e) {} /* v721 */ try { serpDraw(ctx, b, scr, T, W, d, lo, t); } catch (e) {} /* v722 */")
# no tumbling wreck for a dying Serpent (it dissolves into light instead); faster after it sheds
rep("if (dying && b.wreckd && b.wreckd[i]) return;", "if (dying && b.wreckd && b.wreckd[i]) return; if (dying && q.k === \"cserp\") return; /* v722 */")
rep("* (moving ? 1.35 : 1) * (MIM_D[k] ? .5 : 1)) % 1;", "* (moving ? 1.35 : 1) * (MIM_D[k] ? .5 : 1) * (b.shed && b.shed[i] ? 1.6 : 1)) % 1; /* v722 */")
# the storyline counts hatchlings from each won report
rep("function archFromRep(r) { try { if (!r) return;", "function archFromRep(r) { try { serpStory(r); } catch (e) {} /* v722 */ try { if (!r) return;")
rep("function addReport(rep) { try { tchRep(rep); } catch (e) {} /* v700 */", "function addReport(rep) { try { tchRep(rep); } catch (e) {} /* v700 */ try { serpStory(rep); } catch (e) {} /* v722 */")
rep('const GAME_V = 721;', 'const GAME_V = 722;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
