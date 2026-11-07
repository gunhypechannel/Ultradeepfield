import sys, re
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)

# ============ v328 engagement: a named enemy, big-moment celebrations, a reason to come back ============


# ---- 2. a named enemy: the Hive answers to Vael'Khor ----
rep('''const INTRO_POST = ["The swarm is broken. We held, Commander.",''', '''const INTRO_POST = ["The swarm is broken. We held, Commander.", "That swarm answered to Vael'Khor, the Hive Matriarch. She devours whole worlds, and now she knows our name.",''')
rep('''"Now we rebuild. I'll post directives on the Base tab. Complete them and Fleet Command will send supplies."];''',
    '''"Now we rebuild, and we grow strong enough to end Vael'Khor. I'll post directives on the Base tab. Complete them and Fleet Command will send supplies."];''')
rep('''say: "The amber worlds belong to the Hive. I've marked a weak one near us: send the fighters."''', '''say: "The amber worlds belong to Vael'Khor's Hive. I've marked a weak garrison near us: send the fighters and show her we bite back."''')
rep('''"But the Hive knows we're here now. Once your Academy training is done, expect raids on our homeworld."''', '''"Vael'Khor felt that. Once your Academy training is done, expect her raiders over our homeworld."''')
rep('''say: "Send the Colony Ship along with your warships to a Hive world you can beat. Win the battle and the world becomes ours: our second planet."''',
    '''say: "Send the Colony Ship along with your warships to a Hive world you can beat. Win the battle and the world becomes ours: our second planet, and the first world we take back from Vael'Khor."''')

# ---- 3. the big moments get a full-screen celebration (first victory, first colony, the flagship, the Academy done) ----
CELEB = r'''
/* v328 celebrations: queued in S.celeb, shown one at a time when nothing else is on screen (before the Advisor's lines), with the
   moment's art, a burst of light, the reward and a Share button */
function celebrate(c) { S.celeb = S.celeb || []; if (!S.celeb.some(x => x.k === c.k)) { S.celeb.push(c); dirty(); } }
function showCeleb(c) { const w = document.createElement("div"); w.id = "celeb"; const fac = facOf(), art = c.art === "flag" ? FS_PORT[fac] : c.art === "adv" ? ADV_ART : null;
  w.innerHTML = `<div class="cbscrim"></div><div class="cbbox ${c.k}"><div class="cbrays"></div>${art ? `<img class="cbart${c.art === "adv" ? " adv" : ""}" src="${art}" alt="">` : `<div class="cbicon">${c.ic || "★"}</div>`}
    <div class="cbk">${esc(c.kick || "")}</div><h2 class="cbt">${esc(c.t)}</h2><p class="cbs">${esc(c.s)}</p>${c.rw ? `<div class="cbrw">${esc(c.rw)}</div>` : ""}
    <div class="cbbt"><button class="btn amber" data-act="celebX">${esc(c.go || "Onward")}</button>${c.rep && G.mode === "online" ? `<button class="btn ghost" data-act="celebShare" data-id="${esc(c.rep)}">↗ Share the battle</button>` : `<button class="btn ghost" data-act="celebShare">↗ Share</button>`}${c.chat && G.mode === "online" ? `<button class="btn ghost" data-act="celebChat">💬 Say hi in chat</button>` : ""}</div></div>`;
  $("#app").appendChild(w); try { SFX.gong(); } catch (e) {} G.celebNow = c; }
'''
rep('''function flushSay() {''', CELEB.strip('\n') + '''
function flushSay() { if (S.celeb && S.celeb.length && !battle && !sheet && !advLines && !$("#celeb") && !$("#adv") && G.ready) { showCeleb(S.celeb.shift()); dirty(); return; } if ($("#celeb")) return; // v328 a celebration first, then the Advisor
  flushSay0(); }
function flushSay0() {''')
rep('''  sfxToggle: () => {''', '''  celebX: () => { const w = $("#celeb"); if (w) w.remove(); G.celebNow = null; setTimeout(() => { try { flushSay(); coachRender(true); } catch (e) {} }, 60); },
  celebChat: () => { ACT.celebX(); setTimeout(() => ACT.chat({}), 120); },
  celebShare: async d => { const c = G.celebNow || {}; if (d.id && findRep(d.id) && G.mode === "online") { ACT.celebX(); return setTimeout(() => ACT.repShareOpen({ id: d.id }), 120); }
    const text = `${c.t || "Ultra Deep Field"}: ${c.s || ""} Come play Ultra Deep Field with me.`, url = location.protocol.startsWith("http") ? location.href.split("#")[0] : "https://gunhypechannel.github.io/Ultradeepfield/";
    try { if (navigator.share) { await navigator.share({ title: "Ultra Deep Field", text, url }); return; } } catch (e) { return; }
    try { await navigator.clipboard.writeText(text + " " + url); toast("Copied. Paste it to your friends."); } catch (e) { toast("Couldn't share from here.", "warn"); } },
  sfxToggle: () => {''')
