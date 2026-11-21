/* ---------- v703/v704 the Carcinid on the battle screen and the map: profiles, sizes, weapons, and their 3D models (built in code) ----------
   v704 rebuilt after the owner's paintings. The shape language they share:
   - crabs: a wide carapace with a pointed brow, gilded plate rims, curved horns rising off the back, a fringe of hooked fangs under the
     eyes over a cyan core, and enormous crescent pincers (two sickle fingers, serrated inside) that close almost into a ring;
   - ships: long hulls of overlapping armour plates with gilded edges, crescent blades sweeping forward from the prow, sickle claws folded
     under the belly like legs, swept fins on the back, a cyan eye on the flank and twin cyan drives;
   - palette: near-black chitin with a violet sheen, gold-bronze edges and claws, cyan light (the bosses carry their own tints).
   The crabs walk (each leg steps in turn, the pincers lift and the body rides on them), the Kraken's arms writhe, the nest breathes. */
Object.assign(CPROF, { clevd: ["capital", "plasma", .34, 0, 2, 2], cscut: ["fighter", "acid", .12, .24, 7, 0], cspit: ["frigate", "plasma", .08, .12, 5, 0], charv: ["support", "acid", .14, .08, 3, 0], cguard: ["cruiser", "laser", .36, .03, 3, 2],
  cbrood: ["carrier", "acid", .22, .04, 2.6, 2], cwar: ["cruiser", "laser", .28, .08, 4, 1], ccrys: ["frigate", "ion", .2, .1, 4.5, 1], clanc: ["battleship", "plasma", .26, .06, 3.6, 1], cmolt: ["titan", "plasma", .3, 0, 1.8, 3], ckrak: ["titan", "acid", .24, .04, 2.4, 2],
  cfrig: ["frigate", "ion", .16, .14, 5.5, 1], cint: ["interceptor", "laser", .06, .3, 9, 0], cdest: ["frigate", "plasma", .14, .14, 6, 1], cvang: ["cruiser", "ion", .22, .08, 4.2, 2], ccarr: ["carrier", "laser", .2, .04, 3, 3], cpearl: ["interceptor", "beam", .05, .32, 9.5, 0],
  cmint: ["interceptor", "ion", .08, .3, 9, 0], cregent: ["battleship", "beam", .28, .04, 3.2, 3], cempr: ["titan", "beam", .34, 0, 1.8, 5], cbrlord: ["carrier", "acid", .24, .03, 2.6, 4], cnest: ["station", "acid", .3, 0, 0, 2],
  cmar: ["titan", "laser", .34, .02, 1.8, 4], cmat: ["titan", "acid", .3, 0, 1.4, 5], ctyr: ["titan", "plasma", .42, 0, 1.2, 5], cora: ["titan", "ion", .28, .04, 1.6, 4], ckor: ["titan", "beam", .36, 0, 1.6, 6],
  cbeh: ["titan", "plasma", .44, 0, 1, 6], ckbr: ["titan", "acid", .3, .02, 1.8, 4], cpal: ["titan", "ion", .32, .04, 1.6, 5], ccrown: ["titan", "beam", .4, 0, 1.2, 7], ccrownm: ["titan", "plasma", .2, 0, 1.8, 4] });
Object.assign(BOSSK, { clevd: 2.6, cscut: 1.55, cspit: 1.6, charv: 1.6, cguard: 1.85, cbrood: 2, cwar: 1.9, ccrys: 1.7, clanc: 2, cmolt: 2.4, ckrak: 2.6, cfrig: 1.7, cint: 1.55, cdest: 1.75, cvang: 1.9, ccarr: 2.1, cpearl: 1.55, cmint: 1.55, cregent: 2.4, cempr: 2.8, cbrlord: 2.4, cnest: 2.1,
  cmar: 3.2, cmat: 3.2, ctyr: 3.3, cora: 3.2, ckor: 3.6, cbeh: 3.6, ckbr: 3.4, cpal: 3.4, ccrown: 4.2, ccrownm: 4.2 });
Object.assign(MIM_HULL, { clevd: 3.9, cscut: .8, cspit: .9, charv: .95, cguard: 1.4, cbrood: 1.7, cwar: 1.5, ccrys: 1.2, clanc: 1.8, cmolt: 2.6, ckrak: 2.8, cfrig: 1.15, cint: .9, cdest: 1.3, cvang: 1.6, ccarr: 2, cpearl: .85, cmint: .9, cregent: 2.5, cempr: 3, cbrlord: 2.4, cnest: 1.7,
  cmar: 3.7, cmat: 3.7, ctyr: 3.8, cora: 3.7, ckor: 4.2, cbeh: 4.4, ckbr: 4, cpal: 4, ccrown: 5.4, ccrownm: 5.4 });
Object.assign(MIM_PACK, { cscut: 1, cspit: 1, charv: 1, cint: 1, cpearl: 1, cmint: 1 }); MIM_STA.cnest = .44;
Object.assign(BOSS_GLOW, { ckor: "232,180,90", ccrown: "255,210,120", ccrownm: "160,250,255", cmar: "255,90,90", cmat: "220,240,255", ctyr: "255,140,120", cora: "190,120,255", cbeh: "120,240,230", ckbr: "220,90,255", cpal: "200,250,255" });
{ const A = (w, n, c, d, f) => [w, n, c, d, f || {}], T = "#3fe8f0", G = "#ffc870", V = "#b48cff";
  Object.assign(MON_ATK, { cscut: [A("acid", 3, T, .14), A("flak", 4, G, .12)], cspit: [A("plasma", 2, V, .24, { hv: 1 }), A("acid", 3, G, .2)], charv: [A("acid", 3, T, .2), A("flak", 3, "#7ff8e4", .14)], cguard: [A("flak", 6, G, .12), A("ion", 2, "#7ff8e4", .22)],
    cbrood: [A("missile", 5, T, .2, { flank: 1 }), A("acid", 3, V, .2)], cwar: [A("laser", 3, G, .12), A("flak", 5, T, .1)], ccrys: [A("ion", 4, "#9ff8ff", .16), A("laser", 2, "#e8fbff", .14)], clanc: [A("plasma", 3, T, .22, { hv: 1 }), A("laser", 4, G, .12)],
    cmolt: [A("plasma", 4, "#e8fbff", .26, { hv: 1 }), A("missile", 6, T, .2, { flank: 1 })], ckrak: [A("acid", 5, "#d070ff", .2), A("plasma", 2, V, .26, { hv: 1 })],
    clevd: [A("acid", 4, T, .22), A("flak", 8, G, .12)], cfrig: [A("ion", 3, "#7ff8e4", .18), A("missile", 3, G, .2)], cint: [A("laser", 3, "#9ff8ec", .1), A("flak", 5, G, .1)], cdest: [A("plasma", 2, T, .22, { hv: 1 }), A("flak", 5, G, .12)], cvang: [A("ion", 4, T, .18), A("missile", 4, G, .2, { flank: 1 })],
    ccarr: [A("missile", 6, T, .2, { flank: 1 }), A("flak", 6, G, .12)], cpearl: [A("laser", 3, "#e8fbff", .1), A("flak", 4, T, .1)], cmint: [A("ion", 3, V, .14), A("laser", 3, T, .1)], cregent: [A("laser", 5, T, .14), A("plasma", 3, G, .24, { hv: 1 })],
    cempr: [A("plasma", 5, G, .26, { hv: 1 }), A("laser", 6, T, .12)], cbrlord: [A("missile", 8, "#ff7ab0", .2, { flank: 1 }), A("acid", 4, V, .2)], cnest: [A("missile", 4, T, .2, { flank: 1 }), A("plasma", 2, V, .26, { hv: 1 })],
    cmar: [A("laser", 5, "#ff6060", .12), A("plasma", 3, G, .24, { hv: 1 })], cmat: [A("missile", 8, "#e8fbff", .2, { flank: 1 }), A("acid", 4, T, .2)], ctyr: [A("plasma", 4, "#ff9a7a", .26, { hv: 1 }), A("flak", 8, G, .12)], cora: [A("ion", 5, V, .16), A("laser", 4, "#e0c0ff", .12)],
    ckor: [A("plasma", 5, G, .26, { hv: 1 }), A("laser", 6, T, .12)], cbeh: [A("plasma", 5, T, .28, { hv: 1 }), A("flak", 10, G, .12)], ckbr: [A("acid", 6, "#d070ff", .2), A("plasma", 3, V, .26, { hv: 1 })], cpal: [A("ion", 6, "#e8fbff", .16), A("laser", 5, T, .12)],
    ccrown: [A("plasma", 6, G, .28, { hv: 1 }), A("missile", 8, T, .2, { flank: 1 })], ccrownm: [A("plasma", 6, "#e8fbff", .3, { hv: 1 }), A("laser", 6, T, .12)] }); }
Object.assign(MIM_ATK, { cscut: "slam", cguard: "slam", cwar: "slam", clanc: "slam", cmar: "slam", ctyr: "slam", cbeh: "slam", cmolt: "slam", ckor: "slam", ccrown: "slam", ckrak: "grab", ckbr: "grab" }); /* the crabs lunge with their crush (the Kraken and the Krakenbreaker grab); the rest is crcAtkDraw */
Object.assign(MON_EL, { carcinid: "water", crcpat: "water", wkraken: "water" });
const CRC_FACE = {}; /* filled below: the crabs turn -.55, the ships -.22, the Kraken -.3 */
const CRC_CRABS = ["cscut", "cspit", "charv", "cguard", "cbrood", "cwar", "ccrys", "clanc", "cmolt", "cmar", "cmat", "ctyr", "cora", "ckor", "cbeh", "ckbr", "cpal", "ccrown", "ccrownm"];
{ const crab = `vec3 p = position; float ph = mt * 6.28318 + p.x * 2.6 + (p.z > 0. ? 0. : 3.14159), lz = clamp((abs(p.z) - .95) / 1.5, 0., 1.) * (1. - smoothstep(1.15, 1.35, p.x));
    transformed.y += lz * .16 * max(0., sin(ph)); transformed.x += lz * .12 * cos(ph);
    float cl = smoothstep(1.3, 1.9, p.x); transformed.y += cl * (.09 * sin(mt * 2.0944 + (p.z > 0. ? 0. : 1.6)) + .05 * (p.x - 1.3) * sin(mt * 4.18879));
    float tu = smoothstep(.75, 1.9, p.y) * step(abs(p.z), .9) * (1. - cl); transformed.x += tu * .05 * sin(mt * 2.0944 + p.y * 1.4); transformed.z += tu * .04 * cos(mt * 2.0944 + p.y);
    float tl = smoothstep(-1.3, -2.6, p.x) * step(abs(p.z), 1.); transformed.y += tl * .1 * sin(mt * 4.18879 + p.x * 1.6);
    transformed.y += (1. - lz) * .045 * sin(mt * 4.18879);`;
  for (const k of CRC_CRABS) MON_WAVE[k] = crab;
  MON_WAVE.ckrak = MON_WAVE.wkraken = `vec3 p = position; float ar = smoothstep(.4, 4.5, p.x); transformed.y += ar * ar * .55 * sin(mt * 2.0944 + p.x * 1.3 + p.z * 2.2); transformed.z += ar * ar * .45 * cos(mt * 2.0944 + p.x * 1.1 + p.y * 1.7);
    float mn = smoothstep(.2, -2.5, p.x); transformed.yz *= 1. + mn * .05 * sin(mt * 4.18879); transformed.y += .08 * sin(mt * 2.0944);`;
  for (const m of ["crcmar", "crcmat", "crctyr", "crcora", "crckor", "crcbeh", "crckbr", "crcpal", "crccrown"]) MON_WAVE[m] = crab;
  MON_WAVE.cnest = MON_WAVE.carcinid = `vec3 p = position; float an = atan(p.z, p.x), rr = length(p.xz), sp = smoothstep(-.6, 3.6, p.y) * step(.6, rr) * (1. - step(2.35, rr) * step(1.6, p.y) * .7);
    transformed.x += sp * .09 * sin(mt * 2.0944 + an * 3. + p.y); transformed.z += sp * .09 * cos(mt * 2.0944 + an * 3. + p.y);
    float rf = 1. - smoothstep(1.2, 1.7, length(p.xy - vec2(0., 1.1))) * step(abs(p.z), .5); transformed.xy += (p.xy - vec2(0., 1.1)) * (1. - rf) * .03 * sin(mt * 4.18879);`;
  MON_WAVE.clevd = MON_WAVE.slevi; /* v706 the Leviathan's corpse still swims */
  MON_WAVE.crcpat = `transformed.y += .08 * sin(mt * 2.0944 + position.x * .25 + position.z * .3);`; }
