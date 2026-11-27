"""v816: monsters glow (owner: "Add more glow and Effect and HDR"). The galaxy has no bloom pass, so the light is in the monsters
themselves: their glowing parts burn past white into the ACES curve (HDR, x1.7), a rim of their own colour wraps every silhouette
(fresnel .12 -> .42), the glow halo round the bright parts is brighter and wider, metal and shell catch more of the environment,
their aura breathes, and a cloud of glittering motes in their colour drifts round each one (not on weak phones)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 815;", "const GAME_V = 816;")
rep('totalEmissiveRadiance += vEm; { float fr = pow(1. - saturate(abs(dot(normal, normalize(vViewPosition)))), 4.); totalEmissiveRadiance += vec3(" + rgb + ") * fr * .12; }',
    'totalEmissiveRadiance += vEm * 1.9; { float fr = pow(1. - saturate(abs(dot(normal, normalize(vViewPosition)))), 2.2); totalEmissiveRadiance += vec3(" + rgb + ") * fr * .95; } /* v816 HDR glow and a rim of their own colour */')
rep("m.envMapIntensity = .28; m.onBeforeCompile = obc; m.userData.obc = obc; m.userData.pulse", "m.envMapIntensity = .7; m.onBeforeCompile = obc; m.userData.obc = obc; m.userData.pulse")
rep("vEm = aEm; transformed += normal * .075;", "vEm = aEm; transformed += normal * .095;")
rep('({ smoth: ".16", cram: ".28" }[k] || ".5")', '({ smoth: ".26", cram: ".42" }[k] || ".85")')
rep("o.beacon.material.opacity = down ? .15 : it.boss ? .32 : .55;", "o.beacon.material.opacity = down ? .15 : it.boss ? .32 : .6 + .15 * Math.sin(t * .0016 + it.a0 * 3); /* v816 the aura breathes */")
rep("""  const ring = new TH.Object3D(); grp.add(ring); // (kept so the shared pirate animation code has a ring to turn)
  W.scene.add(grp); return { grp, ring, beacon, body, mon: x.mon };""",
"""  const ring = new TH.Object3D(); grp.add(ring); // (kept so the shared pirate animation code has a ring to turn)
  if (!WEAK) try { const mo = new TH.Points(monMoteGeo(W, x.mon, master), monMoteMat(W, x.mon)); mo.scale.setScalar(s); mo.frustumCulled = false; mo.renderOrder = 6; grp.add(mo); } catch (e) {} /* v816 glittering motes */
  W.scene.add(grp); return { grp, ring, beacon, body, mon: x.mon };""")
rep("function monsterObj(W, x) {", """/* v816 a cloud of motes in a monster's colour: a loose shell round its body, each mote circling on its own tilt, twinkling */
function monMoteGeo(W, k, master) { const C = W.moteGeo || (W.moteGeo = {}); if (C[k]) return C[k]; const bb = new TH.Box3().setFromObject(master), sz = bb.getSize(new TH.Vector3()), R = Math.max(.6, Math.max(sz.x, sz.y, sz.z) * .55), N = 42, P = new Float32Array(N * 3), A = new Float32Array(N * 4);
  for (let i = 0; i < N; i++) { const r = R * (.85 + Math.random() * .7), a = Math.random() * TAU, y = (Math.random() - .5) * R * .9; P[i * 3] = Math.cos(a) * r; P[i * 3 + 1] = y; P[i * 3 + 2] = Math.sin(a) * r; A[i * 4] = .15 + Math.random() * .35; A[i * 4 + 1] = Math.random() * TAU; A[i * 4 + 2] = .5 + Math.random(); A[i * 4 + 3] = (Math.random() - .5) * .8; }
  const g = new TH.BufferGeometry(); g.setAttribute("position", new TH.BufferAttribute(P, 3)); g.setAttribute("aM", new TH.BufferAttribute(A, 4)); return C[k] = g; }
function monMoteMat(W, k) { const C = W.moteMat || (W.moteMat = {}); if (C[k]) return C[k]; const rgb = ((MON[k] && MON[k].rgb) || "140,200,255").split(",").map(v => +v / 255);
  return C[k] = new TH.ShaderMaterial({ uniforms: { uT: W.monU, uC: { value: new TH.Color(rgb[0], rgb[1], rgb[2]) }, uPx: { value: (W.size ? W.size[1] : 800) * (W.renderer ? W.renderer.getPixelRatio() : 1) * .5 } }, transparent: true, depthWrite: false, blending: TH.AdditiveBlending,
    vertexShader: "uniform float uT, uPx; attribute vec4 aM; varying float vTw; void main() { float a = uT * aM.x + aM.y, c = cos(a), s = sin(a); vec3 p = position; p = vec3(p.x * c - p.z * s, p.y + sin(uT * aM.z + aM.y) * .25 + p.x * aM.w * .2, p.x * s + p.z * c); vec4 mv = modelViewMatrix * vec4(p, 1.); vTw = .55 + .45 * sin(uT * 3. * aM.z + aM.y * 5.); gl_PointSize = clamp(uPx * .4 * aM.z / -mv.z, 2.5, 34.); gl_Position = projectionMatrix * mv; }",
    fragmentShader: "uniform vec3 uC; varying float vTw; void main() { vec2 d = gl_PointCoord - .5; float r = length(d), f = smoothstep(.5, 0., r); f = f * f + smoothstep(.12, 0., r) * .8; gl_FragColor = vec4((uC * 2. + vec3(.12)) * f * vTw, f * vTw); }" }); }
function monsterObj(W, x) {""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
