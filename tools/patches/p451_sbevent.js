/* v451 THE ULTIMATE SUPER BOSS EVENTS. Two monthly hunts, 36 hours each, 11:00 Phoenix: Vaelthar, "Judgment of the Celestial Wheel",
   on the 25th (first 2026-11-25), and Aexion, "Warform Awakening", on the 5th (first 2026-12-05). With Cube Devastation on the 15th there
   is a great event about every ten days, and they never overlap. Built on the Omega Cube's engine: a shared record per boss
   (event/sb_vae, event/sb_aex: {cyc, hp, dmg, log [[at, left, target]], wp, dead, last}) written under the doc lock, a fight that rises to
   meet any fleet (8-20% of the hull per attack), a bounty per section, a one-time claim when it falls.
   Vaelthar: 100 sections; phases Celestial Guardian, Wheel Awakening (75%), Divine Judgment (50%), Final Eclipse (25%). Every 6 h the
   wheel charges Divine Annihilation (seen live on the map). From Wheel Awakening on, fleets can strike the wheel's stabilizers: break 4 of
   the 6 in a cycle and the charge is interrupted (its core is exposed for an hour: +50% sections); if not, the beam fires (its firepower
   ×1.6 for an hour). Only fleets that choose to attack in that hour are touched: nothing is destroyed unavoidably.
   Aexion: ship form until 60%, when it transforms (live on the map, once, from the record), armour open for 20 min (+25% sections);
   weak points: the stern engines in ship form (each -3% firepower), the shield emitters in Warform (each +6% sections), and below 20%
   Reactor Overdrive: its reactor exposed (double sections, but it hits 50% harder). */
const SB_H = 3600e3, SB_WIN = 36 * SB_H, SB_ARR = 5 * 60e3;
const SBW = {
  vae: { n: "Vaelthar", t: "The Celestial Ruin", ev: "Judgment of the Celestial Wheel", day: 25, first: Date.UTC(2026, 10, 25, 18), m3: "vaelthar", u: "wbVae", HP: 1500000, ATK: 650000, col: "#c890ff", art: "art/boss/vaelthar.webp", ic: "◈",
    mv: ["claw", "wing", "judge", "seal"], diff: "Ultimate", ph: [[75, "Celestial Guardian"], [50, "Wheel Awakening"], [25, "Divine Judgment"], [0, "Final Eclipse"]],
    abil: [["Astral Claw", "Energy-wreathed talons rake the nearest fleets."], ["Divine Wingstorm", "Its wings unleash waves of violet cosmic force."], ["Celestial Judgment", "Rune circles bloom on the wheel and fire concentrated bolts."], ["Golden Seal", "Runic circles bind fleets inside the wheel's reach."],
      ["Divine Annihilation", "Every 6 hours the wheel charges a beam that cuts through formations. Break 4 stabilizers in the cycle to interrupt it."], ["Final Eclipse", "Below 25% the wheel fractures: faster, wilder attacks (+25% firepower)."]],
    mats: ["vwheel", "vscale", "vastral", "vcata"], rare: "vastral" },
  aex: { n: "Aexion", t: "The Warform Sovereign", ev: "Warform Awakening", day: 5, first: Date.UTC(2026, 11, 5, 18), m3: "aexion", u: "wbAex", HP: 1400000, ATK: 600000, col: "#7ac8ff", art: "art/boss/aexion-warform.webp", art0: "art/boss/aexion-ship.webp", ic: "⬢",
    mv: ["broadside", "missiles", "rail"], mv2: ["aegis", "blade", "missiles", "lance"], diff: "Ultimate", ph: [[60, "Dreadnought Assault"], [20, "Sovereign Warform"], [0, "Reactor Overdrive"]],
    abil: [["Titan Broadside", "Heavy plasma volleys from its flank batteries."], ["Missile Saturation", "Guided swarms from its shoulder pods."], ["Railbreaker", "A charged forearm railgun shot at long range."], ["Warform Awakening", "At 60% it transforms into its Warform: its armour is open for 20 minutes (+25% sections)."],
      ["Judgment Blade · Holographic Aegis", "A sweeping energy sword; a reactive hexagonal shield on its arm, powered by its shield emitters."], ["Reactor Overdrive", "Below 20% every weapon fires at once (+30% firepower) and its reactor is exposed."]],
    mats: ["areact", "aalloy", "amatrix", "atitan"], rare: "areact" } };
