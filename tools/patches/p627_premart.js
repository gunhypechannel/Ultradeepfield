/* ---------- v627 the owner's own paintings for the premium skins (skins/pr1..pr16.webp, each with its sphere map), and six more tiers
   above $1,000 (owner: "Here are all plus more for the spender beyond 1000$ the ones featuring gold should have special glows and other
   unique special effects"). Gold worlds (Golden Dynasty, Solar Sovereign and the six jewel worlds) shimmer: a pulsing gold halo, a glint
   that sweeps across the planet and sparkles that wink on their gold and gems, on the 3D map and in every preview. ---------- */
PREM.push(
  { usd: 1500, k: "pr11", n: "Prism Diamond", col: "#dff0ff", b: { prod: .22, build: .20, res: .20, march: 1, forge: .12, fq: 1, chest: 15, spd: .03, atk: .05, def: .05, gold: 1 } },
  { usd: 2000, k: "pr12", n: "Ruby Throne", col: "#ff3a5c", b: { prod: .24, build: .22, res: .22, march: 1, forge: .14, fq: 1, chest: 15, spd: .03, atk: .05, def: .05, gold: 1 } },
  { usd: 3000, k: "pr13", n: "Gilded Citadel", col: "#ffcf4a", b: { prod: .26, build: .24, res: .24, march: 2, forge: .16, fq: 1, chest: 20, spd: .04, atk: .05, def: .05, gold: 1 } },
  { usd: 4000, k: "pr14", n: "Emerald Vault", col: "#3dff8a", b: { prod: .28, build: .26, res: .26, march: 2, forge: .18, fq: 2, chest: 20, spd: .04, atk: .05, def: .05, gold: 1 } },
  { usd: 5000, k: "pr15", n: "Golden Eden", col: "#c8ff4a", b: { prod: .30, build: .28, res: .28, march: 2, forge: .20, fq: 2, chest: 25, spd: .05, atk: .05, def: .05, gold: 1 } },
  { usd: 7500, k: "pr16", n: "Sovereign Hoard", col: "#e6e9f2", b: { prod: .32, build: .30, res: .30, march: 2, forge: .22, fq: 2, chest: 30, spd: .05, atk: .05, def: .05, gold: 1 } });
const PREM_TOP = PREM.length - 1, PREM_GOLD = new Set([5, 9, 11, 12, 13, 14, 15, 16]);
const PREM_D = { pr1: "Green and violet aurora curtains rippling over a deep blue ocean world.", pr2: "Black basalt plates floating on rivers of molten lava.", pr3: "Half glacier, half inferno, split by a blazing seam of fire.",
  pr4: "Glowing turquoise currents swirling between tiny jungle islands.", pr5: "Golden cathedral cities across a stormy blue sea, crowned by a jewelled golden ring.", pr6: "A living nebula: pink, violet and blue gas spiralling round a newborn star.",
  pr7: "A storm giant of electric-blue cloud, veined with lightning.", pr8: "Obsidian rock torn by violet fire, dark flames licking off its edge.", pr9: "A white-gold sun-world, solar flares looping off its surface inside a golden halo.",
  pr10: "A black hole at its heart, its blazing accretion ring bending the storms around it.", pr11: "A world of flawless diamond, veined with gold and set with ruby and emerald.", pr12: "Ruby crystal seas and silver ridges, threaded with veins of gold.",
  pr13: "A citadel world of gold and silver spires, ruby rivers and emerald groves.", pr14: "Emerald valleys under silver peaks, rivers of gold and ruby seams.", pr15: "Seas of molten gold around emerald highlands and crystal waterfalls.",
  pr16: "A hoard of silver, ruby, emerald and gold, every seam glowing." };
for (let t = 1; t <= PREM_TOP; t++) { const P = PREM[t]; PXS[P.k] = { n: P.n, cost: 0, prem: t, img: 1, r: "all", b: +(.12 + .012 * t).toFixed(3), glow: P.col, ec: hex3(P.col), d: PREM_D[P.k], gold: PREM_GOLD.has(t) }; }
/* the gold shimmer drawn over a skin preview (the world fills .68 of the frame) */
const PXG_FX = `<i class="pxglint"></i><i class="pxspk">${"<s></s>".repeat(8)}</i>`;
const pxGoldWrap = (k, inner) => PXS[k] && PXS[k].gold ? `<span class="pxgw">${inner}${PXG_FX}</span>` : inner;
/* and on the 3D map: a gold rim that breathes, a glint sweeping across, and sparkles winking on the bright gold and gems */
const PXG_U = { uT: { value: 0 } };
function pxGoldMat(mat) { mat.onBeforeCompile = sh => { sh.uniforms.uPxT = PXG_U.uT;
  sh.fragmentShader = "uniform float uPxT;\n" + sh.fragmentShader.replace("#include <emissivemap_fragment>", `#include <emissivemap_fragment>
  { vec3 pn = normalize(normal); float pf = pow(1.0 - clamp(dot(pn, normalize(vViewPosition)), 0.0, 1.0), 2.4); float pl = dot(diffuseColor.rgb, vec3(.333));
    float ph = mod(uPxT * .32, 3.2) - 1.6, pg = smoothstep(.2, 0.0, abs((pn.x + pn.y) * .7071 - ph));
    vec2 pc = floor(vUv * vec2(260.0, 130.0)); float pr = fract(sin(dot(pc, vec2(12.9898, 78.233))) * 43758.5453);
    float ps = step(.975, pr) * smoothstep(.45, .75, pl) * pow(max(0.0, sin(uPxT * 2.3 + pr * 80.0)), 14.0);
    totalEmissiveRadiance = totalEmissiveRadiance * .62 + vec3(1.0, .74, .28) * (pf * (.55 + .25 * sin(uPxT * 1.7)) + pg * (.1 + pl * .45)) + vec3(1.0, .96, .85) * ps * 2.6; }`); };
  mat.needsUpdate = true; return mat; }
