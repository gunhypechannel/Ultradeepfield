# v490 Khezaroth remaster (owner's "Cinematic Masterpiece Edition" brief, assets/bosses/khezaroth/ref/remaster-brief-2026-11-12.txt):
# a sculpted lion-pharaoh face (one displaced mesh: broad muzzle, pronounced nose, heavy stern brow, deep-set violet eyes, smooth dark
# stone) instead of the cartoon parts; a visible chest reactor (concentric gold rings turning, a violet core, arcs, light), framed by
# the chest plates that open fully in the Unsealed Heart; dark-matter flesh full of drifting nebula and stars; layered shoulder armour;
# a dimensional portal turning behind its head; the black hole's lensing (an Einstein ring, bent starlight arcs, plasma spiralling in);
# the signature sequence raises one paw (Judgment).
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
a = s.find("    // the face: a lion's (the owner's art)"); b = s.find("    // the nemes: a striped hood"); assert a > 0 and b > a
s = s[:a] + r'''    // v490 the face: one sculpted mesh after the owner's art: a broad feline muzzle pushed forward, a pronounced nose with a dark pad,
    // a heavy stern brow over deep-set slanted eyes, high flat cheeks, a firm mouth and chin; smooth dark stone, darker in the hollows
    const faceL = (u, v) => { const g = (cu, cv, su, sv) => Math.exp(-(((u - cu) / su) ** 2) - (((v - cv) / sv) ** 2)); let h = 0;
      for (const s of [-1, 1]) h += .12 * g(s * .33, .33, .22, .075) + .07 * g(s * .14, .26, .08, .06) - .15 * g(s * .32, .17, .13, .08) + .03 * g(s * .32, .155, .085, .04) + .1 * g(s * .52, .0, .2, .22) + .055 * g(s * .15, -.45, .12, .09) - .055 * g(s * .2, -.64, .08, .03) - .04 * g(s * .2, .45, .08, .15);
      return h + .42 * g(0, -.34, .32, .28) + .17 * g(0, .06, .15, .32) + .1 * g(0, -.17, .15, .08) - .05 * g(0, -.48, .018, .08) - .05 * g(0, -.58, .12, .02) + .1 * g(0, -.78, .18, .1) - .04 * g(0, .3, .05, .1) + .03 * g(0, .6, .5, .25); };
    const FR = 2.75, FC = V(0, 2.0, .35), FX = 1.25, FY = 1.15, fpos = (u, v, o = 0) => { const lo = u * FX, la = v * FY, r = FR * (1 + faceL(u, v) + o); return V(FC.x + Math.sin(lo) * Math.cos(la) * r, FC.y + Math.sin(la) * r, FC.z + Math.cos(lo) * Math.cos(la) * r); };
    { const fg = new TH.SphereGeometry(1, LO ? 64 : 140, LO ? 48 : 110), P2 = fg.attributes.position, C2 = new Float32Array(P2.count * 3);
      for (let i = 0; i < P2.count; i++) { const x = P2.getX(i), y = P2.getY(i), z = P2.getZ(i), lo = Math.atan2(x, z), la = Math.asin(Math.max(-1, Math.min(1, y))), u = lo / FX, v = la / FY, d = Math.hypot(u, v * .9), m = d < .85 ? 1 : Math.max(0, 1 - (d - .85) / .3), hh = faceL(u, v) * m * m * (3 - 2 * m), r = FR * (1 + hh);
        P2.setXYZ(i, FC.x + x * r, FC.y + y * r, FC.z + z * r); const nose = Math.exp(-((u / .1) ** 2) - (((v + .17) / .06) ** 2)), k = Math.max(.25, 1 - Math.max(0, -hh) * 7 - nose * .7); C2[i * 3] = k; C2[i * 3 + 1] = k * .96; C2[i * 3 + 2] = k * 1.04; }
      fg.setAttribute("color", new TH.BufferAttribute(C2, 3)); fg.computeVertexNormals(); const MFv = MF.clone(); MFv.vertexColors = true; MFv.roughness = .62; MFv.metalness = .35; MFv.envMapIntensity = .6; MFv.userData.P = MF.userData.P; rimOn(MFv, .6, RC); head.add(new TH.Mesh(fg, MFv)); }
    for (const sx of [-1, 1]) for (let k = 0; k < 3; k++) { const p = fpos(sx * (.18 + k * .07), -.4 - k * .03, .01); const d = put(head, new TH.Mesh(new TH.SphereGeometry(.05, 4, 3), glowMat(VIOL, .9)), p.toArray()); d.userData.dyn = 1; }
    const mouth = put(head, new TH.Mesh(new TH.BoxGeometry(.01, .01, .01), glowMat(VIOL, 0)), fpos(0, -.6).toArray()); mouth.userData.dyn = 1; mouth.visible = false;
    const eyeM = new TH.MeshBasicMaterial({ color: 0xc890ff, transparent: true, toneMapped: false }), pupM = new TH.MeshBasicMaterial({ color: 0x14041f });
    const eyes = [-1, 1].map(sx => { const p = fpos(sx * .32, .165, .02), e = put(head, new TH.Mesh(new TH.SphereGeometry(.5, 14, 10), eyeM), p.toArray(), [0, sx * -.45, sx * .38], [1.05, .24, .26]); e.userData.dyn = 1;
      put(head, new TH.Mesh(new TH.BoxGeometry(.08, .26, .05), pupM), fpos(sx * .32, .165, .045).toArray(), [0, sx * -.45, sx * .08]);
      const s = sprite(3.0, "rgba(196,120,255,1)", "khz_eye"); s.position.copy(fpos(sx * .32, .165, .12)); head.add(s); return s; });
''' + s[b:]
# the face's own material (smooth dark stone) is MF, defined just before; keep it
# the chest reactor
rep('const heartG = put(hull, new TH.Group(), [0, 7.0, 10.2]); put(heartG, new TH.Mesh(new TH.SphereGeometry(1.25, 18, 12), CORE), [0, 0, 0]);',
    '''const heartG = put(hull, new TH.Group(), [0, 7.5, 10.5]); put(heartG, new TH.Mesh(new TH.SphereGeometry(1.15, 18, 12), CORE), [0, 0, 0]); put(heartG, new TH.Mesh(new TH.CircleGeometry(3.4, 40), MO), [0, 0, -.35]);
    const reacR = [1.7, 2.4, 3.1].map((r, i) => { const g = put(heartG, new TH.Group(), [0, 0, -.1 + i * .05]); g.userData.dyn = 1; put(g, new TH.Mesh(new TH.TorusGeometry(r, .16 - i * .02, 5, 40), MG), [0, 0, 0]); for (let k = 0; k < 6 + i * 2; k++) { const a = k / (6 + i * 2) * TAU; put(g, new TH.Mesh(new TH.BoxGeometry(.3, .3, .3), MG), [Math.cos(a) * r, Math.sin(a) * r, .1]); } put(g, new TH.Mesh(new TH.TorusGeometry(r - .25, .05, 3, 40), glowMat(VIOL, .8)), [0, 0, .05]); return g; });
    const reacArc = bolts(heartG, LO ? 3 : 6, () => { const a = rnd() * TAU, b = a + (rnd() - .5) * 1.5; return [V(Math.cos(a) * 1.2, Math.sin(a) * 1.2, .2), V(Math.cos(b) * 3.1, Math.sin(b) * 3.1, .2)]; }, 0xe0c0ff);''')
