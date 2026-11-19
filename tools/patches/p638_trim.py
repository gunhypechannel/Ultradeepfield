# v638: two-tone hulls (a trim finish), panel seams, glowing inlays, engine trails in the finish colour,
# and other players' finishes are read back from their player records (v635 published them but never read them).
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)
def block(start, end, new):
    global s
    i = s.index(start); j = s.index(end, i)
    s = s[:i] + new + s[j:]

# --- finish specs: "main" or "main.trim" ---
rep('const hullOf = k => { const f = ((S && S.hullF) || {})[k]; return f && hullOk(f) ? f : null; };',
    'const hullOf = k => { const f = ((S && S.hullF) || {})[k]; return f && hullOk(f) ? f : null; };\n'
    '/* v638 two-tone: a trim finish on fins, wings and dark plating. A finish travels as a spec, "obsidian" or "obsidian.gold" */\n'
    'const hullTrimOf = k => { const t = ((S && S.hullT) || {})[k], f = hullOf(k); return f && t && t !== f && hullOk(t) ? t : null; };\n'
    'const finSplit = sp => { const [a, b] = String(sp || "").split("."); return HULL_F[a] ? [a, HULL_F[b] && b !== a ? b : null] : [null, null]; };\n'
    'const finInl = (f, t) => new TH.Color(HULL_F[t || f].rim);\n'
    'const finEng = sp => { const [a, b] = finSplit(sp), c = finInl(a, b); return [new TH.Color(0xffffff).lerp(c, .4), c]; };\n'
    'const HULL_TU = { value: 0 }; (function hullTick(t) { HULL_TU.value = (t || 0) / 1000; requestAnimationFrame(hullTick); })(); /* the inlays\' slow pulse */\n'
    'function cleanHF(v) { if (!v || typeof v !== "object") return null; const o = {}; let n = 0; for (const k in v) { if (++n > 80) break; if (SH[k] && typeof v[k] === "string" && v[k].length < 30 && finSplit(v[k])[0]) o[k] = v[k]; } return Object.keys(o).length ? o : null; }')
block('function hullOfU(u, k) {', '\n/* the fleet\'s finish on the map',
    'function hullSpecU(u, k) { if (!u) return null; if (u === G.me) { const f = hullOf(k), t = hullTrimOf(k); return f ? f + (t ? "." + t : "") : null; }\n'
    '  const m = G.players && G.players[u] && G.players[u].hf, [a, b] = finSplit(m && m[k]); return a ? a + (b ? "." + b : "") : null; }\n'
    'function hullOfU(u, k) { return finSplit(hullSpecU(u, k))[0]; }\n'
    'const hullPubOf = () => { const o = {}; for (const k in (S && S.hullF) || {}) { const sp = hullSpecU(G.me, k); if (sp) o[k] = sp; } return Object.keys(o).length ? o : null; };')
rep('function hullFleet(u, n) { let best = null, bn = 0; for (const [k, v] of Object.entries(n || {})) { const f = hullOfU(u, k);',
    'function hullFleet(u, n) { let best = null, bn = 0; for (const [k, v] of Object.entries(n || {})) { const f = hullSpecU(u, k);')
rep('function hullAccK(k, a) { a = String(a); if (a.includes("^me")) { const f = hullOf(k); return a.replace("^me", f ? "~h" + f : ""); } const m = /\\^u([^\\^]+)\\^/.exec(a); if (m) { const f = hullOfU(m[1], k);',
    'function hullAccK(k, a) { a = String(a); if (a.includes("^me")) { const f = hullSpecU(G.me, k); return a.replace("^me", f ? "~h" + f : ""); } const m = /\\^u([^\\^]+)\\^/.exec(a); if (m) { const f = hullSpecU(m[1], k);')
