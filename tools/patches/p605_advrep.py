# v605 the Advisor never says the same line twice within 2 minutes (owner: "Make advisor not repeat same line for at least 2 minutes").
# One memory of what she said (G.advSaid: line -> time) is shared by her dialog and her hologram, so a line shown in either is not
# shown again in either for 2 minutes, live-event calls included. The dialog also drops a line already waiting in its queue. If every
# line of a dialog is filtered out, whatever was meant to follow it still runs.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('function say(lines) {\n  if (!lines.length) return;\n  advLines = (advLines || []).concat(lines);',
    '''const ADV_REP = 120000; /* v605 */
function advFresh(line) { const T = Date.now(), M = G.advSaid || (G.advSaid = {}); for (const k in M) if (T - M[k] > ADV_REP) delete M[k]; return !(M[line] && T - M[line] < ADV_REP); }
function advMark(line) { (G.advSaid || (G.advSaid = {}))[line] = Date.now(); }
function say(lines) {
  lines = (lines || []).filter((l, i, A) => l && A.indexOf(l) === i && !(advLines || []).includes(l) && advFresh(l)); lines.forEach(advMark); /* v605 nothing twice within 2 minutes */
  if (!lines.length) { if (!$("#adv") && G.advThen) { const th = G.advThen; G.advThen = null; try { th(); } catch (e) {} } return; }
  advLines = (advLines || []).concat(lines);''')
rep('  if (!force && G.holoSaid[line] && T0 - G.holoSaid[line] < 30000) return; // v386: not the same thing again within 30 s',
    '  if (!advFresh(line) && !(G.holoNext && G.holoNext.line === line)) return; // v386: not the same thing again within 30 s; v605: 2 minutes, shared with the dialog, live calls too')
rep('  G.holoSaid[line] = T0; G.holoCur = line; let w = $("#advh");', '  G.holoSaid[line] = T0; advMark(line); G.holoCur = line; let w = $("#advh");')
s2 = re.sub(r"GAME_V = 604\b", "GAME_V = 605", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
