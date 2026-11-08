# v336: building guide labels say why and how far ("Choose Solar Array: powers every extractor", "Tap Upgrade: Lv.6 of 9")
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep("""[[`.sheet [data-act="up"][data-k="${k}"]`, `Tap ${S.b[k] ? "Upgrade" : "Build"}`], [`article.bn[data-kind="b"][data-k="${k}"]`, `Choose ${B[k].n}`],""",
"""[[`.sheet [data-act="up"][data-k="${k}"]`, `Tap ${S.b[k] ? "Upgrade" : "Build"}${bGoalTxt(k)}`], [`article.bn[data-kind="b"][data-k="${k}"]`, `Choose ${B[k].n}${B_WHY[k] ? ": " + B_WHY[k] : ""}`],""")
rep("const bPath = (k, cat) =>", """/* v336: the guide says why a building matters and how far the step takes it */
const B_WHY = { metalMine: "metal pays for almost everything", crystalMine: "crystal pays for research and better ships", gasSynth: "gas fuels fleets and research", solar: "it powers every extractor",
  metalStore: "room for more metal", crystalStore: "room for more crystal", gasTank: "room for more gas", radar: "it warns you of incoming attacks", robotics: "it speeds up every build",
  shipyard: "it builds your ships", lab: "it unlocks and speeds up research", flagDock: "your flagship is built here" };
const bGoalTxt = k => { const st = tutOn() ? TUT[S.tut.i] : null, m = st && /Lv\\.(\\d+)/.exec(st.t), goal = m && (st.t.includes(B[k].n) || st.id === "econ-store") ? +m[1] : 0, nx = (S.b[k] || 0) + 1;
  return goal > nx ? `: Lv.${nx} of ${goal}` : goal === nx && goal > 1 ? `: last level, Lv.${goal}` : ""; };
const bPath = (k, cat) =>""")
open(p, 'w', encoding='utf-8').write(t); print('ok')
