# v384 World Bosses: the Pyramid Overlord with its four Energy Conduits, the Orbital Devourer and the Void Warden join the map as weekly
# world bosses. Code-built 3D models with their own moves (assets/bosses/model/boss3d.js, inlined), a shared hull record, bounties and
# kill shares, a boss card, a Map Events row, cinematic view, live 3D in the battle report, and the Advisor's lines.
import os
p = "docs/index.html"; t = open(p).read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:90]); t = t.replace(a, b)
here = os.path.dirname(os.path.abspath(__file__))
blk = open(os.path.join(here, "p384_wboss_block.js")).read()
b3d = open(os.path.join(here, "..", "..", "assets", "bosses", "model", "boss3d.js")).read()
assert "</script" not in b3d

# the model builder, inline so the website and the artifact both have it
rep('<script src="lib/GLTFLoader-r128.js"></script>', '<script src="lib/GLTFLoader-r128.js"></script>\n<script>\n' + b3d + '\n</script>')
# the game block goes in after the pyramid expeditions
rep('function arrive(f) {\n  const p = G.byId[f.pid]', blk + '\nfunction arrive(f) {\n  const p = G.byId[f.pid]')
# positions: a boss moves on its own path
rep('function pos(p, T) { const a', 'function pos(p, T) { if (p.mv) { const q = p.mv(T, {}); return { x: q.x, y: q.z }; } const a')
rep('function P3(p, T, out) {', 'function P3(p, T, out) { if (p.mv) return p.mv(T, out);')
# combat stats: the boss's hull sections (the Overlord's shield multiplies shields and hull)
rep('  if (MON[k]) { const s = .25 + .15 * (t.mon || 1);', '  if (isWbU(k)) { const m = t.wbSh || 1; return { atk: AL[k].atk, sh: AL[k].sh * m, hull: AL[k].hull * m }; }\n  if (MON[k]) { const s = .25 + .15 * (t.mon || 1);')
rep('ssquid: ["cruiser", "acid", .12, .14, 5, 1]', 'ssquid: ["cruiser", "acid", .12, .14, 5, 1], wbOvl: ["titan", "beam", .38, 0, 1, 8], wbDev: ["titan", "plasma", .34, 0, 1.6, 6], wbWar: ["titan", "ion", .36, 0, 1, 6], wbCon: ["station", "beam", .3, 0, 0, 4]')
rep('const SIDE_LEN = { spyProbe: .3,', 'const SIDE_LEN = { wbOvl: 1.8, wbDev: 1.8, wbWar: 1.8, wbCon: 1.4, spyProbe: .3,')
# fleets: arrival, resolution, target
rep('f.nid ? gatherStart(f) : f.xid ? pirateArrive(f)', 'f.wb ? (f.phase = "resolving") : f.nid ? gatherStart(f) : f.xid ? pirateArrive(f)')
rep('if (f.pid === "nexus" && !f.assault) resolveNexus(f); else resolveAssault(f);', 'if (f.wb) wbResolve(f); else if (f.pid === "nexus" && !f.assault) resolveNexus(f); else resolveAssault(f);')
rep('f.yid ? YB[f.yid] : f.pid === "nexus" ? NEXUS : G.byId[f.pid];', 'f.yid ? YB[f.yid] : f.wb ? WBO[f.wb] : f.pid === "nexus" ? NEXUS : G.byId[f.pid];')
rep('const tgtById = id => G.byId[id] || NB[id] || PB[id] || YB[id] || (id === "nexus" ? NEXUS : null);', 'const tgtById = id => G.byId[id] || NB[id] || PB[id] || YB[id] || wbById(id) || (id === "nexus" ? NEXUS : null);')
# the shared record
rep('db.doc("event/nexus").onSnapshot(s => { G.nexus = s.exists ? cleanNexus(s.data()) : null; softRender(); }, () => {});',
    'db.doc("event/nexus").onSnapshot(s => { G.nexus = s.exists ? cleanNexus(s.data()) : null; softRender(); }, () => {});\n    db.doc("event/wboss").onSnapshot(s => { G.wb = s.exists ? s.data() : null; wbSeen(G.wb); wbClaim(); softRender(); }, () => {}); /* v384 world bosses */')
