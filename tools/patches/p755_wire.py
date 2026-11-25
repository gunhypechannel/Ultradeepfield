"""v755: the Cube Destroyer opaque under every hull finish (owner, photo of a battle: "Cube destroyer still not fixed").
finMat lowered diffuseColor.a for Glyph Holo even on a solidHolo hull, and that alpha went straight into the baked battle sprite (the
canvas keeps it), so the sphere showed its far side, plating grid and equator band through the front. Only the hull, trench and
collar were marked solid; the rest of its parts were not. Now every part of a worldbreaker is solid in hullFinish, and a solid
finMat writes alpha 1 (its glass parts darken instead)."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:160]); s = s.replace(a, b)
rep("const GAME_V = 754;", "const GAME_V = 755;")
rep("""  const n = m.clone(), solid = !!(m.userData && m.userData.solidHolo); if (gly && !solid) {""",
    """  const n = m.clone(), solid = !!((m.userData && m.userData.solidHolo) || o.solid); if (gly && !solid) {""")
# a solid finMat: alpha 1, the see-through part of the glyph glass goes dark instead
rep("""diffuseColor.a *= clamp(.24 + .76 * pow(hf, 1.3) + fgM * .75, 0.0, 1.0);" : "") + " }"); };""",
    """diffuseColor.a *= clamp(.24 + .76 * pow(hf, 1.3) + fgM * .75, 0.0, 1.0);" : "") + " }");
    if (solid) sh.fragmentShader = sh.fragmentShader.replace("gl_FragColor = vec4( outgoingLight, diffuseColor.a );", "gl_FragColor = vec4( outgoingLight * mix(.3, 1.0, diffuseColor.a), 1.0 );"); /* v755 */ };""")
rep("""  const solid = !!(m.userData && m.userData.solidHolo), keep = m.userData && m.userData.keepOBC ? m.onBeforeCompile : null, keepK = keep && m.customProgramCacheKey ? m.customProgramCacheKey() : ""; /* v737 see finMat */""",
    """  const solid = !!((m.userData && m.userData.solidHolo) || k === "worldbreaker"), keep = m.userData && m.userData.keepOBC ? m.onBeforeCompile : null, keepK = keep && m.customProgramCacheKey ? m.customProgramCacheKey() : ""; /* v737 see finMat; v755 every part of the Cube Destroyer */""")
rep("""      return finMat(m, t && (nm === "dark" || nm === "trim" || nm === "gold") ? t : f, false, { ps, inl, auto: !nm && t ? t : null }); };""",
    """      return finMat(m, t && (nm === "dark" || nm === "trim" || nm === "gold") ? t : f, false, { ps, inl, auto: !nm && t ? t : null, solid: k === "worldbreaker" }); }; /* v755 */""")
# the turn: 24 baked poses 15 degrees apart, the nearest one drawn alone (the cross-fade between two poses 30 degrees apart drew two dishes and
# two equator bands on one sphere while it turned: the owner's "distorted and overlapped look")
rep("""M = R(CD_PHI0 + rotK * Math.PI / 6).multiply(R(CD_PHI0).invert());""", """M = R(CD_PHI0 + rotK * CD_ST).multiply(R(CD_PHI0).invert()); /* v755 15-degree steps */""")
rep("""function cdPortDrawn(phi, base) { const u = (phi - CD_PHI0) / (Math.PI / 6), k0 = Math.floor(u), w = u - k0, A = ((k0 % 12) + 12) % 12, B = (A + 1) % 12, got = k => !k || !base || !!shipArtSoon("worldbreaker", base + "~p" + k, "side");
  const a = got(A), bb = got(B), PA = CD_PORT[A], PB = CD_PORT[B]; if (a && bb) return [PA[0] + (PB[0] - PA[0]) * w, PA[1] + (PB[1] - PA[1]) * w]; return a ? PA : bb ? PB : CD_PORT[0]; }""",
    """const CD_N = 24, CD_ST = 2 * Math.PI / 24; /* v755 */
function cdPort24(k) { const h = k / 2, A = Math.floor(h) % 12, B = (A + 1) % 12, w = h - Math.floor(h); return [CD_PORT[A][0] + (CD_PORT[B][0] - CD_PORT[A][0]) * w, CD_PORT[A][1] + (CD_PORT[B][1] - CD_PORT[A][1]) * w]; }
function cdNear(phi, base) { const k0 = ((Math.round((phi - CD_PHI0) / CD_ST) % CD_N) + CD_N) % CD_N, got = k => !k || !base || !!shipArtSoon("worldbreaker", base + "~p" + k, "side");
  for (let d = 0; d <= CD_N / 2; d++) for (const k of d ? [(k0 + d) % CD_N, (k0 - d + CD_N) % CD_N] : [k0]) if (got(k)) return k; return 0; } /* the nearest baked pose */
function cdPortDrawn(phi, base) { return cdPort24(cdNear(phi, base)); }""")
rep("""function cdPose(phi, base) { const st = Math.PI / 6,""", """function cdPose(phi, base) { const k = cdNear(phi, base); return [k ? base + "~p" + k : base, null, 0]; } /* v755 one pose at a time */
function cdPoseOld(phi, base) { const st = Math.PI / 6,""")
rep("""for (let k = 1; k < 12; k++) shipArtSoon("worldbreaker", base + "~p" + k, "side"); } /* v416 bake every pose up front */""",
    """for (let k = 1; k < CD_N; k++) shipArtSoon("worldbreaker", base + "~p" + k, "side"); } /* v416 bake every pose up front (v755 24) */""")
open(p, "w", encoding="utf-8").write(s)
print("ok")
