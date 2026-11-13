# v527 a cleaner, bigger battle replay (owner, with reference screenshots: "everything fits in the screen and is big and significant").
# Every squadron is one big hull (small craft keep a tight flight of up to five), drawn half again as large; its badge is just its
# count, a clean white number under the ship (health bars only once it is hurt). The rank formation (v523) still keeps them apart and
# shrinks a side only if it truly cannot fit.
import sys, re, os
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
n0 = s.count('vc = MON[q.k] ? 1 : Math.min(busy ? 3 : 6, Math.max(1, visN(q.role,'); assert n0 == 2, n0
s = s.replace('vc = MON[q.k] ? 1 : Math.min(busy ? 3 : 6, Math.max(1, visN(q.role,', 'vc = MON[q.k] || bLen(q.k) >= .55 ? 1 : Math.min(busy ? 3 : 5, Math.max(1, visN(q.role,')
n1 = s.count('clamp(W * .1 * bLen(q.k), 11 * d, W * (BOSSK[q.k] || q.k === "worldbreaker" ? .55 : .3)) * zs)'); assert n1 >= 2, n1
s = s.replace('clamp(W * .1 * bLen(q.k), 11 * d, W * (BOSSK[q.k] || q.k === "worldbreaker" ? .55 : .3)) * zs)', 'clamp(W * .15 * bLen(q.k), 13 * d, W * (BOSSK[q.k] || q.k === "worldbreaker" ? .6 : .42)) * zs)')
# the badge: just the count
rep('''      const lw = w1 + w2 + 17 * dS, lh = fs * 1.75, bars = p.sh < .995 || p.wd > .005, th = lh + (bars ? 7 * dS : 0) + (allyIn && !busy ? 13 * dS : 0);''',
    '''      const lw = w2 * 1.25 + 8 * dS, lh = fs * 1.5, bars = p.sh < .97 || p.wd > .02, th = lh + (bars ? 7 * dS : 0) + (allyIn && !busy ? 13 * dS : 0); /* v528 just the number */''')
rep('''      ctx.fillStyle = "rgba(5,11,20,.74)"; ctx.fill(); ctx.strokeStyle = `rgba(${col.glow},.55)`; ctx.lineWidth = 1 * dS; ctx.stroke(); ctx.clip(); ctx.fillStyle = col.main; ctx.fillRect(bx0, by0, 3.2 * dS, lh); ctx.restore();
      ctx.textAlign = "left"; ctx.textBaseline = "middle"; ctx.font = `700 ${fs}px Oxanium, sans-serif`; ctx.fillStyle = "rgba(225,236,246,.86)"; ctx.fillText(nm, bx0 + 8 * dS, ly0 + .5 * dS);
      ctx.font = `800 ${fs * 1.12}px Oxanium, sans-serif`; ctx.fillStyle = q.side === "a" ? "#bfeeff" : "#ffd2bd"; ctx.fillText(cnt, bx0 + 12 * dS + w1, ly0 + .5 * dS); ctx.textBaseline = "alphabetic"; ctx.textAlign = "center";''',
    '''      ctx.restore(); ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.font = `800 ${fs * 1.3}px Oxanium, sans-serif`; ctx.lineJoin = "round"; ctx.lineWidth = 3.4 * dS; ctx.strokeStyle = "rgba(0,0,0,.9)"; const ct = n.toLocaleString("en-US");
      ctx.strokeText(ct, lx, ly0 + .5 * dS); ctx.fillStyle = q.side === "a" ? "#eaf8ff" : "#fff1e6"; ctx.fillText(ct, lx, ly0 + .5 * dS); ctx.textBaseline = "alphabetic";''')
s2 = re.sub(r"GAME_V = 526\b", "GAME_V = 527", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
# the lineup, after the owner's reference: each side's squadrons in a staggered line of two (three past nine) from the front (small
# craft) to the back (titans, then defences), rows sharing the side's half evenly; every hull is sized to its row and column, so even
# a twenty-squadron side fits with every ship big and its number clear
s = open(P, encoding='utf-8').read()
LU = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'p527_lineup.txt'), encoding='utf-8').read()
D0 = s.index('        const pack = () => { rows.length = 0;'); D1 = s.index('/* v523 */', D0)
s = s[:D0] + LU.rstrip('\n') + s[D1:]
open(P, 'w', encoding='utf-8').write(s); print('lineup ok')
