# v654 Glyph Holo remaster (owner: "remaster the glyph premium hull to be more transparent like with multi color glyphs and rune
# symbols"). The holo finish was an opaque rainbow sheen. Now it is hologram glass: the faces are see-through and turn solid toward the
# silhouette, a rainbow rim light runs round the edges, a scan line drifts along the hull, and the surface carries a field of rune
# symbols (64 procedural runes: staves, circled sigils, triangles and twin staves) in many colours, each fading in, changing and
# fading out on its own rhythm. Imported models (livMat) and hand-built hulls (finMat) both; battle pictures show it too.
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)

GLY_FN = r'''float lvGly(vec3 qi, vec3 on, float t, out vec3 col) { vec3 an = abs(on); vec2 g = an.x > an.y && an.x > an.z ? qi.zy : (an.y > an.z ? qi.xz : qi.xy); g *= 9.0;
  vec2 ce = floor(g), f = fract(g); float h = fract(sin(dot(ce, vec2(12.99, 78.23))) * 43758.55); col = vec3(0.0); if (h < .3) return 0.0;
  float ph = t * .22 + h * 9.0, cy = floor(ph), env = sin(fract(ph) * 3.14159); float id = floor(fract(sin((cy + h * 31.0) * 12.99) * 43758.55) * 64.0);
  vec2 uv = (vec2(mod(id, 8.0), floor(id / 8.0)) + .08 + f * .84) / 8.0; float m = texture2D(uGA, uv).r;
  col = lvHsv(fract(h * 5.7 + cy * .13 + t * .02), 1.0, 1.0); return m * (.3 + .7 * env); }
'''

# --- the rune atlas
rep('/* v643 livery materials */', r'''/* v654 the Glyph Holo's runes: 64 procedural runes in an 8 x 8 atlas, white on black */
let GLY_T = null;
function glyTex() { if (GLY_T) return GLY_T; const N = 512, c = document.createElement("canvas"); c.width = c.height = N; const x = c.getContext("2d"), r = rnd(4242), s = N / 8;
  x.fillStyle = "#000"; x.fillRect(0, 0, N, N); x.strokeStyle = "#fff"; x.fillStyle = "#fff"; x.lineCap = "round"; x.lineJoin = "round"; x.lineWidth = s * .08;
  for (let i = 0; i < 64; i++) { x.save(); x.translate((i % 8 + .5) * s, ((i / 8 | 0) + .5) * s); const u = s * .3, ty = i % 4; x.beginPath();
    if (ty === 0) { x.moveTo(0, -u); x.lineTo(0, u); const nb = 1 + (r() * 3 | 0); for (let b = 0; b < nb; b++) { const y0 = -u + r() * u * 1.4, sd = r() < .5 ? -1 : 1, y1 = y0 + (r() - .3) * u * .9; x.moveTo(0, y0); x.lineTo(sd * u * .6, y1); if (r() < .4) { x.moveTo(0, y0); x.lineTo(-sd * u * .6, y1); } } }
    else if (ty === 1) { x.arc(0, 0, u * .7, 0, TAU); x.moveTo(0, -u); x.lineTo(0, u); if (r() < .5) { x.moveTo(-u * .7, 0); x.lineTo(u * .7, 0); } else { x.moveTo(-u * .5, -u * .2); x.lineTo(0, u * .3); x.lineTo(u * .5, -u * .2); } }
    else if (ty === 2) { const n = r() < .5 ? 3 : 4; for (let k = 0; k <= n; k++) { const a = k / n * TAU - Math.PI / 2; x[k ? "lineTo" : "moveTo"](Math.cos(a) * u * .85, Math.sin(a) * u * .85); } x.moveTo(0, 0); x.lineTo(0, -u * .85 * (r() < .5 ? 1 : -.6)); }
    else { x.moveTo(-u * .45, -u); x.lineTo(-u * .45, u); x.moveTo(u * .45, -u); x.lineTo(u * .45, u); const y0 = (r() - .5) * u; x.moveTo(-u * .45, y0 - u * .4); x.lineTo(u * .45, y0 + u * .4); if (r() < .5) { x.moveTo(-u * .45, y0 + u * .4); x.lineTo(u * .45, y0 - u * .4); } }
    x.stroke(); if (r() < .35) { x.beginPath(); x.arc((r() - .5) * u, (r() - .5) * u * 1.4, s * .05, 0, TAU); x.fill(); } x.restore(); }
  GLY_T = new TH.CanvasTexture(c); GLY_T.generateMipmaps = false; GLY_T.minFilter = TH.LinearFilter; GLY_T.magFilter = TH.LinearFilter; return GLY_T; }
/* v643 livery materials */''')

