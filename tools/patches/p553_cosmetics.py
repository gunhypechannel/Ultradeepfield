# v553 cosmetics, the Wardrobe and a new Void Pass track (owner: "better payouts for battle pass, planet skins and other customization
# ... what else can we add to make it worth buying and grinding" -> "I want it all").
# Nine cosmetic kinds per season (banner, portrait frame, warp trail, homeworld aura, laser colour, Advisor outfit, wheel theme, clip
# frame, animated skin), two free ones (Pathfinder frame and trail) and a set aura for owning a whole season. S.cos = { own, eq }.
# What others can see is published in myPub().cos. Pass: premium tier 1 banner, 5 frame, 10 trail, 12 wheel theme, 15 Advisor outfit,
# 20 laser, 22 clip frame, 30 aura, 40 animated skin (with the skin); free tier 10 frame, 30 trail. Tiers already claimed this season
# pay their new cosmetics once (S.cosMig). Art the owner sends later drops in through COS_ART (art/season/s<n>-<kind>.webp).
# Frames and banners show on the profile, the leaderboards and chat; premium pass holders get a gold name in chat.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
def cut(a, b, new):
    global s
    assert s.count(a) == 1, a[:80]; i = s.index(a); j = s.index(b, i); s = s[:i] + new + s[j:]