/* the palettes: [shell base rgb, sheen rgb, glow, gold] */
const CRC_TINT = { def: [[16, 12, 26], [34, 18, 46], 0x3fe8f0, 0xd2a45c], red: [[40, 8, 12], [80, 14, 24], 0xff4050, 0xe0a050], pearl: [[150, 150, 172], [70, 60, 100], 0x5ff0ff, 0xe8d0a0], oracle: [[28, 10, 48], [64, 24, 96], 0xb060ff, 0xd2a45c],
  gold: [[22, 17, 12], [46, 34, 12], 0x3fe8f0, 0xffc860], krak: [[26, 8, 36], [70, 12, 84], 0xd040ff, 0xd2a45c], pale: [[176, 186, 204], [90, 110, 150], 0x5ff8ff, 0xf0e0c0], coral: [[34, 12, 18], [70, 22, 34], 0x3fe8f0, 0xd8a060] };
const CRC_MC = {};
function crcMats(t) { t = CRC_TINT[t] ? t : "def"; if (CRC_MC[t]) return CRC_MC[t]; const [B, K, GL, GO] = CRC_TINT[t], C = CRC_MC[t] = {}, tex = (w, h, draw) => { const x = texCanvas(w, h, draw); x.wrapS = x.wrapT = TH.RepeatWrapping; return x; };
  /* the paintings' chitin: dark plates with a sheen, gilded seams between the segments, pitted with small scales */
  const sC = tex(256, 128, (x, W, H) => { const n = fbm2(7031), img = x.createImageData(W, H), d = img.data;
    for (let py = 0; py < H; py++) for (let px = 0; px < W; px++) { const v = n(px / 22, py / 22, 10, 4), band = Math.abs(Math.sin(py / H * Math.PI * 7)), sc = Math.abs(Math.sin(px * .35) * Math.sin(py * .5)), sp = n(px / 6, py / 6, 10, 2) > .72 ? .55 : 1, ir = n(px / 40 + 7, py / 30, 10, 3), o = (py * W + px) * 4;
      if (band < .1 || (sc < .05 && v > .5)) { d[o] = 214; d[o + 1] = 160; d[o + 2] = 78; } else { d[o] = (B[0] + v * K[0] + ir * 26) * sp; d[o + 1] = (B[1] + v * K[1] + (1 - ir) * 14) * sp; d[o + 2] = (B[2] + v * K[2] + ir * 30) * sp; } d[o + 3] = 255; } x.putImageData(img, 0, 0); });
  const sE = tex(256, 128, (x, W, H) => { x.fillStyle = "#000"; x.fillRect(0, 0, W, H); for (let i = 1; i < 7; i++) { const y = i / 7 * H; x.strokeStyle = "rgba(255,255,255,.5)"; x.lineWidth = 1.1; x.beginPath(); x.moveTo(0, y); for (let px = 0; px <= W; px += 16) x.lineTo(px, y + Math.sin(px * .09 + i) * 2); x.stroke(); }
    const r = rnd(7032); for (let i = 0; i < 40; i++) { x.fillStyle = `rgba(255,255,255,${.3 + r() * .5})`; x.beginPath(); x.arc(r() * W, r() * H, .8 + r() * 1.6, 0, TAU); x.fill(); } });
  sC.encoding = TH.sRGBEncoding;
  C.shell = new TH.MeshPhysicalMaterial({ map: sC, emissiveMap: sE, emissive: GL, emissiveIntensity: .7, metalness: .55, roughness: .3, clearcoat: 1, clearcoatRoughness: .12, envMapIntensity: 1.1 });
  C.shellD = C.shell.clone(); C.shellD.color = new TH.Color(0x9088a8); C.shellD.emissiveIntensity = .4;
  C.under = new TH.MeshPhysicalMaterial({ color: new TH.Color(`rgb(${B[0] + 10},${B[1] + 6},${B[2] + 14})`), roughness: .45, metalness: .2, clearcoat: .6, envMapIntensity: .7 });
  C.joint = new TH.MeshStandardMaterial({ color: 0x0e0a16, roughness: .55, metalness: .2 });
  C.claw = new TH.MeshPhysicalMaterial({ map: sC, color: new TH.Color(GO).lerp(new TH.Color(0xffffff), .25), metalness: .8, roughness: .26, clearcoat: 1, clearcoatRoughness: .1, envMapIntensity: 1.3 }); /* gold over the dark plate pattern */
  C.tip = new TH.MeshPhysicalMaterial({ color: GO, metalness: .9, roughness: .24, clearcoat: 1, envMapIntensity: 1.5 });
  const cC = tex(128, 128, (x, W, H) => { const n = fbm2(7033), img = x.createImageData(W, H), d = img.data; for (let py = 0; py < H; py++) for (let px = 0; px < W; px++) { const v = n(px / 9, py / 9, 10, 3), pore = n(px / 3, py / 3, 10, 2) > .66 ? .45 : 1, o = (py * W + px) * 4;
    d[o] = (190 + v * 60) * pore; d[o + 1] = (50 + v * 50) * pore; d[o + 2] = (180 + v * 70) * pore; d[o + 3] = 255; } x.putImageData(img, 0, 0); });
  cC.encoding = TH.sRGBEncoding;
  C.coral = new TH.MeshPhysicalMaterial({ map: cC, roughness: .75, metalness: 0, clearcoat: .3, emissive: 0x3a0a40, emissiveIntensity: .4, envMapIntensity: .6 });
  C.coralB = C.coral.clone(); C.coralB.color = new TH.Color(0xffb070);
  C.glow = new TH.MeshBasicMaterial({ color: new TH.Color(GL).lerp(new TH.Color(0xffffff), .45), toneMapped: false });
  C.glowS = new TH.MeshBasicMaterial({ color: new TH.Color(GL).multiplyScalar(.7), transparent: true, opacity: .3, toneMapped: false, blending: TH.AdditiveBlending, depthWrite: false });
  C.eye = new TH.MeshBasicMaterial({ color: new TH.Color(GL).lerp(new TH.Color(0xffffff), .3), toneMapped: false });
  C.pearl = new TH.MeshPhysicalMaterial({ color: 0x1a5a64, roughness: .08, metalness: 0, clearcoat: 1, emissive: 0x2fe0d0, emissiveIntensity: .8, envMapIntensity: 1.5 }); C.pearl.userData.pulse = "(.6 + .4 * sin(uMT * 1.5 + vViewPosition.x))";
  C.egg = new TH.MeshPhysicalMaterial({ color: 0x062a30, emissive: GL, emissiveIntensity: 1.1, roughness: .1, clearcoat: 1, transparent: true, opacity: .9, envMapIntensity: .6 }); C.egg.userData.pulse = "(.65 + .35 * sin(uMT * 1.7 + vViewPosition.y * 2.))";
  C.sac = new TH.MeshPhysicalMaterial({ color: 0x03322c, emissive: GL, emissiveIntensity: .85, roughness: .2, clearcoat: .8, transparent: true, opacity: .82, envMapIntensity: .4 }); C.sac.userData.pulse = "(.7 + .3 * sin(uMT * 1.3))";
  C.crys = new TH.MeshPhysicalMaterial({ color: 0x9ff0ff, emissive: GL, emissiveIntensity: .7, roughness: .05, metalness: 0, clearcoat: 1, transparent: true, opacity: .78, envMapIntensity: 1.6 });
  C.metal = new TH.MeshPhysicalMaterial({ color: new TH.Color(`rgb(${B[0] + 30},${B[1] + 24},${B[2] + 34})`), metalness: .85, roughness: .32, clearcoat: 1, envMapIntensity: 1.2 });
  C.rock = new TH.MeshStandardMaterial({ color: 0x0c0a10, roughness: .92, metalness: .05, flatShading: true });
  C.void = new TH.MeshBasicMaterial({ color: 0x010a0c, side: TH.DoubleSide });
  C.core = new TH.MeshPhysicalMaterial({ color: 0x021a18, emissive: GL, emissiveIntensity: 1.3, roughness: .15, clearcoat: 1, transparent: true, opacity: .9 }); C.core.userData.pulse = "(.65 + .35 * sin(uMT * 2.1))";
  C.tower = new TH.MeshPhysicalMaterial({ color: 0x4a3a24, metalness: .8, roughness: .3, clearcoat: 1, emissive: GL, emissiveIntensity: .15, envMapIntensity: 1.2 });
  return C; }
const CRC_SHIP = { /* f: the hull's form, L half-length, w half-width, h height, n armour plates, hk under-claws a side, eggs a side, t tint */
  cfrig: { f: "beetle", L: 2.0, w: .9, h: .55, n: 4 }, cint: { f: "fork", L: 1.9, w: .6, h: .4, n: 3 }, cdest: { f: "trident", L: 2.6, w: .75, h: .5, n: 6 },
  cvang: { f: "manta", L: 2.5, w: .8, h: .5, n: 5 }, ccarr: { f: "pod", L: 2.6, w: 1.0, h: .6, n: 5, hk: 5, eggs: 5 }, cpearl: { f: "needle", L: 2.1, w: .55, h: .36, n: 4, t: "pearl" },
  cmint: { f: "twin", L: 1.9, w: .6, h: .4, n: 3, t: "oracle" }, cregent: { f: "regent", L: 3.2, w: 1.0, h: .6, n: 7 }, cempr: { f: "crown", L: 3.2, w: 1.15, h: .65, n: 6, t: "gold" },
  cbrlord: { f: "hump", L: 2.9, w: 1.05, h: .6, n: 5, hk: 5, t: "krak" } };
