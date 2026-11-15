# v576 The Advisor split (owner: "We need to do a better job at deciding when to use the full screen advisor and the short, for the
# first time interaction maybe do the advisor then the interaction? When you're in planet view and do something it can be the color
# and when you're in map view it could be the hologram?").
# 1) The first time a commander opens one of the main screens, the full-screen Advisor explains it first (two lines, tap through),
#    then the screen opens (ADV_INTRO, advIntro in openSheet; once per screen, never during the tutorial or a battle). The Wardrobe's
#    and the Vault's old hologram hellos are folded into theirs.
# 2) Her look follows where you are: on your planet she appears in full colour (the dialog and the short card); on the galaxy map and
#    in battle she is the hologram. Live-event calls (sbSay: finales, boss warnings) are always the hologram.
import sys, re, json
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
J = lambda o: json.dumps(o, ensure_ascii=False)
INTRO = {
 "events": ["This is the Events hub, Commander. Every boss, every battle for the Cube and every season finale is listed here.", "If something big is coming, you'll see it here first. And I'll warn you too."],
 "archives": ["The Archives. Everything we learn about this galaxy is kept here: the monsters, the Wardens, the old empires.", "Every record you recover tells a little more of the story. Let's fill it together."],
 "wardrobe": ["Everything you earn on the Void Pass can be worn here: banners, frames, warp trails, even my outfits.", "The wardrobe! Go on, Commander... let the whole galaxy see your colours."],
 "vault": ["When a season ends, its cosmetics come here, so nothing you missed is lost for good.", "The Vault. Every token you earn ends up here. Spend wisely... or don't. I won't tell."],
 "finale": ["This is a season finale, Commander. One chapter of the Ten Seals, and the whole galaxy sees how it ends.", "Watch it unfold on the map, then bring the boss down before the hunt ends, or the seal cracks."],
 "flagship": ["Flagship Command. This is your own ship, Commander, the heart of your fleet.", "Every upgrade you give it makes the fleets that sail with it stronger."],
 "ally": ["Your alliance. Commanders who fight together grow faster, share gifts and take on the biggest bosses as one.", "A strong alliance is worth more than any fleet."],
 "ranks": ["The rankings. Every commander in the galaxy, measured against each other.", "Don't worry about the top yet. Just climb, one place at a time."],
 "shop": ["The shop. Shards, boosters and supplies, all in one place.", "Spend smart, Commander. Speed-ups are best saved for the long builds."],
 "ach": ["Achievements. Every milestone you reach is recorded here, and most of them pay out shards.", "Check back now and then. You'll be surprised what you've already earned."],
}
MOOD = {}
for k, (a, b) in INTRO.items(): MOOD[a] = "calm"; MOOD[b] = "warm" if k not in ("finale",) else "grave"
MOOD[INTRO["wardrobe"][1]] = "playful"; MOOD[INTRO["vault"][1]] = "playful"; MOOD[INTRO["ranks"][1]] = "warm"
# ---- 1) the first look at a screen
rep('function openSheet(s) { try {',
    '/* v576 the first time a commander opens a main screen, the full-screen Advisor explains it, then the screen opens */\n'
    'const ADV_INTRO = ' + J(INTRO) + ';\n'
    'function advIntro(s) { try { if (!s || !S || !G.ready || !ADV_INTRO[s.type] || s.noIntro || battle || advLines || $("#adv") || $("#celeb") || tutOn() || G.advThen) return false; S.advOnce = S.advOnce || {}; const k = "in:" + s.type; if (S.advOnce[k]) return false;\n'
    '  if ((s.type === "wardrobe" && S.advOnce.ward) || (s.type === "vault" && S.advOnce.vault)) { S.advOnce[k] = now(); return false; } /* they met her hello before v576 */\n'
    '  advOnce(k); if (s.type === "wardrobe") S.advOnce.ward = now(); if (s.type === "vault") S.advOnce.vault = now(); s.noIntro = 1; G.advThen = () => setTimeout(() => { try { openSheet(s); } catch (e) {} }, 140); say(ADV_INTRO[s.type].slice()); return true; } catch (e) { return false; } }\n'
    'function openSheet(s) { if (advIntro(s)) return; try {')
rep('if (S && advOnce("ward")) setTimeout(() => { try { advHolo(ADV_NEWS.x_ward); } catch (e) {} }, 900); /* v566 */ ', '')
rep('if (S && advOnce("vault")) setTimeout(() => { try { advHolo(ADV_NEWS.x_vault); } catch (e) {} }, 900); /* v566 */ ', '')
# ---- 2) colour on your planet, the hologram on the map
rep('  $("#advt").textContent = advLines[0]; try { document.documentElement.dataset.advMood = advMood(advLines[0]); } catch (e) {} speak(advLines[0]);',
    '  try { $("#adv").classList.toggle("color", advColor()); } catch (e) {} /* v576 */\n  $("#advt").textContent = advLines[0]; try { document.documentElement.dataset.advMood = advMood(advLines[0]); } catch (e) {} speak(advLines[0]);')
rep('w.querySelector(".hsay span").textContent = line;', 'w.classList.toggle("color", force !== 1 && advColor()); /* v576 live-event calls stay the hologram */ w.querySelector(".hsay span").textContent = line;')
rep('function advHolo(line, force) {', 'const advColor = () => view === "base" && !battle && !(typeof G3 !== "undefined" && G3 && G3.cam && G3.cam.cine); /* v576 her full-colour self on your planet; the hologram on the map and in battle */\nfunction advHolo(line, force) {')
CSS = ('/* v576 the Advisor in full colour (on your planet) */\n'
 '#adv.color .advimg,#advh.color .advimg{opacity:1;filter:drop-shadow(0 8px 18px rgba(0,0,0,.6));animation:advColIn .45s cubic-bezier(.2,.9,.3,1) both}\n'
 '#adv.color.talk .advimg,#advh.color.talk .advimg{animation:advColIn .45s cubic-bezier(.2,.9,.3,1) both,advColTalk .5s ease-in-out infinite alternate}\n'
 '#adv.color .hscan,#adv.color .hbeam,#advh.color .hscan,#advh.color .hbeam{display:none}\n'
 '#adv.color .box{border-color:rgba(255,206,140,.55);background:linear-gradient(90deg,rgba(42,32,24,.96),rgba(16,14,20,.96));box-shadow:0 0 26px rgba(255,190,110,.16)}\n'
 '#adv.color .advv{border-color:rgba(255,206,140,.6);color:#ffe6c0;background:rgba(22,16,12,.8)}\n'
 '#advh.color .holo{filter:none}#advh.color .advimg{border-radius:10px;-webkit-mask-image:linear-gradient(180deg,#000 80%,transparent);mask-image:linear-gradient(180deg,#000 80%,transparent)}\n'
 '#advh.color .hsay{background:rgba(18,15,22,.95);border-color:rgba(255,206,140,.55);box-shadow:0 8px 26px rgba(0,0,0,.55);color:#f6efe4}\n'
 '@keyframes advColIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}@keyframes advColTalk{to{transform:translateY(-1.5px) scale(1.012)}}\n'
 '@media (prefers-reduced-motion:reduce){#adv.color .advimg,#advh.color .advimg{animation:none}}\n')
rep('/* v566 her moods: the glow round her hologram', CSS + '/* v566 her moods: the glow round her hologram')
rep('const ADV_MOOD_L = {', 'const ADV_MOOD_L = {' + J(MOOD)[1:-1] + ', ')
s2 = re.sub(r"GAME_V = 575\b", "GAME_V = 576", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
