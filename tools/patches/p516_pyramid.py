# v516 the pyramid station remastered after the owner's painting: dark stone faces banded with glowing gold hieroglyphs, a pharaoh's
# face and two jackal guardians over a blue-lit hangar gate on every face, a gold capstone beam into the sky, a stepped underside with
# a ring engine and a beam below, blue-lit terraces at the waist, four obelisk towers, and a broken orbital ring with gold lights
# turning round the apex. Still one master per lit/dark state, merged, so each station on the map costs the same few draw calls.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)

i0 = s.index('function pyrKit(W) {'); i1 = s.index('/* the open-orbit layer:', i0)
s = s[:i0] + r'''function pyrKit(W) {
  if (W.pyrK) return W.pyrK;
  /* v516 dark basalt blocks; u runs round the four faces, v from the base (0) to the apex (1) */
  const BANDS = [.06, .2, .37, .55, .72];
  const panel = texCanvas(1024, 512, (x, w, h) => { const r = rnd(808); x.fillStyle = "#211d19"; x.fillRect(0, 0, w, h);
    for (let row = 0; row < 32; row++) { const bh = h / 32, off = (row % 2) * 18; for (let i = -1; i < 30; i++) { const k = 26 + r() * 22; x.fillStyle = `rgb(${k + 8},${k + 4},${k})`; x.fillRect(i * 36 + off + 1, row * bh + 1, 34, bh - 2); } }
    for (let i = 0; i < 400; i++) { x.fillStyle = `rgba(${r() < .5 ? "0,0,0" : "120,100,70"},${.15 + r() * .2})`; x.fillRect(r() * w, r() * h, 1 + r() * 6, 1 + r() * 3); }
    for (const b of BANDS) { const y = (1 - b) * h; x.fillStyle = "#6a5228"; x.fillRect(0, y - 7, w, 14); } });
  /* the glow: gold bands, columns of glyphs between them (ankhs, eyes, birds, cartouches), and windows of warm light */
  const lights = texCanvas(1024, 512, (x, w, h) => { const r = rnd(809); x.fillStyle = "#000"; x.fillRect(0, 0, w, h);
    x.fillStyle = "rgba(255,190,70,1)"; for (const b of BANDS) { const y = (1 - b) * h; x.fillRect(0, y - 3, w, 6); x.fillStyle = "rgba(255,150,40,.5)"; x.fillRect(0, y - 7, w, 2); x.fillRect(0, y + 5, w, 2); x.fillStyle = "rgba(255,190,70,1)"; }
    x.strokeStyle = "rgba(255,200,90,.95)"; x.lineWidth = 2.2; x.lineCap = "round";
    const glyph = (cx, cy, s, t) => { x.beginPath();
      if (t === 0) { x.arc(cx, cy - s * .45, s * .22, 0, TAU); x.moveTo(cx, cy - s * .23); x.lineTo(cx, cy + s * .5); x.moveTo(cx - s * .3, cy - s * .05); x.lineTo(cx + s * .3, cy - s * .05); } // ankh
      else if (t === 1) { x.ellipse(cx, cy, s * .42, s * .2, 0, 0, TAU); x.moveTo(cx + s * .06, cy); x.arc(cx, cy, s * .08, 0, TAU); x.moveTo(cx - s * .1, cy + s * .2); x.lineTo(cx - s * .2, cy + s * .48); } // eye
      else if (t === 2) { x.moveTo(cx - s * .4, cy + s * .4); x.lineTo(cx - s * .1, cy - s * .1); x.lineTo(cx + s * .15, cy - s * .35); x.lineTo(cx + s * .35, cy - s * .3); x.moveTo(cx - s * .1, cy - s * .1); x.lineTo(cx + s * .3, cy + s * .2); x.lineTo(cx - s * .2, cy + s * .45); } // bird
      else if (t === 3) { x.roundRect ? x.roundRect(cx - s * .22, cy - s * .48, s * .44, s * .96, s * .2) : x.rect(cx - s * .22, cy - s * .48, s * .44, s * .96); x.moveTo(cx - s * .12, cy - s * .2); x.lineTo(cx + s * .12, cy - s * .2); x.moveTo(cx - s * .12, cy + s * .12); x.lineTo(cx + s * .12, cy + s * .12); } // cartouche
      else { x.moveTo(cx - s * .35, cy + s * .4); x.lineTo(cx, cy - s * .45); x.lineTo(cx + s * .35, cy + s * .4); x.closePath(); } // pyramid
      x.stroke(); };
    for (let k = 0; k < BANDS.length - 1; k++) { const y0 = (1 - BANDS[k + 1]) * h + 10, y1 = (1 - BANDS[k]) * h - 10, s = Math.min(26, (y1 - y0) * .8); if (s < 10) continue;
      for (let i = 0; i < 40; i++) { if (r() < .35) continue; const cx = 12 + i * (w / 40), cy = (y0 + y1) / 2; glyph(cx, cy, s, (r() * 5) | 0); } }
    for (let i = 0; i < 220; i++) { const y = (1 - (.78 + r() * .2)) * h; x.fillStyle = r() < .8 ? "rgba(255,200,110,1)" : "rgba(120,210,255,1)"; x.fillRect(r() * w, y, 3, 2); } });
  panel.encoding = TH.sRGBEncoding; panel.wrapS = panel.wrapT = lights.wrapS = lights.wrapT = TH.RepeatWrapping;
  const hullGeo = new TH.ConeGeometry(1, 1.15, 4, 6), lowGeo = new TH.ConeGeometry(1, .55, 4, 3); hullGeo.rotateY(Math.PI / 4); lowGeo.rotateY(Math.PI / 4); lowGeo.rotateX(Math.PI);
  const M = (o) => new TH.MeshStandardMaterial(o), B = (c, o) => new TH.MeshBasicMaterial(Object.assign({ color: c, toneMapped: false }, o || {}));
  return (W.pyrK = { hullGeo, lowGeo,
    hull: M({ map: panel, emissiveMap: lights, emissive: 0xffffff, emissiveIntensity: 1.5, metalness: .35, roughness: .55, flatShading: true }), // the map scene has no environment map, so very metallic hulls would render black
    hullOff: M({ map: panel, metalness: .35, roughness: .6, flatShading: true, color: 0x8a8070 }),
    dark: M({ color: 0x2a2724, metalness: .5, roughness: .45 }), gold: M({ color: 0xd8a54a, metalness: .6, roughness: .3, emissive: 0x5a3800, emissiveIntensity: .8 }),
    goldOff: M({ color: 0x6a5430, metalness: .5, roughness: .5 }),
    rail: B(0xffa828), railOff: B(0x5a4628), blue: B(0x2f9cff), blueOff: B(0x1a2a36), beam: B(0xffc860, { transparent: true, opacity: .55, blending: TH.AdditiveBlending, depthWrite: false }),
    solar: M({ color: 0x1b2f5a, metalness: .6, roughness: .2, emissive: 0x0a1a3a, emissiveIntensity: .6 }),
    ringGeo: new TH.TorusGeometry(1.75, .07, 10, 72), armGeo: new TH.BoxGeometry(.06, .06, 1.1), padGeo: new TH.BoxGeometry(.3, .08, .22), railGeo: new TH.CylinderGeometry(.018, .018, 1, 6) });
}
function pyramidObj(W, y) {
  const K = pyrKit(W);
  // the static hull is built once (lit and dark versions) and merged into a few meshes; each station only clones it
  if (!W.pyrMaster) { const build = on => { const st = new TH.Group(), G = on ? K.gold : K.goldOff, BL = on ? K.blue : K.blueOff, D = K.dark;
      const put = (geo, mat, x, y, z) => { const m = new TH.Mesh(geo, mat); m.position.set(x || 0, y || 0, z || 0); st.add(m); return m; };
      const hull = new TH.Mesh(K.hullGeo, on ? K.hull : K.hullOff); hull.position.y = .575; st.add(hull);
      const corner = i => { const a = Math.PI / 4 + i * Math.PI / 2; return new TH.Vector3(Math.cos(a), 0, Math.sin(a)); };
      const railTo = (a, b, mat, w) => { const m = new TH.Mesh(K.railGeo, mat || (on ? K.rail : K.railOff)), d = b.clone().sub(a); m.position.copy(a).add(b).multiplyScalar(.5); m.scale.set(w || 1, d.length(), w || 1); m.quaternion.setFromUnitVectors(new TH.Vector3(0, 1, 0), d.normalize()); st.add(m); };
      const apex = new TH.Vector3(0, 1.15, 0);
      for (let i = 0; i < 4; i++) { const c = corner(i).multiplyScalar(1.01); railTo(c, apex, null, 1.6); railTo(c, corner(i + 1).multiplyScalar(1.01)); }
      // the waist: two terraces lit blue, stepping out past the base
      for (const [w, yy, h] of [[1.62, .0, .07], [1.5, -.08, .06]]) { put(new TH.BoxGeometry(w, h, w), D, 0, yy, 0).rotation.y = 0; put(new TH.BoxGeometry(w + .02, .015, w + .02), BL, 0, yy + h / 2 - .004, 0); }
      // the underside: stepped tiers down to a ring engine, with a gold beam below
      for (const [w, yy] of [[1.25, -.17], [1.0, -.26], [.74, -.34], [.5, -.41]]) { put(new TH.BoxGeometry(w, .085, w), D, 0, yy, 0); put(new TH.BoxGeometry(w + .015, .012, w + .015), G, 0, yy - .045, 0); }
      const eng = put(new TH.TorusGeometry(.2, .045, 10, 40), G, 0, -.47, 0); eng.rotation.x = Math.PI / 2;
      put(new TH.CylinderGeometry(.16, .12, .05, 32), on ? K.rail : K.railOff, 0, -.48, 0);
      if (on) { const bm = put(new TH.CylinderGeometry(.03, .09, 1.2, 12, 1, true), K.beam, 0, -1.08, 0); const up = put(new TH.CylinderGeometry(.015, .05, 1.6, 12, 1, true), K.beam, 0, 1.95, 0); }
      // every face: a hangar gate lit blue, two jackal guardians beside it, and a pharaoh's face above
      const tilt = Math.atan2(.707, 1.15);
      for (let i = 0; i < 4; i++) { const a = i * Math.PI / 2, f = new TH.Group(); f.rotation.y = -a + Math.PI / 2; st.add(f);
        const onFace = (h, lat, out) => { const g2 = new TH.Group(); g2.position.set(lat, h, .707 * (1 - h / 1.15) + (out || 0)); g2.rotation.x = -tilt; f.add(g2); return g2; };
        const gate = onFace(.12, 0, .012); const gp = (geo, mat, x, y, z) => { const m = new TH.Mesh(geo, mat); m.position.set(x, y, z); gate.add(m); return m; };
        gp(new TH.BoxGeometry(.3, .2, .03), G, 0, 0, -.01); gp(new TH.PlaneGeometry(.22, .15), BL, 0, -.01, .008);
        for (const sd of [1, -1]) { const j = new TH.Group(); j.position.set(sd * .24, .05, .03); j.rotation.x = tilt; gate.add(j); const jp = (geo, mat, x, y, z) => { const m = new TH.Mesh(geo, mat); m.position.set(x, y, z); j.add(m); return m; };
          jp(new TH.BoxGeometry(.06, .05, .09), D, 0, -.06, 0); jp(new TH.BoxGeometry(.045, .09, .045), D, 0, .0, -.01); jp(new TH.BoxGeometry(.035, .03, .055), D, 0, .06, .015);
          for (const ex of [-.012, .012]) { const ear = jp(new TH.ConeGeometry(.008, .04, 4), G, ex, .09, 0); } jp(new TH.SphereGeometry(.006, 6, 4), BL, 0, .065, .044); }
        const ph = onFace(.56, 0, .006), pp = (geo, mat, x, y, z) => { const m = new TH.Mesh(geo, mat); m.position.set(x, y, z); ph.add(m); return m; };
        const nemes = pp(new TH.CylinderGeometry(.06, .13, .2, 4, 1), G, 0, -.01, 0); nemes.rotation.y = Math.PI / 4; nemes.scale.z = .25;
        pp(new TH.BoxGeometry(.075, .1, .03), D, 0, -.02, .02); pp(new TH.BoxGeometry(.02, .05, .02), G, 0, -.09, .025);
        for (const ex of [-.018, .018]) pp(new TH.BoxGeometry(.018, .007, .006), on ? K.rail : K.railOff, ex, .005, .037);
        for (const sd of [1, -1]) for (let k = 0; k < 3; k++) { const col = onFace(.3 + k * .02, sd * (.18 + k * .02), .004); col.add(new TH.Mesh(new TH.BoxGeometry(.012, .1, .006), on ? K.rail : K.railOff)); } }
      // four obelisk towers at the corners of the upper terrace, tipped with blue light
      for (let i = 0; i < 4; i++) { const c = corner(i).multiplyScalar(1.08); const ob = put(new TH.CylinderGeometry(.02, .05, .55, 4), D, c.x, .27, c.z); ob.rotation.y = Math.PI / 4; put(new TH.OctahedronGeometry(.03, 0), BL, c.x, .57, c.z); put(new TH.BoxGeometry(.11, .02, .11), G, c.x, .02, c.z); }
      const spire = new TH.Mesh(K.railGeo, G); spire.scale.set(1.2, .3, 1.2); spire.position.y = 1.25; st.add(spire);
      return mergeGroup(st); };
    // the orbital ring round the apex: broken into arcs, tilted, with gold-lit modules and two docking spurs
    const ring = new TH.Group();
    for (let k = 0; k < 3; k++) { const arc = new TH.Mesh(new TH.TorusGeometry(1.45, .028, 8, 48, TAU / 3 - .35), K.dark); arc.rotation.set(Math.PI / 2, 0, k * TAU / 3); ring.add(arc);
      const glow = new TH.Mesh(new TH.TorusGeometry(1.45, .012, 6, 48, TAU / 3 - .35), K.rail); glow.rotation.set(Math.PI / 2, 0, k * TAU / 3); glow.position.y = .028; ring.add(glow);
      for (let j = 0; j < 4; j++) { const a = k * TAU / 3 + .15 + j * .45, m = new TH.Mesh(K.padGeo, K.gold); m.position.set(Math.cos(a) * 1.45, 0, -Math.sin(a) * 1.45); m.rotation.y = a; m.scale.set(.35, .6, .55); ring.add(m); } }
    W.pyrMaster = { lit: build(true), off: build(false), ring: mergeGroup(ring) }; }
  const M = W.pyrMaster, grp = new TH.Group(), s = 1.2 + y.lvl * .17, st = new TH.Group(); st.scale.setScalar(s); grp.add(st);
  const lit = M.lit.clone(), off = M.off.clone(); off.visible = false; st.add(lit, off);
  const ring = M.ring.clone(); ring.position.y = .78; ring.rotation.x = .18; const rh = new TH.Group(); rh.add(ring); st.add(rh);
  const cap = new TH.Mesh(W.pyrCap || (W.pyrCap = new TH.OctahedronGeometry(.11, 0)), new TH.MeshBasicMaterial({ color: 0xffd36b, toneMapped: false })); cap.position.y = 1.2; cap.scale.y = 1.6; st.add(cap);
  const beacon = new TH.Sprite(W.additive(W.glow.pyr || (W.glow.pyr = glowTex("255,210,110", .95)), 0xffffff, .9)); beacon.position.y = 1.25 * s; beacon.scale.setScalar(3 * s); grp.add(beacon);
  W.scene.add(grp);
  const o = { grp, ring, beacon, cap, lit: true };
  o.setLit = on => { if (o.lit === on) return; o.lit = on; lit.visible = on; off.visible = !on; };
  return o;
}''' + s[i1:]
s2 = re.sub(r"GAME_V = 515\b", "GAME_V = 516", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
