# v467 every boss on one weekly Wednesday rotation (owner: "all bosses will be on a weekly Wednesday rotation"; every boss, from Wed 2026-11-18).
# One boss event a week, Wednesdays 18:00 UTC (11:00 Phoenix): Vaelthar, the Pyramid Overlord, Cube Devastation, the Orbital Devourer, Aexion,
# the Void Warden, the Elemental Convergence, the Brood Matriarch, the Iron Tyrant, the Event Horizon Wyrm, the Shard Colossus, then round
# again (each returns every 11 weeks). The Convergence hunt that began on Wed 2026-11-11 runs to its end under the old schedule; nothing else
# from the old Monday / monthly calendars runs before the rotation starts.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep("const EV_BASE = Date.UTC(2026, 0, 2, 18), WEEK = 7 * 864e5, EV_DUR = 48 * 3600e3;",
    """const EV_BASE = Date.UTC(2026, 0, 2, 18), WEEK = 7 * 864e5, EV_DUR = 48 * 3600e3;
const ROT0 = Date.UTC(2026, 10, 18, 18), ROT = ["vae", "ovl", "dv", "dev", "aex", "war", "conv", "brd", "tyr", "wym", "col"]; /* v467 the Wednesday boss rotation */
const rotW = T => Math.floor((T - ROT0) / WEEK), rotKey = w => w < 0 ? null : ROT[w % ROT.length];
const rotStartOf = (key, T) => { for (let i = 0; i <= ROT.length; i++) { const w = rotW(T) - i; if (w < 0) return null; if (rotKey(w) === key) return ROT0 + w * WEEK; } return null; };
const rotNextOf = (key, T) => { for (let w = Math.max(0, rotW(T)); w <= Math.max(0, rotW(T)) + ROT.length + 1; w++) { const s0 = ROT0 + w * WEEK; if (rotKey(w) === key && s0 > T) return s0; } return T + WEEK; };""")
# world bosses: all on the Wednesday cycle; from the rotation on, only in their week
rep("wbG2 = k => !!(WB[k] && WB[k].g >= 2),", "wbG2 = k => !!WB[k],")
rep("function wbWin(k, c) { const D = WB[k]; if (!D) return null; const g = D.g || 1;",
    "function wbWin(k, c) { const D = WB[k]; if (!D) return null; const g = D.g || 1; { const s2 = WB2_BASE + c * WEEK; if (s2 >= ROT0) { if (rotKey(rotW(s2)) !== (g === 3 ? \"conv\" : D.con != null ? \"ovl\" : k)) return null; return g === 3 ? (k === \"epx\" ? [s2 + WB_FUSE, s2 + WB_LIVE] : [s2, s2 + WB_FUSE]) : [s2, s2 + WB_LIVE]; } if (g === 1) return null; }")
rep("const wbNext = (k, T = now()) => { const c = wbCycOf(k, T); for (let i = 0; i < 4; i++)", "const wbNext = (k, T = now()) => { const c = wbCycOf(k, T); for (let i = 0; i < 14; i++)")
# super bosses
rep("first: Date.UTC(2026, 10, 25, 18)", "first: ROT0")
rep("first: Date.UTC(2026, 11, 5, 18)", "first: ROT0 + 4 * WEEK")
rep("function sbStartOf(k, T) { const D = SBW[k]; if (T < D.first) return null; const d = new Date(T); let s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), D.day, 18); if (s > T) s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth() - 1, D.day, 18); return Math.max(s, D.first); }",
    "function sbStartOf(k, T) { return rotStartOf(k, T); }")
rep("function sbNext(k, T) { const D = SBW[k]; if (T < D.first) return D.first; const d = new Date(T); let s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), D.day, 18); if (s <= T) s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, D.day, 18); return s; }",
    "function sbNext(k, T) { return rotNextOf(k, T); }")
# Cube Devastation
rep("DV_FIRST = Date.UTC(2026, 10, 15, 18) /* v442 every 15th */", "DV_FIRST = ROT0 + 2 * WEEK /* v467 in the Wednesday rotation */")
rep("function dvStartOf(T) { const d = new Date(T); let s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), 15, 18); if (T < s) s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth() - 1, 15, 18); return s; }",
    "function dvStartOf(T) { const s0 = rotStartOf(\"dv\", T); return s0 == null ? ROT0 - 400 * WEEK : s0; }")
rep("function dvNext(T) { let s = Math.max(DV_FIRST, dvStartOf(T)); if (T >= s) { const d = new Date(s); s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, 15, 18); } return s; }",
    "function dvNext(T) { return rotNextOf(\"dv\", T); }")
# what the game says about when they come
rep("It forms on the 15th of every month at", "It comes in the Wednesday boss rotation, next at")
rep("The Omega Cube, on the 15th of every month,", "The Omega Cube, in the Wednesday boss rotation,")
rep('It returns every ${wbG2(key) ? "Wednesday" : "Monday"} at 18:00 UTC for 48 hours, at full strength, in a new place.', "It returns in the Wednesday boss rotation (one boss a week, 18:00 UTC) for 48 hours, at full strength, in a new place.")
rep('`${wbG2(key) ? "Wednesdays" : "Mondays"} 18:00 UTC`} · ${wbG3(key) ? "the Convergence: every other Wednesday" : "hunts last 48 h"}', '`in ${ftime(wbNext(key, T) - T)}`} · the Wednesday boss rotation')
rep("The Pyramid Overlord, the Orbital Devourer and the Void Warden return every Monday at 18:00 UTC for 48 hours.", "The Pyramid Overlord, the Orbital Devourer and the Void Warden each come in the Wednesday boss rotation (one boss a week, 18:00 UTC) for 48 hours.")
rep("return every other Wednesday at 18:00 UTC for 48 hours (the Elemental Convergence takes the weeks between)", "each come in the Wednesday boss rotation (one boss a week, 18:00 UTC) for 48 hours")
rep("The Elemental Convergence comes every other Wednesday at 18:00 UTC, for 48 hours.", "The Elemental Convergence comes in the Wednesday boss rotation (one boss a week, 18:00 UTC), for 48 hours.")
# the Advisor's news follows the rotation
rep('const c = wbCyc(T); if (T - (WB_BASE + c * WEEK) < 24 * 3600e3) advNews("wb_new", "wb:" + c, { act: "find", r: "ev" }, "Hunt the bosses");\n  const c2 = wbCyc2(T), s2 = WB2_BASE + c2 * WEEK, odd = ((c2 % 2) + 2) % 2 === 1;\n  if (!odd && T - s2 < 24 * 3600e3) advNews("wb2_new"',
    'const c2 = wbCyc2(T), s2 = WB2_BASE + c2 * WEEK, rk = s2 >= ROT0 ? rotKey(rotW(s2)) : null, odd = rk ? rk === "conv" : ((c2 % 2) + 2) % 2 === 1, tit = rk ? ["brd", "tyr", "wym", "col"].includes(rk) : !odd;\n  if (rk && ["ovl", "dev", "war"].includes(rk) && T - s2 < 24 * 3600e3) advNews("wb_new", "wb:" + c2, { act: "find", r: "ev" }, "Hunt the bosses");\n  if (tit && T - s2 < 24 * 3600e3) advNews("wb2_new"')
rep("${!live ? `Every ${E.day} 18:00 UTC, for 48 hours`", "${!live ? `In the Wednesday boss rotation · next in ${ftime(wbGroupNext(g, T) - T)}`")
s = re.sub(r"GAME_V = 466\b", "GAME_V = 467", s)
open(P, 'w').write(s)
