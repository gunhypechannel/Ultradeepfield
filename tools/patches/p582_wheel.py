# v582 The casino Glyph Wheel (owner: "Spinning the wheel should get a better casino sound effect and the jackpot should have more
# animation! It should make players want to spin, allow players to buy lottery spins and put better prizes or increase payouts", and
# "Shouldn't there be some kind of daily reminder to spin the wheel in the shop?").
# Sound: a lever clunk and whoosh, a ratchet clack on every peg, ding-ding and coins on a prize, alarm bells + fanfare + a coin shower
# on a jackpot (all synthesised, WSFX). Show: BIG WIN / JACKPOT / MEGA JACKPOT over the whole screen (gold rays, letters slamming in,
# shards counting up, coins raining, the screen shakes). Paid spins: ◆5 a spin or 5 for ◆22, at most 25 bought a day (S.whlCr credits,
# S.whlPd). Better prizes: every shard prize is bigger, a ◆50 Jackpot and a ◆250 Mega Jackpot, better items more often, odds shown on
# every prize. Reminder: a glowing dot on the ◆ shard button while today's free spin is unused, a "🎰 FREE SPIN READY" band on the
# planet (opens the shop at the wheel), and once a day the Advisor mentions it (3 voiced lines). Not during the Academy.
import sys, re, json
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# better prizes (shard prizes up, two jackpots, the best items more often)
i = s.index('const WHEEL = ['); j = s.index('const wheelName = W =>')
s = s[:i] + '''const WHEEL = [{ k: "sh", n: 3, g: "ᚠ", l: "◆3", col: "#c88aff", w: 12 }, { k: "sh", n: 50, g: "ᛟ", l: "◆50", col: "#ffcf5a", w: .5, jack: 1 }, { k: "sh", n: 5, g: "ᚢ", l: "◆5", col: "#c88aff", w: 9 },
  { k: "crateM", g: "ᛗ", l: "🔩", col: "#b8c6d6", w: 8 }, { k: "xf_bronze", g: "ᚱ", l: "🚀", col: "#ff8a3a", w: 7 }, { k: "sh", n: 10, g: "ᛊ", l: "◆10", col: "#d9a0ff", w: 4 }, { k: "xb_bronze", g: "ᛒ", l: "🏗", col: "#ffb35a", w: 6 },
  { k: "crateC", g: "ᚲ", l: "💎", col: "#7af4ff", w: 7 }, { k: "vipAct1", g: "ᛇ", l: "👑1d", col: "#ffd66a", w: 2 }, { k: "boost5", g: "ᛉ", l: "⚡5", col: "#55d6e8", w: 7 }, { k: "vipPts100", g: "ᚹ", l: "👑+", col: "#ffe08a", w: 5 },
  { k: "crateG", g: "ᚷ", l: "🧪", col: "#5dff9a", w: 6 }, { k: "sh", n: 25, g: "ᛞ", l: "◆25", col: "#ffb0f0", w: 1.5 }, { k: "xr_bronze", g: "ᛁ", l: "🔬", col: "#9a7bff", w: 5 }, { k: "mb1", g: "ᛜ", l: "🧰", col: "#c8d4e0", w: 5 },
  { k: "bm_bronze", g: "ᛏ", l: "⛏", col: "#d0dbe6", w: 4 }, { k: "pAll_gold", g: "ᛚ", l: "📦", col: "#ffcf5a", w: 1.2 }, { k: "bf_bronze", g: "ᚦ", l: "🛸", col: "#5a9aff", w: 4 }, { k: "xs_bronze", g: "ᚾ", l: "🛠", col: "#55e0c0", w: 4 },
  { k: "mb2", g: "ᛃ", l: "🧰+", col: "#5dff9a", w: 2.5 }, { k: "sh", n: 250, g: "ᛝ", l: "◆250", col: "#ff6ad5", w: .08, jack: 2 }]; /* v582 better prizes */
''' + s[j:]
s = s.replace('/* v551 the remastered Holo Glyph Wheel', open('tools/patches/p582_wheel.js', encoding='utf-8').read() + '/* v551 the remastered Holo Glyph Wheel', 1)
# the wheel's card: paid spins, odds, credits
rep('function wheelHTML(T) { const own = !!G.owner, bon = (S.shopFree || "") === shopDay() && cosPrem(G.me) && (S.shopFree2 || "") !== shopDay(), can = (own || (S.shopFree || "") !== shopDay() || bon) && S.wheelPend == null,',
    'function wheelHTML(T) { const own = !!G.owner, bon = (S.shopFree || "") === shopDay() && cosPrem(G.me) && (S.shopFree2 || "") !== shopDay(), cr = S.whlCr || 0, can = (own || (S.shopFree || "") !== shopDay() || bon || cr > 0) && S.wheelPend == null,')
