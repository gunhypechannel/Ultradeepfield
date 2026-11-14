# v557 the Titan Core gate (owner: "These new ships should be gated somehow, maybe by super boss fights or some other way to earn a
# different extra rare resource too to make them"). Each Titan costs 6 Titan Cores (S.tcore) on top of its resources and is built at the
# homeworld only. Cores come from: every super boss you help defeat (2%+ of the damage) and one more for top damage, super-boss
# milestones (60 pts: 1, 120 pts: 2), the Convergence Clean Sweep (2), a top-3 Alliance Conquest week (1), Void Caches (3%) and the
# Vault (40 tokens). Shown on the Titan's card, the inspection viewer, reward lines and the Vault.
import sys, re
P = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('sz: 1.5, req: { shipyard: 12, hyper: 9, plasmaT: 8, armor: 12 }', 'sz: 1.5, tc: 6, req: { shipyard: 12, hyper: 9, plasmaT: 8, armor: 12 }')
rep('sz: 1.5, req: { shipyard: 12, hyper: 9, shields: 12, command: 4 }', 'sz: 1.5, tc: 6, req: { shipyard: 12, hyper: 9, shields: 12, command: 4 }')
rep('sz: 1.5, req: { shipyard: 12, hyper: 9, ionT: 8, computer: 10 }', 'sz: 1.5, tc: 6, req: { shipyard: 12, hyper: 9, ionT: 8, computer: 10 }')
rep('''    if (def.max) n = Math.min(n, def.max - (d.kind === "def" ? S.def[d.k] : own(d.k)) - S.sq.filter(x => x.k === d.k).reduce((a, x) => a + x.left, 0)); if (n <= 0) return;
    const c = mul(def.c, n); if (!pay(c)) return toast("Not enough resources.", "warn");''', '''    if (def.max) n = Math.min(n, def.max - (d.kind === "def" ? S.def[d.k] : own(d.k)) - S.sq.filter(x => x.k === d.k).reduce((a, x) => a + x.left, 0)); if (n <= 0) return;
    if (def.tc) { const have = S.tcore || 0; if (have < def.tc) return toast(`${def.n} needs ${def.tc} Titan Cores ⬢ (you have ${have}). Earn them by defeating super bosses.`, "warn"); n = Math.min(n, Math.floor(have / def.tc)); } /* v557 */
    const c = mul(def.c, n); if (!pay(c)) return toast("Not enough resources.", "warn"); if (def.tc) S.tcore -= def.tc * n;''')
rep('    if (def.max) return toast(`${def.n} can only be built at your homeworld.`, "warn");', '    if (def.max || def.tc) return toast(`${def.n} can only be built at your homeworld.`, "warn");')
rep('    S.shards = (S.shards || 0) + sh; giveItem(it); let extra = "";', '''    S.shards = (S.shards || 0) + sh; giveItem(it); let extra = ""; /* v557 Titan Cores: one for every boss you helped kill, one more for top damage */
    if (D.con == null && share >= .02) { const tcN = 1 + (Object.entries(dm).sort((a, b) => b[1] - a[1])[0][0] === G.me ? 1 : 0); S.tcore = (S.tcore || 0) + tcN; extra += `, ${tcN} Titan Core${tcN > 1 ? "s" : ""} ⬢`; }''')
