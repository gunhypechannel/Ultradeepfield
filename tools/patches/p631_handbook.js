/* ---------- v631 the Commander's Handbook (owner: "remaster the how to play etc tab to be more visually appealing" ... "Build it
   all"). A cover with the Advisor and your reading progress, the map tour as a banner, ten chapter tiles in the game's own art; each
   chapter is three illustrated steps, key numbers as chips, a Show me button that takes you to the real screen and points at it, and
   that chapter's questions answered by the Advisor in speech bubbles. Counters are pictures, with the element wheel beside them. The
   first read of each chapter pays ◆1. ---------- */
const HB_IMG = k => (typeof ART !== "undefined" && ART[k]) || `art/${k}.webp`;
const HB = [
  { k: "basics", n: "First steps", img: "art/command.webp", col: "#38dfee", faq: ["Getting started", "Your account"],
    steps: [["📋", "Follow your quests: each one teaches the next system and pays a reward."], ["🗣", "The Advisor points at the very next thing to tap. Tap ✕ on the hand to hide it for a while."], ["🛡", "Your first 3 days (or until 300 score) your colonies can't be attacked. Learn against the Hive."]],
    chips: ["New commander shield: 3 days", "Or until 300 score"], show: ["Open my quests", () => ACT.nav({ v: "quests" })] },
  { k: "economy", n: "Economy", img: HB_IMG("metalMine"), col: "#ffb347", faq: ["Resources and buildings"],
    steps: [["⛏", "Metal, crystal and gas extractors make resources every minute, even while you're away."], ["☀", "Solar power runs them: keep energy above zero or production slows."], ["📦", "Storage caps what you can hold. Upgrade it before it fills."]],
    chips: ["Every building level uses 1 field", "Planets: 169 to 255 fields"], show: ["Show me my buildings", () => { ACT.nav({ v: "build" }); hbPoint(".bnlist article.bn", "Upgrade an extractor"); }] },
  { k: "research", n: "Research", img: HB_IMG("lab"), col: "#9a7bff", faq: [],
    steps: [["🔬", "The Research Lab unlocks technology: better ships, drives, weapons and shields."], ["🚀", "Drives make fleets faster; Weapons, Shields and Armor make every ship stronger."], ["🪐", "Astrophysics lets you hold more worlds: 1 more every 2 levels."]],
    chips: [`Up to ${typeof MAX_PLANETS !== "undefined" ? MAX_PLANETS : 9} worlds`, "Espionage Tech 2 for probes"], show: ["Open the Research Lab", () => openSheet({ type: "labs" })] },
  { k: "fleet", n: "Fleet and combat", img: HB_IMG("battleship"), col: "#ff6a5a", faq: ["Fleet and combat"], counters: 1,
    steps: [["🛠", "Build ships at the Shipyard. Each ship card shows its class and what it's best against."], ["⚔", "Rapid fire lets a ship hit its favourite target several times a round: bring the right counter."], ["🔧", "Repair docks bring back 30% of lost ships, and 70% of destroyed defenses are rebuilt."]],
    chips: ["30% of lost ships repaired", "70% of defenses rebuilt"], show: ["Open the Shipyard", () => openSheet({ type: "yard", pid: null })] },
  { k: "map", n: "Map and espionage", img: HB_IMG("spyProbe"), col: "#4fe0d0", faq: ["The map"],
    steps: [["🗺", "Your homeworld sits in a layer of the galaxy. Tap any world for its card."], ["🛰", "Send probes with Espionage on a planet card: more probes reveal fleet (2), defenses (3), buildings (5), research (7)."], ["🏳", "Capture worlds with a Colony Ship. A new colony is shielded for 7 days."]],
    chips: ["New colony shield: 7 days", "Probes: Shipyard 3"], show: ["▶ Fly the map tour", () => ACT.mapTour()] },
  { k: "events", n: "Events and bosses", img: "art/boss/el-fire-skin.webp", col: "#ff4d6a", faq: ["Events"],
    steps: [["👾", "World bosses appear on a schedule. Everyone who hits one shares the rewards."], ["🏆", "The top damage dealers and the final blow win the rarest prizes, runes included."], ["⏰", "Check Events for what's live now and what comes next."]],
    chips: ["Bosses drop runes", "Top 3 earn the most"], show: ["Open Events", () => ACT.nav({ v: "events" })] },
  { k: "elements", n: "Elements and runes", img: "art/boss/el-storm-skin.webp", col: "#e06bd8", faq: [], wheel: 1,
    steps: [["💠", "Runes socket into five rings: Fire attack, Water shields, Earth armor, Air speed, Spirit output."], ["✨", "Runes are rare: super bosses drop them; shards from play and the daily Trial slowly make more."], ["🔁", "Full rings unlock pairs, Harmony and Mastery. The right ring hits its counter element harder."]],
    chips: ["Rings open at Lv.5", "10 shards = 1 rune"], show: ["Open my Elements", () => { view = "cmd"; ACT.cmdPage({ k: "elements" }); }] },
  { k: "forge", n: "The Forge", img: "art/mat/crystal-6.webp", col: "#ffd25a", faq: [],
    steps: [["🔥", "The Flagship Dock forges gear for your flagship from materials."], ["💎", "Five of a material rarity fuse into one of the next: Common up to Mythic."], ["🛡", "Wear a full set for its set bonus. Higher rarities need a higher Dock level."]],
    chips: ["5 fuse into 1", "6 rarities"], show: ["Open the Forge", () => openSheet({ type: "flagship", tab: "forge" })] },
  { k: "ally", n: "Alliances", img: HB_IMG("allyStation"), col: "#55d6e8", faq: ["Alliances"],
    steps: [["🤝", "Join or found an alliance to share a station, chat and help."], ["⏩", "Tap Help on your allies' builds to speed them up; they help you back."], ["🛰", "Grow the alliance station together for bonuses everyone shares."]],
    chips: ["Help speeds builds", "Shared station"], show: ["Open Alliances", () => ACT.nav({ v: "ally" })] },
  { k: "shop", n: "Shop and Premium", img: "skins/pr13.webp", col: "#ffcf4a", faq: ["Upgrades and the shop"],
    steps: [["🛍", "The shop sells speed-ups, packs and items for ◆ void shards."], ["🎰", "The Glyph Wheel gives a free spin every day."], ["👑", "Premium tiers reward supporters with exclusive planet skins and buffs."]],
    chips: ["Free wheel spin daily", "16 premium tiers"], show: ["Open the shop", () => depotOpen()] }];
