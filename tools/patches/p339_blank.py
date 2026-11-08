p="docs/index.html"; h=open(p).read()
def rep(a,b):
    global h; assert h.count(a)==1,a[:60]; h=h.replace(a,b)
rep('''function glWatch(W) {''','''/* v339.1: under memory pressure iPhone Safari empties cached canvases (skin paintings and their maps) and resets the GPU, and the
   worlds came back black. A skin whose cached canvas reads empty is dropped and loaded again from its file. */
function pxBlank(c) { try { if (!c || !c.width) return true; const d = c.getContext("2d").getImageData(c.width >> 1, c.height >> 1, 1, 1).data; return d[3] === 0; } catch (e) { return false; } }
function pxPurge(all) { let n = 0; for (const k in PXC) { const C = PXC[k]; if (!C) continue; if (all || (C.art && pxBlank(C.art)) || (C.surf && pxBlank(C.surf)) || (C.lay && C.lay.front && pxBlank(C.lay.front))) { delete PXC[k]; n++; } }
  if (n && typeof G3 !== "undefined" && G3) { for (const k in G3.mats) if (k.startsWith("px:")) delete G3.mats[k]; } return n; }
document.addEventListener("visibilitychange", () => { if (document.visibilityState !== "visible") return; try { if (pxPurge(false) && typeof G3 !== "undefined" && G3 && view === "galaxy") { crumb("skins reloaded after the phone cleared them"); map3DRebuild(); } } catch (e) {} });
function glWatch(W) {''')
rep('''cv.addEventListener("webglcontextlost", e => { e.preventDefault(); G.glLost = (G.glLost || 0) + 1; if (MOBILE) G.glSafe = 1; crumb("GPU reset (graphics context lost)");''',
'''cv.addEventListener("webglcontextlost", e => { e.preventDefault(); G.glLost = (G.glLost || 0) + 1; if (MOBILE) G.glSafe = 1; crumb("GPU reset (graphics context lost)"); try { pxPurge(true); } catch (er) {}''')
# a material is never built from a canvas the phone has emptied
rep('''function pxMat(W, id) {
  const key = "px:" + id; let mat = W.mats[key]; const C = pxReady(id);''','''function pxMat(W, id) {
  const key = "px:" + id; let mat = W.mats[key]; if (PXC[id] && !(mat && mat.userData.ok) && ((PXC[id].art && pxBlank(PXC[id].art)) || (PXC[id].surf && pxBlank(PXC[id].surf)))) { delete PXC[id]; mat = null; delete W.mats[key]; } const C = pxReady(id);''')
open(p,"w").write(h); print("ok")
