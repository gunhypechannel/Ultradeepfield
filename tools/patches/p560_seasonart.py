# v560 the owner's season art pack ("Update all of this art into the game"): a banner, portrait frame and token for each of the six
# seasons (art/season/s<n>-banner|frame|token.webp), the Void Cache closed and open, the Vault and Wardrobe banners, and the three Titans
# painted together (cropped into art/armageddon|sovereign|harbinger.webp card paintings).
# Season banners and premium frames become the art of those cosmetics; the Void Pass banner shows the current season's painting; the
# season token sits on the Void Pass and in the Vault; the cache opens on its own painting. Fix: a banner cosmetic with art was hidden
# behind the .cbn gradient (!important), so art banners now carry their picture through --bnart.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('adv5: "art/season/s6-adv.webp" };', 'adv5: "art/season/s6-adv.webp", /* v560 the season pack */ ...Object.fromEntries([0, 1, 2, 3, 4, 5].flatMap(i => [["banner" + i, `art/season/s${i + 1}-banner.webp`], ["frame" + i, `art/season/s${i + 1}-frame.webp`]])), cache: "art/season/cache.webp", cacheOpen: "art/season/cache-open.webp" };\nconst seasonTok = (si = vpSeason()) => `art/season/s${(((si % 6) + 6) % 6) + 1}-token.webp`; /* v560 */')
rep('return d.art ? `background-image:linear-gradient(90deg,rgba(4,8,16,.8),rgba(4,8,16,.25)),url(${d.art});background-size:cover;background-position:center` : `--c1:${d.col};--c2:${d.col2}`; };',
    'return d.art ? `--bnart:url(${d.art});background-image:linear-gradient(90deg,rgba(4,8,16,.8),rgba(4,8,16,.25)),url(${d.art});background-size:cover;background-position:center` : `--c1:${d.col};--c2:${d.col2}`; };')
# the cache opens on its painting
rep('<div class="rvchest">${art ? `<img src="${art}" alt="">` : ', '<div class="rvchest${art ? " art" : ""}">${art ? `<img class="cl" src="${art}" alt=""><img class="op" src="${COS_ART.cacheOpen}" alt="">` : ')
# the Vault: its banner and the season token
rep('return `<div class="hd vthd"><div><div class="chapter">Void Tokens · ${VT}${fmt(tok)}</div><h2>The Vault</h2>', 'return `<div class="hd vthd art"><img class="vttok" src="${seasonTok()}" alt=""><div><div class="chapter">Void Tokens · ${VT}${fmt(tok)}</div><h2>The Vault</h2>')
# the Wardrobe: its own banner until a banner is equipped
rep('return `<div class="hd cwhd${cosB', 'return `<div class="hd cwhd${bnId ? "" : " wdart"}${cosB')
# the Void Pass banner shows this season's painting and token
rep('<div class="evban vpban art" style="--vc:${col}"><div class="vpart" aria-hidden="true"></div>', '<div class="evban vpban art" style="--vc:${col}"><div class="vpart" aria-hidden="true" style="background-image:url(art/season/s${(((si % 6) + 6) % 6) + 1}-banner.webp)"><img class="vptok" src="${seasonTok(si)}" alt=""></div>')
# the Titans' card paintings
rep('"guardian escortCarrier tender supercarrier worldbreaker " +', '"guardian escortCarrier tender supercarrier worldbreaker armageddon sovereign harbinger " + // v560 the Titans, from the owner\'s painting\n  ')
rep('  if (!SH[k] || typeof ART === "undefined" || !ART[k]) return null;', '  if (!SH[k] || typeof ART === "undefined" || !ART[k] || TITAN_LEN[k]) return null; /* v560 the Titans keep their own hull colours */')
rep('/* v550 the owner\'s art */', '''/* v550 the owner's art */
/* v560 the season pack */
.cbn.art{background-image:linear-gradient(90deg,rgba(4,8,16,.82),rgba(4,8,16,.2)),var(--bnart)!important;background-size:cover!important;background-position:center!important}
.vthd.art,.cwhd.wdart{position:relative;background:linear-gradient(90deg,rgba(4,8,16,.88),rgba(4,8,16,.3)),url(art/season/vault.webp) center/cover no-repeat;min-height:120px}
.cwhd.wdart{background:linear-gradient(90deg,rgba(4,8,16,.88),rgba(4,8,16,.25)),url(art/season/wardrobe.webp) 70% center/cover no-repeat}
.vthd.art{display:flex;align-items:center;gap:12px}.vttok{width:64px;height:64px;flex:none;filter:drop-shadow(0 0 10px rgba(255,207,90,.6));animation:vtt 5s ease-in-out infinite}
@keyframes vtt{50%{transform:translateY(-3px) rotate(4deg)}}
.vpart .vptok{position:absolute!important;right:10px;top:34px;left:auto!important;width:54px!important;height:54px!important;max-width:54px;object-fit:contain!important;z-index:2;filter:drop-shadow(0 0 10px var(--vc));animation:vtt 5s ease-in-out infinite}
.rvchest.art{width:min(78vw,340px)!important;height:min(78vw,340px)!important;border-radius:22px;overflow:hidden;box-shadow:0 0 50px color-mix(in srgb,var(--rc) 60%,transparent)}
.rvchest.art img{position:absolute;inset:0;transition:opacity .25s}.rvchest.art img.op{opacity:0}.rv.open .rvchest.art img.op{opacity:1}.rv.open .rvchest.art img.cl{opacity:0}
.rv.open .rvchest.art{transition:transform .7s ease .75s,opacity .5s ease .85s}''')
s2 = re.sub(r"GAME_V = 559\b", "GAME_V = 560", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
