# v718: the Harbinger's heartbeat (see p718_harb.js)
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__)); R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
A = 'const TCH_ASK = "'
i = s.index(A); j = s.index('\n', i); assert s.count(A) == 1
s = s[:j + 1] + R('p718_harb.js') + s[j + 1:]
rep('function drawBattle(t) {\n  const b = battle, cv = $("#bcv"); if (!cv) return;', 'function drawBattle(t) {\n  const b = battle, cv = $("#bcv"); if (!cv) return; try { harbBattle(b); } catch (e) {} /* v718 the Harbinger\'s heart under the fight */')
rep('.crcprev{', '.hbN{animation:hbPulse var(--hbp,1.15s) infinite ease-out;border-radius:3px}\n@keyframes hbPulse{0%{text-shadow:0 0 0 transparent}6%{color:#c9ffe0;text-shadow:0 0 6px #3dff9a,0 0 14px rgba(61,255,154,.6)}14%{text-shadow:0 0 2px rgba(61,255,154,.3)}22%{color:#b0ffd4;text-shadow:0 0 5px #3dff9a}40%,100%{text-shadow:0 0 0 transparent}}\n@media (prefers-reduced-motion:reduce){.hbN{animation:none}}\n.crcprev{')
rep('const GAME_V = 717;', 'const GAME_V = 718;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
