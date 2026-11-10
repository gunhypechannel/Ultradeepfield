# v402: the Convergence remade from the owner's art. One sigil-titan (BOSS3D.pentarch: spine, five-colour core, element wings,
# rune rings with orbs, pillar and arena) where every lost element is missing its colour. The fusion is a set piece (each survivor flies
# in and docks with a callout, the arena ignites, the title card); it sheds an element at every fifth of its hull and players can aim at
# a wing to break it sooner; the map takes the colours that remain; a five-pip band; the core shatters into shards to collect; Clean
# Sweep when the Pentarch never forms; a layered Convergence theme that loses an instrument with every element; the art as key art.
import json, sys
p = "docs/index.html"; t = open(p).read(); ART = json.load(open(sys.argv[1]))
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (t.count(a), a[:100]); t = t.replace(a, b)

# ---------- the shared record: wings torn loose and damage aimed at each wing, per Convergence ----------
rep("o.cyc = c; o.cyc2 = c2; o.scar =", "o.shed = s2 && Array.isArray(o.shed) ? o.shed.filter(k => WB_EL.includes(k)) : []; o.wing = s2 && o.wing && typeof o.wing === \"object\" ? o.wing : {}; o.cyc = c; o.cyc2 = c2; o.scar =")
rep("""const wbPentAlive = T => WB_EL.filter(k => (wbState(T).hp[k] | 0) > 0).map(k => WB[k].el); // the Elementals that live on in the Pentarch
const wbFuseK = T => { if (G.elePrev === 2) return clamp(((performance.now() - (G.elePrevAt || 0)) / 15000), 0, 1); const w = wbWin("epx", wbCyc2(T)); return w ? clamp((T - w[0]) / (20 * 60e3), 0, 1) : 1; }; // the fusion: 20 minutes""",
"""/* v402: the Elementals that survived to the fusion, and those still in the Pentarch (not yet torn loose) */
const wbFusedIn = st => WB_EL.filter(k => (st.hp[k] | 0) > 0), wbPentLive = st => wbFusedIn(st).filter(k => !(st.shed || []).includes(k));
const wbPentAlive = T => wbPentLive(wbState(T)).map(k => WB[k].el);
const wbSwept = T => { const c2 = wbCyc2(T), w = wbWin("epx", c2); return !G.elePrev && !!w && T >= w[0] && !wbFusedIn(wbState(T)).length; }; // Clean Sweep: all five fell first, so it never formed
/* the fusion as a set piece: 20 minutes from hour 24 (or a 45-second replay): each survivor flies in and docks in turn, then the arena ignites */
const WB_FUSE_MS = 20 * 60e3, WB_FUSE_REP = 45000;
function wbFuse(T) { let e = null; if (G.fuseRep) { e = (performance.now() - G.fuseRep) / WB_FUSE_REP; if (e > 1.2) { G.fuseRep = 0; e = null; } }
  if (e == null) { const w = wbWin("epx", wbCyc2(T)); e = G.elePrev === 2 ? 1 : w ? (T - w[0]) / WB_FUSE_MS : 1; }
  e = clamp(e, 0, 1); const st = wbState(T), L = wbFusedIn(st).length ? wbFusedIn(st) : G.elePrev ? WB_EL : [], n = Math.max(1, L.length), dock = {};
  for (const k of WB_EL) dock[WB[k].el] = 1; L.forEach((k, i) => { const a = i * .72 / n, d = Math.min(.8 - a, 1.7 * .72 / n); dock[WB[k].el] = easeIO(clamp((e - a) / d, 0, 1)); });
  return { e, dock, form: easeIO(clamp((e - .78) / .17, 0, 1)), order: L }; }""")
rep("if (key === \"epx\") return .25 + .15 * WB_EL.filter(k => (st.hp[k] | 0) > 0).length;", "if (key === \"epx\") return .25 + .15 * wbPentLive(st).length;")
rep("""  if (key === "epx") { const n = WB_EL.filter(k => (st.hp[k] | 0) > 0).length; return `${n} of 5 Elementals fused in · ${Math.round(s * 100)}% strength`; }""",
    """  if (key === "epx") { const L = wbPentLive(st), sh = st.shed || []; return `${L.length} of 5 elements still in it${sh.length ? ` · torn loose: ${sh.map(k => WB[k].n).join(", ")}` : ""} · ${Math.round(s * 100)}% strength`; }""")
