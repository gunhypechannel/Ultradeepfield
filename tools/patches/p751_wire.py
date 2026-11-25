"""v751: the Carcinid sculpted after the owner's paintings (crabs, ships, the Kraken, the nest): loader and swap (p751_crc.js), the
sculpted material keeps its own shader when the monster animation (map walk and battle frames) adds the crab wave."""
import sys, os, json
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(D, "..", "..")
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 750;", "const GAME_V = 751;")
js = open(os.path.join(D, "p751_crc.js"), encoding="utf-8").read().strip()
# which units have a sculpt: every .bin present, with its scale from tools/sculpt/crc_sc.json
sc = json.load(open(os.path.join(R, "tools", "sculpt", "crc_sc.json")))
have = {k: v for k, v in sc.items() if os.path.exists(os.path.join(R, "docs", "art", "carcinid", "m", k + ".bin"))}
js = js.replace("const CRC_SC = {}, CRC_GEO = {};", "const CRC_SC = " + json.dumps(have, separators=(",", ":")) + ", CRC_GEO = {};")
rep("\nfunction buildCarc(k) { ", "\n" + js + "\nfunction buildCarc(k) { crcSculptLoad(k); if (CRC_GEO[k]) return crcSculpted(k); /* v751 */ ")
# the sculpted material's own shader survives the animation clone
rep("""  m.customProgramCacheKey = () => "cntsculpt2"; return cntMeshMat.M = m; }""",
    """  m.customProgramCacheKey = () => "cntsculpt2"; m.userData.obc = m.onBeforeCompile; /* v751 kept for the animation clone */ return cntMeshMat.M = m; }""")
rep("""    if (!m) { m = o.material.clone(); m.onBeforeCompile = sh => { sh.uniforms.uMT = U; sh.vertexShader = "uniform float uMT;\\n" + sh.vertexShader.replace("#include <begin_vertex>", "#include <begin_vertex>\\nfloat mt = uMT + modelMatrix[3].x * .37 + modelMatrix[3].z * .23;\\n" + MON_WAVE[kind]); };""",
    """    if (!m) { const pre = o.material.userData && o.material.userData.obc; m = o.material.clone(); m.onBeforeCompile = sh => { if (pre) pre(sh); sh.uniforms.uMT = U; sh.vertexShader = "uniform float uMT;\\n" + sh.vertexShader.replace("#include <begin_vertex>", "#include <begin_vertex>\\nfloat mt = uMT + modelMatrix[3].x * .37 + modelMatrix[3].z * .23;\\n" + MON_WAVE[kind]); }; if (pre) m.userData.sc = 1; /* v751 */""")
rep("""      m.customProgramCacheKey = () => "monwave-" + kind + (pu ? "-p" + hash(pu) : ""); done.set(o.material, m); } o.material = m; }); }""",
    """      m.customProgramCacheKey = () => "monwave-" + kind + (pu ? "-p" + hash(pu) : "") + (m.userData.sc ? "-s" : ""); done.set(o.material, m); } o.material = m; }); }""")
rep("""    if (!m) { m = o.material.clone(); const pu = m.userData && m.userData.pulse ? mbfQ(m.userData.pulse) : null;
      m.onBeforeCompile = sh => { sh.uniforms.uMT = U;""",
    """    if (!m) { const pre = o.material.userData && o.material.userData.obc; m = o.material.clone(); const pu = m.userData && m.userData.pulse ? mbfQ(m.userData.pulse) : null;
      m.onBeforeCompile = sh => { if (pre) pre(sh); sh.uniforms.uMT = U;""")
rep("""      m.customProgramCacheKey = () => "monbat-" + kind + (pu ? "-p" + hash(pu) : ""); done.set(o.material, m); } o.material = m; });""",
    """      m.customProgramCacheKey = () => "monbat-" + kind + (pu ? "-p" + hash(pu) : "") + (pre ? "-s" : ""); done.set(o.material, m); } o.material = m; });""")
open(p, "w", encoding="utf-8").write(s)
print("ok", len(have), "sculpted:", " ".join(sorted(have)))
