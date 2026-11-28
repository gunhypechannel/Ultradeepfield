/* ---------- v837 the Mimic remastered: what they are (owner-approved lore, Nov 27 2026) ----------
   Every swarm card carries a codex entry and her assessment in her voice; opening one also opens "The Living Alloy" in the Archives. */
const MIM_LORE = {
  mstalk: ["The first-born scout. A Stalker hunts by heat and signal, and its hooked grapples hold the prey until the swarm arrives.", "A Stalker never kills alone, Commander. It holds you still for the ones behind it."],
  mhunt: ["Bred to kill fast ships. Its scythes are regrown from the interceptors it devoured, and its tail injects a rot that eats through metal.", "Those scythes used to be somebody's interceptors. Keep the fighters close, Commander."],
  mharv: ["The hive's stomach. Its canisters carry biomass and salvage home to the nests, and a hive without its Harvesters starves.", "Kill the Harvesters first and the hive goes hungry. Hungry hives grow slowly."],
  massim: ["It wears the ships it takes. The wheel in its flank is a stolen reactor it keeps alive, and the Echoes are born inside it.", "That reactor on its side is still running, Commander. It used to be ours."],
  mguard: ["The hive's shield-bearer. Its shields are its own nervous system hardened into hexagonal crystal, and it raises them over every Mimic near it.", "Break the Guardian and the whole pack loses its cover."],
  mtitan: ["A living nursery. Every glowing sac on its flanks is a swarm waiting to hatch, and when it fights, they hatch.", "Every one of those sacs is another swarm, Commander. Don't let it reach the line."] };
Object.assign(ARCH, { m_alloy: { cat: "mimic", t: "The Living Alloy", era: "The invasion", civ: "The swarm", loc: "Every hive", img: "art/mimic/hunter.webp", th: "Extreme",
  frag: "…not flesh, not machine. It grows metal the way we grow bone…",
  interp: "Mimics are neither animals nor machines but a living alloy grown from Omega's own tissue. The cyan light running through them is one shared nervous system, which is why the whole swarm moves as one mind. They are called Mimics because they copy whatever they kill.",
  adv: "Look at the light in them, Commander. That's one mind, spread across every body.",
  enc: ["Commander, I've been studying the bodies we recovered.", "They aren't built. They're grown. Metal, growing like bone."],
  def: ["The analysis is finished, Commander.", "Every Mimic we've ever fought was the same creature. Just wearing different shapes."] } });
ARCH_ORD.splice(ARCH_ORD.indexOf("m_protocol") + 1, 0, "m_alloy");
setTimeout(() => { Object.assign(ACT, { mimLore: d => { const L = MIM_LORE[d.k]; if (!L) return; try { archUnlock("m_alloy", 1, true); setTimeout(() => { try { archUnlock("m_alloy", 2); } catch (e) {} }, 3000); } catch (e) {}
  if (voiceHas(L[1])) { try { speak(L[1]); } catch (e) {} } else { try { advHolo(L[1], true); } catch (e) {} } } });
  try { const st = document.createElement("style"); st.textContent = ".mxcod{margin-top:6px}.mxcod summary{cursor:pointer;font:700 11px/1.4 Oxanium,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#7fe6ff;text-shadow:0 0 8px rgba(95,216,255,.6);list-style:none}.mxcod summary::before{content:'◈ '}.mxcod p{margin:6px 0;font-size:12px;line-height:1.45;color:#cfe9f2}.mxcod .btn{font-size:11px;padding:5px 10px;border-color:rgba(95,216,255,.55);box-shadow:0 0 12px rgba(95,216,255,.25)}"; document.head.appendChild(st); } catch (e) {} }, 0);
