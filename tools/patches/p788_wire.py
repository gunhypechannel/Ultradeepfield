"""v788: the hunt monsters remastered, third pass (owner: "do all of it except the Meshy AI part"): glow, surface detail, translucent
wings and livelier motion, everywhere they appear (map, battles, the Sanctuary, portraits).
- Glow: every sculpted hunt monster carries a soft halo layer that spills light round its glowing parts (scars, veins, eyes, cracks),
  as the light bleeds in the paintings. It travels with the model, so it shows wherever the monster is drawn.
- Surface detail drawn in the shader, in each species' own kind: pores and fine scars on the Void Shark, skin folds on the Squid,
  scales on the Leviathan, crags on the Comet Ram, a fine grain elsewhere.
- Translucent wings: light shines through the Manta's and the Solar Moth's membranes.
- Motion: the Shark snaps its jaw, the Squid's arms curl and reach harder, the Manta's and the Moth's wings beat wider, the Comet Ram
  gallops and tosses its horns.
Applies on top of v787."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 787;", "const GAME_V = 788;")
# surface detail and translucent wings in each species' material
rep('totalEmissiveRadiance += vec3(" + rgb + ") * fr * .12; }"); };',
    r'''totalEmissiveRadiance += vec3(" + rgb + ") * fr * .12; }" + (MON_WING[k] ? " totalEmissiveRadiance += diffuseColor.rgb * " + (k === "smoth" ? "1.1" : "2.6") + " * smoothstep(" + MON_WING[k] + ", abs(vMP.z));" : "")).replace("#include <normal_fragment_maps>", "#include <normal_fragment_maps>\n" + monBump(k)); sh.fragmentShader = MON_NOISE + sh.fragmentShader; };''')
rep("function monSculpted(k) { const D = MON_SC[k], g = new TH.Group(), m = new TH.Mesh(MON_GEO[k], monSculptMat(k)); m.userData.sculpt = 1; m.scale.setScalar(D.s || 1); if (D.r) m.rotation.set(D.r[0], D.r[1], D.r[2]); g.add(m);",
r'''/* v788 surface detail by species (a bump drawn in the shader), translucent wings, and a glow halo round the glowing parts */
const MON_WING = { vmanta: ".9, 1.7", smoth: ".38, .75" }, MON_DET = { swhale: ["pore", 7, .012], ssquid: ["fold", 5, .018], slevi: ["scale", 4.5, .03], cram: ["crag", 2.6, .05], vmanta: ["pore", 9, .006], smoth: ["pore", 9, .006] };
const MON_NOISE = "float mnH(vec3 p) { return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453); }\nfloat mnV(vec3 p) { vec3 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f); return mix(mix(mix(mnH(i), mnH(i + vec3(1, 0, 0)), f.x), mix(mnH(i + vec3(0, 1, 0)), mnH(i + vec3(1, 1, 0)), f.x), f.y), mix(mix(mnH(i + vec3(0, 0, 1)), mnH(i + vec3(1, 0, 1)), f.x), mix(mnH(i + vec3(0, 1, 1)), mnH(i + vec3(1, 1, 1)), f.x), f.y), f.z); }\n";
function monBump(k) { const d = MON_DET[k] || ["pore", 8, .006], q = `vMP * ${(+d[1]).toFixed(2)}`;
  const h = d[0] === "fold" ? `sin(q.x * 3. + mnV(q * .7) * 4.) * .6 + mnV(q * 2.) * .4` : d[0] === "scale" ? `(1. - abs(sin(q.x * 3.1 + sin(q.z * 2.3) * .6) * sin(q.y * 3.1 + q.z * 1.7))) * .7 + mnV(q * 3.) * .3` : d[0] === "crag" ? `mnV(q) * .6 + mnV(q * 2.3) * .3 + mnV(q * 5.1) * .1` : `mnV(q) * .55 + mnV(q * 2.7) * .45`;
  return `#if __VERSION__ >= 300 || defined(GL_OES_standard_derivatives)
 { vec3 q = ${q}; float DH = (${h}) * ${(+d[2]).toFixed(3)}; vec3 sX = dFdx(-vViewPosition), sY = dFdy(-vViewPosition), R1 = cross(sY, normal), R2 = cross(normal, sX); float fD = dot(sX, R1); normal = normalize(abs(fD) * normal - sign(fD) * (dFdx(DH) * R1 + dFdy(DH) * R2)); }
#endif`; }
function monGlowMat(k) { const C = monGlowMat.C || (monGlowMat.C = {}); if (C[k]) return C[k]; const m = new TH.MeshBasicMaterial({ transparent: true, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false });
  const obc = sh => { sh.vertexShader = sh.vertexShader.replace("#include <common>", "#include <common>\nattribute vec3 aEm; varying vec3 vEm;").replace("#include <begin_vertex>", "#include <begin_vertex>\nvEm = aEm; transformed += normal * .075;");
    sh.fragmentShader = sh.fragmentShader.replace("#include <common>", "#include <common>\nvarying vec3 vEm;").replace("#include <color_fragment>", "#include <color_fragment>\n if (vEm.r + vEm.g + vEm.b < .06) discard; diffuseColor.rgb = vEm * " + ({ smoth: ".16", cram: ".28" }[k] || ".5") + ";"); };
  m.onBeforeCompile = obc; m.userData.obc = obc; m.customProgramCacheKey = () => "monglow-" + k; return C[k] = m; }
function monSculpted(k) { const D = MON_SC[k], g = new TH.Group(), m = new TH.Mesh(MON_GEO[k], monSculptMat(k)); m.userData.sculpt = 1; m.scale.setScalar(D.s || 1); if (D.r) m.rotation.set(D.r[0], D.r[1], D.r[2]); g.add(m);
  if (MON_DET[k]) { const gm = new TH.Mesh(MON_GEO[k], monGlowMat(k)); gm.userData.sculpt = 1; gm.scale.copy(m.scale); gm.rotation.copy(m.rotation); gm.renderOrder = 4; g.add(gm); } /* v788 the glow halo */''')
# motion
rep("transformed.z += (.04 + .72 * su * su) * sin(position.x * .78 + sb) - .1 * sh * sin(sb + 1.1); transformed.y += .03 * su * sin(sb * .5 + 1.);",
    "transformed.z += (.04 + .72 * su * su) * sin(position.x * .78 + sb) - .1 * sh * sin(sb + 1.1); transformed.y += .03 * su * sin(sb * .5 + 1.); if (position.x > 2. && position.y < -.12) { float jo = .32 * pow(max(0., sin(mt * .9)), 6.), dx = position.x - 2.; transformed.y -= dx * sin(jo); transformed.x -= dx * (1. - cos(jo)); }")
rep("transformed.y += .36 * e * sin(position.x * 2.2 + mt * 4. + ang * 2.); transformed.z += .36 * e * cos(position.x * 2. + mt * 3.6 + ang * 3.);",
    "transformed.y += .52 * e * sin(position.x * 2.2 + mt * 4. + ang * 2.); transformed.z += .52 * e * cos(position.x * 2. + mt * 3.6 + ang * 3.); transformed.x += .22 * e * sin(mt * 3. + ang * 2.);")
rep("transformed.y += w * w * 1.05 * sin(mt * 1.7 - sp * .55);", "transformed.y += w * w * 1.3 * sin(mt * 1.7 - sp * .55);")
rep("float a = .7 * sin(mt * 2.4), d = sp - .38;", "float a = .95 * sin(mt * 2.4), d = sp - .38;")
rep("float hb = smoothstep(.8, 2.8, position.x); transformed.y += hb * .1 * sin(mt * 1.6);",
    "float hb = smoothstep(.8, 2.8, position.x); transformed.y += hb * (.1 + (position.x - .8) * .1) * sin(mt * 1.6); float lg = smoothstep(-.35, -1., position.y); transformed.x += .24 * lg * sin(mt * 5. + sign(position.z) * 1.6 + step(.5, position.x) * 3.1);")
open(p, "w", encoding="utf-8").write(s)
print("ok")
