"""v782: the Mimics remastered toward their paintings (owner approved: "build it all"). Their sculpted models used the plain
matte sculpt material, so in space they read as dark smudges with flat cyan patches. Now (Mimics only; the Carcinid and the
other sculpts keep theirs):
- wet, glossy black cable-flesh (much lower roughness, stronger reflections), as in the paintings;
- brighter cyan veins and nodes, a cyan rim light on every silhouette, and pulses of light running along the body from head to tail;
- their manes and tails writhe harder;
- the Mimic Hive's neural core sits inside a slowly turning holographic hex dome.
Applies on top of v781."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 781;", "const GAME_V = 782;")
rep('function mimSculpted(k) { const g = new TH.Group(), m = new TH.Mesh(MIM_GEO[k], cntMeshMat()); m.userData.sculpt = 1; m.scale.setScalar((MIM_D[k] && MIM_D[k].s) || 1); g.add(m); sculptGhost(g, MIM_GEO[k + "_g"], (MIM_D[k] && MIM_D[k].s) || 1); g.userData.eng = []; g.userData.keepGeo = 1; return g; }',
r'''/* v782 the Mimics' own sculpt material: wet glossy black, brighter cyan veins, a cyan rim light, pulses running head to tail (in motion) */
function mimSculptMat() { if (mimSculptMat.M) return mimSculptMat.M; const b = cntMeshMat(), m = b.clone(); m.envMapIntensity = .85;
  const obc = sh => { b.userData.obc(sh); sh.vertexShader = sh.vertexShader.replace("#include <common>", "#include <common>\nvarying vec3 vMP;").replace("#include <begin_vertex>", "#include <begin_vertex>\nvMP = position;");
    sh.fragmentShader = sh.fragmentShader.replace("#include <common>", "#include <common>\nvarying vec3 vMP;").replace("roughnessFactor = max(.05, vRM.x);", "roughnessFactor = max(.04, vRM.x * .42);")
      .replace("totalEmissiveRadiance += vEm;", "totalEmissiveRadiance += vEm * 1.9; { float fr = pow(1. - saturate(abs(dot(normal, normalize(vViewPosition)))), 3.); totalEmissiveRadiance += vec3(.1, .55, .95) * fr * .32; }"); };
  m.onBeforeCompile = obc; m.userData.obc = obc; m.userData.pulse = "(1. + 1.5 * pow(.5 + .5 * sin(uMT * 3. - vMP.x * 1.2), 8.))"; m.customProgramCacheKey = () => "mimsculpt3"; return mimSculptMat.M = m; }
function mimSculpted(k) { const g = new TH.Group(), m = new TH.Mesh(MIM_GEO[k], mimSculptMat()); m.userData.sculpt = 1; m.scale.setScalar((MIM_D[k] && MIM_D[k].s) || 1); g.add(m); sculptGhost(g, MIM_GEO[k + "_g"], (MIM_D[k] && MIM_D[k].s) || 1);
  if (k === "mnest") { /* v782 the hive's neural core inside a holographic hex dome */ const dm = new TH.Mesh(new TH.IcosahedronGeometry(2.05, 1), new TH.MeshBasicMaterial({ color: 0x5fd8ff, wireframe: true, transparent: true, opacity: .55, blending: TH.AdditiveBlending, depthWrite: false, toneMapped: false })); dm.position.set(0, 1.2, 0); g.add(dm);
    const sh = new TH.Mesh(new TH.SphereGeometry(2.0, 32, 20), new TH.MeshBasicMaterial({ color: 0x1a8ab8, transparent: true, opacity: .16, blending: TH.AdditiveBlending, depthWrite: false, side: TH.DoubleSide, toneMapped: false })); sh.position.copy(dm.position); g.add(sh); }
  g.userData.eng = []; g.userData.keepGeo = 1; return g; }''')
rep("transformed.z += tw * .3 * sin(mt * ${W1} - dd * 1.6 + p.x * .6); transformed.y += tw * .2 * sin(mt * ${W2} - dd * 1.3 + p.z * 1.2); transformed.x += tw * .12 * sin(mt * ${W1} - dd);",
    "transformed.z += tw * .48 * sin(mt * ${W1} - dd * 1.6 + p.x * .6); transformed.y += tw * .34 * sin(mt * ${W2} - dd * 1.3 + p.z * 1.2); transformed.x += tw * .18 * sin(mt * ${W1} - dd); /* v782 writhe harder */")
open(p, "w", encoding="utf-8").write(s)
print("ok")
