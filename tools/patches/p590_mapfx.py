# v590 the Titan ultimate moment (slow motion, flash, cinematic bars, speed lines) and map battles remastered (tracer heads, kill
# shockwaves and sparks, warp-in flash and streaks, a ring over the side that lost)
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('function fx589Spawn(b, v) { try {', 'function fx589Spawn(b, v) { fx590UltStart(b, v); try {')
rep('  fx589Draw(ctx, b, t, d, vs, scr, Q, T, vtx); fx589Nums(ctx, b, t, d, vs, Q); /* v589 */\n  ctx.globalAlpha = 1;\n  ctx.setTransform(1, 0, 0, 1, 0, 0);\n',
    '  fx589Draw(ctx, b, t, d, vs, scr, Q, T, vtx); fx589Nums(ctx, b, t, d, vs, Q); /* v589 */\n  ctx.globalAlpha = 1;\n  ctx.setTransform(1, 0, 0, 1, 0, 0);\n  fx590Ult(ctx, b, t, W, H, d, scr, vs, vtx, vty); /* v590 */\n')
rep('if (bossLocKey(c.loc)) { c.o.boss = 1; c.o.gd.visible = false; } }', 'if (bossLocKey(c.loc)) { c.o.boss = 1; c.o.gd.visible = false; } if (!reduced) c.o.f5 = fx590Init(W, c); /* v590 */ }')
rep('b.big = big; b.hs = hs || 0; }; o.boom = boom;', 'b.big = big; b.hs = hs || 0; fx590Boom(o, p, big, hs, tn, fsC); }; o.boom = boom;')
rep('    if (k > .88 && !o.ended) { o.ended = 1;', '    fx590Tick(W, c, o, tn, fsC, e, k, q); /* v590 */\n    if (k > .88 && !o.ended) { o.ended = 1;')
rep('function clashDispose(W, c) { const o = c.o; if (!o) return; ', 'function clashDispose(W, c) { const o = c.o; if (!o) return; fx590Free(W, o); ')
i = s.index('/* ---------- v589 battle effects remaster'); s = s[:i] + open('tools/patches/p590_mapfx.js', encoding='utf-8').read() + s[i:]
s2 = re.sub(r"GAME_V = 589\b", "GAME_V = 590", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
