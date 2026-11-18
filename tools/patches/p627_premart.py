# v627: the owner's premium skin paintings, tiers 11-16 above $1,000, gold effects. See p627_premart.js.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
js = open('tools/patches/p627_premart.js', encoding='utf-8').read()
rep('for (let t = 1; t <= 10; t++) { const P = PREM[t], sk = PREM_SKIN[P.k]; PXS[P.k] = { n: P.n, cost: 0, prem: t, alias: sk[0], img: 1, r: "all", b: +(.12 + .012 * t).toFixed(3), glow: P.col, ec: (PXS[sk[0]] || {}).ec || [255, 220, 160], d: sk[1] }; }\n', js)
# hex3 is defined later in the file: hoist a local copy for the table
rep('ec: hex3(P.col)', 'ec: [1, 3, 5].map(i => parseInt(P.col.slice(i, i + 2), 16))')
rep('for (let i = 1; i <= 10; i++) if (usd >= PREM[i].usd) t = i; return t; }', 'for (let i = 1; i <= PREM_TOP; i++) if (usd >= PREM[i].usd) t = i; return t; }')
rep('return S ? Math.min(10, Math.max(S.premT || 0, premUsdTier(S.premUsd || 0))) : 0;', 'return S ? Math.min(PREM_TOP, Math.max(S.premT || 0, premUsdTier(S.premUsd || 0))) : 0;')
rep('if (b.march) r.push(`+${b.march} fleet slot`);', 'if (b.march) r.push(`+${b.march} fleet slot${b.march > 1 ? "s" : ""}`);')
rep('if (b.fq) r.push(`+${b.fq} forge queue slot`);', 'if (b.fq) r.push(`+${b.fq} forge queue slot${b.fq > 1 ? "s" : ""}`);')
rep('nx = t < 10 ? PREM[t + 1] : null, usd = S.premUsd || 0, sel = Math.max(1, Math.min(10, G.premSel || Math.max(1, t)));', 'nx = t < PREM_TOP ? PREM[t + 1] : null, usd = S.premUsd || 0, sel = Math.max(1, Math.min(PREM_TOP, G.premSel || Math.max(1, t)));')
rep('"Ten tiers for commanders who support the game.', '"Sixteen tiers for commanders who support the game.')
rep('<div class="prprog">${[...Array(10)].map((_, i) => `<button class="${i + 1 <= t ? "on" : ""}${i + 1 === sel ? " sel" : ""}"', '<div class="prprog">${[...Array(PREM_TOP)].map((_, i) => `<button class="${i + 1 <= t ? "on" : ""}${i + 1 === sel ? " sel" : ""}${PREM_GOLD.has(i + 1) ? " g" : ""}"')
rep('const card = `<div class="prcard${own ? " own" : ""}" style="--c:${P.col}"><div class="prsk"><canvas data-px="${P.k}" role="img" aria-label="${esc(P.n)} planet skin"></canvas><span class="prring"></span></div><div class="prct"><small>TIER ${sel} · $${P.usd} lifetime</small>',
    'const card = `<div class="prcard${own ? " own" : ""}${PREM_GOLD.has(sel) ? " gold" : ""}" style="--c:${P.col}"><div class="prsk"><canvas data-px="${P.k}" role="img" aria-label="${esc(P.n)} planet skin"></canvas><span class="prring"></span>${PREM_GOLD.has(sel) ? PXG_FX : ""}</div><div class="prct"><small>${sel > 10 ? "BEYOND $1,000 · " : ""}TIER ${sel} · $${P.usd.toLocaleString("en-US")} lifetime</small>')
rep('"Ten tiers, exclusive skins"', '"16 tiers, exclusive skins"')
rep('<div class="pxcard${on ? " on" : ""}" style="--pc:${s.glow}"><canvas data-px="${k}" role="img" aria-label="${esc(s.n)}"></canvas>', '<div class="pxcard${on ? " on" : ""}${s.gold ? " gold" : ""}" style="--pc:${s.glow}">${pxGoldWrap(k, `<canvas data-px="${k}" role="img" aria-label="${esc(s.n)}"></canvas>`)}')
rep('<b class="${premB().gold ? "prgold" : ""}">', '<b class="${premB().gold ? "prgold" + (premT() > 10 ? " prgold2" : "") : ""}">')
# the stand-in paintings are gone
rep('src = src.replace(/^([a-z0-9]+)(-map)?\\.webp$/, (m, a, b) => (PXS[a] && PXS[a].alias ? PXS[a].alias : a) + (b || "") + ".webp"); /* v626 a premium skin shows its stand-in painting until its own art arrives */ ', '')
# 3D: gold worlds get the shimmer shader; its clock runs with the map
rep('mat = W.mats[key] = new TH.MeshStandardMaterial({ map: t, emissiveMap: e, emissive: 0xffffff, emissiveIntensity: 2.1, roughness: .6, metalness: .15, bumpMap: bt, bumpScale: bt ? .04 : 1 }); mat.userData.ok = 1;',
    'mat = W.mats[key] = new TH.MeshStandardMaterial({ map: t, emissiveMap: e, emissive: 0xffffff, emissiveIntensity: 2.1, roughness: .6, metalness: .15, bumpMap: bt, bumpScale: bt ? .04 : 1 }); mat.userData.ok = 1; if (PXS[id].gold) pxGoldMat(mat); /* v627 */')
