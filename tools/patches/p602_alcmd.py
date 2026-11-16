# v602 Alliance Command: the Space Station as the hero, the Cube's plot, a sticky tab bar (see p602_alcmd.js)
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
i = s.index('function alHome(a) {'); j = s.index('/* defense in two steps', i)
s = s[:i] + open('tools/patches/p602_alcmd.js', encoding='utf-8').read() + s[j:]
# the help card without the station (the station has its own tab now)
rep('function helpCards(a) {', 'function helpCards(a, noSt) {')
rep('''    <div class="mcard station"><img class="stimg" src="art/allyStation.webp" alt="Alliance space station" loading="lazy"><h3>Space Station · Lv.${L}</h3>''',
    '''    ${noSt ? "" : `<div class="mcard station"><img class="stimg" src="art/allyStation.webp" alt="Alliance space station" loading="lazy"><h3>Space Station · Lv.${L}</h3>''')
rep('''<p class="note">The station is fully built: 100 members.</p>'}</div>`;''', '''<p class="note">The station is fully built: 100 members.</p>'}</div>`}`;''')
rep('    if (part === "fund") return helpCards(a) + fundCard; /* v584 */', '    if (part === "fund") return helpCards(a) + fundCard; /* v584 */\n    if (part === "fundOnly") return fundCard; /* v602 */')
# switching tabs keeps your place; if you'd scrolled past the tab bar it brings the bar back to the top
rep('alPg: d => { sub.alP = d.v || ""; sub.depU = null; G.crestOpen = false; render(true); try { const v = document.querySelector("#view, main"); if (v) v.scrollTop = 0; } catch (e) {} },',
    'alPg: d => { sub.alP = d.v || ""; sub.depU = null; G.crestOpen = false; render(true); try { const v = document.querySelector("#view, main"), t = document.querySelector(".altabs"); if (v && t) { const top = t.getBoundingClientRect().top - v.getBoundingClientRect().top + v.scrollTop; if (v.scrollTop > top) v.scrollTop = top; } } catch (e) {} }, /* v602 */')
