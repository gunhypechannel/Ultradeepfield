/* v613 consequences (owner: "Do it", for: the Titans as a moral trap / a shared Seal Strain, real choices that last, and a voice for
   Vael'Khor). Every commander's choices and Titan count go to the server (story_act); the galaxy's tally comes back (story_tally) and
   sets the Seal Strain that everyone sees. Offline, the strain counts this commander's own choices and the Seal Ledger. */
const STRAIN_W = { titans: 3, warden: { kill: 4, spare: -3 }, pdata: { solar: 2, verdant: -2 }, signal: { answer: 1, bury: -1 }, queen: { hear: 2 } };
const titansOwned = () => { try { return ["armageddon", "sovereign", "harbinger"].reduce((a, k) => a + (SH[k] ? own(k) : 0), 0); } catch (e) { return 0; } };
function storyTally() { if (G.storyT) return G.storyT; const t = { titans: { _n: titansOwned(), _p: 1 } }, c = S.choices || {}; for (const k in c) t[k] = { _p: 1, [c[k]]: 1 }; return t; }
function strainPts(t) { let P = ((t.titans || {})._n || 0) * STRAIN_W.titans; for (const k of ["warden", "pdata", "signal", "queen"]) for (const v in STRAIN_W[k]) P += ((t[k] || {})[v] || 0) * STRAIN_W[k][v];
  try { for (const L of finLedger()) P += L.st === "cracked" ? 12 : L.st === "held" ? 4 : 0; } catch (e) {} return P; }
function strainNow() { const P = strainPts(storyTally()); return P <= 0 ? 0 : Math.min(99, Math.round(100 * P / (P + 80))); }
const sealHold = () => G.strain != null && G.strain < 25 ? 3 : 0; /* the seals holding well: +3% production on every world */
const STRAIN_SAY = [[25, "Commander, the seals are under strain. Every Titan and every fallen Warden adds to it, ours and everyone else's. I'm only telling you so you know the price."],
  [50, "The strain on the seals just passed halfway. I can hear the Cube counting faster."], [75, "Three quarters, Commander. If this keeps up, the door won't need anyone to open it."]];
const STRAIN_LOW = "The seals are holding well. The galaxy is breathing easier, and our worlds can feel it.";
function storySync(force) { if (!S || !G.ready) return; const T = Date.now(), su = window.udfStory, on = su && G.mode === "online";
  if (on) { const n = titansOwned(); if (S.titRep !== n) { S.titRep = n; dirty(); su.act("titans", "", n).catch(() => {}); }
    if (force || !G.storyAt || T - G.storyAt > 9 * 60e3) { G.storyAt = T; su.tally().then(t => { G.storyT = t || {}; strainCheck(); }).catch(() => {}); } }
  strainCheck(); }
function strainCheck() { const v = G.strain = strainNow(); if (!S.intro || (S.tut && S.tut.k !== "done")) return; S.strainHi = S.strainHi | 0;
  for (const [th, l] of STRAIN_SAY) if (v >= th && S.strainHi < th) { S.strainHi = th; dirty(); S.say.push(l); try { flushSay(); } catch (e) {} return; }
  if (v < 25 && !S.strainLow && S.choices && Object.keys(S.choices).length) { S.strainLow = 1; dirty(); try { advHolo(STRAIN_LOW, true); } catch (e) {} } }
setInterval(() => { try { storySync(); } catch (e) {} }, 60000); setTimeout(() => { try { storySync(true); } catch (e) {} }, 20000);

