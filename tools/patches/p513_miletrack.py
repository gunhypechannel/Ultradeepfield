# v513 the milestone rewards remastered (owner: "boring, not appealing"; on his Fold every row's points label had turned into a
# giant empty circle: the planet-tint swatch rule .tn{aspect-ratio:1;border-radius:50%} and the shop's .tier pill rule reached
# the event rows). Now a reward track: your points in big type with a bar to the next reward, then a path of reward cards, each
# with a node for its points, its rewards as coloured chips (shards, resources, boosts, items, VIP, materials by rarity) and its
# state: claimed (dimmed, a check), ready (glowing, Claim right there), next (its own progress bar), locked.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# the two rules that leaked: the tint swatches and the shop tier pill only style their own elements now
rep('.tints{display:grid;grid-template-columns:repeat(6,1fr);gap:6px}.tn{aspect-ratio:1;', '.tints{display:grid;grid-template-columns:repeat(6,1fr);gap:6px}.tints .tn{aspect-ratio:1;')
rep('.tn.on{border-color:#fff;box-shadow:0 0 0 2px var(--cyan)}', '.tints .tn.on{border-color:#fff;box-shadow:0 0 0 2px var(--cyan)}')
rep('\n.tier{font-style:normal;font-family:var(--f-display);font-size:10px;letter-spacing:.14em;', '\n.sitem .tier{font-style:normal;font-family:var(--f-display);font-size:10px;letter-spacing:.14em;')
CSS = r'''
/* v513 the reward track */
.mtrk{margin:10px 0 6px;padding:14px;border-radius:16px;background:radial-gradient(120% 90% at 0% 0%,rgba(255,190,90,.14),transparent 60%),linear-gradient(180deg,rgba(20,32,52,.9),rgba(10,16,28,.95));border:1px solid rgba(255,200,110,.22);box-shadow:inset 0 0 30px rgba(0,0,0,.35)}
.mtrk-h{display:flex;align-items:flex-end;justify-content:space-between;gap:10px;flex-wrap:wrap}
.mtrk-h small{display:block;font:600 10px/1.2 var(--f-display);letter-spacing:.16em;text-transform:uppercase;color:#c9a96a}
.mtrk-h b{display:block;font:800 34px/1 var(--f-display);color:#ffd27a;text-shadow:0 0 18px rgba(255,190,90,.45);letter-spacing:.02em}
.mtrk-nx{font-size:12px;color:#cfd9e6;text-align:right;max-width:58%}.mtrk-nx em{font-style:normal;color:#ffd27a;font-weight:700}
.mtrk-bar{position:relative;height:10px;margin:12px 4px 4px;border-radius:6px;background:rgba(255,255,255,.07);overflow:visible}
.mtrk-bar>i{position:absolute;inset:0 auto 0 0;border-radius:6px;background:linear-gradient(90deg,#ff9a3c,#ffd27a);box-shadow:0 0 12px rgba(255,190,90,.6)}
.mtrk-bar>u{position:absolute;top:50%;width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;background:#1a2638;border:2px solid rgba(255,255,255,.25);text-decoration:none}
.mtrk-bar>u.on{background:#ffd27a;border-color:#fff3d0;box-shadow:0 0 10px rgba(255,210,122,.8)}
.mtrk-tip{font-size:11.5px;color:var(--muted);margin:6px 2px 0}
.mpath{position:relative;display:flex;flex-direction:column;gap:10px;margin:12px 0 4px;padding-left:4px}
.mpath:before{content:"";position:absolute;left:29px;top:24px;bottom:24px;width:2px;background:linear-gradient(180deg,rgba(255,210,122,.6),rgba(255,255,255,.08))}
.mcrd{position:relative;display:grid;grid-template-columns:52px minmax(0,1fr) auto;gap:10px;align-items:center;padding:10px 12px 10px 4px;border-radius:14px;background:linear-gradient(90deg,rgba(255,255,255,.045),rgba(255,255,255,.015));border:1px solid rgba(255,255,255,.08)}
.mnode{position:relative;z-index:1;width:48px;height:48px;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#121c2c;border:2px solid rgba(255,255,255,.18);font:800 14px/1 var(--f-display);color:#e6edf6}
.mnode small{font:600 8.5px/1.2 var(--f-display);letter-spacing:.12em;color:var(--muted);text-transform:uppercase}
.mbody{min-width:0;display:flex;flex-direction:column;gap:6px}
.mchips{display:flex;flex-wrap:wrap;gap:5px}
.mchip{display:inline-flex;align-items:center;gap:4px;padding:3px 8px;border-radius:999px;font-size:11.5px;font-weight:600;color:#e9f0f8;background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);white-space:normal;line-height:1.25}
.mchip.mc-sh{color:#e6c8ff;background:rgba(170,110,255,.16);border-color:rgba(190,140,255,.4)}
.mchip.mc-vp{color:#ffe08a;background:rgba(255,200,80,.14);border-color:rgba(255,210,110,.4)}
.mchip.mc-it{color:#9ff3ff;background:rgba(80,220,255,.12);border-color:rgba(110,225,255,.35)}
.mchip.mc-mt{color:var(--mc);background:color-mix(in srgb,var(--mc) 14%,transparent);border-color:color-mix(in srgb,var(--mc) 45%,transparent)}
.mchip.mc-mt:before{content:"⬢";font-size:10px;display:inline;margin:0}
.mchip.mc-rs .cost{display:inline-flex;gap:6px}
.mprog{height:5px;border-radius:3px;background:rgba(255,255,255,.08);overflow:hidden}.mprog i{display:block;height:100%;background:linear-gradient(90deg,#4fc3ff,#9ff3ff)}
.mst{font:700 10.5px/1.2 var(--f-display);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);text-align:center;min-width:64px}
.mcrd.done{opacity:.55}.mcrd.done .mnode{border-color:#5dff8a;color:#5dff8a}.mcrd.done .mst{color:#5dff8a}
.mcrd.ready{border-color:rgba(255,200,100,.7);background:linear-gradient(90deg,rgba(255,180,80,.2),rgba(255,180,80,.05));box-shadow:0 0 18px rgba(255,180,80,.25);animation:mready 2.2s ease-in-out infinite}
.mcrd.ready .mnode{border-color:#ffd27a;background:radial-gradient(circle,#ffcf6a,#b86a10);color:#2a1600;box-shadow:0 0 16px rgba(255,200,100,.8)}.mcrd.ready .mnode small{color:#4a2a00}
.mcrd.next{border-color:rgba(110,210,255,.45)}.mcrd.next .mnode{border-color:#4fc3ff;color:#9ff3ff}
.mcrd.lock .mchips{filter:saturate(.6);opacity:.85}
@keyframes mready{50%{box-shadow:0 0 28px rgba(255,190,90,.5)}}
@media (prefers-reduced-motion:reduce){.mcrd.ready{animation:none}}
'''
rep('</style>', CSS + '</style>', s.count('</style>') if s.count('</style>') == 1 else 1) if s.count('</style>') == 1 else None
if CSS not in s:
    i = s.index('/* v125: daily mission tiers are compact rows wherever they appear'); s = s[:i] + CSS + s[i:]
