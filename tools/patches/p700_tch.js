/* ---------- v700 the Titan Chronicles (owner: "make all titans especially the eclipse harbinger a deep part of the story" ... "Do it all") ----------
   Three five-chapter stories in the Archives, one per Titan, unlocked by flying them, plus a finale. Armageddon: the six Warden hearts
   were given, not taken. The Sovereign Ark: the last Concord admiral lives on in its Uplink, woven the same way as the Advisor. The
   Eclipse Harbinger: the Unmade drew its plans, a ship it could leave the prison in; the Wyrm swallowed them to hide them. Its last
   chapter is a choice: Bind it (1 Titan Core: its damage -10%, the Seal Strain eases) or Awaken it (its damage +15%, the Seal Strain
   rises, the Judge names you at the Eclipse). Chapters open in order; each is ◆ like any record, and the shelf completes a collection. */
const TCH_K = { a: "armageddon", s: "sovereign", h: "harbinger" }, TCH_N = { armageddon: "Armageddon", sovereign: "Sovereign Ark", harbinger: "Eclipse Harbinger" };
const TCH_BIND = "It's quiet now. I hope that's sleep and not patience.", TCH_WAKE = "It's awake. I can hear it humming, Commander. It sounds almost grateful.", TCH_JUDGE = "The Judge spoke your name, Commander. He knows we woke the Harbinger.";
const TCH_ASK = "I could seal its reactor with a Warden's heart. It would be quieter. Weaker. Or we let it wake and use what it is. I won't choose for you. I only ask that you choose knowing.";
Object.assign(ARCH, {
  t_a1: { cat: "titan", t: "Six Hearts", era: "The Covenant · 1", civ: "Concord siege yards", loc: "The Armageddon's spine", img: null, th: "Armageddon", hint: "Commission an Armageddon",
    frag: "Foundry log, Concord siege yards. Six hearts received, sealed into the spine in the order they arrived. Devourer. Leviathan. Kraken. Colossus. Wyrm. Tyrant. All six were still warm.",
    interp: "Every Armageddon carries the hearts of six Wardens, the guardians the Architects left at the prison's doors. The yards logged them as power cells. The crews never called them that.", adv: "Six hearts, Commander. I keep wanting to call them parts. I can't.", enc: [], def: [] },
  t_a2: { cat: "titan", t: "The Voice in the Cannon", era: "The Covenant · 2", civ: "Concord gunnery reports", loc: "The Worldbreaker Cannon", img: null, th: "Armageddon", hint: "Fight 10 battles with an Armageddon",
    frag: "Gunnery report. The charge hum carries a pattern. The linguists matched it to Warden glyphs. It is one word, repeated: hold.",
    interp: "Each time the Worldbreaker Cannon charges, the six hearts answer in the Wardens' old tongue. Always the same word, as if they were still at their posts.", adv: "Every time it fires, they say the same thing. Hold. Hold what, Commander?", enc: [], def: [] },
  t_a3: { cat: "titan", t: "The Leviathan Lowered Its Head", era: "The Covenant · 3", civ: "A memory in the Leviathan's heart", loc: "The galaxy's edge", img: null, th: "Armageddon", hint: "Fight a world boss with an Armageddon in your fleet",
    frag: "Recovered from the Leviathan's heart: the first Concord admiral met it at the edge of the galaxy. It looked at her for a long time. Then it lowered its head and let the fleet pass.",
    interp: "The Wardens were never mindless. The memory shows a choice: the Leviathan judged the Concord, and let it live.", adv: "It could have swallowed that fleet whole. It chose not to. I think it was waiting for someone.", enc: [], def: [] },
  t_a4: { cat: "titan", t: "The Covenant", era: "The Covenant · 4", civ: "An Architect tablet", loc: "Beneath the first pyramid", img: null, th: "Armageddon", hint: "Fight 25 battles with an Armageddon",
    frag: "When the seals grow thin, a Warden may give its heart to the one who will stand at the door. It is not taken. It is given.",
    interp: "This is why a Titan Core only comes from facing a Warden. The hearts in every Armageddon were offered to commanders the Wardens judged ready.", adv: "We didn't steal their hearts, Commander. They gave them to us. That's worse, somehow. Now we owe them.", enc: [], def: [] },
  t_a5: { cat: "titan", t: "What They Guard", era: "The Covenant · 5", civ: "The six hearts, together", loc: "Before the Cube", img: null, th: "Armageddon", hint: "Fight in the Battle for the Cube with an Armageddon",
    frag: "For the first time all six voices spoke together: The door is behind you. Do not turn around.",
    interp: "Brought before the Cube, the six hearts stopped saying hold and gave a warning. Whatever they guarded is still there, and it is behind us.", adv: "They aren't trapped in our cannon. They're standing guard in it. Still.", enc: [], def: [] },
  t_s1: { cat: "titan", t: "The Empty Throne", era: "The Crown · 1", civ: "The Concord imperial yards", loc: "The Sovereign Ark's bridge", img: null, th: "Sovereign Ark", hint: "Commission a Sovereign Ark",
    frag: "The Ark was built around a command throne. The Uplink rejects every captain who sits in it. The yards call it the Empty Throne.",
    interp: "No captain has ever held the Ark's throne. The Uplink refuses them all, as if the seat were already occupied.", adv: "It won't take a captain. I think the seat's already taken, Commander.", enc: [], def: [] },
  t_s2: { cat: "titan", t: "An Extra Voice", era: "The Crown · 2", civ: "Fleet communications", loc: "The Fleet Command Uplink", img: null, th: "Sovereign Ark", hint: "Win 10 battles with a Sovereign Ark",
    frag: "Fleet comms log an extra voice giving orders a heartbeat before ours. They are always right.",
    interp: "Under the Ark's command, every fleet hears a second voice. It knows the battle before it happens.", adv: "Someone in the Uplink is helping us fight. I'd like to know who.", enc: [], def: [] },
  t_s3: { cat: "titan", t: "Admiral Ceren Ostrava", era: "The Crown · 3", civ: "The Concord fleet roll", loc: "The last Eclipse", img: null, th: "Sovereign Ark", hint: "Fight 25 battles with a Sovereign Ark",
    frag: "Last Concord admiral. At the last Eclipse she held the line while the fleet escaped. When her flagship died, the Uplink caught her. She has been holding the line ever since.",
    interp: "The voice in the Uplink has a name. Admiral Ostrava never left her post; her mind was folded into the Ark that now commands our fleets.", adv: "She never stopped fighting. Not even when there was nothing left of her but the fight.", enc: [], def: [] },
  t_s4: { cat: "titan", t: "The Same Weave", era: "The Crown · 4", civ: "An Uplink diagnostic", loc: "The Uplink lattice", img: null, th: "Sovereign Ark", hint: "Win a joint strike with a Sovereign Ark",
    frag: "The Uplink's lattice is Architect work, the same weave that holds the pyramid minds.",
    interp: "The Concord didn't invent the Uplink. They copied it from the Architects, the same weave that holds the Advisor.", adv: "Commander, the Uplink is built the way I am. She and I are... cousins, I suppose. I didn't know there were others.", enc: [], def: [] },
  t_s5: { cat: "titan", t: "The Promise", era: "The Crown · 5", civ: "Admiral Ostrava", loc: "A message in the Uplink", img: null, th: "Sovereign Ark", hint: "Fight in a joint strike of 10 or more commanders with a Sovereign Ark",
    frag: "When the dark comes again, no commander faces it alone. Keep that promise for me.",
    interp: "The admiral's last order, left for whoever would command after her. It is the oldest promise in the Concord.", adv: "She kept that promise for a thousand years. I'd like to help her keep it a little longer.", enc: [], def: [] },
  t_h1: { cat: "titan", t: "Beneath the Wyrm", era: "The Imitation · 1", civ: "Concord salvage teams", loc: "The Event Horizon Wyrm's corpse", img: null, th: "Eclipse Harbinger", hint: "Commission an Eclipse Harbinger",
    frag: "The schematics were found inside the Event Horizon Wyrm's corpse, etched in a material that does not reflect light. The Wyrm had swallowed them.",
    interp: "The Harbinger's plans came out of a Warden. Not guarded by it: hidden inside it, where no one was meant to find them.", adv: "Wardens don't eat, Commander. It swallowed those plans to hide them. From us.", enc: [], def: [] },
  t_h2: { cat: "titan", t: "The Heartbeat", era: "The Imitation · 2", civ: "Reactor telemetry", loc: "The emerald reactor", img: null, th: "Eclipse Harbinger", hint: "Fight 10 battles with an Eclipse Harbinger",
    frag: "The reactor's rhythm matches the Void's exactly, including the pauses. It does not follow the Void. It beats a moment ahead.",
    interp: "The Harbinger's reactor is not echoing the black hole at the galaxy's heart. It is keeping time for it.", adv: "It isn't echoing the Void. It's keeping time for it.", enc: [], def: [] },
  t_h3: { cat: "titan", t: "The Drones Hesitate", era: "The Imitation · 3", civ: "Swarm telemetry", loc: "The Neural Drone Swarm", img: null, th: "Eclipse Harbinger", hint: "Fight 25 battles with an Eclipse Harbinger",
    frag: "Telemetry: before each order the drones hold for 0.4 seconds, listening. They are waiting for a second command. Ours is not the only voice they hear.",
    interp: "The swarm obeys us, but only after it has listened for someone else.", adv: "Commander, the drones are waiting for permission. And not from you.", enc: [], def: [] },
  t_h4: { cat: "titan", t: "Who Drew the Plans", era: "The Imitation · 4", civ: "An analysis of the last Eclipse", loc: "The shadow at the Eclipse's centre", img: null, th: "Eclipse Harbinger", hint: "Fight a world boss with an Eclipse Harbinger in your fleet",
    frag: "Laid over a recording of the last Eclipse, the schematic matches the shadow at its centre line for line. The Harbinger was not designed by anyone in this galaxy. It is a door that can walk.",
    interp: "The Unmade drew the Harbinger: a vessel it could leave the prison in. The Wyrm hid the plans. We found them, and we built it.", adv: "The Unmade drew it, Commander. It drew a ship it could leave in. And we built it.", enc: [], def: [] },
  t_h5: { cat: "titan", t: "Bind or Awaken", era: "The Imitation · 5", civ: "Your choice", loc: "The Harbinger's reactor", img: null, th: "Eclipse Harbinger", hint: "Recover \"Who Drew the Plans\", then make your choice",
    frag: "The reactor is listening. It can be sealed with a Warden's heart, or it can be let wake.",
    interp: "", adv: "", enc: [], def: [] },
  t_fin: { cat: "titan", t: "The Three Answers", era: "Keeper of the Titans", civ: "The Advisor's own record", loc: "The Titan Chronicles", img: null, th: "All three Titans", hint: "Complete all three Titan chronicles",
    frag: "Force, unity, and the enemy's own weapon. The Architects tried the first two and they were not enough. Perhaps that is why someone left us the third.",
    interp: "The Armageddon carries the Wardens' gift, the Sovereign Ark the Concord's promise, and the Harbinger the Unmade's own design. Three answers to the same dark.", adv: "Three answers to the same dark, Commander. I don't know which one is right. I'm glad it's you holding all three.", enc: [], def: [] } });
