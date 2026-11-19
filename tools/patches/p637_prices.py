# v637: faction change costs 100 shards and asks first; planet skins stop being free (200+ shards), with a confirm tap.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:90]}')
    s = s.replace(a, b)

# skins: end of pre-release freebies; worlds already wearing a skin keep it (owned for good)
rep('const FREE_SKINS = true;', 'const FREE_SKINS = false; /* v637: shop skins cost shards again (◆200 and up) */\nconst FAC_COST = 100; /* v637: changing faction (was ◆10) */')
rep('const pxOwned = k => PXS[k] && PXS[k].prem ? !!(ownerFree() || premT() >= PXS[k].prem) : !!(FREE_SKINS || ownerFree() || (S && S.pxOwn || {})[k]);',
    'const pxOwned = k => PXS[k] && PXS[k].prem ? !!(ownerFree() || premT() >= PXS[k].prem) : !!(FREE_SKINS || ownerFree() || (S && S.pxOwn || {})[k] || pxKeep(k));\n'
    '/* v637: a skin a world already wore while skins were free stays the player\'s own */\n'
    'function pxKeep(k) { try { if (!S || !G.me || typeof myPlanets !== "function" || !myPlanets().some(p => p && p.px === k)) return false; (S.pxOwn = S.pxOwn || {})[k] = 1; dirty(); return true; } catch (e) { return false; } }')

# skins: the buy button needs a second tap
rep('<button class="btn amber sm" data-act="pxBuy" data-k="${k}" ${(S.shards || 0) >= s.cost ? "" : "disabled"}><span class="shard">◆</span>${fmt(s.cost)}</button>',
    '<button class="btn amber sm${pxArmed(k) ? " pxarm" : ""}" data-act="pxBuy" data-k="${k}" ${(S.shards || 0) >= s.cost ? "" : "disabled"}>${pxArmed(k) ? "Confirm " : ""}<span class="shard">◆</span>${fmt(s.cost)}</button>')
rep('  pxBuy: d => act(() => { const s = PXS[d.k]; if (!s) return; if (s.prem) return toast(`${s.n} comes with Premium Tier ${s.prem}.`, "warn"); S.pxOwn = S.pxOwn || {}; if (pxOwned(d.k)) return; if ((S.shards || 0) < s.cost) return toast(`${s.n} costs ◆${fmt(s.cost)}.`, "warn");\n',
    '  pxBuy: d => act(() => { const s = PXS[d.k]; if (!s) return; if (s.prem) return toast(`${s.n} comes with Premium Tier ${s.prem}.`, "warn"); S.pxOwn = S.pxOwn || {}; if (pxOwned(d.k)) return; if ((S.shards || 0) < s.cost) return toast(`${s.n} costs ◆${fmt(s.cost)}.`, "warn");\n'
    '    if (!pxArmed(d.k)) { G.pxArm = { k: d.k, t: Date.now() }; toast(`Tap again to spend ◆${fmt(s.cost)} on ${s.n}.`); if (sheet) renderSheet(); else render(true); setTimeout(() => { if (G.pxArm && G.pxArm.k === d.k && !pxArmed(d.k)) { G.pxArm = null; if (sheet) renderSheet(); else render(true); } }, 8100); return; } G.pxArm = null;\n')
rep('const pxGoldWrap = ', 'const pxArmed = k => !!(G.pxArm && G.pxArm.k === k && Date.now() - G.pxArm.t < 8000); /* v637 */\nconst pxGoldWrap = ')

# faction: 100 shards, and a confirm panel before anything is charged
rep('You can change it later for <span class="gem"><i>◆</i>10</span>.` : ` Changing costs <span class="gem"><i>◆</i>10</span>.`',
    'You can change it later for <span class="gem"><i>◆</i>${FAC_COST}</span>.` : ` Changing costs <span class="gem"><i>◆</i>${FAC_COST}</span>.`')
rep('if (!first) { if (f === S.faction) return closeSheet(); if ((S.shards || 0) < 10) return toast("Changing faction costs ◆10.", "warn"); }',
    'if (!first) { if (f === S.faction) return closeSheet(); if ((S.shards || 0) < FAC_COST) return toast(`Changing faction costs ◆${FAC_COST}. You have ◆${fmt(S.shards || 0)}.`, "warn");\n'
    '      if (d.ok !== "1") { sheet.fcf = f; renderSheet(); return; } sheet.fcf = null; }')
rep('if (!first) { if ((S.shards || 0) < 10) return toast("Changing faction costs ◆10.", "warn"); S.shards -= 10; }',
    'if (!first) { if ((S.shards || 0) < FAC_COST) return toast(`Changing faction costs ◆${FAC_COST}.`, "warn"); S.shards -= FAC_COST; }')
rep('  faction: () => openSheet({ type: "faction" }),',
    '  faction: () => openSheet({ type: "faction" }),\n  facNo: () => { if (sheet) { sheet.fcf = null; renderSheet(); } },')
# the panel: after the cards grid, inside .facin
i = s.index('function shFaction()'); j = s.index('  </div></div>`;\n}', i)
s = s[:j] + '''    ${!first && sheet && sheet.fcf && FACTIONS[sheet.fcf] ? `<div class="faccf" role="alertdialog" aria-label="Confirm faction change"><p>Switch to <b>${FACTIONS[sheet.fcf].n}</b> for <span class="gem"><i>◆</i>${FAC_COST}</span>?<small>You have ◆${fmt(S.shards || 0)}. Your ships and buildings change look; stats stay the same.</small></p><div><button class="btn ghost" data-act="facNo">Cancel</button><button class="btn amber" data-act="facPick" data-f="${sheet.fcf}" data-ok="1">Switch for ◆${FAC_COST}</button></div></div>` : ""}
''' + s[j:]
rep('.facs{position:relative;display:grid;grid-template-columns:1fr;gap:14px}',
    '.facs{position:relative;display:grid;grid-template-columns:1fr;gap:14px}\n'
    '.faccf{position:fixed;left:max(16px,env(safe-area-inset-left,0px));right:max(16px,env(safe-area-inset-right,0px));bottom:calc(84px + env(safe-area-inset-bottom,0px));z-index:60;max-width:520px;margin:0 auto;animation:faccf .22s ease-out;padding:14px;border:1px solid rgba(255,200,110,.55);border-radius:12px;background:#0a101e;opacity:1;isolation:isolate;box-shadow:0 0 0 100vmax rgba(2,5,12,.55),0 10px 30px rgba(0,0,0,.6),0 0 24px rgba(255,180,80,.18);display:grid;gap:12px}\n'
    '@keyframes faccf{from{transform:translateY(16px);opacity:0}}\n'
    '.faccf p{margin:0;font-size:15px;color:#fff;line-height:1.4}.faccf small{display:block;margin-top:4px;font-size:12px;color:#9fb6c4}\n'
    '.faccf>div{display:flex;gap:10px;justify-content:flex-end;flex-wrap:wrap}\n'
    '.btn.pxarm{animation:pxarm 1s ease-in-out infinite;box-shadow:0 0 0 2px #ffd36b}@keyframes pxarm{50%{filter:brightness(1.35)}}')
rep('const GAME_V = 636', 'const GAME_V = 637')
open(p, 'w', encoding='utf-8').write(s)
