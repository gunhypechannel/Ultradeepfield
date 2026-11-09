# v359: ship hull remaster. Every Meshy ship model is reworked as it loads (glbHull), its shape untouched:
#  - Metal: the colour map's tones are pulled into a steel range (coloured paint keeps its colour), and a new metal/roughness map makes every
#    surface polished metal (metalness .8-.95, roughness .2-.5, with the model's own grain), with stronger studio reflections.
#  - Windows: rows of lit windows painted into a new glow map, running along the hull's length on its sides and decks. Each row stays on
#    one UV island (an island map is rasterised first), so nothing bleeds across texture seams. Every window has a white-hot core and a soft
#    halo in the ship's accent colour (SHOT_COL, the colour it fires in battle). Small craft get a few short rows, capital ships many.
#  - Painted lights: bright, saturated texels of the colour map glow too.
#  - The battle portrait gets the HDR bloom pass (as the hero cards do), so the windows shine.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)

rep("Promise.all(ps).then(() => GLB_BLDS.has(k) ? glbLights(k, s) : null)", "Promise.all(ps).then(() => GLB_BLDS.has(k) ? glbLights(k, s) : GLB_SHIPS.has(k) ? glbHull(k, s) : null)")
rep("function glbNext() {", r'''/* v359 ship hull remaster: polished metal, rows of lit windows with accent-coloured halos, glowing painted lights */
async function glbHull(k, s) {
  try {
    let mesh = null; s.traverse(o => { if (o.isMesh && !mesh && o.material && o.material.map) mesh = o; }); if (!mesh) return;
    const m = mesh.material, img = m.map.image; if (!img || !m.isMeshStandardMaterial) return;
    const toTex = async (c, srgb) => { let t; if (window.createImageBitmap) { const bm = await createImageBitmap(c); t = new TH.Texture(bm); c.width = c.height = 0; } else t = new TH.CanvasTexture(c);
      t.flipY = false; if (srgb) t.encoding = TH.sRGBEncoding; t.anisotropy = texAniso(); t.needsUpdate = true; return t; };
    const acc = new TH.Color(SHOT_COL[k] || "#9fdcff"), AR = acc.r, AG = acc.g, AB = acc.b;
    // 1) metal, in the shader (no texture readback): grey hull tones pulled into a steel range with coloured paint kept, and every surface
    //    polished metal (metalness .8-.95, roughness .2-.5) keeping the model's own grain
    m.onBeforeCompile = sh => { sh.fragmentShader = sh.fragmentShader
      .replace("#include <map_fragment>", `#include <map_fragment>
        { vec3 c = pow(max(diffuseColor.rgb, vec3(0.0)), vec3(1.0 / 2.2)); float L = dot(c, vec3(.2126, .7152, .0722)), mx = max(max(c.r, c.g), c.b), mn = min(min(c.r, c.g), c.b);
          float sat = mx > 0.0 ? (mx - mn) / mx : 0.0, keep = min(1.0, sat * 2.2), L2 = .2 + .52 * pow(L, .9), f = L > .001 ? L2 / L : 1.0, t = 1.0 - keep * .6;
          c *= t * f + (1.0 - t); c *= vec3(1.0 - .04 * (1.0 - keep), 1.0, 1.0 + .05 * (1.0 - keep)); diffuseColor.rgb = pow(clamp(c, 0.0, 1.0), vec3(2.2)); }`)
      .replace("#include <roughnessmap_fragment>", "#include <roughnessmap_fragment>\n roughnessFactor = .2 + .3 * roughnessFactor;")
      .replace("#include <metalnessmap_fragment>", "#include <metalnessmap_fragment>\n metalnessFactor = .8 + .15 * metalnessFactor;"); };
    m.customProgramCacheKey = () => "hull359"; m.roughness = 1; m.metalness = 1; m.envMapIntensity = 1.45;
    // painted lights: bright, saturated texels (read from a small copy) feed the glow map
    const A = 1024, E = new Float32Array(A * A * 3), SA = 512, cc = document.createElement("canvas"); cc.width = cc.height = SA; const cx = cc.getContext("2d", { willReadFrequently: true }); cx.drawImage(img, 0, 0, SA, SA);
    const D = cx.getImageData(0, 0, SA, SA).data; cc.width = cc.height = 0;
    for (let y = 0, i = 0; y < SA; y++) for (let x = 0; x < SA; x++, i += 4) { const r = D[i] / 255, g = D[i + 1] / 255, b = D[i + 2] / 255, mx = Math.max(r, g, b), mn = Math.min(r, g, b), sat = mx > 0 ? (mx - mn) / mx : 0;
      const w = clamp((mx - .5) / .3, 0, 1) * clamp((sat - .3) / .3, 0, 1); if (w > 0) for (let dy = 0; dy < 2; dy++) for (let dx = 0; dx < 2; dx++) { const o = ((y * 2 + dy) * A + x * 2 + dx) * 3; E[o] += r * w * .7; E[o + 1] += g * w * .7; E[o + 2] += b * w * .7; } }
    // 3) windows: UV islands first (triangles sharing vertices), rasterised, so a row of windows never crosses a texture seam
    const g = mesh.geometry, P = g.attributes.position, U = g.attributes.uv, I = g.index; if (P && U) {
      const nT = I ? I.count / 3 : P.count / 3, vi = j => I ? I.getX(j) : j, par = new Int32Array(P.count); for (let i = 0; i < P.count; i++) par[i] = i;
      const fd = a => { while (par[a] !== a) a = par[a] = par[par[a]]; return a; };
      for (let t = 0; t < nT; t++) { const a = fd(vi(t * 3)), b = fd(vi(t * 3 + 1)), c = fd(vi(t * 3 + 2)); par[b] = a; par[fd(c)] = a; }
      const isl = new Int32Array(A * A).fill(-1), bb = new TH.Box3().setFromBufferAttribute(P), len = Math.max(bb.max.x - bb.min.x, .001), hgt = bb.max.y - bb.min.y;
      const tri = []; let tot = 0;
      for (let t = 0; t < nT; t++) { const ia = vi(t * 3), ib = vi(t * 3 + 1), ic = vi(t * 3 + 2), id = fd(ia);
        const u0 = U.getX(ia) * A, v0 = U.getY(ia) * A, u1 = U.getX(ib) * A, v1 = U.getY(ib) * A, u2 = U.getX(ic) * A, v2 = U.getY(ic) * A;
        const x0 = Math.max(0, Math.floor(Math.min(u0, u1, u2))), x1 = Math.min(A - 1, Math.ceil(Math.max(u0, u1, u2))), y0 = Math.max(0, Math.floor(Math.min(v0, v1, v2))), y1 = Math.min(A - 1, Math.ceil(Math.max(v0, v1, v2)));
        const den = (v1 - v2) * (u0 - u2) + (u2 - u1) * (v0 - v2); if (Math.abs(den) < 1e-9) continue;
        for (let y = y0; y <= y1; y++) for (let x = x0; x <= x1; x++) { const px = x + .5, py = y + .5, l0 = ((v1 - v2) * (px - u2) + (u2 - u1) * (py - v2)) / den, l1 = ((v2 - v0) * (px - u2) + (u0 - u2) * (py - v2)) / den; if (l0 >= -.02 && l1 >= -.02 && l0 + l1 <= 1.02) isl[y * A + x] = id; }
        // where windows may go: sides and decks (not the underside or the engine block), weighted by area
        const ax = P.getX(ia), ay = P.getY(ia), az = P.getZ(ia), e1 = [P.getX(ib) - ax, P.getY(ib) - ay, P.getZ(ib) - az], e2 = [P.getX(ic) - ax, P.getY(ic) - ay, P.getZ(ic) - az];
        const n = [e1[1] * e2[2] - e1[2] * e2[1], e1[2] * e2[0] - e1[0] * e2[2], e1[0] * e2[1] - e1[1] * e2[0]], ar = Math.hypot(n[0], n[1], n[2]); if (ar < 1e-12) continue; n[0] /= ar; n[1] /= ar; n[2] /= ar;
        const cxw = ax + (e1[0] + e2[0]) / 3, cyw = ay + (e1[1] + e2[1]) / 3; if (n[1] < -.45 || Math.abs(n[0]) > .7 || (cxw - bb.min.x) / len < .1 || (cyw - bb.min.y) < hgt * .12) continue;
        tri.push([t, ar / 2, id, e1, e2, n, u0, v0, u1 - u0, v1 - v0, u2 - u0, v2 - v0]); tot += ar / 2; }
      // rows: count and length by hull size
      const big = bLen(k), rows = Math.round(clamp(30 + (big - .35) * 520, 24, 520) * (MOBILE ? .8 : 1)), pitch = len * clamp(.016 - big * .004, .008, .014), run = big < .55 ? 3 : big < .9 ? 6 : 10;
      const rr = rnd(hash(k + "win")), cr = .45 + .55 * .35, core = [1 * .65 + AR * .35, 1 * .65 + AG * .35, 1 * .65 + AB * .35];
      for (let r0 = 0; r0 < rows && tot > 0; r0++) { let pick = rr() * tot, T = null; for (const q of tri) { pick -= q[1]; if (pick <= 0) { T = q; break; } } if (!T) T = tri[tri.length - 1];
        const [, , id, e1, e2, n, u0, v0, du1, dv1, du2, dv2] = T;
        // in-plane axes: along the hull (world x projected), and across it
        let d = [1 - n[0] * n[0], -n[0] * n[1], -n[0] * n[2]], dl = Math.hypot(d[0], d[1], d[2]); if (dl < .3) continue; d = d.map(v => v / dl); const hv = [n[1] * d[2] - n[2] * d[1], n[2] * d[0] - n[0] * d[2], n[0] * d[1] - n[1] * d[0]];
        const g11 = e1[0] * e1[0] + e1[1] * e1[1] + e1[2] * e1[2], g12 = e1[0] * e2[0] + e1[1] * e2[1] + e1[2] * e2[2], g22 = e2[0] * e2[0] + e2[1] * e2[1] + e2[2] * e2[2], gd = g11 * g22 - g12 * g12; if (Math.abs(gd) < 1e-18) continue;
        const uvOf = w => { const p1 = w[0] * e1[0] + w[1] * e1[1] + w[2] * e1[2], p2 = w[0] * e2[0] + w[1] * e2[1] + w[2] * e2[2], a = (g22 * p1 - g12 * p2) / gd, b = (g11 * p2 - g12 * p1) / gd; return [a * du1 + b * du2, a * dv1 + b * dv2]; };
        const Ju = uvOf(d), Jv = uvOf(hv), jd = Ju[0] * Jv[1] - Ju[1] * Jv[0]; if (Math.abs(jd) < 1e-9) continue; // pixels per world unit along / across
        const ppu = Math.hypot(Ju[0], Ju[1]); if (ppu * pitch < 1.6 || ppu * pitch > A * .05) continue; // too small to show, or a stretched island
        let a0 = rr(), b0 = rr(); if (a0 + b0 > 1) { a0 = 1 - a0; b0 = 1 - b0; } const c0u = u0 + a0 * du1 + b0 * du2, c0v = v0 + a0 * dv1 + b0 * dv2;
        const ww = pitch * .58, wh = pitch * (rr() < .3 ? 1.15 : .7), hr = pitch * 1.3, nWin = 1 + Math.floor(rr() * run), st = Math.floor(-nWin / 2), lit = .75 + rr() * .5;
        for (let wi = st; wi < st + nWin; wi++) { if (rr() < .12) continue; // the odd dark window
          const cu = c0u + Ju[0] * pitch * wi, cv = c0v + Ju[1] * pitch * wi, ci = Math.floor(cv) * A + Math.floor(cu); if (cu < 0 || cv < 0 || cu >= A || cv >= A || isl[ci] !== id) continue; // off its island: skip that window, keep the row
          const R2 = Math.ceil(hr * Math.max(ppu, Math.hypot(Jv[0], Jv[1]))) + 1;
          for (let y = Math.max(0, Math.floor(cv - R2)); y <= Math.min(A - 1, Math.ceil(cv + R2)); y++) for (let x = Math.max(0, Math.floor(cu - R2)); x <= Math.min(A - 1, Math.ceil(cu + R2)); x++) {
            const pi = y * A + x; if (isl[pi] !== id) continue; const ox = x + .5 - cu, oy = y + .5 - cv, wu = (ox * Jv[1] - oy * Jv[0]) / jd, wv = (Ju[0] * oy - Ju[1] * ox) / jd; // back to world units
            const o = pi * 3; let cR = 0, cG = 0, cB = 0;
            if (Math.abs(wu) < ww / 2 && Math.abs(wv) < wh / 2) { const e = 1.6 * lit; cR = core[0] * e; cG = core[1] * e; cB = core[2] * e; }
            const dd = Math.hypot(wu / hr, wv / (hr * .8)); if (dd < 1) { const hh = Math.pow(1 - dd, 2) * .55 * lit; cR += AR * hh; cG += AG * hh; cB += AB * hh; }
            E[o] += cR; E[o + 1] += cG; E[o + 2] += cB; } } }
    }
    const ec = document.createElement("canvas"); ec.width = ec.height = A; const ex = ec.getContext("2d"), ed = ex.createImageData(A, A), Q = ed.data;
    for (let i = 0, j = 0; i < A * A; i++, j += 3) { Q[i * 4] = 255 * Math.min(1, E[j]); Q[i * 4 + 1] = 255 * Math.min(1, E[j + 1]); Q[i * 4 + 2] = 255 * Math.min(1, E[j + 2]); Q[i * 4 + 3] = 255; }
    ex.putImageData(ed, 0, 0); m.emissiveMap = await toTex(ec, true); m.emissive.set(0xffffff); m.emissiveIntensity = 2.4; m.needsUpdate = true; s.userData.hull = 1;
  } catch (e) { try { crumb("hull remaster failed " + k + ": " + e.message); } catch (e2) {} }
}
function glbNext() {''')
# the battle portrait: bloom so the windows shine (models only)
rep("if (hero || FG) hdrBloom(ox, W, H, S.renderer.toneMappingExposure, FG ? .42 : 1);",
    "if (hero || FG) hdrBloom(ox, W, H, S.renderer.toneMappingExposure, FG ? .42 : 1); else if (ship.userData.glb) { const hid = []; ship.traverse(o => { if (o.isSprite && o.visible) { o.visible = false; hid.push(o); } }); hdrBloom(ox, W, H, S.renderer.toneMappingExposure, .6); hid.forEach(o => o.visible = true); } // v359 the windows' glow (not the engines')")
