# v491: Khezaroth and Medusara modelled from the owner's paintings. Each is a relief mesh sculpted from a depth map of its
# reference art (Depth Anything V2 run on the painting), skinned with the painting itself, cut out of its background, and
# turned to face the camera so it always reads as the art. The game's own effects (beams, singularity, waves, anchors, death)
# stay on top. If the skin cannot load, the code-built model stays in place.
import sys
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

HELP = r'''  /* v491 a boss modelled from its own painting: a dense grid displaced by the painting's depth (sculpted from the art), the
     painting as its skin, cut out of the sky; it turns to face the viewer so it always reads as the art. Anchors (eyes, the
     singularity) are points on its surface for the effects. The code-built model stays until the skin has loaded. */
  const ARL = {};
  function artLoad(k, cb) { let L = ARL[k]; if (!L) { L = ARL[k] = { cbs: [] }; let n = 2; const done = () => { if (--n) return; L.ok = !L.bad; L.cbs.splice(0).forEach(f => f(L)); };
      const im = new Image(); im.onload = () => { const t = new TH.Texture(im); t.encoding = TH.sRGBEncoding; t.anisotropy = 8; t.needsUpdate = true; L.tex = t; done(); }; im.onerror = () => { L.bad = 1; done(); }; im.src = "art/boss/" + k + "-skin.webp";
      const dm = new Image(); dm.onload = () => { try { const c = cv(dm.width, dm.height), x = c.getContext("2d"); x.drawImage(dm, 0, 0); const d = x.getImageData(0, 0, dm.width, dm.height).data, a = new Float32Array(dm.width * dm.height); for (let i = 0; i < a.length; i++) a[i] = d[i * 4] / 255; L.dep = { a, w: dm.width, h: dm.height }; } catch (e) { L.bad = 1; } done(); }; dm.onerror = () => { L.bad = 1; done(); }; dm.src = "art/boss/" + k + "-depth.png"; }
    if (L.ok != null) cb(L); else L.cbs.push(cb); }
  function artRelief(par, o) { const g = new TH.Group(); g.position.set(0, o.cy, o.z); g.userData.dyn = 1; par.add(g); const A = { g, ok: 0, at: {}, mat: null };
    const W = o.iw * o.u, H = o.ih * o.u, x0 = -o.ox * o.u, y0 = o.oy * o.u; // the painting's pixel (ox, oy) sits at the group's origin
    for (const n in o.at) { const a = new TH.Object3D(); a.position.set(x0 + o.at[n][0] * o.u, y0 - o.at[n][1] * o.u, 0); g.add(a); A.at[n] = a; }
    artLoad(o.k, L => { if (!L.ok) return; const D = L.dep, smp = (u, v) => { const x = Math.min(D.w - 1.001, Math.max(0, u * (D.w - 1))), y = Math.min(D.h - 1.001, Math.max(0, v * (D.h - 1))), i = x | 0, j = y | 0, fx = x - i, fy = y - j, q = j * D.w + i;
        return (D.a[q] * (1 - fx) + D.a[q + 1] * fx) * (1 - fy) + (D.a[q + D.w] * (1 - fx) + D.a[q + D.w + 1] * fx) * fy; }, zf = d => Math.max(-o.d0 * o.D * .35, (d - o.d0) * o.D);
      const nx = LOD === 1 ? 110 : 220, ny = Math.round(nx * o.ih / o.iw), geo = new TH.PlaneGeometry(W, H, nx, ny); geo.translate(x0 + W / 2, y0 - H / 2, 0); const P = geo.attributes.position;
      for (let i = 0; i < P.count; i++) { const u = (P.getX(i) - x0) / W, v = (y0 - P.getY(i)) / H; P.setZ(i, zf(smp(u, v))); } geo.computeVertexNormals(); geo.computeBoundingSphere();
      for (const n in A.at) { const a = A.at[n], u = (a.position.x - x0) / W, v = (y0 - a.position.y) / H; a.position.z = zf(smp(u, v)) + .6; }
      const m = new TH.MeshBasicMaterial({ map: L.tex, transparent: true, alphaTest: .05, side: TH.DoubleSide, toneMapped: false }); const mesh = new TH.Mesh(geo, m); mesh.frustumCulled = false; g.add(mesh); A.mat = m; A.ok = 1;
      const cp = new TH.Vector3(); mesh.onBeforeRender = (r, sc, cam) => { if (!g.parent) return; cam.getWorldPosition(cp); g.parent.worldToLocal(cp); const dx = cp.x - g.position.x, dy = cp.y - g.position.y, dz = cp.z - g.position.z;
        g.rotation.set(-Math.atan2(dy, Math.hypot(dx, dz)) * (o.pitch != null ? o.pitch : .6), Math.atan2(dx, dz), 0); g.updateMatrixWorld(true); }; });
    A.step = () => { if (!A.ok) return; for (const h of o.hide) h.visible = false; g.visible = true; };
    A.wp = (n, par2, out) => { A.at[n].getWorldPosition(out); par2.worldToLocal(out); return out; }; return A; }
'''
rep('  function medusara() {', HELP + '  function medusara() {')

