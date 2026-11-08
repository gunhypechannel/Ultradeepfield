# v338 Stage 3: the forge points to where each material comes from ("Find" opens the map finder on its source), a converter (3 of one
# kind make 1 of another at the same rarity, so a surplus can fill a gap without creating value), and Material Selection Boxes
# (pick any kind at the box's rarity). Common to Rare boxes sell for shards; Epic and up only come from packs and events.
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep('const fsHasMats = (f, mats) =>', '''const FS_SRC = { alloy: ["m", "Metal fields"], circuit: ["x", "Pirates"], crystal: ["c", "Crystal fields"], bio: ["w", "Monsters"], cube: ["q", "Cubes"], void: ["w", "Monsters"] }; /* v338: where to go for more */
const FS_CONV = 3, fsConvCost = t => ({ m: 500 * Math.pow(4, t - 1), c: 300 * Math.pow(4, t - 1), g: 0 });
const MB_N = [0, 5, 5, 3, 2, 1, 1]; /* units per Material Selection Box by rarity */
for (let tt = 1; tt <= 6; tt++) SHOP["mb" + tt] = { cat: "forge", col: FS_TIER[tt][1], n: `${FS_TIER[tt][0]} Material Box`, ic: "◈", mbT: tt, cost: [0, 4, 18, 55][tt] || null, stack: true, /* priced per Common-equivalent: 5 Common = 1 Uncommon */
  d: () => `Pick any of the six flagship materials: ${MB_N[tt]} × ${FS_TIER[tt][0]}.${tt >= 4 ? " From packs and events." : ""}`, use: () => { openSheet({ type: "matbox", k: "mb" + tt }); return null; } }; /* v338 */ /* defined here, after FS_TIER: SHOP is built long before it */
const fsHasMats = (f, mats) =>''')
# materials tab: converter on top, a Find button per kind
rep('''    body = fsAutoCombHTML() + `<p class="note">Combine five of a tier into one of the next.''', '''    const cv = sheet.cv || { a: "alloy", b: "void", t: 1 }, cvk = fsMatKey(cv.a, cv.t), cvOk = cv.a !== cv.b && (f.mats[cvk] || 0) >= FS_CONV && can(fsConvCost(cv.t));
    const conv = `<div class="mcard fsconv"><h3>Converter</h3><p class="note">${FS_CONV} of one material make 1 of another at the same rarity. Use a surplus to fill a gap.</p>
      <div class="segc fsf">${keys.map(m => `<button class="${cv.a === m ? "on" : ""}" data-act="fsCv" data-k="a" data-v="${m}" aria-label="From ${FS_MATS[m][0]}"><i class="fsmi fsmat-${m}"></i></button>`).join("")}</div><p class="note" style="text-align:center;margin:2px 0">↓ into ↓</p>
      <div class="segc fsf">${keys.map(m => `<button class="${cv.b === m ? "on" : ""}" data-act="fsCv" data-k="b" data-v="${m}" aria-label="Into ${FS_MATS[m][0]}"><i class="fsmi fsmat-${m}"></i></button>`).join("")}</div>
      <div class="segc fsf">${[1, 2, 3, 4, 5, 6].map(k => `<button class="${cv.t === k ? "on" : ""}" style="color:${FS_TIER[k][1]}" data-act="fsCv" data-k="t" data-v="${k}">${FS_TIER[k][0]}</button>`).join("")}</div>
      <p class="note">${fsMatChip(cvk, FS_CONV, f.mats[cvk] || 0)} → ${fsMatChip(fsMatKey(cv.b, cv.t), 1)} · ${costHTML(fsConvCost(cv.t))}</p>
      <button class="btn wide" data-act="fsConvert" ${cvOk ? "" : "disabled"}>${cv.a === cv.b ? "Pick two different materials" : (f.mats[cvk] || 0) < FS_CONV ? `Needs ${FS_CONV} ${FS_TIER[cv.t][0]} ${FS_MATS[cv.a][0]}` : !can(fsConvCost(cv.t)) ? "Not enough resources" : "Convert"}</button></div>`;
    body = conv + fsAutoCombHTML() + `<p class="note">Combine five of a tier into one of the next.''')
rep('''keys.map(m => `<div class="fstree"><h3><i class="fsmi lg fsmat-${m}"></i>${FS_MATS[m][0]}</h3><small class="note">${FS_MATS[m][2]}</small>''',
    '''keys.map(m => `<div class="fstree"><h3><i class="fsmi lg fsmat-${m}"></i>${FS_MATS[m][0]}<button class="btn ghost sm" style="margin-left:auto" data-act="fsFind" data-r="${FS_SRC[m][0]}">Find ${FS_SRC[m][1]} ›</button></h3><small class="note">${FS_MATS[m][2]}</small>''')
