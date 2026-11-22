/* ---------- v725 eggs, phases 2 and 3 (owner: "Build it all" ... "Finish") ----------
   - Growth: feed a creature to raise it from Hatchling to Juvenile (x1.25 its bonus) to Adult (x1.6); its portrait grows with it.
   - Companion: pick one creature. It flies beside your flagship's fleets on the map and fights in your battle reports, striking at
     the enemy every few seconds with its signature colour (visual only: the sim is untouched).
   - Collection rewards: every element whose wild species you have all hatched gives +1% to that element on top of the cap; the full
     wild collection gives +1% to every element more.
   - Your profile shows your companion and your Sanctuary to other commanders.
   - Event eggs: Cube Mimics (Cube Devastation) and Carcinids (the Season of the Cube's tide) can leave eggs of species found nowhere else.
   - Gifting: give an egg to a member of your alliance (three a day); they claim it from their Sanctuary.
   - The Serpent storyline's payoff: at 12 hatchlings killed one of them leaves an egg, at 30 the mother's own, a Prismatic. */
Object.assign(XS, { cubeling: ["spirit", 2, 0, 1], crcling: ["water", 2, 0, 1] }); // [element, rarity, breed-only, event-only]
const XS_EVN = { cubeling: ["Cube Mimicling", "#9cf6ff", "art/mon/mimic.webp?v=1"], crcling: ["Carcinid Hatchling", "#ff9a6a", "art/carcinid/drone.webp?v=1"] };
const xsEvSp = mon => mon === "mimic" ? "cubeling" : (typeof CRC_M !== "undefined" && CRC_M[mon]) ? "crcling" : null;
const XS_GROW = [["Hatchling", 1], ["Juvenile", 1.25], ["Adult", 1.6]];
const xsGrow = c => XS_GROW[clamp(c && c.g || 0, 0, 2)];
const xsFeedCost = c => { const r = XS[c.sp][1] + 1, g = (c.g || 0) + 1; return { m: 30000 * r * g, c: 20000 * r * g, g: 8000 * r * g }; };
const xsWild = () => Object.keys(XS).filter(k => !XS[k][2] && !XS[k][3]);
const xsBookDone = e => { const X = xsOf(), L = xsWild().filter(k => XS[k][0] === e); return L.length > 0 && L.every(k => X.seen[k]); };
const xsBookAll = () => { const X = xsOf(); return xsWild().every(k => X.seen[k]); };
const xsBookPct = e => (xsBookDone(e) ? 1 : 0) + (xsBookAll() ? 1 : 0);
const xsComp = () => { const X = xsOf(); return X.comp && X.hab.find(c => c.id === X.comp) || null; };
/* what other commanders see */
function xsPub() { try { const X = xsOf(), c = xsComp(); return { l: xsLvl(), n: X.hab.length, bk: Object.keys(XS).filter(k => X.seen[k]).length, c: c ? c.sp : "", cp: c && c.pr ? 1 : 0, cg: c ? c.g || 0 : 0, ct: c ? xsTr(c) : "" }; } catch (e) { return null; } }
function xsPubClean(v) { if (!v || typeof v !== "object") return null; return { l: okInt(v.l), n: okInt(v.n), bk: okInt(v.bk), c: XS[v.c] ? v.c : "", cp: v.cp ? 1 : 0, cg: clamp(okInt(v.cg), 0, 2), ct: XS_TR[v.ct] ? v.ct : "" }; }
function xsProfHTML(P, me) { const v = me ? xsPub() : P && P.xs; if (!v || !v.l) return ""; const c = v.c, r = c ? XR[XS[c][1]] : null;
  return `<h2 class="sec">Xeno Sanctuary</h2><div class="xsprof">${c ? `<div class="xscomp" style="--c:${xsCol(c)};--r:${r[1]}"><img src="${xsImg(c)}" alt=""><div><small>★ Companion</small><b>${v.cp ? "✦ " : ""}${esc(xsName(c))}</b><span>${XS_GROW[v.cg][0]} · ${r[0]}${v.ct ? " · " + XS_TR[v.ct][0] : ""}</span></div></div>` : ""}<p class="note">Sanctuary Lv.${v.l} · ${v.n} creature${v.n === 1 ? "" : "s"} · ${v.bk}/${Object.keys(XS).length} species discovered</p></div>`; }
