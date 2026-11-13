# v517 flagship set looks (owner: crafting should show; "like a ballistic missile"). Stats are unchanged: the set you wear most decides
# how your flagship looks. 2 pieces: its engines, seams, halo and tracers glow in the set's colour (map and battle replay). 4 pieces:
# a pulsing aura round it in battle and a brighter halo on the map. The full set (6 pieces, 4 for the mythic boss sets): a signature
# weapon in every battle replay, a ballistic missile volley (Conqueror, Sovereign), a lance (Harvester, Scientist, Void Hunter,
# Celestial, Gorgon) or a shockwave pulse (Guardian, Architect, Abyssal). Other players see yours: the look is published as tech.fsl.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)

rep('const fsEquipped = f => Object.values(f.eq).map(id => f.inv.find(x => x.id === id)).filter(Boolean);', '''const fsEquipped = f => Object.values(f.eq).map(id => f.inv.find(x => x.id === id)).filter(Boolean);
/* v517 set looks: [colour, signature weapon, its name] */
const FS_LOOK = { conq: ["#ff4a3a", "missiles", "Ballistic missile volley"], guard: ["#4ab8ff", "pulse", "Aegis shockwave"], harv: ["#6aff8a", "lance", "Mining lance"], arch: ["#ffcf4a", "pulse", "Foundry shockwave"],
  sci: ["#4af0ff", "lance", "Ion lance"], hunt: ["#b06aff", "lance", "Void lance"], celes: ["#fff0b0", "lance", "Annihilation lance"], sov: ["#ff9a3a", "missiles", "Warform missile swarm"], abyss: ["#a04aff", "pulse", "Abyssal shockwave"], gorgon: ["#7aff9a", "lance", "Petrifying gaze"] };
const fsSetMax = k => FS_SETS[k][1][FS_SETS[k][1].length - 1][0];
function fsLookOf(f) { if (!f || !f.eq || !f.inv) return null; const c = fsSetCounts(fsEquipped(f)); let best = null;
  for (const k in c) { if (!FS_LOOK[k] || !FS_SETS[k]) continue; const n = c[k], t = n >= fsSetMax(k) ? 3 : n >= 4 ? 2 : n >= 2 ? 1 : 0; if (t && (!best || t > best.t || (t === best.t && n > best.n))) best = { s: k, n, t }; } return best; }
const fsLookCode = l => l ? l.s + l.t : "";
function lookFromCode(c) { const m = /^([a-z]+)([123])$/.exec(String(c || "")); if (!m || !FS_LOOK[m[1]]) return null; const [hex, sig, nm] = FS_LOOK[m[1]], h = parseInt(hex.slice(1), 16);
  return { s: m[1], t: +m[2], col: h, hex, rgba: `rgba(${h >> 16},${h >> 8 & 255},${h & 255},1)`, sig, nm }; }
function uidLook(u) { try { if (!u) return null; if (u === G.me) return S && S.fs && fsBuilt() ? lookFromCode(fsLookCode(fsLookOf(fsOf()))) : null; const p = G.players[u]; return p && p.tech ? lookFromCode(p.tech.fsl) : null; } catch (e) { return null; } }''')
# published, and read back from other players
rep('fl: fsBuilt() ? (acadFlag() ? 2 : 1) : 0 }', 'fl: fsBuilt() ? (acadFlag() ? 2 : 1) : 0, fsl: fsBuilt() ? fsLookCode(fsLookOf(fsOf())) : "" }')
rep('fl: (v.tech || {}).fl == null ? null : okInt((v.tech || {}).fl) },', 'fl: (v.tech || {}).fl == null ? null : okInt((v.tech || {}).fl), fsl: typeof (v.tech || {}).fsl === "string" ? v.tech.fsl.slice(0, 10) : "" },')

# --- the battle replay
rep('const g = groups.get(u) || { f, idx: [], w: 0 };', 'const g = groups.get(u) || { f, u, idx: [], w: 0 };')
rep('if (f) L = [{ f, idx: Q.map((q, i) => q.side === sd ? i : -1).filter(i => i >= 0) }]; }', 'if (f) L = [{ f, u: u || (sd === mineS ? G.me : null), idx: Q.map((q, i) => q.side === sd ? i : -1).filter(i => i >= 0) }]; }')
rep('out[sd] = L.map(e => ({ f: e.f, idx: e.idx, acc: facAcc(e.f), col: FLAG_GLOW[e.f], rgba: `rgba(${FLAG_GLOW[e.f] >> 16},${FLAG_GLOW[e.f] >> 8 & 255},${FLAG_GLOW[e.f] & 255},1)` })); }',
    'out[sd] = L.map(e => { const lk = f4 ? null : uidLook(e.u), col = lk ? lk.col : FLAG_GLOW[e.f]; return { f: e.f, u: e.u, look: lk, idx: e.idx, acc: facAcc(e.f), col, rgba: `rgba(${col >> 16},${col >> 8 & 255},${col & 255},1)` }; }); } /* v517 a set look recolours its flagship */')
