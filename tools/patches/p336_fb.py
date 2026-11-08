# v336: the floating Feedback button hides while the Academy guide points at something (it reappeared under taps meant for a
# closing card and opened the feedback form mid-step); Feedback is also in the Menu now
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep('body:has(.sheet) #fbBtn,body:has(#adv) #fbBtn,', 'body:has(.sheet) #fbBtn,body:has(#adv) #fbBtn,body:has(#tutguide.acad[style*="block"]) #fbBtn,')
rep('''<button class="mbtn" data-act="replayIntro">Replay briefing</button></div>''', '''<button class="mbtn" data-act="replayIntro">Replay briefing</button></div>
    <div class="mcard"><h3>${MI.user.replace("<svg", '<svg style="width:24px;height:24px;color:#38dfee"')}Feedback</h3><p>Found a bug, or something confusing? Tell us, with a screenshot if you like.</p><button class="mbtn" data-act="fbMenu">Send feedback</button></div>''')
rep('''  tutTour: () => {''', '''  fbMenu: () => { const b = document.getElementById("fbBtn"); if (b) b.click(); }, // v336
  tutTour: () => {''')
open(p, 'w', encoding='utf-8').write(t); print('ok')