const SBM = { vwheel: ["Celestial Wheel Fragment", "#e6b84a", "#7a3cc8", "ring"], vscale: ["Divine Scale", "#5a2a8a", "#e0b04a", "scale"], vastral: ["Astral Energy Core", "#f0dcff", "#9a5cff", "orb"], vcata: ["Ancient Rune Catalyst", "#ffd27a", "#a05cff", "rune"],
  areact: ["Warform Reactor Core", "#e8f6ff", "#3aa8ff", "orb"], aalloy: ["Sovereign Alloy", "#c9ced6", "#4a6a9a", "ingot"], amatrix: ["Holographic Matrix", "#9ad8ff", "#2a70ff", "hex"], atitan: ["Titan Weapon Components", "#9aa4b2", "#58b8ff", "gear"] };
for (const k in SBW) { const D = SBW[k], hull = Math.round(D.HP * WB_K / 100); AL[D.u] = { n: D.n + " section", atk: Math.round(D.ATK / 100), sh: Math.round(hull * .05), hull, val: hull * 2 }; }
const SBO = {}; for (const k in SBW) SBO[k] = { id: "sb_" + k, kind: "sboss", lvl: 35, name: SBW[k].n, mv: (T, out) => { const o = out || {}; const p = SBX[k].p; o.x = p[0]; o.y = p[1]; o.z = p[2]; return o; }, r: .01, a0: 0 };
/* the clock: the start of the hunt that contains (or last preceded) T, the next start */
function sbStartOf(k, T) { const D = SBW[k]; if (T < D.first) return null; const d = new Date(T); let s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), D.day, 18); if (s > T) s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth() - 1, D.day, 18); return Math.max(s, D.first); }
function sbNext(k, T) { const D = SBW[k]; if (T < D.first) return D.first; const d = new Date(T); let s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), D.day, 18); if (s <= T) s = Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, D.day, 18); return s; }
G.sb = {}; const SBN = {};
function sbNorm(d, s0) { const o = d && typeof d === "object" && d.cyc === s0 ? d : { cyc: s0 }; o.hp = o.hp == null ? 100 : clamp(Math.round(+o.hp || 0), 0, 100); o.dmg = o.dmg && typeof o.dmg === "object" ? o.dmg : {};
  o.log = Array.isArray(o.log) ? o.log.filter(x => Array.isArray(x) && x.length >= 2).slice(-300) : []; o.wp = o.wp && typeof o.wp === "object" ? o.wp : {}; o.dead = +o.dead || 0; o.last = o.last || null; return o; }
function sbState(k, s0) { const src = G.mode === "online" ? G.sb[k] : ((S && S.ldb) || {})["event/sb_" + k] || null, c = SBN[k]; if (!c || c.cyc !== s0 || c.src !== src) SBN[k] = { cyc: s0, src, st: sbNorm(src ? jcopy(src) : null, s0) }; return SBN[k].st; }
const sbHpAt = (st, T) => { let h = 100; for (const e of st.log) { if (e[0] > T) break; if (!e[2] || e[2] === "core" || e[2] === "reactor") h = e[1]; } return h; };
const sbPhase = (k, hp) => { const P = SBW[k].ph; for (let i = 0; i < P.length; i++) if (hp > P[i][0]) return i; return P.length - 1; };
/* when the window closes: 5 minutes after it falls, or when its 36 hours run out */
const sbEnd = (k, s0) => { const st = sbState(k, s0); return st.dead && st.dead > s0 ? st.dead + 5 * 60e3 : s0 + SB_WIN; };
function sbOn(k, T = now()) { const s0 = sbStartOf(k, T); if (s0 == null) return false; const st = sbState(k, s0); return T >= s0 + SB_ARR && T < sbEnd(k, s0) && st.hp > 0; }
const sbLiveKey = (T = now()) => { for (const k in SBW) { const s0 = sbStartOf(k, T); if (s0 != null && T >= s0 && T < sbEnd(k, s0) + 10 * 60e3) return k; } return null; };
/* Vaelthar's charge cycles (6 h from its arrival): the stabilizers broken in a cycle decide whether the beam fires at its end */
const SB_VC = 6 * SB_H, WPK = { stab: 4, eng: 3, emit: 3 }, wpN = (st, key, kind) => Math.floor((st.wp[key] || 0) / WPK[kind]);
function vaeCycle(s0, T) { const c = Math.floor((T - s0 - SB_ARR) / SB_VC), ce = s0 + SB_ARR + (c + 1) * SB_VC; return { c, ce, cs: ce - SB_VC }; }
function vaeResult(st, s0, c) { const ce = s0 + SB_ARR + (c + 1) * SB_VC; if (sbHpAt(st, ce) > 75) return "dormant"; return wpN(st, "stab" + c, "stab") >= 4 ? "interrupted" : "fired"; }
/* Aexion's transformation: the first time its hull fell to 60% */
const aexXf = st => { for (const e of st.log) if ((!e[2] || e[2] === "core") && e[1] <= 60) return e[0]; return 0; };
/* the modifiers in force for an attack arriving at T against target tgt: sections ×m, its firepower ×fp */
function sbMods(k, st, s0, T, tgt) { let m = 1, fp = 1; const why = []; const hp = st.hp, ph = sbPhase(k, hp);
  if (k === "vae") { const { c } = vaeCycle(s0, T); if (c >= 1) { const prevEnd = s0 + SB_ARR + c * SB_VC; if (T < prevEnd + SB_H) { const r = vaeResult(st, s0, c - 1); if (r === "interrupted") { m *= 1.5; why.push("its core is exposed (+50%)"); } else if (r === "fired") { fp *= 1.6; why.push("Divine Annihilation is still burning (×1.6 firepower)"); } } }
    if (ph === 3) { fp *= 1.25; why.push("Final Eclipse (+25% firepower)"); } }
  else { const xf = aexXf(st); if (!xf) { const e = Math.min(8, wpN(st, "eng", "eng")); if (e) { fp *= 1 - .03 * e; why.push(`${e} engine${e > 1 ? "s" : ""} down (−${e * 3}% firepower)`); } }
    else { if (T < xf + 20 * 60e3) { m *= 1.25; why.push("its armour is open (+25%)"); } const em = Math.min(8, wpN(st, "emit", "emit")); if (em) { m *= 1 + .06 * em; why.push(`${em} shield emitter${em > 1 ? "s" : ""} down (+${em * 6}%)`); } }
    if (ph === 2) { fp *= 1.3; why.push("Reactor Overdrive (+30% firepower)"); if (tgt === "reactor") { m *= 2; fp *= 1.5; why.push("striking the exposed reactor (×2 sections, ×1.5 firepower)"); } } }
  return { m, fp, why }; }
