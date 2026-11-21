# v707: the Iron Tyrant's battle remastered (owner: "remaster the iron tyrants battle animation, remove the black lines on screen and
# make it use broadsides more"), and the Cube turns slowly (owner, with a video of it spinning over the Void: "slow the cube down from
# spinning this fast? Look super unrealistic").
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)

# 1. the black lines: the broadside tracers are additive lines in a picture drawn on a transparent canvas. Additive blending adds the
#    line's alpha too, so a tracer that had faded to black (or one not firing) was still written as an opaque black line across the
#    boss. Now the tracers leave the picture's alpha alone (pure additive light), and a gun that isn't firing draws no tracer at all.
rep('const tracers = new TH.LineSegments(trG, new TH.LineBasicMaterial({ vertexColors: true, transparent: true, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false }));',
    'const tracers = new TH.LineSegments(trG, new TH.LineBasicMaterial({ vertexColors: true, transparent: true, blending: TH.CustomBlending, blendSrc: TH.OneFactor, blendDst: TH.OneFactor, blendSrcAlpha: TH.ZeroFactor, blendDstAlpha: TH.OneFactor, depthWrite: false, toneMapped: false })); /* v707 light only: additive alpha drew black lines */')
rep('const tr = k > 0 && k < 1.6 ? 1 - k / 1.6 : 0, d0 = 2.5 + k * 30, d1 = d0 + 10; trP.set([g.x, g.y, g.z + g.side * d0, g.x + .5, g.y, g.z + g.side * d1], i * 6);',
    'const tr = k > 0 && k < 1.6 ? 1 - k / 1.6 : 0, d0 = 2.5 + k * 30, d1 = tr > 0 ? d0 + 10 : d0; trP.set([g.x, g.y, g.z + g.side * d0, g.x + (tr > 0 ? .5 : 0), g.y, g.z + g.side * d1], i * 6); /* v707 a silent gun draws nothing */')
# a bigger muzzle flash for the broadside
rep('flash.put(i, g.x, g.y, mz + g.side * .8, 6 * fl + .01, fl);', 'flash.put(i, g.x, g.y, mz + g.side * .8, 9 * fl + .01, fl);')

# 2. broadsides more often: about half its moves (was a quarter), never the same non-broadside move twice running
rep('const m = wbMoves(key), mv = m[(Math.random() * m.length) | 0];',
    'const m = wbMoves(key); let mv = m[(Math.random() * m.length) | 0]; if (key === "tyr") { const L0 = WBR.tyrLast, r = Math.random(); mv = r < .55 || L0 !== "broadside" && r < .62 ? "broadside" : ["missiles", "claw", "mines"].filter(x => x !== L0)[(Math.random() * 2) | 0]; WBR.tyrLast = mv; } /* v707 the Tyrant fights with its broadsides */')

# 3. the broadside on the battlefield: the guns fire from along the hull (not one point), in a rolling ripple from stern to bow in time
#    with the model's barrels, two waves of shells (the lower and upper gun decks), each one a hot shell with a smoke trail that lands as
#    an explosion; the whole fleet line is raked. Then the hull rocks with the recoil.
rep('  else { const n = S[3] || 5; for (let j = 0; j < n; j++) {', '''  else if (k === "tyr" && M.m === "broadside" && b.wbBox) { const B = b.wbBox, dir = Math.sign((tg.reduce((a, i) => a + scr[i].y, 0) / tg.length) - B.cy) || 1, N = lo ? 14 : 22;
    for (let j = 0; j < N; j++) { const deck = j % 2, gi = j >> 1, n2 = N >> 1, fx0 = (gi + .5) / n2, a = .02 + fx0 * .5 + deck * .05, v = clamp((u - a) / .28, 0, 1); if (u < a) continue;
      const sx = B.cx + (fx0 - .5) * B.aw * .7 * (WBR.face < 0 ? -1 : 1), sy = B.cy + dir * B.ah * (deck ? .02 : .12), i = tg[(j * 5 + ((M.t0 / 61) | 0)) % tg.length], p = scr[i], tx = p.x + Math.sin(j * 7.1) * 14 * d, ty = p.y + Math.cos(j * 3.3) * 8 * d;
      if (v < .18) { const q = 1 - v / .18; glow(sx, sy, (18 + 20 * q) * d, "rgba(255,190,90,1)", q); glow(sx, sy, 8 * d, "#fff3d0", q); }
      if (v < 1) { const x = sx + (tx - sx) * v, y = sy + (ty - sy) * v - Math.sin(v * Math.PI) * 18 * d, x0 = sx + (tx - sx) * Math.max(0, v - .22), y0 = sy + (ty - sy) * Math.max(0, v - .22) - Math.sin(Math.max(0, v - .22) * Math.PI) * 18 * d;
        ctx.globalAlpha = .5; ctx.strokeStyle = "rgba(255,150,60,1)"; ctx.lineWidth = 7 * d; ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x, y); ctx.stroke(); ctx.globalAlpha = 1; ctx.strokeStyle = "#ffe6b0"; ctx.lineWidth = 2.4 * d; ctx.stroke(); glow(x, y, 9 * d, "#fff6e0", 1); }
      else { hit(tx, ty, .55, "t" + j); const age = (u - a - .28) / .18; if (age < 1) { glow(tx, ty, (26 + 40 * age) * d, "rgba(255,120,40,1)", .9 * (1 - age)); glow(tx, ty, 10 * d, "#ffffff", 1 - age); } } }
    if (u > .1 && u < .8) b.shake = Math.max(b.shake || 0, 2.5 * d); }
  else { const n = S[3] || 5; for (let j = 0; j < n; j++) {''')
rep('tyr: { broadside: ["bolts", .25, .82, 10, 2800],', 'tyr: { broadside: ["bolts", .12, .95, 22, 2800],')

# 4. the Cube over the Void turns slowly: about once every five minutes at rest (was once every 52 s), and even at full energy in the
#    finale no faster than once every 100 s (was once every 13 s)
rep('function cubeSpin(T) { const ph = cubePhase(T); if (!ph) return T * .00012; let a = ph.s * .00012;', 'function cubeSpin(T) { const ph = cubePhase(T); if (!ph) return T * .00002; let a = ph.s * .00002; /* v707 slower */')
rep('a += .00034 * d * (p.e0', 'a += .00004 * d * (p.e0')
rep('W.nexus.rotation.y = LI ? t * .00012 + turn : PH && PH.i < 6 ? cubeSpin(T) : t * .00012; W.nexus.rotation.x = .18; W.nexus.userData.r2.rotation.y = -t * .0012;',
    'W.nexus.rotation.y = LI ? t * .00002 + turn : PH && PH.i < 6 ? cubeSpin(T) : t * .00002; W.nexus.rotation.x = .18; W.nexus.userData.r2.rotation.y = -t * .00025; /* v707 slower */')
rep('const GAME_V = 706;', 'const GAME_V = 707;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
