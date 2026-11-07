import sys
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# v333 every Academy step has a permanent id, and the save remembers the id of the step you're on (S.tut.k). When steps are
# added or moved in a later version, the save finds its step by id instead of by position, so no more index-shifting migrations.
lines = t.split('\n')
start = next(i for i, l in enumerate(lines) if l.startswith('const TUT = ['))
end = next(i for i in range(start, start + 80) if lines[i] == '];')
lines.insert(end + 1, 'TUT.forEach(s => { if (!s.id) s.id = s.t.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, ""); }); // v333: a permanent id for every step')
t = '\n'.join(lines)
rep('''  if (!S.tutScout) { S.tutScout = 1; if (S.tut.i > 12) S.tut.i = Math.min(TUT.length, S.tut.i + 2); dirty(); } /* v332: two scouting steps before the first attack; anyone past them keeps their place */''',
    '''  if (!S.tutScout) { S.tutScout = 1; if (S.tut.i > 12) S.tut.i = Math.min(TUT.length, S.tut.i + 2); dirty(); } /* v332: two scouting steps before the first attack; anyone past them keeps their place */
  if (!G.tutFound) { G.tutFound = 1; const k = S.tut.k, j = k && k !== "done" ? TUT.findIndex(s => s.id === k) : -1; if (j >= 0 && j !== S.tut.i) { S.tut.i = j; dirty(); } } // v333: back to the step this save was on, wherever it now sits
  { const k = TUT[S.tut.i] ? TUT[S.tut.i].id : "done"; if (S.tut.k !== k) { S.tut.k = k; dirty(); } }''')
open(p, 'w', encoding='utf-8', newline='').write(t); print('ok')