/* the weak points open now, with the units left in each */
function sbTargets(k, st, s0, T) { const L = [["core", `${SBW[k].n}`, null]];
  if (k === "vae") { if (st.hp <= 75) { const { c } = vaeCycle(s0, T), d = Math.min(6, wpN(st, "stab" + c, "stab")); L.push(["stab", "Wheel stabilizers", 6 * WPK.stab - (st.wp["stab" + c] || 0), `${d} of 6 broken this cycle`]); } }
  else { const xf = aexXf(st); if (!xf) L.push(["eng", "Stern engines", 8 * WPK.eng - (st.wp.eng || 0), `${Math.min(8, wpN(st, "eng", "eng"))} of 8 destroyed`]); else L.push(["emit", "Shield emitters", 8 * WPK.emit - (st.wp.emit || 0), `${Math.min(8, wpN(st, "emit", "emit"))} of 8 destroyed`]);
    if (sbPhase(k, st.hp) === 2) L.push(["reactor", "Exposed reactor", null, "double damage, deadlier"]); }
  return L; }
function sbFightRise(mkA, mkD, n0, cap, m) { let { F, x } = wbRiseK(mkA(), mkD()); const k = SBW[mkD.k].u; if (F <= 1) return { res: simulate(mkA(), mkD()), rise: 1 };
  const tgt = Math.min(cap, Math.max(1, Math.round(100 * clamp(.08 + .04 * Math.log10(x), .08, .2) * m))); let lo = 1, hi = 0, best = null;
  for (let i = 0; i < 9; i++) { const A = mkA(), D = mkD(); for (const s of D) { s.atk *= F; s.hull *= F; } const res = simulate(A, D), seg = n0 - clamp(Math.round(((res.dLeft || {})[k]) || 0), 0, n0), err = Math.abs(Math.min(seg, cap) - tgt);
    if (!best || err < best.err) best = { res, F, err }; if (err <= 2) break; if (seg > tgt) lo = F; else hi = F; F = hi ? Math.sqrt(Math.max(lo, 1) * hi) : F * Math.max(1.5, Math.pow(seg / Math.max(1, tgt), 1.6)); if (hi && hi / Math.max(lo, 1) < 1.03) break; }
  return { res: best.res, rise: best.F }; }
