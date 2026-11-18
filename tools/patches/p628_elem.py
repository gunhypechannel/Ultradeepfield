# v628: elements balanced and expanded. See p628_elem.js and p628_elui.js.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
js = open('tools/patches/p628_elem.js', encoding='utf-8').read()
ui = open('tools/patches/p628_elui.js', encoding='utf-8').read()
rep('const runePct = e => S ? Math.round((runeOn(e)', 'const runePct0 = e => S ? Math.round((runeOn(e)')
rep('  note(`${why}: +${n} rune${n > 1 ? "s" : ""} (${got.join(", ")}).`, "win");\n}\n', '  note(`${why}: +${n} rune${n > 1 ? "s" : ""} (${got.join(", ")}).`, "win");\n}\n' + js)
a = s.index('function mElem() {'); b = s.index('/* ---------- v625 the Commander tab'); s = s[:a] + ui + s[b:]
# affinity in boss and monster fights
rep('const { res, rise } = wbFightRise(() => stacksOf(f.n, techOf(null), G.me), () => stacksOf({ [D.k]: n0 }, { wbSh: shK }, "wboss"), D.k, n0);', 'const { res, rise } = wbFightRise(() => stacksOf(f.n, techEl(BOSS_EL[key]), G.me), () => stacksOf({ [D.k]: n0 }, { wbSh: shK }, "wboss"), D.k, n0);')
rep('dName: D.n, wb: key, wbSh: shK,', 'dName: D.n, wb: key, elAff: elAffRep(BOSS_EL[key]), wbSh: shK,')
rep('{ res, rise } = sbFightRise(() => stacksOf(f.n, techOf(null), G.me), mkD,', '{ res, rise } = sbFightRise(() => stacksOf(f.n, techEl(BOSS_EL[k]), G.me), mkD,')
rep('dName: D.n, sbk: k, sbForm: form,', 'dName: D.n, sbk: k, elAff: elAffRep(BOSS_EL[k]), sbForm: form,')
rep('res = simulate(stacksOf(f.n, techVs(x), G.me).concat(allyStacks(f.allies, x.lvl)), xStacks(x));', 'res = simulate(stacksOf(f.n, techElVs(x), G.me).concat(allyStacks(f.allies, x.lvl)), xStacks(x));')
rep('boss: !!x.boss, mon: x.mon || null, lvl: x.lvl,', 'boss: !!x.boss, mon: x.mon || null, elAff: x.mon ? elAffRep(MON_EL[x.mon]) : undefined, lvl: x.lvl,')
rep('function playBattle(r) {\n', 'function playBattle(r) {\n  if (r && r.elAff && r.elAff.pct > 0) setTimeout(() => { if (battle) elAffFlash(r.elAff); }, 1400); /* v628 */\n')
# shard sources
rep('S.shards = (S.shards || 0) + sh; rep.shards = sh; }', 'S.shards = (S.shards || 0) + sh; rep.shards = sh; } grantShards(x.mon ? 2 : 1, x.mon ? `Slain ${x.name}` : `Raided ${x.name}`, x.mon ? MON_EL[x.mon] : null); /* v628 */')
rep('const sh = pyrShards(y.lvl); S.shards = (S.shards || 0) + sh; let extra = `◆${sh}`;', 'const sh = pyrShards(y.lvl); S.shards = (S.shards || 0) + sh; let extra = `◆${sh}`; grantShards(1 + (y.lvl >= 4 ? 1 : 0) + (y.lvl >= 7 ? 1 : 0), y.name); /* v628 */')
rep('t.claimed = true; S.shards = (S.shards || 0) + 1;', 't.claimed = true; S.shards = (S.shards || 0) + 1; grantShards(2, "Daily task"); /* v628 */')
rep('S.helpDay.n++; S.helpsGiven', 'S.helpDay.n++; grantShards(1, "Alliance help", null, { quiet: 1 }); /* v628 */ S.helpsGiven')
rep('    const rn = wbRunes(key, dm, st.last[key]); if (rn) {', '    if (BOSS_EL[key]) { grantShards(4, `${D.n} core`, BOSS_EL[key], { nocap: 1, quiet: 1 }); extra += `, 4 ${ELEM[BOSS_EL[key]].n} shards`; } /* v628 */\n    const rn = wbRunes(key, dm, st.last[key]); if (rn) {')
rep('S.shards = (S.shards || 0) + sh; grantRunes(rn, `${D.n} core`); giveItem(it);', 'S.shards = (S.shards || 0) + sh; grantRunes(rn, `${D.n} core`); if (BOSS_EL[k]) grantShards(4, `${D.n} core`, BOSS_EL[k], { nocap: 1 }); giveItem(it);')
# the cache: Void Shop and Glyph Wheel
rep('SHOP.runes3.cat = "legacy";', 'SHOP.runes3.cat = "legacy"; SHOP.rcache = { cat: "special", n: "Rune Shard Cache", ic: "ᛦ", cost: 6, d: () => `Five rune shards of today\'s Trial element${typeof trialEl === "function" && S ? ` (${ELEM[trialEl()].n})` : ""}. They count toward the weekly shard limit.`, use: () => { const e = trialEl(); if (eshLeft(e) < 5) return toast(`This week\'s ${ELEM[e].n} shard limit is nearly reached (${eshLeft(e)} left). Open it on another day.`, "warn"), false; grantShards(5, "Rune Shard Cache", e); return "Shards added."; } }; /* v628 */')
rep('{ k: "mb2", g: "ᛃ", l: "🧰+", col: "#5dff9a", w: 2.5 },', '{ k: "mb2", g: "ᛃ", l: "🧰+", col: "#5dff9a", w: 2.5 }, { k: "rcache", g: "ᛦ", l: "ᛦ", col: "#e06bd8", w: 4 },')
# actions
rep('  runeSlot: d => act(() => {', '''  elTrial: () => act(() => trialRun()),
  ringMaster: d => act(() => { const e = d.e; if (!ELEM[e] || !mastOpen(e)) return toast("Fill a top-tier ring to begin Mastery.", "warn"); if (ringM(e) >= MAST_MAX) return toast("This ring is mastered."); S.runes = S.runes || {}; if ((S.runes[e] || 0) < MAST_COST) return toast(`Mastery takes ${MAST_COST} spare ${ELEM[e].n} runes.`, "warn");
    S.runes[e] -= MAST_COST; S.ringM = S.ringM || {}; S.ringM[e] = ringM(e) + 1; toast(`${ELEM[e].n} Mastery ${S.ringM[e]}: +${(S.ringM[e] * MAST_PER).toFixed(1)}%.`, "win"); try { fgSnd("rn_ring"); } catch (er) {} }),
  elTrans: d => act(() => { const f = d.f, e = d.e; if (!ELEM[f] || !ELEM[e] || f === e) return; S.runes = S.runes || {}; if ((S.runes[f] || 0) < 3) return toast(`You need 3 spare ${ELEM[f].n} runes.`, "warn"); S.runes[f] -= 3; S.runes[e] = (S.runes[e] || 0) + 1; toast(`3 ${ELEM[f].n} runes became 1 ${ELEM[e].n} rune.`, "win"); try { fgSnd("rn_socket"); } catch (er) {} }), /* v628 */
  runeSlot: d => act(() => {''')
