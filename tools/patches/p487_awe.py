# v487 (owner: "Aexion performance should be similar in live map mode but more detailed and elaborated, add special dialogue to all boss
# battles about how this is nuts and that we have never seen anything like this, etc, change it up, mix it in and make it work, should all
# still sound natural but more real like hey the advisor hasn't seen it all").
# 1. Aexion live on the map, in his Warform, fights like he does in the battle reports, only bigger: every 11 s he turns to one of three
#    facings (never the same twice running), holds, strikes (blade, aegis, missiles, lance or a dodge), holds, turns back, rests. The
#    same for everyone (from the shared clock). The fleets he is fending off are there in their fire: streaks pour in from the side he
#    faces and land on his hex shield (ripples, flashes, sparks, the shield kicked back), heavier while he holds the Aegis, and a full
#    volley whenever a real commander's attack lands on the record.
# 2. The Advisor's awe: a pool of natural lines, one set per boss and a shared set, said now and then in boss battle reports (at the
#    boss's first strike, about half the time, never closer than 90 s apart) and mixed into the live super boss and Cube Devastation
#    events (every 6-10 minutes of watching). Never the same line again until the others have been heard.
import re
P = 'docs/index.html'; s = open(P).read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
AWE = {
 "all": ["I've seen a lot of battles, Commander. I have never seen anything like this.",
  "Okay... that's new. That's very, very new.",
  "Are you seeing this? Tell me you're seeing this too.",
  "This is nuts. Absolutely nuts. Keep firing!",
  "Nothing in the archives looks like this. Nothing.",
  "I'm not going to pretend I know what that was. Just keep shooting.",
  "Hold on. It can do that?",
  "That shouldn't be possible. And yet, there it is.",
  "I've run every simulation we have. Not one of them showed this.",
  "Remind me never to say I've seen it all.",
  "My sensors are screaming, Commander. Honestly, I don't blame them.",
  "Wow. Just... wow. Okay, focus. Keep the pressure on!",
  "I've been doing this a long time. This one is going in the records.",
  "Whatever that thing is, it's rewriting the rulebook as we go."],
 "aex": ["It fights like a swordsman! A machine that size, fencing with our whole fleet!",
  "Did it just block that? With a shield on its arm? Unbelievable.",
  "Look at it turn. It's reading our attacks before we even make them."],
 "vae": ["The whole wheel is turning toward us... I don't even have a word for that.",
  "Those runes are bending the space around it. I've never seen energy do that."],
 "omg": ["It's the size of a moon and it's still growing. This is insane.",
  "Cubes are pouring off it like a storm. I've never seen the Collective do this."],
 "scb": ["That tractor beam is dragging whole squadrons in. I've never seen a pull that strong.",
  "The entire Cube just lit up green. I've never seen it this angry."],
 "dev": ["It's swallowing the light around it. I've never seen anything do that.",
  "Those tentacles are longer than our battleships. How is it even moving them?"],
 "war": ["Gravity readings just went off the scale. And I mean literally off it.",
  "It's bending space around that disc. I honestly didn't think that was real."],
 "ovl": ["The Pyramid is waking up... every reading I have just doubled.",
  "It's pulling power from the whole Pyramid. I've never seen it burn this bright."],
 "brd": ["Where are all those drones coming from? It just keeps making more!",
  "That's not a ship. That's a nest. A flying, living nest."],
 "tyr": ["Look at the size of those guns. It's a fortress with engines.",
  "It's raining missiles. I've never seen a barrage this thick."],
 "wym": ["It's coiling around that black hole like it owns it. Maybe it does.",
  "Every segment is armoured differently. That thing was made for war."],
 "col": ["It's held together by nothing. Just crystal, flying in formation. That's impossible.",
  "It's rebuilding itself while we hit it. I've never seen anything heal like that."],
 "eic": ["The cold is freezing our shots in mid-flight. I didn't know ice could do that."],
 "efi": ["Its armour is actually molten. Our shells are melting before they land."],
 "eli": ["That light is so bright my scopes are going blind. Aim where you last saw it!"],
 "est": ["The lightning is jumping between our own ships. I've never seen a storm hunt like this."],
 "ena": ["It's growing back faster than we can cut it. That's not natural. Well, it is. That's the problem."],
 "epx": ["Five elements in one body. Nobody alive has seen a fusion like this.",
  "Fire, ice, lightning, light and life, all at once. This is nuts."],
}
import json
js = json.dumps(AWE, ensure_ascii=False)
rep("function sbSay(line) {", r"""/* v487 the Advisor's awe: per boss and shared, natural, never the same line until the others have been heard */
const AWE = """ + js + r""";
function awePick(k) { let U = []; try { U = JSON.parse(localStorage.getItem("udf_awe") || "[]"); } catch (e) {} const fr = L => (L || []).filter(l => !U.includes(voiceKey(l)));
  let own = fr(AWE[k]), gen = fr(AWE.all), L = own.length && (!gen.length || Math.random() < .6) ? own : gen; if (!L.length) { U = []; L = (AWE[k] || []).concat(AWE.all); }
  const line = L[(Math.random() * L.length) | 0]; U.push(voiceKey(line)); while (U.length > 40) U.shift(); try { localStorage.setItem("udf_awe", JSON.stringify(U)); } catch (e) {} return line; }
function aweSay(k, p = 1) { const n = Date.now(); if (n - (G.aweAt || 0) < 90000 || Math.random() > p) return; G.aweAt = n; try { sbSay(awePick(k)); } catch (e) {} }
function sbSay(line) {""")
# battle reports: at the boss's first strike, about half the time
rep("if (!c.fired && e >= T2) { c.fired = 1; const m = wbMoves(key), mv = m[(Math.random() * m.length) | 0]; WBR.b.act(mv); WBR.mv = { m: mv, t0: t }; }",
    "if (!c.fired && e >= T2) { c.fired = 1; const m = wbMoves(key), mv = m[(Math.random() * m.length) | 0]; WBR.b.act(mv); WBR.mv = { m: mv, t0: t }; if (battle && WBR.awe !== battle) { WBR.awe = battle; if (!G.stress || !G.stress.busy) aweSay(key, .55); } } /* v487 */")
