/* v744 the Continuum Records (drafts awaiting the owner's approval) */
Object.assign(ARCH, {
  cn_cont: { cat: "cnt", t: "The Continuum", era: "Older than our records", civ: "A machine civilisation", loc: "Beyond the charted stars", img: "art/rwar/ark_front.webp", th: "Extreme",
    frag: "…flesh forgets. Machines remember. Death is merely a transmission delay…",
    interp: "A machine civilisation that found fragments of the architecture Omega used to keep minds alive, and built its own. Its commanders do not die; they are sent somewhere to be rebuilt.",
    adv: "Every machine we destroy, Commander, something out there is keeping a copy.", enc: ["Commander, that red signal is back. It's coming from inside our space now.", "It repeats one word. Continuity."], def: ["The signal has gone quiet, Commander.", "For the first time since it started."] },
  cn_ark: { cat: "cnt", t: "The Resurrection Arks", era: "The Resurrection War", civ: "The Continuum", loc: "One in each quarter of the galaxy", img: "art/rwar/ark_side.webp", th: "Extreme",
    frag: "…a commander's mind crosses the relay, the chamber wakes, and the frame is rebuilt around it…",
    interp: "Capital ships of reconstruction chambers. While an Ark lives, has capacity and keeps a relay standing, its commanders come back hours after we kill them. Destroyed, it stays destroyed.",
    adv: "Destroying their fleets buys us time. Destroying the Arks wins the war.", enc: ["Commander, the commander we destroyed yesterday is back. Same signature, new hull.", "Its mind went somewhere when it died. The relays carry it to an Ark."], def: ["An Ark is gone, Commander.", "Its commanders have nowhere left to go."] },
  cn_prime: { cat: "cnt", t: "The Prime Resurrection Ark", era: "The Resurrection War's last day", civ: "The Continuum", loc: "The heart of the galaxy", img: "art/rwar/c_prime.webp", th: "Catastrophic",
    frag: "…every Ark answers to the first, and the first answers to no one…",
    interp: "The citadel every Ark answered to. It came through a gateway at the centre of the galaxy behind three Neural Anchors, and tried to send its mind away as it died.",
    adv: "It wasn't trying to win, Commander. It was trying to get out.", enc: ["Commander, every relay still standing just fired at once, at the same point.", "Something very large is coming through."], def: ["The Prime Ark is gone, Commander.", "Whatever it was sending, it was sending it a long way."] },
  cn_signal: { cat: "cnt", t: "The Final Signal", era: "After the Prime Ark", civ: "Unknown", loc: "Unknown", img: "art/rwar/c_eternal.webp", th: "Unknown",
    frag: "CONTINUITY TRANSFER: INCOMPLETE. UNKNOWN RECIPIENT DETECTED. OMEGA PROTOCOL: ACTIVE.",
    interp: "The Prime Ark's last transmission. The transfer did not finish, but something received part of it, and the protocol it invoked carries Omega's name.",
    adv: "Unknown recipient, Commander. Something was listening.", enc: ["Commander, one last transmission came off the Ark as it broke up.", "It wasn't addressed to any machine we know."], def: ["The signal ends there, Commander.", "But it ended with Omega's name."] } });
ARCH_ORD.push("cn_cont", "cn_ark", "cn_prime", "cn_signal");
ARCH_CAT.push(["cnt", "The Continuum Records", "The machine civilisation that refused to die, and the Arks that rebuilt it."]);
Object.assign(ADV_SAY1, { cntArr: ["Commander, every relay still standing just fired at once. All at the same point, the heart of the galaxy.", "Something very large is coming through. Send everything we have."],
  cntP3: ["The shield is down! Its fabrication hangars are open. Destroy the hangars and cut the conduits before it rebuilds them."],
  cntP4: ["It's trying to send its mind away, Commander. Cut the transmitter array, then hit the reactor."],
  cntColl: ["Its lights are going out. Commander, pull the fleets back. It's coming apart."], cntAway: ["It's pulling back through the gateway. Wounded, Commander, but not finished."] });
