# v338: toasts fade under the guide's tip too (they covered "Tap Build"); the road says when a hull is already unlocked;
# fleet-path labels say where the hull is built
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep('''for (const ts of document.querySelectorAll("#toasts .toast")) { const b = ts.getBoundingClientRect(), over = b.right > r.left - 6 && b.left < r.right + 6 && b.bottom > r.top - 6 && b.top < r.bottom + 6; ts.classList.toggle("gdfade", over); } // v334''',
'''{ const tr = tip.getBoundingClientRect(), hit = (b, q) => q.width && b.right > q.left - 6 && b.left < q.right + 6 && b.bottom > q.top - 6 && b.top < q.bottom + 6; for (const ts of document.querySelectorAll("#toasts .toast")) { const b = ts.getBoundingClientRect(); ts.classList.toggle("gdfade", hit(b, r) || hit(b, tr)); } } // v334; v338: and under the tip''')
rep('''<em>Every stronger hull needs a bigger Shipyard and new research. Build up this road and the hull unlocks.</em></div>`; };''',
'''<em>${r.every(([q, l]) => lvlOf(q) >= l) ? `Everything on its road is done: ${esc(SH[k].n)}s are unlocked. Build them in the Shipyard.` : "Every stronger hull needs a bigger Shipyard and new research. Build up this road and the hull unlocks."}</em></div>`; };''')
rep('''['[data-act="sub"][data-g="build"][data-v="ships"]', "Open Shipyard"], DOCKT("build", "Tap Build")];
  return { i, k, n, d, need, say, rw,''', '''['[data-act="sub"][data-g="build"][data-v="ships"]', `Open Shipyard: ${d.n}s are built there`], DOCKT("build", `Tap Build: ${d.n}s are built in the Shipyard`)];
  return { i, k, n, d, need, say, rw,''')
rep('"Every 2 Astrophysics levels lets us hold another world: build more Colony Ships and send them with escorts to Hive worlds we can beat. I\'ll keep pointing you at the next directive on your path.",', '"Every 2 Astrophysics levels lets us hold another world: build more Colony Ships and send them with escorts to Hive worlds we can beat. I\'ll keep pointing you at the next directive on your path.", "For stronger ships, follow the Fleet Path: every new hull needs a bigger Shipyard and new research, and its card shows the whole road with a tick for each step.",')
open(p, 'w', encoding='utf-8').write(t); print('ok')
