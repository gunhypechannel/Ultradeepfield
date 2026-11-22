/* ---------- v706 the story, rounded out (owner: "Do everything that will round out and perfect this story, i want the story and the order to make sense") ----------
   - The Carcinid tide belongs to the year now: the Leviathan's hunt decides what Korvax rides, the Crown can win (escape), and its ending
     is weighed by the Judge (one held seal fewer) and the Seal Strain, and hardens next year's tide.
   - The Tide of the Carcinid in the Archives: eight records that open as the tide unfolds, ending with what answered the Crown.
   - The Kraken's own record ("The Many-Armed Deep") can be found again: the wild Kraken is back.
   - The Advisor ties the Leviathan's hunt to the tide, and opens week 4 with what Korvax is riding. */
Object.assign(CRC_SAY, {
  lev_held: "The Leviathan is dead, Commander. And the Carcinid are already dragging its body into the Breach.",
  lev_cracked: "The Leviathan fled toward the Breach Zones. The Carcinid are calling it home, Commander.",
  week_4a: "Korvax has the Leviathan in chains, Commander. The beast we couldn't stop is his now. And the Crown is rising to molt.",
  week_4d: "Korvax is riding the Leviathan's corpse into battle. Even dead, it still sings for them. And the Crown is rising to molt.",
  cine_esc: "It got away, Commander. Reborn, and stronger. The Judge saw that. And next year, the tide will come back harder." });
/* week 4 opens with what Korvax rides */
crcWeekSay = function () { if (!S || !G.ready || battle || G.cineOn || document.getElementById("omcine") || (typeof tutOn === "function" && tutOn())) return; const T = now(), w = crcWeek(T); if (w < 1 || w > 4) return; const M = crcS(); M.ws = M.ws || {}; if (M.ws[w]) return; M.ws[w] = 1; dirty();
  try { sbSay(CRC_SAY[w === 4 ? (crcLevFate(T) === "dead" ? "week_4d" : "week_4a") : "week_" + w]); } catch (e) {} };
/* how this year's tide ended (the run before the next one): "win", "esc" or null */
function crcYearOutcome(T) { try { const t0 = crcT0(T), pk = String(t0 - 10 * VP_LEN); if (+pk < VP_BASE + PRO * VP_LEN) return null; const src = G.mode === "online" ? (G.crcDoc || {})["event/carcinid"] : ((S && S.ldb) || {})["event/carcinid"];
    if (!src) return null; if (src.k === pk && src.b && src.b.cc) return T >= +pk + CRC_LEN ? (src.b.cc.dead ? "win" : "esc") : null; return (src.hist || {})[pk] || null; } catch (e) { return null; } }
