# v469 the smaller bosses between the great events (owner: "schedule the smaller boss events in between the bigger boss battle events").
# Wednesdays 18:00 UTC: the four great events in turn (Vaelthar, Cube Devastation, Aexion, the Elemental Convergence), each back every 4
# weeks. Saturdays 18:00 UTC, halfway between: the seven world bosses in turn (the Pyramid Overlord with its conduits, the Orbital Devourer,
# the Void Warden, the Brood Matriarch, the Iron Tyrant, the Event Horizon Wyrm, the Shard Colossus), 48 h each, each back every 7 weeks.
# So there is a boss every few days and never two at once. Starts: Vaelthar Wed 2026-11-18, the Overlord Sat 2026-11-21.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('const ROT0 = Date.UTC(2026, 10, 18, 18), ROT = ["vae", "ovl", "dv", "dev", "aex", "war", "conv", "brd", "tyr", "wym", "col"]; /* v467 the Wednesday boss rotation */',
    'const ROT0 = Date.UTC(2026, 10, 18, 18), ROT = ["vae", "dv", "aex", "conv"], ROTS0 = ROT0 + 3 * 864e5, ROTS = ["ovl", "dev", "war", "brd", "tyr", "wym", "col"]; /* v467 the Wednesday great events; v469 the Saturday world bosses between them */')
rep("const rotW = T => Math.floor((T - ROT0) / WEEK), rotKey = w => w < 0 ? null : ROT[w % ROT.length];",
    "const rotW = T => Math.floor((T - ROT0) / WEEK), rotKey = w => w < 0 ? null : ROT[w % ROT.length], rotWs = T => Math.floor((T - ROTS0) / WEEK), rotKeyS = w => w < 0 ? null : ROTS[w % ROTS.length];")
rep("const rotStartOf = (key, T) => { for (let i = 0; i <= ROT.length; i++) { const w = rotW(T) - i; if (w < 0) return null; if (rotKey(w) === key) return ROT0 + w * WEEK; } return null; };",
    "const rotStartOf = (key, T) => { const sm = ROTS.includes(key), L = sm ? ROTS : ROT, B = sm ? ROTS0 : ROT0, W = Math.floor((T - B) / WEEK); for (let i = 0; i <= L.length; i++) { const w = W - i; if (w < 0) return null; if (L[w % L.length] === key) return B + w * WEEK; } return null; };")
rep("const rotNextOf = (key, T) => { for (let w = Math.max(0, rotW(T)); w <= Math.max(0, rotW(T)) + ROT.length + 1; w++) { const s0 = ROT0 + w * WEEK; if (rotKey(w) === key && s0 > T) return s0; } return T + WEEK; };",
    "const rotNextOf = (key, T) => { const sm = ROTS.includes(key), L = sm ? ROTS : ROT, B = sm ? ROTS0 : ROT0, W = Math.max(0, Math.floor((T - B) / WEEK)); for (let w = W; w <= W + L.length + 1; w++) { const s0 = B + w * WEEK; if (L[w % L.length] === key && s0 > T) return s0; } return T + WEEK; };")
rep("{ const s2 = WB2_BASE + c * WEEK; if (s2 >= ROT0) { if (rotKey(rotW(s2)) !== (g === 3 ? \"conv\" : D.con != null ? \"ovl\" : k)) return null; return g === 3 ? (k === \"epx\" ? [s2 + WB_FUSE, s2 + WB_LIVE] : [s2, s2 + WB_FUSE]) : [s2, s2 + WB_LIVE]; } if (g === 1) return null; }",
    "{ const s2 = WB2_BASE + c * WEEK; if (s2 >= ROT0) { if (g === 3) return rotKey(rotW(s2)) !== \"conv\" ? null : k === \"epx\" ? [s2 + WB_FUSE, s2 + WB_LIVE] : [s2, s2 + WB_FUSE]; const sat = s2 + 3 * 864e5; if (rotKeyS(rotWs(sat)) !== (D.con != null ? \"ovl\" : k)) return null; return [sat, sat + WB_LIVE]; } if (g === 1) return null; }")
