/* ---------- v724 eggs, phase 1 (owner: "I just want eggs to be another fun part of the game" ... "Build it all") ----------
   - The drop is an event: an egg reveal over the screen (it wobbles in, light bursts in its rarity's colour, a Prismatic shimmers),
     and the Advisor reacts to how rare it is. Queued until no battle or cinematic is playing.
   - Tap to warm: each incubating egg can be warmed once every 20 hours, which takes 15% off what is left (at least 5 minutes).
     The egg wobbles harder the nearer it is to hatching.
   - Hatching is a cinematic: the egg shakes, cracks spread, light leaks, the shell bursts, and the creature rises in a glow of its
     rarity, with its trait.
   - Mystery traits: every hatchling rolls one (creatures hatched before this get one from their id, so it never changes).
     Fierce, Giant, Radiant and Hardy raise its element bonus; Lucky raises the chance of eggs from hunts; Swift shortens the
     breeding chamber's rest. */
const XS_TR = { fierce: ["Fierce", "+30% to its element bonus", 15], giant: ["Giant", "+20% to its element bonus. It's huge for its kind.", 15], radiant: ["Radiant", "+15% to its element bonus. It glows.", 10],
  hardy: ["Hardy", "+10% to its element bonus", 25], lucky: ["Lucky", "+2% chance of an egg from every won hunt (up to +6%)", 20], swift: ["Swift", "The breeding chamber rests 15% less (up to 45%)", 15] };
const XS_TRK = Object.keys(XS_TR), XS_TRM = { fierce: 1.3, giant: 1.2, radiant: 1.15, hardy: 1.1 };
function xsTrRoll(r) { const tot = XS_TRK.reduce((a, k) => a + XS_TR[k][2], 0); let x = r * tot; for (const k of XS_TRK) { x -= XS_TR[k][2]; if (x < 0) return k; } return "hardy"; }
function xsTr(c) { if (!c) return "hardy"; if (!c.tr || !XS_TR[c.tr]) c.tr = xsTrRoll((hash(String(c.id) + "|tr") % 1000) / 1000); return c.tr; }
const xsTrMul = c => XS_TRM[xsTr(c)] || 1;
const xsCrPct = c => { const D = XS[c.sp]; return D ? Math.round(XR[D[1]][3] * (c.pr ? 1.5 : 1) * xsTrMul(c) * 10) / 10 : 0; };
const xsLuck = () => { try { return Math.min(.06, (xsOf().hab || []).filter(c => xsTr(c) === "lucky").length * .02); } catch (e) { return 0; } };
const xsSwift = () => { try { return Math.min(.45, (xsOf().hab || []).filter(c => xsTr(c) === "swift").length * .15); } catch (e) { return 0; } };
const xsTrChip = c => { const t = XS_TR[xsTr(c)]; return `<span class="xstr t-${xsTr(c)}" title="${esc(t[1])}">✦ ${t[0]}</span>`; };
const XS_EGG_ADV = ["An egg, Commander. Still warm. I've sent it to the Sanctuary.", "This shell is humming, Commander. Rare stock, and still warm.", "Commander... this egg is glowing from the inside. I've never seen one like it.", "That shell is older than our charts, Commander. Handle it gently."];
const XS_PR_ADV = "It's prismatic, Commander. Every colour at once. I've only ever read about these.";
/* the reveal */
function xsReveal(sp, pr) { (G.eggQ || (G.eggQ = [])).push({ sp, pr: pr ? 1 : 0 }); xsRevealNext(); }
function xsRevealNext() { if (!G.eggQ || !G.eggQ.length || document.getElementById("xsrv")) return;
  if ((typeof battle !== "undefined" && battle) || (G.cineOn && (xsRevealNext.w = (xsRevealNext.w || 0) + 1) < 40) || document.hidden) { clearTimeout(xsRevealNext.t); xsRevealNext.t = setTimeout(xsRevealNext, 1500); return; } xsRevealNext.w = 0; /* a cinematic is waited out, at most a minute */
  const e = G.eggQ.shift(), r = XR[XS[e.sp][1]], col = xsCol(e.sp), el = document.createElement("div"); el.id = "xsrv"; el.className = "xsfx" + (e.pr ? " pr" : ""); el.style.setProperty("--c", col); el.style.setProperty("--r", r[1]);
  el.innerHTML = `<div class="xsrays"></div><div class="xsfxb"><i class="xsegg big xl${e.pr ? " pr" : ""}" style="--c:${col}"></i><small style="color:${r[1]}">${e.pr ? "✦ Prismatic · " : ""}${r[0]} egg</small><b>${esc(xsName(e.sp))}</b><p>${xsLvl() ? "Left in the wreckage, still warm. It's on its way to your Xeno Sanctuary." : "Left in the wreckage, still warm. Build a Xeno Sanctuary to hatch it."}</p><button class="btn amber">${xsLvl() ? "Wonderful" : "Got it"}</button></div>`;
  document.body.appendChild(el); requestAnimationFrame(() => el.classList.add("on")); try { SFX.research(); } catch (e2) {}
  const close = () => { el.classList.remove("on"); setTimeout(() => { el.remove(); xsRevealNext(); }, 350); }; el.addEventListener("click", close);
  setTimeout(() => { try { advHolo(e.pr ? XS_PR_ADV : XS_EGG_ADV[XS[e.sp][1]] || XS_EGG_ADV[0], true); } catch (e2) {} }, 700); }