# --- Medusara: her painted face replaces the code-built head, serpent crown and front ring; the beams fire from her painted eyes ---
i0 = s.index('  function medusara() {'); END = '    out.tick = tick; tick(0); bake(body); return out; }'; j = s.index(END, i0)
MED = r'''    const AR = artRelief(body, { k: "medusara", iw: 1199, ih: 1060, u: .0266, ox: 697, oy: 543, cy: 14, z: 0, D: 16, d0: .55, at: { e0: [482, 360], e1: [718, 292], gem: [570, 192] }, hide: [head, RR, RR2, RR3, storm, ...snakes.map(S2 => S2.g)] }), btL = body.children[body.children.indexOf(stormS) + 1]; stormS.position.z = -16; // her storm glow sits behind the painted face, not over it
    const aE = [0, 1].map(j => { const s2 = sprite(9, "rgba(255,60,40,1)", "med_eye"); s2.material.opacity = 0; AR.at["e" + j].add(s2); return s2; }), aG = sprite(7, "rgba(255,70,90,1)", "med_gem"); aG.material.opacity = 0; AR.at.gem.add(aG);
    const gray2 = new TH.Color(.62, .62, .66), wv2 = new TH.Vector3();
    out.tick = t => { tick(t); if (!AR.ok) return; AR.step(); const fd = f("die", t), die = fd < 0 ? 0 : fd, fl = f("lunge", t), fs = f("storm", t), ch = f("charge", t), T = t * .001;
      AR.mat.opacity = 1 - ss(.6, .97, die); AR.mat.color.setRGB(1, 1, 1).lerp(gray2, ss(.08, .4, die)); AR.g.position.z = bell(fl, .1, .3, .55, .85) * 5; AR.g.position.x = bell(fs, .1, .2, .8, .95) * Math.sin(T * 40) * .25; AR.g.scale.setScalar(1 + Math.sin(T * .5) * .006 + (ch < 0 ? 0 : ss(0, .7, ch) * (1 - ss(.94, 1, ch))) * .02);
      eyes.forEach((E, j) => { aE[j].material.opacity = E.s.material.opacity * .8; aE[j].scale.setScalar(E.s.scale.x * .8); }); aG.material.opacity = gemS.material.opacity * .7; aG.scale.setScalar(gemS.scale.x * .8);
      if (btL && btL.isLineSegments) btL.visible = bell(fs, .05, .2, .8, .95) > .02 || (ch >= 0 && ch > .3);
      beams.forEach((g, j) => { if (g.visible) g.position.copy(AR.wp("e" + j, body, wv2)); }); };
'''
s = s[:j] + MED + '    tick(0); bake(body); return out; }' + s[j + len(END):]

# --- Khezaroth: the painted sphinx replaces the code-built body, crown pyramids and tilted ring; the singularity sits in the painted one ---
i0 = s.index('  function khezaroth() {'); j = s.index(END, i0); assert j < s.index('  function medusara() {')
KHZ = r'''    const AR = artRelief(body, { k: "khezaroth", iw: 1024, ih: 1180, u: .0288, ox: 685, oy: 954, cy: 3.6, z: 6, D: 18, d0: .3, at: { hole: [685, 954], e0: [614, 209], e1: [717, 209], gem: [701, 595] }, hide: [hull, portal, portalC, RB, bhHz, bhRing, disc, ...pyrs.map(p => p.g)] });
    const aE = [0, 1].map(j => { const s2 = sprite(3.2, "rgba(200,120,255,1)", "khz_ae"); AR.at["e" + j].add(s2); return s2; }), aG = sprite(9, "rgba(190,110,255,1)", "khz_ag"); aG.material.opacity = 0; AR.at.gem.add(aG);
    const gray2 = new TH.Color(.55, .52, .6), wv2 = new TH.Vector3();
    out.tick = t => { tick(t); if (!AR.ok) return; if (out.relic) { AR.g.visible = false; return; } AR.step(); const fd = f("die", t), die = fd < 0 ? 0 : fd, T = t * .001, aw = drv.awake != null ? drv.awake : 1;
      const fc = f("claw", t), fk = f("crush", t), fp2 = f("pulse", t), fj = f("judge", t), fb = f("barrage", t), jd = bell(fj, .05, .2, .85, .97);
      AR.mat.opacity = 1 - ss(.5, .78, die); AR.mat.color.setRGB(1, 1, 1).lerp(gray2, ss(.05, .45, die) + (1 - aw) * .5);
      AR.g.position.z = 6 + bell(fc, .15, .35, .55, .85) * 4; AR.g.position.y = 3.6 - bell(fk, .2, .35, .5, .8) * 1.6 + jd * 1.2 + Math.sin(T * .4) * .25; AR.g.scale.setScalar(1 + bell(fp2, .1, .25, .4, .8) * .035 + jd * .04);
      aE.forEach((s2, j) => { s2.material.opacity = (.55 + .25 * Math.sin(T * 2.4 + j) + jd * .6 + bell(fb, .1, .2, .7, .9) * .5) * aw * (1 - ss(.3, .6, die)); s2.scale.setScalar(3.2 * (1 + jd * 1.5)); });
      aG.material.opacity = (bell(fp2, .05, .2, .4, .8) + jd + bell(fb, .1, .2, .7, .9) * .6) * (1 - ss(.3, .6, die)); aG.scale.setScalar(9 * (1 + jd));
      AR.wp("hole", body, wv2); BH.position.copy(wv2); BW.position.copy(wv2); };
'''
s = s[:j] + KHZ + '    tick(0); bake(body); return out; }' + s[j + len(END):]
open(P, 'w', encoding='utf-8').write(s)
print('ok')
import re
s = open(P, encoding='utf-8').read(); s2 = re.sub(r"GAME_V = 490\b", "GAME_V = 491", s); assert s2 != s; open(P, 'w', encoding='utf-8').write(s2)
s = open(P, encoding='utf-8').read()
a = 'root.BOSS3D = { init(T) { TH = T; },'
assert s.count(a) == 1
s = s.replace(a, 'root.BOSS3D = { init(T) { TH = T; if (!ARL.medusara) setTimeout(() => { try { artLoad("khezaroth", () => {}); artLoad("medusara", () => {}); } catch (e) {} }, 0); }, artLoad,')
open(P, 'w', encoding='utf-8').write(s)
