# v641: prices nudged toward Game of War (owner: "Do that"): speed-ups x2, VIP points x2, random teleport ◆70 (aimed stays ◆200)
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
rep('["vipPts100", "100 VIP Points", 8, 0, 100], ["vipPts500", "500 VIP Points", 35, 0, 500], ["vipPts2500", "2,500 VIP Points", 150, 0, 2500], ["vipPts10k", "10,000 VIP Points", 550, 0, 10000]]',
    '["vipPts100", "100 VIP Points", 16, 0, 100], ["vipPts500", "500 VIP Points", 70, 0, 500], ["vipPts2500", "2,500 VIP Points", 300, 0, 2500], ["vipPts10k", "10,000 VIP Points", 1100, 0, 10000]] /* v641 x2 */')
rep('n: "Afterburner Fuel", ic: "🚀", cost: [2, 6, 15][i],', 'n: "Afterburner Fuel", ic: "🚀", cost: [4, 12, 30][i], /* v641 x2 */')
rep('SHOP[`x${q}_${tk}`] = { cat: "accel", tier: i, col, n: nm, ic, cost: [4, 10, 24][i],', 'SHOP[`x${q}_${tk}`] = { cat: "accel", tier: i, col, n: nm, ic, cost: [8, 20, 48][i], /* v641 x2 */')
rep('boost5:   { n: "Boost Pack ×5", ic: "⚡", cost: 8,', 'boost5:   { n: "Boost Pack ×5", ic: "⚡", cost: 16, /* v641 x2 */')
rep('TELEPORT_RAND = 100,', 'TELEPORT_RAND = 70,')
rep('Half the price of an aimed jump (◆${TELEPORT_RAND}, or a ticket); same 24-hour recharge.', 'Cheaper than an aimed jump: ◆${TELEPORT_RAND}, or a ticket. Same 24-hour recharge.')
rep('const GAME_V = 640', 'const GAME_V = 641')
open(p, 'w', encoding='utf-8').write(s)
