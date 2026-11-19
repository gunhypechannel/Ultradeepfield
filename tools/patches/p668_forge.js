/* ---------- v668 the Mimic economy: the Forge, the Mimic reward track, medals ----------
   Everything the invasion drops is spent here. Two exclusive looks (the Neural Hive planet skin and the Mimic Bioweave hull finish) can
   be forged by anyone from materials, or come free on the premium track (Void Pass Premium); the rest is convenience (accelerators,
   shards, a Titan Core), never raw combat power. The track pays out by invasion points; the Omega medal goes to everyone who fought in a
   victorious Convergence. */
const MIM_FORGE = [
  ["px", "Neural Hive planet skin", "A world wrapped in black cable and lit from inside by a cyan neural core. Yours forever.", { tis: 150, alloy: 40, ncf: 15 }],
  ["hull", "Mimic Bioweave hull finish", "Plate your ships in the Mimics' segmented black weave, veined with neural light. Looks only.", { alloy: 60, ncf: 25, cat: 4 }],
  ["acc", "Neural accelerator (silver)", "A silver time accelerator for your Void Shop inventory.", { tis: 40 }],
  ["tcore", "Titan Core ⬢", "One Titan Core, refined from an Alpha's catalysts and Omega's own core.", { cat: 6, osh: 3 }],
  ["sh", "Void Shards ◆25", "Omega Core Shards sell high.", { osh: 1 }]];
const MIM_TRACK = [[100, { sh: 5 }, { tis: 20 }], [300, { tis: 15 }, { sh: 10 }], [600, { item: "crateM" }, { alloy: 10 }], [1000, { sh: 10 }, { px: 1 }], [1600, { alloy: 8 }, { ncf: 6 }], [2400, { sh: 15 }, { hull: 1 }], [3500, { ncf: 5 }, { sh: 30 }], [5000, { cat: 2 }, { tcore: 1 }]];
const mimPrem = () => { try { const v = vpState(); return !!(v && v.pr); } catch (e) { return false; } };
const mimHave = (c, M) => Object.entries(c).every(([k, n]) => (M.m[k] || 0) >= n);
const mimCostTxt = c => Object.entries(c).map(([k, n]) => `<span style="color:${MIM_MAT[k][2]}">${MIM_MAT[k][1]} ${n}</span>`).join(" ");
function mimGrant(r, why) { const M = mimS(), got = [];
  for (const k of ["tis", "alloy", "ncf", "cat", "osh"]) if (r[k]) { M.m[k] = (M.m[k] || 0) + r[k]; got.push(`${r[k]} ${MIM_MAT[k][0]}`); }
  if (r.sh) { S.shards = (S.shards || 0) + r.sh; got.push(`◆${r.sh}`); } if (r.item) { giveItem(r.item); got.push(SHOP[r.item] ? SHOP[r.item].n : r.item); }
  if (r.tcore) { S.tcore = (S.tcore || 0) + r.tcore; got.push("a Titan Core ⬢"); }
  if (r.px) { (S.pxOwn = S.pxOwn || {}).mimichive = 1; got.push("the Neural Hive planet skin"); }
  if (r.hull) { (S.hullOwn = S.hullOwn || {}).mimic = 1; got.push("the Mimic Bioweave hull finish"); }
  if (r.acc) { giveItem("xb_silver"); got.push("a silver time accelerator"); }
  dirty(); if (got.length) { toast(`${why}: ${got.join(", ")}`, "win"); try { logReward(why, null, { shards: r.sh || 0, kind: "event" }); } catch (e) {} } return got; }
function mimForgeHTML() { const M = mimS(), own = { px: !!(S.pxOwn || {}).mimichive, hull: !!(S.hullOwn || {}).mimic };
  return `<h3>The Mimic Forge</h3><div class="mimforge">${MIM_FORGE.map(([k, n, d, c]) => { const done = own[k], ok = !done && mimHave(c, M);
    return `<div class="mimfr${done ? " done" : ""}"><div><b>${esc(n)}</b><small>${esc(d)}</small><em>${mimCostTxt(c)}</em></div><button class="btn${ok ? " pri" : ""}" data-act="mimForge" data-k="${k}"${ok ? "" : " disabled"}>${done ? "Owned" : "Forge"}</button></div>`; }).join("")}</div>`; }
function mimTrackHTML() { const M = mimS(), pr = mimPrem(), got = M.tr || {};
  const cell = (r, i, p) => { const id = (p ? "p" : "f") + i, have = got[id], open = M.pts >= MIM_TRACK[i][0] && (!p || pr), t = Object.entries(r).map(([k, v]) => k === "px" ? "Neural Hive skin" : k === "hull" ? "Bioweave finish" : k === "item" ? (SHOP[v] ? SHOP[v].n : v) : k === "sh" ? `◆${v}` : k === "tcore" ? "Titan Core ⬢" : `${v} ${MIM_MAT[k][0]}`).join(", ");
    return `<button class="mimtc${p ? " p" : ""}${have ? " got" : open ? " ready" : ""}" data-act="mimTrack" data-i="${i}" data-p="${p ? 1 : 0}"${open && !have ? "" : " disabled"}>${have ? "✓ " : ""}${esc(t)}</button>`; };
  return `<h3>Mimic reward track</h3><p class="note">${fmt(M.pts)} invasion points. Premium rewards need Void Pass Premium${pr ? " (yours is active)" : ""}.</p><div class="mimtrack">${MIM_TRACK.map(([pts, f, p], i) => `<div class="mimtr${M.pts >= pts ? " on" : ""}"><b>${fmt(pts)}</b>${cell(f, i, 0)}${cell(p, i, 1)}</div>`).join("")}</div>`; }