JS = r'''
/* ---------- v553 cosmetics and the Wardrobe ---------- */
const COS_SEA = ["Leviathan", "Cube", "Pentarch", "Starhive", "Kraken", "Wyrm"], COS_C2 = ["#ffd36b", "#b8ffcf", "#9fb4ff", "#ff6a3a", "#ff6ad5", "#ff3b2a"];
const COS_K = { banner: ["Banner", "⚑", "b"], frame: ["Portrait frame", "◎", "f"], trail: ["Warp trail", "☄", "t"], aura: ["Homeworld aura", "◍", "a"], laser: ["Laser colour", "⌁", "l"], adv: ["Advisor outfit", "✧", "v"], wheel: ["Wheel theme", "☸", "w"], clip: ["Clip frame", "▣", "c"], skinx: ["Animated skin", "🪐", "x"] };
const COS_ORDER = ["banner", "frame", "trail", "aura", "laser", "adv", "wheel", "clip", "skinx"];
const COS_PT = { 1: "banner", 5: "frame", 10: "trail", 12: "wheel", 15: "adv", 20: "laser", 22: "clip", 30: "aura" }; /* premium tier -> kind (tier 40: skinx) */
const COS_ART = {}; /* id -> file, filled as the owner's season art arrives */
function cosDef(id) { const m = /^([a-z]+?)(F|S)?(\d)$/.exec(id || ""); if (!m || !COS_K[m[1]]) return null; const k = m[1], si = +m[3], free = m[2] === "F", set = m[2] === "S", K = COS_K[k];
  const col = VP_SEASONS[si] ? VP_SEASONS[si][1] : "#7af4ff", col2 = COS_C2[si] || "#ffffff";
  const n = set ? `${COS_SEA[si]} Ascendant aura` : free ? `Pathfinder ${K[0].toLowerCase()} · ${COS_SEA[si]}` : `${COS_SEA[si]} ${k === "adv" ? K[0] : K[0].toLowerCase()}`;
  const tier = set ? null : free ? (k === "frame" ? 10 : 30) : k === "skinx" ? VP_TIERS : +Object.keys(COS_PT).find(t => COS_PT[t] === k);
  return { id, k, si, free, set, n: n[0].toUpperCase() + n.slice(1), col: free ? "#9fe9ff" : col, col2: free ? col : col2, tier, art: COS_ART[id] || null }; }
const cosSx = (si = vpSeason()) => ((si % 6) + 6) % 6;
function cosOf() { if (!S) return { own: {}, eq: {} }; const C = S.cos = S.cos || { own: {}, eq: {} }; C.own = C.own || {}; C.eq = C.eq || {};
  const v = S.vp; if (v && typeof v.s === "number" && C.mig !== v.s) { C.mig = v.s; for (const i of v.cf || []) { const r = vpReward(i, false, v.s); if (r.cos) cosGive(r.cos, 1); } for (const i of v.cp || []) { const r = vpReward(i, true, v.s); if (r.cos) cosGive(r.cos, 1); } }
  return C; }
function cosGive(id, quiet) { const d = cosDef(id); if (!d || !S) return; const C = S.cos = S.cos || { own: {}, eq: {} }; C.own = C.own || {}; C.eq = C.eq || {}; const nu = !C.own[id]; C.own[id] = 1; if (!C.eq[d.k]) C.eq[d.k] = id;
  if (!d.set && !d.free) { const all = COS_ORDER.every(k => C.own[k + d.si]), sid = "auraS" + d.si; if (all && !C.own[sid]) { C.own[sid] = 1; C.eq.aura = sid; if (!quiet) setTimeout(() => toast(`Season set complete! ${cosDef(sid).n} unlocked and equipped.`, "win"), 900); } }
  if (nu && !quiet) G.cosNew = (G.cosNew || 0) + 1; dirty(); }
const cosPubOf = () => { const e = cosOf().eq, o = {}; for (const k of ["banner", "frame", "trail", "aura", "laser", "skinx"]) if (e[k]) o[COS_K[k][2]] = e[k]; return o; };
/* what a commander has equipped: yourself from your save, others from what they publish */
function cosEq(uid, k) { if (!uid) return null; if (uid === G.me) return S ? cosOf().eq[k] || null : null; const p = (G.players || {})[uid]; return p && p.cos ? p.cos[COS_K[k][2]] || null : null; }
const cosPrem = uid => uid === G.me ? !!(S && S.vp && S.vp.pr && S.vp.s === vpSeason()) : !!((G.players || {})[uid] || {}).vpr;
const cosFrame = (uid, inner) => { const d = cosDef(cosEq(uid, "frame")); return d ? `<span class="cfr${d.art ? " art" : ""}" style="--c1:${d.col};--c2:${d.col2}">${inner}${d.art ? `<img class="cfrimg" src="${d.art}" alt="">` : ""}</span>` : inner; };
const cosBannerStyle = id => { const d = cosDef(id); if (!d) return ""; return d.art ? `background-image:linear-gradient(90deg,rgba(4,8,16,.8),rgba(4,8,16,.25)),url(${d.art});background-size:cover;background-position:center` : `--c1:${d.col};--c2:${d.col2}`; };
const cosBannerCls = id => { const d = cosDef(id); return d ? (d.art ? " cbn art" : " cbn") : ""; };
function cosPreview(d, big) { const st = `--c1:${d.col};--c2:${d.col2}`, R = WHL_RUNES || "ᚠᚢᚦᚨᚱ";
  if (d.k === "banner") return `<div class="cpv pbn${d.art ? " art" : ""}" style="${cosBannerStyle(d.id)}"><span>${R[d.si * 3 % R.length]}${R[(d.si * 3 + 5) % R.length]}${R[(d.si * 3 + 9) % R.length]}</span></div>`;
  if (d.k === "frame") return `<div class="cpv pfr" style="${st}"><span class="cfr${d.art ? " art" : ""}" style="${st}"><i class="cfav">◉</i>${d.art ? `<img class="cfrimg" src="${d.art}" alt="">` : ""}</span></div>`;
  if (d.k === "trail") return `<div class="cpv ptr" style="${st}"><i class="pship">➤</i><b></b><b></b><b></b><b></b><b></b><b></b></div>`;
  if (d.k === "aura" || d.k === "skinx") return `<div class="cpv pau${d.set ? " set" : ""}${d.k === "skinx" ? " skx" : ""}" style="${st}${d.k === "skinx" && typeof VP_SEASONS !== "undefined" ? `;--sk:url(skins/${VP_SEASONS[d.si][2]}.webp)` : ""}"><i class="ring r1"></i><i class="ring r2"></i><i class="pl"></i><i class="mo m1"></i><i class="mo m2"></i></div>`;
  if (d.k === "laser") return `<div class="cpv plz" style="${st}"><i></i><i></i><i></i></div>`;
  if (d.k === "adv") return `<div class="cpv padv" style="${st}"><img src="${d.art || ADV_ART}" alt="" style="${d.art ? "" : advFxOf(d)}"></div>`;
  if (d.k === "wheel") return `<div class="cpv pwh" style="${st}"><i></i></div>`;
  if (d.k === "clip") return `<div class="cpv pcl" style="${st}"><i>ULTRA DEEP FIELD</i><b>VICTORY</b><small>${esc(COS_SEA[d.si])} season</small></div>`;
  return ""; }
/* the Advisor's season outfit: her own painted outfit when it exists, a season-coloured hologram until then */
const hueOf = hex => { const c = parseInt(String(hex).slice(1), 16), r = (c >> 16 & 255) / 255, g = (c >> 8 & 255) / 255, b = (c & 255) / 255, mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn; if (!d) return 0; let h = mx === r ? ((g - b) / d) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; return (h * 60 + 360) % 360; };
const advFxOf = d => d ? `filter:hue-rotate(${Math.round(hueOf(d.col) - 190)}deg) saturate(1.35) drop-shadow(0 0 10px ${d.col})` : "";
const advArt = () => { const d = S && cosDef(cosOf().eq.adv); return d && d.art ? d.art : ADV_ART; };
const advFx = () => { const d = S && cosDef(cosOf().eq.adv); return d && !d.art ? advFxOf(d) : ""; };
function shWardrobe() { const C = cosOf(), k = COS_K[sheet.k] ? sheet.k : "banner", cur = vpSeason(), sx = cosSx(cur);
  const ids = []; for (let si = 0; si < 6; si++) { const live = si <= sx || cur >= 6; for (const id of [k + si, k + "F" + si, k + "S" + si]) { const d = cosDef(id); if (!d) continue; if (d.free && k !== "frame" && k !== "trail") continue; if (d.set && k !== "aura") continue; if (live || C.own[id]) ids.push(id); } }
  const own = Object.keys(C.own).length, tot = ids.length, eqd = C.eq[k];
  const tabs = `<div class="cwtabs">${COS_ORDER.map(x => `<button class="${x === k ? "on" : ""}" data-act="cwTab" data-v="${x}"><i>${COS_K[x][1]}</i><span>${COS_K[x][0]}</span></button>`).join("")}</div>`;
  const card = id => { const d = cosDef(id), have = !!C.own[id], on = eqd === id; const src = d.set ? `Own every ${COS_SEA[d.si]} season cosmetic` : `Void Pass · Season ${d.si + 1} · ${d.free ? "free" : "premium"} tier ${d.tier}`;
    return `<div class="cwc${have ? "" : " lock"}${on ? " on" : ""}" style="--c1:${d.col};--c2:${d.col2}">${cosPreview(d)}<b>${esc(d.n)}</b><small>${have ? (on ? "Equipped" : "Owned") : esc(src)}</small>${have ? `<button class="btn ${on ? "ghost" : "amber"} sm" data-act="cwEq" data-k="${k}" data-id="${on ? "" : id}">${on ? "Unequip" : "Equip"}</button>` : `<button class="btn ghost sm" data-act="vpOpen">🔒 Void Pass</button>`}</div>`; };
  const bnId = C.eq.banner, frId = C.eq.frame;
  return `<div class="hd cwhd${cosBannerCls(bnId)}" style="${cosBannerStyle(bnId)}">${cosFrame(G.me, avCanvas(G.me, "avc big"))}<div style="flex:1;min-width:0"><div class="chapter">Customize</div><h2>Wardrobe</h2><p class="note">${own} cosmetic${own === 1 ? "" : "s"} owned. Banners, frames, trails, auras and lasers show to every commander.</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
    ${tabs}<div class="cwdesc">${{ banner: "Your banner runs behind your name on your profile and on the leaderboards.", frame: "A frame around your portrait everywhere it appears: profile, leaderboards, chat.", trail: "Your fleets leave this warp trail on the galaxy map. Everyone sees it.", aura: "A glowing aura and orbiting lights around your homeworld on the galaxy map.", laser: "Your ships fire in this colour in your battles and battle replays.", adv: "The Advisor wears this season outfit whenever she appears.", wheel: "The Holo Glyph Wheel in the Void Shop takes on these colours.", clip: "Your shared battle clips get this season frame.", skinx: "Brings your season planet skin to life: a pulsing corona on the map and in your world view." }[k]}</div>
    <div class="cwgrid">${ids.map(card).join("") || '<p class="note">Nothing here yet.</p>'}</div>`; }
'''
rep('profile: shProfile', 'profile: shProfile, wardrobe: shWardrobe')