JS = r'''/* v513 the reward track: points, a bar to the next reward, and a path of reward cards */
function rwChips(rw) { const c = []; if (rw.shards) c.push(`<span class="mchip mc-sh">◆ ${fmt(rw.shards)} shards</span>`); if (rw.m || rw.c || rw.g) c.push(`<span class="mchip mc-rs">${costHTML({ m: rw.m || 0, c: rw.c || 0, g: rw.g || 0 })}</span>`);
  if (rw.boosts) c.push(`<span class="mchip mc-it">⚡ ${rw.boosts} boost${rw.boosts > 1 ? "s" : ""}</span>`); if (rw.item && SHOP[rw.item]) c.push(`<span class="mchip mc-it">🎁 ${esc(SHOP[rw.item].n)}</span>`); if (rw.vip) c.push(`<span class="mchip mc-vp">♛ VIP +${fmt(rw.vip)}</span>`);
  if (rw.mats) for (const [k, tt, n, p] of (typeof rw.mats === "function" ? rw.mats() : rw.mats)) { const tn = FS_TIER[clamp(tt, 1, 6)]; c.push(`<span class="mchip mc-mt" style="--mc:${tn[1]}">${n > 1 ? n + "× " : ""}${tn[0]} ${k === "low" ? "material" : esc(FS_MATS[k][0])}${p != null && p < 1 ? ` · ${Math.round(p * 100)}%` : ""}</span>`); }
  return c.join(""); }
function mileTrack(list, pts, got, claimAct, unit, tip) { const top = list[list.length - 1][0], nxI = list.findIndex(([need]) => pts < need), nx = nxI >= 0 ? list[nxI] : null, prev = nxI > 0 ? list[nxI - 1][0] : 0;
  const pos = v => Math.sqrt(Math.min(1, v / top)) * 100, ready = list.filter(([need], i) => pts >= need && !got.includes(i)).length;
  const head = `<div class="mtrk-h"><div><small>Your ${esc(unit)}</small><b>${fmt(pts)}</b></div><div class="mtrk-nx">${nx ? `Next reward at <em>${fmt(nx[0])}</em> · ${fmt(nx[0] - pts)} to go` : "Every reward reached!"}${ready ? `<br><em>${ready} ready to claim</em>` : ""}</div></div>
    <div class="mtrk-bar"><i style="width:${pos(pts).toFixed(1)}%"></i>${list.map(([need]) => `<u class="${pts >= need ? "on" : ""}" style="left:${pos(need).toFixed(1)}%"></u>`).join("")}</div>${tip ? `<p class="mtrk-tip">${tip}</p>` : ""}`;
  const cards = list.map(([need, rw], i) => { const done = got.includes(i), rd = !done && pts >= need, isNx = i === nxI, st = done ? "done" : rd ? "ready" : isNx ? "next" : "lock";
    const right = done ? `<span class="mst">✓ Claimed</span>` : rd ? `<button class="btn amber sm" ${claimAct}>Claim</button>` : `<span class="mst">${isNx ? `${fmt(need - pts)} to go` : "🔒 Locked"}</span>`;
    return `<div class="mcrd ${st}"><div class="mnode">${fmt(need)}<small>pts</small></div><div class="mbody"><div class="mchips">${rwChips(rw)}</div>${isNx ? `<div class="mprog"><i style="width:${Math.max(3, (pts - prev) / Math.max(1, need - prev) * 100).toFixed(1)}%"></i></div>` : ""}</div>${right}</div>`; }).join("");
  return `<div class="mtrk">${head}<div class="mpath">${cards}</div></div>`; }
'''
rep('function sbOverview(T, g = 1) {', JS + 'function sbOverview(T, g = 1) {')
rep('''    <h4>Your Hunt points</h4><p><b class="evscore">${fmt(pts)}</b> · ${pts ? (g === 3 ? "every 2.5% of hull you destroy scores 3, or 6 on the Pentarch" : g === 2 ? "every 2.5% of hull you destroy scores 3" : "every 2.5% of hull you destroy scores 3 on the Overlord or Devourer, 2 on the Warden, 1 on a conduit") : `attack any ${g === 2 ? "titan" : "world boss"} to start scoring`}</p>
    <h4>Milestone rewards</h4>${SB_MILE.map(([need, rw], m) => `<div class="tier"><span class="tn">${fmt(need)} pts</span><span class="trw">${rwText(rw)}</span>${sb.mile.includes(m) ? '<span class="pill ok">Claimed</span>' : pts >= need ? '<span class="pill amb">Ready</span>' : '<span class="pill wait">—</span>'}</div>`).join("")}''',
    '''    <h4>Milestone rewards</h4>${mileTrack(SB_MILE, pts, sb.mile, `data-act="sbClaim" data-g="${g}"`, "Hunt points", pts ? (g === 3 ? "Every 2.5% of hull you destroy scores 3, or 6 on the Pentarch." : g === 2 ? "Every 2.5% of hull you destroy scores 3." : "Every 2.5% of hull you destroy scores 3 on the Overlord or Devourer, 2 on the Warden, 1 on a conduit.") : `Attack any ${g === 2 ? "titan" : g === 3 ? "Elemental" : "world boss"} to start scoring.`)}''')
rep('''<h4>Milestone rewards:</h4>${GW_MILE.map(([need, rw], m) => `<div class="tier"><span class="tn">${fmt(need)} pts</span><span class="trw">${rwText(rw)}</span>${g.mile.includes(m) ? '<span class="pill ok">Claimed</span>' : g.pts >= need ? '<span class="pill amb">Ready</span>' : '<span class="pill wait">—</span>'}</div>`).join("")}''',
    '''<h4>Milestone rewards:</h4>${mileTrack(GW_MILE, g.pts, g.mile, 'data-act="gwClaim"', "PvP points", live ? "" : "The war is not running right now.")}''')
# the Battle for the Cube's buttons stay inside the card (long labels used to push the grid wider than the screen)
rep('.cubeacts{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0 4px}', '.cubeacts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:10px 0 4px;max-width:100%}')
rep('.cubeacts .btn{width:100%;min-height:44px;font-size:13px;margin:0}', '.cubeacts .btn{width:100%;min-width:0;max-width:100%;min-height:44px;font-size:13px;margin:0;white-space:normal;line-height:1.25;overflow-wrap:anywhere;box-sizing:border-box}')
s2 = re.sub(r"GAME_V = 512\b", "GAME_V = 513", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
