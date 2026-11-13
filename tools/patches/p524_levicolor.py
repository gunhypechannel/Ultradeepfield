# v524 the Star Leviathan keeps its own colours (owner: "the art and shape need to match the art, not the colour"): the eel-and-
# armoured-head shape stays, painted again in obsidian scales with molten orange seams that breathe, orange eyes, throat and fins.
# Battle ranks: defences (turrets, stations) form their own rank at the very back, closest to the commander who owns them.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
i = s.index('  } else if (k === "slevi") {'); j = s.index('  } else if (k === "ssquid") {')
seg = s[i:j].replace('C.lwhale', 'C.levi').replace('C.leel', 'C.leviB').replace('C.larmor', 'C.larmorO').replace('C.lcyan', 'C.glowL').replace('C.lfin', 'C.lfinO')
seg = seg.replace('cyan throat grooves', 'molten throat').replace('cracked\n       with cyan light', 'seamed\n       with molten light')
s = s[:i] + seg + s[j:]
rep('''  return C;
}
const MONM = {};''', '''  C.leviB = C.levi.clone(); for (const m of ["map", "emissiveMap"]) { const t = C.levi[m].clone(); t.wrapS = t.wrapT = TH.RepeatWrapping; t.repeat.set(7, 2); t.needsUpdate = true; C.leviB[m] = t; } /* the long body: smaller scales */
  C.larmorO = new TH.MeshPhysicalMaterial({ color: 0x1a120e, roughness: .4, metalness: .6, clearcoat: .5, emissive: 0x200800, emissiveIntensity: 1 });
  C.lfinO = new TH.MeshPhysicalMaterial({ color: 0x2a1206, roughness: .3, metalness: .1, clearcoat: .6, emissive: 0xff5a14, emissiveIntensity: .8, transparent: true, opacity: .75, side: TH.DoubleSide }); /* v524 */
  C.levi.userData.pulse = C.leviB.userData.pulse = ".75 + .45 * (.5 + .5 * sin(uMT * 1.1))";
  return C;
}
const MONM = {};''')
rep('ic: "🐉", col: "#5ac8ff", rgb: "90,200,255", per: 10, d: "A sea serpent as long as a fleet, with the armoured head of a whale. Starlight runs in the cracks of its hide, and its jaws can split a battleship."',
    'ic: "🐉", col: "#ff8a4a", rgb: "255,138,74", per: 10, d: "A sea serpent as long as a fleet, with the armoured head of a whale. Molten light runs along its scales, and its jaws can split a battleship."')
rep('slevi: "90,200,255"', 'slevi: "255,138,74"')
rep('slevi: [90, 200, 255]', 'slevi: [255, 138, 74]')
# defences stand closest to their owner: turrets and stations get their own rank behind the titans
rep('capital: 2, titan: 3, station: 3, turret: 3 };', 'capital: 2, titan: 3, station: 4, turret: 4 };')
rep('for (let r = 0; r < 4; r++) { const R = L.filter(p => (RK[Q[p.i].role] != null ? RK[Q[p.i].role] : 1) === r)', 'for (let r = 0; r < 5; r++) { const R = L.filter(p => (RK[Q[p.i].role] != null ? RK[Q[p.i].role] : 1) === r)')
s2 = re.sub(r"GAME_V = 523\b", "GAME_V = 524", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
