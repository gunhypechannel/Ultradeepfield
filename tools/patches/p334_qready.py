import sys
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# v334 (owner's report: "it says I have a quest to claim but can't find it") the Quests badge counts rewards that sit further down
# the page (daily login, daily missions, the event tiers) or on another screen (Mastery). The top of the Quests tab now lists every
# reward that's ready, each with a button that claims it or takes you to it.
rep('''    <div class="advhero"><img src="${ADV_ART}" alt="${ADV}"><div class="advsay"><small>${ADV.toUpperCase()}</small><p>${esc(line)}</p>${act}</div></div>''',
    '''    <div class="advhero"><img src="${ADV_ART}" alt="${ADV}"><div class="advsay"><small>${ADV.toUpperCase()}</small><p>${esc(line)}</p>${act}</div></div>
    ${(() => { const r = [], mN = masteryReady() || 0, soloN = SOLO_TIERS.filter(([need], i) => s.pts >= need && !s.claimed.includes(i)).length, dN = S.daily && S.daily.tasks ? S.daily.tasks.filter(t => !t.claimed && dailyDone(t)).length + (!S.daily.bonus && S.daily.tasks.every(t => t.claimed) ? 1 : 0) : 0; // v334
      if (!ls.claimed) r.push(`<button class="btn amber" data-act="loginClaim">🎁 Daily login reward · claim</button>`);
      if (dN) r.push(`<button class="btn amber" data-act="qJump" data-ev="qdaily">✓ ${dN} daily mission${dN > 1 ? "s" : ""} ready</button>`);
      if (soloN) r.push(`<button class="btn amber" data-act="qJump" data-ev="daily">★ ${soloN} event reward${soloN > 1 ? "s" : ""} ready</button>`);
      if (mN) r.push(`<button class="btn amber" data-act="mastery">◆ ${mN} Mastery reward${mN > 1 ? "s" : ""} ready</button>`);
      return r.length ? `<section class="qready"><b>Ready to claim</b><div>${r.join("")}</div></section>` : ""; })()}''')
rep('''    <h2 class="sec">Daily missions</h2>''', '''    <h2 class="sec" data-ev="qdaily">Daily missions</h2>''')
rep('''  mastery: () => openSheet({ type: "mastery" }),''', '''  mastery: () => openSheet({ type: "mastery" }),
  qJump: d => { const el = document.querySelector(`#view [data-ev="${d.ev}"]`); if (el) el.scrollIntoView({ block: "start", behavior: "smooth" }); }, // v334''')
rep('''#toasts .toast.gdfade{''', '''.qready{margin:0 0 12px;padding:10px 12px;border:1px solid rgba(240,169,69,.55);border-radius:12px;background:rgba(240,169,69,.08)}.qready b{display:block;font:700 11px/1 var(--f-display);letter-spacing:.18em;text-transform:uppercase;color:var(--amber);margin-bottom:8px}.qready div{display:flex;flex-wrap:wrap;gap:8px}
#toasts .toast.gdfade{''')
open(p, 'w', encoding='utf-8', newline='').write(t); print('ok')
