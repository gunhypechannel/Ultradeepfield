# v495 Medusara's serpents like the owner's painting: thick bodies of silver-grey stone scales with gold light between them, in big
# S-curves, one smooth tapered body each (no striped segments, gold bands or crimson seams); heads in the same scales.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)

SCALES = r'''  // v495 serpent scales: rows of overlapping rounded scales, pale stone with dark rims; the light map is the gold between them
  const medScale = glow => paint(glow ? "medsclE" : "medscl", 512, (x, N) => { x.fillStyle = glow ? "#000" : "#3a3640"; x.fillRect(0, 0, N, N); const R = N / 8, H = R * .62;
    for (let row = -1; row < N / H + 1; row++) for (let c = -1; c < N / R + 1; c++) { const cx = c * R + (row % 2 ? R / 2 : 0), cy = row * H;
      x.beginPath(); x.moveTo(cx - R * .52, cy); x.quadraticCurveTo(cx - R * .5, cy + H * 1.25, cx, cy + H * 1.45); x.quadraticCurveTo(cx + R * .5, cy + H * 1.25, cx + R * .52, cy); x.closePath();
      if (glow) { x.strokeStyle = "rgba(255,190,90,1)"; x.lineWidth = N * .014; x.stroke(); }
      else { const gr = x.createLinearGradient(cx, cy, cx, cy + H * 1.45); gr.addColorStop(0, "#c4c0ca"); gr.addColorStop(.65, "#7e7a86"); gr.addColorStop(1, "#38343e"); x.fillStyle = gr; x.fill(); x.strokeStyle = "#1a161e"; x.lineWidth = N * .012; x.stroke();
        x.strokeStyle = "rgba(255,255,255,.25)"; x.lineWidth = N * .003; x.beginPath(); x.moveTo(cx, cy + H * .2); x.lineTo(cx, cy + H * 1.2); x.stroke(); } } }, true);
'''
rep('  function medusara() {', SCALES + '  function medusara() {')
rep('const MSk = new TH.MeshStandardMaterial({ color: 0x15121a, metalness: .85, roughness: .38, envMapIntensity: .55 }); MSk.userData.P = {};',
    'const MSk = new TH.MeshStandardMaterial({ color: 0x9a96a2, metalness: .7, roughness: .34, envMapIntensity: .55, map: medScale(0), emissiveMap: medScale(1), emissive: 0xffa83a, emissiveIntensity: 2.2 }); MSk.userData.P = {}; // v495 stone scales, gold between')
# bigger S-curves, then one tapered tube with the scales running along it
rep('w = Math.sin(u * Math.PI * 2 + i * 1.3) * 1.8 * (1 - u * .4);', 'w = Math.sin(u * Math.PI * 2 + i * 1.3) * 3.2 * (1 - u * .35);')
i0 = s.index('      const cur = new TH.CatmullRomCurve3(pts), NS = LO ? 12 : 20; for (let k = 0; k < NS; k++) {'); j = s.index('bd.scale.setScalar(r); } }', i0) + len('bd.scale.setScalar(r); } }')
assert j - i0 < 900
TUBE = r'''      const cur = new TH.CatmullRomCurve3(pts); { const TS = LO ? 40 : 80, RS = LO ? 10 : 16, tb = new TH.TubeGeometry(cur, TS, 1, RS, false), P2 = tb.attributes.position, U2 = tb.attributes.uv, c0 = V(0, 0, 0), q2 = V(0, 0, 0);
        for (let a2 = 0; a2 <= TS; a2++) { const u = a2 / TS, r = 2.4 * (1 - u * .52) * (1 + .06 * Math.sin(u * 40)); cur.getPointAt(u, c0); for (let b2 = 0; b2 <= RS; b2++) { const k2 = a2 * (RS + 1) + b2; q2.fromBufferAttribute(P2, k2).sub(c0).multiplyScalar(r).add(c0); P2.setXYZ(k2, q2.x, q2.y, q2.z); U2.setXY(k2, u * L * .17, b2 / RS * 1.5); } }
        tb.computeVertexNormals(); put(g, new TH.Mesh(tb, MSk), [0, 0, 0]); }'''
s = s[:i0] + TUBE + s[j:]
s = re.sub(r"GAME_V = 494\b", "GAME_V = 495", s)
open(P, 'w', encoding='utf-8').write(s); print('ok')
s = open(P, encoding='utf-8').read()
rep('color: 0x9a96a2, metalness: .7, roughness: .34, envMapIntensity: .55,', 'color: 0xb4b0bc, metalness: .7, roughness: .32, envMapIntensity: .6,')
rep('emissive: 0xffa83a, emissiveIntensity: 2.2 }', 'emissive: 0xffa83a, emissiveIntensity: .9 }')
# the face skin past the painting's edge: mirror the painting instead of stretching its border into streaks
rep('U[k * 2] = Math.min(1, Math.max(0, (px - X0) / CW)); U[k * 2 + 1] = Math.min(1, Math.max(0, 1 - (py - Y0) / CH)); }', 'U[k * 2] = (px - X0) / CW; U[k * 2 + 1] = 1 - (py - Y0) / CH; } tx.wrapS = tx.wrapT = TH.MirroredRepeatWrapping;')
open(P, 'w', encoding='utf-8').write(s)
