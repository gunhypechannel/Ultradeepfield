/* ---------- v807 the Events hub in the season's clothes: the season's colours and motif, and the Advisor (in this season's outfit)
   handing over whatever is ready to claim in the event you're looking at. ---------- */
function evkHub(html) { const sk = evkSkinOf("events"); let out = html;
  const m = out.match(/<button class="btn amber evclaim"([^>]*)>([\s\S]*?)<\/button>/); if (m && !/\sdisabled/.test(m[1])) {
    const at = m[1], lab = evkTxt(m[2]), ev = evkTxt((out.match(/class="evcard[^"]* on"[\s\S]*?<span class="ecn">([\s\S]*?)<\/span>/) || [])[1]) || "event";
    const cta = `<button class="evk-next claim"${at}><i>🎁</i><span><small>Ready to collect</small><b>${esc(lab)}</b></span><u>›</u></button>`;
    const adv = `<div class="evs-adv"><div class="evs-face" style="background-image:url('${sk.adv}');background-position:${sk.ap};background-size:${sk.as} auto"></div><div class="evs-say"><p>Your ${esc(ev)} rewards are waiting, Commander.</p>${cta}</div></div>`;
    const c0 = out.indexOf('<div class="evchips evhub">'), c1 = c0 < 0 ? -1 : out.indexOf("</div>", c0); out = c1 < 0 ? adv + out : out.slice(0, c1 + 6) + adv + out.slice(c1 + 6); }
  return `<div class="evhubv sheet-like evk-hub" data-skin="${sk.motif}" style="--sc:${sk.col};--sc2:${sk.col2}">${out}</div>`; }
document.addEventListener("click", e => { const b = e.target.closest && e.target.closest("button[data-act]"); if (!b || b.disabled || b.classList.contains("evk-next") || !b.closest(".evk-hub")) return; if (EVK_CLAIM.test(b.dataset.act)) evkBurst(b, /Mile|claim$/i.test(b.dataset.act)); }, true);
