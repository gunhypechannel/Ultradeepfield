# v646 Xeno Sanctuary (owner's friend: "an animal outpost for the base where we can collect rare species, egg incubating and
# cross breeding to make other species"; owner: "Build it all!"). A homeworld building of green bio-domes. Monster hunts can drop
# an egg of that species; eggs hatch in incubators (more with Sanctuary level); hatched creatures live in the habitat and each
# strengthens its element (the same stats the runes raise: fire attack, water shields, earth armour, air speed, spirit output).
# Two creatures can be bred: the egg is usually one parent's species, sometimes Prismatic (x1.5), and the right pair of elements
# can produce one of three breed-only legendaries (the retired Crystal Tortoise, Gravity Spider and Star Leviathan).
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)

# the building
i = s.index('  flagDock:    { n: "Flagship Dock", cat: "fac",'); j = s.index('\n', i) + 1
s = s[:j] + '  sanct:       { n: "Xeno Sanctuary", cat: "fac", c: { m: 12000, c: 9000, g: 3000 }, f: 1.75, req: { cmd: 5, lab: 3 }, d: "Bio-domes where eggs from monster hunts hatch and rare creatures live. Every creature strengthens its element, and pairs can be bred into new species." },\n' + s[j:]
rep('  lunarBase: [-10.5, 16.7], nanite: [0, 16.7], jumpGate: [10.5, 16.7] });', '  lunarBase: [-10.5, 16.7], nanite: [0, 16.7], jumpGate: [10.5, 16.7], sanct: [19, 15.8] }); /* v646 the Sanctuary takes the free corner opposite the Repair Yard */')
rep('for (const k of ["armageddon", "sovereign", "harbinger"]) ART[k] = `art/${k}.webp?v=592`;', 'for (const k of ["armageddon", "sovereign", "harbinger"]) ART[k] = `art/${k}.webp?v=592`;\nART.sanct = ART.sanct || "art/lunarBase.webp"; /* v646 until the Sanctuary has its own painting */')
# its 3D model on the base: green glass bio-domes joined by tubes, glowing eggs inside, a tall central dome from level 3
rep('    case "lunarBase": { // geodesic domes', '''    case "sanct": { /* v646 Xeno Sanctuary: green glass bio-domes, glowing eggs inside, joined by tubes */
      const gl = new TH.MeshStandardMaterial({ color: 0x7dffb8, emissive: 0x1d7a50, emissiveIntensity: .7, roughness: .12, metalness: .1, transparent: true, opacity: .55 });
      const egg = new TH.MeshStandardMaterial({ color: 0xffe9a8, emissive: 0xffb84a, emissiveIntensity: 1.4, roughness: .4 });
      const dome = (x, z, R) => { cyl(R * 1.02, R * 1.05, R * .22, C.dark, x, 0, z, 16); const d = add(new TH.Mesh(new TH.SphereGeometry(R, 14, 7, 0, TAU, 0, Math.PI / 2), gl)); d.position.set(x, R * .22, z);
        cyl(R * 1.06, R * 1.06, .05, C.steel, x, R * .2, z, 16); for (let i = 0; i < 3; i++) { const a = i * 2.1 + x, eg = add(new TH.Mesh(new TH.SphereGeometry(R * .14, 8, 6), egg)); eg.scale.y = 1.3; eg.position.set(x + Math.cos(a) * R * .42, R * .4, z + Math.sin(a) * R * .42); } };
      const spots = [[0, 0, .95 + (e >= 3 ? .35 : 0)], [-1.3, .6, .55], [1.2, .7, .6], [-1, -1.2, .5], [1.25, -1, .55]], n = Math.min(5, 1 + e);
      for (let i = 0; i < n; i++) { dome(...spots[i]); if (i) { const [x, z] = spots[i]; const t = add(new TH.Mesh(new TH.CylinderGeometry(.1, .1, Math.hypot(x, z) - .6, 8), C.steel)); t.position.set(x / 2, .16, z / 2); t.rotation.set(Math.PI / 2, 0, 0); t.rotation.order = "YXZ"; t.rotation.y = Math.atan2(x, z); } }
      break; }
    case "lunarBase": { // geodesic domes''')
