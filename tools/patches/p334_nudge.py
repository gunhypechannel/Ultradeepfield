import sys, re
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# v334 a hint when a commander seems stuck: after 20 s without a tap on an Academy step that's waiting on them (not on a timer),
# the rest of the screen dims around the target and the guide's tip pulses; counted per step in the private save (S.tutStuck)
rep('''function guideFrame() {''', '''addEventListener("pointerdown", () => { G.lastIn = performance.now(); }, true); addEventListener("keydown", () => { G.lastIn = performance.now(); }, true);
const GUIDE_WAIT = /on its way|flying home|Under construction|Researching|in production|Queued|finishes on its own|Wait|gathering|ready in/i;
function guideFrame() {''')
rep('''  g.style.display = "block"; g.classList.toggle("spot", S.tut.i < 9);''',
    '''  const nudge = tutOn() && performance.now() - (G.lastIn || performance.now()) > 20000 && !GUIDE_WAIT.test(GD.label || "") && !document.hidden; // v334
  if (nudge && G.nudged !== S.tut.i) { G.nudged = S.tut.i; const k = tutKey(S.tut.i); S.tutStuck = S.tutStuck || {}; S.tutStuck[k] = (S.tutStuck[k] || 0) + 1; dirty(); }
  g.style.display = "block"; g.classList.toggle("spot", S.tut.i < 9 || nudge); g.classList.toggle("nudge", nudge);''')
rep('''@media (prefers-reduced-motion:reduce){#tutguide .tg-ring,#tutguide .tg-hand{animation:none;transition:none}}''',
    '''#tutguide.nudge .tg-tip{animation:tgnudge 1.1s ease-in-out infinite}#tutguide.nudge .tg-hand{font-size:48px}
@keyframes tgnudge{0%,100%{transform:scale(1)}50%{transform:scale(1.07)}}
@media (prefers-reduced-motion:reduce){#tutguide .tg-ring,#tutguide .tg-hand,#tutguide.nudge .tg-tip{animation:none;transition:none}}''')
v = int(re.search(r"const GAME_V = (\d+)", t).group(1)); t = t.replace(f"const GAME_V = {v}", "const GAME_V = 334", 1)
open(p, 'w', encoding='utf-8', newline='').write(t); print('v334 from', v)