# the moments
rep('''  if (S.chapter === 1 && S.wins >= 1) { S.chapter = 2; S.nextRaid = S.t + 10 * 60000;''', '''  if (S.chapter === 1 && S.wins >= 1) { S.chapter = 2; S.nextRaid = S.t + 10 * 60000;
    celebrate({ k: "win1", kick: "Chapter 1 complete", t: "First Victory", ic: "⚔", s: "The Hive garrison is broken. Our fighters drew first blood against Vael'Khor.", say: "First blood, Commander! The garrison is broken, and Vael'Khor knows it.", rep: (S.reports.find(r => r.kind === "attack" && r.winner === "a") || {}).id, go: "Onward" });''')
rep('''`${p.name} is occupied. Welcome to the empire.`, "win");''', '''`${p.name} is occupied. Welcome to the empire.`, "win");
      if (!prev && myPlanets().length === 2) celebrate({ k: "colony1", kick: "A second world", t: `${p.name} Is Ours`, ic: "🪐", s: `Our flag flies over ${p.name}. The empire now spans two worlds, and the first one we took back from the Hive.`, go: "Onward" });''')
rep('''    toast("Flagship commissioned! It leads your fleets now.", "win");''', '''    toast("Flagship commissioned! It leads your fleets now.", "win"); celebrate({ k: "flag", kick: "Flagship commissioned", t: "Our Flagship Rises", art: "flag", s: "Our flagship leads every fleet from now on. It gains experience in every fight and wears the gear the Dock forges.", go: "Onward" });''')
# ---- 4. a reason to come back: the Academy ends with a supply convoy that lands in 8 hours ----
rep('''  else { S.say.push("That's the Academy done, Commander.''', '''  else { S.retGift = { at: now() + 8 * 3600e3, rw: { m: 30000, c: 20000, g: 10000, shards: 10 } }; // v328
    celebrate({ k: "acad", kick: "Flight Academy", t: "Academy Complete", art: "adv", s: "You've built an empire, won your first battles, settled a second world and commissioned a flagship. The galaxy is yours to take.", rw: "Fleet Command is sending a supply convoy: 30K metal, 20K crystal, 10K gas and ◆10. It lands in 8 hours.", chat: 1, go: "Onward, Commander" });
    S.say.push("That's the Academy done, Commander.''')
rep('''"Every 2 Astrophysics levels lets us hold another world: build more Colony Ships and send them with escorts to Hive worlds we can beat. I'll keep pointing you at the next directive on your path."); S.pathOpen = 1; flushSay(); }''',
    '''"Every 2 Astrophysics levels lets us hold another world: build more Colony Ships and send them with escorts to Hive worlds we can beat. I'll keep pointing you at the next directive on your path.", "And Commander: Fleet Command's supply convoy lands in 8 hours. Come back then and claim it on the Quests tab."); S.pathOpen = 1; flushSay(); }''')
rep('''    ${st ? `<h2 class="sec">Flight Academy · step''', '''    ${S.retGift ? `<article class="card quest${S.retGift.at <= T ? " done hi" : ""}"><header>📦 Fleet Command supply convoy</header><p>${S.retGift.at <= T ? "The convoy has landed. Your supplies are waiting." : "On its way from Fleet Command for finishing the Academy."}</p>
      <div class="rw"><span class="cost">${costHTML(S.retGift.rw)} <span class="shard">◆${S.retGift.rw.shards}</span></span>${S.retGift.at <= T ? `<button class="btn amber" data-act="retClaim">Claim</button>` : `<span class="note">Lands in <span data-end="${S.retGift.at}">${ftime(S.retGift.at - T)}</span></span>`}</div></article>` : ""}
    ${st ? `<h2 class="sec">Flight Academy · step''')
rep('''  sfxToggle: () => {''', '''  retClaim: () => { const g = S.retGift; if (!g || g.at > now()) return; for (const r of ["m", "c", "g"]) S.res[r] += g.rw[r] || 0; S.shards = (S.shards || 0) + (g.rw.shards || 0); logReward("Fleet Command supply convoy", g.rw, { shards: g.rw.shards, kind: "quest" }); S.retGift = null; dirty(); try { SFX.research(); } catch (e) {} toast("Supply convoy unloaded.", "win"); render(true); },
  sfxToggle: () => {''')