/* gifting eggs inside the alliance (the alliance doc's xsg map) */
function xsgClean(o, members) { const r = {}; if (!o || typeof o !== "object") return r; for (const id in o) { const g = o[id]; if (!g || typeof g !== "object" || !members[g.by] || !members[g.to] || !XS[g.sp] || XS[g.sp][2]) continue; r[String(id).slice(0, 40)] = { by: g.by, to: g.to, at: +g.at || 0, sp: g.sp, pr: g.pr ? 1 : 0, c: g.c ? 1 : 0 }; } return r; }
const xsGiftsIn = () => { const a = myAlly(); if (!a) return []; const got = S.xsGot || {}, T = now(); return Object.entries(a.xsg || {}).filter(([id, g]) => g.to === G.me && !g.c && !got[id] && g.at > T - 14 * 864e5); };
const xsGiftsToday = () => (S.xsGiftT || []).filter(t => t > now() - 864e5).length;
function xsGiftHTML() { const a = myAlly(), X = xsOf(); let h = ""; const inc = xsGiftsIn();
  if (inc.length) h += `<div class="xsh"><b>Gifts from your alliance</b></div><div class="xsegs">${inc.map(([id, g]) => `<div class="xsegc">${xsEggHTML(g.sp, g.pr)}<div><b>${g.pr ? "✦ Prismatic " : ""}${esc(xsName(g.sp))}</b><small>from ${esc(nameOf(g.by))}</small></div><button class="btn sm amber" data-act="xsClaim" data-id="${esc(id)}" ${X.eggs.length < XS_EGGS ? "" : "disabled"}>Claim</button></div>`).join("")}</div>`;
  if (a && X.eggs.length) { const mem = Object.keys(a.members).filter(u => u !== G.me); if (mem.length) { const to = mem.includes(G.xsTo) ? G.xsTo : mem[0]; G.xsTo = to; const left = 3 - xsGiftsToday();
    h += `<div class="xsh"><b>Gift an egg</b><small>${left} left today</small></div><div class="xsgift"><select id="xsto" aria-label="Alliance member">${mem.map(u => `<option value="${esc(u)}"${u === to ? " selected" : ""}>${esc(nameOf(u))}</option>`).join("")}</select><div class="xsgl">${[...new Set(X.eggs.filter(e => !XS[e.sp][2]).map(e => e.sp + (e.pr ? "*" : "")))].map(key => { const sp = key.replace("*", ""), pr = key.endsWith("*");
      return `<button class="btn sm" data-act="xsGift" data-sp="${sp}" data-pr="${pr ? 1 : 0}" ${left > 0 ? "" : "disabled"}>${xsEggHTML(sp, pr)}<span>${pr ? "✦ " : ""}${esc(xsName(sp))}</span></button>`; }).join("")}</div></div>`; } }
  return h; }
/* growth, companion and gifts: the habitat card's extra buttons */
function xsCrExtra(c) { const X = xsOf(), g = c.g || 0, fc = g < 2 ? xsFeedCost(c) : null, comp = X.comp === c.id;
  return `<button class="btn sm${comp ? " amber" : ""}" data-act="xsComp" data-id="${c.id}">${comp ? "★ Companion" : "☆ Companion"}</button>${fc ? `<button class="btn sm" data-act="xsFeed" data-id="${c.id}" ${can(fc) ? "" : "disabled"} title="Feed: grows into a ${XS_GROW[g + 1][0]}">Feed</button>` : ""}`; }
