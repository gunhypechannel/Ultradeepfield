# v651 monsters in battle (owner: "make sure all monsters move anatomically correct, also make sure the shield they generate covers their
# body more correctly"). A monster in battle used to be one still picture sliding about with a ship's engine plume and retro jets.
# Now each monster's battle picture is a loop of frames baked with the same body motion it has on the map (MON_WAVE: the shark's
# tail sweep, the manta's and moth's wingbeats, the spider's legs, the serpent's winding, the squid's arms), with every rhythm
# rounded to whole beats of a 3 s loop so it never jumps. It swims faster while it moves. No engine plumes on living things.
# Its shield is fitted to its own silhouette across the whole loop (centre and size from the picture's solid pixels), not a
# fixed oval round the middle of the picture.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)

# --- the baked frames
rep('function monAnimate(master, kind, U) {', r'''/* v651 battle frames: MON_WAVE with every rhythm rounded to a whole number of beats in MBF_P seconds, so the loop closes */
const MBF_P = 3, MBF_Z = 1.25, MBF_N = (typeof WEAK !== "undefined" && WEAK) || (typeof IOS !== "undefined" && IOS) ? 10 : 16, MBF_W = 2 * Math.PI / MBF_P;
const mbfQ = src => String(src).replace(/mt \* \(1\.5 - rr \* \.18\)/g, "mt * " + MBF_W.toFixed(5)).replace(/(uMT|mt) \* (\d+\.\d*|\.\d+|\d+)/g, (m, v, f) => v + " * " + (Math.max(+f >= .6 ? 1 : 0, Math.round(+f / MBF_W)) * MBF_W).toFixed(5));
function monBatPose(root, kind, f) { if (!MON_WAVE[kind]) return null; const U = { value: f / MBF_N * MBF_P }, done = new Map(), wave = mbfQ(MON_WAVE[kind]);
  root.traverse(o => { if (!o.isMesh || !o.material || Array.isArray(o.material)) return; let m = done.get(o.material);
    if (!m) { m = o.material.clone(); const pu = m.userData && m.userData.pulse ? mbfQ(m.userData.pulse) : null;
      m.onBeforeCompile = sh => { sh.uniforms.uMT = U; sh.vertexShader = "uniform float uMT;\n" + sh.vertexShader.replace("#include <begin_vertex>", "#include <begin_vertex>\nfloat mt = uMT;\n" + wave);
        if (pu) sh.fragmentShader = "uniform float uMT;\n" + sh.fragmentShader.replace("#include <emissivemap_fragment>", "#include <emissivemap_fragment>\n totalEmissiveRadiance *= " + pu + ";"); };
      m.customProgramCacheKey = () => "monbat-" + kind + (pu ? "-p" + hash(pu) : ""); done.set(o.material, m); } o.material = m; });
  return [...done.values()]; }
/* which frame a monster in battle shows: its own phase, a little faster while it moves; the nearer of two frames full, the other over it */
function monBatFrame(b, i, k, real, moving) { if (!MON_WAVE[k]) return null; const pre = b.mfPre || (b.mfPre = {}); if (!pre[k]) { pre[k] = 1; for (let f = 0; f < MBF_N; f++) shipArtSoon(k, "~f" + f, "side"); }
  const P = b.mph || (b.mph = []); P[i] = ((P[i] == null ? (i * .37) % 1 : P[i]) + Math.min(80, real || 16) / 1000 / MBF_P * (moving ? 1.35 : 1)) % 1;
  const x = P[i] * MBF_N, f0 = Math.floor(x) % MBF_N, f1 = (f0 + 1) % MBF_N, w = x - Math.floor(x), a0 = shipArtSoon(k, "~f" + f0, "side"), a1 = shipArtSoon(k, "~f" + f1, "side");
  if (!a0 && !a1) return null; if (!a1) return ["~f" + f0, null, 0]; if (!a0) return ["~f" + f1, null, 0]; return w < .5 ? ["~f" + f0, "~f" + f1, w] : ["~f" + f1, "~f" + f0, 1 - w]; }
/* v651 a monster's shield: the ellipse round the solid part of its picture, over every frame of its loop (in picture units) */
const MFIT = {}, MF_GX = 64, MF_GY = 32;
function mfitCv(cv) { if (cv._fit !== undefined) return cv._fit; let F = null; try { const w = cv.width, h = cv.height, D = cv.getContext("2d").getImageData(0, 0, w, h).data, st = w > 400 ? 2 : 1; F = new Uint8Array(MF_GX * MF_GY); let any = 0;
    for (let y = 0; y < h; y += st) for (let x = 0; x < w; x += st) if (D[(y * w + x) * 4 + 3] > 70) { F[((y * MF_GY / h) | 0) * MF_GX + ((x * MF_GX / w) | 0)] = 1; any = 1; }
    if (!any) F = null; } catch (e) { F = null; } return (cv._fit = F); }
/* the smallest upright ellipse round the occupied cells (centred on them), in picture units: [cx, cy, rx, ry] */
function mfitEll(O) { let x0 = MF_GX, x1 = -1, y0 = MF_GY, y1 = -1; for (let y = 0; y < MF_GY; y++) for (let x = 0; x < MF_GX; x++) if (O[y * MF_GX + x]) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
  if (x1 < 0) return null; const cx = (x0 + x1 + 1) / 2 / MF_GX, cy = (y0 + y1 + 1) / 2 / MF_GY, P = [];
  for (let y = 0; y < MF_GY; y++) for (let x = 0; x < MF_GX; x++) if (O[y * MF_GX + x]) { const dx = Math.max(Math.abs(x / MF_GX - cx), Math.abs((x + 1) / MF_GX - cx)), dy = Math.max(Math.abs(y / MF_GY - cy), Math.abs((y + 1) / MF_GY - cy)) * .5; P.push(dx, dy); } /* y in units of the picture's width */
  let best = null; for (let a = .12; a <= 1.6; a += .02) { let r = 0; for (let n = 0; n < P.length; n += 2) { const v = Math.hypot(P[n], P[n + 1] / a); if (v > r) r = v; } const A = r * r * a; if (!best || A < best[0]) best = [A, r, r * a]; }
  return [cx, cy, best[1], best[2] * 2]; }
function monShFit(k, cx, cy, L, face) { const S0 = studio(); if (!S0) return null; let M = MFIT[k]; if (!M) M = MFIT[k] = { done: {}, O: null, e: null, t: 0 };
  const now = performance.now(); if (now - M.t > 250) { M.t = now; for (let f = 0; f < MBF_N; f++) { if (M.done[f]) continue; const cv = S0.cache[k + "|~f" + f + "|side"]; if (!cv || !cv.getContext) continue; M.done[f] = 1; const F = mfitCv(cv); if (!F) continue;
      if (!M.O) M.O = F.slice(); else for (let n = 0; n < F.length; n++) M.O[n] |= F[n]; M.e = mfitEll(M.O); break; } }
  const e = M.e; if (!e) return null; const w = L * (DRAWK[k] || 2) * MBF_Z, h = w / 2, rx = e[2] * w * 1.08, ry = Math.max(e[3] * h * 1.08, rx * .3);
  return [cx + face * (e[0] - .5) * w, cy + (e[1] - .5) * h, rx, ry]; }
function monAnimate(master, kind, U) {''')
rep('''  let rotK = 0; { const mr = /~p(\\d+)$/.exec(String(accent)); if (mr) { rotK = +mr[1]; accent = String(accent).slice(0, mr.index); } }''',
    '''  let rotK = 0; { const mr = /~p(\\d+)$/.exec(String(accent)); if (mr) { rotK = +mr[1]; accent = String(accent).slice(0, mr.index); } }
  let mfr = -1; { const mf = /~f(\\d+)$/.exec(String(accent)); if (mf) { mfr = +mf[1]; accent = String(accent).slice(0, mf.index); } } /* v651 a monster's battle frame */''')
