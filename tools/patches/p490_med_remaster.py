# v490 Medusara remaster (owner's "Cinematic Masterpiece Edition" brief; her title is now "The Petrified Star"):
# biomechanical serpents (thick segmented dark-metal bodies with gold armour bands and crimson energy between the plates, big armoured
# heads with brow ridges, open jaws, long fangs and red eyes) emerging from behind and around her head and moving independently;
# energy runs along them to her face while the gaze charges; red-violet light leaks through her fractures; crystal deposits and small
# ruins on her surface; three gold rings (the ruin ring, a glyph ring, a tilted outer ring); crimson-white beams with arcs; the scene
# darkens as she charges.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
a = s.find("    /* ---- the serpent crown: gold-scaled snakes rising from her head"); b = s.find("    /* ---- the gold ring rail with gothic ruin towers"); assert a > 0 and b > a
s = s[:a] + r'''    /* ---- v490 the serpent crown: biomechanical serpents rising from behind and around her head, each its own living weapon ---- */
    const MSk = new TH.MeshStandardMaterial({ color: 0x15121a, metalness: .85, roughness: .38, envMapIntensity: .55 }); MSk.userData.P = {}; rimOn(MSk, .45, [1, .3, .25]);
    const CRM = new TH.MeshBasicMaterial({ color: 0xff2a3a, toneMapped: false }), segG = new TH.CylinderGeometry(1, 1.08, 1, LO ? 8 : 12, 1), bandG = new TH.TorusGeometry(1.06, .16, 4, LO ? 10 : 16), seamG = new TH.TorusGeometry(1.02, .07, 3, LO ? 10 : 16);
    const NSN = 9, snakes = []; for (let i = 0; i < NSN; i++) { const a = -2.75 + i / (NSN - 1) * 5.5, root = V(Math.sin(a) * 9.5, 14 + Math.cos(a) * 10.5, -5.5), out = V(Math.sin(a), Math.cos(a) * .9 + .2, .05).normalize();
      const g = put(body, new TH.Group(), root.toArray()); g.userData.dyn = 1; const L = 17 + (i % 3) * 3.5, pts = [], up = V(0, 1, 0), fw = V(0, 0, 1);
      for (let k = 0; k <= 12; k++) { const u = k / 12, w = Math.sin(u * Math.PI * 2 + i * 1.3) * 1.8 * (1 - u * .4); pts.push(out.clone().multiplyScalar(L * .62 * u + w).addScaledVector(up, L * .28 * Math.sin(u * Math.PI * .9)).addScaledVector(fw, L * .62 * u * u + 2 * u)); }
      const cur = new TH.CatmullRomCurve3(pts), NS = LO ? 12 : 20; for (let k = 0; k < NS; k++) { const u = (k + .5) / NS, p = cur.getPointAt(u), tg = cur.getTangentAt(u), r = 2.1 * (1 - u * .5), sg = put(g, new TH.Mesh(segG, MSk), p.toArray()); sg.quaternion.setFromUnitVectors(V(0, 1, 0), tg); sg.scale.set(r, 1.05 * L / NS, r);
        const sm = put(g, new TH.Mesh(seamG, CRM), p.clone().addScaledVector(tg, .5 * L / NS).toArray()); sm.quaternion.setFromUnitVectors(V(0, 0, 1), tg); sm.scale.setScalar(r * .98); if (k % 3 === 1) { const bd = put(g, new TH.Mesh(bandG, MG), p.toArray()); bd.quaternion.setFromUnitVectors(V(0, 0, 1), tg); bd.scale.setScalar(r); } }
      const tip = cur.getPointAt(1), hd = put(g, new TH.Group(), tip.toArray(), null, 3.0); const dir = cur.getTangentAt(1).lerp(fw, .45).normalize(); hd.quaternion.setFromUnitVectors(V(0, 0, 1), dir);
      { const sk = new TH.CylinderGeometry(.55, 1.15, 3.0, 6); sk.rotateX(Math.PI / 2); sk.translate(0, 0, 1.1); put(hd, new TH.Mesh(sk, MSk), [0, .2, 0], null, [1.1, .55, 1]); put(hd, sph(MSk, 12), [0, .15, -.4], null, [1.25, .8, 1.2]);
        for (const sx of [-1, 1]) { const br = new TH.ConeGeometry(.28, 2.2, 4); br.rotateX(-Math.PI / 2 - .25); put(hd, new TH.Mesh(br, MG), [sx * .55, .62, .4], [0, sx * -.2, 0]); }
        put(hd, new TH.Mesh(new TH.BoxGeometry(.25, .18, 2.6), MG), [0, .62, .8]); }
      const jaw = put(hd, new TH.Group(), [0, -.25, -.4]); { const jg = new TH.CylinderGeometry(.42, .95, 2.7, 6); jg.rotateX(Math.PI / 2); jg.translate(0, 0, 1.25); put(jaw, new TH.Mesh(jg, MSk), [0, 0, 0], null, [1, .4, 1]); put(jaw, sph(CRM, 8), [0, .14, 1.1], null, [.62, .1, 1.1]); for (const sx of [-1, 1]) put(jaw, new TH.Mesh(new TH.ConeGeometry(.07, .45, 4), WHT), [sx * .35, .3, 2.0]); }
      put(hd, sph(CRM, 8), [0, -.1, 1.3], null, [.62, .14, 1.0]); for (const sx of [-1, 1]) { const fg = new TH.ConeGeometry(.13, 1.15, 5); fg.translate(0, -.55, 0); put(hd, new TH.Mesh(fg, WHT), [sx * .42, -.12, 2.05], [-.25, 0, 0]); put(hd, new TH.Mesh(new TH.ConeGeometry(.06, .4, 4), WHT), [sx * .22, -.1, 2.35], [Math.PI, 0, 0]);
        const e = sprite(2.6, "rgba(255,40,30,1)", "med_se"); e.position.set(sx * .66, .45, .75); hd.add(e); put(hd, sph(REDM, 8), [sx * .62, .4, .7], null, [.26, .14, .22]); }
      const pulse = sprite(5, "rgba(255,60,50,1)", "med_pu"); pulse.material.opacity = 0; g.add(pulse);
      snakes.push({ g, hd, jaw, pts, cur, pulse, a, i, cut: 0, base: g.quaternion.clone() }); }
    // crystal deposits and small ruins on her surface
    for (let i = 0; i < (LO ? 6 : 12); i++) { const u = (rnd() - .5) * 1.8, v = .55 + rnd() * .35, p = fp(u * .9, v, 0), n = p.clone().normalize(), c = put(head, cry(.5 + rnd() * .5, 1.6 + rnd() * 1.8, null, 5), p.toArray()); c.material = new TH.MeshStandardMaterial({ color: 0x2a0a18, emissive: 0xc01838, emissiveIntensity: .5, metalness: .4, roughness: .2, flatShading: true }); c.quaternion.setFromUnitVectors(V(0, 1, 0), n); }
    for (let i = 0; i < (LO ? 3 : 6); i++) { const u = (i / 5 - .5) * 1.6, p = fp(u, -.95 + (i % 2) * .08, 0), n = p.clone().normalize(), t = put(head, new TH.Group(), p.toArray()); t.quaternion.setFromUnitVectors(V(0, 1, 0), n); put(t, new TH.Mesh(new TH.BoxGeometry(.7, 1.6, .7), MSd), [0, .6, 0]); put(t, new TH.Mesh(new TH.ConeGeometry(.45, .9, 4), MSd), [0, 1.8, 0]); }
''' + s[b:]
rep("snakes.forEach((Sn, i) => { const cut = out.snk[i] ? 0 : 1;", "snakes.forEach((Sn, i) => { { const pu = ch < 0 ? -1 : ((T * .6 + i * .13) % 1); Sn.pulse.material.opacity = pu < 0 ? 0 : chg * (1 - Math.abs(pu - .5) * 1.2); if (pu >= 0) Sn.pulse.position.copy(Sn.cur.getPointAt(1 - pu)); } const cut = out.snk[i % 8] ? 0 : 1;")
# red-violet light in her fractures
rep('pal: ["#302c38"], slits: 0, sg: "#ff8a10", veins: 110, vc: "#9a6a28",', 'pal: ["#26222c"], slits: 0, sg: "#ff2a6a", veins: 110, vc: "#a07830",')
# three gold rings
rep("const RR = put(body, new TH.Group(), [0, 10, 0], [.3, 0, .2]); const ringR = 27;", "const RR2 = put(body, new TH.Group(), [0, 14, -2], [Math.PI / 2 - .25, .5, 0]); RR2.add(band(33, 1.0, .8, MG, 0, TAU, LO ? 60 : 120, 30)); const rr2 = put(RR2, runeRing(32, 0xffc060, .3), [0, 0, 0], [Math.PI / 2, 0, 0]);\n    const RR3 = put(body, new TH.Group(), [0, 14, -6], [.2, 0, -.5]); RR3.add(band(39, .8, .7, MG, .4, TAU * .7, LO ? 50 : 100, 22));\n    const RR = put(body, new TH.Group(), [0, 10, 0], [.3, 0, .2]); const ringR = 27;")
rep("RR.rotation.y = T * .05;", "RR.rotation.y = T * .05 * (1 + chg * 2); RR2.rotation.z = -T * .04 * (1 + chg * 2); RR3.rotation.y = T * .03; rr2.material.opacity = .28 * aw * live * (1 + chg); RR2.visible = RR3.visible = die < .95; out.dark = chg * .5 * live;")
# crimson-white beams with arcs
rep("beams.forEach((g, j) => { g.visible = fire > .02 && live > .2; if (!g.visible) return;", "eyeArc(t, (.3 + chg * 3 + fire * 6) * live * aw); beams.forEach((g, j) => { g.visible = fire > .02 && live > .2; if (!g.visible) return;")
rep("    const flare = sprite(24, \"rgba(255,90,60,1)\", \"med_fl\");", "    const eyeArc = bolts(head, LO ? 4 : 8, () => { const sx = rnd() < .5 ? -1 : 1, p = fp(sx * .32, .125, .02), q = fp(sx * (.32 + (rnd() - .5) * .5), .125 + (rnd() - .5) * .4, .02); return [p, q]; }, 0xd070ff);\n    const flare = sprite(24, \"rgba(255,90,60,1)\", \"med_fl\");")
rep("for (const [r, o, c] of [[1.4, .5, RED], [.45, 1, 0xffe0d0]])", "for (const [r, o, c] of [[2.2, .3, RED], [1.2, .6, 0xff5040], [.45, 1, 0xfff0e8]])")
rep("g.children[0].material.opacity = .5 * fire * (.85 + Math.random() * .15); g.children[1].material.opacity = fire; });", "g.children[0].material.opacity = .3 * fire * (.85 + Math.random() * .15); g.children[1].material.opacity = .6 * fire; g.children[2].material.opacity = fire; });")
# her new title
rep('med: { n: "Medusara", t: "The Stone Gaze", ev: "Gaze of the Gorgon"', 'med: { n: "Medusara", t: "The Petrified Star", ev: "Gaze of the Gorgon"')
rep('med: { n: "Medusara", t: "The Stone Gaze", m3: "medusara"', 'med: { n: "Medusara", t: "The Petrified Star", m3: "medusara"')
rep('med: ["◉", "Medusara, the Stone Gaze"]', 'med: ["◉", "Medusara, the Petrified Star"]')
rep('"▶ Watch Medusara, the Stone Gaze"', '"▶ Watch Medusara, the Petrified Star"')
rep('say("m1", "Medusara, the Stone Gaze. Her serpents are her eyes\' shield. All fleets, engage!");', 'say("m1", "Medusara, the Petrified Star. Her serpents are her eyes\' shield. All fleets, engage!");')
s = re.sub(r"GAME_V = 490\b", "GAME_V = 490", s)
open(P, 'w').write(s)
