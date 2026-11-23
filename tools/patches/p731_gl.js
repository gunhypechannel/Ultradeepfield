/* ---------- v731 the battle's light on the graphics chip (owner: "How can we make our game run directly on phones graphic chip?") ----------
   Every beam, bolt, fireball and spark of a battle is drawn on its own light layer, which then had to be laid over the battlefield and
   given its bloom (the glow that bleeds around hot cores). On a phone that was most of the frame: in the Android app the browser draws
   2D canvases without the GPU, and three full-screen copies plus a blurred enlargement cost about 60 ms a frame (10 fps in battle).
   Now the light layer goes to WebGL once a frame and the GPU does the rest: the bloom is a real two-size blur, and the result sits on
   its own canvas over the battle, added to it by the compositor (mix-blend-mode: plus-lighter), exactly as the old "lighter" draw did.
   Without WebGL or plus-lighter, or after a lost GPU context, the old 2D path draws it as before. ?gl2d forces the old path. */
const BGL_OK = (() => { try { return !/[?&]gl2d\b/.test(location.search) && !!(window.CSS && CSS.supports && CSS.supports("mix-blend-mode", "plus-lighter")); } catch (e) { return false; } })();
const BGL_VS = "attribute vec2 p;varying vec2 v;void main(){v=p*.5+.5;gl_Position=vec4(p,0.,1.);}";
const BGL_FS = {
  copy: "precision mediump float;uniform sampler2D t;varying vec2 v;void main(){gl_FragColor=texture2D(t,v);}",
  /* a 4x shrink that averages the whole 4x4 block (four bilinear taps), so thin shots don't sparkle in and out */
  down: "precision mediump float;uniform sampler2D t;uniform vec2 px;varying vec2 v;void main(){gl_FragColor=.25*(texture2D(t,v+px*vec2(-1.,-1.))+texture2D(t,v+px*vec2(1.,-1.))+texture2D(t,v+px*vec2(-1.,1.))+texture2D(t,v+px*vec2(1.,1.)));}",
  blur: "precision mediump float;uniform sampler2D t;uniform vec2 px;varying vec2 v;void main(){vec4 c=texture2D(t,v)*.2270270;c+=(texture2D(t,v+px*1.3846154)+texture2D(t,v-px*1.3846154))*.3162162;c+=(texture2D(t,v+px*3.2307692)+texture2D(t,v-px*3.2307692))*.0702703;gl_FragColor=c;}",
  comp: "precision mediump float;uniform sampler2D L;uniform sampler2D B1;uniform sampler2D B2;uniform float e;uniform float w1;uniform float w2;varying vec2 v;void main(){gl_FragColor=min(texture2D(L,v)*e+texture2D(B1,v)*w1+texture2D(B2,v)*w2,vec4(1.));}" };
function bglInit(b, cv) {
  const c = document.createElement("canvas"); c.className = "bgl"; c.setAttribute("aria-hidden", "true"); cv.parentNode.insertBefore(c, cv.nextSibling);
  const gl = c.getContext("webgl", { alpha: true, premultipliedAlpha: true, antialias: false, depth: false, stencil: false, preserveDrawingBuffer: true, powerPreference: "high-performance" }); if (!gl) { c.remove(); return null; }
  const sh = (ty, src) => { const s = gl.createShader(ty); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error("bgl shader: " + gl.getShaderInfoLog(s)); return s; }, vs = sh(gl.VERTEX_SHADER, BGL_VS);
  const P = {}; for (const k in BGL_FS) { const p = gl.createProgram(); gl.attachShader(p, vs); gl.attachShader(p, sh(gl.FRAGMENT_SHADER, BGL_FS[k])); gl.bindAttribLocation(p, 0, "p"); gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error("bgl link"); const u = {}; for (const n of ["t", "px", "L", "B1", "B2", "e", "w1", "w2"]) u[n] = gl.getUniformLocation(p, n); P[k] = { p, u }; }
  const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW); gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
  const tex = () => { const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t); for (const [k, v] of [[gl.TEXTURE_MIN_FILTER, gl.LINEAR], [gl.TEXTURE_MAG_FILTER, gl.LINEAR], [gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE], [gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE]]) gl.texParameteri(gl.TEXTURE_2D, k, v); return t; };
  const g = { c, gl, P, L: tex(), T: [], w: 0, h: 0, lost: 0 }; g.mk = tex;
  c.addEventListener("webglcontextlost", e => { e.preventDefault(); g.lost = 1; b.glFail = 1; try { crumb("battle GPU light lost"); } catch (er) {} }, false);
  gl.disable(gl.BLEND); gl.disable(gl.DEPTH_TEST); return g; }
