# v337: two lines of code had ended up inside // comments (v332, v334): the hologram never spoke or placed itself, and an expired
# espionage report crashed instead of saying it expired
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep('// she materializes each time; the Academy card steps aside while she talks advHoloPlace(); clearTimeout(G.advhT); speak(line);',
    '/* she materializes each time; the Academy card steps aside while she talks */ advHoloPlace(); clearTimeout(G.advhT); speak(line);')
rep('''// v332: each report counts once (v301: the Academy's "read the report" steps) if (!r) return''',
    '''/* v332: each report counts once (v301: the Academy's "read the report" steps) */ if (!r) return''')
open(p, 'w', encoding='utf-8').write(t); print('ok')
