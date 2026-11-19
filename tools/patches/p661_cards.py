# v661 Archive cards (owner: "How can we make the card system better? Seems kinda boring, also want to give each card 1 void shard for each
# stage of completing it and then the normal rewards"; "Please do"). A new record arrives face down: a sealed card back that pulses; tap it
# and it flips over with a sound and a flash, the painting is revealed, and +1 Void Shard flies up. When it is interpreted it waits as a
# glowing gold card; tap it and it turns holo foil and pays one more. Each collection has a rarity frame (Common: the Fleet Registry; Rare:
# the Bestiary; Epic: warnings, omens, sagas, discoveries; Legendary: the Cube, the final chapter, the Testament). Every card shows two stage
# pips. Sealed records show a proper card back with their hint. The header counts cards and shards earned, and offers Collect all.
# Records already recovered before this show their shards as waiting to be collected. The collection rewards are unchanged.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)

rep('function shArch() {', r'''/* ---------- v661 the cards: rarity, stages, the reveal and its shard ---------- */
const ARCH_RAR = { fleet: 0, best: 1, cube: 3, final: 3 }, ARCH_RN = ["Common", "Rare", "Epic", "Legendary"];
const archRar = k => k === "testament" ? 3 : ARCH_RAR[ARCH[k].cat] != null ? ARCH_RAR[ARCH[k].cat] : 2;
const archGot = k => ((S && S.archC) || {})[k] | 0, archDue = k => Math.max(0, archLv(k) - archGot(k));
function archClaim(k, all) { const n = archDue(k); if (!n) return 0; S.archC = S.archC || {}; S.archC[k] = archLv(k); S.shards = (S.shards || 0) + n; dirty(); if (!all) { G.archFlip = { k, at: performance.now(), lv: archLv(k) }; try { SFX.fanfare && SFX.fanfare(); } catch (e) {} shardFly(n); } return n; }
function shardFly(n) { try { const el = document.createElement("div"); el.className = "arfly"; el.textContent = "+◆" + n; document.body.appendChild(el); setTimeout(() => el.remove(), 1400); } catch (e) {} }
function shArch() {''')
# the card itself
rep('''  const card = k => { const E = ARCH[k], lv = archLv(k), nu = lv > (S.archR[k] | 0); return `<button class="arcard lv${lv}" data-act="archEntry" data-id="${k}">${lv ? archImg(E, lv, k) : `<div class="arimg glyph lock">?</div>`}<span>''',
    '''  const card = k => { const E = ARCH[k], lv = archLv(k), nu = lv > (S.archR[k] | 0), due = archDue(k), got = archGot(k), rr = archRar(k), down = lv && got < 1, fl = G.archFlip && G.archFlip.k === k && performance.now() - G.archFlip.at < 1500;
    if (down) return `<button class="arcard back r${rr}" data-act="archFlip" data-id="${k}"><div class="arback"><i>✦</i><b>${ARCH_RN[rr]}</b><small>A new record</small></div><span><b>Tap to reveal</b><small>+◆${due} for this card</small><em class="arpips"><i class="due"></i><i class="${lv >= 2 ? "due" : ""}"></i></em></span><i class="arnew">NEW</i></button>`;
    return `<button class="arcard lv${lv} r${rr}${lv >= 2 && !due ? " foil" : ""}${due ? " gold" : ""}${fl ? " flip" + (G.archFlip.lv >= 2 ? " f2" : "") : ""}" data-act="${due ? "archFlip" : "archEntry"}" data-id="${k}">${lv ? archImg(E, lv, k) : `<div class="arback sealed"><i>✦</i><b>${ARCH_RN[rr]}</b></div>`}${due ? `<div class="ardue">Tap to interpret · +◆${due}</div>` : ""}<span>''')
rep('''<em>${lv >= 2 ? "Interpreted" : lv ? "Fragment" : "Sealed"}</em></span>${nu ? `<i class="arnew">NEW</i>` : ""}</button>`; };''',
    '''<em><b class="arpips"><i class="${lv >= 1 ? (got >= 1 ? "on" : "due") : ""}"></i><i class="${lv >= 2 ? (got >= 2 ? "on" : "due") : ""}"></i></b>${lv >= 2 ? "Interpreted" : lv ? "Fragment" : "Sealed"} · ${ARCH_RN[rr]}</em></span>${nu && !due ? `<i class="arnew">NEW</i>` : ""}</button>`; };''')
# the header: cards and shards, collect all
rep('''${S.intro ? storyPanel() : ""}<div class="colsum">''', '''${S.intro ? storyPanel() : ""}${(() => { const tot = ARCH_ORD.length, got = ARCH_ORD.filter(k => archLv(k)).length, sh = ARCH_ORD.reduce((a, k) => a + archGot(k), 0), due = ARCH_ORD.reduce((a, k) => a + archDue(k), 0);
      return `<div class="arsum"><div><b>${got} / ${tot} cards</b><small>◆${sh} of ${tot * 2} earned · ◆1 for each card found and ◆1 more when it's interpreted</small><div class="colbar"><i style="width:${(sh / (tot * 2) * 100).toFixed(1)}%"></i></div></div>${due ? `<button class="btn amber sm" data-act="archAll">Collect all · ◆${due}</button>` : ""}</div>`; })()}<div class="colsum">''')
rep('  archEntry: d => openSheet({ type: "archives", id: d.id }),', '''  archEntry: d => openSheet({ type: "archives", id: d.id }),
  archFlip: d => { if (!ARCH[d.id]) return; const n = archClaim(d.id); if (n) { toast(`+◆${n} · ${ARCH[d.id].t}`, "win"); renderSheet(); } else openSheet({ type: "archives", id: d.id }); }, /* v661 */
  archAll: () => { let n = 0; for (const k of ARCH_ORD) n += archClaim(k, true); if (n) { toast(`+◆${n} from your Archive cards.`, "win"); try { SFX.fanfare && SFX.fanfare(true); } catch (e) {} shardFly(n); renderSheet(); } },''')
