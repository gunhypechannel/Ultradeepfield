/* ---------- v731/v732 the battle on the graphics chip (owner: "How can we make our game run directly on phones graphic chip?" ... "Yes finish up") ----------
   In the Android app the browser draws 2D canvases without the GPU, so every full-screen copy and every glow cost real time.
   The battle is now three layers, stacked by the compositor:
     .bgu  (WebGL, under)  the space backdrop with the planet, moved and zoomed with the camera on the GPU (v732)
     #bcv  (2D, middle)    ships, trails, shields, labels: only what needs the 2D canvas
     .bgl  (WebGL, over)   all the light: the light layer and its bloom (v731), every glow sprite drawn in "lighter" mode on the
                           battlefield or the light layer (v732: they no longer touch the 2D canvas at all), and the screen flash.
                           It is added to the picture with mix-blend-mode: plus-lighter, the same sum the old "lighter" draws made.
   Glows that sat under a hull now add their light on top of it: light only adds, so that reads as the hull catching the glow.
   Without WebGL or plus-lighter, in low effects, after a lost GPU context, or with ?gl2d, the old 2D drawing runs unchanged. */
const BGL_OK = (() => { try { return !/[?&]gl2d\b/.test(location.search) && !!(window.CSS && CSS.supports && CSS.supports("mix-blend-mode", "plus-lighter")); } catch (e) { return false; } })();
const BGL_VS = "attribute vec2 p;varying vec2 v;void main(){v=p*.5+.5;gl_Position=vec4(p,0.,1.);}";
const BGL_QVS = "attribute vec2 p;attribute vec2 q;attribute float a;varying vec2 v;varying float al;void main(){v=q;al=a;gl_Position=vec4(p,0.,1.);}";
const BGL_FS = {
  copy: "precision mediump float;uniform sampler2D t;varying vec2 v;void main(){gl_FragColor=texture2D(t,v);}",
  /* a 4x shrink that averages the whole 4x4 block (four bilinear taps), so thin shots don't sparkle in and out */
  down: "precision mediump float;uniform sampler2D t;uniform vec2 px;varying vec2 v;void main(){gl_FragColor=.25*(texture2D(t,v+px*vec2(-1.,-1.))+texture2D(t,v+px*vec2(1.,-1.))+texture2D(t,v+px*vec2(-1.,1.))+texture2D(t,v+px*vec2(1.,1.)));}",
  blur: "precision mediump float;uniform sampler2D t;uniform vec2 px;varying vec2 v;void main(){vec4 c=texture2D(t,v)*.2270270;c+=(texture2D(t,v+px*1.3846154)+texture2D(t,v-px*1.3846154))*.3162162;c+=(texture2D(t,v+px*3.2307692)+texture2D(t,v-px*3.2307692))*.0702703;gl_FragColor=c;}",
  comp: "precision mediump float;uniform sampler2D L;uniform sampler2D B1;uniform sampler2D B2;uniform float e;uniform float w1;uniform float w2;uniform vec4 fl;varying vec2 v;void main(){gl_FragColor=min(texture2D(L,v)*e+texture2D(B1,v)*w1+texture2D(B2,v)*w2+fl,vec4(1.));}" };
const BGL_QFS = "precision mediump float;uniform sampler2D t;varying vec2 v;varying float al;void main(){gl_FragColor=texture2D(t,v)*al;}";
function bglCtx(c, opts) { const gl = c.getContext("webgl", Object.assign({ antialias: false, depth: false, stencil: false, preserveDrawingBuffer: true, powerPreference: "high-performance" }, opts)); if (!gl) return null;
  const sh = (ty, src) => { const s = gl.createShader(ty); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error("bgl shader: " + gl.getShaderInfoLog(s)); return s; };
  const prog = (vsSrc, fsSrc, attrs) => { const p = gl.createProgram(); gl.attachShader(p, sh(gl.VERTEX_SHADER, vsSrc)); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, fsSrc)); attrs.forEach((a, i) => gl.bindAttribLocation(p, i, a)); gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error("bgl link"); const u = {}; for (const n of ["t", "px", "L", "B1", "B2", "e", "w1", "w2", "fl"]) u[n] = gl.getUniformLocation(p, n); return { p, u }; };
  const tex = () => { const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t); for (const [k, v] of [[gl.TEXTURE_MIN_FILTER, gl.LINEAR], [gl.TEXTURE_MAG_FILTER, gl.LINEAR], [gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE], [gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE]]) gl.texParameteri(gl.TEXTURE_2D, k, v); return t; };
  const full = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, full); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
  return { c, gl, prog, tex, full, qb: gl.createBuffer(), lost: 0 }; }