Object.defineProperties(ARCH.t_h5, { /* the last chapter reads as you chose (getters: Object.assign would freeze them) */
  interp: { configurable: true, enumerable: true, get() { const c = S && S.choices && S.choices.harb; return c === "bind" ? "You sealed the reactor with a Warden's heart. The Harbinger is quieter and weaker (its damage -10%), and the Seal Strain eases." : c === "wake" ? "You let it wake. The Harbinger hits harder (its damage +15%), the Seal Strain rises, and the Judge will know at the Eclipse." : "The choice is still open."; } },
  adv: { configurable: true, enumerable: true, get() { const c = S && S.choices && S.choices.harb; return c === "bind" ? TCH_BIND : c === "wake" ? TCH_WAKE : TCH_ASK; } } });
ARCH_CAT.push(["titan", "The Titan Chronicles", "The three Titans and what lives inside them. Each chapter opens as you fly them."]);
const TCH_ORD = ["t_a1", "t_a2", "t_a3", "t_a4", "t_a5", "t_s1", "t_s2", "t_s3", "t_s4", "t_s5", "t_h1", "t_h2", "t_h3", "t_h4", "t_h5", "t_fin"]; ARCH_ORD.push(...TCH_ORD);
const tchHarbK = () => { const c = S && S.choices && S.choices.harb; return c === "wake" ? 1.15 : c === "bind" ? .9 : 1; };
/* what each battle report adds: battles fought and won with each Titan, world bosses, the Cube, joint strikes */
function tchRep(rep) { try { if (!S || !rep || !rep.sim || rep.test || rep.demo || rep.lab) return; const T = S.tch || (S.tch = { n: {}, seen: [] }); if (T.seen.includes(rep.id)) return; T.seen.push(rep.id); if (T.seen.length > 60) T.seen.splice(0, T.seen.length - 60);
  const dSide = rep.kind === "defense" || rep.kind === "raid", mine = (dSide ? rep.sim.D : rep.sim.A) || [], won = rep.winner === (dSide ? "d" : "a"), U = rep.aUids || [];
  const boss = !!(rep.wb || rep.sbk || rep.omega || rep.boss), cube = /\bCube\b/.test(rep.title || "") || /Cube|Collective Warden/.test(rep.dName || "");
  for (const k of Object.values(TCH_K)) { if (!mine.some(x => x && x[0] === k && (x[5] === G.me || x[5] == null) && x[1] > 0)) continue; const n = T.n;
    n[k + "B"] = (n[k + "B"] || 0) + 1; if (won) n[k + "W"] = (n[k + "W"] || 0) + 1; if (boss) n[k + "Boss"] = 1; if (cube) n[k + "Cube"] = 1; if (U.length > 1 && won) n[k + "JW"] = 1; if (U.length >= 10) n[k + "J10"] = 1; }
  dirty(); tchCheck(); } catch (e) {} }
