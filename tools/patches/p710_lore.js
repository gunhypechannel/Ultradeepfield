/* ---------- v710 the dots joined (owner: "Build it all") ----------
   1. Why the Leviathan turned inward: the Architects' records say it felt the Unmade stir; the Carcinid say it heard its old masters.
      "The Warden's Two Songs" (q_warden): it heard both, because its masters were screaming as they fled the thing beneath the Abyss.
   2. The Crown surfaces the same Wednesday Cube Devastation (Chapter 2) begins: the Advisor names it (crown_dv), and again when the Omega
      Cube erupts while the Crown lives (crown_erupt).
   3. The first omen's "something vast outside the wall" is paid off: it was the Abyssal Crown, testing the wall a year early (q_shadow).
   4. The tide opens with a "Previously" (on its screen and in her voice), and the Leviathan's fate is told as week 2 opens.
   5. February links to May: Omega's vault speaks with the voice that answered the Crown (q_vault, the Cube Codex).
   6. A year on: when the Leviathan returns she remembers how last year's hunt ended, and an escaped Crown is announced as the tide opens. */
Object.assign(CRC_SAY, {
  prev_held: "Previously: we brought the Leviathan down at the wall. But the breach it made never closed, and something is coming through.",
  prev_cracked: "Previously: the Leviathan broke the wall and escaped into the dark. The breach never closed, and something is coming through.",
  crown_dv: "Commander, the Crown surfaced on the same day the Cubes began to gather. That's no accident. Everything from the deep is drawn to the Omega Cube.",
  crown_erupt: "The Omega Cube just erupted, and the Crown cried out with it. They're answering the same thing, Commander.",
  crown_back: "Commander, the Crown that escaped us last year is back. Its shell is harder now, and so is Korvax's.",
  y2_held: "A year ago we brought the Leviathan down at the wall. It's back, Commander. The Wardens don't stay dead.",
  y2_cracked: "A year ago the Leviathan broke the wall and escaped us. It's back, Commander, and it remembers the way through." });
/* each week opens with her lines, spaced out: week 1 recaps the wall, week 2 tells the Leviathan's fate */
crcWeekSay = function () { if (!S || !G.ready || battle || G.cineOn || document.getElementById("omcine") || (typeof tutOn === "function" && tutOn())) return; const T = now(), w = crcWeek(T); if (w < 1 || w > 4) return; const M = crcS(); M.ws = M.ws || {}; if (M.ws[w]) return; M.ws[w] = 1; dirty();
  const dead = crcLevFate(T) === "dead", q = [];
  if (w === 1) { q.push(CRC_SAY[dead ? "prev_held" : "prev_cracked"], CRC_SAY.week_1); if (CRC_BOSS.cc && CRC_BOSS.cc.hp > 400) q.push(CRC_SAY.crown_back); }
  else if (w === 2) { q.push(CRC_SAY.week_2); if (!M.levSaid) { M.levSaid = 1; q.push(CRC_SAY[dead ? "lev_held" : "lev_cracked"]); } }
  else q.push(CRC_SAY[w === 4 ? (dead ? "week_4d" : "week_4a") : "week_" + w]);
  q.forEach((t, i) => setTimeout(() => { try { sbSay(t); } catch (e) {} }, i * 14000)); };
crcStoryTick = function () { if (!S || !G.ready || battle || G.cineOn || document.getElementById("omcine")) return; const T = now(), w = crcWeek(T), M = crcS();
  const out = crcYearOutcome(T), pk = String(crcT0(T) - 10 * VP_LEN); if (out === "esc" && T - (+pk + CRC_LEN) < 7 * 864e5) { S.crcEnd = S.crcEnd || {}; if (!S.crcEnd[pk]) { S.crcEnd[pk] = 1; dirty(); crcCine("esc"); return; } }
  /* the Crown and the Omega Cube, the same week */
  if (w === 4 && crcClock(T).e >= CRC_CROWN0) { let C = null, D = null; try { C = crcStC(T).b.cc; D = dvNow(T); } catch (e) {} if (C && !C.dead && D) { const er = D.e >= DV.erupt, fresh = er && D.e - DV.erupt < 3 * 3600e3; /* "just erupted" only while it is fresh */ if (!M.dvSay) { M.dvSay = 1; if (er) M.dvErupt = 1; dirty(); sbSay(CRC_SAY[fresh ? "crown_erupt" : "crown_dv"]); return; } if (er && !M.dvErupt) { M.dvErupt = 1; dirty(); if (fresh) { sbSay(CRC_SAY.crown_erupt); return; } } } }
  /* a year on: the Leviathan returns to the wall */
  const si = vpSeason(T); if (si >= PRO + 10 && seaCyc(si) === 0) { S.levYr = S.levYr || {}; if (!S.levYr[si]) { let o = null; try { const s0 = finLast("lev", T); if (s0 != null) o = finOutcome("lev", s0, T); } catch (e) {} S.levYr[si] = 1; dirty(); setTimeout(() => { try { sbSay(CRC_SAY[o === "held" ? "y2_held" : "y2_cracked"]); } catch (e) {} }, 8000); } } };
