/* ---------- v745 the Resurrection War's economy: the Continuum Forge, the war reward track, the medals and the Continuum looks.
   Everything the war drops is spent here. The looks (Machine Debris planet skin, Continuum Black Chrome hull finish, the Neural Crown
   frame, the Continuum banner, warp trail, laser colour and aura, the Continuum Commander portrait) can all be forged by anyone from war
   materials; two of them (the hull finish and the crown frame) also come free on the premium lane. Nothing here is combat power beyond
   the game's usual accelerators, Titan Cores and flagship materials. Every claim writes its key before it pays. ---------- */
CNT_MAT.elite = ["Elite Flagship Materials", "#e8c070"];
const CNT_FORGE = [
  ["px", "Machine Debris planet skin", "A world buried in black machine wreckage, its seams still lit red.", { alloy: 150, circ: 40, core: 4 }],
  ["hull", "Continuum Black Chrome hull finish", "Plate your ships in the Continuum's black chrome with crimson seams. Looks only.", { alloy: 80, cell: 10, matrix: 4 }],
  ["frame14", "Neural Crown portrait frame", "A chrome ring set with red neural nodes and a crown of spikes.", { matrix: 8, core: 4 }],
  ["banner14", "Continuum banner", "The Prime Resurrection Ark and its fleet.", { echo: 300, circ: 30 }],
  ["av", "Continuum Commander portrait", "Lead as a machine mind with one red eye.", { core: 6, matrix: 6 }],
  ["trail14", "Neural warp trail", "Your fleets leave a crimson wake threaded with icy blue.", { echo: 200, cell: 6 }],
  ["laser14", "Crimson neural laser colour", "Your guns fire the Continuum's red.", { circ: 40, cell: 8 }],
  ["aura14", "Crown of the Continuum aura", "A red-and-ice ring round your homeworld.", { core: 8, matrix: 6 }],
  ["elitefs", "Elite flagship materials", "Three tier-5 alloys, three tier-5 circuits and two tier-5 crystals for your flagship's gear.", { elite: 3, alloy: 40 }],
  ["acc", "Neural accelerator (silver)", "A silver time accelerator for your Void Shop inventory.", { echo: 120 }],
  ["tcore", "Titan Core ⬢", "Refined from Resurrection Cores and a Quantum Neural Matrix.", { core: 6, matrix: 4 }],
  ["sh", "Void Shards ◆25", "A Quantum Neural Matrix sells high.", { matrix: 1 }]];
const CNT_TRACK = [[100, { sh: 5 }, { echo: 40 }], [300, { alloy: 15 }, { sh: 10 }], [600, { banner14: 1 }, { item: "crateM" }], [1000, { sh: 10 }, { px: 1 }], [1600, { circ: 8 }, { frame14: 1 }], [2400, { sh: 15 }, { hull: 1 }], [3500, { cell: 4 }, { sh: 30 }], [5000, { matrix: 3 }, { tcore: 1 }], [7000, { core: 2 }, { aura14: 1 }]];
const CNT_COS = ["frame14", "banner14", "trail14", "laser14", "aura14"];
const cntHave = (c, M) => Object.entries(c).every(([k, n]) => (M.m[k] || 0) >= n);
const cntCostTxt = c => Object.entries(c).map(([k, n]) => `<span class="cntc" style="color:${CNT_MAT[k][1]}"><img class="cntmi s" src="art/rwar/i_${k}.webp" alt="">${n}</span>`).join(" ");
const cntOwn = k => k === "px" ? !!(S.pxOwn || {}).cntdebris : k === "hull" ? !!(S.hullOwn || {}).continuum : k === "av" ? !!(S.avOwn || {}).continuum : /14$/.test(k) ? !!((S.cos || {}).own || {})[k] : false;
function cntGrant2(r, why) { const got = []; const mt = {}; for (const k in CNT_MAT) if (r[k]) { mt[k] = r[k]; got.push(`${r[k]} ${CNT_MAT[k][0]}`); } cntAddM(mt);
  if (r.sh) { S.shards = (S.shards || 0) + r.sh; got.push(`◆${r.sh}`); } if (r.item) { giveItem(r.item); got.push(SHOP[r.item] ? SHOP[r.item].n : r.item); }
  if (r.tcore) { S.tcore = (S.tcore || 0) + r.tcore; got.push("a Titan Core ⬢"); } if (r.px) { (S.pxOwn = S.pxOwn || {}).cntdebris = 1; got.push("the Machine Debris planet skin"); }
  if (r.hull) { (S.hullOwn = S.hullOwn || {}).continuum = 1; got.push("the Continuum Black Chrome hull finish"); } if (r.av) { (S.avOwn = S.avOwn || {}).continuum = 1; got.push("the Continuum Commander portrait"); }
  if (r.acc) { giveItem("xb_silver"); got.push("a silver time accelerator"); }
  if (r.elitefs) { fsDrop([["alloy", 5, 3], ["circuit", 5, 3], ["crystal", 5, 2]], "the Continuum Forge", { nocap: true }); got.push("elite flagship materials"); }
  for (const c of CNT_COS) if (r[c]) { try { cosGive(c); } catch (e) {} got.push(cosDef(c) ? cosDef(c).n : c); }
  dirty(); if (got.length) { toast(`${why}: ${got.join(", ")}`, "win"); try { logReward(why, null, { shards: r.sh || 0, kind: "event" }); } catch (e) {} } return got; }
