# fb-20261118: "Noticed format on this cell" (Bacon Tempest, Android phone 384 px wide, v610, screenshot).
#   The active research row on a narrow phone: the timer, "Get speed-ups", the shard Finish button and the cancel X
#   (.qrow .acts, one line, no wrap) took the whole width of the grid's auto column, so the name column
#   (minmax(0,1fr)) shrank to ~one letter and "RESEARCH / Laser Technology -> Lv. 13" ran down the edge letter by letter.
#   The name column now keeps at least 7.5em and the buttons wrap onto a second line (right-aligned) when they don't fit.
#   Wide screens are unchanged (the buttons still fit on one line there).
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('.qrow{display:grid;grid-template-columns:minmax(0,1fr) auto;',
  '.qrow{display:grid;grid-template-columns:minmax(7.5em,1fr) auto;'),
 ('.qrow .acts{display:flex;gap:6px;align-items:center}',
  '.qrow .acts{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:6px;align-items:center} /* fb-20261118: on narrow phones the buttons wrap instead of crushing the name */'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