# the convoy calls in when it lands, once
rep('''function progress() {
  const q = quest();''', '''function progress() {
  if (S.retGift && S.retGift.at <= now() && !S.retGift.told) { S.retGift.told = 1; note("Fleet Command's supply convoy has landed. Claim it on the Quests tab.", "win"); }
  const q = quest();''')

# the guide waits while a celebration is up
rep('''&& !advLines && !$("#adv") && !$("#authw") &&''', '''&& !advLines && !$("#adv") && !$("#celeb") && !$("#authw") &&''')

# the "make N now (more as your mines refill)" warning compared what's left to build against the total wanted, ships already owned included
rep('''const tutMake = (k, n) => { G.tutN = [k, n, S.tut.i]; const q = tutQty(k, n) || n; return q < n ?''', '''const tutMake = (k, n) => { G.tutN = [k, n, S.tut.i]; const need = Math.max(1, n - own(k) - S.sq.filter(q => q.k === k).reduce((a, q) => a + (q.left || 0), 0)), q = tutQty(k, n) || need; return q < need ?''')

# ---- the Advisor appears as a hologram: she beams up from a projector pad, scanlines roll over her, she flickers now and then
#      and glows as she appears ----
rep('''<div class="box"><img class="advimg" src="${ADV_ART}" alt="">''', '''<div class="box"><img class="advimg" src="${ADV_ART}" alt=""><i class="hscan"></i><i class="hbeam"></i>''')
rep('''#coach.gdhide>*{''', '''#adv .advimg{opacity:.9;filter:drop-shadow(0 0 18px rgba(85,214,232,.7)) grayscale(1) sepia(.6) hue-rotate(150deg) saturate(2.3) brightness(1.1) contrast(1.08);animation:holoIn .8s cubic-bezier(.2,.9,.3,1) both,holoFlick 7s 1.2s infinite}
#adv .hscan{position:absolute;left:0;bottom:0;width:clamp(118px,32vw,230px);height:min(58vh,470px);pointer-events:none;z-index:1;mix-blend-mode:screen;
  background:linear-gradient(180deg,transparent 0,rgba(140,240,255,.32) 50%,transparent 100%) 0 -120%/100% 34% no-repeat,repeating-linear-gradient(180deg,rgba(140,235,255,.24) 0 1px,transparent 1px 3px),linear-gradient(180deg,rgba(85,214,232,.26),rgba(85,214,232,.08) 70%,transparent);
  -webkit-mask-image:linear-gradient(180deg,#000 82%,transparent);mask-image:linear-gradient(180deg,#000 82%,transparent);animation:holoIn .8s cubic-bezier(.2,.9,.3,1) both,holoScan 3.6s 1s linear infinite}
#adv .hbeam{position:absolute;left:0;bottom:-10px;width:clamp(118px,32vw,230px);height:30px;pointer-events:none;z-index:1;background:radial-gradient(ellipse 50% 40% at 50% 55%,rgba(170,245,255,.95),rgba(85,214,232,.45) 45%,transparent 72%);filter:blur(1.5px);animation:holoPad 2.4s ease-in-out infinite}
#adv .hbeam::before{content:"";position:absolute;left:12%;right:12%;bottom:45%;height:min(40vh,320px);background:linear-gradient(0deg,rgba(110,230,255,.45),rgba(85,214,232,.08) 70%,transparent);clip-path:polygon(10% 100%,90% 100%,100% 0,0 0);opacity:.7}
#adv.talk .advimg{animation:holoIn .8s cubic-bezier(.2,.9,.3,1) both,holoTalk .42s ease-in-out infinite alternate}#adv.talk .hbeam{animation-duration:.8s}
@keyframes holoIn{0%{clip-path:inset(100% 0 0 0);opacity:0}45%{clip-path:inset(0 0 0 0);opacity:.9}55%{opacity:.35}62%{opacity:1}70%{opacity:.6}78%,100%{clip-path:inset(0 0 0 0);opacity:1}}
@keyframes holoFlick{0%,90%,100%{opacity:1;transform:none}91%{opacity:.7;transform:translateX(1.5px)}92%{opacity:1;transform:none}95%{opacity:.82}}
@keyframes holoScan{to{background-position:0 220%,0 0,0 0}}@keyframes holoPad{50%{opacity:.7;transform:scaleX(.92)}}
@keyframes holoTalk{from{filter:drop-shadow(0 0 18px rgba(85,214,232,.7)) grayscale(1) sepia(.6) hue-rotate(150deg) saturate(2.3) brightness(1.04) contrast(1.08)}to{filter:drop-shadow(0 0 32px rgba(120,235,255,.95)) grayscale(1) sepia(.6) hue-rotate(150deg) saturate(2.6) brightness(1.24) contrast(1.08)}}
@media (prefers-reduced-motion:reduce){#adv .advimg,#adv .hscan,#adv .hbeam,#adv.talk .advimg{animation:none}}
#coach.gdhide>*{''')

