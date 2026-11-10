# v409 (1): shader compiles no longer force the browser to wait. three.js checks every new shader program by reading its info logs
# (getProgramInfoLog / getShaderInfoLog right after linking), which blocks until the compile finishes, so each new material stalled the
# frame it first drew in (measured: most of the map pre-build's cost on the base screen, and the freezes logged on the galaxy). With the
# check off, browsers that compile in parallel (KHR_parallel_shader_compile) keep drawing meanwhile. ?gldebug turns it back on.
p = "docs/index.html"; t = open(p).read()
n = t.count("new TH.WebGLRenderer("); assert n == 4, n
t = t.replace("new TH.WebGLRenderer(", "glNew(")
a = "const NZ"
assert t.count("function glNew(") == 0
i = t.index("function frame(t) {")
t = t[:i] + """/* v409 every 3D renderer is made here: shader error checks only with ?gldebug (they block until each compile finishes) */
function glNew(o) { const r = new TH.WebGLRenderer(o); try { r.debug.checkShaderErrors = /[?&]gldebug/.test(location.search); } catch (e) {} return r; }
""" + t[i:]
open(p, "w").write(t); print("ok")

