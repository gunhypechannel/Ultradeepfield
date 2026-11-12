# v488 Khezaroth, the Dark Matter Sphinx: the hunt (owner's brief, assets/bosses/khezaroth/ref/brief-2026-11-12.txt; owner chose the
# fifth Wednesday slot: the great events now rotate vae, dv, aex, conv, khz, each back every 5 weeks; first Khezaroth Wed 2026-12-16).
# A defensive, puzzle-like guardian, 100 sections, 36 hours, on the shared record event/sb_khz (compare-and-set like the others).
#   Ancient Guardian (100-75): Abyssal Claw, Gravity Crush, Rune Barrage, gravitational pulses.
#   The Three Seals (75-50) and Judgment of the Abyss (50-25): three rune anchors stand round it (Gravity, Runes, Void), each its own
#     target with its own attack (x1.25 / x1.1 / x1.4 firepower against those who strike it); every standing anchor shields its body
#     (-15% sections each; all three down: +30%). They rebuild each 6-hour cycle. From 50% the singularity charges every 6 hours: break
#     all three anchors in the cycle and it collapses (stunned: +50% sections for an hour), or the shockwave fires (x1.6 firepower for
#     an hour, only for fleets that attack then).
#   The Unsealed Heart (below 25): the chest armour parts; it hits 30% harder, its defences fail (+20%), and its heart is a target
#     (x2 sections, x1.5 firepower).
#   Its fall: the rings fracture, the singularity destabilizes, the light fades, the body breaks into dark-matter fragments that implode;
#     a sphinx relic drifts there until the hunt closes.
# Live on the map for everyone from the shared clock: the 60-second awakening with its own camera (anomaly, debris, runes, the
# silhouette, the eyes, the paws, the black hole, the pulse, the pull-back), the anchors, the Judgment charge and shockwave, the heart,
# the fall and the relic. Owner preview (about 100 s), Boss Lab, scan card with its art, battle reports, four Forge materials with their
# own icons and the Abyssal set, stress cases, voiced Advisor lines.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('const ROT0 = Date.UTC(2026, 10, 18, 18), ROT = ["vae", "dv", "aex", "conv"]', 'const ROT0 = Date.UTC(2026, 10, 18, 18), ROT = ["vae", "dv", "aex", "conv", "khz"]')
rep('mats: ["areact", "aalloy", "amatrix", "atitan"], rare: "areact" } };', '''mats: ["areact", "aalloy", "amatrix", "atitan"], rare: "areact" },
  khz: { n: "Khezaroth", t: "The Dark Matter Sphinx", ev: "Awakening of the Abyss", day: 0, first: ROT0 + 4 * WEEK, m3: "khezaroth", u: "wbKhz", HP: 1700000, ATK: 560000, col: "#a860ff", art: "art/boss/khezaroth.webp", ic: "▲",
    mv: ["claw", "crush", "barrage", "pulse"], diff: "Ultimate", ph: [[75, "Ancient Guardian"], [50, "The Three Seals"], [25, "Judgment of the Abyss"], [0, "The Unsealed Heart"]],
    abil: [["Abyssal Claw", "A forepaw rises and sweeps a blade of dark energy through the line."], ["Gravity Crush", "The singularity between its paws swells and drags fleets into its fire."], ["Rune Barrage", "Its rune rings and floating pyramids fire volleys of rune bolts."],
      ["The Three Seals", "From 75% three rune anchors shield it: Gravity, Runes and Void, each with its own attack. Every standing anchor cuts the sections you break by 15%; all three down exposes its body (+30%). They rebuild every 6 hours."],
      ["Judgment of the Abyss", "From 50% its singularity charges every 6 hours. Break all three anchors in the cycle and it collapses (+50% for an hour); if not, the shockwave fires (×1.6 firepower for an hour)."], ["The Unsealed Heart", "Below 25% its chest armour parts: it hits 30% harder, its defences fail (+20%), and its heart can be struck (×2 sections, ×1.5 firepower)."]],
    mats: ["krelic", "karmor", "kcore", "krune"], rare: "kcore" } };''')