rep('    ctx.translate(x, y); ctx.scale(fsc, 1); ctx.rotate(Math.sin(t * .0007 + e.col) * .012); ctx.drawImage(art, -L0, -L0 / 2, L0 * 2, L0);',
    '''    if (e.look && e.look.t >= 2 && !lo) { ctx.globalCompositeOperation = "lighter"; ctx.strokeStyle = e.rgba; ctx.lineWidth = 2.2 * d; /* v517 the 4-piece aura: two rings breathing round the hull */
      for (let j = 0; j < 2; j++) { const ph = ((t * .0006 + j * .5) % 1); ctx.globalAlpha = (1 - ph) * .55 * fade; ctx.beginPath(); ctx.ellipse(x, y, L0 * (.95 + ph * .45), L0 * (.42 + ph * .22), 0, 0, TAU); ctx.stroke(); }
      ctx.globalAlpha = (.22 + .12 * pul) * fade; ctx.drawImage(glowSprite(e.rgba), x - L0 * 1.6, y - L0 * .8, L0 * 3.2, L0 * 1.6); ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = fade; }
    ctx.translate(x, y); ctx.scale(fsc, 1); ctx.rotate(Math.sin(t * .0007 + e.col) * .012); ctx.drawImage(art, -L0, -L0 / 2, L0 * 2, L0);''')
rep('''shots.splice(0, shots.length - 150); } }
  b.fgS = shots; }''', '''shots.splice(0, shots.length - 150); }
    /* v517 the full set's signature weapon, every few seconds: a missile volley arcing onto the enemy, a lance, or a shockwave */
    if (e.look && e.look.t >= 3 && e.dead == null && !b.paused && !b.done && b.intro <= 0 && foes.length && t >= (e.sigT || (e.sigT = t + 1400))) { const lk = e.look, sg = b.sig || (b.sig = []), pick = () => foes[(Math.random() * foes.length) | 0];
      e.sigT = t + (lk.sig === "missiles" ? 3600 : 3000);
      if (lk.sig === "missiles") for (let j = 0; j < 6; j++) sg.push({ k: "m", x0: x + face * L0 * (.25 - j * .1), y0: y - L0 * .12, i: pick(), t0: t + j * 110, life: 1000, up: L0 * (.6 + Math.random() * .7), rgba: lk.rgba, ox: (Math.random() - .5) * L0 * .3, oy: (Math.random() - .5) * L0 * .1 });
      else if (lk.sig === "lance") sg.push({ k: "l", x0: x + face * L0 * .9, y0: y, i: pick(), t0: t, life: 750, rgba: lk.rgba });
      else { sg.push({ k: "p", x0: x, y0: y, t0: t, life: 850, R: L0 * 2.4, rgba: lk.rgba }); for (let j = 0; j < 3; j++) sg.push({ k: "h", i: pick(), t0: t + 260 + j * 90, life: 300, rgba: lk.rgba }); }
      if (sg.length > 80) sg.splice(0, sg.length - 80); } }
  b.fgS = shots; }''')
rep('''  ctx.restore(); ctx.globalAlpha = 1; }
/* v66: start baking''', '''  if (b.sig && b.sig.length) { b.sig = b.sig.filter(o => t - o.t0 < o.life + 60); ctx.globalCompositeOperation = "lighter";
    for (const o of b.sig) { const k = (t - o.t0) / o.life; if (k < 0) continue; const s = o.i != null ? scr[o.i] : null;
      if (o.k === "m") { if (!s) continue; const tx = s.x + o.ox, ty = s.y + o.oy, cx = (o.x0 + tx) / 2, cy = Math.min(o.y0, ty) - o.up, Pq = u => [(1 - u) * (1 - u) * o.x0 + 2 * (1 - u) * u * cx + u * u * tx, (1 - u) * (1 - u) * o.y0 + 2 * (1 - u) * u * cy + u * u * ty];
        if (k >= 1) { if (!o.hit) { o.hit = 1; b.booms.push({ x: tx, y: ty, t, big: 0 }); } continue; } const u = Math.pow(k, 1.25), a = Pq(Math.max(0, u - .09)), h = Pq(u);
        ctx.globalAlpha = .7; ctx.strokeStyle = o.rgba; ctx.lineWidth = 3.2 * d; ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(h[0], h[1]); ctx.stroke(); ctx.globalAlpha = 1; ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 1.1 * d; ctx.stroke();
        const hr = 7 * d; ctx.drawImage(starSprite(o.rgba), h[0] - hr, h[1] - hr, hr * 2, hr * 2); }
      else if (o.k === "l") { if (!s || k > 1) continue; if (!o.hit) { o.hit = 1; b.booms.push({ x: s.x, y: s.y, t, big: 1 }); } const w = (1 - k) * 8 * d + 1;
        ctx.globalAlpha = .75 * (1 - k * .6); ctx.strokeStyle = o.rgba; ctx.lineWidth = w; ctx.beginPath(); ctx.moveTo(o.x0, o.y0); ctx.lineTo(s.x, s.y); ctx.stroke(); ctx.globalAlpha = 1 - k; ctx.strokeStyle = "#ffffff"; ctx.lineWidth = w * .35; ctx.stroke(); }
      else if (o.k === "p") { if (k > 1) continue; ctx.globalAlpha = (1 - k) * .9; ctx.strokeStyle = o.rgba; ctx.lineWidth = (5 - 3 * k) * d; ctx.beginPath(); ctx.ellipse(o.x0, o.y0, o.R * k, o.R * k * .55, 0, 0, TAU); ctx.stroke(); }
      else if (o.k === "h") { if (s && k >= 0 && !o.hit) { o.hit = 1; b.booms.push({ x: s.x, y: s.y, t, big: 0 }); } } }
    ctx.globalCompositeOperation = "source-over"; }
  ctx.restore(); ctx.globalAlpha = 1; }
/* v66: start baking''')