CSS = '''.alcmd{position:relative;display:flex;flex-direction:column;justify-content:space-between;gap:14px;min-height:230px;padding:14px;border-radius:20px;overflow:hidden;border:1px solid rgba(85,214,232,.4);box-shadow:0 0 28px rgba(85,214,232,.15);isolation:isolate}
.alcmdart{position:absolute;inset:0;z-index:-1}.alcmdart img{width:100%;height:100%;object-fit:cover;object-position:60% 40%;animation:alpan 26s ease-in-out infinite alternate;transform-origin:60% 45%}.alcmdart::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(3,8,16,.55),rgba(3,8,16,.05) 35%,rgba(3,8,16,.25) 60%,rgba(3,8,16,.92)),radial-gradient(90% 70% at 0 0,rgba(3,8,16,.75),transparent 60%)}
@keyframes alpan{from{transform:scale(1.04) translateX(0)}to{transform:scale(1.14) translateX(-3%)}}
.alcmdscan{position:absolute;left:0;right:0;height:40%;top:-40%;background:linear-gradient(180deg,transparent,rgba(122,244,255,.12),transparent);animation:alscan 6s linear infinite;z-index:1}@keyframes alscan{to{top:110%}}
@media (prefers-reduced-motion:reduce){.alcmdart img,.alcmdscan{animation:none}}
.alcmdtop{display:flex;align-items:center;gap:12px}.alcmdtop .alcrest{flex:none}.alcmdid{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px}.alcmdid small{font:600 10.5px var(--f-display);letter-spacing:.18em;color:#7af4ff;text-shadow:0 1px 4px #000}.alcmdid b{font:700 21px/1.15 var(--f-display);color:#fff;text-shadow:0 2px 10px #000;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.alcmdid b em{font-style:normal;color:#ffd36b}
.alonl{display:flex;align-items:center;padding-left:8px}.alonl>i{width:26px;height:26px;margin-left:-8px;border-radius:50%;border:2px solid #08121c;overflow:hidden;display:block}.alonl>i .avc{width:100%!important;height:100%!important;display:block}.alonl em{font-style:normal;margin-left:8px;font-size:12.5px;color:#d6e6ee;text-shadow:0 1px 4px #000;display:flex;align-items:center;gap:5px}
.alcmdst{display:grid;gap:6px;text-align:left;padding:10px 12px;border-radius:14px;border:1px solid rgba(255,211,107,.5);background:rgba(6,12,24,.62);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);color:#eaf7fc;cursor:pointer}.alcmdst:active{transform:scale(.99)}
.alsttl{font:600 11.5px var(--f-display);letter-spacing:.16em;color:#ffd36b}.alsttl b{color:#fff;margin-left:4px}.alstbar{height:6px;border-radius:3px;background:rgba(255,255,255,.12);overflow:hidden}.alstbar i{display:block;height:100%;background:linear-gradient(90deg,#ffb02e,#ffe6a0);box-shadow:0 0 8px #ffb02e}
.alstcap{display:flex;justify-content:space-between;gap:8px;font-size:13px;color:#cfe0ea}.alstcap b{color:#fff}.alstcap em{font-style:normal;color:#7af4ff;font-weight:600}
.altabs{position:sticky;top:0;z-index:6;display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;padding:5px;border-radius:14px;border:1px solid var(--line);background:rgba(5,10,18,.94);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}.altabs::-webkit-scrollbar{display:none}
.altabs button{position:relative;flex:1 1 0;min-width:0;display:flex;flex-direction:column;align-items:center;gap:2px;padding:7px 2px;border:0;border-radius:10px;background:none;color:#8fa6b6;font:600 10px var(--f-body);letter-spacing:-.01em;cursor:pointer;white-space:nowrap}.altabs button span{max-width:100%;overflow:hidden;text-overflow:ellipsis}.altabs svg{width:20px;height:20px}.altabs button.on{background:rgba(85,214,232,.16);color:#eaf7fc;box-shadow:inset 0 0 0 1px rgba(85,214,232,.5)}.altabs button.on svg{color:var(--cyan);filter:drop-shadow(0 0 5px rgba(85,214,232,.6))}.altabs .cbadge{position:absolute;top:2px;right:6px}
.alpane{display:flex;flex-direction:column;gap:10px}
.alstart{position:relative;border-radius:14px;overflow:hidden;aspect-ratio:16/8;max-width:100%;border:1px solid rgba(255,211,107,.35)}.alstart img{width:100%;height:100%;object-fit:cover;display:block}.alstlv{position:absolute;right:10px;top:8px;font:800 26px var(--f-display);color:#ffd36b;text-shadow:0 0 12px rgba(255,176,46,.8),0 2px 6px #000}.alstlv small{font-size:13px;color:#e6eef4;margin-left:2px}
.alpips{display:flex;gap:4px}.alpips i{flex:1;height:6px;border-radius:3px;background:rgba(255,255,255,.1)}.alpips i.on{background:linear-gradient(90deg,#ffb02e,#ffe6a0);box-shadow:0 0 6px #ffb02e}.alpips i.nx{box-shadow:inset 0 0 0 1px rgba(255,211,107,.7)}
.alstup{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap}
.allvl{display:grid!important;grid-template-columns:minmax(0,1fr) 90px auto;align-items:center;gap:12px;width:100%;text-align:left;cursor:pointer;color:inherit}.allvl span:first-child{display:flex;flex-direction:column;gap:2px;min-width:0}.allvl b{font:700 15px var(--f-display)}.allvl small{font-size:12px;color:#93b2c3}.allvl em{font-style:normal;color:var(--muted);font-size:18px}
'''
rep('.al2 .alh2{', CSS + '.al2 .alh2{')
s2 = re.sub(r"GAME_V = 601\b", "GAME_V = 602", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
