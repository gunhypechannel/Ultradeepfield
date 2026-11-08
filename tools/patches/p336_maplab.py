# v336: "Choose this one" on a send button said nothing about what it does
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep('''const mapPath = (final, pick) => () => slotWait() || [fromPick(), ['.sheet [data-act="launch"]', "Send your fleet"], [final, "Choose this one"],''',
'''const mapPath = (final, pick, lab) => () => slotWait() || [fromPick(), ['.sheet [data-act="launch"]', "Send your fleet"], [final, lab || "Tap to send your ships"],''')
rep('''mapPath('.sheet [data-act="raid"]', '.sheet .tgt[data-act="pirate"], .sheet [data-act="pirate"]')();''', '''mapPath('.sheet [data-act="raid"]', '.sheet .tgt[data-act="pirate"], .sheet [data-act="pirate"]', "Tap Raid to attack the pirates")();''')
rep('''mapPath('.sheet [data-act="gather"], .sheet [data-act="launch"]', '.sheet [data-act="node"]')()''', '''mapPath('.sheet [data-act="gather"], .sheet [data-act="launch"]', '.sheet [data-act="node"]', "Tap Send to Gather")()''')
rep('''mapPath('.sheet [data-act="pyrGo"]', '.sheet [data-act="pyramid"]')()''', '''mapPath('.sheet [data-act="pyrGo"]', '.sheet [data-act="pyramid"]', "Tap Explore to send your ships")()''')
open(p, 'w', encoding='utf-8').write(t); print('ok')