# live super bosses: now and then while you watch
rep("{ const ph = sbPhase(k, st.hp); if (st.hp && ph > 0 && e > 600) say(k + s0 + \"p\" + ph, SBL[k][ph]); }",
    "{ const ph = sbPhase(k, st.hp); if (st.hp && ph > 0 && e > 600) say(k + s0 + \"p\" + ph, SBL[k][ph]); }\n  if (!dead && e > 90) { if (X.aweN == null) X.aweN = t + 60000 + Math.random() * 120000; else if (t > X.aweN) { X.aweN = t + 360000 + Math.random() * 240000; aweSay(k); } } /* v487 */")
rep("function dvSay(D) { const e = D.e, s0 = D.s0; G.dvSaid = G.dvSaid || {};",
    "function dvSay(D) { const e = D.e, s0 = D.s0; G.dvSaid = G.dvSaid || {}; if (e >= DV.stage && e < DV.ret) { const tn = performance.now(); if (G.dvAweN == null) G.dvAweN = tn + 90000 + Math.random() * 120000; else if (tn > G.dvAweN) { G.dvAweN = tn + 420000 + Math.random() * 240000; aweSay(\"omg\"); } } /* v487 */")
# Aexion live: fending off the fleets
rep('if (!dead) { const slot = Math.floor(T / 25000); if (slot !== X.slot) { X.slot = slot; const L = (xf ? SBW.aex.mv2 : SBW.aex.mv).filter(n => !(b.shieldGone && n === "aegis") && !(b.swordGone && n === "blade")); b.act(L[Math.abs(hash("a" + slot)) % L.length]); } }',
    'X.bolts.geometry.setDrawRange(0, 0); if (!dead) { if (xf && T - xf > 62000) aexLive(X, b, T, t, scl, st); else { const slot = Math.floor(T / 25000); if (slot !== X.slot) { X.slot = slot; const L = (xf ? SBW.aex.mv2 : SBW.aex.mv).filter(n => !(b.shieldGone && n === "aegis") && !(b.swordGone && n === "blade")); b.act(L[Math.abs(hash("a" + slot)) % L.length]); } } }')
