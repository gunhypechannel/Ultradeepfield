"""v754: the last monsters and the Mimic hive and Nexus sculpted (tools/sculpt/mon3_sculpt.py); a sculpt may carry a second mesh
<k>_g.bin drawn additively and see-through (light, glass, wings, holograms): cntGhostMat. Apply after p752 and p753."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 753;", "const GAME_V = 754;")
rep("""m.userData.obc = m.onBeforeCompile; /* v751 kept for the animation clone */ return cntMeshMat.M = m; }""",
    """m.userData.obc = m.onBeforeCompile; /* v751 kept for the animation clone */ return cntMeshMat.M = m; }
/* v754 the see-through half of a sculpt (a whale of light, glass eggs, wings, holograms): the same vertex material, added on top, no depth writes */
function cntGhostMat() { if (cntGhostMat.M) return cntGhostMat.M; const b = cntMeshMat(), m = b.clone(); m.onBeforeCompile = b.userData.obc; m.userData.obc = b.userData.obc; m.customProgramCacheKey = () => "cntsculpt2";
  m.transparent = true; m.opacity = .45; m.depthWrite = false; m.blending = TH.AdditiveBlending; m.envMapIntensity = 0; return cntGhostMat.M = m; }
function sculptFetch(dir, k, g, done) { const get = u => fetch(u).then(r => r.ok ? r.arrayBuffer() : Promise.reject(Error("HTTP " + r.status)));
  Promise.all([get(dir + k + ".bin"), g ? get(dir + k + "_g.bin").catch(() => null) : null]).then(([b, bg]) => done(cntMeshGeo(b), bg ? cntMeshGeo(bg) : null)).catch(e => console.warn("sculpt " + k, e && e.message)); }
function sculptGhost(g, geo, sc) { if (!geo) return; const m = new TH.Mesh(geo, cntGhostMat()); m.userData.sculpt = 1; m.scale.setScalar(sc || 1); m.renderOrder = 3; g.add(m); }""")
rep("""  fetch("art/mon/m/" + k + ".bin").then(r => r.ok ? r.arrayBuffer() : Promise.reject(Error("HTTP " + r.status))).then(b => { MON_GEO[k] = cntMeshGeo(b); monSculptSwap(k); }).catch(e => console.warn("sculpt " + k, e && e.message)); }""",
    """  sculptFetch("art/mon/m/", k, MON_SC[k].g, (a, b) => { MON_GEO[k + "_g"] = b; MON_GEO[k] = a; monSculptSwap(k); }); }""")
rep("""m.userData.sculpt = 1; m.scale.setScalar(D.s || 1); g.add(m); g.userData.eng = []; g.userData.keepGeo = 1; return g; }""",
    """m.userData.sculpt = 1; m.scale.setScalar(D.s || 1); g.add(m); sculptGhost(g, MON_GEO[k + "_g"], D.s); g.userData.eng = []; g.userData.keepGeo = 1; return g; }""")
rep("""  fetch("art/mimic/m/" + k + ".bin").then(r => r.ok ? r.arrayBuffer() : Promise.reject(Error("HTTP " + r.status))).then(b => { MIM_GEO[k] = cntMeshGeo(b); mimSculptSwap(k); }).catch(e => console.warn("sculpt " + k, e && e.message)); }""",
    """  sculptFetch("art/mimic/m/", k, MIM_SC[k].g, (a, b) => { MIM_GEO[k + "_g"] = b; MIM_GEO[k] = a; mimSculptSwap(k); }); }""")
rep("""m.userData.sculpt = 1; m.scale.setScalar((MIM_D[k] && MIM_D[k].s) || 1); g.add(m); g.userData.eng = []; g.userData.keepGeo = 1; return g; }""",
    """m.userData.sculpt = 1; m.scale.setScalar((MIM_D[k] && MIM_D[k].s) || 1); g.add(m); sculptGhost(g, MIM_GEO[k + "_g"], (MIM_D[k] && MIM_D[k].s) || 1); g.userData.eng = []; g.userData.keepGeo = 1; return g; }""")
rep("""MIM_MAPK = { malpha1: "alpha1", malpha2: "alpha2", malpha3: "alpha3", malpha4: "alpha4", momega: "omega" }""",
    """MIM_MAPK = { malpha1: "alpha1", malpha2: "alpha2", malpha3: "alpha3", malpha4: "alpha4", momega: "omega", mnest: "mimic", mnexus: "nexus" }""")
# the Starhive's battle pieces: the nest ("snest") and the swarm ("swasp") are their own meshes
rep("""  if (!part) { monSculptLoad(k); if (MON_GEO[k]) return monSculpted(k); } /* v752 */""",
    """  { const sk = part ? k + "_" + part : k; monSculptLoad(sk); if (MON_GEO[sk]) return monSculpted(sk); } /* v752, v754 a part has its own sculpt */""")
rep("""function monSculptSwap(k) { try {""", """function monSculptSwap(k) { try { if (k === "swasp_nest" || k === "swasp_swarm") { const u = k === "swasp_nest" ? "snest" : "swasp"; delete MMERGE[u]; if (STU && STU.cache) for (const key in STU.cache) if (key.startsWith(u + "|")) delete STU.cache[key]; }""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
