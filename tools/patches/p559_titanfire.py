# v559 four firing animations for each Titan (owner: "each of these new titans should have 4 different unique firing animations").
# Armageddon: Worldbreaker Cannon (charge + beam), Heavy Plasma Broadsides (main guns: three glowing shells from the flanks), Siege Missile
#   Barrage (second battery), Fortress Point Defence (streams of red tracers at small craft).
# Sovereign Ark: Precision Lance Batteries (main guns: twin white-blue lances), Command Missiles (second battery, from the flanks),
#   Carrier Strike Wings (fighters), Sovereign Defence Grid (cyan flak at small craft).
# Eclipse Harbinger: Eclipse Pulse (main guns: an emerald ring that flies to its target), Neural Drone Swarm, violet plasma (second
#   battery), arm-tip lasers (six beams converging from its arms on small craft).
# Visual only: the volleys and their damage are unchanged; the last shot of each volley still carries its hits.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('if (v.ab && titanFx(b, v)) return; /* v556 */', 'if ((v.ab || (b.Q[v.s] && TITAN_LEN[b.Q[v.s].k])) && titanFx(b, v)) return; /* v556, v559 */')
rep('  sovereign:     ["mass", 3, "#e8f4ff", .18, {}],              // precision lance batteries', '  sovereign:     ["missile", 6, "#cfe8ff", .2, { flank: 1 }], // v559 command missiles (the lances are its main guns)')
rep('''  return false; }
function titanBeamDraw(''', '''  /* v559 the Titans' own main guns and point defence */
  const lo = b.lowFx, main = v.wk === (CPROF[q.k] || [])[1], pd = v.wk === "flak"; if (!main && !pd) return false; const hid = { v, last: true, first: true, n: 1, mis: false, ic: false, side, off: 0, hv: 0, sz, j: 0, hide: 1 };
  if (main) try { capSecond(b, v, q, side, sz, lo); } catch (e) {}
  if (q.k === "armageddon" && main) { const n = lo ? 2 : 3; for (let j = 0; j < n; j++) { const t0 = v.t + j * .09; b.fx.push({ t0, t1: t0 + TRAVEL.plasma * 1.1, v, last: j === n - 1, first: j === 0, n, mis: false, ic: false, side, off: (j - (n - 1) / 2) * .45, hv: 1, sz, j: 300 + j, bs: j % 2 ? 1 : -1, col: j === 1 ? "#ffd070" : "#ff6a2a" }); }
    (b.muz = b.muz || []).push({ s: v.s, t: v.t, big: true, col: "#ff7a3a" }); return true; }
  if (q.k === "armageddon" && pd) { const n = lo ? 3 : 8; for (let j = 0; j < n; j++) { const t0 = v.t + j * .035; b.fx.push({ t0, t1: t0 + .3, v, last: j === n - 1, first: j === 0, n, mis: false, ic: false, side, off: (Math.random() - .5) * .9, hv: 0, sz: 0, j: 400 + j, col: j % 3 ? "#ff4a2a" : "#ffd0a0" }); } return true; }
  if (q.k === "sovereign" && main) { b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: "l", charge: 0, life: .45 }); b.fx.push(Object.assign({}, hid, { t0: v.t, t1: v.t + .1 })); return true; }
  if (q.k === "sovereign" && pd) { const n = lo ? 3 : 6; for (let j = 0; j < n; j++) { const t0 = v.t + j * .05; b.fx.push({ t0, t1: t0 + .28, v, last: j === n - 1, first: j === 0, n, mis: false, ic: false, side, off: (j / (n - 1) - .5) * 1.2, hv: 0, sz: 0, j: 500 + j, col: j % 2 ? "#7af4ff" : "#ffffff" }); } return true; }
  if (q.k === "harbinger" && main) { b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: "p", charge: 0, life: .7 }); b.fx.push(Object.assign({}, hid, { t0: v.t, t1: v.t + .6 })); return true; }
  if (q.k === "harbinger" && pd) { b.beams.push({ t0: v.t, s: v.s, e: v.e, side, ti: "t", charge: 0, life: .4 }); b.fx.push(Object.assign({}, hid, { t0: v.t, t1: v.t + .15 })); return true; }
  return false; }
function titanBeamDraw(''')
rep('''  if (!E0) { ctx.restore(); return; } const k = age / m.life, wv = Lg * .11''', '''  if (m.ti === "l" || m.ti === "p" || m.ti === "t") { if (!E0) { ctx.restore(); return; } const k = clamp(age / m.life, 0, 1); /* v559 */
    if (m.ti === "l") { const ox = S0.x + fc * Lg * .3; for (const dy of [-Lg * .07, Lg * .07]) { const a = (1 - k) * (k < .1 ? k / .1 : 1); ctx.globalAlpha = a * .5; ctx.strokeStyle = "#5fb8ff"; ctx.lineWidth = 7 * d; ctx.beginPath(); ctx.moveTo(ox, S0.y + dy); ctx.lineTo(E0.x, E0.y + dy * .3); ctx.stroke(); ctx.globalAlpha = a; ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2 * d; ctx.beginPath(); ctx.moveTo(ox, S0.y + dy); ctx.lineTo(E0.x, E0.y + dy * .3); ctx.stroke(); }
      ctx.globalAlpha = 1 - k; const fr = Lg * .12; ctx.drawImage(glowSprite("#9fdcff"), E0.x - fr, E0.y - fr, fr * 2, fr * 2); }
    else if (m.ti === "p") { const x = S0.x + (E0.x - S0.x) * k, y = S0.y + (E0.y - S0.y) * k, rr = Lg * (.08 + .14 * k); ctx.globalAlpha = 1 - k * .5; ctx.strokeStyle = "#3dff9a"; ctx.lineWidth = 4 * d; ctx.beginPath(); ctx.ellipse(x, y, rr, rr * .6, 0, 0, TAU); ctx.stroke(); ctx.strokeStyle = "#b06bff"; ctx.lineWidth = 2 * d; ctx.beginPath(); ctx.ellipse(x, y, rr * .7, rr * .42, 0, 0, TAU); ctx.stroke();
      ctx.drawImage(glowSprite("#3dff9a"), x - rr, y - rr, rr * 2, rr * 2); if (k > .85) { const u = (k - .85) / .15, br = Lg * (.2 + .5 * u); ctx.globalAlpha = 1 - u; ctx.drawImage(glowSprite("#9affc8"), E0.x - br, E0.y - br, br * 2, br * 2); } }
    else { for (let i = 0; i < 6; i++) { const a = i / 6 * TAU + T * 2, ox = S0.x + Math.cos(a) * Lg * .32, oy = S0.y + Math.sin(a) * Lg * .2; ctx.globalAlpha = (1 - k) * (.6 + .4 * Math.random()); ctx.strokeStyle = i % 2 ? "#b06bff" : "#3dff9a"; ctx.lineWidth = 2.2 * d; ctx.beginPath(); ctx.moveTo(ox, oy); ctx.lineTo(E0.x, E0.y); ctx.stroke(); }
      ctx.globalAlpha = 1 - k; const fr = Lg * .1; ctx.drawImage(glowSprite("#d0a0ff"), E0.x - fr, E0.y - fr, fr * 2, fr * 2); }
    ctx.restore(); return; }
  if (!E0) { ctx.restore(); return; } const k = age / m.life, wv = Lg * .11''')
rep('more: ["Siege Missile Barrage", "Heavy Plasma Broadsides", "Fortress Point Defence"],', 'more: ["Worldbreaker Cannon: charge, beam and shockwave", "Heavy Plasma Broadsides: glowing shells from both flanks", "Siege Missile Barrage", "Fortress Point Defence: red tracer streams"],')
rep('more: ["Sovereign Defence Grid", "Precision Lance Batteries", "Fleet Command Uplink"],', 'more: ["Precision Lance Batteries: twin white-blue lances", "Command Missiles from both flanks", "Carrier Strike Wings", "Sovereign Defence Grid: cyan flak", "Fleet Command Uplink"],')
rep('more: ["Eclipse Energy Pulse", "Adaptive Alien Barrier", "Collective Targeting Network"],', 'more: ["Eclipse Pulse: an emerald ring that flies to its target", "Neural Drone Swarm", "Violet plasma batteries", "Arm-tip lasers converging from all six arms", "Adaptive Alien Barrier"],')
s2 = re.sub(r"GAME_V = 558\b", "GAME_V = 559", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