function sbMatGive(list, why) { S.sbMat = S.sbMat || {}; const got = []; for (const [k, n] of list) if (n > 0 && SBM[k]) { S.sbMat[k] = (S.sbMat[k] || 0) + n; got.push(`${n} ${SBM[k][0]}`); } return got; }
/* the materials a strike knocks loose: the struck part's own, and a chance of the others */
function sbMatRoll(k, tgt, seg) { const M = SBW[k].mats, out = {}; const add = (m, n) => out[m] = (out[m] || 0) + n;
  const own = { stab: "vwheel", eng: "atitan", emit: "amatrix", reactor: "areact" }[tgt]; if (own) add(own, seg);
  for (let i = 0; i < seg; i++) { const r = Math.random(); if (r < .45) add(M[1], 1); else if (r < .7) add(M[k === "vae" ? 3 : 1], 1); else if (r < .78) add(M[k === "vae" ? 0 : 2], 1); else if (r < .8) add(SBW[k].rare, 1); }
  return Object.entries(out); }
async function sbResolve(f) { const k = f.sb, D = SBW[k];
  G.resolving.add(f.id); const T0 = now();
  const home = () => { f.phase = "back"; f.back = Math.max(T0, f.arrive) + (f.tt || 60000); if (!Object.values(f.n || {}).some(v => v > 0)) S.fleets = S.fleets.filter(x => x !== f); };
  try { const at = f.arrive, s0 = sbStartOf(k, at); if (s0 == null || at < s0 + SB_ARR || at >= sbEnd(k, s0)) { note(`${D.n} was gone when our fleet arrived. Returning.`, "warn"); return home(); }
    const ref = adb().doc("event/sb_" + k); for (let i = 0; i < 8; i++) { const r = await ref.acquire({ holder: G.me, ttlMs: 15000 }); if (r.acquired) break; await sleep(1500); }
    const snap = await ref.get(), cur = sbNorm(snap.exists ? snap.data() : null, s0), n0 = cur.hp; if (!n0) { note(`${D.n} had already fallen when our fleet arrived. Returning.`, "warn"); return home(); }
    let tgt = f.sbT || "core"; const open = sbTargets(k, cur, s0, at).find(x => x[0] === tgt); if (!open || (open[2] != null && open[2] <= 0)) tgt = "core";
    const { m, fp, why } = sbMods(k, cur, s0, at, tgt), cap = tgt === "core" || tgt === "reactor" ? n0 : open[2];
    const mkD = () => { const st2 = stacksOf({ [D.u]: n0 }, { wbSh: 1 }, "wboss"); for (const s of st2) s.atk *= fp; return st2; }; mkD.k = k;
    const mine0 = Object.assign({}, f.n), { res, rise } = sbFightRise(() => stacksOf(f.n, techOf(null), G.me), mkD, n0, cap, tgt === "core" || tgt === "reactor" ? m : 1);
    const rep0 = {}; let seg = Math.min(cap, n0 - clamp(Math.round(((res.dLeft || {})[D.u]) || 0), 0, n0)); const xf0 = aexXf(cur);
    if (tgt === "core" || tgt === "reactor") { const take = Math.min(n0, tgt === "reactor" ? seg * 2 : seg); cur.hp = n0 - take; seg = take; }
    else { const key = tgt === "stab" ? "stab" + vaeCycle(s0, at).c : tgt, b0 = Math.floor((cur.wp[key] || 0) / WPK[tgt]); cur.wp[key] = (cur.wp[key] || 0) + seg; rep0.broke = Math.floor(cur.wp[key] / WPK[tgt]) - b0; }
    if (seg) { cur.dmg[G.me] = (cur.dmg[G.me] || 0) + seg; cur.log.push([at, cur.hp, tgt]); } if (!cur.hp) { cur.dead = at; cur.last = G.me; }
    await ref.set(cur); if (G.mode === "online") G.sb[k] = cur; SBN[k] = null;
    const form = k === "aex" ? (aexXf(cur) && aexXf(cur) <= at ? 1 : 0) : 0, tname = (open || [0, D.n])[1];
    const rep = mkRep({ at, kind: "attack", title: `Assault on ${D.n}${tgt !== "core" ? ` · ${tname}` : ""}`, aUids: [G.me], aName: S.homeName + " Fleet", dName: D.n, sbk: k, sbForm: form, sbSeg: [n0, cur.hp], sbT: tgt, omRise: rise > 1.01 ? Math.round(rise * 10) / 10 : undefined, lvl: 35, ptype: "gas", fortL: 0, alien: true,
      start: res.start, rounds: res.rounds, winner: res.winner, sim: res.sim, lossA: lossesOf(res.start.a, res.aLeft), lossD: lossesOf(res.start.d, res.dLeft) });
    f.n = cleanShips(res.aLeft); repairDocks(rep, lossesOf(mine0, f.n));
    if (seg) { const L = { m: 45000 * seg, c: 30000 * seg, g: 15000 * seg }, ratio = Math.min(1, cargoOf(f.n) / Math.max(1, total(L)));
      rep.loot = { m: Math.floor(L.m * ratio), c: Math.floor(L.c * ratio), g: Math.floor(L.g * ratio) }; f.loot = rep.loot; const sh = 3 * seg; S.shards = (S.shards || 0) + sh; rep.shards = sh; evPts("hunt", seg * 70); S.wins++;
      const got = sbMatGive(sbMatRoll(k, tgt, seg), D.n); rep.sbMats = got; logReward(`${D.n} bounty`, rep.loot, { shards: sh, kind: "battle" }); rep.mats = fsDrop(lootRoll([["void", 5, 1 + Math.floor(seg / 4)]]), D.n, { nocap: 1 }); }
    if (why.length) note(`${D.n}: ${why.join("; ")}.`, "info"); if (rise > 1.01) note(`${D.n} rose to meet our fleet: ×${fmt(Math.round(rise))} toughness and firepower against a force this size.`, "warn");
    if (k === "aex" && !xf0 && aexXf(cur)) note("Our attack broke Aexion past 60%: it is transforming into its Warform! Its armour is open for 20 minutes.", "win");
    if (!cur.hp) { bump("bosses"); note(`We brought down ${D.n}! Everyone who fought it can claim the spoils.`, "win"); }
    else note(seg ? `Our fleet ${tgt === "core" || tgt === "reactor" ? `broke ${seg} section${seg > 1 ? "s" : ""} off ${D.n} (${cur.hp} of 100 left)` : `hit the ${tname.toLowerCase()} for ${seg} sections${rep0.broke ? ` and destroyed ${rep0.broke}` : ""}`}${rep.loot ? `. Bounty: ${fmt(rep.loot.m)} metal, ${fmt(rep.loot.c)} crystal, ${fmt(rep.loot.g)} gas, ◆${rep.shards}${rep.sbMats && rep.sbMats.length ? ", " + rep.sbMats.join(", ") : ""}` : ""}.` : `${D.n} shrugged off our attack.`, seg ? "win" : "loss");
    addReport(rep); sbClaim(); home();
  } catch (e) { note(`Lost contact with the ${D.n} fight. Fleet returning.`, "warn"); home(); }
  finally { G.resolving.delete(f.id); dirty(); progress(); softRender(); } }