/* a canvas layer over or under the 2D battle canvas */
function bglLayer(b, cv, cls, before, opts) { const c = document.createElement("canvas"); c.className = cls; c.setAttribute("aria-hidden", "true"); cv.parentNode.insertBefore(c, before ? cv : cv.nextSibling);
  const g = bglCtx(c, opts); if (!g) { c.remove(); return null; } c.addEventListener("webglcontextlost", e => { e.preventDefault(); g.lost = 1; b.glFail = 1; try { crumb("battle GPU layer lost"); } catch (er) {} }, false); return g; }
function bglInit(b, cv) {
  const o = bglLayer(b, cv, "bgl", false, { alpha: true, premultipliedAlpha: true }), u = o && bglLayer(b, cv, "bgu", true, { alpha: false });
  if (!o || !u) { try { o && o.c.remove(); } catch (e) {} return null; }
  const P = {}; for (const k in BGL_FS) P[k] = o.prog(BGL_VS, BGL_FS[k], ["p"]); P.quad = o.prog(BGL_QVS, BGL_QFS, ["p", "q", "a"]); o.P = P; o.L = o.tex(); o.T = []; o.w = 0; o.h = 0; o.tx = new WeakMap(); o.batch = { l: new Map(), a: new Map() };
  u.P = { quad: u.prog(BGL_QVS, BGL_QFS, ["p", "q", "a"]) }; u.bgT = u.tex(); u.bgSrc = null;
  return { o, u }; }
/* render targets at a quarter and a sixteenth of the battlefield (two each, for the two blur directions), and one at full size */
function bglTargets(g, W, H) { const gl = g.gl; if (g.w === W && g.h === H) return; g.w = W; g.h = H; for (const T of g.T) { gl.deleteTexture(T[2]); gl.deleteFramebuffer(T[3]); } g.T = [];
  for (const dv of [4, 4, 16, 16, 1]) { const w = Math.max(2, Math.ceil(W / dv)), h = Math.max(2, Math.ceil(H / dv)), t = g.tex(); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, w, h, 0, gl.RGBA, gl.UNSIGNED_BYTE, null); const f = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, f); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, t, 0); g.T.push([w, h, t, f]); }
  gl.bindFramebuffer(gl.FRAMEBUFFER, null); }
/* which images can live on the GPU: the cached glow, ring, bolt, flak, puff and star sprites, which never change once made */
function bglStatic(img) { if (!img || typeof img !== "object") return false; if (img.__bglS !== undefined) return img.__bglS; let s = false; try { for (const k in GSPR) if (GSPR[k] === img) { s = true; break; } if (!s && typeof RSPR !== "undefined") for (const k in RSPR) if (RSPR[k] === img) { s = true; break; } } catch (e) {} if (s) img.__bglS = true; return s; }
/* the 2D contexts hand their glow draws to the GPU batch; anything else they draw as before */
function bglHook(ctx, kind) { if (ctx.__bglK) return; ctx.__bglK = kind; const P = CanvasRenderingContext2D.prototype, orig = P.drawImage;
  ctx.__clipN = 0; ctx.__clipS = []; ctx.save = function () { this.__clipS.push(this.__clipN); return P.save.call(this); }; ctx.restore = function () { if (this.__clipS.length) this.__clipN = this.__clipS.pop(); return P.restore.call(this); }; ctx.clip = function () { this.__clipN++; return P.clip.apply(this, arguments); };
  ctx.drawImage = function (img) { const B = battle; if (B && B.glOn && this.globalCompositeOperation === "lighter" && !this.__clipN && !this.shadowBlur && (!this.filter || this.filter === "none") && bglStatic(img) && bglQuad(B, this.__bglK, this, arguments)) return; if (this.__bglK === "l" && B) B.fxDirty = 1; return orig.apply(this, arguments); };
  if (kind === "l") for (const m of ["fill", "stroke", "fillRect", "strokeRect", "fillText", "strokeText", "putImageData"]) { const f = P[m]; ctx[m] = function () { if (battle) battle.fxDirty = 1; return f.apply(this, arguments); }; } }
