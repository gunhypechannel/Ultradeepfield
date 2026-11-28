"""v848: the stress tests run every Carcinid and Continuum wave and boss, and the Mimic hive waves (owner: "the mimic battles in the
45 battle stress test against bosses also include mimic waves i want to have different tests against crab waves and continuum waves also")."""
import sys
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 847;", "const GAME_V = 848;")
# the lab fights' monster sets, shared with the stress tests
rep('mon: B ? B.mon : /^crcp/.test(k) ? "crcpat" : k === "crck" ? "wkraken" : "carcinid",', 'mon: crcLabMon(k),')
rep('function crcLabFight(k) {', '''function crcLabMon(k) { const B = /^b/.test(k) ? CRC_BOSS[k.slice(1)] || CRC_BOSS.cc : null; return B ? B.mon : /^crcp/.test(k) ? "crcpat" : k === "crck" ? "wkraken" : "carcinid"; }
function crcLabFight(k) {''')
rep('const res = simulate(A, D), mon = /^kp(\\d|$)/.test(k) ? "cnpat" : /^kf/.test(k) ? "cnplat" : k === "kprime" ? "cnprimem" : k === "krel" ? "cnrelay" : k === "kark" ? "cnarkm" : k === "ketr" ? "cneterm" : "cncmd";',
    'const res = simulate(A, D), mon = cntLabMon(k);')
rep("const cntLabBig = k =>", '''const cntLabMon = k => /^kp(\\d|$)/.test(k) ? "cnpat" : /^kf/.test(k) ? "cnplat" : k === "kprime" ? "cnprimem" : k === "krel" ? "cnrelay" : k === "kark" ? "cnarkm" : k === "ketr" ? "cneterm" : "cncmd";
const cntLabMods = (k, D0) => cntMods(D0, cntLabBig(k) && k !== "krel" && k !== "kark" ? { cnt: "cmd" } : null);
const cntLabBig = k =>''')
rep('lvl = 20, Z = cntMods(D0, big && k !== "krel" && k !== "kark" ? { cnt: "cmd" } : null);', 'lvl = 20, Z = cntLabMods(k, D0);')
# the stress cases: every lab wave, each its own battle against the stress fleet
rep('''    C.push({ key: u, t: "mim", form, sh: 1, n0, d0: Object.assign({ [u]: n0 }, esc), mk: () => stacksOf(Object.assign({ [u]: n0 }, esc), { mon: 30 }, "monster") }); /* v671 */
  return C; }''', '''    C.push({ key: u, t: "mim", form, sh: 1, n0, d0: Object.assign({ [u]: n0 }, esc), mk: () => stacksOf(Object.assign({ [u]: n0 }, esc), { mon: 30 }, "monster") }); /* v671 */
  /* v848 every wave: the Mimic hives and swarm, the Carcinid Breach Zones, patrols, Kraken and bosses, the Continuum patrols, platforms and bosses */
  const wave = (ic, n, D0, mon, Z) => { const key = Object.keys(D0)[0], m = Z ? Z.m : null; C.push({ key, t: "mim", ic, n, form: "", sh: 1, n0: D0[key], d0: D0, mon, tac: Z ? Z.tac : undefined,
      mk: () => { const D = stacksOf(D0, { mon: 30 }, "monster"); if (m) for (const s of D) { s.atk *= m.bA; s.hull *= m.bH; } return D; },
      mkA: m ? () => { const A = stacksOf(STRESS_FLEET, techOf(null), G.me); for (const s of A) { s.atk *= m.pA; s.sh *= m.pS; } return A; } : null }); };
  for (const [k, n, f] of MIM_LAB) if (/^(hive|echo|swarm)/.test(k)) wave("⬢", "Mimic · " + n, f(), "mimic");
  for (const [k, n, f] of CRC_LAB) wave("❖", "Carcinid · " + n, f(), crcLabMon(k));
  for (const [k, n, f] of CNT_LAB) { const D0 = f(); wave("⬡", "Continuum · " + n, D0, cntLabMon(k), cntLabMods(k, D0)); }
  return C; }''')
rep('const D = c.t === "mim" ? { n: AL[c.key].n, k: c.key }', 'const D = c.t === "mim" ? { n: c.n || AL[c.key].n, k: c.key }')
rep('wbFightRise(() => stacksOf(STRESS_FLEET, techOf(null), G.me), () => c.mk', 'wbFightRise(() => c.mkA ? c.mkA() : stacksOf(STRESS_FLEET, techOf(null), G.me), () => c.mk')
rep('...(c.t === "mim" ? {} : c.t === "sb"', '...(c.t === "mim" ? (c.mon ? { mon: c.mon, pirate: true, cntTac: c.tac } : {}) : c.t === "sb"')
rep('const D = r.c.t === "mim" ? { ic: "⬢", n: (AL[r.c.key] || {}).n || r.c.key }', 'const D = r.c.t === "mim" ? { ic: r.c.ic || "⬢", n: r.c.n || (AL[r.c.key] || {}).n || r.c.key }')
rep("against every super boss in every form, and the Mimic Alphas, Nexus and Omega.", "against every super boss in every form, the Mimic Alphas, Nexus and Omega, and every Mimic, Carcinid and Continuum wave.")
open(p, "w", encoding="utf-8").write(s); print("ok")
