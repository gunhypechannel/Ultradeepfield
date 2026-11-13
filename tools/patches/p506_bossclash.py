# v506 fleets fight world bosses and super bosses on the map (owner): a fleet stops at stand-off range from the boss instead of
# flying into it, and when its attack lands the battle plays out there like other map battles: our line holds its firing range,
# bolts pour into the boss's hull, the boss answers with its own moves and return fire, and our ships blow apart round by round
# as the report says. The real fleet is hidden while its battle is drawn, then flies home from the stand-off point.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
HELP = r'''/* v506 a world or super boss as a map battle's defender: its model on the map, its size, and the range fleets fight it from */
const bossLocKey = L => !L ? null : L.kind === "wboss" ? L.wb : L.kind === "sboss" ? String(L.id).slice(3) : null;
function bossM(L) { const k = bossLocKey(L); if (!k || !G3) return null; if (L.kind === "wboss") { const M = G3.wbM && G3.wbM[k]; return M && M.b && M.b.grp.visible ? { b: M.b, grp: M.b.grp, M, k, col: WB[k] ? WB[k].col : "#ff9a5a" } : null; }
  const X = G3.sb; return X && X.live && X.key === k && X.b ? { b: X.b, grp: X.b.grp, X, k, sb: 1, col: SBW[k] ? SBW[k].col : "#c890ff" } : null; }
function bossMeasure(m) { const b = m.b; if (b._mr && b._ms === m.grp.scale.x) return b._mr; let r = (b.r || 12) * m.grp.scale.x; try { m.grp.updateMatrixWorld(true); const c = m.grp.getWorldPosition(new TH.Vector3()), bx = new TH.Box3(), q = new TH.Box3(); let any = 0;
    m.grp.traverse(o => { if (!o.isMesh || !o.visible || !o.geometry) return; let p = o, vis = true; while (p && p !== m.grp) { if (!p.visible) { vis = false; break; } p = p.parent; } if (!vis) return; if (!o.geometry.boundingBox) o.geometry.computeBoundingBox(); if (o.isInstancedMesh && o.computeBoundingBox) { o.computeBoundingBox(); q.copy(o.boundingBox); } else q.copy(o.geometry.boundingBox); q.applyMatrix4(o.matrixWorld); bx.union(q); any = 1; });
    if (any) r = Math.max(r, Math.hypot(Math.max(Math.abs(bx.min.x - c.x), Math.abs(bx.max.x - c.x)), Math.max(Math.abs(bx.min.z - c.z), Math.abs(bx.max.z - c.z))) * .8); } catch (e) {} b._ms = m.grp.scale.x; return (b._mr = r); } /* its real reach on the map, measured once from its visible hull */
function bossR(L) { const m = bossM(L); if (m) return Math.max(4, bossMeasure(m)); const k = bossLocKey(L); return L.kind === "wboss" && WB[k] ? (WB[k].sc || 1) * 1.6 * 13 : 70; }
function bStand(L) { if (L._bst && L._bstAt > performance.now() - 30000) return L._bst; L._bstAt = performance.now(); return (L._bst = bossR(L) * 1.15 + 8); }
'''
rep('function standOff(a, b, d) {', HELP + 'function standOff(a, b, d) {')
# the course: out to the stand-off point, the fight held there, home from there
rep('else if (PB[tg.id]) b = standOff(a, b, xStand(tg)); else if (near(a)) a = cubeStand(cp, b);', 'else if (PB[tg.id]) b = standOff(a, b, xStand(tg)); else if (bossLocKey(tg)) b = standOff(a, b, bStand(tg)); else if (near(a)) a = cubeStand(cp, b);')
rep(': PB[tg.id] ? standOff({ x: f.ox || hp.x, y: 0, z: f.oy || hp.z }, tp, xStand(tg)) : tp, b: hp,', ': PB[tg.id] ? standOff({ x: f.ox || hp.x, y: 0, z: f.oy || hp.z }, tp, xStand(tg)) : bossLocKey(tg) ? standOff({ x: f.ox || hp.x, y: 0, z: f.oy || hp.z }, tp, bStand(tg)) : tp, b: hp,')
rep('if (PB[tg.id]) { const sb = standOff({ x: f.ox || hp.x, y: 0, z: f.oy || hp.z }, tp, xStand(tg));', 'if (PB[tg.id] || bossLocKey(tg)) { const sb = standOff({ x: f.ox || hp.x, y: 0, z: f.oy || hp.z }, tp, PB[tg.id] ? xStand(tg) : bStand(tg));')
# the battle on the map when the attack lands
rep('    addReport(rep); fightShadow(rep); wbFight(key, seg, !left);', '    addReport(rep); try { mapClash(fleetTarget(f), rep); } catch (e) {} fightShadow(rep); wbFight(key, seg, !left);')
rep('    addReport(rep); fightShadow(rep); sbClaim(); home();', '    addReport(rep); try { mapClash(fleetTarget(f), rep); } catch (e) {} fightShadow(rep); sbClaim(); home();')
rep('const sideCmd = sd => { if (sd === "d" && loc && PB[loc.id]) return null;', 'const sideCmd = sd => { if (sd === "d" && loc && (PB[loc.id] || bossLocKey(loc))) return null;')
rep('const ff = loc && PB[loc.id] && S.fleets.find(f => f.xid === loc.id && f.ox != null);', 'const ff = loc && (PB[loc.id] ? S.fleets.find(f => f.xid === loc.id && f.ox != null) : bossLocKey(loc) ? S.fleets.find(f => fleetTarget(f) === loc && f.ox != null) : null);')
# drawing it: the stand-off radius, the boss as the defender, its moves and its return fire
rep('const q = c.loc === NEXUS ? W.nexus.position : P3(c.loc, T), R = PB[c.loc.id] ? xStand(c.loc) / 1.5 :', 'const BM = bossM(c.loc), q = c.loc === NEXUS ? W.nexus.position : P3(c.loc, T), R = BM ? bStand(c.loc) / 1.5 : PB[c.loc.id] ? xStand(c.loc) / 1.5 :')
rep('if (beastKind(c.loc)) { c.o.bx = beastInit(W, c); c.o.gd.visible = false; } }', 'if (beastKind(c.loc)) { c.o.bx = beastInit(W, c); c.o.gd.visible = false; } if (bossLocKey(c.loc)) { c.o.boss = 1; c.o.gd.visible = false; } }')
rep(': PB[c.loc.id] ? 1.5 : 2.5) + (1 - inK) * (c.ang != null ? 0 : 3)), dR =', ': PB[c.loc.id] || o.boss ? 1.5 : 2.5) + (1 - inK) * (c.ang != null ? 0 : 3)), dR =')
rep('    const BX = o.bx ? beastFx(', '''    if (o.boss) { o.gd.visible = false; if (BM) bossClashFx(W, c, o, BM, e, k, tn, () => alive(o.ga).map(s => out => wpos(o.ga, s, out))); }
    const BX = o.bx ? beastFx(''')
