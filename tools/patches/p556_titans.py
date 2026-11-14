# v556 three Titan-class warships (owner's spec "THREE LEGENDARY TITAN-CLASS WARSHIPS"; names: Armageddon, Sovereign Ark, Eclipse Harbinger,
# the owner picked original names over Galactica/Basestar). Built from the spec's text (the reference images did not arrive).
#  - 3D: each is built in code by buildShip (titanModel), so the battle sprites, ship cards, galaxy-map models and the new inspection
#    viewer all come from the same model. Own PBR materials (tagged so the map's merged minis shade them), animated parts in ud.ti.
#  - Stats sit between the Citadel Supercarrier (~235k) and the Discovery Class (~4.9M): ~1.5M each, at the Reaper's power per cost.
#    Counters: Armageddon > Sovereign Ark > Eclipse Harbinger > Armageddon (rapid fire), bombers break Armageddon and the Ark's hangars,
#    destroyers and Reapers hit the Harbinger's exposed reactor.
#  - Battle sim: Worldbreaker Cannon (3 s charge, +50% damage taken while charging, then a beam at the heaviest enemy formation, x4
#    against turrets and stations); Sovereign Ark: Fleet Command Uplink (+6% accuracy, +15% shields for its side, fighter screen) and
#    Carrier Strike Wings; Eclipse Harbinger: Neural Drone Swarm hitting up to six formations at once. Deterministic (no rng).
#  - Battle visuals: the cannon's charge and beam with shockwaves, fighter wings, drone swarms.
#  - Inspection viewer (Titan detail card -> "Inspect in 3D"): 360 orbit, five views, signature ability and arrival sequences.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)

# ---------------- data ----------------
rep('  worldbreaker:{ n: "Cube Destroyer"', '''  armageddon: { n: "Armageddon", cls: "Titan", c: { m: 700000, c: 550000, g: 250000 }, atk: 12000, sh: 8000, hull: 140000, cargo: 20000, bs: 1200, fu: 900, dt: "hyper", sz: 1.5, req: { shipyard: 12, hyper: 9, plasmaT: 8, armor: 12 }, d: "The Worldbreaker. A gothic siege fortress built around a spinal superweapon: it locks in, charges and fires a beam that guts capital ships and planetary defences. Slow, and exposed while it charges. Rapid fire against Dreadnoughts, Battleships and every turret; strong against the Sovereign Ark. Bombers and the Eclipse Harbinger break it." },
  sovereign:  { n: "Sovereign Ark", cls: "Titan", c: { m: 600000, c: 650000, g: 300000 }, atk: 14000, sh: 36000, hull: 190000, cargo: 60000, bs: 2600, fu: 800, dt: "hyper", sz: 1.5, req: { shipyard: 12, hyper: 9, shields: 12, command: 4 }, d: "Imperial twin-hull command carrier. Its Fleet Command Uplink lifts the accuracy and shields of every ship on your side, and its hangars launch strike wings through the battle. Rapid fire against fighters and drones; strong against the Eclipse Harbinger. Its hangars are its weakness: bombers and Armageddon tear into it." },
  harbinger:  { n: "Eclipse Harbinger", cls: "Titan", c: { m: 550000, c: 600000, g: 350000 }, atk: 20000, sh: 15000, hull: 140000, cargo: 30000, bs: 2000, fu: 850, dt: "hyper", sz: 1.5, req: { shipyard: 12, hyper: 9, ionT: 8, computer: 10 }, d: "A six-armed alien supercarrier around an emerald reactor. Its Neural Drone Swarm strikes up to six enemy formations at once, so it shreds wide fleets and outlasts Armageddon. Its exposed reactor is its weakness: Destroyers, Reapers and the Sovereign Ark's fighter screen hit it hard." },
  worldbreaker:{ n: "Cube Destroyer"''')
rep('  supercarrier: { fighter: 12, heavyFighter: 8, lancer: 4, corvette: 2, drone: 8, spitter: 6 },', '''  supercarrier: { fighter: 12, heavyFighter: 8, lancer: 4, corvette: 2, drone: 8, spitter: 6 },
  armageddon: { battleship: 5, bastion: 4, destroyer: 3, dreadnought: 2, supercarrier: 2, sovereign: 2, rocket: 20, laser: 20, heavyLaser: 10, ion: 8, rail: 6, plasma: 4, fortress: 2, brute: 4, leviathan: 2 }, /* v556 titans */
  sovereign: { fighter: 30, heavyFighter: 20, lancer: 12, corvette: 6, bomber: 6, harbinger: 2, drone: 20, spitter: 12, cdrone: 20 },
  harbinger: { fighter: 20, heavyFighter: 15, lancer: 15, corvette: 10, guardian: 6, escortCarrier: 4, hauler: 20, heavyCargo: 12, armageddon: 2, drone: 15, spitter: 10 },''')
rep('Object.assign(RF.worldbreaker, { guardian: 30, escortCarrier: 20, supercarrier: 5, eclipse: 1 });', 'Object.assign(RF.worldbreaker, { guardian: 30, escortCarrier: 20, supercarrier: 5, eclipse: 1, armageddon: 2, sovereign: 2, harbinger: 2 }); Object.assign(RF.bomber, { armageddon: 3, sovereign: 4 }); RF.destroyer = Object.assign(RF.destroyer || {}, { harbinger: 3 }); RF.dreadnought = Object.assign(RF.dreadnought || {}, { harbinger: 1.5 }); /* v556 titan counters */')
rep('ships: ["worldbreaker", "eclipse"]', 'ships: ["worldbreaker", "eclipse", "armageddon", "sovereign", "harbinger"]')
rep('eclipse: ["titan", "beam", .33, 0, 1.6, 6],', 'eclipse: ["titan", "beam", .33, 0, 1.6, 6], armageddon: ["titan", "beam", .3, 0, 1.0, 4], sovereign: ["titan", "laser", .3, .02, 2.0, 9], harbinger: ["titan", "ion", .27, .1, 2.4, 6],')
rep('  eclipse:       ["plasma", 3, "#e6b3ff", .24, { hv: 1 }],', '  eclipse:       ["plasma", 3, "#e6b3ff", .24, { hv: 1 }],\n  armageddon:    ["missile", 8, "#ff6a2a", .22, { flank: 1 }],  // v556 siege missile barrage\n  sovereign:     ["mass", 3, "#e8f4ff", .18, {}],              // precision lance batteries\n  harbinger:     ["plasma", 4, "#7affc0", .2, { hv: 1 }],       // eclipse energy pulses')
rep('eclipse: "#8fd8ff", guardian: "#e6f0ff",', 'eclipse: "#8fd8ff", armageddon: "#ff5a2a", sovereign: "#a8e4ff", harbinger: "#5dffa8", guardian: "#e6f0ff",')
rep('const SIDE_LEN = { wbOvl: 1.8,', 'const SIDE_LEN = { armageddon: 2.2, sovereign: 2.2, harbinger: 2.1, wbOvl: 1.8,')
rep('const bLen = k => k === "worldbreaker" ? 4.3', 'const TITAN_LEN = { armageddon: 3.2, sovereign: 3.1, harbinger: 3.0 }; /* v556 the Titans: above the Discovery Class, below the Cube Destroyer */\nconst bLen = k => TITAN_LEN[k] ? TITAN_LEN[k] : k === "worldbreaker" ? 4.3')
rep('const DRAWK = { worldbreaker: 3.2,', 'const DRAWK = { armageddon: 2, sovereign: 2, harbinger: 2, worldbreaker: 3.2,')
rep('const MINI_CLS = { spyProbe: "s",', 'const MINI_CLS = { armageddon: "x", sovereign: "x", harbinger: "x", spyProbe: "s",')

