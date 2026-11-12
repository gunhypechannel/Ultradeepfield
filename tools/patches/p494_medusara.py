# v494 Medusara (owner): "Smoothen Medusara's face and make it look more like a petrified star, the snakes' eyes and teeth should look
# different and more convincing, they look silly; the snakes should move more randomly and independently".
#  - the face: pale starstone instead of dark rock covered in red veins: smooth (low relief), a few fine fractures with a gold-white
#    star's light behind them, warm inner glow, and a soft stellar corona behind her head that breathes and flares as she charges
#  - the serpents: slit-pupil amber eyes set under a brow ridge (small glow, no big red blobs); smaller curved ivory fangs and rows of
#    small teeth along both jaws (no long white spikes)
#  - the serpents move on their own: each has its own slow drift (three mixed frequencies, own phases), looks around with its head,
#    darts at random moments, opens its jaws to hiss at random
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)

# --- the face: smooth petrified starstone, fine glowing fractures ---
rep('const MS = hullMat("med", { rows: 1, cols: 1, pal: ["#26222c"], slits: 0, sg: "#ff2a6a", veins: 110, vc: "#a07830", metal: .15, rough: .9, rc: [.75, .45, 1], ei: 1.5, rep: [1, 1], relief: 3.6, n: 1024, rust: 0 }); MS.envMapIntensity = .45; MS.normalScale.set(2.6, 2.6);',
    'const MS = hullMat("med3", { rows: 1, cols: 1, pal: ["#57535e"], slits: 0, sg: "#ffc860", veins: 48, vc: "#ffd890", metal: .12, rough: .7, rc: [1, .8, .55], ei: 2.6, rep: [1, 1], relief: 1.1, n: 1024, rust: 0 }); MS.envMapIntensity = .35; MS.normalScale.set(1, 1); // v494 petrified starstone')
# the stellar corona behind her head
CORONA = r'''    // v494 a petrified star: its light still burns behind the stone, a soft corona round her head
    const coro = sprite(70, "rgba(255,214,140,1)", "med_coro"); coro.position.set(0, 0, -8); coro.material.opacity = .45; head.add(coro); const coro2 = sprite(40, "rgba(255,245,220,1)", "med_coro2"); coro2.position.set(0, 0, -6); coro2.material.opacity = .35; head.add(coro2);
'''
rep('    const shine = sprite(40, "rgba(255,190,90,1)", "med_shine");', CORONA + '    const shine = sprite(40, "rgba(255,190,90,1)", "med_shine");')

# --- the serpents' mouths and eyes ---
rep('for (const sx of [-1, 1]) put(jaw, new TH.Mesh(new TH.ConeGeometry(.07, .45, 4), WHT), [sx * .35, .3, 2.0]); }',
    'for (const sx of [-1, 1]) for (let q = 0; q < 6; q++) put(jaw, new TH.Mesh(TOOTH, IVO), [sx * (.36 - q * .03), .2, 2.05 - q * .26], [.15, 0, 0], [.75, .8 - q * .07, .75]); }')
rep('''      put(hd, sph(CRM, 8), [0, -.1, 1.3], null, [.62, .14, 1.0]); for (const sx of [-1, 1]) { const fg = new TH.ConeGeometry(.13, 1.15, 5); fg.translate(0, -.55, 0); put(hd, new TH.Mesh(fg, WHT), [sx * .42, -.12, 2.05], [-.25, 0, 0]); put(hd, new TH.Mesh(new TH.ConeGeometry(.06, .4, 4), WHT), [sx * .22, -.1, 2.35], [Math.PI, 0, 0]);
        const e = sprite(2.6, "rgba(255,40,30,1)", "med_se"); e.position.set(sx * .66, .45, .75); hd.add(e); put(hd, sph(REDM, 8), [sx * .62, .4, .7], null, [.26, .14, .22]); }''',
    '''      put(hd, sph(CRM, 8), [0, -.1, 1.3], null, [.62, .14, 1.0]); for (const sx of [-1, 1]) { put(hd, new TH.Mesh(FANG, IVO), [sx * .4, -.12, 2.0], [.25, 0, sx * .1]); for (let q = 0; q < 5; q++) put(hd, new TH.Mesh(TOOTH, IVO), [sx * (.34 - q * .03), -.16, 1.75 - q * .26], [Math.PI - .15, 0, 0], [.7, .7 - q * .06, .7]);
        put(hd, new TH.Mesh(new TH.BoxGeometry(.5, .14, .55), MSk), [sx * .6, .6, .72], [.25, sx * -.35, sx * .2]); // the brow ridge over the eye
        const eg = put(hd, new TH.Group(), [sx * .64, .4, .74], [0, sx * .5, 0]); put(eg, sph(SEYE, 10), [0, 0, 0], null, [.2, .13, .12]); put(eg, new TH.Mesh(new TH.BoxGeometry(.035, .2, .02), SPUP), [0, 0, .115]);
        const e = sprite(1.1, "rgba(255,150,40,1)", "med_se2"); e.position.set(0, 0, .15); e.material.opacity = .7; eg.add(e); }''')
