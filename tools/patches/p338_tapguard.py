p='docs/index.html'; t=open(p,encoding='utf-8').read()
a='if (/^(detail|planet|pirate|pyramid|node|spyOpen|repOpen|dmOpen|fleetMap|nav|sub|bcat|rcat|tutShow|shipShow)$/.test(el.dataset.act))'
b='if (/^(detail|planet|planets|pirate|pyramid|node|spyOpen|repOpen|dmOpen|fleetMap|nav|sub|bcat|rcat|tutShow|shipShow|boost|finish|up|make|research)$/.test(el.dataset.act)) /* v338: and taps that reshuffle the queue rows (a −5m tap re-rendered the row and the next tap opened the planet list) */'
assert t.count(a)==1; t=t.replace(a,b); open(p,'w',encoding='utf-8').write(t)