rep('S.shards = (S.shards || 0) + 40; giveItem("teleport");', 'S.shards = (S.shards || 0) + 40; giveItem("teleport"); S.tcore = (S.tcore || 0) + 2;')
rep('  if (rw.shards) S.shards = (S.shards || 0) + rw.shards; if (rw.boosts) S.boosts += rw.boosts;', '  if (rw.shards) S.shards = (S.shards || 0) + rw.shards; if (rw.tc) S.tcore = (S.tcore || 0) + rw.tc; if (rw.boosts) S.boosts += rw.boosts;')
rep('rw.vip ? `<span class="rwi">VIP +${rw.vip}</span>` : "",', 'rw.vip ? `<span class="rwi">VIP +${rw.vip}</span>` : "", rw.tc ? `<span class="rwi tcw">⬢ ${rw.tc} Titan Core${rw.tc > 1 ? "s" : ""}</span>` : "",')
rep('[60, { shards: 20, mats: [["void", 5, 1], ["cube", 5, 1]] }],', '[60, { shards: 20, tc: 1, mats: [["void", 5, 1], ["cube", 5, 1]] }],')
rep('[120, { shards: 35, vip: 200, mats: [["void", 6, 1], ["cube", 5, 1]] }]];', '[120, { shards: 35, vip: 200, tc: 2, mats: [["void", 6, 1], ["cube", 5, 1]] }]];')
rep('S.cq = c.lw; S.shards = (S.shards || 0) + c.sh; if (c.item) giveItem(c.item);', 'S.cq = c.lw; S.shards = (S.shards || 0) + c.sh; if (c.item) giveItem(c.item); if (c.r && c.r <= 3) S.tcore = (S.tcore || 0) + 1;')
rep('  if (r < .04 && pool.length) {', '  if (r > .97) { S.tcore = (S.tcore || 0) + 1; return { t: "A Titan Core ⬢", ic: "⬢", rar: "epic" }; }\n  if (r < .04 && pool.length) {')
rep('''row("✦", "Void Cache", "Open it at once: shards, boosters, tokens or a cosmetic.", 8, "vtBuy", tok >= 8, 'data-k="cache"')''', '''row("✦", "Void Cache", "Open it at once: shards, boosters, tokens or a cosmetic.", 8, "vtBuy", tok >= 8, 'data-k="cache"')}${row("⬢", "Titan Core", `Needed to build Titan-class warships. You have ${S.tcore || 0}.`, 40, "vtBuy", tok >= 40, 'data-k="tcore"')''')
rep('if (d.k === "cache") { if (tok < 8) return;', 'if (d.k === "tcore") { if (tok < 40) return; S.vtok -= 40; S.tcore = (S.tcore || 0) + 1; toast("A Titan Core ⬢ from the Vault.", "win"); } else if (d.k === "cache") { if (tok < 8) return;')
rep("""<button class="btn amber wide t3open" data-act="t3Open" data-k="${k}">◎ Inspect in 3D · ${esc(TITAN_INFO[k].ab)}</button>` : ""}""", """<div class="tcreq${(S.tcore || 0) >= SH[k].tc ? " ok" : ""}"><b>⬢ Titan Cores ${S.tcore || 0} / ${SH[k].tc}</b><small>Needed for every Titan, on top of resources. Earned from super bosses: every boss you help defeat, top damage, boss milestones, Alliance Conquest and Void Caches. Built at your homeworld only.</small></div><button class="btn amber wide t3open" data-act="t3Open" data-k="${k}">◎ Inspect in 3D · ${esc(TITAN_INFO[k].ab)}</button>` : ""}""")
rep("""<h4>Systems</h4><ul>${li(I.more)}</ul></div>`; }""", """<h4>Systems</h4><ul>${li(I.more)}</ul><h4>To build</h4><p>${fmt(SH[k].c.m)} metal, ${fmt(SH[k].c.c)} crystal, ${fmt(SH[k].c.g)} gas and ⬢ ${SH[k].tc} Titan Cores (you have ${S.tcore || 0}), earned in super-boss fights. Built at your homeworld only.</p></div>`; }""")
rep("/* v556 the Titan inspection viewer */", "/* v556 the Titan inspection viewer */\n.tcreq{display:flex;flex-direction:column;gap:2px;padding:9px 11px;margin:0 0 8px;border-radius:12px;border:1px solid rgba(255,154,74,.5);background:linear-gradient(120deg,rgba(255,120,40,.14),rgba(10,12,20,.9))}.tcreq b{color:#ffb070}.tcreq.ok b{color:#5dff9a}.tcreq small{font-size:11.5px;color:var(--muted)}.tcw{color:#ffb070}")
s2 = re.sub(r"GAME_V = 556\b", "GAME_V = 557", s); assert s2 != s; s = s2
open(P, 'w', encoding='utf-8').write(s); print('ok')
