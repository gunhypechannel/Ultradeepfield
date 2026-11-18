# v636: 17 more premium-only planet skins (skins/ps1..ps17, cut from the owner's two sheets: tools/premskin_cut.py), each tied to
# the hull finish it matches and unlocked at that finish's Premium tier, two per finish where there are two (owner: "More premium
# planet skins for premium players only, they should get two planet skins for highest tiers that match the ship color unlock").
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const hullsAt = t =>', '''const PS_SKINS = [["ps1", "gold", "Aurum Spire", "A golden world of cathedral spires, wrapped in a ring of light.", 1], ["ps2", "ruby", "Crimson Crown", "Ruby crystal set in a crown of gold filigree.", 1],
  ["ps3", "cobalt", "Sapphire Sigil", "Deep blue sapphire bound in golden sigils.", 1], ["ps4", "diamond", "Diamond Heart", "A flawless cut diamond the size of a world.", 1], ["ps5", "pink", "Rose Halo", "Pink crystal spires inside a shimmering halo.", 0],
  ["ps6", "copper", "Copper Citadel", "A copper world crowned with a burning citadel.", 0], ["ps7", "emerald", "Emerald Crown", "Emerald crystal crowned in gold.", 1], ["ps8", "glyph", "Opaline Dream", "An opal world of shifting rainbow light and gold.", 1],
  ["ps9", "gold", "Golden Orrery", "A gold world turning inside a jewelled golden ring.", 1], ["ps10", "ruby", "Ruby Vein", "Faceted ruby split by a river of gold.", 1], ["ps11", "cobalt", "Cobalt Tempest", "Blue crystal storms swirling around a cobalt sea.", 0],
  ["ps12", "diamond", "Prismheart", "Diamond facets throwing rainbows across the dark.", 1], ["ps13", "pink", "Blossom Quartz", "Rose quartz gardens and pink crystal peaks.", 0], ["ps14", "copper", "Forgeworld", "A copper machine-city of glowing furnaces.", 0],
  ["ps15", "emerald", "Verdant Cascade", "Emerald cliffs and gold rivers falling into green light.", 1], ["ps16", "amethyst", "Amethyst Halo", "Amethyst spires inside a violet ring.", 0], ["ps17", "obsidian", "Obsidian Gilt", "A night-black world of starlight veined in gold.", 1]];
for (const [k, f, n, d, g] of PS_SKINS) { const F = HULL_F[f]; PXS[k] = { n, cost: 0, prem: F.t, img: 1, r: "all", b: +(.12 + .012 * F.t).toFixed(3), glow: F.rim, ec: [1, 3, 5].map(i => parseInt(F.col.slice(i, i + 2), 16)), d, gold: !!g, fin: f }; }
const premSkinsAt = t => PS_SKINS.filter(([, f]) => HULL_F[f].t === t).map(x => x[2]);
const hullsAt = t =>''')
rep('${hullsAt(sel).length ? `<span class="prperk">Hull finishes:', '${premSkinsAt(sel).length ? `<span class="prperk">Bonus planet skins: ${premSkinsAt(sel).join(", ")} <b>NEW</b></span>` : ""}${hullsAt(sel).length ? `<span class="prperk">Hull finishes:')
# the hull section shows the planets that match the chosen finish
rep('<div class="hfprev"><canvas class="shipart" data-ship="${sel}"', '${fin && PS_SKINS.some(x => x[1] === fin) ? `<div class="hfpl"><small>Matching planets</small>${PS_SKINS.filter(x => x[1] === fin).map(([k, , n]) => `<button data-act="skin" title="${esc(n)}"><canvas data-px="${k}" role="img" aria-label="${esc(n)} planet skin"></canvas><span>${esc(n)}</span></button>`).join("")}</div>` : ""}<div class="hfprev"><canvas class="shipart" data-ship="${sel}"')
css = ('.hfpl{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.hfpl small{font-size:11px;color:var(--muted);flex-basis:100%}.hfpl button{all:unset;cursor:pointer;display:flex;align-items:center;gap:6px;padding:4px 10px 4px 4px;border-radius:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,210,90,.3);font-size:12px}.hfpl canvas{width:34px;height:34px}\n')
i = s.index('</style>', s.index('#celeb{position:fixed')); s = s[:i] + css + s[i:]
s2 = re.sub(r"GAME_V = 635\b", "GAME_V = 636", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
