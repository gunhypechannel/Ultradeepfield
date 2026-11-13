//@@MATS
  /* v515 six new species. Every texture is drawn here, and the owner's paintings can replace any of them later. */
  const T2 = (w, h, draw, srgb) => { const t = tex(w, h, draw); if (srgb) t.encoding = TH.sRGBEncoding; return t; };
  // Void Manta: an indigo hide speckled with pale rosettes, with cyan photophores that glow in rows along the wings
  const mC = T2(512, 256, (x, W, H) => { const r = rnd(731), g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, "#0d1030"); g.addColorStop(.5, "#1b1f52"); g.addColorStop(1, "#0b0d26"); x.fillStyle = g; x.fillRect(0, 0, W, H);
    for (let i = 0; i < 420; i++) { const cx = r() * W, cy = r() * H, rr = 1 + r() * 4; x.fillStyle = `rgba(${r() < .7 ? "150,170,255" : "30,10,60"},${.12 + r() * .2})`; x.beginPath(); x.arc(cx, cy, rr, 0, TAU); x.fill(); } }, 1);
  const mE = T2(512, 256, (x, W, H) => { const r = rnd(732); x.fillStyle = "#000"; x.fillRect(0, 0, W, H);
    for (let i = 0; i < 90; i++) { const cx = r() * W, cy = r() * H, rr = 2 + r() * 4, g = x.createRadialGradient(cx, cy, 0, cx, cy, rr * 2.6); g.addColorStop(0, "rgba(140,250,255,1)"); g.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = g; x.fillRect(cx - rr * 3, cy - rr * 3, rr * 6, rr * 6); } });
  C.manta = new TH.MeshPhysicalMaterial({ map: mC, emissiveMap: mE, emissive: 0xffffff, emissiveIntensity: 1.5, roughness: .4, metalness: .1, clearcoat: .7, clearcoatRoughness: .2, side: TH.DoubleSide });
  C.glowM = new TH.MeshBasicMaterial({ color: 0x7af4ff, toneMapped: false });
  // Starhive nest: papery resin in amber bands, a honeycomb of cells, some of them lit from inside
  const nC = T2(512, 256, (x, W, H) => { const r = rnd(733); for (let y = 0; y < H; y += 4) { x.fillStyle = `rgb(${92 + r() * 40},${58 + r() * 26},${24 + r() * 14})`; x.fillRect(0, y, W, 4); }
    x.strokeStyle = "rgba(30,14,4,.75)"; x.lineWidth = 2; const s = 14; for (let row = 0; row < H / (s * 1.5) + 1; row++) for (let i = 0; i < W / (s * 1.73) + 1; i++) { const cx = i * s * 1.73 + (row % 2) * s * .87, cy = row * s * 1.5; x.beginPath(); for (let k = 0; k < 6; k++) { const a = k / 6 * TAU + Math.PI / 6; k ? x.lineTo(cx + Math.cos(a) * s, cy + Math.sin(a) * s) : x.moveTo(cx + Math.cos(a) * s, cy + Math.sin(a) * s); } x.closePath(); x.stroke(); } }, 1);
  const nE = T2(512, 256, (x, W, H) => { const r = rnd(734), s = 14; x.fillStyle = "#000"; x.fillRect(0, 0, W, H);
    for (let row = 0; row < H / (s * 1.5) + 1; row++) for (let i = 0; i < W / (s * 1.73) + 1; i++) { if (r() < .72) continue; const cx = i * s * 1.73 + (row % 2) * s * .87, cy = row * s * 1.5, g = x.createRadialGradient(cx, cy, 0, cx, cy, s);
      g.addColorStop(0, "rgba(255,210,90,1)"); g.addColorStop(.6, "rgba(255,120,20,.6)"); g.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = g; x.fillRect(cx - s, cy - s, s * 2, s * 2); } });
  C.nest = new TH.MeshStandardMaterial({ map: nC, emissiveMap: nE, emissive: 0xffffff, emissiveIntensity: 1.7, roughness: .9, metalness: 0 });
  const wS = T2(64, 256, (x, W, H) => { for (let i = 0; i < 8; i++) { x.fillStyle = i % 2 ? "#120d06" : "#f2b01e"; x.fillRect(0, i * H / 8, W, H / 8); } }, 1);
  C.wasp = new TH.MeshPhysicalMaterial({ map: wS, roughness: .35, metalness: .2, clearcoat: 1, clearcoatRoughness: .1 });
  C.waspD = new TH.MeshPhysicalMaterial({ color: 0x15100a, roughness: .3, metalness: .3, clearcoat: 1 });
  C.wing = new TH.MeshPhysicalMaterial({ color: 0xcfeaff, roughness: .08, metalness: 0, transparent: true, opacity: .32, side: TH.DoubleSide, depthWrite: false });
  C.glowW = new TH.MeshBasicMaterial({ color: 0xffb02a, toneMapped: false });
  // Crystal Tortoise: a shell of dark basalt scutes with cyan light in the seams; violet and ice crystals grow from it
  const tC = T2(512, 256, (x, W, H) => { const r = rnd(735), n = fbm2(7351); const img = x.createImageData(W, H), d = img.data; for (let px = 0; px < W; px++) for (let py = 0; py < H; py++) { const v = n(px / 40, py / 40, 64, 4), o = (py * W + px) * 4; d[o] = 34 + v * 40; d[o + 1] = 38 + v * 42; d[o + 2] = 48 + v * 50; d[o + 3] = 255; } x.putImageData(img, 0, 0);
    x.strokeStyle = "rgba(6,8,12,.9)"; x.lineWidth = 3; for (let row = 0; row < 5; row++) for (let i = 0; i < 9; i++) { const cx = (i + (row % 2) * .5) * W / 8, cy = (row + .5) * H / 4.5, s = W / 17; x.beginPath(); for (let k = 0; k < 6; k++) { const a = k / 6 * TAU; k ? x.lineTo(cx + Math.cos(a) * s, cy + Math.sin(a) * s * .8) : x.moveTo(cx + Math.cos(a) * s, cy + Math.sin(a) * s * .8); } x.closePath(); x.stroke(); } }, 1);
  const tE = T2(512, 256, (x, W, H) => { x.fillStyle = "#000"; x.fillRect(0, 0, W, H); x.strokeStyle = "rgba(90,230,255,.7)"; x.lineWidth = 1.4; for (let row = 0; row < 5; row++) for (let i = 0; i < 9; i++) { const cx = (i + (row % 2) * .5) * W / 8, cy = (row + .5) * H / 4.5, s = W / 17; x.beginPath(); for (let k = 0; k < 6; k++) { const a = k / 6 * TAU; k ? x.lineTo(cx + Math.cos(a) * s, cy + Math.sin(a) * s * .8) : x.moveTo(cx + Math.cos(a) * s, cy + Math.sin(a) * s * .8); } x.closePath(); x.stroke(); } });
  C.tshell = new TH.MeshPhysicalMaterial({ map: tC, emissiveMap: tE, emissive: 0xffffff, emissiveIntensity: 1.4, roughness: .55, metalness: .2, clearcoat: .5 });
  C.tskin = new TH.MeshStandardMaterial({ color: 0x1f2b28, roughness: .85, metalness: .05 });
  C.crys = new TH.MeshPhysicalMaterial({ color: 0xa98cff, emissive: 0x6a38ff, emissiveIntensity: .9, roughness: .06, metalness: 0, clearcoat: 1, flatShading: true });
  C.crysB = new TH.MeshPhysicalMaterial({ color: 0x9cf4ff, emissive: 0x2ab8ff, emissiveIntensity: .8, roughness: .06, metalness: 0, clearcoat: 1, flatShading: true });
  C.eyeC = new TH.MeshBasicMaterial({ color: 0x8ff6ff, toneMapped: false });
  // Gravity Spider: black chitin traced with violet runes; a caged singularity rides on its back
  const pC = T2(512, 256, (x, W, H) => { const r = rnd(736), g = x.createLinearGradient(0, 0, 0, H); g.addColorStop(0, "#0c0a12"); g.addColorStop(.5, "#1d1828"); g.addColorStop(1, "#0a0910"); x.fillStyle = g; x.fillRect(0, 0, W, H);
    for (let i = 0; i < 260; i++) { x.fillStyle = `rgba(120,100,150,${.05 + r() * .12})`; x.fillRect(r() * W, r() * H, 1 + r() * 3, 1 + r() * 8); } }, 1);
  const pE = T2(512, 256, (x, W, H) => { const r = rnd(737); x.fillStyle = "#000"; x.fillRect(0, 0, W, H); x.lineCap = "round";
    for (let i = 0; i < 14; i++) { x.strokeStyle = `rgba(190,120,255,${.5 + r() * .5})`; x.lineWidth = 1 + r() * 2; x.beginPath(); let px = r() * W, py = r() * H; x.moveTo(px, py); for (let j = 0; j < 5; j++) { px += (r() - .5) * 60; py += (r() - .5) * 40; x.lineTo(px, py); } x.stroke(); } });
  C.spider = new TH.MeshPhysicalMaterial({ map: pC, emissiveMap: pE, emissive: 0xffffff, emissiveIntensity: 1.6, roughness: .3, metalness: .4, clearcoat: 1, clearcoatRoughness: .15 });
  C.gcore = new TH.MeshBasicMaterial({ color: 0xd2a4ff, toneMapped: false });
  C.gring = new TH.MeshBasicMaterial({ color: 0x9a5cff, transparent: true, opacity: .75, toneMapped: false, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide });
  C.eyeP = new TH.MeshBasicMaterial({ color: 0xff4ad8, toneMapped: false });
  // Solar Moth: velvet ember body, gold wings with sun-disc eye spots that blaze
  const fC = T2(256, 128, (x, W, H) => { const r = rnd(738); x.fillStyle = "#5a2a10"; x.fillRect(0, 0, W, H); for (let i = 0; i < 1500; i++) { x.fillStyle = `rgba(${r() < .5 ? "255,170,80" : "40,14,4"},${.15 + r() * .25})`; x.fillRect(r() * W, r() * H, 1, 2 + r() * 3); } }, 1);
  C.mothF = new TH.MeshStandardMaterial({ map: fC, roughness: 1, metalness: 0 });
  const SPOT = [[.66, .7, .11], [.32, .5, .09], [.8, .9, .05], [.45, .82, .04]];
  const vC = T2(512, 512, (x, W, H) => { const r = rnd(739), g = x.createLinearGradient(0, H, W, 0); g.addColorStop(0, "#5c1c06"); g.addColorStop(.45, "#c8641a"); g.addColorStop(1, "#ffd25a"); x.fillStyle = g; x.fillRect(0, 0, W, H);
    x.strokeStyle = "rgba(60,20,4,.55)"; x.lineWidth = 3; for (let i = 0; i < 9; i++) { x.beginPath(); x.moveTo(W * .55, 0); x.quadraticCurveTo(W * (.2 + i * .09), H * .45, W * (i * .12 - .1), H); x.stroke(); }
    for (const [u, v, s] of SPOT) { const cx = u * W, cy = (1 - v) * H, rr = s * W; for (const [f, c] of [[1, "#2a0c02"], [.78, "#ffe9a0"], [.55, "#ff9a1a"], [.3, "#1a0602"]]) { x.fillStyle = c; x.beginPath(); x.arc(cx, cy, rr * f, 0, TAU); x.fill(); } }
    for (let i = 0; i < 2200; i++) { x.fillStyle = `rgba(255,230,160,${r() * .12})`; x.fillRect(r() * W, r() * H, 2, 2); } }, 1);
  const vE = T2(512, 512, (x, W, H) => { x.fillStyle = "#000"; x.fillRect(0, 0, W, H);
    for (const [u, v, s] of SPOT) { const cx = u * W, cy = (1 - v) * H, rr = s * W, g = x.createRadialGradient(cx, cy, 0, cx, cy, rr * 1.1); g.addColorStop(0, "rgba(255,240,180,1)"); g.addColorStop(.5, "rgba(255,160,40,.9)"); g.addColorStop(.8, "rgba(255,90,10,.4)"); g.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = g; x.fillRect(cx - rr * 1.2, cy - rr * 1.2, rr * 2.4, rr * 2.4); }
    x.strokeStyle = "rgba(255,190,80,.5)"; x.lineWidth = 3; x.strokeRect(2, 2, W - 4, H - 4); });
  C.mothW = new TH.MeshPhysicalMaterial({ map: vC, emissiveMap: vE, emissive: 0xffffff, emissiveIntensity: 1.6, roughness: .6, metalness: 0, side: TH.DoubleSide });
  C.glowF = new TH.MeshBasicMaterial({ color: 0xffc45a, toneMapped: false });
  // Comet Ram: frost-cracked ice rock, ridged horns, and a long blue comet tail
  const rC = T2(512, 256, (x, W, H) => { const n = fbm2(7401), img = x.createImageData(W, H), d = img.data; for (let px = 0; px < W; px++) for (let py = 0; py < H; py++) { const v = n(px / 36, py / 36, 64, 5), o = (py * W + px) * 4, ice = v > .55 ? (v - .55) * 3 : 0; d[o] = 60 + v * 70 + ice * 120; d[o + 1] = 72 + v * 80 + ice * 130; d[o + 2] = 92 + v * 90 + ice * 140; d[o + 3] = 255; } x.putImageData(img, 0, 0); }, 1);
  const rE = T2(512, 256, (x, W, H) => { const r = rnd(741); x.fillStyle = "#000"; x.fillRect(0, 0, W, H); x.lineCap = "round"; for (let i = 0; i < 18; i++) { x.strokeStyle = `rgba(120,210,255,${.4 + r() * .5})`; x.lineWidth = .8 + r() * 1.6; x.beginPath(); let px = r() * W, py = r() * H; x.moveTo(px, py); for (let j = 0; j < 6; j++) { px += (r() - .5) * 40; py += (r() - .5) * 30; x.lineTo(px, py); } x.stroke(); } });
  C.ramB = new TH.MeshPhysicalMaterial({ map: rC, emissiveMap: rE, emissive: 0xffffff, emissiveIntensity: 1.5, roughness: .5, metalness: .1, clearcoat: .8, clearcoatRoughness: .25 });
  const hC = T2(512, 64, (x, W, H) => { for (let i = 0; i < 64; i++) { x.fillStyle = i % 2 ? "#8a7f6c" : "#cfc4ad"; x.fillRect(i * W / 64, 0, W / 64, H); } }, 1);
  C.ramH = new TH.MeshPhysicalMaterial({ map: hC, roughness: .45, metalness: .05, clearcoat: .7 });
  C.tail = new TH.MeshBasicMaterial({ color: 0x3f8fd8, transparent: true, opacity: .13, toneMapped: false, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide });
  C.tailC = new TH.MeshBasicMaterial({ color: 0x9fdcff, transparent: true, opacity: .3, toneMapped: false, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide });
