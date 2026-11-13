//@@MATS
  /* v527 the special creatures */
  const keC = T2(256, 256, (x, W, H) => { const g = x.createRadialGradient(W * .5, H * .45, 4, W * .5, H * .5, W * .6); g.addColorStop(0, "#f2b8ff"); g.addColorStop(.5, "#9a3cd8"); g.addColorStop(1, "#3a0a5a"); x.fillStyle = g; x.fillRect(0, 0, W, H);
    const r = rnd(7951); x.strokeStyle = "rgba(255,200,255,.35)"; x.lineWidth = 1.5; for (let i = 0; i < 26; i++) { x.beginPath(); let px = r() * W, py = r() * H; x.moveTo(px, py); for (let j = 0; j < 5; j++) { px += (r() - .5) * 40; py += (r() - .5) * 40; x.lineTo(px, py); } x.stroke(); } }, 1);
  C.kegg = new TH.MeshPhysicalMaterial({ map: keC, emissiveMap: keC, emissive: 0xffffff, emissiveIntensity: .9, roughness: .15, metalness: 0, clearcoat: 1, transparent: true, opacity: .82 }); C.kegg.userData.pulse = ".6 + .6 * (.5 + .5 * sin(uMT * 1.8))";
  C.kembryo = new TH.MeshBasicMaterial({ color: 0x1a0428 });
  C.kflesh = new TH.MeshStandardMaterial({ color: 0x2a1030, roughness: .55, metalness: .1, emissive: 0x3a0a4a, emissiveIntensity: .6 });
  C.ghost = new TH.MeshBasicMaterial({ color: 0x5ff0ff, transparent: true, opacity: .26, toneMapped: false, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide });
  C.ghostB = new TH.MeshBasicMaterial({ color: 0xbffcff, transparent: true, opacity: .7, toneMapped: false, blending: TH.AdditiveBlending, depthWrite: false });
  const roC = T2(512, 256, (x, W, H) => { const n = fbm2(7952), img = x.createImageData(W, H), d = img.data; for (let px = 0; px < W; px++) for (let py = 0; py < H; py++) { const v = n(px / 18, py / 18, 64, 5), o = (py * W + px) * 4; d[o] = 60 + v * 70; d[o + 1] = 46 + v * 54; d[o + 2] = 30 + v * 36; d[o + 3] = 255; } x.putImageData(img, 0, 0);
    x.strokeStyle = "rgba(10,6,2,.85)"; x.lineWidth = 3; for (let i = 0; i < 16; i++) { x.beginPath(); x.moveTo(i * W / 16, 0); x.lineTo(i * W / 16 + 6, H); x.stroke(); } }, 1);
  C.rock = new TH.MeshStandardMaterial({ map: roC, roughness: .9, metalness: .05 });
  C.maw = new TH.MeshStandardMaterial({ color: 0x5a1c10, roughness: .6, emissive: 0xff7a2a, emissiveIntensity: .55 });
  C.tooth = new TH.MeshStandardMaterial({ color: 0xe8d4a8, roughness: .4 });
  const csC = T2(512, 256, (x, W, H) => { x.fillStyle = "#2a1a40"; x.fillRect(0, 0, W, H); for (let row = 0; row < 12; row++) for (let i = 0; i < 40; i++) { const cx = i * W / 38 + (row % 2) * W / 76, cy = row * H / 11; const g = x.createLinearGradient(cx, cy - 10, cx, cy + 10); g.addColorStop(0, "#ffe08a"); g.addColorStop(1, "#8a5a1a"); x.fillStyle = g; x.beginPath(); x.ellipse(cx, cy, W / 80, H / 24, 0, 0, Math.PI); x.fill(); } }, 1);
  C.cserp = new TH.MeshPhysicalMaterial({ map: csC, emissiveMap: csC, emissive: 0xffffff, emissiveIntensity: .7, roughness: .3, metalness: .6, clearcoat: 1 }); C.cserp.userData.pulse = ".7 + .5 * (.5 + .5 * sin(uMT * 2.4))";
  C.cglow = new TH.MeshBasicMaterial({ color: 0xffd36b, toneMapped: false }); C.cviolet = new TH.MeshBasicMaterial({ color: 0xc87aff, toneMapped: false });
  const stC = T2(512, 256, (x, W, H) => { const n = fbm2(7953), img = x.createImageData(W, H), d = img.data; for (let px = 0; px < W; px++) for (let py = 0; py < H; py++) { const v = n(px / 24, py / 24, 64, 5), m = n(px / 60 + 9, py / 60, 64, 3) > .62 ? 1 : 0, o = (py * W + px) * 4; d[o] = 70 + v * 50 - m * 30; d[o + 1] = 72 + v * 52 + m * 20; d[o + 2] = 68 + v * 44 - m * 30; d[o + 3] = 255; } x.putImageData(img, 0, 0);
    x.strokeStyle = "rgba(20,20,18,.8)"; x.lineWidth = 2; const r = rnd(7954); for (let i = 0; i < 40; i++) x.strokeRect(r() * W, r() * H, 20 + r() * 60, 14 + r() * 40); }, 1);
  const stE = T2(512, 256, (x, W, H) => { const r = rnd(7955); x.fillStyle = "#000"; x.fillRect(0, 0, W, H); x.strokeStyle = "rgba(90,255,170,.9)"; x.lineWidth = 2; x.shadowColor = "#3aff9a"; x.shadowBlur = 6; for (let i = 0; i < 22; i++) { x.beginPath(); let px = r() * W, py = r() * H; x.moveTo(px, py); for (let j = 0; j < 3; j++) { if (r() < .5) px += (r() - .5) * 50; else py += (r() - .5) * 40; x.lineTo(px, py); } x.stroke(); } });
  C.stone = new TH.MeshStandardMaterial({ map: stC, emissiveMap: stE, emissive: 0xffffff, emissiveIntensity: 1.2, roughness: .9, metalness: .05 }); C.stone.userData.pulse = ".6 + .6 * (.5 + .5 * sin(uMT * 1.2))";
  C.sgreen = new TH.MeshBasicMaterial({ color: 0x6affb8, toneMapped: false });
