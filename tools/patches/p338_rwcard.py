# v338 Stage 2: materials are shown, not just logged. A reward card (material art, rarity frame, big count, a gold "rare find" flare for
# Epic and up) is built from the exact counts fsDrop granted, so it can never show something that wasn't given. Materials join the
# rewards history. Pirate, monster, Cube, pyramid and field cards preview the loot from the same LOOT rolls that pay out.
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
# fsDrop: log without a duplicate toast, then the card and the history entry
rep('''note(`Flagship materials${why ? ` from ${why}` : ""}: ${Object.entries(c).map(([k, n]) => `${FS_TIER[+k.slice(-1)][0]} ${FS_MATS[k.slice(0, -1)][0]} ×${n}`).join(", ")}.`, "win"); return c; }''',
'''const msg = `Flagship materials${why ? ` from ${why}` : ""}: ${Object.entries(c).map(([k, n]) => `${FS_TIER[+k.slice(-1)][0]} ${FS_MATS[k.slice(0, -1)][0]} ×${n}`).join(", ")}.`;
  S.log.unshift({ t: S.t, msg, kind: "win" }); if (S.log.length > 30) S.log.length = 30; changed = true; /* v338: the card below replaces the toast */
  logReward(why ? `Materials · ${why}` : "Materials", null, { mats: c, kind: "mats" }); if (live) rwCardShow(why, c); return c; }
/* v338: the reward card. Queued, a few seconds each, tap to dismiss; it never blocks a tap anywhere else */
function rwCardShow(why, c) { (G.rwq = G.rwq || []).push([why, c]); if (!G.rwOn) rwCardNext(); }
function rwCardNext() { const it = (G.rwq || []).shift(); let w = $("#rwcard"); if (!it) { G.rwOn = 0; if (w) w.classList.remove("on"); return; } G.rwOn = 1;
  if (!w) { w = document.createElement("div"); w.id = "rwcard"; w.setAttribute("aria-live", "polite"); w.addEventListener("click", () => { clearTimeout(G.rwT); rwCardNext(); }); document.body.appendChild(w); }
  const [why, c] = it, ks = Object.keys(c).sort((a, b) => +b.slice(-1) - +a.slice(-1)), top = +(ks[0] || "1").slice(-1), rare = top >= 4;
  w.className = "on" + (rare ? " rare" : ""); w.style.setProperty("--tc", FS_TIER[top][1]);
  w.innerHTML = `<small>${rare ? "★ RARE FIND · " : ""}MATERIALS${why ? " · " + esc(why.toUpperCase()) : ""}</small><div class="rwm">${ks.map(k => { const tt = +k.slice(-1), m = FS_MATS[k.slice(0, -1)]; return `<span style="--tc:${FS_TIER[tt][1]}"><i class="fsmi lg fsmat-${k.slice(0, -1)}"></i><b>×${c[k]}</b><em>${FS_TIER[tt][0]}<br>${esc(m[0])}</em></span>`; }).join("")}</div>`;
  try { (rare ? SFX.fanfare : SFX.rune)(); } catch (e) {}
  clearTimeout(G.rwT); G.rwT = setTimeout(rwCardNext, rare ? 4800 : 3200); }
/* v338: a "Possible materials" block for a target card, from the same rolls the fight pays */
function lootPreview(rolls, extra) { const ev = rolls.filter(r => r[2] > 0); if (!ev.length) return "";
  const chips = ev.map(([k, tt, n, p, up]) => { const t2 = clamp(tt, 1, 6); return `<span class="lp" style="--tc:${FS_TIER[t2][1]}"><i class="fsmi fsmat-${k === "low" ? "alloy" : k}"></i><b>${k === "low" ? "Material" : esc(FS_MATS[k][0])}</b><em>${FS_TIER[t2][0]} · ${p == null || p >= 1 ? "×" + n : Math.round(p * 100) + "%" + (up ? "*" : "")}</em></span>`; }).join("");
  return `<div class="lprev"><small>POSSIBLE MATERIALS</small><div>${chips}</div>${extra || ""}${ev.some(r => r[4]) ? `<p class="note">* Rare roll: guaranteed at least once every ${LOOT_PITY} tries.</p>` : ""}</div>`; }''')
# history: materials appear in the rewards list
rep('''  if (!(e.res && total(e.res)) && !e.shards && !e.item && !e.runes && !e.boosts) return;''', '''  if (!(e.res && total(e.res)) && !e.shards && !e.item && !e.runes && !e.boosts && !e.mats) return;''')
rep('''${e.boosts ? `<span class="rwi">⚡ ${e.boosts}</span>` : ""}`;
  return `<div class="card rwc">''', '''${e.boosts ? `<span class="rwi">⚡ ${e.boosts}</span>` : ""}${e.mats ? Object.entries(e.mats).map(([k, n]) => `<span class="rwi" style="color:${FS_TIER[+k.slice(-1)][1]}"><i class="fsmi fsmat-${k.slice(0, -1)}"></i>×${n}</span>`).join("") : ""}`;
  return `<div class="card rwc">''')
