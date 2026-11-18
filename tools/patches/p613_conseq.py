# v613: consequences (owner: "Do it" to: the Titans as a moral trap with a shared Seal Strain, choices that last, and a voice for Vael'Khor).
# Server: public.story_acts + story_act()/story_tally() (migrations v613_story_acts, v613_story_tally_fix); client: window.udfStory in
# udf-supabase.js. See p613_conseq.js / .css.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
js = open('tools/patches/p613_conseq.js', encoding='utf-8').read(); css = open('tools/patches/p613_conseq.css', encoding='utf-8').read()
i = s.index('</style>', s.index('#celeb{position:fixed')); s = s[:i] + css + s[i:]
a = s.index('const chProg = (C, m) => '); s = s[:a] + js + '\n' + s[a:]
# the Matriarch in the cinematic player: her painting behind, her face in a ring of Hive light, her words in green
rep('else if (!b.img) { w.querySelectorAll(".cnimg")', 'else if (!b.img && b.adv && prev.dataset.src) { /* v613 the scene stays behind her, dimmed */ }\n    else if (!b.img && b.queen) { const qs = "art/arch/brd.webp"; if (prev.dataset.src !== qs) { flip ^= 1; img.dataset.src = qs; img.style.backgroundImage = `url("${qs}")`; img.className = "cnimg " + (flip ? "b" : "a") + " on kb-in"; prev.classList.remove("on"); } }\n    else if (!b.img) { w.querySelectorAll(".cnimg")')
rep(': b.adv ? `<img class="cnadv" src="${advArt()}" alt="${ADV}">`', ': b.queen ? `<img class="cnqueen" src="${VK_ART}" alt="Queen Vael\'Khor">` : b.adv ? `<img class="cnadv" src="${advArt()}" alt="${ADV}">`')
rep('sub.innerHTML = b.txt ? `${b.who ? `<small>${esc(b.who)}</small>` : ""}<p class="cntx">${esc(b.txt)}</p>` : b.line ? `<p>${esc(b.line)}</p>` : "";',
    'sub.innerHTML = b.txt ? `${b.who ? `<small>${esc(b.who)}</small>` : ""}<p class="cntx">${esc(b.txt)}</p>` : b.line ? `${b.queen ? "<small>Queen Vael\'Khor</small>" : ""}<p>${esc(b.line)}</p>` : "";')
rep('sub.className = "cnsub" + (b.txt ? " tx" : "") + (b.adv ? " adv" : "");', 'sub.className = "cnsub" + (b.txt ? " tx" : "") + (b.adv ? " adv" : "") + (b.queen ? " queen" : ""); if (b.queen && !b.fx) fx.className = "cnfx fx-qn"; else if (b.adv && !b.fx && prev.dataset.src) fx.className = "cnfx fx-dim";')
rep('    mid.innerHTML = b.title ?', '    mid.classList.toggle("ch", !!b.choice); /* v613 room for the choice buttons */\n    mid.innerHTML = b.title ?')
# the seals holding well pay a little
rep('const prodBonus = () => 1 + (runePct("spirit") + allyPass().prod + fsB("prod") + collPct()) / 100;', 'const prodBonus = () => 1 + (runePct("spirit") + allyPass().prod + fsB("prod") + collPct() + (typeof sealHold === "function" ? sealHold() : 0)) / 100; /* v613 */')
# the Archives open on the Seal Strain and your chronicle
rep('<div class="colsum">🏆 <b>${collPct()}</b>', '${S.intro ? storyPanel() : ""}<div class="colsum">🏆 <b>${collPct()}</b>')
# answering the signal brings the Architects' story closer; burying it pushes it back
rep('const st = k => vpStat(k), d = S.bondDays || 0, fac = facOf()', 'const st = k => vpStat(k), d = (S.bondDays || 0) + ((S.choices || {}).signal === "answer" ? 4 : (S.choices || {}).signal === "bury" ? -6 : 0), fac = facOf()')
s2 = re.sub(r"GAME_V = 612\b", "GAME_V = 613", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