/* the Archives */
ARCH_CAT.push(["tide", "The Tide of the Carcinid", "The Abyssal Empire, the sea beyond the wall, and what it was fleeing."]);
Object.assign(ARCH, {
  q_abyss: { cat: "tide", t: "The Abyss", era: "Before the Architects", civ: "The Carcinid Abyssal Empire", loc: "Beyond the outer wall", img: "art/carcinid/s_tide.webp", th: "Extreme",
    frag: "…below the last light there is a sea, and below the sea there is a floor, and below the floor something is breathing…",
    interp: "The Abyss lies beyond the Architects' outer wall: a sea of dark matter that runs all the way down to the prison's floor. The Carcinid ruled it long before the Wardens were made.",
    adv: "A sea with a floor that breathes. I don't like where that floor is, Commander.",
    enc: ["Commander, the first Breach is closed. There was water on the other side. Water, in space."], def: ["I've mapped the water that came through, Commander.", "It's very old. And it's warm, as if something under it is alive."] },
  q_empire: { cat: "tide", t: "The Abyssal Empire", era: "Before the Architects", civ: "The Carcinid", loc: "The Abyss", img: "art/carcinid/s_skullcity.webp", th: "Extreme",
    frag: "We bred the deep beasts and rode them to the edge of everything. Then the builders came, and took the greatest of them for their wall.",
    interp: "The Carcinid bred the Kraken and the Leviathan as war mounts. When the Architects built their prison, they took the Leviathan from them and made it the Warden of their outer wall.",
    adv: "The Leviathan was theirs, Commander. That's half of why it turned inward. It heard them calling it home.",
    enc: ["Commander, the patrol we sank was carrying records. Star charts. Of our worlds."], def: ["I've translated the patrol's records.", "They aren't invasion plans, Commander. They're evacuation routes."] },
  q_kraken: { cat: "tide", t: "The Kraken Returns", era: "This tide", civ: "The deep", loc: "The deep layers", img: "art/mon/kraken.webp", th: "Extreme",
    frag: "The light rose out of the deep in a ring, and the ring was arms.",
    interp: "The Kraken we saw rising in the omens has come back with the Carcinid tide. It was their war-beast once. Now it answers to no one, and its death-cry breaks the war-song that drives Korvax's fleet.",
    adv: "We saw it in the omens, Commander. Pillars of light in a ring. I told you they were arms.",
    enc: ["Commander, the Kraken is dead. Its song just stopped, and Korvax's fleet faltered when it did."], def: ["Another Kraken down.", "They keep rising from the deep, Commander. Not toward us. Away from something."] },
  q_admirals: { cat: "tide", t: "The Claw Admirals", era: "This tide", civ: "The Carcinid", loc: "The Breach Zones", img: "art/carcinid/marshal.webp", th: "Extreme",
    frag: "Five claws on one hand. When the hand closes, nothing escapes it.",
    interp: "The Empire's five Claw Admirals each command a tide: the Red Claw Marshal its vanguard, the Pearl Matron its broods, the Reef Tyrant its fortresses, the Trench Oracle its seers, and Dread Admiral Korvax all of them.",
    adv: "Every admiral we bring down, the tide behind them falters. They lead from the front. I almost respect that.",
    enc: ["Commander, a Claw Admiral has taken the field. The whole brood moves with it."], def: ["A Claw Admiral is dead, Commander.", "Its brood didn't scatter. They went quiet, like they were listening for orders from somewhere deeper."] },
  q_guard: { cat: "tide", t: "The Deep Guardians", era: "Older than the Wardens", civ: "The Abyss", loc: "The deep layers", img: "art/carcinid/s_reefcity.webp", th: "Catastrophic",
    frag: "Cities on their backs, kings in their cities, and none of them remember a time before the guardians walked.",
    interp: "The Trench Behemoth, the Krakenbreaker and the Pale Sovereign are the oldest living things in the Abyss. Whole Carcinid cities were built on their shells, and they walked the sea floor for longer than the Wardens have existed.",
    adv: "They aren't attacking us, Commander. They're climbing. Whatever is down there, even they want to get away from it.",
    enc: ["Commander, something enormous is rising from the deep layers. There's a city on its back."], def: ["A Deep Guardian has fallen.", "The city on its back was empty, Commander. Everyone had already left."] },
  q_korvax: { cat: "tide", t: "Korvax and the Leviathan", era: "This tide", civ: "The Carcinid", loc: "The heart of the Breach", img: "art/carcinid/korvax.webp", th: "Catastrophic",
    frag: "The wall-beast was ours before it was theirs. Alive or dead, it will carry us home.",
    interp: "Dread Admiral Korvax commands every claw of the Empire. He has claimed the Leviathan for himself: chained and alive if it escaped its hunt, its corpse if we slew it. Its war-song is his strength.",
    adv: "He's riding the Warden of the wall into battle, Commander. Whatever we did to it at the wall, he made it his.",
    enc: ["Commander, Dread Admiral Korvax has taken the field. He's riding the Leviathan."], def: ["Korvax is dead, Commander.", "With his last breath he wasn't calling his fleet. He was calling the Crown."] },
  q_crown: { cat: "tide", t: "The Abyssal Crown", era: "Every age", civ: "The Carcinid", loc: "The heart of the galaxy", img: "art/carcinid/s_crownship.webp", th: "Catastrophic",
    frag: "Each molt, a new Crown. Each Crown, the same mind. It has been shedding its shell since before there were stars.",
    interp: "The Abyssal Crown is the Empire's emperor: a crab the size of a moon, with a city on its back. It molts to be reborn. If it completes its molt on this side of the wall, the Empire is reborn here, with it.",
    adv: "It isn't here to conquer us, Commander. It's here to be born somewhere safer than the Abyss. Here.",
    enc: ["Commander, the Abyssal Crown has surfaced. The Great Molting has begun."], def: ["The Crown's tide is over, Commander.", "Whichever way it ended, the Judge was watching."] },
  q_answer: { cat: "tide", t: "What Answered", era: "After the tide", civ: "Unknown", loc: "Beneath the Abyss", img: "art/carcinid/s_moon.webp", th: "Unknown",
    frag: "THE ABYSS REMEMBERS WHAT THE STARS HAVE FORGOTTEN.",
    interp: "The Crown's last cry was answered from far beneath the Abyss, from the prison's floor. The Carcinid were never invading. They were fleeing the same thing every Warden guards: the Unmade, stirring below the deep.",
    adv: "Everything that lives in the deep is running toward us, Commander. Not to fight us. To get away. That should frighten us more than any claw.",
    enc: ["Commander, something answered the Crown. From below the Abyss."], def: ["I've listened to the answer a hundred times, Commander.", "It's the same voice as the black hole. The Unmade is underneath everything."] } });
