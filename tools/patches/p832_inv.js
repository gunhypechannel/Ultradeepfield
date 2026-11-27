/* ---------- v832 the invasion pages remastered, and the Finder's Nearest strip (owner: "simplify the invasion events pages and refine them
   even more to be more addictive, visually pleasing and simple. uses glow and elemental effects whenever we can, in addition to finding the
   closes interaction we enhance the finder. in the invasion menus it should use more art or 3d models with glow no spinning", then "build it
   all"). Each invasion page keeps all of its content, now in the Events layout: its banner as a living hero in its own element (the Mimic
   cyan circuitry, the Carcinid rising tide, the Continuum crimson sparks), a line toward the next reward, and five tabs: Overview · How to
   Play · Rewards · Forge · Enemies (the enemies as still, glowing renders). How to Play has a Take me there that flies to the nearest live
   target of that invasion. The Finder opens with a Nearest strip: the closest target of each kind, its distance and flight time, Go, and
   Next for the one after it. ---------- */
const INVX = {
  mimic: { el: "circuit", c1: "#5fd8ff", c2: "#d4f6ff", pts: "invasion points", set: () => MIM_HIVES,
    s: [["⬢", "Hives appear", "Mimic hives open in the empty sectors, a new stage each week of the season."], ["⚔", "Burn the hives", "Every hive pays Mimic Tissue and invasion points. Mature hives also give up Assimilated Alloy and Neural Core Fragments."], ["▼", "Suppress the swarm", "Everyone's points add to Hive Suppression. At the finale it cuts Omega's shields, regeneration and swarm."], ["🎁", "Forge and claim", "Spend materials in the Mimic Forge, and claim the reward track as your points grow."]],
    p: [["Every hive", "Mimic Tissue + points"], ["Mature hives", "Alloy and Neural Cores"], ["Your daily contribution", "up to 400"]],
    tip: "Every hive you burn weakens Omega for everyone, Commander. Suppression is a team effort." },
  carcinid: { el: "tide", c1: "#ff8a5a", c2: "#ffe0b0", pts: "tide points", set: () => [].concat(CRC_NESTS || [], CRC_PATS || [], CRC_KRAK || [], CRC_BOSSES || []),
    s: [["🌊", "The tide rises", "The Carcinid come up through Breach Zones, stage by stage over the season."], ["⚔", "Hold the breach", "Every Breach Zone and scout patrol you beat pays tide points and materials."], ["🦀", "Break the great ones", "Deep Guardians, Claw Admirals and the Abyssal Crown carry the rarest materials."], ["🎁", "Forge and claim", "Spend materials in the Abyssal Forge, and claim the reward track."]],
    p: [["Every Breach Zone", "Abyssal Chitin"], ["Stage 2+ Breach Zones", "Coral Alloy"], ["Scout patrols", "Tidal Resin"], ["Claw Admirals", "Emperor Shell"], ["The Abyssal Crown", "Crown Reactor Shard"]],
    tip: "The rarest materials ride with the great ones, Commander. The Claw Admirals and the Crown are worth the fight." },
  cnt: { el: "war", c1: "#ff3346", c2: "#ffc0b8", pts: "war points", set: () => [].concat(CNT_NET || [], CNT_PATS || [], CNT_PLATS || [], CNT_PX ? [CNT_PX] : []),
    s: [["⬢", "Destroy their fleets", "Every Continuum fleet destroyed buys time and pays war points."], ["☢", "Hunt the Arks", "Their commanders come back at Resurrection Arks. Destroying the Arks wins the war."], ["⚡", "Cut the network", "Platforms and relays carry the transfer. Without them, a dying commander dies for good."], ["🎁", "Forge and claim", "Spend war materials in the Continuum Forge, and claim the war reward track."]],
    p: [["Anything you destroy", "Neural Echoes"], ["Patrols and platforms", "Machine Alloy"], ["Platforms and relays", "Circuitry"], ["Arks", "Reactor Cells, Resurrection Cores"], ["Commanders", "Quantum Neural Matrices"]],
    tip: "Destroying their fleets buys time, Commander. Destroying their Arks wins the war." } };
