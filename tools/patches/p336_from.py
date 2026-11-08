# v336: "Launch from" follows the warships. After the colony invasion the warships sit at the colony and only a probe is home;
# the guide counted the probe as "ships at home", the raid went out as one probe and was beaten off
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
old_bar = '''  if (opts.length < 2 && cur === "home") return "";
  return `<div class="note">Launch from</div><div class="segc" style="overflow-x:auto">${opts.map(([id, n, c]) => `<button style="flex:none;padding:8px 12px" class="${cur === id ? "on" : ""}" data-act="setFrom" data-id="${id}">${esc(n)} · ${fmt(c)}</button>`).join("")}</div>`;'''
new_bar = '''  if (opts.length < 2 && cur === "home") return "";
  const armN = id => { const g = id === "home" ? S.ships : ((G.byId[id] || {}).garrison || {}); return Object.entries(g).reduce((a, [k, v]) => a + (warK(k) ? v || 0 : 0), 0); }; /* v336 */
  return `<div class="note">Launch from</div><div class="segc" style="overflow-x:auto">${opts.map(([id, n, c]) => `<button style="flex:none;padding:8px 12px" class="${cur === id ? "on" : ""}" data-act="setFrom" data-id="${id}" data-arm="${armN(id)}">${esc(n)} · ${fmt(c)}</button>`).join("")}</div>`;'''
rep(old_bar, new_bar)
rep('''const fromPick = () => { const n = b => parseFloat(b.textContent.split("·").pop()) || 0, on = $('.sheet [data-act="setFrom"].on'); if (!on || n(on) > 0) return null;''',
'''const fromPick = () => { const n = b => b.dataset.arm != null ? +b.dataset.arm : parseFloat(b.textContent.split("·").pop()) || 0, on = $('.sheet [data-act="setFrom"].on'); if (!on || n(on) > 0) return null; /* v336: counts warships, not probes */''')
open(p, 'w', encoding='utf-8').write(t); print('ok')
