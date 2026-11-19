# v643 (prototype): livery remaster. Imported ship models are one mesh with a scrambled AI texture atlas, so zones come from
# the hull's shape: wings/side fins, top towers/fins, nose and tail caps and a spine stripe take the trim; the model's own
# brightest texels (windows, lamps) take the lights; the rest is hull. Finishes are clean metals and gems shaded over the
# model's own surface detail (no more photo texture wrapped over everything).
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)

rep('function hullFinish(obj, sp) {', r'''/* v643 livery materials */
const LIV_K = { gold: 0, silver: 0, copper: 0, cobalt: 0, pink: 1, amethyst: 1, ruby: 1, emerald: 1, obsidian: 2, diamond: 3, glyph: 4 }; // 0 metal, 1 gem, 2 obsidian, 3 diamond, 4 holo
const LIV_C = { gold: "#ffc23a", silver: "#e6edf5", copper: "#e07a3e", cobalt: "#2d63ff", pink: "#ff4fb8", obsidian: "#120d18", amethyst: "#9a45ff", diamond: "#eaf7ff", ruby: "#ff1035", emerald: "#0fe070", glyph: "#30e8ff" };
const LIV_MR = [[1, .13], [.25, .07], [.7, .05], [.15, .04], [.4, .15]]; // metalness, roughness per kind
const LIV_P = { def: [.58, .6, .84, .05] }; // lateral fins, top, nose/tail, spine stripe half-width (shares of the half-size)
function livMat(m, f, t, k, geo) { const F = HULL_F[f]; if (!F || !TH || !m || !m.isMeshStandardMaterial) return m; t = t && HULL_F[t] ? t : f;
  if (!geo.boundingBox) geo.computeBoundingBox(); const bb = geo.boundingBox, c = bb.getCenter(new TH.Vector3()), h = bb.getSize(new TH.Vector3()).multiplyScalar(.5);
  const ka = LIV_K[f], kb = LIV_K[t], P = LIV_P[k] || LIV_P.def, lt = new TH.Color(HULL_F[t].rim);
  const n = m.clone(); n.envMapIntensity = 1.75; n.extensions = Object.assign({}, n.extensions, { derivatives: true });
  const lin = h => new TH.Color(h).convertSRGBToLinear(); /* colours were going in as if already linear: everything came out pale */
  n.onBeforeCompile = sh => { const U = sh.uniforms; U.uA = { value: lin(LIV_C[f]) }; U.uB = { value: lin(LIV_C[t]) }; U.uRA = { value: lin(F.rim) }; U.uRB = { value: lin(HULL_F[t].rim) };
      U.uK = { value: new TH.Vector2(ka, kb) }; U.uMR = { value: new TH.Vector4(LIV_MR[ka][0], LIV_MR[ka][1], LIV_MR[kb][0], LIV_MR[kb][1]) }; U.uLt = { value: lt.clone().convertSRGBToLinear() };
      U.uBc = { value: c }; U.uBh = { value: h }; U.uLP = { value: new TH.Vector4(P[0], P[1], P[2], P[3]) }; U.uT = HULL_TU;
      sh.vertexShader = "uniform vec3 uBc; uniform vec3 uBh; varying vec3 vLN; varying vec3 vON;\n" + sh.vertexShader.replace("#include <project_vertex>", "#include <project_vertex>\n vLN = (position - uBc) / max(uBh, vec3(1e-4)); vON = normalize(normal);");
      sh.fragmentShader = `uniform vec3 uA; uniform vec3 uB; uniform vec3 uRA; uniform vec3 uRB; uniform vec2 uK; uniform vec4 uMR; uniform vec3 uLt; uniform vec4 uLP; uniform float uT; varying vec3 vLN; varying vec3 vON;
vec3 lvHsv(float h, float s, float v) { vec3 k = clamp(abs(mod(h * 6.0 + vec3(0.0, 4.0, 2.0), 6.0) - 3.0) - 1.0, 0.0, 1.0); return v * mix(vec3(1.0), k, s); }
float lvEdge(float e, float v) { float w = fwidth(v) + 1e-4; return smoothstep(e - w, e + w, v); }
float lvZone(vec3 q, float o) { float t = max(lvEdge(uLP.x - o, abs(q.z)), lvEdge(uLP.y - o, q.y)); t = max(t, lvEdge(uLP.z - o, abs(q.x)));
  return max(t, (1.0 - lvEdge(uLP.w + o, abs(q.z))) * step(.5, vON.y) * step(-o, q.y)); }
vec3 lvShade(vec3 base, float kd, float d, vec3 q, float fr, out vec3 em, vec3 rim) { em = vec3(0.0);
  if (kd < .5) return base * (0.16 + 0.95 * d);
  if (kd < 1.5) { em = base * (0.14 + 0.42 * fr + 0.12 * d); return base * (0.12 + 0.75 * d); }
  if (kd < 2.5) { em = rim * pow(fr, 3.0) * 0.16; return base * (0.55 + 0.5 * d); }
  if (kd < 3.5) { float sp = fract(sin(dot(floor(q * 46.0), vec3(12.99, 78.23, 37.71))) * 43758.55); em = lvHsv(fract(sp * 3.1 + fr * 1.5 + uT * .05), .7, 1.0) * pow(sp, 14.0) * (0.6 + 0.4 * sin(uT * 2.3 + sp * 40.0)) * 3.5 + lvHsv(fract(q.x * 1.3 + fr * 2.0), .35, 1.0) * pow(fr, 2.0) * .45; return base * (0.18 + 0.7 * d); }
  vec3 hc = lvHsv(fract(q.x * .45 + q.y * .3 + fr * .7 + uT * .03), .55, 1.0); em = hc * .28; return hc * (0.22 + 0.6 * d); }
` + sh.fragmentShader
        .replace("#include <map_fragment>", `#include <map_fragment>
 vec3 lvE = vec3(0.0); float lvTr = 0.0, lvLt = 0.0;
 { float hl = dot(diffuseColor.rgb, vec3(.3, .59, .11)), d = clamp(hl / .32, .12, 1.7); vec3 q = vLN;
   float fr = pow(1.0 - clamp(abs(dot(normalize(vNormal), normalize(vViewPosition))), 0.0, 1.0), 1.6);
   lvTr = lvZone(q, 0.0); float lvBand = clamp(lvZone(q, .045) - lvTr, 0.0, 1.0);
   lvLt = smoothstep(.55, .85, hl);
   vec3 eA, eB; vec3 cA = lvShade(uA, uK.x, d, q, fr, eA, uRA), cB = lvShade(uB, uK.y, d, q, fr, eB, uRB);
   diffuseColor.rgb = mix(mix(cA, cB, lvTr), uLt * .25, lvLt); lvE = mix(eA, eB, lvTr) + uLt * lvLt * 3.0;
   float pu = .6 + .4 * sin(uT * 1.8 - q.x * 5.0);
   lvE += uRB * lvTr * (pow(fr, 2.2) * .75 + .02);
   lvE += uRB * lvBand * 2.6 * pu;
   { vec3 an = abs(vON); vec2 g = an.y > an.z ? q.xz : q.xy; g *= vec2(7.0, 4.0); vec2 d2 = .5 - abs(fract(g) - .5); float dd = min(d2.x, d2.y), w = fwidth(dd) + 1e-4;
     float ln = (1.0 - smoothstep(w * .7, w * 2.2, dd)) * (1.0 - smoothstep(.12, .3, w)) * step(.55, fract(sin(dot(floor(g), vec2(12.99, 78.23))) * 43758.55));
     lvE += uRB * ln * (1.0 - lvTr) * 1.6 * (.45 + .55 * sin(uT * 2.4 - q.x * 7.0)); diffuseColor.rgb *= 1.0 - ln * .35; } }`)
        .replace("#include <roughnessmap_fragment>", "#include <roughnessmap_fragment>\n roughnessFactor = mix(mix(uMR.y, uMR.w, lvTr), .6, lvLt);")
        .replace("#include <metalnessmap_fragment>", "#include <metalnessmap_fragment>\n metalnessFactor = mix(mix(uMR.x, uMR.z, lvTr), 0.0, lvLt);")
        .replace("#include <emissivemap_fragment>", "#include <emissivemap_fragment>\n totalEmissiveRadiance += lvE;"); };
  n.customProgramCacheKey = () => "livery2"; n.needsUpdate = true; return n; }
function hullFinish(obj, sp, k) {''')
# imported models (untagged materials) use the livery shader; hand-built ships keep their roles
rep("      return finMat(m, t && (nm === \"dark\" || nm === \"trim\" || nm === \"gold\") ? t : f, false, { ps, inl, auto: !nm && t ? t : null }); };",
    "      if (!nm && o.geometry && o.geometry.attributes.uv) return livMat(m, f, t, k, o.geometry); /* v643 */\n"
    "      return finMat(m, t && (nm === \"dark\" || nm === \"trim\" || nm === \"gold\") ? t : f, false, { ps, inl, auto: !nm && t ? t : null }); };")
