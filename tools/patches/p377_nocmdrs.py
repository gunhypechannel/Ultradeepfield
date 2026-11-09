# v377: the Finder panel loses its Commanders tab (the leaderboards keep the commander list); a saved "cmdrs" tab falls back to the Finder
p = "docs/index.html"; t = open(p).read()
def rep(a, b):
    global t; assert t.count(a) == 1, a[:80]; t = t.replace(a, b)
rep('<button class="${t === "cmdrs" ? "on" : ""}" data-act="sub" data-g="gal" data-v="cmdrs">Commanders</button>', '')
rep('  const t = sub.gal;\n  const tabs = `<div class="tabs"><button class="${t === "targets"', '  if (!["targets", "mine", "fav"].includes(sub.gal)) sub.gal = "targets";\n  const t = sub.gal;\n  const tabs = `<div class="tabs"><button class="${t === "targets"')
rep('gal: ["targets", "mine", "fav", "cmdrs"]', 'gal: ["targets", "mine", "fav"]')
open(p, "w").write(t)
