/* ---------- v806 season skins: every event page in its own season's clothes. The page's own painting becomes the hero, the season's
   token sits in the season's frame as a medallion, the Advisor in that season's outfit delivers the next move, the panels carry the
   season's motif and colours, long lore folds away and a row of chips jumps to each section. Built from each page's own HTML. ---------- */
const EVK_SKIN = {
  mimic: { col: "#5fd8ff", col2: "#b48cff", tok: "art/season/s5-token.webp", frm: "art/season/s5-frame.webp", adv: "art/season/s5-adv.webp", ap: "50% 3%", as: "250%", motif: "hex", hue: [190, 270, 200, 285], line: "Commander, the hives are spreading." },
  carcinid: { col: "#e8b45a", col2: "#3fe8f0", tok: "art/carcinid/i_emblem.webp", frm: "art/carcinid/frame.webp", adv: "art/adv/p_point.webp", ap: "28% 4%", as: "235%", motif: "reef", hue: [40, 180, 30, 330], line: "Commander, the tide is rising." },
  cnt: { col: "#ff3346", col2: "#e8eef5", tok: "art/rwar/i_badge.webp", frm: "art/rwar/cos-frame.webp", adv: "art/adv/p_alarm.webp", ap: "50% 3%", as: "230%", motif: "circuit", hue: [355, 0, 210, 10], line: "Commander, their Arks are rebuilding them." },
  aet: { col: "#5fe8d0", col2: "#9ff6ea", tok: "art/season/s19-token.webp", frm: "art/season/s19-frame.webp", adv: "art/season/s19-adv.webp", ap: "50% 3%", as: "250%", motif: "lattice", hue: [168, 175, 190, 150], line: "The Gateway is ready, Commander." } };
function evkSkinOf(type) { if (EVK_SKIN[type]) return Object.assign({ k: type }, EVK_SKIN[type]); if (type === "aettgt") return Object.assign({ k: "aet" }, EVK_SKIN.aet);
  if (type === "aetsaga") { let j = 0; try { const sg = aetSaga(now()); j = sg ? sg.j : 0; } catch (e) {} const n = 16 + j; return Object.assign({}, EVK_SKIN.aet, { k: "aet", tok: `art/season/s${n}-token.webp`, frm: `art/season/s${n}-frame.webp`, adv: `art/season/s${n}-adv.webp`, line: ["Vesper Station has gone quiet, Commander.", "It's moving, Commander.", "Nhalis is changing, Commander.", "The ring is nearly closed, Commander."][j] }); }
  /* every other event page wears the current season */
  let c = 13; try { c = seaCos(vpSeason(now())); } catch (e) {} const has = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 16, 17, 18].includes(c), n = has ? c + 1 : 14, V = VP_SEASONS[has ? c : 13] || VP_SEASONS[13];
  return { k: "sea", col: V[1], col2: COS_C2[has ? c : 13] || "#fff", tok: `art/season/s${n}-token.webp`, frm: `art/season/s${n}-frame.webp`, adv: `art/season/s${n}-adv.webp`, ap: "50% 3%", as: "250%", motif: "stars", hue: [45, 190, 280, 330], line: `${V[0]} is under way, Commander. Every fight counts.` }; }
