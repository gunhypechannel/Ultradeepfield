# v589 Battle effects remastered after the owner's reference videos (Foundation: Galactic Frontier battle footage): skill banners
# when a Titan or super boss uses a named attack, violet chain lightning that leaps across enemy formations for ion/acid weapons,
# starburst light rays on big blasts, and bold pop-in damage numbers (gradient fill, heavy outline, huge gold crits, red kill counts).
# All drawn live on the battle canvas (no textures, no memory cost); off on low-effects devices.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('function spawnVolley(b, v) {\n', 'function spawnVolley(b, v) { fx589Spawn(b, v); /* v589 */\n')
rep('''  const vr = R(), vcol = vr < .4 ? "255,170,110" : vr < .75 ? "255,205,150" : "190,215,255";''', '''  const vr = R(), vcol = vr < .4 ? "255,170,110" : vr < .75 ? "255,205,150" : "190,215,255";
  if (size >= 1.5 && !b.lowFx) { (b.bursts589 = b.bursts589 || []).push({ x, y, t, r: (46 + size * 46) * d, life: 380 + size * 140, rot: R() * TAU, n: 12 + Math.round(size * 3), col: vcol }); if (b.bursts589.length > 8) b.bursts589.shift(); } /* v589 */''')
i = s.index('  b.nums = b.nums.filter(o => t - o.t < 1000);'); j = s.index('ctx.fillStyle = o.col; ctx.fillText(o.txt, o.x, yy); }', i) + len('ctx.fillStyle = o.col; ctx.fillText(o.txt, o.x, yy); }')
s = s[:i] + '  fx589Draw(ctx, b, t, d, vs, scr, Q, T, vtx); fx589Nums(ctx, b, t, d, vs, Q); /* v589 */' + s[j:]
s = s.replace('/* an explosion in layers: a white flash, rolling fireballs', open('tools/patches/p589_bfx.js', encoding='utf-8').read() + '/* an explosion in layers: a white flash, rolling fireballs', 1)
s2 = re.sub(r"GAME_V = 588\b", "GAME_V = 589", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
