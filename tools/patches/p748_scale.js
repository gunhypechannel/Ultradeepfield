/* ---------- v748 the Resurrection War at 10,000 commanders. On the Supabase server, war points and fights go through cnt_apply: the
   server applies them in one short transaction (no lock, no compare-and-set, nothing lost to a race), keeps each commander's points and
   damage in its own tables, and keeps the shared record small (no per-commander maps; n commanders, the top five). This commander's own
   numbers come back with every call and from cnt_me. Elsewhere (the claude.ai artifact, offline) the old path is unchanged. */
/* the server path is used only once the server has answered (the functions exist and this commander is signed in); until then, or if
   it never does, the old path stays in use. Asked again every minute while it hasn't answered. */
function cntProbe() { if (!window.udfCnt || G.mode !== "online" || G.cntSrvOk === true || G.cntProbing || Date.now() - (G.cntProbeT || 0) < 60e3) return; G.cntProbing = 1; G.cntProbeT = Date.now();
  window.udfCnt.me(cntDoc(), cntKey()).then(m => { G.cntSrvOk = !!m; if (m) cntMeSet(m); }, () => { G.cntSrvOk = false; }).finally(() => { G.cntProbing = 0; }); }
const cntSrv = () => { cntProbe(); return !!(window.udfCnt && G.mode === "online" && G.cntSrvOk === true); };
setInterval(() => { try { if (G.ready) cntProbe(); } catch (e) {} }, 15e3);
async function cntSrvW() { if (window.udfCnt && G.mode === "online" && G.cntSrvOk !== true) { G.cntProbeT = 0; cntProbe(); for (let i = 0; i < 40 && G.cntProbing; i++) await sleep(250); } return cntSrv(); } /* a fight waits for the answer */
function cntMeSet(m) { if (!m || typeof m !== "object") return false; const k = cntKey(), p = cntDoc(), o = G.cntMe, ch = !o || o.k !== k || o.p !== p || JSON.stringify(o.m) !== JSON.stringify(m);
  G.cntMe = { k, p, m, t: Date.now() }; if (ch) CNTC = {}; return ch; }
function cntMeLoad(force) { if (!cntSrv()) return; const k = cntKey(), p = cntDoc(), o = G.cntMe; if (!force && o && o.k === k && o.p === p && Date.now() - o.t < 20e3) return; if (G.cntMeBusy) return; G.cntMeBusy = 1;
  window.udfCnt.me(p, k).then(m => { if (cntMeSet(m)) { try { if (sheet && (sheet.type === "cnt" || sheet.type === "pirate")) renderSheet(); else softRender(); } catch (e) {} } }).catch(() => {}).finally(() => { G.cntMeBusy = 0; }); }
/* a v2 record carries no per-commander maps: fill in this commander's own (and the top five) so the rest of the game reads it as before */
function cntV2Fill(o) { const me = G.me, M = G.cntMe && G.cntMe.k === o.k && G.cntMe.p === cntDoc() ? G.cntMe.m : null;
  o.con = {}; for (const [u, v] of (o.top || [])) o.con[u] = v; o.cday = {};
  if (M) { o.con[me] = Math.max(o.con[me] || 0, M.con || 0); o.cday[me] = [M.day, M.today || 0]; }
  for (const g of ["rel", "ark", "cmd"]) for (const id in o[g]) o[g][id].dmg = M && M.dmg && M.dmg[id] ? { [me]: M.dmg[id] } : {};
  if (o.fin) { const f = M && M.fin; o.fin.dmg = f ? { [me]: f.dmg || 0 } : {}; o.fin.hits = f ? { [me]: f.hits || 0 } : {}; o.fin.t10 = !!(f && f.t10); }
  return o; }
/* what a finale fight did, from the server's result and the record after it */
function cntFinMsg(tg, ev, o, seg) { const evs = String(ev || "").split("+"), has = e => evs.includes(e); let m = "";
  if (tg === "conv" || tg === "esc") return has(tg) ? (tg === "conv" ? `Convoy intercepted (${o.conv}): the hangars rebuild ${Math.min(100, o.conv * 15)}% slower.` : `Strike force escorted (${o.esc}): every fleet hits ${Math.min(50, o.esc * 5)}% harder.`) : `Our fleet couldn't break ${cntFinTgName(tg)}. Bring more warships.`;
  if (!seg) return `Our fleet couldn't break a section off ${cntFinTgName(tg)}. Send more firepower.`;
  if (/^anc/.test(tg)) { const i = +tg.slice(3); m = has("p3") ? "The last Neural Anchor is down. The Prime Ark's shield has collapsed: its fabrication chambers are exposed!" : o.anc[i] <= 0 ? `Neural Anchor ${i + 1} is down. ${o.anc.filter(v => v > 0).length} still hold the shield.` : `Neural Anchor ${i + 1}: ${o.anc[i]} of ${o.anc0} left.`; }
  else if (/^hang/.test(tg)) { const i = +tg.slice(4); m = o.hang[i] ? `Fabrication Hangar ${i + 1}: ${o.hang[i]} of ${o.hang0} left.` : `Fabrication Hangar ${i + 1} is destroyed. It builds nothing more.`; }
  else if (/^cond/.test(tg)) { const i = +tg.slice(4); m = o.cond[i] ? `Energy Conduit ${i + 1}: ${o.cond[i]} of ${o.cond0} left.` : `Energy Conduit ${i + 1} is cut.`; }
  else if (tg === "tx") m = has("cut") ? "The transmitter array is down! The transfer is broken off, and the reactor is exposed. Everyone: the reactor!" : `The transmitter array: ${o.tx} of ${o.tx0} left.`;
  else if (tg === "rx") m = has("dead") ? (o.out === "win" ? "THE PRIME ARK'S REACTOR IS GONE. The transfer was stopped. The Ark is dying." : "The Prime Ark's reactor is gone, but the transfer finished first. The Ark is dying; its mind is not.") : `The central reactor: ${o.rx} of ${o.rx0} left.`;
  if (has("p4")) m += " Its defences are broken: the Prime Ark is trying to send its mind away. Cut the transmitter array!";
  return m; }
