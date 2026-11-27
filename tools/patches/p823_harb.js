/* ---------- v823 the Eclipse Harbinger, more of it (owner: "Need more Eclipse Harbinger lines please, this ship needs to be super
   important ... Also want to give it another unique 4 pylon laser attack"; "Building it all, whatever is most logical").
   The Eclipse Cage (HC): on every 4th main volley (every 3rd when awakened) four reactor pylons leave its arms in time with its heart,
   take the corners of a square round the enemy, close a cage of violet and emerald beams, fire inward, and the point they meet collapses
   into a small eclipse that bursts. It is a staging of the Harbinger's own main gun: the volley's damage lands as before. Ten new lines
   (approved as drafted): sending it out, on the base, after a win or a loss, a long-range sighting, awakened near the Eclipse, bound. */
const HARB_L = {
  go: ["The Harbinger is leaving the dock, Commander. Listen. Its heart is already running ahead of the fleet.", "Every captain in that sector just checked their sensors twice. They know what's coming."],
  seen: "Commander, a ship on long-range just turned around. I think it heard the heartbeat.",
  base: ["It's quiet tonight. Even the crews whisper when they walk past the Harbinger.", "I counted its heartbeat for an hour, Commander. It was never the same twice."],
  win: ["They didn't lose to us, Commander. They lost to the thing we built.", "The Harbinger is coming home. Its reactor is calmer... I wish that made me feel better."],
  loss: "It's wounded. I can hear it, Commander. The heartbeat is slower, and angrier.",
  wake: "It's counting down with the sky, Commander. Every beat is one less.",
  bind: "The chains are holding. For now, it's only a ship. For now." };
const harbPick = (k) => { const L = HARB_L[k]; if (!Array.isArray(L)) return L; S.harbI = S.harbI || {}; const i = (S.harbI[k] = ((S.harbI[k] | 0) + 1) % L.length); dirty(); return L[i]; };
const harbOwned = () => { try { return own("harbinger") > 0; } catch (e) { return false; } };
/* sending it out: a reply to your tap, so she says it at once (at most every 10 minutes) */
{ const base = sendFleet; sendFleet = function (p, n, mission, extra) { const f = base(p, n, mission, extra);
    try { if (f && n && n.harbinger > 0 && mission !== "spy" && Date.now() - (G.harbGoAt || 0) > 600000) { G.harbGoAt = Date.now(); const L = mission === "attack" && p && p.owner && p.owner !== G.me ? HARB_L.seen : harbPick("go"); setTimeout(() => { try { G.advPass = 1; advHolo(L, true); } catch (e) {} finally { G.advPass = 0; } }, 900); } } catch (e) {}
    return f; }; }
/* after a battle it fought in: its own words instead of the usual remark */
{ const base = advBattle; advBattle = function (rep) { try { if (rep && !rep.test && S && G.ready && now() - (rep.at || 0) < 5 * 60000) { const mine = (rep.aUids || []).includes(G.me) ? "a" : rep.dUid === G.me ? "d" : null;
        if (mine && JSON.stringify((rep.start || {})[mine] || "").includes('"harbinger"') && rep.winner !== "draw" && now() - (G.advBt || 0) > 90000) { G.advBt = now(); const line = repWin(rep) ? harbPick("win") : HARB_L.loss; if (battle) G.advBtQ = line; else setTimeout(() => { try { advHolo(line, true); } catch (e) {} }, 1600); return; } } } catch (e) {}
    return base(rep); }; }
