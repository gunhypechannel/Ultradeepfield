import re,sys
p="docs/index.html"; h=open(p).read()
def rep(a,b,n=1):
    global h
    c=h.count(a); assert c==n,(c,a[:80]); h=h.replace(a,b)
# Discovery Class: no cap
rep('dt: "hyper", sz: 1.5, max: 1, ally: 2,','dt: "hyper", sz: 1.5, ally: 2,')
rep('An alliance flagship for system dominance. One per commander, and only for members of an alliance with a Space Station Lv.2 or higher.','An alliance flagship for system dominance, only for members of an alliance with a Space Station Lv.2 or higher. Build as many as you can afford.')
rep('eclipse: "The Discovery Class Destroyer is an alliance flagship. One per commander, and its command aura lifts the whole fleet." };',
'''eclipse: "The Discovery Class Destroyer is an alliance flagship. Build as many as you can afford: its command aura lifts the whole fleet.",
  /* v339 research transmissions */
  energyT: "Energy Technology boosts every solar and fusion plant, and most other research needs it first.",
  laserT: "Laser Technology arms our light weapons. Heavy Lasers and the bigger warships need it.",
  ionT: "Ion Technology leads to Cruisers, Ion Cannons and Plasma Technology.",
  hyperT: "Hyperspace Technology adds cargo space, and unlocks the Hyperspace Drive and our heaviest warships.",
  plasmaT: "Plasma Technology raises mine output a little every level, and unlocks Bombers and Plasma Turrets.",
  drive: "The Combustion Drive speeds up Light Fighters, cargo ships and Recyclers.",
  impulse: "The Impulse Drive speeds up Heavy Fighters, Cruisers, Bombers and Colony Ships. Colony Ships need level 3 of it first.",
  hyper: "The Hyperspace Drive speeds up Battleships and every capital ship. The road to the Reaper runs through it.",
  espionage: "Espionage Technology decides how much our probes see, and how well we hide from theirs.",
  computer: "Computer Technology gives us one more fleet slot per level, so more fleets can fly at once.",
  astro: "Astrophysics lets us hold more planets: one more world for every two levels.",
  irn: "The Intergalactic Research Network links our labs, so every level makes research faster.",
  graviton: "Graviton Technology is a capstone research for end-game fleets.",
  weapons: "Weapons Technology adds ten percent damage to every ship and defense, per level.",
  shields: "Shielding Technology adds ten percent shield strength to every ship and defense, per level.",
  armor: "Armour Technology adds ten percent hull strength to every ship and defense, per level.",
  logistics: "Cargo Logistics adds cargo space, so every raid and trade run carries home more.",
  command: "Fleet Command lets our joint strikes hold more ships, and brings more allies to answer our calls.",
  terraform: "Terraforming adds building fields on every planet we hold.",
  repairT: "Fleet Repair Technology makes repairs faster and cheaper." };''')
# every tap plays her transmission (was: first time only)
rep('''function holoFirst(kind, k) { if (!S || !HOLO[k] || (kind !== "b" && kind !== "s")) return; S.holoSeen = S.holoSeen || {}; if (S.holoSeen[k]) return;''',
'''function holoFirst(kind, k) { if (!S || !HOLO[k] || (kind !== "b" && kind !== "s" && kind !== "r")) return; /* v339: every tap on a building, ship or research plays her transmission */''')
rep('''  if ($("#advh.on") || advLines || $("#adv")) return; S.holoSeen[k] = 1; dirty(); setTimeout(() => advHolo(HOLO[k]), 400); }''',
'''  if (advLines || $("#adv")) return; const on = $("#advh.on"); if (on && (acadOn() || (on.querySelector(".hsay span") || {}).textContent === HOLO[k])) return; /* never cut off an Academy briefing, nor restart the same line */
  clearTimeout(G.holoT); G.holoT = setTimeout(() => { if (sheet && (sheet.type === "detail" || sheet.type === "bld") && sheet.k === k) advHolo(HOLO[k]); }, 400); }''')
rep('''  if (best && B[best.k]) { const bt = baseTarget(); openSheet({''','''  if (best && B[best.k]) { const bt = baseTarget(); holoFirst("b", best.k); openSheet({''')
rep('bldInfo: d => { SFX.tapB(d.k); const bt = baseTarget(); openSheet({','bldInfo: d => { SFX.tapB(d.k); holoFirst("b", d.k); const bt = baseTarget(); openSheet({')
open(p,"w").write(h); print("ok")
