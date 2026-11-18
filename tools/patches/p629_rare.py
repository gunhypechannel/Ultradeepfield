# v629: runes and shards made very rare (owner: "Lower elements and runes should be very rare").
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const ESH_N = 10, ESH_CAP = 25, ESH_COL = 1,', 'const ESH_N = 10, ESH_CAP = 6, ESH_COL = 1 / 7, ESH_P = { task: .2, mon: .25, pir: .1, pyr: .3, help: .1 }, /* v629 very rare */')
rep("grantShards(x.mon ? 2 : 1, x.mon ? `Slain ${x.name}` : `Raided ${x.name}`, x.mon ? MON_EL[x.mon] : null); /* v628 */", "if (Math.random() < (x.mon ? ESH_P.mon : ESH_P.pir)) grantShards(1, x.mon ? `Slain ${x.name}` : `Raided ${x.name}`, x.mon ? MON_EL[x.mon] : null); /* v629 */")
rep('grantShards(1 + (y.lvl >= 4 ? 1 : 0) + (y.lvl >= 7 ? 1 : 0), y.name); /* v628 */', 'if (Math.random() < ESH_P.pyr) grantShards(y.lvl >= 7 ? 2 : 1, y.name); /* v629 */')
rep('grantShards(2, "Daily task"); /* v628 */', 'if (Math.random() < ESH_P.task) grantShards(1, "Daily task"); /* v629 */')
rep('grantShards(1, "Alliance help", null, { quiet: 1 }); /* v628 */', 'if (Math.random() < ESH_P.help) grantShards(1, "Alliance help"); /* v629 */')
rep('if (BOSS_EL[key]) { grantShards(4, `${D.n} core`, BOSS_EL[key], { nocap: 1, quiet: 1 }); extra += `, 4 ${ELEM[BOSS_EL[key]].n} shards`; }', 'if (BOSS_EL[key]) { grantShards(2, `${D.n} core`, BOSS_EL[key], { nocap: 1, quiet: 1 }); extra += `, 2 ${ELEM[BOSS_EL[key]].n} shards`; }')
rep('if (BOSS_EL[k]) grantShards(4, `${D.n} core`, BOSS_EL[k], { nocap: 1 });', 'if (BOSS_EL[k]) grantShards(2, `${D.n} core`, BOSS_EL[k], { nocap: 1 });')
rep('win = res.winner === "a", n = win ? 8 : 4;', 'win = res.winner === "a", n = win ? 2 : 1;')
rep('Win: ${ESH_N - 2} ${ELEM[te].n} shards, otherwise 4.', 'Win: 2 ${ELEM[te].n} shards, otherwise 1.')
rep('cost: 6, d: () => `Five rune shards', 'cost: 15, d: () => `Two rune shards')
rep('if (eshLeft(e) < 5) return toast', 'if (eshLeft(e) < 2) return toast')
rep('grantShards(5, "Rune Shard Cache", e);', 'grantShards(2, "Rune Shard Cache", e);')
rep('{ k: "rcache", g: "ᛦ", l: "ᛦ", col: "#e06bd8", w: 4 }', '{ k: "rcache", g: "ᛦ", l: "ᛦ", col: "#e06bd8", w: 1 }')
# transmuting costs 5, not 3
rep('Object.keys(ELEM).filter(e => e !== sel && ((S.runes || {})[e] || 0) >= 3)', 'Object.keys(ELEM).filter(e => e !== sel && ((S.runes || {})[e] || 0) >= 5)')
rep('<small>Transmute 3 spare runes into 1 ${d.n} rune:</small>', '<small>Transmute 5 spare runes into 1 ${d.n} rune:</small>')
rep('data-e="${sel}"><i></i>3 ${ELEM[e].n} → 1</button>', 'data-e="${sel}"><i></i>5 ${ELEM[e].n} → 1</button>')
rep('<em>You need 3 spare runes of another element.</em>', '<em>You need 5 spare runes of another element.</em>')
rep('if ((S.runes[f] || 0) < 3) return toast(`You need 3 spare ${ELEM[f].n} runes.`, "warn"); S.runes[f] -= 3; S.runes[e] = (S.runes[e] || 0) + 1; toast(`3 ${ELEM[f].n} runes', 'if ((S.runes[f] || 0) < 5) return toast(`You need 5 spare ${ELEM[f].n} runes.`, "warn"); S.runes[f] -= 5; S.runes[e] = (S.runes[e] || 0) + 1; toast(`5 ${ELEM[f].n} runes')
# the page's wording
rep('<span>🌍 Your worlds · 1 shard a day each</span><span>📋 Daily tasks · 2</span><span>🐙 Monsters · 2</span><span>☠ Pirates · 1</span><span>🛰 Station expeditions · 1–3</span><span>🤝 Alliance help · 1</span><span>${EL_ICON[te]} Daily Trial · 4–8</span><span>ᛦ Glyph Wheel and the Void Shop</span>',
    '<span>🌍 Your worlds · 1 shard a week each</span><span>${EL_ICON[te]} Daily Trial · 1–2</span><span>🐙 Monsters · rare</span><span>📋 Daily tasks · rare</span><span>🛰 Expeditions · rare</span><span>☠ Pirates · very rare</span><span>🤝 Alliance help · very rare</span><span>ᛦ Glyph Wheel and Void Shop · rare</span>')
rep("and everyone who fought gets 4 shards of the boss's element.", "and everyone who fought gets 2 shards of the boss's element.")
rep('Everyday shards are capped at ${ESH_CAP} per element each week (the Trial and bosses don\'t count).', 'Runes are meant to be rare: everyday shards are capped at ${ESH_CAP} per element each week (the Trial and bosses don\'t count).')
# the sound effects volume and switch: since v334 their line sat behind a // comment, so neither did anything
rep("// v334: ducked under the Advisor's voice AU.sfx.gain.setTargetAtTime(AU.sfxOn ? gainOf(AU.sv) * 1.17 : 0, t, .05);", "// v334: ducked under the Advisor's voice\n  AU.sfx.gain.setTargetAtTime(AU.sfxOn ? gainOf(AU.sv) * 1.17 : 0, t, .05); /* v629 */")
s2 = re.sub(r"GAME_V = 628\b", "GAME_V = 629", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