//@@MODELS
  } else if (k === "vmanta") { // a winged ray the size of a cruiser: a broad disc body, swept wings, curled head lobes and a whip tail with a glowing stinger
    const body = add(new TH.Mesh(new TH.SphereGeometry(1, 48, 24), C.manta)); body.scale.set(2.1, .38, 1.1);
    for (const s of [1, -1]) {
      const w = add(new TH.Mesh(slab([[1.7, 0], [1.0, 1.7], [-.2, 3.5], [-.6, 1.6], [-1.9, 0]], .07), C.manta)); w.rotation.x = s * Math.PI / 2; w.position.y = .02;
      const lobe = add(new TH.Mesh(slab([[.45, 0], [.55, .22], [.2, .3], [-.1, .2], [-.2, 0]], .05), C.manta), 2.0, -.04, s * .5); lobe.rotation.set(s * Math.PI / 2, 0, -.5);
      add(new TH.Mesh(new TH.SphereGeometry(.09, 16, 12), C.glowM), 1.82, .14, s * .62);
      for (let i = 0; i < 9; i++) { const t = (i + 1) / 10, px = 1.7 + (-.2 - 1.7) * t, pz = 3.4 * t; add(new TH.Mesh(new TH.SphereGeometry(.05 * (1 - t * .5), 8, 6), C.glowM), px + .05, .06, s * pz * .97); } }
    const tp = []; for (let i = 0; i <= 8; i++) { const t = i / 8; tp.push([-1.9 - t * 4.8, Math.sin(t * 3) * .12, 0]); }
    add(new TH.Mesh(taperTube(tp, t => .1 * (1 - t * .8), 60, 8), C.manta));
    const st = add(new TH.Mesh(new TH.ConeGeometry(.08, .5, 10), C.glowM), -6.85, .36, 0); st.rotation.z = Math.PI / 2;
    for (let i = 0; i < 5; i++) { const gl = add(new TH.Mesh(new TH.BoxGeometry(.04, .02, .22), C.glowM), .6 - i * .16, -.33, .42); gl.rotation.y = .2; add(new TH.Mesh(new TH.BoxGeometry(.04, .02, .22), C.glowM), .6 - i * .16, -.33, -.42).rotation.y = -.2; } // gill slits that glow underneath
  } else if (k === "swasp") { // a Starhive: a resin nest the size of a station, its cells lit from inside, with the swarm circling it
    const NP = [[1.75, 0], [1.6, .55], [1.15, 1.1], [.45, 1.42], [-.3, 1.45], [-.95, 1.2], [-1.45, .78], [-1.7, .3], [-1.78, 0]], nr = y => { for (let i = 1; i < NP.length; i++) if (y >= NP[i][0]) { const [x0, r0] = NP[i - 1], [x1, r1] = NP[i]; return r1 + (r0 - r1) * (y - x1) / (x0 - x1); } return 0; };
    const nest = lathe(NP, C.nest, 40); nest.rotation.z = Math.PI / 2;
    for (let i = 0; i < 4; i++) { const y = -.9 + i * .6, band = add(new TH.Mesh(new TH.TorusGeometry(nr(y) + .01, .08, 8, 40), C.nest), 0, y, 0); band.rotation.x = Math.PI / 2; }
    add(new TH.Mesh(new TH.ConeGeometry(.3, 1.1, 12), C.nest), 0, 2.2, 0); // the stalk it hangs from
    const mouth = add(new TH.Mesh(new TH.CircleGeometry(.36, 24), C.glowW), 0, -1.55, 0); mouth.rotation.x = Math.PI / 2;
    for (let i = 0; i < 10; i++) { const a = i * 2.4, y = -1 + (i % 5) * .5, rr = nr(y), cell = add(new TH.Mesh(new TH.CylinderGeometry(.18, .2, .3, 6), C.nest), Math.cos(a) * rr * .98, y, Math.sin(a) * rr * .98);
      cell.lookAt(cell.position.clone().multiplyScalar(2)); cell.rotateX(Math.PI / 2); add(new TH.Mesh(new TH.CircleGeometry(.13, 6), C.glowW), Math.cos(a) * (rr + .17), y, Math.sin(a) * (rr + .17)).lookAt(Math.cos(a) * 9, y, Math.sin(a) * 9); }
    for (let i = 0; i < 9; i++) { const a = i / 9 * TAU + (i % 2) * .3, R = 2.5 + (i % 3) * .45, h = -.9 + ((i * 5) % 9) / 9 * 2.2, w = new TH.Group(); w.position.set(Math.cos(a) * R, h, Math.sin(a) * R); w.rotation.y = -(a + Math.PI / 2); w.scale.setScalar(.95 + (i % 3) * .12); g.add(w);
      const put = (m, x, y, z) => { m.position.set(x, y, z); w.add(m); return m; }, el = (mat, rx, ry, rz) => { const ge = new TH.SphereGeometry(1, 20, 14); ge.rotateZ(Math.PI / 2); const m = new TH.Mesh(ge, mat); m.scale.set(rx, ry, rz); return m; };
      put(el(C.wasp, .34, .17, .17), -.36, -.04, 0).rotation.z = .25; put(el(C.waspD, .16, .13, .13), .04, 0, 0); put(el(C.waspD, .1, .1, .11), .24, .02, 0);
      const sting = put(new TH.Mesh(new TH.ConeGeometry(.03, .18, 8), C.glowW), -.74, -.13, 0); sting.rotation.z = Math.PI / 2 + .25;
      for (const s of [1, -1]) { put(new TH.Mesh(new TH.SphereGeometry(.035, 8, 6), C.glowW), .3, .05, s * .06);
        for (const [dx, L] of [[.04, .42], [-.08, .3]]) { const wg = put(new TH.Mesh(new TH.SphereGeometry(1, 16, 8), C.wing), dx - L * .3, .14, s * L * .55); wg.scale.set(L * .32, .01, L * .55); wg.rotation.y = s * .5; } } }
  } else if (k === "ctort") { // a tortoise as big as a moonlet: a basalt shell with glowing seams, crystals growing out of it, and four slow flippers
    const shellG = new TH.SphereGeometry(1, 56, 28, 0, TAU, 0, Math.PI / 2), shell = add(new TH.Mesh(shellG, C.tshell)); shell.scale.set(2.4, 1.35, 1.6);
    const plast = add(new TH.Mesh(new TH.SphereGeometry(1, 40, 16), C.tskin), 0, -.02, 0); plast.scale.set(2.35, .32, 1.55);
    const rim = add(new TH.Mesh(new TH.TorusGeometry(1, .09, 10, 64), C.tshell)); rim.rotation.x = Math.PI / 2; rim.scale.set(2.42, 1.62, 1);
    const r = rnd(7502), up = new TH.Vector3(0, 1, 0);
    for (let i = 0; i < 26; i++) { const big = i < 3, th = r() * TAU, ph = big ? r() * .35 : .3 + r() * .85, nx = Math.cos(th) * Math.sin(ph), ny = Math.cos(ph), nz = Math.sin(th) * Math.sin(ph);
      const p = new TH.Vector3(2.4 * nx, 1.35 * ny, 1.6 * nz), n = new TH.Vector3(nx / 2.4, ny / 1.35, nz / 1.6).normalize(), L = big ? 1.4 + r() * .7 : .35 + r() * .55;
      const c = add(new TH.Mesh(new TH.OctahedronGeometry(1, 0), i % 3 === 1 ? C.crysB : C.crys)); c.scale.set(.13 * L + .06, L, .13 * L + .06); c.quaternion.setFromUnitVectors(up, n.clone().lerp(up, .35).normalize()); c.position.copy(p).addScaledVector(n, L * .55); }
    const neck = add(new TH.Mesh(new TH.CylinderGeometry(.32, .42, .8, 20), C.tskin), 2.45, .05, 0); neck.rotation.z = Math.PI / 2 - .2;
    const head = add(new TH.Mesh(new TH.SphereGeometry(1, 28, 18), C.tskin), 2.95, .2, 0); head.scale.set(.55, .4, .42);
    const beak = add(new TH.Mesh(new TH.ConeGeometry(.2, .35, 12), C.tshell), 3.48, .12, 0); beak.rotation.z = -Math.PI / 2 - .3;
    for (const s of [1, -1]) { add(new TH.Mesh(new TH.SphereGeometry(.07, 12, 8), C.eyeC), 3.15, .33, s * .3);
      const ff = add(new TH.Mesh(new TH.SphereGeometry(1, 24, 10), C.tskin), 1.45, -.12, s * 1.95); ff.scale.set(.95, .1, .55); ff.rotation.y = s * .55;
      const bf = add(new TH.Mesh(new TH.SphereGeometry(1, 20, 10), C.tskin), -1.5, -.12, s * 1.85); bf.scale.set(.55, .09, .4); bf.rotation.y = -s * .5; }
    const tl = add(new TH.Mesh(new TH.ConeGeometry(.14, .55, 10), C.tskin), -2.55, -.02, 0); tl.rotation.z = Math.PI / 2;
  } else if (k === "gspider") { // a void spider: a round abdomen carrying a caged singularity, a narrow head with eight eyes, and eight jointed legs
    const abd = add(new TH.Mesh(new TH.SphereGeometry(1, 40, 24), C.spider), -1.55, .4, 0); abd.scale.set(1.45, 1.1, 1.2);
    const ct = add(new TH.Mesh(new TH.SphereGeometry(1, 32, 18), C.spider), .5, .12, 0); ct.scale.set(.95, .55, .78);
    const hd = add(new TH.Mesh(new TH.SphereGeometry(1, 24, 14), C.spider), 1.38, .18, 0); hd.scale.set(.42, .36, .4);
    for (let i = 0; i < 8; i++) { const a = (i % 4 - 1.5) * .32, row = i < 4 ? 0 : 1; add(new TH.Mesh(new TH.SphereGeometry(row ? .05 : .075, 10, 8), C.eyeP), 1.66 - row * .08, .34 + row * .1, Math.sin(a) * .3); }
    for (const s of [1, -1]) { const f = add(new TH.Mesh(new TH.ConeGeometry(.06, .4, 8), C.gcore), 1.72, -.08, s * .12); f.rotation.z = -Math.PI / 2 - .9; }
    add(new TH.Mesh(new TH.SphereGeometry(.34, 24, 16), C.gcore), -1.55, 1.68, 0);
    for (const [rx, rz] of [[.4, 0], [-.4, .6], [1.2, -.3]]) { const ring = add(new TH.Mesh(new TH.TorusGeometry(.62, .035, 8, 48), C.gring), -1.55, 1.68, 0); ring.rotation.set(Math.PI / 2 + rx, rz, 0); }
    for (let i = 0; i < 4; i++) { const t = new TH.Vector3(-1.55, 1.15, 0); for (const s of [1, -1]) { const p = [[t.x, t.y, 0], [-1.55 + (i - 1.5) * .5, 1.15 + .1, s * .45], [-1.55 + (i - 1.5) * .9, .75, s * 1.05]]; add(new TH.Mesh(taperTube(p, () => .025, 16, 5), C.gring)); } } // the cage struts
    for (let i = 0; i < 4; i++) for (const s of [1, -1]) { const hx = .85 - i * .3, dx = (1.5 - i) * .55, pts = [[hx, .1, s * .5], [hx + dx * .4, .9, s * 1.25], [hx + dx * .8, 1.15, s * 1.9], [hx + dx * 1.3, .3, s * 2.6], [hx + dx * 1.7, -.85, s * 3.0]];
      add(new TH.Mesh(taperTube(pts, t => .13 * (1 - t * .65), 40, 8), C.spider)); add(new TH.Mesh(new TH.SphereGeometry(.07, 8, 6), C.gcore), hx + dx * 1.7, -.88, s * 3.0);
      add(new TH.Mesh(new TH.SphereGeometry(.12, 10, 8), C.spider), hx + dx * .8, 1.15, s * 1.9); }
    for (const z of [-.15, .15]) { const sp = add(new TH.Mesh(new TH.ConeGeometry(.08, .3, 8), C.spider), -2.98, .3, z); sp.rotation.z = Math.PI / 2; }
  } else if (k === "smoth") { // a moth that drinks starlight: a velvet body, feathered antennae, and four great gold wings with burning sun-eyes
    const th = add(new TH.Mesh(new TH.SphereGeometry(1, 28, 18), C.mothF), .55, 0, 0); th.scale.set(.45, .38, .38);
    add(new TH.Mesh(new TH.SphereGeometry(.27, 22, 14), C.mothF), 1.12, .02, 0);
    for (const s of [1, -1]) { add(new TH.Mesh(new TH.SphereGeometry(.13, 16, 12), C.glowF), 1.25, .08, s * .16);
      const ap = [[1.25, .2, s * .08], [1.6, .55, s * .16], [1.95, .75, s * .3]]; add(new TH.Mesh(taperTube(ap, t => .025 * (1 - t * .5), 20, 5), C.mothF));
      for (let j = 1; j < 7; j++) { const t = j / 7, x0 = 1.25 + .7 * t, y0 = .2 + .55 * t, z0 = s * (.08 + .22 * t), fe = add(new TH.Mesh(new TH.ConeGeometry(.012, .16, 4), C.mothF), x0, y0 + .05, z0); fe.rotation.x = s * .4; }
      for (const [sh, rot] of [[[[.95, 0], [1.45, 1.6], [.95, 3.3], [-.2, 2.9], [-.6, 1.9], [-.2, .7], [0, 0]], 0], [[[.2, 0], [-.05, 1.5], [-1.0, 2.4], [-2.0, 1.9], [-2.05, .6], [-1.3, .1], [-.3, 0]], .02]]) {
        const geo = slab(sh, .03); const P2 = geo.attributes.position, UV = geo.attributes.uv; for (let q = 0; q < P2.count; q++) UV.setXY(q, (P2.getX(q) + 2.1) / 3.7, P2.getY(q) / 3.4);
        const w = add(new TH.Mesh(geo, C.mothW), 0, .06 + rot, 0); w.rotation.x = s * (Math.PI / 2 - .12); w.position.z = s * .36; } }
    const ab = lathe([[.2, .22], [-.2, .3], [-.8, .3], [-1.4, .24], [-1.9, .14], [-2.15, .03]], C.mothF, 28); ab.position.y = -.04;
    for (let i = 0; i < 5; i++) { const b = add(new TH.Mesh(new TH.TorusGeometry(.27 - i * .03, .025, 6, 24), C.glowF), -.3 - i * .38, -.04, 0); b.rotation.y = Math.PI / 2; }
  } else if (k === "cram") { // a horned ice-beast that rides a comet: a craggy frozen body, spiralled horns, and a long burning tail of frost
    const bg = new TH.IcosahedronGeometry(1, 4), P2 = bg.attributes.position; for (let i = 0; i < P2.count; i++) { const x = P2.getX(i), y = P2.getY(i), z = P2.getZ(i), d = 1 + .11 * Math.sin(x * 7.1 + y * 3.3) * Math.cos(z * 5.7 - x * 2.1) + .06 * Math.sin(y * 13 + z * 11); P2.setXYZ(i, x * d, y * d, z * d); } bg.computeVertexNormals();
    const body = add(new TH.Mesh(bg, C.ramB), -.3, 0, 0); body.scale.set(2.2, 1.1, 1.15);
    const skull = add(new TH.Mesh(new TH.SphereGeometry(1, 32, 20), C.ramB), 2.0, .2, 0); skull.scale.set(.9, .72, .7);
    const snout = add(new TH.Mesh(new TH.SphereGeometry(1, 24, 14), C.ramB), 2.75, -.05, 0); snout.scale.set(.42, .38, .4);
    for (const s of [1, -1]) { add(new TH.Mesh(new TH.SphereGeometry(.08, 12, 8), C.tailC), 2.55, .3, s * .45);
      const hp = []; for (let i = 0; i <= 14; i++) { const t = i / 14, ph = Math.PI / 3 + t * (5 * Math.PI / 3), R = .9 - .38 * t; hp.push([1.45 + Math.cos(ph) * R, .45 + Math.sin(ph) * R, s * (.55 + t * .8)]); }
      add(new TH.Mesh(taperTube(hp, t => .3 * (1 - t * .8), 80, 14), C.ramH)); }
    for (let i = 0; i < 9; i++) { const sp = add(new TH.Mesh(new TH.ConeGeometry(.12, .7 - i * .04, 6), C.ramB), 1.0 - i * .38, .98 - Math.abs(i - 3) * .05, 0); sp.rotation.z = .6; }
    const tail = add(new TH.Mesh(new TH.ConeGeometry(1.0, 5.5, 28, 1, true), C.tail), -4.8, 0, 0); tail.rotation.z = Math.PI / 2;
    const core = add(new TH.Mesh(new TH.ConeGeometry(.38, 4, 20, 1, true), C.tailC), -4.1, 0, 0); core.rotation.z = Math.PI / 2;
    const r = rnd(7601); for (let i = 0; i < 26; i++) { const t = r(); add(new TH.Mesh(new TH.OctahedronGeometry(.06 + r() * .08, 0), C.tailC), -2.3 - t * 5, (r() - .5) * 1.6 * (1 - t * .5), (r() - .5) * 2 * (1 - t * .4)); }
