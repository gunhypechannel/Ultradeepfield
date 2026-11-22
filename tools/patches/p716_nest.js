    if (part !== "swarm") { /* v715 the Starhive remastered (owner: the nest looked smooth and broken): a paper wasp nest the size of a station. Overlapping
       envelopes of chewed paper, each one a scalloped, wavering band streaked in grey, tan and rust; the open comb under it, every cell
       glowing from inside; a twisted paper stalk; holes torn in the envelope where the comb shows through. Nothing smooth or glossy. */
      const NK = C.nestK || (C.nestK = (() => { const mk = (w, h, f) => { const c = document.createElement("canvas"); c.width = w; c.height = h; f(c.getContext("2d"), w, h); const t = new TH.CanvasTexture(c); t.encoding = TH.sRGBEncoding; t.wrapS = t.wrapT = TH.RepeatWrapping; t.anisotropy = 4; return t; };
        const paper = mk(512, 256, (x, W, H) => { const r = rnd(7311), P = ["#6f6a62", "#8b7f6c", "#a39277", "#5d5348", "#7a6a55", "#958a7a", "#4f463c", "#86735a"]; x.fillStyle = "#6c6358"; x.fillRect(0, 0, W, H);
          for (let i = 0; i < 150; i++) { const y0 = r() * H, amp = 1 + r() * 4, fq = (1 + (r() * 4 | 0)) * TAU / W, ph = r() * TAU, th = 1 + r() * 4.5; x.strokeStyle = P[r() * P.length | 0]; x.globalAlpha = .35 + r() * .55; x.lineWidth = th; x.beginPath(); for (let px = 0; px <= W; px += 8) { const yy = y0 + Math.sin(px * fq + ph) * amp + Math.sin(px * fq * 3.1 + ph * 2) * amp * .35; px ? x.lineTo(px, yy) : x.moveTo(px, yy); } x.stroke(); }
          x.globalAlpha = .5; for (let i = 0; i < 1400; i++) { const v = 40 + r() * 90 | 0; x.fillStyle = `rgb(${v + 10},${v + 4},${v - 6})`; x.fillRect(r() * W, r() * H, 1 + r() * 3, 1); } x.globalAlpha = 1; });
        const bump = mk(256, 128, (x, W, H) => { const r = rnd(7312); x.fillStyle = "#808080"; x.fillRect(0, 0, W, H); for (let i = 0; i < 90; i++) { const y0 = r() * H; x.strokeStyle = r() < .5 ? "#5a5a5a" : "#a8a8a8"; x.globalAlpha = .5; x.lineWidth = 1 + r() * 3; x.beginPath(); for (let px = 0; px <= W; px += 8) { const yy = y0 + Math.sin(px * .05 + i) * 2; px ? x.lineTo(px, yy) : x.moveTo(px, yy); } x.stroke(); } x.globalAlpha = 1; });
        const comb = mk(256, 256, (x, W, H) => { x.fillStyle = "#000"; x.fillRect(0, 0, W, H); const g = x.createRadialGradient(W / 2, H / 2, 4, W / 2, H / 2, W / 2); g.addColorStop(0, "#fff2c0"); g.addColorStop(.35, "#ffb230"); g.addColorStop(.75, "#b84a08"); g.addColorStop(1, "#2a0a00"); x.fillStyle = g; x.beginPath(); for (let k = 0; k < 6; k++) { const a = k / 6 * TAU + Math.PI / 6; k ? x.lineTo(W / 2 + Math.cos(a) * W * .47, H / 2 + Math.sin(a) * H * .47) : x.moveTo(W / 2 + Math.cos(a) * W * .47, H / 2 + Math.sin(a) * H * .47); } x.fill(); });
        const env = new TH.MeshStandardMaterial({ map: paper, bumpMap: bump, bumpScale: .035, roughness: 1, metalness: 0, side: TH.DoubleSide, envMapIntensity: .12, emissive: 0xffffff, emissiveMap: paper, emissiveIntensity: .22 }); /* a little of its own light, like the other monsters, so it reads in the dark */ env.userData.noEnv = 1;
        const wall = new TH.MeshStandardMaterial({ color: 0x6a5a48, roughness: 1, metalness: 0, envMapIntensity: .1 });
        const cell = new TH.MeshBasicMaterial({ map: comb, color: 0xffffff, toneMapped: false });
        const dark = new TH.MeshBasicMaterial({ color: 0x120a05 });
        return { env, wall, cell, dark }; })());
      const rN = rnd(7313), N1 = (a, b) => Math.sin(a * 1.7 + b * 2.3) * .5 + Math.sin(a * 3.1 - b * 1.3) * .3 + Math.sin(a * 5.3 + b * 4.1) * .2;
      /* the envelopes: overlapping bands, top to bottom, each flaring a little at its lower edge, scalloped and wavering */
      const L = 10, top = 1.7, bot = -1.5;
      for (let i = 0; i < L; i++) { const y0 = top - (top - bot) * i / L + .08, y1 = y0 - (top - bot) / L * 1.75, pts = [];
        for (let k = 0; k <= 6; k++) { const u = k / 6, y = y0 + (y1 - y0) * u, rr = Math.max(.08, nr(Math.min(top, Math.max(bot, y)))) * (1 + .045 * i / L) + .03 + Math.pow(u, 2.2) * .16; pts.push(new TH.Vector2(rr, y)); }
        const geo = new TH.LatheGeometry(pts.reverse(), 56), P = geo.attributes.position, v = new TH.Vector3(), seed = rN() * 10;
        for (let j = 0; j < P.count; j++) { v.fromBufferAttribute(P, j); const th = Math.atan2(v.z, v.x), rr = Math.hypot(v.x, v.z), u = (y0 - v.y) / (y0 - y1);
          const wob = 1 + .06 * N1(th * 2 + seed, i) + .025 * Math.sin(th * 9 + seed * 3), sc = u > .8 ? .12 * Math.pow(Math.max(0, Math.sin(th * (5 + i % 3) + seed)), 2) : 0;
          const r2 = rr * wob, y2 = v.y + (u > .8 ? .1 * Math.sin(th * (7 + i % 4) + seed * 2) - sc : .02 * N1(th * 4, seed)); P.setXYZ(j, Math.cos(th) * r2, y2, Math.sin(th) * r2); }
        geo.computeVertexNormals(); const U = geo.attributes.uv; for (let j = 0; j < U.count; j++) U.setXY(j, U.getX(j) * 3, U.getY(j) * .35 + i * .27);
        add(new TH.Mesh(geo, NK.env)); }
      /* the comb under the open mouth: a disc of hexagonal cells, each glowing from inside, deepest in the middle */
      const cr = .17, cells = []; for (let q = -4; q <= 4; q++) for (let s = -4; s <= 4; s++) { const x = cr * 1.74 * (q + s / 2), z = cr * 1.5 * s; if (Math.hypot(x, z) < nr(bot) * .92 + .25) cells.push([x, z]); }
      const wg = new TH.CylinderGeometry(cr, cr, .26, 6, 1, true), cg = new TH.CircleGeometry(cr * .86, 6); cg.rotateX(-Math.PI / 2);
      cells.forEach(([x, z]) => { const dep = .08 * (1 - Math.hypot(x, z) / 1.2) + rN() * .05, w = add(new TH.Mesh(wg, NK.wall), x, bot - .02 + dep, z), c = add(new TH.Mesh(cg, NK.cell), x, bot - .12 + dep, z); w.rotation.y = c.rotation.y = Math.PI / 6; });
      /* a few cells breaking through the envelope low on its sides, where the comb shows */
      for (let i = 0; i < 6; i++) { const a = i * 2.39 + .4, y = -1.1 + (i % 3) * .28, rr = nr(y) * 1.04, c = add(new TH.Mesh(cg, NK.cell), Math.cos(a) * rr, y, Math.sin(a) * rr); c.lookAt(Math.cos(a) * 9, y, Math.sin(a) * 9); c.rotateX(Math.PI / 2); c.scale.setScalar(.8); }
      /* the twisted paper stalk it hangs from */
      { const sg = new TH.CylinderGeometry(.12, .34, 1.3, 9, 8), P = sg.attributes.position, v = new TH.Vector3(); for (let j = 0; j < P.count; j++) { v.fromBufferAttribute(P, j); const tw = v.y * 1.6, c = Math.cos(tw), s = Math.sin(tw), rr = 1 + .12 * Math.sin(Math.atan2(v.z, v.x) * 5 + v.y * 6); P.setXYZ(j, (v.x * c - v.z * s) * rr, v.y, (v.x * s + v.z * c) * rr); } sg.computeVertexNormals(); add(new TH.Mesh(sg, NK.env), 0, top + .55, 0); }
      const throat = add(new TH.Mesh(new TH.CircleGeometry(nr(bot) * .7, 24), NK.dark), 0, bot + .02, 0); throat.rotation.x = Math.PI / 2;
    }