rep("const wbUp = (k, T = now()) => wbOn(k, T) && wbAlive(k, T);", "const wbUp = (k, T = now()) => wbOn(k, T) && wbAlive(k, T) && !(k === \"epx\" && wbSwept(T));")

# ---------- fights: aim at a wing; a wing tears loose at every fifth of the hull, or sooner when it is targeted ----------
rep("""    cur.hp[key] = left; const dm = cur.dmg[key] = cur.dmg[key] || {}; if (seg) dm[G.me] = (dm[G.me] || 0) + seg; if (!left) { cur.dead[key] = at; cur.last[key] = G.me; }""",
"""    cur.hp[key] = left; const dm = cur.dmg[key] = cur.dmg[key] || {}; if (seg) dm[G.me] = (dm[G.me] || 0) + seg; if (!left) { cur.dead[key] = at; cur.last[key] = G.me; }
    const shedNow = []; if (key === "epx" && seg) { const fused = wbFusedIn(cur), live = () => fused.filter(k => !cur.shed.includes(k)), aim = live().includes(f.aim) ? f.aim : null; if (aim) cur.wing[aim] = (cur.wing[aim] || 0) + seg;
      for (const k of live()) if ((cur.wing[k] || 0) >= WB_SEG * .12) { cur.shed.push(k); shedNow.push(k); } // a wing everyone aims at breaks sooner
      const due = [.2, .4, .6, .8].filter(x => 1 - left / WB_SEG >= x).length; while (cur.shed.length < due && live().length) { const k = live().sort((a, b) => (cur.wing[b] || 0) - (cur.wing[a] || 0) || WB_EL.indexOf(a) - WB_EL.indexOf(b))[0]; cur.shed.push(k); shedNow.push(k); } }""")
rep("""      start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) });
    f.n = cleanShips(res.aLeft); repairDocks(rep, lossesOf(mine0, f.n));""", """      start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) });
    if (shedNow.length) rep.shed = shedNow; if (key === "epx") rep.pent = wbFusedIn(cur).filter(k => !cur.shed.includes(k) || shedNow.includes(k)).map(k => WB[k].el);
    f.n = cleanShips(res.aLeft); repairDocks(rep, lossesOf(mine0, f.n));""")
rep("""    if (!left) { bump("bosses"); note(`We brought down the ${D.n}! Everyone who fought it this week can claim the spoils.`, "win"); }""",
    """    if (shedNow.length) note(`${shedNow.map(k => WB[k].n).join(" and ")} torn loose from the Pentarch! ${shedNow.length > 1 ? "Their colours are" : "Its colour is"} gone from the Convergence.`, "win");
    if (!left) { bump("bosses"); note(`We brought down the ${D.n}! Everyone who fought it this week can claim the spoils.`, "win"); }""")
rep("const f = sendFleet(O, n, \"attack\", { wb: key }); if (!f) return; closeSheet(); toast(`Fleet launched at the ${D.n}. Arrival in ${ftime(f.tt)}.`); }),",
    "if (key === \"epx\" && wbSwept(now())) return toast(\"Clean Sweep: the Convergence never formed.\"); const aim = key === \"epx\" && S.epxAim && wbPentLive(wbState()).includes(S.epxAim) ? S.epxAim : null; const f = sendFleet(O, n, \"attack\", { wb: key, aim }); if (!f) return; closeSheet(); toast(`Fleet launched at the ${D.n}${aim ? `, aimed at ${WB[aim].n}'s wing` : \"\"}. Arrival in ${ftime(f.tt)}.`); }),")