rep('.arcard.lv0{opacity:.62}', r'''.arcard.lv0{opacity:.78}
.arcard{--rc:#8c96a3;border-color:color-mix(in srgb,var(--rc) 55%,transparent);box-shadow:inset 0 0 0 1px color-mix(in srgb,var(--rc) 18%,transparent)}.arcard.r1{--rc:#4aa8ff}.arcard.r2{--rc:#b27aff}.arcard.r3{--rc:#ffcf5a;box-shadow:inset 0 0 0 1px rgba(255,207,90,.35),0 0 14px rgba(255,190,70,.18)}
.arback{position:relative;aspect-ratio:4/3;display:grid;place-items:center;align-content:center;gap:4px;background:radial-gradient(circle at 50% 42%,color-mix(in srgb,var(--rc) 35%,transparent),transparent 62%),repeating-linear-gradient(45deg,rgba(255,255,255,.035) 0 6px,transparent 6px 12px),linear-gradient(160deg,#1b1a24,#0b0a10);border-bottom:1px solid color-mix(in srgb,var(--rc) 40%,transparent)}
.arback::before{content:"";position:absolute;inset:8px;border:1px solid color-mix(in srgb,var(--rc) 55%,transparent);border-radius:8px}.arback i{font-style:normal;font-size:34px;color:var(--rc);text-shadow:0 0 16px var(--rc)}.arback b{font:600 10px/1 var(--f-display);letter-spacing:.2em;text-transform:uppercase;color:var(--rc)}.arback small{font-size:10.5px;color:#cfc2a8}
.arback.sealed{opacity:.75}.arcard.back{animation:arPulse 2.4s ease-in-out infinite}@keyframes arPulse{50%{box-shadow:0 0 18px color-mix(in srgb,var(--rc) 55%,transparent),inset 0 0 0 1px var(--rc)}}
.arcard.back span b{color:#fff3d0}.arcard.back span small{color:#ffd36b;font-weight:600}
.arpips{display:inline-flex;gap:3px;margin-right:6px;vertical-align:1px}.arpips i{width:7px;height:7px;border-radius:50%;border:1px solid color-mix(in srgb,var(--rc) 70%,transparent);display:inline-block}.arpips i.on{background:var(--rc);box-shadow:0 0 6px var(--rc)}.arpips i.due{background:#ffd36b;box-shadow:0 0 8px #ffd36b;animation:arDue 1.2s ease-in-out infinite}@keyframes arDue{50%{opacity:.45}}
.arcard.gold{border-color:#ffcf5a;box-shadow:0 0 16px rgba(255,200,80,.35),inset 0 0 0 1px #ffcf5a}.ardue{position:absolute;left:8px;right:8px;top:8px;padding:5px 8px;border-radius:8px;background:rgba(20,14,4,.82);border:1px solid #ffcf5a;color:#ffe29a;font:700 11px/1.2 var(--f-display);letter-spacing:.04em;text-align:center}
.arcard.foil::after{content:"";position:absolute;inset:0;pointer-events:none;border-radius:inherit;background:linear-gradient(115deg,transparent 30%,rgba(255,120,220,.16) 40%,rgba(120,220,255,.2) 47%,rgba(255,240,160,.18) 54%,transparent 64%);background-size:250% 100%;mix-blend-mode:screen;animation:arFoil 5s linear infinite}.arcard.r3.foil::after{animation-duration:3.2s}@keyframes arFoil{from{background-position:120% 0}to{background-position:-130% 0}}
.arcard.flip{animation:arFlipIn .9s cubic-bezier(.2,.8,.2,1) both}.arcard.flip::before{content:"";position:absolute;inset:0;z-index:3;pointer-events:none;background:radial-gradient(circle,rgba(255,255,255,.9),color-mix(in srgb,var(--rc) 60%,transparent) 40%,transparent 70%);animation:arFlash .9s ease-out both}@keyframes arFlipIn{0%{transform:perspective(700px) rotateY(90deg) scale(.96)}60%{transform:perspective(700px) rotateY(-8deg) scale(1.03)}100%{transform:none}}@keyframes arFlash{0%{opacity:1}100%{opacity:0}}
.arcard.f2{animation-name:arFlipIn}.arsum{display:flex;align-items:center;gap:10px;margin:10px 0;padding:10px 12px;border-radius:12px;border:1px solid rgba(226,196,138,.35);background:rgba(20,16,10,.6)}.arsum > div{flex:1;min-width:0;display:flex;flex-direction:column;gap:4px}.arsum b{font:600 14px/1.2 Georgia,serif;color:#f3e2b8}.arsum small{font-size:11.5px;color:#b9a888}
.arfly{position:fixed;left:50%;top:46%;z-index:9999;transform:translate(-50%,0);font:800 30px/1 var(--f-display);color:#e3b8ff;text-shadow:0 0 18px #b27aff,0 2px 0 #000;pointer-events:none;animation:arFly 1.3s ease-out forwards}@keyframes arFly{0%{opacity:0;transform:translate(-50%,10px) scale(.7)}20%{opacity:1;transform:translate(-50%,0) scale(1.15)}100%{opacity:0;transform:translate(-50%,-160px) scale(1)}}
@media (prefers-reduced-motion:reduce){.arcard.back,.arcard.foil::after,.arcard.flip,.arpips i.due{animation:none}}''')
rep('const GAME_V = 660', 'const GAME_V = 661')
open(p, 'w', encoding='utf-8').write(s)
