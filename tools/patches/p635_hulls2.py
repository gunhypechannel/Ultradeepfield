# v635: hull finishes move to the Premium page (with a live preview), six more materials (copper T1, silver T2, cobalt T3, pink
# crystal T6, obsidian T7, glyph holo T16; textures derived from the owner's five: tools/hull_derive.py), map fleets wear their
# finish, and other players see yours (your finishes ride on your public player record as "hf").
# (owner: "Do that and move hull color to the premium players section, add other material colors like obsidian, copper, silver,
# cobalt, pink crystal and glyph holo")
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# the materials, in tier order
a = s.index('const HULL_F = {'); b = s.index('\n', s.index('emerald: { n: "Emerald"', a))
s = s[:a] + '''const HULL_F = { copper: { n: "Copper", t: 1, col: "#e8763e", rim: "#ffa070", met: 1, rough: .25, k: 1.2, tm: .75, sw: "linear-gradient(135deg,#6a2a10,#ff9a5a 45%,#b8501e 60%,#ffd0b0)" },
  silver: { n: "Silver", t: 2, col: "#d8e0ec", rim: "#e8f2ff", met: 1, rough: .18, k: 1.25, tm: .8, sw: "linear-gradient(135deg,#5a6470,#ffffff 45%,#9aa6b4 60%,#f0f6ff)" },
  cobalt: { n: "Cobalt", t: 3, col: "#2a5aff", rim: "#6a9aff", met: .5, rough: .1, k: .9, sw: "linear-gradient(135deg,#0a1650,#4a7aff 45%,#1a3ab0 60%,#b0c8ff)" },
  gold: { n: "Gold", t: 5, col: "#ffb81c", rim: "#ffc040", met: 1, rough: .2, k: 1.3, tm: .75, sw: "linear-gradient(135deg,#7a5410,#ffe08a 45%,#c8901e 60%,#fff3c0)" },
  pink: { n: "Pink Crystal", t: 6, col: "#ff5ab4", rim: "#ff9ad0", met: .45, rough: .08, k: .95, sw: "linear-gradient(135deg,#5a0a38,#ff7ac8 45%,#c02a80 60%,#ffd0ec)" },
  obsidian: { n: "Obsidian", t: 7, col: "#2a2236", rim: "#a070ff", met: .6, rough: .06, k: .7, gl: .9, sw: "linear-gradient(135deg,#050308,#3a2a50 45%,#0a0610 60%,#8a60c0)" },
  amethyst: { n: "Amethyst", t: 8, col: "#9a4dff", rim: "#dba6ff", met: .5, rough: .1, k: .85, sw: "linear-gradient(135deg,#3a1470,#c58cff 45%,#7a3ad0 60%,#efd8ff)" },
  diamond: { n: "Diamond", t: 11, col: "#eef7ff", rim: "#bfe8ff", met: .9, rough: .05, k: 1.25, tm: .5, sw: "linear-gradient(135deg,#9fb8d0,#ffffff 40%,#c8f0ff 55%,#ffd8f4 70%,#ffffff)" },
  ruby: { n: "Ruby", t: 12, col: "#ff1438", rim: "#ff7a94", met: .5, rough: .08, k: .85, sw: "linear-gradient(135deg,#5a0614,#ff4a66 45%,#a8102c 60%,#ffc0cc)" },
  emerald: { n: "Emerald", t: 14, col: "#10d868", rim: "#86ffc0", met: .5, rough: .08, k: .85, sw: "linear-gradient(135deg,#053a1e,#3cff9a 45%,#0e8a48 60%,#c8ffe0)" },
  glyph: { n: "Glyph Holo", t: 16, col: "#30e8ff", rim: "#7afcff", met: .3, rough: .15, k: 1.1, tm: .3, gl: 1.6, sw: "linear-gradient(135deg,#032a30,#3af0ff 45%,#0a7080 60%,#c8fcff)" } };''' + s[b:]