/* it fell: everyone who broke a section claims once: shards by share, elemental runes (the super boss rule, and 1 for everyone who
   fought), its materials (its rarest for the top ten), an item; the top damage a Teleport Ticket */
function sbClaim() { if (!S || !G.ready || G.sbSim) return; const T = now(); for (const k in SBW) { const s0 = sbStartOf(k, T); if (s0 == null) continue; const st = sbState(k, s0), my = st.dmg[G.me] || 0;
  S.sbGot = S.sbGot || {}; if (st.hp > 0 || !my || S.sbGot[k] === s0) continue; S.sbGot[k] = s0; const D = SBW[k], rank = Object.entries(st.dmg).sort((a, b) => b[1] - a[1]).map(x => x[0]), tot = Object.values(st.dmg).reduce((a, b) => a + b, 0) || 1, share = my / tot, i = rank.indexOf(G.me);
  const sh = 30 + Math.round(200 * Math.min(1, share * 4)), rn = 1 + (i < 3 ? 1 : 0) + (i === 0 ? 1 : 0) + (st.last === G.me ? 1 : 0), it = DROPS[(Math.random() * DROPS.length) | 0];
  S.shards = (S.shards || 0) + sh; grantRunes(rn, `${D.n} core`); giveItem(it); if (i === 0) giveItem("teleport"); const got = sbMatGive([[D.rare, i < 10 ? 2 : 1], [D.mats[i < 3 ? 0 : 1], 2]], D.n);
  logReward(`${D.n} destroyed`, null, { shards: sh, item: it, runes: rn, kind: "battle" });
  note(`${D.n} is destroyed! Your share: ◆${sh}, ${rn} elemental rune${rn > 1 ? "s" : ""}, ${got.join(", ")}, ${SHOP[it].n}${i === 0 ? " and a Teleport Ticket for top damage" : ""}.`, "win"); dirty(); } }
