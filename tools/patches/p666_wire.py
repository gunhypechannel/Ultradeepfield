# v666 The Mimic Protocol: Mimic Echoes (owner spec section 5, "Build it all").
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
R = lambda f: open('tools/patches/' + f, encoding='utf-8').read()
rep('const monGone = x =>', R('p666_season.js') + 'for (const b of ECHO_BASE) { AL["e_" + b] = { n: "Echo " + SH[b].n, atk: Math.round(SH[b].atk * .6), sh: Math.round(SH[b].sh * .6), hull: Math.round(SH[b].hull * .6), val: Math.round(((SH[b].c.m || 0) + (SH[b].c.c || 0) + (SH[b].c.g || 0)) * .3), one: 1 }; } /* v666 */\n' + 'const monGone = x =>')
# the Echo units: 60% of the base class, no research; the same combat role as the original
rep('  if (st >= 4) { o.mtitan = 1; o.mguard += 1; } return o; }', '  if (st >= 4) { o.mtitan = 1; o.mguard += 1; } { const e = st >= 2 && mimEchoOn(T || now()); if (e) o["e_" + e.k] = e.n; } return o; }')
rep('  addReport(rep); mapClash(x, rep); addBurn({ xid: x.id, at: f.arrive,', '  if (mimSt) try { mimEcho(x, rep, res, f.arrive); } catch (e) {} /* v666 */\n  addReport(rep); mapClash(x, rep); addBurn({ xid: x.id, at: f.arrive,')
rep('function buildAlien(k) {\n  if (MIM_U[k]) return buildMimic(k);', 'function buildAlien(k) {\n  if (MIM_U[k] || /^e_/.test(k)) return buildMimic(k);')
rep('  if (cls === "mnexus") {', R('p666_echo.js') + '  if (cls === "mnexus") {')
rep('  C.mouth = new TH.MeshBasicMaterial({ color: 0x46c8ff, toneMapped: false });', '  C.mouth = new TH.MeshBasicMaterial({ color: 0x46c8ff, toneMapped: false });\n  C.ecorr = new TH.MeshPhysicalMaterial({ map: sC, color: 0x9aa4b4, emissiveMap: sE, emissive: 0x46ccff, emissiveIntensity: 1.6, metalness: .85, roughness: .3, clearcoat: 1, clearcoatRoughness: .15, envMapIntensity: 1.1 }); /* v666 corrupted plating */')
rep('/* combat profile per unit: role, weapon, armor (damage reduction), evasion, speed, point-defense rating */\nconst CPROF = {', '/* combat profile per unit: role, weapon, armor (damage reduction), evasion, speed, point-defense rating */\nconst CPROF = {')
# after CPROF exists, the Echoes copy their class's profile
rep('const MON_ATK = {', 'try { for (const b of ECHO_BASE) if (CPROF[b]) CPROF["e_" + b] = CPROF[b].slice(); } catch (e) {} /* v666 */\nconst MON_ATK = {')
# the hub: the active Echo
rep('  ${mimHubBoss(T, w)}\n', '  ${(() => { const e = mimEchoOn(T); return e ? `<div class="mimecho"><canvas data-ship="e_${e.k}" width="224" height="112"></canvas><div><b>Mimic Echoes: ${e.n} × ${AL["e_" + e.k].n}</b><small>The Assimilators copied our ${SH[e.k].n}s. They fight in every hive we attack for <span data-end="${e.until}">${ftime(e.until - T)}</span>. Destroy a Stage 3+ hive to wipe them (+2 Alloy each).</small></div></div>` : ""; })()}\n  ${mimHubBoss(T, w)}\n')
rep('.arfly{', '.mimecho{display:flex;gap:9px;align-items:center;padding:7px;border-radius:11px;border:1px solid rgba(255,120,120,.35);background:rgba(40,10,20,.45);margin:8px 0;flex:none}.mimecho canvas{width:112px;height:56px;flex:none}.mimecho div{display:flex;flex-direction:column;gap:2px;min-width:0}.mimecho small{font-size:12px;color:#cab}\n.arfly{')
rep('const GAME_V = 665;', 'const GAME_V = 666;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
