# fb-20261118-0323: the Advisor's Fleet Path kept prompting "research / add to the queue" while the research queue was already
# full (5/5) (Bacon Tempest, v610: Dreadnought step needs Hyperspace Drive Lv.5; lab running Astrophysics + 4 queued).
# (1) spBlocked: a requirement whose lab or build queue is full counts as blocked, so the Advisor shows the directive instead.
# (2) rPath / bPath ("Show me"): with a full queue the guide points at the queue and says so, instead of "Tap Research",
#     which led to a card showing only "Queue full".
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
R = [
 ('  if (nd.r ? rQd(nd.k) : bQd(nd.k)) return aca;\n',
  '  if (nd.r ? rQd(nd.k) : bQd(nd.k)) return aca;\n  if ((nd.r ? rqN() : bqN()) >= Q_MAX) return true; /* fb-20261118: that queue is full, nothing to queue yet */\n'),
 ('"Open Structures to watch it"], DOCKT("build", "Tap Build")]\n  : storeFirst(',
  '"Open Structures to watch it"], DOCKT("build", "Tap Build")]\n  : bqN() >= Q_MAX ? [[".qrow .t", `Build queue full (${Q_MAX}/${Q_MAX}). Queue ${B[k].n} when a slot frees up`], [\'[data-act="sub"][data-g="build"][data-v="bld"]\', "Open Structures to see the queue"], DOCKT("build", "Tap Build")] /* fb-20261118 */\n  : storeFirst('),
 ('"Tap Lab"], DOCKT("build", "Tap Build")]\n  : storeFirst(cost(R[k]',
  '"Tap Lab"], DOCKT("build", "Tap Build")]\n  : rqN() >= Q_MAX ? [[".qrow .t", `Research queue full (${Q_MAX}/${Q_MAX}). Queue ${R[k].n} when a slot frees up`], [\'[data-act="sub"][data-g="build"][data-v="research"]\', "Open Research to see the queue"], [\'.qc[data-act="qgo"][data-q="r"]\', "Tap Lab"], DOCKT("build", "Tap Build")] /* fb-20261118 */\n  : storeFirst(cost(R[k]'),
]
for a, b in R:
    assert t.count(a) == 1, a
    t = t.replace(a, b, 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
