# v615 (owner: "Build all except your first rival"): first-day goals + countdown, the come-back-tomorrow tease and its payoff (with a
# push reminder), the signal log with the first seven daily logins, the flagship lost in the prologue and rebuilt in the Academy,
# and quicker first jobs. See p615_firstday.js.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
js = open('tools/patches/p615_firstday.js', encoding='utf-8').read()
a = s.index('const chProg = (C, m) => '); s = s[:a] + js + '\n' + s[a:]
css = '.omb.d1b{border-color:#9dffc8;background:linear-gradient(90deg,rgba(4,30,22,.94),rgba(10,24,40,.94));color:#dfffee}.card.d1 header{display:flex;justify-content:space-between;align-items:baseline;gap:10px}.card.d1 header b{font-variant-numeric:tabular-nums;color:#9dffc8}.card.d1 .rw{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:10px}\n'
i = s.index('</style>', s.index('#celeb{position:fixed')); s = s[:i] + css + s[i:]
rep('    ${chronHTML()}', '    ${d1HTML()}${chronHTML()}')
rep('hb = omenBand(T) + wheelBand();', 'hb = omenBand(T) + d1Band(T) + wheelBand();')
rep('  loginClaim: () => act(() => { const ls = loginState(); if (ls.claimed) return;', '  d1Claim: () => d1Claim(), d1Go: () => { closeSheet(); ACT.nav({ v: "quests" }); }, /* v615 */\n  loginClaim: () => act(() => { const ls = loginState(); if (ls.claimed) return; loginStory();')
rep('  for (const g of [1, 2, 3]) { try { if (!wbGroupOn(g, T))', '  try { if (S.d1Tease && !S.d2Said) add("signal", Math.max(S.d1Tease + 20 * 3600e3, T + 60e3), "The signal is clearer", "Your Advisor has read the pyramid signal. Come back and hear what it says."); } catch (e) {} /* v615 */\n  for (const g of [1, 2, 3]) { try { if (!wbGroupOn(g, T))')
# the flagship in the prologue, and the Academy brings her back
rep('  { adv: 1, chip: "The Selection", line:', '  { img: "art/faction/", kb: "out", fx: "dim", chip: "The Flagship", line: "The flagship took the worst of it, Commander. She shielded the pods with her own hull. We\'ll rebuild her. I promise." },\n  { adv: 1, chip: "The Selection", line:')
rep('say: "The Flagship Dock is where our flagship is commissioned and where its gear is forged. Find it under Structures, in Facility."', 'say: "The Flagship Dock is where we rebuild the flagship that shielded our pods, and where her gear is forged. Find it under Structures, in Facility."')
rep('say: "Everything\'s ready, Commander. Commission the flagship: from now on it leads every fleet we send, gains experience and wears the gear the Dock forges."', 'say: "Everything\'s ready, Commander. Bring her back: commission the flagship. From now on she leads every fleet we send, gains experience and wears the gear the Dock forges."')
# quicker first jobs: in the first hour of the Academy every job is under five minutes, so it finishes free
rep('return now() - S.tutFast < 3 * 864e5 ? Math.min(t * .25, 600000) : t; };', 'return now() - S.tutFast < 3600e3 ? Math.min(t * .25, 240000) : now() - S.tutFast < 3 * 864e5 ? Math.min(t * .25, 600000) : t; }; /* v615 the first hour: every job finishes free */')
s2 = re.sub(r"GAME_V = 614\b", "GAME_V = 615", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