rep("""  else body = `<h2 class="sec">Attack</h2>${originBar()}""", """  else body = `${key === "epx" ? epxAimBar(st) : ""}<h2 class="sec">Attack</h2>${originBar()}""")
rep("""/* ---------- the boss card ---------- */""", """/* v402 the Pentarch's wings: aim your fleet at one (its damage counts toward breaking that wing) or at the core */
function epxAimBar(st) { const L = wbPentLive(st), a = L.includes(S.epxAim) ? S.epxAim : null;
  return `<h2 class="sec">Aim</h2><p class="note">Every fifth of its hull tears one element loose. Aim at a wing to break it sooner and silence it.</p><div class="aimrow"><button class="aimb${a ? "" : " on"}" data-act="epxAim" data-k="">✪ Core</button>${L.map(k => { const D = WB[k], w = Math.min(100, Math.round((st.wing[k] || 0) / (WB_SEG * .12) * 100));
    return `<button class="aimb${a === k ? " on" : ""}" data-act="epxAim" data-k="${k}" style="--c:${D.col}"><span>${D.ic} ${esc(D.n)}</span><i style="width:${w}%"></i></button>`; }).join("")}</div>`; }
/* ---------- the boss card ---------- */""")
rep("""  elePrev: () =>""", """  epxAim: d => { S.epxAim = d && d.k ? d.k : null; dirty(); if (sheet) renderSheet(); },
  convReplay: () => { if (!G3) { view = "galaxy"; render(); } G.fuseRep = performance.now(); if (G3 && G3.wbM && G3.wbM.epx) G3.wbM.epx.dk = null; closeSheet(); setTimeout(() => { try { ACT.cineObj({ id: "wb_epx" }); } catch (e) {} }, 400); },
  convShards: () => act(() => { const st = wbState(), c2 = st.cyc2, id = "shards:" + c2; S.wbGot = S.wbGot || {}; if (S.wbGot[id]) return toast("You've already gathered the Pentarch's shards."); if (!st.dead.epx || now() - st.dead.epx > 10 * 60e3) return toast("The shards have faded.");
    S.wbGot[id] = 1; const sh = 12 + Math.floor(Math.random() * 9); S.shards = (S.shards || 0) + sh; const mats = fsDrop(lootRoll([["cube", 4, 1], ["crystal", 3, 2]]), "the Pentarch's shards", { nocap: 1 }); logReward("The Pentarch's shards", null, { shards: sh, kind: "battle" }); note(`You gathered the Pentarch's shards: ◆${sh}${mats ? " and forge materials" : ""}.`, "win"); dirty(); }),
  elePrev: () =>""")
rep("G.elePrev = ((G.elePrev || 0) + 1) % 3; G.elePrevAt = performance.now();", "G.elePrev = ((G.elePrev || 0) + 1) % 3; G.elePrevAt = performance.now(); G.fuseRep = G.elePrev === 2 ? performance.now() : 0;")

# ---------- the map: one model, its colours set live; pieces fly in; shed animation; callouts and the title card ----------
rep("""    if (key === "epx") { M.b.form = wbFuseK(T); const al = wbPentAlive(T).join(); if (M.al == null) M.al = al; else if (M.al !== al) { W.scene.remove(g); delete W.wbM.epx; W.wbComp = 0; continue; } } /* the fusion: the aspects fly in; a fallen Elemental leaves it */""",
    """    if (key === "epx") wbPentFx(M, g, q, st, T, t); /* v402: the fusion, the colours that remain, a wing torn loose */""")