/* render targets: [w, h, texture, framebuffer] at a quarter and a sixteenth of the battlefield, two of each for the two blur directions */
function bglTargets(g, W, H) { const gl = g.gl; if (g.w === W && g.h === H) return; g.w = W; g.h = H; for (const T of g.T) { gl.deleteTexture(T[2]); gl.deleteFramebuffer(T[3]); } g.T = [];
  for (const dv of [4, 4, 16, 16]) { const w = Math.max(2, Math.ceil(W / dv)), h = Math.max(2, Math.ceil(H / dv)), t = g.mk(); gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, w, h, 0, gl.RGBA, gl.UNSIGNED_BYTE, null); const f = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, f); gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, t, 0); g.T.push([w, h, t, f]); }
  gl.bindFramebuffer(gl.FRAMEBUFFER, null); }
/* draws the light layer (and its bloom) on the GPU; false means the caller draws it the old 2D way */
function bglLight(b, cv, fxL, W, H, busy) {
  if (!BGL_OK || b.glFail || !fxL) return false;
  try { let g = b.gl; if (!g || g.lost || !g.c.isConnected) { if (g && g.lost) return false; g = b.gl = bglInit(b, cv); if (!g) { b.glFail = 1; return false; } }
    const gl = g.gl; if (g.c.width !== W || g.c.height !== H) { g.c.width = W; g.c.height = H; } g.c.style.visibility = ""; bglTargets(g, W, H);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, g.L); gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true); gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, fxL);
    const pass = (prog, src, dst, px) => { const T = dst ? g.T[dst - 1] : null; gl.bindFramebuffer(gl.FRAMEBUFFER, T ? T[3] : null); gl.viewport(0, 0, T ? T[0] : W, T ? T[1] : H); gl.useProgram(prog.p); gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, src); gl.uniform1i(prog.u.t, 0); if (px) gl.uniform2f(prog.u.px, px[0], px[1]); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); };
    const [a1, b1, a2, b2] = g.T, P = g.P;
    pass(P.down, g.L, 1, [1 / W, 1 / H]); pass(P.blur, a1[2], 2, [1 / a1[0], 0]); pass(P.blur, b1[2], 1, [0, 1 / a1[1]]);
    pass(P.down, a1[2], 3, [1 / a1[0], 1 / a1[1]]); pass(P.blur, a2[2], 4, [1 / a2[0], 0]); pass(P.blur, b2[2], 3, [0, 1 / a2[1]]);
    /* the same bloom strength the 2D path used: a third of it close around each light, the rest spread wide */
    const lv0 = b.qs <= 1.25 || b.tier >= 1 ? (busy ? .5 : .78) : b.qs < 1.75 ? (busy ? .34 : .54) + (busy ? .3 : .46) * .5 : (busy ? .3 : .46) + (busy ? .26 : .42) * .5, bs = Math.min(1.2, lv0 * b.expo);
    gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.viewport(0, 0, W, H); const C = P.comp; gl.useProgram(C.p);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, g.L); gl.uniform1i(C.u.L, 0); gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, a1[2]); gl.uniform1i(C.u.B1, 1); gl.activeTexture(gl.TEXTURE2); gl.bindTexture(gl.TEXTURE_2D, a2[2]); gl.uniform1i(C.u.B2, 2);
    gl.uniform1f(C.u.e, b.expo); gl.uniform1f(C.u.w1, bs * .42); gl.uniform1f(C.u.w2, bs * .75); gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4); gl.activeTexture(gl.TEXTURE0);
    return true; } catch (e) { b.glFail = 1; try { if (b.gl) b.gl.c.style.visibility = "hidden"; errCrumb("battle GPU light: " + (e && e.message)); } catch (er) {} return false; } }
function bglHide(b) { if (b.gl && b.gl.c && b.gl.c.style.visibility !== "hidden") b.gl.c.style.visibility = "hidden"; }
function bglFree(b) { const g = b && b.gl; if (!g) return; try { const x = g.gl.getExtension("WEBGL_lose_context"); if (x) x.loseContext(); } catch (e) {} try { g.c.remove(); } catch (e) {} b.gl = null; }