/* a material's emblem: a small drawn gem in its colours */
function sbMatIcon(k, sz = 22) { const M = SBM[k]; if (!M) return ""; const [n, a, b, shp] = M, id = "g" + k, P = { ring: '<circle cx="12" cy="12" r="7.5" fill="none" stroke="url(#ID)" stroke-width="3.4"/><circle cx="12" cy="12" r="2.4" fill="' + b + '"/>', scale: '<path d="M12 2 L20 9 L16 21 L8 21 L4 9 Z" fill="url(#ID)" stroke="' + b + '" stroke-width="1.2"/>', orb: '<circle cx="12" cy="12" r="8" fill="url(#ID)"/><circle cx="9.5" cy="9.5" r="2.4" fill="#fff" opacity=".7"/>',
    rune: '<path d="M12 2 L21 12 L12 22 L3 12 Z" fill="url(#ID)"/><path d="M12 6 V18 M8 10 L16 14" stroke="#fff" stroke-width="1.6" opacity=".85"/>', ingot: '<path d="M3 15 L7 8 H17 L21 15 Z" fill="url(#ID)" stroke="' + b + '"/><path d="M3 15 H21 V18 H3 Z" fill="' + b + '"/>', hex: '<path d="M12 2 L20.6 7 V17 L12 22 L3.4 17 V7 Z" fill="none" stroke="url(#ID)" stroke-width="2.4"/><path d="M12 7 L16.3 9.5 V14.5 L12 17 L7.7 14.5 V9.5 Z" fill="' + b + '" opacity=".8"/>',
    gear: '<circle cx="12" cy="12" r="6.5" fill="url(#ID)"/><g stroke="' + b + '" stroke-width="2.6">' + [0, 45, 90, 135].map(r => `<path d="M12 1.5 V5 M12 19 V22.5" transform="rotate(${r} 12 12)"/>`).join("") + '</g><circle cx="12" cy="12" r="2.2" fill="#10151e"/>' }[shp];
  return `<svg class="sbmi" width="${sz}" height="${sz}" viewBox="0 0 24 24" aria-label="${esc(n)}"><defs><linearGradient id="${id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></linearGradient></defs>${P.split("ID").join(id)}</svg>`; }