const hbRead = () => (S && S.hbRead) || {};
const hbCount = () => HB.filter(c => hbRead()[c.k]).length;
/* the questions of some FAQ categories, with their global numbers so the Advisor's answer button keeps working */
function hbFaq(cats) { let i = 0, out = ""; for (const [c, L] of FAQ) { for (const [q, a] of L) { if (cats.includes(c)) out += `<div class="faqi hbq" data-q="${esc((q + " " + a).toLowerCase())}"><button class="faqb" data-act="faq" data-i="${i}" aria-expanded="false"><span>${esc(q)}</span><i aria-hidden="true">▸</i></button><p>${esc(a)}</p></div>`; i++; } } return out; }
function hbCounters() { const C = [["fighter", "corvette", "Cruiser", "Light Fighters"], ["battleship", "bastion", "Dreadnought", "Battleships"], ["rocket", "bomber", "Bomber", "Turrets and defenses"], ["bastion", "destroyer", "Destroyer", "Dreadnoughts"], ["sovereign", "dreadnought", "Reaper", "Capital ships"]];
  return `<div class="hbctr"><div class="hbsh">Counters <small>who beats whom</small></div>${C.map(([t, a, an, tn]) => `<div class="hbcr"><span><img src="${HB_IMG(a)}" alt="" loading="lazy"><b>${an}</b></span><i>›</i><span class="t"><img src="${HB_IMG(t)}" alt="" loading="lazy"><b>${tn}</b></span></div>`).join("")}</div>`; }
function hbWheel() { const R = [["water", "fire"], ["fire", "air"], ["air", "earth"], ["earth", "water"]];
  return `<div class="hbctr"><div class="hbsh">The counter wheel <small>elements</small></div><div class="hbwh">${R.map(([a, b]) => `<span style="--a:${ELEM[a].col};--b:${ELEM[b].col}"><b>${EL_ICON[a]} ${ELEM[a].n}</b><i>beats</i><b>${EL_ICON[b]} ${ELEM[b].n}</b></span>`).join("")}<span style="--a:${ELEM.spirit.col};--b:${ELEM.spirit.col}"><b>✦ Spirit</b><i>meets</i><b>✦ Spirit</b></span></div></div>`; }
