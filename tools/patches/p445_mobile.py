# v445 the Cube Devastation countdown hangs just past the edge of the map (owner: "move the countdown towards the edge of the map or
# maybe a little past"): always on the far side from the camera, like a sign on the horizon, gliding round as the camera turns.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep("if (!show) { if (W.dvCd) W.dvCd.grp.visible = false; return; }", "if (!show) { if (W.dvCd) { W.dvCd.grp.visible = false; W.dvCd.hid = 1; } return; }")
rep("""  C.grp.position.set(0, 128 + Math.sin(t * .0006) * 2, 0); C.grp.quaternion.copy(W.camera.quaternion);""",
"""  { const cp = W.camera.position, tg = (W.cam && W.cam.tx != null) ? W.cam : { tx: 0, tz: 0 }; let dx = tg.tx - cp.x, dz = tg.tz - cp.z, l = Math.hypot(dx, dz);
    if (l < 1) { const u = new TH.Vector3(0, 1, 0).applyQuaternion(W.camera.quaternion); dx = u.x; dz = u.z; l = Math.hypot(dx, dz) || 1; }
    const a = Math.atan2(dz / l, dx / l), da = C.a == null ? 9 : Math.atan2(Math.sin(a - C.a), Math.cos(a - C.a)), dt = Math.min(500, Math.max(0, t - (C.tl || t))); C.tl = t;
    C.a = Math.abs(da) > 1.2 || C.hid ? a : C.a + da * (1 - Math.exp(-dt / 350)); /* glides after the camera; a big swing (or coming back to the map) puts it straight there */
    const R = MAP_R + 70; C.hid = 0; C.grp.position.set(Math.cos(C.a) * R, 95 + Math.sin(t * .0006) * 2, Math.sin(C.a) * R); }
  C.grp.quaternion.copy(W.camera.quaternion);""")
# v445 the memory leak behind most phone crashes: three.js copies an object's userData through JSON, and a ship's userData holds live
# meshes (its engine glow, its parts), so every clone of a ship (each wreck on the map) serialised the whole model, textures as
# base64 included: 19 MB and seconds of work per hull, and ~100 MB held on the galaxy map. Clones now share three.js objects and typed
# arrays and copy only plain data.
rep("const TH = window.THREE;\n", """const TH = window.THREE;
(() => { const P = TH.Object3D.prototype, cp0 = P.copy;
  const ud = (v, d) => { if (v === null || typeof v !== "object") return v; if (d > 6 || ArrayBuffer.isView(v) || v.isObject3D || v.isMaterial || v.isTexture || v.isBufferGeometry || v instanceof Map || v instanceof Set) return v;
    if (Array.isArray(v)) return v.map(x => ud(x, d + 1)); const pr = Object.getPrototypeOf(v); if (pr !== Object.prototype && pr !== null) return v; const o = {}; for (const k in v) o[k] = ud(v[k], d + 1); return o; };
  P.copy = function (src, recursive = true) { const u = src.userData; src.userData = {}; try { cp0.call(this, src, false); } finally { src.userData = u; } this.userData = ud(u, 0);
    if (recursive) for (const c of src.children) this.add(c.clone()); return this; }; })(); /* v445 clones share three.js objects in userData (was a JSON copy of whole models) */
""")
# v445 a phone that crashed plays a notch lighter (resolution, effects, detail) for the next 3 days, then goes back to full detail
rep("G.lastCrashFresh = 1; return CRUMBS; }", "G.lastCrashFresh = 1; G.crashBoot = 1; return CRUMBS; }")
rep(""", WEAK = MOBILE && !IOS && ((navigator.hardwareConcurrency || 4) <= 4 || (navigator.deviceMemory || 4) <= 3);
""", """, WEAK = MOBILE && !IOS && ((navigator.hardwareConcurrency || 4) <= 4 || (navigator.deviceMemory || 4) <= 3);
if (MOBILE) { try { if (G.crashBoot) localStorage.setItem("udf.safeUntil", String(Date.now() + 3 * 864e5)); if (+localStorage.getItem("udf.safeUntil") > Date.now()) G.glSafe = 1; } catch (e) {} } /* v445 */
""")
rep("G.glSafe ? 2.4e6 : 3.4e6) / px)", "G.glSafe ? 1.4e6 : 3.4e6) / px)")
s, k = re.subn(r"GAME_V = 444\b", "GAME_V = 445", s); assert k == 1
open(P, 'w').write(s)