# --- the map: a fleet led by a flagship with a look glows in the set's colour, brighter from 4 pieces
rep('function fleet3D(W, n, col, hostile, big, cube, flag) {', 'function fleet3D(W, n, col, hostile, big, cube, flag, look) {')
rep('const fc = flag ? new TH.Color(FLAG_GLOW[flag]) : null,', 'const fc = flag ? new TH.Color(look && look.t ? look.col : FLAG_GLOW[flag]) : null,')
rep('    if (fl1) for (const [x, y, z, rr, c, a] of G1.glow) pts.push([s, x, y, z, rr, a, c ? new TH.Color(c) : fc, 1]); }', '''    if (fl1) for (const [x, y, z, rr, c, a] of G1.glow) pts.push([s, x, y, z, rr * (look && look.t >= 2 ? 1.35 : 1), a, c && !(look && look.t) ? new TH.Color(c) : fc, 1]);
    if (fl1 && look && look.t >= 2) pts.push([s, 0, 0, 0, (G1.len || 1) * (look.t >= 3 ? 1.2 : .9), .32, fc, 1]); } /* v517 the set's aura round the whole hull */''')
rep('''function fleetObj(W, f, hostile, cube) {''', '''const fleetFlagU = (f, hostile) => f.demo || f.raid || f.mission === "spy" ? null : hostile ? f.from : f.u ? f.u : f.js ? ((G.assaults && G.assaults[f.js] && G.assaults[f.js].leader) || G.me) : G.me;
function fleetObj(W, f, hostile, cube) {''')
rep('fformOf(f), !!cube, flag), tot = Object.values(f.n || {})', 'fformOf(f), !!cube, flag, flag ? uidLook(fleetFlagU(f, hostile)) : null), tot = Object.values(f.n || {})')

# --- the Dock: what your sets look like
rep('''      <h2 class="sec">Loadouts</h2><div class="fsload">''', '''      ${fsLookHTML(f)}
      <h2 class="sec">Loadouts</h2><div class="fsload">''')
rep('const fsSetMax = k =>', '''function fsLookHTML(f) { const lk = fsLookOf(f), sets = Object.keys(FS_LOOK).filter(k => FS_SETS[k]); const cur = lk ? FS_LOOK[lk.s] : null;
  const row = (k, n) => { const L = FS_LOOK[k], mx = fsSetMax(k), on = j => n >= j; return `<div class="fslk"><span><i style="background:${L[0]};box-shadow:0 0 8px ${L[0]}"></i>${esc(FS_SETS[k][0])} · ${n}/${mx}</span><b><i class="${on(2) ? "up" : "off"}">2: glow</i> <i class="${on(Math.min(4, mx)) && mx > 4 ? "up" : mx > 4 ? "off" : "hide"}">4: aura</i> <i class="${on(mx) ? "up" : "off"}">${mx}: ${esc(L[2])}</i></b></div>`; };
  const c = fsSetCounts(fsEquipped(f)), shown = sets.filter(k => c[k]);
  return `<h2 class="sec">Flagship look</h2><p class="note">${lk ? `Your flagship flies in <b style="color:${cur[0]}">${esc(FS_SETS[lk.s][0])}</b> colours${lk.t >= 2 ? (lk.t >= 3 ? `, with its aura and the <b>${esc(cur[2])}</b> in every battle` : " with an aura") : ""}. Other commanders see it too.` : "Wear 2 pieces of one set and your flagship glows in its colour. 4 pieces add an aura; the full set adds a signature weapon to every battle."} The look comes from the set you wear most; it adds no stats.</p>${shown.map(k => row(k, c[k])).join("")}`; }
const fsSetMax = k =>''')
rep('.monart{flex-shrink:0;', '.fslk{display:flex;justify-content:space-between;gap:8px;padding:6px 0;border-bottom:1px solid var(--line);font-size:12.5px;flex-wrap:wrap}.fslk span i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}.fslk b{font-weight:500}.fslk b i{font-style:normal;margin-left:6px}.fslk b i.up{color:#fff}.fslk b i.off{opacity:.45}.fslk b i.hide{display:none}\n.monart{flex-shrink:0;')
s2 = re.sub(r"GAME_V = 516\b", "GAME_V = 517", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