rep('atitan: ["Titan Weapon Components", "#9aa4b2", "#58b8ff", "gear"] };', 'atitan: ["Titan Weapon Components", "#9aa4b2", "#58b8ff", "gear"],\n  kcore: ["Abyssal Sphinx Core", "#f0dcff", "#7a2cff", "kcore"], krelic: ["Dark Matter Relic", "#3a2458", "#e0b04a", "krelic"], krune: ["Ancient Gravity Rune", "#ffd27a", "#9a50ff", "krune"], karmor: ["Khezaroth Armor Fragment", "#2a2238", "#e6b23c", "karmor"] };')
# the materials' own icons
rep("""gear: '<circle cx="12" cy="12" r="6.5" fill="url(#ID)"/>""", """kcore: '<circle cx="12" cy="12" r="10.5" fill="none" stroke="#e6b23c" stroke-width="1.1" stroke-dasharray="2 1.4"/><circle cx="12" cy="12" r="7.4" fill="url(#ID)"/><circle cx="12" cy="12" r="3.2" fill="#0a0410"/><ellipse cx="12" cy="12" rx="6.6" ry="2.2" fill="none" stroke="#f0dcff" stroke-width="1" opacity=".85" transform="rotate(-20 12 12)"/><circle cx="9" cy="8.6" r="1.5" fill="#fff" opacity=".7"/>',
    krelic: '<path d="M12 2.5 L21.5 20 H2.5 Z" fill="url(#ID)" stroke="#e0b04a" stroke-width="1.3"/><path d="M7.3 14.5 Q12 10.5 16.7 14.5 Q12 18 7.3 14.5 Z" fill="#e0b04a"/><circle cx="12" cy="14.5" r="1.7" fill="#b46cff"/><path d="M12 2.5 V7" stroke="#e0b04a" stroke-width="1"/>',
    krune: '<path d="M12 1.8 L20.5 7 V17 L12 22.2 L3.5 17 V7 Z" fill="url(#ID)" stroke="#9a50ff" stroke-width="1"/><circle cx="12" cy="12" r="5.6" fill="none" stroke="#2a1040" stroke-width="1.6"/><path d="M12 6.5 V17.5 M8.5 9.5 L15.5 14.5 M15.5 9.5 L12 12" stroke="#2a1040" stroke-width="1.6" stroke-linecap="round"/><circle cx="12" cy="12" r="1.3" fill="#fff"/>',
    karmor: '<path d="M4 6 L13 2.5 L20.5 7.5 L18.5 18 L9 21.5 L3.5 15 Z" fill="url(#ID)" stroke="#e6b23c" stroke-width="1.4"/><path d="M5 9.5 L19.5 10.5 M4.6 13 L18.8 14.2" stroke="#e6b23c" stroke-width="1.6"/><path d="M8 17 L10.5 11.8 L13 15 L16 8" stroke="#c48cff" stroke-width="1" fill="none"/>',
    gear: '<circle cx="12" cy="12" r="6.5" fill="url(#ID)"/>""")