# map: models, labels, taps
rep('cubeLiveFx(W, t, T); missileFx(W, t, T);', 'cubeLiveFx(W, t, T); try { wbMapFx(W, t, T); } catch (e) {} missileFx(W, t, T);')
rep('  for (const [yid0, o] of W.pyramids || []) { const y = YB[yid0];',
    '''  { const st = wbState(T); for (const key in WB) { if (!(st.hp[key] > 0)) continue; const D = WB[key], q = P3(WBO[key], T, WBQ); V3B.set(q.x, q.y + (D.con != null ? 6 : 10) * D.sc * 1.6, q.z); const dd = cp.distanceTo(V3B), s = proj(V3B); if (!s) continue; /* v384 world bosses */
      const sr = (D.con != null ? 6 : 16) * D.sc * 1.6 / dd * k; hits.push({ wb: key, x: s[0], y: s[1], sr: Math.max(sr, 14) });
      if (D.con == null || sr > 5) lbl(D.con == null ? -1e8 : -sr - 3, `${D.ic} ${D.n} · ${Math.round(st.hp[key] / WB_SEG * 100)}%${key === "ovl" && wbCons(T) ? " · shielded" : ""}`, s[0], s[1] - Math.max(sr, 12) - 8, D.col); } }
  for (const [yid0, o] of W.pyramids || []) { const y = YB[yid0];''')
rep("  if (best && best.nid) { ACT.node({ id: best.nid }); return; }", "  if (best && best.wb) { ACT.wboss({ id: best.wb, nofly: 1 }); return; }\n  if (best && best.nid) { ACT.node({ id: best.nid }); return; }")
# the card, its actions, cinematic view
rep("pyramid: shPyramid,", "pyramid: shPyramid, wboss: shWboss,")
rep("  pyramid: d => { const y = YB[d.id]; if (!y) return; ",
    '''  wboss: d => { const key = d.id, O = WBO[key]; if (!O) return; pick = {}; for (const k in S.ships) if (S.ships[k] && SH[k]) pick[k] = S.ships[k]; /* v384 world bosses */
    if (view !== "galaxy") { view = "galaxy"; render(); } G.sel = null; G.selNode = null; if (G3 && !d.nofly) { G3.cam.followFleet = null; G3.cam.follow = null; const q = P3(O, now()); G3.cam.goal = { tx: q.x, ty: q.y, tz: q.z, dist: WB[key].con != null ? 50 : 90 }; }
    openSheet({ type: "wboss", id: key }); },
  wbGo: d => act(() => { const key = d.id, O = WBO[key], D = WB[key]; if (!O || !canPlay()) return; if (!wbAlive(key)) return toast(`The ${D.n} has already fallen this week.`, "warn"); if (slotsFull()) return;
    const n = takeShips(pick); if (!Object.keys(n).length) return; const f = sendFleet(O, n, "attack", { wb: key }); if (!f) return; closeSheet(); toast(`Fleet launched at the ${D.n}. Arrival in ${ftime(f.tt)}.`); }),
  pyramid: d => { const y = YB[d.id]; if (!y) return; ''')
rep('function cineObjStart(id, n) { const it = PB[id] || YB[id] || G.byId[id] || (id[0] === "r" ? NB[id] : null);', 'function cineObjStart(id, n) { const it = PB[id] || YB[id] || G.byId[id] || wbById(id) || (id[0] === "r" ? NB[id] : null);')
rep('function cineObjPos(W, T) { const id = W.cam.cineObj.id, it = PB[id] || YB[id] || G.byId[id] || (id[0] === "r" ? NB[id] : null);',
    'function cineObjPos(W, T) { const id = W.cam.cineObj.id, it = PB[id] || YB[id] || G.byId[id] || wbById(id) || (id[0] === "r" ? NB[id] : null); if (it && it.wb) { const q = P3(it, T); return { x: q.x, y: q.y + 6 * WB[it.wb].sc, z: q.z, yaw: null }; }')
# Finder › Map Events: the bosses come first
rep('      <h2 class="sec">Weekly battle</h2>', '''      <h2 class="sec">World bosses</h2><div class="list">${["ovl", "dev", "war"].map(k => { const D = WB[k], st = wbState(T), hp = st.hp[k] | 0; return `<button class="tgt mev${hp ? " mlive" : ""}" data-act="wboss" data-id="${k}"><span class="lvl" style="color:${D.col};border-color:${D.col}">${D.ic}</span><span><span class="nm">${D.n}</span><br><span class="sub">${hp ? `${Math.round(hp / WB_SEG * 100)}% hull · ${D.where}${k === "ovl" ? ` · shield ${wbCons(T)}/4 conduits` : ""}` : `Defeated · back in ${ftime(wbEnd(st.cyc) - T)}`}</span></span><span class="pill ${hp ? "bad" : "wait"}">${hp ? "Hunt" : "Down"}</span></button>`; }).join("")}</div>
      <h2 class="sec">Weekly battle</h2>''')
