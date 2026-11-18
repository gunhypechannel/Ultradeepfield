# v634: the owner's ArtCraft hull textures (art/hull/<finish>.webp, made more vivid: clarity, crisp facets, saturation, S-curve, lifted
# highlights) mapped onto every hull from all sides (triplanar, in world space, mirrored so it never shows a seam). The hull's own
# panel shading stays; bright facets glow (HDR-style) and the finished render gets bloom. The ship page tints its painting with the
# texture and the swatches show it. (owner: "remaster the texture to be as vivid and breathtaking as possible ... stunning HDR")
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
# textures: loaded on demand; when one lands, everything already baked in that finish is baked again
rep('const hullOk = f =>', '''const HULL_TEX = {}, HULL_TV = 1;
function hullTex(f) { const e = HULL_TEX[f]; if (e) return e.t || null; if (!TH) return null; HULL_TEX[f] = {};
  new TH.TextureLoader().load(`art/hull/${f}.webp?v=${HULL_TV}`, t => { t.wrapS = t.wrapT = TH.MirroredRepeatWrapping; t.anisotropy = 4; HULL_TEX[f].t = t;
    try { const S0 = studio(); if (S0 && S0.cache) for (const key of Object.keys(S0.cache)) if (key.includes("~h" + f)) { delete S0.cache[key]; ART_PEND.delete(key); for (const o of [S0.order, S0.orderSide]) if (o) { const i = o.indexOf(key); if (i >= 0) o.splice(i, 1); } } } catch (er) {}
    clearTimeout(hullTex.t); hullTex.t = setTimeout(() => { try { document.querySelectorAll("canvas[data-ship]").forEach(c => { c._dk = null; c._pend = null; }); if (!battle) render(true); } catch (er) {} }, 200); }, undefined, () => { HULL_TEX[f].fail = 1; });
  return null; }
const hullOk = f =>''')
rep('''function hullFinish(obj, f) { const F = HULL_F[f]; if (!F || !TH) return; const col = new TH.Color(F.col), rim = new TH.Color(F.rim);''',
    '''function hullFinish(obj, f) { const F = HULL_F[f]; if (!F || !TH) return; const col = new TH.Color(F.col), rim = new TH.Color(F.rim), tex = hullTex(f);''')
rep('''      n.onBeforeCompile = sh => { sh.uniforms.uFin = { value: col }; sh.uniforms.uRim = { value: rim }; sh.uniforms.uFk = { value: F.k };
        sh.fragmentShader = "uniform vec3 uFin; uniform vec3 uRim; uniform float uFk;\\n" + sh.fragmentShader
          .replace("#include <map_fragment>", "#include <map_fragment>\\n { float hl = dot(diffuseColor.rgb, vec3(.3, .59, .11)); diffuseColor.rgb = mix(diffuseColor.rgb, uFin * clamp(pow(hl, 1.35) * uFk + .04, 0.0, 1.5), .94); }")
          .replace("#include <emissivemap_fragment>", "#include <emissivemap_fragment>\\n { float hf = pow(1.0 - clamp(dot(normalize(normal), normalize(vViewPosition)), 0.0, 1.0), 2.2); totalEmissiveRadiance += uRim * hf * .85; }"); };
      n.customProgramCacheKey = () => "hullfin-" + f;''',
'''      n.onBeforeCompile = sh => { sh.uniforms.uFin = { value: col }; sh.uniforms.uRim = { value: rim }; sh.uniforms.uFk = { value: F.k }; sh.uniforms.uHT = { value: tex }; sh.uniforms.uTs = { value: F.ts || .8 }; sh.uniforms.uGl = { value: F.gl || .45 };
        sh.vertexShader = "varying vec3 vHW; varying vec3 vHN;\\n" + sh.vertexShader.replace("#include <project_vertex>", "#include <project_vertex>\\n vHW = (modelMatrix * vec4(transformed, 1.0)).xyz; vHN = normalize(mat3(modelMatrix) * objectNormal);");
        sh.fragmentShader = "uniform vec3 uFin; uniform vec3 uRim; uniform float uFk; uniform float uTs; uniform float uGl;" + (tex ? " uniform sampler2D uHT;" : "") + " varying vec3 vHW; varying vec3 vHN;\\n" + sh.fragmentShader
          .replace("#include <map_fragment>", "#include <map_fragment>\\n vec3 hGl = vec3(0.0); { float hl = dot(diffuseColor.rgb, vec3(.3, .59, .11));" + (tex
            ? " vec3 bw = pow(abs(normalize(vHN)), vec3(4.0)); bw /= (bw.x + bw.y + bw.z + 1e-4); vec3 tx = texture2D(uHT, vHW.zy * uTs).rgb * bw.x + texture2D(uHT, vHW.xz * uTs).rgb * bw.y + texture2D(uHT, vHW.xy * uTs).rgb * bw.z; tx = pow(tx, vec3(2.2));"
              + " float tl = dot(tx, vec3(.3, .59, .11)); tx = max(mix(vec3(tl), tx, 1.35), 0.0); diffuseColor.rgb = tx * (0.35 + 0.75 * smoothstep(0.0, 0.85, hl)); hGl = tx * pow(tl, 3.0) * uGl; }"
            : " diffuseColor.rgb = mix(diffuseColor.rgb, uFin * clamp(pow(hl, 1.35) * uFk + .04, 0.0, 1.5), .94); }"))
          .replace("#include <emissivemap_fragment>", "#include <emissivemap_fragment>\\n { float hf = pow(1.0 - clamp(dot(normalize(normal), normalize(vViewPosition)), 0.0, 1.0), 2.2); totalEmissiveRadiance += uRim * hf * (" + (tex ? ".35" : ".85") + ") + hGl; }"); };
      n.customProgramCacheKey = () => "hullfin-" + f + (tex ? "-t" : "");''')
