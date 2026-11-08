# v336: Select all ships leaves Espionage Probes home during the Academy
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
a = '  pkevery: () => { pick = Object.assign({}, originAvail()); renderSheet(); },'
b = '  pkevery: () => { pick = Object.assign({}, originAvail()); if (tutOn()) delete pick.spyProbe; renderSheet(); }, /* v336: the Academy keeps its probes out of the fight (they need them for scouting) */'
assert t.count(a) == 1; t = t.replace(a, b); open(p, 'w', encoding='utf-8').write(t)