# the Feedback pill sits above the chat bar, whatever its height on this phone
rep('/* the Advisor\'s pill folds to its portrait while you scroll', '''setInterval(() => { try { const cb = document.querySelector(".chatbar"), r = cb && cb.getBoundingClientRect(); document.documentElement.style.setProperty("--fbB", r && r.height > 0 && r.top < innerHeight && !document.getElementById("battle") ? Math.round(innerHeight - r.top + 8) + "px" : ""); } catch (e) {} }, 1200); /* v628 */
/* the Advisor's pill folds to its portrait while you scroll''')
css = ('#fbBtn{bottom:var(--fbB,calc(env(safe-area-inset-bottom,0px) + 72px))!important}body:has(#battle) #fbBtn{display:none}'
  '.elshd,.elmast,.eltr,.eltrial,.elpairs,.elcw{flex-shrink:0}.elshd{display:flex;flex-direction:column;gap:4px;margin:6px 0 8px}.elsg{display:flex;gap:3px}.elsg i{flex:1;height:7px;border-radius:4px;background:rgba(255,255,255,.08)}.elsg i.on{background:var(--c);box-shadow:0 0 6px var(--c)}.elshd small{font-size:11.5px;color:var(--muted)}.elshd small b{color:#fff}'
  '.elmast{display:flex;align-items:center;gap:10px;margin-top:10px;padding:8px 10px;border-radius:12px;border:1px solid color-mix(in srgb,var(--c) 45%,transparent);background:color-mix(in srgb,var(--c) 8%,transparent)}.elmast>div{flex:1;min-width:0;display:flex;flex-direction:column;gap:3px}.elmast b{font-size:13px}.elmast small{font-size:11.5px;color:var(--muted)}'
  '.eltr{margin-top:10px;display:flex;flex-direction:column;gap:6px}.eltr small{font-size:11.5px;color:var(--muted)}.eltr>div{display:flex;flex-wrap:wrap;gap:6px}.eltr em{font-size:12px;color:var(--muted);font-style:normal;opacity:.7}.eltr .elchip{flex:none}'
  '.eltrial{display:flex;align-items:center;gap:10px;margin-top:12px;padding:10px 12px;border-radius:14px;border:1px solid color-mix(in srgb,var(--c) 55%,transparent);background:radial-gradient(80% 120% at 0 50%,color-mix(in srgb,var(--c) 22%,transparent),transparent 70%),rgba(8,12,20,.8)}.elti{font-size:30px;width:44px;height:44px;display:grid;place-items:center;border-radius:50%;background:color-mix(in srgb,var(--c) 20%,#0a0e16);box-shadow:0 0 16px color-mix(in srgb,var(--c) 50%,transparent);flex:none}.eltrial>div{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}.eltrial small{font-size:10px;letter-spacing:.16em;color:var(--c)}.eltrial b{font:700 16px var(--f-display)}.eltrial em{font-style:normal;font-size:11.5px;color:var(--muted);line-height:1.35}'
  '.elpairs,.elcw{margin-top:14px}.elsh small{font-size:11px;color:var(--muted)}.elpr{display:grid;grid-template-columns:auto 1fr auto;grid-template-rows:auto auto;column-gap:10px;align-items:center;padding:7px 10px;margin-top:6px;border-radius:12px;background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.06);opacity:.75}.elpr.on{opacity:1;border-color:rgba(255,210,90,.5);background:rgba(255,210,90,.07)}.elpr i{grid-row:span 2;font-style:normal;font-size:17px;letter-spacing:-2px;width:44px;text-align:center}.elpr b{font-size:13.5px}.elpr small{grid-column:2;font-size:11.5px;color:var(--muted)}.elpr em{grid-row:1/span 2;grid-column:3;font-style:normal;font-size:11px;color:var(--muted);text-align:right}.elpr.on em{color:#ffd25a;font-weight:700}.elpr.harm i{color:#ffd25a;font-size:22px}'
  '.elcw p{margin:6px 0 4px;font-size:13px;line-height:1.6}.elcw>small{font-size:11.5px;color:var(--muted);line-height:1.45;display:block}.elcw>small b{color:#fff}'
  '.elways{display:flex;flex-wrap:wrap;gap:5px;margin-top:10px}.elways span{font-size:11.5px;padding:4px 8px;border-radius:10px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.07);color:#cfe3ee}'
  '.elinfo{margin-top:10px;padding:10px 12px;border-radius:12px;background:rgba(255,255,255,.04)}.elinfo p{margin:0 0 6px;font-size:12px;line-height:1.45;color:var(--muted)}.elinfo p:last-child{margin:0}'
  '.elaff{position:fixed;left:50%;top:28%;transform:translateX(-50%);z-index:9999;display:flex;flex-direction:column;align-items:center;gap:4px;padding:10px 18px;border-radius:14px;background:rgba(6,10,18,.82);border:1px solid var(--c);box-shadow:0 0 30px var(--c);pointer-events:none;animation:elaff 2.6s ease-out forwards}.elaff b{font:900 22px var(--f-display);letter-spacing:.12em;color:var(--c);text-shadow:0 0 12px var(--c)}.elaff span{font-size:13px;color:#fff}@keyframes elaff{0%{opacity:0;transform:translateX(-50%) scale(.6)}12%{opacity:1;transform:translateX(-50%) scale(1.08)}20%{transform:translateX(-50%) scale(1)}80%{opacity:1}100%{opacity:0;transform:translateX(-50%) translateY(-14px)}}\n')
i = s.index('</style>', s.index('#celeb{position:fixed')); s = s[:i] + css + s[i:]
s2 = re.sub(r"GAME_V = 627\b", "GAME_V = 628", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