rep('<b>${W.g}</b>${esc(wheelName(W))}${W.jack ? " · jackpot" : ""}</span>`).join("");',
    '<b>${W.g}</b>${esc(wheelName(W))}${W.jack === 2 ? " · MEGA JACKPOT" : W.jack ? " · JACKPOT" : ""}<em>${whlPct(W)}%</em></span>`).join("");')
rep(': can ? (bon && !own ? "♛ Premium bonus spin" : "Free daily spin") : "Spun today"}</b>',
    ': can ? ((S.shopFree || "") !== shopDay() ? "Free daily spin" : bon && !own ? "♛ Premium bonus spin" : cr > 0 ? `${cr} paid spin${cr > 1 ? "s" : ""} ready` : "Free daily spin") : "Spun today"}</b>')
rep('Pull the lever to spin the rings. One free spin every day, ${WHEEL.length} prizes.` : `Next spin in <b data-end="${shopDayEnd()}">${ftime(shopDayE',
    'Pull the lever to spin the rings. ${WHEEL.length} prizes, a ◆50 Jackpot and a ◆250 Mega Jackpot.` : `Next free spin in <b data-end="${shopDayEnd()}">${ftime(shopDayE')
rep('<div class="gwchips">${chips}</div>', '${spin ? "" : `<div class="gwbuy"><button class="btn amber sm" data-act="whlBuy" data-n="1" ${(S.shards || 0) >= WHL_COST && whlBought() < WHL_CAP ? "" : "disabled"}>🎰 Spin ◆${WHL_COST}</button><button class="btn amber sm" data-act="whlBuy" data-n="5" ${(S.shards || 0) >= WHL_PACK[1] && whlBought() + 5 <= WHL_CAP ? "" : "disabled"}>5 spins ◆${WHL_PACK[1]}</button><small>${whlBought()}/${WHL_CAP} bought today</small></div>`}<div class="gwchips">${chips}</div>')
# the pull: a paid credit when today's free spin is gone; the lever sound
rep('function wheelPull() { const bon = (S.shopFree || "") === shopDay() && cosPrem(G.me) && (S.shopFree2 || "") !== shopDay(); if (G.wheel || (!G.owner && (S.shopFree || "") === shopDay() && !bon) || S.wheelPend != null) return;',
    'function wheelPull() { const bon = (S.shopFree || "") === shopDay() && cosPrem(G.me) && (S.shopFree2 || "") !== shopDay(), free = (S.shopFree || "") !== shopDay(), paid = !free && !bon && !G.owner && (S.whlCr || 0) > 0; if (G.wheel || (!G.owner && !free && !bon && !paid) || S.wheelPend != null) return; try { WSFX.lever(); } catch (e) {}')
rep('act(() => { if ((S.shopFree || "") === shopDay() && !G.owner) S.shopFree2 = shopDay(); S.shopFree = shopDay(); S.wheelPend = idx; bump("wheelSpins"); });',
    'act(() => { if (paid) S.whlCr = Math.max(0, (S.whlCr || 0) - 1); else { if ((S.shopFree || "") === shopDay() && !G.owner) S.shopFree2 = shopDay(); S.shopFree = shopDay(); } S.wheelPend = idx; bump("wheelSpins"); });')
rep('try { SFX.click(); } catch (er) {} } if (G.whlA) G.whlA.tick = 1;', 'try { WSFX.tick(G.whlA ? G.whlA.v : 300); } catch (er) {} } if (G.whlA) G.whlA.tick = 1;')
rep('toast(`${W.jack ? "JACKPOT! " : ""}Glyph Wheel: ${wheelName(W)}${W.k === "sh" ? "" : " added to your inventory"}. Spin again tomorrow.`, "win"); try { W.jack ? SFX.fanfare(true) : SFX.research(); } catch (e) {} }',
    'toast(`${W.jack === 2 ? "MEGA JACKPOT! " : W.jack ? "JACKPOT! " : ""}Glyph Wheel: ${wheelName(W)}${W.k === "sh" ? "" : " added to your inventory"}.${(S.whlCr || 0) > 0 ? ` ${S.whlCr} spin${S.whlCr > 1 ? "s" : ""} left.` : " Your next free spin comes tomorrow."}`, "win");\n'
    '  try { W.jack ? WSFX.jackpot(W.jack === 2) : WSFX.win(W.w <= 2.5 ? 1 : 0); } catch (e) {} if (W.jack || W.w <= 2.5) try { wheelShow(W); } catch (e) {} try { render(true); } catch (e) {} } /* v582 */')