# one material at a time, so map fleets can use it too (obj: texture in the model's own space, for instanced fleets)
a = s.index('function hullFinish(obj, f) {'); b = s.index('/* sparkles on the brightest parts', a)
old = s[a:b]
body = old[old.index('const n = m.clone();'):old.index('n.needsUpdate = true; return n;') + len('n.needsUpdate = true; return n;')]
body = body.replace('(f === "gold" ? .75 : f === "diamond" ? .5 : .2)', '(F.tm != null ? F.tm : .2)')
body = body.replace('"#include <project_vertex>\\n vHW = (modelMatrix * vec4(transformed, 1.0)).xyz; vHN = normalize(mat3(modelMatrix) * objectNormal);"',
                    '"#include <project_vertex>\\n" + (obj ? "vHW = transformed * 1.4; vHN = normalize(objectNormal);" : "vHW = (modelMatrix * vec4(transformed, 1.0)).xyz; vHN = normalize(mat3(modelMatrix) * objectNormal);")')
body = body.replace('n.customProgramCacheKey = () => "hullfin-" + f + (tex ? "-t" : "");', 'n.customProgramCacheKey = () => "hullfin-" + f + (tex ? "-t" : "") + (obj ? "-o" : "");')
assert 'obj ?' in body and 'F.tm' in body
s = s[:a] + ('function finMat(m, f, obj) { const F = HULL_F[f]; if (!F || !TH || !m || !m.isMeshStandardMaterial) return m; const col = new TH.Color(F.col), rim = new TH.Color(F.rim), tex = hullTex(f);\n  '
  + body + ' }\nfunction hullFinish(obj, f) { if (!HULL_F[f] || !TH) return; obj.traverse(o => { if (!o.isMesh || !o.material) return; o.material = Array.isArray(o.material) ? o.material.map(m => finMat(m, f)) : finMat(o.material, f); }); }\n') + s[b:]
# whose finish: yours, or another commander's from their public record
rep('function hullAccK(k, a) { a = String(a); if (!a.includes("^me")) return a; const f = hullOf(k); return a.replace("^me", f ? "~h" + f : ""); }',
    '''function hullOfU(u, k) { if (!u) return null; if (u === G.me) return hullOf(k); const m = G.players && G.players[u] && G.players[u].hf, f = m && m[k]; return HULL_F[f] ? f : null; }
const hullPubOf = () => { const o = {}; for (const k in (S && S.hullF) || {}) if (hullOf(k)) o[k] = S.hullF[k]; return Object.keys(o).length ? o : null; };
/* the fleet's finish on the map: the one its most numerous ship type wears */
function hullFleet(u, n) { let best = null, bn = 0; for (const [k, v] of Object.entries(n || {})) { const f = hullOfU(u, k); if (f && v > bn) { best = f; bn = v; } } return best; }
let FLEET_FIN = null;
function hullAccK(k, a) { a = String(a); if (a.includes("^me")) { const f = hullOf(k); return a.replace("^me", f ? "~h" + f : ""); } const m = /\\^u([^\\^]+)\\^/.exec(a); if (m) { const f = hullOfU(m[1], k); return a.replace(m[0], f ? "~h" + f : ""); } return a; }''')
# other commanders' ships in your battles
rep('return { [mine]: myAcc() + "^me", [foe]: SIDE_COL[foe].main + (ff ? "@" + ff : "") }; }', 'return { [mine]: myAcc() + "^me", [foe]: SIDE_COL[foe].main + (ff ? "@" + ff : "") + (fu && fu !== G.me && G.players[fu] ? "^u" + fu + "^" : "") }; }')
rep('+ "@" + f + (u === G.me ? "^me" : ""), enumerable: false,', '+ "@" + f + (u === G.me ? "^me" : G.players[u] ? "^u" + u + "^" : ""), enumerable: false,')
# your finishes go public
rep('cf: secFlag(), sh: hash(G.me) % SHARDS,', 'cf: secFlag(), hf: hullPubOf(), sh: hash(G.me) % SHARDS,')
# map fleets: a finish-specific copy of the faction's materials
rep('''function fleetKit(W, fac) {
  fac = FACTIONS[fac] ? fac : "terran"; W.fkm = W.fkm || {}; if (W.fkm[fac] !== undefined) return W.fkm[fac];
  W.fkm[fac] = null; if (!studio()) return null;''', '''function fleetKit(W, fac) {
  let fin = null; { const i = String(fac).indexOf("~h"); if (i >= 0) { fin = HULL_F[String(fac).slice(i + 2)] ? String(fac).slice(i + 2) : null; fac = String(fac).slice(0, i); } } /* v635 */
  fac = FACTIONS[fac] ? fac : "terran"; const fkey = fac + (fin ? "~h" + fin : ""); W.fkm = W.fkm || {}; if (W.fkm[fkey] !== undefined) return W.fkm[fkey];
  W.fkm[fkey] = null; if (!studio()) return null;''')
