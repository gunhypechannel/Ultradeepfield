# v673 Mimics sized like monsters in battle; swarms as packs; big bosses rise in with their name; coverage hook for the test harness.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
R = lambda f: open('tools/patches/' + f, encoding='utf-8').read()
# definitions right after the size ladder
rep('const SIDE_LEN = { armageddon: 2.2,', R('p673_scale.js') + 'const SIDE_LEN = { armageddon: 2.2,')
rep('const bLen = k => TITAN_LEN[k] ? TITAN_LEN[k] :', 'const bLen = k => MIM_HULL[k] ? MIM_HULL[k] /* v673 */ : /^e_/.test(k) && k.length > 2 ? bLen(k.slice(2)) : TITAN_LEN[k] ? TITAN_LEN[k] :')
rep('L = Math.max(8 * d, clamp(W * .1 * bLen(q.k), 11 * d, W * (BOSSK[q.k] || q.k === "worldbreaker" ? .55 : .3)) * zs * bVsK(b, q))', 'L = bFitL(q.k, Math.max(8 * d, clamp(W * .1 * bLen(q.k), 11 * d, W * bCapW(q.k)) * zs * bVsK(b, q)), W)', 2)
rep('W * (BOSSK[qk.k] || qk.k === "worldbreaker" ? .55 : .3)', 'W * bCapW(qk.k)')
rep('Math.min(3, Math.max(1, visN(q.role, n)))', 'bVc(q, n, 3)')
rep('Math.min(3, Math.max(1, visN(q.role, Math.max(n, 1))))', 'bVc(q, Math.max(n, 1), 3)')
rep('const cx = scr[i].x, cy = scr[i].y, zs = scr[i].s, col = SIDE_COL[q.side];', 'const cx = scr[i].x, cy = scr[i].y, zs = scr[i].s * bRise(b, q) /* v673 */, col = SIDE_COL[q.side];')
rep('intro: reduced ? 0 : 1200,', 'intro: reduced ? 0 : bIntroMs(R.squads), intro0: reduced ? 0 : bIntroMs(R.squads), heroN: bHeroName(R.squads),')
rep('ctx.fillText(intro ? "COMBAT START" : `ROUND ${rnd_}`', 'ctx.fillText(intro ? (b.heroN || "COMBAT START") : `ROUND ${rnd_}`')
# keep the last layout for the coverage test (a reference, no copy)
rep(', P = reps.map(i => { const [rx, ry, w] = fpOf(i);', ', P = b.lastP = reps.map(i => { const [rx, ry, w] = fpOf(i);')
# the Cube Destroyer is locked to its post from the first frame: it used to glide in from its raw simulation spot (55-100 px) and drift as the opening zoom settled
rep('for (const p of P) { const L0 = lay[p.i]; L0.x += (p.x - scr[p.i].x - L0.x) * ease; L0.y += (p.y - scr[p.i].y - L0.y) * ease;', 'for (const p of P) { const L0 = lay[p.i], ez = Q[p.i].k === "worldbreaker" && !b.superSide ? 1 : ease; /* v673 */ L0.x += (p.x - scr[p.i].x - L0.x) * ez; L0.y += (p.y - scr[p.i].y - L0.y) * ez;')
# combat v7: the Cube Destroyer's beam lances reach the whole field (siege range). In v6 it crawled forward from the rear at speed 1.2 and
# first came within its 48 range about 17 s into the fight (round 4 of 8), so most replays showed it silent. Movement is unchanged.
rep('V6 = (o.v || CB_V) >= 6;', 'V6 = (o.v || CB_V) >= 6, V7 = (o.v || CB_V) >= 7, rngOf = s => V7 && s.k === "worldbreaker" ? 160 : WPN[s.wp].rng;')
rep('reach = 1 / (1 + Math.max(0, d - W.rng) / (dc === "skirmish" ? 10 : 22))', 'reach = 1 / (1 + Math.max(0, d - rngOf(s)) / (dc === "skirmish" ? 10 : 22))')
rep('if (s.cd <= 0 && s.tg && active(s.tg) && W.rng > 0 && dist(s, s.tg) <= W.rng + (s.role', 'if (s.cd <= 0 && s.tg && active(s.tg) && W.rng > 0 && dist(s, s.tg) <= rngOf(s) + (s.role')
rep('const CB_V = 6', 'const CB_V = 7')
rep('const sim = { v: V6 ? 6 : V5 ? 5', 'const sim = { v: V7 ? 7 : V6 ? 6 : V5 ? 5')
rep('CB_OK = v => v === 3 || v === 4 || v === 5 || v === 6,', 'CB_OK = v => v === 3 || v === 4 || v === 5 || v === 6 || v === 7, /* v673 v7: the Cube Destroyer fires from the rear (siege range) */')
# merged Cube Destroyer formations (several groups drawn as one ship): each group's beam leaves the drawn ship's gun port, and its aim turns the drawn ship
rep('Q.forEach((q, i) => { if (tot[i] === -1 && rep[i] != null) scr[i] = scr[rep[i]]; }); }', 'Q.forEach((q, i) => { if (tot[i] === -1 && rep[i] != null) scr[i] = scr[rep[i]]; }); b.repOf = rep; /* v673 */ }')
rep('const S0 = scr[m.s], E0 = scr[m.e], g = b.geo && b.geo[m.s], ok = g && g.f === b.gf;', 'const ms = b.repOf && b.repOf[m.s] != null ? b.repOf[m.s] : m.s /* v673 */, S0 = scr[m.s], E0 = scr[m.e], g = b.geo && b.geo[ms], ok = g && g.f === b.gf;')
rep('fc = ok ? g.face : (b.face[m.s] || 1); const ph = (b.cdPhi || {})[m.s] == null ? CD_PHI0 : b.cdPhi[m.s]; const pt = (b.cdPt && b.cdPt[m.s]) || cdPortDrawn(ph, null);', 'fc = ok ? g.face : (b.face[ms] || 1); const ph = (b.cdPhi || {})[ms] == null ? CD_PHI0 : b.cdPhi[ms]; const pt = (b.cdPt && b.cdPt[ms]) || cdPortDrawn(ph, null);')
rep('m = (b.beams || []).find(m => m.wb && m.s === i &&', 'm = (b.beams || []).find(m => m.wb && (m.s === i || (b.repOf && b.repOf[m.s] === i)) &&')
# Archive: play, stop, play again said nothing. advHolo drops any line said in the last 2 minutes (no nagging), and that rule silently
# swallowed every line of a replayed record. A record the player asks to hear (force "arch") always plays, in the hologram style as before.
rep('try { advHolo(l, 1); } catch (e) {}', 'try { advHolo(l, "arch"); } catch (e) {}')
rep('if (!advFresh(line) && !(G.holoNext && G.holoNext.line === line)) return;', 'if (force !== "arch" && !advFresh(line) && !(G.holoNext && G.holoNext.line === line)) return;')
rep('w.classList.toggle("color", force !== 1 && advColor());', 'w.classList.toggle("color", force !== 1 && force !== "arch" && advColor());')
# ...and the record never started while the Advisor was mid-chatter (greetings, omens, hive news): archSeq waited up to a minute for her
# hologram to clear. Now play cuts her off and reads at once, and her other lines hold off while a record is being read.
rep('G.archRd = d.id; const L = [archFragLine(E)]', 'G.archRd = d.id; try { voiceStop(); } catch (e) {} G.holoNext = null; /* v673 */ const L = [archFragLine(E)]')
rep('if (tries++ < 120 && ((a && !a.paused && !a.ended) || (G.sbQ && G.sbQ.length) || ($("#advh.on") && G.holoCur !== L[i - 1])))', 'if (i > 0 && tries++ < 120 && ((a && !a.paused && !a.ended) || (G.sbQ && G.sbQ.length) || ($("#advh.on") && G.holoCur !== L[i - 1])))')
rep('function advHolo(line, force) { if (!line || G.cineOn || (sheet && sheet.type === "depot")) return;', 'function advHolo(line, force) { if (!line || G.cineOn || (sheet && sheet.type === "depot")) return; if (G.archRd && force !== "arch") return; /* v673 a record is being read */')
rep('Lr = (q.role === "station" ? W * .24 : W * .12) * clamp(zs, .6, 1.25);', 'Lr = (MIM_STA[q.k] ? W * MIM_STA[q.k] : q.role === "station" ? W * .24 : W * .12) * clamp(zs, .6, 1.25);')
rep('if (q.role === "station") return [W * .21 * zs, W * .1 * zs, .15];', 'if (q.role === "station") { const m = MIM_STA[q.k] ? MIM_STA[q.k] / .24 : 1; return [W * .21 * zs * m, W * .1 * zs * m * (q.k === "mpylon" || q.k === "mnode" ? 1.6 : 1), .15]; }')
rep('const GAME_V = 672;', 'const GAME_V = 673;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
