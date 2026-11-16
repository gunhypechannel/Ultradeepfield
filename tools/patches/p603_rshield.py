# v603 reactive shields replace the floating numbers in battle (see p603_rshield.js)
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('if (v.bounce || v.sh > 0) { b.shHit[v.e] = T; (b.shDir = b.shDir || [])[v.e] = Math.atan2(sy - ey, sx - ex);',
    'if (v.bounce || v.sh > 0) { b.shHit[v.e] = T; (b.shDir = b.shDir || [])[v.e] = Math.atan2(sy - ey, sx - ex); rs603Hit(b, v.e, ex, ey, sx, sy, v.crit && f.last, f.hv || f.sw, t); /* v603 */')
rep('const sv = clamp(p.sh, 0, 1), sc = sv > .5 ? "110,210,255" : sv > .2 ? "175,140,255" : "255,105,140", fl2 = sv < .2 ? .55 + .45 * Math.sin(t * .09 + i) : 1;',
    'const sv = clamp(p.sh, 0, 1), sc = sv > .5 ? "110,210,255" : sv > .2 ? "175,140,255" : "255,105,140", fl2 = sv < .2 ? .55 + .45 * Math.sin(t * .09 + i) : 1; (b.shG = b.shG || [])[i] = [ex, cy, rx, ry, sv]; /* v603 */')
rep('      if (shA > 0 && !lo) { const a0 = (b.shDir || [])[i];', '      if (shA > 0 && lo) { const a0 = (b.shDir || [])[i]; /* v603: the simple flare only in low effects; the reactive barrier otherwise */')
rep('b.hexes.push({ x: ex, y: cy, t, r: Math.max(5 * d, L * .1), cells: HEX_N });\n          b.nums.push({ x: ex, y: cy - ry - 12 * d, t, txt: "SHIELDS DOWN", col: "#9fd8ff", big: heavyT ? 1 : 0 });',
    '(b.brk603 = b.brk603 || []).push({ t, x: ex, y: cy, rx, ry, col: rs603Col(.6) }); /* v603 the barrier shatters */')
rep('fx589Nums(ctx, b, t, d, vs, Q); /* v589 */', 'b.nums.length = 0; rs603Draw(ctx, b, t, d, W, H, pos); /* v603 no numbers: reactive shields */')
rep('b.hexes = b.hexes.filter(h => t - h.t < 360); drawHexes(ctx, b, t, d);', 'b.hexes = b.hexes.filter(h => t - h.t < 360); if (b.lowFx) drawHexes(ctx, b, t, d); /* v603 the reactive barrier draws the hex cells now */')
i = s.index('/* ---------- v589 battle effects remaster'); s = s[:i] + open('tools/patches/p603_rshield.js', encoding='utf-8').read() + s[i:]
s2 = re.sub(r"GAME_V = 602\b", "GAME_V = 603", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