# other players' finishes: read them back
rep('fac: FACTIONS[v.fac] ? v.fac : "terran",', 'fac: FACTIONS[v.fac] ? v.fac : "terran", hf: cleanHF(v.hf),')
# a texture arriving drops cached pictures / map kits that use it as main or trim
rep('if (key.includes("~h" + f)) {', 'if (finHas(key, f)) {')
rep('if (key.endsWith("~h" + f)) delete G3.fkm[key];', 'if (finHas(key, f)) delete G3.fkm[key];')
rep('const HULL_TEX = {}, HULL_TV = 1;', 'const HULL_TEX = {}, HULL_TV = 1;\nconst finHas = (key, f) => { const m = /~h([a-z.]+)/.exec(String(key)); return !!m && m[1].split(".").includes(f); };')

# --- the finish material ---
block('function finMat(m, f, obj) {', 'function hullFinish(obj, f) {', r'''function finMat(m, f, obj, o) { o = o || {}; const F = HULL_F[f]; if (!F || !TH || !m || !m.isMeshStandardMaterial) return m;
  const T2 = o.auto && HULL_F[o.auto] && o.auto !== f ? o.auto : null, F2 = T2 && HULL_F[T2], tex = hullTex(f), tex2 = T2 ? hullTex(T2) : null, sm = !obj && o.ps > 0, inl = o.inl || new TH.Color(F.rim);
  const n = m.clone(); n.metalness = tex ? (F.tm != null ? F.tm : .2) : F.met; n.roughness = tex ? .32 : F.rough; n.envMapIntensity = tex ? .8 : 1.7;
  if (sm) n.extensions = Object.assign({}, n.extensions, { derivatives: true });
  const br = (i, tx) => tx ? `{ vec3 t = texture2D(uHT${i}, vHW.zy * uTs${i}).rgb * bw.x + texture2D(uHT${i}, vHW.xz * uTs${i}).rgb * bw.y + texture2D(uHT${i}, vHW.xy * uTs${i}).rgb * bw.z; t = pow(t, vec3(2.2)); float tl = dot(t, vec3(.3, .59, .11)); t = max(mix(vec3(tl), t, 1.35), 0.0); c${i} = t * (0.35 + 0.75 * smoothstep(0.0, 0.85, hl)); g${i} = t * pow(tl, 3.0) * uGl${i}; }`
    : `{ c${i} = mix(diffuseColor.rgb, uFin${i} * clamp(pow(hl, 1.35) * uFk${i} + .04, 0.0, 1.5), .94); g${i} = vec3(0.0); }`;
  const dec = i => ` uniform vec3 uFin${i}; uniform float uFk${i}; uniform float uTs${i}; uniform float uGl${i};` + ((i === 1 ? tex : tex2) ? ` uniform sampler2D uHT${i};` : "");
  n.onBeforeCompile = sh => { const U = sh.uniforms; U.uFin1 = { value: new TH.Color(F.col) }; U.uFk1 = { value: F.k }; U.uTs1 = { value: F.ts || .8 }; U.uGl1 = { value: F.gl || .45 }; if (tex) U.uHT1 = { value: tex };
      if (T2) { U.uFin2 = { value: new TH.Color(F2.col) }; U.uFk2 = { value: F2.k }; U.uTs2 = { value: F2.ts || .8 }; U.uGl2 = { value: F2.gl || .45 }; if (tex2) U.uHT2 = { value: tex2 }; }
      U.uRim = { value: new TH.Color(F.rim) }; U.uInl = { value: inl }; U.uT = HULL_TU; U.uPs = { value: o.ps || 1 };
      sh.vertexShader = "varying vec3 vHW; varying vec3 vHN;" + (sm ? " varying vec3 vHO; varying vec3 vHL; uniform float uPs;" : "") + "\n" + sh.vertexShader.replace("#include <project_vertex>", "#include <project_vertex>\n" + (obj ? "vHW = transformed * 1.4; vHN = normalize(objectNormal);" : "vHW = (modelMatrix * vec4(transformed, 1.0)).xyz; vHN = normalize(mat3(modelMatrix) * objectNormal);") + (sm ? " vHO = transformed * uPs; vHL = normalize(objectNormal);" : ""));
      sh.fragmentShader = "uniform vec3 uRim; uniform vec3 uInl; uniform float uT;" + dec(1) + (T2 ? dec(2) : "") + " varying vec3 vHW; varying vec3 vHN;" + (sm ? " varying vec3 vHO; varying vec3 vHL;" : "") + "\n" + sh.fragmentShader
        .replace("#include <map_fragment>", "#include <map_fragment>\n vec3 hGl = vec3(0.0); float hSm = 0.0, hIn = 0.0, hPh = 0.0;\n { float hl = dot(diffuseColor.rgb, vec3(.3, .59, .11)); vec3 bw = pow(abs(normalize(vHN)), vec3(4.0)); bw /= (bw.x + bw.y + bw.z + 1e-4); vec3 c1, g1; " + br(1, tex)
          + (T2 ? " vec3 c2, g2; " + br(2, tex2) + " float mk = 1.0 - smoothstep(.12, .26, hl); c1 = mix(c1, c2, mk); g1 = mix(g1, g2, mk);" : "") + " diffuseColor.rgb = c1; hGl = g1; }"
          /* v638 armour plating: staggered panels with dark seams; a few panels are outlined in glowing inlay that pulses slowly */
          + (sm ? "\n { vec3 an = abs(vHL); vec2 q = an.x > an.y && an.x > an.z ? vHO.yz : (an.y > an.z ? vHO.xz : vHO.xy); q *= vec2(16.0, 11.0); q.x += mod(floor(q.y), 2.0) * .5; vec2 ce = floor(q); vec2 d2 = .5 - abs(fract(q) - .5); float d = min(d2.x, d2.y);"
            + " float w = fwidth(d) + 1e-4; hSm = (1.0 - smoothstep(w * .6, w * 1.8, d)) * (1.0 - smoothstep(.1, .28, w)); hPh = fract(sin(dot(ce, vec2(12.9898, 78.233))) * 43758.5453); hIn = (1.0 - smoothstep(w * .8, w * 3.2, d)) * (1.0 - smoothstep(.1, .28, w)) * step(.68, hPh); diffuseColor.rgb *= 1.0 - hSm * .72; }" : ""))
        .replace("#include <emissivemap_fragment>", "#include <emissivemap_fragment>\n { float hf = pow(1.0 - clamp(dot(normalize(normal), normalize(vViewPosition)), 0.0, 1.0), 2.2); totalEmissiveRadiance += uRim * hf * (" + (tex ? ".35" : ".85") + ") + hGl;"
          + (sm ? " totalEmissiveRadiance += uInl * hIn * (.55 + .45 * sin(uT * 1.6 + hPh * 6.283)) * 2.4;" : "") + " }"); };
  n.customProgramCacheKey = () => "hullfin-" + f + (tex ? "-t" : "") + (obj ? "-o" : "") + (T2 ? "-a" + T2 + (tex2 ? "t" : "") : "") + (sm ? "-s" : ""); n.needsUpdate = true; return n; }
''')
block('function hullFinish(obj, f) {', '\n/* sparkles on the brightest parts', r'''function hullFinish(obj, sp) { const [f, t] = finSplit(sp); if (!f || !TH) return; const inl = finInl(f, t), pc = new TH.Color(0xffffff).lerp(inl, .35), v = new TH.Vector3();
  obj.updateMatrixWorld(true); const sz = new TH.Box3().setFromObject(obj).getSize(new TH.Vector3()), L = Math.max(sz.x, sz.y, sz.z) || 1;
  obj.traverse(o => { if (!o.isMesh || !o.material) return; const ps = o.getWorldScale(v).x / L;
    const one = m => { if (!m) return m; const nm = m.userData && m.userData.sm;
      if (nm === "accent") { const n = m.clone(); n.color.copy(inl); if (n.emissive) n.emissive.copy(inl); return n; } /* glow strips take the inlay colour */
      if (nm === "plume") { const n = m.clone(); n.color.copy(inl); return n; } if (nm === "plumeCore") { const n = m.clone(); n.color.copy(pc); return n; }
      if (nm === "glass" || nm === "bell") return m;
      return finMat(m, t && (nm === "dark" || nm === "trim" || nm === "gold") ? t : f, false, { ps, inl, auto: !nm && t ? t : null }); }; /* untagged (imported) models: the darker plating takes the trim */
    o.material = Array.isArray(o.material) ? o.material.map(one) : one(o.material); }); }''')
