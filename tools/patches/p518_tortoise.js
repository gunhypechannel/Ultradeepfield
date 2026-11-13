//@@MATS
  /* v518 the Crystal Tortoise in high detail: basalt scutes with growth rings, a blue rune carved in each and blue light in the seams
     (all of it breathing slowly), a bump map for depth, scaled skin, horn beak and claws, and blue crystal prisms that pulse */
  const TS = (draw, srgb) => T2(1024, 512, draw, srgb), HEX = (x, cx, cy, s, sy) => { x.beginPath(); for (let k = 0; k < 6; k++) { const a = k / 6 * TAU + Math.PI / 6; k ? x.lineTo(cx + Math.cos(a) * s, cy + Math.sin(a) * s * sy) : x.moveTo(cx + Math.cos(a) * s, cy + Math.sin(a) * s * sy); } x.closePath(); };
  const SC = []; { const cols = 9; for (let row = 0; row < 4; row++) for (let i = 0; i < cols; i++) SC.push([(i + (row % 2) * .5) / cols, .1 + row * .25, row]); }
  const rune = (x, cx, cy, s, r) => { x.beginPath(); const n = 3 + ((r() * 3) | 0); let px = cx + (r() - .5) * s, py = cy - s * .6; x.moveTo(px, py);
    for (let j = 0; j < n; j++) { px = cx + (r() - .5) * s * 1.1; py += s * 1.2 / n; x.lineTo(px, py); } x.moveTo(cx - s * .45, cy); x.lineTo(cx + s * .45, cy); x.moveTo(cx, cy - s * .2); x.arc(cx, cy - s * .2, s * .18, -Math.PI / 2, Math.PI * 1.5); x.stroke(); };
  const tsC = TS((x, W, H) => { const n = fbm2(7811), img = x.createImageData(W, H), d = img.data; for (let px = 0; px < W; px++) for (let py = 0; py < H; py++) { const v = n(px / 30, py / 30, 64, 5), o = (py * W + px) * 4; d[o] = 22 + v * 34; d[o + 1] = 27 + v * 38; d[o + 2] = 36 + v * 46; d[o + 3] = 255; } x.putImageData(img, 0, 0);
    for (const [u, v] of SC) for (const du of [-1, 0, 1]) { const cx = (u + du) * W, cy = v * H, s = W / 19; for (let k = 0; k < 4; k++) { HEX(x, cx, cy, s * (1 - k * .2), 1.1); x.strokeStyle = `rgba(${k ? "90,110,130" : "4,6,10"},${k ? .35 : .95})`; x.lineWidth = k ? 1.5 : 5; x.stroke(); } } }, 1);
  const tsE = TS((x, W, H) => { const r = rnd(7812); x.fillStyle = "#000"; x.fillRect(0, 0, W, H); x.lineCap = "round"; x.lineJoin = "round";
    for (const [u, v] of SC) for (const du of [-1, 0, 1]) { const cx = (u + du) * W, cy = v * H, s = W / 19; HEX(x, cx, cy, s, 1.1); x.strokeStyle = "rgba(60,180,255,.85)"; x.lineWidth = 2.2; x.stroke(); x.strokeStyle = "rgba(150,230,255,1)"; x.lineWidth = 4; x.shadowColor = "#3ac0ff"; x.shadowBlur = 8; rune(x, cx, cy, s * .8, rnd(7813 + Math.round(u * 100) + Math.round(v * 1000))); x.shadowBlur = 0; } });
  const tsB = TS((x, W, H) => { x.fillStyle = "#808080"; x.fillRect(0, 0, W, H); for (const [u, v] of SC) for (const du of [-1, 0, 1]) { const cx = (u + du) * W, cy = v * H, s = W / 19, g = x.createRadialGradient(cx, cy, 0, cx, cy, s); g.addColorStop(0, "#d0d0d0"); g.addColorStop(.85, "#909090"); g.addColorStop(1, "#202020"); x.fillStyle = g; HEX(x, cx, cy, s, 1.1); x.fill(); } });
  C.tshell2 = new TH.MeshPhysicalMaterial({ map: tsC, emissiveMap: tsE, emissive: 0xffffff, emissiveIntensity: 2.2, bumpMap: tsB, bumpScale: .02, roughness: .72, metalness: .2, clearcoat: .25, clearcoatRoughness: .55 }); C.tshell2.userData.pulse = ".72 + .5 * (.5 + .5 * sin(uMT * 1.3))";
  const skC = T2(512, 256, (x, W, H) => { const r = rnd(7814); x.fillStyle = "#1a2222"; x.fillRect(0, 0, W, H); for (let row = 0; row < 26; row++) for (let i = 0; i < 52; i++) { const cx = i * W / 50 + (row % 2) * W / 100, cy = row * H / 24, k = 30 + r() * 26; x.fillStyle = `rgb(${k - 6},${k + 4},${k + 2})`; x.beginPath(); x.ellipse(cx, cy, W / 104, H / 52, 0, 0, TAU); x.fill(); x.strokeStyle = "rgba(0,0,0,.6)"; x.lineWidth = 1; x.stroke(); } }, 1);
  const skB = T2(512, 256, (x, W, H) => { x.fillStyle = "#606060"; x.fillRect(0, 0, W, H); for (let row = 0; row < 26; row++) for (let i = 0; i < 52; i++) { const cx = i * W / 50 + (row % 2) * W / 100, cy = row * H / 24, g = x.createRadialGradient(cx, cy, 0, cx, cy, W / 100); g.addColorStop(0, "#d8d8d8"); g.addColorStop(1, "#303030"); x.fillStyle = g; x.beginPath(); x.ellipse(cx, cy, W / 104, H / 52, 0, 0, TAU); x.fill(); } });
  C.tskin2 = new TH.MeshPhysicalMaterial({ map: skC, bumpMap: skB, bumpScale: .025, roughness: .7, metalness: .05, clearcoat: .25 });
  C.thorn = new TH.MeshPhysicalMaterial({ color: 0x2a2620, roughness: .35, metalness: .1, clearcoat: .8 });
  C.tcrys = new TH.MeshPhysicalMaterial({ color: 0x1f7cff, emissive: 0x0a58ff, emissiveIntensity: .75, roughness: .05, metalness: 0, clearcoat: 1, flatShading: true }); C.tcrys.userData.pulse = ".65 + .7 * (.5 + .5 * sin(uMT * 2.1))";
  C.tcrys2 = new TH.MeshPhysicalMaterial({ color: 0x163cb8, emissive: 0x1a2cff, emissiveIntensity: .7, roughness: .05, metalness: 0, clearcoat: 1, flatShading: true }); C.tcrys2.userData.pulse = ".65 + .7 * (.5 + .5 * sin(uMT * 2.1 + 1.7))";
  C.tglow = new TH.MeshBasicMaterial({ color: 0x6fe0ff, toneMapped: false });
