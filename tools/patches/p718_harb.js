/* ---------- v718 the Harbinger's heartbeat (owner: "Build all": a heartbeat sound, its name pulsing, other ships reacting, the awakened
   heart speeding up toward the Eclipse) ----------
   - harbPeriod(): one beat every 1.15 s (52 a minute). Bound with a Warden's heart: slower (1.45 s). Awakened: it quickens across the
     year as the Eclipse approaches, down to .68 s (88 a minute) in its last days.
   - harbBeat(): a low double thump (lub-dub), synthesised, on the sound-effects bus.
   - In any battle with a Harbinger on the field its heart beats under the fight; when it is ours the enemy hesitates, and she says so.
   - Wherever the words "Eclipse Harbinger" appear, they pulse emerald in time with that heart, and the first time the name shows on a
     screen (at most every 8 s, never in a battle) the heart beats once, softly. */
function harbPeriod(T = now()) { try { const c = S && S.choices && S.choices.harb; if (c === "bind") return 1.45; if (c === "wake") { let nx = null; try { nx = finNext("ecl", T); } catch (e) {} const d = nx ? (nx - T) / 864e5 : 280, k = clamp(1 - d / 280, 0, 1); return 1.15 - .47 * k * k; } } catch (e) {} return 1.15; }
function harbBeat(vol = 1) { try { if (!SFX.ok()) return; const c = AU.ctx, t0 = c.currentTime + .01, P = harbPeriod();
    for (const [dt, f0, pk] of [[0, 62, .34], [Math.min(.26, P * .22), 54, .26]]) { const t = t0 + dt, o = c.createOscillator(), o2 = c.createOscillator(), lp = c.createBiquadFilter(); o.type = "sine"; o2.type = "triangle";
      o.frequency.setValueAtTime(f0, t); o.frequency.exponentialRampToValueAtTime(f0 * .62, t + .16); o2.frequency.setValueAtTime(f0 * 2.02, t); o2.frequency.exponentialRampToValueAtTime(f0 * 1.1, t + .09);
      lp.type = "lowpass"; lp.frequency.value = 220; o.connect(lp); o2.connect(lp); SFX.env(lp, t, pk * vol, .34); o.start(t); o2.start(t); o.stop(t + .4); o2.stop(t + .4); } } catch (e) {} }
const HARB_HES = "Their fleet hesitated, Commander. They heard its heart too.";
function harbBattle(b) { if (!b || !b.Q) return; if (b.hbOn == null) { const mine = (() => { try { return (b.r && (b.r.aUids || []).includes(G.me)) ? "a" : "d"; } catch (e) { return "a"; } })(); b.hbOn = b.Q.some(q => q && q.k === "harbinger"); b.hbMine = b.Q.some(q => q && q.k === "harbinger" && q.side === mine); b.hbT0 = performance.now(); b.hbLast = 0; }
  if (!b.hbOn || b.done || b.ended) return; const T = performance.now(), P = harbPeriod() * 1000; if (T - b.hbLast >= P) { b.hbLast = T; harbBeat(.85); }
  if (b.hbMine && !b.hbSaid && T - b.hbT0 > 6500) { b.hbSaid = 1; try { sbSay(HARB_HES); } catch (e) {} } }
/* the name pulses with the heart: every text node naming it is wrapped once in a span the CSS animates */
(() => { const RX = /Eclipse Harbinger/, SKIP = new Set(["SCRIPT", "STYLE", "TEXTAREA", "INPUT", "CANVAS", "TITLE", "OPTION"]); let q = [], tm = 0, lastBeat = 0;
  const wrap = n => { const txt = n.nodeValue; if (!RX.test(txt)) return false; const p = n.parentNode; if (!p || SKIP.has(p.nodeName) || (p.closest && p.closest("svg")) || (p.classList && p.classList.contains("hbN")) || (p.closest && p.closest(".hbN"))) return false;
    const frag = document.createDocumentFragment(), parts = txt.split(/(Eclipse Harbinger)/); for (const s of parts) { if (!s) continue; if (s === "Eclipse Harbinger") { const sp = document.createElement("span"); sp.className = "hbN"; sp.textContent = s; frag.appendChild(sp); } else frag.appendChild(document.createTextNode(s)); }
    p.replaceChild(frag, n); return true; };
  const scan = root => { let hit = false; if (root.nodeType === 3) return wrap(root); if (root.nodeType !== 1 || SKIP.has(root.nodeName)) return false; const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), L = []; while (w.nextNode()) if (RX.test(w.currentNode.nodeValue)) L.push(w.currentNode); for (const n of L) hit = wrap(n) || hit; return hit; };
  const run = () => { tm = 0; const L = q; q = []; let hit = false; for (const n of L) if (n.isConnected) hit = scan(n) || hit;
    if (hit && !battle && performance.now() - lastBeat > 8000) { lastBeat = performance.now(); harbBeat(.45); } };
  const start = () => { try { document.documentElement.style.setProperty("--hbp", harbPeriod().toFixed(2) + "s"); setInterval(() => { try { document.documentElement.style.setProperty("--hbp", harbPeriod().toFixed(2) + "s"); } catch (e) {} }, 60000);
      new MutationObserver(ms => { for (const m of ms) { for (const n of m.addedNodes) q.push(n); if (m.type === "characterData") q.push(m.target); } if (q.length && !tm) tm = setTimeout(run, 60); }).observe(document.body, { childList: true, subtree: true, characterData: true }); q.push(document.body); run(); } catch (e) {} };
  if (document.body) start(); else document.addEventListener("DOMContentLoaded", start); })();