rep("const D = WB[key], alive = st.hp[key] > 0 && wbOn(key, T), q = P3(WBO[key], T, WBQ)", "const D = WB[key], alive = st.hp[key] > 0 && wbOn(key, T) && !(key === \"epx\" && wbSwept(T)), q = P3(WBO[key], T, WBQ)")
rep("""function wbMapFree(W) {""", """function wbPentFx(M, g, q, st, T, t) { const b = M.b, fz = wbFuse(T); b.form = fz.form; for (const k in fz.dock) b.dock[k] = fz.dock[k]; b.far = 95 / g.scale.x; b.ground = Math.max(5, q.y / g.scale.x);
  const al = wbPentAlive(T), sh = (st.shed || []).map(k => WB[k].el); if (G.elePrev && !wbFusedIn(st).length) al.push(...WB_EL.map(k => WB[k].el).filter(x => !al.includes(x)));
  if (M.al == null) b.setAlive(al); else if (M.al !== al.join()) { for (const el of M.al.split(",")) if (el && !al.includes(el) && sh.includes(el)) b.shed(el); b.setAlive(al); } M.al = al.join();
  const watch = G.fuseRep || (G.wbScan && G.wbScan.key === "epx");
  if (!M.dk) { M.dk = {}; for (const k of fz.order) if (fz.dock[WB[k].el] >= .999) M.dk[k] = 1; M.fw = fz.form; }
  for (const k of fz.order) if (!M.dk[k] && fz.dock[WB[k].el] >= .999) { M.dk[k] = 1; if (watch) advHolo(`${WB[k].n} joins the Convergence!`); }
  if (M.fw < .99 && fz.form >= .99 && watch) convCard(); M.fw = fz.form; }
/* the title card as the arena ignites: the owner's key art */
function convCard() { let el = $("#convcard"); if (el) el.remove(); el = document.createElement("div"); el.id = "convcard"; el.innerHTML = `<img src="${BOSS_ART.conv}" alt="The Convergence">`; $("#app").appendChild(el); setTimeout(() => el.classList.add("on"), 30); setTimeout(() => el.classList.remove("on"), 4600); setTimeout(() => el.remove(), 6000); }
/* the core shattered: shards rain across the galaxy for ten minutes */
function convRain(W, t, T, st) { const on = st.dead && st.dead.epx && T - st.dead.epx < 10 * 60e3 && stCyc(st, "epx") === wbCyc2(T);
  if (!on) { if (W.convRain) { W.scene.remove(W.convRain); W.convRain.geometry.dispose(); W.convRain = null; } return; }
  if (!W.convRain) { const n = 360, g = new TH.BufferGeometry(), P = new Float32Array(n * 3), C = new Float32Array(n * 3), cols = WB_EL.map(k => new TH.Color(WB[k].col));
    for (let i = 0; i < n; i++) { const a = Math.random() * TAU, r = 20 + Math.sqrt(Math.random()) * 150; P[i * 3] = Math.cos(a) * r; P[i * 3 + 1] = Math.random() * 120; P[i * 3 + 2] = Math.sin(a) * r; const c = cols[i % 5]; C[i * 3] = c.r * 2; C[i * 3 + 1] = c.g * 2; C[i * 3 + 2] = c.b * 2; }
    g.setAttribute("position", new TH.BufferAttribute(P, 3)); g.setAttribute("color", new TH.BufferAttribute(C, 3)); W.convRain = new TH.Points(g, new TH.PointsMaterial({ size: 2.4, vertexColors: true, transparent: true, opacity: .9, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false }));
    W.convRain.frustumCulled = false; W.scene.add(W.convRain); W.convRain.userData.t = t; }
  const P = W.convRain.geometry.attributes.position.array, dt = Math.min(.1, (t - W.convRain.userData.t) / 1000); W.convRain.userData.t = t; for (let i = 1; i < P.length; i += 3) { P[i] -= dt * (14 + (i % 7) * 3); if (P[i] < 0) P[i] += 120; } W.convRain.geometry.attributes.position.needsUpdate = true;
  W.convRain.material.opacity = .9 * Math.min(1, (st.dead.epx + 10 * 60e3 - T) / 60e3); }
/* the galaxy takes the colours of the elements still loose while the Convergence is on */
function convTint(W, T) { const a = W.scene && W.scene.userData.amb; if (!a) return; if (!a.userData.base) a.userData.base = a.color.clone(); const base = a.userData.base;
  let tgt = base; if (wbGroupOn(3, T)) { const st = wbState(T), L = wbOn("epx", T) ? wbPentLive(st) : WB_EL.filter(k => st.hp[k] > 0); if (L.length) { const c = new TH.Color(0, 0, 0); for (const k of L) c.add(new TH.Color(WB[k].col)); c.multiplyScalar(1 / L.length); tgt = base.clone().lerp(c, .38); } }
  a.color.lerp(tgt, .02); }
function wbMapFree(W) {""")
rep("  try { wbScanFx(W, t); wbScarFx(W, t, T); } catch (e) {}", "  try { wbScanFx(W, t); wbScarFx(W, t, T); convRain(W, t, T, st); convTint(W, T); } catch (e) {}")
# the replay: the Pentarch as it was in that fight; a lower arena
rep("WBR.b = BOSS3D.prep(BOSS3D[m3](WB[key].el || (key === \"epx\" ? wbPentAlive(now()) : undefined)), wbEnv(WBR.r));", "WBR.b = BOSS3D.prep(BOSS3D[m3](WB[key].el || (key === \"epx\" ? ((battle && battle.r && battle.r.pent) || wbPentAlive(now())) : undefined)), wbEnv(WBR.r)); if (key === \"epx\") { WBR.b.ground = 16; WBR.shedQ = battle && battle.r && battle.r.shed ? battle.r.shed.map(k => WB[k].el) : null; }")
rep("    WBR.b.tick(t); WBR.r.render(WBR.sc, WBR.cam); return WBR.r.domElement; } catch (e) { return null; } }", "    if (WBR.shedQ && b && b.hp < .5) { for (const el of WBR.shedQ) WBR.b.shed(el); WBR.shedQ = null; } /* v402: the wing this fight tore loose breaks mid-battle */\n    WBR.b.tick(t); WBR.r.render(WBR.sc, WBR.cam); return WBR.r.domElement; } catch (e) { return null; } }")
# stained zones: the Pentarch's in the colours that remain
rep("""for (const k of [...WB_EL, "epx"]) if (wbUp(k, T)) { const q = wbPos(k, T, {}), R = k === "epx" ? 95 : 70; z.push({ x: q.x, z: q.z, r2: R * R, c: new TH.Color(...WB_STAIN[k]) }); }""",
    """for (const k of [...WB_EL, "epx"]) if (wbUp(k, T)) { const q = wbPos(k, T, {}), R = k === "epx" ? 95 : 70; let c = new TH.Color(...WB_STAIN[k]); if (k === "epx") { const L = wbPentLive(wbState(T)); if (L.length) { c = new TH.Color(0, 0, 0); for (const e of L) c.add(new TH.Color(...WB_STAIN[e])); c.multiplyScalar(1 / L.length); } } z.push({ x: q.x, z: q.z, r2: R * R, c }); }""")

