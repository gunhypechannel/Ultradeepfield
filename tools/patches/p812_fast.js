/* ---------- v812 the fast start (owner: "Yes build it all": new players reach their first build in about a minute). Brand-new commanders
   (S.fst) see a shorter opening film (5 of 9 scenes), a shorter prologue (the lance battle and the go-back choice stay; the second battle
   is skipped, its reward and celebration kept), and start building straight away: the two naming steps no longer block, a nudge
   asks for the name after the first buildings, and the rest of the story arrives with the third building. Every line kept is one the
   Advisor already speaks; replays from the Archive still show the full version. ---------- */
const CIN_OPEN_FAST = [CIN_OPEN[0], CIN_OPEN[1], CIN_OPEN[6], CIN_OPEN[7], Object.assign({}, CIN_OPEN[8], { t: 2500 })];
const PRO_A_FAST = [PRO_A[3], PRO_A[7]], PRO_B_FAST = [PRO_B[2]], PRO_BACK_FAST = [PRO_BACK[1], PRO_BACK[4]];
const fsFast = () => !!(S && S.fst && !S.proWin);
cinOpen = function (done) { S.cinSeen = 1; dirty(); cinema((S.fst ? CIN_OPEN_FAST : CIN_OPEN).slice(), { gate: true }, done); };
proPlay = function (replay) { const A = !replay && fsFast() ? PRO_A_FAST : PRO_A; cinema(A.slice(), {}, () => { G.advThen = () => { G.proAfter = () => proPods(replay); try { playBattle(introBattle()); setTimeout(proLance, 2500); } catch (e) { G.proAfter = null; proPods(replay); } }; say(!replay && fsFast() ? [INTRO_PRE[0]] : INTRO_PRE); }); };
proPods = function (replay) { const f = !replay && fsFast(); let jumped = 0; cinema((f ? PRO_B_FAST : PRO_B).slice(), { onChoice: v => v === "jump" && !jumped++ ? PRO_JUMP.slice() : (f ? PRO_BACK_FAST : PRO_BACK).slice(), onSkip: () => proLand(replay) }, () => proLand(replay)); };
{ const land = proLand; proLand = function (replay) { if (replay || !fsFast()) return land(replay); S.proDone = 1; dirty(); try { proWin(replay); } catch (e) {} }; }
{ const win = proWin; proWin = function (replay) { if (replay || !fsFast()) return win(replay); S.proWin = 1; S.fsLore = 1; grantRw({ m: 3000, c: 2000, g: 800, shards: 5 }, "The first defence"); fsSkipNames(); dirty();
    celebrate({ k: "firstwin", kick: "You made it", t: "This World Is Ours", art: "adv", s: "Four hundred colonists, safe on a new world. Time to build them a home.", say: INTRO[0], rw: "3,000 metal, 2,000 crystal, 800 gas and ◆5. Already in your stores.", go: "Let's build" }); }; }
/* the naming steps wait: a fast start begins the Academy at "Build a Metal Extractor" (their rewards are paid now), and the name comes
   back as a nudge once the first buildings stand */
function fsSkipNames() { if (!S || !S.fst || !S.tut || S.tut.i >= 2) return; for (let i = S.tut.i; i < 2; i++) { const rw = TUT[i].rw || {}; for (const k of ["m", "c", "g"]) if (rw[k]) S.res[k] += rw[k]; } S.tut.i = 2; S.tut.open = 0; dirty(); }
setInterval(() => { try { if (!S || !S.fst || !S.proWin || G.cineOn || battle || $("#adv") || $("#celeb")) return;
  if (S.fsLore && S.b.crystalMine >= 1) { S.fsLore = 0; dirty(); say([INTRO_POST[1], INTRO[1], INTRO[2], INTRO[3], PRO_END, PRO_TEASE]); return; }
  if (!S.tutNm && !S.fsNm && S.b.metalMine >= 1 && S.b.solar >= 1) { S.fsNm = 1; dirty(); say(["One more thing, Commander: the galaxy still knows you only as \"Commander\". Tap your portrait at the top any time to choose a name."]); } } catch (e) {} }, 4000);