const CRC_CRAB = { /* w half-width, l half-length, h height, claw size, fangs, horn pairs, legs thickness, tint, extras */
  cscut: { w: 1.05, l: 1.1, h: .5, kk: .85, fg: 4, hn: 1, th: .85 }, cspit: { w: 1.1, l: 1.1, h: .55, kk: .75, fg: 4, hn: 0, th: .95, turret: 1 }, charv: { w: 1.3, l: 1.1, h: .45, kk: .7, fg: 4, hn: 0, th: .9, sacs: 1 },
  cguard: { w: 1.25, l: 1.25, h: .95, kk: 1.05, fg: 6, hn: 2, th: 1.25, spikes: 16, coral: 4 }, cbrood: { w: 1.25, l: 1.15, h: .6, kk: .8, fg: 6, hn: 1, th: 1.05, abdo: 1 }, cwar: { w: 1.25, l: 1.2, h: .75, kk: 1.45, fg: 6, hn: 3, th: 1.15 },
  ccrys: { w: 1.15, l: 1.15, h: .6, kk: 1, fg: 4, hn: 1, th: 1, crys: 7 }, clanc: { w: .85, l: 1.35, h: .6, kk: 1.25, fg: 4, hn: 1, th: .95, tail: 1, ant: 1 }, cmolt: { w: 1.35, l: 1.3, h: .85, kk: 1.3, fg: 8, hn: 3, th: 1.25, t: "pale", molt: 1 },
  cmar: { w: 1.4, l: 1.3, h: .85, kk: 1.75, fg: 8, hn: 0, th: 1.3, t: "red", spikes: 16, crest: 7 }, cmat: { w: 1.35, l: 1.25, h: .75, kk: 1.15, fg: 6, hn: 0, th: 1.15, t: "pearl", abdo: 1, pearls: 1 },
  ctyr: { w: 1.5, l: 1.35, h: 1.05, kk: 1.35, fg: 8, hn: 1, th: 1.35, t: "coral", coral: 22, spikes: 6 }, cora: { w: 1.3, l: 1.25, h: .75, kk: 1.15, fg: 8, hn: 0, th: 1.15, t: "oracle", eye3: 1 },
  ckor: { w: 1.55, l: 1.35, h: .95, kk: 1.7, fg: 10, hn: 4, th: 1.35, t: "gold", crown: 1, spikes: 10, crest: 5 }, cbeh: { w: 1.7, l: 1.45, h: 1.2, kk: 1.4, fg: 8, hn: 1, th: 1.45, city: 1, coral: 8 },
  ckbr: { w: 1.4, l: 1.3, h: .85, kk: 1.6, fg: 10, hn: 1, th: 1.3, t: "krak", tent: 10 }, cpal: { w: 1.4, l: 1.3, h: .85, kk: 1.55, fg: 8, hn: 1, th: 1.25, t: "pale", crys: 14 },
  ccrown: { w: 1.75, l: 1.5, h: 1.2, kk: 1.8, fg: 12, hn: 5, th: 1.45, t: "gold", crown: 1, city: 1, coral: 8 }, ccrownm: { w: 1.75, l: 1.5, h: 1.2, kk: 1.8, fg: 12, hn: 5, th: 1.45, t: "pale", crown: 1, molt: 1 } };
