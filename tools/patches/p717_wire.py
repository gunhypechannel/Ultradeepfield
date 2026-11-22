# v717 (owner): "Remaster eclipse harbinger archive lines to be more like the last one about the heart beat, i want people to tremble
# everytime they hear that ships name". Every Harbinger record now builds one dread: its heart beats a moment AHEAD of the Void, as if
# counting down to something, and something on the other side of its door is waiting. The records' Advisor moments (enc/def) were
# empty; they now speak. "The Heartbeat" itself is kept word for word: it is the model for the rest.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
def rep(a, b, n=None):
    global s
    c = s.count(a); assert c >= 1 and (n is None or c == n), (c, a[:90]); s = s.replace(a, b)

# the Fleet Registry
rep("The Eclipse Harbinger was built from schematics found sealed beneath a Warden's corpse. Its emerald reactor pulses with the same rhythm as the Eclipse itself. No one knows who drew the plans.",
    "The Eclipse Harbinger was built from schematics cut out of a Warden's corpse. Its emerald reactor beats in time with the Void at the galaxy's heart. Every crew that has served aboard it reports the same dream: a door, and someone on the other side of it, knocking in time.")
rep("Its heart beats in time with the Void, Commander. I don't like it. But I understand why we built it.",
    "Its heart beats a moment before the Void's, Commander. Not after. Before. I keep asking myself what it's counting down to.")
# 1. Beneath the Wyrm
rep("The schematics were found inside the Event Horizon Wyrm's corpse, etched in a material that does not reflect light. The Wyrm had swallowed them.",
    "The schematics were found inside the Event Horizon Wyrm's corpse, etched in a material that does not reflect light. Three of the salvage team stopped sleeping after they saw them. The fourth stopped speaking.")
rep("The Harbinger's plans came out of a Warden. Not guarded by it: hidden inside it, where no one was meant to find them.",
    "The Harbinger's plans came out of a Warden. Not guarded by it: swallowed by it, so that no one would ever build that ship. We cut them out of its body.")
rep('adv: "Wardens don\'t eat, Commander. It swallowed those plans to hide them. From us.", enc: [], def: []',
    'adv: "Wardens don\'t eat, Commander. That Wyrm swallowed those plans so that no one would ever build this ship. And we built it anyway.", enc: ["Commander, another page of the Harbinger\'s record has surfaced. I almost didn\'t open it."], def: ["The salvage team asked to be reassigned.", "All of them. As far from the Harbinger as the galaxy goes."]')
# 2. The Heartbeat: the model, kept; it gains its spoken moments
rep('adv: "It isn\'t echoing the Void. It\'s keeping time for it.", enc: [], def: []',
    'adv: "It isn\'t echoing the Void. It\'s keeping time for it.", enc: ["Commander... the Harbinger\'s reactor. Listen to it."], def: ["I timed it against the Void a thousand times.", "It is never late. Not once. It is always a moment early, Commander. Like something counting down."]')
# 3. The Drones Hesitate
rep('adv: "Commander, the drones are waiting for permission. And not from you.", enc: [], def: []',
    'adv: "The drones stop and listen before every order, Commander. Then they obey. One day they will hear the other voice first.", enc: ["The Harbinger\'s swarm is doing something it shouldn\'t, Commander."], def: ["I recorded the pause and slowed it down.", "There is a voice in it, Commander. It is saying your name."]')
# 4. Who Drew the Plans
rep('adv: "The Unmade drew it, Commander. It drew a ship it could leave in. And we built it.", enc: [], def: []',
    'adv: "The Unmade drew it, Commander. It drew itself a ship to leave in, and it waited, for an age, for someone to build it. We did.", enc: ["Commander, I laid the Harbinger\'s schematic over the last Eclipse."], def: ["It isn\'t a weapon, Commander.", "It\'s a door. It beats like a heart because something on the other side is waiting to walk through."]')
# 5. Bind or Awaken
rep("The reactor is listening. It can be sealed with a Warden's heart, or it can be let wake.",
    "The reactor is listening. Seal it with a Warden's heart, or let it wake and hear what it has been counting toward.")
# her lines when it is built and when it fights
rep("Eclipse Harbinger commissioned. Its drones are already restless.", "Eclipse Harbinger commissioned. The reactor skipped a beat when the crew said its name.")
rep("The Harbinger is here. Release the swarm, Commander.", "The Harbinger is on the field. Hear that, Commander? Its heart is beating faster. Release the swarm.")
rep("An enemy Harbinger. Spread the fleet before its swarm finds us.", "An enemy Harbinger. Listen... its heart is beating. Spread the fleet before its swarm finds us.")
rep('const GAME_V = 716;', 'const GAME_V = 717;', 1)
open(p, 'w', encoding='utf-8').write(s); print('ok')
