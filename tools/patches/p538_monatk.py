# v538 every space monster gets three attacks in the battle replay (owner: "I want to give all monsters at least 2/3 attacks"). Visual
# only, like the capital ships' second battery (v290 CAP2): the simulation, the damage and the server's checks are untouched. Each
# monster volley shows its main weapon plus one of two signature attacks, alternating volley by volley (MON_ATK[k][0 or 1], picked by
# the volley's time and shooter), in the monster's own colours.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('''function capSecond(b, v, q, side, sz, lo) {
  const c = CAP2[q.k]; if (!c || v.bounce) return;''', '''/* v538 the monsters' signature attacks: [weapon look, shots, colour, delay s, flags], two per monster, alternating volley by volley */
const MON_ATK = {
  swhale:  [["torpedo", 2, "#9fe8ff", .2, {}], ["flak", 6, "#bff3ff", .14, {}]],          // laser turrets · hull torpedoes · tail-gun tracers
  slevi:   [["acid", 3, "#ff8a3a", .2, {}], ["flak", 8, "#ffd36b", .12, {}]],            // plasma breath · molten spit · ember spray
  ssquid:  [["ion", 4, "#c890ff", .18, {}], ["torpedo", 2, "#7fe0ff", .22, {}]],         // acid · ink pulses · venom darts
  vmanta:  [["ion", 3, "#7af4ff", .16, {}], ["mass", 2, "#e8ffff", .2, {}]],             // lasers · gravity pulses · wing slashes
  swasp:   [["flak", 8, "#ffb02a", .1, {}], ["missile", 4, "#ffd36b", .2, {}]],          // acid stings · stinger swarm · launched barbs
  snest:   [["missile", 4, "#ffb02a", .2, { flank: 1 }], ["flak", 6, "#ffd36b", .12, {}]], // acid · larva pods · resin spray
  ctort:   [["ion", 3, "#5fb8ff", .18, {}], ["plasma", 2, "#9fd8ff", .24, { hv: 1 }]],   // crystal slugs · glyph pulses · crystal boulders
  gspider: [["mass", 3, "#c8a0ff", .16, {}], ["acid", 3, "#9a6bff", .2, {}]],            // gravity lance · gravity slugs · web spit
  smoth:   [["flak", 8, "#ffe08a", .1, {}], ["laser", 3, "#fff2b0", .16, {}]],           // ion dust · wing-dust storm · light darts
  cram:    [["plasma", 2, "#bfeaff", .22, { hv: 1 }], ["flak", 6, "#dff6ff", .12, {}]],   // horn slugs · comet fireballs · ice shards
  kegg:    [["flak", 6, "#c890ff", .12, {}], ["ion", 2, "#b07aff", .2, {}]],             // acid · thorn spray · violet pulses
  gwhale:  [["laser", 3, "#bff8ff", .16, {}], ["torpedo", 2, "#7af4ff", .22, {}]],        // ion song · ghost lances · spirit wisps
  reat:    [["acid", 3, "#ff9a4a", .2, {}], ["flak", 6, "#ffcf8a", .12, {}]],            // mass bites · molten spit · rock spray
  cserp:   [["laser", 3, "#ffd36b", .16, {}], ["ion", 3, "#c890ff", .2, {}]],            // plasma breath · golden lances · violet fire
  sent:    [["ion", 3, "#6affb8", .18, {}], ["plasma", 2, "#9dffcf", .26, { hv: 1 }]],    // stone fists · rune pulses · green boulders
};
function capSecond(b, v, q, side, sz, lo) {
  const c = CAP2[q.k] || (MON_ATK[q.k] && MON_ATK[q.k][hash(v.t + "|" + v.s) % 2]); if (!c || v.bounce) return; /* v538 */''')
s2 = re.sub(r"GAME_V = 537\b", "GAME_V = 538", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
