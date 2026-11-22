# v724 (owner: "Build it all", the eggs ideas): eggs phase 1 (p724_eggs.js + p724_eggs.css): the egg reveal, rarity reactions,
# tap to warm, the hatching cinematic and mystery traits.
import sys, os, re
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__))
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
a = "@media (prefers-reduced-motion:reduce){.xsegg.pr,.xsinc.ready .xsegg,.xscr.pr .xsart img{animation:none}}"
rep(a, a + "\n" + R('p724_eggs.css'))
a = "const xsRe = () => { if (sheet) renderSheet(); else render(true); };"
rep(a, a + "\n" + R('p724_eggs.js'))
# traits raise the element bonus; Lucky raises the drop chance; Swift shortens the breeding rest
rep("if (D && D[0] === e) v += XR[D[1]][3] * (c.pr ? 1.5 : 1);", "if (D && D[0] === e) v += XR[D[1]][3] * (c.pr ? 1.5 : 1) * xsTrMul(c); /* v724 */")
rep("if (Math.random() >= XS_DROP * (isElite(x) ? 2 : 1)", "if (Math.random() >= (XS_DROP + xsLuck()) * (isElite(x) ? 2 : 1)")
rep("X.brT = T + XS_BR_CD;", "X.brT = T + XS_BR_CD * (1 - xsSwift()); /* v724 */")
# the drop shows the reveal (it brings the Advisor's line)
i0 = s.index('  setTimeout(() => { try { toast(`${pr ? "A Prismatic " : "An "}${xsName(sp)} egg was left in the wreckage!'); i1 = s.index("}, 2200); }", i0)
s = s[:i0] + "  setTimeout(() => { try { xsReveal(sp, pr); } catch (e) {} }, 2200); /* v724 */ " + s[i1 + len("}, 2200); "):]
# the habitat shows each creature's trait and its bonus with it
rep("pct = Math.round(r[3] * (c.pr ? 1.5 : 1) * 10) / 10, rk", "pct = xsCrPct(c), rk")
rep('<small style="color:${r[1]}">${r[0]}${c.pr ? " · Prismatic" : ""}</small>${R(D[0])}', '<small style="color:${r[1]}">${r[0]}${c.pr ? " · Prismatic" : ""}</small>${R(D[0])}${xsTrChip(c)}')
# incubators: the egg wobbles harder as it nears hatching, and can be warmed
rep('return `<div class="xsinc${done ? " ready" : ""}">${xsEggHTML(it.sp, it.pr, 1)}<b>',
    'return `<div class="xsinc${done ? " ready" : ""}" style="--wb:${clamp((T - it.s) / Math.max(1, it.e - it.s), 0, 1).toFixed(2)}">${done ? xsEggHTML(it.sp, it.pr, 1) : `<button class="xswarm" data-act="xsWarm" data-i="${i}" aria-label="Warm the egg">${xsEggHTML(it.sp, it.pr, 1)}</button>`}<b>')
rep('<small><span data-end="${it.e}">${ftime(left)}</span> left</small>', '<small><span data-end="${it.e}">${ftime(left)}</span> left</small>${T - (it.w || 0) >= XS_WARM ? `<small class="xswt">Tap the egg to warm it</small>` : `<small class="xswt">Warm again in ${ftime(XS_WARM - (T - it.w))}</small>`}')
rep("const XS_CAP_PCT = 15,", "const XS_WARM = 20 * 3600e3; /* v724 */\nconst XS_CAP_PCT = 15,")
rep("  xsHatch: d => act(() => {", """  xsWarm: d => act(() => { const X = xsOf(), it = X.inc[+d.i], T = now(); if (!it || it.e <= T) return; if (T - (it.w || 0) < XS_WARM) return toast(`It's still warm. Again in ${ftime(XS_WARM - (T - it.w))}.`); /* v724 */
    const cut = Math.max(5 * 60e3, (it.e - T) * .15); it.e = Math.max(T, it.e - cut); it.w = T; try { SFX.research(); } catch (e) {} toast(`You warm the egg. Something inside stirs: ${ftime(cut)} sooner.`, "win"); }),
  xsHatch: d => act(() => {""")
# hatching: a trait, and the cinematic instead of the toast
rep('const c = { id: "c" + (S.seq++), sp: it.sp, pr: it.pr || 0, at: now() };', 'const c = { id: "c" + (S.seq++), sp: it.sp, pr: it.pr || 0, at: now(), tr: xsTrRoll(Math.random()) }; /* v724 */')
s, n = re.subn(r'toast\(`\$\{it\.pr \? "✦ Prismatic " : ""\}\$\{xsName\(it\.sp\)\} hatched! [^\n]*?"win"\);\n    try \{ SFX\.research\(\); if \(', 'xsHatchCine(c); /* v724 */\n    setTimeout(() => { try { if (', s); assert n == 1, n
i0 = s.index('xsHatchCine(c); /* v724 */'); i1 = s.index("} catch (e) {} }),", i0); s = s[:i1] + "} catch (e) {} }, 2700); })," + s[i1 + len("} catch (e) {} }),"):]
rep('const GAME_V = 723;', 'const GAME_V = 724;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
