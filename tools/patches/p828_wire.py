"""v828: the Celestial Serpent's attacks and its elemental fire (owner: "add all that and any kind of elemental glow effects make it look
unique, the other monsters look great"). In battle:
- Attack poses: 12 more baked frames (~f100+: six swim phases x jaw half / full open), the jaw opening to ~36 degrees (atk) and the eyes and
  mouth flaring (head emission x up to 3.2). The swim settles onto the nearest of the six phases while it attacks, so the frames match.
- Timing (serpJaw): Coil Strike charges (jaw and eyes rising) to its strike, gapes at the bite, closes; Constrict lunges open, holds half
  open through the squeeze and gapes at the crush; every other shot snaps the jaw half open.
- Elemental fire (serpFx), traced from each frame's own picture (serpSpine: its back, its midline and its mouth): violet spirit flames
  licking up along its back, gold and violet embers rising off the body, a violet glow in the mouth that swells as it opens, and a gout
  of violet fire from the mouth on each strike."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 827;", "const GAME_V = 828;")
# the wave: the attack pose opens the jaw wider
rep("ja = jm * .28 * pow(max(0., sin(mt * .6 - 1.)), 3.);", "ja = jm * max(.28 * pow(max(0., sin(mt * .6 - 1.)), 3.), atk * .62);")
# map: no attack pose
rep(r'''sh.vertexShader.replace("#include <begin_vertex>", "#include <begin_vertex>\nfloat mt = uMT + modelMatrix[3].x * .37 + modelMatrix[3].z * .23;\n"''',
    r'''sh.vertexShader.replace("#include <begin_vertex>", "#include <begin_vertex>\nfloat atk = 0.;\nfloat mt = uMT + modelMatrix[3].x * .37 + modelMatrix[3].z * .23;\n"''')
# battle poses: frames 100+ are the Serpent's attack poses
rep('''function monBatPose(root, kind, f) { if (!MON_WAVE[kind]) return null; const U = { value: f / MBF_N * MBF_P }, done = new Map(), wave = mbfQ(MON_WAVE[kind]);''',
    '''function monBatPose(root, kind, f) { if (!MON_WAVE[kind]) return null; const AP = f >= 100 ? [Math.floor((f - 100) / 10), (f - 100) % 10 / 2] : null, atk = AP ? AP[1] : 0; /* v828 the Serpent's attack poses: phase of six, jaw half / full open */
  const U = { value: AP ? AP[0] / 6 * MBF_P : f / MBF_N * MBF_P }, done = new Map(), wave = mbfQ(MON_WAVE[kind]);''')
rep(r'''sh.vertexShader.replace("#include <begin_vertex>", "#include <begin_vertex>\nfloat mt = uMT;\n" + wave);''',
    r'''sh.vertexShader.replace("#include <begin_vertex>", "#include <begin_vertex>\nfloat atk = " + atk.toFixed(2) + ";\nfloat mt = uMT;\n" + wave);
        if (atk && kind === "cserp" && sh.fragmentShader.includes("varying vec3 vMP")) sh.fragmentShader = sh.fragmentShader.replace("#include <aomap_fragment>", "totalEmissiveRadiance *= 1. + " + (atk * 2.2).toFixed(2) + " * smoothstep(-.75, -.35, dot(vMP - vec3(2.6, 1.75, .01), vec3(.9989, -.0362, -.0288)) / 1.6);\n#include <aomap_fragment>"); /* v828 the eyes and mouth flare */''')
rep('''m.customProgramCacheKey = () => "monbat-" + kind''', '''m.customProgramCacheKey = () => "monbat-" + kind + (atk ? "-a" + atk : "")''')
# which frame: the Serpent settles on a phase and shows its attack pose
rep('''function monBatFrame(b, i, k, real, moving) { if (!MON_WAVE[k]) return null;''', '''function monBatFrame(b, i, k, real, moving) { if (!MON_WAVE[k]) return null; if (k === "cserp") { const r = serpFrame(b, i, real); if (r) return r; } /* v828 */''')
# every Serpent shot is remembered (the jaw snaps on each)
rep('''function beastAtkAdd(b, v) { const q = b.Q[v.s]; if (!q) return;''', '''function beastAtkAdd(b, v) { const q = b.Q[v.s]; if (!q) return; if (q.k === "cserp") { const V = b.serpV || (b.serpV = {}), a = V[v.s] || (V[v.s] = []); if (!a.length || v.t > a[a.length - 1]) { a.push(v.t); if (a.length > 6) a.shift(); } } /* v828 */''')
# where the lead body was drawn, for the fire
rep('''if (mf) { acc3 = mf[0]; acc3b = mf[1]; w3 = mf[2]; }''', '''if (mf) { acc3 = mf[0]; acc3b = mf[1]; w3 = mf[2]; if (q.k === "cserp" && !j) (b.serpAc || (b.serpAc = {}))[i] = { a: w3 > .5 && acc3b ? acc3b : acc3, x: sx, y: sy, L: sz, face: fs2 >= 0 ? 1 : -1, ba: bang }; }''')
rep('''try { serpDraw(ctx, b, scr, T, W, d, lo, t); } catch (e) {} /* v722 */''', '''try { serpDraw(ctx, b, scr, T, W, d, lo, t); } catch (e) {} /* v722 */ try { serpFx(ctx, b, T, d, lo, t); } catch (e) {} /* v828 */''')
NEW = r'''
/* ---------- v828 the Celestial Serpent's attacks and elemental fire (owner: "add all that and any kind of elemental glow effects make it look unique") ---------- */
/* how far its jaw is open (0-1) at battle time T: its Coil Strike and Constrict, and a snap on every other shot */
function serpJaw(b, i, T) { let o = 0; const ease = x => { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); };
  for (const m of b.bAtk || []) { if (m.s !== i) continue; const D = BEAST_DUR[m.a] || 1, u = (T - m.t0) / D; if (u < 0 || u > 1) continue;
    if (m.a === "coil") o = Math.max(o, u < .4 ? .55 * ease(u / .4) : u < .5 ? .55 + .45 * ease((u - .4) / .1) : 1 - ease((u - .5) / .35));
    else if (m.a === "constrict") o = Math.max(o, u < .15 ? ease(u / .15) : u < .7 ? 1 - .45 * ease((u - .15) / .1) : u < .78 ? .55 + .45 * ease((u - .7) / .08) : 1 - ease((u - .82) / .18)); }
  for (const vt of (b.serpV && b.serpV[i]) || []) { const dt = T - vt; if (dt >= 0 && dt < .7) o = Math.max(o, .5 * Math.sin(Math.PI * dt / .7)); }
  return clamp(o, 0, 1); }
function serpFrame(b, i, real) { const T = b.simT || 0, o = serpJaw(b, i, T), J = b.serpJ || (b.serpJ = {}); J[i] = o; if (o < .02) return null;
  const pre = b.serpPre || (b.serpPre = {}); if (!pre.k) { pre.k = 1; for (let ph = 0; ph < 6; ph++) for (const lv of [1, 2]) shipArtSoon("cserp", "~f" + (100 + ph * 10 + lv), "side"); }
  const P = b.mph || (b.mph = []); if (P[i] == null) P[i] = (i * .37) % 1; const ph = Math.round(P[i] * 6) % 6, tgt = ph / 6; let dp = tgt - P[i]; if (dp > .5) dp -= 1; if (dp < -.5) dp += 1;
  P[i] = (P[i] + dp * Math.min(1, (real || 16) / 90) + 1) % 1; /* the swim settles on the pose */
  const sw = monBatFrameSw(b, i, real), a1 = "~f" + (100 + ph * 10 + 1), a2 = "~f" + (100 + ph * 10 + 2), h1 = shipArtSoon("cserp", a1, "side"), h2 = shipArtSoon("cserp", a2, "side"), sw0 = sw && sw[0];
  if (!h1 || !h2 || !sw0) return null; const x = o < .5 ? o * 2 : (o - .5) * 2, A = o < .5 ? sw0 : a1, B = o < .5 ? a1 : a2; return x < .5 ? [A, B, x] : [B, A, 1 - x]; }
/* the plain swim frames without moving the phase (the serpent's own phase is held by serpFrame) */
function monBatFrameSw(b, i) { const P = b.mph, x = P[i] * MBF_N, f0 = Math.floor(x) % MBF_N, f1 = (f0 + 1) % MBF_N, w = x - Math.floor(x), a0 = shipArtSoon("cserp", "~f" + f0, "side"), a1 = shipArtSoon("cserp", "~f" + f1, "side");
  if (!a0 && !a1) return null; if (!a1) return ["~f" + f0]; if (!a0) return ["~f" + f1]; return w < .5 ? ["~f" + f0] : ["~f" + f1]; }
/* its body traced from a frame's picture: points along its back and its midline, and its mouth (in the picture's own -.5..5 frame) */
const SERP_SP = new WeakMap();
function serpSpine(cv) { let r = SERP_SP.get(cv); if (r !== undefined) return r; r = null; try { const W0 = cv.width, H0 = cv.height, D = cv.getContext("2d").getImageData(0, 0, W0, H0).data, st = Math.max(2, W0 / 64 | 0), top = [], mid = [];
    let hx = -1, hy = 0; for (let x = 0; x < W0; x += st) { let y0 = -1, sy = 0, n = 0; for (let y = 0; y < H0; y += 2) { if (D[(y * W0 + x) * 4 + 3] > 60) { if (y0 < 0) y0 = y; sy += y; n++; } }
      if (n > 2) { top.push([x / W0 - .5, y0 / H0 - .5]); mid.push([x / W0 - .5, sy / n / H0 - .5]); if (x > hx) { hx = x; hy = sy / n; } } }
    if (top.length > 4) r = { top, mid, head: [hx / W0 - .5 - .02, hy / H0 - .5 + .01] }; } catch (e) { r = null; } SERP_SP.set(cv, r); return r; }
function serpFx(ctx, b, T, d, lo, t) { if (!b.serpK || !b.serpAc) return; const VI = "rgba(176,92,255,1)", VW = "rgba(226,190,255,1)", GO = "rgba(255,206,100,1)";
  const fr = j => { const v = Math.sin(j * 12.9898 + 4.1) * 43758.5453; return v - Math.floor(v); };
  ctx.save(); ctx.globalCompositeOperation = "lighter";
  for (const i of b.serpK) { const A = b.serpAc[i]; if (!A || !(b.n[i] > 0)) continue; const cv = shipArtSoon("cserp", A.a, "side"); if (!cv) continue; const sp = serpSpine(cv); if (!sp) continue;
    const w = A.L * 2 * MBF_Z, h = w / 2, ca = Math.cos(A.ba || 0), sa = Math.sin(A.ba || 0), at = (u, v) => { const px = A.face * u * w, py = v * h; return [A.x + px * ca - py * sa, A.y + px * sa + py * ca]; };
    const o = (b.serpJ && b.serpJ[i]) || 0, shed = b.shed && b.shed[i] && T >= b.shed[i].t ? 1.35 : 1, pr = .8 + .2 * Math.sin(t * .004 + i);
    /* violet spirit flames along its back, each tongue its own flicker */
    const tp = sp.top, nf = lo ? Math.ceil(tp.length / 3) : tp.length; for (let j = 0; j < nf; j++) { const k = lo ? j * 3 : j, q = tp[k]; if (!q) continue; const tail = (q[0] + .5), fl = .55 + .45 * Math.sin(t * .011 + k * 1.9) * Math.sin(t * .007 + k * .7), len = A.L * (.1 + .16 * tail) * fl * shed, [x, y] = at(q[0], q[1]);
      const lx = x - A.face * len * .3; ctx.globalAlpha = .28 * pr * (.6 + .4 * tail); ctx.drawImage(glowSprite(VI), lx - len * .3, y - len * 1.05, len * .6, len * 1.2); ctx.globalAlpha = .16 * pr; ctx.drawImage(glowSprite(VW), lx - len * .1, y - len * .5, len * .2, len * .55); } /* leaning back, toward the tail */
    /* embers rising off the body, gold and violet */
    const mid = sp.mid, ne = lo ? 8 : 22; for (let j = 0; j < ne; j++) { const ph = (t * .00035 * (1 + fr(j) * .8) + fr(j + 50)) % 1, q = mid[Math.floor(fr(j + 9) * mid.length)], [x, y] = at(q[0], q[1]), s = (1.6 + 2.6 * fr(j + 3)) * d * (1 - ph * .5);
      ctx.globalAlpha = Math.sin(Math.PI * ph) * .85; ctx.drawImage(glowSprite(j % 3 ? GO : VI), x + Math.sin(ph * 6 + j) * A.L * .05 - s, y - ph * A.L * .55 - s, s * 2, s * 2); }
    /* the mouth: a violet glow that swells as the jaw opens */
    const [mx, my] = at(sp.head[0], sp.head[1]), mr = A.L * (.07 + .17 * o) * (.9 + .1 * Math.sin(t * .02)); (b.serpMo || (b.serpMo = {}))[i] = [mx, my]; ctx.globalAlpha = .2 + .45 * o; ctx.drawImage(glowSprite(VI), mx - mr, my - mr, mr * 2, mr * 2); ctx.globalAlpha = .1 + .35 * o; ctx.drawImage(glowSprite(VW), mx - mr * .25, my - mr * .25, mr * .5, mr * .5);
    /* the strike: a gout of violet fire from the mouth toward its prey */
    for (const m of b.bAtk || []) { if (m.s !== i) continue; const u = (T - m.t0) / (BEAST_DUR[m.a] || 1), u0 = m.a === "coil" ? .36 : .7, u1 = m.a === "coil" ? .62 : .95; if (u < u0 || u > u1) continue; const E = (b.serpEp || {})[m.e]; const ex = E ? E[0] : mx + A.face * A.L, ey = E ? E[1] : my;
      const k = (u - u0) / (u1 - u0), dx = ex - mx, dy = ey - my, n = lo ? 6 : 14, reach = Math.min(1, k * 2.2); for (let j = 0; j < n; j++) { const f = j / (n - 1) * reach, r = A.L * (.08 + .22 * f) * (1 - k * .6), wob = Math.sin(t * .03 + j * 1.7) * A.L * .04 * f;
        ctx.globalAlpha = (1 - k) * (1 - f * .45) * .8; ctx.drawImage(glowSprite(j % 4 ? VI : VW), mx + dx * f - r - dy / Math.hypot(dx, dy || 1) * wob, my + dy * f - r + dx / Math.hypot(dx || 1, dy) * wob, r * 2, r * 2); } } }
  ctx.restore(); }
'''
rep('''/* the story: a won fight against Serpents counts its dead hatchlings, once per report */''', NEW.strip("\n") + '''\n/* the story: a won fight against Serpents counts its dead hatchlings, once per report */''')
# the gout aims at its prey's screen spot: remember enemy spots each frame
rep('''  const hp = (i, sd, muz) => { const s0 = scr[i], g = b.geo && b.geo[i]; if (!s0) return [0, 0];''', '''  const hp = (i, sd, muz) => { const s0 = scr[i], g = b.geo && b.geo[i]; if (!s0) return [0, 0]; if (muz && b.serpMo) { const si = b.repOf && b.repOf[i] != null ? b.repOf[i] : i; if (b.serpMo[si] && b.n[si] > 0 && (Q[si] || {}).k === "cserp") return b.serpMo[si]; } /* v828 the Serpent fires from its mouth */''')
rep('''try { serpDraw(ctx, b, scr, T, W, d, lo, t); } catch (e) {} /* v722 */''', '''try { if (b.serpK && b.serpK.length) { const E = b.serpEp || (b.serpEp = {}); for (const m of b.bAtk || []) if (scr[m.e]) E[m.e] = [scr[m.e].x, scr[m.e].y]; } serpDraw(ctx, b, scr, T, W, d, lo, t); } catch (e) {} /* v722 */''')
rep("""    const sx = A.x + (m.wb ? (b.face[m.s] || 1) * Math.min(W * .1 * bLen("worldbreaker") * A.s, W * .55 * A.s) * .62 : 0), sy = A.y + (m.wb ?""", """    const si = b.repOf && b.repOf[m.s] != null ? b.repOf[m.s] : m.s, SM = (Q[si] || {}).k === "cserp" && b.serpMo && b.serpMo[si] && b.n[si] > 0 ? b.serpMo[si] : null; /* v828 the Serpent's beams leave its mouth */ const sx = SM ? SM[0] : A.x + (m.wb ? (b.face[m.s] || 1) * Math.min(W * .1 * bLen("worldbreaker") * A.s, W * .55 * A.s) * .62 : 0), sy = SM ? SM[1] : A.y + (m.wb ?""")
rep("""    for (const m of b.muz || []) { const A = scr[m.s]; if (A && T >= m.t && T - m.t < .22) lights.push({ x: A.x, y: A.y,""", """    for (const m of b.muz || []) { const A0 = scr[m.s], SM = (Q[m.s] || {}).k === "cserp" && b.serpMo && b.serpMo[m.s], A = SM ? { x: SM[0], y: SM[1] } : A0; if (A && T >= m.t && T - m.t < .22) lights.push({ x: A.x, y: A.y,""")
rep("""      case "coil": { const tr = m.tr || (m.tr = []); if (m.px != null && u < .7) { tr.push([m.px, m.py, T]); if (tr.length > 22) tr.shift(); } for (let j = 1; j < tr.length; j++) { const age = T - tr[j][2]; if (age > .45) continue; ctx.globalAlpha = (1 - age / .45) * .75; ctx.strokeStyle = j % 2 ? "rgba(255,211,107,1)" : "rgba(200,140,255,1)"; ctx.lineWidth = Lg * .12 * (1 - age / .45);""",
    """      case "coil": { const tr = m.tr || (m.tr = []), MP = b.serpMo && b.serpMo[m.s]; if (m.px != null && u < .7) { const p0 = MP || [m.px, m.py], l0 = tr[tr.length - 1]; if (!l0 || Math.hypot(p0[0] - l0[0], p0[1] - l0[1]) > 2 * d) { tr.push([p0[0], p0[1], T]); if (tr.length > 22) tr.shift(); } } for (let j = 1; j < tr.length; j++) { const age = T - tr[j][2]; if (age > .45) continue; ctx.globalAlpha = (1 - age / .45) * .55; ctx.strokeStyle = j % 2 ? "rgba(255,211,107,1)" : "rgba(200,140,255,1)"; ctx.lineWidth = Lg * .05 * (1 - age / .45); /* v828 the trail follows its head, not a blob at its middle */""")
open(p, "w", encoding="utf-8").write(s); print("ok")