const xsCrFeedNote = c => (c.g || 0) < 2 ? `<small class="xsfeed">Feed to grow into a ${XS_GROW[(c.g || 0) + 1][0]} (x${XS_GROW[(c.g || 0) + 1][1]}): ${costHTML(xsFeedCost(c))}</small>` : "";
/* the companion in battle: it hovers behind your line and strikes at the enemy */
function compBattle(ctx, b, scr, T, W, d, lo, t) { if (b.cpOff) return; if (b.cp === undefined) { b.cp = null; try { const r = b.r || {}, c = xsComp(); if (!c || r.test === 2) return; const mine = (r.aUids || []).includes(G.me) ? "a" : (r.dUids || []).includes(G.me) || r.dUid === G.me ? "d" : null; if (!mine) return;
      b.cp = { sp: c.sp, pr: c.pr, g: c.g || 0, side: mine, nx: 2.2, hits: [] }; } catch (e) { return; } } const cp = b.cp; if (!cp) return;
  const own = [], foe = []; b.Q.forEach((q, i) => { if (!q || !scr[i] || !(b.n[i] > 0)) return; (q.side === cp.side ? own : foe).push(i); }); if (!own.length) return;
  let ox = 0, oy = 0, ex = 0, ey = 0; for (const i of own) { ox += scr[i].x; oy += scr[i].y; } ox /= own.length; oy /= own.length; for (const i of foe) { ex += scr[i].x; ey += scr[i].y; } if (foe.length) { ex /= foe.length; ey /= foe.length; } else { ex = W / 2; ey = oy; }
  const dx = ex - ox, dy = ey - oy, dl = Math.hypot(dx, dy) || 1, L = clamp(W * .12, 36 * d, 84 * d) * (.85 + .15 * cp.g), bx = clamp(ox < W / 2 ? ox - W * .3 : ox + W * .3, Math.max(L * 1.3, 72 * d), W - Math.max(L * 1.3, 72 * d)) + Math.sin(t * .0016) * L * .08, by = oy - L * 1.8 + Math.sin(t * .0021) * L * .12, rgb = (BEAST_FX[cp.sp] || [160, 240, 255]).join(",");
  /* a strike every 3 s or so at a live enemy: the companion lunges, a bolt of its colour lands with a flash */
  if (foe.length && T >= cp.nx) { cp.nx = T + 2.6 + ((hash(cp.sp + (T | 0)) % 100) / 100) * 1.4; const e = foe[hash("e" + (T * 10 | 0)) % foe.length]; cp.hits.push({ t0: T, e }); if (cp.hits.length > 4) cp.hits.shift(); try { SFX.ok() && mimSfx("whip", clamp(bx / W * 2 - 1, -1, 1)); } catch (e2) {} }
  let lx = 0, ly = 0; ctx.save(); ctx.globalCompositeOperation = "lighter";
  for (const h of cp.hits) { const u = (T - h.t0) / .9, E0 = scr[h.e]; if (u < 0 || u > 1 || !E0) continue; if (u < .3) { const k = Math.sin(Math.PI * u / .3); lx = dx / dl * L * .4 * k; ly = dy / dl * L * .4 * k; }
    if (u > .15 && u < .55) { const k = (u - .15) / .4, x = bx + (E0.x - bx) * k, y = by + (E0.y - by) * k - Math.sin(Math.PI * k) * L * .5; ctx.globalAlpha = 1; ctx.drawImage(glowSprite(`rgba(${rgb},1)`), x - 10 * d, y - 10 * d, 20 * d, 20 * d); ctx.drawImage(glowSprite("rgba(255,255,255,1)"), x - 4 * d, y - 4 * d, 8 * d, 8 * d); }
    if (u >= .55) { const k = (u - .55) / .45; if (!h.hit) { h.hit = 1; b.shake = Math.max(b.shake || 0, 4 * d); } ctx.globalAlpha = (1 - k) * .9; const r2 = L * (.3 + .7 * k); ctx.drawImage(glowSprite(`rgba(${rgb},1)`), E0.x - r2, E0.y - r2, r2 * 2, r2 * 2); } }
  const x = bx + lx, y = by + ly; ctx.globalAlpha = .55 + .15 * Math.sin(t * .004); ctx.drawImage(glowSprite(`rgba(${rgb},1)`), x - L * .9, y - L * .9, L * 1.8, L * 1.8); ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = 1;
  const im = compBattle.img || (compBattle.img = {}), key = cp.sp; let I = im[key]; if (!I) { I = im[key] = new Image(); I.src = xsImg(cp.sp); }
  if (I.complete && I.naturalWidth) { const r = L * .5; ctx.save(); ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.clip(); ctx.drawImage(I, x - r, y - r, r * 2, r * 2); ctx.restore(); ctx.strokeStyle = cp.pr ? `hsl(${(t * .2) % 360},90%,70%)` : XR[XS[cp.sp][1]][1]; ctx.lineWidth = 2.4 * d; ctx.beginPath(); ctx.arc(x, y, r, 0, TAU); ctx.stroke(); }
  ctx.font = `700 ${Math.round(9.5 * d)}px Oxanium, sans-serif`; ctx.textAlign = "center"; ctx.fillStyle = "rgba(255,240,200,.95)"; ctx.fillText("★ " + xsName(cp.sp), x, y + L * .5 + 12 * d); ctx.restore(); }
