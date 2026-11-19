# v670 owner-approved lore: Ten Seals Chapter 5 becomes "The Vault Seal" (the Mimic finale), and six Mimic Protocol Archive records.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
R = lambda f: open('tools/patches/' + f, encoding='utf-8').read()
# Chapter 5: the Kraken's slot, now the Vault Seal, held when Omega dies in the Season of the Mimic
i = s.index('"krk": {"ch": 5, "typ": "wb"'); j = s.index('"lev"', i) if False else None
k0 = s.index('"krk": {', i); depth = 0; k = k0 + len('"krk": ')
while True:
    ch = s[k]
    if ch == '{': depth += 1
    elif ch == '}':
        depth -= 1
        if depth == 0: break
    k += 1
s = s[:k0] + '"krk": {"ch": 5, "typ": "mim", "n": "Omega Awakens", "chap": "The Vault Seal", "ic": "\\u2b22", "col": "#5fd8ff", "set": 0, "d": "Beneath the Cube network lies a prison older than the Wardens: the vault that holds Omega. When the fifth seal weakens, the swarm wakes."}' + s[k + 1:]
rep('if (D.typ === "eclipse") { const sun =', 'if (D.typ === "mim") { const s0 = VP_BASE + (PRO + D.ch - 1 + 10 * n) * VP_LEN + MO_D0; return [s0, s0, s0 + (MO_D1 - MO_D0)]; } /* v670 the Vault Seal: the Mimic finale weekend */ if (D.typ === "eclipse") { const sun =')
rep('    else if (D.typ === "dv") { const st = omState(s0); held = st && st.cyc === s0 && st.hp <= 0; }', '    else if (D.typ === "dv") { const st = omState(s0); held = st && st.cyc === s0 && st.hp <= 0; }\n    else if (D.typ === "mim") { const o = (mimRaw() || {}).o; held = !!(o && o.s === s0 && o.dead); } /* v670 */')
rep('const finKeys = () => Object.keys(FIN_EV).filter(k => k !== "krk" && FIN_EV[k].typ !== "omen"', 'const finKeys = () => Object.keys(FIN_EV).filter(k => FIN_EV[k].typ !== "omen"')
# her Kraken lines go quiet; the chapter's record is rewritten
rep('const FIN_SAY = {', 'const FIN_SAY_KRK_RETIRED = 1; /* v670 */\nconst FIN_SAY = {')
i = s.index('const FIN_SAY = {'); j = s.index('\n', i); line = s[i:j]
a = line.index('"krk": {'); b = a + len('"krk": '); depth = 0
while True:
    ch = line[b]
    if ch == '{': depth += 1
    elif ch == '}':
        depth -= 1
        if depth == 0: break
    b += 1
