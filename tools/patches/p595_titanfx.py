# v595 the Sovereign Ark and the Eclipse Harbinger, remastered firing (see p595_titanfx.js)
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# the abilities: the Ark's strike wing and the Harbinger's swarm become staged shots; a hidden volley lands the damage
rep('  if (v.ab === "wing" || v.ab === "swarm") { const sw = v.ab === "swarm",',
    '''  if ((v.ab === "wing" && q.k === "sovereign") || (v.ab === "swarm" && q.k === "harbinger")) { const sw = v.ab === "swarm"; /* v595 */
    b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: sw ? "HS" : "SW", charge: 0, life: sw ? 1.9 : 2.2, seed: hash(v.t + "|" + v.s) % 997 }); b.fx.push({ t0: v.t, t1: v.t + (sw ? 1.05 : 1.1), v, last: true, first: true, n: 1, mis: false, ic: false, side, off: 0, hv: 0, sz, j: 0, hide: 1 });
    try { if (sw) SFX.swarm && SFX.swarm(10, 0); else SFX.charge && SFX.charge(); } catch (e) {} return true; }
  if (v.ab === "wing" || v.ab === "swarm") { const sw = v.ab === "swarm",''')
rep('if (q.k === "sovereign" && main) { b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: "l", charge: 0, life: .45 }); b.fx.push(Object.assign({}, hid, { t0: v.t, t1: v.t + .1 })); return true; }',
    'if (q.k === "sovereign" && main) { b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: "SL", charge: 0, life: .9, seed: hash(v.t + "|" + v.s) % 997 }); b.fx.push(Object.assign({}, hid, { t0: v.t, t1: v.t + .32 })); return true; } /* v595 */')
rep('if (q.k === "harbinger" && main) { b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: "p", charge: 0, life: .7 }); b.fx.push(Object.assign({}, hid, { t0: v.t, t1: v.t + .6 })); return true; }',
    'if (q.k === "harbinger" && main) { b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: "HP", charge: 0, life: 1.45, seed: hash(v.t + "|" + v.s) % 997 }); b.fx.push(Object.assign({}, hid, { t0: v.t, t1: v.t + .92 })); try { SFX.charge && SFX.charge(); } catch (e) {} return true; } /* v595 */')
rep('if (q.k === "harbinger" && pd) { b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: "t", charge: 0, life: .4 }); b.fx.push(Object.assign({}, hid, { t0: v.t, t1: v.t + .15 })); return true; }',
    'if (q.k === "harbinger" && pd) { b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: "HT", charge: 0, life: .42 }); b.fx.push(Object.assign({}, hid, { t0: v.t, t1: v.t + .15 })); return true; } /* v595 */')
rep('function titanBeamDraw(ctx, b, m, age, scr, W, d, lo, T) { const S0 = scr[m.s], E0 = scr[m.e]; if (!S0) return;',
    'function titanBeamDraw(ctx, b, m, age, scr, W, d, lo, T) { if (m.ti.length === 2) return tx595Draw(ctx, b, m, age, scr, W, d, lo, T); /* v595 */ const S0 = scr[m.s], E0 = scr[m.e]; if (!S0) return;')
i = s.index('function titanBeamDraw('); s = s[:i] + open('tools/patches/p595_titanfx.js', encoding='utf-8').read() + s[i:]
s2 = re.sub(r"GAME_V = 594\b", "GAME_V = 595", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
