/* v685 the memory leak behind the iPhone crashes. three.js keeps a "dispose" listener on every geometry, material and texture a renderer
   draws, and that listener holds the renderer (its canvas, buffers, programs). Objects shared between renderers (three's own PMREM
   background box, BORG's blocks, cached sprites and geometry) are never disposed, so every released map and base renderer stayed alive:
   +150 to 190 MB for each trip between the map and the base on a simulated iPhone, 14 live WebGL contexts after three trips.
   Now each renderer records the listeners it adds and removes them all when it is disposed (glFree, map3DRebuild, t3Free...). */
if (TH && TH.WebGLRenderer && !TH.WebGLRenderer.__v685) { const R0 = TH.WebGLRenderer, ED = TH.EventDispatcher.prototype, ae = ED.addEventListener; let CUR = null;
  ED.addEventListener = function (type, l) { if (type === "dispose" && CUR) (CUR.__dl || (CUR.__dl = [])).push([this, l]); return ae.call(this, type, l); };
  const unhook = r => { const L = r.__dl; r.__dl = null; if (L) for (const [o, l] of L) { try { o.removeEventListener("dispose", l); } catch (e) {} } };
  const W2 = function (...a) { const r = new R0(...a);
    for (const k of ["render", "compile", "setRenderTarget", "initTexture", "clear", "copyFramebufferToTexture", "copyTextureToTexture", "readRenderTargetPixels"]) { const f = r[k]; if (typeof f !== "function") continue; r[k] = function () { const p = CUR; CUR = r; try { return f.apply(this, arguments); } finally { CUR = p; } }; }
    const d0 = r.dispose; r.dispose = function () { try { return d0.apply(this, arguments); } finally { unhook(r); } }; return r; };
  W2.prototype = R0.prototype; W2.__v685 = 1; try { TH.WebGLRenderer = W2; } catch (e) {} }