rep('const SB_VC = 6 * SB_H, WPK = { stab: 4, eng: 3, emit: 3 }', 'const SB_VC = 6 * SB_H, WPK = { stab: 4, eng: 3, emit: 3, an: 15, an0: 15, an1: 15, an2: 15 }')
rep("/* Aexion's transformation: the first time its hull fell to 60% */", r"""/* v488 Khezaroth's three rune anchors (one cycle's worth of breaks each; they rebuild with the cycle) and its Judgment */
const KHZ_AN = [["an0", "Gravity Anchor", "drags our line into its fire"], ["an1", "Rune Anchor", "a rune barrage"], ["an2", "Void Anchor", "a void pulse, deadliest"]];
const khzAnch = (st, c) => [0, 1, 2].map(i => (st.wp["an" + i + "c" + c] || 0) < WPK["an" + i] ? 1 : 0);
function khzResult(st, s0, c) { const ce = s0 + SB_ARR + (c + 1) * SB_VC; if (sbHpAt(st, ce) > 50) return "dormant"; return khzAnch(st, c).every(a => !a) ? "interrupted" : "fired"; }
/* Aexion's transformation: the first time its hull fell to 60% */""")
rep('  else { const xf = aexXf(st); if (!xf) { const e = Math.min(8, wpN(st, "eng", "eng"));', r'''  else if (k === "khz") { const { c } = vaeCycle(s0, T);
    if (ph === 1 || ph === 2) { const al = khzAnch(st, c).filter(x => x).length; if (al) { m *= 1 - .15 * al; why.push(`${al} rune anchor${al > 1 ? "s" : ""} shielding it (−${al * 15}%)`); } else { m *= 1.3; why.push("all three anchors down: its body is exposed (+30%)"); } }
    if (c >= 1) { const prevEnd = s0 + SB_ARR + c * SB_VC; if (T < prevEnd + SB_H) { const r = khzResult(st, s0, c - 1); if (r === "interrupted") { m *= 1.5; why.push("its singularity collapsed: the sphinx is stunned (+50%)"); } else if (r === "fired") { fp *= 1.6; why.push("Judgment of the Abyss is still rippling (×1.6 firepower)"); } } }
    if (tgt === "an0") { fp *= 1.25; why.push("the Gravity Anchor drags our line into its fire (×1.25 firepower)"); } else if (tgt === "an1") { fp *= 1.1; why.push("the Rune Anchor's barrage (×1.1 firepower)"); } else if (tgt === "an2") { fp *= 1.4; why.push("the Void Anchor's pulse (×1.4 firepower)"); }
    if (ph === 3) { fp *= 1.3; m *= 1.2; why.push("the Unsealed Heart: it hits 30% harder but its defences are failing (+20%)"); if (tgt === "heart") { m *= 2; fp *= 1.5; why.push("striking the exposed heart (×2 sections, ×1.5 firepower)"); } } }
  else { const xf = aexXf(st); if (!xf) { const e = Math.min(8, wpN(st, "eng", "eng"));''')
rep('  else { const xf = aexXf(st); if (!xf) L.push(["eng"', r'''  else if (k === "khz") { const ph = sbPhase(k, st.hp); if (ph === 1 || ph === 2) { const { c } = vaeCycle(s0, T); KHZ_AN.forEach(([id, n, sub]) => { const u = st.wp[id + "c" + c] || 0; L.push([id, n, Math.max(0, WPK[id] - u), u >= WPK[id] ? "disabled this cycle" : sub]); }); } if (ph === 3) L.push(["heart", "Exposed heart", null, "double damage, deadlier"]); }
  else { const xf = aexXf(st); if (!xf) L.push(["eng"''')
rep('const own = { stab: "vwheel", eng: "atitan", emit: "amatrix", reactor: "areact" }[tgt];', 'const own = { stab: "vwheel", eng: "atitan", emit: "amatrix", reactor: "areact", an0: "krune", an1: "krune", an2: "krune", heart: "kcore" }[tgt];')
rep('if (r < .45) add(M[1], 1); else if (r < .7) add(M[k === "vae" ? 3 : 1], 1); else if (r < .78) add(M[k === "vae" ? 0 : 2], 1);', 'if (r < .45) add(M[1], 1); else if (r < .7) add(M[k !== "aex" ? 3 : 1], 1); else if (r < .78) add(M[k !== "aex" ? 0 : 2], 1);')
rep('cap = tgt === "core" || tgt === "reactor" ? n0 : open[2];', 'cap = tgt === "core" || tgt === "reactor" || tgt === "heart" ? n0 : open[2];')
rep('tgt === "core" || tgt === "reactor" ? m : 1);', 'tgt === "core" || tgt === "reactor" || tgt === "heart" ? m : 1);')
rep('if (tgt === "core" || tgt === "reactor") { const take = Math.min(n0, tgt === "reactor" ? seg * 2 : seg);', 'if (tgt === "core" || tgt === "reactor" || tgt === "heart") { const take = Math.min(n0, tgt === "reactor" || tgt === "heart" ? seg * 2 : seg);')
rep('const key = tgt === "stab" ? "stab" + vaeCycle(s0, at).c : tgt,', 'const key = tgt === "stab" ? "stab" + vaeCycle(s0, at).c : /^an\\d$/.test(tgt) ? tgt + "c" + vaeCycle(s0, at).c : tgt,')
rep('`Our fleet ${tgt === "core" || tgt === "reactor" ?', '`Our fleet ${tgt === "core" || tgt === "reactor" || tgt === "heart" ?')
# the scan card
rep('  if (live && k === "aex") { const e', '''  if (live && k === "khz") { const { c, ce } = vaeCycle(s0, T), A = khzAnch(st, c), p2 = sbPhase(k, hp), dn = A.filter(a => !a).length; shield = `<dt>Rune anchors</dt><dd>${A.map(a => `<i class="sbpip ${a ? "" : "off"}"></i>`).join("")} ${p2 === 0 ? "dormant" : p2 === 3 ? "shattered" : `${dn}/3 disabled this cycle${hp <= 50 ? ` · Judgment in <b data-end="${ce}">${ftime(ce - T)}</b>` : ""}`}</dd>`; }
  if (live && k === "aex") { const e''')
