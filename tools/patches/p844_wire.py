"""v844: the Mimics rebuilt after the owner's new design legends (armoured chests of chrome ribs over a blazing core, lit bands on the
cables, hooked claws, a brighter throat; the Guardian's crescent tower shield and hammerhead crest, the Harvester's canister rig and
clamp, the Stalker's clawed tentacle crown, the Hunter's blade spines, whip antennae and crescent-bladed whip tail), and in battle
each Mimic drips cyan light and trails a faint mist."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 843;", "const GAME_V = 844;")
rep("function mimAtkX(ctx, b, m, u, S0, E0, Lg, C, gl, d, T, t, scr, hit, pan) {", '''/* v844 every Mimic in battle drips cyan light and trails a faint mist under it, slowly (the design legends' wet glow) */
function mimAmbient(ctx, b, scr, T, d) { if (!b || !b.Q) return; let n = 0; ctx.save(); ctx.globalCompositeOperation = "lighter";
  for (let i = 0; i < b.Q.length && n < 14; i++) { const q = b.Q[i], P = scr[i]; if (!q || !P || !MIM_D[q.k] || !(b.n[i] > 0)) continue; n++;
    const g = b.geo && b.geo[i], Lg = g ? g.L : 40, col = BOSS_GLOW[q.k] || "95,216,255", gs = glowSprite(`rgba(${col},1)`);
    const mr = Lg * (.9 + .08 * Math.sin(T * .7 + i)); ctx.globalAlpha = .1 + .04 * Math.sin(T * .5 + i * 2); ctx.drawImage(gs, P.x - mr, P.y + Lg * .05, mr * 2, mr * .7); /* the mist */
    for (let j = 0; j < 4; j++) { const ph = T * .32 + j / 4 + i * .37, k = ph % 1, c = Math.floor(ph), x = P.x + Math.sin(i * 7.1 + j * 3.3 + c * 12.9) * Lg * .45, y = P.y + Lg * .05 + k * k * Lg * .55, r = Math.max(1.2 * d, Lg * .028) * (1 - k * .5);
      ctx.globalAlpha = (1 - k) * .75; ctx.fillStyle = `rgba(${col},1)`; ctx.beginPath(); ctx.ellipse(x, y, r * .7, r * 1.6, 0, 0, TAU); ctx.fill(); ctx.globalAlpha = (1 - k) * .35; ctx.drawImage(gs, x - r * 3, y - r * 3, r * 6, r * 6); } } /* the drips */
  ctx.restore(); }
function mimAtkX(ctx, b, m, u, S0, E0, Lg, C, gl, d, T, t, scr, hit, pan) {''')
rep("try { mimAtkDraw(ctx, b, scr, T, W, d, lo, t, H); } catch (e) {}", "try { mimAtkDraw(ctx, b, scr, T, W, d, lo, t, H); } catch (e) {} if (!lo) try { mimAmbient(ctx, b, scr, T, d); } catch (e) {}")
open(p, "w", encoding="utf-8").write(s); print("ok")
