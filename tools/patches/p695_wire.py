# v695: the Leviathan's arrival, a 15-second directed entrance (see p695_levin.js), and cinematic cameras keep clear of stars and planets
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__)); R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const TW = RG ? Math.max(coil, gape) : 0, UT = .2;', 'const TW = RG && !out.noTw ? Math.max(coil, gape) : 0, UT = .2; /* v695 noTw: the arrival keeps the head in line while it roars */')
rep('M.b.ring = { R0, Rh: R0, a: Math.atan2(q.z, q.x), y: q.y, yh: q.y, k: 1, s: TAU * .465 * R0 / M.b.N * .57 }; g.position.set(0, 0, 0); g.rotation.set(0, 0, 0); g.scale.setScalar(1); } /* v617 */',
    'M.b.ring = { R0, Rh: R0, a: Math.atan2(q.z, q.x), y: q.y, yh: q.y, k: 1, s: TAU * .465 * R0 / M.b.N * .57 }; g.position.set(0, 0, 0); g.rotation.set(0, 0, 0); g.scale.setScalar(1); if (G.levIn) try { levInFx(W, M, t, T); } catch (e) { crumb("levIn " + e.message); levInEnd(1); } } /* v617; v695 the arrival */')
rep('''  W.camera.position.set(cam.tx + cam.dist * sp * Math.cos(cam.th), cam.ty + cam.dist * Math.cos(cam.ph), cam.tz + cam.dist * sp * Math.sin(cam.th));
  W.camera.lookAt(cam.tx, cam.ty, cam.tz);''', '''  W.camera.position.set(cam.tx + cam.dist * sp * Math.cos(cam.th), cam.ty + cam.dist * Math.cos(cam.ph), cam.tz + cam.dist * sp * Math.sin(cam.th));
  W.camera.lookAt(cam.tx, cam.ty, cam.tz);
  if (G.levIn) { try { levInCam(W, t); } catch (e) {} } else if (cam.cine) { try { const P = W.camera.position, Q = { x: P.x, y: P.y, z: P.z }; camClear(W, Q); if (Q.x !== P.x || Q.y !== P.y || Q.z !== P.z) { P.set(Q.x, Q.y, Q.z); W.camera.lookAt(cam.tx, cam.ty, cam.tz); } } catch (e) {} } /* v695 the Leviathan's arrival directs the camera; cinematic cameras keep clear of stars and planets */''')
rep('setTimeout(() => { try { cineObjStart("wb_" + k); } catch (e) {} }, 1200); },', 'setTimeout(() => { try { if (k === "lev" && levIntroStart(1)) return; /* v695 */ cineObjStart("wb_" + k); } catch (e) {} }, 1200); },')
rep('function wbMapFx(W, t, T) {', R('p695_levin.js') + '''setInterval(() => { try { if (!S || !G.ready || !G3 || view !== "galaxy" || G.levIn || battle || sheet || G.cineOn || tutOn() || G.wbShow || (G3.cam && G3.cam.cine)) return; const T = now(); if (!wbOn("lev", T) || !(wbState(T).hp.lev > 0)) return;
  const cy = wbCycOf("lev", T); if (S.levInSeen === cy) return; S.levInSeen = cy; dirty(); levIntroStart(0); } catch (e) {} }, 2500); /* v695 once per Leviathan event, the first time the map is open while it is live */
function wbMapFx(W, t, T) {''')
rep('  else if (cam.cine && !cam.siege) cineEnd(); // the siege camera directs itself', '  else if (cam.cine && !cam.siege && cam.cine.m !== "levin") cineEnd(); // the siege camera directs itself (v695: so does the Leviathan\'s arrival)')
CUT = "(RG && RG.cut != null ? Math.max(.001, Math.min(1, Math.max(0, (RG.a - TAU * .465 * Math.max(.04, RG.k) * U - RG.cut) / .02))) : 1)" # v695 the part of the body still behind the rift
rep('(i === 0 ? 1.1 : 1) * (LV ? 1 : Math.max(.001, 1 - pull(u)));', '(i === 0 ? 1.1 : 1) * (LV ? 1 : Math.max(.001, 1 - pull(u))) * ' + CUT.replace(' * U', ' * u') + ';')
rep('tail.scale.setScalar(RG ? RG.s * .17 :', 'tail.scale.setScalar(RG ? RG.s * .17 * ' + CUT.replace(' * U', '') + ' :')
rep('const GAME_V = 694;', 'const GAME_V = 695;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