# ---------------- the battle simulation ----------------
rep('sq.some(s => s.side === side && s.k === "supercarrier") ? .15', 'sq.some(s => s.side === side && (s.k === "supercarrier" || s.k === "sovereign")) ? .15')
rep('if (docA === "balanced") sideAcc.a += .06;', 'for (const side of ["a", "d"]) if (sq.some(s => s.side === side && s.k === "sovereign" && s.n > 0)) { sideAcc[side] += .06; for (const s of sq) if (s.side === side) { s.shPer *= 1.15; s.shp = s.n * s.shPer; } } /* v556 Fleet Command Uplink */\n  if (docA === "balanced") sideAcc.a += .06;')
rep('  while (t < T_MAX - 1e-9 && alive("a") && alive("d")) {', '''  /* v556 the Titans' signature abilities, on their own clocks; no randomness, so a replay and a settle give the same result */
  const tiNote = (s, key, txt) => { const k2 = "ti" + key + s.side; if (!joinN[k2]) { joinN[k2] = 1; note_(t, s.side, "ability", txt); } };
  const tiVol = (s, e, wk, mult, atk, ab) => { volley(s, e, wk, mult, atk); if (vols && vols.length) vols[vols.length - 1].ab = ab; };
  const titanAct = s => { if (s.tcd == null) s.tcd = s.k === "armageddon" ? 6 : s.k === "sovereign" ? 2 : 3.5; s.tcd -= dt;
    if (s.k === "armageddon") {
      if (!s.chg && s.tcd <= 0) { let b = null, bv = 0; for (const e of sq) if (e.side !== s.side && active(e)) { const v = e.n * (e.hull + e.sh) * (BIG_R.has(e.role) || e.role === "station" || e.role === "turret" ? 2 : 1); if (v > bv) { bv = v; b = e; } }
        if (b) { s.chg = 3; s.vul = 1.5; s.ctg = b; tiNote(s, "c", `Armageddon locks in and charges the Worldbreaker Cannon`); if (vols) vols.push({ t: Math.round(t * 100) / 100, s: s.id, e: b.id, wk: "beam", n: 0, ic: 0, sh: 0, hull: 0, dead: 0, crit: 0, bounce: 0, ab: "wbcC" }); } }
      if (s.chg) { s.chg -= dt; if (s.chg <= 0) { s.chg = 0; s.vul = 1; s.tcd = 14; const b = s.ctg && active(s.ctg) ? s.ctg : sq.find(e => e.side !== s.side && active(e)); if (b) { tiVol(s, b, "beam", 3, s.atk * (b.role === "station" || b.role === "turret" ? 4 : 1.5), "wbc"); tiNote(s, "f", "The Worldbreaker Cannon fires"); } } } }
    else if (s.k === "sovereign") { if (s.tcd <= 0) { s.tcd = 6; let b = null, bd = 70; for (const e of sq) if (e.side !== s.side && active(e)) { const d2 = dist(s, e); if (d2 < bd) { bd = d2; b = e; } }
        if (b) { tiVol(s, b, "laser", 8, Math.max(80, s.atk * .3), "wing"); tiNote(s, "w", "Sovereign Ark launches its carrier strike wings"); } } }
    else if (s.k === "harbinger") { if (s.tcd <= 0) { s.tcd = 3; const T6 = sq.filter(e => e.side !== s.side && active(e)).sort((a, b) => dist(s, a) - dist(s, b)).slice(0, 6);
        for (const e of T6) tiVol(s, e, "torpedo", 4, Math.max(60, s.atk * .25), "swarm"); if (T6.length) tiNote(s, "s", "Eclipse Harbinger releases its Neural Drone Swarm"); } } };
  while (t < T_MAX - 1e-9 && alive("a") && alive("d")) {''')
rep('          if (b) volley(s, b, "laser", 3 * 4 / WPN.laser.cd, Math.max(50, s.atk * .15)); } }', '          if (b) volley(s, b, "laser", 3 * 4 / WPN.laser.cd, Math.max(50, s.atk * .15)); } }\n      if (s.k === "armageddon" || s.k === "sovereign" || s.k === "harbinger") titanAct(s); /* v556 */')
rep('* (crit ? 1.6 : 1) * aura[s.side]', '* (crit ? 1.6 : 1) * aura[s.side] * (e.vul || 1)')

# ---------------- battle visuals ----------------
rep('const lo = b.lowFx, cap = PERF.battleCap, wk = v.wk,', 'if (v.ab && titanFx(b, v)) return; /* v556 */\n  const lo = b.lowFx, cap = PERF.battleCap, wk = v.wk,')
rep('  for (const m of b.beams) { const age = T - m.t0; if (age < 0) continue;', '  for (const m of b.beams) { const age = T - m.t0; if (age < 0) continue;\n    if (m.ti) { titanBeamDraw(ctx, b, m, age, scr, W, d, lo, T); continue; } /* v556 */')
FX = r'''
/* ---------- v556 Titan battle effects ---------- */
function titanFx(b, v) { const q = b.Q[v.s]; if (!q) return false; const side = q.side, sz = q.sz != null ? q.sz : (q.sz = szOf(q));
  if (v.ab === "wbcC") { b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: "c", charge: 3, life: 0 }); return true; }
  if (v.ab === "wbc") { b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: "b", charge: 0, life: 1.3 }); b.fx.push({ t0: v.t, t1: v.t + .12, v, last: true, first: true, n: 1, mis: false, ic: false, side, off: 0, hv: 0, sz, j: 0, hide: 1 }); try { SFX.charge && SFX.charge(); } catch (e) {} return true; }
  if (v.ab === "wing" || v.ab === "swarm") { const sw = v.ab === "swarm", n = b.lowFx ? 3 : sw ? 6 : 8, mis = sw;
    for (let j = 0; j < n; j++) b.fx.push({ t0: v.t + j * .05, t1: v.t + j * .05 + (sw ? .75 : .55) + (j % 3) * .06, v, last: j === n - 1, first: j === 0, n, mis, ic: false, side, off: (j / (n - 1) - .5) * 1.4, hv: 0, sz: 0, j, bs: sw ? (j % 2 ? 1 : -1) : 0, col: sw ? (j % 2 ? "#b06bff" : "#5dffa8") : "#9fdcff" });
    return true; }
  return false; }
function titanBeamDraw(ctx, b, m, age, scr, W, d, lo, T) { const S0 = scr[m.s], E0 = scr[m.e]; if (!S0) return; const q = b.Q[m.s], fc = b.face[m.s] || 1, Lg = W * .1 * bLen(q.k) * S0.s, bx = S0.x + fc * Lg * .48, by = S0.y;
  ctx.save(); ctx.globalCompositeOperation = "lighter";
  if (m.ti === "c") { const k = clamp(age / m.charge, 0, 1); // the cannon charges: rings close in, arcs jump, a white-hot sphere grows at the muzzle
    for (let r = 0; r < 3; r++) { const u = (k * 2 + r / 3) % 1, rr = Lg * (.32 - .24 * u); ctx.strokeStyle = "#ff6a2a"; ctx.globalAlpha = .25 + .6 * u; ctx.lineWidth = (1.5 + 2 * u) * d; ctx.beginPath(); ctx.ellipse(bx, by, rr * .5, rr, 0, 0, TAU); ctx.stroke(); }
    if (!lo) for (let j = 0; j < 5; j++) { const a = (T * 9 + j * 1.3) % TAU, r1 = Lg * .28, x1 = bx + Math.cos(a) * r1 * .5, y1 = by + Math.sin(a) * r1; ctx.strokeStyle = "#ffd0a0"; ctx.globalAlpha = .4 + Math.random() * .5; ctx.lineWidth = 1.2 * d; ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo((x1 + bx) / 2 + (Math.random() - .5) * 12 * d, (y1 + by) / 2 + (Math.random() - .5) * 12 * d); ctx.lineTo(bx, by); ctx.stroke(); }
    const cr = Lg * (.04 + .16 * k); ctx.globalAlpha = .7 + .3 * k; ctx.drawImage(glowSprite("#ff5a1a"), bx - cr * 3, by - cr * 3, cr * 6, cr * 6); ctx.drawImage(glowSprite("#ffffff"), bx - cr * .8, by - cr * .8, cr * 1.6, cr * 1.6);
    ctx.restore(); return; }
  if (!E0) { ctx.restore(); return; } const k = age / m.life, wv = Lg * .11 * (k < .15 ? k / .15 : 1 - Math.max(0, (k - .6) / .4));
  if (!m.sh) { m.sh = 1; b.shake = Math.max(b.shake || 0, 14 * d); for (let i = 0; i < (lo ? 2 : 5); i++) b.flashes.push({ x: E0.x + (Math.random() - .5) * 30 * d, y: E0.y + (Math.random() - .5) * 22 * d, t: performance.now(), r: (40 + Math.random() * 40) * d, life: 420, rot: Math.random() }); }
  const ang = Math.atan2(E0.y - by, E0.x - bx), L = Math.hypot(E0.x - bx, E0.y - by); ctx.translate(bx, by); ctx.rotate(ang);
  for (const [w, c, a] of [[wv * 2.6, "255,70,20", .35], [wv * 1.4, "255,150,60", .7], [wv * .5, "255,245,225", 1]]) { const g = ctx.createLinearGradient(0, -w, 0, w); g.addColorStop(0, `rgba(${c},0)`); g.addColorStop(.5, `rgba(${c},${a})`); g.addColorStop(1, `rgba(${c},0)`); ctx.fillStyle = g; ctx.globalAlpha = 1; ctx.fillRect(0, -w, L, w * 2); }
  ctx.setTransform(1, 0, 0, 1, 0, 0); try { const m0 = ctx.getTransform && ctx.getTransform(); } catch (e) {}
  ctx.restore(); ctx.save(); ctx.globalCompositeOperation = "lighter"; // shockwaves at the target and at the muzzle
  for (let r = 0; r < 3; r++) { const u = clamp(k * 1.4 - r * .18, 0, 1); if (u <= 0 || u >= 1) continue; ctx.globalAlpha = (1 - u) * .8; ctx.strokeStyle = r ? "#ffb070" : "#ffffff"; ctx.lineWidth = (5 - r) * d * (1 - u) + 1; ctx.beginPath(); ctx.ellipse(E0.x, E0.y, Lg * 1.2 * u, Lg * .6 * u, 0, 0, TAU); ctx.stroke(); }
  ctx.globalAlpha = .9 * (1 - k); const fr = Lg * .3; ctx.drawImage(glowSprite("#ff6a2a"), bx - fr, by - fr, fr * 2, fr * 2); ctx.restore(); }
'''
rep('function spawnVolley(b, v) {', FX + 'function spawnVolley(b, v) {')

