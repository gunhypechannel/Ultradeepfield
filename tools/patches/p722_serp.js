/* ---------- v722 the Celestial Serpent's overhaul on the battle screen (owner: "Build it, It def needs a overhaul in battle simulation") ----------
   - Two moves, in turn: the Coil Strike (v721) and the Constrict, where it lunges at the biggest ship in reach, throws three gold-edged coils
     round it, squeezes three times and crushes it in violet fire.
   - It sheds its skin once in a fight (when it first loses a hatchling, or halfway through): a golden husk peels off and drifts away, and
     from then on it burns brighter, moves faster and strikes more often. She says so.
   - It does not explode when it dies: it dissolves into golden light that rises and fades.
   - The storyline: kills are counted, and at 3, 7, 12, 20 and 30 hatchlings the Advisor notices something about them, building toward
     their mother (the adults "have never been seen"). Visual and narrative only: the battle sim is untouched. */
const SERP_SHED = "It's shedding its skin, Commander. Whatever comes out of that husk is faster.";
const SERP_MILE = [[3, "Another hatchling down, Commander. The gold on its scales was brighter than the last one's."],
  [7, "I compared the hatchlings we've killed. Each one was older than the one before it. Something is raising them, Commander."],
  [12, "Their eyes all turned the same way as they died. Toward the rim of the galaxy. As if something out there was watching."],
  [20, "The hatchlings aren't hunting us, Commander. They're practicing. I don't want to know for whom."],
  [30, "Long-range scans caught a shadow on the rim tonight. Gold-edged, and larger than a moon. I think the mother has noticed what we've been doing to her children."]];
Object.assign(BEAST_DUR, { constrict: 1.9 }); Object.assign(BEAST_HIT, { constrict: .78 }); Object.assign(BEAST_BIG, { constrict: 1 });
/* the Serpent alternates its moves; the Constrict goes for the biggest enemy still flying */
function serpPick(b, v, q) { const c = b.bSerpN || (b.bSerpN = {}); c[v.s] = (c[v.s] || 0) + 1; if (c[v.s] % 2) return null;
  let best = v.e, bl = -1; for (let j = 0; j < b.Q.length; j++) { const o = b.Q[j]; if (!o || o.side === q.side || !(b.n[j] > 0)) continue; const l = bLen(o.k); if (l > bl) { bl = l; best = j; } } return best; }
const SERP_TINT = new WeakMap();
function serpTint(art) { let c = SERP_TINT.get(art); if (c) return c; c = document.createElement("canvas"); c.width = art.width; c.height = art.height; const x = c.getContext("2d"); x.drawImage(art, 0, 0);
  x.globalCompositeOperation = "source-atop"; const g = x.createLinearGradient(0, 0, c.width, c.height); g.addColorStop(0, "rgba(255,226,140,.85)"); g.addColorStop(.6, "rgba(255,190,90,.75)"); g.addColorStop(1, "rgba(190,130,255,.7)"); x.fillStyle = g; x.fillRect(0, 0, c.width, c.height); SERP_TINT.set(art, c); return c; }
function serpGhost(ctx, x, y, L, face, al, sc) { const art = shipArtSoon("cserp", "~f0", "side"); if (!art) return false; const w = L * (DRAWK.cserp || 2) * MBF_Z * (sc || 1), h = w / 2;
  ctx.save(); ctx.globalCompositeOperation = "lighter"; ctx.globalAlpha = al; ctx.translate(x, y); ctx.scale(face, 1); ctx.drawImage(serpTint(art), -w / 2, -h / 2, w, h); ctx.restore(); return true; }