# tag the hand-built ship materials by role
rep('Object.defineProperty(out, "fac", { value: fac, enumerable: false }); // read by the faction kit',
    'for (const nm of [...Object.keys(out), "plume", "plumeCore", "bell"]) if (out[nm]) out[nm].userData.sm = nm; /* v638 roles for two-tone hulls */\n  Object.defineProperty(out, "fac", { value: fac, enumerable: false }); // read by the faction kit')

# --- map fleets ---
rep('let fin = null; { const i = String(fac).indexOf("~h"); if (i >= 0) { fin = HULL_F[String(fac).slice(i + 2)] ? String(fac).slice(i + 2) : null; fac = String(fac).slice(0, i); } } /* v635 */',
    'let fin = null; { const i = String(fac).indexOf("~h"); if (i >= 0) { fin = finSplit(String(fac).slice(i + 2))[0] ? String(fac).slice(i + 2) : null; fac = String(fac).slice(0, i); } } /* v635, v638 specs */')
rep('if (fin) for (const nm of Object.keys(mats)) { const m = mats[nm]; if (/^f|win|eng|neon|glow|light|lamp/i.test(nm) || !m || !m.isMeshStandardMaterial || m.emissiveMap) continue; const n2 = finMat(m, fin, true);',
    'if (fin) for (const nm of Object.keys(mats)) { const m = mats[nm]; if (/^f|win|eng|neon|glow|light|lamp|glass/i.test(nm) || !m || !m.isMeshStandardMaterial || m.emissiveMap) continue; const [f0, t0] = finSplit(fin), inl = finInl(f0, t0); let n2;\n'
    '      if (nm === "accent") { n2 = m.clone(); n2.color.copy(inl); if (n2.emissive) n2.emissive.copy(inl); } else n2 = finMat(m, t0 && /^(dark|trim|gold)$/.test(nm) ? t0 : f0, true, { inl });')