# don't dispose the emissive glow either: dispose its GPU copy like the others
rep("for (const t of [o.material.map, o.material.normalMap, o.material.roughnessMap, o.material.metalnessMap]) if (t) t.dispose();",
    "for (const t of [o.material.map, o.material.normalMap, o.material.roughnessMap, o.material.metalnessMap, o.material.emissiveMap]) if (t) t.dispose();")
open(p, "w").write(h); print("ok")
# the two hand-built hulls: more metal, and the window bloom too
h = open(p).read()
def rep2(a, b):
    global h; assert h.count(a) == 1, a[:60]; h = h.replace(a, b)
rep2('m.color.set(0xc9b8a2); m.metalness = .9; m.roughness = .3; if ("clearcoat" in m) { m.clearcoat = .7; m.clearcoatRoughness = .14; }',
     'm.color.set(0xd2c2aa); m.metalness = .92; m.roughness = .24; m.envMapIntensity = 1.9; if ("clearcoat" in m) { m.clearcoat = .85; m.clearcoatRoughness = .1; } // v359 brighter polished metal')
rep2("emissiveIntensity: 2.2, metalness: .42, roughness: .64, bumpMap: TX.col, bumpScale: .03, envMapIntensity: .22, color: 0x9a9aa0 });",
     "emissiveIntensity: 2.2, metalness: .78, roughness: .4, bumpMap: TX.col, bumpScale: .03, envMapIntensity: .75, color: 0x9a9aa0 }); // v359 dark gunmetal, not stone")
rep2("else if (ship.userData.glb) { const hid = [];", "else if (kind === \"s\") { const hid = [];")
open(p, "w").write(h); print("ok2")
# buildings' light analysis (v353): read its texture from a CPU-side canvas (a GPU canvas readback took seconds on some devices)
h = open(p).read()
rep2('const A = 512, c = document.createElement("canvas"); c.width = c.height = A; const x = c.getContext("2d"); x.drawImage(img, 0, 0, A, A);',
     'const A = 512, c = document.createElement("canvas"); c.width = c.height = A; const x = c.getContext("2d", { willReadFrequently: true }); x.drawImage(img, 0, 0, A, A);')
open(p, "w").write(h); print("ok3")
