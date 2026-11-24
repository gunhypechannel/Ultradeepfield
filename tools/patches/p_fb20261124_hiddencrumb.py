# fb-20261124: a false "Closed unexpectedly after: session restored: rank (0 min)" crash report (owner's iPhone, v741).
# The game went to the background 6 s after launch (the hide handler and bgDiet closed the session), then the session
# restore timer still fired 3 s later while the page was hidden; its crumb() set CRUMBS.open = true again, so when iOS
# later closed the hidden page the next launch reported a crash. Same class of bug as fb-20261112 (bgDiet's crumb).
# A crumb written while the page is hidden is still logged but no longer reopens the session; coming back to the
# screen reopens it as before (the visibilitychange listener), and background kills keep their own udf.bg report.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('function crumb(msg) { CRUMBS.open = true; CRUMBS.ev.push(',
  'function crumb(msg) { if (!document.hidden) CRUMBS.open = true; /* fb-20261124 a crumb while hidden must not reopen the session */ CRUMBS.ev.push('),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