# engine plumes on the map: the core keeps the friend/foe colour, the trail behind it takes the finish
rep('const ec = new TH.Color(col).lerp(new TH.Color(0xffffff), .35), pts = [];',
    'const ec = new TH.Color(col).lerp(new TH.Color(0xffffff), .35), pts = [], fe = FLEET_FIN && finSplit(FLEET_FIN)[0] ? finEng(FLEET_FIN)[1].clone().lerp(new TH.Color(0xffffff), .2) : null;')
rep('else for (let j = 0; j < 4; j++) pts.push([s, x, y, z - j * rr * 2.2, rr * (j ? 3.4 - j * .6 : 4.2), j ? .55 - j * .12 : 1]); }',
    'else for (let j = 0; j < 4; j++) pts.push([s, x, y, z - j * rr * 2.2, rr * (j ? 3.4 - j * .6 : 4.2), j ? .55 - j * .12 : 1, j && fe ? fe : undefined]); }')

# --- ship pictures ---
rep('let fin = null; { const mh = /~h([a-z]+)/.exec(String(accent)); if (mh) { fin = HULL_F[mh[1]] ? mh[1] : null;',
    'let fin = null; { const mh = /~h([a-z.]+)/.exec(String(accent)); if (mh) { fin = finSplit(mh[1])[0] ? mh[1] : null;')
rep('FG = k === "flagship" ? M.neon.color : null, gc = FG ?', 'FG = k === "flagship" ? M.neon.color : null, gc = !FG && fin && kind === "s" ? finEng(fin) : FG ?')

