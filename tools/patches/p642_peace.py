# v642: Peace Shield in the shop (owner: "build it just like that"): 8h ◆70 / 24h ◆200 / 3 days ◆330, shields every world you hold
# from other commanders; attacking, spying on or firing missiles at another commander drops it; 12 h recharge after it ends;
# pirates and monsters are not stopped (shields never stopped them).
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    if c != n: raise SystemExit(f'expected {n} got {c}: {a[:100]}')
    s = s.replace(a, b)

rep('const SHOP_UNITS = {', r'''/* v642 Peace Shield: empire-wide, bought in the shop and used from the inventory */
const PEACE = [[8, 70], [24, 200], [72, 330]], PEACE_CD = 12 * 3600e3, PEACE_MAX = 7 * 864e5;
const peaceLeft = () => { const P = (S && S.peace) || {}, T = now(); return P.until > T ? P.until - T : 0; };
const peaceCdLeft = () => { const P = (S && S.peace) || {}, T = now(); return !peaceLeft() && P.cd > T ? P.cd - T : 0; };
const peaceHrs = h => h < 24 ? h + " hours" : h === 24 ? "24 hours" : h / 24 + " days";
ITIERS.slice(0, 3).forEach(([tk, tn, col], i) => { const [h, c] = PEACE[i];
  SHOP[`peace_${tk}`] = { cat: "special", tier: i, col, n: "Peace Shield", ic: "🛡", cost: c, stack: true,
    d: () => `Shields every world you hold from other commanders for ${peaceHrs(h)}. Attacking, spying on or firing missiles at another commander drops it. Pirates and monsters still come. 12-hour recharge after it ends.${peaceLeft() ? ` Up now: ${ftime(peaceLeft())} left.` : peaceCdLeft() ? ` Recharging: ready in ${ftime(peaceCdLeft())}.` : ""}`,
    use: () => peaceUp(h) }; });
function peaceUp(h) { const T = now(), P = S.peace || {}, cd = peaceCdLeft();
  if (cd) { toast(`Your Peace Shield is recharging. Ready in ${ftime(cd)}.`, "warn"); return null; }
  const base = P.until > T ? P.until : T, until = Math.min(T + PEACE_MAX, base + h * 3600e3); if (until <= base) { toast("Your Peace Shield already runs for the longest time it can (7 days).", "warn"); return null; }
  for (const q of myPlanets()) if (!(q.shieldUntil >= until)) { q.shieldUntil = until; putPlanet(q); }
  S.peace = { until, cd: until + PEACE_CD }; bump("shields"); try { syncPlayer(); } catch (e) {}
  return `Peace Shield up for ${ftime(until - T)}. Commander fleets heading for your worlds will turn back. Attacking another commander drops it.`; }
/* attacking, spying on or firing at another commander drops the Peace Shield (shields from other sources stay) */
function peaceBreak(tgt) { const P = S.peace, T = now(); if (!P || !(P.until > T)) return; const U = P.until;
  for (const q of myPlanets()) if (q.shieldUntil === U) { q.shieldUntil = T; putPlanet(q); }
  S.peace = { until: T, cd: T + PEACE_CD }; note(`Your Peace Shield dropped: you moved against ${tgt && tgt.name ? tgt.name : "another commander"}. It can go up again in 12 hours.`, "warn"); }
const peaceHits = p => { if (!p || !p.owner || p.owner === G.me) return false; const st = pStatus(p); return st === "player" || st === "shielded" || st === "home"; };
const SHOP_UNITS = {''')
rep('''  if (mission === "spy" && p.owner && p.owner !== G.me) publishInbound(p.owner, f); // v279''',
    '''  if ((mission === "attack" || mission === "spy") && peaceHits(p)) peaceBreak(p); /* v642 */
  if (mission === "spy" && p.owner && p.owner !== G.me) publishInbound(p.owner, f); // v279''')
rep('''    const T = now(), tt = misTime(h, p); S.mis.ballistic -= n;''', '''    const T = now(), tt = misTime(h, p); peaceBreak(p); S.mis.ballistic -= n;''')
rep('    ${st !== "shielded" ? strikeReqSection(p, p.lvl) : ""}', '    ${st !== "shielded" && peaceLeft() && peaceHits(p) ? `<div class="callout">🛡 Launching drops your Peace Shield (${ftime(peaceLeft())} left).</div>` : ""}${st !== "shielded" ? strikeReqSection(p, p.lvl) : ""}')
rep('const shopArtOf = k =>', 'SHOP_ART.peace = SHOP_ART.peace || "shields";\nconst shopArtOf = k =>')
rep('const GAME_V = 641', 'const GAME_V = 642')
open(p, 'w', encoding='utf-8').write(s)
