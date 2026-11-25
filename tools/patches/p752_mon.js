/* ---------- v752 the space monsters sculpted after the owner's paintings (tools/sculpt/mon_sculpt.py): each species loads its mesh
   (art/mon/m/<k>.bin, CNT2) the first time it is built, through the same loader and material as the Continuum and the Carcinid; the
   hand-built model stands in until then. Same frame as before (+x the head), so each species' swim wave (MON_WAVE) runs on it. */
const MON_SC = {}, MON_GEO = {};
function monSculptLoad(k) { if (!MON_SC[k] || !TH || typeof fetch !== "function") return; const L = monSculptLoad.L || (monSculptLoad.L = {}); if (L[k]) return; L[k] = 1;
  fetch("art/mon/m/" + k + ".bin").then(r => r.ok ? r.arrayBuffer() : Promise.reject(Error("HTTP " + r.status))).then(b => { MON_GEO[k] = cntMeshGeo(b); monSculptSwap(k); }).catch(e => console.warn("sculpt " + k, e && e.message)); }
function monSculptSwap(k) { try { if (STU && STU.cache) for (const key in STU.cache) if (key.startsWith(k + "|")) delete STU.cache[key]; delete MMERGE[k];
  if (G3) { if (G3.monMaster) delete G3.monMaster[k]; if (G3.pirates) for (const [id, o] of [...G3.pirates]) { const x = PB[id]; if (x && x.mon === k) { G3.scene.remove(o.grp); G3.pirates.delete(id); } } } } catch (e) { console.warn("sculpt swap", e); } }
function monSculpted(k) { const D = MON_SC[k], g = new TH.Group(), m = new TH.Mesh(MON_GEO[k], cntMeshMat()); m.userData.sculpt = 1; m.scale.setScalar(D.s || 1); g.add(m); g.userData.eng = []; g.userData.keepGeo = 1; return g; }