/* ---------- the choices: four moments, one at a time, each remembered by her and by the galaxy ---------- */
const VK_ART = "art/chron/c4.webp";
const STORY_CH = [
  { id: "warden", t: "The Fallen Guardian", when: () => (vpStat("bosses") >= 1 || archLv("d_warden") >= 2) && (S.bondDays || 0) >= 3,
    beats: [{ img: "art/boss/warden-skin.webp", kb: "in", chip: "A choice", txt: "Your salvage fleet has found a Warden, broken but alive. It is still bracing its seal with what's left of its body. Its heart is exposed." },
      { adv: 1, line: "Commander, its heart would build us a Titan. But if it dies, its seal weakens. I won't choose for you.", pose: "explain", choice: [["Harvest its heart", "kill", "+1 Titan Core and ◆30", "Its seal weakens. Seal Strain rises."], ["Let it heal", "spare", "Nothing today", "The seal holds. Seal Strain eases."]] }],
    out: { kill: { rw: { shards: 30, tc: 1 }, lines: ["It's done. We have its heart. I'll log what it cost, even if no one else does."], rec: "Harvested the heart of a living Warden." },
      spare: { rw: {}, lines: ["We leave it be. It watched our ships the whole way out, Commander. I think it knows."], rec: "Let a wounded Warden live." } } },
  { id: "pdata", t: "The Pyramid Map", when: () => archLv("d_pyr") >= 2 && (S.choices || {}).warden && Date.now() - ((S.choiceAt || {}).warden || 0) > 864e5,
    beats: [{ img: "art/arch/ovl.webp", kb: "right", chip: "A choice", txt: "The pyramid network's map is decoded. The Solar Dominion and the Verdant Collective both want it, and both have sent envoys. Neither will share." },
      { adv: 1, line: "The Dominion would use it to wake the pyramids. The Verdant would use it to mend the seals. Someone is going to be very disappointed in us.", pose: "point", choice: [["Give it to the Dominion", "solar", "⚡3 boosts and ◆30", "They wake a pyramid. Seal Strain rises."], ["Give it to the Verdant", "verdant", "Metal, crystal and ◆15", "They mend a seal. Seal Strain eases."], ["Keep it secret", "keep", "An Architect record, now, and ◆10", "Neither House will thank you."]] }],
    out: { solar: { rw: { shards: 30, boosts: 3 }, lines: ["The Dominion is delighted. They've already started waking a pyramid. I hope they know how to put it back to sleep."], rec: "Gave the pyramid map to the Solar Dominion." },
      verdant: { rw: { shards: 15, m: 6000, c: 4000 }, lines: ["The Verdant are mending a seal tonight, with our map. It won't make us richer. It might keep us alive."], rec: "Gave the pyramid map to the Verdant Collective." },
      keep: { rw: { shards: 10 }, fx: () => archUnlock("x_1", 2), lines: ["We keep it. Secrets are safer with us than with either of them. The Syndicate would be proud, Commander. I'm not sure that's a compliment."], rec: "Kept the pyramid map secret." } } },
  { id: "signal", t: "The Call", when: () => archLv("x_1") >= 2 && (S.bondDays || 0) >= 8,
    beats: [{ img: "art/lore/architects.webp", kb: "up", chip: "A choice", txt: "The signal from the pyramids has found your comms array. It's asking for a reply, in a language only your Advisor can read." },
      { adv: 1, line: "It wants us to answer, Commander. I could. I'm afraid of what answers back.", pose: "cube", choice: [["Answer it", "answer", "The Architects' story comes sooner, and ◆20", "Something will hear you."], ["Bury it", "bury", "Seal Strain eases a little, and ◆20", "The truth waits longer."]] }],
    out: { answer: { rw: { shards: 20 }, lines: ["I answered. For a moment the whole array went quiet. Then something said thank you."], rec: "Answered the signal from the pyramids." },
      bury: { rw: { shards: 20 }, lines: ["Buried. It's still calling, just not to us. Thank you, Commander. I wasn't ready."], rec: "Buried the signal from the pyramids." } } },
  { id: "queen", t: "The Queen's Offer", when: () => archLv("l_queen") >= 2 && vpStat("hiveWins") >= 20 && (S.vk || {}).vk3,
    beats: [{ queen: 1, chip: "Incoming transmission", line: "I don't hate you, Commander. I simply want my children to live." },
      { queen: 1, line: "When the door opens, stand aside. Let my swarm pass, and yours will live too. That is all I ask.", choice: [["Refuse her", "refuse", "◆25", "She will remember."], ["Hear her out", "hear", "Her story, and ◆25", "Seal Strain rises."]] }],
    out: { refuse: { rw: { shards: 25 }, q: ["Then we will meet at the door. I will be sorry when you fall. I truly will."], lines: ["Good. I've seen what happens to the ones who listen."], rec: "Refused the Matriarch's offer." },
      hear: { rw: { shards: 25 }, q: ["Thank you. No one has listened to me in ten thousand years.", "My world was the only one it spared. My children are all that is left of it. Wouldn't you open any door for yours?"], lines: ["Commander... be careful. Kindness is how she wins."], rec: "Heard out Queen Vael'Khor." } } }];