# bloom on a finished render, so the bright facets bleed light
rep('const n = m.clone(); n.metalness = F.met; n.roughness = F.rough; n.envMapIntensity = 1.7;', 'const n = m.clone(); n.metalness = tex ? (f === "gold" ? .75 : f === "diamond" ? .5 : .2) : F.met; n.roughness = tex ? .32 : F.rough; n.envMapIntensity = tex ? .8 : 1.7;')
rep('if (hero || FG) hdrBloom(ox, W, H, S.renderer.toneMappingExposure, FG ? .42 : 1);', 'if (hero || FG || fin) hdrBloom(ox, W, H, S.renderer.toneMappingExposure, FG ? .42 : fin ? .4 : 1);')
# swatches and the ship page's painting wear the texture
rep('return `<button class="hfb${on ? " on" : ""}${lk ? " lk" : ""}" data-act="hullSet" data-k="${k}" data-f="${f}" aria-label="${F.n}${lk ? `, unlocks at Premium Tier ${F.t}` : ""}"><i style="background:${F.sw}"></i>',
    'return `<button class="hfb${on ? " on" : ""}${lk ? " lk" : ""}" data-act="hullSet" data-k="${k}" data-f="${f}" aria-label="${F.n}${lk ? `, unlocks at Premium Tier ${F.t}` : ""}"><i style="background:${f ? `url(art/hull/${f}.webp?v=${HULL_TV}) center/200%` : F.sw}"></i>')
rep('if (hf) shEl.style.setProperty("--fin", HULL_F[hf].col); } /* v633 */', 'if (hf) { shEl.style.setProperty("--fin", HULL_F[hf].col); shEl.style.setProperty("--fint", `url(art/hull/${hf}.webp?v=${HULL_TV})`); try { hullTex(hf); } catch (e) {} } } /* v633 */')
rep('.sheet.full.pic.uart[data-fin]:not([data-fin=""]){background-blend-mode:normal,color,normal,normal!important;background:linear-gradient(180deg,rgba(3,8,16,.96) 0%,rgba(3,8,16,.82) 14%,rgba(3,8,16,.06) 30%,rgba(3,8,16,.04) 66%,rgba(3,8,16,.85) 82%,rgba(3,8,16,.96) 100%),linear-gradient(var(--fin),var(--fin)),',
    '.sheet.full.pic.uart[data-fin]:not([data-fin=""]){background-blend-mode:normal,overlay,color,normal,normal!important;background:linear-gradient(180deg,rgba(3,8,16,.96) 0%,rgba(3,8,16,.82) 14%,rgba(3,8,16,.06) 30%,rgba(3,8,16,.04) 66%,rgba(3,8,16,.85) 82%,rgba(3,8,16,.96) 100%),var(--fint) center/260px repeat,linear-gradient(var(--fin),var(--fin)),')
# start loading the textures your fleet wears, as soon as the game runs
rep('const hullsAt = t =>', 'setTimeout(() => { try { for (const f of new Set(Object.keys(SH).map(hullOf).filter(Boolean))) hullTex(f); } catch (e) {} }, 4000);\nconst hullsAt = t =>')
# picking a finish loads its texture
rep('S.hullF = Object.assign({}, S.hullF, { [k]: f }); if (!f) delete S.hullF[k]; dirty();', 'S.hullF = Object.assign({}, S.hullF, { [k]: f }); if (!f) delete S.hullF[k]; else hullTex(f); dirty();')
s2 = re.sub(r"GAME_V = 633\b", "GAME_V = 634", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