rep('''<span class="rk k-${e.kind || "x"}">${e.kind === "plunder" ? "⛏" : e.kind === "battle" ? "⚔" : "★"}</span>''', '''<span class="rk k-${e.kind || "x"}">${e.kind === "plunder" ? "⛏" : e.kind === "battle" ? "⚔" : e.kind === "mats" ? "◈" : "★"}</span>''')
# previews on the target cards
rep('''  const info = `<dl class="kv"><dt>Loot on a win</dt>''', '''  const el = isElite(x), lk = xLootK(x), fk = !(S.fk || {})[lk + ":" + x.lvl] && !trainingPir(x);
  const lprev = lootPreview(lk === "cube" ? LOOT.cube(x.lvl) : lk === "mon" ? LOOT.monster(x.lvl, el) : LOOT.pirate(x.lvl, el), fk ? `<p class="lfk">First ${lk === "cube" ? "Cube" : lk === "mon" ? "monster" : "pirate"} kill at Lv.${x.lvl}: ◆2 and ${matsText(LOOT.first(lk, x.lvl))}</p>` : "");
  const info = `${el ? `<div class="elite">★ ELITE · 60% stronger this week · double materials, triple rare chance</div>` : ""}${lprev}<dl class="kv"><dt>Loot on a win</dt>''')
rep('''  const T = now(), h = originPlanet(), avail = originAvail(), sel = selected(), down = pyrDown(y), g = pyrGuards(y.lvl), L = pyrLoot(y.lvl), sent = S.fleets.some(f => f.yid === y.id && f.phase === "out");
  let body = "";''', '''  const T = now(), h = originPlanet(), avail = originAvail(), sel = selected(), down = pyrDown(y), g = pyrGuards(y.lvl), L = pyrLoot(y.lvl), sent = S.fleets.some(f => f.yid === y.id && f.phase === "out");
  let body = lootPreview(LOOT.pyramid(y.lvl)); /* v338 */''')
rep('''  if (down > T) body = `<p class="note">You emptied this vault.''', '''  if (down > T) body += `<p class="note">You emptied this vault.''')
for a in ['''  else if (!canPlay()) body = `<p class="note">${G.mode === "connecting" ? connNote() : "You can only watch this galaxy."}</p>`;
  else if (sent) body = `<p class="note">An expedition is already on its way.</p>`;''']:
    rep(a, a.replace('body = `', 'body += `'))
# CSS
i = t.index('.cneed{'); t = t[:i] + '''#rwcard{position:fixed;left:50%;top:calc(env(safe-area-inset-top,0px) + 118px);z-index:66;transform:translate(-50%,-14px);opacity:0;pointer-events:none;transition:opacity .25s,transform .25s;max-width:min(92vw,420px);padding:10px 14px 12px;border-radius:14px;background:linear-gradient(180deg,rgba(14,24,36,.96),rgba(7,13,22,.96));border:1px solid var(--tc,#5dd4e8);box-shadow:0 10px 30px rgba(0,0,0,.55),0 0 18px color-mix(in srgb,var(--tc,#5dd4e8) 35%,transparent)}
#rwcard.on{opacity:1;transform:translate(-50%,0);pointer-events:auto}#rwcard small{display:block;font:700 11px/1.3 var(--f-display);letter-spacing:.12em;color:var(--tc,#9fd)}
#rwcard.rare{box-shadow:0 10px 30px rgba(0,0,0,.55),0 0 34px color-mix(in srgb,var(--tc) 70%,transparent);animation:rwflare 1.2s ease-out 1}@keyframes rwflare{0%{filter:brightness(2.2)}100%{filter:none}}
#rwcard .rwm{display:flex;flex-wrap:wrap;gap:8px 14px;margin-top:8px}#rwcard .rwm span{display:flex;align-items:center;gap:4px}#rwcard .rwm .fsmi.lg{width:42px;height:42px;margin:0;box-shadow:0 0 0 2px var(--tc),0 0 12px color-mix(in srgb,var(--tc) 60%,transparent)}
#rwcard .rwm b{font:800 22px/1 var(--f-display);color:#fff}#rwcard .rwm em{font-style:normal;font-size:11px;line-height:1.15;color:var(--tc)}
.lprev{margin:8px 0;padding:8px 10px;border-radius:10px;background:rgba(85,214,232,.06);border:1px solid rgba(85,214,232,.18)}.lprev small{color:var(--cyan);letter-spacing:.1em;font-size:11px}.lprev>div{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
.lprev .lp{display:flex;align-items:center;gap:6px;padding:4px 8px;border-radius:8px;border:1px solid var(--tc);background:rgba(0,0,0,.25);font-size:12px}.lprev .lp b{font-weight:600}.lprev .lp em{font-style:normal;color:var(--tc)}.lprev .note{margin:6px 0 0;font-size:11px}
.lfk{margin:6px 0 0;font-size:12px;color:var(--amber)}.elite{margin:6px 0;padding:6px 10px;border-radius:8px;background:linear-gradient(90deg,rgba(255,190,80,.22),rgba(255,190,80,.05));border:1px solid rgba(255,200,100,.6);color:#ffd890;font:700 12px/1.3 var(--f-display);letter-spacing:.06em}
''' + t[i:]
rep("""  const T = now(), oc = occOf(n.id, T), L = layerOf(n.r);\n""", """  const T = now(), oc = occOf(n.id, T), L = layerOf(n.r);\n  const lpv = n.res === "s" ? "" : lootPreview(LOOT.gather(n.lvl, 60000, n.res), `<p class="note">Per 60K gathered; bigger hauls pay up to 6.</p>`); /* v338 */\n""")
rep('  const info = `${occ}<dl class="kv">${n.res === "s" ?', '  const info = `${occ}${lpv}<dl class="kv">${n.res === "s" ?')
open(p, 'w', encoding='utf-8').write(t); print('ok')