/* the scan card and attack panel */
function shSboss() { const k = (sheet && sheet.id) || sbLiveKey() || "vae", D = SBW[k], T = now(), s0 = sbStartOf(k, T), nx = sbNext(k, T), live = s0 != null && T < sbEnd(k, s0) && T >= s0, st = s0 != null ? sbState(k, s0) : sbNorm(null, 0);
  const on = sbOn(k, T), hp = live ? st.hp : 100, ph = sbPhase(k, hp), my = live ? st.dmg[G.me] || 0 : 0, sent = S.fleets.some(f => f.sb === k && f.phase === "out"), avail = originAvail(), sel = selected(), xf = k === "aex" && live ? aexXf(st) : 0;
  const art = k === "aex" && !xf ? D.art0 : D.art, tg = live ? sbTargets(k, st, s0, T) : [], cur = (S.sbTgt && S.sbTgt[k]) || "core", tsel = tg.find(x => x[0] === cur) ? cur : "core", mods = live ? sbMods(k, st, s0, T, tsel) : { why: [] };
  const lead = live ? Object.entries(st.dmg).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([u, v], i) => `<li><span>${i + 1}. ${esc(u === G.me ? "You" : nameOf(u))}</span><b>${v}</b></li>`).join("") : "";
  let shield = ""; if (live && k === "vae") { const { c, ce } = vaeCycle(s0, T), d = Math.min(6, wpN(st, "stab" + c, "stab")); shield = `<dt>Wheel stabilizers</dt><dd>${[0, 1, 2, 3, 4, 5].map(i => `<i class="sbpip ${i < d ? "off" : ""}"></i>`).join("")} ${hp > 75 ? "dormant" : `${d}/6 broken · charge in <b data-end="${ce}">${ftime(ce - T)}</b>`}</dd>`; }
  if (live && k === "aex") { const e = Math.min(8, wpN(st, xf ? "emit" : "eng", xf ? "emit" : "eng")); shield = `<dt>${xf ? "Shield emitters" : "Stern engines"}</dt><dd>${[0, 1, 2, 3, 4, 5, 6, 7].map(i => `<i class="sbpip ${i < e ? "off" : ""}"></i>`).join("")} ${e}/8 destroyed</dd>`; }
  let body = ""; if (!live) body = `<p class="note">${D.n} tears into the galaxy on the ${D.day}${["th", "st", "nd", "rd"][(D.day % 10 > 3 || [11, 12, 13].includes(D.day)) ? 0 : D.day % 10]} of every month at ${new Date(nx).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })} your time, for 36 hours. Next: <b data-end="${nx}">${ftime(nx - T)}</b>.</p>${duelOwner() ? `<button class="btn ghost wide" data-act="sb${k === "vae" ? "Vae" : "Aex"}">▶ Watch the preview (owner)</button>` : ""}`;
  else if (!on) body = `<p class="note">${hp ? (T < s0 + SB_ARR ? `${D.n} is arriving. Attacks open in <b data-end="${s0 + SB_ARR}">${ftime(s0 + SB_ARR - T)}</b>.` : "It cannot be attacked right now.") : `Destroyed. ${k === "vae" ? "A celestial relic drifts where it fell." : "Its wreck drifts past the Rim."}`}</p>`;
  else if (!canPlay()) body = `<p class="note">${G.mode === "connecting" ? connNote() : "You can only watch this galaxy."}</p>`;
  else if (sent) body = `<p class="note">Our fleet is on its way.</p>`;
  else if (!Object.keys(avail).length) body = `${originBar()}<p class="note">No ships at ${esc((originPlanet() || {}).name || S.homeName)}.</p>`;
  else body = `<h2 class="sec">Target</h2><div class="sbtg">${tg.map(([id, n, left, sub]) => `<button class="sbt ${id === tsel ? "on" : ""}" data-act="sbTgt" data-id="${k}:${id}" ${left != null && left <= 0 ? "disabled" : ""}><b>${esc(n)}</b><small>${esc(sub || (id === "core" ? "its hull" : ""))}</small></button>`).join("")}</div>
    ${mods.why.length ? `<p class="note sbwhy">${esc(mods.why.join(" · "))}</p>` : ""}<h2 class="sec">Attack</h2>${originBar()}${picker(avail)}${speedBar(SBO[k], sel)}<button class="btn wide amber" data-act="sbGo" data-id="${k}" ${Object.keys(sel).length && !slotsFull() ? "" : "disabled"}>⚔ Attack ${esc(D.n)}</button>`;
  const mine = (D.mats || []).map(m => `<span class="sbmat">${sbMatIcon(m)}<b>${fmt((S.sbMat || {})[m] || 0)}</b><small>${esc(SBM[m][0])}</small></span>`).join("");
  return `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter">${live && hp ? "● LIVE · " : ""}${esc(D.ev)}</div><h2>${esc(D.n)}</h2><p class="note">${esc(D.t)} · ${D.diff} super boss</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
    <div class="sbart"><img src="${art}" alt="${esc(D.n)}" loading="lazy"><span class="sbph">${live ? (hp ? esc(D.ph[ph][1]) : "Destroyed") : "Not yet arrived"}</span></div>
    <div class="wbhp"><div class="wbbar"><i style="width:${hp}%;background:${D.col}"></i></div><span>${live ? (hp ? `${hp} of 100 sections · ${esc(D.ph[ph][1])}` : "Destroyed") : "Full strength"}</span></div>
    <dl class="kv">${shield}<dt>Recommended fleet</dt><dd>Your largest: it rises to meet any force, 8–20% of its hull per attack</dd><dt>Your sections</dt><dd>${my || "None yet"}</dd>${live && hp ? `<dt>Leaves in</dt><dd><b data-end="${sbEnd(k, s0)}">${ftime(sbEnd(k, s0) - T)}</b></dd>` : ""}
      <dt>Bounty per section</dt><dd>${costHTML({ m: 45000, c: 30000, g: 15000 })} + ◆3 + its materials</dd><dt>When it falls</dt><dd>◆ shards by share, 1–4 elemental runes, ${esc(SBM[D.rare][0])}, an item; the top damage a Teleport Ticket</dd></dl>
    ${body}${lead ? `<h2 class="sec">Top damage</h2><ol class="wblead">${lead}</ol>` : ""}
    <h2 class="sec">Abilities</h2><ul class="sbab">${D.abil.map(([a, b]) => `<li><b>${esc(a)}</b><span>${esc(b)}</span></li>`).join("")}</ul>
    <h2 class="sec">Your ${esc(D.n)} materials</h2><div class="sbmats">${mine}</div><p class="note">Forge recipes for these are coming.</p>`; }
/* the band over the map: live, or counting down in the last three days */
function sbBand() { const T = now(), b = $("#sbband"); let html = ""; if (view === "galaxy" && !G.sbSim && !sheet && !battle) { const k = sbLiveKey(T);
    if (k) { const D = SBW[k], s0 = sbStartOf(k, T), st = sbState(k, s0); html = st.hp ? `<button class="sbb" data-act="sbOpen" data-id="${k}" style="--c:${D.col}"><b>${D.ic} ${esc(D.n.toUpperCase())}</b><span>${st.hp}/100</span><i>⚔ Attack</i></button>` : ""; }
    else for (const k2 in SBW) { const nx = sbNext(k2, T); if (nx - T < 72 * SB_H) { const D = SBW[k2]; html = `<button class="sbb soon" data-act="sbOpen" data-id="${k2}" style="--c:${D.col}"><b>${D.ic} ${esc(D.n.toUpperCase())}</b><span>arrives in ${ftime(nx - T)}</span></button>`; break; } } }
  if (!html) { if (b) b.remove(); return; } if (!b) { const A = $("#app"); if (!A) return; const e = document.createElement("div"); e.id = "sbband"; e.innerHTML = html; A.appendChild(e); } else if (b.dataset.h !== html) { b.dataset.h = html; b.innerHTML = html; } }