# the pass: the new tracks
cut('function vpReward(i, prem, si = vpSeason()) {', 'const vpRwText = ', r'''function vpReward(i, prem, si = vpSeason()) { const t = i + 1, sx = ((si % 6) + 6) % 6; /* v553 cosmetics on both tracks */
  if (!prem) { if (t === 15) return { shards: 5, title: "Void Walker" }; const r = t % 10 === 0 ? { shards: 15, item: "mb2" } : t % 5 === 0 ? { shards: 5 } : [{ item: "crateM" }, { item: "xb_bronze" }, { item: "crateC" }, { item: "xf_bronze" }, { item: "crateG" }, { item: "xr_bronze" }, { m: 60000 * Math.ceil(t / 8), c: 40000 * Math.ceil(t / 8), g: 15000 * Math.ceil(t / 8) }, { item: "xs_bronze" }][i % 8];
    if (t === 10) r.cos = "frameF" + sx; if (t === 30) r.cos = "trailF" + sx; return r; }
  if (t === 25) return { shards: 10, title: vpInfo(si)[3] }; if (t === 35) return { shards: 10, look: si };
  if (t === VP_TIERS) return { shards: 100, skin: vpInfo(si)[2], cos: "skinx" + sx };
  const r = t === 10 ? { shards: 10, item: "o_staff_7" } : t === 20 ? { shards: 10, item: "mb3" } : t === 30 ? { shards: 10, item: "pAll_gold" } : { shards: 10, item: ["xb_silver", "xs_silver", "xr_silver", "bf_silver", "mb2", "xf_gold", "boost5", "bm_gold", "bc_gold", "bg_gold"][i % 10] };
  if (COS_PT[t]) r.cos = COS_PT[t] + sx; return r; }
''')
rep('const vpRwText = r => [r.shards ? `◆${r.shards}` : "",', JS + 'const vpRwText = r => [r.cos && cosDef(r.cos) ? cosDef(r.cos).n : "", r.shards ? `◆${r.shards}` : "",')
rep('function vpGrant(r) { if (r.shards) S.shards = (S.shards || 0) + r.shards;', 'function vpGrant(r) { if (r.cos) cosGive(r.cos); if (r.shards) S.shards = (S.shards || 0) + r.shards;')
rep('<span>${r.title ? "🎖" : r.look != null ? "✦" : r.skin ? "🪐" :', '<span>${r.cos && cosDef(r.cos) ? COS_K[cosDef(r.cos).k][1] : r.title ? "🎖" : r.look != null ? "✦" : r.skin ? "🪐" :')
rep('''<div class="vpmh"><b>Rewards</b><span class="note">Free · Premium</span></div>''', '''<div class="vpmh"><b>Rewards</b><span class="note">Free · Premium</span></div><button class="btn ghost wide sm cwopen" data-act="wardrobe">👗 Wardrobe · ${Object.keys(cosOf().own).length} cosmetics</button>''')
rep('<b>♛ Unlock Premium</b><small>A second reward on every tier: ◆${VP_PREM} back in shards over the season, speed-ups, boosters, an officer, forge boxes and the exclusive',
    '<b>♛ Unlock Premium</b><small>A second reward on every tier: a season banner the moment you buy, then a portrait frame, warp trail, wheel theme, Advisor outfit, laser colour, clip frame and homeworld aura, ◆${VP_PREM} back in shards, speed-ups, boosters and the exclusive')