# detail sheet: a Sanctuary tab, its effect line and the advisor's note
rep(': k === "flagDock" ? ["Overview", "Flagship"] : null) : null, tab = sheet.tab || 0;', ': k === "flagDock" ? ["Overview", "Flagship"] : k === "sanct" ? ["Overview", "Sanctuary"] : null) : null, tab = sheet.tab || 0;')
rep(': k === "repairYard" ? repairCard() : k === "flagDock" ? fsDockCard() :', ': k === "repairYard" ? repairCard() : k === "flagDock" ? fsDockCard() : k === "sanct" ? sanctCard() :')
rep('    case "flagDock": return `Forges up to', '    case "sanct": return `Incubators ${xsIncN(L)} → <em>${xsIncN(L + 1)}</em> · habitat ${xsCap(L)} → <em>${xsCap(L + 1)}</em> creatures`;\n    case "flagDock": return `Forges up to')
rep('  flagDock: "The Flagship Dock is where', '  sanct: "The Xeno Sanctuary. Eggs from our monster hunts hatch here, and every creature we raise makes its element stronger. Breed the right pair and something rare might hatch.",\n  flagDock: "The Flagship Dock is where')
# creature bonuses join the element stats
rep('function elExtra(e) { let v = ringM(e) * MAST_PER;', 'function elExtra(e) { let v = ringM(e) * MAST_PER + xsPct(e); /* v646 Sanctuary creatures */')
# a monster hunt won can leave an egg
rep('    fsLootPB(x); // v298', '    fsLootPB(x); // v298\n    if (x.mon) try { xsEggDrop(x, rep); } catch (e) {} /* v646 */')