# the Advisor on each boss card
rep('nexus: "Commander, the Super Cube is the prize of the galaxy.', '''wbovl: "Commander, the Pyramid Overlord walks the middle layers. Four Energy Conduits feed its shield, so take them down first. Every hit pays a bounty, and when it falls, everyone who fought it shares the spoils.",
  wbdev: "Commander, the Orbital Devourer never stops moving. Find where it is right now, and strike it with our heaviest ships. Every section of hull we tear off pays a bounty.",
  wbwar: "Commander, the Void Warden guards the deep layers near the Core. It hits hard, so send a strong fleet, and bring it down with our allies for a share of its spoils.",
  wbcon: "Commander, this conduit feeds the Overlord's shield. Destroy all four, and the Overlord takes full damage.",
  nexus: "Commander, the Super Cube is the prize of the galaxy.''')
rep('  else if (s.type === "pyramid") k = "pyramid"; else if (s.type === "nexus") k = "nexus";', '  else if (s.type === "pyramid") k = "pyramid"; else if (s.type === "nexus") k = "nexus"; else if (s.type === "wboss" && s.id) k = "wb" + (s.id[0] === "c" ? "con" : s.id);')
# the battle report: the boss fights as one grand hull, rendered live in 3D
rep('battle.superSide = r.dName === "Collective Warden" ? "d" : r.aName === "The Cube" ? "a" : null;', 'battle.superSide = r.wb ? "d" : r.dName === "Collective Warden" ? "d" : r.aName === "The Cube" ? "a" : null;')
rep('const superSideOf = r => r ? (r.dName === "Collective Warden" ? "d" : r.aName === "The Cube" ? "a" : null) : null;', 'const superSideOf = r => r ? (r.wb ? "d" : r.dName === "Collective Warden" ? "d" : r.aName === "The Cube" ? "a" : null) : null;\nconst scName = r => r && r.wb && WB[r.wb] ? WB[r.wb].n : "Super Cube";')
rep('  for (const q of R.squads) { cardPal(q.k); shipArtSoon', '  for (const q of R.squads) { if (isWbU(q.k)) continue; cardPal(q.k); shipArtSoon')
rep("function scSum(r, side) { const s0 = r.start[side] || {}, L = (side === \"a\" ? r.lossA : r.lossD) || {}; let h0 = 0, h1 = 0, a = 0, sh = 0;",
    "function scSum(r, side) { if (r.wb && r.wbSeg && WB[r.wb]) { const u = AL[WB[r.wb].k]; return { h0: WB_SEG * u.hull, h1: r.wbSeg[1] * u.hull, a: r.wbSeg[0] * u.atk, sh: r.wbSeg[0] * u.sh, integ: r.wbSeg[1] / WB_SEG }; } /* v384: a world boss's whole hull */\n  const s0 = r.start[side] || {}, L = (side === \"a\" ? r.lossA : r.lossD) || {}; let h0 = 0, h1 = 0, a = 0, sh = 0;")
rep('<div class="sccard"><div class="sch"><b>■ Super Cube</b>', '<div class="sccard"><div class="sch"><b>${r.wb ? WB[r.wb].ic : "■"} ${esc(scName(r))}</b>')
rep('<td>Super Cube<small>Collective flagship · ', '<td>${esc(scName(r))}<small>${r.wb ? "World boss" : "Collective flagship"} · ')
rep('{ [ss]: { supercube: scStats(sim.stats[ss]) } }', '{ [ss]: { [r.wb && WB[r.wb] ? WB[r.wb].k : "supercube"]: scStats(sim.stats[ss]) } }')
rep('<span>Unit <b>Super Cube</b></span>', '<span>Unit <b>${esc(scName(b.r))}</b></span>')
rep('const art = shipArtSoon("cube", b.acc[b.superSide], "side"), Lc = Math.min(W, H) * .62, cx = b.scC.x, cy = b.scC.y + Math.sin(t * .0008) * Lc * .01, hp = idx.reduce((s, k) => s + Math.max(0, b.n[k]), 0) / Math.max(1, idx.reduce((s, k) => s + Q[k].n0, 0));',
    'const wbk = b.r.wb, art = wbk ? null : shipArtSoon("cube", b.acc[b.superSide], "side"), Lc = Math.min(W, H) * .62, cx = b.scC.x, cy = b.scC.y + Math.sin(t * .0008) * Lc * .01, hp = idx.reduce((s, k) => s + Math.max(0, b.n[k]), 0) / Math.max(1, wbk ? WB_SEG : idx.reduce((s, k) => s + Q[k].n0, 0));')