# ---------- the five-pip band ----------
rep("""function eventsBadge() {""", """/* v402 the Convergence band: five pips, one per element, dark when it falls */
function convBand() { if (!S || !G.ready) return ""; const T = now(), on3 = wbGroupOn(3, T), nx = wbGroupNext(3, T); if (!on3 && nx - T > 864e5) return "";
  const st = wbState(T), ph2 = wbOn("epx", T), live = ph2 ? wbPentLive(st) : WB_EL.filter(k => st.hp[k] > 0), fuseAt = wbLiveEnd("eic", T);
  const pips = WB_EL.map(k => `<i class="${on3 && !live.includes(k) ? "off" : ""}" style="--c:${WB[k].col}"></i>`).join("");
  const txt = !on3 ? `begins in <i data-end="${nx}">${ftime(nx - T)}</i>` : ph2 ? (wbSwept(T) ? "Clean Sweep! It never formed" : st.hp.epx > 0 ? `The Pentarch · ${Math.round(st.hp.epx / WB_SEG * 100)}% hull` : "The Pentarch has fallen") : `${live.length} of 5 standing · fusion in <i data-end="${fuseAt}">${ftime(fuseAt - T)}</i>`;
  return `<button class="convband${on3 ? " live" : ""}" data-act="events" data-ev="eboss"><span class="cvp">${pips}</span><b>THE CONVERGENCE</b><span>${txt}</span></button>`; }
function eventsBadge() {""")
rep("${callBand()}${cubeBand()}${banner}", "${callBand()}${cubeBand()}${convBand()}${banner}")
rep(".cubeband{display:flex;", ".convband{display:flex;align-items:center;gap:8px;width:100%;padding:5px 12px;border:0;border-top:1px solid #4a2a7a;background:linear-gradient(90deg,rgba(180,120,255,.2),rgba(14,8,26,.92) 55%);color:#eadcff;font-size:12px;text-align:left;cursor:pointer}.convband b{font-family:var(--f-display);letter-spacing:.06em;color:#f2e8ff}.convband i{font-style:normal}.cvp{display:flex;gap:3px}.cvp i{width:9px;height:9px;border-radius:50%;background:var(--c);box-shadow:0 0 6px var(--c)}.cvp i.off{background:#2a2a34;box-shadow:none}#convcard{position:fixed;inset:0;z-index:60;display:grid;place-items:center;pointer-events:none;opacity:0;transition:opacity 1.1s;background:radial-gradient(rgba(0,0,0,.55),rgba(0,0,0,.2))}#convcard.on{opacity:1}#convcard img{width:min(78vw,420px);border-radius:14px;box-shadow:0 0 60px rgba(200,160,255,.55)}.aimrow{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}.aimb{position:relative;overflow:hidden;flex:1 1 30%;min-height:38px;border-radius:10px;border:1px solid var(--c,#b8a8e0);background:rgba(20,14,34,.8);color:#eee;font-size:12px;cursor:pointer}.aimb.on{background:color-mix(in srgb,var(--c,#b8a8e0) 30%,#140e22);box-shadow:0 0 10px var(--c,#b8a8e0)}.aimb span{position:relative;z-index:1}.aimb i{position:absolute;left:0;bottom:0;height:3px;background:var(--c)}.cubeband{display:flex;")
rep("@media (max-height:600px){.cubeband{display:none!important}", "@media (max-height:600px){.cubeband,.convband{display:none!important}")

