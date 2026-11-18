/* v615 the Supply Depot gets its own page (owner: "the depot should have its own page, and I thought the depot person was supposed to
   be voiced; I provided art too"). Quartermaster Ondra Vey, in the owner's portrait, greets you, talks when you tap her, and reacts
   to trades, contracts and a better rate, in her own voice. */
const DEP_GREET = ["Commander! Welcome to the depot. Mind the crates, they bite.", "Back again? Good. Business is slow when you're away.",
  "You look like someone with too much of one thing and not enough of another. I can fix that.", "Prices moved overnight, Commander. Come and see which way."];
const DEP_TRADE = ["Pleasure doing business, Commander.", "Done. Don't spend it all on one dreadnought.", "Crates are loaded. Your haulers will have it before you blink."];
const DEP_CONTRACT = "That hauler's full. Here's your cut, as promised.", DEP_RANKUP = "You've earned a better rate. Don't tell the others.";
const depLines = () => DEP_LINES.flatMap(f => f.length ? ["m", "c", "g"].map(h => f(h)) : [f()]);
function depSay(line) { if (!line) return; G.depSay = line; const p = $("#dpsay"); if (p) p.textContent = line; try { speak(line); } catch (e) {} }
function depotOpen() { closeSheet(); openSheet({ type: "depot" }); const first = !S.depMet; S.depMet = 1; dirty();
  setTimeout(() => depSay(first ? DEP_GREET[0] : DEP_GREET[1 + ((Math.random() * (DEP_GREET.length - 1)) | 0)]), 350); }
function shDepot() { const body = mShop().replace(/^<div class="dpb">[\s\S]*?<\/p><\/div><\/div><\/div>/, "");
  return `<div class="hd"><div style="flex:1;min-width:0"><div class="chapter" style="color:#ffcf5a">Supply Depot</div><h2>Ondra's Trading Post</h2><p class="note">Swap resources at today's prices, fill her contract, buy boosts.</p></div><button class="x" data-act="close" aria-label="Close">✕</button></div>
    <div class="dph2"><div class="dpbn" style="background-image:url(art/allyDepot.webp)"></div><button class="dpport" data-act="depTalk" aria-label="Talk to Ondra"><img src="avatars/ondra.webp" alt="Quartermaster Ondra Vey"></button>
      <div class="dpsay"><small>QUARTERMASTER ONDRA VEY</small><p id="dpsay">${esc(G.depSay || depLine())}</p><button class="btn ghost sm" data-act="depTalk">🔊 Talk to Ondra</button></div></div>${body}`; }
