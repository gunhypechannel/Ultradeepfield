# v725 (owner: "Build it all" then "Finish"): eggs phases 2 and 3 (p725_xs2.js + p725_xs2.css): growth, the companion (map and battle),
# collection rewards, the Sanctuary on profiles, event eggs, gifting eggs in the alliance, and the Serpent storyline's eggs.
import sys, os
p = sys.argv[1] if len(sys.argv) > 1 else 'docs/index.html'; s = open(p, encoding='utf-8').read()
D = os.path.dirname(os.path.abspath(__file__))
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
R = lambda f: open(os.path.join(D, f), encoding='utf-8').read()
a = "@media (prefers-reduced-motion:reduce){.xsrays,.xsegg.xl,"
i = s.index(a); j = s.index("\n", i); s = s[:j + 1] + R('p725_xs2.css') + s[j + 1:]
rep("const xsTrMul = c => XS_TRM[xsTr(c)] || 1;", "const xsTrMul = c => (XS_TRM[xsTr(c)] || 1) * xsGrow(c)[1]; /* v725 growth too */\n" + R('p725_xs2.js'))
rep("const xsName = k => (MON[k] && MON[k].n) || k, xsCol = k => (MON[k] && MON[k].col) || \"#7dffb8\", xsImg = k => `art/mon/${monImg(k)}.webp?v=1`;",
    "const xsName = k => (XS_EVN[k] && XS_EVN[k][0]) || (MON[k] && MON[k].n) || k, xsCol = k => (XS_EVN[k] && XS_EVN[k][1]) || (MON[k] && MON[k].col) || \"#7dffb8\", xsImg = k => XS_EVN[k] ? XS_EVN[k][2] : `art/mon/${monImg(k)}.webp?v=1`; /* v725 event species */")
rep("return Math.min(XS_CAP_PCT, Math.round(v * 10) / 10);", "return Math.min(XS_CAP_PCT, Math.round(v * 10) / 10) + xsBookPct(e); /* v725 collection rewards */")
rep("const sp = x.mon; if (!XS[sp] || XS[sp][2]) return;", "const sp = xsEvSp(x.mon) || x.mon; if (!XS[sp] || XS[sp][2]) return; /* v725 event eggs */")
rep('${seen ? esc(xsName(k)) : XS[k][2] ? "Bred only" : "???"}', '${seen ? esc(xsName(k)) : XS[k][3] ? "Event only" : XS[k][2] ? "Bred only" : "???"}')
rep('<em>+${pct}% ${esc(ELEM[D[0]].stat.toLowerCase())}</em></div>', '<span class="xsgr">${xsGrow(c)[0]}</span><em>+${pct}% ${esc(ELEM[D[0]].stat.toLowerCase())}</em>${xsCrFeedNote(c)}</div>')
rep('<div class="xscb"><button class="btn sm${on ? " amber" : ""}" data-act="xsSel"', '<div class="xscb">${xsCrExtra(c)}<button class="btn sm${on ? " amber" : ""}" data-act="xsSel"')
rep('<div class="xscr${on ? " on" : ""}${c.pr ? " pr" : ""}"', '<div class="xscr${on ? " on" : ""}${c.pr ? " pr" : ""} g${c.g || 0}${X.comp === c.id ? " cmp" : ""}"')
rep('<div class="xsbook">${book}</div></div>`; }', '<div class="xsbook">${book}</div><div class="xsbrw">${Object.keys(ELEM).map(e => `<span class="${xsBookDone(e) ? "ok" : ""}" style="--c:${ELEM[e].col}">${xsBookDone(e) ? "✓" : "○"} ${ELEM[e].n} species +1%</span>`).join("")}<span class="${xsBookAll() ? "ok" : ""}" style="--c:#ffd36b">${xsBookAll() ? "✓" : "○"} Every wild species: +1% to all</span></div></div>`; }')
rep('<div class="xsegs">${eggs}</div>', '<div class="xsegs">${eggs}</div>${xsGiftHTML()}')
rep("X.hab = X.hab.filter(x => x.id !== c.id); G.xsSel", "X.hab = X.hab.filter(x => x.id !== c.id); if (X.comp === c.id) X.comp = null; G.xsSel")
rep("  xsHatch: d => act(() => {", """  xsFeed: d => act(() => { const X = xsOf(), c = X.hab.find(x => x.id === d.id); if (!c || (c.g || 0) >= 2) return; if (!pay(xsFeedCost(c))) return toast("Not enough resources.", "warn"); /* v725 */
    c.g = (c.g || 0) + 1; try { SFX.research(); } catch (e) {} toast(`Your ${xsName(c.sp)} grew into ${c.g === 2 ? "an" : "a"} ${XS_GROW[c.g][0]}! Its bonus is now +${xsCrPct(c)}%.`, "win"); }),
  xsComp: d => act(() => { const X = xsOf(); X.comp = X.comp === d.id ? null : d.id; const c = xsComp(); toast(c ? `${xsName(c.sp)} is your companion. It flies with your flagship and fights at your side.` : "No companion."); }),
  xsGift: d => act(() => { const X = xsOf(), a = myAlly(), to = (document.getElementById("xsto") || {}).value || G.xsTo; if (!a || !a.members[to] || to === G.me || !G.db) return toast("Choose an alliance member.", "warn"); if (xsGiftsToday() >= 3) return toast("Three egg gifts a day. More tomorrow.", "warn");
    const i = X.eggs.findIndex(e => e.sp === d.sp && !!e.pr === (d.pr === "1")); if (i < 0) return; const e = X.eggs.splice(i, 1)[0], id = "x" + (S.seq++) + (now() % 1e6).toString(36); S.xsGiftT = (S.xsGiftT || []).filter(t => t > now() - 864e5).concat(now()); G.xsTo = to;
    G.db.doc("alliances/" + a.id).update({ xsg: { [id]: { by: G.me, to, at: now(), sp: e.sp, pr: e.pr ? 1 : 0 } } }).catch(() => {}); toast(`${e.pr ? "Prismatic " : ""}${xsName(e.sp)} egg sent to ${nameOf(to)}.`, "win"); }),
  xsClaim: d => act(() => { const X = xsOf(), g = xsGiftsIn().find(([id]) => id === d.id); if (!g) return; if (X.eggs.length >= XS_EGGS) return toast("The egg store is full. Incubate some first.", "warn"); const [id, v] = g;
    S.xsGot = Object.assign({}, S.xsGot, { [id]: 1 }); X.eggs.push({ sp: v.sp, pr: v.pr ? 1 : 0 }); const a = myAlly(); if (a && G.db) G.db.doc("alliances/" + a.id).update({ xsg: { [id]: Object.assign({}, v, { c: 1 }) } }).catch(() => {}); setTimeout(() => { try { xsReveal(v.sp, v.pr); } catch (e) {} }, 300); }),
  xsHatch: d => act(() => {""")