rep("p.rotation.y = sx * ht * 1.1; p.position.x = sx * (.1 + ht * 1.6); p.position.z = 8.3 + ht * .8;", "p.rotation.y = sx * (.55 + ht * .6); p.position.x = sx * (1.2 + ht * 1.4); p.position.z = 8.3 + ht * .8;")
rep("heartS.material.opacity = (.25 + ht * .75) * live * (.85 + .15 * Math.sin(T * 4)); heartS.scale.setScalar(9 * (1 + ht * .6 + Math.sin(T * 4) * .06 * ht));",
    "const pul = .5 + .5 * Math.sin(T * (2 + jw * 6)); heartS.material.opacity = (.55 + ht * .45) * live * (.8 + .2 * pul); heartS.scale.setScalar(8 * (1 + ht * .7 + pul * .1 + jw * .5)); reacR.forEach((r, i) => { r.rotation.z = T * (.25 + i * .2) * (i % 2 ? -1 : 1) * (1 + jw * 3 + ht); }); reacArc(t, (.6 + jw * 4 + ht * 3) * live * dark);")
# dark-matter flesh: drifting nebula and stars in its emissive light
rep('const MB = hullMat("khzb", { rows: 1, cols: 1, pal: ["#130a20"], slits: 0, sg: "#a64cff", veins: 46, vc: "#c48cff", metal: .4, rough: .52, rc: RC, ei: 4.0, rep: [3, 2], relief: 1.4 }); MB.envMapIntensity = 1.2;',
    '''const MB = hullMat("khzb", { rows: 1, cols: 1, pal: ["#130a20"], slits: 0, sg: "#a64cff", veins: 46, vc: "#c48cff", metal: .4, rough: .52, rc: RC, ei: 3.0, rep: [2, 1], relief: 1.4 }); MB.envMapIntensity = 1.2;
    MB.emissiveMap = paint("khz_neb" + LOD, LO ? 256 : 512, (x, N) => { x.fillStyle = "#000"; x.fillRect(0, 0, N, N); for (let i = 0; i < 70; i++) { const px = rnd() * N, py = rnd() * N, r = N * (.04 + rnd() * .14), g = x.createRadialGradient(px, py, 0, px, py, r), c = rnd() < .6 ? "150,60,255" : rnd() < .5 ? "220,90,255" : "90,40,200"; g.addColorStop(0, `rgba(${c},${.18 + rnd() * .22})`); g.addColorStop(1, `rgba(${c},0)`); x.fillStyle = g; for (const dx of [-N, 0, N]) for (const dy of [-N, 0, N]) { x.save(); x.translate(dx, dy); x.fillRect(px - r, py - r, 2 * r, 2 * r); x.restore(); } }
      x.strokeStyle = "rgba(200,130,255,.7)"; for (let i = 0; i < 26; i++) { let px = rnd() * N, py = rnd() * N, a = rnd() * TAU; x.lineWidth = .6 + rnd() * 1.6; x.beginPath(); x.moveTo(px, py); for (let k = 0; k < 24; k++) { a += (rnd() - .5) * .9; px += Math.cos(a) * N / 60; py += Math.sin(a) * N / 60; x.lineTo(px, py); } x.stroke(); }
      for (let i = 0; i < N * 1.2; i++) { const b = rnd(); x.fillStyle = `rgba(${230 + rnd() * 25 | 0},${200 + rnd() * 55 | 0},255,${.4 + b * .6})`; x.fillRect(rnd() * N, rnd() * N, b > .97 ? 2 : 1, b > .97 ? 2 : 1); } }); MB.emissiveMap.repeat.set(2, 1);''')