setInterval(() => { try { sbBand(); sbClaim(); } catch (e) {} }, 1000);
/* on the galaxy map, for everyone: the boss stands past the Rim for its 36 hours, its moments played from the shared clock */
function sbLiveTick(W, t) { const T = now(), k = sbLiveKey(T); if (!k || view !== "galaxy") { if (W.sb && W.sb.live) sbFree(W); return; }
  if (W.sb && (!W.sb.live || W.sb.key !== k)) sbFree(W); const X = W.sb || sbBuild(W, k, 1), b = X.b, D = SBX[k], s0 = sbStartOf(k, T), st = sbState(k, s0), e = (T - s0) / 1000; X.live = 1;
  const say = (id, line) => { G.sbSaid = G.sbSaid || {}; if (G.sbSaid[id]) return; G.sbSaid[id] = 1; try { advHolo(line, 1); } catch (er) {} };
  const arr = clamp((e - 1.5) / 4, 0, 1); X.rift.material.opacity = bell01(e, .2, 1.5, 5, 8) * .9; X.rift.scale.setScalar(4 + D.sc * 22 * clamp(e / 3, 0, 1)); X.flash.material.opacity = bell01(e, 1.2, 1.8, 2.4, 4.5); X.flash.scale.setScalar(D.sc * 60);
  if (e < 600) say(k + s0 + "a", k === "vae" ? "WARNING: a celestial anomaly is tearing open beyond the Rim. Vaelthar has arrived!" : "WARNING: a dreadnought-class signature is dropping out of warp. Aexion has arrived!");
  let scl = D.sc * Math.max(.001, 1 - Math.pow(1 - arr, 3)); const dead = st.dead && st.dead < T, df = dead ? (T - st.dead) / 1000 : 0;
  if (k === "vae") { if (dead) scl *= Math.max(.001, 1 - clamp((df - .6) / 2.5, 0, 1)); b.grp.scale.setScalar(scl);
    const { c, ce } = vaeCycle(s0, T), res = vaeResult(st, s0, c), f = (T - (ce - 150e3)) / 180e3; let fa = -1; if (st.hp && sbHpAt(st, ce) <= 75 && f >= 0 && f < 1) { fa = res === "interrupted" && f > .58 ? -1 : f; if (f < .05) say(k + ce + "w", "WARNING: CATASTROPHIC CELESTIAL ENERGY SIGNATURE DETECTED. Break the wheel's stabilizers!"); if (res === "interrupted" && f > .58) say(k + ce + "i", "The charge collapsed! Its core is exposed: strike now!"); }
    b.drive("annihilate", fa); const d = Math.min(6, wpN(st, "stab" + c, "stab")); for (let i = 0; i < 6; i++) b.stab[i] = i < d ? 0 : 1; b.crack = st.hp <= 25 ? .4 + (25 - st.hp) / 25 * .6 : 0;
    if (!dead && fa < 0) { const slot = Math.floor(T / 30000); if (slot !== X.slot) { X.slot = slot; b.act(SBW.vae.mv[Math.abs(hash("v" + slot)) % SBW.vae.mv.length]); } } }
  else { const xf = aexXf(st); b.drive("transform", xf ? clamp((T - xf) / 60000, 0, 1) : 0); if (xf && T - xf < 60000) say(k + xf, "WARNING: Aexion is transforming! Its hull is splitting apart!");
    b.drive("overdrive", st.hp && st.hp <= 20 ? (T / 4200) % 1 : -1); if (!dead) { const slot = Math.floor(T / 25000); if (slot !== X.slot) { X.slot = slot; const L = xf ? SBW.aex.mv2 : SBW.aex.mv; b.act(L[Math.abs(hash("a" + slot)) % L.length]); } }
    if (dead) { const ff = clamp(df / 5, 0, 1); b.grp.rotation.x = -ff * .9; b.grp.position.y = X.B.y - ff * 40; } b.grp.scale.setScalar(scl); }
  b.tick(t); W.renderer.toneMappingExposure = X.exp * (1 - (b.dark || 0) * .4); }