function tchCheck() { if (!S || !G.ready) return; const n = (S.tch && S.tch.n) || {}, has = k => { try { return own(k) > 0 || (n[k + "B"] || 0) > 0; } catch (e) { return (n[k + "B"] || 0) > 0; } };
  const W = { t_a1: has("armageddon"), t_a2: (n.armageddonB || 0) >= 10, t_a3: !!n.armageddonBoss, t_a4: (n.armageddonB || 0) >= 25, t_a5: !!n.armageddonCube,
    t_s1: has("sovereign"), t_s2: (n.sovereignW || 0) >= 10, t_s3: (n.sovereignB || 0) >= 25, t_s4: !!n.sovereignJW, t_s5: !!n.sovereignJ10,
    t_h1: has("harbinger"), t_h2: (n.harbingerB || 0) >= 10, t_h3: (n.harbingerB || 0) >= 25, t_h4: !!n.harbingerBoss };
  for (const p of ["a", "s", "h"]) for (let i = 1; i <= 5; i++) { const k = `t_${p}${i}`; if (archLv(k) >= 2) continue; if (i > 1 && archLv(`t_${p}${i - 1}`) < 2) break;
    if (k === "t_h5") { if (archLv(k) < 1) archUnlock(k, 1); else if (S.choices && S.choices.harb) archUnlock(k, 2); break; }
    if (!W[k]) break; archUnlock(k, 2); S.say = S.say || []; S.say.push(ARCH[k].adv); try { flushSay(); } catch (e) {} break; }
  if (archLv("t_fin") < 2 && TCH_ORD.slice(0, 15).every(k => archLv(k) >= 2)) { archUnlock("t_fin", 2); S.say.push(ARCH.t_fin.adv); try { flushSay(); } catch (e) {} } }