# the Advisor's hunt news
rep('const c2 = wbCyc2(T), s2 = WB2_BASE + c2 * WEEK, rk = s2 >= ROT0 ? rotKey(rotW(s2)) : null, odd = rk ? rk === "conv" : ((c2 % 2) + 2) % 2 === 1, tit = rk ? ["brd", "tyr", "wym", "col"].includes(rk) : !odd;\n  if (rk && ["ovl", "dev", "war"].includes(rk) && T - s2 < 24 * 3600e3) advNews("wb_new", "wb:" + c2, { act: "find", r: "ev" }, "Hunt the bosses");\n  if (tit && T - s2 < 24 * 3600e3) advNews("wb2_new"',
    'const c2 = wbCyc2(T), s2 = WB2_BASE + c2 * WEEK, rk = s2 >= ROT0 ? rotKey(rotW(s2)) : null, odd = rk ? rk === "conv" : ((c2 % 2) + 2) % 2 === 1, sat = s2 + 3 * 864e5, rs = s2 >= ROT0 ? rotKeyS(rotWs(sat)) : null, satNew = T >= sat && T - sat < 24 * 3600e3, tit = rk ? ["brd", "tyr", "wym", "col"].includes(rs) && satNew : !odd && T - s2 < 24 * 3600e3;\n  if (["ovl", "dev", "war"].includes(rs) && satNew) advNews("wb_new", "wb:" + c2, { act: "find", r: "ev" }, "Hunt the bosses");\n  if (tit) advNews("wb2_new"')
# what the game says
for a, b in [("in the Wednesday boss rotation (one boss a week, 18:00 UTC) for 48 hours, at full strength", "in the Saturday hunts between the great events (one boss each Saturday, 18:00 UTC) for 48 hours, at full strength"),
             ("in the Wednesday boss rotation (one boss a week, 18:00 UTC) for 48 hours, each with a tric", "in the Saturday hunts between the great events (one boss each Saturday, 18:00 UTC) for 48 hours, each with a tric"),
             ("in the Wednesday boss rotation (one boss a week, 18:00 UTC) for 48 hours. Every attack, wi", "in the Saturday hunts between the great events (one boss each Saturday, 18:00 UTC) for 48 hours. Every attack, wi"),
             ("in the Wednesday boss rotation (one boss a week, 18:00 UTC), for 48 hours. For the first 2", "in the Wednesday great-event rotation (every fourth Wednesday, 18:00 UTC), for 48 hours. For the first 2")]:
    rep(a, b)
rep("`in ${ftime(wbNext(key, T) - T)}`} · the Wednesday boss rotation", "`in ${ftime(wbNext(key, T) - T)}`} · ${wbG3(key) ? \"a Wednesday great event\" : \"the Saturday hunts\"}")
rep("${!live ? `In the Wednesday boss rotation · next in", "${!live ? `${g === 3 ? \"A Wednesday great event\" : \"Saturday hunts\"} · next in")
# the Boss Lab: both rotations
rep('const rows = ROT.map((k, i) => { let w = w0; while (rotKey(w) !== k) w++; const at = ROT0 + w * WEEK, [ic, n] = nm(k);',
    'const rows = [...ROT, ...ROTS].map(k => [k, rotNextOf(k, T - 1)]).sort((a, b) => a[1] - b[1]).map(([k, at]) => { const [ic, n] = nm(k);')
rep("<p class=\"note\">The Wednesday boss rotation, one boss a week at 18:00 UTC, each back every ${ROT.length} weeks.", "<p class=\"note\">Wednesdays: the great events in turn (each back every ${ROT.length} weeks). Saturdays between them: the world bosses in turn (each back every ${ROTS.length} weeks). All at 18:00 UTC.")
rep("first: ROT0 + 4 * WEEK", "first: ROT0 + 2 * WEEK")
rep("DV_FIRST = ROT0 + 2 * WEEK /* v467 in the Wednesday rotation */", "DV_FIRST = ROT0 + WEEK /* v469 the second Wednesday of the rotation */")
s = re.sub(r"GAME_V = 468\b", "GAME_V = 469", s)
open(P, 'w').write(s)