rep('if (fin && kind === "s") hullFinish(ship, fin);', 'if (fin && kind === "s") hullFinish(ship, fin, k);')
# a model that lands while a panel is open now replaces the stand-in pictures in that panel too (it only redrew with no panel open)
rep("    clearTimeout(glbReady.t); glbReady.t = setTimeout(() => { if (!battle && !sheet && typeof render === \"function\") try { render(); } catch (e) {} }, 400); }",
    "    clearTimeout(glbReady.t); glbReady.t = setTimeout(() => { try { document.querySelectorAll(`canvas[data-ship=\"${k}\"]`).forEach(c => { c._dk = null; c._pend = null; }); if (sheet) thumbs(document); } catch (e) {} if (!battle && !sheet && typeof render === \"function\") try { render(); } catch (e) {} }, 400); }")
rep('n2 = finMat(m, t0 && /^(dark|trim|gold)$/.test(nm) ? t0 : f0, true, { inl });', 'n2 = finMat(m, t0 && /^(dark|trim|gold)$/.test(nm) ? t0 : f0, true, { inl, glow: !!(t0 && /^(dark|trim|gold)$/.test(nm)) });')
rep('U.uRim = { value: new TH.Color(F.rim) }; U.uInl = { value: inl };', 'U.uRim = { value: new TH.Color(F.rim) }; U.uInl = { value: inl }; U.uGlw = { value: o.glow ? 1.6 : 0 };')
rep('sh.fragmentShader = "uniform vec3 uRim; uniform vec3 uInl; uniform float uT;"', 'sh.fragmentShader = "uniform vec3 uRim; uniform vec3 uInl; uniform float uT; uniform float uGlw;"')
rep('totalEmissiveRadiance += uRim * hf * (" + (tex ? ".35" : ".85") + ") + hGl;"', 'totalEmissiveRadiance += uRim * hf * (" + (tex ? ".35" : ".85") + ") + hGl + uInl * (hf * 1.2 + .25) * uGlw;"')
rep('n.customProgramCacheKey = () => "hullfin-" + f + (tex ? "-t" : "") + (obj ? "-o" : "")', 'n.customProgramCacheKey = () => "hullfin-" + f + (tex ? "-t" : "") + (obj ? "-o" : "") + (o.glow ? "-g" : "")')
rep('const GAME_V = 648', 'const GAME_V = 649')
open(p, 'w', encoding='utf-8').write(s)
