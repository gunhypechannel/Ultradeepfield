# v345: ships no longer flicker in Super Cube battle replays (and other flagship replays) on near-square screens such as an unfolded Z Fold.
# Cause: drawBattleFlags set b.fdir ("x" or "y", which way the fleets face) from scratch every frame for every flagship, from the
# direction between its squadrons and the enemy. drawBattle then snapped the field margins (top/bottom strip or left/right strip
# kept free for the flagship) to that axis with no easing. In a Super Cube fight the enemy is the one Cube placed diagonally from
# the attackers, so the direction sits near 45 degrees: switching the margins moved every squadron, that moved the direction back
# over 45 degrees, and the axis flipped x/y/x/y on every frame. The whole fleet jumped between two layouts 30-60 times a second.
# Fix: (1) the axis is chosen once per frame by the first flagship, and only changes when the other axis clearly wins (1.5x) and
# the current one has held for 2 s; (2) the margins ease to their new values (about 0.6 s) instead of snapping, so the one-time
# change when a flagship arrives glides rather than jumps.
p="docs/index.html"; h=open(p).read()
def rep(a,b):
    global h; assert h.count(a)==1,a[:70]; h=h.replace(a,b)
rep('''      b.fdir = Math.abs(uy) >= Math.abs(ux) ? "y" : "x"; /* which way the fleets face: the field leaves room behind each one for its flagship (drawBattle) */''',
'''      if (b.fdirF !== b.gf) { b.fdirF = b.gf; const ay = Math.abs(uy), ax = Math.abs(ux), nd = ay >= ax ? "y" : "x"; /* v345: one decision per frame, with hysteresis: near 45 degrees (the Super Cube sits diagonal to its attackers) it flipped every frame and the fleet flickered between two layouts */
        if (!b.fdir || (nd !== b.fdir && (nd === "y" ? ay > ax * 1.5 : ax > ay * 1.5) && t - (b.fdirT || -1e9) > 2000)) { b.fdir = nd; b.fdirT = t; } } /* which way the fleets face: the field leaves room behind each one for its flagship (drawBattle) */''')
rep('''  const top = fy ? Math.max(H * .14, b.vb[0] + fm) : H * .14, bot = fy ? Math.max(top + H * .25, Math.min(H * .79, b.vb[1] - fm)) : H * .79, xl = Math.max(.06, fxm), xr = Math.max(.06, fxm), T = b.simT, Q = b.Q, r = b.r, lo = b.lowFx;''',
'''  const top0 = fy ? Math.max(H * .14, b.vb[0] + fm) : H * .14, bot0 = fy ? Math.max(top0 + H * .25, Math.min(H * .79, b.vb[1] - fm)) : H * .79, xl0 = Math.max(.06, fxm);
  /* v345 the field margins glide to a new flagship layout instead of snapping (a snap moved every ship at once) */
  const mg = b.mg && b.mg.W === W && b.mg.H === H ? b.mg : (b.mg = { W, H, top: top0, bot: bot0, xl: xl0 }), mke = reduced ? 1 : Math.min(1, real / 600);
  mg.top += (top0 - mg.top) * mke; mg.bot += (bot0 - mg.bot) * mke; mg.xl += (xl0 - mg.xl) * mke;
  const top = mg.top, bot = mg.bot, xl = mg.xl, xr = mg.xl, T = b.simT, Q = b.Q, r = b.r, lo = b.lowFx;''')
open(p,"w").write(h); print("ok")