# forge: "Get more" for each material you're short of
rep('''        <p class="note">Needs ${Object.entries(rc.mats).map(([k, n]) => fsMatChip(k, n, f.mats[k] || 0)).join(" ")}</p>''',
    '''        <p class="note">Needs ${Object.entries(rc.mats).map(([k, n]) => fsMatChip(k, n, f.mats[k] || 0)).join(" ")}</p>${okM ? "" : `<div class="fsget">${[...new Set(Object.entries(rc.mats).filter(([k, n]) => (f.mats[k] || 0) < n).map(([k]) => k.slice(0, -1)))].map(m => `<button class="btn ghost sm" data-act="fsFind" data-r="${FS_SRC[m][0]}">Get ${FS_MATS[m][0]}: ${FS_SRC[m][1]} ›</button>`).join("")}<button class="btn ghost sm" data-act="fsTab" data-v="mats">Combine or convert ›</button></div>`}''')
# actions
rep('''  fsTab: d => {''', '''  fsFind: d => { closeSheet(); ACT.find({ r: d.r }); }, /* v338 */
  fsCv: d => { sheet.cv = Object.assign({ a: "alloy", b: "void", t: 1 }, sheet.cv || {}, { [d.k]: d.k === "t" ? +d.v : d.v }); renderSheet(); },
  fsConvert: () => { const f = fsOf(), cv = sheet.cv || { a: "alloy", b: "void", t: 1 }, k = fsMatKey(cv.a, cv.t); if (cv.a === cv.b || (f.mats[k] || 0) < FS_CONV) return; if (!pay(fsConvCost(cv.t))) return toast("Not enough resources.", "warn");
    f.mats[k] -= FS_CONV; if (f.mats[k] <= 0) delete f.mats[k]; const k2 = fsMatKey(cv.b, cv.t); f.mats[k2] = (f.mats[k2] || 0) + 1; fsBump(); toast(`Converted ${FS_CONV} ${FS_TIER[cv.t][0]} ${FS_MATS[cv.a][0]} into 1 ${FS_MATS[cv.b][0]}.`, "win"); renderSheet(); },
  matboxPick: d => { if (!sheet || sheet.type !== "matbox") return; const k = sheet.k, s = SHOP[k], tt = s && s.mbT; if (!tt || !((S.items || {})[k] > 0) || !FS_MATS[d.v]) return; S.items[k]--; dirty(); closeSheet(); fsDrop([[d.v, tt, MB_N[tt]]], s.n, { nocap: 1 }); },
  fsTab: d => {''')
# Material Selection Boxes in the shop

rep('''const SHOP_CATS = [["vip", "♛ VIP"], ["boost", "Boosters"], ["accel", "Accelerators"], ["res", "Resources"],''', '''const SHOP_CATS = [["vip", "♛ VIP"], ["boost", "Boosters"], ["accel", "Accelerators"], ["res", "Resources"], ["forge", "Forge"],''')
rep('''<button class="btn amber sm" data-act="buy" data-k="${k}" ${(S.shards || 0) >= s.cost ? "" : "disabled"}>◆${s.cost}</button></div></div>`;''',
    '''${s.cost ? `<button class="btn amber sm" data-act="buy" data-k="${k}" ${(S.shards || 0) >= s.cost ? "" : "disabled"}>◆${s.cost}</button>` : `<span class="note">Packs & events</span>`}</div></div>`;''')
rep('''  buy: d => act(() => { const s = SHOP[d.k]; if (!s) return;''', '''  buy: d => act(() => { const s = SHOP[d.k]; if (!s || !s.cost) return;''')
# the box chooser sheet
rep('pyramid: shPyramid,', 'pyramid: shPyramid, matbox: () => { const s = SHOP[sheet.k]; if (!s) return ""; const f = fsOf(), tt = s.mbT; return `<div class="hd"><div><div class="chapter" style="color:${FS_TIER[tt][1]}">Material Selection Box</div><h2>${esc(s.n)}</h2><p class="note">Pick one: you get ${MB_N[tt]} × ${FS_TIER[tt][0]} of it.</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div><div class="fsmb">${Object.keys(FS_MATS).map(m => `<button class="btn" data-act="matboxPick" data-v="${m}" style="--tc:${FS_TIER[tt][1]}"><i class="fsmi lg fsmat-${m}"></i><b>${FS_MATS[m][0]}</b><small>you have ${fmt(f.mats[fsMatKey(m, tt)] || 0)}</small></button>`).join("")}</div>`; },')
i = t.index('.cneed{'); t = t[:i] + '.fsget{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 8px}.fsconv .fsf button .fsmi{width:24px;height:24px;margin:0}.fsmb{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}.fsmb .btn{display:flex;flex-direction:column;align-items:center;gap:4px;padding:10px;border-color:var(--tc)}.fsmb .btn small{opacity:.7}\n' + t[i:]
open(p, 'w', encoding='utf-8').write(t); print('ok')