rep('if (art) ctx.drawImage(art, -Lc, -Lc / 2, Lc * 2, Lc); else drawUnit(ctx, "cube", 0, 0, Lc * .4, SIDE_COL[b.superSide].main, -1);',
    'if (wbk) { const tl = H > W * 1.1, aw = Math.min(Lc * 2.6, W * .96), ah = tl ? aw * .85 : aw / 2; const A = wbArt(wbk, aw, ah, t, { hp, live: alive.length > 0 }); if (A) ctx.drawImage(A, -aw / 2, -ah / 2, aw, ah); } else if (art) ctx.drawImage(art, -Lc, -Lc / 2, Lc * 2, Lc); else drawUnit(ctx, "cube", 0, 0, Lc * .4, SIDE_COL[b.superSide].main, -1);')
rep('ctx.drawImage(glowSprite("rgba(93,255,106,1)"), cx - Lc * 1.1, cy - Lc * .9, Lc * 2.2, Lc * 1.8);', 'ctx.drawImage(glowSprite(wbk ? "rgba(180,92,255,1)" : "rgba(93,255,106,1)"), cx - Lc * 1.1, cy - Lc * .9, Lc * 2.2, Lc * 1.8);')
rep('ctx.fillStyle = "#5dff6a"; ctx.fillRect(cx - Lc * .4, cy + Lc * .36', 'ctx.fillStyle = wbk ? WB[wbk].col : "#5dff6a"; ctx.fillRect(cx - Lc * .4, cy + Lc * .36')
rep('function closeBattle() { if (battle) { crumb("battle closed"); battleFree(battle);', 'function closeBattle() { if (battle) { crumb("battle closed"); battleFree(battle); wbArtFree();')

rep('dN = [r.dName === "Collective Warden" ? "The Super Cube · Collective Warden"', 'dN = [r.wb ? `${WB[r.wb] ? WB[r.wb].n : r.dName} · World boss` : r.dName === "Collective Warden" ? "The Super Cube · Collective Warden"')
rep('return `<div class="bh-ros ${side}"><span class="${pc ? "" : "gone"}"><i>Super Cube</i><b>${pc}%</b><small> integrity</small></span></div>`; }', 'const wpc = b.r.wb ? Math.round(b.Q.reduce((s2, q, i) => s2 + (q.side === side ? Math.max(0, b.n[i]) : 0), 0) / WB_SEG * 100) : pc; return `<div class="bh-ros ${side}"><span class="${wpc ? "" : "gone"}"><i>${esc(scName(b.r))}</i><b>${wpc}%</b><small>${b.r.wb ? " hull" : " integrity"}</small></span></div>`; }')
rep('<span class="bh-doc">${esc(side === b.superSide ? "Assimilation"', '<span class="bh-doc">${esc(side === b.superSide ? (b.r.wb ? "World boss" : "Assimilation")')
rep("tx = clamp(mx, W * .22, W * .78), ty = clamp(my, H * .28, H * .72);", "tx = b.r.wb && W < H ? W / 2 : clamp(mx, W * .22, W * .78), ty = clamp(my, H * .28, H * .72);")
rep('const c = G3.cam; if (c.followMv) followMvEnd(G3, 1); c.follow = null; c.followFleet = null; c.vel = null; c.cineObj = { id }; c.cine = { m: "orbit" }; c.head = it.a0 || 0;',
    'const c = G3.cam; if (c.followMv) followMvEnd(G3, 1); c.follow = null; c.followFleet = null; c.vel = null; c.cineObj = { id }; c.cine = { m: "orbit" }; c.head = it.a0 || 0; if (it.wb) { c.cineObj.fit = 1; c.goal = { dist: (WB[it.wb].con != null ? 45 : 105) * WB[it.wb].sc }; $("#app").classList.add("cine"); cineBar(); wbScanOn(it.wb); return; } /* v384: a world boss gets its scan */')
