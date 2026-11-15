# v596 the Titans' strike craft are the carriers' own models (owner: "Cant we use the model fighters we use for carrier and escort
# carriers just color them titans colors"). The Sovereign Ark's strike wing flies the carriers' baked Fighter (drawSide's studio art)
# washed white-gold with gold trim; the Eclipse Harbinger's swarm flies the Hive Drone (the Hive Lord's carrier craft) darkened to
# its black hull with emerald trim. Each tint is cached per sprite size; until the studio art is baked the drawn shapes stand in.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep("  rnd: (s, i) => { const x = Math.sin(s * 9.13 + i * 78.233) * 43758.5453; return x - Math.floor(x); },",
    '''  /* v596 a carrier craft from the studio (the same baked side view the carriers launch), washed in the Titan's colours */
  craftT: new WeakMap(),
  craft(ctx, k, acc, tint, x, y, an, L) { let art = shipArtSoon(k, acc, "side"); if (!art) return false; const fc = Math.cos(an) >= 0 ? 1 : -1, w = L * (DRAWK[k] || (AL[k] ? 2 : 1.8)), h = w / 2; let sc = 1; try { const m = ctx.getTransform(); sc = Math.hypot(m.a, m.b); } catch (e) {} art = sprMip(art, w * sc);
    let M = tx5.craftT.get(art); if (!M) tx5.craftT.set(art, M = {}); let c = M[tint]; if (!c) { c = document.createElement("canvas"); c.width = art.width; c.height = art.height; const x2 = c.getContext("2d"); x2.drawImage(art, 0, 0); x2.globalCompositeOperation = "source-atop"; x2.fillStyle = tint; x2.fillRect(0, 0, c.width, c.height); M[tint] = c; }
    ctx.save(); ctx.globalCompositeOperation = "source-over"; ctx.translate(x, y); ctx.rotate(an); ctx.scale(1, fc); ctx.drawImage(c, -w / 2, -h / 2, w, h); ctx.restore(); return true; },
  rnd: (s, i) => { const x = Math.sin(s * 9.13 + i * 78.233) * 43758.5453; return x - Math.floor(x); },''')
rep('''      ctx.save(); ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = fade; ctx.translate(x, y); ctx.rotate(an); const g = ctx.createLinearGradient(-fs, -fs, fs, fs);''',
    '''      ctx.globalAlpha = fade; if (!tx5.craft(ctx, "fighter", "#ffcf5a", "rgba(255,226,150,.3)", x, y, an, fs * 1.5)) { /* v596 */
      ctx.save(); ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = fade; ctx.translate(x, y); ctx.rotate(an); const g = ctx.createLinearGradient(-fs, -fs, fs, fs);''')
rep('''ctx.fill(); ctx.strokeStyle = "#ffcf5a"; ctx.lineWidth = Math.max(.8, .9 * d); ctx.stroke(); ctx.restore(); // a gold-trimmed strike fighter''',
    '''ctx.fill(); ctx.strokeStyle = "#ffcf5a"; ctx.lineWidth = Math.max(.8, .9 * d); ctx.stroke(); ctx.restore(); } ctx.globalCompositeOperation = "lighter"; // a gold-trimmed strike fighter''')
rep('''      ctx.save(); ctx.globalCompositeOperation = "source-over"; ctx.translate(x, y); ctx.rotate(an); ctx.fillStyle = "#0b0f0d";''',
    '''      ctx.globalAlpha = 1; if (!tx5.craft(ctx, "drone", "#3dff9a", "rgba(14,40,28,.38)", x, y, an, ds * 2)) { /* v596 the Hive Drone in the Harbinger's black */
      ctx.save(); ctx.globalCompositeOperation = "source-over"; ctx.translate(x, y); ctx.rotate(an); ctx.fillStyle = "#0b0f0d";''')
rep('''ctx.lineTo(-ds * .6, ds * .8); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore();''',
    '''ctx.lineTo(-ds * .6, ds * .8); ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore(); } ctx.globalCompositeOperation = "lighter";''')
rep('tx5.glow(ctx, x + Math.cos(an) * ds * .35, y + Math.sin(an) * ds * .35, ds * 1.2, "#3dff9a", .9); tx5.glow(ctx, x - Math.cos(an) * ds * .5, y - Math.sin(an) * ds * .5, ds * 1.4 * fl, "#b06bff", .6);',
    'tx5.glow(ctx, x + Math.cos(an) * ds * .9, y + Math.sin(an) * ds * .9, ds * .55, "#3dff9a", .9); tx5.glow(ctx, x - Math.cos(an) * ds * 1.1, y - Math.sin(an) * ds * 1.1, ds * .8 * fl, "#b06bff", .55); /* v596 eye at the nose, engines behind */')
s2 = re.sub(r"GAME_V = 595\b", "GAME_V = 596", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
