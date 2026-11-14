# v550 the owner's art for everything that had none (owner: "Here is all the art you asked for"). Cut from his four sheets into
# docs/art/shop (14 shop tiles: runes, VIP activations, VIP points, six material boxes), docs/art/chron (six chapter paintings),
# docs/art/ev (Void Pass banner, Alliance Conquest banner + a square spare), avatars/ondra.webp (Quartermaster Ondra Vey; a second
# quartermaster portrait is kept as avatars/quartermaster2.webp) and art/logo-udf.webp (+ logo-udf2.webp), with transparent backgrounds.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# shop tiles
rep('repairKit: "repairYard", pirIntel: "espionage", teleport: "jumpGate", moonSeed: "lunarBase" };',
    'repairKit: "repairYard", pirIntel: "espionage", teleport: "jumpGate", moonSeed: "lunarBase",\n'
    '  runes3: "shop/runes", vipAct1: "shop/vip1", vipAct7: "shop/vip7", vipAct30: "shop/vip30", vipPts100: "shop/vp100", vipPts500: "shop/vp500", vipPts2500: "shop/vp2500", vipPts10k: "shop/vp10k", /* v550 */\n'
    '  mb1: "shop/mb1", mb2: "shop/mb2", mb3: "shop/mb3", mb4: "shop/mb4", mb5: "shop/mb5", mb6: "shop/mb6" };')
# Chronicles: each chapter's painting heads its card
rep('Chronicles · complete</header><p>', 'Chronicles · complete</header><div class="chart" style="background-image:url(art/chron/c6.webp)"></div><p>')
rep('<b>${esc(ch.title || ch.t)}</b></header>' if '<b>${esc(ch.title || ch.t)}</b></header>' in s else '<b>${esc(ch.t)}</b></header>',
    '<b>${esc(ch.t)}</b></header><div class="chart" style="background-image:url(art/chron/c${C.c + 1}.webp)"></div>')
# Void Pass: the painted banner across the top
rep('''  return `<div class="evban vpban" style="--vc:${col}"><div class="vpglyph"''', '''  return `<div class="evban vpban art" style="--vc:${col}"><div class="vpart" aria-hidden="true"></div><div class="vpglyph"''')
# Alliance Conquest: the painted banner over the sector map
rep('<div class="evban cqban">${cqSvg(M)}', '<div class="evban cqban"><div class="cqart" aria-hidden="true"></div>${cqSvg(M)}')
# Ondra Vey's portrait in the Supply Depot
rep('<img src="avatars/pilot.webp" alt=""><div><small>QUARTERMASTER ONDRA VEY</small>', '<img src="avatars/ondra.webp" alt="Quartermaster Ondra Vey"><div><small>QUARTERMASTER ONDRA VEY</small>')
# battle clips: the logo instead of the typed title
rep('''x.textAlign = "center"; x.fillStyle = "#ffcf5a"; x.shadowColor = "#ffcf5a"; x.shadowBlur = 18; x.font = "800 46px 'Orbitron','Rajdhani',sans-serif"; x.fillText("ULTRA DEEP FIELD", W / 2, 78); x.shadowBlur = 0;''',
    '''x.textAlign = "center"; const lg = CLIP_LOGO.complete && CLIP_LOGO.naturalWidth, oy = lg ? 150 : 0; if (lg) { const lw = 540, lh = lw * CLIP_LOGO.naturalHeight / CLIP_LOGO.naturalWidth; x.drawImage(CLIP_LOGO, (W - lw) / 2, 18, lw, lh); } else { x.fillStyle = "#ffcf5a"; x.shadowColor = "#ffcf5a"; x.shadowBlur = 18; x.font = "800 46px 'Orbitron','Rajdhani',sans-serif"; x.fillText("ULTRA DEEP FIELD", W / 2, 78); x.shadowBlur = 0; }''')
rep('tl.slice(0, 2).forEach((l, i) => x.fillText(l, W / 2, 128 + i * 36));', 'tl.slice(0, 2).forEach((l, i) => x.fillText(l, W / 2, 128 + oy + i * 36));')
rep('x.fillText(who, W / 2, 128 + Math.min(2, tl.length) * 36 + 6);', 'x.fillText(who, W / 2, 128 + oy + Math.min(2, tl.length) * 36 + 6);')
rep('let g = x.createLinearGradient(0, 0, 0, 260); g.addColorStop(0, "rgba(3,6,12,.92)"); g.addColorStop(1, "rgba(3,6,12,0)"); x.fillStyle = g; x.fillRect(0, 0, W, 260);',
    'let g = x.createLinearGradient(0, 0, 0, 260 + oy); g.addColorStop(0, "rgba(3,6,12,.92)"); g.addColorStop(1, "rgba(3,6,12,0)"); x.fillStyle = g; x.fillRect(0, 0, W, 260 + oy);')
rep('const CLIP_URL = "gunhypechannel.github.io/Ultradeepfield";', 'const CLIP_URL = "gunhypechannel.github.io/Ultradeepfield", CLIP_LOGO = new Image(); /* v550 the logo, loaded when a clip starts */')
rep('  const r = b0.r; ACT.breplay();', '  if (!CLIP_LOGO.src) CLIP_LOGO.src = "art/logo-udf.webp";\n  const r = b0.r; ACT.breplay();')
# the VIP tab draws its own rows: give them the painted tiles too
rep('<div class="sit"><span class="sic">${s.ic}</span></div><b>${esc(s.n)}</b>', '<div class="sit">${shopArtOf(k) ? `<span class="sart vipart" style="background-image:url(${shopArtOf(k)})"></span>` : `<span class="sic">${s.ic}</span>`}</div><b>${esc(s.n)}</b>')
css = '''
/* v550 the owner's art */
.chart{margin:8px 0 2px;aspect-ratio:2/1;border-radius:10px;background:center 35%/cover no-repeat;border:1px solid rgba(226,196,138,.45);box-shadow:0 4px 18px rgba(0,0,0,.45)}
.vpban.art{min-height:0}.vpban.art .vpglyph,.vpban.art .vpbot>b{display:none}.vpart{position:relative;aspect-ratio:3.2/1;background:url(art/ev/vpass.webp) center/cover no-repeat}
.vpart::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(5,7,15,.9),rgba(5,7,15,0) 35%)}.vpban.art .vpbot{padding-top:4px;max-width:none;padding-right:96px}
.sitem .sit .sart.vipart{width:100%;height:auto;aspect-ratio:4/3;border-radius:10px}
.vpban.art .vptop small{background:rgba(5,7,15,.72);padding:2px 8px;border-radius:8px}
.cqban .cqart{grid-column:1/-1;margin:-10px -10px 0;aspect-ratio:4.2/1;background:url(art/ev/conquest.webp) center/cover no-repeat;border-bottom:1px solid rgba(122,244,255,.35)}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 549\b", "GAME_V = 550", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