EV_HOW.mimic = { tip: INVX.mimic.tip }; EV_HOW.carcinid = { tip: INVX.carcinid.tip }; EV_HOW.cnt = { tip: INVX.cnt.tip }; /* her tips play through evxTip */
/* the nearest live target of a set, from your current world */
function invNearest(list, skip) { try { const T = now(), h = originPlanet() || homePlanet(); if (!h) return null; const a = pos(h, T);
  const L = (list || []).filter(x => x && PB[x.id] && pirDown(x) <= T && !isFogged(x, T)).map(x => { const b = pos(x, T); return [x, Math.hypot(a.x - b.x, a.y - b.y)]; }).sort((p, q) => p[1] - q[1]);
  return L.length ? L[(skip || 0) % L.length] : null; } catch (e) { return null; } }
function invPage(k, html) { const X = INVX[k]; if (!X) return html; G.invTab = G.invTab || {}; S.evHow = S.evHow || {};
  if (!S.evHow["i_" + k]) { S.evHow["i_" + k] = 1; dirty(); G.invTab[k] = "how"; } const tab = G.invTab[k] || "ov";
  const ci = html.indexOf('data-act="close"'), he = ci < 0 ? 0 : html.indexOf("</div>", ci) + 6, hd = html.slice(0, he);
  const b0 = html.indexOf('<div class="mimban', he), b1 = b0 < 0 ? -1 : html.indexOf("</div></div>", b0) + 12, ban = b0 < 0 ? "" : html.slice(b0, b1);
  const h3 = html.indexOf("<h3>", he), head = (b0 < 0 ? html.slice(he, h3 < 0 ? html.length : h3) : html.slice(he, b0) + html.slice(b1, h3 < 0 ? html.length : h3));
  const secs = { ov: [head], rw: [], fg: [], en: [] }; let rest = h3 < 0 ? "" : html.slice(h3);
  for (const part of rest.split("<h3>").filter(x => x.trim())) { const t = part.slice(0, part.indexOf("</h3>")), s = "<h3>" + part;
    (/reward track/i.test(t) ? secs.rw : /forge|materials/i.test(t) ? secs.fg : /swarm|empire|fleet/i.test(t) ? secs.en : secs.ov).push(s); }
  const nm = (rest.match(/<h3>[^<]*reward track<\/h3><p class="note">([^<.]*)/i) || [])[1] || "", near = invNearest(X.set());
  const go = near ? `<button class="btn amber wide evx-go" data-act="pirate" data-id="${near[0].id}">Take me there · ${esc(near[0].name || "the nearest target")} · ${fmt(Math.round(near[1]))} away ›</button>` : `<button class="btn ghost wide evx-go" disabled style="white-space:normal">Nothing on the map yet</button>`;
  const how = `<div class="evx-how"><div class="evx-steps">${X.s.map(([ic, t, x], i) => `<div class="evx-step" style="--i:${i}"><span class="evx-sn">${i + 1}</span><span class="evx-si">${ic}</span><div><b>${esc(t)}</b><p>${esc(x)}</p></div></div>`).join("")}</div>${go}
    <h4 class="evx-h4">What you earn</h4><div class="evx-pts">${X.p.map(([a, b]) => `<div><span>${esc(a)}</span><b>${esc(b)}</b></div>`).join("")}</div>
    <button class="evx-tip" data-act="evxTip" data-k="${k}"><i class="evx-face" style="background-image:url('${advArt()}')"></i><span><small>${ADV} · tip</small>${esc(X.tip)}</span><u>🔊</u></button></div>`;
  const T = [["ov", "Overview"], ["how", "How to Play"], ["rw", "Rewards"], ["fg", "Forge"], ["en", "Enemies"]];
  const body = tab === "how" ? how : (secs[tab] || secs.ov).join("");
  return `${hd}<div class="evx invx" data-el="${X.el}" style="--x1:${X.c1};--x2:${X.c2}"><div class="evx-hero invh"><canvas class="evx-fx" aria-hidden="true"></canvas>${ban}<i class="evx-sweep"></i></div>${nm ? `<div class="evx-nudge"><b>${esc(nm.trim())}</b> so far · every one counts toward the reward track</div>` : ""}
    <div class="evtabs evx-tabs invt">${T.map(([v, l]) => `<button class="${tab === v ? "on" : ""}" data-act="invTab" data-k="${k}" data-v="${v}">${l}</button>`).join("")}</div><div class="evx-body t-${tab}">${body}</div></div>`; }
{ const b = shMimic; shMimic = function () { const h = b.apply(this, arguments); try { return invPage("mimic", h); } catch (e) { return h; } }; }
{ const b = shCarcinid; shCarcinid = function () { const h = b.apply(this, arguments); try { return invPage("carcinid", h); } catch (e) { return h; } }; }
{ const b = shCnt; shCnt = function () { const h = b.apply(this, arguments); try { return invPage("cnt", h); } catch (e) { return h; } }; }
/* the Finder's Nearest strip: the closest target of each kind */
const NEAR_K = [["x", "☠", "Pirates", "#ff6b5a", "pirate", T => PIRATES.filter(x => !x.boss && !x.mon && pirDown(x) <= T)], ["w", "🦈", "Monsters", "#7fd4ff", "pirate", T => PIRATES.filter(x => x.mon && pirDown(x) <= T)],
  ["q", "■", "Boss Cubes", "#5dff6a", "pirate", T => PIRATES.filter(x => x.boss && !x.mon && pirDown(x) <= T)], ["y", "▲", "Treasure", "#ffd36b", "pyramid", T => PYRAMIDS.filter(y => pyrDown(y) <= T)],
  ["m", "⛏", "Gather", "#5dff9a", "node", T => NODES.filter(x => x.res !== "s" && !occOf(x.id, T))], ["s", "◆", "Shard Mines", "#c890ff", "node", T => NODES.filter(x => x.res === "s" && !shardRest(x))],
  ["h", "⬢", "Hive Worlds", "#f0a945", "planet", T => G.list.filter(p => pStatus(p, T) === "hive")], ["d", "♻", "Salvage", "#9fe8d8", "planet", T => G.list.filter(p => p.debris && (p.debris.m || 0) + (p.debris.c || 0) > 0)]];
