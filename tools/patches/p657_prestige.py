# v657 (owner: "Do it all" to: top ships need something money can't buy; point big spenders at cosmetics).
# (1) Blueprints earned in battle, never sold: the Dreadnought needs 1 Ancient Relic (pyramids), the Reaper 2 Beast Cores (monster
#     hunts), the Cube Destroyer 5 Cube Fragments (Cube fights). Once per account: the blueprint unlocks the ship for good. Anyone who
#     already has one keeps it. Components drop from fresh wins in addReport; the detail sheet, the build buttons and the path show it.
# (2) The Void Shop opens on a Style section: hull finishes (by tier), premium tiers, fleet captains to recruit, and planet skins.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)

rep('function pathCard(m, miss, rw) {', r'''/* ---------- v657 blueprints: the top ships need a piece earned in battle, once; it can never be bought ---------- */
const BP = { bastion: { c: "relic", need: 1 }, dreadnought: { c: "bcore", need: 2 }, worldbreaker: { c: "cfrag", need: 5 } };
const BPC = { relic: { n: "Ancient Relic", ic: "⌬", col: "#ffd27a", src: "Explore and win at pyramids", ch: .5 }, bcore: { n: "Beast Core", ic: "✶", col: "#ff8a5a", src: "Win monster hunts", ch: .4 }, cfrag: { n: "Cube Fragment", ic: "◈", col: "#7dff9a", src: "Win Cube fights", ch: 1 } };
function bpOk(k) { const B0 = BP[k]; if (!B0 || !S) return true; S.bpU = S.bpU || {}; if (S.bpU[k]) return true;
  let has = 0; try { has = own(k) + (S.sq || []).filter(x => x.k === k).length; } catch (e) {} if (has > 0) { S.bpU[k] = 1; dirty(); return true; } return false; }
const bpHave = c => ((S && S.bpc) || {})[c] || 0;
function bpNeed(k) { const B0 = BP[k], C = BPC[B0.c]; toast(`${SH[k].n} needs its blueprint: ${C.ic} ${B0.need} ${C.n}${B0.need > 1 ? "s" : ""} (you have ${bpHave(B0.c)}). ${C.src}. They can't be bought.`, "warn"); }
function bpBox(k) { const B0 = BP[k]; if (!B0) return ""; const C = BPC[B0.c], ok = bpOk(k), h = bpHave(B0.c);
  return `<div class="tcreq bpreq${ok ? " ok" : ""}" style="--bc:${C.col}"><b>${C.ic} ${ok ? "Blueprint unlocked" : `${C.n}s ${h} / ${B0.need}`}</b><small>${ok ? `You earned the ${esc(SH[k].n)} blueprint in battle. Build as many as you like.` : `The ${esc(SH[k].n)} blueprint is earned, never bought. ${C.src}: each win can recover a ${C.n}. With ${B0.need}, the ship unlocks for good.`}</small></div>`; }
/* a fresh win of the right kind can recover a component; when there are enough, the blueprint unlocks */
function bpDrop(rep) { if (!rep || rep.test || !S || rep.kind !== "attack" || rep.winner !== "a") return; const T = now(); if (rep.at && T - rep.at > 10 * 60000) return;
  S.bpGot = S.bpGot || {}; if (rep.id && S.bpGot[rep.id]) return; const t = String(rep.title || "");
  const c = /^Hunt:/.test(t) ? "bcore" : /^Guardians of /.test(t) ? "relic" : /Cube/.test(t) && !/^(Hive raid|Cube strike)/.test(t) ? "cfrag" : null; if (!c) return;
  const ks = Object.keys(BP).filter(k => BP[k].c === c && !bpOk(k)); if (!ks.length) return; if (Math.random() >= BPC[c].ch) return;
  if (rep.id) { S.bpGot[rep.id] = 1; const ids = Object.keys(S.bpGot); if (ids.length > 300) delete S.bpGot[ids[0]]; }
  const C = BPC[c], n = c === "cfrag" && /(Super|Omega|Elite|Warden)/.test(t) ? 2 : 1; S.bpc = S.bpc || {}; S.bpc[c] = (S.bpc[c] || 0) + n; dirty();
  for (const k of ks) { const B0 = BP[k]; if (S.bpc[c] >= B0.need && !S.bpU[k]) { S.bpc[c] -= B0.need; S.bpU[k] = 1;
      setTimeout(() => { try { note(`Blueprint unlocked: the ${SH[k].n}. Your Shipyard can build it now.`, "win"); SFX.fanfare && SFX.fanfare(); advHolo(`Commander, the ${C.n}s are enough. Our engineers have the ${SH[k].n} blueprint. The Shipyard can build it now.`, true); } catch (e) {} }, 2600); return; } }
  const k0 = ks[0]; setTimeout(() => { try { note(`${C.ic} ${C.n} recovered: ${S.bpc[c]} / ${BP[k0].need} toward the ${SH[k0].n} blueprint.`, "win"); } catch (e) {} }, 2200); }
function pathCard(m, miss, rw) {''')
rep('ready = !miss,\n    pct = tot', 'ready = !miss && bpOk(m.k), bpx = BP[m.k] && !bpOk(m.k) ? `<span class="pchip bp" style="--bc:${BPC[BP[m.k].c].col}">${BPC[BP[m.k].c].ic} ${BPC[BP[m.k].c].n}s <b>${bpHave(BP[m.k].c)}/${BP[m.k].need}</b></span>` : "",\n    pct = tot')
rep('const chips = E.map(([k, l]) => { const ok = lvlOf(k) >= l, pk = pathKind(k);', 'const chips = bpx + E.map(([k, l]) => { const ok = lvlOf(k) >= l, pk = pathKind(k);')
rep('${ready ? "" : `<div class="pth-req">${chips}</div>`}', '${ready ? "" : `<div class="pth-req">${chips}</div>`}')
rep('`${met}/${tot} requirements met`', '(miss ? `${met}/${tot} requirements met` : "Blueprint needed")')
# build gates
rep('    if (missing(def.req).length || allyBlock(def)) return;\n', '    if (missing(def.req).length || allyBlock(def)) return;\n    if (d.kind !== "def" && !bpOk(d.k)) return bpNeed(d.k); /* v657 */\n')
rep('    if (def.max || def.tc) return toast(`${def.n} can only be built at your homeworld.`, "warn");', '    if (def.max || def.tc) return toast(`${def.n} can only be built at your homeworld.`, "warn");\n    if (!bpOk(k)) return bpNeed(k); /* v657 */')
rep('function addReport(rep) { battleXP(rep); recordBattle(rep); try { advBattle(rep); } catch (e) {}', 'function addReport(rep) { battleXP(rep); recordBattle(rep); try { advBattle(rep); } catch (e) {} try { bpDrop(rep); } catch (e) {}')
rep('mid = `${kind === "s" && TITAN_INFO[k] ? `<div class="tcreq', 'mid = `${kind === "s" && BP[k] ? bpBox(k) : ""}${kind === "s" && TITAN_INFO[k] ? `<div class="tcreq')
rep('.chipq.met{', '.pchip.bp{cursor:default;border-color:var(--bc);color:var(--bc);background:color-mix(in srgb,var(--bc) 10%,transparent)}.bpreq{border-color:color-mix(in srgb,var(--bc) 60%,transparent)!important}.bpreq b{color:var(--bc)}\n.chipq.met{')