rep('function elExtra(e) {', r'''/* ---------- v646 Xeno Sanctuary ---------- */
const XS = { swhale: ["water", 0], ssquid: ["water", 0], swasp: ["air", 0], reat: ["earth", 0], vmanta: ["spirit", 1], smoth: ["fire", 1], cram: ["air", 1], kegg: ["water", 1],
  gwhale: ["spirit", 2], cserp: ["fire", 2], sent: ["earth", 2], ctort: ["earth", 3, 1], gspider: ["air", 3, 1], slevi: ["fire", 3, 1] }; // [element, rarity, breed-only]
const XR = [["Common", "#9fb6c4", 4, .5], ["Rare", "#5ab8ff", 8, 1], ["Epic", "#c07aff", 16, 1.5], ["Legendary", "#ffc94a", 24, 2.5]]; // name, colour, hatch hours, % per creature
const XS_RCP = [["earth", "water", "ctort"], ["air", "spirit", "gspider"], ["fire", "water", "slevi"]]; // element pair → breed-only legendary
const XS_CAP_PCT = 15, XS_EGGS = 12, XS_BR_CD = 8 * 3600e3, XS_DROP = .15;
const xsIncN = L => L ? Math.min(4, 1 + Math.floor(L / 3)) : 0, xsCap = L => L ? Math.min(14, 2 + L) : 0;
const xsOf = () => { const X = (S.xs = S.xs || {}); X.eggs = X.eggs || []; X.inc = X.inc || []; X.hab = X.hab || []; X.seen = X.seen || {}; return X; };
const xsName = k => (MON[k] && MON[k].n) || k, xsCol = k => (MON[k] && MON[k].col) || "#7dffb8", xsImg = k => `art/mon/${monImg(k)}.webp?v=1`;
const xsLvl = () => (S && S.b && S.b.sanct) || 0;
function xsPct(e) { if (!S || !S.xs || !xsLvl()) return 0; let v = 0; for (const c of S.xs.hab || []) { const D = XS[c.sp]; if (D && D[0] === e) v += XR[D[1]][3] * (c.pr ? 1.5 : 1); } return Math.min(XS_CAP_PCT, Math.round(v * 10) / 10); }
function xsEggDrop(x, rep) { const sp = x.mon; if (!XS[sp] || XS[sp][2]) return; const X = xsOf(); if (X.eggs.length >= XS_EGGS) return;
  if (Math.random() >= XS_DROP * (isElite(x) ? 2 : 1)) return; const pr = Math.random() < .05; X.eggs.push({ sp, pr: pr ? 1 : 0 }); X.seen[sp] = X.seen[sp] || 1; if (rep) rep.egg = sp; dirty();
  setTimeout(() => { try { toast(`${pr ? "A Prismatic " : "An "}${xsName(sp)} egg was left in the wreckage!${xsLvl() ? " It's waiting at the Xeno Sanctuary." : " Build a Xeno Sanctuary to hatch it."}`, "win");
    advHolo(xsLvl() ? "An egg, Commander. Still warm. I've sent it to the Sanctuary." : "An egg, Commander. Still warm. We'll need a Xeno Sanctuary to hatch it.", true); } catch (e) {} }, 2200); }
function xsEggHTML(sp, pr, big) { const c = xsCol(sp); return `<i class="xsegg${pr ? " pr" : ""}${big ? " big" : ""}" style="--c:${c}"></i>`; }
function sanctCard() { const X = xsOf(), L = xsLvl(), T = now(), slots = xsIncN(L), cap = xsCap(L);
  if (!L) return `<div class="dp"><p class="note">Build the Xeno Sanctuary to hatch eggs from monster hunts.${X.eggs.length ? ` You have <b>${X.eggs.length}</b> egg${X.eggs.length > 1 ? "s" : ""} waiting.` : " Every monster hunt you win has a chance to leave an egg."}</p></div>`;
  const sel = G.xsSel || [], R = e => `<span class="xsel" style="--c:${ELEM[e].col}">${ELEM[e].n}</span>`;
  const inc = [...Array(slots)].map((_, i) => { const it = X.inc[i]; if (!it) return `<div class="xsinc empty"><i class="xsegg ghost"></i><small>Empty incubator</small>${X.eggs.length ? `<small class="note">Pick an egg below</small>` : ""}</div>`;
    const done = it.e <= T, left = Math.max(0, it.e - T), hn = Math.max(1, Math.ceil(left / 3600e3 * 2)), k = "xsh|" + i;
    return `<div class="xsinc${done ? " ready" : ""}">${xsEggHTML(it.sp, it.pr, 1)}<b>${it.pr ? "✦ " : ""}${esc(xsName(it.sp))}</b>${done ? `<button class="btn amber sm" data-act="xsHatch" data-i="${i}">Hatch!</button>`
      : `<div class="xsbar"><i style="width:${Math.min(100, (T - it.s) / (it.e - it.s) * 100).toFixed(1)}%"></i></div><small><span data-end="${it.e}">${ftime(left)}</span> left</small><button class="btn sm${buyArmed(k) ? " pxarm" : ""}" data-act="xsRush" data-i="${i}" ${(S.shards || 0) >= hn ? "" : "disabled"}>${buyArmed(k) ? "Confirm" : "Hatch now"} ◆${hn}</button>`}</div>`; }).join("");
  const eg = {}; for (const x of X.eggs) { const key = x.sp + (x.pr ? "*" : ""); eg[key] = (eg[key] || 0) + 1; }
  const free = X.inc.filter(Boolean).length < slots;
  const eggs = Object.keys(eg).length ? Object.entries(eg).map(([key, n]) => { const sp = key.replace("*", ""), pr = key.endsWith("*"), r = XR[XS[sp][1]];
    return `<div class="xsegc">${xsEggHTML(sp, pr)}<div><b>${pr ? "✦ Prismatic " : ""}${esc(xsName(sp))} ×${n}</b><small style="color:${r[1]}">${r[0]} · hatches in ${r[2]} h</small></div><button class="btn sm" data-act="xsInc" data-sp="${sp}" data-pr="${pr ? 1 : 0}" ${free && X.hab.length < cap ? "" : "disabled"}>Incubate</button></div>`; }).join("")
    : `<p class="note">No eggs yet. Win monster hunts: each one has a chance to leave an egg.</p>`;
  const hab = X.hab.length ? X.hab.map(c => { const D = XS[c.sp], r = XR[D[1]], on = sel.includes(c.id), pct = Math.round(r[3] * (c.pr ? 1.5 : 1) * 10) / 10, rk = "xsr|" + c.id;
    return `<div class="xscr${on ? " on" : ""}${c.pr ? " pr" : ""}" style="--c:${xsCol(c.sp)};--r:${r[1]}"><div class="xsart"><img src="${xsImg(c.sp)}" alt="" loading="lazy"></div><div class="xsci"><b>${c.pr ? "✦ " : ""}${esc(xsName(c.sp))}</b><small style="color:${r[1]}">${r[0]}${c.pr ? " · Prismatic" : ""}</small>${R(D[0])}<em>+${pct}% ${esc(ELEM[D[0]].stat.toLowerCase())}</em></div>
      <div class="xscb"><button class="btn sm${on ? " amber" : ""}" data-act="xsSel" data-id="${c.id}">${on ? "✓ Breeding" : "Breed"}</button><button class="btn ghost sm${buyArmed(rk) ? " pxarm" : ""}" data-act="xsRel" data-id="${c.id}">${buyArmed(rk) ? "Confirm" : "Release"}</button></div></div>`; }).join("")
    : `<p class="note">The habitat is empty. Hatched creatures live here.</p>`;
  const a = X.hab.find(c => c.id === sel[0]), b = X.hab.find(c => c.id === sel[1]), bc = xsBrCost(), cd = Math.max(0, (X.brT || 0) - T);
  const rc = a && b ? XS_RCP.find(([x, y]) => (XS[a.sp][0] === x && XS[b.sp][0] === y) || (XS[a.sp][0] === y && XS[b.sp][0] === x)) : null;
  const breed = `<div class="xsbr"><div class="xspair">${a ? `<img src="${xsImg(a.sp)}" alt="">` : "<i>?</i>"}<span>×</span>${b ? `<img src="${xsImg(b.sp)}" alt="">` : "<i>?</i>"}</div>
    <p class="note">${a && b ? `${esc(xsName(a.sp))} × ${esc(xsName(b.sp))}: the egg is usually one parent's kind, sometimes Prismatic.${rc ? ` <b style="color:#ffc94a">This pairing of ${ELEM[rc[0]].n} and ${ELEM[rc[1]].n} can hatch something legendary.</b>` : ""}` : "Pick two creatures with Breed. Some pairings of elements can hatch a species found nowhere in the wild."}</p>
    ${cd ? `<p class="note">The breeding chamber is resting: <b data-end="${X.brT}">${ftime(cd)}</b>.</p>` : `<button class="btn wide amber" data-act="xsBreed" ${a && b && can(bc) && X.eggs.length < XS_EGGS ? "" : "disabled"}>Breed · ${costHTML(bc)}</button>`}</div>`;
  const book = Object.keys(XS).map(k => { const seen = X.seen[k], r = XR[XS[k][1]]; return `<div class="xsbk${seen ? "" : " un"}" title="${seen ? esc(xsName(k)) : "Undiscovered"}"><img src="${xsImg(k)}" alt="" loading="lazy"><small style="color:${seen ? r[1] : "var(--muted)"}">${seen ? esc(xsName(k)) : XS[k][2] ? "Bred only" : "???"}</small></div>`; }).join("");
  const bon = Object.keys(ELEM).map(e => [e, xsPct(e)]).filter(x => x[1] > 0).map(([e, v]) => `<span class="xsel" style="--c:${ELEM[e].col}">${ELEM[e].n} +${v}%</span>`).join("") || '<span class="note">None yet</span>';
  return `<div class="dp xsc"><div class="xsh"><b>Incubators</b><small>${X.inc.filter(Boolean).length}/${slots}</small></div><div class="xsincs">${inc}</div>
    <div class="xsh"><b>Eggs</b><small>${X.eggs.length}/${XS_EGGS}</small></div><div class="xsegs">${eggs}</div>
    <div class="xsh"><b>Habitat</b><small>${X.hab.length}/${cap}</small></div><div class="xshab">${hab}</div>
    <div class="xsh"><b>Breeding chamber</b></div>${breed}
    <div class="xsh"><b>Creature bonuses</b><small>up to +${XS_CAP_PCT}% per element</small></div><div class="xsbon">${bon}</div>
    <div class="xsh"><b>Collection</b><small>${Object.keys(XS).filter(k => X.seen[k]).length}/${Object.keys(XS).length}</small></div><div class="xsbook">${book}</div></div>`; }
const xsBrCost = () => { const L = Math.max(1, xsLvl()); return { m: 30000 * L, c: 30000 * L, g: 10000 * L }; };
const xsRe = () => { if (sheet) renderSheet(); else render(true); };
''' + 'function elExtra(e) {')