rep("emi = MB.userData.P.emi, q0 = new TH.Quaternion();", "emi = MB.emissiveMap, q0 = new TH.Quaternion();")
# layered shoulder armour
rep("put(sh, new TH.Mesh(new TH.TorusGeometry(3.0, .13, 4, 26), MG), [sx * 1.0, .2, 0], [0, Math.PI / 2, sx * -.5], [1.15, 1, 1]);",
    "put(sh, new TH.Mesh(new TH.TorusGeometry(3.0, .13, 4, 26), MG), [sx * 1.0, .2, 0], [0, Math.PI / 2, sx * -.5], [1.15, 1, 1]); for (let k = 0; k < 3; k++) { put(sh, new TH.Mesh(new TH.SphereGeometry(3.0 - k * .45, LO ? 10 : 16, 6, 0, TAU, 0, Math.PI * .32), k % 2 ? MG : MO), [sx * (.9 + k * .55), 1.6 - k * 1.1, .2], [0, 0, sx * (-.85 - k * .2)], [1, .55, 1.15]); put(sh, new TH.Mesh(new TH.BoxGeometry(.12, .12, 3.6 - k * .6), glowMat(VIOL, .8)), [sx * (2.2 + k * .55), .9 - k * 1.1, .3], [0, 0, 0]); }")