# --- livMat: the holo shading, the runes, the transparency
rep('  vec3 hc = lvHsv(fract(q.x * .45 + q.y * .3 + fr * .7 + uT * .03), .55, 1.0); em = hc * .28; return hc * (0.22 + 0.6 * d); }',
    '  vec3 hc = lvHsv(fract(q.x * .45 + q.y * .3 + fr * .7 + uT * .03), .6, 1.0); em = hc * (.1 + pow(fr, 1.5) * 1.1); return mix(vec3(.02, .1, .14), hc, .55) * (0.25 + 0.5 * d); }\n' + GLY_FN)
rep('uniform vec4 uLP; uniform float uT; varying vec3 vLN; varying vec3 vON;\nvec3 lvHsv', 'uniform vec4 uLP; uniform float uT; uniform sampler2D uGA; uniform vec3 uBh; varying vec3 vLN; varying vec3 vON;\nvec3 lvHsv')
rep(' vec3 lvE = vec3(0.0); float lvTr = 0.0, lvLt = 0.0;', ' vec3 lvE = vec3(0.0); float lvTr = 0.0, lvLt = 0.0, lvAl = 1.0;')
rep("     lvE += uRB * ln * (1.0 - lvTr) * 1.6 * (.45 + .55 * sin(uT * 2.4 - q.x * 7.0)); diffuseColor.rgb *= 1.0 - ln * .35; } }`)",
    """     lvE += uRB * ln * (1.0 - lvTr) * 1.6 * (.45 + .55 * sin(uT * 2.4 - q.x * 7.0)); diffuseColor.rgb *= 1.0 - ln * .35; }
   /* v654 Glyph Holo: glass you can see through, solid toward the silhouette, runes in many colours, a drifting scan line */
   float hw = mix(step(3.5, uK.x), step(3.5, uK.y), lvTr) * (1.0 - lvLt);
   if (hw > .01) { vec3 qi = vLN * uBh / max(uBh.x, max(uBh.y, uBh.z)); vec3 gc; float gm = lvGly(qi, vON, uT, gc) * hw;
     float sc = pow(max(0.0, sin(q.x * 3.0 - uT * 1.7)), 24.0), sl = .5 + .5 * sin(q.y * 90.0 + uT * 2.0);
     lvE += gc * gm * 1.5 + lvHsv(fract(q.x * .5 + uT * .05), .5, 1.0) * hw * (sc * .9 + sl * .05);
     diffuseColor.rgb = mix(diffuseColor.rgb, gc * .5, gm * .6);
     lvAl = mix(1.0, clamp(.22 + .78 * pow(fr, 1.3) + gm * .75 + sc * .25, 0.0, 1.0), hw); }
   diffuseColor.a *= lvAl; }`)""")
rep('U.uBc = { value: c }; U.uBh = { value: h };', 'U.uBc = { value: c }; U.uBh = { value: h }; U.uGA = { value: glyTex() };')
rep('  const n = m.clone(); n.envMapIntensity = 1.75;', '  const n = m.clone(); n.envMapIntensity = 1.75; if (ka === 4 || kb === 4) { n.transparent = true; n.depthWrite = true; } /* v654 */')
rep('n.customProgramCacheKey = () => "livery2"; n.needsUpdate = true; return n; }', 'n.customProgramCacheKey = () => "livery3"; n.needsUpdate = true; return n; }')

# --- finMat (hand-built hulls and map fleets)
rep("  const n = m.clone(); n.metalness = tex ? (F.tm != null ? F.tm : .2) : F.met;", "  const gly = f === \"glyph\"; /* v654 */\n  const n = m.clone(); if (gly) { n.transparent = true; n.depthWrite = true; } n.metalness = tex ? (F.tm != null ? F.tm : .2) : F.met;")
rep('U.uRim = { value: new TH.Color(F.rim) }; U.uInl = { value: inl };', 'U.uRim = { value: new TH.Color(F.rim) }; U.uInl = { value: inl }; if (gly) U.uGA = { value: glyTex() };')
rep('''      sh.fragmentShader = "uniform vec3 uRim; uniform vec3 uInl; uniform float uT; uniform float uGlw;" + dec(1)''',
    '''      sh.fragmentShader = "uniform vec3 uRim; uniform vec3 uInl; uniform float uT; uniform float uGlw;" + (gly ? " uniform sampler2D uGA;\\nvec3 lvHsv(float h, float s, float v) { vec3 k = clamp(abs(mod(h * 6.0 + vec3(0.0, 4.0, 2.0), 6.0) - 3.0) - 1.0, 0.0, 1.0); return v * mix(vec3(1.0), k, s); }\\n" + GLY_GLSL : "") + dec(1)''')