# actions
rep('  hullK: d => { G.hullK = d.k; render(true); },', r'''  hullK: d => { G.hullK = d.k; render(true); },
  xsInc: d => act(() => { const X = xsOf(), L = xsLvl(), slots = xsIncN(L), i = [...Array(slots).keys()].find(j => !X.inc[j]); if (i == null) return toast("Every incubator is busy.", "warn");
    if (X.hab.length + X.inc.filter(Boolean).length >= xsCap(L)) return toast("The habitat is full. Raise the Sanctuary's level or release a creature.", "warn");
    const pr = d.pr === "1" ? 1 : 0, ei = X.eggs.findIndex(x => x.sp === d.sp && (x.pr ? 1 : 0) === pr); if (ei < 0) return; X.eggs.splice(ei, 1); const T = now(), h = XR[XS[d.sp][1]][2];
    X.inc[i] = { sp: d.sp, pr, s: T, e: T + h * 3600e3 }; toast(`${xsName(d.sp)} egg in the incubator. It hatches in ${h} hours.`); }),
  xsRush: d => act(() => { const X = xsOf(), i = +d.i, it = X.inc[i]; if (!it) return; const left = it.e - now(); if (left <= 0) return; const n = Math.max(1, Math.ceil(left / 3600e3 * 2));
    if ((S.shards || 0) < n) return toast(`Hatching now costs ◆${n}.`, "warn"); if (!armBuy("xsh|" + i, n)) return; S.shards -= n; it.e = now(); }),
  xsHatch: d => act(() => { const X = xsOf(), i = +d.i, it = X.inc[i]; if (!it || it.e > now()) return; X.inc[i] = null; const c = { id: "c" + (S.seq++), sp: it.sp, pr: it.pr || 0, at: now() };
    X.hab.push(c); X.seen[it.sp] = 1; const r = XR[XS[it.sp][1]]; toast(`${it.pr ? "✦ Prismatic " : ""}${xsName(it.sp)} hatched! ${r[0]} · +${Math.round(r[3] * (it.pr ? 1.5 : 1) * 10) / 10}% ${ELEM[XS[it.sp][0]].stat.toLowerCase()}.`, "win");
    try { SFX.research(); if (XS[it.sp][1] >= 2 || it.pr) advHolo(XS[it.sp][2] ? "Commander... that species hasn't been seen alive in a thousand years. And it hatched in our dome." : "Look at it, Commander. Something that rare, raised by us.", true); } catch (e) {} }),
  xsSel: d => { const s0 = G.xsSel || []; G.xsSel = s0.includes(d.id) ? s0.filter(x => x !== d.id) : s0.concat(d.id).slice(-2); xsRe(); },
  xsRel: d => act(() => { const X = xsOf(), c = X.hab.find(x => x.id === d.id); if (!c) return; const n = [1, 2, 4, 8][XS[c.sp][1]] * (c.pr ? 2 : 1); const rk = "xsr|" + c.id; if (!buyArmed(rk)) { G.buyArm = { k: rk, t: Date.now() }; toast(`Tap Release again to let the ${xsName(c.sp)} go (+◆${n}).`); return; } G.buyArm = null;
    X.hab = X.hab.filter(x => x.id !== c.id); G.xsSel = (G.xsSel || []).filter(x => x !== c.id); S.shards = (S.shards || 0) + n; toast(`${xsName(c.sp)} released to the wild. The ranger guild sent ◆${n} in thanks.`); }),
  xsBreed: d => act(() => { const X = xsOf(), [ia, ib] = G.xsSel || [], a = X.hab.find(c => c.id === ia), b = X.hab.find(c => c.id === ib), T = now(); if (!a || !b || a === b || (X.brT || 0) > T) return;
    if (X.eggs.length >= XS_EGGS) return toast("The egg store is full. Incubate some first.", "warn"); if (!pay(xsBrCost())) return toast("Not enough resources.", "warn");
    const rc = XS_RCP.find(([x, y]) => (XS[a.sp][0] === x && XS[b.sp][0] === y) || (XS[a.sp][0] === y && XS[b.sp][0] === x)), leg = rc && Math.random() < .2;
    const sp = leg ? rc[2] : Math.random() < .5 ? a.sp : b.sp, pr = !leg && Math.random() < ((a.pr || b.pr) ? .35 : .12) ? 1 : 0; X.eggs.push({ sp, pr }); X.brT = T + XS_BR_CD; X.seen[sp] = X.seen[sp] || 1; G.xsSel = [];
    toast(leg ? `Something new is in the egg chamber, Commander: a ${xsName(sp)} egg!` : `A ${pr ? "Prismatic " : ""}${xsName(sp)} egg from the breeding chamber.`, "win"); if (leg) try { advHolo("I've never seen an egg like it. The records say this species died out before the convoy wars.", true); } catch (e) {} }),''')