# a dimensional portal turning behind its head
rep("const RA = put(body, new TH.Group(), [0, 16, -9]);", "const portal = put(body, new TH.Mesh(new TH.CircleGeometry(12, 64), new TH.MeshBasicMaterial({ map: swirlTex(), color: 0xb070ff, transparent: true, opacity: .8, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })), [0, 23, -17]); portal.userData.dyn = 1; const portalC = put(body, new TH.Mesh(new TH.CircleGeometry(4, 32), new TH.MeshBasicMaterial({ color: 0x050008 })), [0, 23, -16.9]);\n    const RA = put(body, new TH.Group(), [0, 16, -9]);")
rep("RA.rotation.z = T * .05 * spin;", "RA.rotation.z = T * .05 * spin; portal.rotation.z = -T * .15 * spin; portal.material.opacity = .75 * runeOn * live; portalC.visible = live > .2;")
# the black hole's lensing
rep("const bhGlow = sprite(16, \"rgba(150,70,255,1)\", \"khz_bhg\"); bhGlow.material.opacity = .4; BH.add(bhGlow);",
    "const bhGlow = sprite(16, \"rgba(150,70,255,1)\", \"khz_bhg\"); bhGlow.material.opacity = .4; BH.add(bhGlow);\n    const ein = ringSprite(13, \"khz_ein\", [[0, \"rgba(0,0,0,0)\"], [.4, \"rgba(0,0,0,0)\"], [.43, \"rgba(235,215,255,.9)\"], [.46, \"rgba(170,120,255,.25)\"], [.6, \"rgba(120,60,255,0)\"], [1, \"rgba(0,0,0,0)\"]]); BH.add(ein);\n    const NSP = LO ? 18 : 32, spG = new TH.BufferGeometry(); spG.setAttribute(\"position\", new TH.BufferAttribute(new Float32Array(NSP * 8 * 6), 3)); const spir = new TH.LineSegments(spG, new TH.LineBasicMaterial({ color: 0xd8a8ff, transparent: true, opacity: .7, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); spir.frustumCulled = false; spir.rotation.x = -Math.PI / 2 + .38; BH.add(spir);")
rep("BH.visible = bhS > .01; BH.scale.setScalar(Math.max(.001, bhS));", "BH.visible = bhS > .01; BH.scale.setScalar(Math.max(.001, bhS)); ein.material.opacity = bhOn * (.7 + .3 * Math.sin(T * 1.3)); ein.scale.setScalar(13 * (1 + Math.sin(T * .9) * .03));\n      { const A = spG.attributes.position.array; for (let i = 0; i < NSP; i++) { const ph = ((T * .25 + i / NSP) % 1), a0 = i / NSP * TAU + T * .6; for (let k = 0; k < 8; k++) { const u0 = (k + ph) / 9, u1 = (k + 1 + ph) / 9, r0 = 8 * (1 - u0) + 1.7, r1 = 8 * (1 - u1) + 1.7, b0 = a0 + u0 * 3.2, b1 = a0 + u1 * 3.2, o = (i * 8 + k) * 6; A[o] = Math.cos(b0) * r0; A[o + 1] = Math.sin(b0) * r0; A[o + 2] = 0; A[o + 3] = Math.cos(b1) * r1; A[o + 4] = Math.sin(b1) * r1; A[o + 5] = 0; } } spG.attributes.position.needsUpdate = true; spir.material.opacity = .55 * bhOn * live * (1 + crush + jw); }")
# the signature sequence lifts one paw
rep("legs.forEach((L, i) => { L.sh.rotation.set(-(1 - paw) * .5 - lift * .55, 0, 0); L.fa.rotation.set((1 - paw) * .9 - lift * .35, 0, 0); L.pw.rotation.set(lift * .35, 0, 0);",
    "legs.forEach((L, i) => { const lf = i === 1 ? lift * 1.5 : lift * .2; L.sh.rotation.set(-(1 - paw) * .5 - lf * .55, 0, 0); L.fa.rotation.set((1 - paw) * .9 - lf * .4, 0, 0); L.pw.rotation.set(lf * .45, 0, 0);")
s = re.sub(r"GAME_V = 489\b", "GAME_V = 490", s)
open(P, 'w').write(s)