/* Vael'Khor's own transmissions, as the Hive war goes on */
const VK_T = [{ id: "vk1", when: () => vpStat("hiveWins") >= 5, q: ["So. The commander who went back for the pods. I know your name now. I wonder if you know mine."], a: "That was her, Commander. Vael'Khor. She's never spoken to anyone before." },
  { id: "vk2", when: () => vpStat("hiveWins") >= 15 && (S.vk || {}).vk1, q: ["You burn my nests and call it victory. I fed those children with my own hands, Commander."], a: "She wants you to feel guilty. Don't let her choose how you feel." },
  { id: "vk3", when: () => archLv("l_queen") >= 2 && (S.vk || {}).vk2, q: ["I was there when the dark came. It looked at my world, and it chose to let us live. Do you know what that feels like? To be chosen?"], a: "She's telling the truth, Commander. That's what frightens me." },
  { id: "vk4", when: () => (G.strain | 0) >= 50 && (S.vk || {}).vk1, q: ["Can you feel it? The seals are thinning. Your Titans sing to it, Commander. Every one of them."], a: "She can feel the strain too. I hate that she's right." }];
const STORY_SPARE = ["Commander, the Warden we spared is standing over our homeworld. It hasn't moved in hours. I think it's guarding us."];
function storyBeats(C) { return C.beats.map(b => Object.assign({}, b)); }
function vkBeats(L, chip) { return L.map((line, i) => ({ queen: 1, chip: i ? undefined : chip, line })); }
function storyPlay(C) { S.choices = S.choices || {}; S.choiceAt = S.choiceAt || {}; G.storyBusy = 1;
  cinema(storyBeats(C), { onChoice: v => { const o = C.out[v]; if (!o || S.choices[C.id]) return []; S.choices[C.id] = v; S.choiceAt[C.id] = Date.now(); dirty();
      try { if (o.rw && Object.keys(o.rw).length) grantRw(o.rw, C.t); } catch (e) {} try { o.fx && o.fx(); } catch (e) {} try { if (window.udfStory && G.mode === "online") window.udfStory.act(C.id, v, 0).then(() => storySync(true)).catch(() => {}); } catch (e) {}
      const tt = (G.storyT || {})[C.id], split = tt && tt._p >= 2 ? Math.round(100 * ((tt[v] || 0) + 1) / (tt._p + 1)) : null; G.storySplitShown = split != null;
      return (o.q ? vkBeats(o.q) : []).concat(o.lines.map(line => ({ adv: 1, line })), split != null ? [{ chip: "The galaxy remembers", txt: `${split}% of commanders made the same choice.`, t: 3800, keep: 1 }] : []); },
    onSkip: () => { G.storyBusy = 0; } }, () => { G.storyBusy = 0; if (!G.storySplitShown) setTimeout(() => storySplit(C), 1500); }); }
function storySplit(C) { const t = (G.storyT || {})[C.id], v = (S.choices || {})[C.id]; if (!t || !v || !(t._p > 1)) return; const pc = Math.round(100 * (t[v] || 0) / t._p), o = C.out[v];
  try { toast(`${pc}% of commanders made the same choice as you: ${o.rec.replace(/\.$/, "").toLowerCase()}.`, "win"); } catch (e) {} }
function storyTick() { try { if (!S || !G.ready || !S.intro || battle || sheet || advLines || G.cineOn || G.storyBusy || $("#celeb") || $("#adv") || (S.tut && S.tut.k !== "done") || G.mode === "connecting") return;
    S.choices = S.choices || {}; S.vk = S.vk || {};
    if (S.choices.warden === "spare" && !S.spareBack && Date.now() - ((S.choiceAt || {}).warden || 0) > 5 * 864e5) { S.spareBack = 1; grantRw({ shards: 50 }, "The Warden's watch"); S.vpTitles = S.vpTitles || []; if (!S.vpTitles.includes("Wardenfriend")) S.vpTitles.push("Wardenfriend"); dirty();
      celebrate({ k: "wardenback", kick: "The Warden you spared", t: "It Came Back", art: "adv", s: "The Warden you let live has taken up a watch over your homeworld. It asks for nothing.", say: STORY_SPARE[0], rw: "◆50 and the title “Wardenfriend”.", go: "Onward" }); return; }
    for (const V of VK_T) if (!S.vk[V.id] && V.when()) { S.vk[V.id] = Date.now(); dirty(); G.storyBusy = 1; cinema(vkBeats(V.q, "Incoming transmission").concat([{ adv: 1, line: V.a }]), { onSkip: () => { G.storyBusy = 0; } }, () => { G.storyBusy = 0; }); return; }
    for (const C of STORY_CH) if (!S.choices[C.id] && C.when()) { storyPlay(C); return; } } catch (e) {} }
setInterval(storyTick, 30000);