//@@MODEL
  } else if (k === "ctort") { /* v518 a tortoise the size of a moonlet, in high detail: a domed shell of rune-carved scutes ringed by
       marginal plates, a spine and flanks of blue crystal prisms, four columned legs with claws that walk, a horn-beaked head on a
       folded neck that looks about and opens its jaw on a blue glow, and a short tail */
    const sg = new TH.SphereGeometry(1, 120, 48, 0, TAU, 0, Math.PI / 2), uv = sg.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setY(i, (uv.getY(i) - .5) * 2);
    const shell = add(new TH.Mesh(sg, C.tshell2)); shell.scale.set(2.4, 1.3, 1.75);
    const plast = add(new TH.Mesh(new TH.SphereGeometry(1, 64, 20), C.thorn), 0, -.05, 0); plast.scale.set(2.3, .28, 1.68);
    for (let i = 0; i < 34; i++) { const a = i / 34 * TAU, m = add(new TH.Mesh(new TH.BoxGeometry(.42, .1, .2), C.tshell2), Math.cos(a) * 2.42, -.01, Math.sin(a) * 1.77); m.rotation.set(0, -a, 0); m.rotateX(.0); m.rotateZ(-.32); } // marginal scutes round the rim
    const up = new TH.Vector3(0, 1, 0), onShell = (th, ph) => { const nx = Math.cos(th) * Math.sin(ph), ny = Math.cos(ph), nz = Math.sin(th) * Math.sin(ph); return [new TH.Vector3(2.4 * nx, 1.3 * ny, 1.75 * nz), new TH.Vector3(nx / 2.4, ny / 1.3, nz / 1.75).normalize()]; };
    const prism = (p, n, L, r0, mat) => { const gq = new TH.Group(); gq.position.copy(p); gq.quaternion.setFromUnitVectors(up, n); g.add(gq);
      const b = new TH.Mesh(new TH.CylinderGeometry(r0, r0 * 1.08, L, 6), mat); b.position.y = L / 2 - r0 * .3; gq.add(b); const tp = new TH.Mesh(new TH.ConeGeometry(r0, r0 * 2.4, 6), mat); tp.position.y = L - r0 * .3 + r0 * 1.2; gq.add(tp); };
    const r = rnd(7820);
    for (let i = 0; i <= 8; i++) { const t = i / 8, x = -1.7 + t * 3.2, ph = Math.acos(Math.min(1, Math.abs(x) / 2.4)) , hgt = 1.3 * Math.sqrt(Math.max(0, 1 - (x / 2.4) ** 2)), L = .35 + .9 * Math.sin(t * Math.PI) ** 1.5;
      prism(new TH.Vector3(x, hgt - .05, 0), new TH.Vector3(-x * .12, 1, 0).normalize(), L, .1 + L * .07, i % 2 ? C.tcrys2 : C.tcrys);
      for (const sd of [1, -1]) if (i % 2 === 0 && i && i < 8) prism(new TH.Vector3(x + .1, hgt - .12, sd * .26), new TH.Vector3(-x * .1, 1, sd * .45).normalize(), L * .55, .07 + L * .04, C.tcrys); }
    for (let i = 0; i < 9; i++) { const th = r() * TAU, ph = .55 + r() * .55, [p, n] = onShell(th, ph); for (let j = 0; j < 3; j++) { const q = p.clone().add(new TH.Vector3((r() - .5) * .25, 0, (r() - .5) * .25)); prism(q, n.clone().lerp(new TH.Vector3((r() - .5), 1, (r() - .5)).normalize(), .3).normalize(), .22 + r() * .38 - j * .05, .045 + r() * .03, j % 2 ? C.tcrys2 : C.tcrys); } }
    // neck in folds, head, beak, jaw (opens on a blue glow), eyes and brow plates, two crystal horns
    add(new TH.Mesh(taperTube([[1.85, -.02, 0], [2.2, .06, 0], [2.48, .18, 0], [2.68, .28, 0]], t => .36 - t * .1, 40, 20), C.tskin2));
    for (let i = 0; i < 4; i++) { const f = add(new TH.Mesh(new TH.TorusGeometry(.33 - i * .025, .03, 8, 28), C.tskin2), 2.0 + i * .17, .02 + i * .07, 0); f.rotation.y = Math.PI / 2; f.rotation.x = .3; }
    const hg0 = g.children.length;
    const skull = add(new TH.Mesh(new TH.SphereGeometry(1, 48, 32), C.tskin2), 2.88, .33, 0); skull.scale.set(.37, .27, .3);
    const beak = add(new TH.Mesh(new TH.ConeGeometry(.16, .34, 16), C.thorn), 3.25, .24, 0); beak.rotation.z = -Math.PI / 2 - .35; beak.scale.z = 1.2;
    const jaw = add(new TH.Mesh(new TH.SphereGeometry(1, 32, 16), C.thorn), 3.04, -.035, 0); jaw.scale.set(.28, .065, .21);
    add(new TH.Mesh(new TH.SphereGeometry(1, 20, 12), C.tglow), 3.0, .07, 0).scale.set(.2, .025, .14);
    for (const s of [1, -1]) { add(new TH.Mesh(new TH.SphereGeometry(.075, 20, 14), C.tglow), 3.05, .42, s * .21);
      const brow = add(new TH.Mesh(new TH.BoxGeometry(.2, .04, .07), C.thorn), 3.0, .5, s * .2); brow.rotation.set(s * .3, s * .2, -.25);
      prism(new TH.Vector3(2.78, .55, s * .14), new TH.Vector3(-.6, 1, s * .4).normalize(), .26, .045, C.tcrys); }
    for (const m of g.children.slice(hg0)) { m.position.x = 2.55 + (m.position.x - 2.55) * 1.3; m.position.y = .15 + (m.position.y - .15) * 1.3; m.position.z *= 1.3; m.scale.multiplyScalar(1.3); }
    // four columned legs: scaled thigh, shin with plates, a broad foot with four claws
    for (const sx of [1, -1]) for (const sz of [1, -1]) { const lx = sx * 1.45, lz = sz * 1.25, fr = sx > 0 ? 1 : .85;
      const th = add(new TH.Mesh(new TH.SphereGeometry(1, 32, 20), C.tskin2), lx, -.32, lz); th.scale.set(.4 * fr, .36, .4 * fr);
      add(new TH.Mesh(new TH.CylinderGeometry(.3 * fr, .34 * fr, .62, 28), C.tskin2), lx, -.68, lz);
      for (let j = 0; j < 6; j++) { const a = j / 6 * TAU, pl = add(new TH.Mesh(new TH.SphereGeometry(.1, 10, 8), C.tskin2), lx + Math.cos(a) * .3 * fr, -.62 - (j % 2) * .12, lz + Math.sin(a) * .3 * fr); pl.scale.set(1, .6, 1); }
      const ft = add(new TH.Mesh(new TH.SphereGeometry(1, 28, 14), C.tskin2), lx + sx * .05, -.98, lz); ft.scale.set(.4 * fr, .14, .38 * fr);
      for (let j = 0; j < 4; j++) { const a = (j - 1.5) * .45 + (sx > 0 ? 0 : Math.PI), cl = add(new TH.Mesh(new TH.ConeGeometry(.05, .2, 8), C.thorn), lx + Math.cos(a) * .4 * fr, -1.0, lz + Math.sin(a) * .34); cl.rotation.z = (sx > 0 ? -1 : 1) * (Math.PI / 2 - .25); cl.rotation.y = -a + (sx > 0 ? 0 : Math.PI); } }
    add(new TH.Mesh(taperTube([[-2.2, -.05, 0], [-2.55, -.12, 0], [-2.85, -.22, 0]], t => .16 * (1 - t * .8), 20, 10), C.tskin2));
    prism(new TH.Vector3(-2.85, -.22, 0), new TH.Vector3(-1, -.2, 0).normalize(), .16, .035, C.tcrys);
