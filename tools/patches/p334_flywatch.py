import sys, re
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
# v334 (owner's request) while a fleet flies, the guide takes you to it on the map ("Show on map"), not to the fleet list.
# On the map, following the fleet, it just says it's on its way.
helper = '''const flyWatch = wait => { const f = S.fleets.find(x => x.phase === "out") || S.fleets.find(x => x.phase === "gather") || S.fleets.find(x => x.phase === "back"); // v334
  if (f && G3 && view === "galaxy" && G3.cam && G3.cam.followFleet === f.id) return [['#fleethud', wait]];
  return f ? [[`[data-act="fleetMap"][data-id="${f.id}"]`, "Tap Show on map to watch it fly"], DOCKT("fleets", "Open Fleets to watch your fleet fly")] : [DOCKT("fleets", wait)]; };
'''
a = 'const tutWaitShips = () =>'
assert t.count(a) == 1; t = t.replace(a, helper + a)
n0 = t.count('[DOCKT("fleets", "Your fleet is on its way. Watch it here")]')
t = t.replace('[DOCKT("fleets", "Your fleet is on its way. Watch it here")]', 'flyWatch("Your fleet is on its way. Watch it fly")')
t = t.replace('[DOCKT("fleets", "Your fleet is on its way there. Wait for the report")]', 'flyWatch("Your fleet is on its way there. Wait for the report")')
t = t.replace('''[DOCKT("fleets", "Your fighters are flying home. They'll be ready in a moment")]''', '''flyWatch("Your fighters are flying home. They'll be ready in a moment")''')
a2 = '''[DOCKT("fleets", S.fleets.some(f => f.phase === "gather") && !S.fleets.some(f => f.phase === "back") ? "Your fighters are gathering at the field. They'll be home soon" : "Your fighters are flying home. They'll be ready in a moment")]'''
assert t.count(a2) == 1
t = t.replace(a2, '''flyWatch(S.fleets.some(f => f.phase === "gather") && !S.fleets.some(f => f.phase === "back") ? "Your fighters are gathering at the field. They'll be home soon" : "Your fighters are flying home. They'll be ready in a moment")''')
print('replaced on-its-way:', n0, 'remaining DOCKT fleets:', len(re.findall(r'DOCKT\("fleets"', t)))
open(p, 'w', encoding='utf-8', newline='').write(t)