# the daily reminder: the band on the planet, the dot on the shard button
rep('if (!html && view === "base" && !sheet && !battle) html = omenBand(T); /* v580 the week\'s omen: on the planet only */',
    'if (!html && view === "base" && !sheet && !battle) html = omenBand(T); /* v580 the week\'s omen: on the planet only */\n  if (view === "base" && !sheet && !battle && !cineOn) { const wb = wheelBand(); if (wb) html = (html || "") + wb; } /* v582 */')
rep('<button class="prem" data-act="openShop" aria-label="Void Shop, ${fmt(S.shards || 0)} Void Shards"><span class="shard">◆</span> ${fmt(S.shards || 0)}</button>',
    '<button class="prem${whlFree() ? " wdot" : ""}" data-act="${whlFree() ? "whlGo" : "openShop"}" aria-label="Void Shop, ${fmt(S.shards || 0)} Void Shards${whlFree() ? ", free spin ready" : ""}"><span class="shard">◆</span> ${fmt(S.shards || 0)}</button>')
rep('  openShop: () => openSheet({ type: "shop", cat: "boost" }),', '  openShop: () => openSheet({ type: "shop", cat: "boost" }), whlGo: () => openSheet({ type: "shop", cat: "boost" }), whlBuy: d => whlBuy(+d.n || 1), /* v582 */')
rep('const ADV_MOOD_L = {', 'const ADV_MOOD_L = {' + ', '.join(json.dumps(x, ensure_ascii=False) + ': "playful"' for x in [
    "Commander, your free spin on the Glyph Wheel is waiting in the Void Shop. Today could be the jackpot.",
    "The Glyph Wheel has a free spin for you today. Go on, pull the lever. I'll keep my fingers crossed.",
    "Don't forget your free spin, Commander. The wheel is glowing, just waiting for you."]) + ', ')
