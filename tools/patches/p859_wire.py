"""v859: the crab bosses' glow cleaned up, and every Carcinid crab and ship given the same treatment (owner: "crab bosses look great but some
of the glow kinda drowns them out can we clean them up and also can we show some of the same love to all the crab ships and waves? give
them a unique feel and make them look awesome"). Models: the nine wave crabs rebuilt with the bosses' builder (crc_boss.py, each its own
tint after its painting), the eleven ships given a glow layer and faint light in their plate cracks (crc_ship.py); the bosses' glow layer,
crack light and heart roughly halved. Material: every crab and ship on the wet crcBossMat, its emission 1.35 -> 1.15. Battle: the water
effects for every crab and ship (lighter than a boss's: a faint halo, three bubbles, drips from crab claws, its blows' charge and spray in
its own colour); the bosses' halo and haze lighter."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 858;", "const GAME_V = 859;")
rep("for (const k of CRC_BK) if (CRC_SC[k]) CRC_SC[k].g = 1;", "for (const k in CRC_SC) CRC_SC[k].g = 1; /* v859 every crab and ship has a glow layer */")
rep("CRC_BK.has(k) ? crcBossMat(k) : cntMeshMat()); /* v855 */", "crcBossMat(k)); /* v855, v859 every crab and ship */")
rep("totalEmissiveRadiance += vEm * 1.35;", "totalEmissiveRadiance += vEm * 1.15;")
rep("totalEmissiveRadiance += vec3(${rgb}) * fr * .3; }", "totalEmissiveRadiance += vec3(${rgb}) * fr * .22; }")
rep("m.customProgramCacheKey = () => \"crcboss1\" + k;", "m.customProgramCacheKey = () => \"crcboss2\" + k;")
rep("const crcBoss = q => q && CRC_BK.has(q.k);", "const crcBoss = q => q && CRC_BK.has(q.k), crcAny = q => q && CRC_SC[q.k]; /* v859 */")
# the ambient water, for every crab and ship
rep("for (let i = 0; i < b.Q.length; i++) { const q = b.Q[i], P = scr[i]; if (!crcBoss(q)) continue; const g = b.geo && b.geo[i], Lg = g ? g.L : 60, col = BOSS_GLOW[q.k] || CRC_WATER,",
    "for (let i = 0; i < b.Q.length; i++) { const q = b.Q[i], P = scr[i]; if (!crcAny(q)) continue; const big = crcBoss(q), crab = CRC_CRABS.includes(q.k), g = b.geo && b.geo[i], Lg = g ? g.L : 60, col = BOSS_GLOW[q.k] || crcRGB(q),")
rep("ctx.globalAlpha = .04 + .035 * br; ctx.drawImage(gs, P.x - Lg * .85", "ctx.globalAlpha = big ? .03 + .025 * br : .018 + .014 * br; ctx.drawImage(gs, P.x - Lg * .85")
rep("ctx.globalAlpha = .06; ctx.drawImage(ws, P.x - Lg * 1.1", "ctx.globalAlpha = big ? .045 : .02; ctx.drawImage(ws, P.x - Lg * 1.1")
rep("for (let j = 0; j < 7; j++) { const ph = T * .28 + j / 7 + i * .31,", "for (let j = 0; j < (big ? 7 : 3); j++) { const ph = T * .28 + j / 7 + i * .31,")
rep("for (let j = 0; j < 4; j++) { const ph = T * .45 + j / 4 + i * .17,", "for (let j = 0; j < (!crab ? 0 : big ? 4 : 2); j++) { const ph = T * .45 + j / 4 + i * .17,")
rep("for (let j = 0; j < 2; j++) { const k = (T / 5 + j * .5 + i * .23) % 1,", "for (let j = 0; j < (big ? 2 : 1); j++) { const k = (T / 5 + j * .5 + i * .23) % 1,")
rep("const e = T - seen[i]; if (e < 3) { /* the entrance", "const e = T - seen[i]; if (big && e < 3) { /* the entrance")
# the attacks, for every crab and ship, in its own colour
rep("for (const m of b.mAtk || []) if (crcBoss(b.Q[m.s])) L.push([m, MIM_DUR[m.a] || 1, 1]);", "for (const m of b.mAtk || []) if (crcAny(b.Q[m.s])) L.push([m, MIM_DUR[m.a] || 1, 1]);")
rep("const q = b.Q[m.s]; if (!crcBoss(q) || !(b.n[m.s] > 0)) continue; const u = (T - m.t0) / D;", "const q = b.Q[m.s]; if (!crcAny(q) || !(b.n[m.s] > 0)) continue; const big = crcBoss(q), wc = big ? CRC_WATER : crcRGB(q), u = (T - m.t0) / D;")
rep("if (u < .3) { const k = u / .3; for (let j = 0; j < 10; j++) { const a = j * .628 + k * 5 + m.seed, rr = Lg * .6 * (1 - k), x = H.x + Math.cos(a) * rr, y = H.y + Math.sin(a) * rr * .55; ctx.globalAlpha = .8 * Math.min(1, k * 3); ctx.fillStyle = `rgba(${CRC_WATER},1)`;",
    "if (u < .3) { const k = u / .3; for (let j = 0; j < (big ? 10 : 5); j++) { const a = j * .628 + k * 5 + m.seed, rr = Lg * .6 * (1 - k), x = H.x + Math.cos(a) * rr, y = H.y + Math.sin(a) * rr * .55; ctx.globalAlpha = .8 * Math.min(1, k * 3); ctx.fillStyle = `rgba(${wc},1)`;")
rep("for (let j = 0; j < 12; j++) { const a = j * .524 + m.seed, dd = Lg * (.15 + .75 * k), x = E0.x + Math.cos(a) * dd, y = E0.y + Math.sin(a) * dd * .55 + k * k * Lg * .25; ctx.globalAlpha = (1 - k) * .9; ctx.fillStyle = `rgba(${CRC_WATER},1)`;",
    "for (let j = 0; j < (big ? 12 : 6); j++) { const a = j * .524 + m.seed, dd = Lg * (.15 + .75 * k), x = E0.x + Math.cos(a) * dd, y = E0.y + Math.sin(a) * dd * .55 + k * k * Lg * .25; ctx.globalAlpha = (1 - k) * (big ? .9 : .7); ctx.fillStyle = `rgba(${wc},1)`;")
rep("&& !CRC_BK.has(b.Q[m.s].k)) mimCharge(", "&& !CRC_SC[b.Q[m.s].k]) mimCharge(")
open(p, "w", encoding="utf-8").write(s); print("ok")