function cntForgeHTML() { const M = cntS(); return `<h3>The Continuum Forge</h3><p class="note">Spend what the war drops. Every look here can be forged by anyone; nothing needs a purchase.</p><div class="mimforge">${CNT_FORGE.map(([k, n, d, c]) => { const done = cntOwn(k), ok = !done && cntHave(c, M) && (k !== "elitefs" || fsOn());
    return `<div class="mimfr cntfr${done ? " done" : ""}"><div><b>${esc(n)}</b><small>${esc(d)}${k === "elitefs" && !fsOn() ? " (your flagship takes command at commander Lv.15)" : ""}</small><em>${cntCostTxt(c)}</em></div><button class="btn${ok ? " pri" : ""}" data-act="cntForge" data-k="${k}"${ok ? "" : " disabled"}>${done ? "Owned" : "Forge"}</button></div>`; }).join("")}</div>`; }
function cntTrackHTML() { const M = cntS(), pr = mimPrem(), got = M.tr || {};
  const nm = (k, v) => k === "px" ? "Machine Debris skin" : k === "hull" ? "Black Chrome finish" : k === "item" ? (SHOP[v] ? SHOP[v].n : v) : k === "sh" ? `◆${v}` : k === "tcore" ? "Titan Core ⬢" : /14$/.test(k) ? (cosDef(k) || {}).n || k : `${v} ${CNT_MAT[k][0]}`;
  const cell = (r, i, p) => { const id = (p ? "p" : "f") + i, have = got[id], open = M.pts >= CNT_TRACK[i][0] && (!p || pr); return `<button class="mimtc${p ? " p" : ""}${have ? " got" : open ? " ready" : ""}" data-act="cntTrack" data-i="${i}" data-p="${p ? 1 : 0}"${open && !have ? "" : " disabled"}>${have ? "✓ " : ""}${esc(Object.entries(r).map(([k, v]) => nm(k, v)).join(", "))}</button>`; };
  return `<h3>War reward track</h3><p class="note">${fmt(M.pts)} war points. Premium rewards need Void Pass Premium${pr ? " (yours is active)" : ""}.</p><div class="mimtrack">${CNT_TRACK.map(([pts, f, p], i) => `<div class="mimtr${M.pts >= pts ? " on" : ""}"><b>${fmt(pts)}</b>${cell(f, i, 0)}${cell(p, i, 1)}</div>`).join("")}</div>`; }
function cntMedalsHTML() { const m = S.medals || {}; if (!m.ark && !m.prime) return "";
  return `<div class="cntmedals">${m.ark ? `<div><img src="art/rwar/i_badge.webp" alt=""><b>Arkbreaker</b><small>×${m.ark} · an Ark destroyed with you in the fight</small></div>` : ""}${m.prime ? `<div><img src="art/rwar/i_trophy.webp" alt=""><b>Prime Ark Trophy</b><small>×${m.prime} · Extinction Protocol, full victory</small></div>` : ""}</div>`; }
