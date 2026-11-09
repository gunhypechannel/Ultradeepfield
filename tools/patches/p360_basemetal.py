# v360: base remaster, more metal. Building models get a softer version of the ships' hull shader (grey tones pulled into a steel range,
# paint kept, metalness .7-.9, roughness .25-.5). Every other built thing on the base (the hand-built buildings and centre, pads, decks, rails,
# lamps, crates, turrets, domes) is made metal with stronger reflections by colMetal, run whenever the base changes. The sand and rocks stay natural.
p = "docs/index.html"; h = open(p).read()
def rep(a, b):
    global h; assert h.count(a) == 1, (h.count(a), a[:70]); h = h.replace(a, b)
rep("m.emissiveMap = et; m.emissive.set(0xffffff); m.emissiveIntensity = 2.6 * (1 + 1.1 * DN_NIGHT);",
    '''m.onBeforeCompile = sh => { sh.fragmentShader = sh.fragmentShader // v360 polished metal, paint kept
      .replace("#include <map_fragment>", `#include <map_fragment>
        { vec3 c = pow(max(diffuseColor.rgb, vec3(0.0)), vec3(1.0 / 2.2)); float L = dot(c, vec3(.2126, .7152, .0722)), mx = max(max(c.r, c.g), c.b), mn = min(min(c.r, c.g), c.b);
          float sat = mx > 0.0 ? (mx - mn) / mx : 0.0, keep = min(1.0, sat * 2.2), L2 = .24 + .56 * pow(L, .9), f = L > .001 ? L2 / L : 1.0, t = 1.0 - keep * .7;
          c *= t * f + (1.0 - t); diffuseColor.rgb = pow(clamp(c, 0.0, 1.0), vec3(2.2)); }`)
      .replace("#include <roughnessmap_fragment>", "#include <roughnessmap_fragment>\\n roughnessFactor = .25 + .25 * roughnessFactor;")
      .replace("#include <metalnessmap_fragment>", "#include <metalnessmap_fragment>\\n metalnessFactor = .7 + .2 * metalnessFactor;"); };
    m.customProgramCacheKey = () => "bld360"; m.roughness = 1; m.metalness = 1;
    m.emissiveMap = et; m.emissive.set(0xffffff); m.emissiveIntensity = 2.6 * (1 + 1.1 * DN_NIGHT);''')
rep("m.emissiveIntensity = 2.6 * (1 + 1.1 * DN_NIGHT); if (!GLB_EMI.includes(m)) GLB_EMI.push(m); m.envMapIntensity = 1.25;",
    "m.emissiveIntensity = 2.6 * (1 + 1.1 * DN_NIGHT); if (!GLB_EMI.includes(m)) GLB_EMI.push(m); m.userData.env0 = 1.5; m.envMapIntensity = 1.5 * DN_ENV;")
rep("function colDayNight(W) {", r'''/* v360 everything built on the base reads as metal: plating, decks, rails, lamps, crates, turrets, domes. Each material once; sand, rocks,
   glass and glow materials are left alone. Runs when the base changes (the shadow map is re-rendered then) and every few seconds. */
const METAL_DONE = new WeakSet(), METAL_LIST = []; let DN_ENV = 1; // reflections of the (daytime) sky fade at night
function colMetal(W) {
  const skip = new Set([W.ground && W.ground.material, W.rockM]);
  W.scene.traverse(o => { if (!o.isMesh) return; for (const m of Array.isArray(o.material) ? o.material : [o.material]) {
    if (!m || METAL_DONE.has(m)) continue; METAL_DONE.add(m); if (skip.has(m) || !m.isMeshStandardMaterial || m.transparent || m.wireframe || (m.userData && m.userData.nometal) || m.customProgramCacheKey !== TH.Material.prototype.customProgramCacheKey) continue;
    m.metalness = Math.max(m.metalness, .8); m.roughness = Math.min(m.roughness, .32); m.envMapIntensity = Math.max(m.envMapIntensity || 1, 1.7); m.userData.env0 = m.envMapIntensity; m.envMapIntensity *= DN_ENV; METAL_LIST.push(m); m.needsUpdate = true; } });
}
function colDayNight(W) {''')
rep("  try { colDayNight(W); } catch (e) {} // v355", "  try { colDayNight(W); } catch (e) {} // v355\n  try { if (W.renderer.shadowMap.needsUpdate || (W.metF = (W.metF || 0) + 1) % 150 === 1) colMetal(W); } catch (e) {} // v360")
rep("  for (const m of GLB_EMI) m.emissiveIntensity = 2.6 * (1 + 1.1 * n);", "  for (const m of GLB_EMI) { m.emissiveIntensity = 2.6 * (1 + 1.1 * n); if (m.userData.env0 == null) m.userData.env0 = m.envMapIntensity; m.envMapIntensity = m.userData.env0 * (.22 + .78 * up); }\n  DN_ENV = .22 + .78 * up; for (let i = METAL_LIST.length - 1; i >= 0; i--) METAL_LIST[i].envMapIntensity = METAL_LIST[i].userData.env0 * DN_ENV; // v360 metal stops mirroring the day sky at night")
open(p, "w").write(h); print("ok")