/* ---------- the Archives: the Seal Strain and your own chronicle ---------- */
function storyPanel() { const v = G.strain != null ? G.strain : strainNow(), t = storyTally(), c = S.choices || {}, col = v < 25 ? "#6dffb0" : v < 50 ? "#ffd36b" : v < 75 ? "#ff9a4a" : "#ff3b4a";
  const rows = STORY_CH.filter(C => c[C.id]).map(C => { const o = C.out[c[C.id]], tt = t[C.id], pc = tt && tt._p > 1 ? Math.round(100 * (tt[c[C.id]] || 0) / tt._p) : null; return `<li><b>${esc(C.t)}</b><span>${esc(o.rec)}${pc != null ? ` <em>${pc}% of commanders chose the same.</em>` : ""}</span></li>`; });
  return `<div class="strain"><div class="sthd"><b>Seal Strain</b><span style="color:${col}">${v}%</span></div><div class="stbar"><i style="width:${v}%;background:${col}"></i></div>
    <p class="note">Every Titan built and every Warden that falls, anywhere in the galaxy, strains the seals. Cracked seals strain them most. Commanders who spare Wardens and help the Verdant ease it.${v < 25 ? " <b>The seals are holding: +3% production on every world.</b>" : ""}</p>
    <h3 class="chrh">Your chronicle</h3><ul class="chron2"><li><b>The night of the ambush</b><span>Went back for the escape pods.</span></li>${rows.join("")}</ul></div>`; }
/* her moods for the new lines (the Matriarch's are voiced by her own voice) */
;[["Commander, its heart would build us a Titan. But if it dies, its seal weakens. I won't choose for you.", "grave"], ["It's done. We have its heart. I'll log what it cost, even if no one else does.", "grave"],
 ["We leave it be. It watched our ships the whole way out, Commander. I think it knows.", "tender"], ["The Dominion would use it to wake the pyramids. The Verdant would use it to mend the seals. Someone is going to be very disappointed in us.", "playful"],
 ["The Dominion is delighted. They've already started waking a pyramid. I hope they know how to put it back to sleep.", "grave"], ["The Verdant are mending a seal tonight, with our map. It won't make us richer. It might keep us alive.", "warm"],
 ["We keep it. Secrets are safer with us than with either of them. The Syndicate would be proud, Commander. I'm not sure that's a compliment.", "playful"], ["It wants us to answer, Commander. I could. I'm afraid of what answers back.", "tender"],
 ["I answered. For a moment the whole array went quiet. Then something said thank you.", "awe"], ["Buried. It's still calling, just not to us. Thank you, Commander. I wasn't ready.", "tender"],
 ["Good. I've seen what happens to the ones who listen.", "grave"], ["Commander... be careful. Kindness is how she wins.", "grave"], [STORY_SPARE[0], "awe"],
 [STRAIN_SAY[0][1], "grave"], [STRAIN_SAY[1][1], "grave"], [STRAIN_SAY[2][1], "urgent"], [STRAIN_LOW, "warm"],
 ["That was her, Commander. Vael'Khor. She's never spoken to anyone before.", "grave"], ["She wants you to feel guilty. Don't let her choose how you feel.", "fierce"],
 ["She's telling the truth, Commander. That's what frightens me.", "tender"], ["She can feel the strain too. I hate that she's right.", "grave"]].forEach(([l, m]) => { CIN_MOOD[l] = m; });

/* her poses, only in the story scenes: one cut-out figure per mood, chosen line by line, kept while it doesn't change */
const POSE_MOOD = { calm: "explain", tender: "welcome", warm: "welcome", excited: "victory", playful: "victory", urgent: "alarm", fierce: "ready", awe: "cube", grave: "explain" };
const POSE_LINE = { "Your signal was very bright, Commander. I'm afraid something else heard it too.": "alarm", "You went back. Hold on to that, Commander. I think you're the one I've been waiting for.": "salute",
  "The fleet is broken, Commander. Our warships are gone.": "defeated", "Every commander I've ever known gave that order. Every one.": "defeated", "It's done. We have its heart. I'll log what it cost, even if no one else does.": "defeated",
  "Commander... be careful. Kindness is how she wins.": "alarm", "Good. I've seen what happens to the ones who listen.": "ready" };
function cnPose(b) { let m = "calm"; try { m = advMood(b.line); } catch (e) {} const k = b.pose || POSE_LINE[b.line] || POSE_MOOD[m] || "explain"; return `<img class="cnpose${b.choice ? " ch" : ""}" src="art/adv/p_${k}.webp" alt="${ADV}">`; }