rep('bio: (S.bio || "").slice(0, 160), nm:', 'xs: xsPub(), /* v725 */ bio: (S.bio || "").slice(0, 160), nm:')
rep('bio: typeof v.bio === "string" ? v.bio.slice(0, 160) : "",', 'bio: typeof v.bio === "string" ? v.bio.slice(0, 160) : "", xs: xsPubClean(v.xs),')
rep('<div class="pstats"><div><b>${fmt(rec.w)}</b>', '${xsProfHTML(P, me)}<div class="pstats"><div><b>${fmt(rec.w)}</b>')
rep('bio: String(d.bio || "").slice(0, 300), titles:', 'bio: String(d.bio || "").slice(0, 300), xsg: xsgClean(d.xsg, members), titles:')
rep("try { serpDraw(ctx, b, scr, T, W, d, lo, t); } catch (e) {} /* v722 */", "try { serpDraw(ctx, b, scr, T, W, d, lo, t); } catch (e) {} /* v722 */ try { compBattle(ctx, b, scr, T, W, d, lo, t); } catch (e) {} /* v725 */")
rep("FLEET_FIN = null; FLEET_ARM = false; FLEET_SOLO = false; const tot", "FLEET_FIN = null; FLEET_ARM = false; FLEET_SOLO = false; if (!hostile && flag && !f.demo && !f.raid && fleetFlagU(f, false) === G.me) compMap(W, grp); /* v725 */ const tot")
rep("if (m) setTimeout(() => { try { sbSay(m[1]); } catch (e) {} }, 5500);", "if (m) setTimeout(() => { try { sbSay(m[1]); } catch (e) {} }, 5500); if (k0 < 12 && k1 >= 12) serpEgg(0); if (k0 < 30 && k1 >= 30) serpEgg(1); /* v725 */")
rep('const GAME_V = 724;', 'const GAME_V = 725;')
open(p, 'w', encoding='utf-8').write(s); print('ok')