rep("exclusive <b>${esc((typeof PXS !== \"undefined\" && PXS[skin] && PXS[skin].n) || skin)}</b> planet skin at tier ${VP_TIERS}.", "exclusive <b>${esc((typeof PXS !== \"undefined\" && PXS[skin] && PXS[skin].n) || skin)}</b> planet skin, animated, at tier ${VP_TIERS}.")
# premium unlock pays tier 1 at once is already true (tiers reached pay out); make tier 1 claimable the moment a season starts: the first tier needs 0 XP
# what other commanders see
rep('ttl: S.vpTitle || null });', 'ttl: S.vpTitle || null, cos: cosPubOf(), vpr: S.vp && S.vp.pr && S.vp.s === vpSeason() ? 1 : 0 });')
# profile: banner and frame; Wardrobe button
rep('return `<div class="hd">${avCanvas(uid, "avc big")}<div style="flex:1;min-width:0">', 'return `<div class="hd${cosBannerCls(cosEq(uid, "banner"))}" style="${cosBannerStyle(cosEq(uid, "banner"))}">${cosFrame(uid, avCanvas(uid, "avc big"))}<div style="flex:1;min-width:0">')
rep('${me ? `<div class="row2"><button class="btn wide" data-act="avatars">Change avatar</button>', '${me ? `<button class="btn amber wide" data-act="wardrobe">👗 Wardrobe</button>` : ""}\n    ${me ? `<div class="row2"><button class="btn wide" data-act="avatars">Change avatar</button>')
# leaderboards
rep('<span class="rkring">${al ? allyEmblem("", r.id) : avCanvas(r.id, "avc podav")}</span>', '<span class="rkring">${al ? allyEmblem("", r.id) : cosFrame(r.id, avCanvas(r.id, "avc podav"))}</span>')
rep('<button class="lb${r.me ? " me" : ""}${open ? " open" : ""}"', '<button class="lb${r.me ? " me" : ""}${open ? " open" : ""}${t !== "alliances" ? cosBannerCls(cosEq(r.id, "banner")) : ""}" style="${t !== "alliances" ? cosBannerStyle(cosEq(r.id, "banner")) : ""}"')
rep('avCanvas(r.id, "avc lbav")', 'cosFrame(r.id, avCanvas(r.id, "avc lbav"))')
# chat: frames and the gold name of premium pass holders
rep('<button class="cu" data-act="profile" data-u="${esc(m.u)}">${esc(nameOf(m.u))}</button>', '<button class="cu${cosPrem(m.u) ? " gold" : ""}" data-act="profile" data-u="${esc(m.u)}">${cosPrem(m.u) ? "♛ " : ""}${esc(nameOf(m.u))}</button>')
rep('${avCanvas(m.u, "avc cavc")}', '${cosFrame(m.u, avCanvas(m.u, "avc cavc"))}')
# actions
rep('  vpTitle: d => {', '''  wardrobe: () => { openSheet({ type: "wardrobe", k: "banner" }); }, /* v553 */
  cwTab: d => { if (sheet && sheet.type === "wardrobe") { sheet.k = d.v; renderSheet(); } },
  cwEq: d => { const C = cosOf(); if (d.id && !C.own[d.id]) return; if (d.id) C.eq[d.k] = d.id; else delete C.eq[d.k]; dirty(); try { syncPlayer(); } catch (e) {} if (d.k === "wheel") G.whlOff = null; try { SFX.click(); } catch (e) {} renderSheet(); },
  vpOpen: () => { closeSheet(); try { ACT.events(); ACT.evPick({ v: "pass" }); } catch (e) {} },
  vpTitle: d => {''')