MATS = r'''    // v494 the serpents' teeth and eyes: ivory, curved; amber eyes with a slit pupil
    const IVO = new TH.MeshStandardMaterial({ color: 0xd8cbb0, roughness: .45, metalness: .05, envMapIntensity: .6 }); IVO.userData.P = {};
    const FANG = (() => { const g = new TH.ConeGeometry(.075, .75, 6, 4); g.translate(0, -.375, 0); const p = g.attributes.position; for (let k = 0; k < p.count; k++) { const y = p.getY(k); p.setZ(k, p.getZ(k) - (y * y) * .45); } g.computeVertexNormals(); return g; })();
    const TOOTH = new TH.ConeGeometry(.035, .2, 4); TOOTH.translate(0, -.1, 0);
    const SEYE = new TH.MeshBasicMaterial({ color: 0xffa020, toneMapped: false }), SPUP = new TH.MeshBasicMaterial({ color: 0x080200 });
'''
rep('    const NSN = 9, snakes = [];', MATS + '    const NSN = 9, snakes = [];')

# --- the serpents move on their own ---
rep('const ln = fl < 0 ? 0 : bell(fl, .1 + (i % 4) * .05, .3 + (i % 4) * .05, .55, .85), sw = Math.sin(T * 1.3 + i * 1.7) * .12 * coil;',
    '''const ln = fl < 0 ? 0 : bell(fl, .1 + (i % 4) * .05, .3 + (i % 4) * .05, .55, .85);
        if (!Sn.n) Sn.n = { f: [.3 + rnd() * .5, .45 + rnd() * .7, .2 + rnd() * .45], p: [rnd() * 9, rnd() * 9, rnd() * 9], dt: rnd() * 6, d0: -9, ht: rnd() * 5, h0: -9, q0: Sn.hd.quaternion.clone(), qq: new TH.Quaternion(), e: new TH.Euler() };
        const N = Sn.n; if (T > N.dt) { N.d0 = T; N.dt = T + 3 + rnd() * 9; } if (T > N.ht) { N.h0 = T; N.ht = T + 2 + rnd() * 7; } const dk = T - N.d0, dart = dk < .8 ? Math.sin(dk / .8 * Math.PI) ** 2 : 0, hk = T - N.h0, hiss = hk < 1.4 ? Math.sin(hk / 1.4 * Math.PI) : 0;
        const nx = Math.sin(T * N.f[0] + N.p[0]) * .6 + Math.sin(T * N.f[1] * 1.7 + N.p[1]) * .4, ny = Math.sin(T * N.f[1] + N.p[1]) * .6 + Math.sin(T * N.f[2] * 2.3 + N.p[2]) * .4, nz = Math.sin(T * N.f[2] + N.p[2]) * .7 + Math.sin(T * N.f[0] * 2.9 + N.p[1]) * .3;
        N.e.set((Math.sin(T * N.f[2] * 1.9 + N.p[0]) * .22 - dart * .25) * coil, Math.sin(T * N.f[0] * 1.4 + N.p[2]) * .38 * coil, Math.sin(T * N.f[1] * .8 + N.p[0]) * .15 * coil); N.qq.setFromEuler(N.e); Sn.hd.quaternion.copy(N.q0).multiply(N.qq);''')
rep('Sn.g.rotation.set(-ln * .9 + chg * -.25 + (1 - coil) * .8, sw + Math.sin(Sn.a) * ln * .2, Math.sin(T * .9 + i) * .08 + (1 - coil) * Math.sign(Sn.a) * .6);',
    'Sn.g.rotation.set(-ln * .9 - dart * .4 + chg * -.25 + (1 - coil) * .8 + nx * .17 * coil, ny * .22 * coil + Math.sin(Sn.a) * ln * .2, nz * .14 * coil + (1 - coil) * Math.sign(Sn.a) * .6);')
rep('Sn.jaw.rotation.x = .3 + ln * .5 + chg * .35 + Math.max(0, Math.sin(T * 2 + i)) * .12;', 'Sn.jaw.rotation.x = .14 + ln * .45 + chg * .3 + hiss * .35 + dart * .4;')

# --- the corona breathes, flares while she charges, goes out as she dies ---
rep('cracks.material.opacity = Math.max(sh * (.7 + .3 * Math.sin(T * 5)), bell(die, .05, .2, .5, .7));',
    'cracks.material.opacity = Math.max(sh * (.7 + .3 * Math.sin(T * 5)), bell(die, .05, .2, .5, .7)); coro.material.opacity = (.32 + .08 * Math.sin(T * .7) + chg * .35 + sh * .3) * aw * live; coro.scale.setScalar(70 * (1 + chg * .25 + .04 * Math.sin(T * .5))); coro2.material.opacity = (.25 + chg * .3) * aw * live;')