# ---------------- 3D models ----------------
MODEL = r'''
/* ---------- v556 the Titans, built in code ---------- */
const TITAN_INFO = {
  armageddon: { tag: "The Worldbreaker · siege fortress", ab: "Worldbreaker Cannon", role: "Siege and anti-capital", adv: ["Heaviest armour of any Titan", "Worldbreaker Cannon: a charged beam at the heaviest enemy formation, ×4 against turrets and stations", "Rapid fire against Battleships, Dreadnoughts and every turret"], weak: ["Slowest ship in the fleet", "Takes +50% damage while the cannon charges", "Bombers and the Eclipse Harbinger break it"],
    more: ["Siege Missile Barrage", "Heavy Plasma Broadsides", "Fortress Point Defence"],
    seq: [[0, "Armageddon slows and locks into firing position"], [.9, "Armour plates retract around the cannon"], [1.7, "Reactor coils spin up; molten channels ignite"], [2.6, "Arcs jump across the focusing rings"], [3.4, "An orange-white sphere forms in the barrel"], [4.3, "The Worldbreaker Cannon fires"], [5.4, "Shockwave. Plates close; cooldown"]],
    arrive: "Emerges from a burning crimson rupture, its cannon powering up" },
  sovereign: { tag: "The imperial command carrier", ab: "Sovereign Fleet Command", role: "Fleet command, carriers, shields", adv: ["Fleet Command Uplink: +6% accuracy and +15% shields for your whole side", "Carrier Strike Wings launch every few seconds", "Fighter screen like a Supercarrier; rapid fire against fighters and drones"], weak: ["Lower direct damage than Armageddon", "Exposed hangars: bombers and Armageddon hit it hard"],
    more: ["Sovereign Defence Grid", "Precision Lance Batteries", "Fleet Command Uplink"],
    seq: [[0, "Blue energy runs across the hull"], [.9, "Twin hangar doors open; launch lights come on"], [1.8, "Fighters accelerate from the launch decks"], [2.9, "Shield arrays unfold"], [3.6, "A tactical field spreads around the Ark"], [4.6, "Escorts form up in fleet formation"]],
    arrive: "Arrives at the head of a fleet formation, hangars glowing blue" },
  harbinger: { tag: "The alien swarm carrier", ab: "Eclipse Swarm", role: "Drone carrier, battlefield control", adv: ["Neural Drone Swarm strikes up to six formations at once", "Shreds wide fleets of small ships", "Strong against Armageddon"], weak: ["Exposed reactor: Destroyers and Reapers hit it hard", "Weaker against the Sovereign Ark's fighter screen"],
    more: ["Eclipse Energy Pulse", "Adaptive Alien Barrier", "Collective Targeting Network"],
    seq: [[0, "The reactor pulses emerald"], [.9, "All six arms turn independently"], [2.0, "The arms lock into a defensive circle"], [2.8, "Violet and green beams join the arm tips"], [3.5, "Hidden launch chambers open"], [4.0, "The drone swarm pours out"], [5.0, "An energy field closes around the core"]],
    arrive: "Materialises in a green distortion, unfolding its six arms" } };
function titanMats(k) { const S = studio(), key = "tim" + k; if (S && S.cache[key]) return S.cache[key]; const T = (S && S.tex) || {};
  const P = (o, mn) => { const ph = (o.clearcoat || 0) > 0, o2 = Object.assign({ metalness: .85, roughness: .32, envMapIntensity: 1.2, flatShading: true }, ph ? { clearcoat: .55, clearcoatRoughness: .2 } : {}, o); if (!ph) { delete o2.clearcoat; } const m = ph ? new TH.MeshPhysicalMaterial(o2) : new TH.MeshStandardMaterial(o2); m.userData.mn = mn; return m; };
  const E = (col, mn) => { const m = new TH.MeshBasicMaterial({ color: col, toneMapped: false }); m.userData.mn = mn; m.userData.c0 = new TH.Color(col); return m; };
  let o; if (k === "armageddon") o = { hull: P({ map: T.dark, color: 0x0b0c0e, roughness: .4, metalness: .55, clearcoat: .15, envMapIntensity: .8 }, "hull"), dark: P({ color: 0x030304, roughness: .45, metalness: .4, clearcoat: 0, envMapIntensity: .7 }, "dark"), trim: P({ color: 0x23262b, roughness: .3, metalness: .95, clearcoat: 0 }, "trim"), glow: E(0xff4a1a, "accent"), hot: E(0xffb070, "engine"), core: E(0xfff0d8, "win"), win: E(0xff7a3a, "win") };
  else if (k === "sovereign") o = { hull: P({ map: T.hull, color: 0xf4f6fa, roughness: .2, metalness: .72, clearcoat: .9 }, "hull"), dark: P({ color: 0x27303c, roughness: .4 }, "dark"), trim: P({ color: 0x9a6514, metalness: 1, roughness: .24, clearcoat: .6, envMapIntensity: 2, flatShading: false }, "gold"), glow: E(0x6fd0ff, "accent"), hot: E(0xd8f2ff, "engine"), core: E(0xffffff, "win"), win: E(0xbfe8ff, "win") };
  else o = { hull: P({ map: T.dark, color: 0x0a0b0e, roughness: .34, metalness: .6, clearcoat: .2, envMapIntensity: 1 }, "dark"), dark: P({ color: 0x020203, roughness: .4, metalness: .35, clearcoat: 0, envMapIntensity: .6 }, "dark"), trim: P({ color: 0x1e2127, roughness: .24 }, "trim"), glow: E(0x3dff9a, "accent"), hot: E(0xb8ffd8, "engine"), core: E(0xe0ffee, "win"), win: E(0xb06bff, "accent") };
  if (S) S.cache[key] = o; return o; }
function titanModel(k, g) { const MT = titanMats(k), ud = g.userData; ud.eng = []; const TI = ud.ti = {}, r = rnd(hash(k) + 11);
  const add = (m, x, y, z, par) => { m.position.set(x || 0, y || 0, z || 0); (par || g).add(m); return m; }, mesh = (geo, mat) => new TH.Mesh(geo, mat);
  const box = (w, h, d, mat, x, y, z, par) => add(mesh(new TH.BoxGeometry(w, h, d), mat), x, y, z, par);
  const cylX = (rt, rb, h, mat, x, y, z, seg, par) => { const m = add(mesh(new TH.CylinderGeometry(rt, rb, h, seg || 24), mat), x, y, z, par); m.rotation.z = Math.PI / 2; return m; };
  const cylY = (rt, rb, h, mat, x, y, z, seg, par) => add(mesh(new TH.CylinderGeometry(rt, rb, h, seg || 24), mat), x, y, z, par);
  const torX = (R, tb, mat, x, y, z, par) => { const m = add(mesh(new TH.TorusGeometry(R, tb, 10, 56), mat), x, y, z, par); m.rotation.y = Math.PI / 2; return m; };
  const ext = (pts, depth, mat, bev) => { const sh = new TH.Shape(); pts.forEach(([x, z], i) => i ? sh.lineTo(x, -z) : sh.moveTo(x, -z)); const geo = new TH.ExtrudeGeometry(sh, { depth, bevelEnabled: bev > 0, bevelThickness: bev || 0, bevelSize: bev || 0, bevelSegments: 1, curveSegments: 6 }); geo.rotateX(-Math.PI / 2); return mesh(geo, mat); };
  const eng = (x, y, z, rr, len, par) => { cylX(rr * 1.18, rr * 1.32, len, MT.dark, x, y, z, 28, par); torX(rr * 1.25, rr * .12, MT.trim, x - len / 2, y, z, par); const n = add(mesh(new TH.CircleGeometry(rr, 28), MT.hot), x - len / 2 - .01, y, z, par); n.rotation.y = -Math.PI / 2; ud.eng.push([x - len / 2, y, z, rr]); };
  const greeb = (x0, x1, y, z0, z1, n, mats) => { for (let i = 0; i < n; i++) box(.05 + r() * .2, .02 + r() * .06, .05 + r() * .16, (mats || [MT.dark, MT.trim])[i % (mats || [0, 0]).length], x0 + r() * (x1 - x0), y, z0 + r() * (z1 - z0)); };
  if (k === "armageddon") { ud.engCol = [0xffe0b0, 0xff4a1a];
    const W1 = [[4.3, .3], [3.3, .95], [-2.5, 2.15], [-3.95, 2.15], [-3.95, -2.15], [-2.5, -2.15], [3.3, -.95], [4.3, -.3]], sc = (P2, sx, sz, dx) => P2.map(([x, z]) => [x * sx + (dx || 0), z * sz]);
    const hw = x => x <= -2.5 ? 2.15 : x <= 3.3 ? 2.15 + (x + 2.5) / 5.8 * (.95 - 2.15) : .95 + (x - 3.3) * (.3 - .95);
    add(ext(W1, .7, MT.hull, .05), 0, -.35, 0); add(ext(sc(W1, .86, .78, -.25), .42, MT.hull, .04), 0, .4, 0); add(ext(sc(W1, .64, .48, -.6), .36, MT.dark, .03), 0, .86, 0);
    add(ext(sc(W1, .8, .7, -.3), .34, MT.dark, .03), 0, -.72, 0); add(ext([[3.7, .05], [1.0, .26], [-2.6, .3], [-2.6, -.3], [1.0, -.26], [3.7, -.05]], .42, MT.trim, .02), 0, -1.12, 0); // belly and keel blade
    for (let x = -3.6; x <= 2.9; x += .42) { const w = hw(x) * .78; box(.07, .1, w * 2, MT.trim, x, .86, 0); box(.05, .4, .06, MT.dark, x, .1, w * 1.27); box(.05, .4, .06, MT.dark, x, .1, -w * 1.27); } // structural ribs
    for (const s of [1, -1]) for (let x = -3.6; x <= 2.6; x += .28) { const z = s * hw(x) * .52; box(.24, .02, .045, MT.glow, x, .87, z); } box(4.6, .03, .09, MT.glow, -.9, 1.23, 0); // molten reactor channels
    for (const s of [1, -1]) { const bz = s * 2.15; box(2.6, 1.05, .72, MT.hull, -2.4, .12, bz); box(2.4, .2, .8, MT.dark, -2.4, .7, bz); // the fortress bastions on each flank
      for (let x = -3.6; x <= -1.2; x += .3) box(.16, .16, .16, MT.trim, x, .88, bz + s * .3); for (let i = 0; i < 5; i++) { const x = -3.4 + i * .5; cylX(.05, .06, .5, MT.dark, x, .25, bz + s * .55).rotation.set(0, Math.PI / 2, Math.PI / 2); box(.18, .04, .02, MT.win, x, .45, bz + s * .37); box(.18, .04, .02, MT.win, x, -.05, bz + s * .37); }
      box(2.5, .03, .03, MT.glow, -2.4, .64, bz + s * .37); box(2.5, .03, .03, MT.glow, -2.4, -.38, bz + s * .37); greeb(-3.5, -1.3, -.42, bz - .3, bz + .3, 10); }
    for (let x = -3.2; x <= 1.6; x += .45) box(.22, .02, .5, MT.glow, x, -.74, 0); /* molten vents along the belly */
    for (const [x, z, h] of [[-2.3, 1.15, 1.6], [-2.3, -1.15, 1.6], [-.9, .72, 1.3], [-.9, -.72, 1.3]]) { cylY(.26, .32, h, MT.hull, x, .86 + h / 2, z, 6); add(mesh(new TH.ConeGeometry(.36, .55, 6), MT.dark), x, .86 + h + .27, z); for (let j = 0; j < 3; j++) box(.04, .18, .02, MT.win, x + .27, 1.1 + j * .35, z); cylY(.4, .4, .06, MT.trim, x, .86 + h * .7, z, 6); } // weapon towers
    for (const z of [.42, -.42]) for (let i = 0; i < 5; i++) { const x = -3.0 + i * .32; box(.2, .05, .2, MT.dark, x, 1.25, z); box(.12, .055, .04, MT.glow, x, 1.26, z); } // dorsal missile silos
    const C = new TH.Group(); g.add(C); C.position.set(0, .48, 0); TI.cannon = C; // the Worldbreaker Cannon: spine, coils, armour, focusing rings, muzzle
    cylX(.27, .31, 4.6, MT.dark, 3.3, 0, 0, 24, C); cylX(.1, .1, 4.4, MT.glow, 3.3, 0, 0, 12, C); cylX(.42, .3, .5, MT.trim, 5.65, 0, 0, 24, C);
    TI.coils = []; for (const x of [.55, 1.05, 1.55]) { const cg = new TH.Group(); cg.position.x = x; C.add(cg); torX(.66, .11, MT.dark, 0, 0, 0, cg); torX(.66, .035, MT.glow, 0, 0, 0, cg); for (let j = 0; j < 8; j++) { const a = j / 8 * TAU; box(.16, .16, .16, MT.trim, 0, Math.cos(a) * .66, Math.sin(a) * .66, cg); } TI.coils.push(cg); }
    TI.rings = []; for (const x of [2.6, 3.3, 4.0, 4.7, 5.3]) { const rg = new TH.Group(); rg.position.x = x; C.add(rg); torX(.44, .045, MT.trim, 0, 0, 0, rg); for (let j = 0; j < 4; j++) { const a = j / 4 * TAU + .4; box(.06, .07, .07, MT.glow, 0, Math.cos(a) * .44, Math.sin(a) * .44, rg); } TI.rings.push(rg); }
    TI.plates = []; for (let j = 0; j < 4; j++) { const pg = new TH.Group(); pg.position.x = 3.1; pg.rotation.x = j / 4 * TAU + Math.PI / 4; C.add(pg); const pl = box(1.7, .07, .42, MT.hull, 0, .36, 0, pg); box(1.5, .02, .05, MT.win, 0, .41, 0, pg); TI.plates.push(pl); }
    TI.core = add(mesh(new TH.SphereGeometry(.22, 20, 14), MT.core), 6.05, 0, 0, C); TI.core.scale.setScalar(.01); TI.core.userData.fx = 2;
    for (const [y, z] of [[.15, .75], [.15, -.75], [.15, 1.6], [.15, -1.6]]) { box(.9, .9, .82, MT.hull, -3.75, y, z); eng(-4.35, y, z, .34, .5); } // four rear drives
    greeb(-3.5, 2.6, .44, -1.2, 1.2, 70); greeb(-3.0, 1.8, -.92, -.9, .9, 30);
    TI.mats = [MT.glow, MT.win]; }
  else if (k === "sovereign") { ud.engCol = [0xffffff, 0x5fb8ff];
    const PR = PROF.sleek; TI.doors = []; TI.lights = []; TI.petals = [];
    for (const s of [1, -1]) { const z0 = s * 1.45; add(fuselage(8.4, .66, PR, .74, 1.05, MT.hull), .1, 0, z0); add(fuselage(7.6, .5, PR, .6, 1.0, MT.dark), -.15, -.2, z0);
      box(6.6, .05, .08, MT.trim, -.2, .42, z0); box(6.6, .035, .035, MT.glow, -.2, .05, z0 + s * .66); box(6.6, .035, .035, MT.glow, -.2, -.12, z0 + s * .62); // gold spine and blue conduits
      for (const x of [2.6, 1.0, -.6, -2.2]) { box(.06, .04, .9, MT.trim, x, .4, z0); box(.06, .3, .03, MT.trim, x, .2, z0 + s * .66); }
      box(5.4, .24, .1, MT.dark, -.4, -.02, z0 + s * .69); for (let i = 0; i < 12; i++) TI.lights.push(box(.12, .05, .02, MT.win, -2.9 + i * .44, -.02, z0 + s * .745)); // the fighter launch corridor
      box(1.6, .08, .56, MT.dark, 2.2, .4, z0); const hl = box(1.5, .02, .46, MT.glow, 2.2, .445, z0); TI.lights.push(hl); for (let i = 0; i < 5; i++) TI.lights.push(box(.05, .022, .4, MT.win, 1.6 + i * .3, .45, z0)); // the hangar deck
      for (const dx of [-.39, .39]) TI.doors.push({ m: box(.78, .05, .54, MT.hull, 2.2 + dx, .48, z0), x0: 2.2 + dx, dx: Math.sign(dx) });
      for (const x of [2.8, 1.4, -.4, -1.8]) { cylY(.08, .1, .08, MT.trim, x, .5, z0); box(.14, .07, .1, MT.hull, x, .56, z0); cylX(.012, .012, .55, MT.dark, x + .3, .57, z0 + .03); cylX(.012, .012, .55, MT.dark, x + .3, .57, z0 - .03); } // lance batteries
      for (const x of [1.9, -1.2]) { const sg = new TH.Group(); sg.position.set(x, .5, z0); g.add(sg); add(mesh(new TH.SphereGeometry(.18, 18, 10, 0, TAU, 0, Math.PI / 2), MT.glow), 0, 0, 0, sg); torX(.22, .02, MT.trim, 0, .02, 0, sg).rotation.set(Math.PI / 2, 0, 0);
        for (let j = 0; j < 6; j++) { const pg = new TH.Group(); pg.rotation.y = j / 6 * TAU; sg.add(pg); const pt = box(.32, .02, .1, MT.hull, .26, .02, 0, pg); TI.petals.push(pg); } } // shield arrays
      for (const yy of [.16, -.16]) for (const dz of [.3, -.3]) eng(-4.1, yy, z0 + dz, .17, .45); greeb(-3.2, 3, .36, z0 - .3, z0 + .3, 22, [MT.dark, MT.trim, MT.hull]); }
    for (const [x, len] of [[2.7, .5], [.4, 2.4], [-2.2, .6]]) { box(len, .16, 2.4, MT.hull, x, .15, 0); box(len * .9, .04, 2.3, MT.trim, x, .25, 0); } // bridges between the hulls
    for (const s of [1, -1]) for (const x of [-1, 1.6]) { const st = cylX(.035, .035, 1.2, MT.dark, x, .4, s * .7); st.rotation.set(0, 0, Math.PI / 2); st.rotation.x = s * .5; }
    box(2.4, .22, 1.7, MT.hull, .3, .38, 0); const tiers = [[2.0, .34, 1.3, .66], [1.45, .32, .95, .99], [.85, .3, .6, 1.3]]; // the command citadel
    for (const [w, h, d2, y] of tiers) { box(w, h, d2, MT.hull, .3, y, 0); box(w * 1.02, .03, d2 * 1.02, MT.trim, .3, y + h / 2, 0); box(.02, h * .4, d2 * .8, MT.win, .3 + w / 2 + .005, y + .02, 0); }
    box(.5, .1, .5, MT.trim, .3, 1.5, 0); cylY(.03, .04, 1.1, MT.dark, .2, 2.05, 0); cylY(.015, .02, .7, MT.trim, .45, 1.85, .18); cylY(.015, .02, .7, MT.trim, .45, 1.85, -.18);
    const dish = add(mesh(new TH.SphereGeometry(.24, 16, 8, 0, TAU, 0, .9), MT.trim), -.2, 1.62, 0); dish.rotation.z = .9; TI.mats = [MT.glow, MT.win]; }
  else { ud.engCol = [0xd6ffe8, 0x3dff9a]; TI.arms = []; TI.ringG = [];
    add(mesh(new TH.SphereGeometry(.82, 32, 20), MT.glow)); TI.core = g.children[g.children.length - 1];
    for (const [a0, a1] of [[0, .95], [Math.PI - .95, .95]]) add(mesh(new TH.SphereGeometry(1.0, 32, 16, 0, TAU, a0, a1), MT.dark));
    add(mesh(new TH.CylinderGeometry(1.45, 1.55, .26, 6), MT.hull)); for (let j = 0; j < 12; j++) { const a = j / 12 * TAU; const p = box(.42, .07, .22, MT.trim, Math.cos(a) * 1.25, .17, Math.sin(a) * 1.25); p.rotation.y = -a; }
    const crescent = (w0, sweep, r0, r1, zoff) => { const L = [], R = [], N = 18; for (let i = 0; i <= N; i++) { const u = i / N, rr = r0 + (r1 - r0) * u, th = sweep * Math.pow(u, 1.5), x = rr * Math.cos(th), z = rr * Math.sin(th), nx = -Math.sin(th), nz = Math.cos(th), w = w0 * Math.pow(1 - u, .55) + .03; L.push([x + nx * w / 2, z + nz * w / 2 + zoff]); R.unshift([x - nx * w / 2, z - nz * w / 2 + zoff]); } return L.concat(R); };
    for (let i = 0; i < 6; i++) { const ag = new TH.Group(); ag.rotation.y = -i / 6 * TAU; g.add(ag); const blade = new TH.Group(); ag.add(blade);
      add(ext(crescent(.62, .95, 1.25, 3.7, 0), .2, MT.hull, .03), 0, -.1, 0, blade); add(ext(crescent(.16, .95, 1.4, 3.5, 0), .05, MT.glow, 0), 0, .12, 0, blade); add(ext(crescent(.3, -.5, 2.9, 4.2, 0), .12, MT.dark, .02), 0, -.06, 0, blade); // blade, emerald channel, the scythe hook
      for (const u of [.25, .45, .65]) { const rr = 1.25 + 2.45 * u, th = .95 * Math.pow(u, 1.5); const hb = box(.22, .08, .14, MT.dark, rr * Math.cos(th), .14, rr * Math.sin(th), blade); hb.rotation.y = -th; const hv = box(.16, .085, .05, MT.win, rr * Math.cos(th), .15, rr * Math.sin(th), blade); hv.rotation.y = -th; } // drone chambers
      const tr = 3.7, tt = .95; cylY(.09, .12, .3, MT.trim, tr * Math.cos(tt), 0, tr * Math.sin(tt), 10, blade); TI.arms.push({ g: ag, blade, a: -i / 6 * TAU, tip: [tr * Math.cos(tt), 0, tr * Math.sin(tt)] }); }
    for (let j = 0; j < 6; j++) { const a = j / 6 * TAU + .5; ud.eng.push([Math.cos(a) * 1.5, -.15, Math.sin(a) * 1.5, .12]); }
    for (const [R, tilt, n] of [[1.8, .38, 10], [2.1, -.32, 14]]) { const rg = new TH.Group(); rg.rotation.x = tilt; g.add(rg); const t0 = add(mesh(new TH.TorusGeometry(R, .045, 10, 80), MT.trim), 0, 0, 0, rg); t0.rotation.x = Math.PI / 2; for (let j = 0; j < n; j++) { const a = j / n * TAU; add(mesh(new TH.SphereGeometry(.05, 8, 6), MT.win), Math.cos(a) * R, 0, Math.sin(a) * R, rg); } TI.ringG.push(rg); }
    TI.mats = [MT.glow, MT.win]; }
  g.userData.titan = k; return g; }
/* the Titan inspection viewer: a live 3D view of the model with an orbit camera, five set views, and the signature-ability and arrival sequences */
function shTitan3D() { const k = sheet.k, D = SH[k], I = TITAN_INFO[k]; if (!D || !I) return ""; setTimeout(t3Start, 0);
  const li = a => a.map(x => `<li>${esc(x)}</li>`).join("");
  return `<div class="hd"><div><div class="chapter">Titan inspection</div><h2>${esc(D.n)}</h2><p class="note">${esc(I.tag)}</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
    <div class="t3w"><div class="t3slot" id="t3slot"></div><div class="t3cap" id="t3cap">Drag to turn · pinch to zoom</div></div>
    <div class="t3views">${[["front", "Front"], ["side", "Side"], ["top", "Top"], ["rear", "Rear"], ["under", "Under"], ["orbit", "360°"]].map(([v, l]) => `<button class="btn ghost sm" data-act="t3View" data-v="${v}">${l}</button>`).join("")}</div>
    <div class="t3acts"><button class="btn amber" data-act="t3Play" data-v="ab">⚡ ${esc(I.ab)}</button><button class="btn ghost" data-act="t3Play" data-v="arr">✦ Arrival</button></div>
    <div class="t3info"><p><b>Role:</b> ${esc(I.role)}</p><h4>Strengths</h4><ul>${li(I.adv)}</ul><h4>Weaknesses</h4><ul>${li(I.weak)}</ul><h4>Systems</h4><ul>${li(I.more)}</ul></div>`; }
function t3Start() { const slot = document.getElementById("t3slot"); if (!slot || !TH) return; let V = G.t3;
  if (V && V.k !== sheet.k) { t3Free(); V = null; }
  if (!V) { try { const cv = document.createElement("canvas"); const rd = new TH.WebGLRenderer({ canvas: cv, antialias: !WEAK, alpha: false }); rd.setPixelRatio(Math.min(devicePixelRatio || 1, IOS ? 1.5 : 2)); rd.toneMapping = TH.ACESFilmicToneMapping; rd.toneMappingExposure = 1.15; rd.outputEncoding = TH.sRGBEncoding; rd.setClearColor(0x03060c, 1);
      const sc = new TH.Scene(), pm = new TH.PMREMGenerator(rd), env = new TH.Scene(), skyT = texCanvas(512, 256, (x, W, H) => { const gr = x.createLinearGradient(0, 0, 0, H); gr.addColorStop(0, "#26405f"); gr.addColorStop(.5, "#0b1422"); gr.addColorStop(1, "#04060a"); x.fillStyle = gr; x.fillRect(0, 0, W, H); x.fillStyle = "#ffffff"; x.fillRect(W * .12, H * .16, W * .24, H * .07); x.fillStyle = "#9fdcff"; x.fillRect(W * .58, H * .24, W * .28, H * .05); x.fillStyle = "#ffcf9a"; x.fillRect(W * .38, H * .68, W * .2, H * .04); });
      env.add(new TH.Mesh(new TH.SphereGeometry(50, 32, 16), new TH.MeshBasicMaterial({ map: skyT, side: TH.BackSide }))); sc.environment = pm.fromScene(env, .01).texture; pm.dispose(); skyT.dispose();
      const key = new TH.DirectionalLight(0xfff1e0, 3.2); key.position.set(4, 6, 5); sc.add(key); const rim = new TH.DirectionalLight(sheet.k === "armageddon" ? 0xff7a4a : sheet.k === "sovereign" ? 0x8fd0ff : 0x7affc0, 3.6); rim.position.set(-6, 2.5, -5); sc.add(rim); sc.add(new TH.AmbientLight(0x334055, .6));
      const sp = new Float32Array(1500 * 3); for (let i = 0; i < 1500; i++) { const u = Math.random() * 2 - 1, a = Math.random() * TAU, R = 60 + Math.random() * 30; sp[i * 3] = Math.sqrt(1 - u * u) * Math.cos(a) * R; sp[i * 3 + 1] = u * R; sp[i * 3 + 2] = Math.sqrt(1 - u * u) * Math.sin(a) * R; }
      const sg = new TH.BufferGeometry(); sg.setAttribute("position", new TH.BufferAttribute(sp, 3)); sc.add(new TH.Points(sg, new TH.PointsMaterial({ color: 0xcfe4ff, size: .18, sizeAttenuation: true })));
      const ship = buildShip(sheet.k, shipMats(myAcc())); ship.traverse(o => { if (o.userData && o.userData.fx === 2) o.userData.fx = 0; }); sc.add(ship); const bb = new TH.Box3().setFromObject(ship), R0 = bb.getSize(new TH.Vector3()).length() / 2; ship.position.sub(bb.getCenter(new TH.Vector3()));
      const cam = new TH.PerspectiveCamera(38, 1, .05, 400); const gt = glowTex("255,255,255", 1), FX = new TH.Group(); sc.add(FX); ship.add(FX);
      const ec = ship.userData.engCol || [0xd8f2ff, 0x4f9fff], engs = (ship.userData.eng || []).map(([x, y, z, rr]) => { const s2 = new TH.Sprite(new TH.SpriteMaterial({ map: gt, color: ec[1], transparent: true, blending: TH.AdditiveBlending, depthWrite: false })); s2.position.set(x - rr * .6, y, z); s2.scale.setScalar(rr * 5); FX.add(s2); return s2; });
      V = G.t3 = { k: sheet.k, cv, rd, sc, ship, cam, R0, th: .8, ph: .35, dist: R0 * 2.6, tth: .8, tph: .35, tdist: R0 * 2.6, auto: 1, seq: null, engs, gt, FX, extra: [], t0: performance.now() };
      t3Wire(cv); } catch (e) { const c2 = document.getElementById("t3cap"); if (c2) c2.textContent = "3D view not available on this device."; return; } }
  if (V.cv.parentNode !== slot) { slot.textContent = ""; slot.appendChild(V.cv); } if (!V.raf) V.raf = requestAnimationFrame(t3Frame); }
function t3Free() { const V = G.t3; if (!V) return; cancelAnimationFrame(V.raf); for (const m of ((V.ship.userData.ti || {}).mats || [])) if (m.userData.c0) m.color.copy(m.userData.c0); for (const o of V.extra) { V.sc.remove(o); o.traverse && o.traverse(x => { if (x.geometry) x.geometry.dispose(); if (x.material && !x.material.userData.mn) x.material.dispose(); }); }
  V.sc.traverse(o => { if (o.geometry && !(o.material && o.material.userData && o.material.userData.mn)) o.geometry.dispose(); }); try { V.rd.dispose(); V.rd.forceContextLoss(); } catch (e) {} G.t3 = null; }
function t3Wire(cv) { const pts = new Map(); let pd = 0; cv.style.touchAction = "none";
  cv.addEventListener("pointerdown", e => { pts.set(e.pointerId, [e.clientX, e.clientY]); cv.setPointerCapture(e.pointerId); const V = G.t3; if (V) V.auto = 0; });
  cv.addEventListener("pointermove", e => { const V = G.t3, p = pts.get(e.pointerId); if (!V || !p) return; if (pts.size === 1) { V.tth -= (e.clientX - p[0]) * .01; V.tph = clamp(V.tph + (e.clientY - p[1]) * .008, -1.45, 1.45); } else if (pts.size === 2) { const L = [...pts.values()], d0 = Math.hypot(L[0][0] - L[1][0], L[0][1] - L[1][1]); pts.set(e.pointerId, [e.clientX, e.clientY]); const M2 = [...pts.values()], d1 = Math.hypot(M2[0][0] - M2[1][0], M2[0][1] - M2[1][1]); if (d0 > 0) V.tdist = clamp(V.tdist * d0 / d1, V.R0 * 1.3, V.R0 * 6); return; } pts.set(e.pointerId, [e.clientX, e.clientY]); });
  const up = e => pts.delete(e.pointerId); cv.addEventListener("pointerup", up); cv.addEventListener("pointercancel", up);
  cv.addEventListener("wheel", e => { const V = G.t3; if (!V) return; e.preventDefault(); V.tdist = clamp(V.tdist * (1 + Math.sign(e.deltaY) * .1), V.R0 * 1.3, V.R0 * 6); }, { passive: false }); }
function t3Frame(now) { const V = G.t3, slot = document.getElementById("t3slot"); if (!V) return; if (!slot) { t3Free(); return; } V.raf = requestAnimationFrame(t3Frame);
  const w = slot.clientWidth, h = slot.clientHeight; if (!w || !h || document.hidden) return; if (V.w !== w || V.h !== h) { V.w = w; V.h = h; V.rd.setSize(w, h, false); V.cam.aspect = w / h; V.cam.updateProjectionMatrix(); }
  const t = now - V.t0, ud = V.ship.userData, TI = ud.ti || {}; if (V.auto) V.tth += .0035;
  V.th += (V.tth - V.th) * .08; V.ph += (V.tph - V.ph) * .08; V.dist += (V.tdist - V.dist) * .08;
  const Q = V.seq, qt = Q ? (now - Q.t0) / 1000 : -1, ab = Q && Q.kind === "ab" ? qt : -1, ar = Q && Q.kind === "arr" ? qt : -1; let shake = 0;
  if (Q && qt > Q.dur) { if (V.lookT) V.lookT.set(0, 0, 0); for (const o of V.extra) { V.sc.remove(o); V.FX.remove(o); V.ship.remove(o); } V.extra = []; V.seq = null; V.ship.position.set(V.ship.userData.p0x || V.ship.position.x, V.ship.position.y, V.ship.position.z); V.ship.scale.setScalar(1); const c = document.getElementById("t3cap"); if (c) c.textContent = "Drag to turn · pinch to zoom"; }
  if (Q) { const I = TITAN_INFO[V.k], L = Q.kind === "ab" ? I.seq : [[0, I.arrive]]; let tx = ""; for (const [at, txt] of L) if (qt >= at) tx = txt; if (tx !== Q.cap) { Q.cap = tx; const c = document.getElementById("t3cap"); if (c) c.textContent = tx; } }
  const glowK = (m, k2) => { if (m && m.userData.c0) m.color.copy(m.userData.c0).multiplyScalar(k2); };
  if (V.k === "armageddon") { const chg = ab < 0 ? 0 : ab < 1.7 ? 0 : ab < 4.3 ? (ab - 1.7) / 2.6 : ab < 5.4 ? 1 : Math.max(0, 1 - (ab - 5.4) / .8), open = ab < 0 ? 0 : ab < .9 ? 0 : ab < 1.6 ? (ab - .9) / .7 : ab < 5.6 ? 1 : Math.max(0, 1 - (ab - 5.6) / .5);
    (TI.coils || []).forEach((c, i) => c.rotation.x = t * .0012 * (i % 2 ? -1 : 1) * (1 + 7 * chg)); (TI.rings || []).forEach((c, i) => c.rotation.x = -t * .0008 * (1 + 4 * chg) + i);
    (TI.plates || []).forEach(p => p.position.y = .36 + open * .32); if (TI.core) TI.core.scale.setScalar(.01 + (ab >= 3.4 && ab < 5.4 ? Math.min(1.6, (ab - 3.4) * 1.4) : 0));
    for (const m of TI.mats || []) glowK(m, 1 + chg * 3.5 + .15 * Math.sin(t * .004));
    if (ab >= 0 && !Q.cg) { const mk = (c, o) => { const sp = new TH.Sprite(new TH.SpriteMaterial({ map: V.gt, color: c, transparent: true, opacity: o, blending: TH.AdditiveBlending, depthWrite: false })); V.ship.add(sp); V.extra.push(sp); return sp; }; Q.cg = mk(0xff6a2a, 0); Q.cg.position.set(6.05, .48, 0); Q.hl = mk(0xff3a10, 0); Q.hl.position.set(-.5, .5, 0); Q.mf = mk(0xfff0d8, 0); Q.mf.position.set(6.1, .48, 0);
      const lg = new TH.BufferGeometry(); lg.setAttribute("position", new TH.BufferAttribute(new Float32Array(16 * 6), 3)); Q.arcs = new TH.LineSegments(lg, new TH.LineBasicMaterial({ color: 0xffd0a0, transparent: true, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); V.ship.add(Q.arcs); V.extra.push(Q.arcs); }
    if (Q && Q.cg) { const cg = ab >= 3.4 && ab < 4.4 ? (ab - 3.4) : ab >= 4.4 && ab < 5.4 ? 1 : 0; Q.cg.scale.setScalar(.4 + cg * 3.6); Q.cg.material.opacity = cg * .95; Q.hl.scale.setScalar(V.R0 * 1.6); Q.hl.material.opacity = chg * .35;
      const arcOn = ab >= 2.6 && ab < 4.4, P2 = Q.arcs.geometry.attributes.position; Q.arcs.visible = arcOn; if (arcOn) { for (let i = 0; i < 16; i++) { const x0 = 2.6 + Math.floor(Math.random() * 4) * .7, a1 = Math.random() * TAU, a2 = Math.random() * TAU; P2.setXYZ(i * 2, x0, .48 + Math.cos(a1) * .44, Math.sin(a1) * .44); P2.setXYZ(i * 2 + 1, x0 + .7, .48 + Math.cos(a2) * .44, Math.sin(a2) * .44); } P2.needsUpdate = true; }
      Q.mf.scale.setScalar(ab >= 4.3 && ab < 5.4 ? 3 + 2 * Math.random() : .01); Q.mf.material.opacity = ab >= 4.3 && ab < 5.4 ? 1 : 0; }
    if (ab >= 4.3 && ab < 5.4) { if (!Q.beam) { const bm = new TH.Mesh(new TH.CylinderGeometry(.28, .28, 1, 20, 1, true), new TH.MeshBasicMaterial({ color: 0xfff4e0, transparent: true, opacity: 1, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); bm.rotation.z = Math.PI / 2; V.ship.add(bm); V.extra.push(bm); Q.beam = bm;
        const bo = new TH.Mesh(new TH.CylinderGeometry(.75, .75, 1, 24, 1, true), new TH.MeshBasicMaterial({ color: 0xff4a10, transparent: true, opacity: .55, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); bo.rotation.z = Math.PI / 2; V.ship.add(bo); V.extra.push(bo); Q.bo = bo;
        const sw = new TH.Mesh(new TH.TorusGeometry(1, .05, 8, 64), new TH.MeshBasicMaterial({ color: 0xffd0a0, transparent: true, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); sw.rotation.y = Math.PI / 2; V.ship.add(sw); V.extra.push(sw); Q.sw = sw; }
      const u = (ab - 4.3) / 1.1, Lb = 60, fl = 1 - Math.max(0, u - .7) / .3, wb = 1 + .35 * Math.sin(t * .06); Q.beam.scale.set(wb, Lb, wb); Q.beam.position.set(6.05 + Lb / 2, .48, 0); Q.beam.material.opacity = fl; Q.bo.scale.set(wb, Lb, wb); Q.bo.position.copy(Q.beam.position); Q.bo.material.opacity = .55 * fl; Q.sw.position.set(6.2 + u * 8, .48, 0); Q.sw.scale.setScalar(.6 + u * 9); Q.sw.material.opacity = 1 - u; shake = (1 - u) * .05; }
    else if (Q && Q.beam) { Q.beam.visible = Q.bo.visible = Q.sw.visible = false; }
    if (ar >= 0) { if (!Q.rift) { const rf = new TH.Sprite(new TH.SpriteMaterial({ map: V.gt, color: 0xff2a10, transparent: true, blending: TH.AdditiveBlending, depthWrite: false })); V.sc.add(rf); V.extra.push(rf); Q.rift = rf; V.ship.userData.p0x = V.ship.position.x; }
      const u = clamp(ar / 4, 0, 1), e = 1 - Math.pow(1 - u, 3); Q.rift.position.set(-6, 0, 0); Q.rift.scale.set(9 * Math.min(1, ar * 1.5), 14 * Math.min(1, ar * 1.5), 1); Q.rift.material.opacity = ar < 4 ? .9 : Math.max(0, 1 - (ar - 4) / 1.5); V.ship.position.x = V.ship.userData.p0x - 14 * (1 - e); for (const m of TI.mats || []) glowK(m, 1 + 2 * (1 - u)); } }
  else if (V.k === "sovereign") { const wave = ab >= 0 && ab < 1.5 ? ab / 1.5 : -1, open = ab < 0 ? 0 : ab < .9 ? 0 : ab < 1.8 ? (ab - .9) / .9 : ab < 5.6 ? 1 : Math.max(0, 1 - (ab - 5.6) / .5), unf = ab < 2.9 ? 0 : Math.min(1, (ab - 2.9) / .7);
    (TI.doors || []).forEach(dd => dd.m.position.x = dd.x0 + dd.dx * open * .55); (TI.lights || []).forEach((m, i) => { m.visible = open > 0 || wave >= 0 ? (wave < 0 || i / 26 < wave + .1) : true; });
    for (const m of TI.mats || []) glowK(m, 1 + open * 1.6 + (wave >= 0 ? 1.2 : 0)); (TI.petals || []).forEach((p, i) => { p.rotation.z = -unf * .9; });
    if (ab >= 1.8 && !Q.wing) { Q.wing = []; const fm = new TH.MeshStandardMaterial({ color: 0xeef3fa, metalness: .8, roughness: .3, emissive: 0x3a8cff, emissiveIntensity: .4 }); for (let i = 0; i < 18; i++) { const f = new TH.Mesh(new TH.ConeGeometry(.08, .32, 4), fm); f.rotation.z = -Math.PI / 2; V.ship.add(f); V.extra.push(f); Q.wing.push({ f, s: i % 2 ? 1 : -1, d: Math.floor(i / 2) * .12, row: i % 6 }); } }
    if (Q && Q.wing) for (const W2 of Q.wing) { const u = clamp((ab - 1.8 - W2.d) / 1.6, 0, 1), e = u * u * (3 - 2 * u), fx0 = 2.1, fz0 = W2.s * 2.2, tx = 6 + (W2.row % 3) * .7, tz = W2.s * (.6 + Math.floor(W2.row / 3) * .55) * 1.4; W2.f.visible = u > 0; W2.f.position.set(fx0 + (tx - fx0) * e + Math.sin(u * 3) * .2 * (1 - e), .1 + Math.sin(e * Math.PI) * .6, fz0 + (tz - fz0) * e); }
    if (ab >= 3.6 && !Q.field) { const fd = new TH.Mesh(new TH.IcosahedronGeometry(1, 3), new TH.MeshBasicMaterial({ color: 0x3a9cff, transparent: true, opacity: .14, wireframe: true, blending: TH.AdditiveBlending, depthWrite: false })); V.sc.add(fd); V.extra.push(fd); Q.field = fd; }
    if (Q && Q.field) { const u = clamp((ab - 3.6) / 1, 0, 1); Q.field.scale.setScalar(V.R0 * (.2 + 1.1 * u)); Q.field.rotation.y = t * .0003; Q.field.material.opacity = .22 * (ab > 5.5 ? Math.max(0, 1 - (ab - 5.5) / .5) : 1); }
    if (ar >= 0) { if (!Q.esc) { Q.esc = []; V.ship.userData.p0x = V.ship.position.x; const em = new TH.MeshStandardMaterial({ color: 0xdfe6ee, metalness: .8, roughness: .3, emissive: 0x2a6cff, emissiveIntensity: .5 }); for (let i = 0; i < 12; i++) { const e2 = new TH.Mesh(new TH.ConeGeometry(.16, .7, 5), em); e2.rotation.z = -Math.PI / 2; V.sc.add(e2); V.extra.push(e2); Q.esc.push({ m: e2, z: (i % 2 ? 1 : -1) * (3.2 + Math.floor(i / 2) % 3 * 1.1), x: -1.5 - Math.floor(i / 6) * 2.2 + (i % 3) * .6, y: (i % 3 - 1) * .7 }); } }
      const u = clamp(ar / 4.5, 0, 1), e = 1 - Math.pow(1 - u, 3), off = -22 * (1 - e); V.ship.position.x = V.ship.userData.p0x + off; for (const E2 of Q.esc) E2.m.position.set(E2.x + off * 1.05, E2.y, E2.z); for (const m of TI.mats || []) glowK(m, 1.6 - .6 * u); } }
  else { const arms = TI.arms || [], pulse = ab >= 0 && ab < 6 ? 1 : 0, spin = ab >= .9 && ab < 2.0 ? 1 : 0, lock = ab >= 2.0 && ab < 6 ? 1 : 0;
    arms.forEach((A, i) => { const indep = spin ? Math.sin((ab - .9) * 3 + i) * .5 * Math.sin(Math.PI * (ab - .9) / 1.1) : 0; A.blade.rotation.y = indep + (lock ? .18 * Math.sin(Math.min(1, (ab - 2) / .6) * Math.PI / 2) : 0); A.blade.rotation.z = lock ? -.12 : 0; });
    V.ship.rotation.y = t * .00012 * (1 + 2 * pulse); (TI.ringG || []).forEach((rg, i) => rg.rotation.y = t * .0009 * (i ? -1 : 1) * (1 + 3 * pulse));
    if (TI.core) TI.core.scale.setScalar(1 + .08 * Math.sin(t * (pulse ? .02 : .004))); for (const m of TI.mats || []) glowK(m, 1 + pulse * (1.2 + .8 * Math.sin(t * .02)));
    if (ab >= 2.8 && !Q.links) { Q.links = []; const lm = [new TH.MeshBasicMaterial({ color: 0x3dff9a, transparent: true, opacity: .8, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false }), new TH.MeshBasicMaterial({ color: 0xb06bff, transparent: true, opacity: .8, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })];
      for (let i = 0; i < 6; i++) { const l = new TH.Mesh(new TH.CylinderGeometry(.06, .06, 1, 8), lm[i % 2]); V.ship.add(l); V.extra.push(l); Q.links.push(l); } }
    if (Q && Q.links) { const tips = arms.map(A => { const v = new TH.Vector3(...A.tip); A.blade.localToWorld(v); V.ship.worldToLocal(v); return v; }); Q.links.forEach((l, i) => { const a = tips[i], b2 = tips[(i + 1) % 6]; l.position.copy(a).add(b2).multiplyScalar(.5); l.scale.set(1, a.distanceTo(b2), 1); l.quaternion.setFromUnitVectors(new TH.Vector3(0, 1, 0), b2.clone().sub(a).normalize()); l.visible = ab < 6; }); }
    if (ab >= 4.0 && !Q.dr) { Q.dr = []; const dm = [new TH.MeshBasicMaterial({ color: 0x9affc8, toneMapped: false }), new TH.MeshBasicMaterial({ color: 0xd0a0ff, toneMapped: false })]; for (let i = 0; i < 48; i++) { const dn = new TH.Mesh(new TH.TetrahedronGeometry(.12), dm[i % 2]); const gw = new TH.Sprite(new TH.SpriteMaterial({ map: V.gt, color: i % 2 ? 0xb06bff : 0x3dff9a, transparent: true, opacity: .8, blending: TH.AdditiveBlending, depthWrite: false })); gw.scale.setScalar(.5); dn.add(gw); V.ship.add(dn); V.extra.push(dn); Q.dr.push({ m: dn, arm: i % 6, ph: Math.random() * TAU, sp: .6 + Math.random() * .8, r: 1 + Math.random() * 3 }); } }
    if (Q && Q.dr) for (const D2 of Q.dr) { const u = clamp((ab - 4) / 2, 0, 1), A = arms[D2.arm], base = A.a, ang = base + D2.ph * .3 + u * D2.sp * 3, R = 2 + u * D2.r * 1.6; D2.m.position.set(Math.cos(-ang) * R, Math.sin(D2.ph + u * 6) * .6 * u, Math.sin(-ang) * R); D2.m.rotation.set(t * .01, t * .013, 0); }
    if (ar >= 0) { if (!Q.dist) { const ds = new TH.Sprite(new TH.SpriteMaterial({ map: V.gt, color: 0x2aff7a, transparent: true, blending: TH.AdditiveBlending, depthWrite: false })); V.sc.add(ds); V.extra.push(ds); Q.dist = ds; }
      const u = clamp(ar / 4, 0, 1), e = 1 - Math.pow(1 - u, 3); Q.dist.scale.setScalar(V.R0 * (3.5 - 1.5 * e)); Q.dist.material.opacity = .85 * (1 - Math.max(0, (ar - 3.5) / 1.5)); V.ship.scale.setScalar(.3 + .7 * e); arms.forEach(A => { A.blade.rotation.y = -(1 - e) * 1.3; }); } }
  for (const s2 of V.engs) s2.material.opacity = .65 + .35 * Math.sin(t * .02 + s2.position.z * 3);
  const cp = V.cam.position; cp.set(Math.cos(V.ph) * Math.cos(V.th) * V.dist, Math.sin(V.ph) * V.dist, Math.cos(V.ph) * Math.sin(V.th) * V.dist); if (shake) cp.add(new TH.Vector3((Math.random() - .5) * shake * V.dist, (Math.random() - .5) * shake * V.dist, 0)); V.look = V.look || new TH.Vector3(); V.look.lerp(V.lookT || (V.lookT = new TH.Vector3()), .06); cp.add(V.look); V.cam.lookAt(V.look);
  V.rd.render(V.sc, V.cam); }
'''
rep('function buildShip(k, M) {', MODEL + 'function buildShip(k, M) {')
rep('  if (k === "flagship") return flagshipModel(g, M, r);', '  if (k === "flagship") return flagshipModel(g, M, r);\n  if (TITAN_INFO[k]) return titanModel(k, g); /* v556 */')
rep('const n = rev.get(o.material) || "hull"', 'const n = rev.get(o.material) || (o.material && o.material.userData && o.material.userData.mn) || "hull"')
rep(': kind === "a" ? [0xd8ff9a, 0x7aff3a] : [0x9fdcff, 0x4f9fff];', ': ship.userData.engCol ? ship.userData.engCol : kind === "a" ? [0xd8ff9a, 0x7aff3a] : [0x9fdcff, 0x4f9fff];')
rep('if (k === "eclipse" && view === "side") ship.rotation.x = .42;', 'if (k === "eclipse" && view === "side") ship.rotation.x = .42; if (view === "side" && TITAN_INFO[k]) ship.rotation.x = k === "harbinger" ? 1.0 : .38; /* v556 */')
# the viewer: sheet, a button on the Titans' cards, actions
rep('profile: shProfile, wardrobe: shWardrobe, vault: shVault', 'profile: shProfile, wardrobe: shWardrobe, vault: shVault, titan3d: shTitan3D')
rep('mid = `<div class="dstat"><div class="dp">', 'mid = `${kind === "s" && TITAN_INFO[k] ? `<button class="btn amber wide t3open" data-act="t3Open" data-k="${k}">◎ Inspect in 3D · ${esc(TITAN_INFO[k].ab)}</button>` : ""}<div class="dstat"><div class="dp">')
rep('  vault: () => {', '''  t3Open: d => { if (TITAN_INFO[d.k]) openSheet({ type: "titan3d", k: d.k }); }, /* v556 */
  t3View: d => { const V = G.t3; if (!V) return; V.auto = d.v === "orbit" ? 1 : 0; const P0 = { front: [0, .12, 2.3], side: [Math.PI / 2, .12, 2.6], top: [Math.PI / 2, 1.42, 2.6], rear: [Math.PI, .12, 2.3], under: [Math.PI / 2, -1.35, 2.6], orbit: [V.tth, .35, 2.6] }[d.v]; if (!P0) return; let th = P0[0]; while (th - V.tth > Math.PI) th -= TAU; while (V.tth - th > Math.PI) th += TAU; V.tth = th; V.tph = P0[1]; V.tdist = V.R0 * P0[2]; },
  t3Play: d => { const V = G.t3; if (!V) return; for (const o of V.extra) { V.sc.remove(o); V.ship.remove(o); } V.extra = []; V.ship.scale.setScalar(1); if (V.ship.userData.p0x != null) V.ship.position.x = V.ship.userData.p0x; V.seq = { kind: d.v === "arr" ? "arr" : "ab", t0: performance.now(), dur: d.v === "arr" ? 5.5 : 6.4 }; V.auto = 0; const big = V.k === "armageddon" && d.v !== "arr"; V.tth = d.v === "arr" ? Math.PI * .7 : big ? Math.PI * .5 : Math.PI * .35; V.tph = big ? .22 : .3; V.tdist = V.R0 * (d.v === "arr" ? 3.2 : big ? 3.4 : 2.7); if (V.lookT) V.lookT.set(big ? V.R0 * .55 : 0, 0, 0); try { d.v === "arr" ? SFX.fanfare(true) : SFX.charge(); } catch (e) {} },
  vault: () => {''')
css = '''
/* v556 the Titan inspection viewer */
.t3open{margin:0 0 8px}
.t3w{position:relative;margin:4px 0 8px;border-radius:14px;overflow:hidden;border:1px solid rgba(122,244,255,.35);background:#03060c}
.t3slot{width:100%;height:min(92vw,58vh,560px)}.t3slot canvas{display:block;width:100%;height:100%}
.t3cap{position:absolute;left:0;right:0;bottom:0;padding:10px 12px;font-size:13px;color:#e9f6ff;background:linear-gradient(0deg,rgba(3,6,12,.92),rgba(3,6,12,0));text-shadow:0 0 8px #000;pointer-events:none}
.t3views{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px}.t3views .btn{flex:1 1 auto}
.t3acts{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px}
.t3info{font-size:13px}.t3info h4{margin:10px 0 4px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#7af4ff}.t3info ul{margin:0;padding-left:18px}.t3info li{margin:2px 0}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 555\b", "GAME_V = 556", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