function shHowTo() { const ch = HB.find(c => c.k === G.hbCh), hd = (t, sub) => `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter">${sub}</div><h2>${t}</h2></div><button class="x" data-act="close" aria-label="Close">✕</button></div>`;
  if (ch) { const rd = hbRead()[ch.k];
    return hd(esc(ch.n), "Commander's Handbook") + `<div class="hbpage" style="--c:${ch.col}"><button class="gwlink hbback" data-act="hbCh" data-k="">‹ All chapters</button>
      <div class="hbhero"><img src="${ch.img}" alt="" loading="lazy"><div><small>CHAPTER ${HB.indexOf(ch) + 1} OF ${HB.length}</small><b>${esc(ch.n)}</b>${rd ? `<em>✓ Read</em>` : ""}</div></div>
      <ol class="hbsteps">${ch.steps.map(([ic, t], i) => `<li><span>${ic}</span><p><b>Step ${i + 1}</b>${esc(t)}</p></li>`).join("")}</ol>
      <div class="hbchips">${ch.chips.map(x => `<span>${esc(x)}</span>`).join("")}</div>
      <button class="btn amber wide" data-act="hbShow" data-k="${ch.k}">${esc(ch.show[0])} ›</button>
      ${ch.counters ? hbCounters() : ""}${ch.wheel || ch.counters ? hbWheel() : ""}
      ${ch.faq.length ? `<div class="faq hbfaq"><div class="hbadv"><img src="${afUrl("p_explain")}" alt=""><p>Questions about ${esc(ch.n.toLowerCase())}? Tap one and I'll answer.</p></div>${hbFaq(ch.faq)}</div>` : ""}
      ${HB.indexOf(ch) < HB.length - 1 ? `<button class="hbnext" data-act="hbCh" data-k="${HB[HB.indexOf(ch) + 1].k}"><small>NEXT CHAPTER</small><b>${esc(HB[HB.indexOf(ch) + 1].n)} ›</b></button>` : ""}<div class="fgpad"></div></div>`; }
  const n = hbCount();
  const cover = `<div class="hbcover"><img class="hbav" src="${afUrl("p_welcome")}" alt=""><div><small>ETC.</small><h2>Commander's Handbook</h2><p>${n >= HB.length ? "Every chapter read. You know the galaxy, Commander." : `${n} of ${HB.length} chapters read · each new one pays ◆1`}</p><i class="gwbar"><b style="width:${n / HB.length * 100}%"></b></i></div><button class="x" data-act="close" aria-label="Close">✕</button></div>`;
  const tour = `<button class="hbtour" data-act="mapTour"><span class="hbtp">▶</span><div><b>Neighbourhood tour</b><small>A guided flight over your homeworld, your neighbours and the galaxy beyond</small></div></button>`;
  const tiles = `<div class="hbtiles">${HB.map((c, i) => `<button class="hbtile${hbRead()[c.k] ? " rd" : ""}" style="--c:${c.col}" data-act="hbCh" data-k="${c.k}"><img src="${c.img}" alt="" loading="lazy"><span><small>${i + 1}</small><b>${esc(c.n)}</b></span>${hbRead()[c.k] ? `<i>✓</i>` : `<i class="nw">◆1</i>`}</button>`).join("")}</div>`;
  const chipsQ = ["What should I do first?", "attack", "boss", "rune", "alliance", "shop"];
  const ask = `<div class="faq hbask"><div class="hbadv"><img src="${afUrl("p_explain")}" alt=""><p>Ask me anything. Tap a question and I'll answer it, out loud too.</p></div><input id="faqq" class="faqq" type="search" placeholder="Search questions" aria-label="Search questions" autocomplete="off"><div class="hbqc">${chipsQ.map(q => `<button data-act="hbQ" data-q="${esc(q)}">${esc(q)}</button>`).join("")}</div>
    ${(() => { let i = 0; return FAQ.map(([c, L]) => `<section class="faqc"><h4>${esc(c)}</h4>${L.map(([q, a]) => `<div class="faqi hbq" data-q="${esc((q + " " + a).toLowerCase())}"><button class="faqb" data-act="faq" data-i="${i++}" aria-expanded="false"><span>${esc(q)}</span><i aria-hidden="true">▸</i></button><p>${esc(a)}</p></div>`).join("")}</section>`).join(""); })()}<p class="note faqnone" hidden>No question matches. Try another word.</p></div>`;
  return `<div class="hbwrap">${cover}${tour}${tiles}${ask}<div class="fgpad"></div></div>`; }
/* Show me: take you to the screen, then ring the thing to tap for a few seconds */
function hbPoint(sel, label, n = 0) { setTimeout(() => { try { const el = [...document.querySelectorAll(sel)].find(e => e.getBoundingClientRect().height > 4); if (!el) return n < 12 && hbPoint(sel, label, n + 1); el.scrollIntoView({ block: "center", behavior: "smooth" });
  setTimeout(() => { const r = el.getBoundingClientRect(), o = document.createElement("div"); o.className = "hbpt"; o.style.cssText = `left:${r.left - 6}px;top:${r.top - 6}px;width:${r.width + 12}px;height:${r.height + 12}px`; o.innerHTML = `<i>👆</i><b>${esc(label)}</b>`; document.body.appendChild(o);
    const kill = () => { o.remove(); removeEventListener("pointerdown", kill, true); }; addEventListener("pointerdown", kill, true); setTimeout(kill, 4500); }, 450); } catch (e) {} }, n ? 200 : 300); }