rep('data-act="sb${k === "vae" ? "Vae" : "Aex"}"', 'data-act="labPrev" data-k="${k}"')
rep("""if (!live) body = `<p class="note">${D.n} tears into the galaxy on the ${D.day}${["th", "st", "nd", "rd"][(D.day % 10 > 3 || [11, 12, 13].includes(D.day)) ? 0 : D.day % 10]} of every month at ${new Date(nx).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })} your time, for 36 hours.""",
    """if (!live) body = `<p class="note">${D.n} comes with the Wednesday boss rotation, every ${ROT.length} weeks, at ${new Date(nx).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })} your time, for 36 hours.""")
rep('`Destroyed. ${k === "vae" ? "A celestial relic drifts where it fell." : "Its wreck drifts past the Rim."}`', '`Destroyed. ${k === "vae" ? "A celestial relic drifts where it fell." : k === "khz" ? "An ancient sphinx relic drifts where it fell." : "Its wreck drifts past the Rim."}`')
rep('const set = k === "vae" ? "celes" : "sov",', 'const set = { vae: "celes", aex: "sov", khz: "abyss" }[k],')
rep('sov: ["Sovereign", [[2, { hul: 3, atk: 2 }], [4, { hul: 4, atk: 3, spd: 3 }]]] };', 'sov: ["Sovereign", [[2, { hul: 3, atk: 2 }], [4, { hul: 4, atk: 3, spd: 3 }]]], abyss: ["Abyssal", [[2, { shd: 3, hul: 2 }], [4, { shd: 4, hul: 3, boss: 4 }]]] };')
rep('computer: ["Aegis Logic Core", { amatrix: 8, atitan: 4, areact: 2 }] } } };', 'computer: ["Aegis Logic Core", { amatrix: 8, atitan: 4, areact: 2 }] } },\n  abyss: { k: "khz", it: { weapon: ["Abyssal Claw", { krune: 6, karmor: 8, kcore: 2 }], shield: ["Aegis of the Pharaoh", { krelic: 6, karmor: 6, kcore: 2 }], reactor: ["Dark Matter Heart", { kcore: 3, krune: 4, krelic: 6 }], artifact: ["Eye of Khezaroth", { krune: 6, krelic: 4, kcore: 2 }] } } };')
# the Advisor
rep('  aex: [null, "Aexion stands in its Warform. Target the shield emitters to break its Aegis.", "Reactor Overdrive! Its core is exposed. Every fleet, strike the reactor now!"] };',
    '  aex: [null, "Aexion stands in its Warform. Target the shield emitters to break its Aegis.", "Reactor Overdrive! Its core is exposed. Every fleet, strike the reactor now!"],\n  khz: [null, "The Three Seals are awake. Three rune anchors are shielding Khezaroth: take them down to expose its body.", "Judgment of the Abyss. Its singularity charges every six hours. Break all three anchors before it fires!", "Its chest armour is splitting open... that\'s its heart! Strike the dark-matter heart!"] };')