/* on the base, awakened near the Eclipse, bound: once a day each, through the queue (calm moments only; Important shows the Eclipse line) */
setInterval(() => { try { if (!S || !G.ready || tutOn() || !harbOwned()) return; const d = utcDay(); S.harbDay = S.harbDay || {};
    const c = S.choices && S.choices.harb; if (c === "wake" && S.harbDay.wake !== d) { let nx = null; try { nx = finNext("ecl", now()); } catch (e) {} if (nx && nx - now() < 3 * 864e5) { S.harbDay.wake = d; dirty(); advQueue(HARB_L.wake, 2, "live"); return; } }
    if (c === "bind" && S.harbDay.bind !== d) { S.harbDay.bind = d; dirty(); advQueue(HARB_L.bind, 1, "note"); return; }
    if (view === "base" && S.harbDay.base !== d && G.readyAt && Date.now() - G.readyAt > 120000) { S.harbDay.base = d; dirty(); advQueue(harbPick("base"), 1, "note"); } } catch (e) {} }, 15000);
/* ---- the Eclipse Cage ---- */
Object.assign(TX595, {
  HC(ctx, b, m, age, S0, E0, fc, Lg, d, lo, T, scr) { if (!E0) return; const aw = !!(S && S.choices && S.choices.harb === "wake"), R = Lg * (aw ? .52 : .44), ry = .62;
    const C = [[-1, -1], [1, -1], [1, 1], [-1, 1]].map(([sx, sy]) => [E0.x + sx * R, E0.y + sy * R * ry]), COL = ["176,107,255", "61,255,154", "176,107,255", "61,255,154"], HEX = ["#b06bff", "#3dff9a", "#b06bff", "#3dff9a"];
    const FLY = .85, CLOSE = .32, IN = .3, COL0 = FLY + CLOSE, COL1 = COL0 + IN, END = COL1 + .75, ease = tx5.ease || (u => u * u * (3 - 2 * u));
    if (age > END) return;
    /* the reactor gathers, beating */ tx5.glow(ctx, S0.x, S0.y, Lg * .3 * (.7 + .3 * Math.sin(age * 22)), "#3dff9a", age < FLY ? .75 : Math.max(0, .5 - (age - FLY)));
    const P = C.map((c, i) => { const t0 = i * .12, u = clamp((age - t0) / (FLY - .36), 0, 1), e = ease(u), a0 = (i / 4) * TAU + .4, sx = S0.x + Math.cos(a0) * Lg * .34, sy = S0.y + Math.sin(a0) * Lg * .2;
      const mx = (sx + c[0]) / 2 + (i % 2 ? 1 : -1) * Lg * .25, my = (sy + c[1]) / 2 - Lg * .3; return { x: (1 - e) * (1 - e) * sx + 2 * (1 - e) * e * mx + e * e * c[0], y: (1 - e) * (1 - e) * sy + 2 * (1 - e) * e * my + e * e * c[1], u, i }; });
    /* the pylons: a long violet-emerald crystal with a white heart, a trail while they fly, a ring as each takes its corner */
    for (const p of P) { if (p.u <= 0) continue; const s = Lg * .07, live = age < COL1 + .1 ? 1 : Math.max(0, 1 - (age - COL1 - .1) / .4);
      if (p.u < 1 && !lo) tx5.glow(ctx, p.x, p.y, s * 2.6, HEX[p.i], .45);
      ctx.globalAlpha = live; ctx.fillStyle = `rgba(${COL[p.i]},.85)`; ctx.beginPath(); ctx.moveTo(p.x, p.y - s * 1.6); ctx.lineTo(p.x + s * .45, p.y); ctx.lineTo(p.x, p.y + s * 1.6); ctx.lineTo(p.x - s * .45, p.y); ctx.closePath(); ctx.fill();
      tx5.glow(ctx, p.x, p.y, s * 1.4, "#ffffff", .8 * live); if (p.u >= 1) { const k = Math.min(1, (age - p.i * .12 - (FLY - .36)) / .3); if (k < 1) tx6.ring(ctx, p.x, p.y, s * (1 + k * 5), 2 * d * (1 - k), HEX[p.i], 1 - k, ry); } }
    if (age >= FLY - .02 && !m.b1) { m.b1 = 1; try { harbBeat(.9); } catch (e) {} }
    /* the cage closes: each pylon lays a beam to the next */
    if (age >= FLY) { const k = clamp((age - FLY) / CLOSE, 0, 1), fade = age < COL1 + .15 ? 1 : Math.max(0, 1 - (age - COL1 - .15) / .35);
      for (let i = 0; i < 4; i++) { const A = C[i], B2 = C[(i + 1) % 4], x2 = A[0] + (B2[0] - A[0]) * k, y2 = A[1] + (B2[1] - A[1]) * k;
        tx5.beam(ctx, A[0], A[1], x2, y2, [[Lg * .03 + d, COL[i], .45], [Lg * .008 + .7 * d, "255,255,255", .95]], fade);
        if (!lo && k >= 1 && fade > .2) tx5.bolt(ctx, A[0], A[1], B2[0], B2[1], 9, Lg * .05, i * 5 + Math.floor(age * 24), HEX[(i + 1) % 4], 1.1 * d, .5 * fade); } }
    /* then inward: four beams meet in the middle */
    if (age >= COL0) { const k = clamp((age - COL0) / IN, 0, 1), fade = age < COL1 + .1 ? 1 : Math.max(0, 1 - (age - COL1 - .1) / .3);
      for (let i = 0; i < 4; i++) { const A = C[i], x2 = A[0] + (E0.x - A[0]) * k, y2 = A[1] + (E0.y - A[1]) * k; tx5.beam(ctx, A[0], A[1], x2, y2, [[Lg * .045 + d, COL[i], .55], [Lg * .012 + d, "255,255,255", 1]], fade); }
      tx5.glow(ctx, E0.x, E0.y, Lg * .16 * k, "#3dff9a", k); }
    /* the point collapses into a small eclipse, then bursts */
    if (age >= COL1) { const c = (age - COL1) / (END - COL1);
      if (!m.hit) { m.hit = 1; b.shake = Math.max(b.shake || 0, (aw ? 12 : 9) * d); b.flash = Math.max(b.flash || 0, aw ? .32 : .24); try { harbBeat(1); } catch (e) {} }
      if (c < .35) { const r = Lg * .14 * (1 - c / .35 * .6); tx5.glow(ctx, E0.x, E0.y, r * 3.4, "#3dff9a", 1); ctx.globalCompositeOperation = "source-over"; ctx.globalAlpha = .96; ctx.fillStyle = "#000"; ctx.beginPath(); ctx.arc(E0.x, E0.y, r, 0, TAU); ctx.fill(); ctx.globalCompositeOperation = "lighter"; ctx.globalAlpha = 1; ctx.strokeStyle = "#dfffee"; ctx.lineWidth = 1.6 * d; ctx.beginPath(); ctx.arc(E0.x, E0.y, r, 0, TAU); ctx.stroke(); }
      else { const e = (c - .35) / .65, a = 1 - e; tx5.glow(ctx, E0.x, E0.y, Lg * (.22 + .38 * e), "#3dff9a", a * .85); tx5.glow(ctx, E0.x, E0.y, Lg * .1 * (1 - e * .5), "#ffffff", a); tx5.flare(ctx, E0.x, E0.y, Lg * (.7 * a + .15), "#c9a8ff", a * .7);
        tx6.ring(ctx, E0.x, E0.y, Lg * (.15 + .7 * e), 3 * d * a, "#b06bff", a, ry); if (!lo) for (let i = 0; i < (aw ? 9 : 6); i++) { const an = tx5.rnd(m.seed || 7, i) * TAU, Rr = Lg * (.35 + .6 * e); tx5.bolt(ctx, E0.x, E0.y, E0.x + Math.cos(an) * Rr, E0.y + Math.sin(an) * Rr * ry, 7, Rr * .12, i * 3 + Math.floor(age * 30), i % 2 ? "#b06bff" : "#3dff9a", 1.4 * d, a); } } } } });