function bglQuad(b, kind, ctx, A) { const g = b.gl && b.gl.o; if (!g) return false; const img = A[0], iw = img.width, ih = img.height; if (!iw || !ih) return true; const ga = ctx.globalAlpha; if (ga <= 0) return true;
  let sx = 0, sy = 0, sw = iw, sh = ih, dx, dy, dw, dh; if (A.length >= 9) { sx = A[1]; sy = A[2]; sw = A[3]; sh = A[4]; dx = A[5]; dy = A[6]; dw = A[7]; dh = A[8]; } else if (A.length >= 5) { dx = A[1]; dy = A[2]; dw = A[3]; dh = A[4]; } else { dx = A[1]; dy = A[2]; dw = iw; dh = ih; }
  const m = ctx.getTransform(), W = b.glW, H = b.glH, X = (x, y) => (m.a * x + m.c * y + m.e) / W * 2 - 1, Y = (x, y) => 1 - (m.b * x + m.d * y + m.f) / H * 2;
  const x0 = dx, y0 = dy, x1 = dx + dw, y1 = dy + dh, u0 = sx / iw, v0 = sy / ih, u1 = (sx + sw) / iw, v1 = (sy + sh) / ih;
  let arr = g.batch[kind === "l" ? "l" : "a"].get(img); if (!arr) { arr = []; g.batch[kind === "l" ? "l" : "a"].set(img, arr); }
  const p00 = [X(x0, y0), Y(x0, y0)], p10 = [X(x1, y0), Y(x1, y0)], p01 = [X(x0, y1), Y(x0, y1)], p11 = [X(x1, y1), Y(x1, y1)];
  arr.push(p00[0], p00[1], u0, v0, ga, p10[0], p10[1], u1, v0, ga, p01[0], p01[1], u0, v1, ga, p10[0], p10[1], u1, v0, ga, p11[0], p11[1], u1, v1, ga, p01[0], p01[1], u0, v1, ga);
  return true; }
function bglDrawBatch(g, map) { const gl = g.gl, Q = g.P.quad; if (!map.size) return; gl.useProgram(Q.p); gl.uniform1i(Q.u.t, 0); gl.activeTexture(gl.TEXTURE0); gl.bindBuffer(gl.ARRAY_BUFFER, g.qb);
  gl.enableVertexAttribArray(0); gl.enableVertexAttribArray(1); gl.enableVertexAttribArray(2); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 20, 0); gl.vertexAttribPointer(1, 2, gl.FLOAT, false, 20, 8); gl.vertexAttribPointer(2, 1, gl.FLOAT, false, 20, 16);
  gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE);
  for (const [img, arr] of map) { if (!arr.length) continue; let t = g.tx.get(img); if (!t) { t = g.tex(); gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false); gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img); g.tx.set(img, t); }
    gl.bindTexture(gl.TEXTURE_2D, t); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(arr), gl.STREAM_DRAW); gl.drawArrays(gl.TRIANGLES, 0, arr.length / 5); }
  gl.disable(gl.BLEND); gl.disableVertexAttribArray(1); gl.disableVertexAttribArray(2); map.clear(); }
function bglFull(g) { const gl = g.gl; gl.bindBuffer(gl.ARRAY_BUFFER, g.full); gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0); }
/* start of a frame: true when this frame draws the GPU way (the caller then skips the 2D backdrop) */
function bglBegin(b, cv, mainCtx, W, H, lo) {
  if (!BGL_OK || b.glFail || lo) { bglHide(b); b.glOn = false; return false; }
  try { let G = b.gl; if (G && (G.o.lost || G.u.lost)) { b.glFail = 1; bglHide(b); b.glOn = false; return false; }
    if (!G || !G.o.c.isConnected) { G = b.gl = bglInit(b, cv); if (!G) { b.glFail = 1; b.glOn = false; return false; } }
    for (const g of [G.o, G.u]) { if (g.c.width !== W || g.c.height !== H) { g.c.width = W; g.c.height = H; } if (g.c.style.visibility) g.c.style.visibility = ""; }
    b.glW = W; b.glH = H; b.glOn = true; b.fxDirty = 0; bglHook(mainCtx, "a"); G.o.batch.l.clear(); G.o.batch.a.clear(); return true;
  } catch (e) { b.glFail = 1; b.glOn = false; bglHide(b); try { errCrumb("battle GPU begin: " + (e && e.message)); } catch (er) {} return false; } }
/* the backdrop on the GPU: uploaded once (and again if it is rebuilt), then moved with the camera every frame */
function bglBackdrop(b, W, H, vs, tx, ty) { const u = b.gl.u, gl = u.gl;
  if (u.bgSrc !== b.bg || u.bgV !== b.bgV) { gl.bindTexture(gl.TEXTURE_2D, u.bgT); gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, false); gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, false); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, b.bg); u.bgSrc = b.bg; u.bgV = b.bgV; }
  gl.viewport(0, 0, W, H); gl.clearColor(.008, .02, .035, 1); gl.clear(gl.COLOR_BUFFER_BIT);
  const X = x => x / W * 2 - 1, Y = y => 1 - y / H * 2, x0 = X(tx), x1 = X(tx + vs * W), y0 = Y(ty), y1 = Y(ty + vs * H);
  const Q = u.P.quad; gl.useProgram(Q.p); gl.uniform1i(Q.u.t, 0); gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, u.bgT); gl.bindBuffer(gl.ARRAY_BUFFER, u.qb);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([x0, y0, 0, 0, 1, x1, y0, 1, 0, 1, x0, y1, 0, 1, 1, x1, y0, 1, 0, 1, x1, y1, 1, 1, 1, x0, y1, 0, 1, 1]), gl.STREAM_DRAW);
  gl.enableVertexAttribArray(0); gl.enableVertexAttribArray(1); gl.enableVertexAttribArray(2); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 20, 0); gl.vertexAttribPointer(1, 2, gl.FLOAT, false, 20, 8); gl.vertexAttribPointer(2, 1, gl.FLOAT, false, 20, 16); gl.drawArrays(gl.TRIANGLES, 0, 6); }