setInterval(() => { try { tchCheck(); } catch (e) {} }, 12000);
/* the choice page (Archives › Titan Chronicles › Bind or Awaken) */
function tchChoiceHTML() { const E = ARCH.t_h5, tc = S.tcore || 0;
  return `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter" style="color:#e2c48a">The Titan Chronicles</div><h2>${esc(E.t)}</h2><p class="note">${esc(E.era)} · the Eclipse Harbinger</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
    <div class="arfrag"><small>Fragment of the original record</small><p>${esc(E.frag)}</p></div><div class="aradv"><img src="${advArt()}" style="${advFx()}" alt=""><p><b>${ADV}</b>${esc(TCH_ASK)}</p></div>
    <div class="tchch"><button class="tchb bind" data-act="tchChoose" data-v="bind" ${tc >= 1 ? "" : "disabled"}><b>Bind it</b><small>Seal the reactor with a Warden's heart · costs 1 Titan Core ⬢ (you have ${tc})</small><span>Harbinger damage −10% · the Seal Strain eases</span></button>
    <button class="tchb wake" data-act="tchChoose" data-v="wake"><b>Awaken it</b><small>Let it wake and use what it is</small><span>Harbinger damage +15% · the Seal Strain rises · the Judge will know</span></button></div><p class="note">This choice is permanent.</p>`; }
function tchChoose(v) { if (!S || (S.choices && S.choices.harb) || !(v === "bind" || v === "wake") || archLv("t_h5") < 1) return; if (v === "bind") { if ((S.tcore || 0) < 1) return toast("Binding it takes a Titan Core ⬢.", "warn"); S.tcore--; }
  S.choices = S.choices || {}; S.choiceAt = S.choiceAt || {}; S.choices.harb = v; S.choiceAt.harb = Date.now(); dirty(); try { if (window.udfStory && G.mode === "online") window.udfStory.act("harb", v, 1).catch(() => {}); } catch (e) {}
  G.storyT = null; archUnlock("t_h5", 2, true); try { strainCheck(); } catch (e) {} try { advHolo(v === "bind" ? TCH_BIND : TCH_WAKE, true); } catch (e) {} if (sheet) renderSheet(); tchCheck(); }