rep('if (fin && kind === "s") hullFinish(ship, fin, k); S.scene.add(ship);', 'if (fin && kind === "s") hullFinish(ship, fin, k); const mfM = mfr >= 0 && kind === "a" ? monBatPose(ship, k, mfr) : null; S.scene.add(ship);')
rep('S.camera.position.copy(dir.multiplyScalar(dist)); S.camera.lookAt(0, 0, 0); S.camera.updateProjectionMatrix();', 'S.camera.position.copy(dir.multiplyScalar(dist * (mfr >= 0 ? MBF_Z : 1))); S.camera.lookAt(0, 0, 0); S.camera.updateProjectionMatrix(); /* v651 room for the limbs in motion */')
rep('if (art) { const w = L * (DRAWK[k] || (AL[k] ? 2 : 1.8)), h = w / 2;', 'if (art) { const w = L * (DRAWK[k] || (AL[k] ? 2 : 1.8)) * (/~f\\d+$/.test(accent) ? MBF_Z : 1), h = w / 2; /* v651 */')
rep('    S.scene.remove(ship); ship.traverse(o => {', '    S.scene.remove(ship); if (mfM) mfM.forEach(m => m.dispose()); ship.traverse(o => {')

# --- the battle: frames, no plumes, fitted shield
rep('vc = MON[q.k] ? 1 : Math.min(busy ? 3 : 6, Math.max(1, visN(q.role, Math.max(n, 1)))), moving = Math.hypot(nx.x - p.x, nx.y - p.y) > .2;',
    'vc = MON[q.k] ? 1 : Math.min(busy ? 3 : 6, Math.max(1, visN(q.role, Math.max(n, 1)))), moving = Math.hypot(nx.x - p.x, nx.y - p.y) > .2;\n      const mf = MON[q.k] && !dying ? monBatFrame(b, i, q.k, real, moving) : null; /* v651 */')