rep('''    Object.defineProperty(mats, "fac", { value: fac, enumerable: false });
    W.fkm[fac] = { mats, geo: {}, acc: new Map(), engT: glowTex("255,255,255", 1) };
  } catch (e) { W.fkm[fac] = null; }
  return W.fkm[fac];''', '''    if (fin) for (const nm of Object.keys(mats)) { const m = mats[nm]; if (/^f|win|eng|neon|glow|light|lamp/i.test(nm) || !m || !m.isMeshStandardMaterial || m.emissiveMap) continue; const n2 = finMat(m, fin, true); n2.envMap = m.envMap; n2.userData.mn = nm; mats[nm] = n2; }
    Object.defineProperty(mats, "fac", { value: fac, enumerable: false });
    W.fkm[fkey] = { mats, geo: {}, acc: new Map(), engT: glowTex("255,255,255", 1) };
  } catch (e) { W.fkm[fkey] = null; }
  return W.fkm[fkey];''')
rep('const K = fleetKit(W, flag || (hostile ? "terran" : facOf())); if (!K) return miniFleet(W, n, col, hostile);', 'const K = fleetKit(W, (flag || (hostile ? "terran" : facOf())) + (FLEET_FIN ? "~h" + FLEET_FIN : "")); if (!K) return miniFleet(W, n, col, hostile);')
rep('  const flag = fleetFlag(f, hostile), grp = fleet3D(W,', '  FLEET_FIN = f.demo || f.raid || f.mission === "spy" ? null : hullFleet(fleetFlagU(f, hostile), f.n); const flag = fleetFlag(f, hostile), grp = fleet3D(W,')
rep('flag ? uidLook(fleetFlagU(f, hostile)) : null), tot =', 'flag ? uidLook(fleetFlagU(f, hostile)) : null); FLEET_FIN = null; const tot =')
# a landed texture also refreshes map fleets made from colour alone
rep('    clearTimeout(hullTex.t); hullTex.t = setTimeout(', '    try { if (G3 && G3.fkm) for (const key of Object.keys(G3.fkm)) if (key.endsWith("~h" + f)) delete G3.fkm[key]; } catch (er) {}\n    clearTimeout(hullTex.t); hullTex.t = setTimeout(')
# the picker lives on the Premium page now: a ship-type row, a live preview, the swatches
rep('function hullPick(k) {', '''function hullSection() { const own = Object.keys(SH).filter(k => (S.ships || {})[k] > 0), ks = own.length ? own : ["fighter", "corvette", "battleship"], sel = SH[G.hullK] ? G.hullK : ks[0], fin = hullOf(sel);
  return `<div class="hfsec"><div class="hfsh"><b>Hull finishes</b><small>Plate your ships in metal and gems. Looks only; other commanders see them too.</small></div>
    <div class="hfks">${ks.map(k => `<button class="${k === sel ? "on" : ""}" data-act="hullK" data-k="${k}">${esc(SH[k].n)}${hullOf(k) ? ` <i style="background:url(art/hull/${hullOf(k)}.webp?v=${HULL_TV}) center/200%"></i>` : ""}</button>`).join("")}</div>
    <div class="hfprev"><canvas class="shipart" data-ship="${sel}" role="img" aria-label="${esc(SH[sel].n)}${fin ? " in " + HULL_F[fin].n : ""}"></canvas><span>${fin ? HULL_F[fin].n : "Standard"}</span></div>${hullPick(sel)}</div>`; }
function hullPick(k) {''')
rep('[["", { n: "Standard", t: 0, sw: "linear-gradient(135deg,#3a4652,#9aa8b6 50%,#55626e)" }], ...Object.entries(HULL_F)]', '[["", { n: "Standard", t: 0, sw: "linear-gradient(135deg,#3a4652,#9aa8b6 50%,#55626e)" }], ...Object.entries(HULL_F).sort((x, y) => x[1].t - y[1].t)]')
rep('return hd + prog + card + chest + how + `<div class="fgpad"></div>`; }', 'return hd + prog + card + chest + hullSection() + how + `<div class="fgpad"></div>`; }')
# the ship's page keeps a small link to it
rep('${kind === "s" && !P ? hullPick(k) : ""}', '${kind === "s" && !P ? `<button class="hflink" data-act="hullGo" data-k="${k}"><i style="background:${hullOf(k) ? `url(art/hull/${hullOf(k)}.webp?v=${HULL_TV}) center/200%` : "linear-gradient(135deg,#3a4652,#9aa8b6 50%,#55626e)"}"></i>Hull finish: <b>${hullOf(k) ? HULL_F[hullOf(k)].n : "Standard"}</b><em>Premium ›</em></button>` : ""}')
rep('  hullAll: d => {', '''  hullK: d => { G.hullK = d.k; render(true); },
  hullGo: d => { G.hullK = d.k; closeSheet(); setTimeout(() => { ACT.premOpen(); setTimeout(() => { const e = document.querySelector(".hfsec"); if (e) e.scrollIntoView({ block: "start", behavior: "smooth" }); }, 400); }, 60); },
  hullAll: d => {''')
