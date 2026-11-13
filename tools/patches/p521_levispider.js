//@@MATS
  /* v520 the Star Leviathan as its card shows it: an armoured space whale, slate hide, glowing cyan throat grooves and energy cracks */
  const lwC = T2(1024, 512, (x, W, H) => { const n = fbm2(7901), img = x.createImageData(W, H), d = img.data;
    for (let px = 0; px < W; px++) { const u = px / W, back = .5 + .5 * Math.cos((u - .75) * TAU); for (let py = 0; py < H; py++) { const v = n(px / 26, py / 26, 64, 5), o = (py * W + px) * 4;
      d[o] = 20 + back * -6 + (1 - back) * 46 + v * 30; d[o + 1] = 28 + (1 - back) * 52 + v * 34; d[o + 2] = 40 + (1 - back) * 62 + v * 40; d[o + 3] = 255; } } x.putImageData(img, 0, 0);
    const r = rnd(7902); x.strokeStyle = "rgba(8,12,18,.85)"; x.lineWidth = 3; for (let i = 0; i < 26; i++) { const u = .1 + i * .011; x.beginPath(); x.moveTo(u * W, H * .1); x.lineTo(u * W + (r() - .5) * 6, H * .62); x.stroke(); }
    for (let i = 0; i < 300; i++) { x.fillStyle = `rgba(${r() < .5 ? "150,170,190" : "6,8,12"},${.2 + r() * .3})`; x.beginPath(); x.arc(r() * W, r() * H, 1 + r() * 3, 0, TAU); x.fill(); } }, 1);
  const lwE = T2(1024, 512, (x, W, H) => { const r = rnd(7903); x.fillStyle = "#000"; x.fillRect(0, 0, W, H); x.lineCap = "round";
    for (let i = 0; i < 26; i++) { const u = .1 + i * .011 + .0055; x.strokeStyle = `rgba(90,220,255,${.55 + r() * .45})`; x.lineWidth = 2; x.shadowColor = "#3ad0ff"; x.shadowBlur = 6; x.beginPath(); x.moveTo(u * W, H * .12); x.lineTo(u * W, H * .6); x.stroke(); }
    for (let i = 0; i < 26; i++) { x.strokeStyle = `rgba(${r() < .8 ? "110,230,255" : "190,120,255"},${.5 + r() * .5})`; x.lineWidth = 1 + r() * 2; x.beginPath(); let px = r() * W, py = r() * H; x.moveTo(px, py); for (let j = 0; j < 7; j++) { px += (r() - .5) * 50; py += (r() - .5) * 36; x.lineTo(px, py); } x.stroke(); }
    x.shadowBlur = 0; for (let i = 0; i < 260; i++) { x.fillStyle = `rgba(160,240,255,${r()})`; x.fillRect(r() * W, r() * H, 2, 2); } });
  C.lwhale = new TH.MeshPhysicalMaterial({ map: lwC, emissiveMap: lwE, emissive: 0xffffff, emissiveIntensity: 1.8, roughness: .55, metalness: .2, clearcoat: .5, clearcoatRoughness: .35, side: TH.DoubleSide }); C.lwhale.userData.pulse = ".75 + .45 * (.5 + .5 * sin(uMT * 1.1))";
  C.larmor = new TH.MeshPhysicalMaterial({ color: 0x1c2532, roughness: .35, metalness: .7, clearcoat: .8, emissive: 0x05202e, emissiveIntensity: 1 });
  C.lfin = new TH.MeshPhysicalMaterial({ color: 0x23303e, roughness: .45, metalness: .3, clearcoat: .6, emissive: 0x0a4a6a, emissiveIntensity: .9, side: TH.DoubleSide });
  C.lcyan = new TH.MeshBasicMaterial({ color: 0x7ae8ff, toneMapped: false });
  /* v520 the Gravity Spider, scarier: black armour plates traced with magenta seams, glowing joints, a purple core eye */
  const spC = T2(512, 256, (x, W, H) => { const r = rnd(7911); x.fillStyle = "#0b0910"; x.fillRect(0, 0, W, H); for (let i = 0; i < 70; i++) { const k = 14 + r() * 18; x.fillStyle = `rgb(${k + 6},${k},${k + 12})`; x.fillRect(r() * W, r() * H, 20 + r() * 70, 10 + r() * 30); }
    x.strokeStyle = "rgba(0,0,0,.9)"; x.lineWidth = 2; for (let i = 0; i < 70; i++) x.strokeRect(r() * W, r() * H, 20 + r() * 70, 10 + r() * 30); }, 1);
  const spE = T2(512, 256, (x, W, H) => { const r = rnd(7912); x.fillStyle = "#000"; x.fillRect(0, 0, W, H); x.lineCap = "round"; x.shadowColor = "#ff3ad8"; x.shadowBlur = 6;
    for (let i = 0; i < 18; i++) { x.strokeStyle = `rgba(255,${60 + r() * 60},${200 + r() * 55},${.6 + r() * .4})`; x.lineWidth = 1.2 + r() * 2.2; x.beginPath(); let px = r() * W, py = r() * H; x.moveTo(px, py); for (let j = 0; j < 4; j++) { if (r() < .5) px += (r() - .5) * 90; else py += (r() - .5) * 60; x.lineTo(px, py); } x.stroke(); } });
  C.sp2 = new TH.MeshPhysicalMaterial({ map: spC, emissiveMap: spE, emissive: 0xffffff, emissiveIntensity: 1.7, roughness: .28, metalness: .55, clearcoat: 1, clearcoatRoughness: .12 }); C.sp2.userData.pulse = ".7 + .5 * (.5 + .5 * sin(uMT * 2.6))";
  C.spM = new TH.MeshBasicMaterial({ color: 0xff3ad8, toneMapped: false }); C.spM.userData.pulse = "1.";
  C.spEye = new TH.MeshBasicMaterial({ color: 0xc860ff, toneMapped: false });
  C.spFang = new TH.MeshPhysicalMaterial({ color: 0x120c16, roughness: .15, metalness: .4, clearcoat: 1 });