rep('aex: "A dreadnought-class signature is closing on our galaxy. Aexion arrives within three days." };', 'aex: "A dreadnought-class signature is closing on our galaxy. Aexion arrives within three days.", khz: "Something ancient is stirring in the dark between the stars. Khezaroth wakes within three days." };\nconst SB_BACK = { vae: "Long-range sensors have found Vaelthar\'s signature again. It\'s coming back stronger, within three days.", aex: "Aexion\'s signature is back on our scanners, stronger than before. It arrives within three days.", khz: "The gravity readings are bending again. Khezaroth is waking, within three days." };')
rep('(k2 === "vae" ? "Long-range sensors have found Vaelthar\'s signature again. It\'s coming back stronger, within three days." : "Aexion\'s signature is back on our scanners, stronger than before. It arrives within three days.")', 'SB_BACK[k2]')
rep('''say(k + s0 + "a", back ? (k === "vae" ? "They're back... Vaelthar has returned, and its energy readings are even stronger than before!" : "It's back... Aexion has returned, and it's even stronger than before. All fleets, battle stations!") : k === "vae" ? "WARNING: a celestial anomaly is tearing open beyond the Rim. Vaelthar has arrived!" : "WARNING: a dreadnought-class signature is dropping out of warp. Aexion has arrived!");''',
    '''say(k + s0 + "a", k === "khz" ? (back ? "It's back. Khezaroth's anomaly is opening again, and the pull is stronger than last time." : "WARNING: a massive gravitational anomaly is opening in the ancient sector!") : back ? (k === "vae" ? "They're back... Vaelthar has returned, and its energy readings are even stronger than before!" : "It's back... Aexion has returned, and it's even stronger than before. All fleets, battle stations!") : k === "vae" ? "WARNING: a celestial anomaly is tearing open beyond the Rim. Vaelthar has arrived!" : "WARNING: a dreadnought-class signature is dropping out of warp. Aexion has arrived!");''')