/* the hatch */
function xsHatchCine(c) { if (document.getElementById("xsrv")) document.getElementById("xsrv").remove(); const D = XS[c.sp], r = XR[D[1]], col = xsCol(c.sp), t = XS_TR[xsTr(c)], el = document.createElement("div"); el.id = "xsrv"; el.className = "xsfx hatch" + (c.pr ? " pr" : ""); el.style.setProperty("--c", col); el.style.setProperty("--r", r[1]);
  const cracks = [...Array(6)].map((_, i) => { const a = i * 60 + (hash(c.id + i) % 30); let x = 50, y = 50, p = `M50 50`; for (let k = 1; k <= 4; k++) { const aa = (a + (k % 2 ? 18 : -18)) * Math.PI / 180; x += Math.cos(aa) * 9; y += Math.sin(aa) * 11; p += ` L${x.toFixed(1)} ${y.toFixed(1)}`; } return `<path d="${p}" style="--d:${.25 + i * .12}s"/>`; }).join("");
  const shards = [...Array(10)].map((_, i) => `<i style="--a:${i * 36 + (hash(c.id + "s" + i) % 20)}deg;--s:${.6 + (i % 3) * .25}"></i>`).join("");
  el.innerHTML = `<div class="xsrays"></div><div class="xsfxb"><div class="xshatch"><i class="xsegg big xl${c.pr ? " pr" : ""}" style="--c:${col}"></i><svg viewBox="0 0 100 100" class="xscrack">${cracks}</svg><div class="xsshards">${shards}</div><img src="${xsImg(c.sp)}" alt=""></div>
    <div class="xshi"><small style="color:${r[1]}">${c.pr ? "✦ Prismatic · " : ""}${r[0]}</small><b>${esc(xsName(c.sp))} hatched!</b>${xsTrChip(c)}<p>${esc(t[1])} · +${xsCrPct(c)}% ${esc(ELEM[D[0]].stat.toLowerCase())}</p><button class="btn amber">Welcome home</button></div></div>`;
  document.body.appendChild(el); requestAnimationFrame(() => el.classList.add("on")); try { SFX.charge && SFX.charge(0); } catch (e) {}
  setTimeout(() => { try { el.classList.add("burst"); SFX.blast && SFX.blast(1.6, 0); SFX.research(); } catch (e) {} }, 1900);
  let ok = 0; setTimeout(() => { ok = 1; }, 2600); el.addEventListener("click", ev => { if (!ok && !ev.target.closest("button")) return; el.classList.remove("on"); setTimeout(() => el.remove(), 350); }); }