# ---------- the Advisor: countdown, docking, shedding, shards, Clean Sweep ----------
rep('const ADV_NEWS = {', 'const ADV_NEWS = {"wb3_soon": "Commander, the Elementals are gathering at the Void. The Convergence begins in ten minutes. Watch it, or strike now while they are apart.", "wb3_sweep": "Commander, a Clean Sweep! All five Elementals fell before the fusion, and the Convergence never formed. Everyone who fought them can claim the spoils.", "wb3_shards": "Commander, the Pentarch\'s core has shattered! Its shards are raining across the galaxy. Gather them before they fade.", "wb_shed_eic": "Commander, Glacius has been torn loose from the Pentarch! Its frost is gone from the Convergence.", "wb_shed_efi": "Commander, Ignis has been torn loose from the Pentarch! Its fire is gone from the Convergence.", "wb_shed_eli": "Commander, Solara has been torn loose from the Pentarch! Its light is gone from the Convergence.", "wb_shed_est": "Commander, Voltaris has been torn loose from the Pentarch! Its storm is gone from the Convergence.", "wb_shed_ena": "Commander, Verdanth has been torn loose from the Pentarch! Its green is gone from the Convergence.", ')
rep("""  if (odd && T - s2 >= WB_FUSE && T - s2 < WB_FUSE + 3 * 3600e3) advNews("wb3_fuse", "wb3f:" + c2, { act: "cineObj", id: "wb_epx" }, "Watch the fusion"); }""",
"""  if (odd && T - s2 >= WB_FUSE - 10 * 60e3 && T - s2 < WB_FUSE) advNews("wb3_soon", "wb3s:" + c2, { act: "events", ev: "eboss" }, "The Convergence");
  if (odd && T - s2 >= WB_FUSE && T - s2 < WB_FUSE + 3 * 3600e3) { if (wbSwept(T)) advNews("wb3_sweep", "wb3w:" + c2, { act: "events", ev: "eboss" }, "Claim"); else advNews("wb3_fuse", "wb3f:" + c2, { act: "cineObj", id: "wb_epx" }, "Watch the fusion"); }
  if (odd) { const st = wbState(T); if (st.dead.epx && T - st.dead.epx < 10 * 60e3) advNews("wb3_shards", "wb3x:" + c2, { act: "convShards" }, "Gather shards"); } }""")
rep("""function wbNews(prev, st) { if (!prev) return;""", """function wbNews(prev, st) { if (!prev) return; if (prev.cyc2 === st.cyc2) for (const k of st.shed || []) if (!(prev.shed || []).includes(k)) advNews("wb_shed_" + k, `shed:${st.cyc2}:${k}`, { act: "cineObj", id: "wb_epx" }, "Watch");""")
# Clean Sweep: everyone who fought an Elemental claims once
rep("""function wbClaim() { if (!S || !G.ready) return; const st = wbState(), c0 = st.cyc; S.wbGot = S.wbGot || {};""", """function wbClaim() { if (!S || !G.ready) return; const st = wbState(), c0 = st.cyc; S.wbGot = S.wbGot || {};
  if (wbSwept(now()) && !S.wbGot["sweep:" + st.cyc2] && WB_EL.some(k => ((st.dmg[k] || {})[G.me] || 0) > 0)) { S.wbGot["sweep:" + st.cyc2] = 1; S.medals = S.medals || {}; S.medals.sweep = (S.medals.sweep || 0) + 1; S.shards = (S.shards || 0) + 40; giveItem("teleport");
    logReward("Clean Sweep · the Convergence", null, { shards: 40, item: "teleport", kind: "battle" }); note(`Clean Sweep! All five Elementals fell before the fusion. Your reward: ◆40, a Teleport Ticket and the Clean Sweep medal (×${S.medals.sweep}).`, "win"); dirty(); }""")

# ---------- the event page: the art, the replay, the rules ----------
rep("""Object.assign(BOSS_ART, BOSS_ART_EL);""", """Object.assign(BOSS_ART, BOSS_ART_EL, """ + json.dumps(ART) + """); // v402 the owner's Convergence art: the banner, the Pentarch's portrait, the title card""")
rep("""  const rules = g === 3 ? `The Elemental Convergence comes every other Wednesday at 18:00 UTC, for 48 hours. For the first 24 hours the five Elementals, Glacius, Ignis, Solara, Voltaris and Verdanth, tear into the galaxy, staining the worlds around them with their element. Then the survivors fly to the black hole at the centre and fuse into the Pentarch, and for the last 24 hours it tears at the Void. Every Elemental slain before the fusion is missing from the Pentarch, and it is that much weaker. Every 2.5% of hull you destroy scores 3 Hunt points, or 6 on the Pentarch, and every attack pays a bounty and drops forge materials.` :""",
    """  const rules = g === 3 ? `The Elemental Convergence comes every other Wednesday at 18:00 UTC, for 48 hours. For the first 24 hours the five Elementals, Glacius, Ignis, Solara, Voltaris and Verdanth, tear into the galaxy, staining the worlds around them with their element. Then the survivors fly to the black hole at the centre and fuse into the Pentarch, and for the last 24 hours it tears at the Void. Every Elemental slain before the fusion is dark in the Pentarch, and it is that much weaker; slay all five and it never forms: a Clean Sweep, with a medal for everyone who fought. At every fifth of its hull the Pentarch tears one element loose, and you can aim at a wing to break it sooner. When it falls its core shatters into shards: gather them within ten minutes. Every 2.5% of hull you destroy scores 3 Hunt points, or 6 on the Pentarch, and every attack pays a bounty and drops forge materials.` :""")