rep("/* v454 Aexion's death (owner:", r"""/* v487 Aexion live, in his Warform: he fends off the fleets from three facings (the battle reports' beat, on the shared clock, so everyone
   sees the same fight), and their fire pours in from the side he faces and breaks on his shield */
function aexLive(X, b, T, t, sc, st) { const CY = 11000, slot = Math.floor(T / CY), e = T % CY, dirOf = n => [-1, 0, 1][Math.abs(hash("ad" + n)) % 3];
  let dir = dirOf(slot); if (dir === dirOf(slot - 1)) dir = dir === 0 ? (slot % 2 ? 1 : -1) : 0;
  const L = SBW.aex.mv2.filter(n => !(b.shieldGone && n === "aegis") && !(b.swordGone && n === "blade")), mv = L.length ? L[Math.abs(hash("am" + slot)) % L.length] : null, DUR = { dodge: 1500, blade: 2600, aegis: 2400, missiles: 3000, lance: 3200 }[mv] || 2600;
  if (X.y0 == null) X.y0 = b.grp.rotation.y; const sm = u => u <= 0 ? 0 : u >= 1 ? 1 : u * u * (3 - 2 * u), A = 1800, B = A + DUR + 700;
  const face = dir * (e < 900 ? sm(e / 900) : e < B ? 1 : 1 - sm((e - B) / 900)); b.grp.rotation.y = X.y0 + face * Math.PI / 4;
  if (mv && e >= A && X.slot !== slot) { X.slot = slot; if (e < A + 1500) b.act(mv); }
  // a real commander's attack on the record: a full volley
  const lg = st.log && st.log.length ? st.log[st.log.length - 1][0] : 0; if (X.lgA == null) X.lgA = lg; else if (lg !== X.lgA) { X.lgA = lg; X.vol = t; }
  const ang = X.y0 + face * Math.PI / 4, fx = Math.sin(ang), fz = Math.cos(ang), gp = b.grp.position, LV = X.lv || (X.lv = []), vol = t - (X.vol || -1e9) < 1400;
  const rate = vol ? 45 : mv === "aegis" && e > A && e < A + DUR ? 80 : e > 500 && e < B + 300 ? 170 : 900;
  if (t > (X.lvN || 0) && LV.length < 40) { X.lvN = t + rate * (.6 + Math.random() * .8); const d = 280 + Math.random() * 160, sp = (Math.random() - .5) * 240;
    LV.push({ a: new TH.Vector3(gp.x + fx * d + fz * sp, gp.y + 4 * sc + (Math.random() - .5) * 110, gp.z + fz * d - fx * sp), b: new TH.Vector3(gp.x + fx * 3.2 * sc + fz * (Math.random() - .5) * 9 * sc, gp.y + (4 + (Math.random() - .5) * 7) * sc, gp.z + fz * 3.2 * sc - fx * (Math.random() - .5) * 9 * sc), t0: t, L: 420 + Math.random() * 120 }); }
  const P = X.bolts.geometry.attributes.position.array, C = X.bolts.geometry.attributes.color.array; let n = 0;
  for (let i = LV.length - 1; i >= 0; i--) { const q = LV[i], s0 = (t - q.t0) / q.L; if (s0 >= 1) { LV.splice(i, 1); sbBoom(X, q.b, t, 3.6 * sc * (vol ? 1.4 : 1)); if (t - (X.hitT || 0) > (vol ? 420 : 950)) { X.hitT = t; b.act("hit"); } continue; }
    if (n >= X.NS) continue; const s1 = Math.min(1, s0 + .22); P.set([q.a.x + (q.b.x - q.a.x) * s0, q.a.y + (q.b.y - q.a.y) * s0, q.a.z + (q.b.z - q.a.z) * s0, q.a.x + (q.b.x - q.a.x) * s1, q.a.y + (q.b.y - q.a.y) * s1, q.a.z + (q.b.z - q.a.z) * s1], n * 6); C.set([.3, .5, .7, 1, .8, .5], n * 6); n++; }
  X.bolts.geometry.setDrawRange(0, n * 2); X.bolts.geometry.attributes.position.needsUpdate = true; X.bolts.geometry.attributes.color.needsUpdate = true; X.bolts.material.opacity = .7 + Math.random() * .3; sbBoomTick(X, t); }
/* v454 Aexion's death (owner:""")
s = re.sub(r"GAME_V = 486\b", "GAME_V = 487", s)
open(P, 'w').write(s)
