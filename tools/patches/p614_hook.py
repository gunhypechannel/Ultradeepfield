# v614 (owner: "Does the advisor cover anything about the flagship tab? Is there a way during the tutorial to mix up early missions more,
# players shouldn't feel like they are just upgrading metal over and over? How can we improve to make this hook players better?")
# (1) Four Academy steps that aren't upgrades, spread through the long economy stretch: open the Archives, scan a space monster, see
#     the week's events, join an alliance. Saves keep their place by step id, so nobody is moved. (2) The Advisor explains each
#     Flagship tab the first time you open it. (3) Void Essence no longer names the retired Leviathans as a source.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
A = '''  { lv: 3, id: "archive-first", t: "Open the Ancient Archives", say: "Every battle and every ruin teaches us something. The Archives keep it all, and I'll read any record to you. Open one and listen.", ok: s => Object.keys(s.archR || {}).length > 0, open: () => ACT.archOpen(), path: () => [['.sheet .arcard.lv2, .sheet .arcard.lv1', "Open a recovered record"], SHOWME], rw: { m: 800, c: 600, g: 300, shards: 2 } }, /* v614 */
'''
B = '''  { lv: 4, id: "scan-monster", t: "Scan a space monster", say: "Giants roam the lanes out there. Find one with the Finder and open its card, and I'll scan it for the Bestiary. Don't attack yet. Just look.", ok: s => ARCH_ORD.some(k => /^b_/.test(k) && k !== "b_hive" && k !== "b_coll" && (s.arch || {})[k]), find: "w", path: () => [SHOWME], rw: { m: 1500, c: 1000, g: 500, shards: 3 } }, /* v614 */
'''
C = '''  { lv: 5, id: "events-hub", t: "See what's coming this week", say: "The galaxy never sits still. World bosses, Cube battles and season finales all run on a schedule. Open the Events hub and see what's coming.", ok: s => !!s.tutEv || view === "rank", open: () => ACT.events({}), path: () => [SHOWME], rw: { m: 3000, c: 2000, g: 1000, shards: 3 } }, /* v614 */
'''
D = '''  { lv: 5, id: "join-alliance", t: "Join an alliance", say: "Nobody survives an Eclipse alone. Join an alliance, or found your own. Allies share boss hunts, joint strikes and supplies.", ok: s => !!myAlly() || G.mode !== "online", go: { v: "ally" }, path: () => [SHOWME], rw: { m: 5000, c: 3000, g: 1500, shards: 5 } }, /* v614 */
'''
rep('  { lv: 4, id: "read-your-reports-in-mail", t: "Watch your battle replay"', A + '  { lv: 4, id: "read-your-reports-in-mail", t: "Watch your battle replay"')
i = s.index('  { lv: 4, t: "Upgrade the Crystal Refinery to Lv.5"'); j = s.index('\n', i) + 1; s = s[:j] + B + s[j:]
rep('  { lv: 5, id: "econ-solar7"', C + '  { lv: 5, id: "econ-solar7"')
rep('  { lv: 5, id: "econ-store"', D + '  { lv: 5, id: "econ-store"')
rep('  events: d => { if (sheet) closeSheet();', '  events: d => { if (S) S.tutEv = 1; if (sheet) closeSheet();')
# the Flagship tabs, explained once each
rep('function openSheet(s) {', '''const FS_GUIDE = { over: "This is our flagship, Commander. It leads every fleet we send, earns experience in every battle, and grows stronger along with us.",
  skills: "Every level the flagship gains gives you a skill point. Spend them here. Each branch changes how the whole fleet fights.",
  gear: "Eight slots of gear. Weapons, shields and armour lift the fleet it leads, and the rest help at home: research, building and production.",
  forge: "The Forge turns rare materials into gear. Queue a piece and it finishes while you play. A bigger Dock forges more at once.",
  mats: "These are our rare materials. Pirates drop circuitry, monsters drop tissue, and fields, Cubes and pyramids give the rest. Short of one? This tells you where to hunt." };
function fsGuide(tab) { try { if (!S || !FS_GUIDE[tab] || (tab !== "over" && !(fsOf() || {}).built)) return; S.fsG = S.fsG || {}; if (S.fsG[tab]) return; S.fsG[tab] = 1; dirty(); advHolo(FS_GUIDE[tab], true); } catch (e) {} } /* v614 */
function openSheet(s) { if (s && s.type === "flagship") setTimeout(() => fsGuide(s.tab || "over"), 700);''')
rep('  fsTab: d => { sheet.tab = d.v; sheet.it = null; renderSheet(); },', '  fsTab: d => { sheet.tab = d.v; sheet.it = null; renderSheet(); fsGuide(d.v); },')
rep('void: ["Void Essence", "✧", "Cube cores, Leviathans and joint strikes"]', 'void: ["Void Essence", "✧", "Cube cores, Celestial Serpents and joint strikes"]')
rep('TUT.forEach(s => { if (!s.id)', 'ADV_MOOD_L[TUT.find(s => s.id === "events-hub").say] = "warm"; ADV_MOOD_L[TUT.find(s => s.id === "join-alliance").say] = "warm"; for (const k in FS_GUIDE) ADV_MOOD_L[FS_GUIDE[k]] = "calm"; /* v614 */\nTUT.forEach(s => { if (!s.id)')
s2 = re.sub(r"GAME_V = 613\b", "GAME_V = 614", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