# (2) the shop opens on Style
rep('const SHOP_CI = { packs: "◆",', 'const SHOP_CI = { style: "✧", packs: "◆",')
rep('''  const SECS = (window.udfShop && G.mode === "online" ? [["packs", "Packs"]] : [])''', '''  const SECS = [["style", "Style"]].concat(window.udfShop && G.mode === "online" ? [["packs", "Packs"]] : [])''')
rep('''const cat = sheet.cat = sheet.cat || (window.udfShop && G.mode === "online" ? "packs" : "boost")''', '''const cat = sheet.cat = sheet.cat || "style"''')
rep('''let body; const secBody = k => k === "packs" ? packsBody()''', '''let body; const secBody = k => k === "style" ? styleBody() : k === "packs" ? packsBody()''')
rep('function shShop() {', r'''/* v657 the shop's first section: looks and status, not progress */
function styleBody() { const pt = premT(), ks = Object.keys(SH).filter(k => { try { return own(k) > 0; } catch (e) { return false; } }), hk = SH[G.hullK] ? G.hullK : ks[0] || "battleship", nf = Object.values(HULL_F).filter(F => pt >= F.t).length;
  const sw = Object.entries(HULL_F).map(([f, F]) => `<i class="${pt >= F.t || G.owner ? "" : "lk"}" style="background:url(art/hull/${f}.webp?v=${HULL_TV}) center/200%,${F.sw}" title="${esc(F.n)} · Premium Tier ${F.t}"></i>`).join("");
  return `<p class="note">Make your empire unmistakable. Looks and status only: none of this changes a battle, and other commanders see all of it.</p>
  <div class="sty"><div class="styc"><div class="stys">${sw}</div><b>Hull finishes</b><small>${nf ? `${nf} of ${Object.keys(HULL_F).length} unlocked at Premium Tier ${pt}.` : "Metal, gem and holo finishes for your warships, with a second trim colour."} Glyph Holo, Diamond, Obsidian and more, unlocked by Premium tier.</small><button class="btn amber sm" data-act="hullGo" data-k="${hk}">Style your ships</button></div>
    <div class="styc"><div class="stypt"><span>${pt ? "Tier " + pt : "Premium"}</span></div><b>Premium tiers</b><small>${pt ? `You're at Premium Tier ${pt}. Each tier adds an exclusive planet skin, more hull finishes and a lasting bonus.` : "Every tier adds an exclusive planet skin, hull finishes and a lasting bonus. Tiers never expire."}</small><button class="btn ghost sm" data-act="premOpen">See the tiers</button></div>
    <div class="styc wide"><b>Fleet captains</b><small>A face for every fleet, each with a small perk. Recruit once, keep forever.</small>${capRow()}</div>
    <div class="styc"><div class="stypl">${PS_SKINS.slice(0, 4).map(x => `<canvas data-px="${x[0]}" role="img" aria-label="${esc(x[2])}"></canvas>`).join("")}</div><b>Planet skins</b><small>Premium looks for any world you hold, each with a small production perk.</small><button class="btn ghost sm" data-act="shopCat" data-v="skins">Browse skins</button></div></div>`; }
function shShop() {''')
rep('.chipq.met{', r'''.sty{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,230px),1fr));gap:10px;margin:8px 0 4px}.styc{display:flex;flex-direction:column;gap:6px;padding:12px;border-radius:14px;border:1px solid rgba(255,210,120,.28);background:radial-gradient(120% 120% at 0 0,rgba(255,200,110,.12),transparent 60%),rgba(6,12,22,.6);min-width:0}
.styc.wide{grid-column:1/-1}.styc b{font-family:var(--f-display);letter-spacing:.06em;color:#ffe2a8}.styc small{color:var(--muted);font-size:12px;line-height:1.4}.styc .btn{align-self:flex-start;margin-top:auto}
.stys{display:flex;gap:4px;flex-wrap:wrap}.stys i{width:26px;height:26px;border-radius:6px;border:1px solid rgba(255,255,255,.25);box-shadow:inset 0 0 6px rgba(255,255,255,.25)}.stys i.lk{opacity:.35;filter:grayscale(.6)}
.stypt span{display:inline-block;font-family:var(--f-display);font-size:13px;letter-spacing:.12em;padding:4px 12px;border-radius:999px;color:#1a1200;background:linear-gradient(135deg,#7a5410,#ffe08a 45%,#c8901e 60%,#fff3c0)}
.stypl{display:flex;gap:6px}.stypl canvas{width:56px;height:56px;border-radius:50%;display:block}
.chipq.met{''')
# path cards: the painted card art (owner: "can't we use art thumbnails")
rep('<div class="pth-art"><canvas ${sh ? `data-ship="${m.k}"` : `data-rs="${m.k}|1"`} role="img" aria-label="${esc(m.n)}"></canvas></div>',
    '<div class="pth-art">${ART[m.k] ? `<img src="${ART[m.k]}" alt="${esc(m.n)}" loading="lazy">` : `<canvas ${sh ? `data-ship="${m.k}"` : `data-rs="${m.k}|1"`} role="img" aria-label="${esc(m.n)}"></canvas>`}</div>')
rep('.pth-art canvas{width:84px;height:56px;display:block}', '.pth-art canvas{width:84px;height:56px;display:block}.pth-art img{width:100%;height:100%;object-fit:cover;display:block}.pth-art{position:relative}.pth-art::after{content:"";position:absolute;inset:0;border-radius:inherit;box-shadow:inset 0 0 0 1px rgba(255,255,255,.08),inset 0 -14px 18px -10px rgba(0,0,0,.55);pointer-events:none}')
rep('@media (max-width:360px){.pth{grid-template-columns:64px minmax(0,1fr);grid-template-areas:"a b" "g g" "q q" "r r"}.pth-art,.pth-art canvas{width:64px;height:44px}', '@media (max-width:360px){.pth{grid-template-columns:72px minmax(0,1fr);grid-template-areas:"a b" "g g" "q q" "r r"}.pth-art,.pth-art canvas{width:72px;height:54px}')
rep('const GAME_V = 656', 'const GAME_V = 657')
open(p, 'w', encoding='utf-8').write(s)