# --- picker ---
rep('<span>${fin ? HULL_F[fin].n : "Standard"}</span></div>${hullPick(sel)}',
    '<span>${fin ? HULL_F[fin].n + (hullTrimOf(sel) ? " · " + HULL_F[hullTrimOf(sel)].n + " trim" : "") : "Standard"}</span></div>${hullPick(sel)}')
rep('''    + `</div>${ok || Object.keys(HULL_F).some(hullOk) ? `<button class="gwlink" data-act="hullAll"''',
    '''    + `</div>${ok ? hullTrimRow(k, ok) : ""}${ok || Object.keys(HULL_F).some(hullOk) ? `<button class="gwlink" data-act="hullAll"''')
rep('function hullPick(k) {', r'''function hullTrimRow(k, ok) { const tr = hullTrimOf(k);
  return `<div class="hft"><b>Trim</b><small>${tr ? `${HULL_F[tr].n} on the fins, dark plating and glowing seams` : "A second finish for the fins, dark plating and glowing seams"}</small></div><div class="hfr">`
    + [["", { n: "None", t: 0, sw: "linear-gradient(135deg,#3a4652,#9aa8b6 50%,#55626e)" }], ...Object.entries(HULL_F).filter(([f]) => f !== ok).sort((x, y) => x[1].t - y[1].t)].map(([f, F]) => { const lk = f && !hullOk(f), on = f === (tr || "");
      return `<button class="hfb${on ? " on" : ""}${lk ? " lk" : ""}" data-act="hullTrim" data-k="${k}" data-t="${f}" aria-label="${F.n} trim${lk ? `, unlocks at Premium Tier ${F.t}` : ""}"><i style="background:${f ? `url(art/hull/${f}.webp?v=${HULL_TV}) center/200%` : F.sw}"></i><small>${lk ? `🔒 T${F.t}` : F.n}</small></button>`; }).join("") + `</div>`; }
function hullPick(k) {''')
rep('  hullK: d => { G.hullK = d.k; render(true); },',
    '  hullK: d => { G.hullK = d.k; render(true); },\n'
    '  hullTrim: d => { const k = d.k, t = d.t || "", f = hullOf(k); if (!f) return; if (t && !hullOk(t)) { toast(`${HULL_F[t].n} unlocks at Premium Tier ${HULL_F[t].t}.`, "warn"); return; }\n'
    '    S.hullT = Object.assign({}, S.hullT, { [k]: t }); if (!t) delete S.hullT[k]; else hullTex(t); dirty(); toast(t ? `${SH[k] ? SH[k].n : k}: ${HULL_F[f].n} with ${HULL_F[t].n} trim.` : `${SH[k] ? SH[k].n : k}: no trim.`, "win"); try { if (t) fgSnd("fg_reveal"); } catch (e) {} render(true); },')
rep('hullAll: d => { const f = hullOf(d.k) || ""; S.hullF = {}; if (f) for (const k of Object.keys(SH)) S.hullF[k] = f; dirty();',
    'hullAll: d => { const f = hullOf(d.k) || "", t = hullTrimOf(d.k) || ""; S.hullF = {}; S.hullT = {}; if (f) for (const k of Object.keys(SH)) { S.hullF[k] = f; if (t) S.hullT[k] = t; } dirty();')
rep('for (const f of new Set(Object.keys(SH).map(hullOf).filter(Boolean))) hullTex(f);',
    'for (const f of new Set([...Object.keys(SH).map(hullOf), ...Object.keys(SH).map(hullTrimOf)].filter(Boolean))) hullTex(f);')
rep('.hfp{flex-shrink:0;', '.hft{display:flex;flex-direction:column;gap:2px;margin-top:4px;padding-top:10px;border-top:1px solid rgba(255,210,90,.2)}.hft b{font-size:14px;font-weight:700;color:#ffd36b;letter-spacing:.04em}.hft small{font-size:12px;color:#9fb6c4}\n.hfp{flex-shrink:0;')
rep('const GAME_V = 637', 'const GAME_V = 638')
open(p, 'w', encoding='utf-8').write(s)
