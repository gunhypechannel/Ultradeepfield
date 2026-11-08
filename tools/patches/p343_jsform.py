# v343: joint-strike formation. A member's fleet is drawn as part of the strike army (the leader's formation), but its fleet card
# offered its own formation buttons, which changed nothing on screen. Now those buttons show and set the strike's formation
# (leader only, until the strike lands), and the leader can change it on the march too, not only before launch.
p="docs/index.html"; h=open(p).read()
def rep(a,b):
    global h; assert h.count(a)==1,(h.count(a),a[:70]); h=h.replace(a,b)
rep('strikeForm: d => { const a = G.assaults[d.id]; if (!a || a.leader !== G.me || !FORMS[d.v] || now() >= a.launch) return;',
    'strikeForm: d => { const a = G.assaults[d.id]; if (!a || !FORMS[d.v]) return; if (a.leader !== G.me) return toast(`Only ${nameOf(a.leader)} (the strike leader) can change the formation.`, "warn"); if (now() >= a.arrive) return;')
rep('${formPicker(a, leader && !launched)}','${formPicker(a, leader && now() < a.arrive)}')
rep('''${f.n && sumShips(f.n) ? `<div class="segc fform">${Object.entries(FORMS).map(([k, F]) => `<button class="${fformOf(f) === k ? "on" :''',
    '''${f.n && sumShips(f.n) && f.assault && G.assaults[f.assault] ? (() => { const a = G.assaults[f.assault], cur = FORMS[a.form] ? a.form : "wedge", lead = a.leader === G.me && now() < a.arrive; return `<div class="segc fform">${Object.entries(FORMS).map(([k, F]) => `<button class="${k === cur ? "on" : ""}" data-act="strikeForm" data-id="${a.id}" data-v="${k}" title="${esc(F.d)}" ${lead ? "" : "disabled"}>${F.ic} ${F.n}</button>`).join("")}</div><p class="note">Joint strike formation${lead ? ": the whole army flies this way." : `, set by ${esc(nameOf(a.leader))}.`}</p>`; })() : f.n && sumShips(f.n) ? `<div class="segc fform">${Object.entries(FORMS).map(([k, F]) => `<button class="${fformOf(f) === k ? "on" :''')
open(p,"w").write(h); print("ok")