line = line[:a] + '"krk": {}' + line[b + 1:]; s = s[:i] + line + s[j:]
c5a = s.index('"c_5": {'); c5b = s.index('}', s.index('"def": [', c5a)) + 1
s = s[:c5a] + '"c_5": {"cat": "saga", "t": "Chapter 5: The Vault Seal", "era": "Season 7 finale", "civ": "The Seal Ledger", "loc": "Beneath the Cube network", "img": "art/mimic/nexus.webp", "th": "The Ten Seals", "frag": "Beneath the Cube network lies a prison older than the Wardens: the vault that holds Omega.", "interp": "When the fifth seal weakens, the swarm wakes.", "adv": "The fifth seal was never a Warden. It was a lock.", "enc": ["Chapter five has opened, Commander.", "The vault beneath the Cube network is weakening."], "def": ["The fifth chapter is closed.", "Omega is gone. But not all of it."]}' + s[c5b:]
# the records, their pictures and their names
i = s.index('ARCH_ORD.splice(ARCH_ORD.indexOf("l_judge") + 1, 0,'); j = s.index('\n', i)
s = s[:j + 1] + R('p670_lore.js') + s[j + 1:]
rep('function archImg(E, lv, k) { if (/^[ahdx]_/.test(k) && E.img)', 'function archImg(E, lv, k) { if (/^[ahdxm]_/.test(k) && E.img)')
rep("if (k !== \"testament\" && !/^[bslecoahdx]_/.test(k) && Object.entries(S.arch).filter(([q, v]) => v >= 2 && !/^[bslecoahdx]_/.test(q))", "if (k !== \"testament\" && !/^[bslecoahdxm]_/.test(k) && Object.entries(S.arch).filter(([q, v]) => v >= 2 && !/^[bslecoahdxm]_/.test(q))")
rep('const archName = k => /^a_/.test(k) ? "The Age of Ashes" :', 'const archName = k => /^m_/.test(k) ? "The Mimic Protocol" : /^a_/.test(k) ? "The Age of Ashes" :')
# when they unlock
rep('  M.pts += L.pts; M.kills[st] = (M.kills[st] || 0) + 1;', '  try { archUnlock("m_protocol", 1, true); setTimeout(() => archUnlock("m_protocol", 2), 3000); } catch (e) {} /* v670 */\n  M.pts += L.pts; M.kills[st] = (M.kills[st] || 0) + 1;')
rep('  note(`The Assimilators absorbed the wrecks of our ${SH[best].n}s.', '  try { archUnlock("m_echo", 1); } catch (e) {} /* v670 */\n  note(`The Assimilators absorbed the wrecks of our ${SH[best].n}s.')
rep('M.m.alloy = (M.m.alloy || 0) + 2 * n; M.echo = null; rep.echoWipe = n;', 'M.m.alloy = (M.m.alloy || 0) + 2 * n; M.echo = null; rep.echoWipe = n; try { archUnlock("m_echo", 2, true); } catch (e) {}')
rep('    addReport(rep); try { mapClash(fleetTarget(f), rep); } catch (e) {} mimClaim(); home();', '    try { archUnlock("m_alpha", 1, true); if (!nx && A.dead) archUnlock("m_alpha", 2, true); } catch (e) {} /* v670 */\n    addReport(rep); try { mapClash(fleetTarget(f), rep); } catch (e) {} mimClaim(); home();')
rep('    addReport(rep); try { mapClash(fleetTarget(f), rep); } catch (e) {} moClaimM(); moCineCheck(); home();', '    try { archUnlock("m_omega", 1, true); if (omPhX(o) >= 2) archUnlock("m_vault", 2, true); } catch (e) {} /* v670 */\n    addReport(rep); try { mapClash(fleetTarget(f), rep); } catch (e) {} moClaimM(); moCineCheck(); home();')
rep('  if (!M.cine[k + "a"]) { M.cine[k + "a"] = 1; dirty(); return moCine("arr"); }', '  if (!M.cine[k + "a"]) { M.cine[k + "a"] = 1; dirty(); try { archUnlock("m_vault", 1, true); } catch (e) {} return moCine("arr"); }')
rep('  if (M.moEnd && !M.moEnd.seen) { M.moEnd.seen = 1; dirty(); return moFinal(); }', '  if (M.moEnd && !M.moEnd.seen) { M.moEnd.seen = 1; dirty(); try { archUnlock("m_omega", 2, true); archUnlock("m_frag", 2, true); } catch (e) {} return moFinal(); }')
rep('const moPh = hp =>', 'const omPhX = o => o && o.hp != null ? (o.hp > 200 ? 1 : o.hp > 100 ? 2 : 3) : 1; /* v670 */\nconst moPh = hp =>')
rep('dv: "Cube Devastation", conv: "The Elemental Convergence" }, [a, b] = SEA_FIN[x];', 'dv: "Cube Devastation", conv: "The Elemental Convergence" }, [a, b0] = SEA_FIN[x], b = b0 || "krk"; /* v670 the Vault Seal in the Kraken\'s old slot */')
rep('const GAME_V = 669;', 'const GAME_V = 670;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