rep('''.replace("#include <map_fragment>", "#include <map_fragment>\\n vec3 hGl = vec3(0.0); float hSm = 0.0, hIn = 0.0, hPh = 0.0;''',
    '''.replace("#include <map_fragment>", "#include <map_fragment>\\n vec3 hGl = vec3(0.0); float hSm = 0.0, hIn = 0.0, hPh = 0.0, fgM = 0.0; vec3 fgC = vec3(0.0);''')
rep('''diffuseColor.rgb *= 1.0 - hSm * .72; }" : ""))''',
    '''diffuseColor.rgb *= 1.0 - hSm * .72; }" : "") + (gly ? "\\n { vec3 gq = " + (sm ? "vHO * 2.2; vec3 gn = vHL;" : "vHW * .9; vec3 gn = vHN;") + " fgM = lvGly(gq, gn, uT, fgC); diffuseColor.rgb = mix(diffuseColor.rgb * .55, fgC * .5, fgM * .6); }" : ""))''')
rep('''          + (sm ? " totalEmissiveRadiance += uInl * hIn * (.55 + .45 * sin(uT * 1.6 + hPh * 6.283)) * 2.4;" : "") + " }"); };''',
    '''          + (sm ? " totalEmissiveRadiance += uInl * hIn * (.55 + .45 * sin(uT * 1.6 + hPh * 6.283)) * 2.4;" : "")
          + (gly ? " totalEmissiveRadiance += fgC * fgM * 1.5 + lvHsv(fract(hf * 1.5 + uT * .05), .55, 1.0) * pow(hf, 1.3) * .9; diffuseColor.a *= clamp(.24 + .76 * pow(hf, 1.3) + fgM * .75, 0.0, 1.0);" : "") + " }"); };''')
rep('''  n.customProgramCacheKey = () => "hullfin-" + f +''', '''  n.customProgramCacheKey = () => "hullfin2-" + f +''')
# the GLSL shared by both
rep('let GLY_T = null;', 'let GLY_T = null;\nconst GLY_GLSL = ' + repr(GLY_FN).replace("'", '"') + ';')
# swatch in the picker: rune colours
rep('glyph: { n: "Glyph Holo", t: 16, col: "#30e8ff", rim: "#7afcff", met: .3, rough: .15, k: 1.1, tm: .3, gl: 1.6, sw: "linear-gradient(135deg,#032a30,#3af0ff 45%,#0a7080 60%,#c8fcff)" } };',
    'glyph: { n: "Glyph Holo", t: 16, col: "#30e8ff", rim: "#7afcff", met: .3, rough: .15, k: 1.1, tm: .3, gl: 1.6, sw: "linear-gradient(135deg,rgba(3,42,48,.55),rgba(58,240,255,.75) 30%,rgba(200,110,255,.7) 50%,rgba(255,210,90,.7) 68%,rgba(120,255,170,.75) 85%,rgba(200,252,255,.6))" } };')
# hull editor: every ship type you own anywhere (colonies, fleets in flight), then the ones you've unlocked but not built yet
rep('function hullSection() { const own = Object.keys(SH).filter(k => (S.ships || {})[k] > 0), ks = own.length ? own : ["fighter", "corvette", "battleship"],',
    'function hullSection() { const ownN = k => { try { return own(k) || 0; } catch (e) { return (S.ships || {})[k] || 0; } }, mine = Object.keys(SH).filter(k => ownN(k) > 0 || hullOf(k)), soon = Object.keys(SH).filter(k => !mine.includes(k) && !missing(SH[k].req || {}).length), ks = mine.length || soon.length ? mine.concat(soon) : ["fighter", "corvette", "battleship"],')
rep('<div class="hfks">${ks.map(k => `<button class="${k === sel ? "on" : ""}" data-act="hullK" data-k="${k}">${esc(SH[k].n)}',
    '<div class="hfks">${ks.map(k => `<button class="${k === sel ? "on" : ""}${mine.includes(k) ? "" : " soon"}" data-act="hullK" data-k="${k}"${mine.includes(k) ? "" : ` title="Not built yet: the finish is ready when you build it"`}>${esc(SH[k].n)}${mine.includes(k) ? "" : " <small>not built</small>"}')
rep('.hfks{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}', '.hfks{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}.hfks .soon{opacity:.72;border-style:dashed}.hfks .soon small{font-size:10px;opacity:.8;margin-left:3px}')
rep('const GAME_V = 653', 'const GAME_V = 654')
open(p, 'w', encoding='utf-8').write(s)
