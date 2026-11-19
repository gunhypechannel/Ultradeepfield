/* v670 the Mimic Protocol in the Archives (owner-approved, Nov 19 2026): its own category, six records, unlocked by playing the invasion */
ARCH_CAT.push(["mimic", "The Mimic Protocol", "An ancient adaptive organism, its hive mind, and the vault that held it."]);
Object.assign(ARCH, {
  m_protocol: { cat: "mimic", t: "The Mimic Protocol", era: "Before the Wardens", civ: "An extinct civilization", loc: "Sealed sectors across the galaxy", img: "art/mimic/stalker.webp", th: "Extreme",
    frag: "…it takes whatever it touches, flesh or steel, and learns it. We meant to make a weapon of it. It made something of us instead…",
    interp: "An ancient adaptive organism that absorbs living tissue and technology. An extinct civilization tried to weaponize it, and failed.",
    adv: "Every hive we burn is one less thing it has learned from us.", enc: ["Commander, something is growing in the empty sectors.", "It builds nests out of whatever it finds. Including wrecks."], def: ["That hive is gone, Commander.", "The records were right. It learns. So do we."] },
  m_omega: { cat: "mimic", t: "Omega", era: "Before the Wardens", civ: "The swarm itself", loc: "The vault beneath the Cube network", img: "art/mimic/titan.webp", th: "Catastrophic",
    frag: "…not a leader. A single mind, spread across every one of them…",
    interp: "The collective consciousness the swarm grew into. It commands the Alphas, which command everything else.",
    adv: "Omega wants the Cube network itself. Through it, every connected galaxy.", enc: ["Commander, the swarm is moving as one.", "There is a single mind behind all of it. The records call it Omega."], def: ["Omega has fallen silent, Commander.", "Every Alpha just lost its voice at once."] },
  m_vault: { cat: "mimic", t: "The Vault", era: "Before the Wardens", civ: "An extinct civilization", loc: "Beneath the Cube network", img: "art/mimic/nexus.webp", th: "Catastrophic",
    frag: "…we could not kill it, so we built it a prison, and we wired the prison into the Cubes…",
    interp: "Omega's prison, a dimensional vault wired into the Cube network. Recent Cube activity has weakened it.",
    adv: "Every Cube we've broken may have been a crack in that vault.", enc: ["Commander, the Cube network is drawing power from somewhere below it.", "There's a vault down there. Something has been pushing on the door."], def: ["The vault stands empty, Commander.", "Whatever it held, it isn't holding it anymore."] },
  m_alpha: { cat: "mimic", t: "The Alphas", era: "The invasion", civ: "The swarm", loc: "The four quarters of the galaxy", img: "art/mon/alpha1.webp", th: "Extreme",
    frag: "…four sovereigns, one for each quarter, each speaking for the mind below…",
    interp: "Regional sovereigns. Each rules its hives through a Neural Nexus.",
    adv: "Break the Nexus and the Alpha stands alone. That's when it bleeds.", enc: ["Commander, something is coordinating the hives in this quarter.", "It's an Alpha. And it's listening to something through that Nexus."], def: ["The Alpha is down, Commander.", "Its hives are scattering without it."] },
  m_echo: { cat: "mimic", t: "Mimic Echoes", era: "The invasion", civ: "The swarm", loc: "Mature hives", img: "art/mimic/hive.webp", th: "Severe",
    frag: "…it took our dead ships and sent them back to us…",
    interp: "Wrecks the Assimilators absorb come back as copies of the ships we lost.",
    adv: "They copy the shape, not the crew. Our pilots still fly better.", enc: ["Commander, those are our ships out there. Or they were.", "The Assimilators rebuilt them from our wrecks."], def: ["The Echoes are gone, Commander.", "Nothing left of ours for it to wear."] },
  m_frag: { cat: "mimic", t: "The Fragment", era: "After the Convergence", civ: "Omega", loc: "The ancient Cube network", img: "art/mimic/nexus.webp", th: "Unknown",
    frag: "I did not create the swarm. I was created to survive what is coming.",
    interp: "As Omega's body failed, a fragment of its consciousness escaped into the ancient Cube network.",
    adv: "Survive what is coming, it said. Not who. What.", enc: ["Commander, we intercepted a transmission. It came from Omega.", "It wasn't a threat. It sounded like a warning."], def: ["The transmission ends there, Commander.", "Something of it is still in the Cubes."] } });
ARCH_ORD.push("m_protocol", "m_alpha", "m_echo", "m_vault", "m_omega", "m_frag");
{ const i = ARCH_ORD.indexOf("krk"); if (i >= 0) ARCH_ORD.splice(i, 1); } /* the Kraken is retired: its card can no longer be found */