css = r'''
/* v553 cosmetics */
.cfr{position:relative;display:inline-grid;place-items:center;border-radius:50%;padding:3px;background:conic-gradient(from var(--fa,0deg),var(--c1),var(--c2),var(--c1),var(--c2),var(--c1));animation:cfrs 6s linear infinite;box-shadow:0 0 12px color-mix(in srgb,var(--c1) 60%,transparent);flex:none}
.cfr>canvas,.cfr>.cfav{border-radius:50%;display:block}.cfr.art{background:none;box-shadow:none;padding:6px}.cfrimg{position:absolute;inset:-14%;width:128%;height:128%;pointer-events:none;object-fit:contain}
@property --fa{syntax:"<angle>";inherits:false;initial-value:0deg}@keyframes cfrs{to{--fa:360deg}}
.cbn{background-image:radial-gradient(120% 140% at 0% 0%,color-mix(in srgb,var(--c1) 45%,transparent),transparent 60%),radial-gradient(90% 120% at 100% 100%,color-mix(in srgb,var(--c2) 35%,transparent),transparent 60%),repeating-linear-gradient(120deg,color-mix(in srgb,var(--c1) 10%,transparent) 0 2px,transparent 2px 14px),linear-gradient(90deg,#0a1020,#0a0d1c)!important;border-color:color-mix(in srgb,var(--c1) 60%,transparent)!important}
.hd.cbn{border-radius:14px;padding:12px;margin-bottom:8px;border:1px solid}.lb.cbn{border:1px solid}
.cu.gold{color:#ffcf5a!important;text-shadow:0 0 8px rgba(255,207,90,.6)}
.cwopen{margin:6px 0}
.cwtabs{display:flex;gap:6px;overflow-x:auto;padding:2px 0 8px;scrollbar-width:none}.cwtabs::-webkit-scrollbar{display:none}
.cwtabs button{flex:none;display:flex;flex-direction:column;align-items:center;gap:2px;min-width:74px;padding:7px 6px;border-radius:12px;border:1px solid rgba(122,244,255,.25);background:rgba(8,18,30,.7);color:#d6e2ea;font-size:10.5px}
.cwtabs button i{font-style:normal;font-size:18px;color:#7af4ff}.cwtabs button.on{border-color:#7af4ff;background:rgba(122,244,255,.14);color:#fff}
.cwdesc{font-size:12.5px;color:var(--muted);margin:2px 0 10px}
.cwgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.cwc{display:flex;flex-direction:column;gap:5px;padding:8px;border-radius:14px;border:1px solid color-mix(in srgb,var(--c1) 45%,transparent);background:linear-gradient(160deg,color-mix(in srgb,var(--c1) 12%,transparent),rgba(8,14,24,.92) 60%)}
.cwc.on{box-shadow:0 0 0 2px var(--c1),0 0 18px color-mix(in srgb,var(--c1) 45%,transparent)}.cwc.lock .cpv{filter:grayscale(.7) brightness(.6)}.cwc b{font-size:13px}.cwc small{font-size:11px;color:var(--muted);flex:1}
.cpv{position:relative;aspect-ratio:4/3;border-radius:10px;overflow:hidden;background:radial-gradient(circle at 50% 50%,#121a33,#05070f 75%)}
.pbn{display:grid;place-items:center}.pbn.cbn span,.pbn span{font-size:28px;letter-spacing:.3em;color:color-mix(in srgb,var(--c1) 70%,#fff);text-shadow:0 0 12px var(--c1);opacity:.85}
.pbn:not(.art){background-image:radial-gradient(120% 140% at 0% 0%,color-mix(in srgb,var(--c1) 55%,transparent),transparent 60%),radial-gradient(90% 120% at 100% 100%,color-mix(in srgb,var(--c2) 45%,transparent),transparent 60%),repeating-linear-gradient(120deg,color-mix(in srgb,var(--c1) 14%,transparent) 0 2px,transparent 2px 14px),linear-gradient(90deg,#0a1020,#0a0d1c)}.pbn.art{background-size:cover}.pbn.art span{display:none}
.pfr{display:grid;place-items:center}.pfr .cfr{width:62%;aspect-ratio:1}.cfav{font-style:normal;width:100%;height:100%;display:grid!important;place-items:center;background:#0b1626;color:#9fb4c8;font-size:34px}
.ptr .pship{position:absolute;left:68%;top:46%;font-style:normal;color:#fff;font-size:20px;text-shadow:0 0 8px var(--c1);animation:ptrs 1.6s ease-in-out infinite}
.ptr b{position:absolute;top:50%;width:12px;height:12px;margin-top:-6px;border-radius:50%;background:radial-gradient(circle,#fff,var(--c1) 40%,transparent 70%);animation:ptrd 1.2s linear infinite}
.ptr b:nth-child(odd){background:radial-gradient(circle,#fff,var(--c2) 40%,transparent 70%)}.ptr b:nth-child(2){animation-delay:-.2s}.ptr b:nth-child(3){animation-delay:-.4s}.ptr b:nth-child(4){animation-delay:-.6s}.ptr b:nth-child(5){animation-delay:-.8s}.ptr b:nth-child(6){animation-delay:-1s}.ptr b:nth-child(7){animation-delay:-1.2s}
@keyframes ptrd{from{left:66%;transform:scale(1);opacity:1}to{left:4%;transform:scale(.25);opacity:0}}@keyframes ptrs{50%{transform:translateY(-3px)}}
.pau .pl{position:absolute;left:50%;top:50%;width:36%;aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle at 35% 30%,#9fb8d8,#2a3f66 55%,#0b1424);box-shadow:0 0 24px color-mix(in srgb,var(--c1) 70%,transparent)}
.pau.skx .pl{background:var(--sk) center/cover;animation:skx 2.4s ease-in-out infinite}@keyframes skx{50%{box-shadow:0 0 38px var(--c1),0 0 70px color-mix(in srgb,var(--c2) 60%,transparent);filter:brightness(1.25) saturate(1.3)}}
.pau .ring{position:absolute;left:50%;top:50%;aspect-ratio:1;border-radius:50%;transform:translate(-50%,-50%);border:2px solid transparent}
.pau .r1{width:62%;border-color:var(--c1) transparent var(--c2) transparent;animation:pauR 5s linear infinite;box-shadow:0 0 14px var(--c1)}.pau .r2{width:78%;border-color:transparent color-mix(in srgb,var(--c2) 80%,transparent);border-style:dashed;animation:pauR 9s linear infinite reverse}
.pau.set .r1{border-width:3px;box-shadow:0 0 26px var(--c1),inset 0 0 18px var(--c1)}
.pau .mo{position:absolute;left:50%;top:50%;width:7px;height:7px;margin:-3.5px;border-radius:50%;background:#fff;box-shadow:0 0 10px var(--c1),0 0 4px #fff;animation:pauM 4s linear infinite}.pau .m2{animation-duration:6.5s;animation-direction:reverse;background:var(--c2)}
@keyframes pauR{to{transform:translate(-50%,-50%) rotate(360deg)}}@keyframes pauM{from{transform:rotate(0) translateX(46px)}to{transform:rotate(360deg) translateX(46px)}}
.plz i{position:absolute;left:8%;height:3px;border-radius:3px;background:linear-gradient(90deg,transparent,var(--c1),#fff);box-shadow:0 0 10px var(--c1);animation:plz 1s linear infinite}.plz i:nth-child(1){top:30%;width:40%}.plz i:nth-child(2){top:50%;width:55%;animation-delay:-.35s;background:linear-gradient(90deg,transparent,var(--c2),#fff);box-shadow:0 0 10px var(--c2)}.plz i:nth-child(3){top:70%;width:35%;animation-delay:-.7s}
@keyframes plz{from{transform:translateX(-60%);opacity:0}30%{opacity:1}to{transform:translateX(180%);opacity:0}}
.padv img{position:absolute;left:50%;bottom:0;height:100%;width:auto;max-width:none;transform:translateX(-50%)}
.pwh i{position:absolute;left:50%;top:50%;width:66%;aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;background:radial-gradient(circle,#05070f 0 22%,transparent 23%),repeating-conic-gradient(color-mix(in srgb,var(--c1) 70%,transparent) 0 18deg,color-mix(in srgb,var(--c2) 45%,transparent) 18deg 36deg);box-shadow:0 0 0 3px var(--c1),0 0 20px var(--c1);animation:pauR 4s linear infinite}
.pcl{display:flex;flex-direction:column;align-items:center;justify-content:space-between;padding:8px 0;aspect-ratio:9/12;margin:0 auto;width:62%;border:2px solid var(--c1);box-shadow:inset 0 0 18px var(--c1);background:linear-gradient(180deg,#05070f,#0c1630 50%,#05070f)}
.pcl i{font-style:normal;font-size:9px;letter-spacing:.1em;color:#ffcf5a}.pcl b{font:900 15px var(--f-display,sans-serif);color:var(--c1);text-shadow:0 0 10px var(--c1)}.pcl small{font-size:9px;color:var(--c2)}
'''
rep('.shopgrid{display:grid;', css.strip() + '\n.shopgrid{display:grid;')
s2 = re.sub(r"GAME_V = 552\b", "GAME_V = 553", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