/* the companion beside your flagship's fleets on the map: its own 3D model (a glowing orb for the event species), bobbing alongside */
const XS_HAS3D = new Set(["swhale", "ssquid", "swasp", "reat", "vmanta", "smoth", "cram", "kegg", "gwhale", "cserp", "sent", "ctort", "gspider", "slevi"]);
function compMap(W, grp) { try { const c = xsComp(); if (!c || !TH) return; const box = new TH.Box3().setFromObject(grp), sz = new TH.Vector3(); box.getSize(sz); const span = Math.max(sz.x, sz.z, .5);
    let m; if (XS_HAS3D.has(c.sp)) { W.compMaster = W.compMaster || {}; const master = W.compMaster[c.sp] || (W.compMaster[c.sp] = mergeGroup(buildMonster(c.sp))); m = master.clone(); const mb = new TH.Box3().setFromObject(m), ms = new TH.Vector3(); mb.getSize(ms); m.scale.setScalar(span * .32 * (.8 + .2 * (c.g || 0)) / Math.max(ms.x, ms.y, ms.z, .01)); }
    else { m = new TH.Sprite(W.additive(W.glow["comp" + c.sp] || (W.glow["comp" + c.sp] = glowTex(xsHexRgb(xsCol(c.sp)), .6)), 0xffffff, .9)); m.scale.setScalar(span * .35); }
    const holder = new TH.Group(); holder.add(m); const halo = new TH.Sprite(W.additive(W.glow["comph" + c.sp] || (W.glow["comph" + c.sp] = glowTex(xsHexRgb(xsCol(c.sp)), .45)), 0xffffff, .45)); halo.scale.setScalar(span * .5); holder.add(halo);
    const x0 = box.max.x + span * .22, y0 = sz.y * .6 + span * .08; holder.position.set(x0, y0, (box.min.z + box.max.z) / 2); grp.add(holder);
    const ph = (hash(c.id) % 628) / 100; halo.onBeforeRender = () => { const tt = performance.now() * .001 + ph; holder.position.y = y0 + Math.sin(tt * 1.6) * span * .04; holder.position.x = x0 + Math.sin(tt * .7) * span * .03; m.rotation && (m.rotation.y = Math.sin(tt * .5) * .4); };
    grp.userData.comp = holder; } catch (e) {} }
const xsHexRgb = h => { const n = parseInt(String(h).replace("#", ""), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255].join(","); };
/* the Serpent's eggs (the storyline's payoff) */
function serpEgg(pr) { try { const X = xsOf(); if (X.eggs.length >= XS_EGGS) { S.serpOwe = (S.serpOwe || []).concat(pr ? 1 : 0); return; } X.eggs.push({ sp: "cserp", pr: pr ? 1 : 0 }); dirty(); setTimeout(() => { try { xsReveal("cserp", pr); } catch (e) {} }, 9000); } catch (e) {} }