function nearStrip() { try { const T = now(), h = originPlanet() || homePlanet(); if (!h) return ""; const a = pos(h, T), I = G.nearI || (G.nearI = {}), sh = {}; for (const k in S.ships || {}) if (S.ships[k] && SH[k]) sh[k] = S.ships[k];
  const cards = NEAR_K.map(([r, ic, nm, col, act, f]) => { let L = []; try { L = f(T).filter(x => !isFogged(x, T)).map(x => { const b = pos(x, T); return [x, Math.hypot(a.x - b.x, a.y - b.y)]; }).sort((p, q) => p[1] - q[1]).slice(0, 8); } catch (e) {} if (!L.length) return "";
    const i = (I[r] || 0) % L.length, [x, d] = L[i]; let ms = 0; try { ms = Object.keys(sh).length ? travelMs(h, x, sh) : 0; } catch (e) {}
    return `<div class="nrc" style="--nc:${col}"><div class="nrt"><span class="nri">${ic}</span><b>${nm}</b><small>${i + 1}/${L.length}</small></div><div class="nrn">${esc(x.name || "")}${x.lvl ? ` · Lv.${x.lvl}` : ""}</div><div class="nrd">${fmt(Math.round(d))} away${ms ? ` · ✈ ${ftime(ms)}` : ""}</div><div class="nrb"><button class="btn amber sm" data-act="${act}" data-id="${x.id}">Go ›</button>${L.length > 1 ? `<button class="btn ghost sm" data-act="nearNext" data-r="${r}">Next</button>` : ""}</div></div>`; }).join("");
  return cards ? `<div class="nrst"><div class="nrh">◎ Nearest to ${esc(h.name || "you")}</div><div class="nrrow">${cards}</div></div>` : ""; } catch (e) { return ""; } }
{ const b = shFind; shFind = function () { const h = b.apply(this, arguments); try { if ((G.find || "m") === "o") return h; const ci = h.indexOf('data-act="close"'), j = ci < 0 ? -1 : h.indexOf("</div>", ci); return j < 0 ? h : h.slice(0, j + 6) + nearStrip() + h.slice(j + 6); } catch (e) { return h; } }; }
setTimeout(() => Object.assign(ACT, {
  invTab: d => { (G.invTab = G.invTab || {})[d.k] = d.v; if (sheet) renderSheet(); },
  nearNext: d => { const I = G.nearI || (G.nearI = {}); I[d.r] = (I[d.r] || 0) + 1; if (sheet) renderSheet(); } }), 0);
{ const st = document.createElement("style"); st.textContent = `
.invx .evx-tabs button{font-size:11.5px;padding-left:2px;padding-right:2px}.invh .mimban{margin:0;border-radius:0}.invh .mimban img{filter:saturate(1.15) contrast(1.05)}
.invx .mimcls{display:grid;grid-template-columns:1fr;gap:10px}.invx .mimcl{position:relative;display:flex;gap:10px;align-items:center;padding:8px;border-radius:14px;background:radial-gradient(120% 140% at 0% 50%,color-mix(in srgb,var(--x1) 22%,transparent),rgba(0,0,0,.25) 60%);border:1px solid color-mix(in srgb,var(--x1) 40%,transparent);box-shadow:0 0 14px color-mix(in srgb,var(--x1) 18%,transparent)}
.invx .mimcl canvas{flex:0 0 46%;max-width:46%;height:auto;filter:drop-shadow(0 0 10px var(--x1)) drop-shadow(0 0 2px var(--x2))}.invx .mimcl b{color:#fff;text-shadow:0 0 8px var(--x1)}.invx .mimcl em{color:var(--x1);font-style:normal;font-size:11px}
.invx .mimmat{border-color:color-mix(in srgb,var(--x1) 35%,transparent)!important;box-shadow:inset 0 0 12px color-mix(in srgb,var(--x1) 12%,transparent)}.invx .mimmat img,.invx .mimmat i{filter:drop-shadow(0 0 6px var(--x1))}
.invx .mimtc:not([disabled]){border-color:#ffd36b;box-shadow:0 0 14px rgba(255,211,107,.5);animation:evxReady 1.5s ease-in-out infinite}.invx .mimbar i{background:linear-gradient(90deg,var(--x1),var(--x2),var(--x1));background-size:200% 100%;box-shadow:0 0 10px var(--x1);animation:evxFlow 2.4s linear infinite}
.invx .crclore{border-color:color-mix(in srgb,var(--x1) 30%,transparent)}.invx .mimwk{border-color:color-mix(in srgb,var(--x1) 35%,transparent)}
.nrst{flex:0 0 auto;margin:4px 0 10px}.nrh{font:700 11px system-ui;letter-spacing:.12em;text-transform:uppercase;color:#8fe8ff;margin:0 2px 6px;text-shadow:0 0 8px rgba(95,216,255,.6)}
.nrrow{display:flex;gap:8px;overflow-x:auto;padding:2px 2px 8px;scrollbar-width:none}.nrrow::-webkit-scrollbar{display:none}
.nrc{flex:0 0 150px;display:flex;flex-direction:column;gap:4px;padding:9px;border-radius:14px;background:linear-gradient(180deg,color-mix(in srgb,var(--nc) 16%,transparent),rgba(0,0,0,.3));border:1px solid color-mix(in srgb,var(--nc) 45%,transparent);box-shadow:0 0 12px color-mix(in srgb,var(--nc) 20%,transparent)}
.nrt{display:flex;align-items:center;gap:6px}.nri{color:var(--nc);font-size:16px;filter:drop-shadow(0 0 5px var(--nc))}.nrt b{font-size:12.5px;color:#fff}.nrt small{margin-left:auto;font-size:10px;color:#8ea4b5}
.nrn{font-size:12px;color:#dfe8ef;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.nrd{font-size:11px;color:#9fb3c2}.nrb{display:flex;gap:6px;margin-top:2px}.nrb .btn{flex:1;padding-left:4px;padding-right:4px}`; document.head.appendChild(st); }