ARCH_ORD.push("q_abyss", "q_empire", "q_kraken", "q_admirals", "q_guard", "q_korvax", "q_crown", "q_answer");
if (!ARCH_ORD.includes("krk")) ARCH_ORD.splice(Math.max(0, ARCH_ORD.indexOf("lev") + 1), 0, "krk"); /* the Kraken is back: its record can be found again */
/* the tide's records open as it unfolds (one at a time, so each gets its moment) */
function crcArchTick() { if (!S || !G.ready || battle || G.cineOn || document.getElementById("omcine")) return; const T = now(), w = crcWeek(T), M = crcS(), st = crcStC(T), e = crcClock(T).e, K = S.crcKrk || {}, dead = id => !!(st.b[id] && st.b[id].dead);
  const kills = (M.kills || []).reduce((a, b) => a + b, 0), out = crcYearOutcome(T), C = st.b.cc;
  const want = [["q_abyss", kills >= 1, kills >= 5], ["q_empire", (M.pat || 0) >= 1, (M.pat || 0) >= 3], ["q_kraken", (K.n || 0) >= 1, (K.n || 0) >= 2], ["krk", (K.n || 0) >= 1, (K.n || 0) >= 2],
    ["q_admirals", w >= 2 && w <= 5, ["ca0", "ca1", "ca2", "ca3", "ca4"].some(dead)], ["q_guard", w >= 3 && w <= 5, ["cg0", "cg1", "cg2"].some(dead)], ["q_korvax", w >= 4 && w <= 5, dead("ca4")],
    ["q_crown", e >= CRC_CROWN0 || !!out, !!(C && C.dead) || !!out], ["q_answer", !!(C && C.dead) || !!out, !!(C && C.dead) || !!out]];
  for (const [k, a, b] of want) { const lv = archLv(k); if (b && lv < 2) { archUnlock(k, 2); return; } if (a && lv < 1) { archUnlock(k, 1); return; } } }
/* the Leviathan's hunt, told as part of the tide; and the Crown's escape, once, when the tide ends without its death */
function crcStoryTick() { if (!S || !G.ready || battle || G.cineOn || document.getElementById("omcine")) return; const T = now(), w = crcWeek(T);
  if (w >= 1 && w <= 2) { const M = crcS(); if (!M.levSaid) { let o = null; try { const s0 = finLast("lev", T); if (s0 != null && T - s0 < 45 * 864e5) o = finOutcome("lev", s0, T); } catch (e) {} if (o) { M.levSaid = o; dirty(); setTimeout(() => { try { sbSay(CRC_SAY[o === "held" ? "lev_held" : "lev_cracked"]); } catch (e) {} }, 22000); } } }
  const out = crcYearOutcome(T), pk = String(crcT0(T) - 10 * VP_LEN); if (out === "esc" && T - (+pk + CRC_LEN) < 7 * 864e5) { S.crcEnd = S.crcEnd || {}; if (!S.crcEnd[pk]) { S.crcEnd[pk] = 1; dirty(); crcCine("esc"); } } }
setInterval(() => { try { crcStoryTick(); crcArchTick(); } catch (e) {} }, 15000);