//@@LEVI
  } else if (k === "slevi") { /* v520 the Star Leviathan as its card shows it: an armoured whale the size of a dreadnought, plated head and
       back, a ridge of bone spikes, long pectoral fins, broad flukes, cyan light in its throat grooves and in the cracks of its hide */
    const body = lathe([[4.35, 0], [4.28, .3], [4.05, .66], [3.55, .98], [2.85, 1.16], [1.85, 1.26], [.6, 1.2], [-.6, 1.02], [-1.8, .78], [-2.9, .5], [-3.8, .3], [-4.5, .2], [-4.85, .14]], C.lwhale, 96); body.scale.set(1, .82, .9);
    const ry = x => { const P = [[4.35, 0], [4.05, .66], [3.55, .98], [2.85, 1.16], [1.85, 1.26], [.6, 1.2], [-.6, 1.02], [-1.8, .78], [-2.9, .5], [-3.8, .3], [-4.5, .2]]; for (let i = 1; i < P.length; i++) if (x >= P[i][0]) { const [a, ra] = P[i - 1], [b, rb] = P[i]; return rb + (ra - rb) * (x - b) / (a - b); } return .15; };
    for (let i = 0; i < 12; i++) { const x = 3.9 - i * .48, rr = ry(x), w = Math.max(.25, rr * .75), pl = add(new TH.Mesh(new TH.CylinderGeometry(rr, rr, .5, 20, 1, true, Math.PI / 2 - w / rr, 2 * w / rr), C.larmor), x, 0, 0); pl.rotation.z = Math.PI / 2; pl.scale.set(.82 * 1.04, 1, .9 * 1.04); } // overlapping plates along the back
    for (let i = 0; i < 16; i++) { const x = 2.6 - i * .42, rr = ry(x), sp = add(new TH.Mesh(new TH.ConeGeometry(.07 + rr * .05, .3 + rr * .35, 8), C.bone), x, rr * .82 + .12, 0); sp.rotation.z = .55; }
    for (const s of [1, -1]) {
      const fin = add(new TH.Mesh(slab([[.55, 0], [.4, 1.6], [-.8, 3.7], [-.55, 1.6], [-.7, 0]], .08), C.lfin), 1.55, -.55, s * .82); fin.rotation.set(s * (Math.PI / 2 + .55), 0, -.25);
      const fl = add(new TH.Mesh(slab([[.35, 0], [-.35, .9], [-1.35, 2.1], [-.95, .75], [-1.1, 0]], .07), C.lfin), -4.7, 0, 0); fl.rotation.x = s * Math.PI / 2;
      add(new TH.Mesh(new TH.SphereGeometry(.085, 16, 12), C.lcyan), 3.15, .12, s * .9);
      const lid = add(new TH.Mesh(new TH.BoxGeometry(.4, .06, .14), C.larmor), 3.2, .24, s * .88); lid.rotation.set(s * .35, s * .25, -.15);
      add(new TH.Mesh(taperTube([[4.3, -.08, s * .02], [3.85, -.24, s * .6], [3.1, -.36, s * .9], [2.35, -.4, s * .98]], () => .025, 30, 6), C.gill));
      for (let j = 0; j < 3; j++) { const pl = add(new TH.Mesh(new TH.BoxGeometry(.7 - j * .15, .05, .35), C.larmor), 3.6 - j * .55, .32 + j * .12, s * (.55 + j * .1)); pl.rotation.set(s * (.6 - j * .1), 0, -.12); } }
//@@SPIDER
  } else if (k === "gspider") { /* v520 a far scarier Gravity Spider: plated black armour with magenta seams, an armoured abdomen ringed
       with glowing bands and spines, a caged singularity with rings, a purple core eye in a ring of six, curved fangs, palps, and
       eight four-jointed legs with glowing joints and spiked femurs, high-kneed like the card */
    const abd = add(new TH.Mesh(new TH.SphereGeometry(1, 64, 40), C.sp2), -1.7, .55, 0); abd.scale.set(1.5, 1.12, 1.08);
    for (let i = 0; i < 6; i++) { const x = -1.7 + (i - 2.5) * .44, f = Math.sqrt(Math.max(.05, 1 - ((x + 1.7) / 1.5) ** 2)), b = add(new TH.Mesh(new TH.TorusGeometry(1, .035, 8, 48, Math.PI * 1.3), C.spM), x, .55, 0); b.rotation.set(0, Math.PI / 2, -Math.PI * .15); b.scale.set(1.08 * f * 1.02, 1.12 * f * 1.02, 1);
      for (let j = -1; j <= 1; j++) { const sp = add(new TH.Mesh(new TH.ConeGeometry(.05, .32, 6), C.spFang), x, .55 + 1.12 * f * Math.cos(j * .5), 1.08 * f * Math.sin(j * .5)); sp.rotation.set(j * .5, 0, .35); } }
    const ct = add(new TH.Mesh(new TH.SphereGeometry(1, 48, 28), C.sp2), .45, .18, 0); ct.scale.set(.95, .48, .74);
    for (let i = 0; i < 4; i++) { const pl = add(new TH.Mesh(new TH.SphereGeometry(1, 24, 12, 0, TAU, 0, Math.PI / 2), C.sp2), .85 - i * .3, .33, 0); pl.scale.set(.28, .2, .5 - i * .05); }
    const hd = add(new TH.Mesh(new TH.SphereGeometry(1, 32, 20), C.sp2), 1.38, .22, 0); hd.scale.set(.42, .34, .4);
    add(new TH.Mesh(new TH.TorusGeometry(.19, .04, 10, 32), C.spFang), 1.72, .28, 0).rotation.y = Math.PI / 2;
    const eye = add(new TH.Mesh(new TH.SphereGeometry(.17, 28, 20), C.spEye), 1.69, .28, 0); eye.scale.x = .7;
    for (let i = 0; i < 6; i++) { const a = i / 6 * TAU; add(new TH.Mesh(new TH.SphereGeometry(.045, 12, 8), C.spM), 1.66, .28 + Math.sin(a) * .3, Math.cos(a) * .3); }
    for (const s of [1, -1]) { add(new TH.Mesh(taperTube([[1.62, .02, s * .14], [1.88, -.12, s * .2], [2.0, -.38, s * .16], [1.94, -.6, s * .08]], t => .085 * (1 - t * .8), 30, 10), C.spFang)); add(new TH.Mesh(new TH.SphereGeometry(.03, 8, 6), C.spM), 1.94, -.6, s * .08);
      add(new TH.Mesh(taperTube([[1.5, .05, s * .3], [1.95, .2, s * .45], [2.25, -.05, s * .5], [2.35, -.32, s * .46]], t => .05 * (1 - t * .5), 24, 8), C.sp2)); }
    add(new TH.Mesh(new TH.SphereGeometry(.38, 32, 24), C.gcore), -1.7, 1.98, 0);
    for (const [rx, rz] of [[.4, 0], [-.5, .7], [1.2, -.4]]) { const ring = add(new TH.Mesh(new TH.TorusGeometry(.66, .03, 8, 64), C.gring), -1.7, 1.98, 0); ring.rotation.set(Math.PI / 2 + rx, rz, 0); }
    for (let i = 0; i < 4; i++) { const a = i / 4 * TAU + .4; add(new TH.Mesh(taperTube([[-1.7 + Math.cos(a) * .7, 1.45, Math.sin(a) * .6], [-1.7 + Math.cos(a) * .62, 1.95, Math.sin(a) * .55], [-1.7 + Math.cos(a) * .2, 2.48, Math.sin(a) * .18]], () => .028, 16, 5), C.sp2)); }
    for (let i = 0; i < 4; i++) for (const s of [1, -1]) { const th = .95 - i * .62, hx = .95 - i * .33, dx = Math.sin(th), dz = s * Math.cos(th), L = i === 0 ? 1.12 : 1;
      const P0 = [hx, .12, s * .5], P1 = [hx + dx * .85 * L, 1.65 * L, s * .5 + dz * .85 * L], P2 = [hx + dx * 1.95 * L, 1.3 * L, s * .5 + dz * 1.95 * L], P3 = [hx + dx * 2.6 * L, .1, s * .5 + dz * 2.6 * L], P4 = [hx + dx * 2.95 * L, -1.0, s * .5 + dz * 2.95 * L];
      const mid = (a, b, h) => [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + h, (a[2] + b[2]) / 2];
      add(new TH.Mesh(taperTube([P0, mid(P0, P1, .05), P1], t => .15 - t * .03, 20, 10), C.sp2)); add(new TH.Mesh(taperTube([P1, mid(P1, P2, .12), P2], t => .12 - t * .025, 20, 10), C.sp2));
      add(new TH.Mesh(taperTube([P2, mid(P2, P3, .05), P3], t => .095 - t * .025, 20, 8), C.sp2)); add(new TH.Mesh(taperTube([P3, P4], t => .07 * (1 - t * .75), 14, 8), C.spFang));
      for (const J of [P1, P2, P3]) add(new TH.Mesh(new TH.SphereGeometry(.075, 12, 8), C.spM), J[0], J[1], J[2]);
      for (let j = 1; j < 4; j++) { const t = j / 4, sp = add(new TH.Mesh(new TH.ConeGeometry(.03, .2, 6), C.spFang), P1[0] + (P2[0] - P1[0]) * t, P1[1] + (P2[1] - P1[1]) * t + .1, P1[2] + (P2[2] - P1[2]) * t); sp.rotation.x = -s * .4; } }
    for (const z of [-.15, .15]) { const sp = add(new TH.Mesh(new TH.ConeGeometry(.08, .34, 8), C.sp2), -3.2, .45, z); sp.rotation.z = Math.PI / 2; }