//@@MODELS
  } else if (k === "kegg") { /* v527 a drifting clutch of Kraken eggs on a mass of root-flesh: each egg lit violet from inside, a curled embryo shadow in each */
    const root = add(new TH.Mesh(new TH.SphereGeometry(1, 32, 20), C.kflesh), 0, -.55, 0); root.scale.set(1.9, .55, 1.6);
    const r = rnd(7961), P = [[0, .7, 0, 1.0], [1.1, .35, .5, .85], [-1.0, .3, .7, .8], [.3, .3, -1.1, .82], [-.7, .25, -.8, .72], [1.2, .2, -.7, .7], [-1.5, .1, -.1, .62]];
    for (const [x, y, z, s] of P) { const e = add(new TH.Mesh(new TH.SphereGeometry(1, 32, 24), C.kegg), x, y, z); e.scale.set(.62 * s, .85 * s, .62 * s); e.rotation.z = (r() - .5) * .5;
      const em = add(new TH.Mesh(new TH.TorusGeometry(.22 * s, .12 * s, 10, 20, Math.PI * 1.5), C.kembryo), x, y, z); em.rotation.set(r() * 3, r() * 3, 0); }
    for (let i = 0; i < 9; i++) { const a = i / 9 * TAU, pts = [[Math.cos(a) * 1.2, -.6, Math.sin(a) * 1.0], [Math.cos(a) * 2.0, -.9 - r() * .4, Math.sin(a) * 1.7], [Math.cos(a + .3) * 2.8, -1.5 - r() * .5, Math.sin(a + .3) * 2.4]]; add(new TH.Mesh(taperTube(pts, t => .14 * (1 - t * .85), 24, 8), C.kflesh)); }
  } else if (k === "gwhale") { /* v527 the Ghost Whale: a whale of cold light, its skeleton glowing through its skin */
    const body = lathe([[4.2, 0], [4.1, .45], [3.6, .95], [2.6, 1.3], [1.2, 1.4], [-.4, 1.2], [-1.8, .85], [-3.0, .45], [-3.9, .2], [-4.3, .12]], C.ghost, 64); body.scale.set(1, .82, .92);
    add(new TH.Mesh(taperTube([[3.8, .1, 0], [1.5, .3, 0], [-1.0, .2, 0], [-3.0, 0, 0], [-4.2, -.05, 0]], t => .12 * (1 - t * .6), 60, 8), C.ghostB));
    for (let i = 0; i < 12; i++) { const x = 2.8 - i * .4, rr = 1.15 - Math.abs(i - 3) * .07, rb = add(new TH.Mesh(new TH.TorusGeometry(rr * .95, .035, 6, 32, Math.PI * 1.1), C.ghostB), x, .2, 0); rb.rotation.set(0, Math.PI / 2, Math.PI * .95); rb.scale.set(1, .8, 1); }
    const sk = add(new TH.Mesh(new TH.SphereGeometry(1, 24, 16), C.ghostB), 3.5, .25, 0); sk.scale.set(.55, .35, .4);
    for (const s of [1, -1]) { const fin = add(new TH.Mesh(slab([[.5, 0], [.35, 1.5], [-.7, 3.3], [-.5, 1.5], [-.6, 0]], .05), C.ghost), 1.4, -.55, s * 1.0); fin.rotation.set(s * (Math.PI / 2 + .5), 0, -.25);
      const fl = add(new TH.Mesh(slab([[.3, 0], [-.3, .8], [-1.2, 1.9], [-.85, .65], [-1.0, 0]], .05), C.ghost), -4.1, 0, 0); fl.rotation.x = s * Math.PI / 2;
      add(new TH.Mesh(new TH.SphereGeometry(.08, 12, 8), C.ghostB), 3.2, .2, s * .95); }
  } else if (k === "reat") { /* v527 Rock Eaters: three barrel worms of plated stone, each a round maw ringed with teeth and lit from its gullet */
    const worm = (ox, oy, oz, ry, sc) => { const w = new TH.Group(); w.position.set(ox, oy, oz); w.rotation.y = ry; w.scale.setScalar(sc); g.add(w); const put = m => (w.add(m), m);
      const b = lathe([[1.5, .62], [1.2, .7], [.4, .72], [-.6, .66], [-1.4, .5], [-1.9, .3], [-2.1, .1]], C.rock, 32); g.remove(b); w.add(b);
      for (let i = 0; i < 6; i++) { const rg = put(new TH.Mesh(new TH.TorusGeometry(.7 - Math.abs(i - 1.5) * .04, .08, 8, 28), C.rock)); rg.position.x = 1.2 - i * .5; rg.rotation.y = Math.PI / 2; }
      const m = put(new TH.Mesh(new TH.CircleGeometry(.5, 28), C.maw)); m.position.x = 1.52; m.rotation.y = Math.PI / 2;
      for (let i = 0; i < 14; i++) { const a = i / 14 * TAU, t = put(new TH.Mesh(new TH.ConeGeometry(.05, .26, 6), C.tooth)); t.position.set(1.5, Math.cos(a) * .48, Math.sin(a) * .48); t.rotation.x = a + Math.PI; } };
    worm(.6, .2, 0, 0, 1); worm(-1.0, -.4, 1.5, .5, .8); worm(-.6, .3, -1.6, -.4, .75);
  } else if (k === "cserp") { /* v527 a Celestial Serpent hatchling: a young gold dragon-serpent, violet-eyed, trailing light */
    const pts = []; for (let i = 0; i <= 12; i++) { const t = i / 12; pts.push([2.0 - t * 5.6, Math.sin(t * 5) * .5 * t, Math.sin(t * 6.5 + 1) * .9 * t]); }
    add(new TH.Mesh(taperTube(pts, t => (t < .06 ? .3 + t * 3 : .5 * (1 - t * .85)), 160, 18), C.cserp));
    const hd = add(new TH.Mesh(new TH.SphereGeometry(1, 28, 18), C.cserp), 2.35, .1, 0); hd.scale.set(.55, .3, .34);
    const sn = add(new TH.Mesh(new TH.ConeGeometry(.2, .5, 12), C.cserp), 2.9, .05, 0); sn.rotation.z = -Math.PI / 2; sn.scale.z = 1.3;
    for (const s of [1, -1]) { add(new TH.Mesh(new TH.SphereGeometry(.07, 12, 8), C.cviolet), 2.6, .2, s * .22); const hn = add(new TH.Mesh(new TH.ConeGeometry(.05, .45, 8), C.cglow), 2.1, .38, s * .18); hn.rotation.set(s * .4, 0, .9);
      const fr = add(new TH.Mesh(slab([[.2, 0], [0, .35], [-.4, .55], [-.3, .2], [-.4, 0]], .02), C.cglow), 1.9, .15, s * .3); fr.rotation.x = s * (Math.PI / 2 - .5); }
    const cv = new TH.CatmullRomCurve3(pts.map(p => new TH.Vector3(...p))), q = new TH.Vector3(); for (let i = 1; i < 14; i++) { cv.getPointAt(i / 14, q); const fn = add(new TH.Mesh(new TH.ConeGeometry(.04, .25, 6), C.cglow), q.x, q.y + .45 * (1 - i / 16), q.z); fn.rotation.z = .5; }
  } else if (k === "sent") { /* v527 a Petrified Sentinel: a stone guardian giant, moss in its seams, green runes waking along its body and a green core in its chest */
    const B = (w, h, d, x, y, z, rx, ry, rz) => { const m = add(new TH.Mesh(new TH.BoxGeometry(w, h, d, 2, 2, 2), C.stone), x, y, z); m.rotation.set(rx || 0, ry || 0, rz || 0); return m; };
    B(1.5, 1.6, 1.1, 0, 1.0, 0); B(1.8, .5, 1.3, 0, 1.85, 0); B(1.2, .6, .9, 0, .05, 0); B(.7, .6, .7, 0, 2.45, 0); B(.75, .18, .75, 0, 2.82, 0, 0, 0, .05);
    add(new TH.Mesh(new TH.SphereGeometry(.2, 20, 14), C.sgreen), 0, 1.2, .56); add(new TH.Mesh(new TH.TorusGeometry(.3, .05, 8, 28), C.stone), 0, 1.2, .56);
    for (const s of [1, -1]) { add(new TH.Mesh(new TH.BoxGeometry(.14, .07, .04), C.sgreen), s * .16, 2.5, .36); B(.6, .55, .7, s * 1.25, 1.85, 0, 0, 0, s * .15); B(.42, 1.1, .45, s * 1.35, 1.1, .05, .1, 0, s * .06); B(.5, .55, .55, s * 1.4, .35, .2, .3);
      B(.5, 1.0, .55, s * .4, -.75, 0); B(.6, .25, .8, s * .4, -1.35, .12); }
    const r = rnd(7962); for (let i = 0; i < 10; i++) { const rk = add(new TH.Mesh(new TH.DodecahedronGeometry(.12 + r() * .18, 0), C.stone), (r() - .5) * 4, -1.5 + r() * 4.5, (r() - .5) * 3); rk.rotation.set(r() * 3, r() * 3, 0); } // shards of the mountain it stood in, still orbiting it
