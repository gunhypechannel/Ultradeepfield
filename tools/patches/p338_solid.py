# v338: the guide no longer flashes. The idle Build/Lab/Ships chips pulse their opacity down to .55, and the guide hid itself every
# time its target dipped under .9 (the v334 fade-in check), so it blinked on and off. Its ring pulsed as well. Now: the target stops
# pulsing while it's pointed at, the fade-in check skips looping animations, and the ring and tip are solid.
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep("box-shadow:0 0 0 4px rgba(255,211,107,.25),0 0 26px rgba(255,211,107,.8);animation:tutp .8s ease-in-out infinite alternate;transition:left .18s,top .18s,width .18s,height .18s}",
    "box-shadow:0 0 0 4px rgba(255,211,107,.25),0 0 26px rgba(255,211,107,.8);transition:left .18s,top .18s,width .18s,height .18s}.gdon{animation:none!important}")
rep("#tutguide.nudge .tg-tip{animation:tgnudge 1.1s ease-in-out infinite}", "#tutguide.nudge .tg-tip{box-shadow:0 0 0 3px rgba(255,211,107,.55),0 6px 18px rgba(0,0,0,.5)}")
rep("if (el) { let op = 1; for (let n = el; n && n.nodeType === 1 && op > .5; n = n.parentElement) op *= +getComputedStyle(n).opacity;",
    "if (GD.on !== el) { if (GD.on) GD.on.classList.remove(\"gdon\"); if (el) el.classList.add(\"gdon\"); GD.on = el; } /* v338: what the guide points at stops pulsing */\n  if (el) { let op = 1; for (let n = el; n && n.nodeType === 1 && op > .5; n = n.parentElement) { const lp = n.getAnimations && n.getAnimations().some(a => a.effect && a.effect.getTiming && a.effect.getTiming().iterations === Infinity); if (!lp) op *= +getComputedStyle(n).opacity; } /* v338: a looping pulse isn't a fade-in */")
open(p, 'w', encoding='utf-8').write(t); print('ok')
