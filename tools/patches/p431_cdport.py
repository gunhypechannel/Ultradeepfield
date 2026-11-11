# v431: (3) economy: costs 1.5x (a Light Fighter 4,500/1,500), job times 1.15x (ECON_K, ECON_T). (1) the Cube Destroyer's beam leaves its red gun port (owner: "line up its gun port as close as possible"). The port was placed
#  at 0.49 of a hull length from the centre, but the art is drawn 3.2 lengths wide round the centre, and the port, measured in the
#  baked art itself (the centroid of its red pixels), sits only ~0.13 out. It also swings round the hull in each of the 12 turn
#  poses (v416), so each pose has its own measured spot, blended exactly as the drawing cross-fades the poses.
#  (2) label/value lists (.kv: a target's loot, teamwork and strength, a probe's flight and charts, ...) no longer squeeze the label
#  into a one-letter column when a value is a long sentence: the label keeps at least min(42%, 9em) and the value wraps.
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)
rep("const CD_PHI0 = -.314;", """/* v431 the red gun port in each baked pose (k = 0..11, 30 degrees apart from the rest aim), in hull lengths from the centre of the
   drawn art (3.2 L x 1.6 L): forward (mirrored with the hull) and down. Measured on the art: the rim of red in the port's direction,
   drawn in a little to the port's middle. */
const CD_PORT = [[.474, .169], [.495, -.116], [.383, -.340], [.123, -.501], [-.116, -.503], [-.359, -.375], [-.490, -.157], [-.497, .106], [-.398, .320], [-.151, .486], [.082, .499], [.344, .377]];
/* the port of the pose actually on screen: a pose not baked yet is drawn as the nearest one that is (cdPose), so the beam follows the picture */
function cdPortDrawn(phi, base) { const u = (phi - CD_PHI0) / (Math.PI / 6), k0 = Math.floor(u), w = u - k0, A = ((k0 % 12) + 12) % 12, B = (A + 1) % 12, got = k => !k || !base || !!shipArtSoon("worldbreaker", base + "~p" + k, "side");
  const a = got(A), bb = got(B), PA = CD_PORT[A], PB = CD_PORT[B]; if (a && bb) return [PA[0] + (PB[0] - PA[0]) * w, PA[1] + (PB[1] - PA[1]) * w]; return a ? PA : bb ? PB : CD_PORT[0]; }
const CD_PHI0 = -.314;""")
rep("if (Math.abs(phi - CD_PHI0) > .01) { const P = cdPose(phi, base); acc3 = P[0]; acc3b = P[1]; w3 = P[2]; } }",
    "if (Math.abs(phi - CD_PHI0) > .01) { const P = cdPose(phi, base); acc3 = P[0]; acc3b = P[1]; w3 = P[2]; } if (!j) (b.cdPt || (b.cdPt = []))[i] = Math.abs(phi - CD_PHI0) > .01 ? cdPortDrawn(phi, base) : CD_PORT[0]; } /* v431 where the lead hull's gun port is on screen */")
rep("m.ox = S0.x + fc * Lg * .491 * Math.cos(ph); m.oy = S0.y - Lg * .491 * Math.sin(ph); /* v416 the dish where the turned station holds it */",
    "const pt = (b.cdPt && b.cdPt[m.s]) || cdPortDrawn(ph, null); m.ox = S0.x + fc * Lg * pt[0]; m.oy = S0.y + Lg * pt[1]; /* v431 from the gun port as it is drawn */")
rep(".kv{display:grid;grid-template-columns:minmax(0,1fr) auto;", ".kv{display:grid;grid-template-columns:minmax(min(42%,9em),auto) minmax(min(40%,10em),1fr);")
rep("const UNI = 8, PRM = UNI / 60;", """/* v431 economy (owner: "balance the game based off Light Fighters costing 4,500 metal and 1,500 crystal", and "slightly slower"):
   every building, research, ship, defence and missile costs 1.5x what it did (a Light Fighter 3,000/1,000 -> 4,500/1,500). Job
   times follow cost, so they are held to 1.15x (ECON_TK in the time formulas) instead of 1.5x. Resource output is unchanged.
   Jobs already queued keep what was paid and their finish time. */
const ECON_K = 1.5, ECON_T = 1.15, ECON_TK = ECON_T / ECON_K; for (const D0 of [B, R, SH, DF, MS]) for (const k in D0) { const c = D0[k] && D0[k].c; if (c) for (const r in c) if (typeof c[r] === "number") c[r] = Math.round(c[r] * ECON_K); }
const UNI = 8, PRM = UNI / 60;""")
rep("* 1.44 / (UNI", "* 1.44 * ECON_TK / (UNI", 3)
rep("* 3.6 * RES_SLOW / (UNI", "* 3.6 * RES_SLOW * ECON_TK / (UNI")
rep("if (!p.sq) p.sq = { k, n, start: now(), each: colShipTime(p, def.c) }; else csList(p).push({ k, n });", "if (!p.sq) p.sq = { k, n, start: now(), each: colShipTime(p, def.c) }; else csList(p).push({ k, n, c: mul(def.c, n) }); /* v431 the price paid, for a fair refund */")
rep("const c = d.s ? mul(SH[it.k].c, it.n) : it.c; settle(p);", "const c = d.s ? (it.c || mul(SH[it.k].c, it.n / ECON_K)) : it.c; settle(p); /* v431 queued before the price rise: refund what was paid */")
t = t.replace("const GAME_V = 430;", "const GAME_V = 431;")
open(p, "w").write(t); print("ok")