/* the new records */
Object.assign(ARCH, {
  q_shadow: { cat: "tide", t: "The Shadow at the Wall", era: "The prologue, a year before the tide", civ: "The Carcinid", loc: "Outside the Architects' outer wall", img: "art/carcinid/s_citadel.webp", th: "Extreme",
    frag: "We pressed our shell against the wall, and the wall grew warm, and the beast inside it turned to look.",
    interp: "In the first omen, fire ran along the Rim and something vast passed outside the wall. It was the Abyssal Crown. A year before the tide, it was already pressing against the Architects' wall, searching for a way through, and the Warden inside turned to watch it.",
    adv: "We saw it in the prologue, Commander, and we called it an omen. It was the Crown, testing the wall.",
    enc: ["Commander, the Carcinid charts mark our Rim in fire. The fire from our first omen. They were the ones who lit it."], def: ["The fire at the Rim was the Crown's shell, scraping the wall.", "It was knocking, Commander. And the Leviathan answered the door."] },
  q_warden: { cat: "tide", t: "The Warden's Two Songs", era: "Chapter 1", civ: "The Leviathan", loc: "The Architects' outer wall", img: "art/arch/lev.webp", th: "Extreme",
    frag: "Below it, the floor began to breathe. Beyond it, its old masters began to scream. It turned toward both.",
    interp: "The Leviathan heard two things at once. Beneath the Abyss, the Unmade stirring at the prison's floor. Beyond the wall, the Carcinid who bred it, screaming as they fled. It turned inward to reach the door, and its masters followed the path it broke.",
    adv: "The Architects' records and the Carcinid's both tell the truth, Commander. It heard the thing below, and it heard its masters running from it.",
    enc: ["Commander, I've laid the Architects' warden logs beside the Carcinid war-songs. They describe the same night."], def: ["The Leviathan wasn't choosing between them, Commander.", "The Warden and its masters were both answering the same thing."] },
  q_vault: { cat: "cube", t: "The Voice in the Vault", era: "Chapter 5", civ: "Omega", loc: "Beneath the Cube network", img: "art/mimic/nexus.webp", th: "Catastrophic",
    frag: "Down in the vault the prisoner whispers, and its words are the ones the Crown heard. The Abyss remembers.",
    interp: "When Omega stirred in its vault, the Cube network carried its whisper across the galaxy. It was speaking in the voice that answered the Abyssal Crown. Omega isn't the Unmade, but it has lain beside the prison's floor for an age, listening, and it has learned to speak for it.",
    adv: "We heard that voice under the Abyss, Commander. Now it's under the Cubes. Whatever it is, it's beneath everything we stand on.",
    enc: ["Commander, the Cube network is carrying a whisper. I've heard it before. When the Crown died."], def: ["Omega has been listening to the floor of the prison for a very long time, Commander.", "It learned the voice. That's what frightens me. It learned it."] } });
ARCH_ORD.splice(Math.max(0, ARCH_ORD.indexOf("q_abyss")), 0, "q_shadow", "q_warden"); ARCH_ORD.push("q_vault");
function loreArchTick() { if (!S || !G.ready || battle || G.cineOn || document.getElementById("omcine")) return true; const T = now(), w = crcWeek(T), M = crcS(), kills = (M.kills || []).reduce((a, b) => a + b, 0), crown = w >= 4 && crcClock(T).e >= CRC_CROWN0;
  let omega = false; try { const s0 = finLast("krk", T); omega = s0 != null && T - s0 < 40 * 864e5; } catch (e) {} const si0 = vpSeason(T), mim = seaCyc(si0) === 4; if (mim && T >= VP_BASE + si0 * VP_LEN + 26 * 864e5) omega = true; /* the Omega finale is that Saturday */
  const want = [["q_warden", w >= 1 && w <= 5, w >= 1 && w <= 5 && kills >= 3], ["q_shadow", w >= 1 && w <= 5 && kills >= 2, crown], ["q_vault", mim, omega]];
  for (const [k, a, b] of want) { const lv = archLv(k); if (b && lv < 2) { archUnlock(k, 2); return true; } if (a && lv < 1) { archUnlock(k, 1); return true; } } return false; }
/* one unlock at a time across both lists, so no two records speak over each other */
{ const crcArchTick0 = crcArchTick; crcArchTick = function () { try { if (loreArchTick()) return; } catch (e) {} crcArchTick0(); }; }