const evkTxt = h => (h || "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
const evkMedal = sk => `<div class="evs-medal"><i style="background-image:url('${sk.tok}')"></i><b style="background-image:url('${sk.frm}')"></b></div>`;
/* the transform: hero from the page's header and painting, the Advisor with the next move, section chips; morph-safe (pure string) */
function evkStage(html) { if (!sheet || !EVK_T.has(sheet.type) || /^aet$|^aettgt$/.test(sheet.type) || html.includes("evs-hero")) return html; const sk = evkSkinOf(sheet.type);
  const E = 'aria-label="Close">✕</button></div>', a = html.indexOf('<div class="hd'), b = html.indexOf(E); if (a < 0 || b < a) return html;
  const hd = html.slice(a, b + E.length), kick = evkTxt((hd.match(/<div class="chapter"[^>]*>([\s\S]*?)<\/div>/) || [])[1]), title = evkTxt((hd.match(/<h2[^>]*>([\s\S]*?)<\/h2>/) || [])[1]).replace(/^[^\w"'“]+\s*/, ""), extra = (hd.match(/<p[\s\S]*?<\/p>/g) || []).join("");
  let rest = html.slice(b + E.length), art = "", sub = "", pill = "";
  const ban = rest.match(/<div class="mimban[^"]*"><img src="([^"]+)"[^>]*><div><b>([\s\S]*?)<\/b><span>([\s\S]*?)<\/span><\/div><\/div>/);
  if (ban) { art = ban[1]; sub = ban[2]; pill = ban[3]; rest = rest.replace(ban[0], ""); }
  else { const sb = rest.match(/<div class="sbart"><img src="([^"]+)"[^>]*>(?:<span class="sbph">([\s\S]*?)<\/span>)?<\/div>/); if (sb) { art = sb[1]; pill = sb[2] || ""; rest = rest.replace(sb[0], ""); } }
  /* the next move goes into the Advisor's hands; the first short note becomes her line */
  let cta = ""; const cm = rest.match(/<button class="evk-next[\s\S]*?<\/button>/); if (cm) { cta = cm[0]; rest = rest.replace(cm[0], ""); }
  if (cta) { const ca = (cta.match(/data-act="([^"]+)"/) || [])[1], lab = evkTxt((cta.match(/<b>([\s\S]*?)<\/b>/) || [])[1]); /* the same button lower down is now redundant */
    if (ca) { const re = new RegExp(`<button class="btn[^"]*" data-act="${ca}"[^>]*>([\\s\\S]*?)<\\/button>`); const dm = rest.match(re); if (dm && evkTxt(dm[1]) === lab) rest = rest.replace(dm[0], ""); } }
  let line = sk.line; const nm = rest.match(/<p class="note[^"]*"[^>]*>([^<]{20,240})<\/p>/); if (nm) { line = nm[1]; rest = rest.replace(nm[0], ""); }
  rest = rest.replace(/<details class="crclore"\s+open(="")?>/g, '<details class="crclore">');
  let i = 0; const secs = []; rest = rest.replace(/<h3>([\s\S]*?)<\/h3>/g, (m, t) => { const id = "evs" + i++; secs.push([id, evkTxt(t).replace(/ · .*$/, "")]); return `<h3 id="${id}" class="evs-h">${t}</h3>`; });
  const nav = secs.length > 2 ? `<div class="evs-nav">${secs.map(([id, t]) => `<button data-act="evsJump" data-id="${id}">${esc(t)}</button>`).join("")}</div>` : "";
  const hero = `<div class="evk-hero evs-hero" style="--c:${sk.col}"><div class="evk-art" style="background-image:url('${art || sk.tok}')"></div><div class="evk-sh"></div>${evkMedal(sk)}
    <div class="evk-ht"><small>${esc(kick)}</small><b>${esc(title)}</b>${sub ? `<span>${sub}</span>` : ""}${pill ? `<div class="evk-hc"><i class="st">⏱ ${pill}</i></div>` : ""}</div><button class="x evk-x" data-act="close" aria-label="Close">✕</button></div>`;
  const adv = `<div class="evs-adv"><div class="evs-face" style="background-image:url('${sk.adv}');background-position:${sk.ap};background-size:${sk.as} auto"></div><div class="evs-say"><p>${line}</p>${cta}</div></div>`;
  return html.slice(0, a) + hero + adv + (extra ? `<div class="evs-extra">${extra}</div>` : "") + nav + rest; }
Object.assign(AET_ACT, { evsJump: d => { const h = document.getElementById(d.id), s = $(".sheet"); if (h && s) s.scrollTo({ top: h.offsetTop - 60, behavior: "smooth" }); } });
/* the Aetherion screens wear the medallion too */
{ const b = aetHero; aetHero = T => b(T).replace('<div class="evk-ht">', evkMedal(evkSkinOf("aet")) + '<div class="evk-ht">'); }
/* claim bursts in the season's colours */
{ const b = evkBurst; evkBurst = (el, big) => { const sk = sheet && EVK_T.has(sheet.type) ? evkSkinOf(sheet.type) : null; b(el, big); if (sk) { const box = document.querySelector(".evk-burst:last-of-type"); if (box) box.querySelectorAll("i").forEach((x, j) => x.style.setProperty("--h", sk.hue[j % 4])); } }; }
