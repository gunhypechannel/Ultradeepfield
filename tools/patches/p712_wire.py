# v712 (owner): "Allow players to warp planet 3 times in 24 hours". Each planet's jump drive now holds 3 jumps in any 24 hours (it was one
# jump, then a 24-hour cooldown). S.tpLog[planet] keeps the times of its jumps; once 3 fall inside 24 hours the drive is ready again when
# the oldest of them is 24 hours old. A cooldown left over from before (S.tpCd) counts as one of the three.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const TELEPORT_SHARDS = 200, TELEPORT_RAND = 70, TELEPORT_CD = 24 * 3600e3', '''const TELEPORT_SHARDS = 200, TELEPORT_RAND = 70, TELEPORT_CD = 24 * 3600e3, TELEPORT_MAX = 3; /* v712 three jumps per planet in any 24 hours */
function tpLogOf(id, T = now()) { const L = (((S && S.tpLog) || {})[id] || []).filter(t => T - t < TELEPORT_CD); const c = ((S && S.tpCd) || {})[id] || 0; if (c > T && !L.length) L.push(c - TELEPORT_CD); return L; }
const tpReadyAt = (id, T = now()) => { const L = tpLogOf(id, T); return L.length < TELEPORT_MAX ? 0 : Math.min(...L) + TELEPORT_CD; }, tpLeft = (id, T = now()) => Math.max(0, TELEPORT_MAX - tpLogOf(id, T).length);
const tpLeftTxt = (id, T) => { const n = tpLeft(id, T); return n < TELEPORT_MAX && n > 0 ? ` · ${n} of ${TELEPORT_MAX} jumps left` : ""; }''')
rep('(S.tpCd || {})[p.id] || 0', 'tpReadyAt(p.id, T)', 5)
rep('S.tpCd = S.tpCd || {}; S.tpCd[p.id] = T + TELEPORT_CD;', 'S.tpLog = S.tpLog || {}; S.tpLog[p.id] = tpLogOf(p.id, T).concat(T); if (S.tpCd) delete S.tpCd[p.id];')
rep("toast(`${p.name}'s jump drives are still cooling down.`, \"warn\")", "toast(`${p.name} has used all ${TELEPORT_MAX} of its jumps for now. Its drive recharges in ${ftime(tpReadyAt(p.id, T) - T)}.`, \"warn\")")
rep("Each planet's jump drive recharges for 24 hours.</p>", "Each planet's jump drive holds 3 jumps in any 24 hours.</p>")
rep('<dt>Cooldown</dt><dd>24 hours per planet</dd>', '<dt>Jumps</dt><dd>3 per planet in any 24 hours</dd>')
rep('<small>${zoneOf(p.r)} → ${zoneOf(e.r)}</small>', '<small>${zoneOf(p.r)} → ${zoneOf(e.r)}${tpLeftTxt(p.id, T)}</small>')
rep('<small>[${coordStr(p)}] → [${coordStr(loc)}]</small>', '<small>[${coordStr(p)}] → [${coordStr(loc)}]${tpLeftTxt(p.id, T)}</small>')
rep('<small>[${coordStr(p)}] → somewhere new</small>', '<small>[${coordStr(p)}] → somewhere new${tpLeftTxt(p.id, T)}</small>')
rep('tpCd: {}, fog: ""', 'tpCd: {}, tpLog: {}, fog: ""')
rep('const GAME_V = 711;', 'const GAME_V = 712;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