for (const k of CRC_CRABS) CRC_FACE[k] = -.55; for (const k of Object.keys(CRC_SHIP)) CRC_FACE[k] = -.22; CRC_FACE.ckrak = -.3;
function buildCarc(k) { const D = CRC_CRAB[k] || CRC_SHIP[k] || {}, C = crcMats(D.t), g = new TH.Group(), r = rnd(hash("crc" + k)); g.userData.eng = [];
  const V = (x, y, z) => new TH.Vector3(x, y, z), add = (m, x, y, z) => { if (x != null) m.position.set(x, y || 0, z || 0); g.add(m); return m; };
  const ell = (sx, sy, sz, mat, x, y, z, seg) => { const m = add(new TH.Mesh(new TH.SphereGeometry(1, seg || 18, Math.round((seg || 18) * .7)), mat), x, y, z); m.scale.set(sx, sy, sz); return m; };
  const seg = (a, b, r0, r1, mat) => { const d = b.clone().sub(a), L = d.length(), m = new TH.Mesh(new TH.CylinderGeometry(r1, r0, L, 8, 1), mat); m.position.copy(a).addScaledVector(d, .5); m.quaternion.setFromUnitVectors(V(0, 1, 0), d.normalize()); g.add(m); return m; };
  const cone = (len, rad, mat, from, dir, bend) => { const geo = new TH.ConeGeometry(rad, len, 8, 4); geo.translate(0, len / 2, 0); if (bend) { const P = geo.attributes.position; for (let i = 0; i < P.count; i++) { const y = P.getY(i) / len; P.setZ(i, P.getZ(i) + bend * y * y * len); } geo.computeVertexNormals(); }
    const m = add(new TH.Mesh(geo, mat)); m.position.copy(from); m.quaternion.setFromUnitVectors(V(0, 1, 0), dir.clone().normalize()); return m; };
  /* a crescent blade: a tapering, slightly flattened horn that leaves along dir and curls toward bend; teeth along its inner edge */
  const sickle = (base, dir, bend, len, w, mat, o) => { o = o || {}; const N = 14, R = 7, T0 = dir.clone().normalize(), B0 = bend.clone().normalize(), curl = o.curl == null ? .6 : o.curl, th = o.th == null ? .5 : o.th, pts = [];
    for (let i = 0; i <= N; i++) { const t = i / N; pts.push(base.clone().addScaledVector(T0, len * t).addScaledVector(B0, len * curl * t * t)); }
    const P = [], I = [], sd = new TH.Vector3(), up = new TH.Vector3(), rad = [], fr = [];
    for (let i = 0; i <= N; i++) { const t = i / N, c = pts[i], tg = (i < N ? pts[i + 1].clone().sub(c) : c.clone().sub(pts[i - 1])).normalize(); sd.crossVectors(tg, B0).normalize(); up.crossVectors(sd, tg).normalize();
      const rr = w * Math.pow(1 - t, .85) * (1 + .35 * Math.sin(Math.PI * Math.min(1, t * 2.5))) + .004; rad.push(rr); fr.push([c, sd.clone(), up.clone()]);
      for (let j = 0; j <= R; j++) { const a = j / R * TAU, cs = Math.cos(a) * rr * th, sn = Math.sin(a) * rr; P.push(c.x + sd.x * cs + up.x * sn, c.y + sd.y * cs + up.y * sn, c.z + sd.z * cs + up.z * sn); } }
    for (let i = 0; i < N; i++) for (let j = 0; j < R; j++) { const a = i * (R + 1) + j, b = a + R + 1; I.push(a, b, a + 1, a + 1, b, b + 1); }
    const geo = new TH.BufferGeometry(); geo.setAttribute("position", new TH.Float32BufferAttribute(P, 3)); geo.setIndex(I); geo.computeVertexNormals(); const m = add(new TH.Mesh(geo, mat));
    if (o.teeth) for (let q = 1; q <= o.teeth; q++) { const fi = Math.round((.12 + .7 * q / (o.teeth + 1)) * N), [c, , u] = fr[fi]; cone(w * .55 * (1 - fi / N) + .04, rad[fi] * .35 + .012, o.tm || C.tip, c.clone().addScaledVector(u, rad[fi] * .7), u.clone().addScaledVector(pts[Math.min(N, fi + 1)].clone().sub(c).normalize(), .6)); }
    if (o.spine) for (let q = 1; q <= o.spine; q++) { const fi = Math.round((.1 + .55 * q / (o.spine + 1)) * N), [c, , u] = fr[fi]; cone(w * .5, rad[fi] * .3 + .01, C.tip, c.clone().addScaledVector(u, -rad[fi] * .7), u.clone().multiplyScalar(-1).addScaledVector(pts[Math.max(0, fi - 1)].clone().sub(c).normalize(), .5)); }
    return m; };
  /* a carapace: a flattened dome, pointed and narrowed toward the front, ridged across, with a gilded rim */
  const shell = (rx, ry, rz, o, x, y, z, mat) => { o = o || {}; const geo = new TH.SphereGeometry(1, 44, 26), P = geo.attributes.position;
    for (let i = 0; i < P.count; i++) { let px = P.getX(i), py = P.getY(i), pz = P.getZ(i); if (py < 0) py *= o.belly == null ? .35 : o.belly; const f = Math.max(0, px); px *= 1 + (o.point == null ? .14 : o.point) * f * f; pz *= 1 - (o.tri || 0) * f * f;
      py += (o.ridge == null ? .05 : o.ridge) * Math.cos(px * Math.PI * 3.2) * Math.max(0, py); if (o.keel) py += o.keel * Math.max(0, py) * Math.max(0, 1 - Math.abs(pz) * 2.2); pz *= 1 + .07 * Math.max(0, 1 - Math.abs(py) * 6); P.setXYZ(i, px * rx, py * ry, pz * rz); }
    geo.computeVertexNormals(); const m = add(new TH.Mesh(geo, mat || C.shell), x || 0, y || 0, z || 0);
    if (!o.norim && (!mat || mat === C.shell)) { const rim = add(new TH.Mesh(new TH.TorusGeometry(1, .035, 6, 56), C.tip), x || 0, (y || 0) + .01, z || 0); rim.rotation.x = Math.PI / 2; rim.scale.set(rx * 1.01, rz * 1.04 * (1 - (o.tri || 0) * .3), ry * 1.4); }
    return m; };
  const glowAt = (p, r0, r1) => { ell(r0, r0, r0, C.glow, p.x, p.y, p.z, 10); ell(r1, r1, r1, C.glowS, p.x, p.y, p.z, 10); };
  const coralTree = (base, h, spread, depth, mat, glowTip) => { const grow = (a, dir, len, d, rd) => { const b = a.clone().addScaledVector(dir.clone().normalize(), len); seg(a, b, rd, rd * .72, mat); ell(rd * .74, rd * .74, rd * .74, mat, b.x, b.y, b.z, 8);
      if (d <= 0) { if (glowTip) glowAt(b, rd * .9, rd * 2.4); return; } const nb = 2 + (r() < .35 ? 1 : 0); for (let i = 0; i < nb; i++) grow(b, dir.clone().normalize().add(V((r() - .5) * spread, .25 + r() * .3, (r() - .5) * spread)), len * (.62 + r() * .2), d - 1, rd * .72); };
    grow(base, V((r() - .5) * .3, 1, (r() - .5) * .3), h, depth, h * .12); };
  const crystal = (p, h, dir) => { const m = add(new TH.Mesh(new TH.ConeGeometry(h * .2, h, 6, 1), C.crys)); m.geometry.translate(0, h / 2, 0); m.position.copy(p); m.quaternion.setFromUnitVectors(V(0, 1, 0), dir.clone().normalize()); ell(h * .2, h * .2, h * .2, C.glowS, p.x + dir.x * h * .5, p.y + dir.y * h * .5, p.z + dir.z * h * .5, 8); return m; };
  const tower = (p, h, rd) => { seg(p, p.clone().add(V(0, h * .7, 0)), rd, rd * .7, C.tower); cone(h * .45, rd * .8, C.tip, p.clone().add(V(0, h * .65, 0)), V(0, 1, 0)); ell(rd * .45, rd * .3, rd * .45, C.glow, p.x, p.y + h * .45, p.z, 8); };
  /* ---------- the crabs ---------- */
  if (CRC_CRAB[k]) { const W = D.w * 1.25, L = D.l * 1.2, H = D.h * 1.25, kk = D.kk, th = D.th * 1.2;
    shell(L, H, W, { point: .22, ridge: .07, belly: .35, tri: .35, keel: .25 });
    for (let i = 0; i < 3; i++) { const p = shell(L * (.55 - i * .1), H * .3, W * (.85 - i * .2), { point: .4, ridge: 0, belly: .2, tri: .5, keel: .5 }, L * (.25 - i * .38), H * (.72 + i * .08), 0); p.rotation.z = -.2; } /* the gilded plates across the back */ shell(L * .9, .26, W * .86, { belly: 1, ridge: 0, norim: 1 }, 0, -.13, 0, C.under);
    /* the brow: a pointed rostrum and two hooked brow horns over cyan eyes; a fringe of fangs below them over the glowing core */
    cone(.45, .07, C.tip, V(L * 1.08, H * .18, 0), V(1, .25, 0), 0); for (const s of [1, -1]) { sickle(V(L * .86, H * .32, s * .3), V(1, .45, s * .5), V(0, -.2, -s), .45 + kk * .1, .07, C.claw, { curl: .45 }); ell(.09, .06, .07, C.eye, L * .93, H * .2, s * .24, 10); ell(.2, .14, .14, C.glowS, L * .95, H * .2, s * .25, 8); }
    for (let i = 0; i < D.fg; i++) { const s = i % 2 ? 1 : -1, j = Math.floor(i / 2), z = s * (.08 + j * .11 * 2.2 / Math.max(2, D.fg / 2)), len = (.42 + (j === 0 ? .2 : 0)) * (.8 + kk * .25); sickle(V(L * .9 - j * .04, -H * .08, z), V(.35, -1, s * .1), V(-1, 0, -s * .2), len, .05 + .015 * kk, C.claw, { curl: .5 }); }
    glowAt(V(L * .78, -H * .3, 0), .12 + kk * .04, .3 + kk * .08);
    /* the horns: crescents rising off the back of the shell, curling forward */
    for (let i = 0; i < D.hn; i++) for (const s of [1, -1]) { const t = i / Math.max(1, D.hn), x = -L * (.15 + .55 * t), z = s * W * (.45 + .3 * t); sickle(V(x, H * (.55 - .25 * t), z), V(-.35, 1, s * .45), V(1, 0, -s * .3), .8 + .5 * (1 - t) + H * .4, .11, C.claw, { curl: .5, spine: 2 }); }
    /* the legs: thick spiked segments, the last one a sickle curling under */
    const nl = 4; for (const s of [1, -1]) for (let i = 0; i < nl; i++) { const xi = .55 - i * .42 * L / 1.1, lean = (nl / 2 - .5 - i) * .22, R = W / 1.1, hip = V(xi, -.05, s * W * .72), knee = V(xi + lean * .6, H * .55, s * 1.2 * R), ank = V(xi + lean * 1.1, -H * .2, s * 1.6 * R);
      seg(hip, knee, .1 * th, .085 * th, C.shell); seg(knee, ank, .085 * th, .065 * th, C.shell); sickle(ank, V(lean * .3, -1, s * .3), V(lean >= 0 ? 1 : -1, 0, s * .15), (.55 + H * .15) * th, .07 * th, C.claw, { curl: .3, spine: 1 });
      for (const [a, b2] of [[hip, knee], [knee, ank]]) cone(.18 * th, .045 * th, C.tip, a.clone().lerp(b2, .55), V(.2, 1, s * .6), .05);
      for (const j of [knee, ank]) { ell(.1 * th, .1 * th, .1 * th, C.joint, j.x, j.y, j.z, 8); ell(.045 * th, .045 * th, .045 * th, C.glow, j.x, j.y - .06 * th, j.z, 6); } }
    /* the pincers: an armoured arm, a spiked palm, and two crescent fingers that close almost into a ring */
    for (const s of [1, -1]) { const q = 1.3 * kk * (s === 1 && (k === "cguard" || k === "cwar") ? 1.12 : 1), sh = V(.95, 0, s * W * .55), el = V(1.45, .35, s * W * .98), wr = V(1.95, .22, s * W * .8), pm = V(2.25 + .12 * (q - 1), .2, s * W * .72);
      seg(sh, el, .16 * q, .15 * q, C.shell); seg(el, wr, .15 * q, .18 * q, C.shell); ell(.16 * q, .16 * q, .16 * q, C.joint, el.x, el.y, el.z, 8); cone(.2 * q, .05 * q, C.tip, el, V(0, 1, s * .4), .05);
      const palm = ell(.55 * q, .4 * q, .3 * q, C.shell, pm.x, pm.y, pm.z, 20); palm.rotation.y = s * .12; for (let i = 0; i < 4; i++) cone(.14 * q, .04 * q, C.tip, V(pm.x + (-.2 + i * .14) * q, pm.y + .28 * q, pm.z), V(.25, 1, s * .25));
      const tipX = pm.x + .38 * q; sickle(V(tipX, pm.y + .12 * q, pm.z), V(1, .55, -s * .08), V(.15, -1, -s * .12), 1.25 * q, .14 * q, C.claw, { curl: .66, teeth: 5 }); /* the upper finger arches over */
      sickle(V(tipX - .05 * q, pm.y - .14 * q, pm.z), V(1, -.4, -s * .06), V(0, 1, -s * .1), 1.0 * q, .12 * q, C.claw, { curl: .55, teeth: 4 }); /* the lower finger curls up to meet it */
      ell(.07 * q, .05 * q, .05 * q, C.glow, pm.x - .1 * q, pm.y - .03 * q, pm.z + s * .22 * q, 8); }
    /* their own features, big and high on the back so they read from the side, as in the paintings */
    const TY = H * 1.02, back = (d, a) => V(Math.cos(a) * L * d - .25, TY - d * d * H * .6, Math.sin(a) * W * d * .75);
    if (D.spikes) for (let i = 0; i < D.spikes; i++) { const a = r() * TAU, el = .25 + r() * .9, p = V(Math.cos(a) * Math.cos(el) * L * .95, Math.sin(el) * H * 1.05, Math.sin(a) * Math.cos(el) * W * .85); cone(.3 + r() * .3, .07, C.tip, p, p.clone().normalize().add(V(0, .4, 0)), .04); }
    if (D.crest) for (let i = 0; i < D.crest; i++) { const x = L * (.3 - 1.1 * i / (D.crest - 1)), h = (1.1 + .7 * Math.sin(Math.PI * (i + .5) / D.crest)) * kk * .8; sickle(V(x, TY * .95, 0), V(-.35, 1, 0), V(-1, -.1, 0), h, .14, C.claw, { curl: .45, spine: 2 }); }
    if (D.coral) for (let i = 0; i < D.coral; i++) { const a = r() * TAU, d = Math.sqrt(r()) * .75; coralTree(back(d, a), .35 + r() * .35, .9, 2, i % 3 ? C.coral : C.coralB, i % 2 === 0); }
    if (D.crys) for (let i = 0; i < D.crys; i++) { const a = r() * TAU, d = Math.sqrt(r()) * .7; crystal(back(d, a), .7 + r() * .9, V((r() - .5) * .6 - .3, 1, (r() - .5) * .8)); }
    if (D.turret) { for (let i = 0; i < 5; i++) { const a = i / 5 * TAU; coralTree(V(-.15 + Math.cos(a) * .35, H * .8, Math.sin(a) * .35), .35 + r() * .15, .9, 2, i % 3 ? C.coral : C.coralB, true); }
      const bA = V(.1, H * .9, 0), bB = V(.95, H * .9 + .8, 0); seg(bA, bB, .17, .13, C.coralB); for (let i = 0; i < 3; i++) { const pp = bA.clone().lerp(bB, .25 + i * .25); ell(.2, .06, .2, C.tip, pp.x, pp.y, pp.z, 12).quaternion.setFromUnitVectors(V(0, 1, 0), bB.clone().sub(bA).normalize()); } glowAt(bB, .13, .34); }
    if (D.sacs) for (const s of [1, -1]) { ell(.55, .4, .42, C.sac, -.25, H * .95, s * .45, 20); for (let i = 0; i < 3; i++) { const b = ell(.57, .06, .44, C.shellD, -.25 + (i - 1) * .3, H * .95, s * .45, 14); b.scale.set(.1, .43, .45); } }
    if (D.abdo) { const ax = -L - .9, ay = H * .75, ab = ell(1.5, 1.05, 1.25, C.sac, ax, ay, 0, 28); for (let i = 0; i < 5; i++) { const b = ell(1, 1, 1, C.shell, ax + (i - 2) * .55, ay, 0, 24); b.scale.set(.1, 1.07 * Math.cos((i - 2) * .45), 1.27 * Math.cos((i - 2) * .45)); } ab.renderOrder = 1;
      for (let i = 0; i < 16; i++) { const a = r() * TAU, p = V(ax + (r() - .5) * 2, ay + Math.sin(a) * .8, Math.cos(a) * .95); ell(.2, .26, .2, C.egg, p.x, p.y, p.z, 12); } }
    if (D.pearls) { for (let i = 0; i < 11; i++) { const a = -Math.PI * .8 + i / 10 * Math.PI * 1.6; ell(.18, .18, .18, C.pearl, Math.cos(a) * L * .45 + .2, TY + .15, Math.sin(a) * W * .45, 14); cone(.5 + (i % 2) * .35, .06, C.tip, V(Math.cos(a) * L * .45 + .2, TY + .25, Math.sin(a) * W * .45), V(0, 1, 0)); } glowAt(V(.2, TY + .8, 0), .12, .35); ell(.35, .35, .35, C.pearl, .2, TY + .8, 0, 20); }
    if (D.tail) { for (let i = 0; i < 5; i++) { const x = -L - .25 - i * .42, s0 = 1 - i * .14; shell(.32, .38 * s0, .62 * s0, { ridge: 0, belly: .5 }, x, .05, 0); } for (const s of [-1, 0, 1]) { const f = ell(.45, .05, .2, C.shellD, -L - 2.45, .05, s * .25, 12); f.rotation.y = s * .5; } }
    if (D.ant) for (const s of [1, -1]) { const t = new TH.Mesh(new TH.TubeGeometry(new TH.CatmullRomCurve3([V(L, H * .25, s * .15), V(L + .8, H * .6, s * .3), V(L + .5, H + 1.3, s * .5), V(-.4, H + 1.9, s * .7)]), 24, .025, 5, false), C.tip); g.add(t); }
    if (D.eye3) { glowAt(V(L * .82, H * .62, 0), .16, .55); const hy = TY + 1.3; for (const [rr, a] of [[1.1, 0], [.8, .5]]) { const halo = add(new TH.Mesh(new TH.TorusGeometry(rr, .05, 8, 48), C.glow), -.1, hy, 0); halo.rotation.x = Math.PI / 2 + a; } ell(1.5, .1, 1.5, C.glowS, -.1, hy, 0, 20);
      ell(.32, .32, .32, C.core, -.1, hy, 0, 20); glowAt(V(-.1, hy, 0), .16, .8); for (let i = 0; i < 4; i++) { const a = i / 4 * TAU; sickle(V(-.1 + Math.cos(a) * .4, TY, Math.sin(a) * .4), V(Math.cos(a) * .3, 1, Math.sin(a) * .3), V(-Math.cos(a), 0, -Math.sin(a)), 1.3, .08, C.claw, { curl: .4 }); }
      for (let i = 0; i < 6; i++) { const z = (i - 2.5) * .2, t = new TH.Mesh(taperTube([[L * .6, -H * .1, z], [L * .95, -H * .7, z * 1.4], [L * .7, -H * 1.4, z * 1.8], [L * .9, -H * 2, z * 2]], u => .07 * (1 - u * .8), 20, 6), C.shell); g.add(t); } }
    if (D.crown) { for (let i = 0; i < 11; i++) { const a = -Math.PI * .8 + i / 10 * Math.PI * 1.6, p = V(Math.cos(a) * L * .45 + .1, TY, Math.sin(a) * W * .45), h = (i % 2 ? .8 : 1.5) * (i === 5 ? 1.5 : 1) * (k === "ccrown" || k === "ccrownm" ? 1.4 : 1); cone(h, .12, C.tip, p, V(Math.cos(a) * .25, 1, Math.sin(a) * .25), 0); }
      glowAt(V(L * .4 + .1, TY + .6, 0), .2, .7); const ring = add(new TH.Mesh(new TH.TorusGeometry(L * .48, .06, 6, 40), C.tip), .1, TY + .05, 0); ring.rotation.x = Math.PI / 2; ring.scale.set(1, W / L, 1); }
    if (D.city) for (let i = 0; i < 16; i++) { const a = r() * TAU, d = Math.sqrt(r()) * .65; tower(back(d, a), 1 + r() * 1.5, .1 + r() * .06); }
    if (D.tent) for (let i = 0; i < D.tent; i++) { const s = i % 2 ? 1 : -1, a = (i >> 1) / (D.tent / 2), base = V(-L * .2 - a * .9, H * .6, s * W * .6), pts = [base]; let p = base.clone(); for (let j = 1; j <= 6; j++) { p = p.clone().add(V(-.45 - r() * .2, .45 * Math.sin(j * .9 + i) + .35, s * (.3 + r() * .2))); pts.push(p); }
      const t = new TH.Mesh(taperTube(pts.map(v => [v.x, v.y, v.z]), u => .24 * (1 - u * .85), 34, 8), C.shell); g.add(t); for (let j = 1; j < 6; j++) ell(.06, .06, .06, C.glow, pts[j].x, pts[j].y - .14, pts[j].z, 6); }
    if (D.molt) { for (const s of [1, -1]) { const o2 = shell(L * .75, H * .6, W * .55, { ridge: .06, belly: 1, norim: 1 }, -L * .3, TY + .3, s * W * .55, C.shellD); o2.rotation.x = s * .7; o2.rotation.z = .3; }
      for (let i = 0; i < 10; i++) { const a = r() * TAU; const b = ell(.7, .035, .035, C.glow, Math.cos(a) * L * .55, TY * .9, Math.sin(a) * W * .55, 6); b.rotation.y = a; } glowAt(V(-.2, TY + .2, 0), .3, 1.2); } }
  /* ---------- the ships ---------- */
  else if (CRC_SHIP[k]) { const L = D.L * .92, W = D.w * 1.3, H = D.h * 1.8, n = D.n, F = D.f;
    C.blade = C.blade || C.shell.clone(); C.blade.color = new TH.Color(0x9a8aa8); C.blade.metalness = .7; C.blade.emissiveIntensity = .9;
    const plates = (len, h, w, x0, y0, z0, cnt, tilt) => { for (let i = 0; i < cnt; i++) { const t = cnt > 1 ? i / (cnt - 1) : 0, x = x0 + len * (.5 - t), sw = 1 - Math.pow(Math.abs(t - .35) * 1.3, 2) * .6; const p = shell(len / cnt * 1.6, h * .62 * sw, w * sw, { point: .4, ridge: 0, belly: .2, tri: .5, keel: .8 }, x, y0 + h * .45 * sw, z0); p.rotation.z = tilt == null ? -.2 : tilt; } };
    const hull = (l, h, w, x, y, z, o) => shell(l, h, w, Object.assign({ point: .28, ridge: 0, belly: .6, tri: .45, keel: .45, norim: 1 }, o || {}), x || 0, y || 0, z || 0, C.shellD);
    const drives = (xs, zs, sc) => { for (const zz of zs) { const s2 = sc || 1, nac = add(new TH.Mesh(new TH.CylinderGeometry(.16 * s2, .2 * s2, .7 * s2, 14), C.metal), xs, .05, zz); nac.rotation.z = Math.PI / 2;
      const ring = add(new TH.Mesh(new TH.TorusGeometry(.18 * s2, .03 * s2, 6, 20), C.tip), xs - .18 * s2, .05, zz); ring.rotation.y = Math.PI / 2; ell(.06 * s2, .15 * s2, .15 * s2, C.glow, xs - .33 * s2, .05, zz, 12); ell(.3 * s2, .26 * s2, .26 * s2, C.glowS, xs - .43 * s2, .05, zz, 10); } };
    const eye = (x, y, z, r0) => { glowAt(V(x, y, z), r0, r0 * 3.4); const rg = add(new TH.Mesh(new TH.TorusGeometry(r0 * 1.5, r0 * .3, 8, 24), C.tip), x, y, z); rg.lookAt(x, y, z + 1); };
    const hooks = (cnt, x0, x1, y, z, len) => { for (let i = 0; i < cnt; i++) for (const s of [1, -1]) { const x = x0 + (x1 - x0) * i / Math.max(1, cnt - 1); sickle(V(x, y, s * z), V(.5, -1, s * .45), V(1, .15, -s * .1), len, .08, i % 2 ? C.blade : C.claw, { curl: .65 }); } };
    const fins = (cnt, x0, x1, y, z, len) => { for (let i = 0; i < cnt; i++) for (const s of [1, -1]) { const x = x0 + (x1 - x0) * i / Math.max(1, cnt - 1); sickle(V(x, y, s * z), V(-.8, 1, s * .5), V(-1, -.3, 0), len * (.7 + .3 * Math.sin(Math.PI * (i + .5) / cnt)), .1, C.blade, { curl: .5, spine: 1 }); } };
    const pincer = (base, dir, sc, s) => { const p = ell(.28 * sc, .2 * sc, .18 * sc, C.shell, base.x, base.y, base.z, 14); sickle(base.clone().add(V(.15 * sc, .08 * sc, 0)), dir.clone().add(V(0, .5, 0)), V(.1, -1, -s * .2), .75 * sc, .09 * sc, C.claw, { curl: .65, teeth: 3 }); sickle(base.clone().add(V(.12 * sc, -.08 * sc, 0)), dir.clone().add(V(0, -.4, 0)), V(0, 1, -s * .1), .6 * sc, .08 * sc, C.claw, { curl: .55, teeth: 2 }); return p; };
    if (F === "beetle") { /* the Scuttle Frigate: a short, high beetle hull; two great claws hooking down off the brow, mandibles beneath */
      hull(L * .85, H * 1.1, W * 1.05, 0, 0, 0, { point: .3, tri: .3, keel: .6 }); plates(L * 1.4, H * .5, W * 1.05, -.1, H * .3, 0, n);
      for (const s of [1, -1]) { sickle(V(L * .55, H * .35, s * W * .6), V(1, .25, s * .2), V(.1, -1, -s * .35), L * .95, .2, C.blade, { curl: .75, teeth: 4, spine: 2 }); sickle(V(L * .6, -H * .3, s * W * .25), V(1, -.4, s * .1), V(0, 1, -s * .3), L * .5, .09, C.claw, { curl: .6, teeth: 2 }); }
      hooks(3, L * .2, -L * .5, -H * .45, W * .55, .6); fins(2, -L * .1, -L * .6, H * .9, W * .35, .8); eye(L * .45, H * .1, W * .95, .09); eye(L * .45, H * .1, -W * .95, .09); drives(-L * .9, [-W * .4, W * .4], 1.1); }
    else if (F === "fork") { /* the Tidal Interceptor: a slim fuselage with two long arms thrust forward, each ending in an open pincer */
      hull(L * .9, H * .45, W * .45, 0, 0, 0, { point: .7, tri: .7 }); plates(L * 1.3, H * .3, W * .5, -.2, H * .05, 0, n);
      for (const s of [1, -1]) { const a = V(L * .1, 0, s * W * .4), e2 = V(L * .55, 0, s * W * 1.05), f2 = V(L * 1.05, .02, s * W * .85); seg(a, e2, .09, .08, C.shell); seg(e2, f2, .08, .07, C.shell); ell(.1, .1, .1, C.joint, e2.x, e2.y, e2.z, 8); pincer(f2, V(1, 0, -s * .15), 1.05, s);
        const wg = shell(L * .35, .08, W * .9, { point: .2, ridge: 0, belly: 1, tri: .6 }, -L * .45, 0, s * W * .9); wg.rotation.y = s * .55; }
      fins(1, -L * .3, -L * .3, H * .4, W * .2, .9); drives(-L * .95, [-W * .3, W * .3], .9); eye(L * .5, H * .1, W * .45, .06); eye(L * .5, H * .1, -W * .45, .06); }
    else if (F === "trident") { /* the Reef Guard Destroyer: a long spine-ship; a trident of blades at the prow, coral growing along the back */
      hull(L, H * .8, W * .7); plates(L * 1.5, H * .4, W * .75, -.05, H * .15, 0, n);
      cone(L * .9, .12, C.claw, V(L * 1.05, 0, 0), V(1, 0, 0), 0); for (const s of [1, -1]) sickle(V(L * .85, 0, s * W * .45), V(1, s * .35, s * .45), V(0, -s * .6, -s), L * .9, .15, C.blade, { curl: .5, teeth: 3 });
      for (let i = 0; i < 5; i++) coralTree(V(L * (.3 - .25 * i), H * .7, (r() - .5) * W * .3), .22, .8, 1, i % 2 ? C.coral : C.coralB, true);
      hooks(4, L * .3, -L * .6, -H * .35, W * .5, .55); drives(-L * .95, [-W * .35, W * .35]); eye(L * .4, 0, W * .72, .08); eye(L * .4, 0, -W * .72, .08); }
    else if (F === "manta") { /* the Abyssal Vanguard: an arrowhead hull with two great claw-wings swept back, their tips hooking forward */
      hull(L * .95, H * .75, W * .7); plates(L * 1.4, H * .4, W * .75, 0, H * .15, 0, n);
      for (const s of [1, -1]) { const wg = shell(L * .7, .12, W * 1.3, { point: .5, ridge: 0, belly: 1, tri: .4 }, -L * .2, -H * .05, s * W * 1.05); wg.rotation.y = s * .5; sickle(V(L * .05, -H * .05, s * W * 2.1), V(1, 0, -s * .1), V(0, -.2, -s), L * .8, .14, C.blade, { curl: .55, teeth: 3 }); sickle(V(-L * .75, 0, s * W * 1.6), V(-1, .3, s * .4), V(1, 0, 0), L * .45, .09, C.claw, { curl: .5 }); }
      for (const s of [1, -1]) sickle(V(L * .85, H * .1, s * W * .4), V(1, s * .3, s * .2), V(0, -s * .6, -s * .5), L * .6, .12, C.claw, { curl: .55, teeth: 2 }); drives(-L * .95, [-W * .35, W * .35]); eye(L * .35, H * .15, 0, .11); }
    else if (F === "pod") { /* the Brood Warden Carrier: a fat oval hull; rows of glowing eggs down both flanks, a fringe of little hooks below */
      hull(L * .9, H * 1.05, W * 1.2, 0, 0, 0, { point: .2, tri: .2, keel: .3 }); plates(L * 1.4, H * .45, W * 1.15, -.1, H * .45, 0, n);
      for (const s of [1, -1]) for (let i = 0; i < D.eggs; i++) { const x = L * (.4 - 1 * i / (D.eggs - 1)); ell(.2, .24, .17, C.egg, x, H * .05, s * W * 1.12, 12); ell(.36, .36, .24, C.glowS, x, H * .05, s * W * 1.18, 8); ell(.2, .04, .2, C.tip, x, H * .3, s * W * 1.1, 8); }
      for (const s of [1, -1]) sickle(V(L * .85, 0, s * W * .4), V(1, s * .3, s * .2), V(0, -s * .7, -s * .5), L * .5, .12, C.claw, { curl: .6, teeth: 2 }); hooks(D.hk, L * .4, -L * .6, -H * .4, W * .7, .45); drives(-L * .95, [-W * .5, 0, W * .5]); }
    else if (F === "needle") { /* the Pearl Hunter: a long pale needle with two thin pincer prongs and a fan of tail fins */
      hull(L * 1.05, H * .4, W * .38, 0, 0, 0, { point: .6, tri: .8 }); plates(L * 1.2, H * .25, W * .4, -.1, H * .05, 0, n);
      for (const s of [1, -1]) sickle(V(L * .9, s * H * .2, s * W * .2), V(1, s * .4, s * .1), V(0, -s, -s * .2), L * .95, .1, C.claw, { curl: .5, teeth: 3 });
      for (let i = 0; i < 3; i++) { const a = (i - 1) * .9; sickle(V(-L * .7, 0, 0), V(-1, Math.cos(a) * .8, Math.sin(a) * .8), V(-1, 0, 0), .7, .08, C.blade, { curl: .3 }); } drives(-L * 1.0, [-W * .25, W * .25], .8); eye(L * .45, H * .1, 0, .07); }
    else if (F === "twin") { /* the Molting Interceptor: two slim hulls split like a molting shell, joined by a bridge, violet light in the cracks */
      for (const s of [1, -1]) { hull(L * .85, H * .45, W * .32, 0, 0, s * W * .55, { point: .7, tri: .6 }); plates(L * 1.1, H * .28, W * .32, -.1, H * .05, s * W * .55, n); for (const u of [1, -1]) sickle(V(L * .8, u * H * .15, s * W * .55), V(1, u * .4, 0), V(0, -u, 0), L * .7, .1, C.claw, { curl: .55, teeth: 2 }); }
      const br = add(new TH.Mesh(new TH.BoxGeometry(L * .5, .08, W * 1.1), C.shellD), 0, 0, 0); for (let i = 0; i < 4; i++) ell(L * .2, .02, .02, C.glow, L * (.3 - .2 * i), H * .3, (i % 2 ? 1 : -1) * W * .55, 6); drives(-L * .9, [-W * .55, W * .55], .85); eye(L * .2, H * .05, 0, .09); }
    else if (F === "regent") { /* the Tidal Regent: a long flagship; crescents fore and aft, a great cyan eye amidships, a crest of spines */
      hull(L, H * .85, W * .8); plates(L * 1.5, H * .45, W * .85, 0, H * .2, 0, n);
      for (let q = 0; q < 2; q++) for (const s of [1, -1]) sickle(V(L * (.8 - q * .2), H * (-.05 + q * .45), s * W * (.6 - q * .12)), V(1, .15 + q * .3, s * (.25 + q * .1)), V(-.1, -.8, -s * .5), L * (1.05 - q * .2), .2 - q * .04, C.blade, { curl: .65, teeth: 4, spine: 1 });
      for (const s of [1, -1]) sickle(V(-L * .6, H * .2, s * W * .5), V(-1, .2, s * .4), V(1, .2, 0), L * .55, .12, C.blade, { curl: .55 });
      eye(L * .05, H * 1.05, 0, .2); for (let i = 0; i < 7; i++) cone(.35 + .3 * Math.sin(i / 6 * Math.PI), .07, C.tip, V(L * (.45 - .17 * i), H * 1, 0), V(-.5, 1, 0), -.1);
      hooks(4, L * .3, -L * .55, -H * .4, W * .55, .7); drives(-L * .95, [-W * .4, W * .4], 1.2); }
    else if (F === "crown") { /* the Emperor's Shell: a wide golden hull crowned with spires; double crescents and a ring of blades */
      hull(L * .95, H * .95, W * 1.05, 0, 0, 0, { point: .4, tri: .4 }); plates(L * 1.5, H * .5, W * 1.05, 0, H * .3, 0, n);
      for (let q = 0; q < 2; q++) for (const s of [1, -1]) sickle(V(L * (.8 - q * .15), H * (q * .5), s * W * (.7 - q * .15)), V(1, .2 + q * .3, s * (.3 + q * .1)), V(-.1, -.85, -s * .5), L * (1.1 - q * .15), .22 - q * .04, C.claw, { curl: .7, teeth: 5, spine: 2 });
      for (let i = 0; i < 9; i++) { const a = -Math.PI * .8 + i / 8 * Math.PI * 1.6, h = (i % 2 ? .45 : .8) * (i === 4 ? 1.5 : 1); cone(h, .08, C.tip, V(Math.cos(a) * L * .3, H * 1.05, Math.sin(a) * W * .45), V(Math.cos(a) * .3, 1, Math.sin(a) * .3)); } eye(L * .05, H * 1.3, 0, .14);
      for (let i = 0; i < 5; i++) for (const s of [1, -1]) sickle(V(L * (.3 - .25 * i), 0, s * W * 1.0), V(.2, -.2, s), V(1, 0, 0), .6, .09, C.claw, { curl: .5 }); hooks(5, L * .3, -L * .6, -H * .4, W * .6, .6); drives(-L * .95, [-W * .5, 0, W * .5], 1.2); }
    else if (F === "hump") { /* the Broodlord Carrier: a tall humped back carrying a great brood sac, pink coral, hooked legs beneath */
      hull(L * .95, H * .8, W * .9); const sac = ell(L * .55, H * 1.1, W * .75, C.sac, -L * .15, H * .9, 0, 24); for (let i = 0; i < 4; i++) { const b2 = ell(L * .56, H * 1.12, W * .76, C.shell, -L * .15, H * .9, 0, 20); b2.scale.set(.06, H * 1.12, W * .76); b2.position.x = -L * .15 + (i - 1.5) * L * .25; }
      for (let i = 0; i < 9; i++) ell(.15, .18, .15, C.egg, -L * .15 + (r() - .5) * L * .7, H * (.6 + r() * .8), (r() - .5) * W * .9, 10);
      for (let i = 0; i < 5; i++) coralTree(V(L * (.4 - .15 * i), H * .5, (r() - .5) * W * .5), .2, .8, 1, C.coral, true); for (const s of [1, -1]) sickle(V(L * .85, 0, s * W * .4), V(1, s * .3, s * .2), V(0, -s * .7, -s * .5), L * .7, .14, C.blade, { curl: .6, teeth: 3 });
      hooks(D.hk, L * .4, -L * .6, -H * .35, W * .6, .6); drives(-L * .95, [-W * .45, 0, W * .45]); }
    for (const s of [1, -1]) ell(L * .55, .02, .02, C.glow, -.1, -H * .1, s * W * (F === "pod" ? 1.2 : F === "manta" ? .75 : F === "fork" || F === "needle" ? .45 : F === "twin" ? 0 : .8), 6); }
  /* ---------- the wild Kraken: a long mantle trailing behind, a ring of eyes, arms reaching forward ---------- */
  else if (k === "ckrak") { const C2 = crcMats("krak"), M = new TH.Mesh(new TH.LatheGeometry([[0, 0], [.55, .2], [.8, .9], [.75, 1.8], [.5, 2.8], [.18, 3.5], [0, 3.7]].map(([rr, y]) => new TH.Vector2(rr, y)), 24), C2.shell);
    M.rotation.z = Math.PI / 2; M.position.set(.2, .1, 0); M.scale.set(1, 1, .9); g.add(M); for (const s of [1, -1]) { const f = ell(.9, .05, .55, C2.shellD, -2.6, .1, s * .45, 14); f.rotation.y = s * .6; }
    for (const s of [1, -1]) { glowAt(V(.35, .35, s * .62), .14, .4); ell(.09, .09, .05, C2.joint, .42, .35, s * .66, 8); }
    for (let i = 0; i < 8; i++) { const a = i / 8 * TAU, by = Math.sin(a) * .45, bz = Math.cos(a) * .45, pts = [[.4, by, bz]]; let px = .4, py = by, pz = bz;
      for (let j = 1; j <= 6; j++) { px += .55 + r() * .15; py += Math.sin(a) * .2 + Math.sin(j * 1.3 + i) * .3; pz += Math.cos(a) * .25 + Math.cos(j * 1.1 + i) * .25; pts.push([px, py, pz]); }
      g.add(new TH.Mesh(taperTube(pts, u => .2 * (1 - u * .85), 36, 8), C2.shell)); for (let j = 1; j < 6; j++) ell(.045, .045, .045, C2.glow, pts[j][0], pts[j][1] - .12, pts[j][2], 6); }
    for (let i = 0; i < 10; i++) { const a = r() * TAU; ell(.06, .06, .06, C2.glow, -.5 - r() * 2.4, Math.sin(a) * .6, Math.cos(a) * .55, 6); } }
  /* ---------- the Breach nest: a rift into the Abyss in a mound of rock, ringed by crescent spires, choked with coral and eggs ---------- */
  else if (k === "cnest") {
    const base = add(new TH.Mesh(new TH.DodecahedronGeometry(3, 1), C.rock), 0, -1.55, 0); base.scale.set(1, .32, .85);
    for (let i = 0; i < 9; i++) { const a = r() * TAU, d = 1.6 + r() * 1.3, b = add(new TH.Mesh(new TH.DodecahedronGeometry(.35 + r() * .35, 0), C.rock), Math.cos(a) * d, -1.05, Math.sin(a) * d * .85); b.rotation.set(r() * 3, r() * 3, r() * 3); }
    for (let i = 0; i < 9; i++) { const a = i / 9 * TAU + .2, p = V(Math.cos(a) * 2.35, -1.1, Math.sin(a) * 2.0), in2 = V(-Math.cos(a), 0, -Math.sin(a)); sickle(p, V(0, 1, 0).addScaledVector(in2, .15), in2, 3.4 + r() * 1.2, .26, i % 2 ? C.shell : C.claw, { curl: .35, spine: 2 }); }
    const ring = add(new TH.Mesh(new TH.TorusGeometry(1.15, .2, 10, 36), C.claw), 0, 1.1, 0); ring.scale.set(1, 1.35, 1);
    for (let i = 0; i < 12; i++) { const a = i / 12 * TAU; cone(.42, .08, C.tip, V(Math.cos(a) * 1.25, 1.1 + Math.sin(a) * 1.6, 0), V(Math.cos(a), Math.sin(a) * 1.3, 0)); }
    const hole = add(new TH.Mesh(new TH.CircleGeometry(1.02, 36), C.void), 0, 1.1, 0); hole.scale.set(1, 1.35, 1);
    const core = ell(.55, .75, .2, C.core, 0, 1.1, 0, 20); ell(1.0, 1.35, .5, C.glowS, 0, 1.1, 0, 18); ell(1.5, 1.9, .9, C.glowS, 0, 1.1, 0, 14); core.renderOrder = 2;
    for (let i = 0; i < 14; i++) { const a = r() * TAU, d = .9 + r() * 1.7; coralTree(V(Math.cos(a) * d, -1.0, Math.sin(a) * d * .85), .45 + r() * .45, 1, 2, i % 3 ? C.coral : C.coralB, i % 2 === 0); }
    for (let i = 0; i < 26; i++) { const a = r() * TAU, d = .6 + r() * 1.8, s = .14 + r() * .16; ell(s, s * 1.15, s, C.egg, Math.cos(a) * d, -.95 + s * .6, Math.sin(a) * d * .85, 12); } }
  else if (k === "clevd") { /* v706 the Leviathan, slain at the wall and dragged into the Breach: its own body gone dark, cyan rot in the wounds, gilded Carcinid chains and a war-saddle on its back */
    const m = buildMonster("slevi"); m.traverse(o => { if (!o.isMesh || !o.material || Array.isArray(o.material)) return; const mt = o.material.clone(); if (mt.color) mt.color.multiplyScalar(.6).lerp(new TH.Color(0x6a5a8a), .25); if (mt.emissive) { mt.emissive.setHex(0x2fd8e0); mt.emissiveIntensity = Math.max(.35, (mt.emissiveIntensity || 0) * .8); } o.material = mt; }); g.add(m);
    const bb = new TH.Box3().setFromObject(m), sz = bb.getSize(new TH.Vector3()), c = bb.getCenter(new TH.Vector3()), R = Math.min(sz.y, sz.z) * .55;
    for (let i = 0; i < 4; i++) { const x = bb.min.x + sz.x * (.3 + i * .12), ring = add(new TH.Mesh(new TH.TorusGeometry(R, R * .09, 8, 28), C.tip), x, c.y, c.z); ring.rotation.y = Math.PI / 2; }
    for (let i = 0; i < 3; i++) { const x = bb.min.x + sz.x * (.3 + i * .12); seg(V(x, c.y + R, c.z), V(x + sz.x * .12, c.y + R, c.z), R * .05, R * .05, C.tip); }
    const sx = bb.min.x + sz.x * .62, sy = bb.max.y; shell(.9, .35, .6, { point: .3, ridge: .05 }, sx, sy + .1, c.z); for (let i = 0; i < 5; i++) cone(.6 + (i % 2) * .3, .06, C.tip, V(sx - .4 + i * .2, sy + .35, c.z), V(-.2, 1, 0));
    for (let i = 0; i < 8; i++) glowAt(V(bb.min.x + sz.x * r(), c.y + (r() - .3) * sz.y * .6, c.z + (r() - .5) * sz.z * .5), .08, .3); }
  else if (k === "cpat") { /* a scout patrol on the map: a frigate with two interceptors on its wings */
    const f = buildCarc("cfrig"); g.add(f); for (const s of [1, -1]) { const c = buildCarc("cint"); c.scale.setScalar(.72); c.position.set(-1.4, .35, s * 2.3); g.add(c); } }
  return g; }