rep('.hfp{flex-shrink:0;', r'''.xsc{display:flex;flex-direction:column;gap:10px}.xsc>*{flex-shrink:0}.xsh{display:flex;align-items:baseline;justify-content:space-between;margin-top:6px;border-bottom:1px solid rgba(125,255,184,.18);padding-bottom:4px}.xsh b{font:700 15px var(--f-display);color:#7dffb8;letter-spacing:.04em}.xsh small{color:var(--muted);font-size:12px}
.xsincs{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px}.xsinc{display:flex;flex-direction:column;align-items:center;gap:5px;padding:10px 8px;border-radius:14px;background:radial-gradient(80% 70% at 50% 30%,rgba(125,255,184,.14),transparent 70%),rgba(6,14,16,.7);border:1px solid rgba(125,255,184,.3);text-align:center}.xsinc b{font-size:13px}.xsinc small{font-size:11.5px;color:var(--muted)}.xsinc.empty{opacity:.75;border-style:dashed}.xsinc.ready{border-color:#ffd25a;box-shadow:0 0 16px rgba(255,210,90,.35)}
.xsbar{width:100%;height:6px;border-radius:4px;background:rgba(255,255,255,.08);overflow:hidden}.xsbar i{display:block;height:100%;background:linear-gradient(90deg,#3ce88e,#b8ffdc)}
.xsegg{display:inline-block;width:26px;height:33px;border-radius:50% 50% 46% 46%/58% 58% 42% 42%;background:radial-gradient(40% 30% at 35% 30%,rgba(255,255,255,.85),transparent 70%),radial-gradient(circle at 60% 70%,rgba(0,0,0,.35),transparent 60%),radial-gradient(18% 14% at 65% 40%,rgba(255,255,255,.35),transparent),var(--c);box-shadow:0 0 14px color-mix(in srgb,var(--c) 60%,transparent);flex:none}.xsegg.big{width:44px;height:56px}.xsegg.ghost{--c:#2a3a40;box-shadow:none;opacity:.5}.xsegg.pr{background:radial-gradient(40% 30% at 35% 30%,rgba(255,255,255,.9),transparent 70%),conic-gradient(from 0deg,#ff7ad9,#7af4ff,#9dff7a,#ffd36b,#ff7ad9);animation:xspr 4s linear infinite}.xsinc.ready .xsegg{animation:xswob 1.2s ease-in-out infinite}
@keyframes xswob{0%,100%{transform:rotate(0)}25%{transform:rotate(-8deg)}75%{transform:rotate(8deg)}}@keyframes xspr{to{filter:hue-rotate(360deg)}}
.xsegs{display:flex;flex-direction:column;gap:6px}.xsegc{display:flex;align-items:center;gap:10px;padding:6px 10px;border-radius:12px;background:rgba(255,255,255,.035)}.xsegc>div{flex:1;min-width:0;display:flex;flex-direction:column}.xsegc b{font-size:13px}.xsegc small{font-size:11.5px}
.xshab{display:flex;flex-direction:column;gap:8px}.xscr{display:flex;align-items:center;gap:10px;padding:8px;border-radius:14px;border:1px solid color-mix(in srgb,var(--r) 45%,transparent);background:linear-gradient(90deg,color-mix(in srgb,var(--c) 14%,transparent),rgba(6,12,18,.6))}.xscr.on{border-color:#ffd25a;box-shadow:0 0 12px rgba(255,210,90,.35)}
.xsart{width:72px;height:72px;flex:none;border-radius:12px;overflow:hidden;background:#040a10}.xsart img{width:100%;height:100%;object-fit:cover}.xscr.pr .xsart img{animation:xspr 5s linear infinite}
.xsci{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}.xsci b{font-size:14px}.xsci small{font-size:11.5px}.xsci em{font-style:normal;font-size:12px;color:#8affb4}.xscb{display:flex;flex-direction:column;gap:4px}
.xsel{display:inline-block;width:max-content;font-size:11px;padding:1px 7px;border-radius:8px;color:var(--c);border:1px solid color-mix(in srgb,var(--c) 55%,transparent)}
.xsbr{display:flex;flex-direction:column;gap:8px;align-items:stretch}.xspair{display:flex;align-items:center;justify-content:center;gap:12px}.xspair img,.xspair i{width:68px;height:68px;border-radius:14px;object-fit:cover;background:#040a10;border:1px solid rgba(125,255,184,.3);display:grid;place-items:center;font-style:normal;color:var(--muted);font-size:24px}.xspair span{font-size:22px;color:#ffd25a}
.xsbon{display:flex;flex-wrap:wrap;gap:6px}.xsbook{display:grid;grid-template-columns:repeat(auto-fill,minmax(70px,1fr));gap:6px}.xsbk{display:flex;flex-direction:column;align-items:center;gap:3px;text-align:center}.xsbk img{width:62px;height:62px;border-radius:12px;object-fit:cover;background:#040a10}.xsbk.un img{filter:brightness(0) drop-shadow(0 0 4px rgba(125,255,184,.4));opacity:.7}.xsbk small{font-size:10.5px;line-height:1.2}
@media (prefers-reduced-motion:reduce){.xsegg.pr,.xsinc.ready .xsegg,.xscr.pr .xsart img{animation:none}}
.hfp{flex-shrink:0;''')
rep('const bicon = k =>', 'try { BI.sanct = BI.sanct || \'<path d="M6 30a14 14 0 0 1 28 0z"/><path d="M3 30h34"/><ellipse cx="20" cy="23" rx="3.2" ry="4.2"/><path d="M13 30a7 7 0 0 1 4-10"/>\'; } catch (e) {}\nconst bicon = k =>')
rep('const GAME_V = 645', 'const GAME_V = 646')
open(p, 'w', encoding='utf-8').write(s)