s = re.sub(r"GAME_V = 493\b", "GAME_V = 494", s)
open(P, 'w', encoding='utf-8').write(s); print('ok')
s = open(P, encoding='utf-8').read()
# the mouths: a dark wet red inside, not the glowing crimson of the seams
rep('put(jaw, sph(CRM, 8), [0, .14, 1.1], null, [.62, .1, 1.1]);', 'put(jaw, sph(MOU, 8), [0, .14, 1.1], null, [.62, .1, 1.1]);')
rep('      put(hd, sph(CRM, 8), [0, -.1, 1.3], null, [.62, .14, 1.0]); for (const sx of [-1, 1]) { put(hd, new TH.Mesh(FANG, IVO)', '      put(hd, sph(MOU, 8), [0, -.1, 1.3], null, [.62, .14, 1.0]); for (const sx of [-1, 1]) { put(hd, new TH.Mesh(FANG, IVO)')
rep("    const SEYE = new TH.MeshBasicMaterial({ color: 0xffa020, toneMapped: false }), SPUP = new TH.MeshBasicMaterial({ color: 0x080200 });",
    "    const SEYE = new TH.MeshBasicMaterial({ color: 0xffa020, toneMapped: false }), SPUP = new TH.MeshBasicMaterial({ color: 0x080200 }), MOU = new TH.MeshStandardMaterial({ color: 0x4a0a10, roughness: .35, metalness: 0, emissive: 0x1a0204 }); MOU.userData.P = {};")
open(P, 'w', encoding='utf-8').write(s)
s = open(P, encoding='utf-8').read()
# viper heads: a smooth wedge skull (wide at the back, tapering to the snout, flat underneath) and a shallow lower jaw, in place of
# the six-sided cylinders; a softer rim light so the heads don't glow pink
rep('rimOn(MSk, .45, [1, .3, .25]);', 'rimOn(MSk, .3, [.9, .45, .35]);')
VH = r'''    const VH = top => { const g = new TH.SphereGeometry(1, LO ? 14 : 26, LO ? 10 : 18), p = g.attributes.position; for (let k = 0; k < p.count; k++) { let x = p.getX(k), y = p.getY(k); const z = p.getZ(k), zz = -.9 + (z + 1) / 2 * 3.3, u = (zz + .9) / 3.3, w = 1.02 - .56 * u * u, h = .62 - .3 * u;
        x *= w * (1 + .08 * Math.max(0, y)); y = top ? Math.max(y, -.1) * h : Math.min(y, .1) * h * .5; p.setXYZ(k, x, y, zz); } g.computeVertexNormals(); return g; }, VHT = VH(1), VHJ = VH(0);
'''
rep('    const NSN = 9, snakes = [];', VH + '    const NSN = 9, snakes = [];')
rep('{ const sk = new TH.CylinderGeometry(.55, 1.15, 3.0, 6); sk.rotateX(Math.PI / 2); sk.translate(0, 0, 1.1); put(hd, new TH.Mesh(sk, MSk), [0, .2, 0], null, [1.1, .55, 1]); put(hd, sph(MSk, 12), [0, .15, -.4], null, [1.25, .8, 1.2]);',
    '{ put(hd, new TH.Mesh(VHT, MSk), [0, .08, 0]);')
rep('{ const jg = new TH.CylinderGeometry(.42, .95, 2.7, 6); jg.rotateX(Math.PI / 2); jg.translate(0, 0, 1.25); put(jaw, new TH.Mesh(jg, MSk), [0, 0, 0], null, [1, .4, 1]);',
    '{ put(jaw, new TH.Mesh(VHJ, MSk), [0, .04, .45], null, [.9, 1, .88]);')
open(P, 'w', encoding='utf-8').write(s)
s = open(P, encoding='utf-8').read()
rep('MOU = new TH.MeshStandardMaterial({ color: 0x4a0a10, roughness: .35, metalness: 0, emissive: 0x1a0204 }); MOU.userData.P = {};', 'MOU = new TH.MeshStandardMaterial({ color: 0x160205, roughness: .8, metalness: 0, envMapIntensity: .08 }); MOU.userData.P = {};')
rep('const br = new TH.ConeGeometry(.28, 2.2, 4); br.rotateX(-Math.PI / 2 - .25); put(hd, new TH.Mesh(br, MG), [sx * .55, .62, .4], [0, sx * -.2, 0]);',
    'const br = new TH.ConeGeometry(.12, 1.1, 6); br.rotateX(-Math.PI / 2 - .35); put(hd, new TH.Mesh(br, MG), [sx * .5, .5, -.1], [0, sx * -.25, 0]);')
rep('put(hd, new TH.Mesh(new TH.BoxGeometry(.25, .18, 2.6), MG), [0, .62, .8]);', 'put(hd, new TH.Mesh(new TH.BoxGeometry(.08, .06, 1.7), MG), [0, .56, .5], [.1, 0, 0]);')
open(P, 'w', encoding='utf-8').write(s)