# fighters still out gathering at a resource field didn't count as busy, so the pyramid step sent you to a station with no ships home
rep('''const tutWaitShips = () => !Object.values(S.ships || {}).some(v => v > 0) && S.fleets.some(f => f.phase === "back" || f.phase === "out") ? [DOCKT("fleets", "Your fighters are flying home. They'll be ready in a moment")] : null;''',
    '''const tutWaitShips = () => !Object.values(S.ships || {}).some(v => v > 0) && S.fleets.some(f => f.phase === "back" || f.phase === "out" || f.phase === "gather") ? [DOCKT("fleets", S.fleets.some(f => f.phase === "gather") && !S.fleets.some(f => f.phase === "back") ? "Your fighters are gathering at the field. They'll be home soon" : "Your fighters are flying home. They'll be ready in a moment")] : null; // v328: gathering counts as busy''')

# ---- styles ----
rep('''#coach.gdhide>*{''', '''/* v328 celebrations and the Advisor's voice button */
#celeb{position:fixed;inset:0;z-index:95;display:flex;align-items:flex-start;justify-content:center;padding:18px;overflow-y:auto;overscroll-behavior:contain}#celeb .cbscrim{position:fixed;inset:0;background:radial-gradient(circle at 50% 45%,rgba(30,40,70,.55),rgba(0,0,0,.88));animation:fadeIn .35s ease}
#celeb .cbbox{position:relative;margin:auto 0;width:min(420px,100%);text-align:center;padding:26px 18px 18px;border-radius:20px;background:linear-gradient(180deg,rgba(18,30,52,.96),rgba(6,12,24,.97));border:1px solid rgba(255,206,110,.55);box-shadow:0 0 60px rgba(255,180,70,.28),inset 0 0 40px rgba(255,200,120,.06);animation:cbIn .55s cubic-bezier(.2,1.4,.4,1);overflow:hidden}
#celeb .cbrays{position:absolute;left:50%;top:22%;width:640px;height:640px;margin:-320px 0 0 -320px;background:repeating-conic-gradient(from 0deg,rgba(255,210,120,.13) 0 6deg,transparent 6deg 18deg);animation:cbSpin 18s linear infinite;pointer-events:none;mask:radial-gradient(circle,#000 20%,transparent 62%);-webkit-mask:radial-gradient(circle,#000 20%,transparent 62%)}
#celeb .cbart{position:relative;width:100%;max-height:200px;object-fit:contain;filter:drop-shadow(0 8px 26px rgba(255,190,90,.35));animation:cbArt 1.1s ease-out}#celeb .cbart.adv{max-height:min(200px,24vh);object-fit:cover;object-position:top;border-radius:12px}#celeb .cbart{max-height:min(200px,26vh)}
#celeb .cbicon{position:relative;font-size:76px;line-height:1.1;filter:drop-shadow(0 0 22px rgba(255,200,110,.8));animation:cbArt 1.1s ease-out}
#celeb .cbk{position:relative;margin-top:8px;font:600 12px var(--f-display);letter-spacing:.28em;text-transform:uppercase;color:#ffd36b}#celeb .cbt{position:relative;margin:4px 0 6px;font:800 30px var(--f-display);letter-spacing:.03em;background:linear-gradient(180deg,#fff6dc,#ffc861);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:0 0 30px rgba(255,190,90,.25)}
#celeb .cbs{position:relative;color:#d7e4ef;font-size:15px;line-height:1.45;margin:0 4px}#celeb .cbrw{position:relative;margin:12px 0 0;padding:9px 10px;border-radius:12px;background:rgba(255,200,110,.1);border:1px solid rgba(255,200,110,.35);color:#ffe2a6;font-size:13.5px}
#celeb .cbbt{position:relative;display:flex;flex-direction:column;gap:8px;margin-top:16px}#celeb .cbbt .btn{width:100%}
@keyframes cbIn{from{transform:scale(.6) translateY(30px);opacity:0}to{transform:none;opacity:1}}@keyframes cbSpin{to{transform:rotate(360deg)}}@keyframes cbArt{from{transform:scale(1.25);opacity:0;filter:brightness(2.2)}to{transform:none;opacity:1}}
.adv .box{position:relative}
#coach.gdhide>*{''')

v = int(re.search(r"const GAME_V = (\d+)", t).group(1)); t = t.replace(f"const GAME_V = {v}", "const GAME_V = 328", 1)
open(p, 'w', encoding='utf-8', newline='').write(t); print('v328 from', v)