rep('if (o[key] !== keep) { if (BX && g === o.gd) {', 'if (o[key] !== keep) { if (o.boss && g === o.gd) { if (o[key] > keep && o[key] >= 0 && BM) { boom(bossPt(BM, V.clone()), 1); try { if (BM.b.moves && BM.b.moves.includes("hit")) BM.b.act("hit"); } catch (er) {} } o[key] = keep; continue; } if (BX && g === o.gd) {')
rep('const fromA = BX ? true : Math.random() < .5 + (fa - fd) * .3,', 'const fromA = BX || o.boss ? true : Math.random() < .5 + (fa - fd) * .3,')
rep('if (BX) { beastPt(o.bx, BX.cen, BX.dir, V2, 1); o.bx.hit = tn; } else if (ds.length)', 'if (BX) { beastPt(o.bx, BX.cen, BX.dir, V2, 1); o.bx.hit = tn; } else if (o.boss) { if (BM) bossPt(BM, V2); else V2.set(q.x, q.y, q.z); } else if (ds.length)')
FX = r'''/* v506 a point on the boss's hull, and the boss's side of the battle: its own attack moves through the fight, and return fire
   (heavy bolts in its colour) from its body into our line */
function bossPt(BM, out) { const c = BM.grp.getWorldPosition(out), r = bossR({ kind: BM.sb ? "sboss" : "wboss", wb: BM.k, id: "sb_" + BM.k }) * .55, a = Math.random() * TAU, u = Math.random() * 2 - 1, h = Math.sqrt(1 - u * u) * r;
  return c.set(c.x + Math.cos(a) * h, c.y + u * r * .6 + (BM.b.h || 0) * BM.grp.scale.x * .3, c.z + Math.sin(a) * h); }
function bossClashFx(W, c, o, BM, e, k, tn, shipsAt) { const live = k < .86 && !reduced; if (!live) return;
  if (!o.bn || tn > o.bn) { o.bn = tn + 5200 + Math.random() * 1800; if (e > 1200) { try { const L = BM.sb ? (SBW[BM.k].mv || []) : (BM.b.moves || []).filter(x => x !== "hit" && x !== "link"); if (L.length && BM.k !== "aex") BM.b.act(L[(Math.random() * L.length) | 0]); if (BM.M) BM.M.next = performance.now() + 12000; } catch (er) {} } }
  if (!o.bf || tn > o.bf) { o.bf = tn + 380 + Math.random() * 420; const S2 = shipsAt(); if (S2.length) { const a = bossPt(BM, new TH.Vector3()), b = S2[(Math.random() * S2.length) | 0](new TH.Vector3()); if (!o.bcol) { const cc = new TH.Color(BM.col); o.bcol = [cc.r, cc.g, cc.b]; } o.bl.push({ a, b, t0: tn, L: a.distanceTo(b), col: o.bcol }); } } }
'''
rep('function drawClashes(W, t, T) {', FX + 'function drawClashes(W, t, T) {')
# the boss battle reads at map scale: our line drawn at the Cube battles' size, more fire, hull hits sized to the boss, and the
# cinematic camera frames our line and the boss together
rep('fsT = cube ? 1.55 : fs;', 'fsT = cube ? 1.55 : o.boss ? Math.max(2.6, bossR(c.loc) / 18) : fs;')
rep('nShots = atCube ? clamp(Math.ceil((aliveA.length + aliveD.length) / 10), 3, 14) : 3;', 'nShots = atCube ? clamp(Math.ceil((aliveA.length + aliveD.length) / 10), 3, 14) : o.boss ? 8 : 3;')
rep('b.sp.scale.setScalar(fsC * (b.big ? 1.6 : .6) * (.4 + a * 1.6)); }', 'b.sp.scale.setScalar((b.hs || fsC * (b.big ? 1.6 : .6)) * (.4 + a * 1.6)); }')
rep('const boom = (p, big) => { const b = o.booms.find(x => tn - x.t0 > 700) || o.booms[0]; b.t0 = tn; b.sp.position.copy(p); b.big = big; };', 'const boom = (p, big, hs) => { const b = o.booms.find(x => tn - x.t0 > 700) || o.booms[0]; b.t0 = tn; b.sp.position.copy(p); b.big = big; b.hs = hs || 0; };')
rep('if (o[key] > keep && o[key] >= 0 && BM) { boom(bossPt(BM, V.clone()), 1);', 'if (o[key] > keep && o[key] >= 0 && BM) { boom(bossPt(BM, V.clone()), 1, bossR(c.loc) * .45);')
rep("if (s1 >= 1 && Math.random() < .35) { const sb = o.booms.find(x => tn - x.t0 > 700); if (sb) { sb.t0 = tn; sb.sp.position.copy(b.b); sb.big = 0; } }", "if (s1 >= 1 && Math.random() < (o.boss ? .6 : .35)) { const sb = o.booms.find(x => tn - x.t0 > 700); if (sb) { sb.t0 = tn; sb.sp.position.copy(b.b); sb.big = 0; sb.hs = o.boss && !b.rf ? bossR(c.loc) * .12 : 0; } }")
rep("o.bl.push({ a, b, t0: tn, L: a.distanceTo(b), col: o.bcol }); } } }", "o.bl.push({ a, b, t0: tn, L: a.distanceTo(b), col: o.bcol, rf: 1 }); } } }")
rep('if (c) { const a = c.o.ga.position, b = c.o.gd.position;', 'if (c) { const a = c.o.ga.position, bm = c.o.boss && bossM(c.loc), b = bm ? bm.grp.getWorldPosition(new TH.Vector3()) : c.o.gd.position;')
rep('cam.goal = Object.assign({}, cam.goal || {}, { dist: clamp(a.distanceTo(b) * 1.2, 15, 90) }); cineBar(); } }', 'cam.goal = Object.assign({}, cam.goal || {}, { dist: clamp(a.distanceTo(b) * (bm ? 2.6 : 1.2), 15, bm ? 500 : 90) }); cineBar(); } }')
rep('(b.L ? Math.min(.22, 3.5 / b.L) : .22)', '(b.L ? Math.min(.22, (o.boss ? 11 : 3.5) / b.L) : .22)')
rep("o.bl.push({ a: V.clone(), b: V2.clone(), t0: tn, col: fromA ? (c.you === \"a\" ? [.4, 1, 1] : [1, .35, .3]) : (c.you === \"a\" ? [1, .45, .2] : [.4, 1, 1]) }); }", "o.bl.push({ a: V.clone(), b: V2.clone(), t0: tn, L: o.boss ? V.distanceTo(V2) : 0, col: fromA ? (c.you === \"a\" ? [.4, 1, 1] : [1, .35, .3]) : (c.you === \"a\" ? [1, .45, .2] : [.4, 1, 1]) }); }")
# against a boss the bolts are glowing tracers (a 1-pixel line is lost at boss scale): a sprite at the head of every shot
rep('    o.bolts.geometry.setDrawRange(0, n * 2);', '    if (o.boss) bossTracers(W, o, tn, fsC, c); o.bolts.geometry.setDrawRange(0, n * 2);')
rep('function drawClashes(W, t, T) {', r"""function bossTracers(W, o, tn, fsC, c) { if (!o.tr) { o.tr = []; const tx = W.glow.trc || (W.glow.trc = glowTex("255,255,255", 1)); for (let i = 0; i < 40; i++) { const sp = new TH.Sprite(W.additive(tx, 0xffffff, 0)); sp.renderOrder = 15; W.scene.add(sp); o.tr.push(sp); } o.trR = bossR(c.loc); }
  let i = 0; for (const b of o.bl) { if (i >= o.tr.length) break; const s0 = Math.min(1, (tn - b.t0) / 320), sp = o.tr[i++]; sp.position.set(b.a.x + (b.b.x - b.a.x) * s0, b.a.y + (b.b.y - b.a.y) * s0, b.a.z + (b.b.z - b.a.z) * s0); sp.material.color.setRGB(b.col[0], b.col[1], b.col[2]); sp.material.opacity = .95; sp.scale.setScalar(b.rf ? o.trR * .09 : fsC * 1.1); }
  for (; i < o.tr.length; i++) o.tr[i].material.opacity = 0; }
function drawClashes(W, t, T) {""")
rep('W.scene.remove(o.bolts); o.bolts.geometry.dispose(); o.bolts.material.dispose();', 'W.scene.remove(o.bolts); o.bolts.geometry.dispose(); o.bolts.material.dispose(); if (o.tr) for (const sp of o.tr) { W.scene.remove(sp); sp.material.dispose(); }')
s2 = re.sub(r"GAME_V = 505\b", "GAME_V = 506", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