rep('function cineEnd() { if (!G3 || !G3.cam.cine) return;', 'function cineEnd() { wbScanOff(); if (!G3 || !G3.cam.cine) return;')
rep('if (c.cineObj) { const id = c.cineObj.id, it = PB[id] || YB[id] || (id[0] === "r" ? NB[id] : null); if (it) w.textContent', 'if (c.cineObj) { const id = c.cineObj.id, it = PB[id] || YB[id] || (id[0] === "r" ? NB[id] : null), wo = wbById(id); if (wo) w.textContent = `${WB[wo.wb].ic} Scanning · ${WB[wo.wb].n} · ${Math.round(wbHp(wo.wb) / WB_SEG * 100)}% hull`; else if (it) w.textContent')
# styles
i = t.index('</style>', t.index('.fshero{'))
t = t[:i] + '''
/* v384 world bosses */
.wbhp{display:flex;flex-direction:column;gap:5px;margin:8px 0 6px}.wbhp span{font:600 12px/1 var(--mono,ui-monospace,monospace);color:#d9c6ff;letter-spacing:.04em}
.wbbar{height:9px;border-radius:5px;background:rgba(255,255,255,.08);overflow:hidden;box-shadow:inset 0 0 0 1px rgba(201,166,255,.25)}.wbbar i{display:block;height:100%;border-radius:5px;box-shadow:0 0 12px currentColor}
.wblead{list-style:none;margin:4px 0 10px;padding:0;display:flex;flex-direction:column;gap:4px}.wblead li{display:flex;justify-content:space-between;gap:10px;padding:6px 10px;border-radius:8px;background:rgba(201,166,255,.07);font-size:13px}.wblead b{color:#d9a0ff;font-variant-numeric:tabular-nums}
#wbscan{position:fixed;inset:0;pointer-events:none;z-index:40;--sc:#c58bff}#wbscan .ws-c{position:absolute;width:34px;height:34px;border:2px solid var(--sc);opacity:.85}
#wbscan .tl{top:calc(env(safe-area-inset-top,0px) + 58px);left:14px;border-right:0;border-bottom:0}#wbscan .tr{top:calc(env(safe-area-inset-top,0px) + 58px);right:14px;border-left:0;border-bottom:0}#wbscan .bl{bottom:calc(env(safe-area-inset-bottom,0px) + 86px);left:14px;border-right:0;border-top:0}#wbscan .br{bottom:calc(env(safe-area-inset-bottom,0px) + 86px);right:14px;border-left:0;border-top:0}
#wbscan .ws-line{position:absolute;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,#9ff3ff,transparent);box-shadow:0 0 14px #5fd8ff;animation:wsScan 3.6s linear infinite;opacity:.7}@keyframes wsScan{0%{top:12%}100%{top:84%}}
#wbscan .ws-ret{position:absolute;left:50%;top:50%;width:150px;height:150px;margin:-75px 0 0 -75px;border:1px dashed rgba(159,243,255,.55);border-radius:50%;animation:wsRet 9s linear infinite}#wbscan .ws-ret::before{content:"";position:absolute;inset:22px;border:1px solid rgba(159,243,255,.3);border-radius:50%}@keyframes wsRet{to{transform:rotate(360deg)}}
#wbscan .ws-card{position:absolute;left:16px;top:calc(env(safe-area-inset-top,0px) + 104px);width:min(270px,calc(100vw - 32px));padding:12px 14px;border:1px solid color-mix(in srgb,var(--sc) 60%,transparent);border-radius:10px;background:rgba(6,8,18,.66);backdrop-filter:blur(4px);font-size:12px;color:#dfe9ff}
#wbscan .ws-card small{display:block;font:600 10px/1 ui-monospace,monospace;letter-spacing:.14em;color:#9ff3ff;animation:wsBlink 1.2s steps(2) infinite}@keyframes wsBlink{50%{opacity:.35}}#wbscan .ws-card>b{display:block;margin:6px 0 8px;font-size:16px;color:var(--sc);text-shadow:0 0 10px var(--sc)}
#wbscan dl{margin:0;display:flex;flex-direction:column;gap:5px}#wbscan dl div{display:grid;grid-template-columns:76px minmax(0,1fr);gap:8px;opacity:0;animation:wsIn .4s ease forwards;animation-delay:var(--d)}@keyframes wsIn{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}
#wbscan dt{color:#7f8cab;font:600 10px/1.5 ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase}#wbscan dd{margin:0;line-height:1.35}#wbscan .ws-th{color:#ff7a6a;font-weight:700;letter-spacing:.08em}
@media (prefers-reduced-motion:reduce){#wbscan .ws-line,#wbscan .ws-ret{animation:none}#wbscan dl div{animation:none;opacity:1}}
''' + t[i:]
open(p, "w").write(t)
print("ok")