rep('  else { if (e < 9) { b.grp.position.copy(X.B); aexWarp(', '  else if (k === "khz") khzLive(W, X, b, T, t, e, st, s0, dead, df, scl, say);\n  else { if (e < 9) { b.grp.position.copy(X.B); aexWarp(')
rep("/* v454 Aexion's death (owner:", r"""/* v488 Khezaroth live: the awakening (60 s, its own camera), the anchors of the cycle, the Judgment charge on the shared clock, the
   unsealed heart, its fall into fragments and the relic it leaves */
const KHZ_WAKE = [[.05, "w1", "Gravity readings are spiking. Space is folding in on itself out there."], [.24, "w2", "There are ruins in the anomaly. Ancient ones... and the runes on them are lighting up."], [.42, "w3", "Something enormous is taking shape in there. Is that... a sphinx?"],
  [.56, "w4", "Its eyes just opened. Khezaroth is awake!"], [.76, "w5", "It's forming a black hole between its claws. Brace for the pulse!"], [.95, "w6", "Look at the size of it. Our fleets look like dust next to that thing."]];
function khzCam(X, e) { const sc = X.b.grp.scale.x || 4, P = Math.PI, ss2 = (a, b, x) => { const u = clamp((x - a) / (b - a), 0, 1); return u * u * (3 - 2 * u); };
  const ap = ss2(12, 30, e), face = ss2(31, 35, e) * (1 - ss2(40, 44, e)), paws = ss2(40, 44, e) * (1 - ss2(54, 58, e)), back = ss2(54, 62, e);
  return { y: 12 * sc + face * 8 * sc - paws * 6 * sc + back * 10 * sc, d: 1100 - ap * 560 - face * 300 - paws * 180 + back * 700, th: .32 - ap * .12 - face * .1 + back * .2, ph: .9 - ap * .45 - face * .35 + back * .25 }; }
function khzLive(W, X, b, T, t, e, st, s0, dead, df, scl, say) { const k = "khz"; b.grp.scale.setScalar(scl); const dt = Math.min(64, t - (X.lt || t)); X.lt = t;
  const aw = clamp(e / 60, 0, 1); b.drive("awake", aw < 1 ? aw : -1); if (e < 300) for (const [a, id, line] of KHZ_WAKE) if (aw >= a) say(k + s0 + id, line);
  { const c = W.cam, want = c && e < 62 && camAuto(); if (want) { if (!X.cine) X.cine = { tx: c.tx, ty: c.ty, tz: c.tz, dist: c.dist, ph: c.ph, th: c.th, out: 0 }; SBX_CAM(X, W, 0, dt, khzCam(X, e)); }
    else if (X.cine && c) { const C = X.cine; if (performance.now() - (G.camTouch || 0) < 5000) X.cine = null; else { C.out += dt; const q = 1 - Math.pow(.95, (dt || 16) / 16.7); for (const kk of ["tx", "ty", "tz", "dist", "ph"]) c[kk] += (C[kk] - c[kk]) * q; let dp = C.th - c.th; while (dp > Math.PI) dp -= TAU; while (dp < -Math.PI) dp += TAU; c.th += dp * q; if (C.out > 3500) X.cine = null; } } }
  const hp = st.hp, ph = sbPhase(k, hp), { c, ce } = vaeCycle(s0, T); b.anchOn = !dead && hp && (ph === 1 || ph === 2) ? 1 : 0; b.anch = khzAnch(st, c);
  if (b.anchOn && X.anP && X.anC === c) b.anch.forEach((a, i) => { if (!a && X.anP[i]) say(k + c + "an" + i, ["The Gravity Anchor is down!", "The Rune Anchor is down!", "The Void Anchor is down!"][i]); }); if (b.anchOn && X.anC === c && b.anch.every(x => !x)) say(k + c + "an3", "All three anchors are out. Its body is exposed!"); X.anP = b.anch.slice(); X.anC = c;
  const f = (T - (ce - 150e3)) / 180e3, res = khzResult(st, s0, c); let fj = -1;
  if (!dead && hp && sbHpAt(st, ce) <= 50 && f >= 0 && f < 1) { fj = res === "interrupted" && f > .58 ? -1 : f; if (f < .06) say(k + ce + "w", "CRITICAL: DARK MATTER SINGULARITY EXPANDING. DISABLE THE GRAVITY ANCHORS."); if (f > .3 && f < .7 && res !== "interrupted") say(k + ce + "w2", "The starlight is bending into it... it's pulling everything in!");
    if (res === "interrupted" && f > .58) say(k + ce + "i", "The anchors are down and its singularity collapsed! It's stunned. Hit it now!"); if (res !== "interrupted" && f > .76 && f < .9) say(k + ce + "f", "Gravitational shockwave! It's tearing through the fleets!"); }
  b.drive("judge", fj); X.ht = (X.ht || 0) + ((ph === 3 && hp && !dead ? 1 : 0) - (X.ht || 0)) * Math.min(1, dt * .0015); b.drive("heart", X.ht > .002 ? X.ht : -1);
  if (!dead && hp && fj < 0 && aw >= 1) { const slot = Math.floor(T / 14000); if (slot !== X.slot) { X.slot = slot; const L = b.moves; b.act(L[Math.abs(hash("k" + slot)) % L.length]); } }
  if (dead) { const dd = df / 10; b.drive("die", dd < 1 ? dd : -1); b.relic = dd >= 1 ? 1 : 0; b.anchOn = 0; if (dd < 2) say(k + st.dead + "x", "Its singularity is collapsing... Khezaroth is breaking apart! It's imploding!"); if (dd > 1.2 && dd < 8) say(k + st.dead + "r", "It's gone. Only a relic of the sphinx is left, drifting where it fell."); } else b.relic = 0; }
/* the owner preview, about 100 s: the awakening, Ancient Guardian, the Three Seals (the fleet breaks the anchors), Judgment of the Abyss
   (the shockwave cuts the fleet), the Unsealed Heart, its fall and the relic */
function sbKhz(X, W, b, s, t, dt, say, yaw, side) { const sc = SBX.khz.sc; b.drive("awake", s < 26 ? Math.max(0, s / 26) : -1);
  for (const [a, id, line] of KHZ_WAKE) if (s / 26 >= a && s < 30) say("k" + id, line);
  if (s > 27) say("k1", "Khezaroth, the Dark Matter Sphinx. An ancient guardian of the abyss. All fleets, engage!");
  for (const [at, mv, kn, near] of [[28, "claw", 3, 1], [31.5, "crush", 4, 1], [35, "barrage", 4], [38.5, "pulse", 3, 1], [74, "claw", 4, 1], [77, "crush", 4, 1], [79.5, "barrage", 5]]) if (s > at && !X["m" + at]) { X["m" + at] = 1; b.act(mv); if (kn) setTimeout(() => { try { sbKillN(X, kn, performance.now(), near); } catch (e) {} }, mv === "barrage" ? 1500 : 1000); }
  b.anchOn = s > 41 && s < 71 ? 1 : 0; if (s > 41) say("k2", SBL.khz[1]);
  for (const [at, mv, kn] of [[42.5, "ag", 3], [45, "ar", 3], [47.5, "av", 4]]) if (s > at && !X["a" + at]) { X["a" + at] = 1; b.act(mv); setTimeout(() => { try { sbKillN(X, kn, performance.now()); } catch (e) {} }, 1200); }
  b.anch = b.anch || [1, 1, 1]; for (let i = 0; i < 3; i++) { const at = 49.5 + i * 2; if (s > at && b.anch[i]) { b.anch[i] = 0; const p = X.V.set(...[[-26, 10, 10], [26, 10, 10], [0, 31, -8]][i]); b.grp.localToWorld(p); sbBoom(X, p.clone(), t, 70); sbBoom(X, p.clone().add(new TH.Vector3(10, 6, 0)), t + 200, 50); say("ka" + i, ["The Gravity Anchor is down!", "The Rune Anchor is down!", "The Void Anchor is down!"][i]); } }
  const J0 = 55, JL = 15, fj = (s - J0) / JL; b.drive("judge", fj >= 0 && fj < 1 ? fj : -1); X.quiet = fj > .2 && fj < .76;
  if (fj > 0) say("k3", "CRITICAL: DARK MATTER SINGULARITY EXPANDING. DISABLE THE GRAVITY ANCHORS."); if (fj > .35) say("k4", "The starlight is bending into it... it's pulling everything in!");
  if (fj > .77 && !X.jk) { X.jk = 1; sbKillN(X, 12, t, 1); say("k5", "Gravitational shockwave! It's tearing through the fleets!"); }
  const ht = clamp((s - 71) / 4, 0, 1); b.drive("heart", ht > 0 ? ht : -1); if (s > 71.5) say("k6", SBL.khz[3]);
  if (s > 82 && !X.fall) { X.fall = s; say("k7", "Its singularity is collapsing... Khezaroth is breaking apart! It's imploding!"); }
  if (X.fall) { const dd = (s - X.fall) / 10; b.drive("die", dd < 1 ? dd : -1); b.relic = dd >= 1 ? 1 : 0; b.anchOn = 0; b.drive("heart", -1); if (dd > 1.1) say("k8", "It's gone. Only a relic of the sphinx is left, drifting where it fell."); }
  const bp = b.grp.position, tb = { tx: bp.x, tz: bp.z };
  const K = s < 26 ? Object.assign(tb, khzCam(X, s * 60 / 26)) : s < 41 ? Object.assign(tb, { y: 14 * sc, d: 520, th: .18, ph: .55 + (s - 26) * .03 }) : s < 55 ? Object.assign(tb, { y: 20 * sc, d: 760, th: .34, ph: 1.0 - (s - 41) * .03 })
    : s < 71 ? Object.assign(tb, { y: (10 + bell01(fj, 0, .3, .7, .8) * 6) * sc, d: 460 + fj * 220, th: .1 + fj * .12, ph: .25 }) : s < 82 ? Object.assign(tb, { y: 9 * sc, d: 300, th: .08, ph: .15 + (s - 71) * .02 }) : Object.assign(tb, { y: 8 * sc, d: 640 + (s - 82) * 18, th: .25, ph: .5 });
  SBX_CAM(X, W, s, dt, K); }
/* v454 Aexion's death (owner:""")
rep('if (P.key === "vae") sbVae(X, W, b, s, t, dt, say, yaw, side); else sbAex(X, W, b, s, t, dt, say, yaw, side);', 'if (P.key === "vae") sbVae(X, W, b, s, t, dt, say, yaw, side); else if (P.key === "khz") sbKhz(X, W, b, s, t, dt, say, yaw, side); else sbAex(X, W, b, s, t, dt, say, yaw, side);')
rep('aex: { n: "Aexion", t: "The Warform Sovereign", m3: "aexion", p: [360, 40, -250], sc: 4.3, dur: 110, col: "#7ac8ff", look: 4 } };', 'aex: { n: "Aexion", t: "The Warform Sovereign", m3: "aexion", p: [360, 40, -250], sc: 4.3, dur: 110, col: "#7ac8ff", look: 4 },\n  khz: { n: "Khezaroth", t: "The Dark Matter Sphinx", m3: "khezaroth", p: [-330, 30, -310], sc: 4.2, dur: 100, col: "#a860ff", look: 6 } };')
rep('for (const k of ["vae", "aex"]) db.doc("event/sb_" + k)', 'for (const k of ["vae", "aex", "khz"]) db.doc("event/sb_" + k)')
rep('if (k === "vae" || k === "aex") return sbSimStart(k);', 'if (SBW[k]) return sbSimStart(k);')
rep('live = k => k === "vae" || k === "aex" ? sbLiveKey(T) === k', 'live = k => SBW[k] ? sbLiveKey(T) === k')
rep('NM = { vae: ["✦", "Vaelthar, the Celestial Ruin"], aex: ["✦", "Aexion, the Warform Sovereign"],', 'NM = { vae: ["✦", "Vaelthar, the Celestial Ruin"], aex: ["✦", "Aexion, the Warform Sovereign"], khz: ["▲", "Khezaroth, the Dark Matter Sphinx"],')
rep('sbVae: () => sbSimStart("vae"), sbAex: () => sbSimStart("aex"),', 'sbVae: () => sbSimStart("vae"), sbAex: () => sbSimStart("aex"), sbKhz: () => sbSimStart("khz"),')
rep('${G.sbSim && G.sbSim.key === "aex" ? "■ Stop the Aexion preview" : "▶ Watch Aexion, the Warform Sovereign"}</button>', '${G.sbSim && G.sbSim.key === "aex" ? "■ Stop the Aexion preview" : "▶ Watch Aexion, the Warform Sovereign"}</button><button class="btn ghost wide" data-act="${G.sbSim && G.sbSim.key === "khz" ? "sbStop" : "sbKhz"}">${G.sbSim && G.sbSim.key === "khz" ? "■ Stop the Khezaroth preview" : "▶ Watch Khezaroth, the Dark Matter Sphinx"}</button>')
# battle reports
rep('const big = wbk === "omg" ? 1.35 : wbk === "vae" ? 1.2 : 1', 'const big = wbk === "omg" ? 1.35 : wbk === "vae" ? 1.2 : wbk === "khz" ? 1.25 : 1')
rep('aexion: [-.4, [-26, 10, 64], [0, 9, 0]], aexW:', 'aexion: [-.4, [-26, 10, 64], [0, 9, 0]], khezaroth: [0, [-24, 20, 96], [0, 13, 4]], aexW:')
rep('const WB_FRONT = { supercube: 0, omega: 0,', 'const WB_FRONT = { khezaroth: 0, supercube: 0, omega: 0,')
rep('if (WBR.b.debris) { WBR.b.debris.visible = false; WBR.b.noDeb = 1; } /* v486, v488 */', 'if (WBR.b.debris) { WBR.b.debris.visible = false; WBR.b.noDeb = 1; } if (key === "khz" && battle && battle.r) { const h = (battle.r.sbSeg || [100])[0]; WBR.b.anchOn = h <= 75 && h > 25 ? 1 : 0; if (h <= 25) WBR.b.drive("heart", 1); } /* v486, v488 */')
rep('con: [[.6, .4, .95], [.9, .85, 1]], epx: [[.6, .5, .8], [1, .95, 1]] };', 'con: [[.6, .4, .95], [.9, .85, 1]], epx: [[.6, .5, .8], [1, .95, 1]], khz: [[.45, .16, .85], [.92, .78, 1]] };')
rep('{ key: "aex", t: "sb", form: "Warform", sh: 1, n0: 55, sbForm: 1 },', '{ key: "aex", t: "sb", form: "Warform", sh: 1, n0: 55, sbForm: 1 }, { key: "khz", t: "sb", form: "Ancient Guardian", sh: 1, n0: 100 }, { key: "khz", t: "sb", form: "Three Seals", sh: 1, n0: 60 }, { key: "khz", t: "sb", form: "Unsealed Heart", sh: 1, n0: 20 },')
# the Advisor's awe for it
rep('"vae": ["The whole wheel is turning toward us', '"khz": ["It\'s a sphinx the size of a moon, and it\'s holding a black hole in its paws. I\'ve got nothing, Commander.", "The light itself is bending around it. I\'ve never seen gravity do that.", "Those runes are older than anything in our records. Older than the galaxy maps."], "vae": ["The whole wheel is turning toward us')
s = re.sub(r"GAME_V = 488\b", "GAME_V = 488", s)
open(P, 'w').write(s)
