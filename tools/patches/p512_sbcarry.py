# v512 every attack on a super boss counts (owner): a section is only destroyed when the fight breaks a whole one, so a smaller
# fleet used to do nothing at all. Now the damage a fight deals to the boss's hull that falls short of a whole section is kept
# (per commander, per boss, per appearance) and carried into the next attack: once it adds up to a section, that attack breaks an
# extra one. The report shows it; the server's fight check compares the simulator's own result (before the carried damage).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const rep0 = {}; let seg = Math.min(cap, n0 - clamp(Math.round(((res.dLeft || {})[D.u]) || 0), 0, n0)); const xf0 = aexXf(cur);',
    'const rep0 = {}, simLeft = clamp(Math.round(((res.dLeft || {})[D.u]) || 0), 0, n0); let seg = Math.min(cap, n0 - simLeft); const xf0 = aexXf(cur); const carry = sbCarryAdd(k, s0, res, D.u, seg, Math.max(0, Math.min(cap, n0) - seg)); seg += carry; rep0.carry = carry; if (carry) note(`The damage from our earlier attacks added up: ${carry} more section${carry > 1 ? "s" : ""} of ${D.n} broke.`, "win");')
rep('const rep = mkRep({ at, kind: "attack", title: `Assault on ${D.n}${tgt !== "core" ? ` · ${tname}` : ""}`,', 'const rep = mkRep({ at, kind: "attack", simLeft, sbCarry: rep0.carry || undefined, title: `Assault on ${D.n}${tgt !== "core" ? ` · ${tname}` : ""}`,')
rep('G.db.fn("settle_fight", { kind: rep.omega ? "om" : rep.sbk ? "sb" : "wb", unit, n0: sg[0], left: sg[1],', 'G.db.fn("settle_fight", { kind: rep.omega ? "om" : rep.sbk ? "sb" : "wb", unit, n0: sg[0], left: rep.simLeft != null ? rep.simLeft : sg[1], /* v512 the simulator\'s own result, before carried damage */')
rep('async function sbResolve(f) {', r'''/* v512 the damage a fight deals short of a whole section, kept for the next attack on the same boss in the same appearance */
function sbCarryAdd(k, s0, res, u, seg, room) { try { const st = (((res.sim || {}).stats || {}).d || {})[u], hull = (AL[u] || {}).hull; if (!st || !hull) return 0; const prog = Math.max(0, st.taken / hull - seg);
    S.sbCarry = S.sbCarry || {}; let c = S.sbCarry[k]; if (!c || c.s0 !== s0) c = S.sbCarry[k] = { s0, v: 0 }; c.v += prog; const add = Math.min(room, Math.floor(c.v)); c.v -= add; if (room <= 0) c.v = Math.min(c.v, .999); dirty(); return add; } catch (e) { return 0; } }
async function sbResolve(f) {''')
# with every attack counting, the super bosses take the 2x hull planned in v510 (owner's fleet: ~2.5 sections an attack, about what it did before at 1x without the carry; 1.5x gave ~6, easier than before) (without the carry it left the owner's fleet doing nothing)
rep('const BOSS_HARD = { hull: 1, atk: 1.5 };', 'const BOSS_HARD = { hull: 2, atk: 1.5 };')
# the owner approved the Archives' Empire Origins links (Imhotep's era for the Walking Temple, Hypatia's star catalogues for the Wyrm)
rep('Proposed lore: nothing here overrides Empire Origins canon until the owner approves it.', 'The owner approved these links as canon for both games (2026-11-12).')
# the rules say so
rep('<p class="note">${esc(D.t)} · ${D.diff} super boss', '<p class="note sbfree">No ship is lost for good: every ship it destroys comes home damaged to your Repair Yard. Every attack counts, even a small one: damage short of a whole section carries over to your next attack.</p><p class="note">${esc(D.t)} · ${D.diff} super boss')
rep("const rules = g === 3 ? `The Elemental Convergence comes", "const rules = g === 3 ? `No ship is lost for good in the Convergence: every ship it destroys comes home damaged to your Repair Yard. The Elemental Convergence comes")
s2 = re.sub(r"GAME_V = 511\b", "GAME_V = 512", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
