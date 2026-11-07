import sys
p = sys.argv[1]; t = open(p, encoding='utf-8', newline='').read()
def rep(a, b, n=1):
    global t; c = t.count(a); assert c == n, (c, a[:110]); t = t.replace(a, b)
# v331: mail all friends / mail all alliance members. One message goes to each commander's own inbox (a direct conversation),
# marked as sent to everyone; up to 60 recipients, once every 2 minutes.
rep('''async function chatPost(ch, to, msg) {''', '''async function chatPost(ch, to, msg, quiet) {''')
rep('''if (s.exists) { toast("This chat room is full for today. Try again tomorrow.", "warn"); return false; }''', '''if (s.exists) { if (!quiet) toast("This chat room is full for today. Try again tomorrow.", "warn"); return false; }''')
rep('''    toast("Couldn't send that message.", "warn"); return false; } }''', '''    if (!quiet) toast("Couldn't send that message.", "warn"); return false; } }
const MAIL_ALL_GAP = 120000, MAIL_ALL_MAX = 60;
function mailGroup(g) { const bl = new Set(S.blocked || []), al = S.ally && G.alliances[S.ally];
  const ids = g === "f" ? (S.friends || []) : al ? Object.keys(al.members || {}) : [];
  return [...new Set(ids)].filter(u => typeof u === "string" && u && u !== G.me && !bl.has(u) && !isBot(u)).slice(0, MAIL_ALL_MAX); }
async function mailAll(g, text) { const to = mailGroup(g), who = g === "a" ? "alliance members" : "friends";
  if (!to.length) { toast(g === "a" ? (S.ally ? "No other members in your alliance yet." : "Join an alliance first.") : "Add friends from a commander's card first.", "warn"); return false; }
  const wait = (S.mailAllAt || 0) + MAIL_ALL_GAP - now(); if (wait > 0) { toast(`You can mail everyone again in ${ftime(wait)}.`, "warn"); return false; }
  S.mailAllAt = now(); dirty(); toast(`Sending to ${to.length} ${who}…`); let ok = 0;
  for (let i = 0; i < to.length; i += 4) { const r = await Promise.all(to.slice(i, i + 4).map(u => chatPost("d", u, { u: G.me, x: text, t: now(), bc: g }, true).catch(() => false))); ok += r.filter(Boolean).length; }
  toast(ok === to.length ? `Sent to all ${ok} ${who}.` : ok ? `Sent to ${ok} of ${to.length} ${who}. The rest couldn't be reached.` : "Couldn't send that message.", ok ? "win" : "warn"); return ok > 0; }''')
rep('''  if (v.re && typeof v.re === "object" && typeof v.re.u === "string" && typeof v.re.x === "string") o.re =''', '''  if (v.bc === "f" || v.bc === "a") o.bc = v.bc; // v331: sent to all friends / all alliance members
  if (v.re && typeof v.re === "object" && typeof v.re.u === "string" && typeof v.re.x === "string") o.re =''')
rep('''          ${m.re ? `<span class="cre">''', '''          ${m.bc ? `<span class="cx csub">📣 ${mine ? "You sent this" : "Sent"} to all ${m.bc === "a" ? "alliance members" : "friends"}</span>` : ""}
          ${m.re ? `<span class="cre">''')
rep('''  const ch = sheet.ch || "g", to = sheet.to, msg = { u: G.me, x: text, t: now() };''', '''  if (sheet.bc) { const g = sheet.bc; inp.value = ""; sheet.draft = ""; if (await mailAll(g, text)) { sheet.bc = null; sheet.ch = "d"; } else inp.value = text; renderSheet(); return; } // v331
  const ch = sheet.ch || "g", to = sheet.to, msg = { u: G.me, x: text, t: now() };''')
rep('''  else if (sheet.to) { const c = CHAT.dms[dmKey(G.me, sheet.to)], msgs = c ? c.m : [];''', '''  else if (sheet.bc) { const g = sheet.bc, to = mailGroup(g), who = g === "a" ? "your alliance" : "your friends"; // v331: mail everyone at once
    body = `<div class="dmhd"><button class="btn ghost sm" data-act="chatTab" data-v="d">‹ Back</button><b>📣 Mail all ${g === "a" ? "alliance members" : "friends"}</b><span></span></div>
      <p class="note">${to.length ? `Goes to each of the ${to.length} commander${to.length > 1 ? "s" : ""} in ${who} as a direct message: ${esc(to.slice(0, 8).map(nameOf).join(", "))}${to.length > 8 ? ` and ${to.length - 8} more` : ""}.` : g === "a" ? (S.ally ? "No other members in your alliance yet." : "Join an alliance first.") : "Add friends from a commander's card first."}</p>
      ${to.length ? `<div class="chatin"><input class="minput" id="chatin" maxlength="240" placeholder="Message ${who}" aria-label="Message ${who}" autocomplete="off" value="${esc(sheet.draft || "")}"><button class="btn" data-act="chatSend">Send to ${to.length}</button></div>` : ""}`; }
  else if (sheet.to) { const c = CHAT.dms[dmKey(G.me, sheet.to)], msgs = c ? c.m : [];''')
rep('''    body = `<div class="flist">${convs.map(c => { const lm = c.m[c.m.length - 1],''', '''    const nf = mailGroup("f").length, na = mailGroup("a").length; // v331
    body = `<div class="row2 mallrow"><button class="btn sm wide" data-act="mailAllOpen" data-g="f"${nf ? "" : " disabled"}>📣 Mail all friends${nf ? ` · ${nf}` : ""}</button><button class="btn sm wide" data-act="mailAllOpen" data-g="a"${na ? "" : " disabled"}>📣 Mail all alliance${na ? ` · ${na}` : ""}</button></div><div class="flist">${convs.map(c => { const lm = c.m[c.m.length - 1],''')
rep('''  chatTab: d => { sheet.ch = d.v; sheet.to = null; renderSheet(); },''', '''  chatTab: d => { sheet.ch = d.v; sheet.to = null; sheet.bc = null; renderSheet(); },
  mailAllOpen: d => { chatInit(); if (sheet && sheet.type === "chat") { Object.assign(sheet, { ch: "d", to: null, bc: d.g, draft: "" }); renderSheet(); } else openSheet({ type: "chat", ch: "d", bc: d.g }); }, // v331''')
rep('''${G.mode === "online" ? `<button class="btn sm" data-act="mailNew">✉ New message</button>` : ""}''', '''${G.mode === "online" ? `<button class="btn sm" data-act="mailNew">✉ New message</button><button class="btn ghost sm" data-act="mailNew">📣 Mail all</button>` : ""}''')
rep('''.mailhd{display:flex;''', '''.mallrow{margin:0 0 10px}.mallrow .btn{flex:1}.mailhd{display:flex;''')
open(p, 'w', encoding='utf-8', newline='').write(t); print('ok')
