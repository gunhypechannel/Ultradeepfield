/* ---------- v623 the materials forge (owner: "How can we improve this page? I don't like it and think it needs to be more visually
   entertaining"): one material at a time behind icon tabs, its six rarities as glowing crystals with a ring that fills toward the
   five a fusion needs, a burst when they fuse (and a bigger one for a Mythic), Fuse all, what each rarity is worth in crafted gear,
   and the next goal. The converter and auto-combine fold away underneath. ---------- */
function fsGoal(f, m) { const n = t => f.mats[fsMatKey(m, t)] || 0;
  for (let t = 5; t >= 1; t--) if (n(t) >= 5) return `Ready: five ${FS_TIER[t][0]} make a <b style="color:${FS_TIER[t + 1][1]}">${FS_TIER[t + 1][0]}</b>. Tap the glowing crystal, or Fuse all.`;
  let best = null; for (let t = 1; t <= 5; t++) { const k = n(t); if (k > 0 && (!best || t > best.t)) best = { t, need: 5 - k }; }
  if (!best) return `No ${esc(FS_MATS[m][0])} yet. ${esc(FS_MATS[m][2])}.`;
  const nx = best.t + 1, first = !n(nx) && ![...Array(6 - nx)].some((_, i) => n(nx + 1 + i));
  return `${best.need} more <b style="color:${FS_TIER[best.t][1]}">${FS_TIER[best.t][0]}</b> to fuse ${first ? "your first" : "a"} <b style="color:${FS_TIER[nx][1]}">${FS_TIER[nx][0]}</b>.`; }
function fsForgeHTML(f, m) { const keys = Object.keys(FS_MATS), tot = mm => [1, 2, 3, 4, 5, 6].reduce((a, t) => a + (f.mats[fsMatKey(mm, t)] || 0), 0), fx = G.fsFx && performance.now() - G.fsFx.at < 1800 ? G.fsFx : null;
  const tabs = `<div class="fgtabs" role="tablist">${keys.map(k => `<button role="tab" class="${k === m ? "on" : ""}" data-act="fsMatTab" data-v="${k}" aria-label="${FS_MATS[k][0]}, ${tot(k)}"><i class="fsmi fsmat-${k}"></i><small>${fmt(tot(k))}</small></button>`).join("")}</div>`;
  let any = false; const gems = [1, 2, 3, 4, 5, 6].map(t => { const k = fsMatKey(m, t), n = f.mats[k] || 0, ok = t < 6 && n >= 5 && can(fsCombCost(t)); if (ok) any = true;
    return `<button class="fgem${ok ? " ready" : ""}${n ? "" : " none"}${fx && fx.k === k ? " pop" + (t === 6 ? " big" : "") : ""}${t === 6 ? " myth" : ""}" style="--c:${FS_TIER[t][1]};--p:${t < 6 ? Math.min(1, n / 5).toFixed(2) : n ? 1 : 0}"${t < 6 ? ` data-act="fsComb" data-k="${k}"` : ""} aria-label="${FS_TIER[t][0]}: ${n}${ok ? `. Tap to fuse five into one ${FS_TIER[t + 1][0]}` : ""}">`
      + `<span class="fgring"></span><span class="fgcry"></span>${fx && fx.k === k ? `<i class="fgin">${"<s></s>".repeat(5)}</i>` : ""}<b>${fmt(n)}</b><small>${FS_TIER[t][0]}</small><em>gear ×${FS_TMUL[t]}</em></button>`; }).join("");
  return tabs + `<div class="fgcard" style="--tc:${FS_TIER[6][1]}"><i class="fgbg fsmat-${m}"></i><div class="fghd"><i class="fsmi lg fsmat-${m}"></i><div><b>${esc(FS_MATS[m][0])}</b><small>${esc(FS_MATS[m][2])}</small></div><button class="btn ghost sm" data-act="fsFind" data-r="${FS_SRC[m][0]}">Find ${FS_SRC[m][1]} ›</button></div>`
    + `<div class="fggems">${gems}</div><p class="fgnext">${fsGoal(f, m)}</p><button class="btn wide fgall" data-act="fsCombAll" data-v="${m}" ${any ? "" : "disabled"}>✦ Fuse all</button>`
    + `<p class="note fguse">Five of a rarity fuse into one of the next. Gear crafted from a rarity gets its stat multiplier (gear ×).</p></div>`; }
/* the fusion moment: the sound (the owner's pick once it is in; a chime meanwhile), a buzz, and for a Mythic a flash and the Advisor */
function fsFuseFx(k2, t2, n) { G.fsFx = { k: k2, at: performance.now() }; const big = t2 === 6;
  try { wsLoad(); if (!wsPlay(big ? "fuse_big" : "fuse")) (big ? WSFX.jackpot(false) : WSFX.win(t2 >= 4 ? 1 : 0)); } catch (e) {}
  try { if (navigator.vibrate) navigator.vibrate(big ? [60, 40, 60, 40, 220] : [30, 20, 60]); } catch (e) {}
  if (big) { try { const fl = document.createElement("div"); fl.className = "fgflash"; document.body.appendChild(fl); setTimeout(() => fl.remove(), 1400); } catch (e) {} setTimeout(() => { try { advHolo("A Mythic, Commander. Very few of those exist anywhere in the galaxy.", true); } catch (e) {} }, 900); }
  setTimeout(() => { try { if (sheet && sheet.type === "flagship") renderSheet(); } catch (e) {} }, 1850); }
