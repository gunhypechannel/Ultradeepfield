/* ---------- v674 map fleets: clean and proportional ----------
   Owner (iPhone screenshot): fleets on the map were 2 to 5 planets long, the Cube Destroyer sat like an orb at each fleet's nose, and
   five attacks on one Cube piled into one blob. Measured at iPhone size: planets 77-98 px across, fleets 120-490 px.
   - Ordinary fleets were drawn as joint-strike armadas: fleet3D's `big` argument doubles as the formation name, so every fleet of yours
     (formation "wedge", a string) got three hulls per class and twice the count. FLEET_ARM says when a fleet really is an armada.
   - Size by strength: a fleet's span is set against a planet's diameter (PL_D) in four steps by what it carries (fleetTier):
     scouts and raids 0.9, a battle fleet 1.15, a heavy fleet 1.45, a titan or Cube Destroyer armada 1.8 planet diameters.
     Joint strikes grow on top of that, up to 2.6. A fleet never shrinks below 30 px on screen, so it stays findable when zoomed out.
   - The Cube Destroyer flies at the rear of its formation (it led, an orb at the nose).
   - Fleets bound for the same world fan out into lanes as they close in (fleetLanes), instead of stacking. */
let FLEET_ARM = false;
const PL_D = 2 * (.38 + .42) * VIS_K; /* a typical world's diameter on the map */
function fleetTier(n) { n = n || {}; let c = 0, ti = 0; for (const k in n) { const v = +n[k] || 0; if (v <= 0) continue; c += v * unitCost(k); if (k === "worldbreaker") ti = 3; else if (MINI_CLS[k] === "x") ti = Math.max(ti, 2); }
  return Math.max(ti, c < 5e5 ? 0 : c < 2e7 ? 1 : c < 5e8 ? 2 : 3); }
const FLEET_SPAN = [.9, 1.15, 1.45, 1.8];
/* the fleet's size multiplier (userData.size) so its formation spans the tier's share of a planet; span is the formation's own width */
function fleetSzOf(n, grp, extra) { const sp = (grp && grp.userData.span) || 20, tgt = Math.min(2.6, FLEET_SPAN[fleetTier(n)] * (extra || 1)) * PL_D; return tgt / (FLEET_FS * sp); }
/* lanes: fleets flying out to the same world, ordered by id, so each knows its place across the approach */
function fleetLanes(list) { const by = new Map(); for (const [id, f] of list) { if (!f || f.phase !== "out" || !f.pid || id === "raid") continue; const a = by.get(f.pid) || []; a.push(id); by.set(f.pid, a); }
  const out = new Map(); for (const a of by.values()) if (a.length > 1) { a.sort(); a.forEach((id, i) => out.set(id, [i, a.length])); } return out; }
