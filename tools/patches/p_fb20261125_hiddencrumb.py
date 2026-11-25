# fb-20261125: a crash report from the owner's Fold (v749) read "Closed unexpectedly after: session restored: ally (1 min)".
# The log shows the game went to the background 4 s after launch ("background: 1 drawing buffers released", the session
# marked closed), and 26 s later, still hidden (no "back from the background" line), the delayed session restore ran and
# wrote its crumb. crumb() always set CRUMBS.open = true, so a session sitting in the background was reopened; when Android
# then closed the hidden app normally, the next launch reported it as a crash. A crumb written while the page is hidden now
# leaves the session closed (the visibilitychange handler reopens it on return, as before). Diagnostics only.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('function crumb(msg) { CRUMBS.open = true; CRUMBS.ev.push(',
  'function crumb(msg) { CRUMBS.open = !document.hidden; /* fb-20261125 a crumb written in the background must not reopen the session */ CRUMBS.ev.push('),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