rep('          if (ba) { ctx.translate(sx, sy); ctx.rotate(ba); ctx.translate(-sx, -sy); } }', '          if (mf) { acc3 = mf[0]; acc3b = mf[1]; w3 = mf[2]; } /* v651 the monster\'s body in motion */\n          if (ba) { ctx.translate(sx, sy); ctx.rotate(ba); ctx.translate(-sx, -sy); } }')
rep('if (!lo && !(busy && j > 1)) { /* v83: big fights', 'if (!lo && !MON[q.k] && !(busy && j > 1)) { /* v651 living things have no engines. v83: big fights')
a = 'ex = cx - face * L * .25 * Math.min(vc - 1, 2), rx = L * (.62 + .22 * Math.min(vc - 1, 3)), ry = L * (.32 + .18 * Math.min(vc - 1, 2));'
rep(a, 'sf = MON[q.k] && vc === 1 ? monShFit(q.k, cx, cy, L, face) : null, /* v651 */ ex = sf ? sf[0] : cx - face * L * .25 * Math.min(vc - 1, 2), ecy = sf ? sf[1] : cy, rx = sf ? sf[2] : L * (.62 + .22 * Math.min(vc - 1, 3)), ry = sf ? sf[3] : L * (.32 + .18 * Math.min(vc - 1, 2));')
i = s.index('ecy = sf ? sf[1] : cy'); j = s.index('ctx.drawImage(glowSprite("fire"), ex - hr, cy - hr, hr * 2, hr * 2)', i) + 80
seg = s[i:j]
for x, y in [('[ex, cy, rx, ry, sv]', '[ex, ecy, rx, ry, sv]'), ('ctx.ellipse(ex, cy, rx, ry, 0, 0, TAU)', 'ctx.ellipse(ex, ecy, rx, ry, 0, 0, TAU)'), ('ctx.ellipse(ex, cy, rx * e2', 'ctx.ellipse(ex, ecy, rx * e2'),
             ('{ x: ex, y: cy, t,', '{ x: ex, y: ecy, t,'), ('{ t, x: ex, y: cy, rx', '{ t, x: ex, y: ecy, rx'), ('SFX.shield(sp(ex, cy))', 'SFX.shield(sp(ex, ecy))'), ('y: cy / H', 'y: ecy / H'), ('ex - hr, cy - hr', 'ex - hr, ecy - hr')]:
    if seg.count(x) != 1: raise SystemExit('seg ' + x + ' ' + str(seg.count(x)))
    seg = seg.replace(x, y)
s = s[:i] + seg + s[j:]
rep('const GAME_V = 650', 'const GAME_V = 651')
open(p, 'w', encoding='utf-8').write(s)
