"""v830: the Events pages, simplified and alive, with How to Play for every event (p830_events.js), and the last three titans' shipyard
transmissions (owner approved the drafts)."""
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else "docs/index.html"
s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:140]); s = s.replace(a, b)
rep("const GAME_V = 829;", "const GAME_V = 830;")
rep("function shEvents(inline) {\n  const T = now(), E = evState(), tab = E.evTab === \"rk\" ? \"rk\" : \"ov\",", "function shEvents0(inline, parts) { /* v830 the old page; shEvents (p830) lays it out */\n  const T = now(), E = evState(), tab = E.evTab === \"rk\" ? \"rk\" : \"ov\",")
rep("  return `${inline ? \"\" : `<div class=\"hd evhd\"><div><h2>Events</h2></div><button class=\"x\" data-act=\"close\" aria-label=\"Close\">✕</button></div>`}${tabs}${chips}${evBanner(k, T)}${body}${claim}`;\n}",
    "  if (parts) return { k, tab, body, claim, VIS }; /* v830 */\n  return `${inline ? \"\" : `<div class=\"hd evhd\"><div><h2>Events</h2></div><button class=\"x\" data-act=\"close\" aria-label=\"Close\">✕</button></div>`}${tabs}${chips}${evBanner(k, T)}${body}${claim}`;\n}")
rep("function mileTrack(list, pts, got, claimAct, unit, tip) { const top = list[list.length - 1][0], nxI = list.findIndex(([need]) => pts < need), nx = nxI >= 0 ? list[nxI] : null, prev = nxI > 0 ? list[nxI - 1][0] : 0;\n  const pos = v => Math.sqrt(Math.min(1, v / top)) * 100, ready = list.filter(([need], i) => pts >= need && !got.includes(i)).length;",
    "function mileTrack(list, pts, got, claimAct, unit, tip) { const top = list[list.length - 1][0], nxI = list.findIndex(([need]) => pts < need), nx = nxI >= 0 ? list[nxI] : null, prev = nxI > 0 ? list[nxI - 1][0] : 0;\n  const pos = v => Math.sqrt(Math.min(1, v / top)) * 100, ready = list.filter(([need], i) => pts >= need && !got.includes(i)).length; G.mtLast = { pts, nx, ready, unit }; /* v830 the page's nudge */")
js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "p830_events.js"), encoding="utf-8").read()
rep("/* the other events keep their existing panels, shown under their banner */", js + "\n/* the other events keep their existing panels, shown under their banner */")
# the last three titans' transmissions in the shipyard
rep('''  eclipse: "The Discovery Class Destroyer is an alliance flagship, with no limit on how many you build. Its command aura lifts the whole fleet.",''',
    '''  eclipse: "The Discovery Class Destroyer is an alliance flagship, with no limit on how many you build. Its command aura lifts the whole fleet.",
  armageddon: "The Armageddon is a siege fortress built around one gun. When the Worldbreaker Cannon fires, capital ships stop existing.",
  sovereign: "The Sovereign is the crown of the fleet: an imperial carrier that commands every ship beside it and fills the sky with strike wings.",
  harbinger: "The Eclipse Harbinger was built from schematics we don't fully understand. Four pylons, one cage of light, and I still don't know what it was made to fight.",''')
rep("lab = evkTxt(m[2]), ev = evkTxt((out.match(/class=\"evcard[^\"]* on\"[\\s\\S]*?<span class=\"ecn\">([\\s\\S]*?)<\\/span>/) || [])[1]) || \"event\";", "lab = evkTxt(m[2]), ev = (evkTxt((out.match(/class=\"evcard[^\"]* on\"[\\s\\S]*?<span class=\"ecn\">([\\s\\S]*?)<\\/span>/) || [])[1]) || \"event\").replace(/ rewards$/i, \"\"); /* v830 Daily Rewards */")
open(p, "w", encoding="utf-8").write(s); print("ok")
