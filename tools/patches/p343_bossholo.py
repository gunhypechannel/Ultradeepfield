# v343: her transmission when a Void Shark, Nebula Squid, Star Leviathan, Cube, pyramid station or the Super Cube card opens
p="docs/index.html"; h=open(p).read()
a="function openSheet(s) {"
assert h.count(a)==1
h=h.replace(a,'''const BOSS_HOLO = {
  swhale: "Commander, that's a Void Shark: a cruiser-sized predator with laser turrets bolted to its hide. Bring heavy hulls, and it drops Exotic Tissue for the forge.",
  ssquid: "Commander, Nebula Squids are fast, many-armed and hunt in packs. Bring Cruisers and armour. They drop Exotic Tissue, and sometimes Void Essence.",
  slevi: "Commander, a Star Leviathan. Its jaws can split a battleship, so scout it first and send our heaviest fleet. It guards rare flagship materials.",
  cube: "Commander, a Cube. One fleet rarely breaks it, so call a joint strike with our allies. Cubes drop Cube Fragments and Void Essence, the rarest materials in the forge.",
  pyramid: "Commander, a derelict pyramid station. Send an expedition to open its vault for shards, resources and rare items. From level 3, something guards the halls.",
  nexus: "Commander, the Super Cube. From Friday to Sunday, alliances fight to seize and hold it. Every minute our alliance holds it earns glory and rewards for every member." };
function bossHolo(s) { if (!s || !S) return; let k = null;
  if (s.type === "pirate") { const x = PB[s.id]; k = x ? (x.mon && BOSS_HOLO[x.mon] ? x.mon : x.boss ? "cube" : null) : null; }
  else if (s.type === "pyramid") k = "pyramid"; else if (s.type === "nexus") k = "nexus";
  if (!k || advLines || $("#adv")) return; const L = BOSS_HOLO[k], on = $("#advh.on"); if (on && (acadOn() || (on.querySelector(".hsay span") || {}).textContent === L)) return;
  clearTimeout(G.holoT); G.holoT = setTimeout(() => { if (sheet && sheet.type === s.type && sheet.id === s.id) advHolo(L); }, 500); }
function openSheet(s) { try { if (!sheet || sheet.type !== (s && s.type) || sheet.id !== (s && s.id)) bossHolo(s); } catch (e) {}''')
open(p,"w").write(h); print("ok")
