# v682: every boss attack crosses the screen — the Super Cube's tractor/burst/wave, the world bosses' bite/coil/charge/summon,
# and the Omega Cube's model now plays the move its battle shows (it still picked random moves after v681)
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('function wbStrike(ctx, b, scr, Q, W, H, t, d, lo) { const k = b.r && (b.r.wb || (b.r.sbk && WB_STRIKE[b.r.sbk] ? b.r.sbk : null)) /* v681 super bosses too */, M = WBR.mv;',
    'const wbCol = k => (WB[k] || (typeof SBW !== "undefined" && SBW[k]) || { col: "#5dff7a" }).col; /* v682 */\nfunction wbStrike(ctx, b, scr, Q, W, H, t, d, lo) { const k = b.r && (b.r.wb || (b.r.sbk && WB_STRIKE[b.r.sbk] ? b.r.sbk : null) || (!b.r.omega && b.superSide && !b.r.sbk ? "scb" : null)) /* v681 super bosses, v682 the Super Cube */, M = WBR.mv;')
rep('PB = !!WB[k] /* v493', 'PB = !!(WB[k] || SBW[k] || k === "scb") /* v682 super bosses and the Super Cube too; v493')
rep('glowSprite(PB && k !== "wym" ? WB[k].col : "rgba(255,170,60,1)")', 'glowSprite(PB && k !== "wym" ? wbCol(k) : "rgba(255,170,60,1)")')
rep(': [(WB[k] || SBW[k]).col], col = j => els[j % els.length];', ': [wbCol(k)], col = j => els[j % els.length];')
rep('  epx: { converge: ["beam", .5, .95, 0, 3400], storm: ["bolts", .2, .9, 12, 3000], cataclysm: ["wave", .45, .95, 0, 3200] } };',
    '''  epx: { converge: ["beam", .5, .95, 0, 3400], storm: ["bolts", .2, .9, 12, 3000], cataclysm: ["wave", .45, .95, 0, 3200] },
  scb: { tractor: ["beam", .3, .85, 0, 3000], burst: ["bolts", .3, .85, 8, 2600], wave: ["wave", .35, .9, 0, 2600] } }; /* v682 the Super Cube */
Object.assign(WB_STRIKE.ovl, { summon: ["bolts", .4, .9, 6, 3000] }); Object.assign(WB_STRIKE.war, { summon: ["bolts", .4, .9, 6, 3000] }); Object.assign(WB_STRIKE.c0, { charge: ["beam", .3, .85, 0, 2600] });
Object.assign(WB_STRIKE.dev, { bite: ["bolts", .35, .7, 3, 2000] }); Object.assign(WB_STRIKE.krk, { bite: ["bolts", .35, .7, 3, 2000] }); Object.assign(WB_STRIKE.wym, { coil: ["wave", .35, .85, 0, 2600] }); Object.assign(WB_STRIKE.lev, { coil: ["wave", .35, .85, 0, 2600] }); /* v682 the moves that still stayed in the box */''')
# the Omega Cube's model follows its battle
rep('const BMV_ACT = { aex:', 'const BMV_ACT = { omg: { tractor: "tractor", wave: "wave", split: "burst" }, aex:')
rep('function bossAct(b, a, t) { try { const k = b.r && b.r.sbk,', 'function bossAct(b, a, t) { try { const k = bmvKey(b) || (b.r && b.r.sbk),')
rep('if (!(battle && battle.r && battle.r.sbk === key && BMV_ACT[key]))', 'if (!(battle && battle.r && (battle.r.sbk === key || bmvKey(battle) === key) && BMV_ACT[key]))')
rep('const GAME_V = 681;', 'const GAME_V = 682;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