/* ---------- v704 the Carcinid fight with their own moves (owner: "multiple unique attack animations and reactive shielding") ----------
   Every Carcinid unit has two signature attacks that alternate volley by volley, drawn on the battlefield in time with its real shots:
   - Pincer Lance: the prow blades charge and two curved beams close on the target like a pair of pincers, crossing in a flash;
   - Spine Volley: a fan of gilded spines arcs out and stitches across the target;
   - Tidal Pulse: a ring of abyssal water rolls out from the shooter and breaks over the target, its shields flickering;
   - Brood Launch: glowing eggs are flung out, crack, and the brood streaks in on the target in a swarm of sparks;
   - Claw Crush: the ghost of a giant crescent pincer snaps shut on the target, with a shockwave;
   - Coral Mortar: glowing coral is lobbed in high arcs and bursts in violet spore-clouds;
   - Abyssal Beam: an eye charges and a thick cyan-gold beam tears across the field.
   Reactive shielding: when a Carcinid unit is hit while its shields hold, a hexagonal carapace-shield lights where the shot lands (cyan
   plates with gilded seams, rippling out from the impact, brighter the more shield is left); once the shields are gone, the shell sparks
   gold instead. Pictures only; the fight itself is unchanged. */
const CRC_ATK = { clevd: ["beam", "crush"], cfrig: ["lance", "mortar"], cint: ["spines", "lance"], cdest: ["mortar", "spines"], cvang: ["lance", "pulse"], ccarr: ["brood", "spines"], cpearl: ["spines", "pulse"], cmint: ["pulse", "spines"], cregent: ["beam", "lance"],
  cempr: ["beam", "crush"], cbrlord: ["brood", "mortar"], cscut: ["spines", "crush"], cspit: ["mortar", "spines"], charv: ["pulse", "spines"], cguard: ["crush", "pulse"], cbrood: ["brood", "mortar"], cwar: ["crush", "lance"], ccrys: ["pulse", "spines"],
  clanc: ["lance", "crush"], cmolt: ["crush", "beam"], ckrak: ["pulse", "crush"], cnest: ["brood", "mortar"], cmar: ["crush", "lance"], cmat: ["brood", "pulse"], ctyr: ["mortar", "crush"], cora: ["pulse", "beam"], ckor: ["beam", "crush"],
  cbeh: ["crush", "mortar"], ckbr: ["crush", "pulse"], cpal: ["pulse", "beam"], ccrown: ["beam", "brood"], ccrownm: ["beam", "crush"] };
