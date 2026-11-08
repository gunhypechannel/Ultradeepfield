# v336: the homeworld naming step opens a small, clear naming card (the full skin sheet buried Save under 100+ skins and the name was prefilled)
p = 'docs/index.html'; t = open(p, encoding='utf-8').read()
def rep(a, b, n=1):
    global t; assert t.count(a) == n, (a[:80], t.count(a)); t = t.replace(a, b)
rep('''  const pxSel = sheet.px != null ? sheet.px : (p.px || "");
  return `<div class="hd"><canvas class="pv"''', '''  const pxSel = sheet.px != null ? sheet.px : (p.px || "");
  if (p.kind === "home" && tutAt("name-your-homeworld")) return `<div class="chapter">Flight Academy · your capital</div><h2>Name your homeworld</h2>
    <p class="note">Every commander sees this name on the galaxy map. Tap the box, type a name, then tap Save name.</p>
    <input class="minput" id="pname" maxlength="20" value="${esc(sheet.nm || "")}" placeholder="${esc(p.name)}" aria-label="Homeworld name" style="font-size:18px">
    <button class="btn wide amber" data-act="skinSave" style="margin-top:12px">Save name</button>
    <p class="note" style="margin-top:10px">Its look can be changed later: tap your homeworld, then Rename &amp; reskin.</p>`; /* v336 */
  return `<div class="hd"><canvas class="pv"''')
rep('''    const raw = (($("#pname") || {}).value != null ? $("#pname").value : (sheet.nm != null ? sheet.nm : p.name));''',
'''    const raw = (($("#pname") || {}).value != null ? $("#pname").value : (sheet.nm != null ? sheet.nm : p.name)).trim() || p.name; /* v336: an empty box keeps the current name */''')
rep('''path: () => [['.sheet [data-act="skinSave"]', "Type a name, then tap Save"], ['.sheet #pname', "Type your homeworld's name"], SHOWME]''',
'''path: () => (($(".sheet #pname") || {}).value || "").trim().length >= 2 ? [['.sheet [data-act="skinSave"]', "Tap Save name"], SHOWME] : [['.sheet #pname', "Tap here and type a name for your homeworld"], SHOWME]''')
open(p, 'w', encoding='utf-8').write(t); print('ok')