/* the light layer: the 2D part of it (only uploaded when something was drawn there) plus its GPU glows, into one full-size target, then the bloom */
function bglLight(b, fxL, W, H, busy) { const G = b.gl; if (!G || !b.glOn) return false;
  try { const g = G.o, gl = g.gl; bglTargets(g, W, H); const [a1, b1, a2, b2, F] = g.T, P = g.P;
    const pass = (prog, src, dst, px) => { const T = g.T[dst - 1]; gl.bindFramebuffer(gl.FRAMEBUFFER, T[3]); gl.viewport(0, 0, T[0], T[1]); gl.useProgram(prog.p); gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, src); gl.uniform1i(prog.u.t, 0); if (px) gl.uniform2f(prog.u.px, px[0], px[1]); bglFull(g); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); };
    gl.bindFramebuffer(gl.FRAMEBUFFER, F[3]); gl.viewport(0, 0, W, H); gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);
    if (fxL && b.fxDirty) { gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, g.L); gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true); gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, fxL); pass(P.copy, g.L, 5); }
    gl.bindFramebuffer(gl.FRAMEBUFFER, F[3]); gl.viewport(0, 0, W, H); bglDrawBatch(g, g.batch.l);
    pass(P.down, F[2], 1, [1 / W, 1 / H]); pass(P.blur, a1[2], 2, [1 / a1[0], 0]); pass(P.blur, b1[2], 1, [0, 1 / a1[1]]);
    pass(P.down, a1[2], 3, [1 / a1[0], 1 / a1[1]]); pass(P.blur, a2[2], 4, [1 / a2[0], 0]); pass(P.blur, b2[2], 3, [0, 1 / a2[1]]);
    /* the same bloom strength the 2D path used: part of it close around each light, the rest spread wide */
    const lv0 = b.qs <= 1.25 || b.tier >= 1 ? (busy ? .5 : .78) : b.qs < 1.75 ? (busy ? .34 : .54) + (busy ? .3 : .46) * .5 : (busy ? .3 : .46) + (busy ? .26 : .42) * .5;
    b.glComp = { e: b.expo, w1: Math.min(1.2, lv0 * b.expo) * .42, w2: Math.min(1.2, lv0 * b.expo) * .75 }; return true;
  } catch (e) { b.glFail = 1; b.glOn = false; bglHide(b); try { errCrumb("battle GPU light: " + (e && e.message)); } catch (er) {} return false; } }
/* end of a frame: the light, its bloom, the battlefield glows and the flash, onto the top layer */
function bglFlush(b) { const G = b.gl; if (!G || !b.glOn) return;
  try { const g = G.o, gl = g.gl, W = b.glW, H = b.glH; gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.viewport(0, 0, W, H); gl.clearColor(0, 0, 0, 0); gl.clear(gl.COLOR_BUFFER_BIT);
    const cp = b.glComp, fl = b.glFlash || 0;
    if (cp && g.T.length) { const [a1, , a2, , F] = g.T, C = g.P.comp; gl.useProgram(C.p); gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, F[2]); gl.uniform1i(C.u.L, 0); gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, a1[2]); gl.uniform1i(C.u.B1, 1); gl.activeTexture(gl.TEXTURE2); gl.bindTexture(gl.TEXTURE_2D, a2[2]); gl.uniform1i(C.u.B2, 2);
      gl.uniform1f(C.u.e, cp.e); gl.uniform1f(C.u.w1, cp.w1); gl.uniform1f(C.u.w2, cp.w2); gl.uniform4f(C.u.fl, fl, fl * .925, fl * .82, fl); bglFull(g); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); gl.activeTexture(gl.TEXTURE0); }
    bglDrawBatch(g, g.batch.a); b.glComp = null;
  } catch (e) { b.glFail = 1; b.glOn = false; bglHide(b); try { errCrumb("battle GPU flush: " + (e && e.message)); } catch (er) {} } }
function bglHide(b) { const G = b && b.gl; if (!G) return; for (const g of [G.o, G.u]) if (g && g.c && g.c.style.visibility !== "hidden") g.c.style.visibility = "hidden"; }
function bglFree(b) { const G = b && b.gl; if (!G) return; for (const g of [G.o, G.u]) { if (!g) continue; try { const x = g.gl.getExtension("WEBGL_lose_context"); if (x) x.loseContext(); } catch (e) {} try { g.c.remove(); } catch (e) {} } b.gl = null; }