const CRC_ADUR = { lance: 1.1, spines: .9, pulse: 1.2, brood: 1.5, crush: 1, mortar: 1.3, beam: 1.4 };
function crcAtkAdd(b, v) { const q = b.Q[v.s]; if (!q || v.e == null || v.e < 0) return; const ks = CRC_ATK[q.k]; if (!ks) return; const L = b.cAtk || (b.cAtk = []), last = b.cAtkT || (b.cAtkT = {}), cnt = b.cAtkN || (b.cAtkN = {});
  if (last[v.s] != null && v.t - last[v.s] < 1.3) return; last[v.s] = v.t; const a = ks[(cnt[v.s] = (cnt[v.s] || 0) + 1) % 2]; L.push({ s: v.s, e: v.e, t0: v.t, a, seed: (v.s * 7 + L.length) % 13 }); if (L.length > 28) L.shift(); }
function crcShAdd(b, v) { const e = b.Q[v.e]; if (!e || !CRC_ATK[e.k]) return; const H = b.cSh || (b.cSh = []), lt = b.cShT || (b.cShT = {}); if (lt[v.e] != null && v.t - lt[v.e] < .35) return; lt[v.e] = v.t; H.push({ e: v.e, s: v.s, t0: v.t + .32, seed: H.length % 9 }); if (H.length > 30) H.shift(); }
const crcRGB = q => BOSS_GLOW[q.k] || (CRC_SHIP[q.k] && CRC_SHIP[q.k].t === "oracle" ? "190,120,255" : CRC_SHIP[q.k] && CRC_SHIP[q.k].t === "krak" ? "220,90,255" : "63,232,240");
function crcAtkDraw(ctx, b, scr, T, W, d, lo, t) { const A = b.cAtk, Hh = b.cSh; if ((!A || !A.length) && (!Hh || !Hh.length)) return; ctx.save(); ctx.lineCap = "round"; ctx.globalCompositeOperation = "lighter";
  const gold = "255,200,112";
  for (const m of A || []) { const D = CRC_ADUR[m.a], u = (T - m.t0) / D; if (u < 0 || u > 1) continue; const S0 = scr[m.s], E0 = scr[m.e]; if (!S0 || !E0) continue; const q = b.Q[m.s], g = b.geo && b.geo[m.s], Lg = g ? g.L : 40, col = crcRGB(q), C = a => `rgba(${col},${a})`, G = a => `rgba(${gold},${a})`, gl = glowSprite(C(1)), dir = Math.sign(E0.x - S0.x) || 1;
    const fx = S0.x + dir * Lg * .45, fy = S0.y, dx = E0.x - fx, dy = E0.y - fy, dl = Math.hypot(dx, dy) || 1, nx = -dy / dl, ny = dx / dl, fade = Math.min(1, u / .08, (1 - u) / .15);
    if (!m.snd) { m.snd = 1; try { mimSfx(m.a === "crush" ? "slam" : m.a === "mortar" || m.a === "brood" ? "hiss" : "hum", clamp(S0.x / W * 2 - 1, -1, 1)); } catch (e) {} }
    if (m.a === "lance") { const ch = Math.min(1, u / .35); ctx.globalAlpha = fade * ch; for (const s of [1, -1]) ctx.drawImage(gl, fx - Lg * .2, fy + s * Lg * .18 - Lg * .2, Lg * .4, Lg * .4);
      if (u > .35) { const k = Math.min(1, (u - .35) / .25); for (const s of [1, -1]) { const bx = fx, by = fy + s * Lg * .18, cx = fx + dx * .5 + nx * s * dl * .28, cy = fy + dy * .5 + ny * s * dl * .28, ex = E0.x, ey = E0.y;
        ctx.beginPath(); ctx.moveTo(bx, by); const steps = 16; for (let i = 1; i <= steps * k; i++) { const tt = i / steps, x = (1 - tt) * (1 - tt) * bx + 2 * (1 - tt) * tt * cx + tt * tt * ex, y = (1 - tt) * (1 - tt) * by + 2 * (1 - tt) * tt * cy + tt * tt * ey; ctx.lineTo(x, y); }
        ctx.globalAlpha = fade * .3; ctx.strokeStyle = C(1); ctx.lineWidth = 9 * d; ctx.stroke(); ctx.globalAlpha = fade; ctx.lineWidth = 2.6 * d; ctx.strokeStyle = "#fff"; ctx.stroke(); }
        if (k >= 1) { const r = Lg * (.5 + (u - .6) * 2); ctx.globalAlpha = fade; ctx.drawImage(gl, E0.x - r, E0.y - r, r * 2, r * 2); ctx.strokeStyle = G(1); ctx.lineWidth = 2 * d; ctx.beginPath(); ctx.moveTo(E0.x - r * .5, E0.y - r * .5); ctx.lineTo(E0.x + r * .5, E0.y + r * .5); ctx.moveTo(E0.x - r * .5, E0.y + r * .5); ctx.lineTo(E0.x + r * .5, E0.y - r * .5); ctx.stroke(); } } }
    else if (m.a === "spines") { const n = lo ? 5 : 9; for (let i = 0; i < n; i++) { const off = (i - (n - 1) / 2) / n, st = i * .025, k = clamp((u - st) / .55, 0, 1); if (k <= 0) continue; const arc = Math.sin(Math.PI * k) * dl * .22 * off * 2, x = fx + dx * k + nx * arc, y = fy + dy * k + ny * arc + E0.y * 0;
        const k2 = Math.max(0, k - .08), x2 = fx + dx * k2 + nx * Math.sin(Math.PI * k2) * dl * .22 * off * 2, y2 = fy + dy * k2 + ny * Math.sin(Math.PI * k2) * dl * .22 * off * 2; ctx.globalAlpha = fade * (k < 1 ? 1 : 0); ctx.strokeStyle = G(1); ctx.lineWidth = 2.2 * d; ctx.beginPath(); ctx.moveTo(x2, y2); ctx.lineTo(x, y); ctx.stroke();
        if (k >= 1 && u - st < .75) { const r = Lg * .18; ctx.globalAlpha = fade * .9; ctx.drawImage(glowSprite(G(1)), E0.x + off * Lg * .8 - r, E0.y + Math.sin(i * 2.3) * Lg * .25 - r, r * 2, r * 2); } } }
    else if (m.a === "pulse") { const k = u, r = dl * k * 1.05; ctx.globalAlpha = fade * (1 - k * .6); ctx.strokeStyle = C(1); for (let i = 0; i < 3; i++) { const rr = r - i * Lg * .25; if (rr <= 0) continue; ctx.lineWidth = (5 - i * 1.4) * d; ctx.beginPath(); ctx.ellipse(fx, fy, rr, rr * .5, Math.atan2(dy, dx), -.6, .6); ctx.stroke(); }
      if (k > .75) { const r2 = Lg * (.5 + (k - .75) * 3); ctx.globalAlpha = fade; ctx.drawImage(gl, E0.x - r2, E0.y - r2, r2 * 2, r2 * 2); } }
    else if (m.a === "brood") { const n = lo ? 4 : 7; for (let i = 0; i < n; i++) { const st = i * .04, k = clamp((u - st) / .8, 0, 1); if (k <= 0 || k >= 1) continue; const lob = k < .3 ? k / .3 : 1, ex = fx + nx * (i - n / 2) * Lg * .25 * lob, ey = fy + ny * (i - n / 2) * Lg * .25 * lob - Lg * .4 * lob;
        if (k < .3) { ctx.globalAlpha = fade; ctx.fillStyle = C(.9); ctx.beginPath(); ctx.ellipse(ex, ey, 4 * d, 5 * d, 0, 0, TAU); ctx.fill(); }
        else { const kk = (k - .3) / .7, x = ex + (E0.x - ex) * kk + Math.sin(kk * 12 + i) * Lg * .1 * (1 - kk), y = ey + (E0.y - ey) * kk + Math.cos(kk * 10 + i) * Lg * .1 * (1 - kk); ctx.globalAlpha = fade; ctx.drawImage(gl, x - 6 * d, y - 6 * d, 12 * d, 12 * d); ctx.fillStyle = "#fff"; ctx.fillRect(x - 1.2 * d, y - 1.2 * d, 2.4 * d, 2.4 * d);
          if (kk > .92) { const r = Lg * .3; ctx.drawImage(gl, E0.x - r + (i - n / 2) * 3 * d, E0.y - r, r * 2, r * 2); } } } }
    else if (m.a === "crush") { const k = u, r = Lg * 1.1, o = k < .45 ? .9 - k / .45 * .75 : .15, ang = Math.atan2(-dy, -dx); ctx.globalAlpha = fade * .85; ctx.strokeStyle = G(1); ctx.lineWidth = 6 * d;
      for (const s of [1, -1]) { ctx.beginPath(); ctx.arc(E0.x, E0.y, r * .6, ang + s * (Math.PI * .15 + o), ang + s * (Math.PI * .95), s < 0); ctx.stroke(); }
      ctx.strokeStyle = C(1); ctx.lineWidth = 2 * d; for (const s of [1, -1]) { ctx.beginPath(); ctx.arc(E0.x, E0.y, r * .48, ang + s * (Math.PI * .2 + o), ang + s * (Math.PI * .9), s < 0); ctx.stroke(); }
      if (k > .45) { const kk = (k - .45) / .55, rr = r * (.3 + kk); ctx.globalAlpha = fade * (1 - kk); ctx.strokeStyle = G(1); ctx.lineWidth = (5 - 4 * kk) * d; ctx.beginPath(); ctx.ellipse(E0.x, E0.y, rr, rr * .5, 0, 0, TAU); ctx.stroke(); if (!m.hit) { m.hit = 1; b.shake = Math.max(b.shake || 0, 8 * d); } } }
    else if (m.a === "mortar") { const n = lo ? 2 : 4; for (let i = 0; i < n; i++) { const st = i * .08, k = clamp((u - st) / .7, 0, 1); if (k <= 0) continue; const tx = E0.x + (i - n / 2) * Lg * .22, ty = E0.y + Math.sin(i * 3) * Lg * .15;
        if (k < 1) { const x = fx + (tx - fx) * k, y = fy + (ty - fy) * k - Math.sin(Math.PI * k) * Math.max(Lg * 1.5, dl * .35); ctx.globalAlpha = fade; ctx.drawImage(glowSprite("rgba(255,122,176,1)"), x - 7 * d, y - 7 * d, 14 * d, 14 * d); ctx.fillStyle = "#ffd0e8"; ctx.beginPath(); ctx.arc(x, y, 2.4 * d, 0, TAU); ctx.fill(); }
        else if (u - st < .95) { const kk = (u - st - .7) / .25, r = Lg * (.25 + kk * .5); ctx.globalAlpha = fade * (1 - kk); ctx.drawImage(glowSprite("rgba(180,140,255,1)"), tx - r, ty - r, r * 2, r * 2); } } }
    else if (m.a === "beam") { const ch = Math.min(1, u / .4), ex0 = fx, ey0 = fy - Lg * .05; ctx.globalAlpha = fade * ch; const cr = Lg * (.15 + .25 * ch); ctx.drawImage(gl, ex0 - cr, ey0 - cr, cr * 2, cr * 2);
      if (u > .4) { const k = Math.min(1, (u - .4) / .12), x1 = ex0 + dx * 1.15 * k, y1 = ey0 + dy * 1.15 * k, wv = 1 + .25 * Math.sin(T * 40); ctx.beginPath(); ctx.moveTo(ex0, ey0); ctx.lineTo(x1, y1);
        ctx.globalAlpha = fade * .25; ctx.strokeStyle = C(1); ctx.lineWidth = 22 * d * wv; ctx.stroke(); ctx.globalAlpha = fade * .6; ctx.strokeStyle = G(1); ctx.lineWidth = 9 * d * wv; ctx.stroke(); ctx.globalAlpha = fade; ctx.strokeStyle = "#fff"; ctx.lineWidth = 3 * d; ctx.stroke();
        if (k >= 1) { const r = Lg * .8 * wv; ctx.drawImage(gl, E0.x - r, E0.y - r, r * 2, r * 2); if (!m.hit) { m.hit = 1; b.shake = Math.max(b.shake || 0, 10 * d); b.flash = Math.max(b.flash || 0, .12); } } } } }
  /* reactive shielding: hexagonal carapace plates light where the shot lands */
  for (const h of Hh || []) { const k = (T - h.t0) / .6; if (k < 0 || k > 1) continue; const E0 = scr[h.e], S0 = scr[h.s]; if (!E0 || !S0 || !(b.n[h.e] > 0)) continue; const q = b.Q[h.e], g = b.geo && b.geo[h.e], Lg = g ? g.L : 40;
    let sh = 1; try { sh = bPos(b, h.e, T).sh; if (sh == null) sh = 1; } catch (e) {} const col = sh > .02 ? crcRGB(q) : gold, R = Lg * .62, ang = Math.atan2(S0.y - E0.y, S0.x - E0.x), ix = E0.x + Math.cos(ang) * R * .9, iy = E0.y + Math.sin(ang) * R * .45, al = (1 - k) * (sh > .02 ? .35 + .65 * Math.min(1, sh) : .8);
    ctx.globalAlpha = al * .35; ctx.strokeStyle = `rgba(${col},1)`; ctx.lineWidth = 1.6 * d; ctx.beginPath(); ctx.ellipse(E0.x, E0.y, R, R * .5, 0, ang - 1.1, ang + 1.1); ctx.stroke();
    if (sh > .02) { const hs = Lg * .09, rip = k * R * 1.2; for (let i = -2; i <= 2; i++) for (let j = -1; j <= 1; j++) { const hx = ix + (i * 1.5 + (j & 1) * .75) * hs * 1.15, hy = iy + j * hs * 1.3, dd = Math.hypot(hx - ix, hy - iy); if (dd > rip + hs || dd < rip - hs * 2.5) continue;
        ctx.globalAlpha = al * (1 - dd / (R * 1.3)); ctx.strokeStyle = `rgba(${col},1)`; ctx.lineWidth = 1.4 * d; ctx.beginPath(); for (let a = 0; a < 6; a++) { const aa = a / 6 * TAU, px = hx + Math.cos(aa) * hs * .6, py = hy + Math.sin(aa) * hs * .6; a ? ctx.lineTo(px, py) : ctx.moveTo(px, py); } ctx.closePath(); ctx.stroke();
        ctx.strokeStyle = `rgba(${gold},${.6 * al})`; ctx.lineWidth = .8 * d; ctx.stroke(); }
      const fr = Lg * .3 * (1 - k * .5); ctx.globalAlpha = al; ctx.drawImage(glowSprite(`rgba(${col},1)`), ix - fr, iy - fr, fr * 2, fr * 2); }
    else { for (let i = 0; i < 5; i++) { const a = ang + (i - 2) * .5 + h.seed, l = Lg * .25 * k; ctx.globalAlpha = (1 - k); ctx.strokeStyle = `rgba(${gold},1)`; ctx.lineWidth = 1.5 * d; ctx.beginPath(); ctx.moveTo(ix, iy); ctx.lineTo(ix + Math.cos(a) * l, iy + Math.sin(a) * l); ctx.stroke(); } } }
  ctx.restore(); }
