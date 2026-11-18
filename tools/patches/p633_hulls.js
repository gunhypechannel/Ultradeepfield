/* ---------- v633 premium hull finishes (owner: "I want premium players able to get ships in different hull materials like gold, emerald,
   ruby, diamond, amethyst" ... "Do it all"). A finish is set per ship type (or for the whole fleet) on the ship's page. It is looks only:
   no stats. Gold opens at Premium Tier 5, Amethyst 8, Diamond 11, Ruby 12, Emerald 14. The renderer recolours the hull (its texture
   detail kept), makes it metal or polished gem, edges it with a glow of its colour and scatters sparkles on its brightest parts; your
   battles, Shipyard renders and the ship's page all show it. Your own side is marked "^me" in its accent so only your ships wear it. ---------- */
const HULL_F = { gold: { n: "Gold", t: 5, col: "#ffb81c", rim: "#ffc040", met: 1, rough: .2, k: 1.3, sw: "linear-gradient(135deg,#7a5410,#ffe08a 45%,#c8901e 60%,#fff3c0)" },
  amethyst: { n: "Amethyst", t: 8, col: "#9a4dff", rim: "#dba6ff", met: .5, rough: .1, k: .85, sw: "linear-gradient(135deg,#3a1470,#c58cff 45%,#7a3ad0 60%,#efd8ff)" },
  diamond: { n: "Diamond", t: 11, col: "#eef7ff", rim: "#bfe8ff", met: .9, rough: .05, k: 1.25, sw: "linear-gradient(135deg,#9fb8d0,#ffffff 40%,#c8f0ff 55%,#ffd8f4 70%,#ffffff)" },
  ruby: { n: "Ruby", t: 12, col: "#ff1438", rim: "#ff7a94", met: .5, rough: .08, k: .85, sw: "linear-gradient(135deg,#5a0614,#ff4a66 45%,#a8102c 60%,#ffc0cc)" },
  emerald: { n: "Emerald", t: 14, col: "#10d868", rim: "#86ffc0", met: .5, rough: .08, k: .85, sw: "linear-gradient(135deg,#053a1e,#3cff9a 45%,#0e8a48 60%,#c8ffe0)" } };
const hullOk = f => !!HULL_F[f] && (premT() >= HULL_F[f].t || !!G.owner);
const hullOf = k => { const f = ((S && S.hullF) || {})[k]; return f && hullOk(f) ? f : null; };
/* "^me" in an accent marks your own ships: it becomes "~h<finish>" for a ship type that wears one, or nothing */
function hullAccK(k, a) { a = String(a); if (!a.includes("^me")) return a; const f = hullOf(k); return a.replace("^me", f ? "~h" + f : ""); }
function hullFinish(obj, f) { const F = HULL_F[f]; if (!F || !TH) return; const col = new TH.Color(F.col), rim = new TH.Color(F.rim);
  obj.traverse(o => { if (!o.isMesh || !o.material) return; const one = !Array.isArray(o.material), mats = one ? [o.material] : o.material;
    const out = mats.map(m => { if (!m || !m.isMeshStandardMaterial) return m; const n = m.clone(); n.metalness = F.met; n.roughness = F.rough; n.envMapIntensity = 1.7;
      n.onBeforeCompile = sh => { sh.uniforms.uFin = { value: col }; sh.uniforms.uRim = { value: rim }; sh.uniforms.uFk = { value: F.k };
        sh.fragmentShader = "uniform vec3 uFin; uniform vec3 uRim; uniform float uFk;\n" + sh.fragmentShader
          .replace("#include <map_fragment>", "#include <map_fragment>\n { float hl = dot(diffuseColor.rgb, vec3(.3, .59, .11)); diffuseColor.rgb = mix(diffuseColor.rgb, uFin * clamp(pow(hl, 1.35) * uFk + .04, 0.0, 1.5), .94); }")
          .replace("#include <emissivemap_fragment>", "#include <emissivemap_fragment>\n { float hf = pow(1.0 - clamp(dot(normalize(normal), normalize(vViewPosition)), 0.0, 1.0), 2.2); totalEmissiveRadiance += uRim * hf * .85; }"); };
      n.customProgramCacheKey = () => "hullfin-" + f; n.needsUpdate = true; return n; });
    o.material = one ? out[0] : out; }); }
/* sparkles on the brightest parts of a finished render */
function finSpark(cv, f, k) { try { const F = HULL_F[f]; if (!F) return; const x = cv.getContext("2d"), w = cv.width, h = cv.height, D = x.getImageData(0, 0, w, h).data, r = rnd(hash(k + f)), pts = [];
  for (let i = 0; i < 2600 && pts.length < 9; i++) { const px = (r() * w) | 0, py = (r() * h) | 0, j = (py * w + px) * 4; if (D[j + 3] > 200 && D[j] + D[j + 1] + D[j + 2] > 560) pts.push([px, py]); }
  x.save(); x.globalCompositeOperation = "lighter"; const R0 = Math.max(4, w / 70);
  for (const [px, py] of pts) { const s = R0 * (.6 + r() * .9), g = x.createRadialGradient(px, py, 0, px, py, s); g.addColorStop(0, "rgba(255,255,255,.95)"); g.addColorStop(.3, F.rim + "aa"); g.addColorStop(1, "rgba(0,0,0,0)"); x.fillStyle = g; x.beginPath(); x.arc(px, py, s, 0, TAU); x.fill();
    x.strokeStyle = "rgba(255,255,255,.75)"; x.lineWidth = Math.max(1, s / 7); x.beginPath(); x.moveTo(px - s * 1.8, py); x.lineTo(px + s * 1.8, py); x.moveTo(px, py - s * 1.8); x.lineTo(px, py + s * 1.8); x.stroke(); }
  x.restore(); } catch (e) {} }
function hullPick(k) { const cur = (S.hullF || {})[k] || "", ok = hullOf(k);
  return `<div class="hfp"><div class="hfh"><b>Hull finish</b><small>${ok ? `${HULL_F[ok].n} · looks only` : "Premium players can plate their ships in gold and gems"}</small></div><div class="hfr">`
    + [["", { n: "Standard", t: 0, sw: "linear-gradient(135deg,#3a4652,#9aa8b6 50%,#55626e)" }], ...Object.entries(HULL_F)].map(([f, F]) => { const lk = f && !hullOk(f), on = f === (ok || "") && !(f && cur !== f);
      return `<button class="hfb${on ? " on" : ""}${lk ? " lk" : ""}" data-act="hullSet" data-k="${k}" data-f="${f}" aria-label="${F.n}${lk ? `, unlocks at Premium Tier ${F.t}` : ""}"><i style="background:${F.sw}"></i><small>${lk ? `🔒 T${F.t}` : F.n}</small></button>`; }).join("")
    + `</div>${ok || Object.keys(HULL_F).some(hullOk) ? `<button class="gwlink" data-act="hullAll" data-k="${k}">Use ${ok ? HULL_F[ok].n.toLowerCase() : "standard"} on every ship type</button>` : `<button class="gwlink" data-act="premOpen">See the premium tiers ›</button>`}</div>`; }
const hullsAt = t => Object.entries(HULL_F).filter(([, F]) => F.t <= t).map(([, F]) => F.n);