/* the shed, the brighter body after it, and the death */
function serpDraw(ctx, b, scr, T, W, d, lo, t) { const Q = b.Q; if (!b.serpK) { b.serpK = Q.map((q, i) => q && q.k === "cserp" ? i : -1).filter(i => i >= 0); } if (!b.serpK.length) return;
  const sh = b.shed || (b.shed = {}), last = b.serpP || (b.serpP = {}); ctx.save();
  for (const i of b.serpK) { const q = Q[i], g = b.geo && b.geo[i], S0 = scr[i]; if (!g || !S0) continue; const alive = b.n[i] > 0;
    if (alive) last[i] = { x: S0.x, y: S0.y, L: g.L, face: g.face };
    const nc = b.serpN || (b.serpN = {}); if (nc[i] == null) nc[i] = b.n[i]; if (b.n[i] < nc[i] && last[i]) { (b.serpD || (b.serpD = [])).push(Object.assign({ t: T, j: i * 7 + b.n[i] }, last[i])); nc[i] = b.n[i]; } else if (b.n[i] > nc[i]) nc[i] = b.n[i];
    if (alive && !sh[i] && T > 3 && (b.n[i] < q.n0 || T > (b.end || 40) * .45)) { sh[i] = { t: T, x: S0.x, y: S0.y, L: g.L, face: g.face }; if (!b.serpSaid) { b.serpSaid = 1; try { sbSay(SERP_SHED); } catch (e) {} } try { mimSfx("hiss", clamp(S0.x / W * 2 - 1, -1, 1)); } catch (e) {} b.flash = Math.max(b.flash || 0, .12); }
    const s0 = sh[i]; if (s0) { const k = (T - s0.t) / 2.6; if (k >= 0 && k < 1) { const x = s0.x - s0.face * s0.L * .7 * k, y = s0.y - s0.L * .25 * k; serpGhost(ctx, x, y, s0.L, s0.face, .5 * (1 - k), 1 + .1 * k);
        ctx.globalCompositeOperation = "lighter"; for (let j = 0; j < (lo ? 8 : 18); j++) { const r1 = Math.sin(j * 91.7) * .5 + .5, r2 = Math.sin(j * 37.3) * .5 + .5, px = x + (r1 - .5) * s0.L * 1.6, py = y + (r2 - .5) * s0.L * .5 - k * s0.L * (.3 + r2 * .5); ctx.globalAlpha = (1 - k) * .9; ctx.drawImage(glowSprite(j % 3 ? "rgba(255,215,110,1)" : "rgba(200,140,255,1)"), px - 3 * d, py - 3 * d, 6 * d, 6 * d); } }
      if (alive && T >= s0.t) { const pr = .7 + .3 * Math.sin(t * .006 + i), L = g.L; ctx.globalCompositeOperation = "lighter"; ctx.globalAlpha = .3 * pr; ctx.drawImage(glowSprite("rgba(255,205,100,1)"), S0.x - L * 1.1, S0.y - L * .55, L * 2.2, L * 1.1); ctx.globalAlpha = .2 * pr; ctx.drawImage(glowSprite("rgba(190,120,255,1)"), S0.x - L * .7, S0.y - L * .4, L * 1.4, L * .8); } }
  }
  /* each hatchling that dies comes apart as golden light, rising (the last one with the whole body) */
  for (const P of b.serpD || []) { const k = (T - P.t) / 2.6, i = P.j; if (k < 0 || k >= 1) continue; serpGhost(ctx, P.x, P.y - P.L * .15 * k, P.L, P.face, Math.max(0, .8 - k * 1.3), 1);
    ctx.globalCompositeOperation = "lighter"; const n = lo ? 18 : 44; for (let j = 0; j < n; j++) { const r1 = Math.sin(j * 12.9 + i) * .5 + .5, r2 = Math.sin(j * 78.2 + i) * .5 + .5, st = r2 * .35, kk = clamp((k - st) / (1 - st), 0, 1); if (kk <= 0) continue;
      const px = P.x + (r1 - .5) * P.L * 1.8 + Math.sin(kk * 6 + j) * P.L * .06, py = P.y + (r2 - .5) * P.L * .4 - kk * P.L * (1 + r1 * 1.2); ctx.globalAlpha = (1 - kk) * .95; const s = (3 + 4 * r2) * d * (1 - kk * .5); ctx.drawImage(glowSprite(j % 4 ? "rgba(255,215,110,1)" : "rgba(200,140,255,1)"), px - s, py - s, s * 2, s * 2); }
    ctx.globalAlpha = (1 - k) * .45; const cw = P.L * .5; ctx.drawImage(glowSprite("rgba(255,225,150,1)"), P.x - cw, P.y - P.L * 1.6 * k - cw, cw * 2, cw * 2 + P.L * k); }
  ctx.restore(); }
/* the story: a won fight against Serpents counts its dead hatchlings, once per report */
function serpStory(r) { try { if (!S || !r || r.test || r.mon !== "cserp" || r.winner !== "a" || !(r.aUids || []).includes(G.me)) return; const id = r.id || (r.at + "|" + r.title), seen = S.serpR || (S.serpR = []); if (seen.includes(id)) return; seen.push(id); if (seen.length > 40) seen.shift();
    const k0 = S.serpK || 0, n = Math.max(1, (r.lossD && r.lossD.cserp) || 1), k1 = k0 + n; S.serpK = k1; dirty();
    const m = SERP_MILE.filter(x => k0 < x[0] && k1 >= x[0]).pop(); if (m) setTimeout(() => { try { sbSay(m[1]); } catch (e) {} }, 5500); } catch (e) {} }
