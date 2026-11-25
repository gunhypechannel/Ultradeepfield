/* ---------- v751 the Carcinid sculpted (tools/sculpt/crc_lib.py, crc_crab.py, crc_ship.py): each unit loads its own mesh
   (art/carcinid/m/<k>.bin, CNT2 format, the same loader and material as the Continuum) the first time it is built; until it arrives,
   and if it never does, the hand-built model stands in. The crabs keep their walk (MON_WAVE's crab wave, same frame: +x forward,
   claws past x 1.3, legs out beyond |z| .95), which now runs on the sculpted mesh too. */
const CRC_SC = {}, CRC_GEO = {};
function crcSculptLoad(k) { if (!CRC_SC[k] || !TH || typeof fetch !== "function") return; const L = crcSculptLoad.L || (crcSculptLoad.L = {}); if (L[k]) return; L[k] = 1;
  fetch("art/carcinid/m/" + k + ".bin").then(r => r.ok ? r.arrayBuffer() : Promise.reject(Error("HTTP " + r.status))).then(b => { CRC_GEO[k] = cntMeshGeo(b); crcSculptSwap(k); }).catch(e => console.warn("sculpt " + k, e && e.message)); }
function crcSculptSwap(k) { try { const ks = [k].concat(k === "cfrig" || k === "cint" ? ["cpat"] : []); /* the map patrol is a frigate with two interceptors */
  if (STU && STU.cache) for (const key in STU.cache) if (ks.some(q => key.startsWith(q + "|"))) delete STU.cache[key]; for (const q of ks) delete MMERGE[q];
  const ms = Object.keys(CRC_M).filter(m => ks.includes(CRC_M[m])); for (const m of ms) delete MMERGE[m]; if (G3) { if (G3.monMaster) for (const m of ms) delete G3.monMaster[m];
    if (G3.pirates) for (const [id, o] of [...G3.pirates]) { const x = PB[id]; if (x && ms.includes(x.mon)) { G3.scene.remove(o.grp); G3.pirates.delete(id); } } } } catch (e) { console.warn("sculpt swap", e); } }
function crcSculpted(k) { const D = CRC_SC[k], g = new TH.Group(), m = new TH.Mesh(CRC_GEO[k], cntMeshMat()); m.userData.sculpt = 1; m.scale.setScalar(D.s || 1); g.add(m);
  g.userData.eng = (D.eng || []).map(e => e.slice()); g.userData.engCol = [0xbffcf4, 0x3fe0c8]; g.userData.keepGeo = 1; return g; }