css = ('.hfsec{flex-shrink:0;margin-top:12px;padding:12px;border-radius:16px;border:1px solid rgba(255,210,90,.4);background:radial-gradient(90% 60% at 50% 0,rgba(255,200,80,.12),transparent 70%),rgba(6,12,20,.6);display:flex;flex-direction:column;gap:10px}.hfsec>*{flex-shrink:0}'
  '.hfsh b{font:700 16px var(--f-display);color:#ffd25a;display:block}.hfsh small{font-size:11.5px;color:var(--muted)}.hfsec .hfp{margin:0;background:none;border:0;padding:0;-webkit-backdrop-filter:none;backdrop-filter:none}.hfsec .hfh{display:none}'
  '.hfks{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}.hfks::-webkit-scrollbar{display:none}.hfks button{all:unset;flex:none;cursor:pointer;font-size:12px;padding:6px 10px;border-radius:12px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);display:flex;align-items:center;gap:6px}.hfks button.on{border-color:#ffd25a;color:#ffd25a;background:rgba(255,210,90,.1)}.hfks i{width:12px;height:12px;border-radius:4px}'
  '.hfprev{position:relative;border-radius:14px;overflow:hidden;background:radial-gradient(ellipse at 50% 55%,#13253a,#03070d 75%)}.hfprev canvas{display:block;width:100%;height:150px}.hfprev span{position:absolute;left:10px;top:8px;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#ffd25a}'
  '.hflink{all:unset;box-sizing:border-box;cursor:pointer;flex-shrink:0;margin:10px 0 4px;display:flex;align-items:center;gap:8px;padding:9px 12px;border-radius:12px;background:rgba(6,12,20,.78);border:1px solid rgba(255,210,90,.35);font-size:13px}.hflink i{width:26px;height:26px;border-radius:8px;flex:none}.hflink b{color:#ffd25a}.hflink em{margin-left:auto;font-style:normal;font-size:12px;color:#ffd25a}\n')
i = s.index('</style>', s.index('#celeb{position:fixed')); s = s[:i] + css + s[i:]
s2 = re.sub(r"GAME_V = 634\b", "GAME_V = 635", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
