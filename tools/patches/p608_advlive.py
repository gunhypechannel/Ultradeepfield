# v608 the Advisor comes alive: a face for every mood, lips that follow her voice, blinks, and full-body poses for the big moments
# (see p608_advlive.js). Art: docs/art/adv/*.webp, cut from the owner's expression and pose sheets with the backgrounds removed;
# the talking frames (n_1, n_2) and the blink (n_b) are her mouth and eyes laid onto the one neutral face (n_0) so nothing jumps.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# every line she shows picks her face
rep('$("#advt").textContent = advLines[0]; try { document.documentElement.dataset.advMood = advMood(advLines[0]); } catch (e) {} speak(advLines[0]);',
    '$("#advt").textContent = advLines[0]; try { document.documentElement.dataset.advMood = advMood(advLines[0]); } catch (e) {} speak(advLines[0]); try { afSet(advLines[0], "dlg"); } catch (e) {} /* v608 */', 2)
rep('try { document.documentElement.dataset.advMood = advMood(line); } catch (e) {} /* v566 */',
    'try { document.documentElement.dataset.advMood = advMood(line); } catch (e) {} /* v566 */ setTimeout(() => { try { afSet(line, "holo"); } catch (e) {} }, 0); /* v608 */')
rep('speak(FTOUR_[i][1]); ftPlace();', 'speak(FTOUR_[i][1]); try { afSet(FTOUR_[i][1], "tour"); } catch (e) {} /* v608 */ ftPlace();')
# celebrations with her art show a full pose; an incoming attack brings the alarm pose
rep('c.art === "adv" ? ADV_ART : null', 'c.art === "adv" ? advCelebArt(c) : null')
rep('class="cbart${c.art === "adv" ? " adv" : ""}"', 'class="cbart${c.art === "adv" ? " adv" + (afOn() ? " pose" : "") : ""}"')
rep('fresh.forEach(x => G.alertSeen.add(x.id));', 'fresh.forEach(x => G.alertSeen.add(x.id)); try { advPose("alarm", { force: 1 }); } catch (e) {} /* v608 */')
CSS = r'''
/* v608 her faces and poses */
.adv .advimg.afc{height:auto;aspect-ratio:420/510;object-position:50% 0}
#advh .advimg.afc{object-position:50% 0}
.cbart.adv.pose{aspect-ratio:auto;height:min(260px,32vh);width:auto;max-width:100%;object-fit:contain;border:0;border-radius:0;filter:drop-shadow(0 10px 26px rgba(0,0,0,.55)) drop-shadow(0 0 22px rgba(255,200,120,.25))}
#advpose{position:fixed;z-index:40;bottom:calc(env(safe-area-inset-bottom,0px) + 58px);right:max(0px,env(safe-area-inset-right,0px));height:min(50vh,540px);pointer-events:none;opacity:0;transform:translateX(40px);transition:opacity .45s ease,transform .55s cubic-bezier(.2,.9,.3,1)}
#advpose.l{right:auto;left:max(0px,env(safe-area-inset-left,0px));transform:translateX(-40px)}
#advpose.on{opacity:1;transform:none}
#advpose img{display:block;height:100%;width:auto;max-width:62vw;object-fit:contain;object-position:50% 100%;-webkit-mask-image:linear-gradient(180deg,#000 78%,transparent);mask-image:linear-gradient(180deg,#000 78%,transparent);opacity:.92;filter:drop-shadow(0 0 16px rgba(85,214,232,.7)) grayscale(1) sepia(.6) hue-rotate(150deg) saturate(2.3) brightness(1.1) contrast(1.08)}
#advpose.on img{animation:holoIn .8s cubic-bezier(.2,.9,.3,1) both,holoFlick 7s 1.2s infinite}
#advpose.flip img{transform:scaleX(-1)}
#advpose .apbeam{position:absolute;left:10%;right:10%;bottom:-8px;height:26px;background:radial-gradient(ellipse 50% 40% at 50% 55%,rgba(170,245,255,.9),rgba(85,214,232,.4) 45%,transparent 72%);filter:blur(1.5px)}
#advpose.color img{opacity:1;filter:drop-shadow(0 10px 22px rgba(0,0,0,.6))}
#advpose.color .apbeam{display:none}
@media (prefers-reduced-motion:reduce){#advpose,#advpose.on img{transition:opacity .3s;transform:none;animation:none}#advpose.flip img{transform:scaleX(-1)}}
'''
m = re.search(r'html\[data-adv-mood=tender\] #advh\.talk \.advimg[^{]*\{[^}]*\}', s); assert m
s = s[:m.end()] + CSS + s[m.end():]
i = s.index('/* ---------- v589 battle effects remaster'); s = s[:i] + open('tools/patches/p608_advlive.js', encoding='utf-8').read() + s[i:]
s2 = re.sub(r"GAME_V = 607\b", "GAME_V = 608", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