rep("""<small>${!live ? `Every ${E.day} 18:00 UTC, for 48 hours` : g === 3 ? (wbOn("epx", T) ? (st.hp.epx > 0 ? "The Pentarch tears at the Void. Bring it down!" : "The Pentarch has fallen. The Void is saved.")""",
    """<small>${!live ? `Every ${E.day} 18:00 UTC, for 48 hours` : g === 3 ? (wbOn("epx", T) ? (wbSwept(T) ? "Clean Sweep! The Convergence never formed." : st.hp.epx > 0 ? `The Pentarch tears at the Void: ${wbPentLive(st).length} of 5 elements still in it. Bring it down!` : "The Pentarch has fallen. The Void is saved.")""")
rep("""  const cons = g !== 1 ? "" :""", """  const cons = g === 3 ? `<button class="btn ghost wide" data-act="convReplay" style="margin:6px 0">▶ Watch the fusion${wbOn("epx", T) ? "" : " (preview)"}</button>${S.medals && S.medals.sweep ? `<p class="note">🏆 Clean Sweep medal ×${S.medals.sweep}</p>` : ""}` : g !== 1 ? "" :""")
rep("""d: "The Elementals fused into one, tearing at the black hole at the centre of the galaxy. Every Elemental slain before the fusion is missing from it, and it is that much weaker." } });""",
    """d: "The Elementals fused into one titan, tearing at the black hole at the centre of the galaxy. Every Elemental slain before the fusion is dark in it. At every fifth of its hull it tears an element loose; aim at a wing to break it sooner." } });""")
rep("""["What is the Elemental Convergence?", "Every other Wednesday at eighteen hundred UTC, five Elementals tear through the Void for forty-eight hours. For the first day they stain the worlds around them with their element. Then the survivors fuse into the Pentarch above the black hole. Every Elemental we slay before the fusion is missing from the Pentarch, so hunt them early."]""",
    """["What is the Elemental Convergence?", "Every other Wednesday at eighteen hundred UTC, five Elementals tear through the Void for forty-eight hours. For the first day they stain the worlds around them with their element. Then the survivors fuse into the Pentarch above the black hole. Every Elemental we slay first is dark in it, and if all five fall it never forms. In the fight, it tears an element loose at every fifth of its hull, and aiming at a wing breaks it sooner."]""")

