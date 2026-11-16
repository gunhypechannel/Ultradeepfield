# v597 the Missions tab tracks the Void Pass instead of the Fleet Path (owner: "In missions tab can we replace fleet path with void
# pass rewards tracker"). A compact card: season token, name and countdown, the tier and XP bar (with the bonus multiplier when it
# is on), the tier just reached and the next two as free/premium rows (tap a cosmetic to preview), today's and this week's mission
# progress, "Claim N rewards" when any wait, and "Open Void Pass". The Fleet Path stays with the Advisor (her path chip and card).
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('    <h2 class="sec">Fleet path · hull ${Math.min(SHIP_PATH.length, (S.shipQ || 0) + 1)} of ${SHIP_PATH.length}</h2>${fleetPathCard()}\n',
    '    <h2 class="sec">Void Pass rewards</h2>${vpTracker(T)} <!-- v597 (was the Fleet Path) -->\n')
rep('function vpBody(T) {', '''function vpTracker(T) { try { const v = vpState(T), si = vpSeason(T), [nm, col] = vpInfo(si), lv = Math.min(VP_TIERS, Math.floor(v.xp / VP_XP)), into = lv >= VP_TIERS ? VP_XP : v.xp - lv * VP_XP, n = vpReady(), mul = vpMul(T); /* v597 */
    const dm = vpMissions(v, "d"), wm = vpMissions(v, "w"), dd = dm.filter(m => m.done).length, wd = wm.filter(m => m.done).length;
    const cell = (i, prem) => { const r = vpReward(i, prem, si), got = (prem ? v.cp : v.cf).includes(i), open = i < lv, lock = prem && !v.pr; return `<div class="vpc${prem ? " p" : ""}${got ? " got" : open && !lock ? " ready" : ""}${lock ? " lock" : ""}${r.cos ? " cos" : ""}"${r.cos ? ` data-act="cosPrev" data-id="${r.cos}" role="button"` : ""}><span>${r.cos && cosDef(r.cos) ? COS_K[cosDef(r.cos).k][1] : r.title ? "🎖" : r.look != null ? "✦" : r.skin ? "🪐" : r.shards && !r.item ? "◆" : r.m ? "▣" : "🎁"}</span><small>${esc(vpRwText(r))}</small>${got ? "<em>✓</em>" : lock ? "<em>♛</em>" : ""}</div>`; };
    const i0 = Math.max(0, Math.min(VP_TIERS - 3, lv - 1)), rows = [i0, i0 + 1, i0 + 2].filter(i => i < VP_TIERS).map(i => `<div class="vpt${i < lv ? " on" : ""}${i === lv ? " cur" : ""}"><b>${i + 1}</b>${cell(i, false)}${cell(i, true)}</div>`).join("");
    return `<section class="vptk" style="--vc:${col}"><button class="vptkh" data-act="vpOpen"><img class="vptok" src="${seasonTok(si)}" alt=""><span><small>SEASON ${si + 1} · ${esc(nm)}</small><b>Tier ${lv}<em>/${VP_TIERS}</em>${v.pr ? ' <i class="vpkp">♛ Premium</i>' : ""}</b></span><span class="vptke">ends in <b data-end="${vpEnd(si)}">${ftime(vpEnd(si) - T)}</b> ›</span></button>
      <div class="vpxp"><i style="width:${(into / VP_XP * 100).toFixed(1)}%"></i></div><div class="vptkx"><small>${lv >= VP_TIERS ? "Every tier reached" : `${fmt(into)} / ${fmt(VP_XP)} XP to tier ${lv + 1}`}</small>${mul > 1 ? `<em>⚡ XP ×${mul}</em>` : ""}</div>
      <div class="vptkr">${rows}</div>
      <div class="vptkm"><span class="${dd >= dm.length ? "ok" : ""}">Daily missions <b>${dd}/${dm.length}</b></span><span class="${wd >= wm.length ? "ok" : ""}">Weekly missions <b>${wd}/${wm.length}</b></span></div>
      <div class="vptkb">${n ? `<button class="btn amber" data-act="vpClaim">Claim ${n} reward${n > 1 ? "s" : ""}</button>` : ""}<button class="btn ghost" data-act="vpOpen">Open Void Pass ›</button></div></section>`; } catch (e) { return ""; } }
function vpBody(T) {''')
CSS = '''.vptk{display:flex;flex-direction:column;gap:8px;padding:12px;border-radius:16px;border:1.5px solid color-mix(in srgb,var(--vc) 60%,transparent);background:radial-gradient(120% 120% at 100% 0,color-mix(in srgb,var(--vc) 22%,#0b0f24),#060a14 70%);box-shadow:0 0 22px color-mix(in srgb,var(--vc) 22%,transparent)}
.vptkh{display:flex;align-items:center;gap:10px;background:none;border:0;padding:0;color:inherit;text-align:left;cursor:pointer;width:100%}.vptkh .vptok{width:44px!important;height:44px!important;max-width:44px;flex:none;position:static!important;animation:none;border-radius:50%;filter:drop-shadow(0 0 8px var(--vc))}
.vptkh>span:nth-child(2){flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}.vptkh small{font:600 10.5px var(--f-display);letter-spacing:.14em;color:color-mix(in srgb,var(--vc) 70%,#fff);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.vptkh b{font:700 20px var(--f-display);color:#fff}.vptkh b em{font-style:normal;font-size:14px;color:#9fb3c2}.vpkp{font:700 11px var(--f-display);font-style:normal;color:#ffcf5a;vertical-align:middle}
.vptke{flex:none;font-size:12px;color:#a9bccb}.vptke b{color:#ffd36b;font-variant-numeric:tabular-nums}.vptkx{display:flex;justify-content:space-between;gap:8px;font-size:12px;color:#a9bccb}.vptkx em{font-style:normal;color:#ffd36b;font-weight:700}
.vptkr{display:flex;flex-direction:column;gap:5px}.vptkm{display:flex;gap:8px}.vptkm span{flex:1;padding:7px 10px;border-radius:10px;background:rgba(255,255,255,.04);border:1px solid var(--line);font-size:12.5px;color:#cfdbe4;display:flex;justify-content:space-between;gap:6px}.vptkm span.ok{border-color:rgba(93,255,138,.45);color:#c9ffd9}.vptkm b{color:#fff}
.vptkb{display:flex;gap:8px}.vptkb .btn{flex:1}
'''
rep('.vptrack{display:flex;', CSS + '.vptrack{display:flex;')
s2 = re.sub(r"GAME_V = 596\b", "GAME_V = 597", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
