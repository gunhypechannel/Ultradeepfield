# v335: the "Ready to claim" box lists every reward the Quests badge counts (Academy step + Directive were counted but not listed)
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep("""      if (!ls.claimed) r.push(`<button class="btn amber" data-act="loginClaim">🎁 Daily login reward · claim</button>`);""",
"""      if (td) r.push(`<button class="btn amber" data-act="tutClaim">🎓 Academy reward · collect</button>`); /* v335: these two were counted in the badge but never listed here */
      if (ok) r.push(`<button class="btn amber" data-act="claim">📜 Directive reward · ${esc(q.t)}</button>`);
      if (!ls.claimed) r.push(`<button class="btn amber" data-act="loginClaim">🎁 Daily login reward · claim</button>`);""")
open(p, 'w', encoding='utf-8').write(t); print('ok')