# ---------- the Convergence theme: a layer per element, each falling silent as its element falls ----------
rep("""function applyAudio() {""", """/* v402 the Convergence theme, generated: a drum and drone always, and one layer per element (ice bells, fire brass, a choir of light,
   a storm arpeggio, a nature pluck). It plays while you watch the Convergence (a scan, the fusion, a replay of its battles), under
   your own track, and each element's layer drops out when that element falls. */
function convWant() { if (!AU.ctx || !AU.musicOn || AU.muted || document.hidden) return null; const k = G.wbScan && G.wbScan.key, rb = typeof battle !== "undefined" && battle && battle.r && battle.r.wb;
  if (!(G.fuseRep || (k && wbG3(k)) || (rb && wbG3(rb)))) return null; const st = wbState(), T = now(); return wbOn("epx", T) || k === "epx" || rb === "epx" || G.fuseRep ? (wbPentLive(st).length || G.elePrev ? (G.elePrev && !wbFusedIn(st).length ? WB_EL : wbPentLive(st)) : []) : WB_EL.filter(x => st.hp[x] > 0 || G.elePrev); }
function convTheme() { const want = convWant(), c = AU.ctx; if (!c) return;
  if (!want) { if (AU.conv) { const C = AU.conv; AU.conv = null; C.out.gain.setTargetAtTime(0, c.currentTime, .6); setTimeout(() => { clearInterval(C.iv); C.stop.forEach(o => { try { o.stop(); } catch (e) {} }); try { C.out.disconnect(); } catch (e) {} }, 3000); AU.cduck = 1; applyAudio(); } return; }
  if (!AU.conv) { const out = c.createGain(); out.gain.value = 0; out.connect(AU.master); const L = {}, stop = []; for (const k of WB_EL) { L[k] = c.createGain(); L[k].gain.value = 0; L[k].connect(out); }
    const base = c.createGain(); base.gain.value = 1; base.connect(out); const mt = m => 440 * Math.pow(2, (m - 69) / 12);
    const dr = c.createOscillator(); dr.frequency.value = mt(26); const dg = c.createGain(); dg.gain.value = .16; dr.connect(dg); dg.connect(base); dr.start(); stop.push(dr);
    const ch = [62, 65, 69, 74].map(m => { const o = c.createOscillator(), g = c.createGain(); o.type = "sine"; o.frequency.value = mt(m + 12); g.gain.value = .035; o.connect(g); g.connect(L.eli); o.start(); stop.push(o); return o; }); // the choir of light: a held high chord
    const blip = (dest, type, f, v, d, t, f2) => { const o = c.createOscillator(), g = c.createGain(); o.type = type; o.frequency.setValueAtTime(f, t); if (f2) o.frequency.exponentialRampToValueAtTime(f2, t + d); g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(v, t + .01); g.gain.exponentialRampToValueAtTime(.0001, t + d); o.connect(g); g.connect(dest); o.start(t); o.stop(t + d + .05); };
    let s = 0; const scale = [50, 53, 57, 60, 62, 65, 69, 72];
    const iv = setInterval(() => { if (document.hidden) return; const t = c.currentTime + .05, b = s % 16;
      if (b % 4 === 0) blip(base, "sine", 110, .5, .35, t, 40); if (b === 14) blip(base, "sine", 160, .3, .25, t, 70); // the drum
      if (b === 0 && s % 32 === 0) [38, 45].forEach(m => blip(L.efi, "sawtooth", mt(m), .09, 1.6, t)); if (b === 8) blip(L.efi, "sawtooth", mt(41), .07, .9, t);
      if (b % 2 === 1) blip(L.eic, "sine", mt(scale[(s * 5) % 8] + 24), .05, 1.4, t);
      blip(L.est, "square", mt(scale[(s * 3) % 8] + 12), .025, .14, t); if (b % 2 === 0) blip(L.est, "square", mt(scale[(s * 3 + 2) % 8] + 12), .02, .12, t + .15);
      if ([0, 3, 6, 10, 12].includes(b)) blip(L.ena, "triangle", mt(scale[(s + b) % 8]), .09, .45, t);
      s++; }, 300);
    AU.conv = { out, L, iv, stop }; out.gain.setTargetAtTime(.15, c.currentTime, 1.2); AU.cduck = .2; applyAudio(); }
  const C = AU.conv, t = c.currentTime, v = AU.musicOn && !AU.muted ? gainOf(AU.mv) / gainOf(50) : 0; C.out.gain.setTargetAtTime(.15 * v, t, .8);
  for (const k of WB_EL) C.L[k].gain.setTargetAtTime(want.includes(k) ? 1 : 0, t, 1.2); }
setInterval(() => { try { convTheme(); } catch (e) {} }, 1000);
function applyAudio() {""")
rep("AU.mus.gain.setTargetAtTime(AU.musicOn ? .1 * gainOf(AU.mv) / gainOf(50) * (AU.duck || 1) : 0,", "AU.mus.gain.setTargetAtTime(AU.musicOn ? .1 * gainOf(AU.mv) / gainOf(50) * (AU.duck || 1) * (AU.cduck || 1) : 0,")
rep("* (.1 * gainOf(AU.mv) / gainOf(50)) * 1.6 * (AU.duck || 1), 0, 1);", "* (.1 * gainOf(AU.mv) / gainOf(50)) * 1.6 * (AU.duck || 1) * (AU.cduck || 1), 0, 1);")
t = t.replace("const GAME_V = 401;", "const GAME_V = 402;")
open(p, "w").write(t); print("ok")
# (applied after) coordStr for world bosses (no orbit angle: NaN); the Convergence row in the boss card spans the full width (a long line squeezed the labels to one letter)
# (applied after) the Pentarch on the map: sc .72 (it filled a scan); pieces fly in from 95 units out, where the Elementals roamed
# (applied after) the band reads 'Fusing · n of m joined' during the fusion
