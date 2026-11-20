/* ---------- v673 the Mimics on the battle screen: sized like the monsters they are ----------
   Owner: the Mimics "look puny and insignificant"; fleets and units should fill as much of the screen as they can while staying true to
   how big each side is against the other. They had no entry in the size ladder, so every Mimic fell back to the default hull length:
   Omega was drawn at 1.89 (a Titan is 3.2, the Cube Destroyer 4.3) and the Alphas below a Dreadnought. Now:
   - MIM_HULL puts them on the ladder: the swarm at fighter-to-destroyer size, the Brood Titan and the Nexus structures at Titan size, the
     Alphas above the Titans and Omega the biggest thing that ever takes the field. Echoes copy the hull they mimic.
   - bCapW: the largest bosses (Alphas, Omega) may span up to 78% of the screen instead of 55%.
   - The Pylon and Node sprites are mostly empty space (a tall thin spire), so DRAWK draws them larger.
   - The swarm draws as a pack (up to five bodies), not one creature with a ×6 badge.
   - A big boss (length 3.6 or more: the Alphas, Omega, and the Cube Destroyer when it defends) rises into the frame during a longer
     opening, and the banner names it instead of "COMBAT START". */
const MIM_HULL = { mstalk: .8, mhunt: .92, mharv: .92, massim: 1.08, mguard: 1.35, mnest: 1.7, mtitan: 2.7, mnode: 2.5, mpylon: 2.6, mnexus: 3.2, malpha1: 3.9, malpha2: 3.9, malpha3: 3.9, malpha4: 3.9, momega: 5.4, momegax: 5.8 };
const MIM_PACK = { mstalk: 1, mhunt: 1, mharv: 1, massim: 1 };
Object.assign(DRAWK, { mpylon: 3.1, mnode: 2.8, mnexus: 2.4 });
const bCapW = k => (MIM_HULL[k] || 0) >= 3.6 ? .78 : BOSSK[k] || k === "worldbreaker" ? .55 : .3;
const bVc = (q, n, cap) => MIM_PACK[q.k] || /^e_/.test(q.k) ? Math.min(5, Math.max(1, n)) : Math.min(cap, Math.max(1, visN(q.role, n)));
/* no hull is ever drawn wider than 95% of the screen (a lone Cube Destroyer whose foes were all gone could reach 150%) */
const bFitL = (k, L, W) => Math.min(L, W * .95 / (DRAWK[k] || (AL[k] ? 2 : 1.8)));
/* the Mimic structures are stations (drawn by the station path at a fixed quarter of the screen); their sprites are tall and mostly empty, so they get their own, larger size */
const MIM_STA = { mnexus: .4, mnode: .36, mpylon: .58, mnest: .44 };
const bHero = k => (MIM_HULL[k] || 0) >= 3.6;
function bIntroMs(Q) { return (Q || []).some(q => q && bHero(q.k)) ? 2700 : 1200; }
function bHeroName(Q) { let best = null; for (const q of Q || []) if (q && bHero(q.k) && (!best || MIM_HULL[q.k] > MIM_HULL[best.k])) best = q; return best ? ((AL[best.k] || {}).n || "").toUpperCase() : null; }
/* the rise: a hero boss grows from 55% to full size over the first 1.5 s of its opening, then holds */
function bRise(b, q) { if (!b || !(b.intro > 0) || !bHero(q.k) || !b.intro0) return 1; const u = clamp((b.intro0 - b.intro) / 1500, 0, 1); return .55 + .45 * (1 - Math.pow(1 - u, 3)); }
