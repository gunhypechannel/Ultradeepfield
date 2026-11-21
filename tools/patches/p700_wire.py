# v700: the Titan Chronicles (see p700_tch.js)
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__)); R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('{ const i = ARCH_ORD.indexOf("krk"); if (i >= 0) ARCH_ORD.splice(i, 1); } /* the Kraken is retired: its card can no longer be found */',
    '{ const i = ARCH_ORD.indexOf("krk"); if (i >= 0) ARCH_ORD.splice(i, 1); } /* the Kraken is retired: its card can no longer be found */\n' + R('p700_tch.js').rstrip('\n'))
rep('[bslecoahdxm]_', '[bslecoahdxmt]_', 2)
rep('[bslecoahdx]_', '[bslecoahdxt]_')
rep('function addReport(rep) { battleXP(rep);', 'function addReport(rep) { try { tchRep(rep); } catch (e) {} /* v700 */ battleXP(rep);')
rep('out.push({ k, n: n[k], atk: s.atk, sh: s.sh,', 'out.push({ k, n: n[k], atk: k === "harbinger" && own && own === G.me && S ? s.atk * tchHarbK() : s.atk /* v700 the Harbinger bound or awake */, sh: s.sh,')
rep('function shArch() { const id = sheet.id; S.archR = S.archR || {};', 'function shArch() { const id = sheet.id; S.archR = S.archR || {}; if (id === "t_h5" && archLv(id) === 1 && !(S.choices && S.choices.harb)) return tchChoiceHTML(); /* v700 */')
rep('for (const k of ["warden", "pdata", "signal", "queen"])', 'for (const k of ["warden", "pdata", "signal", "queen", "harb"])')
rep('const STRAIN_W = { titans: 3,', 'const STRAIN_W = { harb: { bind: -3, wake: 4 } /* v700 */, titans: 3,')
rep('setTimeout(() => { try { sbSay(ECL_SAY[v][1]); } catch (er) {} }, 15000); }', 'setTimeout(() => { try { sbSay(ECL_SAY[v][1]); } catch (er) {} }, 15000); if (S && S.choices && S.choices.harb === "wake") setTimeout(() => { try { sbSay(TCH_JUDGE); } catch (er) {} }, 30000); /* v700 */ }')
rep('  cineOff: () => cineEnd(),', '  cineOff: () => cineEnd(), tchChoose: d => tchChoose(d.v), /* v700 */')
rep('#app.cine #cubepanel{display:none}', '''#app.cine #cubepanel{display:none}
.tchch{display:flex;flex-direction:column;gap:10px;margin:14px 0 6px;flex:none}.tchb{display:flex;flex-direction:column;gap:4px;text-align:left;padding:14px;border-radius:14px;border:1px solid var(--line);background:rgba(10,22,34,.6);color:inherit;cursor:pointer}.tchb b{font-size:16px}.tchb small{color:var(--muted);font-size:12.5px}.tchb span{font-size:13px}
.tchb.bind{border-color:rgba(120,200,255,.5)}.tchb.bind b{color:#9fd8ff}.tchb.wake{border-color:rgba(61,255,154,.45);background:linear-gradient(180deg,rgba(40,90,60,.35),rgba(10,22,34,.6))}.tchb.wake b{color:#3dff9a}.tchb[disabled]{opacity:.5;cursor:not-allowed}''')
rep('function archImg(E, lv, k) {', 'function archImg(E, lv, k) { if (/^t_/.test(k)) return archImg(E, lv, "s_" + (TCH_K[k[2]] || "harbinger")); /* v700 a chronicle shows its Titan */')
rep('"scb": ["That tractor beam is dragging whole squadrons in. Nothing should pull that hard.", ', '"scb": ["The archives warned us about this. Seeing it is something else.", "That tractor beam is dragging whole squadrons in. Nothing should pull that hard.", ') # v700 the owner's replacement lines (v699 removed the wrong ones)
rep('"omg": ["Cubes are pouring off it', '"omg": ["It\'s bigger than a planet, and it\'s still growing. This is insane.", "Cubes are pouring off it')
rep('const GAME_V = 699;', 'const GAME_V = 700;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