rep('if (W.shieldM) W.shieldM.uniforms.uT.value = reduced ? 0 : t * .001;', 'if (W.shieldM) W.shieldM.uniforms.uT.value = reduced ? 0 : t * .001; PXG_U.uT.value = reduced ? 2.4 : t * .001;')
css = ('.prprog{grid-template-columns:repeat(8,minmax(0,1fr))!important}.prprog button.g{position:relative;overflow:hidden}.prprog button.g::after{content:"";position:absolute;inset:0;background:linear-gradient(115deg,transparent 35%,rgba(255,230,150,.55) 50%,transparent 65%);background-size:300% 100%;animation:pxglint 3.2s ease-in-out infinite}'
  '.pxgw{position:relative;display:block;flex:none;line-height:0}.pxgw canvas{display:block;filter:drop-shadow(0 0 10px rgba(255,200,80,.5));animation:pxhalo 2.6s ease-in-out infinite}'
  '.pxglint{position:absolute;left:16%;top:16%;width:68%;height:68%;border-radius:50%;overflow:hidden;pointer-events:none;mix-blend-mode:screen}.pxglint::before{content:"";position:absolute;inset:-20%;background:linear-gradient(115deg,transparent 40%,rgba(255,236,170,.75) 49%,rgba(255,255,240,.95) 50%,rgba(255,236,170,.75) 51%,transparent 60%);background-size:300% 100%;animation:pxglint 3.6s ease-in-out infinite}'
  '.pxspk{position:absolute;inset:0;pointer-events:none}.pxspk s{position:absolute;width:12%;height:12%;background:radial-gradient(closest-side,#fff 0,#ffe7a0 30%,transparent 70%),linear-gradient(0deg,transparent 46%,#fff4c8 50%,transparent 54%),linear-gradient(90deg,transparent 46%,#fff4c8 50%,transparent 54%);opacity:0;transform:scale(.2) rotate(0);animation:pxspk 2.4s ease-in-out infinite}'
  '.pxspk s:nth-child(1){left:24%;top:30%}.pxspk s:nth-child(2){left:60%;top:22%;animation-delay:.3s}.pxspk s:nth-child(3){left:70%;top:55%;animation-delay:.9s}.pxspk s:nth-child(4){left:36%;top:64%;animation-delay:1.3s}.pxspk s:nth-child(5){left:48%;top:40%;animation-delay:1.7s}.pxspk s:nth-child(6){left:18%;top:52%;animation-delay:2.1s}.pxspk s:nth-child(7){left:56%;top:72%;animation-delay:.6s}.pxspk s:nth-child(8){left:76%;top:34%;animation-delay:1.5s}'
  '@keyframes pxglint{0%,15%{background-position:100% 0}60%,100%{background-position:0 0}}@keyframes pxspk{0%,100%{opacity:0;transform:scale(.2) rotate(0)}45%{opacity:1;transform:scale(1) rotate(45deg)}70%{opacity:0;transform:scale(.3) rotate(90deg)}}@keyframes pxhalo{50%{filter:drop-shadow(0 0 18px rgba(255,210,100,.8))}}'
  '.pxcard.gold{border-color:rgba(255,210,90,.65);background:radial-gradient(60% 90% at 12% 50%,rgba(255,200,80,.18),transparent 70%),linear-gradient(180deg,#2a2210,#140f06)}.pxcard.gold canvas{width:112px;height:112px}'
  '.prsk .pxglint,.prsk .pxspk{z-index:1}.prcard.gold{border-color:rgba(255,215,110,.75);box-shadow:0 0 26px rgba(255,200,80,.22),inset 0 0 30px rgba(255,200,80,.1)}.prcard.gold .prring{border:0;inset:-10px;background:conic-gradient(from 0deg,transparent,#ffd25a 12%,transparent 25%,#fff3c0 50%,transparent 62%,#ffd25a 80%,transparent);-webkit-mask:radial-gradient(closest-side,transparent 92%,#000 93%);mask:radial-gradient(closest-side,transparent 92%,#000 93%);box-shadow:none;animation:fgspin 6s linear infinite}'
  '.prcard.gold.own .prsk canvas{filter:drop-shadow(0 0 14px rgba(255,200,80,.6));animation:pxhalo 2.6s ease-in-out infinite}.prcard.gold::before{content:"";position:absolute;inset:0;pointer-events:none;background:radial-gradient(2px 2px at 12% 30%,#ffe7a0,transparent),radial-gradient(2px 2px at 82% 20%,#fff,transparent),radial-gradient(1.5px 1.5px at 70% 70%,#ffe7a0,transparent),radial-gradient(2px 2px at 25% 80%,#fff3c0,transparent),radial-gradient(1.5px 1.5px at 92% 55%,#ffd25a,transparent);animation:prdust 7s linear infinite}@keyframes prdust{from{transform:translateY(12px);opacity:.3}50%{opacity:1}to{transform:translateY(-12px);opacity:.3}}'
  '.prgold2{background:linear-gradient(100deg,#ffd25a 30%,#fff6d0 50%,#ffd25a 70%);background-size:250% 100%;-webkit-background-clip:text;background-clip:text;color:transparent!important;animation:pxglint 4s linear infinite}'
  '@media (prefers-reduced-motion:reduce){.pxspk,.pxglint,.prcard.gold::before{display:none}.pxgw canvas,.prprog button.g::after{animation:none}}\n')
i = s.index('</style>', s.index('#celeb{position:fixed')); s = s[:i] + css + s[i:]
s2 = re.sub(r"GAME_V = 626\b", "GAME_V = 627", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
