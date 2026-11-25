"""v757: the cinematic camera stops jumping around a filmed monster. Owner (video of the Comet Ram in Orbit view): "I thought we fixed
the monsters from doing this". Cause: every frame the cinematic camera was shoved straight out of any planet whose 2.6x-radius bubble
it was inside. Among the dense planets a monster swims through, orbiting in and out of those bubbles teleported the camera to the far
side of a planet (whole frames of a planet instead of the monster). Now the camera behaves like a boom: it stays on the line to what it
films and only shortens when it would end up inside a planet, easing back out. A planet the subject is itself inside is ignored.
The filmed monster is also tracked by its body whether or not the fog flag hides it, so the aim no longer flips between body and spot."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 756;", "const GAME_V = 757;")
rep("""  if (o && o.mon && o.body && o.grp.visible) { const v = o.body.getWorldPosition(V3);""",
    """  if (o && o.mon && o.body && o.dc != null) { const v = o.body.getWorldPosition(V3);""")
rep("""else if (cam.cine) { try { const P = W.camera.position, Q = { x: P.x, y: P.y, z: P.z }; camClear(W, Q); if (Q.x !== P.x || Q.y !== P.y || Q.z !== P.z) { P.set(Q.x, Q.y, Q.z); W.camera.lookAt(cam.tx, cam.ty, cam.tz); } } catch (e) {} }""",
    """else if (cam.cine) { try { camBoom(W, cam); } catch (e) {} }""")
rep("""/* every cinematic camera keeps clear of stars and planets""",
    """/* v757 the cinematic camera is a boom: it stays on the line to its subject and only draws in (easing back out) to keep out of a planet
   (the glass worlds may pass between it and its subject) or in front of a star, instead of being shoved out of each planet's bubble, which teleported it round the far side */
function camBoom(W, cam) { const P = W.camera.position, tx = cam.tx, ty = cam.ty, tz = cam.tz, dx = P.x - tx, dy = P.y - ty, dz = P.z - tz, L = Math.hypot(dx, dy, dz); if (!(L > .01)) return;
  const ux = dx / L, uy = dy / L, uz = dz / L; let lim = L; const V = W._ccV || (W._ccV = new TH.Vector3());
  const hit = (cx, cy, cz, r, inOnly) => { const ox = tx - cx, oy = ty - cy, oz = tz - cz, c = ox * ox + oy * oy + oz * oz - r * r; if (c <= 0) return; if (inOnly && (P.x - cx) ** 2 + (P.y - cy) ** 2 + (P.z - cz) ** 2 > r * r) return; const b = ox * ux + oy * uy + oz * uz, h = b * b - c; if (h <= 0) return; const t0 = -b - Math.sqrt(h); if (t0 > 0 && t0 < lim) lim = t0; };
  for (const b of W.binaries || []) for (const st of [b.big, b.small]) { if (!st || !st.userData) continue; st.getWorldPosition(V); hit(V.x, V.y, V.z, (st.userData.rad || 4) * 3); }
  if (W.planets) for (const [, o] of W.planets) { if (!o.grp || !o.grp.visible) continue; const q = o.grp.position, r = (o.rad || 2) * (o.grp.scale.x || 1) * 1.15 + .2; if (Math.abs(q.x - P.x) > r || Math.abs(q.z - P.z) > r) continue; hit(q.x, q.y, q.z, r, 1); }
  const want = Math.max(Math.min(L, 1.2), lim * .92 - .2) / L, k = cam.boom == null ? want : cam.boom, e = 1 - Math.pow(want < k ? .55 : .93, W.dtk || 1); cam.boom = k + (want - k) * e;
  if (cam.boom < .999) { P.set(tx + dx * cam.boom, ty + dy * cam.boom, tz + dz * cam.boom); W.camera.lookAt(tx, ty, tz); } }
/* every cinematic camera keeps clear of stars and planets""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
# Owner: "wouldnt it be a good idea to slow down the monster animations in battle simulation? they seem very fast and not convincing".
# Battle frames ran the map's swim rhythms (written for a monster a few pixels long) on a creature filling the screen, squeezed into a
# 3 s loop of 16 baked poses: every rhythm was rounded up to at least one beat per 3 s (a slow 0.5 sway ran 4x fast) and a tail beat
# got 8 poses. Now the loop is 6 s of 24 poses (14 on weaker phones), every rhythm plays at half its map speed, moving adds a fifth
# rather than a third, and the Mimics keep their heavier pace relative to the rest.
s = open(p, encoding="utf-8").read()
rep("""const MBF_P = 3, MBF_Z = 1.25, MBF_N = (typeof WEAK !== "undefined" && WEAK) || (typeof IOS !== "undefined" && IOS) ? 10 : 16, MBF_W = 2 * Math.PI / MBF_P;""",
    """const MBF_P = 6, MBF_Z = 1.25, MBF_N = (typeof WEAK !== "undefined" && WEAK) || (typeof IOS !== "undefined" && IOS) ? 14 : 24, MBF_W = 2 * Math.PI / MBF_P, MBF_SL = .5; /* v757 a 6 s loop at half the map's pace (was 3 s of 16 poses at full pace) */""")
rep("""(Math.max(+f >= .6 ? 1 : 0, Math.round(+f / MBF_W)) * MBF_W).toFixed(5));""",
    """(Math.max(+f >= .6 ? 1 : 0, Math.round(+f * MBF_SL / MBF_W)) * MBF_W).toFixed(5));""")
rep("""/ 1000 / MBF_P * (moving ? 1.35 : 1) * (MIM_D[k] ? .5 : 1)""", """/ 1000 / MBF_P * (moving ? 1.2 : 1) * (MIM_D[k] ? .7 : 1)""")
open(p, "w", encoding="utf-8").write(s)
print("ok2")