rep('.gwchips{display:flex;flex-wrap:wrap;justify-content:center;gap:5px;margin-top:6px}', '''.gwchips{display:flex;flex-wrap:wrap;justify-content:center;gap:5px;margin-top:6px}.gwchips em{font-style:normal;opacity:.7;margin-left:5px;font-size:.92em}
.gwbuy{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:8px;margin-top:8px}.gwbuy small{flex-basis:100%;opacity:.65;font-size:11px}
.prem.wdot{position:relative}.prem.wdot::after{content:"";position:absolute;top:-3px;right:-3px;width:11px;height:11px;border-radius:50%;background:#ff4fa3;box-shadow:0 0 0 2px #0a1020,0 0 10px #ff4fa3;animation:wdot 1.4s ease-in-out infinite}
@keyframes wdot{50%{transform:scale(1.35);box-shadow:0 0 0 2px #0a1020,0 0 18px #ffcf5a}}
#omband{display:flex;flex-direction:column;align-items:center;gap:6px}.omb.whb{border-color:#ffcf5a;background:linear-gradient(90deg,rgba(60,24,4,.94),rgba(40,8,48,.94));color:#ffeab0;box-shadow:0 0 18px rgba(255,207,90,.45);animation:whb 2.2s ease-in-out infinite}
@keyframes whb{50%{box-shadow:0 0 30px rgba(255,120,200,.6)}}
#gwjp{position:fixed;inset:0;z-index:9000;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at 50% 50%,rgba(60,30,0,.55),rgba(0,0,0,.82));animation:gwjin .25s ease-out;cursor:pointer;overflow:hidden}
#gwjp.l1{background:radial-gradient(circle at 50% 50%,rgba(40,20,60,.35),rgba(0,0,0,.55))}#gwjp.out{animation:gwjout .4s ease-in forwards}
#gwjp canvas{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.gwjr{position:absolute;left:50%;top:50%;width:220vmax;height:220vmax;margin:-110vmax 0 0 -110vmax;background:repeating-conic-gradient(rgba(255,214,110,.22) 0 7deg,transparent 7deg 18deg);animation:gwjspin 9s linear infinite;mask:radial-gradient(circle,#000 0,transparent 30%);-webkit-mask:radial-gradient(circle,#000 0,transparent 30%)}
#gwjp.l1 .gwjr{opacity:.5}#gwjp.l3 .gwjr{background:repeating-conic-gradient(rgba(255,110,210,.25) 0 7deg,rgba(110,230,255,.18) 7deg 12deg,transparent 12deg 18deg);animation-duration:5s}
.gwjc{position:relative;display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center;padding:0 16px}
.gwjt{font-family:var(--f-display);font-weight:900;font-size:clamp(40px,13vw,104px);letter-spacing:.04em;line-height:1;white-space:nowrap}
#gwjp.l1 .gwjt{font-size:clamp(34px,10vw,72px)}#gwjp.l3 .gwjt{font-size:clamp(30px,10.5vw,96px)}
.gwjt span{display:inline-block;background:linear-gradient(180deg,#fff8d8 0%,#ffd34a 45%,#e07a00 60%,#ffe9a0 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 0 14px rgba(255,190,60,.9)) drop-shadow(0 4px 0 #6a3500);animation:gwjl .55s cubic-bezier(.2,1.6,.4,1) both,gwjb 1.1s ease-in-out infinite;animation-delay:calc(var(--i) * 70ms),calc(.6s + var(--i) * 70ms)}
#gwjp.l3 .gwjt span{background:linear-gradient(180deg,#fff 0%,#ff9be8 35%,#8af0ff 65%,#fff6a0 100%);-webkit-background-clip:text;background-clip:text;filter:drop-shadow(0 0 16px rgba(255,120,220,.95)) drop-shadow(0 4px 0 #3a0a5a);animation:gwjl .55s cubic-bezier(.2,1.6,.4,1) both,gwjb 1.1s ease-in-out infinite,gwjh 2s linear infinite;animation-delay:calc(var(--i) * 70ms),calc(.6s + var(--i) * 70ms),0s}
.gwja{font-family:var(--f-display);font-size:clamp(30px,9vw,64px);font-weight:800;color:#ffe9a8;text-shadow:0 0 18px rgba(255,200,80,.9);animation:gwjl .6s .5s cubic-bezier(.2,1.6,.4,1) both}#gwjp.l1 .gwja{font-size:clamp(22px,6vw,40px)}
.gwjc small{color:#fff;opacity:.75;animation:gwjin .4s 1.2s both}
@keyframes gwjin{from{opacity:0}}@keyframes gwjout{to{opacity:0;transform:scale(1.06)}}@keyframes gwjspin{to{transform:rotate(360deg)}}
@keyframes gwjl{0%{opacity:0;transform:translateY(-60px) scale(2.6) rotate(-8deg)}100%{opacity:1;transform:none}}@keyframes gwjb{50%{transform:translateY(-6px) scale(1.06)}}@keyframes gwjh{to{filter:hue-rotate(360deg) drop-shadow(0 0 16px rgba(255,120,220,.95))}}
#app.gwshake{animation:gwshake .9s cubic-bezier(.36,.07,.19,.97)}@keyframes gwshake{10%,90%{transform:translate(-2px,1px)}20%,80%{transform:translate(4px,-2px)}30%,50%,70%{transform:translate(-7px,3px)}40%,60%{transform:translate(7px,-3px)}}''')
# the jackpot lines: the old one named the old ◆25 jackpot; a new line for the Mega Jackpot
OLDJ = "Twenty-five shards! I'm not saying I rigged it... but I'm not saying I didn't."; NEWJ = "Fifty shards! I'm not saying I rigged it... but I'm not saying I didn't."
MEGA = "Two hundred and fifty shards! Commander, the whole wheel just lit up for you. I've never seen that happen!"
rep(OLDJ, NEWJ, 2)
rep('"x_jack1": ', '"x_mega": ' + json.dumps(MEGA) + ', "x_jack1": ')
rep('const ADV_MOOD_L = {', 'const ADV_MOOD_L = {' + json.dumps(MEGA) + ': "excited", ')
rep('try { if (W.jack) advHolo(ADV_NEWS[advPk("x_jack", 2)], true);', 'try { if (W.jack === 2) advHolo(ADV_NEWS.x_mega, true); else if (W.jack) advHolo(ADV_NEWS[advPk("x_jack", 2)], true);')
rep('won ? `${won.jack ? "JACKPOT! " : ""}You won', 'won ? `${won.jack === 2 ? "MEGA JACKPOT! " : won.jack ? "JACKPOT! " : ""}You won')
s2 = re.sub(r"GAME_V = 580\b", "GAME_V = 582", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
