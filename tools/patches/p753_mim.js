/* ---------- v753 the Mimic sculpted after the owner's paintings (tools/sculpt/mim_sculpt.py): owner, "make sure to do them without legs
   so they are more like ships". Each class loads its mesh (art/mimic/m/<cls>.bin, CNT2) the first time it is built; the hand-built
   creature stands in until then. Built in buildMimic's frame at unit scale (scaled here by MIM_D.s); its swim wave drops the legs. */
const MIM_SC = {}, MIM_GEO = {}, MIM_MAPK = { malpha1: "alpha1", malpha2: "alpha2", malpha3: "alpha3", malpha4: "alpha4", momega: "omega" };
function mimSculptLoad(k) { if (!MIM_SC[k] || !TH || typeof fetch !== "function") return; const L = mimSculptLoad.L || (mimSculptLoad.L = {}); if (L[k]) return; L[k] = 1;
  fetch("art/mimic/m/" + k + ".bin").then(r => r.ok ? r.arrayBuffer() : Promise.reject(Error("HTTP " + r.status))).then(b => { MIM_GEO[k] = cntMeshGeo(b); mimSculptSwap(k); }).catch(e => console.warn("sculpt " + k, e && e.message)); }
function mimSculptSwap(k) { try { const mk = MIM_MAPK[k]; if (STU && STU.cache) for (const key in STU.cache) if (key.startsWith(k + "|") || (mk && key.startsWith(mk + "|"))) delete STU.cache[key]; delete MMERGE[k];
  if (mk && G3) { if (G3.monMaster) delete G3.monMaster[mk]; if (G3.pirates) for (const [id, o] of [...G3.pirates]) { const x = PB[id]; if (x && x.mon === mk) { G3.scene.remove(o.grp); G3.pirates.delete(id); } } } } catch (e) { console.warn("sculpt swap", e); } }
function mimSculpted(k) { const g = new TH.Group(), m = new TH.Mesh(MIM_GEO[k], cntMeshMat()); m.userData.sculpt = 1; m.scale.setScalar((MIM_D[k] && MIM_D[k].s) || 1); g.add(m); g.userData.eng = []; g.userData.keepGeo = 1; return g; }
